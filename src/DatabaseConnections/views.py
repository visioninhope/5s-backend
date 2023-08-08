from rest_framework.response import Response
from rest_framework import generics, status

from src.DatabaseConnections.models import ConnectionInfo
from src.DatabaseConnections.serilisers import ConnectionInfoSerializer


class UpdateActiveResourceView(generics.UpdateAPIView):
    serializer_class = ConnectionInfoSerializer

    def update(self, request, *args, **kwargs):
        connector_type: str = request.data.get("type")

        if connector_type == "database":
            connector_to_activate: ConnectionInfo = ConnectionInfo.objects.filter(type="database")
            connector_to_deactivate: ConnectionInfo = ConnectionInfo.objects.filter(type="api")
        elif connector_type == "api":
            connector_to_activate: ConnectionInfo = ConnectionInfo.objects.filter(type="api")
            connector_to_deactivate: ConnectionInfo = ConnectionInfo.objects.filter(type="database")
        else:
            return Response(
                {"detail": "Either 'api' or 'database' parameter must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not connector_to_activate.exists():
            return Response({"detail": "Connection doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        connector_to_deactivate.update(is_active=False)
        connector_to_activate.update(is_active=True)
        return Response({"detail": "Active resource updated successfully."})
