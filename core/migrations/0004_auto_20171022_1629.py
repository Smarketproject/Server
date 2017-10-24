# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imagem',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='Server/images'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='preco',
            field=models.FloatField(max_length=8, verbose_name='Preco'),
        ),
    ]
