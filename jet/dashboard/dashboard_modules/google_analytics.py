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
from googleapiclient.discovery import build
import httplib2
from jet.dashboard.modules import DashboardModule
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials, AccessTokenRefreshError, Storage
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.encoding import force_text

try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode

try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt

JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE = getattr(
    settings,
    'JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE',
    ''
)


class ModuleCredentialStorage(Storage):
    def __init__(self, module):
        super(ModuleCredentialStorage, self).__init__()
        self.module = module

    def locked_get(self):
        pass

    def locked_put(self, credentials):
        pass

    def locked_delete(self):
        pass

    def get(self):
        try:
            settings = json.loads(self.module.settings)
            credential = settings['credential']
            return OAuth2Credentials.from_json(credential)
        except (ValueError, KeyError):
            return None

    def put(self, credentials):
        self.module.update_settings({'credential': credentials.to_json()})

    def delete(self):
        self.module.pop_settings(('credential',))


class GoogleAnalyticsClient:
    credential = None
    analytics_service = None

    def __init__(self, storage=None, redirect_uri=None):
        self.FLOW = flow_from_clientsecrets(
            JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE,
            scope='https://www.googleapis.com/auth/analytics.readonly',
            redirect_uri=redirect_uri,
            prompt='consent'
        )

        if storage is not None:
            credential = storage.get()
            credential.set_store(storage)
            self.set_credential(credential)

    def get_oauth_authorize_url(self, state=''):
        self.FLOW.params['state'] = state
        authorize_url = self.FLOW.step1_get_authorize_url()
        return authorize_url

    def set_credential(self, credential):
        self.credential = credential
        self.set_analytics_service(self.credential)

    def set_credential_from_request(self, request):
        self.set_credential(self.FLOW.step2_exchange(request.GET))

    def set_analytics_service(self, credential):
        http = httplib2.Http()
        http = credential.authorize(http)
        self.analytics_service = build('analytics', 'v3', http=http)

    def api_profiles(self):
        if self.analytics_service is None:
            return None, None

        try:
            profiles = self.analytics_service.management().profiles().list(
                accountId='~all',
                webPropertyId='~all'
            ).execute()

            return profiles['items'], None
        except (TypeError, KeyError) as e:
            return None, e

    def api_ga(self, profile_id, date1, date2, group=None):
        if self.analytics_service is None:
            return None, None

        if group == 'day':
            dimensions = 'ga:date'
        elif group == 'week':
            dimensions = 'ga:year,ga:week'
        elif group == 'month':
            dimensions = 'ga:year,ga:month'
        else:
            dimensions = ''

        try:
            data = self.analytics_service.data().ga().get(
                ids='ga:' + profile_id,
                start_date=date1.strftime('%Y-%m-%d'),
                end_date=date2.strftime('%Y-%m-%d'),
                metrics='ga:users,ga:sessions,ga:pageviews',
                dimensions=dimensions
            ).execute()

            return data, None
        except TypeError as e:
            return None, e


class CredentialWidget(Widget):
    module = None

    def render(self, name, value, attrs=None):
        if value and len(value) > 0:
            link = '<a href="%s">%s</a>' % (
                reverse('jet-dashboard:google-analytics-revoke', kwargs={'pk': self.module.model.pk}),
                force_text(_('Revoke access'))
            )
        else:
            link = '<a href="%s">%s</a>' % (
                reverse('jet-dashboard:google-analytics-grant', kwargs={'pk': self.module.model.pk}),
                force_text(_('Grant access'))
            )

        attrs = self.build_attrs({
            'type': 'hidden',
            'name': 'credential',
        })
        attrs['value'] = force_unicode(value) if value else ''

        return format_html('%s<input{} />' % link, flatatt(attrs))


class GoogleAnalyticsSettingsForm(forms.Form):
    credential = forms.CharField(label=_('Access'), widget=CredentialWidget)
    counter = forms.ChoiceField(label=_('Counter'))
    period = forms.ChoiceField(label=_('Statistics period'), choices=(
        (0, _('Today')),
        (6, _('Last week')),
        (30, _('Last month')),
        (31 * 3 - 1, _('Last quarter')),
        (364, _('Last year')),
    ))

    def set_module(self, module):
        self.fields['credential'].widget.module = module
        self.set_counter_choices(module)

    def set_counter_choices(self, module):
        counters = module.counters()
        if counters is not None:
            self.fields['counter'].choices = (('', '-- %s --' % force_text(_('none'))),)
            self.fields['counter'].choices.extend(map(lambda x: (x['id'], x['websiteUrl']), counters))
        else:
            label = force_text(_('grant access first')) if module.credential is None else force_text(_('counters loading failed'))
            self.fields['counter'].choices = (('', '-- %s -- ' % label),)


