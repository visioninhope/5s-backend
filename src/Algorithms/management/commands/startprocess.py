from django.core.management.base import BaseCommand

from ....core.logger import logger

from src.Algorithms.models import CameraAlgorithm
from src.Algorithms.utils import yolo_proccesing


class Command(BaseCommand):
	"""
	Checks if any processes have been started and
	puts them back to work at the start of the project
	"""

	def handle(self, *args, **kwargs):
		self.start_process()
		logger.info("The command was executed")

	def start_process(self) -> None:
		all_camera_algorithms = CameraAlgorithm.objects.filter(is_active=True).exclude(
			process_id=None
		)
		for camera_algorithm in all_camera_algorithms:
			try:
				result = yolo_proccesing.start_yolo_processing(
					camera=camera_algorithm.camera,
					algorithm=camera_algorithm.algorithm,
					url=camera_algorithm.yolo_url,
				)
			except:
				logger.critical(
					f"Camera {camera_algorithm.camera} with alogithm {camera_algorithm.algorithm}"
				)
				logger.critical(
					f"has not been renewed. Server url -> {camera_algorithm.yolo_url}"
				)
			else:
				if not result["success"] or "pid" not in result:
					logger.critical("Cannot find status in response")
					
				new_process_id = result["pid"]

				camera_algorithm.process_id = new_process_id
				camera_algorithm.save()

				logger.info(f"Camera {camera_algorithm.camera} with alogithm")
				logger.info(
					f"{camera_algorithm.algorithm} were successfully restored and given a new PID -> {new_process_id}."
				)

					
