import requests

from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, mixins

from .const import SERVER_URL
from .serializers import SystemMessagesSerializer
from .models import SystemMessage


class FindCameraAPIView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        cameras_response = requests.get(f"{SERVER_URL}:7654/get_all_onvif_cameras/")
        try:
            cameras = cameras_response.json()
        except ValueError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response_data = {"results": cameras}
        return Response(response_data, status=status.HTTP_200_OK)


class SystemMessagesApiView(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = SystemMessagesSerializer
    queryset = SystemMessage.objects.order_by("-id")

    def get_queryset(self):
        page_size = self.request.query_params.get('page_size', 25)
        paginator = Paginator(self.queryset, page_size)
        page_number = self.request.query_params.get('page', 1)
        page = paginator.get_page(page_number)
        return page
