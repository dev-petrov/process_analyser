import abc
import json
from datetime import datetime

from detector.algorythm import json_default


class BaseAnomalyLogger(abc.ABC):
    def get_message(self, data: dict) -> str:
        return json.dumps(data, indent=4, default=json_default)

    def log(self, data: dict, dttm: datetime) -> None:
        self._log(self.get_message(data), dttm)

    @abc.abstractmethod
    def _log(self, log_data: str, dttm: datetime) -> None:  # pragma: no cover
        pass
