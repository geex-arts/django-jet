from importlib import import_module
try:
    from django.core.urlresolvers import reverse
except ImportError: # Django 1.11
    from django.urls import reverse

from django.template.loader import render_to_string
from jet.dashboard import modules
from jet.dashboard.models import UserDashboardModule
from django.utils.translation import ugettext_lazy as _
from jet.ordered_set import OrderedSet
from jet.utils import get_admin_site_name, context_to_dict

try:
    from django.template.context_processors import csrf
except ImportError:
    from django.core.context_processors import csrf


class Dashboard(object):
    """
    Base dashboard class. All custom dashboards should inherit it.
    """

    #: Number of columns in which widgets can be placed
    columns = 2

    #: Dashboard Modules (widgets) that dashboard is filled with, when the user open it for the first time
    #:
    #: List of dashboard module **instances**
    children = None

    #: Dashboard Modules (widgets) that user can add to dashboard at any time
    # (not created when the user open dashboard for the first time)
    #:
    #: List of dashboard module **classes**
    available_children = None
    app_label = None
    context = None
    modules = None

    class Media:
        css = ()
        js = ()

    def __init__(self, context, **kwargs):
        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])
        self.children = self.children or []
        self.available_children = self.available_children or []
        self.set_context(context)

    def set_context(self, context):
        self.context = context
        self.init_with_context(context)
        self.load_modules()

    def init_with_context(self, context):
        """
        Override this method to fill your custom **Dashboard** class with widgets.
        You should add your widgets to ``children`` and ``available_children`` attributes.

        Usage example:

        .. code-block:: python

            from django.utils.translation import ugettext_lazy as _
            from jet.dashboard import modules
            from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


            class CustomIndexDashboard(Dashboard):
                columns = 3

                def init_with_context(self, context):
                    self.available_children.append(modules.LinkList)
                    self.children.append(modules.LinkList(
                        _('Support'),
                        children=[
                            {
                                'title': _('Django documentation'),
                                'url': 'http://docs.djangoproject.com/',
                                'external': True,
                            },
                            {
                                'title': _('Django "django-users" mailing list'),
                                'url': 'http://groups.google.com/group/django-users',
                                'external': True,
                            },
                            {
                                'title': _('Django irc channel'),
                                'url': 'irc://irc.freenode.net/django',
                                'external': True,
                            },
                        ],
                        column=0,
                        order=0
                    ))

        """
        pass

    def load_module(self, module_fullname):
        package, module_name = module_fullname.rsplit('.', 1)
        package = import_module(package)
        module = getattr(package, module_name)

        return module

    def create_initial_module_models(self, user):
        module_models = []

        i = 0

        for module in self.children:
            column = module.column if module.column is not None else i % self.columns
            order = module.order if module.order is not None else int(i / self.columns)

            module_models.append(UserDashboardModule.objects.create(
                title=module.title,
                app_label=self.app_label,
                user=user.pk,
                module=module.fullname(),
                column=column,
                order=order,
                settings=module.dump_settings(),
                children=module.dump_children()
            ))
            i += 1

        return module_models

    def load_modules(self):
        module_models = UserDashboardModule.objects.filter(
            app_label=self.app_label,
            user=self.context['request'].user.pk
        ).all()

        if len(module_models) == 0:
            module_models = self.create_initial_module_models(self.context['request'].user)

        loaded_modules = []

        for module_model in module_models:
            module_cls = module_model.load_module()
            if module_cls is not None:
                module = module_cls(model=module_model, context=self.context)
                loaded_modules.append(module)

        self.modules = loaded_modules

    def render(self):
        context = context_to_dict(self.context)
        context.update({
            'columns': range(self.columns),
            'modules': self.modules,
            'app_label': self.app_label,
        })
        context.update(csrf(context['request']))

        return render_to_string('jet.dashboard/dashboard.html', context)

    def render_tools(self):
        context = context_to_dict(self.context)
        context.update({
            'children': self.children,
            'app_label': self.app_label,
            'available_children': self.available_children
        })
        context.update(csrf(context['request']))

        return render_to_string('jet.dashboard/dashboard_tools.html', context)

    def media(self):
        unique_css = OrderedSet()
        unique_js = OrderedSet()

        for js in getattr(self.Media, 'js', ()):
            unique_js.add(js)
        for css in getattr(self.Media, 'css', ()):
            unique_css.add(css)

        for module in self.modules:
            for js in getattr(module.Media, 'js', ()):
                unique_js.add(js)
            for css in getattr(module.Media, 'css', ()):
                unique_css.add(css)

        class Media:
            css = list(unique_css)
            js = list(unique_js)

        return Media


class AppIndexDashboard(Dashboard):
    def get_app_content_types(self):
        return self.app_label + '.*',

    def models(self):
        return self.app_label + '.*',


class DefaultIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.available_children.append(modules.Feed)

        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ],
            column=0,
            order=0
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('auth.*',),
            column=1,
            order=0
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('auth.*',),
            column=2,
            order=0
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            10,
            column=0,
            order=1
        ))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5,
            column=1,
            order=1
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ],
            column=2,
            order=1
        ))


class DefaultAppIndexDashboard(AppIndexDashboard):
    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)

        self.children.append(modules.ModelList(
            title=_('Application models'),
            models=self.models(),
            column=0,
            order=0
        ))
        self.children.append(modules.RecentActions(
            include_list=self.get_app_content_types(),
            column=1,
            order=0
        ))


class DashboardUrls(object):
    _urls = []

    def get_urls(self):
        return self._urls

    def register_url(self, url):
        self._urls.append(url)

    def register_urls(self, urls):
        self._urls.extend(urls)

urls = DashboardUrls()
