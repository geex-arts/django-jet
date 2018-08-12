import json
from django import forms
from django.core.exceptions import ValidationError
from jet.dashboard.models import UserDashboardModule
from jet.dashboard.utils import get_current_dashboard
from jet.utils import user_is_authenticated


class UpdateDashboardModulesForm(forms.Form):
    app_label = forms.CharField(required=False)
    modules = forms.CharField()
    modules_objects = []

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(UpdateDashboardModulesForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(UpdateDashboardModulesForm, self).clean()

        if not user_is_authenticated(self.request.user) or not self.request.user.is_staff:
            raise ValidationError('error')

        try:
            modules = json.loads(data['modules'])

            for module in modules:
                db_module = UserDashboardModule.objects.get(
                    user=self.request.user,
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

        if not user_is_authenticated(self.request.user) or not self.request.user.is_staff:
            raise ValidationError('error')

        if 'app_label' in data:
            index_dashboard_cls = get_current_dashboard('app_index' if data['app_label'] else 'index')
            index_dashboard = index_dashboard_cls({'request': self.request}, app_label=data['app_label'])

            if 'type' in data:
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
        self.instance.user = self.request.user
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

        if not user_is_authenticated(self.request.user) or not self.request.user.is_staff:
            raise ValidationError('error')

        if self.instance.user != self.request.user:
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

        if not user_is_authenticated(self.request.user) or self.instance.user != self.request.user:
            raise ValidationError('error')

        return cleaned_data

    def save(self, commit=True):
        if commit:
            self.instance.delete()


class ResetDashboardForm(forms.Form):
    app_label = forms.CharField(required=False)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ResetDashboardForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserDashboardModule
        fields = []

    def clean(self):
        data = super(ResetDashboardForm, self).clean()
        data['app_label'] = data['app_label'] if data['app_label'] else None

        if not user_is_authenticated(self.request.user) or not self.request.user.is_staff:
            raise ValidationError('error')

        return data

    def save(self, commit=True):
        if commit:
            UserDashboardModule.objects.filter(
                user=self.request.user,
                app_label=self.cleaned_data['app_label']
            ).delete()
