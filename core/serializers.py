from rest_framework import serializers
from .models import User






class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=User
		fields=('username', 'email', 'cpf', 'password')
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
