from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Order(models.Model):

    createdAt = models.DateTimeField()
    customer = models.ForeignKey("Customer", on_delete=models.DO_NOTHING)
    paymentType = models.ForeignKey("PaymentType", on_delete=models.DO_NOTHING)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = (F('user.date_joined').asc(nulls_last=True),)

