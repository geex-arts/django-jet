# encoding: utf-8
import datetime
import json
from django import forms
try:
    from django.core.urlresolvers import reverse
except ImportError: # Django 1.11
    from django.urls import reverse

from django.forms import Widget
from django.utils import formats
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from jet.dashboard.modules import DashboardModule
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.encoding import force_text

try:
    from urllib import request
    from urllib.parse import urlencode
    from urllib.error import URLError, HTTPError
except ImportError:
    import urllib2 as request
    from urllib2 import URLError, HTTPError
    from urllib import urlencode

JET_MODULE_YANDEX_METRIKA_CLIENT_ID = getattr(settings, 'JET_MODULE_YANDEX_METRIKA_CLIENT_ID', '')
JET_MODULE_YANDEX_METRIKA_CLIENT_SECRET = getattr(settings, 'JET_MODULE_YANDEX_METRIKA_CLIENT_SECRET', '')


class YandexMetrikaClient:
    OAUTH_BASE_URL = 'https://oauth.yandex.ru/'
    API_BASE_URL = 'https://api-metrika.yandex.ru/'
    CLIENT_ID = JET_MODULE_YANDEX_METRIKA_CLIENT_ID
    CLIENT_SECRET = JET_MODULE_YANDEX_METRIKA_CLIENT_SECRET

    def __init__(self, access_token=None):
        self.access_token = access_token

    def request(self, base_url, url, data=None, headers=None):
        url = '%s%s' % (base_url, url)

        if data is not None:
            data = urlencode(data).encode()

        if headers is None:
            headers = {}

        req = request.Request(url, data, headers)

        try:
            f = request.urlopen(req)
            result = f.read().decode('utf8')
            result = json.loads(result)
        except URLError as e:
            return None, e

        return result, None

    def get_oauth_authorize_url(self, state=''):
        return '%sauthorize' \
               '?response_type=code' \
               '&state=%s' \
               '&client_id=%s' % (self.OAUTH_BASE_URL, state, self.CLIENT_ID)

    def oauth_request(self, url, data=None):
        return self.request(self.OAUTH_BASE_URL, url, data)

    def oath_token_request(self, code):
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET
        }
        return self.oauth_request('token', data)

    def api_request(self, url, data=None):
        headers = None
        if self.access_token is not None:
            headers = {'Authorization': 'OAuth %s' % self.access_token}
        return self.request(self.API_BASE_URL, url, data, headers)

    def api_counters_request(self):
        return self.api_request('counters.json')

    def api_stat_traffic_summary(self, counter, date1, date2, group=None):
        if group is None:
            group = 'day'
        return self.api_request('stat/traffic/summary.json?id=%s&date1=%s&date2=%s&group=%s' % (
            counter,
            date1.strftime('%Y%m%d'),
            date2.strftime('%Y%m%d'),
            group
        ))


class AccessTokenWidget(Widget):
    module = None

    def render(self, name, value, attrs=None):
        if value and len(value) > 0:
            link = '<a href="%s">%s</a>' % (
                reverse('jet-dashboard:yandex-metrika-revoke', kwargs={'pk': self.module.model.pk}),
                force_text(_('Revoke access'))
            )
        else:
            link = '<a href="%s">%s</a>' % (
                reverse('jet-dashboard:yandex-metrika-grant', kwargs={'pk': self.module.model.pk}),
                force_text(_('Grant access'))
            )

        if value is None:
            value = ''

        return format_html('%s<input type="hidden" name="access_token" value="%s">' % (link, value))


class YandexMetrikaSettingsForm(forms.Form):
    access_token = forms.CharField(label=_('Access'), widget=AccessTokenWidget)
    counter = forms.ChoiceField(label=_('Counter'))
    period = forms.ChoiceField(label=_('Statistics period'), choices=(
        (0, _('Today')),
        (6, _('Last week')),
        (30, _('Last month')),
        (31 * 3 - 1, _('Last quarter')),
        (364, _('Last year')),
    ))

    def set_module(self, module):
        self.fields['access_token'].widget.module = module
        self.set_counter_choices(module)

    def set_counter_choices(self, module):
        counters = module.counters()
        if counters is not None:
            self.fields['counter'].choices = (('', '-- %s --' % force_text(_('none'))),)
            self.fields['counter'].choices.extend(map(lambda x: (x['id'], x['site']), counters))
        else:
            label = force_text(_('grant access first')) if module.access_token is None else force_text(_('counters loading failed'))
            self.fields['counter'].choices = (('', '-- %s -- ' % label),)


