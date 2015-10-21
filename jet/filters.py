from django.contrib.admin import RelatedFieldListFilter
from django.contrib.admin.utils import get_model_from_relation
from django.core.urlresolvers import reverse
from django.forms.utils import flatatt
from django.utils.encoding import smart_text
from django.utils.html import format_html


class RelatedFieldAjaxListFilter(RelatedFieldListFilter):
    ajax_attrs = None

    def has_output(self):
        return True

    def field_choices(self, field, request, model_admin):
        app_label = field.related_model._meta.app_label
        model_name = field.related_model._meta.object_name

        self.ajax_attrs = format_html('{}', flatatt({
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

        queryset = field.related_model._default_manager.filter(**{rel_name: self.lookup_val}).all()
        return [(x._get_pk_val(), smart_text(x)) for x in queryset]
