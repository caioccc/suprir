# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-22 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_mensagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensagem',
            name='categoria',
            field=models.CharField(blank=True, choices=[('Ajuda ao Profissional', 'Ajuda ao Profissional'), ('Ajuda ao Cliente', 'Ajuda ao Cliente'), ('Problemas na compra', 'Problemas na compra')], max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='mensagem',
            name='resolvido',
            field=models.BooleanField(default=False),
        ),
    ]
