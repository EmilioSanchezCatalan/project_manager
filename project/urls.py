from django.urls import path
from .views import ProjectDetailView, ProjectTeacherListView, ProjecTeachertDetailView, ProjectTeacherCreate, ProjectTeacherEdit

urlpatterns = [
    path('/', ProjectDetailView.as_view(), name="project"),
    path('/teacher/list', ProjectTeacherListView.as_view(), name="teacher_project_list"),
    path('/teacher', ProjecTeachertDetailView.as_view(), name="teacher_project"),
    path('/teacher/create', ProjectTeacherCreate.as_view(), name="teacher_project_create"),
    path('/teacher/edit', ProjectTeacherEdit.as_view(), name="teacher_project_edit")
]