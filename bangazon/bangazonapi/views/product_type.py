"""View module for handling requests about product types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import ProductType

class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for intineraries
    Arguments:
        serializers
    """

    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='product_type',
            lookup_field='id'
        )
        #the fields are the columns you want to include in the database
        fields = ('id', 'name')
        depth = 2