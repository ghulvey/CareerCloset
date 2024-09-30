from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.core.mail import send_mail
from CareerCloset import settings

from access.models import AccessAssignment
from common.send_email import send_generic_email


class InviteUser(View):
    template_name = 'inviteUser.html'

    @method_decorator(login_required)
    @method_decorator(permission_required('access.add_invite', raise_exception=True))
    def delete(self, request, *args, **kwargs):
        invite_id = request.GET['id']
        invite = AccessAssignment.objects.get(id=invite_id)
        invite.state = 'canceled'
        invite.save()
        return HttpResponse('Invite deleted')

    @method_decorator(login_required)
    @method_decorator(permission_required('access.add_invite', raise_exception=True))
    def get(self, request, *args, **kwargs):
        default_expiration = (timezone.now() + timezone.timedelta(days=180)).strftime('%Y-%m-%d')
        groups = Group.objects.all()
        return render(request, self.template_name, {
            'default_expiration': default_expiration,
            'groups': groups
        })

    @method_decorator(login_required)
    @method_decorator(permission_required('access.add_invite', raise_exception=True))
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        expiration = request.POST['expDate']
        if expiration == '':
            expiration = None
        if request.POST['expDateSet'] == 'false':
            expiration = None
        if request.POST['group'] == '':
            return HttpResponse('Group is required')
        if email == '':
            return HttpResponse('Email is required')
        group_id = request.POST['group']
        group = Group.objects.get(id=group_id)
        # create a new invite object
        invite = AccessAssignment.objects.create(email=email, access_expires_at=expiration, created_by=request.user,
                                                 assigned_group=group)
        invite_link = settings.WEBSITE_URL + '/auth/access/accept/' + invite.invite_code + '/'
        print("Invite created for email: ", invite.email, " with code: ", invite.invite_code)
        send_generic_email(email, 'Invitation to Career Closet', 'You have been granted backend access to Career '
                                                                 'Closet. Please click the following link to accept '
                                                                 'the invitation: <a href="' + invite_link + '">' + invite_link + '</a>. This invitation will expire on ' + invite.invite_expires_at.strftime(
            "%m/%d/%Y, %I:%M %p") + '.')
        return redirect('access_list')