class GoogleAnalyticsChartSettingsForm(GoogleAnalyticsSettingsForm):
    show = forms.ChoiceField(label=_('Show'), choices=(
        ('ga:users', capfirst(_('users'))),
        ('ga:sessions', capfirst(_('sessions'))),
        ('ga:pageviews', capfirst(_('views'))),
    ))
    group = forms.ChoiceField(label=_('Group'), choices=(
        ('day', _('By day')),
        ('week', _('By week')),
        ('month', _('By month')),
    ))


class GoogleAnalyticsPeriodVisitorsSettingsForm(GoogleAnalyticsSettingsForm):
    group = forms.ChoiceField(label=_('Group'), choices=(
        ('day', _('By day')),
        ('week', _('By week')),
        ('month', _('By month')),
    ))


class GoogleAnalyticsBase(DashboardModule):
    settings_form = GoogleAnalyticsSettingsForm
    ajax_load = True
    contrast = True
    period = None
    credential = None
    counter = None
    error = None
    storage = None

    def __init__(self, title=None, period=None, **kwargs):
        kwargs.update({'period': period})
        super(GoogleAnalyticsBase, self).__init__(title, **kwargs)

    def settings_dict(self):
        return {
            'period': self.period,
            'credential': self.credential,
            'counter': self.counter
        }

    def load_settings(self, settings):
        try:
            self.period = int(settings.get('period'))
        except TypeError:
            self.period = 0
        self.credential = settings.get('credential')
        self.storage = ModuleCredentialStorage(self.model)
        self.counter = settings.get('counter')

    def init_with_context(self, context):
        raise NotImplementedError('subclasses of GoogleAnalytics must provide a init_with_context() method')

    def counters(self):
        try:
            client = GoogleAnalyticsClient(self.storage)
            profiles, exception = client.api_profiles()
            return profiles
        except Exception:
            return None

    def get_grouped_date(self, data, group):
        if group == 'week':
            date = datetime.datetime.strptime(
                '%s-%s-%s' % (data['ga_year'], data['ga_week'], '0'),
                '%Y-%W-%w'
            )
        elif group == 'month':
            date = datetime.datetime.strptime(data['ga_year'] + data['ga_month'], '%Y%m')
        else:
            date = datetime.datetime.strptime(data['ga_date'], '%Y%m%d')
        return date

    def format_grouped_date(self, data, group):
        date = self.get_grouped_date(data, group)

        if group == 'week':
            date = u'%s — %s' % (
                (date - datetime.timedelta(days=6)).strftime('%d.%m'),
                date.strftime('%d.%m')
            )
        elif group == 'month':
            date = date.strftime('%b, %Y')
        else:
            date = formats.date_format(date, 'DATE_FORMAT')
        return date

    def counter_attached(self):
        if self.credential is None:
            self.error = mark_safe(_('Please <a href="%s">attach Google account and choose Google Analytics counter</a> to start using widget') % reverse('jet-dashboard:update_module', kwargs={'pk': self.model.pk}))
            return False
        elif self.counter is None:
            self.error = mark_safe(_('Please <a href="%s">select Google Analytics counter</a> to start using widget') % reverse('jet-dashboard:update_module', kwargs={'pk': self.model.pk}))
            return False
        else:
            return True

    def api_ga(self, group=None):
        if self.counter_attached():
            date1 = datetime.datetime.now() - datetime.timedelta(days=self.period)
            date2 = datetime.datetime.now()

            try:
                client = GoogleAnalyticsClient(self.storage)
                result, exception = client.api_ga(self.counter, date1, date2, group)

                if exception is not None:
                        raise exception

                return result
            except Exception as e:
                error = _('API request failed.')
                if isinstance(e, AccessTokenRefreshError):
                    error += _(' Try to <a href="%s">revoke and grant access</a> again') % reverse('jet-dashboard:update_module', kwargs={'pk': self.model.pk})
                self.error = mark_safe(error)


