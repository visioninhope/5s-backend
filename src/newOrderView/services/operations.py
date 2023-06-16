from typing import Iterable, List, Any, Tuple, Dict
from datetime import datetime, timedelta
import logging
import pytz

import pyodbc

from django.db.models import Q
from django.contrib.postgres.fields import JSONField
from django.db.models.query import QuerySet

from src.CameraAlgorithms.models.camera import Camera, ZoneCameras
from src.MsSqlConnector.connector import connector as connector_service
from src.Reports.models import Report

from ..utils import add_ms, convert_to_gmt0, convert_to_unix

logger = logging.getLogger(__name__)


class OperationServices:
    @staticmethod
    def get_operations(from_date: str, to_date: str) -> List[Dict[str, Any]]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        stanowiska_query: str = """
            SELECT
                indeks AS id,
                raport AS orderId
            FROM Stanowiska
        """

        stanowiska_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=stanowiska_query
        )

        result_list: List[Dict[str, Any]] = []

        for row in stanowiska_data:
            operation_id: int = row[0]
            operation_name: str = row[1]

            operations_query: str = """
                SELECT
                    sk.indeks AS id,
                    sk.data AS startTime,
                    LEAD(sk.data) OVER (ORDER BY sk.data) AS endTime,
                    z.zlecenie AS orderId
                FROM Skany sk
                    JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                    JOIN zlecenia z ON sz.indekszlecenia = z.indeks
                WHERE sk.stanowisko = ?
            """

            params: List[Any] = [operation_id]

            if from_date and to_date:
                operations_query += " AND sk.data >= ? AND sk.data <= ?"

                from_date_dt: datetime = datetime.strptime(from_date, "%Y-%m-%d")
                from_date_dt: datetime = from_date_dt + timedelta(microseconds=1)

                to_date_dt: datetime = datetime.strptime(to_date, "%Y-%m-%d")
                to_date_dt: datetime = (
                    to_date_dt + timedelta(days=1) - timedelta(microseconds=1)
                )

                params.extend([from_date_dt, to_date_dt])

            operations_query += " ORDER BY sk.data"

            operations_data: List[Tuple[Any]] = connector_service.executer(
                connection=connection, query=operations_query, params=params
            )

            operations_list: List[Dict[str, Any]] = []

            if not operations_data:
                continue

            for i in range(len(operations_data)):
                operation_row: Tuple[Any] = operations_data[i]

                id: int = operation_row[0]
                orderId: str = operation_row[3].strip()
                startTime: str = str(operation_row[1])
                endTime: str = (
                    str(operation_row[2]) if i < len(operations_data) - 1 else None
                )

                operation: Dict[str, Any] = {
                    "id": id,
                    "orId": orderId,
                    "sTime": startTime,
                    "eTime": endTime,
                }

                startTime_dt: datetime = add_ms(startTime)
                startTime_dt: datetime = convert_to_gmt0(startTime_dt)
                startTime_unix: int = convert_to_unix(startTime_dt)

                operation["sTime"] = startTime_unix

                if endTime is not None:
                    endTime_dt: datetime = add_ms(endTime)
                    endTime_dt = endTime_dt.astimezone(pytz.utc)

                    if endTime_dt.date() > startTime_dt.date():
                        endTime_dt = startTime_dt + timedelta(hours=1)
                    else:
                        endTime_dt = endTime_dt or startTime_dt + timedelta(hours=1)

                    endTime_dt: datetime = convert_to_gmt0(endTime_dt)
                    endTime_unix: int = convert_to_unix(endTime_dt)

                    operation["eTime"] = endTime_unix
                else:
                    endTime_dt = startTime_dt + timedelta(hours=1)

                    endTime_dt: datetime = convert_to_gmt0(endTime_dt)
                    endTime_unix: int = convert_to_unix(endTime_dt)

                    operation["eTime"] = endTime_unix

                operations_list.append(operation)

            # Machine Control

            zone_cameras_ids: Iterable[int] = ZoneCameras.objects.filter(
                index_workplace=operation_id
            ).values_list("id", flat=True)
            zone_cameras_ids: List[int] = [
                JSONField().to_python(id) for id in zone_cameras_ids
            ]

            reports_with_matching_zona_id: Iterable[QuerySet[Report]] = Report.objects.filter(
                Q(algorithm=3) & Q(extra__has_key="zoneId")
            )

            print(reports_with_matching_zona_id)

            for zone_camera_id in zone_cameras_ids:
                zone_reports: Iterable[QuerySet[Report]] = reports_with_matching_zona_id.filter(
                    Q(extra__zoneId__exact=zone_camera_id)
                )

                print(zone_camera_id)
                print(zone_reports)

                reports: List[Dict[str, Any]] = []

                for report in zone_reports:
                    zone_data: Dict[str, Any] = report.extra
                    camera_ip: str = report.camera.id

                    zone_id: int = zone_data["zoneId"]
                    zone_name: str = zone_data["zoneName"]

                    machine_control_report_id: int = report.id

                    start_tracking: str = report.start_tracking
                    stop_tracking: str = report.stop_tracking

                    sTime: int = int(
                        datetime.strptime(
                            start_tracking, "%Y-%m-%d %H:%M:%S.%f"
                        ).timestamp()
                    )
                    eTime: int = int(
                        datetime.strptime(stop_tracking, "%Y-%m-%d %H:%M:%S.%f").timestamp()
                    )

                    report_data: Dict[str, Any] = {
                        "zoneId": machine_control_report_id,
                        "orId": zone_name,
                        "camera": camera_ip,
                        "sTime": sTime * 1000,
                        "eTime": eTime * 1000,
                    }

                    reports.append(report_data)

                machine_result: Dict[str, Any] = {
                    "oprTypeID": zone_id,
                    "inverse": True,
                    "oprName": zone_name,
                    "oprs": reports,
                }

                result_list.append(machine_result)

            operation_result = {
                "oprTypeID": operation_id,
                "inverse": False,
                "oprName": operation_name,
                "oprs": operations_list,
            }

            result_list.append(operation_result)

        return result_list

    @staticmethod
    def get_whnet_operation() -> List[Dict[str, Any]]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        query: str = """
            SELECT
                indeks AS id,
                raport AS operationName
            FROM Stanowiska
        """

        data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=query
        )
        result_list: List[Dict[str, Any]] = []

        for order_row in data:
            order: Dict[str, Any] = {
                "id": int(order_row[0]),
                "operationName": str(order_row[1]).strip(),
            }

            result_list.append(order)

        return result_list
