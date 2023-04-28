import math
from typing import Any, Dict

import requests

from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from src.Algorithms.utils import yolo_proccesing


class OrderViewPaginnator(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        page_size = self.get_page_size(self.request)
        all_page_count = math.ceil(count / page_size)

        return Response(
            OrderedDict(
                [
                    ("count", count),
                    ("current_page", self.page.number),
                    ("records_on_page", page_size),
                    ("all_page_count", all_page_count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


def get_skany_video_info(time, camera_ip):
    server_host = yolo_proccesing.get_algorithm_url()
    video_chacker_host = f"{server_host}:3456/is_video_available/"

    response = {
        "camera_ip": camera_ip,
        "time": time,
    }
    try:
        request = requests.post(
            url=f"{video_chacker_host}:3456/is_video_available/",
            json=response,
        )
    except Exception:
        return None
    else:
        result = request.json()["camera_ip"] = camera_ip

    return result
