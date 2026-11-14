"""Пакет алгоритмической обработки числовых рядов."""

from .generator import random_series, sine_series, trend_series
from .stats import mean, median, spread, summarize
from .moving_average import (
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
)
from .io_json import save_series_json, load_series_json
from .io_file import load_series_txt, load_series_csv, load_series_auto
from .io_csv import (
    save_series_csv,
    save_results_csv,
    load_results_csv,
)

__all__ = [
    # генерация
    "random_series", "sine_series", "trend_series",
    # статистика
    "mean", "median", "spread", "summarize",
    # скользящие средние
    "simple_moving_average", "centered_moving_average", "exponential_moving_average",
    # ввод-вывод JSON
    "save_series_json", "load_series_json",
    # чтение простых текстовых файлов
    "load_series_txt", "load_series_csv", "load_series_auto",
    # ввод-вывод CSV (расширенный)
    "save_series_csv", "save_results_csv", "load_results_csv",
]

__version__ = "1.2.0"