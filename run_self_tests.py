"""Запуск минимальных тестов без pytest."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from num_series import (
    random_series, sine_series, trend_series,
    mean, median, spread, summarize,
    simple_moving_average, centered_moving_average, exponential_moving_average,
)


def check(name, cond):
    print(("OK   " if cond else "FAIL ") + name)
    if not cond:
        raise SystemExit(1)


def main() -> int:
    check("random len", len(random_series(10, seed=1)) == 10)
    check("random reproducible", random_series(5, seed=42) == random_series(5, seed=42))
    check("sine len", len(sine_series(20, seed=1)) == 20)
    check("trend simple", trend_series(5, noise=0.0) == [0.0, 1.0, 2.0, 3.0, 4.0])

    check("mean", mean([1, 2, 3, 4, 5]) == 3.0)
    check("median odd", median([3, 1, 2]) == 2.0)
    check("median even", median([1, 2, 3, 4]) == 2.5)
    check("spread", spread([1, 5, 2, 9]) == 8.0)
    check("summarize", summarize([1, 2, 3])["count"] == 3)

    check("sma", simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0])
    check("cma", centered_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0])

    ema = exponential_moving_average([1.0, 2.0, 3.0], 0.5)
    check("ema", all(abs(a - b) < 1e-9 for a, b in zip(ema, [1.0, 1.5, 2.25])))

    # проверки ошибок
    try:
        simple_moving_average([1, 2], 3)
        check("sma window error", False)
    except ValueError:
        check("sma window error", True)

    try:
        mean([])
        check("empty mean error", False)
    except ValueError:
        check("empty mean error", True)

    print("\nВсе проверки пройдены.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())