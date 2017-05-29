=======
Filters
=======

RelatedFieldAjaxListFilter
--------------------------

See :doc:`autocomplete` documentation for details.

django-admin-rangefilter
------------------------

In order to fix compatibility issues with ``django-admin-rangefilter`` package you should use JET's admin filter class
``jet.filters.DateRangeFilter`` instead of ``rangefilter.filter.DateRangeFilter``.

.. code:: python

    #from rangefilter.filter import DateRangeFilter
    from jet.filters import DateRangeFilter


    class MyUserAdmin(UserAdmin):
        ...
        list_filter = (
            ('date_joined', DateRangeFilter),
        )
