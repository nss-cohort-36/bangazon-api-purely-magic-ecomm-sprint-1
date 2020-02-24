"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer, Product, ProductType

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products
    Arguments:
        serializers
    """

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'productType',)
        depth = 2

class Products(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single product
        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_product = Product()
        new_product.name = request.data["name"]
        new_product.customer_id = request.auth.user.id
        new_product.productType_id = request.data["productType_id"]

        new_product.save()

        serializer = ProductSerializer(new_product, context={'request': request})

        return Response(serializer.data)


    # handles GET all
    def list(self, request):
        """Handle GET requests to products resource
        Returns:
            Response -- JSON serialized list of products
        """
        items = Product.objects.all()

        # test
        customer = self.request.query_params.get('customer', None)
        if customer is not None:
            items = items.filter(customer__id=customer)

        serializer = ProductSerializer(
            items,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    # handles PUT
    def update(self, request, pk=None):
      """Handle PUT requests for a product
      Returns:
          Response -- Empty body with 204 status code
      """
      item = Product.objects.get(pk=pk)
      item.name = request.data["name"]
      item.productType_id = request.data["productType_id"]
      item.customer_id = request.data["customer_id"]
      item.save()

      return Response({}, status=status.HTTP_204_NO_CONTENT)

    # handles DELETE
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            item = Product.objects.get(pk=pk)
            item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)