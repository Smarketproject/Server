from django.shortcuts import render
from .models import User, Purchase
from .models import Product
from rest_framework import viewsets, permissions, generics
from .serializers import UserSerializer
from .serializers import ProductSerializer
from djoser.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
import json
from django.http import JsonResponse
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.AllowAny]
	queryset = User.objects.all()
	serializer_class=UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class=ProductSerializer





class List(APIView):
	permission_classes = [permissions.IsAuthenticated]
	authentication_classes = (authentication.TokenAuthentication,)
	def get(self, request, format=None):
		us = self.request.user.id
		#entry.objects.filter(blog__name='Beatles Blog')
		#Blog.objects.filter(entry__headline__contains='Lennon')
		obj = Purchase.objects.filter(id_user = us).values('products__name', 'id_user', 'id')

		return Response(obj)

	