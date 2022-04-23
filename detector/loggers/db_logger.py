from datetime import datetime

from detector.db import AnomalyLog, session_scope

from .base_logger import BaseAnomalyLogger


class DataBaseAnomalyLogger(BaseAnomalyLogger):
    def _log(self, log_data: str, dttm: datetime) -> None:
        with session_scope() as session:
            session.add(
                AnomalyLog(
                    dttm=dttm,
                    reason=log_data,
                )
            )

    def __str__(self) -> str:
        return "DataBaseAnomalyLogger"
