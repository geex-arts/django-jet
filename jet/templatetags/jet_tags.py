from __future__ import unicode_literals
import json
import os
from django import template
try:
    from django.core.urlresolvers import reverse
except ImportError: # Django 1.11
    from django.urls import reverse

from django.forms import CheckboxInput, ModelChoiceField, Select, ModelMultipleChoiceField, SelectMultiple
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
try:
    from django.utils.encoding import smart_text as smart_txt
except ImportError: # Django 3+
    '''
    "The smart_text() and force_text() aliases (since Django 2.0) of 
    smart_str() and force_str() are deprecated...".

    Taken from:
    https://docs.djangoproject.com/en/4.0/releases/3.0/#deprecated-features-3-0
    '''
    from django.utils.encoding import smart_str as smart_txt

from jet import settings, VERSION
from jet.models import Bookmark
from jet.utils import get_model_instance_label, get_model_queryset, get_possible_language_codes, \
    get_admin_site, get_menu_items

try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl


register = template.Library()
assignment_tag = register.assignment_tag if hasattr(register, 'assignment_tag') else register.simple_tag


@assignment_tag
def jet_get_date_format():
    return get_format('DATE_INPUT_FORMATS')[0]


@assignment_tag
def jet_get_time_format():
    return get_format('TIME_INPUT_FORMATS')[0]


@assignment_tag
def jet_get_datetime_format():
    return get_format('DATETIME_INPUT_FORMATS')[0]


@assignment_tag(takes_context=True)
def jet_get_menu(context):
    return get_menu_items(context)


@assignment_tag
def jet_get_bookmarks(user):
    if user is None:
        return None
    return Bookmark.objects.filter(user=user.pk)


@register.filter
def jet_is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.filter
def jet_select2_lookups(field):
    if hasattr(field, 'field') and \
            (isinstance(field.field, ModelChoiceField) or isinstance(field.field, ModelMultipleChoiceField)):
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

            initial_value = field.value()

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
                    try:
                        initial_object = model.objects.get(pk=initial_value)
                        attrs['data-object-id'] = initial_value
                        choices.append((initial_object.pk, get_model_instance_label(initial_object)))
                    except model.DoesNotExist:
                        pass

                if isinstance(field.field.widget, RelatedFieldWidgetWrapper):
                    field.field.widget.widget = Select(attrs)
                else:
                    field.field.widget = Select(attrs)
                field.field.choices = choices

    return field


@assignment_tag(takes_context=True)
def jet_get_current_theme(context):
    if 'request' in context and 'JET_THEME' in context['request'].COOKIES:
        theme = context['request'].COOKIES['JET_THEME']
        if isinstance(settings.JET_THEMES, list) and len(settings.JET_THEMES) > 0:
            for conf_theme in settings.JET_THEMES:
                if isinstance(conf_theme, dict) and conf_theme.get('theme') == theme:
                    return theme
    return settings.JET_DEFAULT_THEME


@assignment_tag
def jet_get_themes():
    return settings.JET_THEMES


@assignment_tag
def jet_get_current_version():
    return VERSION


@register.filter
def jet_append_version(url):
    if '?' in url:
        return '%s&v=%s' % (url, VERSION)
    else:
        return '%s?v=%s' % (url, VERSION)


@assignment_tag
def jet_get_side_menu_compact():
    return settings.JET_SIDE_MENU_COMPACT


@assignment_tag
def jet_change_form_sibling_links_enabled():
    return settings.JET_CHANGE_FORM_SIBLING_LINKS


def jet_sibling_object(context, next):
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

    return {
        'label': str(sibling_object),
        'url': url
    }


@assignment_tag(takes_context=True)
def jet_previous_object(context):
    return jet_sibling_object(context, False)


@assignment_tag(takes_context=True)
def jet_next_object(context):
    return jet_sibling_object(context, True)


@assignment_tag(takes_context=True)
def jet_popup_response_data(context):
    if context.get('popup_response_data'):
        return context['popup_response_data']

    return json.dumps({
        'action': context.get('action'),
        'value': context.get('value') or context.get('pk_value'),
        #'obj': smart_text(context.get('obj')),
        'obj': smart_txt(context.get('obj')),   # Django 2&3+
        'new_value': context.get('new_value')
    })


@assignment_tag(takes_context=True)
def jet_delete_confirmation_context(context):
    if context.get('deletable_objects') is None and context.get('deleted_objects') is None:
        return ''
    return mark_safe('<div class="delete-confirmation-marker"></div>')


@assignment_tag
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
