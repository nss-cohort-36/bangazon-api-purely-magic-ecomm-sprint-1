import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from kennywoodapi.models import ParkArea
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestPaymentType(TestCase):

    def setUp(self):
        self.merchantName = 'A Negative',
        self.accountNumber = '99988833'
        self.expirationDate = '2024-01-01T00:00:00Z'
        self.createdAt = '2019-01-01T00:00:00Z',
        self.customer_id: 1

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     string = 'hello world'
    #     self.assertEqual(string.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         string.split(2)

# if __name__ == '__main__':
#     unittest.main()