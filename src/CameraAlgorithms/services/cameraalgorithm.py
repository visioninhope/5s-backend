import requests
import logging

from typing import Any, Dict, Iterable, List, Optional, Set

from src.Core.exceptions import InvalidResponseError, SenderError, CameraConnectionError
from src.Core.utils import Sender
from src.Core.const import SERVER_URL
from src.Inventory.models import Items
from src.OrderView.models import IndexOperations
from src.CompanyLicense.decorators import check_active_cameras, check_active_algorithms

from ..models import Camera, ZoneCameras, Algorithm, CameraAlgorithm
from .logs_services import logs_service

logger = logging.getLogger(__name__)


@check_active_cameras
@check_active_algorithms
def CreateCameraAlgorithms(camera_algorithm_data: Dict[str, Any]) -> None:
    camera: Dict[str, str] = camera_algorithm_data.get("camera")
    algorithms: List[Dict[str, Any]] = camera_algorithm_data.get("algorithms", [])

    create_camera(camera)

    logger.warning(f"Camera [{camera['ip']}] created successfully")

    create_camera_algorithms(camera, algorithms)


def check_connection(camera_data: Dict[str, str]) -> bool:
    try:
        response = Sender("add_camera", camera_data)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/add_camera") from e

    return response["status"]


def DeleteCamera(camera_instance: Camera) -> Dict[str, Any]:
    query_list_cameraalgorithms: Iterable[
        CameraAlgorithm
    ] = CameraAlgorithm.objects.filter(camera=camera_instance)

    for camera_algorithm in query_list_cameraalgorithms:
        pid: int = camera_algorithm.process_id
        stop_and_update_algorithm(pid)

    camera_id: int = camera_instance.id
    camera_instance.delete()

    return {
        "status": True,
        "message": f"Camera {camera_id} was successfully deleted.",
    }


def create_camera(camera: Dict[str, str]) -> None:
    ip: str = camera["ip"]
    name: str = camera["name"]
    username: str = camera["username"]
    password: str = camera["password"]

    camera_data: Dict[str, str] = {
        "id": ip,
        "name": name,
        "username": username,
        "password": password,
    }

    is_camera_exist: Iterable[Camera] = Camera.objects.filter(
        id=ip, name=name, username=username, password=password
    ).exists()
    if is_camera_exist:
        return

    if not check_connection({"ip": ip, "username": username, "password": password}):
        raise CameraConnectionError(ip)

    try:
        camera_obj_to_update: Camera = Camera.objects.get(id=ip)
    except Camera.DoesNotExist:
        Camera.objects.create(**camera_data, is_active=True)
        return
    else:
        camera_obj_to_update.name: str = name
        camera_obj_to_update.username: str = username
        camera_obj_to_update.password: str = password
        camera_obj_to_update.save()
        return


