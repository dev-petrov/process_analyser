import time as systime
from argparse import ArgumentParser
from datetime import datetime, timedelta

from detector import settings
from detector.detect_process import DetectProcess

from .base_command import BaseCommand


class DetectCommand(BaseCommand):
    description = "Anomaly detect process"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "--logger_filename",
            help="File name for file logger",
            type=str,
            default=settings.DETECTOR_LOGGER_FILENAME,
        )
        parser.add_argument(
            "--logger",
            help="Type of logger",
            default=settings.DETECTOR_LOGGER,
            choices=["console", "db", "file"],
        )
        parser.add_argument("--detector_file", help="Detector file", type=str, default=None)
        parser.add_argument("--verbose", help="Print additional info", default=False, type=bool)

    def handle(self, *args, **options):

        logger = self.get_instance("logger", options)

        print("Starting detector service.")
        print(f"Using logger: {logger}")
        verbose = options.get("verbose", settings.DETECTOR_VERBOSE)
        detector_file = options.get("detector_file", settings.DETECTOR_FILE)

        detect_process = DetectProcess(
            logger,
            verbose=verbose,
            detector_file=detector_file,
        )

        print("Detector service started.")

        while True:
            next_run_at = datetime.now() + timedelta(seconds=60)
            detect_process.run()
            sleep_secs = (next_run_at - datetime.now()).total_seconds()
            print(f"Sleeping {sleep_secs} secs...")
            systime.sleep(sleep_secs)
