from importlib import import_module

from django.db.models import Field

from jet import settings


def get_user_field():
    pkg, mod = settings.JET_USER_FIELD.rsplit('.', 1)
    cls = getattr(import_module(pkg), mod)
    assert issubclass(cls, Field), 'JET_USER_FIELD is not instance of Field class'
    return cls


UserField = get_user_field()
