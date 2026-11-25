"""Базовые статистические показатели: среднее, медиана, размах."""

import math
from typing import Dict, Sequence


def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")


def mean(data: Sequence[float]) -> float:
    """Среднее арифметическое."""
    _ensure_not_empty(data)
    return sum(data) / len(data)


def median(data: Sequence[float]) -> float:
    """Медиана (устойчива к выбросам)."""
    _ensure_not_empty(data)
    s = sorted(data)
    k = len(s) // 2
    if len(s) % 2:
        return float(s[k])
    return (s[k - 1] + s[k]) / 2.0


def spread(data: Sequence[float]) -> float:
    """Размах ряда: max - min."""
    _ensure_not_empty(data)
    return float(max(data) - min(data))


def summarize(data: Sequence[float]) -> Dict[str, float]:
    """Сводный отчёт: count, mean, median, spread, min, max."""
    _ensure_not_empty(data)
    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": float(min(data)),
        "max": float(max(data)),
    }
def autocorrelation_lag1(data: Sequence[float]) -> float:
    """
    Автокорреляция первого порядка.

    Рассчитывает корреляцию между x[i] и x[i-1].
    """

    if len(data) < 2:
        raise ValueError("Необходимо минимум 2 значения")

    x = data[:-1]
    y = data[1:]

    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    numerator = sum(
        (x[i] - mean_x) * (y[i] - mean_y)
        for i in range(len(x))
    )

    denominator_x = sum(
        (v - mean_x) ** 2 for v in x
    )

    denominator_y = sum(
        (v - mean_y) ** 2 for v in y
    )

    denominator = math.sqrt(
        denominator_x * denominator_y
    )

    if denominator == 0:
        return 0.0

    return numerator / denominator
def lag1_autocorrelation(data):
    """Выборочная автокорреляция с лагом 1.

    r(1) = sum((x[i] - m) * (x[i-1] - m)) / sum((x[i] - m)^2),
    где m — среднее ряда. Для константного ряда возвращает 1.0.
    """
    if not isinstance(data, (list, tuple)) or len(data) < 2:
        raise ValueError("Автокорреляция требует ряд длиной не менее 2 элементов")
    m = sum(data) / len(data)
    c0 = sum((x - m) ** 2 for x in data)          # дисперсия (несмещённая на 1/n)
    if c0 == 0:
        return 1.0
    c1 = sum((data[i] - m) * (data[i - 1] - m) for i in range(1, len(data)))
    return c1 / c0

