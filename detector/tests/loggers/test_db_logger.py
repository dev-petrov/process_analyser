from detector.db import AnomalyLog
from detector.loggers import DataBaseAnomalyLogger


def test_database_logger(db_session, log_data):
    logger = DataBaseAnomalyLogger()

    logger.log(log_data)

    assert db_session.query(AnomalyLog).count() == 1
    log = db_session.query(AnomalyLog).one()
    assert log.reason == str(log_data)
    assert str(logger) == "DataBaseAnomalyLogger"
