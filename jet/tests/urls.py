import django
from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()


if django.VERSION > (1,9):  # https://docs.djangoproject.com/en/dev/releases/1.9/#passing-a-3-tuple-or-an-app-name-to-include
    urlpatterns = [
        url(r'^jet/', include('jet.urls', 'jet')),
        url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', admin.site.urls),
    ]
else:
    urlpatterns = [
        url(r'^jet/', include('jet.urls', 'jet')),
        url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
    ]

if django.VERSION[:2] < (1, 8):
    from django.conf.urls import patterns
    urlpatterns = patterns('', *urlpatterns)
