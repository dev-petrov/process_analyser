import json
from datetime import datetime

from detector.loggers import FileAnomalyLogger


def test_file_logger(mocker, log_data, patched_file_reader):
    filename = "some_file.txt"
    logger = FileAnomalyLogger(filename)

    patcher_file_reader, patched_file = patched_file_reader
    patched_open = mocker.patch("detector.loggers.file_logger.open", return_value=patcher_file_reader)

    dttm = datetime.now()

    logger.log(log_data, dttm)
    patched_open.assert_called_once_with(filename, "a")
    patched_file.write.assert_called_once_with(f"{dttm}: {json.dumps(log_data, indent=4)}")

    assert str(logger) == f"FileAnomalyLogger, filename: {filename}"

    patched_open.reset_mock()
    patched_file.reset_mock()

    logger = FileAnomalyLogger(None)
    assert logger._file_name == "anomaly_logger.log"
    logger.log(log_data, dttm)
    patched_open.assert_called_once_with("anomaly_logger.log", "a")
    patched_file.write.assert_called_once_with(f"{dttm}: {json.dumps(log_data, indent=4)}")

    assert str(logger) == "FileAnomalyLogger, filename: anomaly_logger.log"
