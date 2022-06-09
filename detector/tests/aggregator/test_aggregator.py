from datetime import datetime

from sqlalchemy import and_, case, func

from detector.aggregator import Aggregator
from detector.aggregator.aggregation_settings import AggregationSetting, CustomAggregation, SimpleAggregation
from detector.db import extract_time


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
        custom_agg=[
            CustomAggregation(
                "time_of_day",
                lambda x: case(
                    [
                        (
                            and_(
                                extract_time(func.max(x.max_dttm)) >= "00:00:00",
                                extract_time(func.max(x.max_dttm)) < "06:00:00",
                            ),
                            0,
                        ),
                        (
                            and_(
                                extract_time(func.max(x.max_dttm)) >= "06:00:00",
                                extract_time(func.max(x.max_dttm)) < "12:00:00",
                            ),
                            1,
                        ),
                        (
                            and_(
                                extract_time(func.max(x.max_dttm)) >= "12:00:00",
                                extract_time(func.max(x.max_dttm)) < "18:00:00",
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
