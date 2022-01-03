import json
from django import forms
from django.contrib.admin.models import LogEntry
from django.db.models import Q
from django.template.loader import render_to_string
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError: # Django 4 (tested with Django 4.0)
    from django.utils.translation import gettext_lazy as _
from jet.utils import get_app_list, LazyDateTimeEncoder, context_to_dict
import datetime


class DashboardModule(object):
    """
    Base dashboard module class. All dashboard modules (widgets) should inherit it.
    """

    #: Path to widget's template. There is no need to extend such templates from any base templates.
    template = 'jet.dashboard/module.html'
    enabled = True

    #: Specify if module can be draggable or has static position.
    draggable = True

    #: Specify if module can be collapsed.
    collapsible = True

    #: Specify if module can be deleted.
    deletable = True
    show_title = True

    #: Default widget title that will be displayed for widget in the dashboard. User can change it later
    #: for every widget.
    title = ''

    #: Specify title url. ``None`` if title shouldn't be clickable.
    title_url = None
    css_classes = None

    #: HTML content that will be displayed before widget content.
    pre_content = None

    #: HTML content that will be displayed after widget content.
    post_content = None
    children = None

    #: A ``django.forms.Form`` class which may contain custom widget settings. Not required.
    settings_form = None

    #: A ``django.forms.Form`` class which may contain custom widget child settings, if it has any. Not required.
    child_form = None

    #: Child name that will be displayed when editing module contents. Required if ``child_form`` set.
    child_name = None

    #: Same as child name, but plural.
    child_name_plural = None
    settings = None
    column = None
    order = None

    #: A boolean field which specify if widget should be rendered on dashboard page load or fetched
    #: later via AJAX.
    ajax_load = False

    #: A boolean field which makes widget ui color contrast.
    contrast = False

    #: Optional style attributes which will be applied to widget content container.
    style = False

    class Media:
        css = ()
        js = ()

    def __init__(self, title=None, model=None, context=None, **kwargs):
        if title is not None:
            self.title = title
        self.model = model
        self.context = context or {}

        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])

        self.children = self.children or []

        if self.model:
            self.load_from_model()

    def fullname(self):
        return self.__module__ + "." + self.__class__.__name__

    def load_settings(self, settings):
        """
        Should be implemented to restore saved in database settings. Required if you have custom settings.
        """
        pass

    def load_children(self, children):
        self.children = children

    def store_children(self):
        """
        Specify if children field should be saved to database.
        """
        return False

    def settings_dict(self):
        """
        Should be implemented to save settings to database. This method should return ``dict`` which will be serialized
        using ``json``. Required if you have custom settings.
        """
        pass

    def dump_settings(self, settings=None):
        settings = settings or self.settings_dict()
        if settings:
            return json.dumps(settings, cls=LazyDateTimeEncoder)
        else:
            return ''

    def dump_children(self):
        if self.store_children():
            return json.dumps(self.children, cls=LazyDateTimeEncoder)
        else:
            return ''

    def load_from_model(self):
        self.title = self.model.title

        if self.model.settings:
            try:
                self.settings = json.loads(self.model.settings)
                self.load_settings(self.settings)
            except ValueError:
                pass

        if self.store_children() and self.model.children:
            try:
                children = json.loads(self.model.children)
                self.load_children(children)
            except ValueError:
                pass

    def init_with_context(self, context):
        """
        Allows you to load data and initialize module's state.
        """
        pass

    def get_context_data(self):
        context = context_to_dict(self.context)
        context.update({
            'module': self
        })
        return context

    def render(self):
        self.init_with_context(self.context)
        return render_to_string(self.template, self.get_context_data())


class LinkListItemForm(forms.Form):
    url = forms.CharField(label=_('URL'))
    title = forms.CharField(label=_('Title'))
    external = forms.BooleanField(label=_('External link'), required=False)


class LinkListSettingsForm(forms.Form):
    layout = forms.ChoiceField(label=_('Layout'), choices=(('stacked', _('Stacked')), ('inline', _('Inline'))))


