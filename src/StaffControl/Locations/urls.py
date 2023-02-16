from rest_framework.routers import DefaultRouter
from src.StaffControl.Locations.views import (
    CameraViewSet,
    GateViewSet,
    LocationViewSet,
    SaveCameraDetailsView,
    GetCamerasLink,
    GetCameraImagesAPIView,
)
from django.urls import path, include

router = DefaultRouter()

router.register(r"camera", CameraViewSet, basename="Camera")
router.register(r"gate", GateViewSet, basename="gates")
router.register(r"location", LocationViewSet, basename="locations")

urlpatterns = [
    path("post_camera/", SaveCameraDetailsView.as_view()),
    path("get_camera_links/", GetCamerasLink.as_view()),
    path("get_camera_images/", GetCameraImagesAPIView.as_view()),
]

urlpatterns += router.urls
