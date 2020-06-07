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
    ClienteList, EditarPerfilView, RejeiteContratoForm, andamento_contrato_servico, ListCupons, CreateCupom, EditCupom, RemoveCupom, DocumentoContratoProfissional, EditEntrada, DeleteEntrada, \
    CreateEntrada, ListEntradas, ListSaidas, CreateSaida, EditSaida, DeleteSaida, FluxoCaixa, get_month_data, ListInteresse, CreateInteresse, UpdateInteresse, DeleteInteresse, ListPropostas, \
    CreateProposta, DeleteProposta, reject_bid, generate_process, ListProcessos, ViewProcesso, FinalizarProcesso, DocumentoContratoComCliente, ComoFuncionaFQEF
from app.views.StoreModule import IndexView, AreaProfissional, ViewServicoDetail, ProfissionalView, SobreView, \
    ContatoView, add_cart, CarrinhoView, remove_item_cart, MeuPerfil, ListServicesProfissionalView, MeusContratosView, \
    DocumentoContrato, gerar_contrato, aplicar_cupom, AvaliacaoView, RegrasETermos, PoliticaPrivacidade, ComoFunciona, PerguntasFrequentes

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
    url(r'^avaliar/(?P<pk>[0-9]+)/$', AvaliacaoView.as_view(), name='avaliar-servico'),
    url(r'^regras-e-termos/$', RegrasETermos.as_view(), name='regras-e-termos'),
    url(r'^politica-de-privacidade/$', PoliticaPrivacidade.as_view(), name='politica-de-privacidade'),
    url(r'^como-funciona/$', ComoFunciona.as_view(), name='como-funciona'),
    url(r'^perguntas-frequentes/$', PerguntasFrequentes.as_view(), name='perguntas-frequentes'),

    url(r'^startsystemdefault/$', StartSystem.as_view(), name='startsystem'),
    url(r'^starttestdefault/$', StartTestSystem.as_view(), name='starttestsystem'),

    url(r'^painel/$', DashboardView.as_view(), name='dashboard-profissional'),
    url(r'^painel/documento/(?P<pk>[0-9]+)$', DocumentoContratoComCliente.as_view(), name='documento-contrato-com-cliente'),
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
    url(r'^painel/cupons/$', ListCupons.as_view(), name='list-cupons'),
    url(r'^painel/cupons/create/$', CreateCupom.as_view(), name='create-cupom'),
    url(r'^painel/cupons/(?P<pk>[0-9]+)/$', EditCupom.as_view(), name='edit-cupom'),
    url(r'^painel/cupons/delete/(?P<pk>[0-9]+)/$', RemoveCupom.as_view(), name='delete-cupom'),
    url(r'^painel/entradas/$', ListEntradas.as_view(), name='list-entradas'),
    url(r'^painel/entradas/create/$', CreateEntrada.as_view(), name='create-entrada'),
    url(r'^painel/entradas/(?P<pk>[0-9]+)/$', EditEntrada.as_view(), name='edit-entrada'),
    url(r'^painel/entradas/delete/(?P<pk>[0-9]+)/$', DeleteEntrada.as_view(), name='delete-entrada'),
    url(r'^painel/saidas/$', ListSaidas.as_view(), name='list-saidas'),
    url(r'^painel/saidas/create/$', CreateSaida.as_view(), name='create-saida'),
    url(r'^painel/saidas/(?P<pk>[0-9]+)/$', EditSaida.as_view(), name='edit-saida'),
    url(r'^painel/saidas/delete/(?P<pk>[0-9]+)/$', DeleteSaida.as_view(), name='delete-saida'),
    url(r'^painel/fluxocaixa/$', FluxoCaixa.as_view(), name='fluxo-caixa'),
    url(r'^painel/fluxocaixa/get-data/$', get_month_data, name='get-data-fluxo'),
    url(r'^painel/faz-que-eu-faco/$', ComoFuncionaFQEF.as_view(), name='como-funciona-fqef'),
    url(r'^painel/interesses/$', ListInteresse.as_view(), name='list-interesses'),
    url(r'^painel/interesses/create/$', CreateInteresse.as_view(), name='create-interesse'),
    url(r'^painel/interesses/(?P<pk>[0-9]+)/$', UpdateInteresse.as_view(), name='edit-interesse'),
    url(r'^painel/interesses/delete/(?P<pk>[0-9]+)/$', DeleteInteresse.as_view(), name='delete-interesse'),
    url(r'^painel/propostas/$', ListPropostas.as_view(), name='list-propostas'),
    url(r'^painel/propostas/create/(?P<pk>[0-9]+)/$', CreateProposta.as_view(), name='create-proposta'),
    url(r'^painel/propostas/delete/(?P<pk>[0-9]+)/$', DeleteProposta.as_view(), name='delete-proposta'),
    url(r'^painel/propostas/reject/(?P<pk>[0-9]+)/$', reject_bid, name='rejeitar-proposta'),
    url(r'^painel/propostas/acept/(?P<pk>[0-9]+)/$', generate_process, name='aceitar-proposta'),
    url(r'^painel/processo/documento/(?P<pk>[0-9]+)$', DocumentoContratoProfissional.as_view(), name='documento-contrato-pro'),
    url(r'^painel/processos/$', ListProcessos.as_view(), name='list-processos'),
    url(r'^painel/processos/view/(?P<pk>[0-9]+)/$', ViewProcesso.as_view(), name='view-processo'),
    url(r'^painel/processos/finalizar/(?P<pk>[0-9]+)/$', FinalizarProcesso.as_view(), name='finalizar-processo'),
]
