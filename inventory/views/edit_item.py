from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from access.models import ClothingItem, Category, Color, Size, Gender


class EditItem(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('change_clothingitem', raise_exception=True))
    def get(self, request, *args, **kwargs):

        item = ClothingItem.objects.get(clothing_id=kwargs['pk'])

        categories = Category.objects.all()
        colors = Color.objects.all()
        sizes = Size.objects.all()
        genders = Gender.objects.all()

        images = item.images.filter(clothing_item=item)

        return render(request, 'edit-item.html', {
            'item': item,
            'categories': categories,
            'colors': colors,
            'sizes': sizes,
            'genders': genders,
            'images': images
        })