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
            "-l",
            "--logger",
            help="Type of logger",
            nargs="+",
            default=settings.DETECTOR_LOGGER,
            choices=["console", "db", "file"],
        )
        parser.add_argument("--detector_file", help="Detector file", type=str, default=None)
        parser.add_argument("--verbose", help="Print additional info", default=False, type=bool)

    def handle(self, *args, **options):

        loggers = [self.get_instance("logger", {**options, "logger": logger}) for logger in options["logger"]]

        print("Starting detector service.")
        print(f"Using loggers: {', '.join(map(str, loggers))}")
        verbose = options.get("verbose", settings.DETECTOR_VERBOSE)
        detector_file = options.get("detector_file", settings.DETECTOR_FILE)

        detect_process = DetectProcess(
            loggers,
            verbose=verbose,
            detector_file=detector_file,
            min_normal_state_difference=settings.MAX_DIFFERENCE_TO_SKIP,
        )

        print("Detector service started.")

        next_run_at = datetime.now()

        while True:
            next_run_at = next_run_at + timedelta(seconds=60)
            detect_process.run()
            print("Sleeping...")
            sleep_secs = (next_run_at - datetime.now()).total_seconds()
            systime.sleep(sleep_secs)
