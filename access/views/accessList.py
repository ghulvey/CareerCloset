from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from access.models import Invite


class AccessList(View):
    @method_decorator(login_required)
    @method_decorator(permission_required('access.view_invite', raise_exception=True))
    @staticmethod
    def get(request, *args, **kwargs):
        context = {
            'invites': Invite.objects.filter(state='pending'),
            'users': User.objects.filter(is_staff=True)
        }
        return render(request, 'accessList.html', context)