from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from access import models

@login_required
def index(request):
    return render(request, 'home.html')


def login(request, *args, **kwargs):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('/admin'))
        else:
            messages.error(request,'username or password not correct')
            return redirect(reverse('/error'))
    else:
        form = AuthenticationForm()
    return render(request,'registration/login.html',{'form':form})


def women(request):
    green_color = models.Color.objects.get(color_name='Green')
    
    green_clothing_items = models.ClothingItem.objects.filter(color=green_color)

    context = {
        'context': green_clothing_items,
    }
    return render(request, 'women.html', context)

def men(request):
    grey_color = models.Color.objects.get(color_name='Grey')
    
    grey_clothing_items = models.ClothingItem.objects.filter(color=grey_color)

    context = {
        'context': grey_clothing_items,
    }
    return render(request, 'men.html', context)
