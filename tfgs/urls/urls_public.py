"""
    Configuración de las urls de las vistas asociadas a las vistas publicas
    de TFGs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from tfgs.views.views_public import TfgListView, TfgDetailView, CentersListView
from tfgs.views.views_public import TfgHistoryListView, CentersHistoryListView, TfgHistoryDetailView

urlpatterns = [
    path('centers', CentersListView.as_view(), name="public_centers_tfgs_list"),
    path('<int:center_id>', TfgListView.as_view(), name="public_tfgs_list"),
    path('details/<int:center_id>/<int:pk>', TfgDetailView.as_view(), name="public_tfgs_detail"),
    path('history/centers', CentersHistoryListView.as_view(), name="public_centers_history_tfgs_list"),
    path('history/<int:center_id>', TfgHistoryListView.as_view(), name="public_history_tfgs_list"),
    path('history/details/<int:center_id>/<int:pk>', TfgHistoryDetailView.as_view(), name="public_history_tfgs_detail"),
]
