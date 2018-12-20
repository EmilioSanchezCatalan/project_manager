"""
    Configuración de las urls de las vistas asociadas a las vistas publicas
    de TFMs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from tfms.views.views_public import TfmListView, TfmDetailView

urlpatterns = [
    path('', TfmListView.as_view(), name="public_tfms_list"),
    path('<int:pk>', TfmDetailView.as_view(), name="public_tfms_detail"),
]