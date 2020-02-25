"""View module for handling requests about product types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers
    Arguments:
        serializers
    """

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        #the fields are the columns you want to include in the database
        fields = ('id',)
        # depth = 2

class Customers(ViewSet):

    #handles GET for a single product type
    def retrieve(self, request, pk=None):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer,
            context = {'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    #handles Get request to list ALL product_types
    def list(self, request):
        customer = Customer.objects.all()

        serializer = CustomerSerializer(
            customer, many = True, context={'request':request})

        return Response(serializer.data)