import unittest
from django.test import TestCase
from django.urls import reverse
from ..models import ProductType

class TestProductTypes(TestCase):
    def test_get_product_type(self):
        # create the test payment type
        new_product_type = ProductType.objects.create(
            name="Potions"
        )
        
        response = self.client.get(reverse('history:product_type_list'))
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.context['animal_list']), 1)
        
        self.assertIn(new_product_type.name.encode(), response.content)