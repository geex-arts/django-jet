================
Custom Dashboard
================

.. note::
   Django JET Dashboard tries to be as compatible as possible with django-admin-tools dashboard so that
   django-admin-tools modules could be easily ported to Django JET. In most cases it will be enough to
   change python imports and remove extending in modules templates.

Dashboard represents ``Dashboard`` class instances with ``DashboardModule`` class instances as its children.
Any custom **Dashboard** class should inherit from ``jet.dashboard.dashboard.Dashboard``
and use ``init_with_context`` to fill it with widgets. You should add your widgets
to the ``children`` and ``available_children`` attributes.

Before you continue, make sure you have completed the :doc:`install_dashboard`.

Set Up Custom Dashboard
-----------------------

* Create ``dashboard.py`` in any suitable location (e.g., in your project root) with the following content:

   .. code-block:: python

      from django.utils.translation import ugettext_lazy as _
      from jet.dashboard import modules
      from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


      class CustomIndexDashboard(Dashboard):
          columns = 3

          def init_with_context(self, context):
              self.available_children.append(modules.LinkList)
              self.children.append(modules.LinkList(
                  _('Support'),
                  children=[
                      {
                          'title': _('Django documentation'),
                          'url': 'http://docs.djangoproject.com/',
                          'external': True,
                      },
                      {
                          'title': _('Django "django-users" mailing list'),
                          'url': 'http://groups.google.com/group/django-users',
                          'external': True,
                      },
                      {
                          'title': _('Django irc channel'),
                          'url': 'irc://irc.freenode.net/django',
                          'external': True,
                      },
                  ],
                  column=0,
                  order=0
              ))


* Add the path to your ``dashboard.py`` in your ``settings.py`` file.  For example, if your
  ``dashboard.py`` is in the project root:

.. code:: python

    JET_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

That's all, now you have a dashboard with only one widget - ``LinkList``. Dashboard reset may be needed
if you had another dashboard already rendered for any user. Visit :doc:`dashboard_modules` to learn
about other widgets you can add to your custom dashboard or :doc:`dashboard_custom_module` or to create
your own.
