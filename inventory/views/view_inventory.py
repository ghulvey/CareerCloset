from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from access.models import ClothingItem


class ViewInventory(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('view_clothingitem', raise_exception=True))
    def get(self, request):

        items = ClothingItem.objects.all()

        return render(request, 'view-inventory.html', {
            'items': items
        })