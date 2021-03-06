import json
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
        return df.astype(dict([(field, float) for field in float_columns])).round(6)

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

    def detect(
        self, data: pd.DataFrame, raise_exception=True, find_closest_states=True, max_difference_to_skip=None
    ) -> list[dict[str, Any]]:
        if not hasattr(self, "_normal_states") or not hasattr(self, "_splits"):
            raise ValueError('You should call "fit" or "load_model" first.')
        data = self._clean_df(data)
        anomalies = []

        dict_data = data.to_dict("index")

        for i, state in data.iterrows():
            if state not in self._normal_states:
                state, has_out_of_range = self._encode(data.loc[i], return_out_of_range=True)
                if (
                    not has_out_of_range
                    and max_difference_to_skip is not None
                    and self._normal_states.closest_states(state, max_distance=max_difference_to_skip)
                ):
                    continue
                anomalies.append(
                    {
                        "index": i,
                        "aggregated": dict_data[i],
                        "closest_states": list(
                            self._normal_states.closest_states_with_fields_differ(
                                state,
                                max_distance=MAX_DISTANCE,
                                ignore_zero_difference=has_out_of_range,
                            ).values()
                        )
                        if find_closest_states
                        else [],
                        "out_of_range": has_out_of_range,
                    }
                )

        if anomalies and raise_exception:
            raise AnomalyException(anomalies)

        return anomalies

    @property
    def _columns(self) -> list[str]:
        return self._splits.as_columns

    def _encode(self, row: pd.Series, return_out_of_range=False) -> Union[tuple[int], tuple[tuple[int], bool]]:
        new_row = np.zeros(len(self._columns))
        next_index = 0
        has_out_of_range = False
        for split in self._splits:
            curr_index_start = next_index
            next_index += len(split.splits)
            value = row[split.field]
            value_index, out_of_range = split.get_value_position(value)
            if out_of_range:
                has_out_of_range = True
            new_row[curr_index_start + value_index] = 1
        if not return_out_of_range:
            return tuple(new_row)
        else:
            return tuple(new_row), has_out_of_range

    def get_closest_states(self, state: Union[tuple[int], State], max_distance=3) -> StatesCollection:
        return self._normal_states.closest_states(state, max_distance=max_distance)

    def __str__(self) -> str:
        return "AnomalyDetector"
