from __future__ import unicode_literals
import json
import os
from django import template
from django.core.urlresolvers import reverse
from django.forms import CheckboxInput, ModelChoiceField, Select, ModelMultipleChoiceField, SelectMultiple
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from jet import settings, VERSION
from jet.models import Bookmark, PinnedApplication
from jet.utils import get_app_list, get_model_instance_label, get_model_queryset, get_possible_language_codes, \
    get_admin_site

try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl


register = template.Library()


@register.simple_tag
def jet_get_date_format():
    return get_format('DATE_INPUT_FORMATS')[0]


@register.simple_tag
def jet_get_time_format():
    return get_format('TIME_INPUT_FORMATS')[0]


@register.simple_tag
def jet_get_datetime_format():
    return get_format('DATETIME_INPUT_FORMATS')[0]


@register.assignment_tag(takes_context=True)
def jet_get_menu(context):
    if settings.JET_SIDE_MENU_CUSTOM_APPS not in (None, False):
        app_list = get_app_list(context, False)
        app_dict = {}
        models_dict = {}

        for app in app_list:
            app_label = app.get('app_label', app.get('name'))
            app_dict[app_label] = app

            for model in app['models']:
                if app_label not in models_dict:
                    models_dict[app_label] = {}

                models_dict[app_label][model['object_name']] = model

            app['models'] = []

        app_list = []
        settings_app_list = settings.JET_SIDE_MENU_CUSTOM_APPS

        if isinstance(settings_app_list, dict):
            admin_site = get_admin_site(context)
            settings_app_list = settings_app_list.get(admin_site.name, [])

        for item in settings_app_list:
            app_label, models = item

            if app_label in app_dict:
                app = app_dict[app_label]

                for model_label in models:
                    if model_label == '__all__':
                        app['models'] = models_dict[app_label].values()
                        break
                    elif model_label in models_dict[app_label]:
                        model = models_dict[app_label][model_label]
                        app['models'].append(model)

                app_list.append(app)
    else:
        app_list = get_app_list(context)

    current_found = False

    pinned = PinnedApplication.objects.filter(user=context.get('user').pk).values_list('app_label', flat=True)

    all_aps = []
    apps = []
    pinned_apps = []

    for app in app_list:
        if not current_found:
            for model in app['models']:
                if 'admin_url' in model and context['request'].path.startswith(model['admin_url']):
                    model['current'] = True
                    current_found = True
                    break

            if not current_found and context['request'].path.startswith(app['app_url']):
                app['current'] = True
                current_found = True

        if app.get('app_label', app.get('name')) in pinned:
            pinned_apps.append(app)
        else:
            apps.append(app)

        all_aps.append(app)

    return {'apps': apps, 'pinned_apps': pinned_apps, 'all_apps': all_aps}


@register.assignment_tag
def jet_get_bookmarks(user):
    if user is None:
        return None
    return Bookmark.objects.filter(user=user.pk)


@register.filter
def jet_is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.filter
def jet_select2_lookups(field):
    if hasattr(field, 'field') and isinstance(field.field, ModelChoiceField):
        qs = field.field.queryset
        model = qs.model

        if getattr(model, 'autocomplete_search_fields', None) and getattr(field.field, 'autocomplete', True):
            choices = []
            app_label = model._meta.app_label
            model_name = model._meta.object_name

            attrs = {
                'class': 'ajax',
                'data-app-label': app_label,
                'data-model': model_name,
                'data-ajax--url': reverse('jet:model_lookup')
            }

            form = field.form
            initial_value = form.data.get(field.name) if form.data != {} else form.initial.get(field.name)

            if hasattr(field, 'field') and isinstance(field.field, ModelMultipleChoiceField):
                if initial_value:
                    initial_objects = model.objects.filter(pk__in=initial_value)
                    choices.extend(
                        [(initial_object.pk, get_model_instance_label(initial_object))
                            for initial_object in initial_objects]
                    )

                if isinstance(field.field.widget, RelatedFieldWidgetWrapper):
                    field.field.widget.widget = SelectMultiple(attrs)
                else:
                    field.field.widget = SelectMultiple(attrs)
                field.field.choices = choices
            elif hasattr(field, 'field') and isinstance(field.field, ModelChoiceField):
                if initial_value:
                    initial_object = model.objects.get(pk=initial_value)
                    attrs['data-object-id'] = initial_value
                    choices.append((initial_object.pk, get_model_instance_label(initial_object)))

                if isinstance(field.field.widget, RelatedFieldWidgetWrapper):
                    field.field.widget.widget = Select(attrs)
                else:
                    field.field.widget = Select(attrs)
                field.field.choices = choices

    return field


