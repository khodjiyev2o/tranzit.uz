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
            overall_price, detailed_info, discount_price = self.calculate_price(serializer.validated_data)
            return Response({"overall_price": overall_price,
                             "detailed_info": detailed_info,
                             "discount_price": discount_price},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def calculate_price(self, data):
        price, discount_price = 0, 0
        detailed_info = []
        if data["front_right"]:
            seats_price = {}
            price += settings.PRICING_RULES['front_right']
            seats_price['price'] = settings.PRICING_RULES['front_right']
            seats_price['seat'] = "front_right"
            detailed_info.append(seats_price)
        if data["back_left"]:
            seats_price = {}
            price += settings.PRICING_RULES['back_left']
            seats_price['price'] = settings.PRICING_RULES['back_left']
            seats_price['seat'] = "back_left"
            detailed_info.append(seats_price)
        if data["back_middle"]:
            seats_price = {}
            price += settings.PRICING_RULES['back_middle']
            seats_price['price'] = settings.PRICING_RULES['back_middle']
            seats_price['seat'] = "back_middle"
            detailed_info.append(seats_price)
        if data["back_right"]:
            seats_price = {}
            price += settings.PRICING_RULES['back_right']
            seats_price['price'] = settings.PRICING_RULES['back_right']
            seats_price['seat'] = "back_right"
            detailed_info.append(seats_price)
        additional_people = data["number_of_people"] - 1
        if additional_people > 0:
            discount_price = settings.DISCOUNT_PRICE_FOR_ADDITIONAL_PERSON * additional_people
            price -= discount_price

        return price, detailed_info, discount_price


__all__ = ['GetOrderPriceAPIView']
