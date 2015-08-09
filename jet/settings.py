from django.conf import settings

# Theme
JET_THEME = getattr(settings, 'JET_THEME', 'default')

# Dashboard
JET_INDEX_DASHBOARD = getattr(settings, 'JET_INDEX_DASHBOARD', 'jet.dashboard.DefaultIndexDashboard')
JET_APP_INDEX_DASHBOARD = getattr(settings, 'JET_APP_INDEX_DASHBOARD', 'jet.dashboard.DefaultAppIndexDashboard')