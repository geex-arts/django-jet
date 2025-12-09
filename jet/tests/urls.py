import django
from django.urls import include, path
from django.contrib import admin

admin.autodiscover()


try:
    from django.urls import path

    urlpatterns = [
        path('jet/', include('jet.urls', 'jet')),
        path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
        path('admin/doc/', include('django.contrib.admindocs.urls')),
        path('admin/', admin.site.urls),
    ]
except ImportError:  # Django < 2.0
    urlpatterns = [
        path('jet/', include('jet.urls', 'jet')),
        path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
        path('admin/doc/', include('django.contrib.admindocs.urls')),
        path('admin/', include(admin.site.urls)),
    ]

if django.VERSION[:2] < (1, 8):
    from django.conf.urls import patterns
    urlpatterns = patterns('', *urlpatterns)
