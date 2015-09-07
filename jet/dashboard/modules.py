import json
from django import forms
from django.contrib.admin.models import LogEntry
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from jet.utils import get_app_list, LazyDateTimeEncoder
import datetime


class DashboardModule(object):
    template = 'jet.dashboard/module.html'
    enabled = True
    draggable = True
    collapsible = True
    deletable = True
    show_title = True
    title = ''
    title_url = None
    css_classes = None
    pre_content = None
    post_content = None
    children = None
    settings_form = None
    child_form = None
    child_name = None
    child_name_plural = None
    settings = None
    column = None
    order = None
    ajax_load = False
    contrast = False
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
        pass

    def load_children(self, children):
        self.children = children

    def store_children(self):
        return False

    def settings_dict(self):
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
        pass

    def get_context_data(self):
        context = self.context
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
    title = _('Links')
    template = 'jet.dashboard/modules/link_list.html'
    layout = 'stacked'
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
            'layout': self.layout
        }

    def load_settings(self, settings):
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
    title = _('Applications')
    template = 'jet.dashboard/modules/app_list.html'
    models = None
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
            app['models'] = filter(
                lambda model: self.models is None or model['object_name'] in self.models or app.get('app_label', app.get('name')) + '.*' in self.models,
                app['models']
            )
            app['models'] = filter(
                lambda model: self.exclude is None or model['object_name'] not in self.exclude and app.get('app_label', app.get('name')) + '.*' not in self.exclude,
                app['models']
            )
            app['models'] = list(app['models'])

            if self.hide_empty and len(list(app['models'])) == 0:
                app_to_remove.append(app)

        for app in app_to_remove:
            app_list.remove(app)

        self.children = app_list


class ModelList(DashboardModule):
    title = _('Models')
    template = 'jet.dashboard/modules/model_list.html'
    models = None
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
            app['models'] = filter(
                lambda model: self.models is None or model['object_name'] in self.models or app.get('app_label', app.get('name')) + '.*' in self.models,
                app['models']
            )
            app['models'] = filter(
                lambda model: self.exclude is None or model['object_name'] not in self.exclude and app.get('app_label', app.get('name')) + '.*' not in self.exclude,
                app['models']
            )
            app['models'] = list(app['models'])

            models.extend(app['models'])

        self.children = models


class RecentActionsSettingsForm(forms.Form):
    limit = forms.IntegerField(label=_('Items limit'), min_value=1)


class RecentActions(DashboardModule):
    title = _('Recent Actions')
    template = 'jet.dashboard/modules/recent_actions.html'
    limit = 10
    include_list = None
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
    title = _('RSS Feed')
    template = 'jet.dashboard/modules/feed.html'
    feed_url = None
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

