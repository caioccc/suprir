from django import template
from datetime import datetime, timedelta, time

from app.models import CarrinhoDeServicos, ContratoDeServico

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


@register.filter
def get_numero_telefone_zap(telefone):
    try:
        telefone = str(telefone)
        if telefone[0] == '0':
            telefone = telefone[1:]
        if len(telefone) < 10:
            telefone = '5583' + telefone
        else:
            telefone = '55' + telefone
        return telefone
    except (Exception,):
        return telefone


@register.filter
def get_avaliacao_media(servico):
    try:
        sum = 0
        qtd = 0
        comms = servico.comentarioservico_set.all()
        for com in comms:
            if com.avaliacao:
                qtd += 1
                sum += int(com.avaliacao)
        return int(sum / qtd)
    except (Exception,):
        return 0


@register.filter
def get_qtd_realizados(servico):
    try:
        sum = 0
        for cont in ContratoDeServico.objects.filter(profissional=servico.profissional, status='REALIZADO'):
            for item_servico in cont.carrinho.itemservico_set.all():
                if item_servico.servico.id == servico.id:
                    sum += 1
        return int(sum)
    except (Exception,):
        return 0


@register.filter
def get_url_search(params):
    try:
        strin = ''
        for key in params:
            if key != 'page':
                strin += ('&' + str(key) + '=' + str(params[key]))
        return strin
    except (Exception,):
        return ''
