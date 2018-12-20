"""
    Configuración de las urls de las convocatorias.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from announcements.views.views_tfm import AnnounTfmListView, AnnounTfmCreateView
from announcements.views.views_tfm import AnnounTfmUpdateView, AnnounTfmCloseStatus
from announcements.views.views_tfm import AnnounTfmDeleteView, AnnounTfmPublicStatus

urlpatterns = [
    path('', AnnounTfmListView.as_view(), name="announ_tfms_list"),
    path('create', AnnounTfmCreateView.as_view(), name="announ_tfms_create"),
    path('edit/<int:pk>', AnnounTfmUpdateView.as_view(), name="announ_tfms_update"),
    path('delete/<int:id>', AnnounTfmDeleteView.as_view(), name="announ_tfms_delete"),
    path('public_status/<int:id>', AnnounTfmPublicStatus.as_view(), name="announ_tfms_status_public"),
    path('close_status/<int:id>', AnnounTfmCloseStatus.as_view(), name="announ_tfms_status_close"),
]