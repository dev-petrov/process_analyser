from datetime import datetime

from detector.db import AnomalyLog
from detector.loggers import DataBaseAnomalyLogger


def test_database_logger(db_session, log_data):
    logger = DataBaseAnomalyLogger()

    dttm = datetime.now()

    logger.log(log_data, dttm)

    assert db_session.query(AnomalyLog).count() == 1
    log = db_session.query(AnomalyLog).one()
    assert log.reason == str(log_data)
    assert log.dttm == dttm
    assert str(logger) == "DataBaseAnomalyLogger"
