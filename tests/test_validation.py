from __future__ import annotations

import os
from pathlib import Path

import pytest

from ctf_malware_lab.errors import ValidationError
from ctf_malware_lab.validation import (
    MAX_SAMPLE_BYTES,
    read_regular_file,
    validate_display_text,
    validate_trace_text,
)


def test_regular_file_is_read(tmp_path: Path) -> None:
    path = tmp_path / "sample.bin"
    path.write_bytes(b"abc")
    assert read_regular_file(path) == b"abc"


def test_symlink_fifo_directory_and_oversize_are_rejected(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.write_bytes(b"x")
    link = tmp_path / "link"
    link.symlink_to(target)
    with pytest.raises(ValidationError):
        read_regular_file(link)
    with pytest.raises(ValidationError):
        read_regular_file(tmp_path)
    if hasattr(os, "mkfifo"):
        fifo = tmp_path / "fifo"
        os.mkfifo(fifo)
        with pytest.raises(ValidationError):
            read_regular_file(fifo)
    large = tmp_path / "large"
    large.write_bytes(b"x" * 17)
    with pytest.raises(ValidationError):
        read_regular_file(large, limit=16)


@pytest.mark.parametrize("value", ["line\nfeed", "tab\tvalue", "escape\x1b"])
def test_display_text_rejects_controls(value: str) -> None:
    with pytest.raises(ValidationError):
        validate_display_text(value, label="test")


def test_display_text_rejects_surrogate_and_size() -> None:
    with pytest.raises(ValidationError):
        validate_display_text("\ud800", label="test")
    with pytest.raises(ValidationError):
        validate_display_text("x" * 257, label="test")


def test_trace_limit_is_utf8_bytes() -> None:
    assert validate_trace_text("örnek") == "örnek"
    with pytest.raises(ValidationError):
        validate_trace_text("ş" * (1024 * 1024 // 2 + 1))
    assert MAX_SAMPLE_BYTES == 8 * 1024 * 1024
