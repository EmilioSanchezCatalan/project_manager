"""
    Configuración de las urls de las vistas asociadas a los profesores
    y sus tfms.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

    Version: 1.0.
"""

from django.urls import path
from tfms.views.views_teacher import TeacherTfmListView, TeacherTfmDraftListView
from tfms.views.views_teacher import TeacherTfmCreateView, TeacherDraftTfmCreateView
from tfms.views.views_teacher import TeacherTfmUpdateView, TeacherTfmDelete
from tfms.views.views_teacher import TeacherTfmDetailView


urlpatterns = [
    path('public/', TeacherTfmListView.as_view(), name="teacher_tfms_list" ),
    path('public/create/', TeacherTfmCreateView.as_view(), name="teacher_tfms_create"),
    path('draft/', TeacherTfmDraftListView.as_view(), name="teacher_draft_tfms_list"),
    path('draft/create/', TeacherDraftTfmCreateView.as_view(), name="teacher_draft_tfms_create"),
    path('<int:pk>/', TeacherTfmDetailView.as_view(), name="teacher_tfms_detail"),
    path('edit/<int:pk>/', TeacherTfmUpdateView.as_view(), name="teacher_tfms_update"),
    path('delete/<int:id>/', TeacherTfmDelete.as_view(), name="teacher_tfms_delete"),
]