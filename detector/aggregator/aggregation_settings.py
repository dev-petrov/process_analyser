from dataclasses import dataclass
from typing import Callable

from sqlalchemy import Time, and_, case, cast, func


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
            ("cpu_percent", "memory_percent", "num_threads", "connections", "open_files"),
        ),
        SimpleAggregation(
            "sum",
            ("num_threads", "connections", "open_files", "cpu_percent", "memory_percent"),
        ),
        SimpleAggregation(
            "max",
            ("cpu_percent", "connections", "memory_percent", "open_files"),
        ),
    ],
    custom_agg=[
        CustomAggregation(
            "idle_status_count",
            lambda x: func.count(x.status).filter(x.status == "idle"),
        ),
        CustomAggregation(
            "sleeping_status_count",
            lambda x: func.count(x.status).filter(x.status == "sleeping"),
        ),
        CustomAggregation(
            "root_processes_count",
            lambda x: func.count(x.username).filter(x.username == "root"),
        ),
        CustomAggregation(
            "time_of_day",
            lambda x: case(
                [
                    (and_(cast(func.max(x.dttm), Time) >= "00:00:00", cast(func.max(x.dttm), Time) < "06:00:00"), 0),
                    (and_(cast(func.max(x.dttm), Time) >= "06:00:00", cast(func.max(x.dttm), Time) < "12:00:00"), 1),
                    (and_(cast(func.max(x.dttm), Time) >= "12:00:00", cast(func.max(x.dttm), Time) < "18:00:00"), 2),
                ],
                else_=3,
            ),
        ),
    ],
    qualitatives=["time_of_day"],
)

# CustomAggregation(
#     "idle_status_count_distinct",
#     lambda x: func.count(distinct(x.pid)).filter(x.status == "idle"),
# ),
# CustomAggregation(
#     "running_status_count",
#     lambda x: func.count(x.status).filter(x.status == "running"),
# ),
# CustomAggregation(
#     "running_status_count_distinct",
#     lambda x: func.count(distinct(x.pid)).filter(x.status == "running"),
# ),
# CustomAggregation(
#     "sleeping_status_count_distinct",
#     lambda x: func.count(distinct(x.pid)).filter(x.status == "sleeping"),
# ),
# CustomAggregation(
#     "root_processes_count_distinct",
#     lambda x: func.count(distinct(x.pid)).filter(x.username == "root"),
# ),
# {
#     "simple_agg": [
#         ("avg", ("cpu_percent", "memory_percent", "num_threads", "connections", "open_files")),  # nice
#         ("sum", ("num_threads", "connections", "open_files")),
#         # ('min', ('connections', 'open_files')), # cpu_percent, memory_percent, num_threads, nice
#         ("max", ("cpu_percent", "connections")),  # memory_percent, num_threads, nice, open_files_max
#     ],
#     "custom_agg": [
#         # ('zombie_status_count', lambda x: func.count(x.status).filter(x.status == 'zombie')),
#         # ('zombie_status_count_distinct', lambda x: func.count(distinct(x.pid)).filter(x.status == 'zombie')),
#         # ('disk_sleep_status_count', lambda x: func.count(x.status).filter(x.status == 'disk_sleep')),
#         # ('disk_sleep_status_count_distinct',
# lambda x: func.count(distinct(x.pid)).filter(x.status == 'disk_sleep')),
#         # ('system_processes_count', lambda x: func.count(x.username).filter(x.username.startswith('system'))),
#         # ('system_processes_count_distinct', lambda x: func.count(distinct(x.pid))
# .filter(x.username.startswith('system'))),
#     ],
# }
