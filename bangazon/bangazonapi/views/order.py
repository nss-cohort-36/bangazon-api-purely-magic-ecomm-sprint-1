"""View module for handling requests about intineraries"""
import json
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from bangazonapi.models import Customer, PaymentType, Order, OrderProduct, Product
from .product import ProductSerializer

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for intineraries
    Arguments:
        serializers
    """

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'createdAt', 'customer', 'paymentType',)
        depth = 2

class Orders(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single order
        Returns:
            Response -- JSON serialized order instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        req_body = json.loads(request.body.decode())
        new_order = Order()
        new_order.customer_id = request.auth.user.customer.id
        new_order.save()

        new_orderproduct = OrderProduct()
        products = Product.objects.all()
        new_orderproduct.order_id = new_order.id 
        new_orderproduct.product_id = req_body['product_id']
        new_orderproduct.save()

        serializer = OrderSerializer(new_order, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to orders resource
        Returns:
            Response -- JSON serialized list of orders
        """

        orders = Order.objects.all()
        # forgein key goes here
        paymentType = self.request.query_params.get('paymentType', None)
        customer = self.request.query_params.get('customer', None)
        if paymentType is not None:
            orders = orders.filter(paymentType__id=paymentType)
        if customer is not None:
            orders = orders.filter(customer__id=customer)

        serializer = OrderSerializer(orders, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

