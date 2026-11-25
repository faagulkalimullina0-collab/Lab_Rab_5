"""Формирование числовых рядов (случайные, синусоида, тренд)."""

import math
import random
from typing import List, Optional


def _validate_n(n: int) -> None:
    """Проверка, что n — положительное целое число."""
    try:
        is_positive_int = (n > 0) and (int(n) == n)
    except (TypeError, ValueError) as err:
        raise ValueError(
            f"n должно быть положительным целым числом "
            f"(получено: {n!r}; причина: {err.args[0]})"
        ) from err
    if not is_positive_int:
        raise ValueError(
            f"n должно быть положительным целым числом (получено: {n!r})"
        )


def random_series(
    n: int,
    low: float = -100.0,
    high: float = 100.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Ряд из n равномерно распределённых случайных чисел на [low, high]."""
    _validate_n(n)
    if low >= high:
        raise ValueError(
            f"low должно быть меньше high (получено: {low} >= {high})"
        )
    rng = random.Random(seed)
    return [rng.uniform(low, high) for _ in range(n)]


def sine_series(
    n: int,
    amplitude: float = 1.0,
    frequency: float = 1.0,
    noise: float = 0.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Синусоидальный ряд с аддитивным шумом (для наглядной проверки MA)."""
    _validate_n(n)
    rng = random.Random(seed)
    return [
        amplitude * math.sin(2 * math.pi * frequency * i / n)
        + (rng.uniform(-noise, noise) if noise else 0.0)
        for i in range(n)
    ]


def trend_series(
    n: int,
    start: float = 0.0,
    step: float = 1.0,
    noise: float = 0.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Линейный тренд (полезно, чтобы увидеть, что MA смещается)."""
    _validate_n(n)
    rng = random.Random(seed)
    return [
        start + step * i + (rng.uniform(-noise, noise) if noise else 0.0)
        for i in range(n)
    ]
def ar1_series(
    n: int = 800,
    phi: float = 0.7,
    seed: Optional[int] = None,
) -> List[float]:
    """
    Генерация временного ряда AR(1).

    x[0] = 0
    x[i] = 0.7 * x[i-1] + random.gauss(0, 1)
    """

    _validate_n(n)

    if not isinstance(phi, (int, float)):
        raise ValueError("phi должен быть числом")

    if abs(phi) >= 1:
        raise ValueError("Для стационарного AR(1) необходимо |phi| < 1")

    rng = random.Random(seed)

    data = [0.0]

    for i in range(1, n):
        value = phi * data[i - 1] + rng.gauss(0, 1)
        data.append(value)

    return data
