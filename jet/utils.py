from importlib import import_module
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.core.urlresolvers import reverse, resolve
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.encoding import force_text
from django.utils.encoding import smart_text
from django.utils.functional import Promise
from jet import settings


class JsonResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.
    :param data: Data to be dumped into json. By default only ``dict`` objects
      are allowed to be passed due to a security flaw before EcmaScript 5. See
      the ``safe`` parameter for more information.
    :param encoder: Should be an json encoder class. Defaults to
      ``django.core.serializers.json.DjangoJSONEncoder``.
    :param safe: Controls if only ``dict`` objects may be serialized. Defaults
      to ``True``.
    """

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        if safe and not isinstance(data, dict):
            raise TypeError('In order to allow non-dict objects to be '
                'serialized set the safe parameter to False')
        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=encoder)
        super(JsonResponse, self).__init__(content=data, **kwargs)


def get_app_list(context):
    template_response = get_admin_site(context.get('current_app', '')).index(context['request'])

    try:
        return template_response.context_data['app_list']
    except Exception:
        return None


def get_admin_site(current_app):
    try:
        resolver_match = resolve(reverse('%s:index' % current_app))
        for func_closure in resolver_match.func.func_closure:
            if isinstance(func_closure.cell_contents, AdminSite):
                return func_closure.cell_contents
    except:
        pass

    return admin.site


def get_admin_site_name(context):
    return get_admin_site(context).name


def get_current_dashboard(location):
    if location == 'index':
        path = settings.JET_INDEX_DASHBOARD
    elif location == 'app_index':
        path = settings.JET_APP_INDEX_DASHBOARD
    else:
        raise ValueError('Unknown dashboard location: %s' % location)

    module, cls = path.rsplit('.', 1)
    module = import_module(module)
    index_dashboard_cls = getattr(module, cls)

    return index_dashboard_cls


class LazyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return obj


def get_model_instance_label(instance):
    if getattr(instance, "related_label", None):
        return instance.related_label()
    return smart_text(instance)
