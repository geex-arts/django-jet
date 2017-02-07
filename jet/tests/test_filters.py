from django.contrib import admin
from django.test import TestCase, RequestFactory
from django.utils.encoding import smart_text
from jet.filters import RelatedFieldAjaxListFilter
from jet.tests.models import RelatedToTestModel, TestModel

try:
    from django.contrib.admin.utils import get_fields_from_path
except ImportError: # Django 1.6
    from django.contrib.admin.util import get_fields_from_path


class FakeChangeList(object):
    def get_query_string(self, *args, **kwargs):
        return ""


class FiltersTestCase(TestCase):
    def setUp(self):
        self.models = []
        self.factory = RequestFactory()
        self.models.append(TestModel.objects.create(field1='first', field2=1))
        self.models.append(TestModel.objects.create(field1='second', field2=2))
        self.fake_change_list = FakeChangeList()

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

        field_choices = list_filter.field_choices(field, request, model_admin)

        self.assertEqual(field_choices, [
            (self.models[0].pk, smart_text(self.models[0])),
            (self.models[1].pk, smart_text(self.models[1])),
        ])

        # check choice selection
        choices = list(list_filter.choices(self.fake_change_list))
        choices[0]['display'] = str(choices[0]['display'])  # gettext_lazy()
        self.assertEqual(choices, [
            {'display': 'All', 'query_string': '', 'selected': True},
            {'display': 'first1', 'query_string': '', 'selected': False},
            {'display': 'second2', 'query_string': '', 'selected': False},
        ])

    def test_related_field_ajax_list_filter_with_initial(self):
        initial = self.models[1]
        request = self.factory.get('url', {'field__id__exact': initial.pk})
        field, lookup_params, model, model_admin, field_path = self.get_related_field_ajax_list_filter_params()
        list_filter = RelatedFieldAjaxListFilter(field, request, lookup_params, model, model_admin, field_path)

        self.assertTrue(list_filter.has_output())

        field_choices = list_filter.field_choices(field, request, model_admin)

        self.assertEqual(field_choices, [
            (self.models[0].pk, smart_text(self.models[0])),
            (self.models[1].pk, smart_text(self.models[1])),
        ])

        # check choice selection
        choices = list(list_filter.choices(self.fake_change_list))
        choices[0]['display'] = str(choices[0]['display'])  # gettext_lazy()
        self.assertEqual(choices, [
            {'display': 'All', 'query_string': '', 'selected': False},
            {'display': 'first1', 'query_string': '', 'selected': False},
            {'display': 'second2', 'query_string': '', 'selected': True},
        ])
