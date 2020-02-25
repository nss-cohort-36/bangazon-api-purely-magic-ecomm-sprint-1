"""bangazon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# change to push
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from bangazonapi.views import PaymentTypes
from bangazonapi.models import *
from bangazonapi.views import ProductTypes
from bangazonapi.views import Orders
from bangazonapi.views import register_user, login_user



# from bangazon.bangazonapi.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'paymenttypes', PaymentTypes, 'paymenttype')
router.register(r'product_types', ProductTypes, 'product_types')
router.register(r'orders', Orders, 'order')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user),
    path('login/', login_user),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
