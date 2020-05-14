# coding=utf-8
from django.contrib.auth.mixins import AccessMixin


class ProfessionalUserRequiredMixin(AccessMixin):
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
