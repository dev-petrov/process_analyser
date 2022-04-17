from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass
class AnomalyExceptionDetail:
    count: int
    details: Iterable[pd.Series]


class AnomalyException(BaseException):
    detail: AnomalyExceptionDetail

    def __init__(self, anomalies: Iterable[pd.Series]):
        self.detail = AnomalyExceptionDetail(
            count=len(anomalies),
            details=anomalies,
        )