def create_camera_algorithms(
    camera: Dict[str, str], algorithms: List[Dict[str, Any]]
) -> None:
    camera_obj: Camera = Camera.objects.get(id=camera["ip"])

    algorithm_names: Set[str] = {algo["name"] for algo in algorithms}
    algo_to_delete: List[str] = get_algorithms_to_delete(camera_obj, algorithm_names)

    for algo in algo_to_delete:
        pid: int = CameraAlgorithm.objects.get(
            camera=camera_obj, algorithm__name=algo
        ).process_id
        stop_and_update_algorithm(pid)
        logger.warning(f"Successfully deleted pid {pid}")

    for algorithm in algorithms:
        algorithm_obj: Algorithm = Algorithm.objects.get(name=algorithm["name"])
        camera_algo_obj = CameraAlgorithm.objects.filter(
            algorithm=algorithm_obj, camera=camera_obj
        )

        algorithm_name: str = algorithm["name"]
        rtsp_link: str = camera_rtsp_link(camera_obj.id)

        data: List[Dict[str, Any]] = []
        areas: List[Dict[str, Any]] = []
        stelag: List[Dict[str, Any]] = []

        request: Dict[str, Any] = {
            "camera_url": rtsp_link,
            "algorithm": algorithm_obj.name,
            "image_name": algorithm_obj.image_name,
            "server_url": SERVER_URL,
            "link_reports": f"{SERVER_URL}:8000/api/reports/report-with-photos/",
            "extra": data,
        }

        zones: List[Optional[Dict[str, int]]] = algorithm.get("config", {}).get(
            "zonesID", []
        )

        is_similar: bool = compare_zones(
            algorithm_obj, camera_obj, algorithm.get("config", {}).get("zonesID", [])
        )

        if camera_algo_obj.exists() and is_similar:
            continue
        else:
            if camera_algo_obj.exists():
                pid: int = camera_algo_obj.get(
                    algorithm=algorithm_obj, camera=camera_obj
                ).process_id
                stop_and_update_algorithm(pid)
                logger.warning(
                    f"Successfully deleted -> {algorithm_name} with pid {pid}"
                )

        if algorithm_name == "min_max_control":
            algorithm_items: Iterable[Items] = Items.objects.filter(
                camera=camera_obj.id
            )
            for item in algorithm_items:
                areas.append(
                    {
                        "itemId": item.id,
                        "itemName": item.name,
                        "coords": item.coords,
                        "lowStockLevel": item.low_stock_level,
                        "task": item.object_type,
                    }
                )

            for zone_id in zones:
                zone_camera = ZoneCameras.objects.get(
                    id=zone_id["id"], camera=camera_obj
                )

                stelag.append(
                    {
                        "zoneId": zone_camera.id,
                        "zoneName": zone_camera.name,
                        "coords": zone_camera.coords,
                    }
                )

            new_data: Dict[str, Any] = {
                "areas": areas,
                "zones": stelag,
            }
            data.append(new_data)
            request["extra"] = data

        elif algorithm_name == "machine_control" or algorithm_name == "machine_control_js":
            logger.info("Starting machine control algorithm")
            for zone_id in zones:
                zone_camera: ZoneCameras = ZoneCameras.objects.get(
                    id=zone_id["id"], camera=camera_obj
                )
                coords: Dict[str, Any] = zone_camera.coords
                coords[0]["zoneId"] = zone_camera.id
                coords[0]["zoneName"] = zone_camera.name

                data.append([{"coords": coords}])

            if len(data) > 0:
                request["extra"] = data[0]
            else:
                request["extra"] = data

        elif algorithm_name == "operation_control":
            operation_control_id = algorithm["config"]["operation_control_id"]
            index_operations_obj = IndexOperations.objects.filter(camera=camera_obj)

            if (
                index_operations_obj.exists()
                and index_operations_obj.type_operation != operation_control_id
            ):
                index_operations_obj.type_operation = operation_control_id
                index_operations_obj.save()
                continue

            index_operation = IndexOperations(
                type_operation=operation_control_id, camera=camera_obj
            )
            IndexOperations.objects.filter(camera=camera_obj).delete()
            index_operation.save()

        else:
            # Runs for any custom algorithm
            for zone_id in zones:
                zone_camera: ZoneCameras = ZoneCameras.objects.get(
                    id=zone_id["id"], camera=camera_obj
                )
                coords: Dict[str, Any] = zone_camera.coords
                coords[0]["zoneId"] = zone_camera.id
                coords[0]["zoneName"] = zone_camera.name

                data.append([{"coords": coords}])

            if len(data) > 0:
                request["extra"] = data[0]
            else:
                request["extra"] = data

        logger.info(f"Starting {algorithm_name} algorithm")

        response: Dict[str, Any] = send_run_request(request)
        save_data(
            algorithm_obj=algorithm_obj,
            camera_obj=camera_obj,
            pid=response["pid"],
            zones=zones,
        )


def create_single_camera_algorithms(
    camera_data: Dict[str, str], algorithm_data: Dict[str, Any]
) -> None:
    camera_obj: Camera = Camera.objects.get(id=camera_data["ip"])
    algorithm_obj: Algorithm = Algorithm.objects.get(name=algorithm_data["name"])

    rtsp_link: str = camera_rtsp_link(camera_obj.id)

    data: List[Dict[str, Any]] = []
    areas: List[Dict[str, Any]] = []
    stelag: List[Dict[str, Any]] = []

    request: Dict[str, Any] = {
        "camera_url": rtsp_link,
        "algorithm": algorithm_obj.name,
        "image_name": algorithm_obj.image_name,
        "server_url": SERVER_URL,
        "link_reports": f"{SERVER_URL}:8000/api/reports/report-with-photos/",
        "extra": data,
    }

    zones: List[Optional[Dict[str, int]]] = algorithm_data.get("config", {}).get(
        "zonesID", []
    )

    algorithm_items: Iterable[Items] = Items.objects.filter(camera=camera_obj.id)
    for item in algorithm_items:
        areas.append(
            {
                "itemId": item.id,
                "itemName": item.name,
                "coords": item.coords,
                "lowStockLevel": item.low_stock_level,
                "task": item.object_type,
            }
        )

    for zone_id in zones:
        zone_camera = ZoneCameras.objects.get(id=zone_id["id"], camera=camera_obj)

        stelag.append(
            {
                "zoneId": zone_camera.id,
                "zoneName": zone_camera.name,
                "coords": zone_camera.coords,
            }
        )

    new_data: Dict[str, Any] = {
        "areas": areas,
        "zones": stelag,
    }
    data.append(new_data)
    request["extra"] = data

    response: Dict[str, Any] = send_run_request(request)
    logger.warning("Successfullyj")
    save_data(
        algorithm_obj=algorithm_obj,
        camera_obj=camera_obj,
        pid=response["pid"],
        zones=zones,
    )


