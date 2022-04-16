import pandas as pd

from collectors.base_collector import BaseCollector
from db import BaseRawValue, session_scope


class DBCollector(BaseCollector):
    _db_cls: BaseRawValue

    def __init__(self, raw_value_cls: BaseRawValue, *args, **kwargs) -> None:
        self._db_cls = raw_value_cls
        super().__init__(*args, **kwargs)

    def _collect(self, data: pd.DataFrame) -> None:
        with session_scope() as session:
            data.dttm = pd.to_datetime(data.dttm, unit="s")
            data.create_time = pd.to_datetime(data.create_time, unit="s")
            session.add_all([self._db_cls(**kwargs) for kwargs in data.to_dict("records")])

    def __str__(self) -> str:
        return "DBCollector"
