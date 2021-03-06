# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-06-09 23:34
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import djmoney.money


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdicionalDeServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(blank=True, max_length=100, null=True)),
                ('descricao', models.CharField(blank=True, max_length=300, null=True)),
                ('valor_currency', djmoney.models.fields.CurrencyField(choices=[(b'BRL', 'Brazilian Real')], default='XYZ', editable=False, max_length=3)),
                ('valor', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), max_digits=14, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0, 'BRL'))])),
                ('disponivel', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Adicional de Servico',
                'verbose_name_plural': 'Adicionais de Servicos',
            },
        ),
        migrations.CreateModel(
            name='AdicionalEscolhido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('adicional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.AdicionalDeServico')),
            ],
            options={
                'verbose_name': 'Adicional Escolhido',
                'verbose_name_plural': 'Adicionais Escolhidos',
            },
        ),
        migrations.CreateModel(
            name='CarrinhoDeServicos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('cep', models.CharField(blank=True, max_length=200, null=True, verbose_name='CEP')),
                ('bairro', models.CharField(blank=True, max_length=200, null=True, verbose_name='Bairro')),
                ('endereco', models.CharField(blank=True, max_length=300, null=True, verbose_name='Endere\xe7o')),
                ('numero', models.CharField(blank=True, max_length=5, null=True, verbose_name='N\xfamero')),
                ('cidade', models.CharField(blank=True, max_length=200, null=True, verbose_name='Cidade')),
                ('estado', models.CharField(blank=True, max_length=200, null=True, verbose_name='Estado')),
                ('complemento', models.CharField(blank=True, max_length=300, null=True, verbose_name='Ponto de Refer\xeancia')),
                ('lat', models.CharField(blank=True, max_length=300, null=True)),
                ('lng', models.CharField(blank=True, max_length=300, null=True)),
                ('subtotal_currency', djmoney.models.fields.CurrencyField(choices=[(b'BRL', 'Brazilian Real')], default='XYZ', editable=False, max_length=3)),
                ('subtotal', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), max_digits=14, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0, 'BRL'))])),
                ('valor_total_currency', djmoney.models.fields.CurrencyField(choices=[(b'BRL', 'Brazilian Real')], default='XYZ', editable=False, max_length=3)),
                ('valor_total', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), max_digits=14, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0, 'BRL'))])),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Carrinho de Servico',
                'verbose_name_plural': 'Carrinhos de Servicos',
            },
        ),
        migrations.CreateModel(
            name='CategoriaDeProfissional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('categoria', models.CharField(blank=True, max_length=300, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Categoria de Profissional',
                'verbose_name_plural': 'Categorias de Profissional',
            },
        ),
        migrations.CreateModel(
            name='CategoriaDeServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('categoria', models.CharField(blank=True, max_length=300, null=True)),
                ('disponivel', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Categoria de Servico',
                'verbose_name_plural': 'Categorias de Servico',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('cep', models.CharField(blank=True, max_length=200, null=True, verbose_name='CEP')),
                ('bairro', models.CharField(blank=True, max_length=200, null=True, verbose_name='Bairro')),
                ('endereco', models.CharField(blank=True, max_length=300, null=True, verbose_name='Endere\xe7o')),
                ('numero', models.CharField(blank=True, max_length=5, null=True, verbose_name='N\xfamero')),
                ('cidade', models.CharField(blank=True, max_length=200, null=True, verbose_name='Cidade')),
                ('estado', models.CharField(blank=True, max_length=200, null=True, verbose_name='Estado')),
                ('complemento', models.CharField(blank=True, max_length=300, null=True, verbose_name='Ponto de Refer\xeancia')),
                ('lat', models.CharField(blank=True, max_length=300, null=True)),
                ('lng', models.CharField(blank=True, max_length=300, null=True)),
                ('telefone_1', models.CharField(blank=True, max_length=30, null=True)),
                ('whatsapp', models.CharField(blank=True, max_length=30, null=True)),
                ('photo', models.URLField(blank=True, default='https://placehold.it/300x300', null=True)),
                ('cpf', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('cnpj', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to=b'')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='ComentarioServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('avaliacao', models.IntegerField(blank=True, default=10, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('status', models.BooleanField(default=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Cliente')),
            ],
            options={
                'verbose_name': 'Comentario',
                'verbose_name_plural': 'Comentarios',
            },
        ),
        migrations.CreateModel(
            name='ContratoDeServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('ABERTO', 'ABERTO'), ('EM ANDAMENTO', 'EM ANDAMENTO'), ('REJEITADO', 'REJEITADO'), ('REALIZADO', 'REALIZADO')], default='ABERTO', max_length=100, null=True)),
                ('motivo', models.TextField(blank=True, null=True)),
                ('is_avaliado', models.BooleanField(default=False)),
                ('carrinho', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.CarrinhoDeServicos')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Cliente')),
            ],
            options={
                'verbose_name': 'Contrato de Servico',
                'verbose_name_plural': 'Contratos de Servicos',
            },
        ),
        migrations.CreateModel(
            name='Cupom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('codigo', models.CharField(max_length=300)),
                ('valor_de_desconto_currency', djmoney.models.fields.CurrencyField(choices=[(b'BRL', 'Brazilian Real')], default='XYZ', editable=False, max_length=3)),
                ('valor_de_desconto', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), max_digits=14, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0, 'BRL'))])),
                ('is_approved', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Cupom',
                'verbose_name_plural': 'Cupons',
            },
        ),
        migrations.CreateModel(
            name='EmailOuTelegramaAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('title', models.CharField(max_length=200)),
                ('enviado', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('valor_currency', djmoney.models.fields.CurrencyField(choices=[(b'BRL', 'Brazilian Real')], default='XYZ', editable=False, max_length=3)),
                ('valor', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), max_digits=14, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0, 'BRL'))])),
                ('descricao', models.CharField(blank=True, max_length=300, null=True)),
                ('cliente', models.CharField(blank=True, max_length=300, null=True)),
                ('telefone', models.IntegerField(blank=True, null=True)),
                ('data', models.DateField()),
                ('tipo_pagamento', models.CharField(blank=True, choices=[('DEBITO', 'DEBITO'), ('CREDITO', 'CREDITO'), ('BOLETO', 'BOLETO'), ('DINHEIRO', 'DINHEIRO'), ('CHEQUE', 'CHEQUE'), ('DEBITO', 'DEBITO')], max_length=300, null=True, verbose_name='Tipo de Pagamento')),
            ],
            options={
                'verbose_name': 'Entrada',
                'verbose_name_plural': 'Entradas',
            },
        ),
        migrations.CreateModel(
            name='FormaPagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('forma', models.CharField(blank=True, default='DINHEIRO', max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Forma de Pagamento',
                'verbose_name_plural': 'Formas de Pagamento',
            },
        ),
        migrations.CreateModel(
            name='FotoServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(blank=True, default='https://placehold.it/300x300', null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=b'')),
                ('is_approved', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Foto de Servico',
                'verbose_name_plural': 'Fotos de Servicos',
            },
        ),
        migrations.CreateModel(
            name='GeneralMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('message', models.TextField(blank=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Mensagem Geral do Sistema',
                'verbose_name_plural': 'Mensagens Gerais do sistema',
            },
        ),
        migrations.CreateModel(
            name='Interesse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(blank=True, max_length=300, null=True)),
                ('descricao', models.TextField(blank=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Interesse',
                'verbose_name_plural': 'Interesses',
            },
        ),
        migrations.CreateModel(
            name='ItemCupom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('cupom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Cupom')),
            ],
            options={
                'verbose_name': 'Item de Cupom',
                'verbose_name_plural': 'Itens de Cupom',
            },
        ),
        migrations.CreateModel(
            name='ItemServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('valor_total_currency', djmoney.models.fields.CurrencyField(choices=[(b'BRL', 'Brazilian Real')], default='XYZ', editable=False, max_length=3)),
                ('valor_total', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), max_digits=14, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0, 'BRL'))])),
                ('carrinho', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.CarrinhoDeServicos')),
            ],
            options={
                'verbose_name': 'Item Servico',
                'verbose_name_plural': 'Itens Servicos',
            },
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(blank=True, max_length=300, null=True)),
                ('categoria', models.CharField(blank=True, choices=[('Ajuda ao Profissional', 'Ajuda ao Profissional'), ('Ajuda ao Cliente', 'Ajuda ao Cliente'), ('Problemas na compra', 'Problemas na compra')], max_length=300, null=True)),
                ('mensagem', models.TextField(blank=True, null=True)),
                ('nome', models.CharField(blank=True, max_length=300, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefone', models.IntegerField(blank=True, null=True)),
                ('resolvido', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Mensagem',
                'verbose_name_plural': 'Mensagens',
            },
        ),
        migrations.CreateModel(
            name='Processo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(blank=True, max_length=300, null=True)),
                ('descricao', models.TextField(blank=True)),
                ('status', models.CharField(blank=True, choices=[('AGUARDANDO PAGAMENTO', 'AGUARDANDO PAGAMENTO'), ('ABERTO', 'ABERTO'), ('EM ANDAMENTO', 'EM ANDAMENTO'), ('REJEITADO', 'REJEITADO'), ('REALIZADO', 'REALIZADO')], default='AGUARDANDO PAGAMENTO', max_length=100, null=True)),
                ('motivo', models.TextField(blank=True, null=True)),
                ('interesse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Interesse')),
            ],
            options={
                'verbose_name': 'Processo',
                'verbose_name_plural': 'Processo',
            },
        ),
        migrations.CreateModel(
            name='Profissional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('cep', models.CharField(blank=True, max_length=200, null=True, verbose_name='CEP')),
                ('bairro', models.CharField(blank=True, max_length=200, null=True, verbose_name='Bairro')),
                ('endereco', models.CharField(blank=True, max_length=300, null=True, verbose_name='Endere\xe7o')),
                ('numero', models.CharField(blank=True, max_length=5, null=True, verbose_name='N\xfamero')),
                ('cidade', models.CharField(blank=True, max_length=200, null=True, verbose_name='Cidade')),
                ('estado', models.CharField(blank=True, max_length=200, null=True, verbose_name='Estado')),
                ('complemento', models.CharField(blank=True, max_length=300, null=True, verbose_name='Ponto de Refer\xeancia')),
                ('lat', models.CharField(blank=True, max_length=300, null=True)),
                ('lng', models.CharField(blank=True, max_length=300, null=True)),
                ('telefone_1', models.CharField(blank=True, max_length=30, null=True)),
                ('whatsapp', models.CharField(blank=True, max_length=30, null=True)),
                ('photo', models.URLField(blank=True, default='https://placehold.it/300x300', null=True)),
                ('cpf', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('cnpj', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to=b'')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefone_2', models.CharField(blank=True, max_length=30, null=True)),
                ('link_facebook', models.URLField(blank=True, null=True)),
                ('link_instagram', models.URLField(blank=True, null=True)),
                ('url_site', models.URLField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('receber_pelo_sistema', models.BooleanField(default=False)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.CategoriaDeProfissional')),
            ],
            options={
                'verbose_name': 'Profissional',
                'verbose_name_plural': 'Profissionais',
            },
        ),
        migrations.CreateModel(
            name='Proposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(blank=True, max_length=300, null=True)),
                ('descricao', models.TextField(blank=True)),
                ('status', models.CharField(blank=True, choices=[('ACEITO', 'ACEITO'), ('REJEITADO', 'REJEITADO'), ('AGUARDANDO', 'AGUARDANDO')], default='AGUARDANDO', max_length=300, null=True)),
                ('interesse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Interesse')),
                ('profissional_socio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Profissional')),
            ],
            options={
                'verbose_name': 'Proposta',
                'verbose_name_plural': 'Proposta',
            },
        ),
        migrations.CreateModel(
            name='RecycleTelegramItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, max_length=300, null=True)),
                ('chat_id', models.CharField(blank=True, max_length=300, null=True)),
                ('last_name', models.CharField(blank=True, max_length=300, null=True)),
                ('username', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name': 'Telegram Bot Reciclavel',
                'verbose_name_plural': 'Bots Reciclaveis',
            },
        ),
        migrations.CreateModel(
            name='Saida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('valor_currency', djmoney.models.fields.CurrencyField(choices=[(b'BRL', 'Brazilian Real')], default='XYZ', editable=False, max_length=3)),
                ('valor', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), max_digits=14, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0, 'BRL'))])),
                ('descricao', models.CharField(blank=True, max_length=300, null=True)),
                ('cliente', models.CharField(blank=True, max_length=300, null=True)),
                ('telefone', models.IntegerField(blank=True, null=True)),
                ('data', models.DateField()),
                ('tipo_pagamento', models.CharField(blank=True, choices=[('DEBITO', 'DEBITO'), ('CREDITO', 'CREDITO'), ('BOLETO', 'BOLETO'), ('DINHEIRO', 'DINHEIRO'), ('CHEQUE', 'CHEQUE'), ('DEBITO', 'DEBITO')], max_length=300, null=True, verbose_name='Tipo de Pagamento')),
                ('profissional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Profissional')),
            ],
            options={
                'verbose_name': 'Saida',
                'verbose_name_plural': 'Saidas',
            },
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(blank=True, max_length=300, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('disponivel', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=True)),
                ('valor_a_combinar', models.BooleanField(default=False)),
                ('valor_base_currency', djmoney.models.fields.CurrencyField(choices=[(b'BRL', 'Brazilian Real')], default='XYZ', editable=False, max_length=3)),
                ('valor_base', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), max_digits=14, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0, 'BRL'))])),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.CategoriaDeServico')),
                ('profissional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Profissional')),
            ],
            options={
                'verbose_name': 'Servico',
                'verbose_name_plural': 'Servicos',
            },
        ),
        migrations.CreateModel(
            name='TelegramBot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, max_length=300, null=True)),
                ('chat_id', models.CharField(blank=True, max_length=300, null=True)),
                ('last_name', models.CharField(blank=True, max_length=300, null=True)),
                ('username', models.CharField(blank=True, max_length=300, null=True)),
                ('is_approved', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Telegram Bot',
                'verbose_name_plural': 'Telegram Bots',
            },
        ),
        migrations.AddField(
            model_name='profissional',
            name='telegram_bot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TelegramBot'),
        ),
        migrations.AddField(
            model_name='profissional',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='processo',
            name='profissional_dono',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profissional_dono', to='app.Profissional'),
        ),
        migrations.AddField(
            model_name='processo',
            name='profissional_socio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profissional_socio', to='app.Profissional'),
        ),
        migrations.AddField(
            model_name='processo',
            name='proposta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Proposta'),
        ),
        migrations.AddField(
            model_name='itemservico',
            name='servico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Servico'),
        ),
        migrations.AddField(
            model_name='interesse',
            name='profissional_dono',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Profissional'),
        ),
        migrations.AddField(
            model_name='fotoservico',
            name='servico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Servico'),
        ),
        migrations.AddField(
            model_name='entrada',
            name='profissional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Profissional'),
        ),
        migrations.AddField(
            model_name='cupom',
            name='profissional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Profissional'),
        ),
        migrations.AddField(
            model_name='contratodeservico',
            name='profissional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Profissional'),
        ),
        migrations.AddField(
            model_name='comentarioservico',
            name='servico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Servico'),
        ),
        migrations.AddField(
            model_name='categoriadeservico',
            name='profissional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Profissional'),
        ),
        migrations.AddField(
            model_name='carrinhodeservicos',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Cliente'),
        ),
        migrations.AddField(
            model_name='carrinhodeservicos',
            name='cupom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ItemCupom'),
        ),
        migrations.AddField(
            model_name='carrinhodeservicos',
            name='forma_pagamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.FormaPagamento'),
        ),
        migrations.AddField(
            model_name='carrinhodeservicos',
            name='profissional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Profissional'),
        ),
        migrations.AddField(
            model_name='adicionalescolhido',
            name='item_servico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ItemServico'),
        ),
        migrations.AddField(
            model_name='adicionaldeservico',
            name='servico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Servico'),
        ),
    ]
