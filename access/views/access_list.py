from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from access.models import AccessAssignment


class AccessList(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('access.view_accessassignment', raise_exception=True))
    def get(self, request, *args, **kwargs):
        context = {
            'invites': AccessAssignment.objects.filter(state='pending'),
            'users': AccessAssignment.objects.filter(state='applied'),
        }
        return render(request, 'access-list.html', context)