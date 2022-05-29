import re
import threading
from datetime import datetime

import pandas as pd
import psutil as ps

from detector import settings


class ProcessGetter:
    _current_pid: int

    def __init__(self) -> None:
        self._current_pid = threading.current_thread().native_id

    def _enrich_process(self, process: ps.Process) -> dict:
        process = process.info
        process["open_files"] = len(process["open_files"]) if process["open_files"] else 0
        process["connections"] = len(process["connections"]) if process["connections"] else 0
        process["cmdline"] = " ".join(process["cmdline"]) if process["cmdline"] else None
        try:
            parent_name = ps.Process(process["ppid"]).name()
        except BaseException:
            parent_name = None
        process["parent_name"] = parent_name

        return process

    def get_data(self) -> tuple[datetime, pd.DataFrame]:
        dttm = datetime.now().timestamp()

        def _filter_process(process: ps.Process) -> bool:
            process = process.info
            return not (
                process["pid"] == self._current_pid
                or (settings.EXCLUDE_EXE and re.match(settings.EXCLUDE_EXE, process["exe"]))
                or (
                    settings.EXCLUDE_COMMAND
                    and process["cmdline"]
                    and re.match(settings.EXCLUDE_COMMAND, " ".join(process["cmdline"]))
                )
                or (settings.EXCLUDE_NAME and process["cmdline"] and re.match(settings.EXCLUDE_NAME, process["name"]))
            )

        processes = list(
            map(
                self._enrich_process,
                filter(
                    _filter_process,
                    ps.process_iter(
                        [
                            "pid",
                            "name",
                            "username",
                            "terminal",
                            "num_threads",
                            "nice",
                            "exe",
                            "memory_percent",
                            "cmdline",
                            "create_time",
                            "connections",
                            "status",
                            "cpu_percent",
                            "ppid",
                            "open_files",
                        ]
                    ),
                ),
            )
        )

        df = pd.DataFrame(
            data=processes,
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
        ).fillna(0)

        df["dttm"] = dttm

        return pd.to_datetime(dttm, unit="s"), df

    def __str__(self) -> str:
        return "ProcessGetter"
