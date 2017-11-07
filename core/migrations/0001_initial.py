# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 16:26
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import helpers.barcode
import helpers.cpf


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=128, unique=True, verbose_name='Username')),
                ('email', models.EmailField(max_length=128, unique=True, validators=[django.core.validators.EmailValidator], verbose_name='Email')),
                ('cpf', models.CharField(max_length=11, unique=True, validators=[helpers.cpf.validate_CPF], verbose_name='Cpf')),
                ('func_smarket_active', models.BooleanField(default=False, verbose_name='Smarket')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Equipe')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Data de entrada')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('finalized', models.BooleanField(default=False)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Carrinho',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('id_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cart', verbose_name='Carrinho')),
            ],
            options={
                'verbose_name_plural': 'Itens',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Nome')),
                ('price', models.FloatField(max_length=8, verbose_name='Preco')),
                ('image', models.ImageField(upload_to='images')),
                ('bar_code', models.CharField(max_length=13, validators=[helpers.barcode.validate_ean], verbose_name='Cod_barras')),
            ],
            options={
                'verbose_name': 'Produto',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(max_length=8, verbose_name='Valor')),
                ('transaction_code', models.CharField(max_length=13, verbose_name='Código de Transação')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cart', verbose_name='Carrinho')),
            ],
            options={
                'verbose_name': 'Compra',
            },
        ),
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=13, verbose_name='Token')),
                ('image', models.ImageField(editable=False, upload_to='images')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('id_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cart', verbose_name='Carrinho')),
            ],
        ),
        migrations.CreateModel(
            name='Validator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ok', models.BooleanField(default=False)),
                ('report', models.CharField(max_length=13, verbose_name='Relatório')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('id_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cart', verbose_name='Carrinho')),
            ],
            options={
                'verbose_name_plural': 'Validações',
                'verbose_name': 'Validação',
            },
        ),
        migrations.AddField(
            model_name='purchase',
            name='id_validator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Validator', verbose_name='Validação'),
        ),
        migrations.AddField(
            model_name='item',
            name='id_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Product', verbose_name='Produto'),
        ),
    ]
