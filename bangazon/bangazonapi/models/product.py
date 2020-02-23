from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

class Product(models.Model):

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75)
    imagePath = models.CharField(max_length=255)
    createdAt = models.DateTimeField()
    customer = models.ForeignKey("Customer", on_delete=models.DO_NOTHING)
    productType = models.ForeignKey("ProductType", on_delete=models.DO_NOTHING)
    

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = (F('user.date_joined').asc(nulls_last=True),)