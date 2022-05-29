from os import getenv

from dotenv import load_dotenv

COLLECTORS = {
    "db": {
        "class": "DBCollector",
        "args": ["raw_values_cls"],
    },
    "csv": {
        "class": "CsvCollector",
        "args": ["collector_filename"],
    },
}
LOGGERS = {
    "console": {
        "class": "ConsoleAnomalyLogger",
    },
    "db": {
        "class": "DataBaseAnomalyLogger",
    },
    "file": {
        "class": "FileAnomalyLogger",
        "args": ["logger_filename"],
    },
}

INSTANCE_TYPES = {
    "collector": {
        "module": "detector.collectors",
        "classes": COLLECTORS,
    },
    "logger": {
        "module": "detector.loggers",
        "classes": LOGGERS,
    },
}

load_dotenv()

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_NAME = getenv("DB_NAME", "./anomaly.db")
DB_PREFIX = getenv("DB_PREFIX", "sqlite")
DETECTOR_LOGGER_FILENAME = getenv("DETECTOR_LOGGER_FILENAME")
DETECTOR_LOGGER = getenv("DETECTOR_LOGGER", "db")
DETECTOR_VERBOSE = getenv("DETECTOR_VERBOSE", False)
DETECTOR_FILE = getenv("DETECTOR_FILE")
API_TOKEN = getenv("API_TOKEN")
EXCLUDE_EXE = getenv("EXCLUDE_EXE", "")
EXCLUDE_COMMAND = getenv("EXCLUDE_COMMAND", "")
EXCLUDE_NAME = getenv("EXCLUDE_NAME", "")
MAX_DISTANCE = int(getenv("MAX_DISTANCE", 3))
