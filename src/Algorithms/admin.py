from django.contrib import admin

from .models import Algorithm, CameraAlgorithm


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_available",
    )
    list_filter = ("is_available",)


@admin.register(CameraAlgorithm)
class CameraAlgorithmAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "algorithm",
        "camera",
        "is_active",
        "process_id",
    )
    list_filter = ("camera", "process_id", "is_active")
