from django.contrib import admin
from .models import CustomUser, History, ImageUsers
from apps.Locations.models import Location
from django.utils.safestring import mark_safe


@admin.register(CustomUser)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'date_joined', 'dataset')
    list_filter = ('id',)


@admin.register(ImageUsers)
class ImageTaskAdmin(admin.ModelAdmin):
    pass


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('people', 'id', 'entry_date', 'release_date', 'get_image', 'dataset', 'location')
    list_filter = ('people', 'id')
    readonly_fields = ("get_image",)

    def location(self, obj):
        result = CustomUser.objects.filter(id=obj.people.id).values('location_id')[0]['location_id']
        return result

    def dataset(self, obj):
        result = CustomUser.objects.filter(id=obj.people.id).values('dataset')[0]['dataset']
        return result

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url} "width="50" height="60" />')

    get_image.short_description = 'image'
