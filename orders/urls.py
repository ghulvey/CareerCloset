from django.urls import path

import orders.views
import orders.views.order_details
import orders.views.view_orders

urlpatterns = [
    path('', orders.views.view_orders.ViewOrders.as_view(), name='view_orders'),
    path('<str:pk>/', orders.views.order_details.OrderDetails.as_view(), name='view_order'),
    # path('edit/<str:pk>/', orders.views.edit_order.EditOrder.as_view(), name='edit_order'),
    # path('delete/<str:pk>/', orders.views.delete_order.DeleteOrder.as_view(), name='delete_order'),
]