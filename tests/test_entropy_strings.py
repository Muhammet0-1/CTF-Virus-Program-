from __future__ import annotations

import random

from ctf_malware_lab.entropy import high_entropy_regions, shannon_entropy
from ctf_malware_lab.models import FileKind
from ctf_malware_lab.strings import extract_strings
from ctf_malware_lab.triage import classify_file


def test_entropy_boundaries() -> None:
    assert shannon_entropy(b"") == 0
    assert shannon_entropy(b"A" * 1000) == 0
    assert shannon_entropy(bytes(range(256))) == 8


def test_high_entropy_regions_are_bounded() -> None:
    randomizer = random.Random(7)
    data = randomizer.randbytes(4096 * 20)
    regions = high_entropy_regions(data)
    assert 1 <= len(regions) <= 16
    assert all(region.entropy >= 7.2 for region in regions)


def test_ascii_and_utf16_strings_are_deduplicated() -> None:
    data = b"prefix HarmlessASCII suffix\x00W\x00i\x00d\x00e\x00T\x00e\x00x\x00t\x00"
    strings = extract_strings(data)
    assert any("HarmlessASCII" in item for item in strings)
    assert "WideText" in strings


def test_string_count_is_bounded() -> None:
    data = b"\x00".join(f"STRING{index:04d}".encode() for index in range(300))
    assert len(extract_strings(data)) == 200


def test_file_classification() -> None:
    assert classify_file(b"") is FileKind.EMPTY
    assert classify_file(b"MZrest") is FileKind.PE
    assert classify_file(b"\x7fELFrest") is FileKind.ELF
    assert classify_file(b"PK\x03\x04rest") is FileKind.ZIP
    assert classify_file(b"%PDF-1.7") is FileKind.PDF
    assert classify_file(b"#!/usr/bin/env python\n") is FileKind.SCRIPT
    assert classify_file(b"plain readable text") is FileKind.TEXT
    assert classify_file(b"\x00\xff\x01\x80") is FileKind.UNKNOWN
