# coding=utf-8
from __future__ import unicode_literals

from base64 import b64encode

import pyimgur
from django.contrib.auth.models import User
from django.db import models


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

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    telefone_1 = models.CharField(max_length=30, blank=True, null=True)
    whatsapp = models.CharField(max_length=30, blank=True, null=True)
    photo = models.URLField(blank=True, null=True)
    cpf = models.CharField(max_length=100, blank=True, null=True, default="")
    cnpj = models.CharField(max_length=100, blank=True, null=True, default="")
    is_online = models.BooleanField(default=False)
    file = models.FileField(blank=True, null=True)

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
        return self.user.first_name

    def __unicode__(self):
        return u'%s' % self.user.first_name


class Cliente(CommonUserData):
    class Meta:
        verbose_name = u'Cliente'
        verbose_name_plural = u'Clientes'


class CategoriaDeProfissional(TimeStamped):
    class Meta:
        verbose_name = u'Categoria de Profissional'
        verbose_name_plural = u'Categorias de Profissional'

    categoria = models.CharField(max_length=300, blank=True, null=True)

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
    valor_base = models.CharField(max_length=300, blank=True, null=True)
    profissional = models.ForeignKey(Profissional, blank=True, null=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.titulo

    def __unicode__(self):
        return "%s" % self.titulo

    def save(self, *args, **kwargs):
        self.valor_base = float(str(self.valor_base).replace(',', '.'))
        super(Servico, self).save(*args, **kwargs)


class AdicionalDeServico(TimeStamped):
    class Meta:
        verbose_name = u'Adicional de Servico'
        verbose_name_plural = u'Adicionais de Servicos'

    titulo = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.CharField(max_length=300, blank=True, null=True)
    servico = models.ForeignKey(Servico, blank=True, null=True, on_delete=models.CASCADE)
    valor = models.CharField(max_length=10)
    disponivel = models.BooleanField(default=True)

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
    url = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)

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


STATUS = (
    ('EM ANDAMENTO', 'EM ANDAMENTO'),
    ('REJEITADO', 'REJEITADO'),
    ('REALIZADO', 'REALIZADO'),
)


class CarrinhoDeServicos(TimeStamped, BaseAddress):
    class Meta:
        verbose_name = u'Carrinho de Servico'
        verbose_name_plural = u'Carrinhos de Servicos'

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    profissional = models.ForeignKey(Profissional, blank=True, null=True, on_delete=models.CASCADE)
    subtotal = models.CharField(max_length=10, blank=True, null=True)
    valor_total = models.TextField(blank=True, null=True)
    forma_pagamento = models.ForeignKey(FormaPagamento, blank=True, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s - %s - %s - %s' % (self.id, self.cliente, self.profissional, self.valor_total)

    def __str__(self):
        return u'%s - %s - %s - %s' % (self.id, self.cliente, self.profissional, self.valor_total)

    def save(self, *args, **kwargs):
        subtotal = 0.0
        for item in self.itemservico_set.all():
            subtotal = float(subtotal) + float(str(item.valor_total).replace(',', '.'))
        self.subtotal = float(format(subtotal, '.2f'))
        self.valor_total = format(subtotal, '.2f')
        super(CarrinhoDeServicos, self).save(*args, **kwargs)


class ItemServico(TimeStamped):
    class Meta:
        verbose_name = u'Item Servico'
        verbose_name_plural = u'Itens Servicos'

    carrinho = models.ForeignKey(CarrinhoDeServicos, blank=True, null=True, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, blank=True, null=True, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)
    valor_total = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        valor_base = float(str(self.servico.valor_base).replace(',', '.').replace(" ", ""))
        valor_opcionais = 0.0
        if self.adicionalescolhido_set.first():
            for opc in self.adicionalescolhido_set.all():
                valor_opcionais = float(valor_opcionais) + float(
                    str(opc.adicional.valor).replace(',', '.').replace(" ", ""))
        valor_unitario = float(valor_base) + float(valor_opcionais)
        self.valor_total = format(float(valor_unitario), '.2f')
        super(ItemServico, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s - %s' % (self.carrinho.id, self.servico)

    def __str__(self):
        return u'%s - %s' % (self.carrinho.id, self.servico)


class AdicionalEscolhido(TimeStamped):
    class Meta:
        verbose_name = u'Adicional Escolhido'
        verbose_name_plural = u'Adicionais Escolhidos'

    adicional = models.ForeignKey(AdicionalDeServico, blank=True, null=True, on_delete=models.CASCADE)
    item_servico = models.ForeignKey(ItemServico, blank=True, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.adicional

    def __str__(self):
        return u'%s' % self.adicional


class ContratoDeServico(TimeStamped):
    class Meta:
        verbose_name = u'Contrato de Servico'
        verbose_name_plural = u'Contratos de Servicos'

    carrinho = models.OneToOneField(CarrinhoDeServicos, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, blank=True, null=True, default='EM ANDAMENTO')

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.carrinho)

    def __str__(self):
        return u'%s - %s' % (self.id, self.carrinho)


class ComentarioServico(TimeStamped):
    class Meta:
        verbose_name = u'Comentario'
        verbose_name_plural = u'Comentarios'

    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'Servico:%s Cliente:%s' % (self.servico, self.cliente)

    def __str__(self):
        return u'Servico:%s Cliente:%s' % (self.servico, self.cliente)