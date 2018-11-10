from django.urls import path
from .views import TfmListView, TeacherTfmListView, TeacherTfmDelete

urlpatterns = [
    path('', TfmListView.as_view(), name="public_tfms_list"),
    path('teacher/', TeacherTfmListView.as_view(), name="teacher_tfms_list"),
    path('teacher/delete/<int:id>', TeacherTfmDelete.as_view(), name="teacher_tfms_delete")
]