class GoogleAnalyticsVisitorsTotals(GoogleAnalyticsBase):
    """
    Google Analytics widget that shows total number of users, sessions and viewers for a particular period of time.
    Period may be following: Today, Last week, Last month, Last quarter, Last year
    """

    title = _('Google Analytics visitors totals')
    template = 'jet.dashboard/modules/google_analytics_visitors_totals.html'

    #: Which period should be displayed. Allowed values - integer of days
    period = None

    def __init__(self, title=None, period=None, **kwargs):
        kwargs.update({'period': period})
        super(GoogleAnalyticsVisitorsTotals, self).__init__(title, **kwargs)

    def init_with_context(self, context):
        result = self.api_ga()

        if result is not None:
            try:
                self.children.append({'title': _('users'), 'value': result['totalsForAllResults']['ga:users']})
                self.children.append({'title': _('sessions'), 'value': result['totalsForAllResults']['ga:sessions']})
                self.children.append({'title': _('views'), 'value': result['totalsForAllResults']['ga:pageviews']})
            except KeyError:
                self.error = _('Bad server response')


class GoogleAnalyticsVisitorsChart(GoogleAnalyticsBase):
    """
    Google Analytics widget that shows users/sessions/viewer chart for a particular period of time.
    Data is grouped by day, week or month
    Period may be following: Today, Last week, Last month, Last quarter, Last year
    """

    title = _('Google Analytics visitors chart')
    template = 'jet.dashboard/modules/google_analytics_visitors_chart.html'
    style = 'overflow-x: auto;'

    #: Which period should be displayed. Allowed values - integer of days
    period = None

    #: What data should be shown. Possible values: ``ga:users``, ``ga:sessions``, ``ga:pageviews``
    show = None

    #: Sets grouping of data. Possible values: ``day``, ``week``, ``month``
    group = None
    settings_form = GoogleAnalyticsChartSettingsForm

    class Media:
        js = ('jet.dashboard/vendor/chart.js/Chart.min.js', 'jet.dashboard/dashboard_modules/google_analytics.js')

    def __init__(self, title=None, period=None, show=None, group=None, **kwargs):
        kwargs.update({'period': period, 'show': show, 'group': group})
        super(GoogleAnalyticsVisitorsChart, self).__init__(title, **kwargs)

    def settings_dict(self):
        settings = super(GoogleAnalyticsVisitorsChart, self).settings_dict()
        settings['show'] = self.show
        settings['group'] = self.group
        return settings

    def load_settings(self, settings):
        super(GoogleAnalyticsVisitorsChart, self).load_settings(settings)
        self.show = settings.get('show')
        self.group = settings.get('group')

    def init_with_context(self, context):
        result = self.api_ga(self.group)

        if result is not None:
            try:
                for data in result['rows']:
                    row_data = {}

                    i = 0
                    for column in result['columnHeaders']:
                        row_data[column['name'].replace(':', '_')] = data[i]
                        i += 1

                    date = self.get_grouped_date(row_data, self.group)
                    self.children.append((date, row_data[self.show.replace(':', '_')]))
            except KeyError:
                self.error = _('Bad server response')


class GoogleAnalyticsPeriodVisitors(GoogleAnalyticsBase):
    """
    Google Analytics widget that shows users, sessions and viewers for a particular period of time.
    Data is grouped by day, week or month
    Period may be following: Today, Last week, Last month, Last quarter, Last year
    """

    title = _('Google Analytics period visitors')
    template = 'jet.dashboard/modules/google_analytics_period_visitors.html'

    #: Which period should be displayed. Allowed values - integer of days
    period = None

    #: Sets grouping of data. Possible values: ``day``, ``week``, ``month``
    group = None
    contrast = False
    settings_form = GoogleAnalyticsPeriodVisitorsSettingsForm

    def __init__(self, title=None, period=None, group=None, **kwargs):
        kwargs.update({'period': period, 'group': group})
        super(GoogleAnalyticsPeriodVisitors, self).__init__(title, **kwargs)

    def settings_dict(self):
        settings = super(GoogleAnalyticsPeriodVisitors, self).settings_dict()
        settings['group'] = self.group
        return settings

    def load_settings(self, settings):
        super(GoogleAnalyticsPeriodVisitors, self).load_settings(settings)
        self.group = settings.get('group')

    def init_with_context(self, context):
        result = self.api_ga(self.group)

        if result is not None:
            try:
                for data in reversed(result['rows']):
                    row_data = {}

                    i = 0
                    for column in result['columnHeaders']:
                        row_data[column['name'].replace(':', '_')] = data[i]
                        i += 1

                    date = self.format_grouped_date(row_data, self.group)
                    self.children.append((date, row_data))
            except KeyError:
                self.error = _('Bad server response')
