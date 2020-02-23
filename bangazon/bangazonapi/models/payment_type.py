from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class PaymentType(models.Model):

    merchantName = models.CharField(max=25)
    accountNumber = models.CharField(max=25)
    expirationDate = models.DateTimeField()
    customer = models.ForeignKey("Customer", on_delete=models.DO_NOTHING)
    createdAt = models.DateTimeField()

    def __str__(self):
        return f'{self.merchantName}'

    class Meta:
        ordering = (F('user.date_joined').asc(nulls_last=True),)