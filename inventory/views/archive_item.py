from pydoc import describe
from unicodedata import category

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from access.models import Category, Color, Size, ClothingItem, ClothingItemImage, Gender

class ArchiveItemView(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('change_item', raise_exception=True))
    def get(self, request, *args, **kwargs):
        item_id = kwargs['pk']
        item = ClothingItem.objects.get(pk=item_id)
        return render(request, 'archive-item.html', {
            'item': item
        })

    @method_decorator(login_required)
    @method_decorator(permission_required('change_item', raise_exception=True))
    def post(self, request, *args, **kwargs):
        item_id = kwargs['pk']
        item = ClothingItem.objects.get(pk=item_id)
        item.availability_status = 'archived'
        item.save()
        return redirect('inventory_view')
