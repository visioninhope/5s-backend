from collections import defaultdict
from typing import List, Any, Tuple, Dict, Optional
from datetime import datetime, timedelta
import logging

import pyodbc

from src.Core.types import Query
from src.MsSqlConnector.connector import connector as connector_service
from src.CameraAlgorithms.models import Camera
from src.Reports.models import SkanyReport
from src.OrderView.models import IndexOperations
from src.OrderView.utils import get_skany_video_info
from src.newOrderView.utils import convert_to_gmt0, convert_to_unix, calculate_duration

logger = logging.getLogger(__name__)


class OrderServices:
    @staticmethod
    def get_order(from_date: str, to_date: str) -> List[Dict[str, Any]]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        order_query: Query = """
            SELECT
                sk.indeks AS id,
                z.zlecenie AS orderId,
                sk.data AS startTime,
                LEAD(sk.data) OVER (ORDER BY sk.data) AS endTime
            FROM Skany sk
                JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                JOIN zlecenia z ON sz.indekszlecenia = z.indeks
            WHERE sk.data >= ? AND sk.data <= ?
        """

        if from_date and to_date:
            from_date_dt: datetime = datetime.strptime(from_date, "%Y-%m-%d")
            from_date_dt: datetime = from_date_dt + timedelta(microseconds=1)

            to_date_dt: datetime = datetime.strptime(to_date, "%Y-%m-%d")
            to_date_dt: datetime = (
                to_date_dt + timedelta(days=1) - timedelta(microseconds=1)
            )

        params: List[Any] = [from_date_dt, to_date_dt]

        order_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_query, params=params
        )

        result_dict: Dict[str, int] = defaultdict(int)

        for order_row in order_data:
            order_id: str = order_row[1].strip()
            startTime: datetime = order_row[2]
            endTime: Optional[datetime] = order_row[3]

            if endTime is not None:
                if endTime.date() > startTime.date():
                    endTime: datetime = startTime + timedelta(hours=1)
                else:
                    endTime: datetime = endTime or startTime + timedelta(hours=1)

            else:
                endTime: datetime = startTime + timedelta(hours=1)

            duration: int = calculate_duration(startTime, endTime)

            result_dict[order_id] += duration

        result_list: List[Dict[str, Any]] = [
            {"orId": order_id, "duration": duration}
            for order_id, duration in result_dict.items()
        ]

        return result_list

    @staticmethod
    def get_order_by_details(operation_id: int) -> Dict[str, Any]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        order_query: Query = """
            WITH Operation AS (
                SELECT
                    sk.data AS operationTime
                FROM Skany sk
                    JOIN Stanowiska st ON sk.stanowisko = st.indeks
                WHERE sk.indeks = ?
            )
            SELECT
                z.indeks AS id,
                z.zlecenie AS orderId,
                st.raport AS operationName,
                u.imie AS firstName,
                u.nazwisko AS lastName,
                CONVERT(VARCHAR(23), op.operationTime, 121) AS startTime,
                CASE
                    WHEN DATEPART(year, sk_next.data) > DATEPART(year, op.operationTime)
                        OR DATEPART(month, sk_next.data) > DATEPART(month, op.operationTime)
                        OR DATEPART(day, sk_next.data) > DATEPART(day, op.operationTime)
                        THEN DATEADD(hour, 1, op.operationTime)
                    ELSE CONVERT(VARCHAR(23), sk_next.data, 121)
                END AS endTime,
                st.indeks AS workplaceID,
                sk.indeks AS operationID,
                z.typ AS type
            FROM Zlecenia z
                JOIN Skany_vs_Zlecenia sz ON z.indeks = sz.indekszlecenia
                JOIN Skany sk ON sz.indeksskanu = sk.indeks
                JOIN Stanowiska st ON sk.stanowisko = st.indeks
                JOIN Uzytkownicy u ON sk.uzytkownik = u.indeks
                JOIN Operation op ON op.operationTime = sk.data
                LEFT JOIN Skany sk_next ON sk_next.data > op.operationTime
                                        AND sk_next.stanowisko = st.indeks
            WHERE sk.indeks = ?
        """

        params: List[Any] = [operation_id, operation_id]

        order_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_query, params=params
        )

        if order_data:
            id: int = order_data[0][8]
            orderId: str = order_data[0][1].strip()
            operationName: str = order_data[0][2]
            firstName: str = order_data[0][3]
            lastName: str = order_data[0][4]
            startTime: datetime = datetime.strptime(
                str(order_data[0][5]), "%Y-%m-%d %H:%M:%S.%f"
            )
            endTime_str: Optional[str] = str(order_data[0][6]) if order_data[0][6] else None

            if endTime_str:
                if "." not in endTime_str:
                    endTime_str += ".000"
                endTime = datetime.strptime(endTime_str, "%Y-%m-%d %H:%M:%S.%f")
            else:
                endTime = startTime + timedelta(hours=1)

            workplaceID: int = order_data[0][7]
            elementType: str = order_data[0][9]
            video_data: Optional[Dict[str, Any]] = None

            if startTime is not None:
                camera_obj: Optional[Camera] = None
                operation_status: Optional[bool] = None
                video_data: Dict[str, bool] = {}

                skany_report: Optional[SkanyReport] = SkanyReport.objects.filter(
                    skany_index=id
                ).first()
                camera_obj: Optional[Camera] = IndexOperations.objects.filter(
                    type_operation=workplaceID
                ).first()

                if skany_report:
                    operation_status: Optional[bool] = skany_report.violation_found
                    video_time: Optional[bool] = skany_report.start_time
                    video_time_unix: int = convert_to_unix(video_time)

                    if camera_obj and video_time:
                        video_data: Dict[str, Any] = get_skany_video_info(
                            time=(video_time_unix), camera_ip=camera_obj.camera.id
                        )

            startTime: datetime = convert_to_gmt0(startTime)
            endTime: datetime = convert_to_gmt0(endTime)

            startTime_unix: int = convert_to_unix(startTime)
            endTime_unix: int = convert_to_unix(endTime)

            result: Dict[str, Any] = {
                "id": id,
                "orId": orderId,
                "oprName": operationName,
                "elType": elementType,
                "sTime": startTime_unix,
                "eTime": endTime_unix,
                "frsName": firstName,
                "lstName": lastName,
                "status": operation_status,
                "video": video_data,
            }

            return result
        else:
            return {}
