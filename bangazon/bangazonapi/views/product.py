"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer, Product, ProductType, Order
from rest_framework.decorators import action

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
        fields = ('id', 'url', 'name', 'customer', 'productType', 'price', 'description', 'quantity', 'location', 'imagePath', 'createdAt',)
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
        #creating the parameters to filter by
        customer = self.request.query_params.get('customer', None)
        location = self.request.query_params.get('location', None)
        type = self.request.query_params.get('productType', None)
        quantity = self.request.query_params.get('quantity', None)
        name = self.request.query_params.get('name', None)

        if customer is not None:
            items = items.filter(customer_id=customer)

        # Example GET request:
        #   http://localhost:8000/products?location=louisville
        if location is not None:
            items = items.filter(location__contains=location)

        # Example request:
        #   http://localhost:8000/products?productType=2
        if type is not None:
            items = items.filter(productType__id=type)

        # Example request:
        #   http://localhost:8000/products?quantity=20
        if quantity is not None:
            items = items.order_by("-created_date")[:int(quantity)]

        # Example request:
        #   http://localhost:8000/products?name="white strips"
        if name is not None:
            items = items.filter(name__contains=name)


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

    @action(methods=['get'], detail=False)
    def cart(self, request):

        current_user = Customer.objects.get(user=request.auth.user)

        try:
            open_order = Order.objects.get(customer=current_user, paymentType=None)
            products_on_order = Product.objects.filter(cart__order=open_order)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products_on_order, many=True, context={'request': request})
        return Response(serializer.data)