from django import template
from datetime import datetime, timedelta, time

from app.models import CarrinhoDeServicos

register = template.Library()


@register.filter
def get_user_name(user):
    try:
        return user.first_name
    except (Exception,):
        return ''


@register.filter
def get_qtd_servicos_realizados_mes(user):
    now = datetime.now()
    return len(user.profissional.contratodeservico_set.filter(created_at__month=now.month, status='REALIZADO'))


@register.filter
def get_qtd_servicos_em_andamento(user):
    now = datetime.now()
    try:
        return len(user.profissional.contratodeservico_set.filter(created_at__month=now.month, status='EM ANDAMENTO'))
    except (Exception,):
        return 0


@register.filter
def get_carrinhos_em_aberto(user):
    try:
        return user.profissional.carrinhodeservicos_set.order_by('-created_at').filter(status=True)
    except (Exception,):
        return 0


@register.filter
def get_qtd_meus_servicos_cadastrados(user):
    try:
        return len(user.profissional.servico_set.all())
    except (Exception,):
        return 0
