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

from app.views.LoginModule import LoginView, LogoutView, RegistroCliente, RegistroProfissional, StartSystem, \
    StartTestSystem
from app.views.PanelModule import DashboardView, ContractUpdateView, \
    finalizar_contrato_servico, ServicosList, CreateServico, UpdateServico, DeleteServico, ListComentarios, RevisaoView, \
    ClienteList, EditarPerfilView, RejeiteContratoForm, andamento_contrato_servico
from app.views.StoreModule import IndexView, AreaProfissional, ViewServicoDetail, ProfissionalView, SobreView, \
    ContatoView, add_cart, CarrinhoView, remove_item_cart, MeuPerfil, ListServicesProfissionalView, MeusContratosView, \
    DocumentoContrato, gerar_contrato, aplicar_cupom

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/login/$', auth_views.login),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', ViewServicoDetail.as_view(), name='view-servico'),
    url(r'^profissionais/$', ProfissionalView.as_view(), name='list-profissionais'),
    url(r'^profissionais/(?P<pk>[0-9]+)/$', ListServicesProfissionalView.as_view(), name='list-services-profissional'),
    url(r'^sobre/$', SobreView.as_view(), name='sobre'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^account/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^registro/$', RegistroCliente.as_view(), name='registro-cliente'),
    url(r'^area-profissional/$', AreaProfissional.as_view(), name='area-profissional'),
    url(r'^area-profissional/registro/$', RegistroProfissional.as_view(), name='registro-profissional'),
    url(r'^contato/$', ContatoView.as_view(), name='fale-conosco'),
    url(r'^add-cart/$', add_cart, name='add-carrinho'),
    url(r'^remove-item-cart/$', remove_item_cart, name='remove-item-carrinho'),
    url(r'^carrinho/(?P<pk>[0-9]+)/$', CarrinhoView.as_view(), name='carrinho'),
    url(r'^meuperfil/(?P<pk>[0-9]+)/$', MeuPerfil.as_view(), name='meu-perfil'),
    url(r'^meuscontratos/$', MeusContratosView.as_view(), name='meus-contratos'),
    url(r'^meuscontratos/documento/(?P<pk>[0-9]+)$', DocumentoContrato.as_view(), name='documento-contrato'),
    url(r'^gerarcontrato/$', gerar_contrato, name='gerar-contrato'),
    url(r'^aplicar-cupom/$', aplicar_cupom, name='aplicar-cupom'),

    url(r'^startsystemdefault/$', StartSystem.as_view(), name='startsystem'),
    url(r'^starttestdefault/$', StartTestSystem.as_view(), name='starttestsystem'),

    url(r'^painel/$', DashboardView.as_view(), name='dashboard-profissional'),
    url(r'^painel/edit/(?P<pk>[0-9]+)/$', ContractUpdateView.as_view(), name='editar-contrato'),
    url(r'^painel/finalizar/(?P<pk>[0-9]+)/$', finalizar_contrato_servico, name='finalizar-contrato'),
    url(r'^painel/andamento/(?P<pk>[0-9]+)/$', andamento_contrato_servico, name='andamento-contrato'),
    url(r'^painel/rejeite/(?P<pk>[0-9]+)/$', RejeiteContratoForm.as_view(), name='rejeite-contrato-form'),

    url(r'^painel/clientes/$', ClienteList.as_view(), name='list-clientes'),
    url(r'^painel/servicos/$', ServicosList.as_view(), name='list-servicos'),
    url(r'^painel/servicos/create/$', CreateServico.as_view(), name='create-servico'),
    url(r'^painel/servicos/(?P<pk>[0-9]+)/$', UpdateServico.as_view(), name='edit-servico'),
    url(r'^painel/servicos/delete/(?P<pk>[0-9]+)/$', DeleteServico.as_view(), name='delete-servico'),
    url(r'^painel/comentarios/$', ListComentarios.as_view(), name='list-comentarios'),
    url(r'^painel/comentarios/revisao/(?P<pk>[0-9]+)/$', RevisaoView.as_view(), name='revisao-servico'),
    url(r'^painel/perfil/(?P<pk>[0-9]+)/$', EditarPerfilView.as_view(), name='editar-perfil'),
]
