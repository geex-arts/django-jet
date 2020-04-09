from django.views.decorators.http import require_POST, require_GET
from jet.forms import AddBookmarkForm, RemoveBookmarkForm, ToggleApplicationPinForm, ModelLookupForm
from jet.models import Bookmark
from jet.utils import JsonResponse


@require_POST
def add_bookmark_view(request):
    result = {'error': False}
    form = AddBookmarkForm(request, request.POST)

    if form.is_valid():
        bookmark = form.save()
        result.update({
            'id': bookmark.pk,
            'title': bookmark.title,
            'url': bookmark.url
        })
    else:
        result['error'] = True

    return JsonResponse(result)


@require_POST
def remove_bookmark_view(request):
    result = {'error': False}

    try:
        instance = Bookmark.objects.get(pk=request.POST.get('id'))
        form = RemoveBookmarkForm(request, request.POST, instance=instance)

        if form.is_valid():
            form.save()
        else:
            result['error'] = True
    except Bookmark.DoesNotExist:
        result['error'] = True

    return JsonResponse(result)


@require_POST
def toggle_application_pin_view(request):
    result = {'error': False}
    form = ToggleApplicationPinForm(request, request.POST)

    if form.is_valid():
        pinned = form.save()
        result['pinned'] = pinned
    else:
        result['error'] = True

    return JsonResponse(result)


@require_GET
def model_lookup_view(request):
    result = {'error': False}

    form = ModelLookupForm(request, request.GET)

    if form.is_valid():
        items, total = form.lookup()
        result['items'] = items
        result['total'] = total
    else:
        result['error'] = True

    return JsonResponse(result)
