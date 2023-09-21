from django.core.management.base import BaseCommand

from src.CameraAlgorithms.models import Algorithm
from src.Core.const import ALGORITHMS


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_or_update_algorithms()

    def create_or_update_algorithms(self):
        for algorithms_data in ALGORITHMS:
            print(algorithms_data)
            algorithm, created = Algorithm.objects.update_or_create(
                name=algorithms_data["name"],
                defaults={
                    "is_available": algorithms_data["is_available"],
                    "image_name": algorithms_data["image_name"],
                    "description": algorithms_data["description"],
                },
            )
            if created:
                algorithm.save()
