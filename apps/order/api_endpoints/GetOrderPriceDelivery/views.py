from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.order.api_endpoints.GetOrderPriceDelivery.serializers import GetDeliveryOrderPriceSerializer


class GetDeliveryOrderPriceAPIView(GenericAPIView):
    serializer_class = GetDeliveryOrderPriceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Calculate the price based on criteria
            overall_price = self.calculate_price(serializer.validated_data)
            return Response({"overall_price": overall_price, },
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def calculate_price(self, data):
        return 50000


__all__ = ['GetDeliveryOrderPriceAPIView']
