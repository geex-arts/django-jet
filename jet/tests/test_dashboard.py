from django.contrib.auth.models import User
try:
    from django.core.urlresolvers import reverse
except ImportError: # Django 1.11
    from django.urls import reverse

from django.test import TestCase, Client
from jet.dashboard.dashboard import Dashboard
from jet.dashboard.modules import LinkList, RecentActions
from jet.dashboard.models import UserDashboardModule
from jet.tests.dashboard import TestIndexDashboard


class DashboardTestCase(TestCase):
    class Request:
        def __init__(self, user):
            self.user = user

    def setUp(self):
        self._login()
        self._init_dashboard()

    def _login(self):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin'
        self.admin = Client()
        self.admin_user = User.objects.create_superuser(username, email, password)
        return self.admin.login(username=username, password=password)

    def _init_dashboard(self):
        UserDashboardModule.objects.create(
            title='',
            module='jet.dashboard.modules.LinkList',
            app_label=None,
            user=self.admin_user,
            column=0,
            order=0
        )
        UserDashboardModule.objects.create(
            title='',
            module='jet.dashboard.modules.RecentActions',
            app_label=None,
            user=self.admin_user,
            column=0,
            order=1
        )
        self.dashboard = TestIndexDashboard({'request': self.Request(self.admin_user)})

    def test_custom_columns(self):
        self.assertEqual(self.dashboard.columns, 3)

    def test_init_with_context_called(self):
        self.assertTrue(self.dashboard.init_with_context_called)

    def test_load_modules(self):
        self.assertEqual(len(self.dashboard.modules), 2)
        self.assertTrue(isinstance(self.dashboard.modules[0], LinkList))
        self.assertTrue(isinstance(self.dashboard.modules[1], RecentActions))

    def test_media(self):
        media = self.dashboard.media()
        self.assertEqual(len(media.js), 2)
        self.assertEqual(media.js[0], 'file.js')
        self.assertEqual(media.js[1], 'file2.js')
        self.assertEqual(len(media.css), 2)
        self.assertEqual(media.css[0], 'file.css')
        self.assertEqual(media.css[1], 'file2.css')

    def test_index_dashboard_view(self):
        response = self.admin.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('dashboard' in response.context)

        dashboard = response.context['dashboard']

        self.assertIsInstance(dashboard, Dashboard)
        self.assertIsNone(dashboard.app_label)

    def test_app_index_dashboard_view(self):
        app_label = 'tests'
        response = self.admin.get(reverse('admin:app_list', args=(app_label,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('dashboard' in response.context)

        dashboard = response.context['dashboard']

        self.assertIsInstance(dashboard, Dashboard)
        self.assertEqual(dashboard.app_label, app_label)
