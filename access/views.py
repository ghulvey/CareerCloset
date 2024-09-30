from datetime import datetime, timezone

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import now
from django.utils import timezone

from access.models import AccessAssignment


def access_list(request):
    context = {
        'invites': AccessAssignment.objects.filter(state='pending'),
        'users': User.objects.filter(is_staff=True)
    }
    return render(request, 'accessList.html', context)


@login_required()
def remove_access(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_staff = False
    user.groups.remove_all()
    user.save()
    return redirect('access_list')