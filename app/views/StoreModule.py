from django.shortcuts import render

# Create your views here.
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
        print(filter_categorias)
        return filter_categorias


class IndexView(UserLoggedMixin, CustomContextMixin, ListView):
    model = Servico
    template_name = 'index.html'
    ordering = '?'
    context_object_name = 'servicos'


class AreaProfissional(CustomContextMixin, TemplateView):
    template_name = 'area_profissionals.html'
