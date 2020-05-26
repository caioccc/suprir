import requests

from app.models import ContratoDeServico

BOT_TOKEN = '1072888475:AAGL8G9-Pv1K7wsLpRlmGgh5xEDeZfom-GY'


def telegram_bot_sendtext(chat_id, message):
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=html&text=' + message
    response = requests.get(send_text)
    return response.json()


def make_message_telegram(contratoDeServico=ContratoDeServico):
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
