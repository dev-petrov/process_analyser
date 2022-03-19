import argparse
import time as systime
from data_getters import BaseGetter
from collectors import BaseCollector
from loggers import BaseAnomalyLogger
from aggregators import BaseAggregator
from algorythms import BaseAnomalyDetector
from utils import get_instance

class DetectProcess:
    def __init__(
        self, 
        data_getter_obj: BaseGetter, 
        logger_obj: BaseAnomalyLogger,
        aggregator_obj: BaseAggregator, 
        anomaly_detector_obj: BaseAnomalyDetector,
        collector_obj: BaseCollector = None,
        verbose=False,
    ):
        self.data_getter = data_getter_obj
        self.collector = collector_obj
        self.logger = logger_obj
        self.aggregator = aggregator_obj
        self.anomaly_detecor = anomaly_detector_obj
        self.verbose = verbose

    def _print_if_verbose(self, data):
        if self.verbose:
            print(data)

    def get_data(self):
        return self.data_getter.get_data()
    
    def collect(self, data):
        if self.collector:
            self._print_if_verbose('Collecting data')
            self.collector.collect(data)
    
    def log(self, data):
        self.logger.log(data)

    def get_aggregated_train_data(self, dttm):
        return self.aggregator.get_aggregated_rows(dttm)
    
    def get_aggregated_data_for_detect(self, df):
        return self.aggregator.aggregate_current_data(df)

    def detect(self, train_data, cached, detect_data):
        if not cached:
            self.anomaly_detecor.fit(train_data)
        return self.anomaly_detecor.detect(detect_data)

    def run(self):
        self._print_if_verbose('Getting data')
        dttm, data = self.get_data()

        self._print_if_verbose('Getting train data')

        train_data, cached = self.get_aggregated_train_data(dttm)

        self._print_if_verbose('Detecting')

        anomalies = self.detect(
            train_data,
            cached,
            self.get_aggregated_data_for_detect(data),
        )

        self._print_if_verbose('Detection end')

        for anomaly in anomalies:
            self.log(anomaly)

        if len(anomalies) == 0:
            self.collect(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Anomaly detector')
    parser.add_argument('--collector', help='Type of collector. If defined collects data without anomalies', default=None, choices=['csv', 'db'])
    parser.add_argument('--collector_filename', help='File name for csv collector', type=str)
    parser.add_argument('--logger_filename', help='File name for file logger', type=str)
    parser.add_argument('--interval', help='Interval in secs for trigger detect. Default 1 sec', default=1, type=int)
    parser.add_argument('--data_getter', help='How to get data', choices=['process'], default='process')
    parser.add_argument('--logger', help='Type of logger', default='console', choices=['console', 'db', 'file'])
    parser.add_argument('--aggregator', help='Type of aggregation', default='default', choices=['default'])
    parser.add_argument('--detector', help='Detector algorythm', default='default', choices=['default'])
    parser.add_argument('--verbose', help='Print additional info', default=False, type=bool)


    args = parser.parse_args()

    collector = get_instance('collector', args) if args.collector else None
    data_getter = get_instance('data_getter', args)
    logger = get_instance('logger', args)
    aggregator = get_instance('aggregator', args)
    detector = get_instance('detector', args)

    print("Starting detector service.")
    print(f"Using collector: {collector}")
    print(f"Using data_getter: {data_getter}")
    print(f"Using logger: {logger}")
    print(f"Using aggregator: {aggregator}")
    print(f"Using detector: {detector}")
    interval = args.interval
    print(f"Using interval {interval} secs")

    detect_process = DetectProcess(
        data_getter,
        logger,
        aggregator,
        detector,
        collector_obj=collector,
        verbose=args.verbose,
    )

    print('Detector service started.')

    while True:
        detect_process.run()
        interval = args.interval
        print(f"Sleeping {interval} secs...")
        systime.sleep(interval)
