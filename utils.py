from data_getters import ProcessGetter
from collectors import DBCollector, CsvCollector
from loggers import FileAnomalyLogger, DataBaseAnomalyLogger, ConsoleAnomalyLogger
from aggregators import DefaultAggregator
from algorythms import DefaultAnomalyDetector

COLLECTORS = {
    'db': {
        'class': DBCollector,
    },
    'csv': {
        'class': CsvCollector,
        'args': ['collector_filename'],
    }
}
DATA_GETTERS = {
    'process': {
        'class': ProcessGetter,
    }
}
LOGGERS = {
    'console': {
        'class': ConsoleAnomalyLogger,
    },
    'db': {
        'class': DataBaseAnomalyLogger,
    },
    'file': {
        'class': FileAnomalyLogger,
        'args': ['logger_filename'],
    }
}
AGGREGATORS = {
    'default': {
        'class': DefaultAggregator,
    }
}
DETECTORS = {
    'default': {
        'class': DefaultAnomalyDetector,
    }
}

INSTANCE_TYPES = {
    'collector': COLLECTORS,
    'data_getter': DATA_GETTERS,
    'logger': LOGGERS,
    'aggregator': AGGREGATORS,
    'detector': DETECTORS,
}

def get_instance(instance_type, args, instance_args=[], instance_kwargs={}):
    available_classes = INSTANCE_TYPES[instance_type]
    
    instance_name = getattr(args, instance_type)
    cls = available_classes[instance_name]['class']
    instance_args = instance_args + [getattr(args, arg, None) for arg in available_classes[instance_name].get('args', [])]

    return cls(*instance_args, **instance_kwargs)
