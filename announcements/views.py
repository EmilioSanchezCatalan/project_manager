from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from project_manager.settings import PAGINATION
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from login.decorators import is_center
from tfgs.models import Tfgs
from announcements.models import AnnouncementsTfg, AnnouncementsTfm
from announcements.forms import FilterAnnouncementsForm, CreateAnnouncementsForm
import datetime

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfgListView(ListView):
    model = AnnouncementsTfg
    template_name = "announcements/announcements_tfg_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset().filter(centers=self.request.user.userinfos.centers)
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__contains=name)
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = FilterAnnouncementsForm(initial=self.request.GET.dict())
        return context

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfgCreateView(CreateView):
    model = AnnouncementsTfg
    template_name = "announcements/announcements_form.html"
    form_class = CreateAnnouncementsForm
    success_url = reverse_lazy("announ_tfgs_list")

    def get(self, request, *args, **kwargs):
        if AnnouncementsTfg.objects.exclude(status=AnnouncementsTfg.STATUS_CLOSE):
            messages.warning(self.request, "Ya tiene una convocatoria abierta en curso", 'warning')
            return HttpResponseRedirect(reverse("announ_tfgs_list"))
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = "announ_tfgs_list"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = AnnouncementsTfg.STATUS_OPEN
        self.object.centers = self.request.user.userinfos.centers
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfgUpdateView(UpdateView):
    model = AnnouncementsTfg
    template_name = "announcements/announcements_form.html"
    form_class = CreateAnnouncementsForm
    success_url = reverse_lazy("announ_tfgs_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = "announ_tfgs_list"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.centers = self.request.user.userinfos.centers
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfgPublicStatus(RedirectView):
    url = "announ_tfgs_list"
    pattern_name = 'public_announ_tfg'
    
    def get_redirect_url(self, *args, **kwargs):
        announ = AnnouncementsTfg.objects.get(id=kwargs['id'], centers=self.request.user.userinfos.centers)
        if announ.status == AnnouncementsTfg.STATUS_OPEN:
            announ.status = AnnouncementsTfg.STATUS_PUBLIC
            announ.save()
            messages.error(self.request, "Se ha modificado el estado a \'" + AnnouncementsTfg.STATUS_TEXT_PUBLIC + "\'", 'success')
        else:
            messages.error(self.request, "La convocatoria no se encuentra en el estado: \'" + AnnouncementsTfg.STATUS_TEXT_OPEN + "\'", 'danger')
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfgCloseStatus(RedirectView):
    url = "announ_tfgs_list"
    pattern_name = 'public_announ_tfg'
    
    def get_redirect_url(self, *args, **kwargs):
        announ = AnnouncementsTfg.objects.get(id=kwargs['id'], centers=self.request.user.userinfos.centers)
        if announ.status == AnnouncementsTfg.STATUS_PUBLIC:
            announ.status = AnnouncementsTfg.STATUS_CLOSE
            announ.save()
            self.not_assigned_tfgs(announ.id)
            messages.error(self.request, "Se ha modificado el estado a \'" + AnnouncementsTfg.STATUS_TEXT_CLOSE + "\'", 'success')
        else:
            messages.error(self.request, "La convocatoria no se encuentra en el estado: \'" + AnnouncementsTfg.STATUS_TEXT_PUBLIC + "\'", 'danger')
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url

    def not_assigned_tfgs(self, announ_id):
        queryset = Tfgs.objects.filter(announcements=announ_id)
        for query in queryset:
            if len(query.students.all()) <= 0:
                query.draft = True
                query.announcements = None
                query.save()
            else:
                query.date_assignment = datetime.datetime.now()
                query.save()

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfgDeleteView(RedirectView):
    url = "announ_tfgs_list"
    pattern_name = 'delete_Tfm'
    
    def get_redirect_url(self, *args, **kwargs):
        announ = AnnouncementsTfg.objects.get(id=kwargs['id'], centers=self.request.user.userinfos.centers)
        if announ.status != AnnouncementsTfg.STATUS_CLOSE:
            announ.delete()
            messages.success(self.request, "La convocatoria se ha borrado correctamente", "success")
        else:
            messages.warning(self.request, "No se puede borrar una convocatoria cerrada", "warning")
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url

@method_decorator(user_passes_test(is_center), name="dispatch")
class AnnounTfmListView(ListView):
    model = AnnouncementsTfm
    template_name = "announcements/announcements_list.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = super().get_queryset().filter(centers=self.request.user.userinfos.centers)
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__contains=name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = FilterAnnouncementsForm(initial=self.request.GET.dict())
        return context