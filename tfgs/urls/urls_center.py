"""
    Configuración de las urls de las vistas asociadas a los profesores
    y sus TFGs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from tfgs.views.views_center import CenterTfgListView, CenterTfgDetailView
from tfgs.views.views_center import CenterTfgUpdateView
from tfgs.views.views_center import CenterValidationOk, CenterValidationError

urlpatterns = [
    path('center/<int:announ_id>', CenterTfgListView.as_view(), name="center_tfgs_list"),
    path('center/<int:announ_id>/detail/<int:pk>', CenterTfgDetailView.as_view(), name="center_tfgs_detail"),
    path('center/<int:announ_id>/edit/<int:pk>', CenterTfgUpdateView.as_view(), name="center_tfgs_update"),
    path('center/<int:announ_id>/validation/ok/<int:id>/<int:validate>', CenterValidationOk.as_view(), name="center_tfgs_validation_ok"),
    path('center/<int:announ_id>/validation/error/<int:id>/<int:validate>', CenterValidationError.as_view(), name="center_tfgs_validation_error"),
]