class YandexMetrikaChartSettingsForm(YandexMetrikaSettingsForm):
    show = forms.ChoiceField(label=_('Show'), choices=(
        ('visitors', capfirst(_('visitors'))),
        ('visits', capfirst(_('visits'))),
        ('page_views', capfirst(_('views'))),
    ))
    group = forms.ChoiceField(label=_('Group'), choices=(
        ('day', _('By day')),
        ('week', _('By week')),
        ('month', _('By month')),
    ))


class YandexMetrikaPeriodVisitorsSettingsForm(YandexMetrikaSettingsForm):
    group = forms.ChoiceField(label=_('Group'), choices=(
        ('day', _('By day')),
        ('week', _('By week')),
        ('month', _('By month')),
    ))


class YandexMetrikaBase(DashboardModule):
    settings_form = YandexMetrikaSettingsForm
    ajax_load = True
    contrast = True
    period = None
    access_token = None
    expires_in = None
    token_type = None
    counter = None
    error = None

    def settings_dict(self):
        return {
            'period': self.period,
            'access_token': self.access_token,
            'expires_in': self.expires_in,
            'token_type': self.token_type,
            'counter': self.counter
        }

    def load_settings(self, settings):
        try:
            self.period = int(settings.get('period'))
        except TypeError:
            self.period = 0
        self.access_token = settings.get('access_token')
        self.expires_in = settings.get('expires_in')
        self.token_type = settings.get('token_type')
        self.counter = settings.get('counter')

    def init_with_context(self, context):
        raise NotImplementedError('subclasses of YandexMetrika must provide a init_with_context() method')

    def counters(self):
        client = YandexMetrikaClient(self.access_token)
        counters, exception = client.api_counters_request()

        if counters is not None:
            return counters['counters']
        else:
            return None

    def format_grouped_date(self, date, group):
        if group == 'week':
            date = u'%s — %s' % (
                (date - datetime.timedelta(days=7)).strftime('%d.%m'),
                date.strftime('%d.%m')
            )
        elif group == 'month':
            date = date.strftime('%b, %Y')
        else:
            date = formats.date_format(date, 'DATE_FORMAT')
        return date

    def counter_attached(self):
        if self.access_token is None:
            self.error = mark_safe(_('Please <a href="%s">attach Yandex account and choose Yandex Metrika counter</a> to start using widget') % reverse('jet-dashboard:update_module', kwargs={'pk': self.model.pk}))
            return False
        elif self.counter is None:
            self.error = mark_safe(_('Please <a href="%s">select Yandex Metrika counter</a> to start using widget') % reverse('jet-dashboard:update_module', kwargs={'pk': self.model.pk}))
            return False
        else:
            return True

    def api_stat_traffic_summary(self, group=None):
        if self.counter_attached():
            date1 = datetime.datetime.now() - datetime.timedelta(days=self.period)
            date2 = datetime.datetime.now()

            client = YandexMetrikaClient(self.access_token)
            result, exception = client.api_stat_traffic_summary(self.counter, date1, date2, group)

            if exception is not None:
                error = _('API request failed.')
                if isinstance(exception, HTTPError) and exception.code == 403:
                    error += _(' Try to <a href="%s">revoke and grant access</a> again') % reverse('jet-dashboard:update_module', kwargs={'pk': self.model.pk})
                self.error = mark_safe(error)
            else:
                return result


