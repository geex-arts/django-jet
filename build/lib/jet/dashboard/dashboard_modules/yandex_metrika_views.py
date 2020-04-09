from django.conf.urls import url
from django.contrib import messages
try:
    from django.core.urlresolvers import reverse
except ImportError: # Django 1.11
    from django.urls import reverse

from django.http import HttpResponse
from django.shortcuts import redirect
from jet.dashboard.dashboard_modules.yandex_metrika import YandexMetrikaClient
from jet.dashboard.models import UserDashboardModule
from jet.dashboard import dashboard
from django.utils.translation import ugettext_lazy as _


def yandex_metrika_grant_view(request, pk):
    client = YandexMetrikaClient()
    return redirect(client.get_oauth_authorize_url(pk))


def yandex_metrika_revoke_view(request, pk):
    try:
        module = UserDashboardModule.objects.get(pk=pk)
        module.pop_settings(('access_token', 'expires_in', 'token_type', 'counter'))
        return redirect(reverse('jet-dashboard:update_module', kwargs={'pk': module.pk}))
    except UserDashboardModule.DoesNotExist:
        return HttpResponse(_('Module not found'))


def yandex_metrika_callback_view(request):
    try:
        state = request.GET['state']
        code = request.GET['code']

        module = UserDashboardModule.objects.get(pk=state)

        client = YandexMetrikaClient()
        result, exception = client.oath_token_request(code)

        if result is None:
            messages.error(request, _('API request failed.'))
        else:
            module.update_settings(result)

        return redirect(reverse('jet-dashboard:update_module', kwargs={'pk': module.pk}))
    except KeyError:
        return HttpResponse(_('Bad arguments'))
    except UserDashboardModule.DoesNotExist:
        return HttpResponse(_('Module not found'))


dashboard.urls.register_urls([
    url(
        r'^yandex-metrika/grant/(?P<pk>\d+)/$',
        yandex_metrika_grant_view,
        name='yandex-metrika-grant'
    ),
    url(
        r'^yandex-metrika/revoke/(?P<pk>\d+)/$',
        yandex_metrika_revoke_view,
        name='yandex-metrika-revoke'
    ),
    url(
        r'^yandex-metrika/callback/$',
        yandex_metrika_callback_view,
        name='yandex-metrika-callback'
    ),
])
