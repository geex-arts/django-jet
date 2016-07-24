from django.contrib import admin
from jet.tests.models import TestModel


class TestModelAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2')

admin.site.register(TestModel, TestModelAdmin)
