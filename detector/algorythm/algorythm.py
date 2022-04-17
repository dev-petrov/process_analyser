import json

import numpy as np
import pandas as pd

from detector.aggregator.aggregation_settings import AGGREGATION_SETTINGS

from .exceptions import AnomalyException
from .splits import SplitsCollection
from .utils import json_default


class AnomalyDetector:
    _splits: SplitsCollection
    _normal_states: set[int]
    _qualitatives: list[str]

    def __init__(self, qualitatives: list[str] = None) -> None:
        if qualitatives is None:
            qualitatives = AGGREGATION_SETTINGS.qualitatives
        self._qualitatives = qualitatives

    def fit(self, data: pd.DataFrame) -> None:
        df = self._clean_df(data)
        self._splits = SplitsCollection.build(df, qualitatives=self._qualitatives)
        normal_states = pd.DataFrame(
            columns=self._columns,
            data=list(df.apply(self._encode, axis=1)),
        )
        cols = list(normal_states.columns)
        total_rows = len(normal_states)
        normal_states = normal_states.sort_values(cols)
        normal_states["group"] = "g" + (normal_states.groupby(cols).ngroup() + 1).astype(str)
        normal_states_groupped = (
            normal_states.groupby("group")[cols[0]]
            .count()
            .apply(lambda x: x / total_rows)
            .sort_values(ascending=False)
            .reset_index()
            .rename({cols[0]: "density"}, axis=1)
        )
        total_percent = 0
        groups = []
        for _, row in normal_states_groupped.iterrows():
            total_percent += row.density
            groups.append(row.group)
            if total_percent > 0.89:
                break

        self._normal_states = set(map(tuple, normal_states[normal_states.group.isin(groups)][cols].values))

    @classmethod
    def _clean_df(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        cols_to_float = map(lambda x: (x[0], np.float64), filter(lambda x: x[1] == "object", df.dtypes.iteritems()))
        return df.astype(dict(cols_to_float))

    def save_model(self, path: str) -> None:
        data = {
            "splits": self._splits,
            "normal_states": self._normal_states,
        }
        with open(path, "w") as file:
            file.write(json.dumps(data, default=json_default))

    def load_model(self, path: str) -> None:
        with open(path) as file:
            data = json.loads(file.read())
        self._splits = SplitsCollection.load_from_dict(data["splits"])
        self._normal_states = set(map(tuple, data["normal_states"]))

    def detect(self, data: pd.DataFrame, raise_exception=True) -> list[pd.Series]:
        if not hasattr(self, "_normal_states") or not hasattr(self, "_splits"):
            raise ValueError('You should call "fit" or "load_model" first.')
        anomalies = []

        for i, state in enumerate(list(data.apply(self._encode, axis=1))):
            if state not in self._normal_states:
                anomalies.append(data.loc[i])

        if anomalies and raise_exception:
            raise AnomalyException(anomalies)

        return anomalies

    @property
    def _columns(self) -> list[str]:
        return self._splits.as_columns

    def _encode(self, row: pd.Series) -> tuple[int]:
        new_row = np.zeros(len(self._columns))
        next_index = 0
        for split in self._splits:
            curr_index_start = next_index
            next_index += len(split.splits)
            value = row[split.field]
            value_index = split.get_value_position(value)
            if value_index is None:
                raise AnomalyException([row])
            new_row[curr_index_start + value_index] = 1
        return tuple(new_row)

    def __str__(self) -> str:
        return "DefaultAnomalyDetector"
