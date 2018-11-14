from django.urls import path
from .views import TfgListView, TfgDetailView, TeacherTfgListView, TeacherTfgDetailView
from .views import TeacherTfgCreateView, TeacherTfgDeleteView

urlpatterns = [
    path('', TfgListView.as_view(), name="public_tfgs_list"),
    path('<int:pk>', TfgDetailView.as_view(), name="public_tfgs_detail"),
    path('teacher/', TeacherTfgListView.as_view(), name="teacher_tfgs_list" ),
    path('teacher/<int:pk>', TeacherTfgDetailView.as_view(), name="teacher_tfgs_detail"),
    path('teacher/create', TeacherTfgCreateView.as_view(), name="teacher_tfgs_create"),
    path('teacher/delete/<int:id>', TeacherTfgDeleteView.as_view(), name="teacher_tfgs_delete")
]