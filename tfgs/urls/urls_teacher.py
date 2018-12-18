"""
    Configuración de las urls de las vistas asociadas a los profesores
    y sus TFGs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from tfgs.views.views_teacher import TeacherTfgListView, TeacherTfgDraftListView
from tfgs.views.views_teacher import TeacherTfgCreateView, TeacherDraftTfgCreateView
from tfgs.views.views_teacher import TeacherTfgUpdateView, TeacherTfgDeleteView
from tfgs.views.views_teacher import TeacherTfgDetailView


urlpatterns = [
    path('public/', TeacherTfgListView.as_view(), name="teacher_tfgs_list" ),
    path('public/create/', TeacherTfgCreateView.as_view(), name="teacher_tfgs_create"),
    path('draft/', TeacherTfgDraftListView.as_view(), name="teacher_draft_tfgs_list"),
    path('draft/create/', TeacherDraftTfgCreateView.as_view(), name="teacher_draft_tfgs_create"),
    path('<int:pk>/', TeacherTfgDetailView.as_view(), name="teacher_tfgs_detail"),
    path('edit/<int:pk>/', TeacherTfgUpdateView.as_view(), name="teacher_tfgs_update"),
    path('delete/<int:id>/', TeacherTfgDeleteView.as_view(), name="teacher_tfgs_delete"),
]