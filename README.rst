==========
Django JET
==========

**Modern template for Django admin interface with improved functionality**

Free for non-commercial use. If you would like to use it in commercial project, please email at support@jet.geex-arts.com

.. image:: https://raw.githubusercontent.com/geex-arts/jet/static/logo.png
    :width: 500px
    :height: 500px
    :scale: 50%
    :alt: Screenshot #1
    :align: center
    
* Home page: incoming
* **Live Demo**: http://demo.jet.geex-arts.com/admin/
* PyPI: https://pypi.python.org/pypi/django-jet
* Support: support@jet.geex-arts.com

Screenshots
===========

.. image:: https://raw.githubusercontent.com/geex-arts/jet/static/screen1_720.png
    :alt: Screenshot #1
    :align: center
    :target: https://raw.githubusercontent.com/geex-arts/jet/static/screen1.png
    
.. image:: https://raw.githubusercontent.com/geex-arts/jet/static/screen2_720.png
    :alt: Screenshot #1
    :align: center
    :target: https://raw.githubusercontent.com/geex-arts/jet/static/screen2.png
    
.. image:: https://raw.githubusercontent.com/geex-arts/jet/static/screen3_720.png
    :alt: Screenshot #1
    :align: center
    :target: https://raw.githubusercontent.com/geex-arts/jet/static/screen3.png

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
        
* Make sure 'django.core.context_processors.request' context processor is enabled in settings.py:

    .. code:: python
            
        from django.conf import global_settings
        
        TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
            'django.core.context_processors.request',
        )

* Add URL-pattern to the urlpatterns of your Django project urls.py file (they are needed for related–lookups and autocompletes):

    .. code:: python
    
        urlpatterns = patterns(
            '',
            url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
            url(r'^admin/', include(admin.site.urls)),
            ...
        )

* Create database tables:

    .. code:: python
    
        python manage.py migrate jet
        # or 
        python manage.py syncdb
        
* Collect static if you are in production environment:

    .. code:: python
    
            python manage.py collectstatic
        
* Clear your browser cache

Documentation
=============
Incoming
