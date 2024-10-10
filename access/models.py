from datetime import timedelta, datetime

from django.contrib.auth.models import Group
from django.db import models
from django.template.defaultfilters import default
from django.template.defaulttags import now
from django.utils.crypto import get_random_string

from common.file_storage import MediaStorage

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

# Size Model
class Size(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_value = models.CharField(max_length=10)

    def __str__(self):
        return self.size_value


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


# ClothingItem Model
class ClothingItem(models.Model):
    clothing_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)  # ForeignKey to Size
    color = models.ForeignKey(Color, on_delete=models.CASCADE)  # ForeignKey to Color
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ForeignKey to Category
    availability_status = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField('ClothingItemImage', related_name='images')

    def __str__(self):
        return self.name

class ClothingItemImage(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='inventory', storage=MediaStorage())

    def __str__(self):
        return self.clothing_item.name

# User (for identification only)
class Customer(models.Model):
    user_id = models.AutoField(primary_key=True)  # Random identifier or confirmation number
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.email} - {self.user_id}"


# Transaction Model
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)  # ForeignKey to User for identification
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)  # ForeignKey to ClothingItem
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id}: {self.user.email} - {self.clothing_item.name} on {self.transaction_date}"
