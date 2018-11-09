from django.views.generic.list import ListView
from .models import Tfms
from core.models import Masters

# Create your views here.
class TfmListView(ListView):
    model = Tfms
    template_name = "core/public_project_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name_project", "")
        master = self.request.GET.get("formation_project", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if master:
            queryset = queryset.filter(masters_id=master)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfms"
        context['formations'] = Masters.objects.all()
        context['default_select_value'] = "Masters"
        context['filters'] = self.request.GET.dict()
        return context
