from __future__ import annotations

import json

from ctf_malware_lab.compare import compare_reports
from ctf_malware_lab.replay import replay_jsonl
from ctf_malware_lab.reporting import (
    render_comparison,
    render_replay,
    render_static,
    sanitize_terminal,
)
from ctf_malware_lab.triage import triage_bytes


def test_static_json_jsonl_and_sarif_are_valid() -> None:
    report = triage_bytes(b"powershell https://example.invalid")
    assert json.loads(render_static(report, "json"))["risk_score"] > 0
    assert json.loads(render_static(report, "jsonl"))["file_kind"] == "text"
    sarif = json.loads(render_static(report, "sarif"))
    assert sarif["version"] == "2.1.0"
    assert sarif["runs"][0]["results"]
    assert "NaN" not in render_static(report, "json")


def test_strings_are_opt_in() -> None:
    report = triage_bytes(b"HarmlessReadableString")
    assert "strings" not in json.loads(render_static(report, "json"))
    assert "strings" in json.loads(render_static(report, "json", include_strings=True))


def test_replay_and_comparison_outputs() -> None:
    trace = (
        '{"timestamp":"2026-01-01T00:00:00Z","type":"network-intent",'
        '"process":"demo","target":"example.invalid"}'
    )
    replay = replay_jsonl(trace)
    assert json.loads(render_replay(replay, "json"))["event_count"] == 1
    assert json.loads(render_replay(replay, "sarif"))["runs"][0]["results"]
    comparison = compare_reports(triage_bytes(b"a"), triage_bytes(b"b"))
    assert "Risk farkı" in render_comparison(comparison, "text")


def test_control_characters_are_escaped() -> None:
    value = sanitize_terminal("before\n\x1bafter\x00")
    assert "\n" not in value
    assert "\x1b" not in value
    assert "\\x0a" in value
    assert "\\x1b" in value
    assert "\\x00" in value
