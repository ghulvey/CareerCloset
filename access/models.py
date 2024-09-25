from datetime import timedelta, datetime

from django.contrib.auth.models import Group
from django.db import models
from django.template.defaultfilters import default
from django.template.defaulttags import now
from django.utils.crypto import get_random_string

enum = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('expired', 'Expired'),
    ('canceled', 'Canceled')
)


class Invite(models.Model):
    email = models.EmailField()
    invite_code = models.CharField(primary_key=True, max_length=10, unique=True, default=get_random_string(10), editable=False)
    state = models.CharField(max_length=10, choices=enum, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invite_expires_at = models.DateTimeField(default=datetime.now() + timedelta(days=7))
    access_expires_at = models.DateTimeField(default=None, null=True)
    assigned_group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True)
    assigned_user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_by', null=True)


    def __str__(self):
        return self.email
