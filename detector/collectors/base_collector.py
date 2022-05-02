import abc
from datetime import datetime, timedelta
import sys

import pandas as pd
from pytz.reference import LocalTimezone


class BaseCollector(abc.ABC):
    _verbose: bool
    _tz_offset: timedelta

    def __init__(self, verbose=False) -> None:
        self._verbose = verbose
        self._tz_offset = timedelta(seconds=LocalTimezone().utcoffset(datetime.now()).seconds)

    @abc.abstractmethod
    def _collect(self, data: pd.DataFrame) -> None:  # pragma: no cover
        pass

    def collect(self, data: pd.DataFrame) -> None:
        dttm = datetime.now()
        self._collect(data)

        if self._verbose:  # pragma: no cover
            print(f"{dttm + self._tz_offset}: Collected {len(data)} rows")
