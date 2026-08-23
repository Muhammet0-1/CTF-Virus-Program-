from __future__ import annotations

from ctf_malware_lab.compare import compare_reports
from ctf_malware_lab.quarantine import build_quarantine_plan
from ctf_malware_lab.triage import triage_bytes


def test_identical_reports_have_no_delta() -> None:
    left = triage_bytes(b"same", sample_name="left.bin")
    right = triage_bytes(b"same", sample_name="right.bin")
    report = compare_reports(left, right)
    assert report.identical
    assert report.entropy_delta == 0
    assert report.risk_delta == 0
    assert report.added_indicators == ()


def test_comparison_reports_added_rules_and_indicators() -> None:
    left = triage_bytes(b"plain")
    right = triage_bytes(b"powershell https://example.invalid")
    report = compare_reports(left, right)
    assert not report.identical
    assert "MLB001" in report.added_rules
    assert report.added_indicators
    assert report.risk_delta > 0


def test_quarantine_plan_is_deterministic_and_never_mutates() -> None:
    report = triage_bytes(b"powershell")
    first = build_quarantine_plan(report)
    second = build_quarantine_plan(report)
    assert first == second
    assert first.mode == "simulation-only"
    assert first.proposed_name == f"{report.sha256}.quarantine"
    assert not first.would_copy_bytes
    assert not first.would_delete_source
    assert len(first.verification_token) == 64


def test_clean_plan_uses_manual_review_reason() -> None:
    plan = build_quarantine_plan(triage_bytes(b"plain"))
    assert plan.reasons == ("manual-review",)
