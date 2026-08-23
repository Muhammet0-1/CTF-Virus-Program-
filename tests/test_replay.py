from __future__ import annotations

import json
from pathlib import Path

import pytest

from ctf_malware_lab.errors import ParseError, ValidationError
from ctf_malware_lab.models import EventKind
from ctf_malware_lab.replay import parse_events, replay_events, replay_jsonl


def event_line(
    kind: str,
    *,
    second: int = 0,
    process: str = "demo",
    target: str = "training-target",
    details: object | None = None,
) -> str:
    data: dict[str, object] = {
        "timestamp": f"2026-01-01T00:00:{second:02d}Z",
        "type": kind,
        "process": process,
        "target": target,
    }
    if details is not None:
        data["details"] = details
    return json.dumps(data)


def test_fixture_replays_in_order() -> None:
    text = Path("tests/fixtures/synthetic_trace.jsonl").read_text(encoding="utf-8")
    report = replay_jsonl(text)
    assert report.event_count == 3
    assert report.events[0].kind is EventKind.PROCESS_START
    assert report.risk_score == 8
    assert report.events[-1].timestamp.endswith("Z")


@pytest.mark.parametrize(
    ("kind", "rule_id", "attack_id"),
    [
        ("persistence-attempt", "MLB101", "T1547"),
        ("credential-access", "MLB102", "T1003"),
        ("backup-delete-attempt", "MLB103", "T1490"),
        ("defense-evasion-signal", "MLB104", "T1497"),
        ("script-interpreter", "MLB105", "T1059"),
        ("network-intent", "MLB106", "T1071"),
    ],
)
def test_behavior_rules(kind: str, rule_id: str, attack_id: str) -> None:
    report = replay_jsonl(event_line(kind))
    finding = report.findings[0]
    assert finding.rule_id == rule_id
    assert finding.attack_id == attack_id


def test_bulk_rename_threshold() -> None:
    lines = [event_line("file-rename", second=index) for index in range(20)]
    report = replay_jsonl("\n".join(lines))
    assert any(item.rule_id == "MLB107" for item in report.findings)


@pytest.mark.parametrize(
    "text",
    [
        "not-json",
        "[]",
        '{"timestamp":"2026-01-01T00:00:00Z","type":"unknown","process":"a","target":"b"}',
        '{"timestamp":"2026-01-01T00:00:00","type":"file-read","process":"a","target":"b"}',
        '{"timestamp":"2026-01-01T00:00:00Z","type":"file-read","process":"a","target":"b","extra":1}',
    ],
)
def test_malformed_events_are_rejected(text: str) -> None:
    with pytest.raises((ParseError, ValidationError)):
        replay_jsonl(text)


def test_out_of_order_and_nested_details_are_rejected() -> None:
    with pytest.raises(ParseError):
        replay_jsonl(event_line("file-read", second=2) + "\n" + event_line("file-read", second=1))
    with pytest.raises(ValidationError):
        replay_jsonl(event_line("file-read", details={"nested": {"x": 1}}))


def test_event_count_limit_is_enforced() -> None:
    line = event_line("file-read")
    with pytest.raises(ValidationError):
        parse_events("\n".join([line] * 1001))
    events = parse_events(line)
    with pytest.raises(ValidationError):
        replay_events(events * 1001)
