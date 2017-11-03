from rest_framework import serializers
from .models import User
from .models import Product






class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=User
		fields=('username', 'email', 'cpf', 'password', 'id')
		extra_kwargs = {"password":
							{"write_only": True}
							}
	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		cpf = validated_data['cpf']
		password = validated_data['password']
		user_obj = User(
				username = username,
				email = email,
				cpf = cpf
			)
		user_obj.set_password(password)
		user_obj.save()


		return validated_data

class ProductSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Product
		fields=('nome', 'peso', 'preco')

	def create(self, validated_data):
		nome = validated_data['nome']
		peso = validated_data['peso']
		preco = validated_data['preco']
		user_obj = Product(
				nome = nome,
				peso = peso,
				preco = preco
			)
		user_obj.save()


		return validated_data

