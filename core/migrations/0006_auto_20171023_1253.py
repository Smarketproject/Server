# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_product_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='imagem',
            field=models.ImageField(upload_to='Imagem'),
        ),
    ]
