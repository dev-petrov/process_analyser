from datetime import datetime

import pandas as pd
import pytest


@pytest.fixture
def processes_data(process_info_factory):
    dttm = datetime.now()
    processes = [process_info_factory(dttm=dttm) for i in range(10)]
    return dttm, pd.DataFrame(
        columns=[
            "dttm",
            "pid",
            "name",
            "username",
            "ppid",
            "parent_name",
            "cpu_percent",
            "memory_percent",
            "num_threads",
            "terminal",
            "nice",
            "cmdline",
            "exe",
            "status",
            "create_time",
            "connections",
            "open_files",
        ],
        data=[
            (
                p.dttm.timestamp(),
                p.pid,
                p.name,
                p.username,
                p.ppid,
                p.parent_name,
                p.cpu_percent,
                p.memory_percent,
                p.num_threads,
                p.terminal,
                p.nice,
                p.cmdline,
                p.exe,
                p.status,
                p.create_time,
                p.connections,
                p.open_files,
            )
            for p in processes
        ],
    )
