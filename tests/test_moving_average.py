"""Тесты модуля moving_average."""

import pytest
from num_series.moving_average import (
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
)


def test_sma_basic():
    assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


def test_sma_length():
    data = list(range(10))
    assert len(simple_moving_average(data, 4)) == 7


def test_sma_window_too_big():
    with pytest.raises(ValueError):
        simple_moving_average([1, 2], 3)


def test_sma_window_zero():
    with pytest.raises(ValueError):
        simple_moving_average([1, 2, 3], 0)


def test_cma_odd_window():
    result = centered_moving_average([1, 2, 3, 4, 5], 3)
    assert result == [2.0, 3.0, 4.0]


def test_cma_even_window_raises():
    with pytest.raises(ValueError):
        centered_moving_average([1, 2, 3, 4], 2)


def test_ema_basic():
    data = [1.0, 2.0, 3.0]
    alpha = 0.5
    expected = [1.0, 1.5, 2.25]
    result = exponential_moving_average(data, alpha)
    assert all(abs(a - b) < 1e-9 for a, b in zip(result, expected))


def test_ema_invalid_alpha():
    with pytest.raises(ValueError):
        exponential_moving_average([1, 2, 3], 0)
    with pytest.raises(ValueError):
        exponential_moving_average([1, 2, 3], 1.5)