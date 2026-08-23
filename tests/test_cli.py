from __future__ import annotations

import json
from pathlib import Path

import pytest

from ctf_malware_lab.cli import main


def test_triage_json_and_stix(capsys: pytest.CaptureFixture[str]) -> None:
    sample = "tests/fixtures/harmless.txt"
    assert main(["triage", sample, "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["size"] > 0
    assert main(["triage", sample, "--format", "stix"]) == 0
    assert json.loads(capsys.readouterr().out)["type"] == "bundle"


def test_replay_compare_and_plan(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["replay", "tests/fixtures/synthetic_trace.jsonl", "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["event_count"] == 3
    left = tmp_path / "left"
    right = tmp_path / "right"
    left.write_bytes(b"a")
    right.write_bytes(b"powershell")
    assert main(["compare", str(left), str(right), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["risk_delta"] > 0
    assert main(["quarantine-plan", str(right)]) == 0
    assert json.loads(capsys.readouterr().out)["mode"] == "simulation-only"


def test_catalog_and_self_test(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["catalog"]) == 0
    assert "persistence-attempt" in capsys.readouterr().out
    assert main(["self-test"]) == 0
    assert "başarılı" in capsys.readouterr().out


def test_invalid_file_returns_code_two(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    missing = tmp_path / "missing"
    assert main(["triage", str(missing)]) == 2
    assert "Hata:" in capsys.readouterr().err
