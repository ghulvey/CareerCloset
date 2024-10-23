from django.urls import path

import inventory.views.create_item

urlpatterns = [
    path('create/', inventory.views.create_item.CreateItem.as_view(), name='inventory_create'),
]