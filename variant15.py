import argparse
import csv

from num_series.generator import ar1_series

from num_series.stats import (
    autocorrelation_lag1,
    mean
)

from num_series.moving_average import (
    simple_moving_average,
    exponential_moving_average
)


def calculate_roughness(data):
    """Средний квадрат разности соседних значений."""

    if len(data) < 2:
        return 0.0

    return sum(
        (data[i] - data[i - 1]) ** 2
        for i in range(1, len(data))
    ) / (len(data) - 1)


def main():

    parser = argparse.ArgumentParser(
        description="Лабораторная работа 5. Вариант 15"
    )

    parser.add_argument(
        "--n",
        type=int,
        default=800,
        help="Количество элементов"
    )

    parser.add_argument(
        "--window",
        type=int,
        default=10,
        help="Размер окна SMA"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42
    )

    args = parser.parse_args()

    if args.n < 2:
        parser.error("n должно быть не меньше 2")

    if args.window < 1 or args.window > args.n:
        parser.error("Некорректный размер окна")

    # 1. Генерация AR(1)

    data = ar1_series(
        n=args.n,
        phi=0.7,
        seed=args.seed
    )
    print("=" * 55)
    print("ЛАБОРАТОРНАЯ РАБОТА №5")
    print("ВАРИАНТ 15")
    print("=" * 55)

    print("\n1. Генерация ряда AR(1)")
    print("Количество элементов:", len(data))
    print("Первые 10 значений:")
    print([round(x, 4) for x in data[:10]])

    # 2. Статистика
    print("\n2. Статистические показатели")

    print("Среднее значение:", round(mean(data), 5))

    correlation = autocorrelation_lag1(data)

    print(
        "Автокорреляция lag-1:",
        round(correlation, 5)
    )

    # 3. SMA

    sma = simple_moving_average(
        data,
        args.window
    )

    print("\n3. Простая скользящая средняя SMA")

    print("Размер окна:", args.window)
    print("Количество значений:", len(sma))

    print([round(x, 4) for x in sma[:10]])

    # 4. EMA

    # Меньшее alpha обеспечивает более сильное сглаживание.
    alpha = 1 / (args.window + 1)

    ema = exponential_moving_average(
        data,
        alpha
    )

    print("\n4. Экспоненциальная скользящая средняя EMA")

    print("Alpha:", round(alpha, 5))
    print("Количество значений:", len(ema))

    print([round(x, 4) for x in ema[:10]])

    # 5. Сравнение сглаживания

    print("\n5. Сравнение SMA и EMA")

    # Сравниваем одинаковые временные участки.
    sma_part = sma
    ema_part = ema[args.window - 1:]

    sma_r = calculate_roughness(sma_part)
    ema_r = calculate_roughness(ema_part)

    print("Изменчивость SMA:", round(sma_r, 7))
    print("Изменчивость EMA:", round(ema_r, 7))

    if ema_r < sma_r:
        print("EMA сглаживает сильнее SMA")
    else:
        print("EMA не сглаживает сильнее SMA")

    # 6. Сохранение CSV

    with open(
        "variant15_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "AR1",
            "SMA",
            "EMA"
        ])

        for i in range(args.n):

            sma_value = (
                sma[i - args.window + 1]
                if i >= args.window - 1
                else ""
            )

            writer.writerow([
                data[i],
                sma_value,
                ema[i]
            ])

    print("\n6. Результаты сохранены")

    print("Файл: variant15_results.csv")

    print("\nРАБОТА ЗАВЕРШЕНА")




if __name__ == "__main__":
    main()