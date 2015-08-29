import json
from django.test import TestCase
from jet.tests.models import TestModel
from jet.utils import JsonResponse, get_model_instance_label


class UtilsTestCase(TestCase):
    def test_json_response(self):
        response = JsonResponse({'str': 'string', 'int': 1})
        response_dict = json.loads(response.content.decode())
        expected_dict = {"int": 1, "str": "string"}
        self.assertEqual(response_dict, expected_dict)
        self.assertEqual(response.get('Content-Type'), 'application/json')

    def test_get_model_instance_label(self):
        field1 = 'value'
        field2 = 2
        pinned_application = TestModel.objects.create(field1=field1, field2=field2)
        self.assertEqual(get_model_instance_label(pinned_application), '%s%d' % (field1, field2))



