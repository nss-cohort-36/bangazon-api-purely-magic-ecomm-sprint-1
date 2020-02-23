from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver



class ProductType(models.Model):

    name = models.CharField(max_length=55)
    

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = (F('user.date_joined').asc(nulls_last=True),)