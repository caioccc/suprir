# coding=utf-8
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from app.mixins.CustomMixins import UserLoggedMixin
from app.models import Servico, CategoriaDeProfissional, Profissional


class CustomContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        kwargs['categorias'] = CategoriaDeProfissional.objects.all()
        kwargs['estados'] = self.get_estados()
        kwargs['cidades'] = self.get_cidades()
        kwargs['filter_categorias'] = self.get_filter_categorias()
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


class IndexView(UserLoggedMixin, CustomContextMixin, ListView):
    model = Servico
    template_name = 'index.html'
    paginate_by = 5
    context_object_name = 'servicos'

    def get_params_search(self):
        return self.request.GET

    def get_context_data(self, **kwargs):
        kwargs['params'] = self.get_params_search()
        return super(IndexView, self).get_context_data(**kwargs)

    def get_queryset(self):
        params = self.get_params_search()
        servicos = self.model.objects.all()
        if 'estado' in params:
            servicos = self.model.objects.filter(profissional__estado__icontains=params['estado'])
        if 'cidade' in params:
            servicos = servicos.filter(profissional__cidade__icontains=params['cidade'])
        if 'query' in params:
            servicos = servicos.filter(titulo__icontains=params['query'])
        if 'categoria' in params:
            servicos = servicos.filter(profissional__categoria__id=params['categoria'])
        categories = [str(key).replace('_filter', '') for key in params if '_filter' in key]
        if len(categories) > 0:
            servicos = servicos.filter(profissional__categoria_id__in=categories)
        return servicos.order_by('?')


class AreaProfissional(CustomContextMixin, TemplateView):
    template_name = 'area_profissionals.html'
