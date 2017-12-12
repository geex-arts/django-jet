from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class JetDashboardConfig(AppConfig):
    name = 'jet.dashboard'
    label = 'jet.dashboard'
    verbose_name = _('Jet Dashboard')
