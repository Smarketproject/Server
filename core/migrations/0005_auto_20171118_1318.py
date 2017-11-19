# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-18 15:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_purchase_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cart', unique=True, verbose_name='Carrinho'),
        ),
    ]