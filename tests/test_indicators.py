from __future__ import annotations

from ctf_malware_lab.indicators import extract_indicators
from ctf_malware_lab.models import IndicatorKind


def test_indicator_types_are_extracted_without_resolution() -> None:
    strings = (
        "https://example.invalid/path",
        "analyst@example.invalid",
        "192.0.2.10",
        r"HKCU\Software\Training",
        r"C:\Lab\sample.bin",
        "/opt/training/sample.bin",
        "a" * 64,
    )
    indicators = extract_indicators(strings, "b" * 64)
    kinds = {item.kind for item in indicators}
    assert {
        IndicatorKind.URL,
        IndicatorKind.DOMAIN,
        IndicatorKind.EMAIL,
        IndicatorKind.IPV4,
        IndicatorKind.REGISTRY,
        IndicatorKind.PATH,
        IndicatorKind.SHA256,
    }.issubset(kinds)


def test_invalid_ipv4_is_not_emitted() -> None:
    values = extract_indicators(("999.999.999.999",), "a" * 64)
    assert not any(item.kind is IndicatorKind.IPV4 for item in values)


def test_indicators_are_deduplicated_and_sorted() -> None:
    values = extract_indicators(("EXAMPLE.INVALID example.invalid",), "a" * 64)
    domains = [item.value for item in values if item.kind is IndicatorKind.DOMAIN]
    assert domains == ["example.invalid"]
    assert list(values) == sorted(values, key=lambda item: (item.kind.value, item.value.casefold()))
