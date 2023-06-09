from django.contrib import admin
from .models.camera import Camera, ZoneCameras
from .models.algorithm import Algorithm, CameraAlgorithm, CameraAlgorithmLog


@admin.register(Camera)
class CamerasAdmin(admin.ModelAdmin):
    list_filter = ("id",)


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    list_filter = ("id", "name")


@admin.register(CameraAlgorithm)
class CameraAlgorithmAdmin(admin.ModelAdmin):
    list_filter = ("id", "algorithm", "camera")


@admin.register(CameraAlgorithmLog)
class CameraAlgorithmLogAdmin(admin.ModelAdmin):
    list_filter = ("id",)


@admin.register(ZoneCameras)
class ZoneCamerasAdmin(admin.ModelAdmin):
    readonly_fields = ["is_active"]
    list_display = (
        "camera",
        "name",
        "coords",
        "workplace",
        "index_workplace",
        "date_created",
        "date_updated"
    )
