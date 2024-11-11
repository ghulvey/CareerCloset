from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import redirect, render, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from access.models import ClothingItemImage



class DeleteImage(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('access.delete_clothingitem', raise_exception=True))
    def get(self, request, *args, **kwargs):

        image = ClothingItemImage.objects.get(id=kwargs['pk'])

        image.delete()

        return HttpResponse(status=204)
