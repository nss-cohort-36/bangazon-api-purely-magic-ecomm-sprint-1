from django.db import models
from .customer import Customer
from .product_type import ProductType

class Product(models.Model):

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75)
    imagePath = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey("Customer", on_delete=models.DO_NOTHING)
    productType = models.ForeignKey("ProductType", on_delete=models.DO_NOTHING)
    

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ("name",)