def save_data(
    algorithm_obj: Algorithm,
    camera_obj: Camera,
    pid: int,
    zones: List[Dict[str, int]],
) -> None:
    new_record: CameraAlgorithm = CameraAlgorithm(
        algorithm=algorithm_obj,
        camera=camera_obj,
        process_id=pid,
        zones=zones,
    )
    new_record.save()

    if zones is not None:
        update_status_zones_true(zones)

    logger.warning(f"New record -> {algorithm_obj.name} on camera {camera_obj.id}")


def camera_rtsp_link(id: str) -> str:
    cameras_data = Camera.objects.get(id=id)
    return f"rtsp://{cameras_data.username}:{cameras_data.password}@{cameras_data.id}/h264_stream"


def get_algorithms_to_delete(camera_obj: Camera, algorithms: Set[str]) -> List[str]:
    existing_algorithms = CameraAlgorithm.objects.filter(camera=camera_obj)
    existing_algorithm_names = set(
        algorithm.algorithm.name for algorithm in existing_algorithms
    )

    if not algorithms:
        return existing_algorithm_names

    algorithms_to_delete = existing_algorithm_names - algorithms

    return algorithms_to_delete


def send_run_request(request: Dict[str, Any]) -> Dict[str, Any]:
    logger.warning(f"Request data for algorithm {request}")
    try:
        response = Sender("run", request)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/run") from e
    if not response["status"]:
        raise InvalidResponseError("/run", response["status"])

    return response


def stop_and_update_algorithm(pid: int) -> None:
    algo_name: str = CameraAlgorithm.objects.get(process_id=pid).algorithm.name
    camera_ip: str = CameraAlgorithm.objects.get(process_id=pid).camera.id

    if algo_name == "operation_control":
        IndexOperations.objects.filter(camera=camera_ip).delete()

    stop_camera_algorithm(pid)
    update_status_algorithm(pid)


def stop_camera_algorithm(pid: int) -> Dict[str, Any]:
    cstm_port = None
    algorithm_name = CameraAlgorithm.objects.get(process_id=pid).algorithm.name
    camera_id = CameraAlgorithm.objects.get(process_id=pid).camera.id

    try:
        response = Sender("stop", {"pid": pid}, cstm_port=cstm_port)
    except requests.exceptions.HTTPError as e:
        raise SenderError("/stop") from e

    logger.warning(
        f"[INFO] Stopping camera algorithm. Algorithm: {algorithm_name}, camera: {camera_id}, PID: {pid}"
    )
    logger.warning(response)
    if not response["status"]:
        CameraAlgorithm.objects.get(process_id=pid).delete()
        raise InvalidResponseError("/stop", response["status"])

    return response


def update_status_algorithm(pid: int):
    camera_algorithm = CameraAlgorithm.objects.filter(process_id=pid).first()
    if camera_algorithm:
        logs_service.delete_log(
            algorithm_name=camera_algorithm.algorithm.name,
            camera_ip=camera_algorithm.camera.id,
        )

        if camera_algorithm.zones is not None:
            update_status_zone_false(camera_algorithm.zones)

        camera_algorithm.delete()


def update_status_zone_false(data):
    """Update status zone in the end"""

    for zone in data:
        zone_id = zone.get("id")
        if zone_id:
            try:
                zone_obj = ZoneCameras.objects.get(id=zone_id)
                zone_obj.is_active = False
                zone_obj.save()
            except ZoneCameras.DoesNotExist:
                pass


def update_status_zones_true(zones):
    """Update status zones on True"""

    for zone in zones:
        zone_id = zone.get("id")
        if zone_id:
            try:
                zone_obj = ZoneCameras.objects.get(id=zone_id)
                zone_obj.is_active = True
                zone_obj.save()
            except ZoneCameras.DoesNotExist:
                pass


def compare_zones(
    algorithm_obj: Algorithm, camera_obj: Camera, zones: List[Optional[Dict[str, int]]]
) -> bool:
    if CameraAlgorithm.objects.filter(
        algorithm=algorithm_obj, camera=camera_obj
    ).exists():
        camera_algorithm = CameraAlgorithm.objects.get(
            algorithm=algorithm_obj, camera=camera_obj
        )
        saved_zones = camera_algorithm.zones
        if saved_zones == zones:
            return True
    return False
