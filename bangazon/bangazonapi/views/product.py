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
        fields = ('id', 'url', 'name', 'customer', 'productType', 'price', 'description', 'quantity', 'location', 'imagePath', 'createdAt')
        # fields = ('id', 'url', 'name', 'customer',)
        depth = 2

class Products(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single product
        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_product = Product()
        new_product.name = request.data["name"]
        # joe's changes
        new_product.customer = Customer.objects.get(user=request.auth.user.id)
        new_product.productType_id = request.data["productType_id"]
        new_product.price = request.data["price"]
        new_product.description = request.data["description"]
        new_product.quantity = request.data["quantity"]
        new_product.location = request.data["location"]
        # new_product.imagePath = request.data["imagePath"]

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
        # product_list = []

        # for item in items:
        #    new_product = Product()
        #    new_product.productType_id = ProductType.objects.get(pk=item.productType_id)
        #    new_product.id = item.id
        #    new_product.name = item.name
        #    new_product.customer_id =  Customer.objects.get(pk=item.customer_id)
        #    product_list.append(new_product)



        # test
        customer = self.request.query_params.get('customer', None)
        if customer is not None:
            items = items.filter(customer_id=customer)

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
      item.price = request.data["price"]
      item.description = request.data["description"]
      item.quantity = request.data["quantity"]
      item.location = request.data["location"]
      item.imagePath = request.data["imagePath"]
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