import sys
import time as systime
from argparse import ArgumentParser
from datetime import datetime, timedelta

from detector.collectors.base_collector import BaseCollector
from detector.data_getter import ProcessGetter
from detector.db import RawCleanedValue

from .base_command import BaseCommand


class CollectCommand(BaseCommand):
    description = "Data collect process"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--collector", help="Type of collector", default="csv", choices=["csv", "db"])
        parser.add_argument("--filename", help="File name for csv collector", type=str)

    def handle(self, *args, **options):
        options["raw_values_cls"] = RawCleanedValue

        collector: BaseCollector = self.get_instance("collector", options, instance_kwargs={"verbose": True})
        process_getter = ProcessGetter()

        sys.stdout.write("Starting collector service.")
        sys.stdout.write(f"Using collector: {collector}")

        sys.stdout.write("Collecting...")

        while True:
            next_run_at = datetime.now() + timedelta(seconds=60)
            dttm, data = process_getter.get_data()
            collector.collect(data)
            sleep_secs = (next_run_at - datetime.now()).total_seconds()
            sys.stdout.write(f"Sleeping {sleep_secs} secs...")
            systime.sleep(sleep_secs)
