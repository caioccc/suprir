from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from app.mixins.CustomMixins import UserLoggedMixin


class IndexView(UserLoggedMixin, TemplateView):
    template_name = 'index.html'


class AreaProfissional(TemplateView):
    template_name = 'area_profissionals.html'
