import os
from decimal import Decimal

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

    assert str(detector) == "AnomalyDetector"

    anomalies = detector.detect(df.iloc[20:21, :].reset_index(), raise_exception=False)
    assert len(anomalies) == 1
    assert [anomalies[0]["aggregated"]["x1"], anomalies[0]["aggregated"]["x2"]] == [7.4, 9.744]
    assert anomalies[0]["closest_states"] == [
        [
            {
                "field": "x1",
                "self_interval": (
                    Decimal("8.75056783919598046850296668708324432373046875"),
                    Decimal("11.430956359906506492052358225919306278228759765625"),
                ),
                "state_interval": (
                    Decimal("6.6656643101493813219349249266088008880615234375"),
                    Decimal("8.75056783919598046850296668708324432373046875"),
                ),
            },
            {
                "field": "x2",
                "self_interval": (
                    Decimal("13.1607989949748738212065291008912026882171630859375"),
                    Decimal("14.9078879495110587782846778281964361667633056640625"),
                ),
                "state_interval": (
                    Decimal("9.2447559366329290497787951608188450336456298828125"),
                    Decimal("10.979859296482413100193298305384814739227294921875"),
                ),
            },
        ],
        [
            {
                "field": "x1",
                "self_interval": (
                    Decimal("8.75056783919598046850296668708324432373046875"),
                    Decimal("11.430956359906506492052358225919306278228759765625"),
                ),
                "state_interval": (
                    Decimal("6.6656643101493813219349249266088008880615234375"),
                    Decimal("8.75056783919598046850296668708324432373046875"),
                ),
            }
        ],
        [
            {
                "field": "x2",
                "self_interval": (
                    Decimal("10.979859296482413100193298305384814739227294921875"),
                    Decimal("13.1607989949748738212065291008912026882171630859375"),
                ),
                "state_interval": (
                    Decimal("9.2447559366329290497787951608188450336456298828125"),
                    Decimal("10.979859296482413100193298305384814739227294921875"),
                ),
            }
        ],
    ]

    anomalies = detector.detect(df.iloc[19:20, :].reset_index(), raise_exception=False)
    assert len(anomalies) == 0

    pytest.raises(AnomalyException, detector.detect, df.iloc[20:21, :].reset_index())
    pytest.raises(AnomalyException, detector.detect, pd.DataFrame(columns=["x1", "x2"], data=[(-100, 1000)]))

    assert detector.detect(df.iloc[20:21, :].reset_index(), raise_exception=False, max_difference_to_skip=1) == []

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
            (8.1, 2, 3, 2),
            (8.25, 2, 3, 2),
            (2.412, 8, 3, 2),
            (1.1, 8, 3, 1),
            (9.89, 8, 3, 2),
            (1.1, 8, 3, 1),
            (2.67, 8, 3, 2),
            (1.156, 10, 3, 1),
        ],
    )

    splits = SplitsCollection.build(data, qualitatives=["character"])

    pytest.raises(ValueError, splits.__getitem__, "str_index").match("index should be int not str")
    pytest.raises(ValueError, splits.split_vector, "00").match("vector has invalid len")

    assert splits._splits[-1].get_value_position(1) == 0

    assert str(splits) == (
        "[QuantitativeSplit(field='float', splits=[(-0.5126697208058462, 6.356331658291458),"
        " (6.356331658291458, 11.725643000913047)]), QuantitativeSplit(field='int', splits="
        "[(0.0, 5.0), (5.0, 11.0)]), QualitativeSplit(field='character', splits=[1, 2])]"
    )

    assert repr(splits) == str(splits)
    assert len(splits) == 3

    data = pd.DataFrame(
        columns=["float", "int"],
        data=[
            (1.1, 1),
            *[(2.34, 8) for _ in range(30)],
            (1.1, 1),
            (1.1, 8),
            (8.1, 9),
            *[(8.25, 9) for _ in range(30)],
            (2.412, 8),
            (1.1, 8),
            (9.89, 8),
            *[(9.89, 8) for _ in range(30)],
            (1.1, 15),
            *[(2.67, 16) for _ in range(20)],
            (1.156, 16),
            *[(1.156, 17) for _ in range(30)],
            (1.156, 16),
            (1.156, 20),
        ],
    )

    splits = SplitsCollection.build(data)
    assert len(splits) == 2
    assert str(splits) == (
        "[QuantitativeSplit(field='float', splits=[(-0.10085921505940987,"
        " 5.561256281407035), (5.561256281407035, 11.55562561428394)]), "
        "QuantitativeSplit(field='int', splits=[(1.0, 13.0), (13.0, 20.0)])]"
    )
    assert SplitsCollection._get_interval(data.loc[:1, "int"]) == (1, 8)


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
        State((0.0, 1.0, 1.0, 0.0, 0.0)): [
            {
                "field": "x1",
                "self_interval": (
                    Decimal("8.75056783919598046850296668708324432373046875"),
                    Decimal("11.430956359906506492052358225919306278228759765625"),
                ),
                "state_interval": (
                    Decimal("6.6656643101493813219349249266088008880615234375"),
                    Decimal("8.75056783919598046850296668708324432373046875"),
                ),
            }
        ],
        State((1.0, 0.0, 0.0, 1.0, 0.0)): [
            {
                "field": "x2",
                "self_interval": (
                    Decimal("10.979859296482413100193298305384814739227294921875"),
                    Decimal("13.1607989949748738212065291008912026882171630859375"),
                ),
                "state_interval": (
                    Decimal("9.2447559366329290497787951608188450336456298828125"),
                    Decimal("10.979859296482413100193298305384814739227294921875"),
                ),
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
