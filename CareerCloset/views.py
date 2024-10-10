from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


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

items = [
    {'name': 'Product 1', 'description': 'Description of product 1', 'price': 29.99},
    {'name': 'Product 2', 'description': 'Description of product 2', 'price': 49.99},
    {'name': 'Product 3', 'description': 'Description of product 3', 'price': 19.99},
]

def women_view(request):
    # Pass the items to the template
    context = {'items': items}
    return render(request, 'women.html', context)