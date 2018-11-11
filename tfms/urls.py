from django.urls import path
from .views import TfmListView, TfmDetailView, TeacherTfmListView, TeacherTfgDetailView, TeacherTfmDelete

urlpatterns = [
    path('', TfmListView.as_view(), name="public_tfms_list"),
    path('<int:pk>', TfmDetailView.as_view(), name="public_tfms_detail"),
    path('teacher/', TeacherTfmListView.as_view(), name="teacher_tfms_list"),
    path('teacher/<int:pk>', TeacherTfgDetailView.as_view(), name="teacher_tfms_detail"),
    path('teacher/delete/<int:id>', TeacherTfmDelete.as_view(), name="teacher_tfms_delete")
]