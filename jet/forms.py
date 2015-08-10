import json
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model
import operator
from jet.models import Bookmark, PinnedApplication, UserDashboardModule
from jet.utils import get_current_dashboard, get_model_instance_label
from functools import reduce


class AddBookmarkForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(AddBookmarkForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bookmark
        fields = ['url', 'title']

    def save(self, commit=True):
        self.instance.user = self.request.user.pk
        return super(AddBookmarkForm, self).save(commit)


class RemoveBookmarkForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(RemoveBookmarkForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bookmark
        fields = []

    def clean(self):
        cleaned_data = super(RemoveBookmarkForm, self).clean()

        if self.instance.user != self.request.user.pk:
            raise ValidationError('error')

        return cleaned_data

    def save(self, commit=True):
        if commit:
            self.instance.delete()


class ToggleApplicationPinForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ToggleApplicationPinForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PinnedApplication
        fields = ['app_label']

    def save(self, commit=True):
        if commit:
            try:
                pinned_app = PinnedApplication.objects.get(
                    app_label=self.cleaned_data['app_label'],
                    user=self.request.user.pk
                )
                pinned_app.delete()
                return False
            except PinnedApplication.DoesNotExist:
                PinnedApplication.objects.create(
                    app_label=self.cleaned_data['app_label'],
                    user=self.request.user.pk
                )
                return True


class UpdateDashboardModulesForm(forms.Form):
    app_label = forms.CharField(required=False)
    modules = forms.CharField()
    modules_objects = []

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(UpdateDashboardModulesForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(UpdateDashboardModulesForm, self).clean()

        try:
            modules = json.loads(data['modules'])

            for module in modules:
                db_module = UserDashboardModule.objects.get(
                    user=self.request.user.pk,
                    app_label=data['app_label'] if data['app_label'] else None,
                    pk=module['id']
                )

                column = module['column']
                order = module['order']

                if db_module.column != column or db_module.order != order:
                    db_module.column = column
                    db_module.order = order

                    self.modules_objects.append(db_module)
        except Exception:
            raise ValidationError('error')

        return data

    def save(self):
        for module in self.modules_objects:
            module.save()


class AddUserDashboardModuleForm(forms.ModelForm):
    type = forms.CharField()
    module = forms.IntegerField()
    module_cls = None

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(AddUserDashboardModuleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserDashboardModule
        fields = ['app_label']

    def clean_app_label(self):
        data = self.cleaned_data['app_label']
        return data if data != '' else None

    def clean(self):
        data = super(AddUserDashboardModuleForm, self).clean()

        index_dashboard_cls = get_current_dashboard('app_index' if data['app_label'] else 'index')
        index_dashboard = index_dashboard_cls({'request': self.request}, app_label=data['app_label'])

        if data['type'] == 'children':
            module = index_dashboard.children[data['module']]
        elif data['type'] == 'available_children':
            module = index_dashboard.available_children[data['module']]()
        else:
            raise ValidationError('error')

        self.module_cls = module
        return data

    def save(self, commit=True):
        self.instance.title = self.module_cls.title
        self.instance.module = self.module_cls.fullname()
        self.instance.user = self.request.user.pk
        self.instance.column = 0
        self.instance.order = -1
        self.instance.settings = self.module_cls.dump_settings()
        self.instance.children = self.module_cls.dump_children()

        return super(AddUserDashboardModuleForm, self).save(commit)


class UpdateDashboardModuleCollapseForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(UpdateDashboardModuleCollapseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserDashboardModule
        fields = ['collapsed']

    def clean(self):
        data = super(UpdateDashboardModuleCollapseForm, self).clean()

        if self.instance.user != self.request.user.pk:
            raise ValidationError('error')

        return data


class RemoveDashboardModuleForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(RemoveDashboardModuleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserDashboardModule
        fields = []

    def clean(self):
        cleaned_data = super(RemoveDashboardModuleForm, self).clean()

        if self.instance.user != self.request.user.pk:
            raise ValidationError('error')

        return cleaned_data

    def save(self, commit=True):
        if commit:
            self.instance.delete()


class ModelLookupForm(forms.Form):
    app_label = forms.CharField()
    model = forms.CharField()
    q = forms.CharField(required=False)
    page = forms.IntegerField(required=False)
    page_size = forms.IntegerField(required=False, min_value=1, max_value=1000)
    object_id = forms.IntegerField(required=False)
    model_cls = None

    def clean(self):
        data = super(ModelLookupForm, self).clean()

        try:
            self.model_cls = get_model(data['app_label'], data['model'])
        except:
            raise ValidationError('error')

        return data

    def lookup(self):
        qs = self.model_cls.objects

        if self.cleaned_data['q']:
            if getattr(self.model_cls, 'autocomplete_search_fields', None):
                search_fields = self.model_cls.autocomplete_search_fields()
                filter_data = [Q((field + '__icontains', self.cleaned_data['q'])) for field in search_fields]
                # if self.cleaned_data['object_id']:
                #     filter_data.append(Q(pk=self.cleaned_data['object_id']))
                qs = qs.filter(reduce(operator.or_, filter_data))
            else:
                qs = qs.none()

        limit = self.cleaned_data['page_size'] or 100
        page = self.cleaned_data['page'] or 1
        offset = (page - 1) * limit

        items = list(map(
            lambda instance: {'id': instance.pk, 'text': get_model_instance_label(instance)},
            qs.all()[offset:offset + limit]
        ))
        total = qs.count()

        return items, total