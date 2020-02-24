from django.db import models
from .order import Order
from .product import Product
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class OrderProduct(models.Model):
    """
    Creates the join table for the many to many relationship between orders and products
    """
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        ordering = ("product",)