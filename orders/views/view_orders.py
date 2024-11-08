from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from access.models import Order

class ViewOrders(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('view_order', raise_exception=True))
    def get(self, request):

        pending_orders = Order.objects.filter(order_status='pending')

        pickup_orders = Order.objects.filter(order_status='processed')

        return render(request, 'view-orders.html', {
            'pending_orders': pending_orders,
            'pickup_orders': pickup_orders
        })
    