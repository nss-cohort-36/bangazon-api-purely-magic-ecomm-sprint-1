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
        paymenttype = PaymentType.objects.all()
        #get all paymenttypes
        area = self.request.query_params.get('area', None)
        #get all attractions but filtered by a parameter.  this instance area. area =?
        #foo.com/attractions?area=? to the right is a query param
        if area is not None:
            paymenttypes = paymenttypes.filter(area__id=area)

        serializer = PaymentTypeSerializer(paymenttypes, many=True, context={'request': request})

        return Response(serializer.data)