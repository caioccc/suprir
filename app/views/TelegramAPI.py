import requests
from django.core.mail import send_mail


BOT_TOKEN = '1072888475:AAGL8G9-Pv1K7wsLpRlmGgh5xEDeZfom-GY'


def telegram_bot_sendtext(chat_id, message):
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=html&text=' + message
    response = requests.get(send_text)
    return response.json()


def make_message_telegram(contratoDeServico):
    message = '<b>NOVO CONTRATO GERADO</b>\n\n<pre> Cliente: ' + contratoDeServico.cliente.user.first_name + ' ' + \
              contratoDeServico.cliente.user.last_name + '</pre>\n\n<pre>Valor Total: ' + str(contratoDeServico.carrinho.valor_total) + '</pre>\n\n<pre>' + \
              contratoDeServico.carrinho.forma_pagamento.forma + '</pre>\n<pre>Telefone Cliente: ' + contratoDeServico.cliente.user.username + '</pre>\n\n<pre>Link:</pre>' + \
              '<a href="http://localhost:8000/painel/">http://localhost:8000/painel/</a>'
    return message


def telegram_bot_sendphoto(photo):
    bot_chatID = '451429199'
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendPhoto?chat_id=' + bot_chatID + '&parse_mode=html&photo=' + photo
    response = requests.get(send_text)
    return response.json()


def get_chat_ids():
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/getUpdates?limit=300'
    response = requests.get(send_text)
    result = response.json()
    dic = []
    if len(result['result']) > 0:
        for item in result['result']:
            chat = item['message']['chat']
            dic.append({
                'id': chat['id'],
                'first_name': chat['first_name'],
                'last_name': chat['last_name'],
                'username': chat['username']
            })
    return dic


def send_mail_and_telegram(object_custom_user, mensagem, titulo_email, ):
    try:
        if object_custom_user.telegram_bot:
            telegram_bot_sendtext(chat_id=str(object_custom_user.telegram_bot.chat_id), message=mensagem)
    except (Exception,):
        print('Erro ao notificar ' + titulo_email + ' para ' + str(object_custom_user) +
              ' via telegram')
    try:
        if object_custom_user.email:
            send_mail(subject=titulo_email, message=mensagem,
                      from_email='suporte.suprir@gmail.com', recipient_list=(str(object_custom_user.email),))
    except (Exception,):
        print('Erro ao notificar ' + titulo_email + ' para ' + str(object_custom_user) +
              ' via email')


def send_mail_and_telegram_admin(object_custom_user, mensagem, titulo_email):
    try:
        if object_custom_user.telegram_bot:
            telegram_bot_sendtext(chat_id=str(object_custom_user.telegram_bot.chat_id), message=mensagem)
    except (Exception,):
        print('Erro ao notificar ' + titulo_email + ' para ' + str(object_custom_user) +
              ' via telegram')
    if object_custom_user.email:
        send_mail(subject=titulo_email, message=mensagem,
                  from_email='suporte.suprir@gmail.com', recipient_list=(str(object_custom_user.email),))