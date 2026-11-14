"""Тесты CLI main.py."""

import json
from pathlib import Path

import pytest
from main import main


def test_cli_runs_ok(capsys):
    code = main(["--kind", "sine", "--n", "10", "--window", "3"])
    out = capsys.readouterr().out
    assert code == 0
    assert "SMA" in out
    assert "EMA" in out


def test_cli_invalid_kind(capsys):
    with pytest.raises(SystemExit):
        main(["--kind", "bad"])


def test_cli_save_and_load(tmp_path, capsys):
    path = tmp_path / "s.json"
    code1 = main(["--kind", "trend", "--n", "8", "--save", str(path)])
    assert code1 == 0
    assert path.exists()

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["meta"]["n"] == 8
    assert len(payload["data"]) == 8

    code2 = main(["--load", str(path), "--window", "3"])
    assert code2 == 0