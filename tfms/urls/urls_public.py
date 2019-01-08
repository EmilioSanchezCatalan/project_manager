"""
    Configuración de las urls de las vistas asociadas a las vistas publicas
    de TFMs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from tfms.views.views_public import TfmListView, TfmDetailView, CentersListView
from tfms.views.views_public import TfmHistoryListView, CentersHistoryListView, TfmHistoryDetailView

urlpatterns = [
    path('centers', CentersListView.as_view(), name="public_centers_tfms_list"),
    path('<int:center_id>', TfmListView.as_view(), name="public_tfms_list"),
    path('details/<int:center_id>/<int:pk>', TfmDetailView.as_view(), name="public_tfms_detail"),
    path('history/centers', CentersHistoryListView.as_view(), name="public_centers_history_tfms_list"),
    path('history/<int:center_id>', TfmHistoryListView.as_view(), name="public_history_tfms_list"),
    path('history/details/<int:center_id>/<int:pk>', TfmHistoryDetailView.as_view(), name="public_history_tfms_detail"),
]
