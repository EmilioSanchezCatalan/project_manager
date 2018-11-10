from django.urls import path
from .views import TfgListView, TeacherTfgListView, TeacherTfgDelete

urlpatterns = [
    path('', TfgListView.as_view(), name="public_tfgs_list"),
    path('teacher/', TeacherTfgListView.as_view(), name="teacher_tfgs_list" ),
    path('teacher/delete/<int:id>', TeacherTfgDelete.as_view(), name="teacher_tfgs_delete")
]