from collectors import CsvCollector


def test_csv_collector(mocker, patched_file_reader, processes_data):
    dttm, data = processes_data
    filename = "some_file.csv"
    patcher_file_reader, patched_file = patched_file_reader
    patched_open = mocker.patch("collectors.csv_collector.open", return_value=patcher_file_reader)

    collector = CsvCollector(None)

    assert collector._filename == "collected_data.csv"

    collector = CsvCollector(filename)

    assert collector._filename == filename
    assert str(collector) == f"CsvCollector, filename: {filename}"
    collector.collect(data)

    patched_open.assert_called_once_with(filename, "a")
    patched_file.write.assert_called_once_with(data.to_csv(header=False, index=False))
