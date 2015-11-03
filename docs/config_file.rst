Config file
===========

Options available in settings.py:

JET_DEFAULT_THEME
-----------------

Django JET allows you to change default theme. This feature is mainly used for customizing color schemes rather than
making absolutely different themes. This option in fact make Django load different css styles.

Possible built-in themes are:

* default
* green
* light-violet
* light-green
* light-blue
* light-gray

To change theme use parameter:

.. code:: python

    JET_DEFAULT_THEME = 'light-gray'

JET_THEMES
----------

You can allow your users to change admin panel color scheme. This option will add color scheme chooser to the user dropdown menu. Make ``JET_THEMES`` an empty list to disable this feature.

.. code:: python

    JET_THEMES = [
        {
            'theme': 'default', # theme folder name
            'color': '#47bac1', # color of the theme's button in user menu
            'title': 'Default' # theme title
        },
        {
            'theme': 'violet',
            'color': '#a464c4',
            'title': 'Violet'
        },
        {
            'theme': 'green',
            'color': '#44b78b',
            'title': 'Green'
        },
        {
            'theme': 'light-green',
            'color': '#2faa60',
            'title': 'Light Green'
        },
        {
            'theme': 'light-violet',
            'color': '#a464c4',
            'title': 'Light Violet'
        },
        {
            'theme': 'light-blue',
            'color': '#5EADDE',
            'title': 'Light Blue'
        },
        {
            'theme': 'light-gray',
            'color': '#222',
            'title': 'Light Gray'
        }
    ]

CUSTOM JET_THEME
----------------

You are free to add your own color schemes by adding new folder to **/static/jet/css/themes/**.
You can use **/jet/static/jet/css/themes/light-violet/** folder as an example (available in Django JET repository).
_variables.scss contains **all** customizable variables. You'll have to compile all .scss files in theme directory
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

    JET_APP_INDEX_DASHBOARD = 'jet.dashboard.DefaultAppIndexDashboard'

