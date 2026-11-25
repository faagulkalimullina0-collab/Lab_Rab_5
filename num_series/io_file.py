"""Чтение рядов из файлов: TXT, CSV и автовыбор формата."""

from pathlib import Path

from num_series.io_json import load_series_json as _load_json


def load_series_txt(path):
    """Чтение TXT: по одному числу в строке, '#' — комментарий.

    Ошибка нечисловой строки содержит номер строки в формате ':N:'.
    """
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"Файл не найден: {path}")

    values = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        try:
            values.append(float(line))
        except ValueError:
            raise ValueError(
                f"Нечисловая строка в TXT, строка :{lineno}: «{line}»"
            ) from None

    if not values:
        raise ValueError("TXT-файл не содержит чисел")
    return values


def load_series_csv(path):
    """Чтение CSV: заголовок пропускается, значения собираются из всех колонок.

    Разделители: ',' или ';' (можно вперемешку).
    Строка со смесью чисел и текста — ошибка; строка без чисел — заголовок.
    """
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"Файл не найден: {path}")

    values = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        fields = [f.strip() for f in line.replace(";", ",").split(",") if f.strip()]

        parsed = []
        unparsed = []
        for f in fields:
            try:
                parsed.append(float(f))
            except ValueError:
                unparsed.append(f)

        if parsed and unparsed:
            raise ValueError(
                f"Нечисловое значение в CSV, строка :{lineno}: «{unparsed[0]}»"
            )
        if parsed:
            values.extend(parsed)
        # ни одно поле не число — это заголовок, пропускаем

    if not values:
        raise ValueError("CSV-файл не содержит чисел")
    return values


def load_series_auto(path):
    """Автовыбор парсера по расширению: .json, .txt, .csv."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix not in (".json", ".txt", ".csv"):
        raise ValueError(
            f"Неизвестное расширение файла: '{suffix or path.name}' — "
            f"ожидались .json, .txt или .csv ({path})"
        )
    if suffix == ".json":
        loaded, _meta = _load_json(path, with_meta=True)
        return loaded
    if suffix == ".csv":
        return load_series_csv(path)
    return load_series_txt(path)
