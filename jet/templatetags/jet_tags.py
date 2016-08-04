from __future__ import unicode_literals
import django
from django import template
from django.core.urlresolvers import reverse
from django.db.models import OneToOneField
from django.forms import CheckboxInput, ModelChoiceField, Select, ModelMultipleChoiceField, SelectMultiple
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.formats import get_format
from django.template import loader, Context
from jet import settings, VERSION
from jet.models import Bookmark, PinnedApplication
import re
from jet.utils import get_app_list, get_model_instance_label, get_model_queryset
try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl


register = template.Library()


@register.simple_tag
def get_date_format():
    return get_format('DATE_INPUT_FORMATS')[0]


@register.simple_tag
def get_time_format():
    return get_format('TIME_INPUT_FORMATS')[0]


@register.simple_tag
def get_datetime_format():
    return get_format('DATETIME_INPUT_FORMATS')[0]


@register.tag
def format_breadcrumbs(parser, token):
    nodelist = parser.parse(('endformat_breadcrumbs',))
    parser.delete_first_token()
    return FormatBreadcrumbsNode(nodelist)


class FormatBreadcrumbsNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)

        regex = re.compile('<[^!(a>)]([^>]|\n)*[^!(/a)]>', re.IGNORECASE)
        clean = re.sub(regex, '', output)
        clean = clean.replace('\u203A', '&rsaquo;')
        items = clean.split('&rsaquo;')

        items = map(lambda i: i.strip(), items)
        items = filter(None, items)

        t = loader.get_template('admin/breadcrumbs.html')
        c = {'items': items}

        if django.VERSION[:2] < (1, 9):
            c = Context(c)

        return t.render(c)


@register.assignment_tag
def filter_fieldsets_with_errors(fieldsets):
    i = 0
    fieldsets_with_errors = list()

    for fieldset in fieldsets:
        errors = False

        for line in fieldset:
            for field in line:
                if hasattr(field.field, 'errors') and len(field.field.errors) > 0:
                    errors = True
                    break
            if errors:
                break

        if errors:
            fieldsets_with_errors.append(i)

        i += 1

    return fieldsets_with_errors


@register.assignment_tag
def is_fieldset_selected(fieldset_index, fieldsets_with_errors):
    if len(fieldsets_with_errors) == 0:
        return fieldset_index == 0
    else:
        return fieldset_index == fieldsets_with_errors[0]


@register.assignment_tag
def is_fieldset_with_errors(fieldset_index, fieldsets_with_errors):
    return fieldset_index in fieldsets_with_errors


@register.assignment_tag
def formset_has_errors(formset):
    if formset is None or getattr(formset, 'errors') is None:
        return False
    for errors in formset.errors:
        if errors:
            return True
    return False


@register.filter
def get_type(value):
    return type(value).__name__


@register.filter
def format_deletable_object(deletable_object):
    item = None
    items = []

    for object in deletable_object:
        if type(object) != list:
            item = {'text': object}
            items.append(item)
        elif item is not None:
            item['list'] = object

    return items


@register.assignment_tag(takes_context=True)
def get_menu(context):
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

        for item in settings.JET_SIDE_MENU_CUSTOM_APPS:
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

    pinned = PinnedApplication.objects.values_list('app_label', flat=True)

    all_aps = []
    apps = []
    pinned_apps = []

    for app in app_list:
        if not current_found:
            for model in app['models']:
                if context['request'].path.startswith(model['admin_url']):
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
def get_bookmarks(user):
    if user is None:
        return None
    return Bookmark.objects.filter(user=user.pk)


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.filter
def select2_lookups(field):
    if hasattr(field, 'field') and isinstance(field.field, ModelChoiceField):
        qs = field.field.queryset
        model = qs.model

        if getattr(model, 'autocomplete_search_fields', None):
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


@register.simple_tag(takes_context=True)
def jet_add_preserved_filters(context, url, popup=False, to_field=None):
    try:
        from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
        try:
            return add_preserved_filters(context, url, popup, to_field)
        except TypeError:
            return add_preserved_filters(context, url, popup)  # old django
    except ImportError:
        return url


@register.filter()
def if_onetoone(formset):
    return getattr(formset, 'fk') and isinstance(formset.fk, OneToOneField)


@register.assignment_tag
def format_current_language(language):
    language = language.replace('_', '-').lower()
    split = language.split('-', 2)
    if len(split) == 2:
        language = split[0] + '-' + split[1].upper() if split[0] != split[1] else split[0]
    return language


@register.assignment_tag(takes_context=True)
def get_current_theme(context):
    if 'request' in context and 'JET_THEME' in context['request'].COOKIES:
        theme = context['request'].COOKIES['JET_THEME']
        if isinstance(settings.JET_THEMES, list) and len(settings.JET_THEMES) > 0:
            for conf_theme in settings.JET_THEMES:
                if isinstance(conf_theme, dict) and conf_theme.get('theme') == theme:
                    return theme
    return settings.JET_DEFAULT_THEME


@register.assignment_tag
def get_themes():
    return settings.JET_THEMES


@register.assignment_tag
def get_current_jet_version():
    return VERSION


@register.assignment_tag
def get_side_menu_compact():
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
    queryset = get_model_queryset(model, preserved_filters=preserved_filters)

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

    url = reverse('admin:%s_%s_change' % (
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
