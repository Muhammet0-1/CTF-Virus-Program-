from __future__ import annotations

import ast
from pathlib import Path


def test_production_source_has_no_active_or_dynamic_execution_surface() -> None:
    forbidden_imports = {
        "socket",
        "subprocess",
        "requests",
        "urllib.request",
        "http.client",
        "ctypes",
    }
    forbidden_calls = {"eval", "exec", "compile", "__import__"}
    for path in Path("src/ctf_malware_lab").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(alias.name not in forbidden_imports for alias in node.names), path
            if isinstance(node, ast.ImportFrom):
                assert node.module not in forbidden_imports, path
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in forbidden_calls, path


def test_gui_import_does_not_start_event_loop() -> None:
    from ctf_malware_lab.gui import LabWindow

    assert LabWindow.__name__ == "LabWindow"
