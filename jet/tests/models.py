from django.db import models
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class TestModel(models.Model):
    field1 = models.CharField(max_length=255)
    field2 = models.IntegerField()

    def __str__(self):
        return '%s%d' % (self.field1, self.field2)


@python_2_unicode_compatible
class RelatedToTestModel(models.Model):
    field = models.ForeignKey(TestModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.field


@python_2_unicode_compatible
class SearchableTestModel(models.Model):
    field1 = models.CharField(max_length=255)
    field2 = models.IntegerField()

    def __str__(self):
        return '%s%d' % (self.field1, self.field2)

    @staticmethod
    def autocomplete_search_fields():
        return 'field1'
