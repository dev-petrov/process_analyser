from distutils.util import strtobool
from os import getenv

from dotenv import load_dotenv

from collectors import CsvCollector, DBCollector
from loggers import ConsoleAnomalyLogger, DataBaseAnomalyLogger, FileAnomalyLogger

COLLECTORS = {
    "db": {
        "class": DBCollector,
        "args": ["raw_values_cls"],
    },
    "csv": {
        "class": CsvCollector,
        "args": ["collector_filename"],
    },
}
LOGGERS = {
    "console": {
        "class": ConsoleAnomalyLogger,
    },
    "db": {
        "class": DataBaseAnomalyLogger,
    },
    "file": {
        "class": FileAnomalyLogger,
        "args": ["logger_filename"],
    },
}

INSTANCE_TYPES = {
    "collector": COLLECTORS,
    "logger": LOGGERS,
}

AVAILABLE_CONFIG_SETTINGS = {
    "logger": str,
    "logger_filename": str,
    "verbose": strtobool,
}

load_dotenv()

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_NAME = getenv("DB_NAME")
DB_TEST_TYPE = getenv("DB_TEST_TYPE")
