from dataclasses import dataclass
from typing import Callable

from sqlalchemy import and_, case, func

from detector.db import extract_time


@dataclass
class SimpleAggregation:
    func_name: str
    fields: tuple[str]


@dataclass
class CustomAggregation:
    label: str
    func: Callable


@dataclass
class AggregationSetting:
    simple_agg: list[SimpleAggregation]
    custom_agg: list[CustomAggregation]
    qualitatives: list[str]


AGGREGATION_SETTINGS = AggregationSetting(
    simple_agg=[
        SimpleAggregation(
            "avg",
            ("cpu_percent", "memory_percent", "num_threads"),
        ),
        SimpleAggregation(
            "sum",
            ("cpu_percent", "memory_percent", "num_threads", "connections", "open_files"),
        ),
        SimpleAggregation(
            "max",
            ("cpu_percent", "memory_percent", "num_threads", "connections", "open_files"),
        ),
    ],
    custom_agg=[
        CustomAggregation(
            "connections_avg",
            lambda x: func.avg(x.connections).filter(x.connections != 0),
        ),
        CustomAggregation(
            "open_files_avg",
            lambda x: func.avg(x.open_files).filter(x.open_files != 0),
        ),
        CustomAggregation(
            "idle_status_count",
            lambda x: func.count(x.status).filter(x.status.contains("idle")),
        ),
        CustomAggregation(
            "sleeping_status_count",
            lambda x: func.count(x.status).filter(x.status.contains("sleeping")),
        ),
        CustomAggregation(
            "running_status_count",
            lambda x: func.count(x.status).filter(x.status.contains("running")),
        ),
        CustomAggregation(
            "zombie_status_count",
            lambda x: func.count(x.status).filter(x.status.contains("zombie")),
        ),
        CustomAggregation(
            "disk_sleep_status_count",
            lambda x: func.count(x.status).filter(x.status.contains("disk_sleep")),
        ),
        CustomAggregation(
            "root_processes_count",
            lambda x: func.count(x.username).filter(x.username == "root"),
        ),
        CustomAggregation(
            "system_processes_count",
            lambda x: func.count(x.username).filter(x.username.startswith("sys")),
        ),
        CustomAggregation(
            "time_of_day",
            lambda x: case(
                [
                    (
                        and_(
                            extract_time(func.max(x.dttm)) >= "00:00:00",
                            extract_time(func.max(x.dttm)) < "06:00:00",
                        ),
                        0,
                    ),
                    (
                        and_(
                            extract_time(func.max(x.dttm)) >= "06:00:00",
                            extract_time(func.max(x.dttm)) < "12:00:00",
                        ),
                        1,
                    ),
                    (
                        and_(
                            extract_time(func.max(x.dttm)) >= "12:00:00",
                            extract_time(func.max(x.dttm)) < "18:00:00",
                        ),
                        2,
                    ),
                ],
                else_=3,
            ),
        ),
    ],
    qualitatives=["time_of_day"],
)
