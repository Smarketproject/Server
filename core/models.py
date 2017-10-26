import re  # Futuras Regex
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from helpers.cpf import validate_CPF
from helpers.barcode import GTIN


# Nao esqueçam do makemigrations e migrate após a criaçao da model, para criar uma tabela no banco

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Username', max_length=128, unique=True)
    email = models.EmailField('Email', unique=True, max_length=128, validators=[validators.EmailValidator])
    cpf = models.CharField('Cpf', max_length=11, unique=True, validators=[validate_CPF])
    func_smarket_active = models.BooleanField('Smarket', default=False)
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'cpf']
    objects = UserManager()

    def get_name(self):
        return str(self.username)

    def get_short_name(self):
        return str(self.username).split(" ")[0]


class Product(models.Model):
    name = models.CharField('Nome', max_length=128, unique=True)
    weight = models.FloatField('Peso', max_length=8),
    price = models.FloatField('Preco', max_length=8)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class Purchase(models.Model):
    id_user = models.ForeignKey('User')
    products = models.ManyToManyField(Product)

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

# Nice! It could be even better tho. See this: https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/
'''
class Purchase_Product(models.Model):
	id_purchase = models.ForeignKey('Purchase')
	id_product = models.ForeignKey('Product')
	price = models.FloatField('Preco', max_length=8)
'''
