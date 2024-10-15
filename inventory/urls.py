from django.urls import path

import inventory.views.create_item
import inventory.views.view_inventory
import inventory.views.edit_item

urlpatterns = [
    path('', inventory.views.view_inventory.ViewInventory.as_view(), name='inventory_view'),
    path('create/', inventory.views.create_item.CreateItem.as_view(), name='inventory_create'),
    path('edit/<str:pk>/', inventory.views.edit_item.EditItem.as_view(), name='inventory_edit'),
]