import pandas as pd

from collectors.base_collector import BaseCollector


class CsvCollector(BaseCollector):
    _filename: str

    def __init__(self, filename: str, *args, **kwargs) -> None:
        if not filename:
            filename = "collected_data.csv"
        self._filename = filename
        super().__init__(*args, **kwargs)

    def _collect(self, data: pd.DataFrame) -> None:
        with open(self._filename, "a") as file:
            file.write(data.to_csv(header=False, index=False))

    def __str__(self) -> str:
        return f"CsvCollector, filename: {self._filename}"
