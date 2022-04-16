from loggers.base_logger import BaseAnomalyLogger


class ConsoleAnomalyLogger(BaseAnomalyLogger):
    def _log(self, log_data: str) -> None:
        print(log_data)

    def __str__(self) -> str:
        return "ConsoleAnomalyLogger"
