from django.contrib import messages
from django.core.exceptions import ValidationError
try:
    from django.core.urlresolvers import reverse
except ImportError: # Django 1.11
    from django.urls import reverse

from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST, require_GET
from jet.dashboard.forms import UpdateDashboardModulesForm, AddUserDashboardModuleForm, \
    UpdateDashboardModuleCollapseForm, RemoveDashboardModuleForm, ResetDashboardForm
from jet.dashboard.models import UserDashboardModule
from jet.utils import JsonResponse, get_app_list, SuccessMessageMixin, user_is_authenticated
from django.views.generic import UpdateView
from django.utils.translation import ugettext_lazy as _


class UpdateDashboardModuleView(SuccessMessageMixin, UpdateView):
    model = UserDashboardModule
    fields = ('title',)
    template_name = 'jet.dashboard/update_module.html'
    success_message = _('Widget was successfully updated')
    object = None
    module = None

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def get_success_url(self):
        if self.object.app_label:
            return reverse('admin:app_list', kwargs={'app_label': self.object.app_label})
        else:
            return reverse('admin:index')

    def get_module(self):
        object = self.object if getattr(self, 'object', None) is not None else self.get_object()
        return object.load_module()

    def get_settings_form_kwargs(self):
        kwargs = {
            'initial': self.module.settings
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_settings_form(self):
        if self.module.settings_form:
            form = self.module.settings_form(**self.get_settings_form_kwargs())
            if hasattr(form, 'set_module'):
                form.set_module(self.module)
            return form

    def get_children_formset_kwargs(self):
        kwargs = {
            'initial': self.module.children,
            'prefix': 'children',
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_children_formset(self):
        if self.module.child_form:
            return formset_factory(self.module.child_form, can_delete=True, extra=1)(**self.get_children_formset_kwargs())

    def clean_children_data(self, children):
        children = list(filter(
            lambda item: isinstance(item, dict) and item and item.get('DELETE') is not True,
            children
        ))
        for item in children:
            item.pop('DELETE')
        return children

    def get_current_app(self):
        app_list = get_app_list({'request': self.request})

        for app in app_list:
            if app.get('app_label', app.get('name')) == self.object.app_label:
                return app

    def get_context_data(self, **kwargs):
        data = super(UpdateDashboardModuleView, self).get_context_data(**kwargs)
        data['title'] = _('Change')
        data['module'] = self.module
        data['settings_form'] = self.get_settings_form()
        data['children_formset'] = self.get_children_formset()
        data['child_name'] = self.module.child_name if self.module.child_name else _('Items')
        data['child_name_plural'] = self.module.child_name_plural if self.module.child_name_plural else _('Items')
        data['app'] = self.get_current_app()
        return data

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request):
            index_path = reverse('admin:index')
            return HttpResponseRedirect(index_path)

        self.object = self.get_object()
        self.module = self.get_module()(model=self.object)
        return super(UpdateDashboardModuleView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        settings_form = self.get_settings_form()
        children_formset = self.get_children_formset()

        data = request.POST.copy()

        if settings_form:
            if settings_form.is_valid():
                settings = settings_form.cleaned_data
                data['settings'] = self.module.dump_settings(settings)
            else:
                return self.form_invalid(self.get_form(self.get_form_class()))

        if children_formset:
            if children_formset.is_valid():
                self.module.children = self.clean_children_data(children_formset.cleaned_data)
                data['children'] = self.module.dump_children()
            else:
                return self.form_invalid(self.get_form(self.get_form_class()))

        request.POST = data

        return super(UpdateDashboardModuleView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        if 'settings' in form.data:
            form.instance.settings = form.data['settings']
        if 'children' in form.data:
            form.instance.children = form.data['children']
        return super(UpdateDashboardModuleView, self).form_valid(form)


@require_POST
def update_dashboard_modules_view(request):
    result = {'error': False}
    form = UpdateDashboardModulesForm(request, request.POST)

    if form.is_valid():
        form.save()
    else:
        result['error'] = True

    return JsonResponse(result)


@require_POST
def add_user_dashboard_module_view(request):
    result = {'error': False}
    form = AddUserDashboardModuleForm(request, request.POST)

    if form.is_valid():
        module = form.save()
        result['id'] = module.pk
        messages.success(request, _('Widget has been successfully added'))

        if module.app_label:
            result['success_url'] = reverse('admin:app_list', kwargs={'app_label': module.app_label})
        else:
            result['success_url'] = reverse('admin:index')
    else:
        result['error'] = True

    return JsonResponse(result)


@require_POST
def update_dashboard_module_collapse_view(request):
    result = {'error': False}

    try:
        instance = UserDashboardModule.objects.get(pk=request.POST.get('id'))
        form = UpdateDashboardModuleCollapseForm(request, request.POST, instance=instance)

        if form.is_valid():
            module = form.save()
            result['collapsed'] = module.collapsed
        else:
            result['error'] = True
    except UserDashboardModule.DoesNotExist:
        result['error'] = True

    return JsonResponse(result)


@require_POST
def remove_dashboard_module_view(request):
    result = {'error': False}

    try:
        instance = UserDashboardModule.objects.get(pk=request.POST.get('id'))
        form = RemoveDashboardModuleForm(request, request.POST, instance=instance)

        if form.is_valid():
            form.save()
        else:
            result['error'] = True
    except UserDashboardModule.DoesNotExist:
        result['error'] = True

    return JsonResponse(result)


@require_GET
def load_dashboard_module_view(request, pk):
    result = {'error': False}

    try:
        if not user_is_authenticated(request.user) or not request.user.is_staff:
            raise ValidationError('error')

        instance = UserDashboardModule.objects.get(pk=pk, user=request.user.pk)
        module_cls = instance.load_module()
        module = module_cls(model=instance, context={'request': request})
        result['html'] = module.render()
    except (ValidationError, UserDashboardModule.DoesNotExist):
        result['error'] = True

    return JsonResponse(result)


@require_POST
def reset_dashboard_view(request):
    result = {'error': False}
    form = ResetDashboardForm(request, request.POST)

    if form.is_valid():
        form.save()
    else:
        result['error'] = True

    return JsonResponse(result)
