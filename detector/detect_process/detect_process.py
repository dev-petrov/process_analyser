from datetime import datetime
from typing import Any

import pandas as pd

from detector.aggregator import Aggregator
from detector.algorythm import AnomalyDetector, AnomalyException
from detector.collectors import DBCollector
from detector.data_getter import ProcessGetter
from detector.db import RawValue
from detector.loggers.base_logger import BaseAnomalyLogger


class DetectProcess:  # pragma: no cover
    _logger: BaseAnomalyLogger
    _data_getter: ProcessGetter
    _collector: DBCollector
    _aggregator: Aggregator
    _detector: AnomalyDetector
    _verbose: bool
    _run_cnt: int = 0

    def __init__(
        self,
        logger_obj: BaseAnomalyLogger,
        verbose=False,
        detector_file=None,
    ) -> None:
        self._data_getter = ProcessGetter()
        self._collector = DBCollector(RawValue)
        self._logger = logger_obj
        self._aggregator = Aggregator()
        self._detector = AnomalyDetector()
        self._verbose = verbose
        if not detector_file:
            print("Fit detector")
            self._detector.fit(self._aggregator.get_train_data())
            print("Detector fitted")
        else:
            print("Loading detector")
            self._detector.load_model(detector_file)
            print("Detector loaded")

    def _print_if_verbose(self, data: Any) -> None:
        if self._verbose:
            print(data)

    def _get_data(self) -> pd.DataFrame:
        return self._data_getter.get_data()

    def _collect(self, data: pd.DataFrame) -> None:
        self._print_if_verbose("Collecting data")
        self._collector.collect(data)

    def _log(self, data: dict) -> None:
        self._logger.log(data)

    def _get_data_for_detect(self, dttm: datetime) -> pd.DataFrame:
        return self._aggregator.get_detect_data(dttm)

    def _detect(self, detect_data: pd.DataFrame) -> list[pd.Series]:
        return self._detector.detect(detect_data)

    def run(self) -> None:
        self._print_if_verbose("Getting data")
        dttm, data = self._get_data()
        self._collect(data)

        if self._run_cnt + 1 < self._aggregator.period_length:
            self._run_cnt += 1
            self._print_if_verbose(
                f"Collected {self._run_cnt} portions of {self._aggregator.period_length}. Skipping detecting..."
            )
            return

        self._print_if_verbose("Detecting")

        try:
            self._detect(
                self._get_data_for_detect(dttm),
            )
        except AnomalyException as e:
            self._print_if_verbose(f"Logging {e.detail.count} anomalies...")
            for anomaly in e.detail.details:
                self._log(anomaly)

        self._print_if_verbose("Detection end")
