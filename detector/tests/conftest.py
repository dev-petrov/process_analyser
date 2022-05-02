import sys

import pytest
from pytest_factoryboy import register
from sqlalchemy_utils import create_database, database_exists, drop_database

from detector.db import Base, Session, get_engine
from detector.settings import DB_NAME, DB_PREFIX
from detector.tests.factories import ProcessInfoFactory, RawValueCleanedFactory, RawValueFactory

register(ProcessInfoFactory)
register(RawValueCleanedFactory)
register(RawValueFactory)


@pytest.fixture(scope="session")
def db_connection():  # pragma: no cover
    if "sqlite" in DB_PREFIX:
        engine = get_engine(test=True)
        yield engine.connect()
    else:
        db_name = f"{DB_NAME}_test"
        sys.stdout.write(f"Creating test database {db_name}")
        engine = get_engine(test=True, name=db_name)
        if database_exists(engine.url):  # pragma: no cover
            answer = input(f"Database {db_name} already exists. Destroy? y/N: ")
            if answer == "y":
                drop_database(engine.url)
            else:
                sys.exit(0)
        create_database(engine.url)
        yield engine.connect()

        sys.stdout.write(f"Destroying test database {db_name}")
        drop_database(engine.url)


@pytest.fixture(scope="session")
def setup_database(db_connection):
    Session.configure(bind=db_connection)
    Base.metadata.create_all(db_connection)


@pytest.fixture
def db_session(setup_database, db_connection):
    session = Session()
    transaction = db_connection.begin()
    yield session
    transaction.rollback()
    Session.remove()


@pytest.fixture
def patched_file_reader(mocker):
    patched_file = mocker.MagicMock()
    patcher_file_reader = mocker.MagicMock()
    patcher_file_reader.__enter__.return_value = patched_file
    return patcher_file_reader, patched_file


@pytest.fixture(autouse=True)
def setup_session(db_session, raw_value_cleaned_factory, raw_value_factory):
    raw_value_cleaned_factory._meta.sqlalchemy_session = db_session
    raw_value_factory._meta.sqlalchemy_session = db_session
