from django.urls import path

import access.views
from access.views import acceptInvite, inviteUser, accessList


urlpatterns = [
    path('access/', access.views.accessList.AccessList.as_view(), name='access_list'),
    path('access/invite/', access.views.inviteUser.InviteUser.as_view(), name='invite_user'),
    path('access/accept/<str:invite_code>/', access.views.acceptInvite.AcceptInvite.as_view(), name='accept_invite'),
]
