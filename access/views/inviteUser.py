from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.core.mail import send_mail
from CareerCloset import settings

from access.models import Invite


class InviteUser(View):
    template_name = 'inviteUser.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        expiration = request.POST['expDate']
        # create a new invite object
        invite = Invite.objects.create(email=email, access_expires_at=expiration, created_by=request.user)
        print("Invite created for email: ", invite.email, " with code: ", invite.invite_code)
        send_mail(
            'Invitation to Career Closet',
            'You have been granted backend access to Career Closet. Please click the following link to accept the invitation: http://' + request.get_host() + '/auth/access/accept/' + invite.invite_code + '/ . This invitation will expire on ' + invite.invite_expires_at.strftime("%m/%d/%Y, %H:%M:%S") + '.',
            settings.EMAIL_FROM,
            [email]
        )
        return redirect('access_list')
