from django.shortcuts import render, get_object_or_404, redirect 
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.views.generic import (
    RedirectView, TemplateView, ListView, DetailView, View
)
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings as Dsettings
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Purchase, Cart, Item, Product, Validator
from .serializers import UserSerializer
from .serializers import ProductSerializer

from rest_framework import viewsets, permissions, generics, status
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from hashid_field import HashidField
import hashlib, uuid

import json

import logging

from djoser.conf import settings

from pagseguro import PagSeguro

import pyqrcode

import png

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile 
from django.core.files import File
logger = logging.getLogger(__name__)
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
		cart = Cart.objects.filter(id_user = us).values('id')
		hist = []
		

		for item in cart:
			
			cart_id = item.get('id')
			total = Cart.objects.get(pk=cart_id).total()
			finalized = Cart.objects.get(pk=cart_id).finalized
			itens = Item.objects.filter(id_cart= cart_id)
			purchase_id = Purchase.objects.filter(id_cart=cart_id).values('id')
			purchase = Purchase.objects.get(id_cart=cart_id)
			prod = []
			cart = {
				'cart_id': cart_id,
				'Products': prod,
				'Total': total,
				'Finalizado': finalized,
				'purchase_id': purchase_id[0].get('id'),  
				'created_at': purchase.created_at
			}

			for item in itens:
				obj = Product.objects.filter(id=item.id_product_id).values()
				price = obj[0].get('price')
				name = obj[0].get('name')
				bar_code = obj[0].get('bar_code')
				
				#prod.append(
                #	{
                #    	'id': item.id_product_id,
                #    	'name': str(name),
                #    	'quantity': item.quantity,
                #    	'price': '%.2f' % price,
                #    	'bar_code': bar_code
                #	})
			
			hist.append(cart)
		
		return Response(hist)

class Show_cart(APIView):
	def get(self, request, *args, **kwargs):
		pk = self.kwargs.get('pk')
		itens = Item.objects.filter(id_cart= pk)
		
		prod = []
		for item in itens:
				obj = Product.objects.filter(id=item.id_product_id).values()
				price = obj[0].get('price')
				name = obj[0].get('name')
				bar_code = obj[0].get('bar_code')
				
				prod.append(
                	{
                    	'id': item.id_product_id,
                    	'name': str(name),
                    	'quantity': item.quantity,
                    	'price': '%.2f' % price,
                    	'bar_code': bar_code
                	})
		return Response(prod)


class Show_products(APIView):
	
	def get(self, request):
		objs = Product.objects.all()
		return Response(objs.values())


class Peso(APIView):

	def post(self, request):
		peso = request.data.get('weight')
		if peso == None:
			return Response(' "weight" is required. ')



		return Response(peso)





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



class Update_password(APIView):
	
	def post(self, request):
		if check_password(self.request.data.get('password'), self.request.user.password) == True:
			User_object = self.request.user
			User_object.set_password(self.request.data.get('new_password'))
			User_object.save()
			return Response("Senha Alterada com Sucesso")
		else: return Response('Senha Invalida', status=status.HTTP_401_UNAUTHORIZED)



