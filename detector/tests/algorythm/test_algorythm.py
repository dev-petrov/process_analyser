import os

import pandas as pd
import pytest

from detector.algorythm import AnomalyDetector, AnomalyException
from detector.algorythm.splits import SplitsCollection
from detector.algorythm.states import State, StatesCollection


def test_algorythm():
    df = pd.read_csv("./detector/tests/algorythm/test_data.csv")

    detector = AnomalyDetector()

    pytest.raises(ValueError, detector.detect, df).match('You should call "fit" or "load_model" first.')
    pytest.raises(ValueError, detector.classify, df).match('You should call "fit" or "load_model" first.')

    detector.fit(df, clear_anomalies=False)

    classified = detector.classify(df)

    assert "label" in classified.columns

    detector.fit(df)

    assert detector._normal_states == {
        (0.0, 1.0, 0.0, 0.0, 1.0),
        (0.0, 1.0, 1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0, 1.0, 0.0),
    }
    assert detector._columns == ["x1_1", "x1_2", "x2_1", "x2_2", "x2_3"]

    assert str(detector) == "DefaultAnomalyDetector"

    anomalies = detector.detect(df.iloc[20:21, :].reset_index(), raise_exception=False)
    assert len(anomalies) == 1
    assert [anomalies[0]["aggregated"]["x1"], anomalies[0]["aggregated"]["x2"]] == [7.4, 9.744]
    assert anomalies[0]["closest_states"] == [
        [
            {
                "field": "x1",
                "self_interval": (8.75056783919598, 11.430956359906506),
                "state_interval": (6.6656643101493795, 8.75056783919598),
            },
            {
                "field": "x2",
                "self_interval": (13.160798994974874, 14.907887949511057),
                "state_interval": (9.244755936632929, 10.979859296482413),
            },
        ],
        [
            {
                "field": "x1",
                "self_interval": (8.75056783919598, 11.430956359906506),
                "state_interval": (6.6656643101493795, 8.75056783919598),
            }
        ],
        [
            {
                "field": "x2",
                "self_interval": (10.979859296482413, 13.160798994974874),
                "state_interval": (9.244755936632929, 10.979859296482413),
            }
        ],
    ]

    anomalies = detector.detect(df.iloc[19:20, :].reset_index(), raise_exception=False)
    assert len(anomalies) == 0

    pytest.raises(AnomalyException, detector.detect, df.iloc[20:21, :].reset_index())
    pytest.raises(AnomalyException, detector.detect, pd.DataFrame(columns=["x1", "x2"], data=[(-100, 1000)]))

    df["qualitative"] = 1

    detector = AnomalyDetector(qualitatives=["qualitative"])
    detector.fit(df)

    anomalies = detector.detect(df.iloc[20:21, :].reset_index(), raise_exception=False)
    assert len(anomalies) == 1

    anomalies = detector.detect(df.iloc[19:20, :].reset_index(), raise_exception=False)
    assert len(anomalies) == 0

    detector.save_model("./detector/tests/algorythm/__test_save.json")

    detector_new = AnomalyDetector()
    detector_new.load_model("./detector/tests/algorythm/__test_save.json")

    assert detector._normal_states == detector_new._normal_states

    os.remove("./detector/tests/algorythm/__test_save.json")


def test_splits_collection():
    data = pd.DataFrame(
        columns=["float", "int", "int_no_min", "character"],
        data=[
            (1.1, 1, 3, 1),
            (2.34, 2, 3, 1),
            (1.1, 2, 3, 2),
            (1.1, 2, 3, 2),
            (1.1, 2, 3, 2),
            (1.1, 8, 3, 2),
            (1.1, 8, 3, 1),
            (1.1, 8, 3, 2),
            (1.1, 8, 3, 1),
            (1.1, 8, 3, 2),
            (1.1, 10, 3, 1),
        ],
    )

    splits = SplitsCollection.build(data, qualitatives=["character"])

    pytest.raises(ValueError, splits.__getitem__, "str_index").match("index should be int not str")
    pytest.raises(ValueError, splits.split_vector, "00").match("vector has invalid len")

    assert splits._splits[-1].get_value_position(1) == 0

    assert str(splits) == (
        "[QuantitativeSplit(field='float', splits=[(1.1, 1.8352763819095477),"
        " (1.8352763819095477, 2.34)]), QuantitativeSplit(field='int', splits=[(0, 5), (5, 11)]), "
        "QualitativeSplit(field='character', splits=[1, 2])]"
    )

    assert repr(splits) == str(splits)
    assert len(splits) == 3


def test_states_collection():
    df = pd.read_csv("./detector/tests/algorythm/test_data.csv")
    detector = AnomalyDetector()
    detector.fit(df)

    anomaly_vector = (1.0, 0.0, 1.0, 0.0, 0.0)

    closest_states = detector.get_closest_states(anomaly_vector, max_distance=1)

    assert closest_states == {
        (0.0, 1.0, 1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0, 1.0, 0.0),
    }

    assert closest_states.fields_differ(anomaly_vector) == {
        State((1.0, 0.0, 0.0, 1.0, 0.0)): [
            {
                "field": "x2",
                "self_interval": (10.979859296482413, 13.160798994974874),
                "state_interval": (9.244755936632929, 10.979859296482413),
            }
        ],
        State((0.0, 1.0, 1.0, 0.0, 0.0)): [
            {
                "field": "x1",
                "self_interval": (8.75056783919598, 11.430956359906506),
                "state_interval": (6.6656643101493795, 8.75056783919598),
            }
        ],
    }

    assert State((0.0, 1.0, 0.0, 0.0, 1.0)) ^ anomaly_vector == 2

    assert len(detector._normal_states) == 3
    assert detector._normal_states[0] == State((0.0, 1.0, 0.0, 0.0, 1.0))

    pytest.raises(ValueError, detector._normal_states.__getitem__, "str_index").match("index should be int not str")

    collection = StatesCollection(
        {
            (0.0, 1.0, 0.0, 0.0, 1.0),
            (0.0, 1.0, 1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0, 1.0, 0.0),
        }
    )

    pytest.raises(ValueError, collection.fields_differ, anomaly_vector).match(
        "You should create StatesCollection with SplitsCollection."
    )

    assert str(detector._normal_states[0]) == "01001"
    assert str(detector._normal_states) == "{01001, 01100, 10010}"
