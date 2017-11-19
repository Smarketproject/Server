# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-18 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Aguardando Pagamento'), (1, 'Concluída'), (2, 'Cancelada')], default=0, verbose_name='Situação'),
        ),
    ]