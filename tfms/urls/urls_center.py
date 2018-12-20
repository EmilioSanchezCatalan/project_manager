"""
    Configuración de las urls de las vistas asociadas a los profesores
    y sus TFMs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from tfms.views.views_center import CenterTfmListView, CenterTfmDetailView
from tfms.views.views_center import CenterTfmUpdateView, CenterValidationOk
from tfms.views.views_center import CenterValidationError

urlpatterns = [
    path('center/<int:announ_id>', CenterTfmListView.as_view(), name="center_tfms_list"),
    path('center/<int:announ_id>/detail/<int:pk>', CenterTfmDetailView.as_view(), name="center_tfms_detail"),
    path('center/<int:announ_id>/edit/<int:pk>', CenterTfmUpdateView.as_view(), name="center_tfms_update"),
    path('center/<int:announ_id>/validation/ok/<int:id>/<int:validate>', CenterValidationOk.as_view(), name="center_tfms_validation_ok"),
    path('center/<int:announ_id>/validation/error/<int:id>/<int:validate>', CenterValidationError.as_view(), name="center_tfms_validation_error"),
]