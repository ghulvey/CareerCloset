from django.urls import path

import inventory.views
from inventory.views import view_inventory, create_item, edit_item, archive_item, delete_image

urlpatterns = [
    path('', inventory.views.view_inventory.ViewInventory.as_view(), name='inventory_view'),
    path('create/', inventory.views.create_item.CreateItem.as_view(), name='inventory_create'),
    path('edit/<str:pk>/', inventory.views.edit_item.EditItem.as_view(), name='inventory_edit'),
    path('archive/<str:pk>/', inventory.views.archive_item.ArchiveItemView.as_view(), name='inventory_archive'),
    path('delete-image/<str:pk>/', inventory.views.delete_image.DeleteImage.as_view(), name='delete_image'),
]