import sys

import pytest
from pytest_factoryboy import register
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from db import Base, Session
from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_TEST_TYPE, DB_USER
from tests.factories import ProcessInfoFactory, RawValueCleanedFactory, RawValueFactory

register(ProcessInfoFactory)
register(RawValueCleanedFactory)
register(RawValueFactory)


@pytest.fixture(scope="session")
def db_connection():
    if DB_TEST_TYPE == "postgres":
        db_name = f"{DB_NAME}_test"
        print(f"Creating test database {db_name}")
        engine = create_engine(
            "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                DB_USER,
                DB_PASSWORD,
                DB_HOST,
                DB_PORT,
                db_name,
            )
        )
        if database_exists(engine.url):  # pragma: no cover
            answer = input(f"Database {db_name} already exists. Destroy? y/N: ")
            if answer == "y":
                drop_database(engine.url)
            else:
                sys.exit(0)
        create_database(engine.url)
        yield engine.connect()

        print(f"Destroying test database {db_name}")
        drop_database(engine.url)
    else:
        engine = create_engine("sqlite://")
        yield engine.connect()


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
