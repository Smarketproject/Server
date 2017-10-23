from django.shortcuts import render
from .models import User
from .models import Product
from rest_framework import viewsets
from .serializers import UserSerializer
from .serializers import ProductSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class=UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class=ProductSerializer

