"""Тесты модуля num_series.io_json с использованием фикстуры tmp_path."""
import json
import pytest

from num_series.io_json import save_series_json, load_series_json


class TestSaveAndLoadJSON:
    def test_roundtrip_with_meta(self, tmp_path):
        file_path = tmp_path / "subdir" / "series.json"
        original = [1.0, 2.5, -3.75, 4.0]
        save_series_json(original, file_path, meta={"kind": "sine", "seed": 42})
        assert file_path.exists()
        loaded, meta = load_series_json(file_path, with_meta=True)
        assert loaded == pytest.approx(original)
        assert meta["kind"] == "sine"
        assert meta["seed"] == 42
        assert meta["n"] == len(original)
        assert "created" in meta

    def test_load_bare_list_json(self, tmp_path):
        file_path = tmp_path / "bare.json"
        file_path.write_text("[10, 20.5, -5]", encoding="utf-8")
        loaded, meta = load_series_json(file_path, with_meta=True)
        assert loaded == [10.0, 20.5, -5.0]
        assert meta == {}

    def test_save_empty_raises(self, tmp_path):
        with pytest.raises(ValueError, match="пуст"):
            save_series_json([], tmp_path / "empty.json")

    @pytest.mark.parametrize("bad_data", [[1, "two", 3], [1, True, 3], [None]])
    def test_save_non_numeric_raises(self, tmp_path, bad_data):
        with pytest.raises(ValueError, match="не является числом"):
            save_series_json(bad_data, tmp_path / "bad.json")

    def test_load_missing_file_raises(self, tmp_path):
        with pytest.raises(ValueError, match="не найден"):
            load_series_json(tmp_path / "no_such_file.json")

    def test_load_broken_json_raises(self, tmp_path):
        file_path = tmp_path / "broken.json"
        file_path.write_text("{not valid json", encoding="utf-8")
        with pytest.raises(ValueError, match="корректным JSON"):
            load_series_json(file_path)

    def test_load_missing_data_key_raises(self, tmp_path):
        file_path = tmp_path / "no_data.json"
        file_path.write_text(json.dumps({"meta": {"n": 0}}), encoding="utf-8")
        with pytest.raises(ValueError, match="нет поля 'data'"):
            load_series_json(file_path)

    def test_load_empty_data_raises(self, tmp_path):
        file_path = tmp_path / "empty_data.json"
        file_path.write_text(json.dumps({"data": []}), encoding="utf-8")
        with pytest.raises(ValueError, match="пуст"):
            load_series_json(file_path)
