from unicodedata import category

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from access.models import Category, Color, Size, ClothingItem, ClothingItemImage


class CreateItem(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('inventory.add_item', raise_exception=True))
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        colors = Color.objects.all()
        sizes = Size.objects.all()
        return render(request, 'create-item.html', {
            'categories': categories,
            'colors': colors,
            'sizes': sizes
        })

    @method_decorator(login_required)
    @method_decorator(permission_required('inventory.add_item', raise_exception=True))
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        category_id = request.POST['category']
        color_id = request.POST['color']
        size_id = request.POST['size']
        image = request.FILES['image']

        category = Category.objects.get(category_id=category_id)
        color = Color.objects.get(color_id=color_id)
        size = Size.objects.get(size_id=size_id)

        # create a new item object
        item = ClothingItem.objects.create(name=name, category=category, color=color, size=size)

        number_of_images = item.images.get(clothing_item=item).count()

        # create a new item image object
        for image in request.FILES:
            file = request.FILES[image]
            if file.type != 'image/jpeg' and file.type != 'image/png':
                continue
            if file.size > 25 * 1024 * 1024: # 25MB
                continue
            if number_of_images > 6:
                break
            ClothingItemImage.objects.create(clothing_item=item, image=file)
            number_of_images += 1

        return redirect('inventory_create')