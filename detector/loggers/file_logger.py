from .base_logger import BaseAnomalyLogger


class FileAnomalyLogger(BaseAnomalyLogger):
    _file_name: str

    def __init__(self, file_name: str) -> None:
        if not file_name:
            file_name = "anomaly_logger.log"
        self._file_name = file_name

    def _log(self, log_data: str) -> None:
        with open(self._file_name, "a") as file:
            file.write(log_data)

    def __str__(self) -> str:
        return f"FileAnomalyLogger, filename: {self._file_name}"
