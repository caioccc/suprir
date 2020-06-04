# coding=utf-8
import calendar
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView
from django.views.generic import ListView, UpdateView
from djmoney.money import Money

from app.forms import FormContrato, FormCarrinho, ItemServicoFormSet, FormServico, FotoServicoFormSet, FormProfissional, \
    FormUser, FormRejeiteContrato, FormCreateCupom, FormEditCupom, FormEntrada, FormSaida, FormInteresse, FormProposta, FormProcesso
from app.mixins.CustomMixins import ProfessionalUserRequiredMixin
from app.models import ContratoDeServico, Servico, ComentarioServico, Cliente, Profissional, Cupom, Entrada, Saida, Interesse, Proposta, Processo
from app.views.TelegramAPI import send_mail_and_telegram


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


def andamento_contrato_servico(request, pk):
    try:
        contrato = ContratoDeServico.objects.get(id=pk)
        contrato.status = 'EM ANDAMENTO'
        contrato.save()
        send_mail_and_telegram(contrato.cliente, 'Oi, seu contrato mudou de status. Agora ele esta em andamento. Obrigado pela preferencia.', 'Parece que o status do contrato de servico mudou.')
    except (Exception,):
        messages.error(request, 'Erro ao dar andamento no servico, tente novamente.')
    return redirect('/painel')


