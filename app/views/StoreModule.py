# coding=utf-8
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.views.generic import TemplateView
from search_views.filters import BaseFilter
from search_views.views import SearchListView

from app.forms import ServicoSearchForm, ProfissionalSearchForm, FormComentario, FormContratoAvaliacao
from app.forms import FormMensagem, FormEditCliente
from app.mixins.CustomMixins import UserLoggedMixin, CustomContextMixin
from app.models import Servico, Profissional, Mensagem, CarrinhoDeServicos, ItemServico, Cliente, ContratoDeServico, ItemCupom, FormaPagamento, ComentarioServico
from app.views.TelegramAPI import telegram_bot_sendtext, make_message_telegram


class ServicoFilter(BaseFilter):
    search_fields = {
        'query': ['titulo', 'descricao'],
        'estado': {'operator': '__icontains', 'fields': ['profissional__estado']},
        'cidade': {'operator': '__icontains', 'fields': ['profissional__cidade']},
        'preco_min': {'operator': '__gte', 'fields': ['valor_base']},
        'preco_max': {'operator': '__lte', 'fields': ['valor_base']},
    }


class ProfissionalFilter(BaseFilter):
    search_fields = {
        'query_p': {'operator': '__icontains', 'fields': ['user__username', ]},
        'estado': {'operator': '__icontains', 'fields': ['estado']},
        'cidade': {'operator': '__icontains', 'fields': ['cidade']},
    }


class IndexView(CustomContextMixin, SearchListView):
    model = Servico
    template_name = 'index.html'
    paginate_by = 5
    context_object_name = 'servicos'
    ordering = '?'

    form_class = ServicoSearchForm
    filter_class = ServicoFilter

    def get_params_search(self):
        return self.request.GET

    def get_context_data(self, **kwargs):
        kwargs['params'] = self.get_params_search()
        return super(IndexView, self).get_context_data(**kwargs)

    def get_queryset(self):
        params = self.get_params_search()
        servicos = self.model.objects.filter(is_approved=True, disponivel=True)
        if 'categoria' in params:
            servicos = servicos.filter(profissional__categoria__id=params['categoria'])
        categories = [str(key).replace('_filter', '') for key in params if '_filter' in key]
        if len(categories) > 0:
            servicos = servicos.filter(profissional__categoria_id__in=categories)
        if 'ordering' in params:
            servicos = servicos.order_by(params['ordering'])
        else:
            servicos = servicos.order_by('?')
        return servicos


class AreaProfissional(CustomContextMixin, TemplateView):
    template_name = 'area_profissionals.html'


class ViewServicoDetail(CustomContextMixin, DetailView):
    model = Servico
    template_name = 'item_detail.html'
    context_object_name = 'servico'


class ProfissionalView(CustomContextMixin, SearchListView):
    model = Profissional
    template_name = 'profissionals.html'
    paginate_by = 12
    context_object_name = 'profissionais'
    ordering = '?'

    form_class = ProfissionalSearchForm
    filter_class = ProfissionalFilter

    def get_params_search(self):
        return self.request.GET

    def get_context_data(self, **kwargs):
        kwargs['params'] = self.get_params_search()
        return super(ProfissionalView, self).get_context_data(**kwargs)

    def get_queryset(self):
        params = self.get_params_search()
        profissionais = self.model.objects.filter(is_approved=True)
        if 'categoria' in params:
            profissionais = profissionais.filter(categoria__id=params['categoria'])
        categories = [str(key).replace('_filter', '') for key in params if '_filter' in key]
        if len(categories) > 0:
            profissionais = profissionais.filter(categoria_id__in=categories)
        if 'ordering' in params:
            profissionais = profissionais.order_by(params['ordering'])
        return profissionais


class ListServicesProfissionalView(CustomContextMixin, DetailView):
    model = Profissional
    template_name = 'list-services-profissional.html'
    context_object_name = 'profissional'


class SobreView(CustomContextMixin, TemplateView):
    template_name = 'about.html'


