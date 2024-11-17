from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View

from access.models import AccessAssignment
from common.log_event import log_event


class RevokeAccessView(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('access.delete_accessassignment', raise_exception=True))
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
        log_event('Access', 'Access Revoked', request.user.id, 'Access revoked for ' + user.username)
        return redirect('access_list')

    @method_decorator(login_required)
    @method_decorator(permission_required('access.delete_accessassignment', raise_exception=True))
    def get(self, request, *args, **kwargs):
        invite = AccessAssignment.objects.get(id=kwargs['pk'])
        return render(request, 'revoke-access.html', {
            'invite': invite
        })
