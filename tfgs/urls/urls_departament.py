"""
    Configuración de las urls de las vistas asociadas a los departamentos
    y sus TFGs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from tfgs.views.views_departament import DepartamentTfgListView, DepartamentTfgDetailView
from tfgs.views.views_departament import DepartamentTfgUpdateView
from tfgs.views.views_departament import DepartamentValidationOk, DepartamentValidationError

urlpatterns = [
    path('departament/', DepartamentTfgListView.as_view(), name="departament_tfgs_list"),
    path('departament/<int:pk>', DepartamentTfgDetailView.as_view(), name="departament_tfgs_detail"),
    path('departament/edit/<int:pk>', DepartamentTfgUpdateView.as_view(), name="departament_tfgs_update"),
    path('departament/validation/ok/<int:id>/<int:validate>', DepartamentValidationOk.as_view(), name="departament_tfgs_validation_ok"),
    path('departament/validation/error/<int:id>/<int:validate>', DepartamentValidationError.as_view(), name="departament_tfgs_validation_error"),
]