from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from apps.Locations.models import Camera, Gate, Location
from apps.Locations.serializers import (
    CameraSerializer,
    GateSerializer,
    LocationSerializer,
)
from rest_framework.response import Response


from .service import onvif_camera


class CameraViewSet(ModelViewSet):
    """List of all Camer"""

    serializer_class = CameraSerializer
    queryset = Camera.objects.all()

    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly,]


class GateViewSet(ModelViewSet):
    """List of all gates"""

    serializer_class = GateSerializer
    queryset = Gate.objects.all()

    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly,]


class LocationViewSet(ModelViewSet):
    """List of all locations"""

    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly,]


class GetOnvifCameraView(APIView):
    """Get list of all cameras and fill table with them"""

    def get(self, request, *args, **kwargs):
        all_cameras_ips = onvif_camera.start()
        print(f"Onvif camera list: %s" % all_cameras_ips)

        return Response(all_cameras_ips)
