from django.db import models

from src.Cameras.models import Camera
from src.Reports.models import Report


class Items(models.Model):
    """Models items"""

    name = models.TextField(max_length=75, verbose_name="Item name")
    status = models.CharField(max_length=20, default="Out of stock")
    current_stock_level = models.IntegerField(verbose_name="Current stock level", default=0)
    low_stock_level = models.IntegerField(verbose_name="Low stock level")
    email = models.EmailField(blank=True, null=True, verbose_name="Email to send notifications")
    camera = models.ForeignKey(Camera, related_name='camera_id', on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Date updated", auto_now=True)
    coords = models.TextField(verbose_name="Area coordinates", blank=True, null=True)

    def __str__(self):
        return self.name
