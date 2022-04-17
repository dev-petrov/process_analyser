from detector.collectors import DBCollector
from detector.db import RawCleanedValue, RawValue


def test_db_collector(db_session, processes_data):
    dttm, data = processes_data

    collector = DBCollector(RawCleanedValue)
    collector.collect(data)

    assert db_session.query(RawCleanedValue).count() == 10
    assert db_session.query(RawValue).count() == 0

    collector = DBCollector(RawValue)
    collector.collect(data)

    assert db_session.query(RawValue).count() == 10
    assert db_session.query(RawCleanedValue).count() == 10

    assert str(collector) == "DBCollector"
