from importlib import import_module
from jet.dashboard import settings


def get_current_dashboard(location):
    if location == 'index':
        path = settings.JET_INDEX_DASHBOARD
    elif location == 'app_index':
        path = settings.JET_APP_INDEX_DASHBOARD
    else:
        raise ValueError('Unknown dashboard location: %s' % location)

    module, cls = path.rsplit('.', 1)

    try:
        module = import_module(module)
        index_dashboard_cls = getattr(module, cls)
        return index_dashboard_cls
    except ImportError:
        return None
