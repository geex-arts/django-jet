try:
    from django.urls import reverse
except ImportError: # Django 1.11
    from django.urls import reverse

from django.urls import path, re_path
from django.contrib import messages
from django.shortcuts import redirect
from httplib2 import ServerNotFoundError
from jet.dashboard.dashboard_modules.google_analytics import GoogleAnalyticsClient, ModuleCredentialStorage
from jet.dashboard.models import UserDashboardModule
from jet.dashboard import dashboard
from django.http import HttpResponse
from oauth2client.client import FlowExchangeError
from django.utils.translation import gettext_lazy as _


def google_analytics_grant_view(request, pk):
    redirect_uri = request.build_absolute_uri(reverse('jet-dashboard:google-analytics-callback'))
    client = GoogleAnalyticsClient(redirect_uri=redirect_uri)
    return redirect(client.get_oauth_authorize_url(pk))


def google_analytics_revoke_view(request, pk):
    try:
        module = UserDashboardModule.objects.get(pk=pk)
        ModuleCredentialStorage(module).delete()
        return redirect(reverse('jet-dashboard:update_module', kwargs={'pk': module.pk}))
    except UserDashboardModule.DoesNotExist:
        return HttpResponse(_('Module not found'))


def google_analytics_callback_view(request):
    module = None

    try:
        state = request.GET['state']
        module = UserDashboardModule.objects.get(pk=state)

        redirect_uri = request.build_absolute_uri(reverse('jet-dashboard:google-analytics-callback'))
        client = GoogleAnalyticsClient(redirect_uri=redirect_uri)
        client.set_credential_from_request(request)

        ModuleCredentialStorage(module).put(client.credential)
    except (FlowExchangeError, ValueError, ServerNotFoundError):
        messages.error(request, _('API request failed.'))
    except KeyError:
        return HttpResponse(_('Bad arguments'))
    except UserDashboardModule.DoesNotExist:
        return HttpResponse(_('Module not found'))

    return redirect(reverse('jet-dashboard:update_module', kwargs={'pk': module.pk}))

dashboard.urls.register_urls([
    path('google-analytics/grant/<int:pk>/', google_analytics_grant_view, name='google-analytics-grant'),
    path('google-analytics/revoke/<int:pk>/', google_analytics_revoke_view, name='google-analytics-revoke'),
    re_path(r'^google-analytics/callback/', google_analytics_callback_view, name='google-analytics-callback'),
])
