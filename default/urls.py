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
from app.views.PanelModule import DashboardView
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

]
