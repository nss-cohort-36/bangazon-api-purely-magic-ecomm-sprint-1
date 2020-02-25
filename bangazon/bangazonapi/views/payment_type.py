from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import PaymentType, Customer

class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for paymenttype

    Arguments:
        serializers
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymentType',
            lookup_field='id'
        )
        fields = ('id', 'merchantName', 'accountNumber', 'expirationDate', 'createdAt', 'customer_id')
        # depth = 2

class PaymentTypes(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET operations

        Returns:
            Response -- JSON serialized paymenttype instance
        """

        try:
            paymenttype = PaymentType.objects.get(pk=pk) 
            serializer = PaymentTypeSerializer(paymenttype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET to list of paymenttypes resource

        Returns:
            Response -- JSON serialized attraction attractions
        """
        ##get all payment types
        paymenttypes = PaymentType.objects.all()
        #foreign key goes here
        customer = self.request.query_params.get('customer', None)
        if customer is not None:
            orders = orders.filter(customer_id=customer)

        serializer = PaymentTypeSerializer(paymenttypes, many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized PaymentType instance
        """
        newpaymenttype = PaymentType()
        newpaymenttype.merchantName = request.data["merchantName"]
        newpaymenttype.accountNumber = request.data["accountNumber"]
        newpaymenttype.expirationDate = request.data["expirationDate"]
        newpaymenttype.createdAt = request.data["createdAt"]
        newpaymenttype.customer_id = request.auth.user.customer.id
        newpaymenttype.save()

        serializer = PaymentTypeSerializer(newpaymenttype, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a  single payment-type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            paymenttype = PaymentType.objects.get(pk=pk)
            paymenttype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a payment_type

        Returns:
            Response -- Empty body with 204 status code
        """
        paymenttype = PaymentType.objects.get(pk=pk)
        paymenttype.merchantName = request.data["merchantName"]
        paymenttype.accountNumber = request.data["accountNumber"]
        paymenttype.expirationDate = request.data["expirationDate"]
        # paymenttype.createdAt = request.data["createdAt"]
        # paymenttype.customer_id = request.auth.user.customer.id
        paymenttype.save()


        return Response({}, status=status.HTTP_204_NO_CONTENT)
