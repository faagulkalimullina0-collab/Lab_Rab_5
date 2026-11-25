"""Скользящие средние на основе collections.deque."""

from collections import deque
from typing import Deque, List, Sequence


def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError(
            "Ряд пуст: расчёт скользящей средней невозможен"
        )


def _check_window(window: int, n: int) -> None:
    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError("window должен быть целым числом")

    if window < 1:
        raise ValueError("window должен быть >= 1")

    if window > n:
        raise ValueError("window больше длины ряда")


def _check_alpha(alpha: float) -> None:
    if not 0 < alpha <= 1:
        raise ValueError("alpha должен быть в (0, 1]")


def simple_moving_average_deque(
    data: Sequence[float],
    window: int
) -> List[float]:
    """Простая скользящая средняя через deque."""

    _ensure_not_empty(data)
    _check_window(window, len(data))

    buf: Deque[float] = deque(maxlen=window)

    running = 0.0
    result = []

    for i, x in enumerate(data):

        if len(buf) == window:
            running -= buf[0]

        buf.append(x)
        running += x

        if i >= window - 1:
            result.append(running / window)

    return result


def centered_moving_average_deque(
    data: Sequence[float],
    window: int
) -> List[float]:
    """Центрированная скользящая средняя через deque."""

    _ensure_not_empty(data)
    _check_window(window, len(data))

    if window % 2 == 0:
        raise ValueError(
            "Центрированное MA требует нечётного окна"
        )

    buf: Deque[float] = deque(maxlen=window)

    running = 0.0
    result = []

    for x in data:

        if len(buf) == window:
            running -= buf[0]

        buf.append(x)
        running += x

        if len(buf) == window:
            result.append(running / window)

    return result


def exponential_moving_average_deque(
    data: Sequence[float],
    alpha: float
) -> List[float]:
    """Экспоненциальная скользящая средняя."""

    _ensure_not_empty(data)
    _check_alpha(alpha)

    prev = float(data[0])
    result = [prev]

    for x in data[1:]:
        prev = alpha * x + (1 - alpha) * prev
        result.append(prev)

    return result


__all__ = [
    "simple_moving_average_deque",
    "centered_moving_average_deque",
    "exponential_moving_average_deque",
]
