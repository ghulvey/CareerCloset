from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View

from access.models import AccessAssignment


class RevokeAccessView(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('access.add_invite', raise_exception=True))
    def post(self, request, *args, **kwargs):
        invite = AccessAssignment.objects.get(id=kwargs['pk'])
        user = invite.assigned_user
        group = invite.assigned_group
        invite.state = 'canceled'
        invite.access_expires_at = timezone.now()
        invite.save()
        user.groups.remove(group)
        # Remove the user from the group
        group.user_set.remove(user)
        user.is_superuser = False
        user.is_staff = False
        user.save()
        return redirect('access_list')

    @method_decorator(login_required)
    @method_decorator(permission_required('access.add_invite', raise_exception=True))
    def get(self, request, *args, **kwargs):
        invite = AccessAssignment.objects.get(id=kwargs['pk'])
        return render(request, 'revokeAccess.html', {
            'invite': invite
        })
