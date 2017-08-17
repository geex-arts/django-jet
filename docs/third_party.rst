===============
Third party App
===============

In this section we will treat with a few errors that `django-jet` could be with third party applications:

DJANGO-ROSETTA
--------------

As you can see in [198](https://github.com/geex-arts/django-jet/issues/198) and [207](https://github.com/geex-arts/django-jet/issues/207) issues, `django-jet` have problems with `django-rosetta`, it can't renderize the styles properly.

You can solve it with this [steps](https://github.com/geex-arts/django-jet/issues/198#issuecomment-302629559):

1. Create `templates/rosetta/base.html` file.
2. Add the following content in these file:

.. code:: html/django

    {% extends 'admin/base.html' %}
    {% load static %}

    {% block title %}Rosetta{% endblock %}

    {% block extrastyle %}

    {% endblock %}

    {% block extrahead %}
        <script src="//www.google.com/jsapi" type="text/javascript"></script>
        <script type="text/javascript">
        //<!--
            google.load("jquery", "1.3");
            {% if rosetta_settings.ENABLE_TRANSLATION_SUGGESTIONS %}google.load("language", "1");{% endif %}
            {% include 'rosetta/js/rosetta.js' %}
        //-->
        </script>
    {% endblock %}

    {% block content %}
      <div id="header">
          {% block header %}
          <div id="branding">
              <h1 id="site-name"><a href="{% url 'rosetta-pick-file' %}">Rosetta</a> </h1>
          </div>
          {% endblock %}
      </div>
      <div class="breadcrumbs">{% block breadcumbs %}{% endblock %}</div>
      <div id="content" class="flex">
          {% block main %}{% endblock %}
      </div>
      <div id="footer" class="breadcumbs">
          <a href="https://github.com/mbi/django-rosetta">Rosetta</a> <span class="version">{{version}}</span>
      </div>
    {% endblock %}

3. Save it and refresh the browser, the problem should be fixed now:

.. image:: https://cloud.githubusercontent.com/assets/159728/26557266/e8adcf7c-446d-11e7-8d66-f11cf1edb05e.png
    :width: 500px
    :height: 500px
    :scale: 50%



It's all. Thanks to [Boros Gabór](https://github.com/gabor-boros) for supply this solution.

DJANGO-TREEBEARD
----------------
