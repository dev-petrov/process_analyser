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
        parser.add_argument("--collector_filename", help="File name for csv collector", type=str)

    def handle(self, *args, **options):
        options["raw_values_cls"] = RawCleanedValue

        collector: BaseCollector = self.get_instance("collector", options, instance_kwargs={"verbose": True})
        process_getter = ProcessGetter()

        print("Starting collector service.")
        print(f"Using collector: {collector}")

        print("Collecting...")

        next_run_at = datetime.now()

        while True:
            next_run_at = next_run_at + timedelta(seconds=60)
            dttm, data = process_getter.get_data()
            collector.collect(data)
            print(f"Sleeping...")
            sleep_secs = (next_run_at - datetime.now()).total_seconds()
            systime.sleep(sleep_secs)
