# coding=utf-8
from __future__ import unicode_literals

from base64 import b64encode

import pyimgur
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from app.views.TelegramAPI import send_mail_and_telegram_admin


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)


class BaseAddress(models.Model):
    class Meta:
        abstract = True

    cep = models.CharField(max_length=200, blank=True, null=True, verbose_name='CEP')
    bairro = models.CharField(max_length=200, blank=True, null=True, verbose_name='Bairro')
    endereco = models.CharField(max_length=300, blank=True, null=True, verbose_name='Endereço')
    numero = models.CharField(max_length=5, blank=True, null=True, verbose_name='Número')
    cidade = models.CharField(max_length=200, blank=True, null=True, verbose_name='Cidade')
    estado = models.CharField(max_length=200, blank=True, null=True, verbose_name='Estado')
    complemento = models.CharField(max_length=300, blank=True, null=True, verbose_name='Ponto de Referência')
    lat = models.CharField(max_length=300, blank=True, null=True)
    lng = models.CharField(max_length=300, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            self.numero = self.numero.replace("_", "")
        except (Exception,):
            pass
        super(BaseAddress, self).save(*args, **kwargs)


class CommonUserData(TimeStamped, BaseAddress):
    class Meta:
        abstract = True

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, blank=True, null=True)
    telefone_1 = models.CharField(max_length=30, blank=True, null=True)
    whatsapp = models.CharField(max_length=30, blank=True, null=True)
    photo = models.URLField(blank=True, null=True, default='https://placehold.it/300x300')
    cpf = models.CharField(max_length=100, blank=True, null=True, default="")
    cnpj = models.CharField(max_length=100, blank=True, null=True, default="")
    is_online = models.BooleanField(default=False)
    file = models.FileField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            self.telefone_1 = self.telefone_1.replace("_", "")
            self.whatsapp = self.whatsapp.replace("_", "")
        except (Exception,):
            pass
        try:
            CLIENT_ID = "cdadf801dc167ab"
            bencode = b64encode(self.file.read())
            client = pyimgur.Imgur(CLIENT_ID)
            r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': bencode})
            file = r['link']
            self.photo = file
        except (Exception,):
            pass
        super(CommonUserData, self).save(*args, **kwargs)

    def __str__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)

    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)


class TelegramBot(TimeStamped):
    class Meta:
        verbose_name = u'Telegram Bot'
        verbose_name_plural = u'Telegram Bots'

    first_name = models.CharField(max_length=300, blank=True, null=True)
    chat_id = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=300, blank=True, null=True)
    is_approved = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.chat_id

    def __str__(self):
        return u'%s' % self.chat_id


