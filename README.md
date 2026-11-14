# Лабораторная работа №5 — Алгоритмическая обработка числовых рядов

**Студент:** Калимуллина Фаягуль, группа БЦШ02-26-02

Модульное консольное приложение: генерация числовых рядов, расчёт базовых
статистических показателей и скользящих средних.

## Структура

```
num_series/           # пакет
  __init__.py         # публичный API
  generator.py        # генерация рядов (random / sine / trend)
  stats.py            # mean, median, spread, summarize
  moving_average.py   # SMA, CMA, EMA
  io_json.py          # сохранение/чтение JSON
  io_file.py          # чтение txt/csv
tests/                # pytest-тесты
main.py               # CLI
run_self_tests.py     # запуск проверок без pytest
```

## Запуск

```bash
# Генерация + анализ
python main.py --kind sine --n 20 --window 3 --alpha 0.3 --seed 7

# Случайный ряд, сохранение в JSON
python main.py --kind random --n 50 --save data/random.json

# Загрузка из JSON
python main.py --load data/random.json --window 5

# Экспорт в CSV
python main.py --kind trend --n 30 --export out.csv
# Сохранить только исходный ряд в CSV
python main.py --kind trend --n 30 --export out.csv

# Сохранить исходный ряд + SMA + EMA + CMA в один CSV
python main.py --kind sine --n 20 --window 3 --save-csv results.csv
```

## Параметры CLI

| Аргумент         | Описание                              |
|------------------|---------------------------------------|
| `--kind`         | тип ряда: `random` / `sine` / `trend` |
| `--n`            | количество точек                      |
| `--seed`         | зерно ГПСЧ                            |
| `--window`       | окно скользящей средней               |
| `--alpha`        | коэффициент EMA, `0 < alpha <= 1`     |
| `--load PATH`    | загрузить ряд из файла                |
| `--save PATH`    | сохранить ряд в JSON                  |
| `--export FILE`  | экспорт в CSV                         |
| `--save-csv FILE` | сохранить value + sma + ema + cma в CSV |

## Тесты

```bash
python run_self_tests.py    # без pytest — гарантированно работает
pytest -v                   # если установлен pytest
```

## Особенности реализации

- SMA реализован **через бегущую сумму** — O(n), а не O(n·w).
- Статистика считается **вручную**, без `statistics` / `numpy` / `pandas`.
- Ошибки пробрасываются через `raise ValueError(...) from err` —
  сохраняется исходная причина.
- Локальный `random.Random(seed)` — не загрязняет глобальный ГПСЧ.