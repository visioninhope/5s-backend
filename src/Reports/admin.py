from django.contrib import admin
from .models import Report, SkanyReport
from src.ImageReport.models import Image
from django.utils.safestring import mark_safe



# @admin.register(Report)
# class ReportAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "algorithm",
#         "camera",
#         "start_tracking",
#         "stop_tracking",
#         "violation_found",
#         "date_created",
#     )
#     list_filter = ("algorithm", "camera",)
class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class ReportAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['algorithm', 'id', 'camera', 'violation_found', 'num_photos', 'date_created']
    list_filter = ['algorithm', 'camera', 'violation_found']
    search_fields = ['algorithm__name', 'camera__name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('photos')
        return queryset

    def num_photos(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="150px" height="120px" />')

    num_photos.short_description = 'Number of Photos'


admin.site.register(Report, ReportAdmin)


@admin.register(SkanyReport)
class SkanyReportAdmin(admin.ModelAdmin):
    list_display = ("report", "skany_index")
