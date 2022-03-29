import argparse
from datetime import datetime, timedelta
import time as systime
from data_getters import ProcessGetter
from collectors import DBCollector
from loggers import BaseAnomalyLogger
from aggregators import Aggregator
from algorythms import AnomalyDetector
from utils import get_instance

class DetectProcess:
    def __init__(
        self, 
        logger_obj: BaseAnomalyLogger,
        verbose=False,
    ):
        self.data_getter = ProcessGetter()
        self.collector = DBCollector()
        self.logger = logger_obj
        self.aggregator = Aggregator()
        self.detector = AnomalyDetector()
        self.verbose = verbose
        print("Fit detector")
        self.detector.fit(self.aggregator.get_train_data())
        print("Detector fitted")

    def _print_if_verbose(self, data):
        if self.verbose:
            print(data)

    def _get_data(self):
        return self.data_getter.get_data()
    
    def _collect(self, data):
        self._print_if_verbose('Collecting data')
        self.collector.collect(data)
    
    def _log(self, data):
        self.logger.log(data)
    
    def _get_data_for_detect(self, dttm):
        return self.aggregator.get_detect_data(dttm)

    def _detect(self, detect_data):
        return self.detector.detect(detect_data)

    def run(self):
        self._print_if_verbose('Getting data')
        dttm, data = self._get_data()
        self._collect(data)

        self._print_if_verbose('Detecting')

        anomalies = self._detect(
            self._get_data_for_detect(dttm),
        )

        self._print_if_verbose('Detection end')

        for anomaly in anomalies:
            self._log(anomaly)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Anomaly detector')
    parser.add_argument('--logger_filename', help='File name for file logger', type=str)
    parser.add_argument('--logger', help='Type of logger', default='console', choices=['console', 'db', 'file'])
    parser.add_argument('--verbose', help='Print additional info', default=False, type=bool)


    args = parser.parse_args()

    logger = get_instance('logger', args)
    
    print("Starting detector service.")
    print(f"Using logger: {logger}")

    detect_process = DetectProcess(
        logger,
        verbose=args.verbose,
    )

    print('Detector service started.')

    while True:
        next_run_at = datetime.now() + timedelta(seconds=60)
        detect_process.run()
        sleep_secs = (next_run_at - datetime.now()).total_seconds()
        print(f"Sleeping {sleep_secs} secs...")
        systime.sleep(sleep_secs)
