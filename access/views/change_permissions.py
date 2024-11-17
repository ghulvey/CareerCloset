from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View

from access.models import AccessAssignment
from common.log_event import log_event


class ChangePermissions(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('access.update_accessassignment', raise_exception=True))
    def post(self, request, *args, **kwargs):
        invite = AccessAssignment.objects.get(id=kwargs['pk'])
        user = invite.assigned_user
        # Edit the AccessAssignment group and expiration date
        group = Group.objects.get(id=request.POST['group'])
        invite.assigned_group = group
        expire = request.POST['expDate']
        expire_set = request.POST['expDateSet']
        if expire_set == 'false' or expire == '':
            invite.access_expires_at = None
        else:
            invite.access_expires_at = expire
        invite.save()
        # Edit the user group and permissions
        user.is_superuser = False
        user.is_staff = True
        user.groups.clear()
        user.groups.add(group)
        if invite.assigned_group.name == 'Admin':
            user.is_superuser = True
        else:
            user.is_superuser = False
        user.save()
        log_event('Access', 'Permissions Changed', request.user.id, 'Permissions changed for ' + user.username + ' to ' + group.name)
        return redirect('access_list')

    @method_decorator(login_required)
    @method_decorator(permission_required('access.update_accessassignment', raise_exception=True))
    def get(self, request, *args, **kwargs):
        invite = AccessAssignment.objects.get(id=kwargs['pk'])
        return render(request, 'change-permissions.html', {
            'invite': invite,
            'groups': Group.objects.all()
        })
