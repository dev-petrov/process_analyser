from datetime import datetime
import sys

from .base_logger import BaseAnomalyLogger


class ConsoleAnomalyLogger(BaseAnomalyLogger):
    def _log(self, log_data: str, dttm: datetime) -> None:
        print(dttm, log_data)

    def __str__(self) -> str:
        return "ConsoleAnomalyLogger"
