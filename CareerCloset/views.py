from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from access.models import ClothingItem, ShoppingCart


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

def product_list(request):
    products = ClothingItem.objects.all()
    return render(request, 'product_list.html', {'products': products})

def view_cart(request):
    cart_items = ShoppingCart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})

def add_to_cart(request, product_id):
    product = ClothingItem.objects.get(pk=product_id)
    cart_item = ShoppingCart(user=request.user, product=product)
    cart_item.save()
    return redirect(reverse('cart'))

def remove_from_cart(request, cart_id):
    cart_item = ShoppingCart.objects.get(pk=cart_id)
    cart_item.delete()
    return redirect(reverse('cart'))