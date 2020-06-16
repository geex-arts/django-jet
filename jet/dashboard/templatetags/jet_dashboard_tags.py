from __future__ import unicode_literals
import django
from django import template
from jet.dashboard.utils import get_current_dashboard

register = template.Library()
if django.VERSION >= (1, 9):  # https://docs.djangoproject.com/en/dev/releases/1.9/#assignment-tag
    assignment_tag = register.simple_tag
else:
    assignment_tag = register.assignment_tag()


@assignment_tag(takes_context=True)
def get_dashboard(context, location):
    dashboard_cls = get_current_dashboard(location)

    app_label = context['request'].resolver_match.kwargs.get('app_label')

    return dashboard_cls(context, app_label=app_label)


@register.filter
def format_change_message(log_entry):
    # Django 1.10+
    if hasattr(log_entry, 'get_change_message'):
        return log_entry.get_change_message()
    else:
        return log_entry.change_message
