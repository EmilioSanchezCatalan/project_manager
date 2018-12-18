"""
    Configuración de las urls de las convocatorias.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from announcements.views.views_tfg import AnnounTfgListView, AnnounTfgCreateView
from announcements.views.views_tfg import AnnounTfgUpdateView, AnnounTfgCloseStatus
from announcements.views.views_tfg import AnnounTfgDeleteView, AnnounTfgPublicStatus

urlpatterns = [
    path('', AnnounTfgListView.as_view(), name="announ_tfgs_list"),
    path('create', AnnounTfgCreateView.as_view(), name="announ_tfgs_create"),
    path('edit/<int:pk>', AnnounTfgUpdateView.as_view(), name="announ_tfgs_update"),
    path('delete/<int:id>', AnnounTfgDeleteView.as_view(), name="announ_tfgs_delete"),
    path('public_status/<int:id>', AnnounTfgPublicStatus.as_view(), name="announ_tfgs_status_public"),
    path('close_status/<int:id>', AnnounTfgCloseStatus.as_view(), name="announ_tfgs_status_close"),
]