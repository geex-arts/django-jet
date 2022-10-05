from django.db.models import PositiveIntegerField
from django.test import TestCase

from jet.fields import get_user_field


class UserFieldTest(TestCase):

    def test_default_user_field(self):
        default_cls = PositiveIntegerField
        cls = get_user_field()
        self.assertIsNotNone(cls)
        self.assertEqual(cls, default_cls)
