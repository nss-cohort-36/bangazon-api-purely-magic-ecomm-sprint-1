"""View module for handling requests about product types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import ProductType

class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product_types
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


class ProductTypes(ViewSet):

    #handles POST
    def create(self, request):
        new_product_type = ProductType()
        new_product_type.name = request.data["name"]

        new_product_type.save()

        serializer = ProductTypeSerializer(new_product_type, context={'request': request})

        return Response(serializer.data)


    #handles GET for a single product type
    def retrieve(self, request, pk=None):
        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(product_type,
            context = {'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    #handles Get request to list ALL product_types
    def list(self, request):
        product_type = ProductType.objects.all()

        serializer = ProductTypeSerializer(
            product_type, many = True, context={'request':request})

        return Response(serializer.data)


    #handles PUT
    def update(self, request, pk=None):
       
        product_type = ProductType.objects.get(pk=pk)
        product_type.starttime = request.data['name']

        product_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    #handles DELETE and returns serialized detail of deleted product type
    def destroy(self, request, pk=None):
        try:
            product_type = ProductType.objects.get(pk=pk)
            product_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)