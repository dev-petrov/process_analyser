from datetime import timedelta, datetime
from functools import cached_property
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from db import RawCleanedValue, RawValue, engine

class Aggregator:
    period_length = 10
    aggregation_settings = {
        'cpu_percent_avg': {
            'func': func.avg,
            'column': 'cpu_percent',
        },
        'memory_percent_avg': {
            'func': func.avg,
            'column': 'memory_percent',
        },
        'num_threads_avg': {
            'func': func.avg,
            'column': 'num_threads',
        },
        'num_threads_min': {
            'func': func.min,
            'column': 'num_threads',
        },
        'num_threads_max': {
            'func': func.max,
            'column': 'num_threads',
        },
        'nice_avg': {
            'func': func.avg,
            'column': 'nice',
        },
        'connections_avg': {
            'func': func.avg,
            'column': 'connections',
        },
        'connections_min': {
            'func': func.min,
            'column': 'connections',
        },
        'connections_max': {
            'func': func.max,
            'column': 'connections',
        },
        'open_files_avg': {
            'func': func.avg,
            'column': 'open_files',
        },
        'open_files_min': {
            'func': func.min,
            'column': 'open_files',
        },
        'open_files_max': {
            'func': func.max,
            'column': 'open_files',
        },
        'idle_process': {
            'func': lambda x: func.count(x).filter(x == 'idle'),
            'column': 'status',
        },
        'running_process': {
            'func': lambda x: func.count(x).filter(x == 'running'),
            'column': 'status',
        },
        'sleeping_process': {
            'func': lambda x: func.count(x).filter(x == 'sleeping'),
            'column': 'status',
        },
        'zombie_process': {
            'func': lambda x: func.count(x).filter(x == 'zombie'),
            'column': 'status',
        },
        'disk_sleep_process': {
            'func': lambda x: func.count(x).filter(x == 'disk-sleep'),
            'column': 'status',
        },
        'root_processes': {
            'func': lambda x: func.count(x).filter(x == 'root'),
            'column': 'username',
        },
        'system_processes': {
            'func': lambda x: func.count(x).filter(x.startswith('system')),
            'column': 'username',
        },
        # 'newly_created': {
        #     'sql': lambda x: (cast(func.count(x).filter(x.startswith('system')), Float) / cast(func.count(x), Float)),
        #     'df': lambda x: np.count_nonzero(x.str.startswith('system')) / np.count_nonzero(x),
        #     'column': 'username',
        # }
    }

    def get_train_data(self):
        aggregation_settings = [
            setting['func'](getattr(RawCleanedValue, setting['column'])).label(label)
            for label, setting in self.aggregation_settings.items()
        ]
        with Session(engine) as session:
            dttms = list(
                map(
                    lambda x: x['unique_dttm'],
                    session.query(distinct(RawCleanedValue.dttm).label('unique_dttm')).order_by('unique_dttm').all()
                )
            )
            return [
                self._get_aggregate_query(dttm, session, aggregation_settings, RawCleanedValue).first()
                for dttm in dttms[self.period_length:]
            ]
    
    def _get_aggregate_query(self, dttm: datetime, session: Session, aggregation_settings: list, raw_value_cls):
        dttm_from = dttm - timedelta(minutes=self.period_length)
        dttm_to = dttm
        return session.query(*aggregation_settings).filter(
            raw_value_cls.dttm >= dttm_from, 
            raw_value_cls.dttm <= dttm_to,
        )

    @cached_property
    def sql_aggregation_settings(self):
        return [
            setting['func'](getattr(RawValue, setting['column'])).label(label)
            for label, setting in self.aggregation_settings.items()
        ]

    def get_detect_data(self, dttm: datetime):
        with Session(engine) as session:
            return self._get_aggregate_query(dttm, session, self.sql_aggregation_settings, RawValue).all()
