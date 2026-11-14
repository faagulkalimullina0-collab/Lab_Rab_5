"""Точка входа: обработка числовых рядов (генерация / чтение / сохранение)."""

from __future__ import annotations

import argparse
import csv
import sys
from typing import List, Optional, Tuple

from num_series import (
    random_series,
    sine_series,
    trend_series,
    summarize,
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
    save_series_json,
    load_series_auto,
    save_series_csv,
    save_results_csv,
)

def build_series(kind: str, n: int, seed: int) -> List[float]:
    """Генерирует ряд заданного типа."""
    if kind == "random":
        return random_series(n, low=-50, high=50, seed=seed)
    if kind == "sine":
        return sine_series(n, amplitude=10, frequency=2, noise=1.5, seed=seed)
    if kind == "trend":
        return trend_series(n, start=0, step=1.0, noise=0.5, seed=seed)
    raise ValueError(f"Неизвестный тип ряда: {kind!r}")



def obtain_series(args: argparse.Namespace) -> Tuple[List[float], str]:
    """Возвращает (ряд, описание источника)."""
    if args.load:
        data = load_series_auto(args.load)
        return data, f"файл: {args.load}"
    data = build_series(args.kind, args.n, args.seed)
    return data, f"сгенерирован ({args.kind}, n={args.n}, seed={args.seed})"





def print_series(title: str, values: List[float], fmt: str = "{:>10.3f}") -> None:
    print(f"\n{title} (n={len(values)}):")
    print(" " + " ".join(fmt.format(v) for v in values))


def print_header(source: str) -> None:
    print("=" * 60)
    print(f"Источник данных: {source}")
    print("-" * 60)


def print_stats(stats: dict) -> None:
    print(f"Среднее арифметическое : {stats['mean']:>10.4f}")
    print(f"Медиана                : {stats['median']:>10.4f}")
    print(f"Размах (max - min)     : {stats['spread']:>10.4f}")
    print(f"min / max              : {stats['min']:>10.4f} / {stats['max']:.4f}")


def print_footer() -> None:
    print("=" * 60)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Алгоритмическая обработка числовых рядов",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Пример: python main.py --kind sine --n 20 --save data/s.json",
    )
    parser.add_argument("--kind", choices=["random", "sine", "trend"], default="sine",
                        help="тип генерируемого ряда")
    parser.add_argument("--n", type=int, default=20,
                        help="количество точек в ряде")
    parser.add_argument("--seed", type=int, default=42,
                        help="зерно ГПСЧ для воспроизводимости")
    parser.add_argument("--load", metavar="PATH",
                        help="загрузить ряд из файла (.json/.txt/.csv); "
                             "отменяет --kind/--n/--seed")
    parser.add_argument("--save", metavar="PATH",
                        help="сохранить ряд в JSON-файл")
    parser.add_argument("--export", metavar="FILE",
                        help="экспортировать ТОЛЬКО ряд в CSV (i, value)")
    parser.add_argument("--save-csv", metavar="FILE",
                        help="сохранить исходный ряд + SMA + EMA + CMA в CSV")
    parser.add_argument("--window", type=int, default=3,
                        help="размер окна для скользящей средней")
    parser.add_argument("--alpha", type=float, default=0.3,
                        help="коэффициент сглаживания для EMA, 0 < alpha <= 1")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    # --- 1. Получаем ряд ---
    try:
        data, source = obtain_series(args)
    except ValueError as err:
        print(f"Ошибка получения ряда: {err}", file=sys.stderr)
        return 1

    # --- 2. Сохраняем исходные данные (до анализа) ---
    if args.save:
        meta = {"source": source}
        if not args.load:
            meta.update({"kind": args.kind, "seed": args.seed})
        try:
            save_series_json(data, args.save, meta=meta)
            print(f"[сохранено JSON] {args.save} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка сохранения JSON: {err}", file=sys.stderr)
            return 1

    if args.export:
        try:
            save_series_csv(data, args.export, header=True)
            print(f"[экспортировано CSV] {args.export} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка экспорта CSV: {err}", file=sys.stderr)
            return 1

    # --- 3. Анализ ---
    try:
        stats = summarize(data)
        sma = simple_moving_average(data, args.window)
        ema = exponential_moving_average(data, args.alpha)
        cma = (
            centered_moving_average(data, args.window)
            if args.window % 2 == 1 else None
        )
    except ValueError as err:
        print(f"Ошибка анализа: {err}", file=sys.stderr)
        return 1

    # --- 3.5. Экспорт расширенного CSV: value + sma + ema + cma ---
    if args.save_csv:
        try:
            save_results_csv(data, args.save_csv, sma=sma, ema=ema, cma=cma)
            print(f"[сохранено результаты CSV] {args.save_csv}")
        except ValueError as err:
            print(f"Ошибка сохранения результатов CSV: {err}", file=sys.stderr)
            return 1

    # --- 4. Вывод ---
    print_header(source)
    print_stats(stats)
    print_series("Исходный ряд", data)
    print_series(f"SMA (window={args.window})", sma)
    print_series(f"EMA (alpha={args.alpha})", ema)
    if cma is not None:
        print_series(f"Центрированное MA (window={args.window})", cma)
    print_footer()
    return 0



if __name__ == "__main__":
    raise SystemExit(main())