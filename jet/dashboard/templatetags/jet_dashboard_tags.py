from __future__ import unicode_literals
from django import template
from jet.dashboard.utils import get_current_dashboard

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_dashboard(context, location):
    dashboard_cls = get_current_dashboard(location)
    dashboard = dashboard_cls(context)
    return dashboard