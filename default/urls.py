"""default URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app.views.LoginModule import LoginView, LogoutView, RegistroCliente, RegistroProfissional
from app.views.PanelModule import DashboardView, ContractUpdateView, rejeitar_contrato_servico, \
    finalizar_contrato_servico, ServicosList, CreateServico, UpdateServico, DeleteServico
from app.views.StoreModule import IndexView, AreaProfissional

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/login/$', auth_views.login),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^account/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^registro/$', RegistroCliente.as_view(), name='registro-cliente'),
    url(r'^area-profissional/$', AreaProfissional.as_view(), name='area-profissional'),
    url(r'^area-profissional/registro/$', RegistroProfissional.as_view(), name='registro-profissional'),

    url(r'^painel/$', DashboardView.as_view(), name='dashboard-profissional'),
    url(r'^painel/edit/(?P<pk>[0-9]+)/$', ContractUpdateView.as_view(), name='editar-contrato'),
    url(r'^painel/finalizar/(?P<pk>[0-9]+)/$', finalizar_contrato_servico, name='finalizar-contrato'),
    url(r'^painel/rejeitar/(?P<pk>[0-9]+)/$', rejeitar_contrato_servico, name='rejeitar-contrato'),
    url(r'^painel/servicos/$', ServicosList.as_view(), name='list-servicos'),
    url(r'^painel/servicos/create/$', CreateServico.as_view(), name='create-servico'),
    url(r'^painel/servicos/(?P<pk>[0-9]+)/$', UpdateServico.as_view(), name='edit-servico'),
    url(r'^painel/servicos/delete/(?P<pk>[0-9]+)/$', DeleteServico.as_view(), name='delete-servico'),
]
