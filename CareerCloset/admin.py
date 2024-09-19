from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission


class CareerClosetAdminSite(admin.AdminSite):
    site_header = 'Career Closet'
    site_title = 'Career Closet Administration'
    index_title = 'Welcome to the Career Closet Administration Portal'
    login_template = 'registration/login.html'


admin_site = CareerClosetAdminSite()

admin_site.register(User)
admin_site.register(Group)
admin_site.register(Permission)
