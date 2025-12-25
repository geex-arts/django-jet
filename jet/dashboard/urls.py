import django
try:
    from django.conf.urls import url
except ImportError: # Django 3+ (tested with Django 4.0)
    from django.urls import re_path as url

try:
    from django.views.i18n import JavaScriptCatalog
    javascript_catalog = JavaScriptCatalog.as_view()
except ImportError:  # Django < 2.0
    from django.views.i18n import javascript_catalog

from jet.dashboard import dashboard
from jet.dashboard.views import update_dashboard_modules_view, add_user_dashboard_module_view, \
    update_dashboard_module_collapse_view, remove_dashboard_module_view, UpdateDashboardModuleView, \
    load_dashboard_module_view, reset_dashboard_view

app_name = 'dashboard'

urlpatterns = [
    url(
        r'^module/(?P<pk>\d+)/$',
        UpdateDashboardModuleView.as_view(),
        name='update_module'
    ),
    url(
        r'^update_dashboard_modules/$',
        update_dashboard_modules_view,
        name='update_dashboard_modules'
    ),
    url(
        r'^add_user_dashboard_module/$',
        add_user_dashboard_module_view,
        name='add_user_dashboard_module'
    ),
    url(
        r'^update_dashboard_module_collapse/$',
        update_dashboard_module_collapse_view,
        name='update_dashboard_module_collapse'
    ),
    url(
        r'^remove_dashboard_module/$',
        remove_dashboard_module_view,
        name='remove_dashboard_module'
    ),
    url(
        r'^load_dashboard_module/(?P<pk>\d+)/$',
        load_dashboard_module_view,
        name='load_dashboard_module'
    ),
    url(
        r'^reset_dashboard/$',
        reset_dashboard_view,
        name='reset_dashboard'
    ),
    url(
        r'^jsi18n/$',
        javascript_catalog,
        {'packages': 'jet'},
        name='jsi18n'
    ),
]

urlpatterns += dashboard.urls.get_urls()

if django.VERSION[:2] < (1, 8):
    from django.conf.urls import patterns
    urlpatterns = patterns('', *urlpatterns)
