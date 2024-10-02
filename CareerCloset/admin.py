from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session

from access.models import AccessAssignment, Size, Color, Category, ClothingItem, Customer, Transaction

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
admin_site.register(Size)
admin_site.register(Color)
admin_site.register(Category)
admin_site.register(ClothingItem)
admin_site.register(Customer)
admin_site.register(Transaction)


class InviteAdmin(admin.ModelAdmin):
    list_display = (
        'invite_code', 'email', 'state', 'assigned_group', 'created_at', 'updated_at', 'invite_expires_at', 'access_expires_at', 'assigned_user',
        'created_by')
    list_filter = (
        'state', 'created_at', 'updated_at', 'invite_expires_at', 'access_expires_at', 'assigned_user', 'created_by')
    search_fields = ('email', 'invite_code', "assigned_user__first_name", "assigned_user__last_name")
    ordering = ('-created_at',)


admin_site.register(AccessAssignment, InviteAdmin)
