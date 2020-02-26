"""View module for handling requests about order product join table"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer, Product, OrderProduct

class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order products
    Arguments:
        serializers
    """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'url', 'order', 'product',)

        depth = 2

class OrderProducts(ViewSet):

    def create(self, request):
        new_orderproduct = OrderProduct()
        new_orderproduct.order_id = request.data["order_id"]
        new_orderproduct.product_id = request.data["product_id"]

        new_orderproduct.save()

        serializer = OrderProductSerializer(new_orderproduct, context={'request': request})

        return Response(serializer.data)
        

    def retrieve(self, request, pk=None):
        """ GET requests for single orderproduct

        Returns:
            Response -- JSON serialized order_product instance
        """

        try:
            orderproduct = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(orderproduct, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """GET requests for orderproduct list resource

        Returns:
            Response -- JSON serialized list of order_product instances
        """

        items = OrderProduct.objects.all()

        order = self.request.query_params.get('order', None)
        product = self.request.query_params.get('product', None)
        if order is not None:
            items = items.filter(order__id=order)

        if product is not None:
            orders = orders.filter(product__id=product)

        serializer = OrderProductSerializer(items, many=True, context={'request': request})

        return Response(serializer.data)