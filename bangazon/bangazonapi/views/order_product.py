"""View module for handling requests about order_product join table"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Order, OrderProduct, Product


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order_product

    Arguments:
        serializers
    """

    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='order_product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'order', 'product')
        depth = 2

class OrderProduct(ViewSet):
    def retrieve(self, request, pk=None):
        """ GET requests for single order_product item

        Returns:
            Response -- JSON serialized order_product instance
        """
        try:
            order_product_item = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(order_product_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """GET requests for order_product list resource

        Returns:
            Response -- JSON serialized list of order_product instances
        """

        order_product_items = OrderProduct.objects.all()

        customer = self.request.query_params.get('customer', None)
        product = self.request.query_params.get('product', None)
        if customer and product is not None:
            order_product_items = order_product_items.filter(customer__id=customer, product__id=product)

        serializer = OrderProductSerializer(order_product_items, many=True, context={'request': request})

        return Response(serializer.data)