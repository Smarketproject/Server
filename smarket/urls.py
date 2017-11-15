"""smarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from core import views
from rest_framework import routers
from djoser import views as viewd
from django.conf import settings
from django.conf.urls.static import static

router=routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'user', views.ProductViewSet)





urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include(router.urls)),

    url(r'^login/', viewd.TokenCreateView.as_view(), name='login2'),
    
    url(r'^logout/', viewd.TokenDestroyView.as_view(),name='logout2'),
    
    url(r'^me/$', viewd.UserView.as_view(), name='user'),

    url(r'^purchase/show/$', views.Show_purchases.as_view(), name='Show_purchases'),

    url(r'^product/showall/$', views.Show_products.as_view(), name='Show_products'),

    url(r'^cart/showall/$', views.Show_carts.as_view(), name='Show_carts'),

    url(r'^product/scanner/$', views.Get_products.as_view(), name='user'),

    url(r'^userup/$', views.Update_password.as_view(), name='userUp'),

    url(r'^finalizando/(?P<pk>\d+)/pagseguro/$', views.Pagseguro.as_view()),

    url(
        r'^notificacoes/pagseguro/$', views.pagseguro_notification,
        name='pagseguro_notification'
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
