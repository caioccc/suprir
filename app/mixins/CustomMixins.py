# coding=utf-8
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic.base import ContextMixin

from app.forms import ServicoSearchForm
from app.models import CategoriaDeProfissional, Profissional, ContratoDeServico, Proposta, Processo, GeneralMessage


class UserLoggedMixin(object):
    DASHBOARD_PROFISSIONAL_URL = '/painel/'
    INDEX_URL = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            print('logged user:', request.user)
            try:
                if request.user.profissional:
                    print('Logged pro:', request.user.profissional)
                    return redirect(self.DASHBOARD_PROFISSIONAL_URL)
            except (Exception,):
                return super(UserLoggedMixin, self).dispatch(request, *args, **kwargs)
        return super(UserLoggedMixin, self).dispatch(request, *args, **kwargs)


class ProfessionalUserRequiredMixin(AccessMixin, ContextMixin):
    login_url = '/login/'
    """
    CBV mixin which verifies that the current user is authenticated.
    """

    def get_context_data(self, **kwargs):
        new_contracts = ContratoDeServico.objects.filter(
            Q(profissional=self.request.user.profissional),
            Q(status='ABERTO')
        )
        new_propostas = Proposta.objects.filter(
            Q(interesse__profissional_dono=self.request.user.profissional),
            Q(status='AGUARDANDO')
        )
        alerta_contratos = ContratoDeServico.objects.filter(
            Q(profissional=self.request.user.profissional),
            Q(status__in=['ABERTO', 'EM ANDAMENTO'])
        )
        alerta_processos = Processo.objects.filter(
            Q(profissional_dono=self.request.user.profissional) | Q(profissional_socio=self.request.user.profissional),
            Q(status__in=['AGUARDANDO PAGAMENTO', 'ABERTO'])
        )
        general_message = GeneralMessage.objects.filter(status=True)
        kwargs['new_contracts'] = new_contracts
        kwargs['new_propostas'] = new_propostas
        kwargs['alerta_contratos'] = alerta_contratos
        kwargs['alerta_processos'] = alerta_processos
        kwargs['general_message'] = general_message.first()
        return super(ProfessionalUserRequiredMixin, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        try:
            pro = request.user.profissional
            print('logged profissional:', pro)
        except (Exception,):
            return self.handle_no_permission()
        return super(ProfessionalUserRequiredMixin, self).dispatch(request, *args, **kwargs)


class CustomContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        kwargs['categorias'] = CategoriaDeProfissional.objects.all()
        kwargs['estados'] = self.get_estados()
        kwargs['cidades'] = self.get_cidades()
        kwargs['filter_categorias'] = self.get_filter_categorias()
        kwargs['form_query'] = ServicoSearchForm
        return super(CustomContextMixin, self).get_context_data(**kwargs)

    def get_estados(self):
        estados = Profissional.objects.order_by('estado').values_list('estado', flat=True).exclude(
            estado=None)
        if len(estados) > 0:
            estados = estados.distinct()
        return estados

    def get_cidades(self):
        cidades = Profissional.objects.order_by('cidade').values_list('cidade', flat=True).exclude(
            cidade=None)
        if len(cidades) > 0:
            cidades = cidades.distinct()
        return cidades

    def get_filter_categorias(self):
        filter_categorias = []
        for categoria in CategoriaDeProfissional.objects.all():
            dic = {}
            dic['categoria'] = categoria
            dic['quantidade'] = Profissional.objects.filter(categoria=categoria).count()
            filter_categorias.append(dic)
        return filter_categorias
