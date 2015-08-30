============
Autocomplete
============

By default Django JET renders all possible choices for select inputs. This behavior may be unwanted if number of
available options is rather big. In this case Django JET allows you to load these options dynamically through AJAX.

In order to achieve this functionality all you have to do is specify which model fields should be
searchable by AJAX queries. Add this static method to your model and that's it!

.. code:: python

    @staticmethod
    def autocomplete_search_fields():
        return 'field1', 'field2'

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

Now all your admin select boxes will perform AJAX queries to load available options while you type.

.. note:: This work for both ForeignKey and ManyToManyField fields.