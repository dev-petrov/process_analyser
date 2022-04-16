from datetime import datetime

from db import AnomalyLog, session_scope
from loggers.base_logger import BaseAnomalyLogger


class DataBaseAnomalyLogger(BaseAnomalyLogger):
    def _log(self, log_data: str) -> None:
        with session_scope() as session:
            session.add(
                AnomalyLog(
                    dttm=datetime.now(),
                    reason=log_data,
                )
            )

    def __str__(self) -> str:
        return "DataBaseAnomalyLogger"
