import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazonapi.models import OrderProduct, Order, Customer, ProductType, Product
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

print("test file loads-----------------")

class testOrderProducts(TestCase):


        def setUp(self):
            self.username = 'chollyp7'
            self.password = 'bitemerobot'
            self.user = User.objects.create_user(username=self.username, password=self.password)
            self.customer = Customer.objects.create(
            user=self.user)
            self.token = Token.objects.create(user=self.user)
            self.name = "anti-garlic tablets"
            self.price = "9.00"
            self.description = "12 hour slow release tablets to offset the dangers of Italian food"
            self.quantity = 9
            self.location = "Brentwood"
            self.imagePath = ""
            self.created_at = "2019-12-12T00:00:00Z"
            self.producType_id = ProductType.objects.create(name=self.name)
            self.name = "medicinal"
            self.customer_id = 1
            self.productType_id = 1
            self.product_id = Product.objects.create(name=self.name, price=self.price, description=self.description, 
            quantity=self.quantity, productType_id=self.productType_id, location=self.location, imagePath=self.imagePath, created_at=self.created_at, customer_id=self.customer_id)
            # *** Payment Type instances ***
            self.paymentType = 1
            self.createdAt = "2019-12-12T00:00:00Z"
            self.order_id = Order.objects.create(customer_id=self.customer_id, createdAt=self.createdAt)