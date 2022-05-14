import os

import pandas as pd

from detector.algorythm import AnomalyDetector, AnomalyException
from detector.algorythm.splits import SplitsCollection


def test_algorythm():
    df = pd.read_csv("./detector/tests/algorythm/test_data.csv")

    detector = AnomalyDetector()

    detail = None

    try:
        detector.detect(df)
    except ValueError as e:
        detail = str(e)

    assert detail == 'You should call "fit" or "load_model" first.'

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
    assert [anomalies[0].x1, anomalies[0].x2] == [7.4, 9.744]

    anomalies = detector.detect(df.iloc[19:20, :].reset_index(), raise_exception=False)
    assert len(anomalies) == 0

    exception_raised = False

    try:
        detector.detect(df.iloc[20:21, :].reset_index())
    except AnomalyException:
        exception_raised = True

    assert exception_raised

    exception_raised = False

    try:
        detector.detect(pd.DataFrame(columns=["x1", "x2"], data=[(-100, 1000)]))
    except AnomalyException:
        exception_raised = True

    assert exception_raised

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

    assert splits._splits[-1].get_value_position(1) == 0

    assert str(splits) == (
        "[QuantitativeSplit(field='float', splits=[(1.1, 1.8352763819095477),"
        " (1.8352763819095477, 2.34)]), QuantitativeSplit(field='int', splits=[(0, 5), (5, 11)]), "
        "QuantitativeSplit(field='int_no_min', splits=[(3, 3)]), "
        "QualitativeSplit(field='character', splits=[1, 2])]"
    )

    assert repr(splits) == str(splits)
