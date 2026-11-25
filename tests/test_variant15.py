"""Самостоятельное задание (вариант 15): AR(1)-ряд, автокорреляция lag-1,
сравнение сглаживания SMA и EMA."""
import math

import pytest

from num_series.generator import ar1_series
from num_series.stats import lag1_autocorrelation
from num_series import simple_moving_average, exponential_moving_average


def roughness(series):
    """Средний модуль соседних перепадов — мера «изрезанности» ряда."""
    return sum(abs(series[i] - series[i - 1]) for i in range(1, len(series))) / (len(series) - 1)


class TestAr1Generator:
    def test_length(self):
        assert len(ar1_series(50, seed=15)) == 50

    def test_reproducible(self):
        assert ar1_series(30, seed=15) == ar1_series(30, seed=15)

    def test_first_element_is_zero(self):
        assert ar1_series(10, seed=3)[0] == 0.0

    def test_positive_autocorrelation(self):
        data = ar1_series(500, seed=15)
        assert lag1_autocorrelation(data) > 0.5

    def test_invalid_n(self):
        with pytest.raises(ValueError):
            ar1_series(0, seed=1)


class TestLag1Autocorrelation:
    def test_white_noise_near_zero(self):
        from num_series import random_series
        data = random_series(2000, low=-1, high=1, seed=42)
        assert abs(lag1_autocorrelation(data)) < 0.1

    def test_perfect_trend_near_one(self):
        data = [float(i) for i in range(100)]
        assert lag1_autocorrelation(data) > 0.95

    def test_manual_reference(self):
        # ручной эталон для [0, 1, 2, 3, 4]
        data = [0.0, 1.0, 2.0, 3.0, 4.0]
        m = 2.0
        c1 = sum((data[i] - m) * (data[i - 1] - m) for i in range(1, 5))
        c0 = sum((x - m) ** 2 for x in data)
        assert math.isclose(lag1_autocorrelation(data), c1 / c0, rel_tol=1e-12)

    def test_too_short_raises(self):
        with pytest.raises(ValueError):
            lag1_autocorrelation([1.0])

    def test_constant_series_returns_one(self):
        assert lag1_autocorrelation([5.0] * 10) == 1.0


class TestSmoothingVariant15:
    def test_sma_reduces_roughness(self):
        data = ar1_series(300, seed=15)
        assert roughness(simple_moving_average(data, 10)) < roughness(data)

    def test_ema_reduces_roughness(self):
        data = ar1_series(300, seed=15)
        assert roughness(exponential_moving_average(data, 2 / 11)) < roughness(data)

    def test_ema_smoothes_more_with_smaller_alpha(self):
        # краевой кейс: EMA с меньшим alpha сглаживает сильнее SMA того же окна
        data = ar1_series(300, seed=15)
        r_sma = roughness(simple_moving_average(data, 10))
        r_ema = roughness(exponential_moving_average(data, 0.05))
        assert r_ema < r_sma

    def test_ema_roughness_decreases_with_alpha(self):
        # чем меньше alpha, тем сильнее сглаживание EMA
        data = ar1_series(300, seed=15)
        r_big = roughness(exponential_moving_average(data, 0.5))
        r_small = roughness(exponential_moving_average(data, 0.05))
        assert r_small < r_big
