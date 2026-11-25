"""Интеграционные тесты CLI main.py: запуск как внешнего процесса через subprocess."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAIN = PROJECT_ROOT / "main.py"


def run_cli(*args, timeout=60):
    """Запускает main.py в отдельном процессе и возвращает CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(PROJECT_ROOT),
    )


class TestCliHappyPath:
    def test_help_works(self):
        proc = run_cli("--help")
        assert proc.returncode == 0, proc.stderr
        assert "--kind" in proc.stdout

    def test_default_run_succeeds(self):
        proc = run_cli("--kind", "sine", "--n", "100", "--window", "5", "--seed", "1")
        assert proc.returncode == 0, proc.stderr
        assert proc.stdout.strip(), "программа должна что-то выводить"

    def test_output_contains_stats(self):
        proc = run_cli("--kind", "random", "--n", "50", "--window", "5")
        assert proc.returncode == 0, proc.stderr
        out = proc.stdout.lower()
        assert "средн" in out
        assert "медиан" in out

    def test_reproducible_output_with_seed(self):
        args = ("--kind", "sine", "--n", "30", "--window", "3", "--seed", "7")
        assert run_cli(*args).stdout == run_cli(*args).stdout


class TestCliSaveLoad:
    """Проверка сохранения и загрузки ряда через флаги --save и --load."""

    def test_save_creates_json(self, tmp_path):
        out = tmp_path / "series.json"
        proc = run_cli("--kind", "sine", "--n", "20", "--window", "3",
                       "--save", str(out))
        assert proc.returncode == 0, proc.stderr
        assert out.exists()
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert len(payload["data"]) == 20

    def test_load_roundtrip(self, tmp_path):
        out = tmp_path / "series.json"
        saved = run_cli("--kind", "sine", "--n", "20", "--window", "3",
                        "--save", str(out))
        assert saved.returncode == 0, saved.stderr
        proc = run_cli("--load", str(out), "--window", "3")
        assert proc.returncode == 0, proc.stderr
        assert proc.stdout.strip()


class TestCliErrors:
    """Некорректные аргументы CLI должны давать ненулевой код возврата."""

    def test_invalid_window_fails(self):
        proc = run_cli("--kind", "sine", "--n", "10", "--window", "0")
        assert proc.returncode != 0

    def test_window_bigger_than_n_fails(self):
        proc = run_cli("--kind", "sine", "--n", "10", "--window", "50")
        assert proc.returncode != 0

    def test_invalid_n_fails(self):
        proc = run_cli("--kind", "sine", "--n", "abc")
        assert proc.returncode != 0

    def test_unknown_kind_fails(self):
        proc = run_cli("--kind", "no_such_kind", "--n", "10")
        assert proc.returncode != 0


class TestCliBenchmark:
    """Флаг --benchmark выводит времена обеих реализаций SMA."""

    def test_benchmark_flag_runs(self):
        proc = run_cli("--kind", "random", "--n", "200", "--window", "10",
                       "--benchmark")
        assert proc.returncode == 0, proc.stderr
        out = proc.stdout.lower()
        assert "list" in out
        assert "deque" in out


class TestCLIVariant15:
    """Интеграция варианта 15: AR(1)-ряд и автокорреляция lag-1 в выводе."""

    def test_ar1_run_prints_autocorrelation(self):
        proc = run_cli("--kind", "ar1", "--n", "100", "--window", "10",
                       "--seed", "1")
        assert proc.returncode == 0, proc.stderr
        assert "автокорреляц" in proc.stdout.lower()
