from __future__ import unicode_literals
import datetime
from collections import OrderedDict

try:
    import pytz
except ImportError:
    pytz = None

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_text
from django.utils.html import format_html
from django.core.urlresolvers import reverse

try:
    from django.contrib.admin.utils import get_model_from_relation
except ImportError:  # Django 1.6
    from django.contrib.admin.util import get_model_from_relation

try:
    from django.forms.utils import flatatt
except ImportError:  # Django 1.6
    from django.forms.util import flatatt


def make_dt_aware(dt):
    if pytz is not None and settings.USE_TZ:
        timezone = pytz.timezone(settings.TIME_ZONE)
        if dt.tzinfo is not None:
            dt = timezone.normalize(dt)
        else:
            dt = timezone.localize(dt)
    return dt


class RelatedFieldAjaxListFilter(admin.RelatedFieldListFilter):
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


class DateRangeFilter(admin.filters.FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_gte = '{}__gte'.format(field_path)
        self.lookup_kwarg_lte = '{}__lte'.format(field_path)

        super(DateRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)

        self.form = self.get_form(request)

    def choices(self, cl):
        yield {
            'system_name': slugify(self.title),
            'query_string': cl.get_query_string(
                {}, remove=[self.lookup_kwarg_gte, self.lookup_kwarg_lte]
            )
        }

    def expected_parameters(self):
        return [self.lookup_kwarg_gte, self.lookup_kwarg_lte]

    def queryset(self, request, queryset):
        if self.form.is_valid():
            validated_data = dict(self.form.cleaned_data.items())
            if validated_data:
                return queryset.filter(
                    **self._make_query_filter(validated_data)
                )
        return queryset

    def _make_query_filter(self, validated_data):
        query_params = {}
        date_value_gte = validated_data.get(self.lookup_kwarg_gte, None)
        date_value_lte = validated_data.get(self.lookup_kwarg_lte, None)

        if date_value_gte:
            query_params['{0}__gte'.format(self.field_path)] = make_dt_aware(
                datetime.datetime.combine(date_value_gte, datetime.time.min)
            )
        if date_value_lte:
            query_params['{0}__lte'.format(self.field_path)] = make_dt_aware(
                datetime.datetime.combine(date_value_lte, datetime.time.max)
            )
        return query_params

    def get_template(self):
        return 'rangefilter/date_filter.html'

    template = property(get_template)

    def get_form(self, request):
        form_class = self._get_form_class()
        return form_class(self.used_parameters)

    def _get_form_class(self):
        fields = self._get_form_fields()

        form_class = type(
            str('DateRangeForm'),
            (forms.BaseForm,),
            {'base_fields': fields}
        )
        form_class.media = self._get_media()

        return form_class

    def _get_form_fields(self):
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