class YandexMetrikaVisitorsTotals(YandexMetrikaBase):
    """
    Yandex Metrika widget that shows total number of visitors, visits and viewers for a particular period of time.
    Period may be following: Today, Last week, Last month, Last quarter, Last year
    """

    title = _('Yandex Metrika visitors totals')
    template = 'jet.dashboard/modules/yandex_metrika_visitors_totals.html'

    #: Which period should be displayed. Allowed values - integer of days
    period = None

    def __init__(self, title=None, period=None, **kwargs):
        kwargs.update({'period': period})
        super(YandexMetrikaVisitorsTotals, self).__init__(title, **kwargs)

    def init_with_context(self, context):
        result = self.api_stat_traffic_summary()

        if result is not None:
            try:
                self.children.append({'title': _('visitors'), 'value': result['totals']['visitors']})
                self.children.append({'title': _('visits'), 'value': result['totals']['visits']})
                self.children.append({'title': _('views'), 'value': result['totals']['page_views']})
            except KeyError:
                self.error = _('Bad server response')


class YandexMetrikaVisitorsChart(YandexMetrikaBase):
    """
    Yandex Metrika widget that shows visitors/visits/viewer chart for a particular period of time.
    Data is grouped by day, week or month
    Period may be following: Today, Last week, Last month, Last quarter, Last year
    """

    title = _('Yandex Metrika visitors chart')
    template = 'jet.dashboard/modules/yandex_metrika_visitors_chart.html'
    style = 'overflow-x: auto;'

    #: Which period should be displayed. Allowed values - integer of days
    period = None

    #: What data should be shown. Possible values: ``visitors``, ``visits``, ``page_views``
    show = None

    #: Sets grouping of data. Possible values: ``day``, ``week``, ``month``
    group = None
    settings_form = YandexMetrikaChartSettingsForm

    class Media:
        js = ('jet.dashboard/vendor/chart.js/Chart.min.js', 'jet.dashboard/dashboard_modules/yandex_metrika.js')

    def __init__(self, title=None, period=None, show=None, group=None, **kwargs):
        kwargs.update({'period': period, 'show': show, 'group': group})
        super(YandexMetrikaVisitorsChart, self).__init__(title, **kwargs)

    def settings_dict(self):
        settings = super(YandexMetrikaVisitorsChart, self).settings_dict()
        settings['show'] = self.show
        settings['group'] = self.group
        return settings

    def load_settings(self, settings):
        super(YandexMetrikaVisitorsChart, self).load_settings(settings)
        self.show = settings.get('show')
        self.group = settings.get('group')

    def init_with_context(self, context):
        result = self.api_stat_traffic_summary(self.group)

        if result is not None:
            try:
                for data in result['data']:
                    date = datetime.datetime.strptime(data['date'], '%Y%m%d')
                    key = self.show if self.show is not None else 'visitors'
                    self.children.append((date, data[key]))
            except KeyError:
                self.error = _('Bad server response')


class YandexMetrikaPeriodVisitors(YandexMetrikaBase):
    """
    Yandex Metrika widget that shows visitors, visits and viewers for a particular period of time.
    Data is grouped by day, week or month
    Period may be following: Today, Last week, Last month, Last quarter, Last year
    """

    title = _('Yandex Metrika period visitors')
    template = 'jet.dashboard/modules/yandex_metrika_period_visitors.html'

    #: Which period should be displayed. Allowed values - integer of days
    period = None

    #: Sets grouping of data. Possible values: ``day``, ``week``, ``month``
    group = None
    contrast = False
    settings_form = YandexMetrikaPeriodVisitorsSettingsForm

    def __init__(self, title=None, period=None, group=None, **kwargs):
        kwargs.update({'period': period, 'group': group})
        super(YandexMetrikaPeriodVisitors, self).__init__(title, **kwargs)

    def settings_dict(self):
        settings = super(YandexMetrikaPeriodVisitors, self).settings_dict()
        settings['group'] = self.group
        return settings

    def load_settings(self, settings):
        super(YandexMetrikaPeriodVisitors, self).load_settings(settings)
        self.group = settings.get('group')

    def init_with_context(self, context):
        result = self.api_stat_traffic_summary(self.group)

        if result is not None:
            try:
                for data in reversed(result['data']):
                    date = datetime.datetime.strptime(data['date'], '%Y%m%d')
                    date = self.format_grouped_date(date, self.group)
                    self.children.append((date, data))
            except KeyError:
                self.error = _('Bad server response')
