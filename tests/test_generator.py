"""Тесты модуля generator."""

import pytest
from num_series.generator import random_series, sine_series, trend_series


def test_random_series_length():
    data = random_series(10, seed=1)
    assert len(data) == 10


def test_random_series_reproducible():
    a = random_series(5, seed=42)
    b = random_series(5, seed=42)
    assert a == b


def test_random_series_bounds():
    data = random_series(100, low=0, high=1, seed=7)
    assert all(0 <= v <= 1 for v in data)


def test_random_series_invalid_low_high():
    with pytest.raises(ValueError):
        random_series(5, low=10, high=1)


def test_invalid_n():
    with pytest.raises(ValueError):
        random_series(0)
    with pytest.raises(ValueError):
        random_series(-3)


def test_sine_series_length():
    assert len(sine_series(20, seed=1)) == 20


def test_trend_series_monotonic_without_noise():
    data = trend_series(5, start=0, step=1.0, noise=0.0)
    assert data == [0.0, 1.0, 2.0, 3.0, 4.0]