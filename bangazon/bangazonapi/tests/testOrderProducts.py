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
            self.createdAt = "2019-12-12T00:00:00Z"
            self.productType_id = ProductType.objects.create(name=self.name)
            self.name = "medicinal"
            self.customer_id = 1
            self.productType_id = 1
            self.product_id = Product.objects.create(name=self.name, price=self.price, description=self.description, 
            quantity=self.quantity, productType_id=self.productType_id, location=self.location, imagePath=self.imagePath, createdAt=self.createdAt, customer_id=self.customer_id)
            # *** Payment Type instances ***
            self.paymentType = 1
            self.createdAt = "2019-12-12T00:00:00Z"
            self.order_id = Order.objects.create(customer_id=self.customer_id, createdAt=self.createdAt)


            # ***CREATE*** 
        def test_post_order_product(self):
            new_orderproduct = {
                "order_id": 1,
                "product_id": 1
            }                   

            #  Use the client to send the request and store the response
            response = self.client.post(
                reverse('orderproduct-list'), new_orderproduct, HTTP_AUTHORIZATION='Token ' + str(self.token)
            )

            # Getting 200 back because we have a success url
            self.assertEqual(response.status_code, 200)

            # Query the table to see if there's one ParkArea instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
            self.assertEqual(OrderProduct.objects.count(), 1)

            # And see if it's the one we just added by checking one of the properties. Here, name.
            self.assertEqual(OrderProduct.objects.get().order_id, 1)


            # ***READ***
        def test_get_order_product(self):
            new_orderproduct = {
                "order_id": 1,
                "product_id": 1
            }                   


            # Now we can grab all the area (meaning the one we just created) from the db
            response = self.client.get(reverse('orderproduct-list'))

            # Check that the response is 200 OK.
            # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
            self.assertEqual(response.status_code, 200)

            # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
            # Are we responding with the data we asked for? There's just one parkarea in our dummy db, so it should contain a list with one instance in it
            self.assertEqual(len(response.data), 1)

            # test the contents of the data before it's serialized into JSON
            self.assertEqual(response.data[0]['id'], 1)
            
            # self.assertIn( new_orderproduct.order_id, response.content)


        # ***DESTROY***
        def test_delete_order_product(self):
            new_orderproduct = Product.objects.create(
                order_id=1,
                product_id=1,
        )
        # Delete a product. As shown in our post and get tests above, new_product
        # will be the only product in the database, and will have an id of 1
            response = self.client.delete(
                reverse('orderproduct-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))
            self.assertEqual(response.status_code, 204)
        # Confirm that the product is NOT in the database, which means no products will be
        # response = self.client.get(reverse('product-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        # self.assertEqual(len(response.data), 0)
            response = self.client.get(reverse('orderproduct-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
            self.assertEqual(len(response.data), 0)

if __name__ == '__main__':
    unittest.main()