@register.assignment_tag(takes_context=True)
def jet_get_current_theme(context):
    if 'request' in context and 'JET_THEME' in context['request'].COOKIES:
        theme = context['request'].COOKIES['JET_THEME']
        if isinstance(settings.JET_THEMES, list) and len(settings.JET_THEMES) > 0:
            for conf_theme in settings.JET_THEMES:
                if isinstance(conf_theme, dict) and conf_theme.get('theme') == theme:
                    return theme
    return settings.JET_DEFAULT_THEME


@register.assignment_tag
def jet_get_themes():
    return settings.JET_THEMES


@register.assignment_tag
def jet_get_current_version():
    return VERSION


@register.filter
def jet_append_version(url):
    if '?' in url:
        return '%s&v=%s' % (url, VERSION)
    else:
        return '%s?v=%s' % (url, VERSION)


@register.assignment_tag
def jet_get_side_menu_compact():
    return settings.JET_SIDE_MENU_COMPACT


@register.assignment_tag
def jet_change_form_sibling_links_enabled():
    return settings.JET_CHANGE_FORM_SIBLING_LINKS


def jet_sibling_object_url(context, next):
    original = context.get('original')

    if not original:
        return

    model = type(original)
    preserved_filters_plain = context.get('preserved_filters', '')
    preserved_filters = dict(parse_qsl(preserved_filters_plain))
    admin_site = get_admin_site(context)

    if admin_site is None:
        return

    request = context.get('request')
    queryset = get_model_queryset(admin_site, model, request, preserved_filters=preserved_filters)

    if queryset is None:
        return

    sibling_object = None
    object_pks = list(queryset.values_list('pk', flat=True))

    try:
        index = object_pks.index(original.pk)
        sibling_index = index + 1 if next else index - 1
        exists = sibling_index < len(object_pks) if next else sibling_index >= 0
        sibling_object = queryset.get(pk=object_pks[sibling_index]) if exists else None
    except ValueError:
        pass

    if sibling_object is None:
        return

    url = reverse('%s:%s_%s_change' % (
        admin_site.name,
        model._meta.app_label,
        model._meta.model_name
    ), args=(sibling_object.pk,))

    if preserved_filters_plain != '':
        url += '?' + preserved_filters_plain

    return url


@register.assignment_tag(takes_context=True)
def jet_previous_object_url(context):
    return jet_sibling_object_url(context, False)


@register.assignment_tag(takes_context=True)
def jet_next_object_url(context):
    return jet_sibling_object_url(context, True)


@register.assignment_tag(takes_context=True)
def jet_popup_response_data(context):
    if context.get('popup_response_data'):
        return context['popup_response_data']

    return json.dumps({
        'action': context.get('action'),
        'value': context.get('value') or context.get('pk_value'),
        'obj': smart_text(context.get('obj')),
        'new_value': context.get('new_value')
    })


@register.simple_tag(takes_context=True)
def jet_delete_confirmation_context(context):
    if context.get('deletable_objects') is None and context.get('deleted_objects') is None:
        return ''
    return mark_safe('<div class="delete-confirmation-marker"></div>')


@register.assignment_tag
def jet_static_translation_urls():
    language_codes = get_possible_language_codes()

    urls = []
    url_templates = [
        'jet/js/i18n/jquery-ui/datepicker-__LANGUAGE_CODE__.js',
        'jet/js/i18n/jquery-ui-timepicker/jquery.ui.timepicker-__LANGUAGE_CODE__.js',
        'jet/js/i18n/select2/__LANGUAGE_CODE__.js'
    ]

    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

    for tpl in url_templates:
        for language_code in language_codes:
            url = tpl.replace('__LANGUAGE_CODE__', language_code)
            path = os.path.join(static_dir, url)

            if os.path.exists(path):
                urls.append(url)
                break

    return urls
