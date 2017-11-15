from django.shortcuts import render, get_object_or_404, redirect 
from .models import User, Purchase, Cart, Order
from .models import Product
from rest_framework import viewsets, permissions, generics, status
from .serializers import UserSerializer
from .serializers import ProductSerializer
from djoser.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.views.generic import (
    RedirectView, TemplateView, ListView, DetailView, View
)

import logging
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

# Get an instance of a logger
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


class Update_password(APIView):
	
	def post(self, request):
		if check_password(self.request.data.get('password'), self.request.user.password) == True:
			User_object = self.request.user
			User_object.set_password(self.request.data.get('new_password'))
			User_object.save()
			return Response("Senha Alterada com Sucesso")
		else: return Response('Senha Invalida', status=status.HTTP_401_UNAUTHORIZED)

class RecuperarSenha(APIView):

	def post(self, request):
		email = self.request.data.get('email')
		carinha = User.objects.filter(email = email).values()

		return Response(carinha)

class Pagseguro(RedirectView):
	
	permission_classes = [permissions.IsAuthenticated]
	authentication_classes = (authentication.TokenAuthentication,)
	
	def get_redirect_url(self, *args, **kwargs):
		order_pk = self.kwargs.get('pk')
		
		print (order_pk)
		logger.error(self.request.user.id)
		
		order = get_object_or_404(
			Purchase.objects.filter(id=order_pk))
		
		print(order)
		
		email = self.request.user.email
		us = 4
		pg = order.pagseguro(email, us)
		
		response = pg.checkout()
		
		return response.payment_url

class CheckoutView( TemplateView):

   

    def get(self, request, *args, **kwargs):
        
        order = Order.objects.create_order(
                user=self.request.user
            )
        response = super(CheckoutView, self).get(request, *args, **kwargs)
        response.context_data['order'] = order
        
        return response



@csrf_exempt
def pagseguro_notification(request):
    notification_code = request.POST.get('notificationCode', None)
    if notification_code:
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )
        notification_data = pg.check_notification(notification_code)
        status = notification_data.status
        reference = notification_data.reference
        try:
            order = Order.objects.get(pk=reference)
        except Order.DoesNotExist:
            pass
        else:
            order.pagseguro_update_status(status)
    return HttpResponse('OK')






checkout = CheckoutView.as_view()