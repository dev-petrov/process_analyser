from copy import deepcopy

class AnomalyDetector:
    _clean_data = []

    def fit(self, data: list):
        self._clean_data = deepcopy(data)

    def detect(self, data: list):
        return []
    
    def __str__(self):
        return "DefaultAnomalyDetector"
