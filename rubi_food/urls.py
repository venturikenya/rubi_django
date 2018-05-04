"""rubi_delivery URL Configuration

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
from django.conf.urls import url
from . import views
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

app_name='rubi_food'
urlpatterns = [
    url(r'^rubi_api/$', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^(?P<id>[0-9]+)/history/',views.history,name='history'),
    url(r'^dashboard/',views.dash,name='dashboard'),
    url(r'^(?P<id>[0-9]+)/Cart/$', views.clear_cart, name='clear_cart'),
]
