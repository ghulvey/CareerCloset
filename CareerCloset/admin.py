﻿from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session

from access.models import Invite


class CareerClosetAdminSite(admin.AdminSite):
    site_header = 'Career Closet'
    site_title = 'Career Closet Administration'
    index_title = 'Welcome to the Career Closet Administration Portal'
    login_template = 'registration/login.html'


admin_site = CareerClosetAdminSite()

admin_site.register(User)
admin_site.register(Group)
admin_site.register(Permission)
admin_site.register(ContentType)
admin_site.register(Session)
admin_site.register(LogEntry)


class InviteAdmin(admin.ModelAdmin):
    list_display = (
        'invite_code', 'email', 'state', 'created_at', 'updated_at', 'invite_expires_at', 'access_expires_at', 'assigned_user',
        'created_by')
    list_filter = (
        'state', 'created_at', 'updated_at', 'invite_expires_at', 'access_expires_at', 'assigned_user', 'created_by')
    search_fields = ('email', 'invite_code', "assigned_user__first_name", "assigned_user__last_name")
    ordering = ('-created_at',)


admin_site.register(Invite, InviteAdmin)