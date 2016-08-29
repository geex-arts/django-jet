Contributing
============

Django JET is open-source and every member of the community can contribute to it. We are happy to see patches
and improvements with Django JET. But please keep in mind that there are some guidelines you should follow.

.. _requirements:

Requirements
------------

* Git master branch should always be stable
* All pull requests are made to git dev branch
* Non AGPL compatible code is not eligible for inclusion

Guidelines For Reporting An Issue/Feature
-----------------------------------------

So you've found a bug or have a great idea for a feature. Here's the steps you should take
to help get it added/fixed in Django JET:

* First check if there's an existing issue/pull request for this bug/feature. Issues can be found here
  https://github.com/geex-arts/django-jet/issues, PRs here https://github.com/geex-arts/django-jet/pulls
* If there isn't one there, please add an issue. The ideal report includes:

  * A description of the problem/suggestion
  * How to reproduce the bug
  * If relevant including the versions of your:

        * Python interpreter
        * Django
        * Django JET
        * Optionally of the other dependencies involved

  * It would be great if you also make a pull request which solves your issue

Guidelines For Contributing Code
--------------------------------

If you're ready to contribute back some code/docs, the process should look like:

* Fork the project on GitHub into your own account
* Clone your copy of Django JET to a separate folder
* Install it into your demo project using ``pip install -e PATH_TO_CLONED_JET``
* Make a new branch in git & commit your changes there
* Push your new branch up to GitHub
* Again, ensure there isn't already an issue or pull request out there on it. If there is and you feel you have
  a better fix, please take note of the issue number and mention it in your pull request
* Create a new pull request (based on your branch), including what the problem/feature is, versions of
  your software and referencing any related issues/pull requests

In order to be merged into Django JET, contributions must have the following:

* A solid patch that:

  * is clear
  * works across all supported versions of Python/Django
  * follows the existing style of the code base (mostly PEP-8)

* Desirably a test case that demonstrates the previous flaw that now passes with the included patch
* If it adds/changes a public API, it must also include documentation for those changes
* Must be appropriately licensed (see requirements_)

If your contribution lacks any of these things, they will have to be added by a core contributor before
being merged into Django JET proper, which may take time to get to.

Contribution Translations
-------------------------

If you want to add new translations locale, please do not use automatic Django locale generation, because it will
produce files with missing JS strings and duplicates. Instead copy the following well formatted "en" files to your
new locale folder:

* jet/locale/LOCALE/LC_MESSAGES/django.mo
* jet/locale/LOCALE/LC_MESSAGES/djangojs.mo
* jet/dashboard/locale/LOCALE/LC_MESSAGES/django.mo
* jet/dashboard/locale/LOCALE/LC_MESSAGES/djangojs.mo

Contribution Styles/Javascript/Translations
-------------------------------------------

Javascript/CSS/Translations need to be built each time after updating. For this you need `Node <http://nodejs.org>`_
and `Gulp <http://gulpjs.com>`_. It's out of the scope of this tutorial to go into details, but you should
find lots of useful references on how to install it.

Node is needed for Gulp, so install it using your system package manager:

.. code-block:: bash

    apt-get install -nodejs
    # or
    yum install nodejs
    # or
    brew install node
    # ...

Now you are able to install Gulp globally:

.. code-block:: bash

    npm install --global gulp-cli

Change your working directory to Django JET where ``package.json`` and ``gulpfile.js`` are located and
install Gulp dependencies:

.. code-block:: bash

    npm install

Now you are ready for contribution. Run Gulp from JET's directory to build all styles/scripts/locales and
start watching for changes (gulp will rebuild files as soon they change):

.. code-block:: bash

    gulp

Or if you want just to perform a single build without watching for changes run:

.. code-block:: bash

    gulp build

Building produces the following files:

* CSS files for each theme:

  * jet/static/jet/css/themes/THEME_NAME/base.css
  * jet/static/jet/css/themes/THEME_NAME/jquery-ui.theme.css
  * jet/static/jet/css/themes/THEME_NAME/select2.theme.css

* CSS for other JS libraries used in JET – jet/static/jet/css/vendor.css
* Combined JS scripts of JET – jet/static/jet/js/build/bundle.min.js
* Localization files for JS libraries:

  * jet/static/jet/js/i18n/jquery-ui/
  * jet/static/jet/js/i18n/jquery-ui-timepicker/
  * jet/static/jet/js/i18n/select2/

* Compiled Django localizations:

  * jet/locale/LOCALE/LC_MESSAGES/django.mo
  * jet/locale/LOCALE/LC_MESSAGES/djangojs.mo
  * jet/dashboard/locale/LOCALE/LC_MESSAGES/django.mo
  * jet/dashboard/locale/LOCALE/LC_MESSAGES/djangojs.mo

You should commit generated build files together with sources.

Contribution Documentation
--------------------------

If you update documentation files, you can build the html files (this is not needed with a pull-request,
but you might wanna check how documentation will look like locally). To do so change your working directory
to ``docs/`` inside JET and run:

.. code-block:: bash

    make html

``docs/_build/html/`` folder will contain all html files including starting ``index.html``.
