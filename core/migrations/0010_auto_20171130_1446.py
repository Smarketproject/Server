# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 16:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_cart_hashed_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cart', verbose_name='Carrinho')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='func_smarket_active',
            field=models.BooleanField(default=True, verbose_name='Smarket'),
        ),
    ]