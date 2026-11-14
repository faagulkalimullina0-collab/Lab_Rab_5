"""Сохранение и чтение числовых рядов в CSV.

Форматы:
  - простой: один столбец "value" (или без заголовка) — только исходный ряд;
  - расширенный: столбцы i, value, sma, ema, cma — результаты анализа.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Union

PathLike = Union[str, Path]


def save_series_csv(
    data: Sequence[float],
    path: PathLike,
    header: bool = True,
    delimiter: str = ",",
) -> None:
    """Сохраняет числовой ряд в CSV.

    Args:
        data: числовой ряд.
        path: путь к файлу (создастся/перезапишется).
        header: писать ли строку-заголовок ``i,value``.
        delimiter: разделитель (по умолчанию ``,``).

    Raises:
        ValueError: если ряд пуст, содержит нечисловые значения,
                    или файл не удалось записать.
    """
    if not data:
        raise ValueError("Ряд пуст: нечего сохранять в CSV")
    for i, v in enumerate(data):
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            raise ValueError(f"Элемент data[{i}] = {v!r} не является числом")

    file_path = Path(path)
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=delimiter)
            if header:
                writer.writerow(["i", "value"])
            for i, v in enumerate(data):
                writer.writerow([i, v])
    except OSError as err:
        raise ValueError(
            f"Не удалось записать CSV {file_path}: {err}"
        ) from err


def save_results_csv(
    data: Sequence[float],
    path: PathLike,
    sma: Optional[Sequence[float]] = None,
    ema: Optional[Sequence[float]] = None,
    cma: Optional[Sequence[float]] = None,
    delimiter: str = ",",
) -> None:
    """Сохраняет исходный ряд и результаты анализа в один CSV.

    Столбцы: i, value, sma, ema, cma.
    Ряды разной длины (SMA/EMA/CMA короче исходного) выравниваются
    по индексу: в отсутствующих ячейках остаётся пустая строка.

    Raises:
        ValueError: если data пуст или файл не удалось записать.
    """
    if not data:
        raise ValueError("Ряд пуст: нечего сохранять в CSV")

    n = len(data)

    def _get(seq: Optional[Sequence[float]], idx: int) -> str:
        if seq is None or idx >= len(seq):
            return ""
        return repr(float(seq[idx]))

    file_path = Path(path)
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(["i", "value", "sma", "ema", "cma"])
            for i in range(n):
                writer.writerow([
                    i,
                    float(data[i]),
                    _get(sma, i),
                    _get(ema, i),
                    _get(cma, i),
                ])
    except OSError as err:
        raise ValueError(
            f"Не удалось записать CSV {file_path}: {err}"
        ) from err


def load_results_csv(path: PathLike, delimiter: str = ",") -> Dict[str, List[float]]:
    """Читает CSV с результатами анализа.

    Ожидаемый формат: заголовок ``i,value,sma,ema,cma`` (или подмножество).
    Возвращает словарь вида ``{"value": [...], "sma": [...], ...}``.

    Raises:
        ValueError: если файл не найден, пуст или содержит нечисловые данные.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    result: Dict[str, List[float]] = {}
    try:
        with file_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            if not reader.fieldnames:
                raise ValueError(f"Файл {file_path} пуст или без заголовка")
            # Обязательный столбец — value (или data)
            value_col = "value" if "value" in reader.fieldnames else None
            if value_col is None:
                raise ValueError(
                    f"В файле {file_path} нет столбца 'value'"
                )
            for col in reader.fieldnames:
                if col == "i":
                    continue
                result.setdefault(col, [])
            for lineno, row in enumerate(reader, start=2):
                for col in result:
                    raw = (row.get(col) or "").strip()
                    if not raw:
                        continue
                    try:
                        result[col].append(float(raw))
                    except ValueError as err:
                        raise ValueError(
                            f"{file_path}:{lineno}: столбец '{col}' "
                            f"значение {raw!r} не число"
                        ) from err
    except OSError as err:
        raise ValueError(
            f"Не удалось прочитать файл {file_path}: {err}"
        ) from err

    if not result.get("value"):
        raise ValueError(f"Файл {file_path} не содержит столбца 'value'")
    return result