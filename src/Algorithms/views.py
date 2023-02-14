from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Algorithm, CameraAlgorithm
from .serializers import (
    CameraAlgorithmSerializer,
    AlgorithmUpdateSerializer,
    AlgorithmStatusSerializer,
)

from src.StaffControl.Locations.models import Camera

from rest_framework.exceptions import NotFound


class AlgorithmUpdateView(generics.UpdateAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmUpdateSerializer

    def update(self, request, *args, **kwargs):
        received_data = request.data
        for algorithm_name, is_available in received_data.items():
            try:
                algorithm = Algorithm.objects.get(name=algorithm_name)
            except Algorithm.DoesNotExist:
                raise NotFound(
                    detail=f"Algorithm with name '{algorithm_name}' not found"
                )

            algorithm.is_available = is_available
            algorithm.save()

        return Response({"message": "Algorithm status updated"})


class CameraAlgorithmCreateView(generics.CreateAPIView):
    serializer_class = CameraAlgorithmSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        errors = []

        for algorithm_name, camera_ips in data.items():
            algorithm = Algorithm.objects.filter(name=algorithm_name).first()
            if not algorithm:
                errors.append(f"Algorithm with name {algorithm_name} does not exist")
                continue

            if not algorithm.is_available:
                errors.append(f"Algorithm with name {algorithm_name} is not available")
                continue

            cameras = Camera.objects.filter(id__in=camera_ips)
            if not cameras.exists():
                missing_ips = set(camera_ips) - set(
                    cameras.values_list("id", flat=True)
                )
                errors.append(f"Cameras with ip {', '.join(missing_ips)} do not exist")
                continue

            CameraAlgorithm.objects.bulk_create(
                [
                    CameraAlgorithm(algorithm=algorithm, camera_id=camera)
                    for camera in cameras
                ]
            )

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "Camera Algorithm records created successfully"}
            )


class AlgorithmStatusView(generics.GenericAPIView):
    serializer_class = AlgorithmStatusSerializer

    def get(self, request, *args, **kwargs):
        algorithms = Algorithm.objects.all()
        available_algorithms = list(
            algorithms.filter(is_available=True).values_list("name", flat=True)
        )
        unavailable_algorithms = list(
            algorithms.filter(is_available=False).values_list("name", flat=True)
        )

        return Response(
            {"true": available_algorithms, "false": unavailable_algorithms},
            status=status.HTTP_200_OK,
        )
