from django.contrib.admin import AdminSite
from django.contrib.admin import ModelAdmin
from django.conf import settings

# Theme
JET_DEFAULT_THEME = getattr(settings, 'JET_DEFAULT_THEME', 'default')
JET_THEMES = getattr(settings, 'JET_THEMES', [])

# Side menu
JET_SIDE_MENU_COMPACT = getattr(settings, 'JET_SIDE_MENU_COMPACT', False)
JET_SIDE_MENU_CUSTOM_APPS = getattr(settings, 'JET_SIDE_MENU_CUSTOM_APPS', None)

# Improved usability
JET_CHANGE_FORM_SIBLING_LINKS = getattr(settings, 'JET_CHANGE_FORM_SIBLING_LINKS', True)

# Date time
JET_HEADER_DATE_FORMAT = getattr(settings, 'JET_HEADER_DATE_FORMAT')
JET_HEADER_TIME_FORMAT = getattr(settings, 'JET_HEADER_TIME_FORMAT')

ModelAdmin.list_per_page = getattr(settings, 'LIST_PER_PAGE')
AdminSite.site_title = getattr(settings, 'SITE_TITLE')
AdminSite.site_header = getattr(settings, 'SITE_HEADER')

