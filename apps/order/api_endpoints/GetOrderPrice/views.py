from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.order.api_endpoints.GetOrderPrice.serializers import GeneratePriceSerializer
from django.conf import settings


class GetOrderPriceAPIView(GenericAPIView):
    serializer_class = GeneratePriceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Calculate the price based on criteria
            overall_price, detailed_info = self.calculate_price(serializer.validated_data)
            return Response({"overall_price": overall_price, "detailed_info": detailed_info}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def calculate_price(self, data):
        price = 0
        detailed_info = {}
        if data["front_right"]:
            price += settings.PRICING_RULES['front_right']
            detailed_info['front_right'] = settings.PRICING_RULES['front_right']
        if data["back_left"]:
            price += settings.PRICING_RULES['back_left']
            detailed_info['back_left'] = settings.PRICING_RULES['back_left']
        if data["back_middle"]:
            price += settings.PRICING_RULES['back_middle']
            detailed_info['back_middle'] = settings.PRICING_RULES['back_middle']
        if data["back_right"]:
            price += settings.PRICING_RULES['back_right']
            detailed_info['back_right'] = settings.PRICING_RULES['back_right']

        additional_people = data["number_of_people"] - 1
        if additional_people > 0:
            discounted_price = settings.DISCOUNT_PRICE_FOR_ADDITIONAL_PERSON * additional_people
            price -= discounted_price
            detailed_info['discount_for_additiona_person'] = discounted_price
        return price, detailed_info


__all__ = ['GetOrderPriceAPIView']
