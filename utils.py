from collectors import DBCollector, CsvCollector
from loggers import FileAnomalyLogger, DataBaseAnomalyLogger, ConsoleAnomalyLogger
from distutils.util import strtobool

COLLECTORS = {
    'db': {
        'class': DBCollector,
        'args': ['raw_values_cls'],
    },
    'csv': {
        'class': CsvCollector,
        'args': ['collector_filename'],
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

INSTANCE_TYPES = {
    'collector': COLLECTORS,
    'logger': LOGGERS,
}

AVAILABLE_CONFIG_SETTINGS = {
    'logger': str,
    'logger_filename': str,
    'verbose': strtobool,
}

def get_instance(instance_type, args, instance_args=[], instance_kwargs={}):
    available_classes = INSTANCE_TYPES[instance_type]
    
    instance_name = getattr(args, instance_type)
    cls = available_classes[instance_name]['class']
    instance_args = instance_args + [getattr(args, arg, None) for arg in available_classes[instance_name].get('args', [])]

    return cls(*instance_args, **instance_kwargs)

def get_configuration_from_file(filename):
    settings = {}
    with open(filename) as file:
        for i, line in enumerate(file.readlines()):
            setting = list(map(lambda x: x.strip(), line.split('=')))
            if len(setting) != 2:
                print(f'Warn: in row {i + 1} expected key=value syntax got {line}.')
                continue
            setting_key, setting_value = setting
            setting_func = AVAILABLE_CONFIG_SETTINGS.get(setting_key.lower())
            if not setting_func:
                print(f'Warn: {setting_key} is not a valid key.')
                continue

            settings[setting_key.lower()] = setting_func(setting_value)
    
    return settings
