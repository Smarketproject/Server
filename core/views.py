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



class Show_purchases(APIView):
	permission_classes = [permissions.IsAuthenticated]
	authentication_classes = (authentication.TokenAuthentication,)
	def get(self, request, format=None):
		us = self.request.user.id
		#entry.objects.filter(blog__name='Beatles Blog')
		#Blog.objects.filter(entry__headline__contains='Lennon')
		obj = Purchase.objects.filter(id_user = us).values('products__name', 'id_user', 'id', 'created_at')

		return Response(obj)


class Show_products(APIView):
	def get(self, request):
		objs = Product.objects.all()
		return Response(objs.values())


class Get_products(APIView):

	def post(self, request):
		
		
		obj = request.data
		bar_code = obj.get('bar_code')
		

		produto = Product.objects.filter(bar_code = bar_code).values()
		
		
		return Response(produto)

class Show_carts(APIView):
	def get(self, request):
		carts = Cart.objects.filter(finalized=True)
		return Response(carts.values())



