from dataclasses import asdict, dataclass, field
from typing import Any, Generator, Optional, Union

import pandas as pd

from .splits import SplitsCollection


@dataclass
class EllipsoidParam:
    field: str
    mean: float
    std: float

    @property
    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class QualitativeValue:
    field: str
    value: float

    @property
    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class State:
    state: tuple[int]
    ellipsoid_params: list[EllipsoidParam] = field(default_factory=list)
    qualitative_values: list[QualitativeValue] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.state = tuple(map(int, self.state))

    def __hash__(self) -> int:
        return hash(self.state)

    def __repr__(self) -> str:
        return self.binary_vector

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, State):
            return self.state == __o.state
        return self.state == __o

    def __xor__(self, __o: object) -> int:
        return self.distance(__o)

    @property
    def binary_vector(self) -> str:
        return "".join(map(str, map(int, self.state)))

    @property
    def as_int(self) -> int:
        return int(self.binary_vector, 2)

    @property
    def normal_ellipsoid_params(self) -> list[EllipsoidParam]:
        return [param for param in self.ellipsoid_params if param.std != 0]

    @property
    def ellipsoid_params_as_qualitatives(self) -> list[QualitativeValue]:
        return [QualitativeValue(param.field, param.mean) for param in self.ellipsoid_params if param.std == 0]

    def _difference_vector(self, state: "State") -> str:
        return "{0:b}".format(state.as_int ^ self.as_int)

    def distance(self, state: Union["State", tuple[int]], /) -> int:
        if isinstance(state, tuple):
            state = State(state)

        return int(sum(map(int, self._difference_vector(state))) / 2)

    def fields_differ(
        self, state: Union["State", tuple[int]], splits_collection: SplitsCollection, /
    ) -> list[dict[str, Any]]:
        if isinstance(state, tuple):
            state = State(state)

        difference_indexes = [
            i
            for i, vector in enumerate(
                splits_collection.split_vector(self._difference_vector(state).zfill(len(self.binary_vector)))
            )
            if any(map(int, vector))
        ]

        splited_vector_self = splits_collection.split_vector(self.binary_vector)
        splited_vector_state = splits_collection.split_vector(state.binary_vector)

        return [
            {
                "field": splits_collection[index].field,
                "self_interval": splits_collection[index].get_value_from_vector(splited_vector_self[index]),
                "state_interval": splits_collection[index].get_value_from_vector(splited_vector_state[index]),
            }
            for index in difference_indexes
        ]

    def __contains__(self, obj: pd.Series) -> bool:
        ellipsoid_value = 0

        for ellipsoid in self.normal_ellipsoid_params:
            value = obj[ellipsoid.field]
            ellipsoid_value += (float(value) - ellipsoid.mean) ** 2 / (ellipsoid.std) ** 2

        return ellipsoid_value <= 1 and all(
            [
                obj[qualitative_value.field] == qualitative_value.value
                for qualitative_value in self.qualitative_values + self.ellipsoid_params_as_qualitatives
            ]
        )

    @property
    def as_dict(self) -> dict:
        return {
            "qualitative_values": [qualitative_value.as_dict for qualitative_value in self.qualitative_values],
            "ellipsoid_params": [ellipsoid_param.as_dict for ellipsoid_param in self.ellipsoid_params],
            "state": self.state,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "State":
        return cls(
            data["state"],
            [EllipsoidParam(**params) for params in data["ellipsoid_params"]],
            [QualitativeValue(**params) for params in data["qualitative_values"]],
        )


class StatesCollection:
    _states: set[State]
    _splits: SplitsCollection

    def __init__(self, states: set[Union[State, tuple[int]]], splits: Optional[SplitsCollection] = None) -> None:
        self._states = set(State(state) if not isinstance(state, State) else state for state in states)
        self._splits = splits

    def __repr__(self) -> str:
        return str(self._states)

    def __contains__(self, obj: pd.Series) -> bool:
        return any([obj in state for state in self._states])

    def __len__(self) -> int:
        return len(self._states)

    def __iter__(self) -> Generator[State, None, None]:
        for state in self._states:
            yield state

    def __getitem__(self, index: int) -> State:
        if not isinstance(index, int):
            raise ValueError("index should be int not {}".format(type(index).__name__))

        return list(self._states)[index]

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, StatesCollection):
            return self._states == __o._states

        return self._states == __o

    def closest_states(self, state: Union["State", tuple[int]], max_distance: int = 3) -> "StatesCollection":
        if isinstance(state, tuple):
            state = State(state)

        return StatesCollection(
            sorted(filter(lambda s: s ^ state <= max_distance, self._states), key=lambda s: s ^ state),
            splits=self._splits,
        )

    def fields_differ(self, state: Union["State", tuple[int]]) -> dict[State, list[dict[str, Any]]]:
        if not self._splits:
            raise ValueError("You should create StatesCollection with SplitsCollection.")
        return {st: st.fields_differ(state, self._splits) for st in self._states}

    def closest_states_with_fields_differ(
        self, state: Union["State", tuple[int]], max_distance: int = 3
    ) -> dict[State, list[dict[str, Any]]]:
        return self.closest_states(state, max_distance=max_distance).fields_differ(state)

    def to_dict(self) -> list[tuple[int]]:
        return [state.as_dict for state in self._states]

    @classmethod
    def build(cls, states: set[tuple[int]], data: pd.DataFrame, splits: SplitsCollection) -> "StatesCollection":
        states_objs = set()
        columns = splits.splits_columns
        qualitative_fields = splits.qualitative_fields
        for state in states:
            state_splits = splits.splits_from_state(state)
            filt = True
            for column in columns:
                if column in qualitative_fields:
                    filt &= data[column] == state_splits[column]
                    continue
                mi, ma = state_splits[column]
                filt &= (data[column] >= mi) & (data[column] < ma)
            values = data[filt]
            ellipsoids = []
            qualitative_values = []
            for column in columns:
                if column in qualitative_fields:
                    qualitative_values.append(
                        QualitativeValue(
                            column,
                            state_splits[column],
                        )
                    )
                    continue
                column_values = values[column]
                if len(column_values) <= 2:
                    mi, ma = state_splits[column]
                    mean, std = (ma + mi) / 2, (ma - mi)
                else:
                    mean, std = column_values.mean(), 3 * column_values.std()
                ellipsoids.append(
                    EllipsoidParam(
                        column,
                        mean,
                        std,
                    )
                )
            states_objs.add(State(state, ellipsoids, qualitative_values))

        return cls(
            states_objs,
            splits=splits,
        )

    @classmethod
    def from_dict(cls, data: list, splits: Optional[SplitsCollection] = None) -> "StatesCollection":
        return cls(
            set(State.from_dict(state) for state in data),
            splits=splits,
        )
