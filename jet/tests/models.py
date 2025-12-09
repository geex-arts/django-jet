from django.db import models


class TestModel(models.Model):
    field1 = models.CharField(max_length=255)
    field2 = models.IntegerField()

    def __str__(self):
        return '%s%d' % (self.field1, self.field2)


class RelatedToTestModel(models.Model):
    field = models.ForeignKey(TestModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.field


class SearchableTestModel(models.Model):
    field1 = models.CharField(max_length=255)
    field2 = models.IntegerField()

    def __str__(self):
        return '%s%d' % (self.field1, self.field2)

    @staticmethod
    def autocomplete_search_fields():
        return 'field1'
