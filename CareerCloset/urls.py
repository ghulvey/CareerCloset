"""
URL configuration for CareerCloset project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include

import auth
from CareerCloset.admin import admin_site
from CareerCloset import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin_site.urls),
    path('auth/', include('access.urls')),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('', views.index, name='index'),
    path('women.html', views.women, name='women'),
    path('men.html', views.men, name='men'),
    path('home.html', views.index, name='home'),
]