class EmailOuTelegramaAdmin(TimeStamped):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    message = models.TextField()
    title = models.CharField(max_length=200)
    enviado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        customuser = None
        try:
            customuser = self.user.cliente
        except (Exception,):
            print('Nao eh cliente')
        try:
            customuser = self.user.profissional
        except (Exception,):
            print('Nao eh profissional')
        try:
            send_mail_and_telegram_admin(customuser, self.message, self.title)
            self.enviado = True
        except (Exception,):
            print('erro ao enviar mensagem')
        return super(EmailOuTelegramaAdmin, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


class RecycleTelegramItem(TimeStamped):
    class Meta:
        verbose_name = u'Telegram Bot Reciclavel'
        verbose_name_plural = u'Bots Reciclaveis'

    first_name = models.CharField(max_length=300, blank=True, null=True)
    chat_id = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=300, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


class Cliente(CommonUserData):
    class Meta:
        verbose_name = u'Cliente'
        verbose_name_plural = u'Clientes'


class CategoriaDeProfissional(TimeStamped):
    class Meta:
        verbose_name = u'Categoria de Profissional'
        verbose_name_plural = u'Categorias de Profissional'

    categoria = models.CharField(max_length=300, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.categoria

    def __unicode__(self):
        return "%s" % self.categoria


class Profissional(CommonUserData):
    class Meta:
        verbose_name = u'Profissional'
        verbose_name_plural = u'Profissionais'

    categoria = models.ForeignKey(CategoriaDeProfissional, blank=True, null=True, on_delete=models.CASCADE)
    telefone_2 = models.CharField(max_length=30, blank=True, null=True)
    link_facebook = models.URLField(blank=True, null=True)
    link_instagram = models.URLField(blank=True, null=True)
    url_site = models.URLField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    telegram_bot = models.ForeignKey(TelegramBot, blank=True, null=True)
    receber_pelo_sistema = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            self.telefone_2 = self.telefone_2.replace("_", "")
        except (Exception,):
            pass
        super(Profissional, self).save(*args, **kwargs)


class CategoriaDeServico(TimeStamped):
    class Meta:
        verbose_name = u'Categoria de Servico'
        verbose_name_plural = u'Categorias de Servico'

    categoria = models.CharField(max_length=300, blank=True, null=True, )
    profissional = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE)
    disponivel = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.categoria

    def __unicode__(self):
        return "%s" % self.categoria


class Servico(TimeStamped):
    class Meta:
        verbose_name = u'Servico'
        verbose_name_plural = u'Servicos'

    categoria = models.ForeignKey(CategoriaDeServico, blank=True, null=True)
    titulo = models.CharField(max_length=300, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    profissional = models.ForeignKey(Profissional, blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)
    valor_a_combinar = models.BooleanField(default=False)
    valor_base = MoneyField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Money(0, 'BRL'))])

    def __str__(self):
        return "%s" % self.titulo

    def __unicode__(self):
        return "%s" % self.titulo

    def save(self, *args, **kwargs):
        super(Servico, self).save(*args, **kwargs)


class AdicionalDeServico(TimeStamped):
    class Meta:
        verbose_name = u'Adicional de Servico'
        verbose_name_plural = u'Adicionais de Servicos'

    titulo = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.CharField(max_length=300, blank=True, null=True)
    servico = models.ForeignKey(Servico, blank=True, null=True, on_delete=models.CASCADE)
    valor = MoneyField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Money(0, 'BRL'))])
    disponivel = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.titulo

    def __str__(self):
        return u'%s' % self.titulo

    def save(self, *args, **kwargs):
        self.valor = float(str(self.valor).replace(',', '.'))
        super(AdicionalDeServico, self).save(*args, **kwargs)


class FotoServico(TimeStamped):
    class Meta:
        verbose_name = u'Foto de Servico'
        verbose_name_plural = u'Fotos de Servicos'

    servico = models.ForeignKey(Servico, blank=True, null=True, on_delete=models.CASCADE)
    url = models.URLField(blank=True, null=True, default='https://placehold.it/300x300')
    file = models.FileField(blank=True, null=True)
    is_approved = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.url

    def __str__(self):
        return u'%s' % self.url

    def save(self, *args, **kwargs):
        try:
            CLIENT_ID = "cdadf801dc167ab"
            bencode = b64encode(self.file.read())
            client = pyimgur.Imgur(CLIENT_ID)
            r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': bencode})
            file = r['link']
            self.url = file
        except (Exception,):
            pass
        return super(FotoServico, self).save(*args, **kwargs)


class FormaPagamento(TimeStamped):
    class Meta:
        verbose_name = u'Forma de Pagamento'
        verbose_name_plural = u'Formas de Pagamento'

    forma = models.CharField(max_length=100, blank=True, null=True, default="DINHEIRO")

    def __unicode__(self):
        return u'%s' % self.forma

    def __str__(self):
        return u'%s' % self.forma


STATUS_CONTRATO = (
    ('ABERTO', 'ABERTO'),
    ('EM ANDAMENTO', 'EM ANDAMENTO'),
    ('REJEITADO', 'REJEITADO'),
    ('REALIZADO', 'REALIZADO'),
)


class Cupom(TimeStamped):
    class Meta:
        verbose_name = u'Cupom'
        verbose_name_plural = u'Cupons'

    profissional = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=300)
    valor_de_desconto = MoneyField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Money(0, 'BRL'))])
    is_approved = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


