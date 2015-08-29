from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TestModel(models.Model):
    field1 = models.CharField(max_length=255)
    field2 = models.IntegerField()

    def __str__(self):
        return '%s%d' % (self.field1, self.field2)
