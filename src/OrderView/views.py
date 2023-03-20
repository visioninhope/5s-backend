from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from src.OrderView.services import orderView_service, ms_sql_service


class GetAllProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = orderView_service.get_filtered_orders_list()
        return Response(response, status=status.HTTP_200_OK)


class GetOrderDataByZlecenieAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, zlecenie_id):
        response = orderView_service.get_order(zlecenie_id)
        return Response(response, status=status.HTTP_200_OK)


class CreateConectionAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = ms_sql_service.create_connection(request.data)
        return Response(response, status=status.HTTP_201_CREATED)