class pagamento(APIView):
	
	def get(self, request, *args, **kwargs):
		
		
		try:
			purchase = Purchase.objects.get(pk=self.kwargs.get('pk'))
		except ObjectDoesNotExist:
			return Response('Esse id nao existe.')
		
		pg = PagSeguro(
            email=Dsettings.PAGSEGURO_EMAIL, 
            token=Dsettings.PAGSEGURO_TOKEN,
            config={'sandbox': Dsettings.PAGSEGURO_SANDBOX}
            )
		pg.reference_prefix = None
		pg.shipping = None

		
		user_id = self.request.user.id
		email = self.request.user.email
		pg.sender = {'email': email}
		pk = self.kwargs.get('pk')
		pg.reference = pk
		
		cart_id = Purchase.objects.filter(id=pk).values('id_cart_id')[0].get('id_cart_id')
		
		itens = Item.objects.filter(id_cart= cart_id)
		
		for item in itens:
			obj = Product.objects.filter(id=item.id_product_id).values('price')
			price = obj[0].get('price')
			obj2 = Product.objects.filter(id=item.id_product_id).values('name')
			name = obj2[0].get('name')
			pg.items.append(
                {
                    'id': item.id_product_id,
                    'description': str(name),
                    'quantity': item.quantity,
                    'amount': '%.2f' % price
                })
		response = pg.checkout()
		
		if Purchase.objects.filter(id=pk).values('payment_link')[0].get('payment_link') == '-':
			
			p = Purchase.objects.get(id=pk)
			p.payment_link = response.payment_url
			p.save()
		else:
			return Response(Purchase.objects.filter(id=pk).values('payment_link')[0].get('payment_link'))
		return Response(response.payment_url)



class CloseCart(APIView):
	permission_classes = [permissions.IsAuthenticated]
	authentication_classes = (authentication.TokenAuthentication,)

	def post(self, request):
		user_id = self.request.user.id
		obj = self.request.data.get('products')
		
		if obj == None:
			return Response(' "products" is required. ')

		for item in obj:
			
			if item.get('bar_code') == None:
				return Response(' "bar_code" is required. ')

			try:
				product = Product.objects.get(bar_code=item.get('bar_code'))
			except ObjectDoesNotExist:
				return Response('O código de barras ( %s ) não está cadastrado.' %(item.get('bar_code')))

			if item.get('quantity') == None:
				return Response(' "quantity" is required.')

		b = Cart(id_user=self.request.user)
		b.save()
		
		for item in obj:
			product = Product.objects.get(bar_code=item.get('bar_code'))
			quantity = item.get('quantity')
			iten = Item(id_product=product, id_cart=b, quantity=quantity).save()
		purchase = Purchase(id_cart=b, id_validator=Validator.objects.get(pk=1), value=b.total(), transaction_code='-')
		purchase.save()


		#i = purchase.id 
		#hashed_id = HashidField(i)
		#hashed_id.save()

		i = purchase.id
		salt = uuid.uuid4().hex
		hash_ =  hashlib.sha512()
		hash_.update(('i'+salt).encode('utf-8')) 
		hashed_id =  hash_.hexdigest()
		a = hashed_id[0:13]
		
		b.hashed_id = a
		b.save()		
		p_id = {
			"purchase_id": purchase.id,
			"status": "Compra Finalizada"
		}
		
		return Response(p_id)



#class Teste(APIView):
#	pass
#	def get(self, request):
#		pass
#		a = pyqrcode.create(12355555555555555)
#		b = a.png("teste.png")
#		ImageFile(a.png("teste.png")).save()
#		default_storage.save('/home/arthur/smarket/Server/images/', ImageFile(a.png("teste.png")))
#		return Response(a.png("teste.png"))

#		#QUANDO O QR CODE É GERADO?
#		user1=User(name='abc')
#		user1.pic.save('abc.png', File(open('/tmp/pic.png', 'r')))


class ReadQR(APIView):
	def post(self, request):
		request.data.get()


 	  	









@csrf_exempt
def pagseguro_notification(request):
    notification_code = request.POST.get('notificationCode', None)
    if notification_code:
        pg = PagSeguro(
            email=Dsettings.PAGSEGURO_EMAIL, token=Dsettings.PAGSEGURO_TOKEN,
            config={'sandbox': Dsettings.PAGSEGURO_SANDBOX}
        )
        notification_data = pg.check_notification(notification_code)
        status = notification_data.status
        reference = notification_data.reference
        try:
            purchase = Purchase.objects.get(pk=reference)
        except ObjectDoesNotExist:
            return ("nao existe")
        else:
            purchase.update_status(status)
    return HttpResponse('OK')






