from datetime import timedelta, datetime

from django.contrib.auth.models import Group, User
from django.db import models
from django.template.defaultfilters import default
from django.template.defaulttags import now
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.file_storage import get_random_filename

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
    invite_expires_at = models.DateTimeField(default=None, null=True)
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

# Size Model
class Size(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_value = models.CharField(max_length=10)

    def __str__(self):
        return self.size_value

# Gender Model
class Gender(models.Model):
    gender_id = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=50, default='Genderless')

    def __str__(self):
        return self.gender_name

# Color Model
class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    color_name = models.CharField(max_length=50)

    def __str__(self):
        return self.color_name


# Category Model
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

availability_statuses = (
    ('available', 'Available'),
    ('on_order', 'On Order'),
    ('ready_for_pickup', 'Ready for Pickup'),
    ('picked_up', 'Picked Up'),
    ('archived', 'Archived'),
)


# ClothingItem Model
class ClothingItem(models.Model):
    clothing_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)  # ForeignKey to Size
    color = models.ForeignKey(Color, on_delete=models.CASCADE)  # ForeignKey to Color
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ForeignKey to Category
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, default=1)
    availability_status = models.CharField(max_length=50, choices=availability_statuses, default='available')
    date_added = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField('ClothingItemImage', related_name='clothing_images', blank=True)

    def __str__(self):
        return self.name

class ClothingItemImage(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='clothing_images')
    image = models.ImageField(upload_to=get_random_filename)
    index = models.IntegerField(default=0)

    def __str__(self):
        return self.clothing_item.name

# User (for identification only)
class Customer(models.Model):
    id = models.AutoField(primary_key=True, default=1)  # Manually define a default value
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.user.username} - {self.email}"

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, email=instance.email)

@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    instance.customer.save()

# Transaction Model
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)  # ForeignKey to User for identification
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)  # ForeignKey to ClothingItem
    transaction_date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Transaction {self.transaction_id}: {self.user.email} - {self.clothing_item.name} on {self.transaction_date}"
    

pickup_methods = (
    ('self', 'Self Pickup'),
    ('desk', 'Pickup at Desk'),
)

order_statuses = (
    ('pending', 'Pending'),
    ('processed', 'Processed'),
    ('picked_up', 'Picked Up'),
    ('canceled', 'Canceled'),
)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_status = models.CharField(max_length=50, choices=order_statuses, default='pending')
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True)
    transactions = models.ManyToOneRel(Transaction, field_name='order', related_name='transactions', to='access.Transaction')
    expiration_date = models.DateTimeField(blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)

    pickup_method = models.CharField(max_length=50, choices=pickup_methods, default='desk')
    pickup_notes = models.TextField(blank=True)
    pickup_code = models.CharField(max_length=10, blank=True)

    order_processed_at = models.DateTimeField(blank=True, null=True)
    order_picked_up_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.order_id}: {self.user.email} on {self.order_date}"

class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    clothing_item = models.OneToOneField(ClothingItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.clothing_item.name} in cart {self.cart.id}"
