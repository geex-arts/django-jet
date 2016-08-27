from datetime import datetime, date
import json
from django.contrib.admin import AdminSite
from django.test import TestCase
from jet.tests.models import TestModel
from jet.utils import JsonResponse, get_model_instance_label, get_app_list, get_admin_site, LazyDateTimeEncoder


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

    def test_get_app_list(self):
        class User:
            is_active = True
            is_staff = True

            def has_module_perms(self, app):
                return True

            def has_perm(self, object):
                return True

        class Request:
            user = User()

        app_list = get_app_list({
            'request': Request(),
            'user': None
        })

        self.assertIsInstance(app_list, list)

        for app in app_list:
            self.assertIsInstance(app, dict)
            self.assertIsNotNone(app, app.get('models'))
            self.assertIsNotNone(app, app.get('app_url'))
            self.assertIsNotNone(app, app.get('app_label'))

            for model in app['models']:
                self.assertIsNotNone(app, model.get('object_name'))
                self.assertIsNotNone(app, model.get('name'))

    def test_get_admin_site(self):
        admin_site = get_admin_site({})
        self.assertIsInstance(admin_site, AdminSite)

    def test_lazy_date_time_encoder_dates(self):
        encoder = LazyDateTimeEncoder()

        ts = datetime.now()
        self.assertEqual(encoder.encode(ts), '"%s"' % ts.isoformat())

        ts = date(2015, 5, 3)
        self.assertEqual(encoder.encode(ts), '"%s"' % ts.isoformat())

    def test_lazy_date_time_encoder_dict(self):
        encoder = LazyDateTimeEncoder()
        self.assertEqual(encoder.encode({'key': 1}), '{"key": 1}')

