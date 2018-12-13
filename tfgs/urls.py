from django.urls import path
from .views import TfgListView, TfgDetailView, TeacherTfgListView, TeacherTfgDetailView
from .views import TeacherTfgCreateView, TfgUpdateView, TeacherTfgDeleteView
from .views import TeacherDraftTfgCreateView, TeacherTfgDraftListView
from .views import DepartamentTfgListView, DepartamentTfgDetailView, DepartamentValidationOk, DepartamentValidationError
from .views import CenterTfgListView, CenterTfgDetailView, CenterValidationOk, CenterValidationError

urlpatterns = [
    path('', TfgListView.as_view(), name="public_tfgs_list"),
    path('<int:pk>', TfgDetailView.as_view(), name="public_tfgs_detail"),
    path('teacher/public', TeacherTfgListView.as_view(), name="teacher_tfgs_list" ),
    path('teacher/public/create', TeacherTfgCreateView.as_view(), name="teacher_tfgs_create"),
    path('teacher/draft', TeacherTfgDraftListView.as_view(), name="teacher_draft_tfgs_list"),
    path('teacher/draft/create', TeacherDraftTfgCreateView.as_view(), name="teacher_draft_tfgs_create"),
    path('teacher/<int:pk>', TeacherTfgDetailView.as_view(), name="teacher_tfgs_detail"),
    path('teacher/edit/<int:pk>', TfgUpdateView.as_view(), name="teacher_tfgs_update"),
    path('teacher/delete/<int:id>', TeacherTfgDeleteView.as_view(), name="teacher_tfgs_delete"),
    path('departament/', DepartamentTfgListView.as_view(), name="departament_tfgs_list"),
    path('departament/<int:pk>', DepartamentTfgDetailView.as_view(), name="departament_tfgs_detail"),
    path('departament/edit/<int:pk>', TfgUpdateView.as_view(), name="departament_tfgs_update"),
    path('departament/validation/ok/<int:id>/<int:validate>', DepartamentValidationOk.as_view(), name="departament_tfgs_validation_ok"),
    path('departament/validation/error/<int:id>/<int:validate>', DepartamentValidationError.as_view(), name="departament_tfgs_validation_error"),
    path('center/<int:announ_id>', CenterTfgListView.as_view(), name="center_tfgs_list"),
    path('center/<int:announ_id>/detail/<int:pk>', CenterTfgDetailView.as_view(), name="center_tfgs_detail"),
    path('center/<int:announ_id>/edit/<int:pk>', TfgUpdateView.as_view(), name="center_tfgs_update"),
    path('center/<int:announ_id>/validation/ok/<int:id>/<int:validate>', CenterValidationOk.as_view(), name="center_tfgs_validation_ok"),
    path('center/<int:announ_id>/validation/error/<int:id>/<int:validate>', CenterValidationError.as_view(), name="center_tfgs_validation_error"),

]