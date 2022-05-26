from dataclasses import dataclass
from typing import Any, Generator, Optional, Union

from .splits import SplitsCollection


@dataclass
class State:
    state: tuple[int]

    def __post_init__(self) -> None:
        self.state = tuple(map(int, self.state))

    def __hash__(self) -> int:
        return hash(self.state)

    def __repr__(self) -> str:
        return self.binary_vector

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, State):
            return self.state == __o.state
        return self.state == __o

    @property
    def binary_vector(self) -> str:
        return "".join(map(str, map(int, self.state)))

    @property
    def as_int(self) -> int:
        return int(self.binary_vector, 2)

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


class StatesCollection:
    _states: set[State]
    _splits: SplitsCollection

    def __init__(self, states: set[Union[State, tuple[int]]], splits: Optional[SplitsCollection] = None) -> None:
        self._states = set(State(state) if not isinstance(state, State) else state for state in states)
        self._splits = splits

    def __contains__(self, obj: Any) -> bool:
        return obj in self._states

    def __len__(self) -> int:
        return len(self._states)

    def __iter__(self) -> Generator[State, None, None]:
        for state in self._states:
            yield state

    def __getitem__(self, index: int) -> State:
        if not isinstance(index, int):
            raise ValueError("index should be int not {}".format(type(index)))

        return list(self._states)[index]

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, StatesCollection):
            return self._states == __o._states

        return self._states == __o

    def closest_states(self, state: Union["State", tuple[int]], max_distance: int = 3) -> "StatesCollection[State]":
        if isinstance(state, tuple):
            state = State(state)

        return StatesCollection(
            sorted(filter(lambda s: s.distance(state) <= max_distance, self._states), key=lambda s: s.distance(state)),
            splits=self._splits,
        )

    def fields_differ(self, state: Union["State", tuple[int]]) -> dict[State, list[dict[str, Any]]]:
        if not self._splits:
            raise ValueError("You should create StatesCollection with SplitsCollection.")
        return {st: st.fields_differ(state, self._splits) for st in self._states}

    def to_dict(self) -> list[tuple[int]]:
        return [state.state for state in self._states]
