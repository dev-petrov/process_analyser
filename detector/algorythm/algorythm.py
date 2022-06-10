import json
from decimal import Decimal
from typing import Any, Union

import numpy as np
import pandas as pd

from detector.aggregator.aggregation_settings import AGGREGATION_SETTINGS
from detector.settings import MAX_DISTANCE

from .exceptions import AnomalyException
from .splits import SplitsCollection
from .states import State, StatesCollection
from .utils import json_default


class AnomalyDetector:
    _splits: SplitsCollection
    _normal_states: StatesCollection
    _groups: dict[tuple[int], int]
    _qualitatives: list[str]

    def __init__(self, qualitatives: list[str] = None) -> None:
        if qualitatives is None:
            qualitatives = AGGREGATION_SETTINGS.qualitatives
        self._qualitatives = qualitatives

    def fit(self, data: pd.DataFrame, clear_anomalies=True) -> None:
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
            if total_percent > 0.89 and clear_anomalies:
                break

        self._normal_states = StatesCollection.build(
            set(map(tuple, normal_states[normal_states.group.isin(groups)][cols].values)), df, self._splits
        )
        self._groups = {state: i + 1 for i, state in enumerate(self._normal_states)}

    def classify(self, data: pd.DataFrame) -> pd.DataFrame:
        if not hasattr(self, "_groups") or not hasattr(self, "_splits"):
            raise ValueError('You should call "fit" or "load_model" first.')
        data = data.copy()
        data["label"] = data.apply(lambda x: self._groups.get(self._encode(x), "anomaly"), axis=1)

        return data

    def _clean_df(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        float_columns = list(
            map(lambda x: x[0], filter(lambda x: x[1] in ["object", "float64"], df.dtypes.iteritems()))
        )
        df = df.astype(dict([(field, float) for field in float_columns])).round(6)
        cols_to_decimal = dict([(field, np.dtype(Decimal)) for field in float_columns])
        return df.astype(cols_to_decimal)

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
        self._normal_states = StatesCollection.from_dict(data["normal_states"], splits=self._splits)

    def detect(self, data: pd.DataFrame, raise_exception=True) -> list[dict[str, Any]]:
        if not hasattr(self, "_normal_states") or not hasattr(self, "_splits"):
            raise ValueError('You should call "fit" or "load_model" first.')
        data = self._clean_df(data)
        anomalies = []

        dict_data = data.to_dict("index")

        for i, state in data.iterrows():
            if state not in self._normal_states:
                anomalies.append(
                    {
                        "index": i,
                        "aggregated": dict_data[i],
                        "closest_states": list(
                            self._normal_states.closest_states_with_fields_differ(
                                self._encode(data.loc[i]), max_distance=MAX_DISTANCE
                            ).values()
                        ),
                    }
                )

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
            new_row[curr_index_start + value_index] = 1
        return tuple(new_row)

    def get_closest_states(self, state: Union[tuple[int], State], max_distance=3) -> StatesCollection:
        return self._normal_states.closest_states(state, max_distance=max_distance)

    def __str__(self) -> str:
        return "AnomalyDetector"
