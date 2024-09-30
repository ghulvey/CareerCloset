from datetime import timedelta, datetime

from django.contrib.auth.models import Group
from django.db import models
from django.template.defaultfilters import default
from django.template.defaulttags import now
from django.utils.crypto import get_random_string

enum = (
    ('pending', 'Pending'),
    ('applied', 'Applied'),
    ('expired', 'Expired'),
    ('canceled', 'Canceled')
)


class AccessAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    invite_code = models.CharField(max_length=10, unique=True, editable=False)
    state = models.CharField(max_length=10, choices=enum, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invite_expires_at = models.DateTimeField(default=datetime.now() + timedelta(days=7))
    access_expires_at = models.DateTimeField(default=None, null=True)
    assigned_group = models.ForeignKey('auth.Group', on_delete=models.CASCADE, null=True)
    assigned_user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_by', null=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = get_random_string(10)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
