import abc
from datetime import datetime


class BaseAnomalyLogger(abc.ABC):
    def get_message(self, data: dict) -> str:
        return str(data)

    def log(self, data: dict, dttm: datetime) -> None:
        self._log(self.get_message(data), dttm)

    @abc.abstractmethod
    def _log(self, log_data: str, dttm: datetime) -> None:  # pragma: no cover
        pass
