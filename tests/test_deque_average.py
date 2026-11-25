"""Тесты модуля num_series.deque_average и дифференциальная проверка с list-версией."""
import random
import pytest

from num_series.moving_average import (
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
)
from num_series.deque_average import (
    simple_moving_average_deque,
    centered_moving_average_deque,
    exponential_moving_average_deque,
)


class TestDequeMovingAverage:
    def test_sma_classic(self):
        assert simple_moving_average_deque([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]

    def test_sma_matches_list_implementation(self):
        rng = random.Random(42)
        data = [rng.uniform(-100, 100) for _ in range(200)]
        for w in (1, 3, 7, 25, 200):
            expected = simple_moving_average(data, w)
            actual = simple_moving_average_deque(data, w)
            assert actual == pytest.approx(expected)

    def test_cma_matches_list_implementation(self):
        rng = random.Random(7)
        data = [rng.uniform(-50, 50) for _ in range(60)]
        for w in (1, 3, 5, 11):
            assert centered_moving_average_deque(data, w) == pytest.approx(
                centered_moving_average(data, w)
            )

    def test_cma_even_window_raises(self):
        with pytest.raises(ValueError, match="нечётного"):
            centered_moving_average_deque([1, 2, 3, 4], 2)

    def test_ema_matches_list_implementation(self):
        rng = random.Random(13)
        data = [rng.uniform(-10, 10) for _ in range(80)]
        for alpha in (0.1, 0.3, 0.7, 1.0):
            assert exponential_moving_average_deque(data, alpha) == pytest.approx(
                exponential_moving_average(data, alpha)
            )

    def test_empty_and_invalid_window(self):
        with pytest.raises(ValueError, match="пуст"):
            simple_moving_average_deque([], 3)
        with pytest.raises(ValueError, match="больше длины"):
            simple_moving_average_deque([1, 2], 5)
        with pytest.raises(ValueError):
            exponential_moving_average_deque([1, 2, 3], alpha=0.0)
