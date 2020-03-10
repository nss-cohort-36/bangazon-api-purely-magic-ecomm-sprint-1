from django.db import models
from .customer import Customer
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class PaymentType(models.Model):
#test
    name = models.CharField(max_length=25)
    number = models.CharField(max_length=25)
    expiry = models.CharField(max_length=25)
    customer = models.ForeignKey("customer", on_delete=models.DO_NOTHING)
    # createdAt = models.DateTimeField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ("name",)



