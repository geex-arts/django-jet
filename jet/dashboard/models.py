from importlib import import_module
import json
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jet.utils import LazyDateTimeEncoder


@python_2_unicode_compatible
class UserDashboardModule(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    module = models.CharField(verbose_name=_('module'), max_length=255)
    app_label = models.CharField(verbose_name=_('application name'), max_length=255, null=True, blank=True)
    user = models.PositiveIntegerField(verbose_name=_('user'))
    column = models.PositiveIntegerField(verbose_name=_('column'))
    order = models.IntegerField(verbose_name=_('order'))
    settings = models.TextField(verbose_name=_('settings'), default='', blank=True)
    children = models.TextField(verbose_name=_('children'), default='', blank=True)
    collapsed = models.BooleanField(verbose_name=_('collapsed'), default=False)

    class Meta:
        verbose_name = _('user dashboard module')
        verbose_name_plural = _('user dashboard modules')
        ordering = ('column', 'order')

    def __str__(self):
        return self.module

    def load_module(self):
        try:
            package, module_name = self.module.rsplit('.', 1)
            package = import_module(package)
            module = getattr(package, module_name)

            return module
        except AttributeError:
            return None
        except ImportError:
            return None

    def pop_settings(self, pop_settings):
        settings = json.loads(self.settings)

        for setting in pop_settings:
            if setting in settings:
                settings.pop(setting)

        self.settings = json.dumps(settings, cls=LazyDateTimeEncoder)
        self.save()

    def update_settings(self, update_settings):
        settings = json.loads(self.settings)

        settings.update(update_settings)

        self.settings = json.dumps(settings, cls=LazyDateTimeEncoder)
        self.save()