class ContatoView(CustomContextMixin, CreateView):
    template_name = 'contato.html'
    form_class = FormMensagem
    model = Mensagem
    success_url = '/contato/'

    def form_valid(self, form):
        messages.success(self.request, 'Mensagem enviada com sucesso.')
        return super(ContatoView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ocorreu algum erro, tente novamente')
        return super(ContatoView, self).form_invalid(form)


def check_cart(cart, servico):
    if len(cart.itemservico_set.all()) == 0:
        cart.profissional = None
        cart.save()
    if cart.profissional is not None:
        if servico.profissional.id == cart.profissional.id:
            return True
        else:
            return False
    else:
        cart.profissional = servico.profissional
        cart.save()
        return True


def add_item_servico(request, cart):
    observacoes = ''
    servico = None
    if 'observacoes' in request.POST:
        observacoes = request.POST['observacoes']
    if 'idservico' in request.POST:
        servico = Servico.objects.get(id=request.POST['idservico'])
    if check_cart(cart, servico):
        valor_total = servico.valor_base
        item = ItemServico(
            carrinho=cart,
            servico=servico,
            observacoes=observacoes,
            valor_total=valor_total
        )
        item.save()
        cart.save()
    else:
        messages.error(request, 'Você não pode adicionar no carrinho serviços de diferentes profissionais')


def remove_item_servico(request, cart):
    if 'iditemservico' in request.GET:
        item = ItemServico.objects.get(id=request.GET['iditemservico'])
        item.delete()
        cart.save()


def get_cart(request):
    carrinhos = request.user.cliente.carrinhodeservicos_set.filter(status=True)
    if len(carrinhos) > 0:
        carrinho = carrinhos[0]
        carrinho.save()
        return carrinho
    else:
        new_cart = CarrinhoDeServicos(
            cliente=request.user.cliente
        )
        new_cart.save()
        return new_cart


def add_cart(request):
    try:
        if not request.user.is_authenticated:
            return redirect('/login/')
        cart = get_cart(request)
        add_item_servico(request, cart)
        return redirect('/carrinho/' + str(cart.id))
    except (Exception,):
        cart = get_cart(request)
        messages.error(request, 'Ocorreu algum erro, tente novamente.')
        return redirect('/carrinho/' + str(cart.id))


def remove_item_cart(request):
    try:
        if not request.user.is_authenticated:
            return redirect('/login/')
        cart = get_cart(request)
        remove_item_servico(request, cart)
        return redirect('/carrinho/' + str(cart.id))
    except (Exception,):
        cart = get_cart(request)
        messages.error(request, 'Ocorreu algum erro, tente novamente.')
        return redirect('/carrinho/' + str(cart.id))


class CarrinhoView(LoginRequiredMixin, CustomContextMixin, DetailView):
    login_url = '/login/'
    template_name = 'cart.html'
    model = CarrinhoDeServicos
    context_object_name = 'carrinho'


class MeuPerfil(LoginRequiredMixin, CustomContextMixin, UpdateView):
    login_url = '/login/'
    template_name = 'meu-perfil.html'
    model = Cliente
    context_object_name = 'cliente'
    form_class = FormEditCliente

    def get_success_url(self):
        return '/meuperfil/' + str(self.request.user.cliente.pk)

    def form_valid(self, form):
        return super(MeuPerfil, self).form_valid(form)


def gerar_contrato(request):
    carrinho = get_cart(request)
    try:
        if len(carrinho.itemservico_set.all()) < 1:
            messages.error(request, 'Nenhum item no carrinho. Favor selecione algum servico.')
            return redirect('/carrinho/' + str(carrinho.id))
        if 'forma' in request.GET:
            forma = request.GET['forma']
            forma_pgto = FormaPagamento.objects.filter(forma__iexact=forma)
            forma_pgto = forma_pgto.first()
            carrinho.forma_pagamento = forma_pgto
            carrinho.save()
        else:
            messages.error(request, 'Nenhuma forma de pagamento informado.')
            return redirect('/carrinho/' + str(carrinho.id))
        contract = ContratoDeServico(
            carrinho=carrinho,
            cliente=request.user.cliente,
            profissional=carrinho.profissional
        )
        contract.save()
        carrinho.status = False
        carrinho.save()
        try:
            if carrinho.profissional.telegram_bot:
                mensagem = make_message_telegram(contract)
                telegram_bot_sendtext(chat_id=str(carrinho.profissional.telegram_bot.chat_id), message=mensagem)
        except (Exception,):
            print('Erro ao notificar via telegram')
        messages.success(request, 'Contrato gerado. Aguarde o profissional dar andamento ao contrato.')
        return redirect('/meuscontratos/')
    except (Exception,):
        messages.error(request, 'Erro ao gerar contrato, tente novamente.')
        return redirect('/carrinho/' + str(carrinho.id))


def aplicar_cupom(request):
    carrinho = get_cart(request)
    try:
        if 'cupom' in request.GET:
            cupom_code = request.GET['cupom']
            cupons = carrinho.profissional.cupom_set.filter(codigo__iexact=cupom_code)
            if len(cupons) > 0:
                cupom = cupons.first()
                if cupom.is_approved:
                    item_cupom = ItemCupom(cupom=cupom)
                    item_cupom.save()
                    carrinho.cupom = item_cupom
                    carrinho.save()
                    messages.success(request, 'Cupom adicionado com sucesso.')
                    return redirect('/carrinho/' + str(carrinho.id))
                else:
                    messages.error(request, 'Este cupom nao é válido.')
                    return redirect('/carrinho/' + str(carrinho.id))
            else:
                messages.error(request, 'Este cupom nao é válido.')
                return redirect('/carrinho/' + str(carrinho.id))
        else:
            messages.error(request, 'Nenhum cupom informado.')
            return redirect('/carrinho/' + str(carrinho.id))
    except (Exception,):
        messages.error(request, 'Erro ao aplicar o cupom, tente novamente.')
        return redirect('/carrinho/' + str(carrinho.id))


class MeusContratosView(LoginRequiredMixin, CustomContextMixin, ListView):
    login_url = '/login/'
    model = ContratoDeServico
    paginate_by = 5
    template_name = 'meus_contratos.html'
    context_object_name = 'contratos'

    def get_queryset(self):
        return self.model.objects.filter(cliente=self.request.user.cliente).order_by('-published_at')


class DocumentoContrato(LoginRequiredMixin, CustomContextMixin, DetailView):
    login_url = '/login/'
    model = ContratoDeServico
    template_name = 'documento-contrato.html'
    context_object_name = 'contrato'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.cliente.contratodeservico_set.filter(id=self.kwargs['pk']).exists():
            return self.handle_no_permission()
        return super(DocumentoContrato, self).dispatch(request, *args, **kwargs)


class AvaliacaoView(LoginRequiredMixin, CustomContextMixin, UpdateView):
    login_url = '/login/'
    model = ContratoDeServico
    template_name = 'avaliacao.html'
    context_object_name = 'contrato'
    form_class = FormContratoAvaliacao
    success_url = '/meuscontratos/'

    def get_queryset(self):
        return super(AvaliacaoView, self).get_queryset()

    def get_context_data(self, **kwargs):
        data = super(AvaliacaoView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['form_avaliacao'] = FormComentario(self.request.POST, self.request.FILES)
        else:
            data['form_avaliacao'] = FormComentario(initial={'cliente': self.request.user.cliente,
                                                             'servico': self.object.carrinho.itemservico_set.first().servico})
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form_avaliacao = context['form_avaliacao']
        with transaction.atomic():
            if form_avaliacao.is_valid():
                form_avaliacao.save()
                self.object = form.save()
                contrato = self.object
                contrato.is_avaliado = True
                contrato.save()
                messages.success(self.request, 'Avaliacao realizada com sucesso.')
            else:
                return self.form_invalid(form)
        return super(AvaliacaoView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ocorreu algum erro, tente novamente')
        return super(AvaliacaoView, self).form_invalid(form)
