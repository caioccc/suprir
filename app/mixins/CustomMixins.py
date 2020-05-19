# coding=utf-8
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class UserLoggedMixin(object):
    DASHBOARD_PROFISSIONAL_URL = '/painel/'
    INDEX_URL = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            print('logged user:', request.user)
            try:
                if request.user.profissional:
                    print('Logged pro:', request.user.profissional)
                    return redirect(self.DASHBOARD_PROFISSIONAL_URL)
            except (Exception,):
                return super(UserLoggedMixin, self).dispatch(request, *args, **kwargs)
        return super(UserLoggedMixin, self).dispatch(request, *args, **kwargs)


class ProfessionalUserRequiredMixin(AccessMixin):
    login_url = '/login/'
    """
    CBV mixin which verifies that the current user is authenticated.
    """

    def dispatch(self, request, *args, **kwargs):
        try:
            pro = request.user.profissional
            print('logged profissional:', pro)
        except (Exception,):
            return self.handle_no_permission()
        return super(ProfessionalUserRequiredMixin, self).dispatch(request, *args, **kwargs)
