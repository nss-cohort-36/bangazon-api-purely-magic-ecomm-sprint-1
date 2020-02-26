"""View module for handling requests about intineraries"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer, PaymentType, Order

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
        new_order = Order()
        new_order.customer_id = request.auth.user.customer.id
        new_order.paymentType_id = request.data["paymentType_id"]

        new_order.save()

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
            orders = orders.filter(customer_id=customer)

        serializer = OrderSerializer(orders, many=True, context={'request': request})

        return Response(serializer.data)