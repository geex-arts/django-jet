from django.conf import settings

# Theme
JET_DEFAULT_THEME = getattr(settings, 'JET_DEFAULT_THEME', 'default')
JET_THEMES = getattr(settings, 'JET_THEMES', [])