class ItemCupom(TimeStamped):
    class Meta:
        verbose_name = u'Item de Cupom'
        verbose_name_plural = u'Itens de Cupom'

    cupom = models.ForeignKey(Cupom, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


class CarrinhoDeServicos(TimeStamped, BaseAddress):
    class Meta:
        verbose_name = u'Carrinho de Servico'
        verbose_name_plural = u'Carrinhos de Servicos'

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    profissional = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE)
    subtotal = MoneyField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Money(0, 'BRL'))])
    valor_total = MoneyField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Money(0, 'BRL'))])
    forma_pagamento = models.ForeignKey(FormaPagamento, blank=True, null=True, on_delete=models.CASCADE)
    status = models.BooleanField(blank=True, default=True)
    cupom = models.ForeignKey(ItemCupom, blank=True, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id

    def save(self, *args, **kwargs):
        subtotal = 0.0
        for item in self.itemservico_set.all():
            subtotal = subtotal + item.valor_total
        if self.cupom:
            subtotal = subtotal - self.cupom.cupom.valor_de_desconto
        self.subtotal = subtotal
        self.valor_total = subtotal
        super(CarrinhoDeServicos, self).save(*args, **kwargs)


class ItemServico(TimeStamped):
    class Meta:
        verbose_name = u'Item Servico'
        verbose_name_plural = u'Itens Servicos'

    carrinho = models.ForeignKey(CarrinhoDeServicos, blank=True, null=True, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, blank=True, null=True, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)
    valor_total = MoneyField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Money(0, 'BRL'))])

    def save(self, *args, **kwargs):
        if not self.servico.valor_a_combinar:
            valor_base = self.servico.valor_base
            valor_opcionais = 0.0
            if self.adicionalescolhido_set.first():
                for opc in self.adicionalescolhido_set.all():
                    valor_opcionais = valor_opcionais + opc.adicional.valor
            valor_unitario = valor_base + valor_opcionais
            self.valor_total = valor_unitario
        else:
            self.valor_total = Money(0, 'BRL')
        super(ItemServico, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


class AdicionalEscolhido(TimeStamped):
    class Meta:
        verbose_name = u'Adicional Escolhido'
        verbose_name_plural = u'Adicionais Escolhidos'

    adicional = models.ForeignKey(AdicionalDeServico, blank=True, null=True, on_delete=models.CASCADE)
    item_servico = models.ForeignKey(ItemServico, blank=True, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


class ContratoDeServico(TimeStamped):
    class Meta:
        verbose_name = u'Contrato de Servico'
        verbose_name_plural = u'Contratos de Servicos'

    carrinho = models.OneToOneField(CarrinhoDeServicos, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CONTRATO, blank=True, null=True, default='ABERTO')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    profissional = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE)
    motivo = models.TextField(blank=True, null=True)
    is_avaliado = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


class ComentarioServico(TimeStamped):
    class Meta:
        verbose_name = u'Comentario'
        verbose_name_plural = u'Comentarios'

    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    avaliacao = models.IntegerField(blank=True, null=True, default=10, validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    status = models.BooleanField(default=True, )

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


CHOICES_CATEGORIA_MENSAGEM = [
    ('Ajuda ao Profissional', 'Ajuda ao Profissional'),
    ('Ajuda ao Cliente', 'Ajuda ao Cliente'),
    ('Problemas na compra', 'Problemas na compra'),
]


class Mensagem(TimeStamped):
    class Meta:
        verbose_name = u'Mensagem'
        verbose_name_plural = u'Mensagens'

    titulo = models.CharField(max_length=300, blank=True, null=True)
    categoria = models.CharField(choices=CHOICES_CATEGORIA_MENSAGEM, max_length=300, blank=True, null=True)
    mensagem = models.TextField(blank=True, null=True)
    nome = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.IntegerField(blank=True, null=True)
    resolvido = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


CHOICES_FLUXO_CAIXA = (
    ('DEBITO', 'DEBITO'),
    ('CREDITO', 'CREDITO'),
    ('BOLETO', 'BOLETO'),
    ('DINHEIRO', 'DINHEIRO'),
    ('CHEQUE', 'CHEQUE'),
    ('DEBITO', 'DEBITO')
)


class Entrada(TimeStamped):
    class Meta:
        verbose_name = u'Entrada'
        verbose_name_plural = u'Entradas'

    profissional = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE)
    valor = MoneyField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Money(0, 'BRL'))])
    descricao = models.CharField(max_length=300, blank=True, null=True)
    cliente = models.CharField(max_length=300, blank=True, null=True)
    telefone = models.IntegerField(blank=True, null=True)
    data = models.DateField()
    tipo_pagamento = models.CharField(max_length=300, blank=True, null=True,
                                      choices=CHOICES_FLUXO_CAIXA, verbose_name='Tipo de Pagamento')

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


