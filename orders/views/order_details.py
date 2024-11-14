from datetime import timedelta, timezone
import random
import string
import django
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from access.models import Order, Transaction, ClothingItemImage
from common.send_email import send_generic_email

class OrderDetails(View):

    @method_decorator(login_required)
    @method_decorator(permission_required('access.change_order', raise_exception=True))
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, order_id=kwargs['pk'])

        items = Transaction.objects.filter(order=order.order_id)

        result = []

        for item in items:

            images = ClothingItemImage.objects.filter(clothing_item=item.clothing_item)

            image_url = None

            if images:
                image_url = images[0].image.url


            result.append({
                'id': item.clothing_item.clothing_id,
                'image': image_url,
                'category': item.clothing_item.category,
                'color': item.clothing_item.color,
            })


        return render(request, 'order-details.html', {
            'order': order,
            'items': result
        })
    
    @method_decorator(login_required)
    @method_decorator(permission_required('access.view_order', raise_exception=True))
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, order_id=kwargs['pk'])

        if request.POST['action'] == 'cancel':
            order.order_status = 'canceled'

            for transaction in Transaction.objects.filter(order=order.order_id):
                transaction.clothing_item.availability_status = 'available'
                transaction.clothing_item.save()

            order.save()

            send_generic_email(order.user.email, 'Career Closet Order', 'Your order from the Kent State Career Closet has been canceled. This may be because you have not picked up your order within 7 days or requested the order be cancelled. If this is not the case please check for an email sent from our staff, they will provide explanation on why the order could not be completed. If you have any questions please feel free to contact the Career Service office.')

        elif request.POST['action'] == 'ready':
            order.order_status = 'processed'
            order.order_processed_at = django.utils.timezone.now()
            order.expiration_date = django.utils.timezone.now() + timedelta(days=7)

            order.pickup_method =  'self' if request.POST['pickup_type'] == 'self_serve' else 'desk'

            if order.pickup_method == 'self':
                order.pickup_code = request.POST['pickup_box']
                send_generic_email(order.user.email, 'Career Closet Order', 'Your order from the Kent State Career Closet is ready for pickup. You will be able to use contactless pickup. When you arrive to our office look for the Career Closet pickup boxes. Your order will be in box: ' + order.pickup_code + '. Please pickup your order within 7 days. Orders may be returned back to inventory after 7 days. If you have any questions please feel free to contact the Career Service office.')
            else:
                order.pickup_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
                send_generic_email(order.user.email, 'Career Closet Order', 'Your order from the Kent State Career Closet is ready for pickup. Your order will be at the front desk in Career Services. When you arrive to our office tell the receptionist you are here to pickup a Career Closet order. Give them your order code: ' + order.pickup_code + '. Please pickup your order within 7 days. Orders may be returned back to inventory after 7 days. If you have any questions please feel free to contact the Career Service office.')

            for transaction in Transaction.objects.filter(order=order.order_id):
                transaction.clothing_item.availability_status = 'ready_for_pickup'
                transaction.clothing_item.save()

            order.save()

        elif request.POST['action'] == 'picked_up':
            order.order_status = 'picked_up'
            order.order_picked_up_at = django.utils.timezone.now()

            send_generic_email(order.user.email, 'Career Closet Order', 'Your order from the Kent State Career Closet has been picked up. If you have any questions please feel free to contact the Career Service office.')


            for transaction in Transaction.objects.filter(order=order.order_id):
                transaction.clothing_item.availability_status = 'picked_up'
                transaction.clothing_item.save()

            order.save()

        return redirect('view_order', pk=order.order_id)