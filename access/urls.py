from django.urls import path

import access.views
from access.views import acceptInvite, inviteUser, accessList, deleteInvite, revokeAccess, changePermissions


urlpatterns = [
    path('access/', access.views.accessList.AccessList.as_view(), name='access_list'),
    path('access/invite/', access.views.inviteUser.InviteUser.as_view(), name='invite_user'),
    path('access/accept/<str:invite_code>/', access.views.acceptInvite.AcceptInvite.as_view(), name='accept_invite'),
    path('access/delete-invite/<str:pk>/', access.views.deleteInvite.DeleteInvite.as_view(), name='delete_invite'),
    path('access/revoke/<str:pk>/', access.views.revokeAccess.RevokeAccessView.as_view(), name='revoke_access'),
    path('access/change/<str:pk>/', access.views.changePermissions.ChangePermissions.as_view(), name='change_permissions'),
]
