import re #Futuras Regex
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from helpers.cpf import validate_CPF
from helpers.barcode import GTIN
# Create your models here.

#class Cachorro(models.Model):
#	nome(atributo que irá ser salvo como coluna no banco de dados) = models.CharField(tipo de informaçao que o campo irá ocupar ex:letras, numeros, booleanos)('Nome', max_length=128(limitadores e validadores))
#	cor = models.CharField('Cor', max_length=128)




#Nao esqueçam do makemigrations e migrate após a criaçao da model, para criar uma tabela no banco



class Cachorro(models.Model):
	nome = models.CharField('Nome', max_length=128)
	cor = models.CharField('Cor', max_length=128)




class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField('Username', max_length=128, unique=True)
	email = models.EmailField('Email',unique=True, max_length=128, validators=[validators.EmailValidator])
	cpf = models.CharField('Cpf', max_length=11, unique=True, validators=[validate_CPF])
	#password = models.CharField('Senha', max_length=16)
	func_smarket_active = models.BooleanField('Smarket', default=False)
	is_staff = models.BooleanField('Equipe', default=False)
	is_active = models.BooleanField('Ativo', default=True)
	date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)
	#created = models.DateTimeField('Criado em', auto_now_add=True)
	#modified = models.DateTimeField('Modificado em', auto_now=True)

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
	nome = models.CharField('Nome', max_length=128, unique=True)
	peso = models.FloatField('Peso', max_length=128),
	preco = models.FloatField('Preco', max_length=8)
	imagem = models.ImageField(upload_to= 'Server/Imagem')
	barcode = models.IntegerField('Barcode', unique=True, validators=[GTIN])
#	is_staff = models.BooleanField('Equipe', default=True)
#	is_active = models.BooleanField('Ativo', default=True)
#	date_created = models.DateTimeField('Data de criacao', auto_now_add=True)
