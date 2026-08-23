from __future__ import annotations

import random
from pathlib import Path

import pytest

from ctf_malware_lab.errors import ValidationError
from ctf_malware_lab.models import FileKind
from ctf_malware_lab.triage import triage_bytes, triage_file


def test_harmless_fixture_triage() -> None:
    report = triage_file(Path("tests/fixtures/harmless.txt"))
    assert report.file_kind is FileKind.TEXT
    assert report.size > 0
    assert len(report.sha256) == 64
    assert len(report.sha1) == 40
    assert report.indicators
    assert report.risk_score < 20


@pytest.mark.parametrize(
    ("content", "rule_id", "attack_id"),
    [
        (b"powershell", "MLB001", "T1059"),
        (rb"CurrentVersion\Run", "MLB002", "T1547.001"),
        (b"VirtualBox", "MLB003", "T1497"),
        (b"WriteProcessMemory CreateRemoteThread", "MLB004", "T1055"),
        (b"vssadmin delete shadows", "MLB005", "T1490"),
        (b"lsass minidump", "MLB006", "T1003.001"),
    ],
)
def test_static_rules_are_explainable(content: bytes, rule_id: str, attack_id: str) -> None:
    report = triage_bytes(content)
    finding = next(item for item in report.findings if item.rule_id == rule_id)
    assert finding.attack_id == attack_id
    assert finding.explanation
    assert finding.recommendation


def test_high_entropy_signal_and_regions() -> None:
    data = random.Random(42).randbytes(8192)
    report = triage_bytes(data)
    assert any(item.rule_id == "MLB007" for item in report.findings)
    assert report.high_entropy_regions


def test_size_limit_is_enforced() -> None:
    with pytest.raises(ValidationError):
        triage_bytes(b"x" * (8 * 1024 * 1024 + 1))


def test_sample_name_is_validated() -> None:
    with pytest.raises(ValidationError):
        triage_bytes(b"x", sample_name="bad\nname")
