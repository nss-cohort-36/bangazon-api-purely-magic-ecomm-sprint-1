from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class ProductType(models.Model):

    name = models.CharField(max_length=55)
    

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ("name",)