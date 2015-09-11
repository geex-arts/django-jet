Config file
===========

Options available in settings.py:

JET_THEME
---------

Django JET allows you to change default theme. This feature is mainly used for customizing color schemes rather than
making absolutely different themes. This option in fact make Django load different css styles.

Possible built-in themes are:

* default
* green

.. note:: More themes are incoming in future.

To change theme use parameter:

.. code:: python

    JET_THEME = 'default'

CUSTOM JET_THEME
----------------

You are free to add your own color schemes by adding new folder to **/static/jet/css/themes/**.
You can use **/jet/static/jet/css/themes/green/** folder as an example (available in Django JET repository).
_variables.scss contains **all** used colors. You'll have to compile all .scss files in theme directory
to start using your own theme.


JET_INDEX_DASHBOARD
-------------------

Sets which dashboard class will be used for rendering admin index dashboard. Allows you to create
your own dashboard with custom modules and pre-installed layout.

.. code:: python

    JET_INDEX_DASHBOARD = 'jet.dashboard.DefaultIndexDashboard'

JET_APP_INDEX_DASHBOARD
-----------------------

Same as **JET_INDEX_DASHBOARD**, but for application pages

.. code:: python

    JET_APP_INDEX_DASHBOARD = g'jet.dashboard.DefaultAppIndexDashboard'

