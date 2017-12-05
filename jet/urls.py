import django
from django.conf.urls import url

from jet.views import add_bookmark_view, remove_bookmark_view, toggle_application_pin_view, model_lookup_view

urlpatterns = [
    url(
        r'^add_bookmark/$',
        add_bookmark_view,
        name='add_bookmark'
    ),
    url(
        r'^remove_bookmark/$',
        remove_bookmark_view,
        name='remove_bookmark'
    ),
    url(
        r'^toggle_application_pin/$',
        toggle_application_pin_view,
        name='toggle_application_pin'
    ),
    url(
        r'^model_lookup/$',
        model_lookup_view,
        name='model_lookup'
    ),
]

if django.VERSION[0] >= 2:
    from django.views.i18n import JavaScriptCatalog
    urlpatterns.append(url(
        r'^jsi18n/$',
        JavaScriptCatalog.as_view(packages=['django.conf', 'django.contrib.admin', 'jet']),
        name='jsi18n')
    )
else:
    from django.views.i18n import javascript_catalog
    urlpatterns.append(url(
        r'^jsi18n/$',
        javascript_catalog,
        {'packages': ('django.conf', 'django.contrib.admin', 'jet',)},
        name='jsi18n'
    ))

if django.VERSION[:2] < (1, 8):
    from django.conf.urls import patterns
    urlpatterns = patterns('', *urlpatterns)
