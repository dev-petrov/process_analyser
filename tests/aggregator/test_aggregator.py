from datetime import datetime

from sqlalchemy import Time, and_, case, cast, func

from aggregator import Aggregator
from aggregator.aggregation_settings import AggregationSetting, CustomAggregation, SimpleAggregation
from settings import DB_TEST_TYPE

SQLITE_SETTINGS = CustomAggregation(
    "time_of_day",
    lambda x: case(
        [
            (
                and_(func.TIME(func.max(x.dttm)) >= "00:00:00", func.TIME(func.max(x.dttm)) < "06:00:00"),
                0,
            ),
            (
                and_(func.TIME(func.max(x.dttm)) >= "06:00:00", func.TIME(func.max(x.dttm)) < "12:00:00"),
                1,
            ),
            (
                and_(func.TIME(func.max(x.dttm)) >= "12:00:00", func.TIME(func.max(x.dttm)) < "18:00:00"),
                2,
            ),
        ],
        else_=3,
    ),
)

PG_SETTINGS = CustomAggregation(
    "time_of_day",
    lambda x: case(
        [
            (and_(cast(func.max(x.dttm), Time) >= "00:00:00", cast(func.max(x.dttm), Time) < "06:00:00"), 0),
            (and_(cast(func.max(x.dttm), Time) >= "06:00:00", cast(func.max(x.dttm), Time) < "12:00:00"), 1),
            (and_(cast(func.max(x.dttm), Time) >= "12:00:00", cast(func.max(x.dttm), Time) < "18:00:00"), 2),
        ],
        else_=3,
    ),
)


def test_aggregator(db_session, raw_value_cleaned_factory, raw_value_factory):
    data = [
        (datetime(2022, 4, 15, 10), ((0.2, 0.3), (0.1, 0.1))),
        (datetime(2022, 4, 15, 10, 1), ((0.2, 0.3), (0.1, 0.1))),
        (datetime(2022, 4, 15, 10, 2), ((0.2, 0.3), (0.1, 0.1))),
        (datetime(2022, 4, 15, 10, 3), ((0.2, 0.3), (0.1, 0.1))),
        (datetime(2022, 4, 15, 14), ((0.2, 0.3), (0.1, 0.1))),
        (datetime(2022, 4, 15, 20), ((0.2, 0.3), (0.1, 0.1))),
        (datetime(2022, 4, 16, 3), ((0.2, 0.3), (0.1, 0.1))),
    ]

    for dttm, processes in data:
        for cpu, mem in processes:
            raw_value_cleaned_factory(dttm=dttm, cpu_percent=cpu, memory_percent=mem)
            raw_value_factory(dttm=dttm, cpu_percent=cpu, memory_percent=mem)

    aggregator = Aggregator()

    aggregator.period_length = 2
    aggregator.aggregation_settings = AggregationSetting(
        simple_agg=[
            SimpleAggregation(
                "sum",
                ["cpu_percent", "memory_percent"],
            ),
        ],
        custom_agg=[PG_SETTINGS if DB_TEST_TYPE == "postgres" else SQLITE_SETTINGS],
        qualitatives=["time_of_day"],
    )

    data = aggregator.get_train_data()

    assert data.values.round(1).tolist() == [
        [0.6, 0.8, 1],
        [0.6, 0.8, 1],
        [0.3, 0.4, 2],
        [0.3, 0.4, 3],
        [0.3, 0.4, 0],
    ]

    data = aggregator.get_detect_data(datetime(2022, 4, 15, 10, 1))
    assert data.values.round(1).tolist() == [[0.6, 0.8, 1]]
