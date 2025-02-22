from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django.db.models import Q

from src.Reports.models import Report
from src.Core.paginators import NoPagination
from src.CompanyLicense.decorators import validate_license
from src.Reports.serializers import ReportSerializers, SearchReportSerializers

from .models import Items
from .serializers import ItemsSerializer


class ItemsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    pagination_class = NoPagination
    ALLOWED_STATUSES = ["Out of stock", "Low stock level", "In stock"]

    @validate_license
    def get_queryset(self):
        status = self.request.query_params.get("status", None)
        if status is not None:
            queryset = self.queryset.filter(status=status)
        else:
            queryset = self.queryset.filter(status__in=self.ALLOWED_STATUSES)

        camera = self.request.query_params.get("camera", None)
        if camera is not None:
            queryset = queryset.filter(camera=camera)

        order = self.request.query_params.get("order", None)
        if order == "desc":
            reversed_statuses = list(reversed(self.ALLOWED_STATUSES))
            queryset = sorted(queryset, key=lambda x: reversed_statuses.index(x.status))
        else:
            queryset = sorted(
                queryset, key=lambda x: self.ALLOWED_STATUSES.index(x.status)
            )

        return queryset


# @validate_license
class ItemsCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer


class ItemsRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class ItemsHistoryViewSet(APIView):
    permission_classes = [IsAuthenticated]

    @validate_license
    def get(self, request, date, start_time, end_time, item_id=None):
        algorithm_name = "min_max_control"
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()

        start_of_day = datetime.combine(date_obj, start_time_obj)
        end_of_day = datetime.combine(date_obj, end_time_obj)

        queryset = Report.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by("-date_created", "-id")

        if algorithm_name:
            queryset = queryset.filter(algorithm__name=algorithm_name)

        if item_id:
            queryset = queryset.filter(extra__icontains=f'"itemId": {item_id},')

        queryset = queryset.order_by("algorithm__name", "camera__id", "id")

        serializer = ReportSerializers(queryset, many=True, context={'item_id': item_id})

        return Response(serializer.data)


class HistoryViewSet(APIView):
    """Search by date and item_id"""

    permission_classes = [IsAuthenticated]

    @validate_license
    def get(self, request, date, item_id=None):
        algorithm_name = "min_max_control"
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_of_day = datetime.combine(date_obj, datetime.min.time())
        end_of_day = datetime.combine(date_obj, datetime.max.time())

        queryset = Report.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        )

        if algorithm_name:
            queryset = queryset.filter(algorithm__name=algorithm_name)

        if item_id:
            queryset = queryset.filter(extra__icontains=f'"itemId": {item_id},').order_by('id')

        serializer = SearchReportSerializers(queryset, many=True, context={'item_id': item_id})

        return Response(serializer.data)
