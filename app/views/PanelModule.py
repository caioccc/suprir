# coding=utf-8
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView
from django.views.generic import ListView, UpdateView
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin

from app.forms import FormContrato, FormCarrinho, ItemServicoFormSet, FormServico, FotoServicoFormSet
from app.mixins.CustomMixins import ProfessionalUserRequiredMixin
from app.models import ContratoDeServico, Servico, ComentarioServico


class DashboardView(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    template_name = 'panel/dashboard.html'
    model = ContratoDeServico
    context_object_name = 'contratos'
    ordering = '-created_at'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(profissional=self.request.user.profissional)
        return super(DashboardView, self).get_queryset()


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


class ServicosList(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    template_name = 'panel/list-servicos.html'
    model = Servico
    context_object_name = 'servicos'
    ordering = '-created_at'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(profissional=self.request.user.profissional)
        return super(ServicosList, self).get_queryset()


class CreateServico(LoginRequiredMixin, ProfessionalUserRequiredMixin, CreateView):
    template_name = 'panel/create-servico.html'
    model = Servico
    form_class = FormServico
    context_object_name = 'servico'
    success_url = '/painel/servicos/'

    def get_initial(self):
        self.initial['profissional'] = self.request.user.profissional
        return super(CreateServico, self).get_initial()

    def get_context_data(self, **kwargs):
        data = super(CreateServico, self).get_context_data(**kwargs)
        if self.request.POST:
            data['fotoservicoset'] = FotoServicoFormSet(self.request.POST, self.request.FILES,
                                                        instance=self.object)
        else:
            data['fotoservicoset'] = FotoServicoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        fotoservicoset = context['fotoservicoset']
        with transaction.atomic():
            self.object = form.save()
            if fotoservicoset.is_valid():
                fotoservicoset.instance = self.object
                fotoservicoset.save()
        messages.success(self.request, 'Serviço criado com sucesso.')
        return super(CreateServico, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ocorreu algum erro, tente novamente')
        return super(CreateServico, self).form_invalid(form)


class UpdateServico(LoginRequiredMixin, ProfessionalUserRequiredMixin, UpdateView):
    template_name = 'panel/update-servico.html'
    model = Servico
    form_class = FormServico
    context_object_name = 'servico'
    success_url = '/painel/servicos/'

    def get_initial(self):
        # self.initial['profissional'] = self.request.user.profissional
        return super(UpdateServico, self).get_initial()

    def get_context_data(self, **kwargs):
        data = super(UpdateServico, self).get_context_data(**kwargs)
        if self.request.POST:
            data['fotoservicoset'] = FotoServicoFormSet(self.request.POST, self.request.FILES,
                                                        instance=self.object)
        else:
            data['fotoservicoset'] = FotoServicoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        fotoservicoset = context['fotoservicoset']
        with transaction.atomic():
            self.object = form.save()
            if fotoservicoset.is_valid():
                fotoservicoset.instance = self.object
                fotoservicoset.save()
        messages.success(self.request, 'Serviço atualizado com sucesso.')
        return super(UpdateServico, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ocorreu algum erro, tente novamente')
        return super(UpdateServico, self).form_invalid(form)


class DeleteServico(LoginRequiredMixin, ProfessionalUserRequiredMixin, DeleteView):
    model = Servico
    template_name = 'panel/delete-servico.html'
    context_object_name = 'servico'
    success_url = '/painel/servicos/'


class ListComentarios(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    model = ComentarioServico
    template_name = 'panel/list-comentarios.html'
    context_object_name = 'comentarios'
    ordering = '-created_at'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(servico__profissional=self.request.user.profissional)
        return super(ListComentarios, self).get_queryset()


class RevisaoView(LoginRequiredMixin, ProfessionalUserRequiredMixin, DeleteView):
    model = ComentarioServico
    template_name = 'panel/revisao-comentario.html'
    context_object_name = 'comentario'
    success_url = '/painel/comentarios/'

    def revisao(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status = False
        self.object.save()
        return HttpResponseRedirect(success_url)

    # Add support for browsers which only accept GET and POST for now.
    def post(self, request, *args, **kwargs):
        return self.revisao(request, *args, **kwargs)
