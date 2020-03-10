import json
import unittest
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazonapi.models import Product, Customer, ProductType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class TestProduct(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.customer = Customer.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.product_type = ProductType.objects.create(name="Blood")

    def test_post_product(self):
        # define a product to be sent to the API
        new_product = {
            "name": "O- Blood",
            "price": 999.99,
            "description": "Hungry for some universal?",
            "quantity": 1,
            "location": "Transylvania",
            "imagePath": "",
            "productType_id": 1,
            "customer": self.customer.id
        }

        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one Product instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(Product.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(Product.objects.get().name, 'O- Blood')

    def test_get_products(self):
        new_product = Product.objects.create(
            name="Wooden Stake Proof Vest",
            price=500.00,
            description="For when you need to fight that midnight wood.",
            quantity=5,
            location="Seattle",
            imagePath="",
            productType_id=1,
            customer_id=self.customer.id
        )

        # Now we can grab all the product (meaning the one we just created) from the db
        response = self.client.get(reverse('product-list'))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one parkarea in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["name"], "Wooden Stake Proof Vest")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_product.name.encode(), response.content)


if __name__ == '__main__':
    unittest.main()
