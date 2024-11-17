from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from access.models import AccessAssignment
from common.log_event import log_event


class DeleteInvite(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('access.delete_accessassignment', raise_exception=True))
    def get(self, request, *args, **kwargs):
        invite = get_object_or_404(AccessAssignment, pk=kwargs['pk'])
        return render(request, 'delete-invite.html', {'invite': invite})

    @method_decorator(login_required)
    @method_decorator(permission_required('access.delete_accessassignment', raise_exception=True))
    def post(self, request, *args, **kwargs):
        invite = get_object_or_404(AccessAssignment, pk=kwargs['pk'])
        invite.state = 'canceled'
        invite.save()
        log_event('Access', 'Invite Deleted', request.user.id, 'Invite deleted for ' + invite.email)
        return redirect('access_list')
