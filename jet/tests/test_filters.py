from django.contrib import admin
from django.test import TestCase, RequestFactory
from django.utils.encoding import smart_text
from jet.filters import RelatedFieldAjaxListFilter
from jet.tests.models import RelatedToTestModel, TestModel

try:
    from django.contrib.admin.utils import get_fields_from_path
except ImportError: # Django 1.6
    from django.contrib.admin.util import get_fields_from_path


class FiltersTestCase(TestCase):
    def setUp(self):
        self.models = []
        self.factory = RequestFactory()
        self.models.append(TestModel.objects.create(field1='first', field2=1))
        self.models.append(TestModel.objects.create(field1='second', field2=2))

    def get_related_field_ajax_list_filter_params(self):
        model = RelatedToTestModel
        field_path = 'field'
        field = get_fields_from_path(model, field_path)[-1]
        lookup_params = {}
        model_admin = admin.site._registry.get(model)

        return field, lookup_params, model, model_admin, field_path

    def test_related_field_ajax_list_filter(self):
        request = self.factory.get('url')
        field, lookup_params, model, model_admin, field_path = self.get_related_field_ajax_list_filter_params()
        list_filter = RelatedFieldAjaxListFilter(field, request, lookup_params, model, model_admin, field_path)

        self.assertTrue(list_filter.has_output())

        choices = list_filter.field_choices(field, request, model_admin)

        self.assertIsInstance(choices, list)
        self.assertEqual(len(choices), 0)

    def test_related_field_ajax_list_filter_with_initial(self):
        initial = self.models[1]
        request = self.factory.get('url', {'field__id__exact': initial.pk})
        field, lookup_params, model, model_admin, field_path = self.get_related_field_ajax_list_filter_params()
        list_filter = RelatedFieldAjaxListFilter(field, request, lookup_params, model, model_admin, field_path)

        self.assertTrue(list_filter.has_output())

        choices = list_filter.field_choices(field, request, model_admin)

        self.assertIsInstance(choices, list)
        self.assertEqual(len(choices), 1)
        self.assertEqual(choices[0], (initial.pk, smart_text(initial)))

