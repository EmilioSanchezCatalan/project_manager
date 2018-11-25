from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from login.forms import CreateStudentForm
from login.models import Students
from login.decorators import is_teacher, is_from_group, is_departaments
from core.forms import CreateTutor2Form
from .forms import FilterPublicTfgForm, FilterTeacherTfgForm, CreateTfgForm, FilterDepartamentTfgForm
from .models import Tfgs


class TfgListView(ListView):
    model = Tfgs
    template_name = "tfgs/public_tfgs_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        # filtrar solo por aquellos que este validados completamente
        name = self.request.GET.get("name_project", "")
        carrer = self.request.GET.get("formation_project", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if carrer:
            queryset = queryset.filter(carrers_id=carrer)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = FilterPublicTfgForm(initial=self.request.GET.dict())
        return context

class TfgDetailView(DetailView):
    model = Tfgs
    teamplate_name = "tfgs/tfgs_detail"
    
    # filtrar solo por aquellos que este validados completamente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfgs_id=context['tfgs'].id)
        context["back_url"] = "public_tfgs_list"
        return context

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfgListView(ListView):
    model = Tfgs
    template_name = "tfgs/teacher_tfgs_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        name = self.request.GET.get("search_text", "")
        carrer = self.request.GET.get("formation_project", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if carrer:
            queryset = queryset.filter(carrers_id=carrer)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfgs"
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['form_filter'] = FilterTeacherTfgForm(initial=self.request.GET.dict(), user=self.request.user)
        context['nbar'] = "tfg"
        return context

    @staticmethod
    def __check_filters_is_applied(params_dict):
        for param_name in params_dict.keys():
            if param_name != "search_text" and params_dict[param_name] != "":
                return True
        return False

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfgDetailView(DetailView):
    model = Tfgs
    teamplate_name = "tfgs/tfgs_detail"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfgs_id=context['tfgs'].id)
        context["back_url"] = "teacher_tfgs_list"
        return context

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfgCreateView(CreateView):
    model = Tfgs
    form_class = CreateTfgForm
    success_url = reverse_lazy("teacher_tfgs_list")
    template_name = "tfgs/tfgs_create_form.html"

    def get_form_kwargs(self):
        kwargs = super(TeacherTfgCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_form1"] = CreateStudentForm(prefix="student1")
        context["student_form2"] = CreateStudentForm(prefix="student2")
        context["tutor2_form"] = CreateTutor2Form(prefix="tutor2")
        context["back_url"] = "teacher_tfgs_list"
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        student1_form, student2_form, tutor2_form = None, None, None
        if self.request.POST.get('has_student') == 'on':
            student1_form = CreateStudentForm(
                self.request.POST,
                prefix="student1",
                instance=self.__get_student_tfg(
                    self.request.POST.get('student1-dni')
                )
            )
            student1_val = student1_form.is_valid()
        else:
            student1_val = True
        if self.request.POST.get('has_tutor2') == 'on':
            tutor2_form = CreateTutor2Form(
                self.request.POST,
                prefix="tutor2"
            )
            tutor2_val = tutor2_form.is_valid()
        else:
            tutor2_val = True
        if self.request.POST.get('has_student') == 'on' and self.request.POST.get('is_team') == 'on':
            student2_form = CreateStudentForm(
                self.request.POST,
                prefix="student2",
                instance=self.__get_student_tfg(
                    self.request.POST.get('student2-dni')
                )
            )
            student2_val = student2_form.is_valid()
        else:
            student2_val = True
        if form.is_valid() and student1_val and tutor2_val and student2_val:
            return self.form_valid(form, student1_form, student2_form, tutor2_form)
        else:
            return self.form_invalid(form, student1_form, student2_form, tutor2_form)

    def form_valid(self, form, student1_form=None, student2_form=None, tutor2_form=None):
        tutor2 = self.__createtutor2(tutor2_form)
        self.__createTfg(form, tutor2)
        self.__createStudent(self.object, student1_form)
        self.__createStudent(self.object, student2_form)
        messages.success(self.request, "Creado correctamente nuevo trabajo fin de grado con titulo: \"" + self.object.title + "\"", 'success')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, student1_form=None, student2_form=None, tutor2_form=None):
        if student1_form is None:
            student1_form = CreateStudentForm(prefix="student1")
        if student2_form is None:
            student2_form = CreateStudentForm(prefix="student2")
        if tutor2_form is None:
            tutor2_form = CreateTutor2Form(prefix="tutor2")
        
        self.__errorsForm(form)
        self.__errorsForm(student1_form)
        self.__errorsForm(student2_form)
        self.__errorsForm(tutor2_form)
        return self.render_to_response(self.get_context_data(
            form=form,
            student1_form=student1_form,
            student2_form=student2_form,
            tutor2_form=tutor2_form
        ))
    
    def __errorsForm(self, form):
        form_errors = form.errors
        for fields_error in form_errors.keys():
            for error in form_errors[fields_error]:
                messages.error(self.request,  fields_error + ": " + error, 'danger')

    def __createTfg(self, form, tutor2=None):
        self.object = form.save(commit=False)
        self.object.tutor1 = self.request.user
        self.object.tutor2 = tutor2
        self.object.save()
        form.save_m2m()
    
    @staticmethod
    def __get_student_tfg(dni):
        try:
            return Students.objects.get(dni=dni)
        except:
            return None

    @staticmethod
    def __createStudent(tfg, form=None):
        if form is not None:
            student = form.save(commit=False)
            student.tfgs = tfg
            student.save()

    @staticmethod
    def __createtutor2(form=None):
        if form is not None:
            return form.save()
        else:
            return None

@method_decorator(user_passes_test(is_from_group), name="dispatch")
class TeacherTfgUpdateView(UpdateView):
    model = Tfgs
    form_class = CreateTfgForm
    template_name = "tfgs/tfgs_update_form.html"
    success_url = reverse_lazy("teacher_tfgs_list")

    def get_form_kwargs(self):
        kwargs = super(TeacherTfgUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['tfg'] = self.get_object()
        return kwargs

    def get_queryset(self):
        queryset = super(TeacherTfgUpdateView, self).get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tfg = self.get_object()
        list_students = self.__get_students_tfg(tfg)
        context["student_form1"] = CreateStudentForm(prefix="student1", instance=list_students[0])
        context["student_form2"] = CreateStudentForm(prefix="student2", instance=list_students[1])
        context["number_students"] = tfg.students.all().count()
        context["tutor2_form"] = CreateTutor2Form(prefix="tutor2", instance=tfg.tutor2)
        context["back_url"] = "teacher_tfgs_list"
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        student1_form, student2_form, tutor2_form = None, None, None
        form = self.get_form()
        form.instance = self.object
        if self.request.POST.get('has_student') == 'on':
            student1_form = CreateStudentForm(
                self.request.POST,
                prefix="student1",
                instance=self.__get_student_tfg(
                    self.request.POST.get('student1-dni')
                )
            )
            student1_val = student1_form.is_valid()
        else:
            student = self.__get_student_tfg(self.request.POST.get('student1-dni'))
            if student is not None:
                student.tfgs = None
                student.save()
            student1_val = True
        if self.request.POST.get('has_tutor2') == 'on':
            tutor2_form = CreateTutor2Form(self.request.POST, prefix="tutor2", instance=self.object.tutor2)
            tutor2_val = tutor2_form.is_valid()
        else:
            tutor2_val = True
        if self.request.POST.get('has_student') == 'on' and self.request.POST.get('is_team') == 'on':
            student2_form = CreateStudentForm(
                self.request.POST,
                prefix="student2",
                instance=self.__get_student_tfg(
                    self.request.POST.get('student2-dni')
                )
            )
            student2_val = student2_form.is_valid()
        else:
            student = self.__get_student_tfg(self.request.POST.get('student2-dni'))
            if student is not None:
                student.tfgs = None
                student.save()
            student2_val = True
        if form.is_valid() and student1_val and tutor2_val and student2_val:
            return self.form_valid(form, student1_form, student2_form, tutor2_form)
        else:
            return self.form_invalid(form, student1_form, student2_form, tutor2_form)

    def form_valid(self, form, student1_form=None, student2_form=None, tutor2_form=None):
        tutor2 = self.__createtutor2(tutor2_form)
        self.__createTfg(form, tutor2)
        self.__createStudent(self.object, student1_form)
        self.__createStudent(self.object, student2_form)
        messages.success(self.request, "Actualizado correctamente el trabajo fin de grado con titulo: \"" + self.object.title + "\"", 'success')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, student1_form=None, student2_form=None, tutor2_form=None):
        if student1_form is None:
            student1_form = CreateStudentForm(prefix="student1")
        if student2_form is None:
            student2_form = CreateStudentForm(prefix="student2")
        if tutor2_form is None:
            tutor2_form = CreateTutor2Form(prefix="tutor2")
        
        self.__errorsForm(form)
        self.__errorsForm(student1_form)
        self.__errorsForm(student2_form)
        self.__errorsForm(tutor2_form)
        return self.render_to_response(self.get_context_data(
            form=form,
            student1_form=student1_form,
            student2_form=student2_form,
            tutor2_form=tutor2_form
        ))
    
    def __errorsForm(self, form):
        form_errors = form.errors
        for fields_error in form_errors.keys():
            for error in form_errors[fields_error]:
                messages.error(self.request,  fields_error + ": " + error, 'danger')

    def __createTfg(self, form, tutor2=None):
        self.object = form.save(commit=False)
        self.object.tutor1 = self.request.user
        self.object.tutor2 = tutor2
        self.object.save()
        form.save_m2m()

    @staticmethod
    def __get_student_tfg(dni):
        try:
            return Students.objects.get(dni=dni)
        except:
            return None

    @staticmethod
    def __get_students_tfg(tfg):
        list_students = [None, None]
        students = tfg.students.all()
        number_students = students.count()
        if number_students > 0:
            list_students[0] = students[0]
        if number_students > 1:
            list_students[1] = students[1]
        return list_students

    @staticmethod
    def __createStudent(tfg, form=None):
        if form is not None:
            student = form.save(commit=False)
            student.tfgs = tfg
            student.save()

    @staticmethod
    def __createtutor2(form=None):
        if form is not None:
            return form.save()
        else:
            return None

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfgDeleteView(RedirectView):
    url = "teacher_tfgs_list"
    pattern_name = 'delete_Tfm'
    
    def get_redirect_url(self, *args, **kwargs):
        Tfgs.objects.filter(id=kwargs['id'], tutor1=self.request.user).delete()
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url
    
@method_decorator(user_passes_test(is_departaments), name="dispatch")
class DepartamentTfgListView(ListView):
    model = Tfgs
    template_name = "tfgs/departament_tfgs_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(carrers__departament=self.request.user.userinfos.departaments)
        name = self.request.GET.get("search_text", "")
        carrer = self.request.GET.get("formation_project", "")
        area = self.request.GET.get("area", "")
        tutor = self.request.GET.get("tutor", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if carrer:
            queryset = queryset.filter(carrers_id=carrer)
        if area:
            queryset = queryset.filter(tutor1__userinfos__areas_id=area)
        if tutor:
            queryset = queryset.filter(tutor1_id=tutor)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfgs"
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['form_filter'] = FilterDepartamentTfgForm(initial=self.request.GET.dict(), user=self.request.user)
        context['nbar'] = "tfg"
        return context

    @staticmethod
    def __check_filters_is_applied(params_dict):
        for param_name in params_dict.keys():
            if param_name != "search_text" and params_dict[param_name] != "":
                return True
        return False