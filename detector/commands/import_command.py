import os
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

    def handle(self, *args, **options):
        readers = {
            "csv": pd.read_csv,
            "xlsx": pd.read_excel,
        }
        file_type = options["file_type"]
        drop_previous = options.get("drop_previous", False)
        filename = options["filename"]

        print(f"Reading {file_type} file...")

        df = readers[file_type](
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

        print("Importing...")

        with session_scope() as session:
            # TODO check for duplicates
            if drop_previous:
                with session.begin():
                    session.query(RawCleanedValue).delete()
            df.dttm = pd.to_datetime(df.dttm, unit="s")
            df.create_time = pd.to_datetime(df.create_time, unit="s")
            total_rows = len(df)
            chunks = np.array_split(df.to_dict("records"), int(total_rows / 10000) + 1)
            del df
            added_rows = 0
            for chunk in chunks:
                with session.begin():
                    session.add_all([RawCleanedValue(**kwargs) for kwargs in chunk])
                    added_rows += len(chunk)
                    os.system("clear")
                    print(f"Added {round((added_rows / total_rows) * 100, 2)}% rows.")

        print(f"Successfully imported {total_rows} rows.")
