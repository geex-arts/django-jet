from __future__ import unicode_literals
from django import template
from django.core.urlresolvers import reverse
from django.db.models import OneToOneField
from django.forms import CheckboxInput, ModelChoiceField, Select, ModelMultipleChoiceField, SelectMultiple
from django.utils.formats import get_format
from django.template import loader, Context
from jet import settings
from jet.models import Bookmark, PinnedApplication
import re
from jet.utils import get_app_list, get_model_instance_label

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
        c = Context({'items': items})

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
    app_list = get_app_list(context)

    current_found = False

    pinned = PinnedApplication.objects.values_list('app_label', flat=True)

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

    return {'apps': apps, 'pinned_apps': pinned_apps}


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

            initial_value = field.form.initial.get(field.name)

            if hasattr(field, 'field') and isinstance(field.field, ModelMultipleChoiceField):
                if initial_value:
                    initial_objects = model.objects.filter(pk__in=initial_value)
                    choices.extend(
                        [(initial_object.pk, get_model_instance_label(initial_object))
                            for initial_object in initial_objects]
                    )

                field.field.widget.widget = SelectMultiple(attrs, choices=choices)
            elif hasattr(field, 'field') and isinstance(field.field, ModelChoiceField):
                if initial_value:
                    initial_object = model.objects.get(pk=initial_value)
                    attrs['data-object-id'] = initial_value
                    choices.append((initial_object.pk, get_model_instance_label(initial_object)))

                field.field.widget.widget = Select(attrs, choices=choices)

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
    return settings.JET_THEME
