from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.mixins.CustomMixins import ProfessionalUserRequiredMixin
from app.models import ContratoDeServico


class DashboardView(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    template_name = 'panel/dashboard.html'
    model = ContratoDeServico
    context_object_name = 'contratos'
    ordering = '-created_at'
    login_url = '/login/'
