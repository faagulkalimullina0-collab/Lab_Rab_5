"""Чтение числовых рядов из простых текстовых файлов (txt, csv)."""

import re
from pathlib import Path
from typing import List, Union

PathLike = Union[str, Path]
_SEPARATORS = re.compile(r"[;,\s]+")


def load_series_txt(path: PathLike) -> List[float]:
    """Читает числа из .txt — по одному на строку (пустые и #-строки пропускаются)."""
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    result: List[float] = []
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for lineno, raw in enumerate(f, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    result.append(float(line))
                except ValueError as err:
                    raise ValueError(
                        f"{file_path}:{lineno}: '{line}' не является числом"
                    ) from err
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл {file_path}: {err}") from err

    if not result:
        raise ValueError(f"Файл {file_path} не содержит чисел")
    return result


def load_series_csv(path: PathLike) -> List[float]:
    """Читает числа из .csv — через разделитель, возможно с заголовком."""
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    result: List[float] = []
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for lineno, raw in enumerate(f, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                tokens = [t for t in _SEPARATORS.split(line) if t]
                if not tokens:
                    continue
                try:
                    values = [float(t) for t in tokens]
                except ValueError:
                    if lineno == 1:
                        continue  # считаем заголовком
                    raise ValueError(
                        f"{file_path}:{lineno}: строка '{line}' содержит "
                        f"нечисловые значения"
                    )
                result.extend(values)
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл {file_path}: {err}") from err

    if not result:
        raise ValueError(f"Файл {file_path} не содержит чисел")
    return result


def load_series_auto(path: PathLike) -> List[float]:
    """Автоматически выбирает парсер по расширению."""
    from .io_json import load_series_json

    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        return load_series_json(path)
    if suffix in {".txt", ".dat"}:
        return load_series_txt(path)
    if suffix in {".csv", ".tsv"}:
        return load_series_csv(path)
    try:
        return load_series_csv(path)
    except ValueError:
        return load_series_txt(path)