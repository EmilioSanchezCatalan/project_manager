from django.urls import path
from .views import AnnounTfgListView, AnnounTfgCreateView, AnnounTfgUpdateView, AnnounTfgDeleteView
from .views import AnnounTfgPublicStatus, AnnounTfgCloseStatus

from .views import AnnounTfmListView 

urlpatterns = [
    path('tfg/', AnnounTfgListView.as_view(), name="announ_tfgs_list"),
    path('tfg/create', AnnounTfgCreateView.as_view(), name="announ_tfgs_create"),
    path('tfg/edit/<int:pk>', AnnounTfgUpdateView.as_view(), name="announ_tfgs_update"),
    path('tfg/delete/<int:id>', AnnounTfgDeleteView.as_view(), name="announ_tfgs_delete"),
    path('tfg/public_status/<int:id>', AnnounTfgPublicStatus.as_view(), name="announ_tfgs_status_public"),
    path('tfg/close_status/<int:id>', AnnounTfgCloseStatus.as_view(), name="announ_tfgs_status_close"),
    path('tfm/', AnnounTfmListView.as_view(), name="announ_tfms_list")
]