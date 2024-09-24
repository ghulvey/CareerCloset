from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.utils.decorators import method_decorator

from access.models import Invite


class AcceptInvite(View):
    @method_decorator(login_required)
    def get(self, request, invite_code=None, *args, **kwargs):
        invite = Invite.objects.get(invite_code=invite_code)
        if invite.state != 'pending':
            return HttpResponse('Invite is not pending')
        if invite.invite_expires_at < timezone.now():
            return HttpResponse('Invite has expired')
        if invite.email != request.user.email:
            return HttpResponse('Invite email does not match user email')
        user = request.user
        invite.state = 'accepted'
        invite.assigned_user = request.user
        # set user to staff and add to group
        user.is_staff = True
        user.groups.clear()
        user.groups.add(invite.assigned_group)

        if invite.assigned_group.name == 'Admin':
            user.is_superuser = True
        else:
            user.is_superuser = False

        # execute in a transaction
        try:
            with transaction.atomic():
                invite.save()
                user.save()
        except Exception as e:
            print(e)
            return 'Error accepting invite'
        # logout user, fields are not updated until next login
        logout(request)
        return redirect('index')
