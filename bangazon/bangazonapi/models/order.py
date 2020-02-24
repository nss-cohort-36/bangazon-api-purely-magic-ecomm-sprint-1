from django.db import models
from .customer import Customer
from .payment_type import PaymentType
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Order(models.Model):

    createdAt = models.DateTimeField()
    customer = models.ForeignKey("Customer", on_delete=models.DO_NOTHING)
    paymentType = models.ForeignKey("PaymentType", on_delete=models.DO_NOTHING)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = (createdAt,)



