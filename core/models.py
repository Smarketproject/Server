from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from helpers.cpf import validate_CPF
from helpers.barcode import validate_ean

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
    bar_code = models.CharField('Cod_barras', max_length=13, validators=[validate_ean])
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Produto'

class Purchase(models.Model):
    id_user = models.ForeignKey('Cart', verbose_name='Carrinho')
    id_validator = models.ForeignKey('Validator', verbose_name='Validação')
    value = models.FloatField('Valor', max_length=8)
    transaction_code = models.CharField('Código de Transação', max_length=13)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Compra'

class Item(models.Model):
    id_product = models.ForeignKey('Product', verbose_name='Produto')
    id_cart = models.ForeignKey('Cart', verbose_name='Carrinho')
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Itens'

    def __str__(self):
        return "{} unidade(s) de {}".format(self.quantity, self.id_product.name)

class Cart(models.Model):
    id_user = models.ForeignKey('User', verbose_name='Usuário')
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    finalized = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Carrinho'

    def __str__(self):
        return "{} - {}".format(self.id_user.username, self.pk)

class QRCode(models.Model):
    id_cart = models.ForeignKey('Cart', verbose_name='Carrinho')
    token = models.CharField('Token', max_length=13)
    image = models.ImageField(upload_to='images', editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)

class Validator(models.Model):
    id_cart = models.ForeignKey('Cart', verbose_name='Carrinho')
    ok = models.BooleanField(default=False)
    report = models.CharField('Relatório', max_length=13)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    class Meta:
        verbose_name = 'Validação'
        verbose_name_plural = 'Validações'