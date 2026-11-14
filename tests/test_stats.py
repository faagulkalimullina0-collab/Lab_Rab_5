"""Тесты модуля stats."""

import pytest
from num_series.stats import mean, median, spread, summarize


def test_mean():
    assert mean([1, 2, 3, 4, 5]) == 3.0


def test_median_odd():
    assert median([3, 1, 2]) == 2.0


def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5


def test_spread():
    assert spread([1, 5, 2, 9]) == 8.0


def test_summarize_keys():
    s = summarize([1, 2, 3])
    assert set(s) == {"count", "mean", "median", "spread", "min", "max"}
    assert s["count"] == 3


def test_empty_raises():
    for fn in (mean, median, spread, summarize):
        with pytest.raises(ValueError):
            fn([])