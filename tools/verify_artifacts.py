"""Wheel ve sdist bütünlüğünü kurulum yapmadan doğrular."""

from __future__ import annotations

import tarfile
import zipfile
from pathlib import Path


def main() -> int:
    wheels = list(Path("dist").glob("ctf_virus_lab-*.whl"))
    sdists = list(Path("dist").glob("ctf_virus_lab-*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise SystemExit("tam olarak bir wheel ve bir sdist bekleniyordu")
    with zipfile.ZipFile(wheels[0]) as archive:
        wheel_names = set(archive.namelist())
        bad = archive.testzip()
    if bad is not None:
        raise SystemExit(f"wheel ZIP bütünlüğü bozuk: {bad}")
    required_wheel = {
        "ctf_malware_lab/__init__.py",
        "ctf_malware_lab/cli.py",
        "ctf_malware_lab/gui.py",
        "ctf_malware_lab/replay.py",
        "ctf_malware_lab/triage.py",
        "ctf_malware_lab/py.typed",
    }
    if not required_wheel.issubset(wheel_names):
        raise SystemExit("wheel gerekli paket dosyalarını içermiyor")
    with tarfile.open(sdists[0], "r:gz") as archive:
        sdist_names = archive.getnames()
    for suffix in (
        "/tests/conftest.py",
        "/tests/test_triage.py",
        "/tests/fixtures/harmless.txt",
        "/tests/fixtures/synthetic_trace.jsonl",
        "/README.md",
        "/LICENSE",
        "/agent.py",
    ):
        if not any(name.endswith(suffix) for name in sdist_names):
            raise SystemExit(f"sdist içinde eksik: {suffix}")
    print("Paket artefaktları doğrulandı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