class LinkList(DashboardModule):
    """
    List of links widget.

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

    title = _('Links')
    template = 'jet.dashboard/modules/link_list.html'

    #: Specify widget layout.
    #: Allowed values ``stacked`` and ``inline``.
    layout = 'stacked'

    #: Links are contained in ``children`` attribute which you can pass as constructor parameter
    #: to make your own preinstalled link lists.
    #:
    #: ``children`` is an array of dictinaries::
    #:
    #:     [
    #:          {
    #:              'title': _('Django documentation'),
    #:              'url': 'http://docs.djangoproject.com/',
    #:              'external': True,
    #:          },
    #:          ...
    #:     ]
    children = []
    settings_form = LinkListSettingsForm
    child_form = LinkListItemForm
    child_name = _('Link')
    child_name_plural = _('Links')

    def __init__(self, title=None, children=list(), **kwargs):
        children = list(map(self.parse_link, children))
        kwargs.update({'children': children})
        super(LinkList, self).__init__(title, **kwargs)

    def settings_dict(self):
        return {
            'draggable': self.draggable,
            'deletable': self.deletable,
            'collapsible': self.collapsible,
            'layout': self.layout
        }

    def load_settings(self, settings):
        self.draggable = settings.get('draggable', self.draggable)
        self.deletable = settings.get('deletable', self.deletable)
        self.collapsible = settings.get('collapsible', self.collapsible)
        self.layout = settings.get('layout', self.layout)

    def store_children(self):
        return True

    def parse_link(self, link):
        if isinstance(link, (tuple, list)):
            link_dict = {'title': link[0], 'url': link[1]}
            if len(link) >= 3:
                link_dict['external'] = link[2]
            return link_dict
        elif isinstance(link, (dict,)):
            return link


class AppList(DashboardModule):
    """
    Shows applications and containing models links. For each model "created" and "change" links are displayed.

    Usage example:

    .. code-block:: python

        from django.utils.translation import ugettext_lazy as _
        from jet.dashboard import modules
        from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


        class CustomIndexDashboard(Dashboard):
            columns = 3

            def init_with_context(self, context):
                self.children.append(modules.AppList(
                    _('Applications'),
                    exclude=('auth.*',),
                    column=0,
                    order=0
                ))

    """

    title = _('Applications')
    template = 'jet.dashboard/modules/app_list.html'

    #: Specify models which should be displayed. ``models`` is an array of string formatted as ``app_label.model``.
    #: Also its possible to specify all application models with * sign (e.g. ``auth.*``).
    models = None

    #: Specify models which should NOT be displayed. ``exclude`` is an array of string formatted as ``app_label.model``.
    #: Also its possible to specify all application models with * sign (e.g. ``auth.*``).
    exclude = None
    hide_empty = True

    def settings_dict(self):
        return {
            'models': self.models,
            'exclude': self.exclude
        }

    def load_settings(self, settings):
        self.models = settings.get('models')
        self.exclude = settings.get('exclude')

    def init_with_context(self, context):
        app_list = get_app_list(context)
        app_to_remove = []

        for app in app_list:
            app_name = app.get('app_label', app.get('name', ''))
            app['models'] = filter(
                lambda model: self.models is None or ('%s.%s' % (app_name, model['object_name'])) in self.models or ('%s.*' % app_name) in self.models,
                app['models']
            )
            app['models'] = filter(
                lambda model: self.exclude is None or (('%s.%s' % (app_name, model['object_name'])) not in self.exclude and ('%s.*' % app_name) not in self.exclude),
                app['models']
            )
            app['models'] = list(app['models'])

            if self.hide_empty and len(list(app['models'])) == 0:
                app_to_remove.append(app)

        for app in app_to_remove:
            app_list.remove(app)

        self.children = app_list


class ModelList(DashboardModule):
    """
    Shows models links. For each model "created" and "change" links are displayed.

    Usage example:

    .. code-block:: python

        from django.utils.translation import ugettext_lazy as _
        from jet.dashboard import modules
        from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


        class CustomIndexDashboard(Dashboard):
            columns = 3

            def init_with_context(self, context):
                self.children.append(modules.ModelList(
                    _('Models'),
                    exclude=('auth.*',),
                    column=0,
                    order=0
                ))

    """

    title = _('Models')
    template = 'jet.dashboard/modules/model_list.html'

    #: Specify models which should be displayed. ``models`` is an array of string formatted as ``app_label.model``.
    #: Also its possible to specify all application models with * sign (e.g. ``auth.*``).
    models = None

    #: Specify models which should NOT be displayed. ``exclude`` is an array of string formatted as ``app_label.model``.
    #: Also its possible to specify all application models with * sign (e.g. ``auth.*``).
    exclude = None
    hide_empty = True

    def settings_dict(self):
        return {
            'models': self.models,
            'exclude': self.exclude
        }

    def load_settings(self, settings):
        self.models = settings.get('models')
        self.exclude = settings.get('exclude')

    def init_with_context(self, context):
        app_list = get_app_list(context)
        models = []

        for app in app_list:
            app_name = app.get('app_label', app.get('name', ''))
            app['models'] = filter(
                lambda model: self.models is None or ('%s.%s' % (app_name, model['object_name'])) in self.models or ('%s.*' % app_name) in self.models,
                app['models']
            )
            app['models'] = filter(
                lambda model: self.exclude is None or (('%s.%s' % (app_name, model['object_name'])) not in self.exclude and ('%s.*' % app_name) not in self.exclude),
                app['models']
            )
            app['models'] = list(app['models'])

            models.extend(app['models'])

        self.children = models


class RecentActionsSettingsForm(forms.Form):
    limit = forms.IntegerField(label=_('Items limit'), min_value=1)


class RecentActions(DashboardModule):
    """
    Display list of most recent admin actions with following information:
    entity name, type of action, author, date

    Usage example:

    .. code-block:: python

        from django.utils.translation import ugettext_lazy as _
        from jet.dashboard import modules
        from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


        class CustomIndexDashboard(Dashboard):
            columns = 3

            def init_with_context(self, context):
                self.children.append(modules.RecentActions(
                    _('Recent Actions'),
                    10,
                    column=0,
                    order=0
                ))

    """

    title = _('Recent Actions')
    template = 'jet.dashboard/modules/recent_actions.html'

    #: Number if entries to be shown (may be changed by each user personally).
    limit = 10

    #: Specify actions of which models should be displayed. ``include_list`` is an array of string
    #: formatted as ``app_label.model``. Also its possible to specify all application models
    #: with * sign (e.g. ``auth.*``).
    include_list = None

    #: Specify actions of which models should NOT be displayed. ``exclude_list`` is an array of string
    #: formatted as ``app_label.model``. Also its possible to specify all application models
    #: with * sign (e.g. ``auth.*``).
    exclude_list = None
    settings_form = RecentActionsSettingsForm
    user = None

    def __init__(self, title=None, limit=10, **kwargs):
        kwargs.update({'limit': limit})
        super(RecentActions, self).__init__(title, **kwargs)

    def settings_dict(self):
        return {
            'limit': self.limit,
            'include_list': self.include_list,
            'exclude_list': self.exclude_list,
            'user': self.user
        }

    def load_settings(self, settings):
        self.limit = settings.get('limit', self.limit)
        self.include_list = settings.get('include_list')
        self.exclude_list = settings.get('exclude_list')
        self.user = settings.get('user', None)

    def init_with_context(self, context):
        def get_qset(list):
            qset = None
            for contenttype in list:
                try:
                    app_label, model = contenttype.split('.')

                    if model == '*':
                        current_qset = Q(
                            content_type__app_label=app_label
                        )
                    else:
                        current_qset = Q(
                            content_type__app_label=app_label,
                            content_type__model=model
                        )
                except:
                    raise ValueError('Invalid contenttype: "%s"' % contenttype)

                if qset is None:
                    qset = current_qset
                else:
                    qset = qset | current_qset
            return qset

        qs = LogEntry.objects

        if self.user:
            qs = qs.filter(
                user__pk=int(self.user)
            )

        if self.include_list:
            qs = qs.filter(get_qset(self.include_list))
        if self.exclude_list:
            qs = qs.exclude(get_qset(self.exclude_list))

        self.children = qs.select_related('content_type', 'user')[:int(self.limit)]


class FeedSettingsForm(forms.Form):
    limit = forms.IntegerField(label=_('Items limit'), min_value=1)
    feed_url = forms.URLField(label=_('Feed URL'))


class Feed(DashboardModule):
    """
    Display RSS Feed entries with following information:
    entry title, date and link to the full version

    Usage example:

    .. code-block:: python

        from django.utils.translation import ugettext_lazy as _
        from jet.dashboard import modules
        from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


        class CustomIndexDashboard(Dashboard):
            columns = 3

            def init_with_context(self, context):
                self.children.append(modules.Feed(
                    _('Latest Django News'),
                    feed_url='http://www.djangoproject.com/rss/weblog/',
                    limit=5,
                    column=0,
                    order=0
                ))

    """

    title = _('RSS Feed')
    template = 'jet.dashboard/modules/feed.html'

    #: URL of the RSS feed (may be changed by each user personally).
    feed_url = None

    #: Number if entries to be shown (may be changed by each user personally).
    limit = None
    settings_form = FeedSettingsForm
    ajax_load = True

    def __init__(self, title=None, feed_url=None, limit=None, **kwargs):
        kwargs.update({'feed_url': feed_url, 'limit': limit})
        super(Feed, self).__init__(title, **kwargs)

    def settings_dict(self):
        return {
            'feed_url': self.feed_url,
            'limit': self.limit
        }

    def load_settings(self, settings):
        self.feed_url = settings.get('feed_url')
        self.limit = settings.get('limit')

    def init_with_context(self, context):
        if self.feed_url is not None:
            try:
                import feedparser

                feed = feedparser.parse(self.feed_url)

                if self.limit is not None:
                    entries = feed['entries'][:self.limit]
                else:
                    entries = feed['entries']

                for entry in entries:
                    try:
                        entry.date = datetime.date(*entry.published_parsed[0:3])
                    except:
                        pass

                    self.children.append(entry)
            except ImportError:
                self.children.append({
                    'title': _('You must install the FeedParser python module'),
                    'warning': True,
                })
        else:
            self.children.append({
                'title': _('You must provide a valid feed URL'),
                'warning': True,
            })

