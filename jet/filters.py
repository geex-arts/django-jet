from django.contrib.admin import RelatedFieldListFilter
from django.utils.encoding import smart_text
from django.utils.html import format_html
try:
    from django.core.urlresolvers import reverse
except ImportError: # Django 1.11
    from django.urls import reverse

try:
    from django.contrib.admin.utils import get_model_from_relation
except ImportError: # Django 1.6
    from django.contrib.admin.util import get_model_from_relation

try:
    from django.forms.utils import flatatt
except ImportError: # Django 1.6
    from django.forms.util import flatatt


class RelatedFieldAjaxListFilter(RelatedFieldListFilter):
    template = 'jet/related_field_ajax_list_filter.html'
    ajax_attrs = None

    def has_output(self):
        return True

    def field_choices(self, field, request, model_admin):
        model = field.remote_field.model if hasattr(field, 'remote_field') else field.related_field.model
        app_label = model._meta.app_label
        model_name = model._meta.object_name

        self.ajax_attrs = format_html('{0}', flatatt({
            'data-app-label': app_label,
            'data-model': model_name,
            'data-ajax--url': reverse('jet:model_lookup'),
            'data-queryset--lookup': self.lookup_kwarg
        }))

        if self.lookup_val is None:
            return []

        other_model = get_model_from_relation(field)
        if hasattr(field, 'rel'):
            rel_name = field.rel.get_related_field().name
        else:
            rel_name = other_model._meta.pk.name

        queryset = model._default_manager.filter(**{rel_name: self.lookup_val}).all()
        return [(x._get_pk_val(), smart_text(x)) for x in queryset]


try:
    from collections import OrderedDict
    from django import forms
    from django.contrib.admin.widgets import AdminDateWidget
    from rangefilter.filter import DateRangeFilter as OriginalDateRangeFilter
    from django.utils.translation import ugettext as _


    class DateRangeFilter(OriginalDateRangeFilter):
        def get_template(self):
            return 'rangefilter/date_filter.html'

        def _get_form_fields(self):
            # this is here, because in parent DateRangeFilter AdminDateWidget
            # could be imported from django-suit
            return OrderedDict((
                (self.lookup_kwarg_gte, forms.DateField(
                    label='',
                    widget=AdminDateWidget(attrs={'placeholder': _('From date')}),
                    localize=True,
                    required=False
                )),
                (self.lookup_kwarg_lte, forms.DateField(
                    label='',
                    widget=AdminDateWidget(attrs={'placeholder': _('To date')}),
                    localize=True,
                    required=False
                )),
            ))

        @staticmethod
        def _get_media():
            css = [
                'style.css',
            ]
            return forms.Media(
                css={'all': ['range_filter/css/%s' % path for path in css]}
            )
except ImportError:
    pass
