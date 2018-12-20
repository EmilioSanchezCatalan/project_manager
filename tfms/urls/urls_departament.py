"""
    Configuración de las urls de las vistas asociadas a los departamentos
    y sus TFMs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from tfms.views.views_departament import DepartamentTfmListView, DepartamentTfmDetailView
from tfms.views.views_departament import DepartamentTfmUpdateView
from tfms.views.views_departament import DepartamentValidationOk, DepartamentValidationError

urlpatterns = [
    path('departament/', DepartamentTfmListView.as_view(), name="departament_tfms_list"),
    path('departament/<int:pk>', DepartamentTfmDetailView.as_view(), name="departament_tfms_detail"),
    path('departament/edit/<int:pk>', DepartamentTfmUpdateView.as_view(), name="departament_tfms_update"),
    path('departament/validation/ok/<int:id>/<int:validate>', DepartamentValidationOk.as_view(), name="departament_tfms_validation_ok"),
    path('departament/validation/error/<int:id>/<int:validate>', DepartamentValidationError.as_view(), name="departament_tfms_validation_error"),
]