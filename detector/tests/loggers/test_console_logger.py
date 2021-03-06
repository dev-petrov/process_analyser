import json
from datetime import datetime

from detector.loggers import ConsoleAnomalyLogger


def test_console_logger(mocker, log_data):
    logger = ConsoleAnomalyLogger()

    patched_print = mocker.patch("detector.loggers.console_logger.print")

    dttm = datetime.now()

    logger.log(log_data, dttm)

    patched_print.assert_called_once_with(dttm, json.dumps(log_data, indent=4))

    assert str(logger) == "ConsoleAnomalyLogger"
