from datetime import datetime

import pytest
from pandas import Timestamp

from data_getter import ProcessGetter


@pytest.fixture
def patched_process(mocker):
    process = mocker.patch("data_getter.process_getter.ps.Process", autoscope=True)
    process.return_value = process
    process.name.return_value = "Parent name"
    process.info = {
        "pid": 2,
        "name": "Name",
        "username": "root",
        "terminal": "terminal",
        "num_threads": 1,
        "nice": 18,
        "exe": "some.py",
        "memory_percent": 0.12,
        "cmdline": ["python", "some.py", "run"],
        "create_time": datetime(2022, 10, 1),
        "connections": ["conn"],
        "status": "running",
        "cpu_percent": 0.5,
        "ppid": 1,
        "open_files": ["file1", "file2"],
    }
    return process


@pytest.fixture
def patched_process_iter(mocker, patched_process):
    return mocker.patch(
        "data_getter.process_getter.ps.process_iter", return_value=[patched_process, mocker.Mock(info={"pid": 10})]
    )


@pytest.fixture
def patched_current_thread(mocker):
    return mocker.patch("data_getter.process_getter.threading.current_thread", return_value=mocker.Mock(native_id=10))


def test_process_getter(patched_process, patched_process_iter, patched_current_thread):
    process_getter = ProcessGetter()

    assert process_getter._current_pid == 10

    dttm, data = process_getter.get_data()

    patched_process_iter.assert_called_once_with(
        [
            "pid",
            "name",
            "username",
            "terminal",
            "num_threads",
            "nice",
            "exe",
            "memory_percent",
            "cmdline",
            "create_time",
            "connections",
            "status",
            "cpu_percent",
            "ppid",
            "open_files",
        ]
    )
    patched_process.assert_called_once_with(1)

    assert isinstance(dttm, datetime)

    assert len(data) == 1
    assert data.to_dict("records") == [
        {
            "dttm": dttm.timestamp(),
            "pid": 2,
            "name": "Name",
            "parent_name": "Parent name",
            "username": "root",
            "terminal": "terminal",
            "num_threads": 1,
            "nice": 18,
            "exe": "some.py",
            "memory_percent": 0.12,
            "cmdline": "python some.py run",
            "create_time": Timestamp(2022, 10, 1),
            "connections": 1,
            "status": "running",
            "cpu_percent": 0.5,
            "ppid": 1,
            "open_files": 2,
        }
    ]
    assert str(process_getter) == "ProcessGetter"


def test_no_parent(patched_process, patched_process_iter, patched_current_thread):
    process_getter = ProcessGetter()

    patched_process.reset_mock()
    patched_process.side_effect = ValueError

    dttm, data = process_getter.get_data()

    assert isinstance(dttm, datetime)

    assert len(data) == 1
    assert data.to_dict("records") == [
        {
            "dttm": dttm.timestamp(),
            "pid": 2,
            "name": "Name",
            "parent_name": 0,
            "username": "root",
            "terminal": "terminal",
            "num_threads": 1,
            "nice": 18,
            "exe": "some.py",
            "memory_percent": 0.12,
            "cmdline": "python some.py run",
            "create_time": Timestamp(2022, 10, 1),
            "connections": 1,
            "status": "running",
            "cpu_percent": 0.5,
            "ppid": 1,
            "open_files": 2,
        }
    ]
