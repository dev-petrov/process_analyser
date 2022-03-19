import pandas as pd

class BaseAnomalyDetector:

    clean_data = []

    def fit(self, data: pd.DataFrame):
        self.clean_data = data.copy()

    def detect(self, row):
        return []

class DefaultAnomalyDetector(BaseAnomalyDetector):
    def __str__(self):
        return "DefaultAnomalyDetector"
