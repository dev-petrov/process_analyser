from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import distinct, func, literal_column
from sqlalchemy.orm import Query, Session

from detector.db import BaseRawValue, RawCleanedValue, RawValue, session_scope

from .aggregation_settings import AGGREGATION_SETTINGS, AggregationSetting


class Aggregator:
    period_length = 10
    aggregation_settings: AggregationSetting = AGGREGATION_SETTINGS

    def get_train_data(self) -> pd.DataFrame:
        with session_scope() as session:
            dttms = list(
                map(
                    lambda x: x["unique_dttm"],
                    session.query(distinct(RawCleanedValue.dttm).label("unique_dttm")).order_by("unique_dttm").all(),
                )
            )
            return pd.DataFrame(
                [
                    self._get_aggregate_query(dttm, session, RawCleanedValue).first()
                    for dttm in dttms[self.period_length :]  # noqa: E203
                ]
            )

    def _get_aggregate_query(self, dttm: datetime, session: Session, raw_value_cls: BaseRawValue) -> Query:
        dttm_from = dttm - timedelta(minutes=self.period_length) + timedelta(seconds=2)
        dttm_to = dttm
        average_fields = ["cpu_percent", "memory_percent", "num_threads", "connections", "open_files"]
        groupped_processes_qs = (
            session.query(
                raw_value_cls.username,
                *[func.avg(getattr(raw_value_cls, field)).label(field) for field in average_fields],
                func.max(raw_value_cls.dttm).label("max_dttm"),
                func.string_agg(raw_value_cls.status, literal_column("','")).label("status"),
            )
            .filter(
                raw_value_cls.dttm > dttm_from,
                raw_value_cls.dttm <= dttm_to,
            )
            .group_by("pid", "username")
            .subquery()
        )
        aggregation_settings = [
            getattr(func, simple_agg.func_name)(getattr(groupped_processes_qs.c, field)).label(
                f"{field}_{simple_agg.func_name}"
            )
            for simple_agg in self.aggregation_settings.simple_agg
            for field in simple_agg.fields
        ] + [
            custom_agg.func(groupped_processes_qs.c).label(custom_agg.label)
            for custom_agg in self.aggregation_settings.custom_agg
        ]
        return session.query(*aggregation_settings)

    def get_detect_data(self, dttm: datetime) -> pd.DataFrame:
        with session_scope() as session:
            return pd.DataFrame(self._get_aggregate_query(dttm, session, RawValue).all())
