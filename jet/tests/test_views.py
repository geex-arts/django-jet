import json
from django.contrib.auth.models import User
try:
    from django.core.urlresolvers import reverse
except ImportError: # Django 1.11
    from django.urls import reverse

from django.test import TestCase, Client
from jet.dashboard.modules import LinkList
from jet.models import Bookmark
from jet.dashboard.models import UserDashboardModule


class ViewsTestCase(TestCase):
    def setUp(self):
        self.assertTrue(self._login())

    def _login(self):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin'
        self.admin = Client()
        self.admin_user = User.objects.create_superuser(username, email, password)
        return self.admin.login(username=username, password=password)

    def test_module_update_view(self):
        title = 'Quick links Test'
        new_title = title + '2'
        new_layout = 'stacked'
        module = UserDashboardModule.objects.create(
            title=title,
            module='jet.dashboard.modules.LinkList',
            app_label=None,
            user=self.admin_user,
            column=0,
            order=0,
            settings='{"layout": "inline"}',
            children='[]'
        )

        response = self.admin.get(reverse('jet-dashboard:update_module', kwargs={'pk': module.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['module'] is not None)
        self.assertTrue(isinstance(response.context['module'], LinkList))
        self.assertEqual(response.context['module'].title, title)

        post = {
            'title': new_title,
            'layout': new_layout,
            'children-TOTAL_FORMS': '2',
            'children-INITIAL_FORMS': '1',
            'children-MIN_NUM_FORMS': '0',
            'children-MAX_NUM_FORMS': '1000',
            'children-0-url': 'http://docs.djangoproject.com/',
            'children-0-title': 'Django documentation',
            'children-0-external': 'on',
            'children-1-url': '',
            'children-1-title': '',
            'children-__prefix__-url': '',
            'children-__prefix__-title': '',
            '_save': 'Save'
        }

        self.admin.post(reverse('jet-dashboard:update_module', kwargs={'pk': module.pk}), post)
        self.assertEqual(response.status_code, 200)
        module = UserDashboardModule.objects.get(pk=module.pk)
        settings = json.loads(module.settings)
        self.assertEqual(module.title, new_title)
        self.assertEqual(settings['layout'], new_layout)

        module.delete()

    def test_add_bookmark_view(self):
        url = 'http://test.com/'
        title = 'Title'
        response = self.admin.post(reverse('jet:add_bookmark'), {'url': url, 'title': title})
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['error'])
        self.assertNotEqual(response['id'], None)
        bookmark = Bookmark.objects.get(pk=response['id'])
        self.assertNotEqual(bookmark, None)
        self.assertEqual(bookmark.title, title)
        self.assertEqual(bookmark.url, url)

    def test_add_bookmark_view_unauthorized(self):
        url = 'http://test.com/'
        title = 'Title'
        response = self.client.post(reverse('jet:add_bookmark'), {'url': url, 'title': title})
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertTrue(response['error'])

    def test_remove_bookmark_view(self):
        url = 'http://test.com/'
        title = 'Title'
        bookmark = Bookmark.objects.create(url=url, title=title, user=self.admin_user)
        response = self.admin.post(reverse('jet:remove_bookmark'), {'id': bookmark.id})
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['error'])
        self.assertFalse(Bookmark.objects.filter(pk=bookmark.pk).exists())

    def test_toggle_application_pin_view(self):
        app_label = 'test_app'

        response = self.admin.post(reverse('jet:toggle_application_pin'), {'app_label': app_label})
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['error'])
        self.assertTrue(response['pinned'])

        response = self.admin.post(reverse('jet:toggle_application_pin'), {'app_label': app_label})
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['error'])
        self.assertFalse(response['pinned'])

    def test_update_dashboard_modules_view(self):
        app_label = None
        module_0 = UserDashboardModule.objects.create(
            title='',
            module='jet.dashboard.modules.LinkList',
            app_label=app_label,
            user=self.admin_user,
            column=0,
            order=0
        )
        module_1 = UserDashboardModule.objects.create(
            title='',
            module='jet.dashboard.modules.LinkList',
            app_label=app_label,
            user=self.admin_user,
            column=0,
            order=1
        )
        response = self.admin.post(reverse('jet-dashboard:update_dashboard_modules'), {
            'app_label': '',
            'modules': json.dumps([
                {'id': module_0.pk, 'column': 0, 'order': 1},
                {'id': module_1.pk, 'column': 0, 'order': 0}
            ])
        })

        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['error'])

        module_0 = UserDashboardModule.objects.get(pk=module_0.pk)
        module_1 = UserDashboardModule.objects.get(pk=module_1.pk)

        self.assertEqual(module_0.order, 1)
        self.assertEqual(module_1.order, 0)

        module_0.delete()
        module_1.delete()

    def test_add_user_dashboard_module_view(self):
        response = self.admin.post(reverse('jet-dashboard:add_user_dashboard_module'), {
            'app_label': '',
            'type': 'available_children',
            'module': 0
        })

        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['error'])
        self.assertNotEqual(response['id'], None)
        module = UserDashboardModule.objects.get(pk=response['id'])
        self.assertNotEqual(module, None)

    def test_add_user_app_dashboard_module_view(self):
        app_label = 'auth'
        response = self.admin.post(reverse('jet-dashboard:add_user_dashboard_module'), {
            'app_label': app_label,
            'type': 'available_children',
            'module': 0
        })

        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['error'])
        self.assertNotEqual(response['id'], None)
        module = UserDashboardModule.objects.get(pk=response['id'])
        self.assertNotEqual(module, None)
        self.assertEqual(module.app_label, app_label)

    def test_update_dashboard_module_collapse_view(self):
        module = UserDashboardModule.objects.create(
            title='',
            module='jet.dashboard.modules.LinkList',
            app_label=None,
            user=self.admin_user,
            column=0,
            order=0
        )
        response = self.admin.post(reverse('jet-dashboard:update_dashboard_module_collapse'), {
            'id': module.pk, 'collapsed': True
        })
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['error'])
        self.assertTrue(response['collapsed'])

        module = UserDashboardModule.objects.get(pk=module.pk)
        response = self.admin.post(reverse('jet-dashboard:update_dashboard_module_collapse'), {
            'id': module.pk, 'collapsed': False
        })
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['error'])
        self.assertFalse(response['collapsed'])

        module.delete()

    def test_remove_dashboard_module_view(self):
        module = UserDashboardModule.objects.create(
            title='',
            module='jet.dashboard.modules.LinkList',
            app_label=None,
            user=self.admin_user,
            column=0,
            order=0
        )
        response = self.admin.post(reverse('jet-dashboard:remove_dashboard_module'), {'id': module.pk})
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertFalse(response['error'])
        self.assertFalse(UserDashboardModule.objects.filter(pk=module.pk).exists())
