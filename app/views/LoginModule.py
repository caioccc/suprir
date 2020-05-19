# coding=utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import FormView, RedirectView

from app.forms import FormLogin, FormRegisterCliente, FormRegisterProfissional
from app.models import Cliente, Profissional


class LoginView(FormView):
    """
    Displays the login form.
    """
    template_name = 'login.html'
    form_class = FormLogin
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(**data)
        print(user)
        try:
            profissional = user.profissional
            if not profissional.is_approved:
                messages.error(self.request, 'Usuário ainda não foi aprovado. Aguarde 24 horas!')
                return self.form_invalid(form)
        except (Exception,):
            pass

        if user is not None:
            login(self.request, user)
        else:
            messages.error(self.request, 'Nenhum usuário encontrado')
            return self.form_invalid(form)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        url = '/'
        profissional = None
        cliente = None
        try:
            user = self.request.user
        except (Exception,):
            user = None
        try:
            profissional = user.profissional
        except (Exception,):
            pass

        try:
            cliente = user.cliente
        except (Exception,):
            pass

        if user:
            if profissional:
                url = '/painel/'
                self.success_url = url
            elif cliente:
                url = '/'
                self.success_url = url
            elif user.is_superuser:
                url = '/admin/'
                self.success_url = url
            else:
                url = '/'
                self.success_url = url
        else:
            url = '/'
            self.success_url = url
        return url


class LogoutView(RedirectView):
    url = '/'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegistroCliente(FormView):
    template_name = 'register-client.html'
    form_class = FormRegisterCliente
    success_url = '/login/'

    def get(self, request, *args, **kwargs):
        return super(RegistroCliente, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('')
        return super(RegistroCliente, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        user_data = {}
        if len(data['telefone']) < 10:
            messages.error(self.request, 'Insira um Telefone valido')
            return self.form_invalid(form)
        if len(data['password']) < 5:
            messages.error(self.request, 'Insira uma senha maior que 5 caracteres')
            return self.form_invalid(form)
        user_data['username'] = data['telefone']
        user_data['first_name'] = data['nome']
        user_data['last_name'] = data['sobrenome']
        user_data['password'] = data['password']
        data_address_client = self.get_address_client(data)
        try:
            user = User.objects.create_user(**user_data)
            cliente = Cliente(
                telefone_1=data['telefone'],
                user=user,
                whatsapp=data['telefone'],
                **data_address_client
            )
            cliente.save()
        except (Exception,):
            messages.error(self.request, 'Ja existe uma conta com este numero')
            return self.form_invalid(form)
        messages.success(self.request, 'Registrado com Sucesso')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return super(RegistroCliente, self).form_invalid(form)

    def get_address_client(self, data):
        data_pro = {}
        if 'cep' in data:
            data_pro['cep'] = data['cep']
        if 'bairro' in data:
            data_pro['bairro'] = data['bairro']
        if 'endereco' in data:
            data_pro['endereco'] = data['endereco']
        if 'numero' in data:
            data_pro['numero'] = data['numero']
        if 'cidade' in data:
            data_pro['cidade'] = data['cidade']
        if 'estado' in data:
            data_pro['estado'] = str(data['estado']).upper()
        return data_pro


class RegistroProfissional(FormView):
    template_name = 'register-profissional.html'
    form_class = FormRegisterProfissional
    success_url = '/login/'

    def get(self, request, *args, **kwargs):
        return super(RegistroProfissional, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('')
        return super(RegistroProfissional, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        user_data = {}
        if len(data['telefone']) < 10:
            messages.error(self.request, 'Insira um Telefone valido')
            return self.form_invalid(form)
        if len(data['password']) < 5:
            messages.error(self.request, 'Insira uma senha maior que 5 caracteres')
            return self.form_invalid(form)
        user_data['username'] = data['telefone']
        user_data['first_name'] = data['nome']
        user_data['last_name'] = data['sobrenome']
        user_data['password'] = data['password']
        data_pro = self.get_profissional_data(data)
        try:
            user = User.objects.create_user(**user_data)
            profissional = Profissional(
                telefone_1=data['telefone'],
                user=user,
                **data_pro
            )
            profissional.save()
        except (Exception,):
            messages.error(self.request, 'Ja existe uma conta com este numero')
            return self.form_invalid(form)
        messages.success(self.request, 'Registrado com Sucesso. Aguarde 24 horas para ser aprovado!')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return super(RegistroProfissional, self).form_invalid(form)

    def get_profissional_data(self, data):
        data_pro = {}
        if 'cpf' in data:
            data_pro['cpf'] = data['cpf']
        if 'cnpj' in data:
            data_pro['cnpj'] = data['cnpj']
        if 'cep' in data:
            data_pro['cep'] = data['cep']
        if 'bairro' in data:
            data_pro['bairro'] = data['bairro']
        if 'endereco' in data:
            data_pro['endereco'] = data['endereco']
        if 'numero' in data:
            data_pro['numero'] = data['numero']
        if 'cidade' in data:
            data_pro['cidade'] = data['cidade']
        if 'estado' in data:
            data_pro['estado'] = str(data['estado']).upper()
        if 'telefone_2' in data:
            data_pro['telefone_2'] = data['telefone_2']
            data_pro['whatsapp'] = data['telefone_2']
        if 'categoria' in data:
            data_pro['categoria'] = data['categoria']
        if 'link_facebook' in data:
            data_pro['link_facebook'] = data['link_facebook']
        if 'link_instagram' in data:
            data_pro['link_instagram'] = data['link_instagram']
        if 'url_site' in data:
            data_pro['url_site'] = data['url_site']
        return data_pro