class RejeiteContratoForm(LoginRequiredMixin, ProfessionalUserRequiredMixin, UpdateView):
    model = ContratoDeServico
    form_class = FormRejeiteContrato
    context_object_name = 'contrato'
    template_name = 'panel/rejeite-contrato-form.html'
    success_url = '/painel/'

    def get_initial(self):
        data = super(RejeiteContratoForm, self).get_initial()
        data['status'] = 'REJEITADO'
        return data

    def form_valid(self, form):
        cliente = ContratoDeServico.objects.get(pk=self.kwargs.get(self.pk_url_kwarg)).cliente
        send_mail_and_telegram(cliente, 'Oi, seu contrato gerado foi rejeitado pelo profissional. Por favor, entre no sistema e entre em contato com o profissional.',
                               'Contrato de Servico foi rejeitado.')
        messages.success(self.request, 'A Administracao ira avaliar o processo.')
        return super(RejeiteContratoForm, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ocorreu algum erro, tente novamente')
        return super(RejeiteContratoForm, self).form_invalid(form)


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


class ClienteList(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    model = Cliente
    template_name = 'panel/list-clientes.html'
    context_object_name = 'clientes'
    ordering = '-created_at'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(
            carrinhodeservicos__profissional=self.request.user.profissional).distinct()
        return super(ClienteList, self).get_queryset()


class EditarPerfilView(LoginRequiredMixin, ProfessionalUserRequiredMixin, UpdateView):
    template_name = 'panel/editar-perfil.html'
    model = Profissional
    form_class = FormProfissional
    context_object_name = 'profissional'
    success_url = '/painel/perfil/'

    def get_success_url(self):
        return '/painel/perfil/' + str(self.request.user.profissional.pk) + '/'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.request.user.profissional.pk
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def form_valid(self, form):
        context = self.get_context_data()
        form_user = context['form_user']
        with transaction.atomic():
            self.object = form.save()
            if form_user.is_valid():
                form_user.instance = self.object.user
                form_user.save()
        messages.success(self.request, 'Perfil atualizado com sucesso.')
        return super(EditarPerfilView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ocorreu algum erro, tente novamente')
        return super(EditarPerfilView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        data = super(EditarPerfilView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['form_user'] = FormUser(self.request.POST, self.request.FILES,
                                         instance=self.object.user)
        else:
            data['form_user'] = FormUser(instance=self.object.user)
        return data


class ListCupons(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    template_name = 'panel/list-cupons.html'
    model = Cupom
    ordering = '-created_at'
    context_object_name = 'cupons'

    def get_queryset(self):
        return self.model.objects.filter(profissional=self.request.user.profissional)


class CreateCupom(LoginRequiredMixin, ProfessionalUserRequiredMixin, CreateView):
    model = Cupom
    form_class = FormCreateCupom
    template_name = 'panel/create-cupom.html'
    context_object_name = 'cupom'
    success_url = '/painel/cupons/'

    def get_initial(self):
        data = super(CreateCupom, self).get_initial()
        data['profissional'] = self.request.user.profissional
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Cupom criado com sucesso')
        return super(CreateCupom, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(CreateCupom, self).form_invalid(form)


class EditCupom(LoginRequiredMixin, ProfessionalUserRequiredMixin, UpdateView):
    model = Cupom
    form_class = FormEditCupom
    template_name = 'panel/update-cupom.html'
    context_object_name = 'cupom'
    success_url = '/painel/cupons/'

    def get_initial(self):
        data = super(EditCupom, self).get_initial()
        data['profissional'] = self.request.user.profissional
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Cupom atualizado com sucesso')
        return super(EditCupom, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(EditCupom, self).form_invalid(form)


class RemoveCupom(LoginRequiredMixin, ProfessionalUserRequiredMixin, DeleteView):
    model = Cupom
    template_name = 'panel/delete-cupom.html'
    context_object_name = 'cupom'
    success_url = '/painel/cupons/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cupom removido com sucesso')
        return super(RemoveCupom, self).delete(self.request, *args, **kwargs)


class DocumentoContratoComCliente(LoginRequiredMixin, ProfessionalUserRequiredMixin, DetailView):
    model = ContratoDeServico
    template_name = 'documento-contrato.html'
    context_object_name = 'contrato'


class DocumentoContratoProfissional(LoginRequiredMixin, ProfessionalUserRequiredMixin, DetailView):
    model = Processo
    template_name = 'panel/documento-contrato-meiafolha.html'
    context_object_name = 'processo'


class ListEntradas(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    template_name = 'panel/list-entradas.html'
    model = Entrada
    ordering = '-created_at'
    context_object_name = 'entradas'

    def get_queryset(self):
        return self.model.objects.filter(profissional=self.request.user.profissional).order_by('-created_at')


class CreateEntrada(LoginRequiredMixin, ProfessionalUserRequiredMixin, CreateView):
    template_name = 'panel/create-entrada.html'
    model = Entrada
    form_class = FormEntrada
    context_object_name = 'entrada'
    success_url = '/painel/entradas/'

    def get_initial(self):
        data = super(CreateEntrada, self).get_initial()
        data['profissional'] = self.request.user.profissional
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Entrada criada com sucesso.')
        return super(CreateEntrada, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente.')
        return super(CreateEntrada, self).form_invalid(form)


class EditEntrada(LoginRequiredMixin, ProfessionalUserRequiredMixin, UpdateView):
    template_name = 'panel/update-entrada.html'
    model = Entrada
    form_class = FormEntrada
    context_object_name = 'entrada'
    success_url = '/painel/entradas/'

    def form_valid(self, form):
        messages.success(self.request, 'Entrada atualizada com sucesso.')
        return super(EditEntrada, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente.')
        return super(EditEntrada, self).form_invalid(form)


class DeleteEntrada(LoginRequiredMixin, ProfessionalUserRequiredMixin, DeleteView):
    model = Entrada
    template_name = 'panel/delete-entrada.html'
    context_object_name = 'entrada'
    success_url = '/painel/entradas/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Entrada removida com sucesso')
        return super(DeleteEntrada, self).delete(self.request, *args, **kwargs)


class ListSaidas(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    template_name = 'panel/list-saidas.html'
    model = Saida
    ordering = '-created_at'
    context_object_name = 'saidas'

    def get_queryset(self):
        return self.model.objects.filter(profissional=self.request.user.profissional).order_by('-created_at')


class CreateSaida(LoginRequiredMixin, ProfessionalUserRequiredMixin, CreateView):
    template_name = 'panel/create-saida.html'
    model = Saida
    form_class = FormSaida
    context_object_name = 'saida'
    success_url = '/painel/saidas/'

    def get_initial(self):
        data = super(CreateSaida, self).get_initial()
        data['profissional'] = self.request.user.profissional
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Saida criada com sucesso.')
        return super(CreateSaida, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente.')
        return super(CreateSaida, self).form_invalid(form)


class EditSaida(LoginRequiredMixin, ProfessionalUserRequiredMixin, UpdateView):
    template_name = 'panel/update-saida.html'
    model = Saida
    form_class = FormSaida
    context_object_name = 'saida'
    success_url = '/painel/saidas/'

    def form_valid(self, form):
        messages.success(self.request, 'Saida atualizada com sucesso.')
        return super(EditSaida, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente.')
        return super(EditSaida, self).form_invalid(form)


class DeleteSaida(LoginRequiredMixin, ProfessionalUserRequiredMixin, DeleteView):
    model = Saida
    template_name = 'panel/delete-saida.html'
    context_object_name = 'saida'
    success_url = '/painel/saidas/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Saida removida com sucesso')
        return super(DeleteSaida, self).delete(self.request, *args, **kwargs)


class FluxoCaixa(LoginRequiredMixin, ProfessionalUserRequiredMixin, TemplateView):
    template_name = 'panel/fluxo-caixa.html'

    def get_saldo_total(self):
        soma_entrada = Money(0, 'BRL')
        for entrada in Entrada.objects.filter(profissional=self.request.user.profissional):
            soma_entrada += entrada.valor
        soma_saida = Money(0, 'BRL')
        for saida in Saida.objects.filter(profissional=self.request.user.profissional):
            soma_saida += saida.valor
        return soma_entrada - soma_saida

    def get_total_entradas_mes(self):
        now = datetime.now()
        soma = Money(0, 'BRL')
        for entrada in Entrada.objects.filter(profissional=self.request.user.profissional,
                                              data__month=now.month,
                                              data__year=now.year):
            soma += entrada.valor
        return soma

    def get_total_saidas_mes(self):
        now = datetime.now()
        soma = Money(0, 'BRL')
        for saida in Saida.objects.filter(profissional=self.request.user.profissional,
                                          data__month=now.month,
                                          data__year=now.year):
            soma += saida.valor
        return soma

    def get_saldo_operacional_mes(self):
        ent = self.get_total_entradas_mes()
        sai = self.get_total_saidas_mes()
        return ent - sai

    def get_context_data(self, **kwargs):
        kwargs['entradas_mes'] = self.get_total_entradas_mes()
        kwargs['saidas_mes'] = self.get_total_saidas_mes()
        kwargs['saldo_operacional'] = self.get_saldo_operacional_mes()
        kwargs['saldo_total'] = self.get_saldo_total()
        return super(FluxoCaixa, self).get_context_data(**kwargs)


def get_month_data(request):
    array = []
    now = datetime.now()
    entrada = Entrada.objects.filter(profissional=request.user.profissional, data__year=now.year).order_by('data')
    if len(entrada) > 0:
        entrada = entrada.first().data
    else:
        entrada = now.date()
    saida = Saida.objects.filter(profissional=request.user.profissional, data__year=now.year).order_by('data')
    if len(saida) > 0:
        saida = saida.first().data
    else:
        saida = now.date()
    data_mais_antiga = min(entrada, saida)

    now = now + timedelta(days=1)
    diff = (now.date() - data_mais_antiga).days
    sum_entrada_dia = Money(0, 'BRL')
    sum_saida_dia = Money(0, 'BRL')
    for i in range(diff):
        data_busca_entradas = data_mais_antiga + timedelta(days=i)
        entradas_dia = Entrada.objects.filter(profissional=request.user.profissional,
                                              data__year=data_busca_entradas.year,
                                              data__month=data_busca_entradas.month,
                                              data__day=data_busca_entradas.day)
        saidas_dia = Saida.objects.filter(profissional=request.user.profissional,
                                          data__year=data_busca_entradas.year,
                                          data__month=data_busca_entradas.month,
                                          data__day=data_busca_entradas.day)

        for entrada in entradas_dia:
            sum_entrada_dia += entrada.valor

        for saida in saidas_dia:
            sum_saida_dia += saida.valor
        val_sum = sum_entrada_dia - sum_saida_dia
        array.append([
            calendar.timegm(data_busca_entradas.timetuple()) * 1000,
            float(val_sum)
        ])

    return JsonResponse(array, safe=False)


class ListInteresse(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    template_name = 'panel/list-interesse.html'
    context_object_name = 'interesses'
    model = Interesse
    ordering = '-created_at'

    def get_queryset(self):
        return self.model.objects.filter(status=True).order_by('-created_at')


class CreateInteresse(LoginRequiredMixin, ProfessionalUserRequiredMixin, CreateView):
    template_name = 'panel/create-interesse.html'
    context_object_name = 'interesse'
    model = Interesse
    form_class = FormInteresse
    success_url = '/painel/interesses'

    def get_initial(self):
        data = super(CreateInteresse, self).get_initial()
        data['profissional_dono'] = self.request.user.profissional
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Interesse criado com sucesso')
        return super(CreateInteresse, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(CreateInteresse, self).form_invalid(form)


class UpdateInteresse(LoginRequiredMixin, ProfessionalUserRequiredMixin, UpdateView):
    template_name = 'panel/update-interesse.html'
    context_object_name = 'interesse'
    model = Interesse
    form_class = FormInteresse
    success_url = '/painel/interesses'

    def form_valid(self, form):
        messages.success(self.request, 'Interesse atualizado com sucesso')
        return super(UpdateInteresse, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(UpdateInteresse, self).form_invalid(form)


class DeleteInteresse(LoginRequiredMixin, ProfessionalUserRequiredMixin, DeleteView):
    model = Interesse
    template_name = 'panel/delete-interesse.html'
    context_object_name = 'interesse'
    success_url = '/painel/interesses/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Interesse removido com sucesso')
        return super(DeleteInteresse, self).delete(self.request, *args, **kwargs)


class ListPropostas(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    template_name = 'panel/list-propostas.html'
    model = Proposta
    context_object_name = 'propostas_realizadas'
    ordering = '-created_at'

    def get_queryset(self):
        return self.model.objects.filter(profissional_socio=self.request.user.profissional)

    def get_context_data(self, **kwargs):
        kwargs['propostas_recebidas'] = self.model.objects.filter(interesse__profissional_dono=self.request.user.profissional).order_by('-created_at')
        return super(ListPropostas, self).get_context_data(**kwargs)


def generate_process(request, pk, ):
    proposta = Proposta.objects.get(pk=pk)
    proposta.status = 'ACEITO'
    proposta.save()
    interesse = proposta.interesse
    interesse.status = False
    interesse.save()
    proc = Processo(
        profissional_dono=proposta.interesse.profissional_dono,
        profissional_socio=proposta.profissional_socio,
        titulo=proposta.interesse.titulo,
        interesse=proposta.interesse,
        proposta=proposta,
        descricao=''
    )
    proc.save()
    mensagem = 'Sua proposta foi aceita. Acesse o sistema do SUPRIR para checar o status do novo processo gerado.'
    send_mail_and_telegram(proposta.profissional_socio, mensagem, 'Sua proposta foi aceita.')
    messages.success(request, 'Proposta Aceita com sucesso. Um Processo foi aberto e está aguardando pagamento.')
    return redirect('/painel/processos/')


def reject_bid(request, pk):
    proposta = Proposta.objects.get(pk=pk)
    proposta.status = 'REJEITADO'
    proposta.save()
    mensagem = 'Sua proposta foi rejeitada. Acesse o sistema do SUPRIR imediatamente.'
    send_mail_and_telegram(proposta.profissional_socio, mensagem, 'Sua proposta foi rejeitada.')
    messages.success(request, 'Proposta Rejeitada')
    return redirect('/painel/propostas/')


class CreateProposta(LoginRequiredMixin, ProfessionalUserRequiredMixin, CreateView):
    model = Proposta
    context_object_name = 'proposta'
    success_url = '/painel/propostas/'
    form_class = FormProposta
    template_name = 'panel/create-proposta.html'

    def get_initial(self):
        data = super(CreateProposta, self).get_initial()
        data['profissional_socio'] = self.request.user.profissional
        data['interesse'] = Interesse.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Proposta criada com sucesso')
        interesse = Interesse.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        mensagem = 'Um nova proposta foi criada para seu interesse cadastrado. Acesse o sistema SUPRIR imediatamente para aceitar ou rejeitar ela.'
        send_mail_and_telegram(interesse.profissional_dono, mensagem, 'Uma nova proposta para seu interesse foi criado.')
        return super(CreateProposta, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(CreateProposta, self).form_invalid(form)


class DeleteProposta(LoginRequiredMixin, ProfessionalUserRequiredMixin, DeleteView):
    model = Proposta
    template_name = 'panel/delete-proposta.html'
    context_object_name = 'proposta'
    success_url = '/painel/propostas/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Proposta removida com sucesso')
        return super(DeleteProposta, self).delete(self.request, *args, **kwargs)


class ListProcessos(LoginRequiredMixin, ProfessionalUserRequiredMixin, ListView):
    template_name = 'panel/list-processos.html'
    model = Processo
    context_object_name = 'processos'
    ordering = '-created_at'

    def get_queryset(self):
        return self.model.objects.filter(Q(profissional_dono=self.request.user.profissional) |
                                         Q(profissional_socio=self.request.user.profissional))


class ViewProcesso(LoginRequiredMixin, ProfessionalUserRequiredMixin, UpdateView):
    template_name = 'panel/view-processo.html'
    model = Processo
    form_class = FormProcesso
    context_object_name = 'processo'
    success_url = '/painel/processos/'


class FinalizarProcesso(LoginRequiredMixin, ProfessionalUserRequiredMixin, DeleteView):
    model = Processo
    template_name = 'panel/finalizar-processo.html'
    context_object_name = 'processo'
    success_url = '/painel/processos/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = 'REALIZADO'
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
