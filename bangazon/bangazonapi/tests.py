import unittest
from django.test import TestCase
from django.urls import reverse
from .models import ProductType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestProductTypes(TestCase):

    # Base setup for the user test element
    def setUpUser(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)
    
    def test_post_product_type(self):
        # define a product_type to be sent to the API
        new_product_type = {
              "name": "Potions"
            }

        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('producttype-list'), new_product_type
          )

        # Assert
        # Getting 200 back because we have a success url (or a 302 if the view is redirecting )
        self.assertEqual(response.status_code, 200)
    
        self.assertEqual(ProductType.objects.count(), 1)

        self.assertEqual(ProductType.objects.get().name, 'Potions')


    
    def test_get_product_type(self):
        # create the test payment type
        new_product_type = ProductType.objects.create(
            name="Potions"
        )
        
        response = self.client.get(reverse('producttype-list'))
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.context['producttype-list']), 1)
        
        self.assertIn(new_product_type.name.encode(), response.content)