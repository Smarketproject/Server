from django.conf.urls import url
from fake import views

urlpatterns = [

    url(r'^scale$', views.scale, name='scale'),

]