from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView

from app.forms import FormContrato, FormCarrinho, ItemServicoFormSet
from app.mixins.CustomMixins import ProfessionalUserRequiredMixin
from app.models import ContratoDeServico


class DashboardView(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    template_name = 'panel/dashboard.html'
    model = ContratoDeServico
    context_object_name = 'contratos'
    ordering = '-created_at'


class ContractUpdateView(LoginRequiredMixin, ProfessionalUserRequiredMixin, UpdateView):
    context_object_name = 'contrato'
    model = ContratoDeServico
    success_url = '/painel/'
    template_name = 'panel/view-contract.html'
    form_class = FormContrato

    def get_context_data(self, **kwargs):
        data = super(ContractUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['carrinho_form'] = FormCarrinho(self.request.POST, instance=self.object.carrinho)
            data['itemservicoset'] = ItemServicoFormSet(self.request.POST, self.request.FILES,
                                                        instance=self.object.carrinho)
        else:
            data['carrinho_form'] = FormCarrinho(instance=self.object.carrinho)
            data['itemservicoset'] = ItemServicoFormSet(instance=self.object.carrinho)
        return data

    def form_valid(self, form):
        print(form)
        return super(ContractUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ContractUpdateView, self).form_invalid(form)


def finalizar_contrato_servico(request, pk):
    try:
        contrato = ContratoDeServico.objects.get(id=pk)
        contrato.status = 'REALIZADO'
        contrato.save()
    except (Exception,):
        messages.error(request, 'Erro ao finalizar servico, tente novamente.')
    return redirect('/painel')


def rejeitar_contrato_servico(request, pk):
    try:
        contrato = ContratoDeServico.objects.get(id=pk)
        contrato.status = 'REJEITADO'
        contrato.save()
    except (Exception,):
        messages.error(request, 'Erro ao rejeitar servico, tente novamente.')
    return redirect('/painel')
