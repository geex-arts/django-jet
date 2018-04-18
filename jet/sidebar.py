import itertools

from django.dispatch import Signal
from django.shortcuts import render
from django.template import loader, Template, Context
from django.views.generic.base import TemplateResponseMixin
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe


class Section:
    """
    Section base class rendered in Sidebar. Template is cached
    at a class level.
    """
    order = 0
    """
    Item order in the sidebar
    """
    title = None
    """
    Title of the menu
    """
    template_name = ''
    """
    Template used to render item
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_context_data(self, request, page_context):
        """
        Return context to use in template. If None is returned, it
        renders nothing but an empty string.
        """
        return {
            'self': self,
            'request': request,
            'ctx': page_context,
        }

    def render(self, request, page_context):
        """
        Render the section
        """
        context = self.get_context_data(request, page_context)
        if context is None:
            return ''
        return mark_safe(
            loader.get_template(self.template_name) \
                .render(context, request)
        )

    def popups(self):
        """
        If there are submenus to be rendered, this is the place to tell
        it. Return popups as a list of Section.
        """
        return []

    def __lt__(a, b):
        return a.order < b.order


class Sidebar(Section):
    """
    Sidebar is the main class to render the sidebar. Sidebar triggers
    a signal at rendering to retrieve sections (check out
    `Sidebar.signal`)
    """
    signal = Signal(['request', 'page_context', 'sections'])
    """
    [class] signal used to retrieve sections. Signal arguments:
    - request: request being processed
    - page_context: context of admin page being rendered
    - sections: array of sections to render.

    To render a section, two ways: return a Section from signal receiver
    or add sections instances to the given `sections` list.
    """
    request = None
    """
    Section being rendered
    """
    page_context = None
    """
    Current admin page being rendered
    """
    static_sections = []
    """
    [class attribute] Sections to always render.
    """

    template_name = 'jet/sidebar/sidebar.html'

    def __init__(self, request, page_context, **kwargs):
        self.request = request
        self.page_context = page_context
        super().__init__(**kwargs)

    @classmethod
    def connect(cl, *args, **kwargs):
        """
        Shortcut to self.signal.connect
        """
        cl.signal.connect(*args, **kwargs)

    @classmethod
    def disconnect(cl, *args, **kwargs):
        """
        Shortcut to self.signal.disconnect
        """
        cl.signal.disconnect(*args, **kwargs)

    @classmethod
    def add(cl, section):
        """
        Add a section to the static sections
        """
        cl.static_sections.append(section)
        cl.static_sections.sort()

    @classmethod
    def remove(cl, section):
        """
        Remove a section from static sections
        """
        cl.static_sections.remove(section)

    @cached_property
    def sections(self):
        """
        Gather items by triggering signal, and return them sorted by
        priority as an iterator.

        :param HttpRequest|None request: request being processed;
        :param sender: signal sender (if None, use self)
        :param \**kwargs: 'kwargs' attribute to pass to receivers
        """
        sections = []
        results = (v for r,v in
            self.signal.send(
                sender = self,
                sections = sections,
                request = self.request,
                page_context = self.page_context,
            )
            if isinstance(v, Section)
        )
        return sorted(itertools.chain(
            self.static_sections, sections, results
        ))

    def render(self, request = None, page_context = None):
        """
        Render sidebar. `request` and `page_context` by default are
        thoses used when instanciating the sidebar.
        """
        request = request or self.request
        page_context = page_context or self.page_context
        return super().render(request, page_context)

    def popups(self):
        return itertools.chain.from_iterable(
            item.popups() for item in self.sections
        )

    def render_sections(self):
        return [
            section.render(self.request, self.page_context)
                for section in self.sections
        ]

    def render_popups(self):
        return [
            section.render(self.request, self.page_context)
                for section in self.popups()
        ]



#
# Sections provided by default in JET
#
class NavSection(Section):
    template_name = 'jet/sidebar/section_nav.html'
    order = 1000

class AppPopup(Section):
    template_name = 'jet/sidebar/popup_app.html'
    app = None

    def get_context_data(self, request, page_context):
        context = super().get_context_data(request, page_context)
        context['app'] = self.app
        return context

class AppsSection(Section):
    template_name = 'jet/sidebar/section_apps.html'
    order = 2000

    def get_context_data(self, request, page_context):
        from jet.utils import get_menu_items
        self._apps = [
            app for app in get_menu_items(page_context)
                if app.get('has_perms')
        ]
        context = super().get_context_data(request, page_context)
        context['app_list'] = self._apps
        return context

    def popups(self):
        if not hasattr(self, '_popups'):
            self._popups = [ AppPopup(app = app) for app in self._apps ]
        return self._popups

class BookmarkSection(Section):
    template_name = 'jet/sidebar/section_bookmarks.html'
    order = 3000


# default sections to render in sidebar
Sidebar.static_sections += [
    NavSection(),
    AppsSection(),
    BookmarkSection(),
]

