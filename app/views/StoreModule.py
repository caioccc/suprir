# coding=utf-8
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView
from django.views.generic import TemplateView
from search_views.filters import BaseFilter
from search_views.views import SearchListView

from app.forms import ServicoSearchForm, ProfissionalSearchForm, FormMensagem
from app.mixins.CustomMixins import UserLoggedMixin, CustomContextMixin
from app.models import Servico, Profissional, Mensagem, CarrinhoDeServicos, ItemServico


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
        servicos = self.model.objects.all()
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
        profissionais = self.model.objects.all()
        if 'categoria' in params:
            profissionais = profissionais.filter(categoria__id=params['categoria'])
        categories = [str(key).replace('_filter', '') for key in params if '_filter' in key]
        if len(categories) > 0:
            profissionais = profissionais.filter(categoria_id__in=categories)
        if 'ordering' in params:
            profissionais = profissionais.order_by(params['ordering'])
        return profissionais


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
    if 'iditemservico' in request.POST:
        item = ItemServico.objects.get(id=request.POST['iditemservico'])
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
    template_name = 'cart.html'
    model = CarrinhoDeServicos
    context_object_name = 'carrinho'
