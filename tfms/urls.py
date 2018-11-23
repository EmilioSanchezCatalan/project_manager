from django.urls import path
from .views import TfmListView, TfmDetailView, TeacherTfmListView, TeacherTfmDetailView, TeacherTfmDelete
from .views import TeacherTfmCreateView, TeacherTfmUpdateView
urlpatterns = [
    path('', TfmListView.as_view(), name="public_tfms_list"),
    path('<int:pk>', TfmDetailView.as_view(), name="public_tfms_detail"),
    path('teacher/', TeacherTfmListView.as_view(), name="teacher_tfms_list"),
    path('teacher/<int:pk>', TeacherTfmDetailView.as_view(), name="teacher_tfms_detail"),
    path('teacher/create', TeacherTfmCreateView.as_view(), name="teacher_tfms_create"),
    path('teacher/edit/<int:pk>', TeacherTfmUpdateView.as_view(), name="teacher_tfms_update"),
    path('teacher/delete/<int:id>', TeacherTfmDelete.as_view(), name="teacher_tfms_delete")
]