from django.urls import path
from .views import TfgListView, TfgDetailView, TeacherTfgListView, TeacherTfgDetailView
from .views import TeacherTfgCreateView, TfgUpdateView, TeacherTfgDeleteView
from .views import DepartamentTfgListView, DepartamentTfgDetailView, DepartamentValidation

urlpatterns = [
    path('', TfgListView.as_view(), name="public_tfgs_list"),
    path('<int:pk>', TfgDetailView.as_view(), name="public_tfgs_detail"),
    path('teacher/', TeacherTfgListView.as_view(), name="teacher_tfgs_list" ),
    path('teacher/<int:pk>', TeacherTfgDetailView.as_view(), name="teacher_tfgs_detail"),
    path('teacher/create', TeacherTfgCreateView.as_view(), name="teacher_tfgs_create"),
    path('edit/<int:pk>', TfgUpdateView.as_view(), name="tfgs_update"),
    path('teacher/delete/<int:id>', TeacherTfgDeleteView.as_view(), name="teacher_tfgs_delete"),
    path('departament/', DepartamentTfgListView.as_view(), name="departament_tfgs_list"),
    path('departament/<int:pk>', DepartamentTfgDetailView.as_view(), name="departament_tfgs_detail"),
    path('departament/validation/<int:id>/<int:validate>', DepartamentValidation.as_view(), name="departament_tfgs_validation")

]