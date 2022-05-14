from curses import wrapper, window
from argparse import ArgumentParser

import numpy as np
import pandas as pd

from detector.db import RawCleanedValue, session_scope

from .base_command import BaseCommand


class ImportCommand(BaseCommand):
    description = "Import data helper"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--file_type", help="Type of file", default="csv", choices=["csv", "xlsx"])
        parser.add_argument("--filename", help="File name", type=str, required=True)
        parser.add_argument("--drop_previous", help="Drop previous rows", type=bool, default=False)
    
    def _handle(self, stdscr: window, read_func, filename, drop_previous=False):
        stdscr.clear()
        stdscr.refresh()
        rows, cols = stdscr.getmaxyx()

        row_pos = round(rows / 2)

        stdscr.addstr(row_pos, 0, "Reading file...")
        stdscr.refresh()

        df = read_func(
            filename,
            names=[
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
        )

        with session_scope() as session:
            # TODO check for duplicates
            if drop_previous:
                stdscr.addstr(row_pos, 0, "Dropping previous...")
                stdscr.refresh()
                with session.begin():
                    session.query(RawCleanedValue).delete()
            df.dttm = pd.to_datetime(df.dttm, unit="s")
            df.create_time = pd.to_datetime(df.create_time, unit="s")
            total_rows = len(df)
            chunks = np.array_split(df.to_dict("records"), int(total_rows / 10000) + 1)
            del df
            added_rows = 0
            MAX_SPACES = cols - 10 - len(str(total_rows)) * 2 - len("Importing ")
            stdscr.addstr(row_pos, 0, "Importing...")
            stdscr.refresh()
            for chunk in chunks:
                with session.begin():
                    session.add_all([RawCleanedValue(**kwargs) for kwargs in chunk])
                    added_rows += len(chunk)
                    progress = round((added_rows / total_rows) * MAX_SPACES)
                    stdscr.addstr(row_pos, 0, "Importing [" + "=" * progress + ">" + " " * (MAX_SPACES - progress) + f"] {added_rows} / {total_rows}")
                    stdscr.refresh()

        stdscr.addstr(row_pos, 0, f"Successfully imported {total_rows} rows.")
        stdscr.refresh()

    def handle(self, *args, **options):
        readers = {
            "csv": pd.read_csv,
            "xlsx": pd.read_excel,
        }
        file_type = options["file_type"]
        drop_previous = options.get("drop_previous", False)
        filename = options["filename"]

        wrapper(self._handle, readers[file_type], filename, drop_previous=drop_previous)
