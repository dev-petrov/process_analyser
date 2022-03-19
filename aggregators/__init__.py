import pandas as pd
import numpy as np
from datetime import timedelta, datetime, time
from functools import cached_property
from sqlalchemy.orm import Session
from sqlalchemy import func, text, cast, Float
from db import RawValue, engine

class BaseAggregator:
    period_step = 1
    period_length = 10
    aggregation_settings = {}
    _current_time_period = None

    def __init__(self):
        assert self.period_length <= 60
        assert self.period_length >= self.period_step
    
    @cached_property
    def sql_aggregation_settings(self):
        return [
            setting['sql'](getattr(RawValue, setting['column'])).label(label)
            for label, setting in self.aggregation_settings.items()
        ]

    @cached_property
    def df_aggregation_settings(self):
        return {
            label: pd.NamedAgg(column=setting['column'], aggfunc=setting['df'])
            for label, setting in self.aggregation_settings.items()
        }
    
    @cached_property
    def aggregated_rows(self):
        tm_from = self._current_time_period
        tm_to = (datetime.combine(datetime.min, self._current_time_period) + timedelta(minutes=self.period_length)).time()

        with Session(engine) as session:
            time_filter = 'TIME(raw_values.dttm) >= "{}" and TIME(raw_values.dttm) < "{}"'.format(tm_from, tm_to)
            dt = text('DATE(raw_values.dttm)')
            query = session.query(*self.sql_aggregation_settings, dt).filter(
                text(time_filter)
            ).group_by(dt)
            print(query)
            rows = query.all()
        
        return rows

    def get_aggregated_rows(self, dttm: datetime):
        time_period = time(dttm.hour, int(dttm.minute / self.period_step) * self.period_step)
        cached = True

        if time_period != self._current_time_period:
            cached = False
            self._current_time_period = time_period
            if 'aggregated_rows' in self.__dict__:
                del self.__dict__['aggregated_rows']
        
        return self.aggregated_rows, cached
    
    def aggregate_current_data(self, df: pd.DataFrame):
        return df.groupby('dttm').agg(
            **self.df_aggregation_settings,
        )


class DefaultAggregator(BaseAggregator):
    aggregation_settings = {
        'cpu_percent_avg': {
            'sql': func.avg,
            'df': np.mean,
            'column': 'cpu_percent',
        },
        'memory_percent_avg': {
            'sql': func.avg,
            'df': np.mean,
            'column': 'memory_percent',
        },
        'num_threads_avg': {
            'sql': func.avg,
            'df': np.mean,
            'column': 'num_threads',
        },
        'num_threads_min': {
            'sql': func.min,
            'df': np.min,
            'column': 'num_threads',
        },
        'num_threads_max': {
            'sql': func.max,
            'df': np.max,
            'column': 'num_threads',
        },
        'nice_avg': {
            'sql': func.avg,
            'df': np.mean,
            'column': 'nice',
        },
        'connections_avg': {
            'sql': func.avg,
            'df': np.mean,
            'column': 'connections',
        },
        'connections_min': {
            'sql': func.min,
            'df': np.min,
            'column': 'connections',
        },
        'connections_max': {
            'sql': func.max,
            'df': np.max,
            'column': 'connections',
        },
        'open_files_avg': {
            'sql': func.avg,
            'df': np.mean,
            'column': 'open_files',
        },
        'open_files_min': {
            'sql': func.min,
            'df': np.min,
            'column': 'open_files',
        },
        'open_files_max': {
            'sql': func.max,
            'df': np.max,
            'column': 'open_files',
        },
        'idle_process': {
            'sql': lambda x: (cast(func.count(x).filter(x == 'idle'), Float) / cast(func.count(x), Float)),
            'df': lambda x: np.count_nonzero(x == 'idle') / np.count_nonzero(x),
            'column': 'status',
        },
        'running_process': {
            'sql': lambda x: (cast(func.count(x).filter(x == 'running'), Float) / cast(func.count(x), Float)),
            'df': lambda x: np.count_nonzero(x == 'running') / np.count_nonzero(x),
            'column': 'status',
        },
        'sleeping_process': {
            'sql': lambda x: (cast(func.count(x).filter(x == 'sleeping'), Float) / cast(func.count(x), Float)),
            'df': lambda x: np.count_nonzero(x == 'sleeping') / np.count_nonzero(x),
            'column': 'status',
        },
        'zombie_process': {
            'sql': lambda x: (cast(func.count(x).filter(x == 'zombie'), Float) / cast(func.count(x), Float)),
            'df': lambda x: np.count_nonzero(x == 'zombie') / np.count_nonzero(x),
            'column': 'status',
        },
        'disk_sleep_process': {
            'sql': lambda x: (cast(func.count(x).filter(x == 'disk-sleep'), Float) / cast(func.count(x), Float)),
            'df': lambda x: np.count_nonzero(x == 'disk-sleep') / np.count_nonzero(x),
            'column': 'status',
        },
        'root_processes': {
            'sql': lambda x: (cast(func.count(x).filter(x == 'root'), Float) / cast(func.count(x), Float)),
            'df': lambda x: np.count_nonzero(x == 'root') / np.count_nonzero(x),
            'column': 'username',
        },
        'system_processes': {
            'sql': lambda x: (cast(func.count(x).filter(x.startswith('system')), Float) / cast(func.count(x), Float)),
            'df': lambda x: np.count_nonzero(x.str.startswith('system')) / np.count_nonzero(x),
            'column': 'username',
        },
        # 'newly_created': {
        #     'sql': lambda x: (cast(func.count(x).filter(x.startswith('system')), Float) / cast(func.count(x), Float)),
        #     'df': lambda x: np.count_nonzero(x.str.startswith('system')) / np.count_nonzero(x),
        #     'column': 'username',
        # }
    }

    def __str__(self):
        return "DefaultAggregator"
