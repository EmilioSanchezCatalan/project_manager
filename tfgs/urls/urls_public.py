"""
    Configuración de las urls de las vistas asociadas a las vistas publicas
    de TFGs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from tfgs.views.views_public import TfgListView, TfgDetailView

urlpatterns = [
    path('', TfgListView.as_view(), name="public_tfgs_list"),
    path('<int:pk>', TfgDetailView.as_view(), name="public_tfgs_detail"),
]