import pandas as pd
from pytz.reference import LocalTimezone
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from data_getters import ProcessGetter

from db import engine

class BaseCollector:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.process_getter = ProcessGetter()
        self.tz_offset = timedelta(seconds=LocalTimezone().utcoffset(datetime.now()).seconds)

    def _collect(self, data):
        raise NotImplementedError()

    def collect(self, data=None):
        dttm = datetime.now()
        if not data:
            dttm, data = self.process_getter.get_data()
        self._collect(data)

        if self.verbose:
            print(f"{dttm + self.tz_offset}: Collected {len(data)} rows")

class CsvCollector(BaseCollector):
    def __init__(self, filename, *args, **kwargs):
        if not filename:
            filename = 'collected_data.csv'
        self.filename = filename
        super().__init__(*args, **kwargs)

    def _collect(self, data):
        with open(self.filename, 'a') as file:
            file.write(data.to_csv(header=False, index=False))
    
    def __str__(self):
        return f"CsvCollector, filename: {self.filename}"

class DBCollector(BaseCollector):
    def __init__(self, raw_value_cls, *args, **kwargs):
        self.db_cls = raw_value_cls
        super().__init__(*args, **kwargs)

    def _collect(self, data: pd.DataFrame):
        with Session(engine) as session, session.begin():
            data.dttm = pd.to_datetime(data.dttm, unit='s')
            data.create_time = pd.to_datetime(data.create_time, unit='s')
            session.add_all(
                [
                    self.db_cls(**kwargs)
                    for kwargs in data.to_dict('records')
                ]
            )

    def __str__(self):
        return "DBCollector"
