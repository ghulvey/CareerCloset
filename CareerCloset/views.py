from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from access import models
from access.models import Cart, CartItem, ClothingItem, Transaction, Customer, Favorite, FavoriteItem
from django.contrib.auth.models import Permission

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
    women_gender = models.Gender.objects.get(gender_name="Female")
    genderless = models.Gender.objects.get(gender_name = "Genderless")
    women_clothing_items = models.ClothingItem.objects.filter(gender=women_gender, availability_status="available").prefetch_related('images')
    women_clothing_items |= models.ClothingItem.objects.filter(gender=genderless, availability_status="available").prefetch_related('images')


    context = {
        'context': women_clothing_items,
    }
    return render(request, 'women.html', context)

def men(request):
    men_gender = models.Gender.objects.get(gender_name="Men")
    genderless = models.Gender.objects.get(gender_name="Genderless")
    men_clothing_items = models.ClothingItem.objects.filter(gender=men_gender, availability_status="available").prefetch_related('images')
    men_clothing_items |= models.ClothingItem.objects.filter(gender=genderless, availability_status="available").prefetch_related('images')
    
    context = {
        'context': men_clothing_items,
    }
    return render(request, 'men.html', context)

def clothing_item_detail(request, clothing_id):
    clothing_item = get_object_or_404(ClothingItem, pk=clothing_id)
    images = clothing_item.images.all() 

    context = {
        'clothing_item': clothing_item,
        'images': images,
    }
    return render(request, 'clothing_item_detail.html', context)

"""
@login_required
def add_to_favorites(request, clothing_id):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    
    # Get the Customer instance associated with the logged-in user
    customer = get_object_or_404(Customer, user=request.user)
    
    # Get the ClothingItem instance by clothing_id
    clothing_item = get_object_or_404(ClothingItem, clothing_id=clothing_id)
    
    # Add the clothing item to favorites (if not already in favorites)
    favorite, created = Favorite.objects.get_or_create(customer=customer, clothing_item=clothing_item)
    
    # Redirect to favorites page or any other page as needed
    return redirect('favorites')
"""

@login_required
def add_to_favorites(request, clothing_id):
    # Get the Customer profile associated with the current user
    customer = get_object_or_404(Customer, user=request.user)
    favorite, created = Favorite.objects.get_or_create(user=customer)
    clothing_item = get_object_or_404(ClothingItem, pk=clothing_id)

    # Check if the item is already in the cart
    if Favorite.objects.filter(favorite=favorite, clothing_item=clothing_item).exists():
        messages.info(request, "This item is already in your favorites.")
    else:
        # Add item to cart if not already present
        Favorite.objects.create(favorite=favorite, clothing_item=clothing_item)
        messages.success(request, "Item added to favoroite.")

    return redirect("view_cart")

@login_required
def view_favorites(request):
    # Get the Customer instance associated with the logged-in User
    customer = get_object_or_404(Customer, user=request.user)
    
    # Fetch all favorited items for the Customer
    favorites = Favorite.objects.filter(user=customer)

    return render(request, 'favorites/view_favorites.html', {'favorites': favorites})

@login_required
def remove_from_favorites(request, clothing_id):
    favorite = get_object_or_404(Favorite, user=request.user)
    clothing_item = get_object_or_404(ClothingItem, pk=clothing_id)

    # Remove item from favorites
    if favorite.clothing_items.filter(pk=clothing_item.pk).exists():
        favorite.clothing_items.remove(clothing_item)
        messages.success(request, "Item removed from favorites.")
    else:
        messages.info(request, "This item is not in your favorites.")

    return redirect("view_favorites")

@login_required
def add_to_cart(request, clothing_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    clothing_item = get_object_or_404(ClothingItem, pk=clothing_id)

    # Check if the item is already in the cart
    if CartItem.objects.filter(cart=cart, clothing_item=clothing_item).exists():
        messages.info(request, "This item is already in your cart.")
    else:
        # Add item to cart if not already present
        CartItem.objects.create(cart=cart, clothing_item=clothing_item)
        messages.success(request, "Item added to cart.")

    return redirect("view_cart")

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/view_cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, cart_item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect("view_cart")


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    order = models.Order.objects.create(user=request.user)

    for item in cart.items.all():
        item.clothing_item.availability_status = 'on_order'
        Transaction.objects.create(user=request.user, clothing_item=item.clothing_item, order=order)
        item.clothing_item.save()

    cart.items.all().delete()
    return render(request, "cart/checkout.html")

@login_required
@permission_required('access.view_order')
def backend_home(request):

    permissions = request.user.get_all_permissions()
    
    access_permission = 'access.view_accessassignment' in permissions
    order_permission = 'access.view_order' in permissions
    inventory_permission = 'access.view_clothingitem' in permissions
    django_admin_permission = request.user.is_superuser

    context = {
        'access_permission': access_permission,
        'order_permission': order_permission,
        'inventory_permission': inventory_permission,
        'django_admin_permission': django_admin_permission,
    }
    return render(request, 'backend-home.html', context)