from loggers import ConsoleAnomalyLogger


def test_console_logger(mocker, log_data):
    logger = ConsoleAnomalyLogger()

    patched_print = mocker.patch("loggers.console_logger.print")

    logger.log(log_data)

    patched_print.assert_called_once_with(str(log_data))

    assert str(logger) == "ConsoleAnomalyLogger"
