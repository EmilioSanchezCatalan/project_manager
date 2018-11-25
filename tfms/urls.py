from django.urls import path
from .views import TfmListView, TfmDetailView, TeacherTfmListView, TeacherTfmDelete
from .views import TeacherTfmCreateView, TfmUpdateView, TeacherTfmDetailView
from .views import DepartamentTfmListView, DepartamentTfmDetailView, DepartamentValidation

urlpatterns = [
    path('', TfmListView.as_view(), name="public_tfms_list"),
    path('<int:pk>', TfmDetailView.as_view(), name="public_tfms_detail"),
    path('edit/<int:pk>', TfmUpdateView.as_view(), name="tfms_update"),
    path('teacher/', TeacherTfmListView.as_view(), name="teacher_tfms_list"),
    path('teacher/<int:pk>', TeacherTfmDetailView.as_view(), name="teacher_tfms_detail"),
    path('teacher/create', TeacherTfmCreateView.as_view(), name="teacher_tfms_create"),
    path('teacher/delete/<int:id>', TeacherTfmDelete.as_view(), name="teacher_tfms_delete"),
    path('departament/', DepartamentTfmListView.as_view(), name="departament_tfms_list"),
    path('departament/<int:pk>', DepartamentTfmDetailView.as_view(), name="departament_tfms_detail"),
    path('departament/validation/<int:id>/<int:validate>', DepartamentValidation.as_view(), name="departament_tfms_validation")
]