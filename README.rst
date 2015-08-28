==========
Django JET
==========

**Modern template for Django admin interface with improved functionality**

Free for non-commercial use. If you would like to use it in commercial project, please email at support@jet.geex-arts.com

.. image:: https://raw.githubusercontent.com/geex-arts/jet/static/logo.png
    :width: 250px
    :height: 250px
    :alt: Screenshot #1
    :align: center
    
* Home page: incoming
* Demo: incoming
* PyPI: https://pypi.python.org/pypi/django-jet
* Support: support@jet.geex-arts.com

Screenshots
===========

.. image:: https://raw.githubusercontent.com/geex-arts/jet/static/screen1.png
    :alt: Screenshot #1
    :align: center
    
.. image:: https://raw.githubusercontent.com/geex-arts/jet/static/screen2.png
    :alt: Screenshot #1
    :align: center
    
.. image:: https://raw.githubusercontent.com/geex-arts/jet/static/screen3.png
    :alt: Screenshot #1
    :align: center

Beta
====
Current version is still in beta phase. Use it at your own risk (though may be already enough workable).

License
=======
Django JET is licensed under a
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License

See online version of this license here:
https://creativecommons.org/licenses/by-nc-sa/4.0/

Installation
============

* Download and install latest version of Django JET:

    .. code:: python
    
        pip install django-jet
        # or
        easy_install django-jet

* Add 'jet' application to the INSTALLED_APPS setting of your Django project settings.py file (note it should be before 'django.contrib.admin'):

    .. code:: python
    
        INSTALLED_APPS = (
            ...
            'jet',
            'django.contrib.admin',
        )

* Add URL-pattern to the urlpatterns of your Django project urls.py file (they are needed for related–lookups and autocompletes):

    .. code:: python
    
        urlpatterns = patterns(
            '',
            url(r'^jet/', include('jet.urls')), # Django JET URLS
            url(r'^admin/', include(admin.site.urls)),
            ...
        )

* Apply migrations:

    .. code:: python
    
        python manage.py migrate jet
        
* Collect static if you are in production environment:

    .. code:: python
    
            python manage.py collectstatic
        
* Clear your browser cache

Documentation
=============
Incoming
