# coding=utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView

from app.forms import FormLogin


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
                return self.form_invalid(form)
        except (Exception,):
            pass

        if user is not None:
            login(self.request, user)
        else:
            return self.form_invalid(form)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Nenhum usuário encontrado')
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
