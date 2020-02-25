from django.db import models
from .customer import Customer
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class PaymentType(models.Model):

    merchantName = models.CharField(max_length=25)
    accountNumber = models.CharField(max_length=25)
    expirationDate = models.DateTimeField()
    customer = models.ForeignKey("customer", on_delete=models.DO_NOTHING)
    createdAt = models.DateTimeField()

    def __str__(self):
        return f'{self.merchantName}'

    class Meta:
        ordering = ("merchantName",)



