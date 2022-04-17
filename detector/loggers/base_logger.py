import abc


class BaseAnomalyLogger(abc.ABC):
    def get_message(self, data: dict) -> str:
        return str(data)

    def log(self, data: dict) -> None:
        self._log(self.get_message(data))

    @abc.abstractmethod
    def _log(self, log_data: str) -> None:  # pragma: no cover
        pass
