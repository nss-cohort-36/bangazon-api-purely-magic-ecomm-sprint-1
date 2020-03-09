import json
import unittest
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazonapi.models import PaymentType, Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestPaymentType(TestCase):
   
    def setUp(self):
        self.username = 'testuser'
        self.password = 'taco'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.customer = Customer.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)

    def test_post_payment_type(self):
        # define a payment type to be sent to be sent to the API
        new_payment_type = {
            "merchantName": "ZZ Negative",
            "accountNumber": "777",
            "expirationDate": "2029-01-01T00:00:00Z",
            "createdAt": "2029-01-01T00:00:00Z",
            "customer_id": 1
        }

        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('paymenttype-list'), new_payment_type, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one PT instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(PaymentType.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(PaymentType.objects.get().merchantName, 'ZZ Negative')
        
    
if __name__ == '__main__':
    unittest.main()