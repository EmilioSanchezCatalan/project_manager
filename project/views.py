from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
class ProjectDetailView(TemplateView):
    template_name = "project/project_detail.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProjecTeachertDetailView(TemplateView):
    template_name = "project/project_detail.html"


class ProjectTeacherCreate(TemplateView):
    template_name = "project/project_form.html"


class ProjectTeacherEdit(TemplateView):
    template_name = "project/project_form.html"


class ProjectTeacherListView(TemplateView):
    template_name = "project/project_list.html"


class ProjectDepartamentCreate(TemplateView):
    template_name = "project/project_form.html"


class ProjectDepartamentEdit(TemplateView):
    template_name = "project/project_form.html"


class ProjectDepartamentListView(TemplateView):
    template_name = "project/project_list.html"