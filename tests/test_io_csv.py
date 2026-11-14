"""Тесты модуля io_csv."""

import pytest
from num_series.io_csv import (
    save_series_csv,
    save_results_csv,
    load_results_csv,
)


def test_save_and_load_results(tmp_path):
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    sma = [2.0, 3.0, 4.0]
    ema = [1.0, 1.5, 2.25, 3.125, 4.0625]
    cma = [2.0, 3.0, 4.0]
    path = tmp_path / "res.csv"
    save_results_csv(data, path, sma=sma, ema=ema, cma=cma)
    assert path.exists()

    parsed = load_results_csv(path)
    assert parsed["value"] == data
    assert parsed["sma"] == sma
    assert parsed["ema"] == ema
    assert parsed["cma"] == cma


def test_save_series_csv_empty(tmp_path):
    with pytest.raises(ValueError):
        save_series_csv([], tmp_path / "x.csv")


def test_load_results_csv_missing(tmp_path):
    with pytest.raises(ValueError):
        load_results_csv(tmp_path / "nope.csv")