from typing import Dict, List, Any

from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework import generics, status
from rest_framework.response import Response

from src.Core.paginators import NoPagination
from src.MsSqlConnector.connector import connector as connector_service

from .services import OperationServices, OrderServices
from .utils import generate_hash


class GetOperation(generics.GenericAPIView):
    pagination_class = NoPagination

    @connector_service.check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")
        operations_type_id = request.GET.getlist("typeID")

        key: str = generate_hash("get_operation", from_date, to_date)
        response = cache.get(key)

        if response is None:
            response: List[Dict[str, Any]] = OperationServices.get_operations(
                from_date, to_date, operations_type_id
            )
            cache.set(key, response, timeout=120)

        if response:
            return JsonResponse(data=response, status=status.HTTP_200_OK, safe=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetMachine(generics.GenericAPIView):
    pagination_class = NoPagination

    @connector_service.check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        key: str = generate_hash("get_machine", from_date, to_date)
        response = cache.get(key)

        if response is None:
            response: List[Dict[str, Any]] = OperationServices.get_machine(
                from_date, to_date
            )
            cache.set(key, response, timeout=60)

        if response:
            return JsonResponse(data=response, status=status.HTTP_200_OK, safe=False)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetOrders(generics.GenericAPIView):
    pagination_class = NoPagination

    @connector_service.check_database_connection
    def get(self, request):
        from_date: str = request.GET.get("from")
        to_date: str = request.GET.get("to")

        key: str = generate_hash("get_order", from_date, to_date)
        response = cache.get(key)

        if response is None:
            response: List[Dict[str, str]] = OrderServices.get_order(from_date, to_date)
            cache.set(key, response, timeout=120)

        return JsonResponse(response, status=status.HTTP_200_OK, safe=False)


class GetOrderByDetail(generics.GenericAPIView):
    pagination_class = NoPagination

    @connector_service.check_database_connection
    def get(self, request):
        operation_id: int = request.GET.get("operation")
        response: Dict[str, Any] = OrderServices.get_order_by_details(operation_id)
        return JsonResponse(data=response, status=status.HTTP_200_OK)


class GetWhnetOperation(generics.GenericAPIView):
    pagination_class = NoPagination

    @method_decorator(cache_page(30))
    @connector_service.check_database_connection
    def get(self, request):
        response: Dict[str, Any] = OperationServices.get_whnet_operation()

        return JsonResponse(data=response, status=status.HTTP_200_OK, safe=False)
