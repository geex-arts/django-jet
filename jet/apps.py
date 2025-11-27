from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class JetConfig(AppConfig):
    name = 'jet'
    label = 'jet'
    verbose_name = _('Jet Admin Skin')
