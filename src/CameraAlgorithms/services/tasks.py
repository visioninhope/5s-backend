from celery import shared_task

from dateutil.parser import parse

import logging

from src.Core.utils import Sender
from src.CameraAlgorithms.models.algorithm import Algorithm

logger = logging.getLogger(__name__)


@shared_task
def uploading_algorithm(id_algorithm, image_name):
    """Background loading of the algorithm"""

    algorithm = Algorithm.objects.get(id=id_algorithm)
    result = Sender("loading", image_name)
    if result.get("status"):
        date_created = parse(result.get("date"))
        algorithm.date_created = date_created
        algorithm.download_status = True
        algorithm.save()
        return "success True"
    else:
        return logger.warning(f"Error loading {algorithm.image_name}")
