from datetime import datetime

from detector.loggers import ConsoleAnomalyLogger


def test_console_logger(mocker, log_data):
    logger = ConsoleAnomalyLogger()

    patched_sys = mocker.patch("detector.loggers.console_logger.sys")

    dttm = datetime.now()

    logger.log(log_data, dttm)

    patched_sys.stdout.write.assert_called_once_with(dttm, str(log_data))

    assert str(logger) == "ConsoleAnomalyLogger"
