import abc
from dataclasses import dataclass
from typing import Generator, Optional, Union

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.signal import argrelextrema


@dataclass
class BaseSplit(abc.ABC):
    field: str
    splits: list[Union[tuple[float, float], tuple[int, int], float, int]]

    @abc.abstractmethod
    def get_value_position(self, value: Union[float, int]) -> Optional[int]:  # pragma: no cover
        pass


class QuantitativeSplit(BaseSplit):
    def get_value_position(self, value: Union[float, int]) -> Optional[int]:
        index = None
        for i, (min, max) in enumerate(self.splits):
            if value >= min and value <= max:
                index = i
                break
        return index


class QualitativeSplit(BaseSplit):
    def get_value_position(self, value: Union[float, int]) -> Optional[int]:
        index = None
        for i, qualitative_value in enumerate(self.splits):
            if value == qualitative_value:
                index = i
                break
        return index


@dataclass
class SplitsCollection:
    _splits: list[BaseSplit]

    @classmethod
    def _append_qualitative(cls, splits: list[BaseSplit], field: str, values: pd.Series) -> list[BaseSplit]:
        splits.append(
            QualitativeSplit(
                field=field,
                splits=sorted(values.unique()),
            )
        )
        return splits

    @classmethod
    def _append_quantitative(cls, splits: list[BaseSplit], field: str, values: pd.Series) -> list[BaseSplit]:
        result = []
        serie = values.copy()
        dtype = serie.dtype
        maximum = serie.min()
        minimums = cls._find_mininmums(serie)
        if len(minimums):
            maximum, _ = cls._get_interval(serie[serie <= minimums[0]], dtype == "int64")
        else:
            maximum, _ = cls._get_interval(serie, dtype == "int64")
        for local_min in minimums:
            minimum = maximum
            maximum = local_min
            if dtype == "int64":
                maximum = round(maximum)
            result.append((minimum, maximum))
        minimum = maximum
        maximum = serie.max() if serie.max() != maximum else maximum + 1
        _, maximum = cls._get_interval(serie[serie >= minimum], dtype == "int64")
        result.append((minimum, maximum))
        splits.append(
            QuantitativeSplit(
                field=field,
                splits=result,
            )
        )
        return splits

    @staticmethod
    def _get_interval(data: pd.Series, need_round: bool) -> tuple[float, float]:
        def _prepare_result(min, max):
            if need_round:
                min, max = round(min), round(max)
            return min, max

        if len(data) < 2:
            return _prepare_result(data.min(), data.max())
        return _prepare_result(
            min(data.mean() - 3 * data.std(), data.min()),
            max(data.mean() + 3 * data.std(), data.max()),
        )

    @staticmethod
    def _find_mininmums(data: pd.Series) -> np.ndarray:
        lines = sns.histplot(data, kde=True).get_lines()
        if not len(lines):
            return []
        x, y = lines[0].get_data()
        plt.close()
        filt = x >= 0
        x = x[filt]
        y = y[filt]
        sortId = np.argsort(x)
        x = x[sortId]
        y = y[sortId]
        return x[argrelextrema(y, np.less)[0]]

    @property
    def as_columns(self) -> list[str]:
        return [f"{split.field}_{i+1}" for split in self._splits for i in range(len(split.splits))]

    def __iter__(self) -> Generator[BaseSplit, None, None]:
        for split in self._splits:
            yield split

    @classmethod
    def load_from_dict(cls, data: list[dict[str, Union[list[Union[int, float]], str]]]) -> "SplitsCollection":
        split_types = {
            "qualitative": QualitativeSplit,
            "quantitative": QuantitativeSplit,
        }
        return cls([split_types[split["type"]](split["field"], split["splits"]) for split in data])

    @classmethod
    def build(cls, data: pd.DataFrame, qualitatives: list[str] = []) -> "SplitsCollection":
        splits = []
        for field in data.columns:
            if field in qualitatives:
                cls._append_qualitative(splits, field, data[field])
                continue
            cls._append_quantitative(splits, field, data[field])
        return cls(splits)

    def to_dict(self) -> list[dict[str, Union[list[Union[int, float]], str]]]:
        return [
            {
                "field": split.field,
                "splits": split.splits,
                "type": "qualitative" if isinstance(split, QualitativeSplit) else "quantitative",
            }
            for split in self
        ]

    def __str__(self) -> str:
        return str([split for split in self])

    def __repr__(self) -> str:
        return self.__str__()
