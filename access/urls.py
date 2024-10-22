from django.urls import path, include

import access.views
from access.views import accept_invite, invite_user, access_list, delete_invite, revoke_access, change_permissions
from . import views


urlpatterns = [
    path('access/', access.views.access_list.AccessList.as_view(), name='access_list'),
    path('access/invite/', access.views.invite_user.InviteUser.as_view(), name='invite_user'),
    path('access/accept/<str:invite_code>/', access.views.accept_invite.AcceptInvite.as_view(), name='accept_invite'),
    path('access/delete-invite/<str:pk>/', access.views.delete_invite.DeleteInvite.as_view(), name='delete_invite'),
    path('access/revoke/<str:pk>/', access.views.revoke_access.RevokeAccessView.as_view(), name='revoke_access'),
    path('access/change/<str:pk>/', access.views.change_permissions.ChangePermissions.as_view(), name='change_permissions'),
    path('', include('cart.urls')),
    path('', views.product_list, name='product_list'),
    path('/home',views.home, name='home'),
    path('/cart',views.view_cart, name='cart'),
    path('/add-to-cart/<int:product_id>',views.add_to_cart, name='add_to_cart'),
    path('/remove-from-cart/<int:cart_id>',views.remove_from_cart, name='remove_from_cart'),
]
