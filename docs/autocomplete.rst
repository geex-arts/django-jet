============
Autocomplete
============


By default Django JET renders all possible choices for select inputs. This behavior may be unwanted if number of
available options is rather big. In this case Django JET allows you to load these options dynamically through AJAX.

Configuration
-------------

In order to achieve this functionality all you have to do is:

-
    Specify which model fields should be searchable by AJAX queries. Add this static method which must return
    a ``tuple`` or ``list`` of fields you want to be searchable with AJAX:

.. code:: python

    @staticmethod
    def autocomplete_search_fields():
        return 'field1', 'field2'

    # for single field

    @staticmethod
    def autocomplete_search_fields():
        return 'field1',

Example from Django JET demo site:

.. code:: python

    class Address(models.Model):
        name = models.CharField(_('name'), max_length=255)
        city = models.ForeignKey(City, verbose_name=_('city'), related_name='addresses')
        zip = models.IntegerField(_('zip/postal code'))

        class Meta:
            verbose_name = _('address')
            verbose_name_plural = _('addresses')
            unique_together = ('name', 'city')

        def __str__(self):
            return self.name

        @staticmethod
        def autocomplete_search_fields():
            return 'name', 'city__name'

- Use custom AJAX filter class ``jet.filters.RelatedFieldAjaxListFilter`` if you have any foreign key list filters:

.. code:: python

    from jet.filters import RelatedFieldAjaxListFilter

    class PersonAdmin(admin.ModelAdmin):
        list_filter = (
            ...
            ('address', RelatedFieldAjaxListFilter),
        )

- Now all your admin select boxes will perform AJAX queries to load available options while you type.

.. note::
    This works for both ForeignKey and ManyToManyField fields.

Disabling Autocomplete For Form Fields
--------------------------------------

Autocomplete is nice, but sometimes you don't want this behaviour (e.x. because you want to limit the provided
queryset for a particular widget). In this case you can disable autocompletion this way:

    .. code:: python

        class YourForm(forms.ModelForm):
            def __init__(self, *args, **kwargs):
                super(YourForm, self).__init__(*args, **kwargs)
                if SOME_CASE(self.instance):
                    self.fields['FIELD_NAME'].autocomplete = False
                    self.fields['FIELD_NAME'].queryset = Model.queryset.some_filter()
