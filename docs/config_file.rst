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

COMPACT MENU
------------

If you don't have a lot of apps and models it can be annoying to have a two-level menu.
In this case you can use menu's compact mode, which will list applications and models in the side menu without need
to move pointer over applications to show models.

.. code:: python

    JET_SIDE_MENU_COMPACT = True

Default is ``False``

CUSTOM MENU
-----------

By default JET displays all applications and it models in the side menu in the alphabetical order.
To display applications and models you want or to change their order you can use ``JET_SIDE_MENU_CUSTOM_APPS`` setting.

.. code:: python

    JET_SIDE_MENU_CUSTOM_APPS = [
        ('core', [ # Each list element is a tuple with application name (app_label) and list of models
            'User',
            'MenuItem',
            'Block',
        ]),
        ('shops', [
            'Shop',
            'City',
            'MetroStation',
        ]),
        ('feedback', [
            'Feedback',
        ]),
    ]

If want to show all application's models use ``__all__`` keyword.

.. code:: python

    JET_SIDE_MENU_CUSTOM_APPS = [
        ('core', ['__all__']),
        ...
    ]

.. note::

    You can use ``jet_custom_apps_example`` management command to generate example ``JET_SIDE_MENU_CUSTOM_APPS``
    setting which includes all your applications and models. You can use it this way:

    .. code:: python

        python manage.py jet_custom_apps_example


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

