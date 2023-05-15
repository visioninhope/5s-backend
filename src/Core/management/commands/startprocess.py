import logging
from typing import Dict, Any

from django.core.management.base import BaseCommand

from src.Core.const import SERVER_URL
from src.Core.exceptions import SenderError, InvalidResponseError
from src.Inventory.models import Items
from src.Algorithms.models import CameraAlgorithm
from src.Cameras.models import Camera

from src.CameraAlgorithms.services.cameraalgorithm import (
    camera_rtsp_link,
    send_run_request,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.start_process()

    def start_process(self) -> None:
        camera_algorithms = CameraAlgorithm.objects.filter(is_active=True).exclude(
            process_id=None
        )
        camera_obj: Camera = camera_algorithms.camera
        algorithm_obj: CameraAlgorithm = camera_algorithms.algorithm
        rtsp_link: str = camera_rtsp_link(camera_obj.id)

        for camera_algorithm in camera_algorithms:
            extra_params = []
            if camera_algorithm.algorithm.name == "min_max_control":
                algorithm_items = Items.objects.filter(camera=camera_algorithm.camera)

                for item in algorithm_items:
                    extra_params.append(
                        {
                            "itemId": item.id,
                            "coords": item.coords,
                            "itemName": item.name,
                        }
                    )

            request: Dict[str, Any] = {
                "camera_url": rtsp_link,
                "algorithm": algorithm_obj.name,
                "server_url": SERVER_URL,
                "extra": extra_params,
            }

            try:
                result = send_run_request(request)
            except SenderError as e:
                logger.critical(f"Yolo server is not available. Details: {e}")
            except InvalidResponseError as e:
                logger.critical(
                    f"Yolo can't start algorithm {algorithm_obj.name} on camera {camera_obj.id}. Details: {e}"
                )
            else:
                new_process_id = result["pid"]

                camera_algorithm.process_id = new_process_id
                camera_algorithm.save()