class Saida(TimeStamped):
    class Meta:
        verbose_name = u'Saida'
        verbose_name_plural = u'Saidas'

    profissional = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE)
    valor = MoneyField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Money(0, 'BRL'))])
    descricao = models.CharField(max_length=300, blank=True, null=True)
    cliente = models.CharField(max_length=300, blank=True, null=True)
    telefone = models.IntegerField(blank=True, null=True)
    data = models.DateField()
    tipo_pagamento = models.CharField(max_length=300, blank=True, null=True,
                                      choices=CHOICES_FLUXO_CAIXA, verbose_name='Tipo de Pagamento')

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


class Interesse(TimeStamped):
    class Meta:
        verbose_name = u'Interesse'
        verbose_name_plural = u'Interesses'

    profissional_dono = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=300, blank=True, null=True)
    descricao = models.TextField(blank=True, )
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.titulo

    def __str__(self):
        return u'%s' % self.titulo


STATUS_PROPOSTA = (
    ('ACEITO', 'ACEITO'),
    ('REJEITADO', 'REJEITADO'),
    ('AGUARDANDO', 'AGUARDANDO')
)


class Proposta(TimeStamped):
    class Meta:
        verbose_name = u'Proposta'
        verbose_name_plural = u'Proposta'

    profissional_socio = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=300, blank=True, null=True)
    interesse = models.ForeignKey(Interesse, blank=True, null=True, on_delete=models.CASCADE)
    descricao = models.TextField(blank=True, )
    status = models.CharField(max_length=300, blank=True, null=True,
                              choices=STATUS_PROPOSTA, default='AGUARDANDO')

    def __unicode__(self):
        return u'%s' % self.titulo

    def __str__(self):
        return u'%s' % self.titulo


STATUS_PROCESSO = (
    ('AGUARDANDO PAGAMENTO', 'AGUARDANDO PAGAMENTO'),
    ('ABERTO', 'ABERTO'),
    ('EM ANDAMENTO', 'EM ANDAMENTO'),
    ('REJEITADO', 'REJEITADO'),
    ('REALIZADO', 'REALIZADO'),
)


class Processo(TimeStamped):
    class Meta:
        verbose_name = u'Processo'
        verbose_name_plural = u'Processo'

    profissional_socio = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE,
                                           related_name='profissional_socio')
    profissional_dono = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE,
                                          related_name='profissional_dono')
    titulo = models.CharField(max_length=300, blank=True, null=True)
    interesse = models.ForeignKey(Interesse, blank=True, null=True, on_delete=models.CASCADE)
    proposta = models.ForeignKey(Proposta, blank=True, null=True, on_delete=models.CASCADE)
    descricao = models.TextField(blank=True, )
    status = models.CharField(max_length=100, choices=STATUS_PROCESSO, blank=True, null=True, default='AGUARDANDO PAGAMENTO')
    motivo = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id


class GeneralMessage(TimeStamped):
    class Meta:
        verbose_name = u'Mensagem Geral do Sistema'
        verbose_name_plural = u'Mensagens Gerais do sistema'

    title = models.CharField(max_length=300, blank=True, null=True)
    message = models.TextField(blank=True, )
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.id

    def __str__(self):
        return u'%s' % self.id
