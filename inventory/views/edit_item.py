from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from access.models import ClothingItem, Category, Color, Size, Gender, ClothingItemImage
from common.log_event import log_event


class EditItem(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('access.change_clothingitem', raise_exception=True))
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
    
    @method_decorator(login_required)
    @method_decorator(permission_required('access.change_clothingitem', raise_exception=True))
    def post(self, request, *args, **kwargs):

        item = ClothingItem.objects.get(clothing_id=kwargs['pk'])

        name = request.POST['name']
        description = request.POST['description']
        category_id = request.POST['category']
        color_id = request.POST['color']
        size_id = request.POST['size']

        category = Category.objects.get(category_id=category_id)
        color = Color.objects.get(color_id=color_id)
        size = Size.objects.get(size_id=size_id)

        item.name = name
        item.description = description
        item.category = category
        item.color = color
        item.size = size

        number_of_images = item.images.count()

        # create a new item image object
        for image in request.FILES:
            file = request.FILES[image]
            if file.size > 25 * 1024 * 1024:  # 25MB
                continue
            if number_of_images > 6:
                break
            image = ClothingItemImage.objects.create(clothing_item=item, image=file, index=number_of_images)
            item.images.add(image)
            number_of_images += 1

        item.save()

        log_event('Inventory', 'Item Edited', request.user.id, 'Item edited: ' + item.clothing_id)
        return redirect('inventory_view')