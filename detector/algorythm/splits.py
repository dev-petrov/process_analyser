import abc
from dataclasses import dataclass
from decimal import Decimal
from statistics import mean, stdev
from typing import Generator, Union

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.signal import argrelextrema


@dataclass
class BaseSplit(abc.ABC):
    field: str
    splits: list[Union[tuple[Decimal, Decimal], float, int]]

    @abc.abstractmethod
    def get_value_position(self, value: Union[float, int]) -> tuple[int, bool]:  # pragma: no cover
        pass

    def get_value_from_vector(self, vector: str) -> int:
        for i, value in enumerate(map(int, vector)):
            if value:
                return self.splits[i]


@dataclass
class QuantitativeSplit(BaseSplit):
    def get_value_position(self, value: Union[float, int]) -> tuple[int, bool]:
        index = None
        out_of_range = False
        for i, (min, max) in enumerate(self.splits):
            if value >= min and value < max:
                index = i
                break
        if index is None and value == self.splits[-1][-1]:
            index = i
        if index is None:
            index = 0 if value < self.splits[0][0] else i
            out_of_range = True
        return index, out_of_range


class QualitativeSplit(BaseSplit):
    def get_value_position(self, value: Union[float, int]) -> tuple[int, bool]:
        index = None
        out_of_range = False
        for i, qualitative_value in enumerate(self.splits):
            if value == qualitative_value:
                index = i
                break
        if index is None:
            index = 0 if value < min(self.splits) else i
            out_of_range = True
        return index, out_of_range


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
        serie = values.copy()
        need_round = serie.dtype == "int64"

        def _round(x):
            if need_round:
                x = round(x)
            return float(x)

        local_minimums = list(cls._find_mininmums(serie))

        if not local_minimums:
            return

        local_minimums.insert(0, cls._get_interval(serie[serie < local_minimums[0]])[0])
        local_minimums.append(cls._get_interval(serie[serie >= local_minimums[-1]])[1])

        _splits = [(_round(local_minimums[i]), _round(local_minimums[i + 1])) for i in range(len(local_minimums) - 1)]
        _splits = [(mi, ma) for mi, ma in _splits if mi != ma]

        if len(_splits) < 2:  # pragma no cover
            return

        total = len(serie)
        final_splits = []
        previous_need_append = False
        splits_count = 0

        for mi, ma in _splits:
            percentage = len(serie[(serie >= mi) & (serie < ma)]) / total
            if (percentage < 0.02 and splits_count) or previous_need_append:
                final_splits[splits_count - 1] = (final_splits[splits_count - 1][0], ma)
                previous_need_append = False
                continue
            elif percentage < 0.02:
                previous_need_append = True
            splits_count += 1
            final_splits.append((mi, ma))

        if len(final_splits) < 2:  # pragma no cover
            return

        splits.append(
            QuantitativeSplit(
                field=field,
                splits=final_splits,
            )
        )
        return splits

    @staticmethod
    def _get_interval(data: pd.Series) -> tuple[float, float]:
        if len(data) <= 2:
            return data.min(), data.max()
        return (min(mean(data) - 3 * stdev(data), data.min()), max(mean(data) + 3 * stdev(data), data.max()))

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
        return [f"{split.field}_{i+1}" for split in self for i in range(len(split.splits))]

    @property
    def splits_columns(self) -> list[str]:
        return [split.field for split in self]

    @property
    def qualitative_fields(self) -> list[str]:
        return [split.field for split in self if isinstance(split, QualitativeSplit)]

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

    def __len__(self) -> int:
        return len(self._splits)

    def __getitem__(self, index: int) -> BaseSplit:
        if not isinstance(index, int):
            raise ValueError("index should be int not {}".format(type(index).__name__))

        return self._splits[index]

    def split_vector(self, vector: str) -> list[str]:
        if len(vector) != len(self.as_columns):
            raise ValueError("vector has invalid len")

        splited_vector = []

        i = 0
        for split in self:
            splited_vector.append(vector[i : i + len(split.splits)])  # noqa: E203
            i += len(split.splits)

        return splited_vector

    def splits_from_state(self, state: tuple[int]) -> dict[str, tuple[float, float]]:
        splited_vector = self.split_vector("".join(map(str, map(int, state))))

        return {split.field: split.get_value_from_vector(splited_vector[i]) for i, split in enumerate(self)}
