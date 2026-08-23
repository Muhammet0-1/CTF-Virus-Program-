from __future__ import annotations

import json

from ctf_malware_lab.graphs import behavior_graph, ioc_graph
from ctf_malware_lab.replay import replay_jsonl
from ctf_malware_lab.stix import stix_bundle
from ctf_malware_lab.triage import triage_bytes


def test_ioc_graph_uses_safe_ids_and_is_bounded() -> None:
    report = triage_bytes(b"https://example.invalid/path", sample_name="sample.bin")
    graph = ioc_graph(report)
    assert graph.startswith("flowchart TD")
    assert report.sha256[:12] in graph
    assert len(graph.splitlines()) <= 1 + 2 * 64


def test_behavior_graph_contains_only_bounded_timeline() -> None:
    lines = [
        (
            '{"timestamp":"2026-01-01T00:00:00Z","type":"file-read",'
            f'"process":"demo","target":"item-{index}"}}'
        )
        for index in range(100)
    ]
    graph = behavior_graph(replay_jsonl("\n".join(lines)))
    assert graph.startswith("flowchart LR")
    assert "E64" in graph
    assert "E65" not in graph


def test_mermaid_labels_cannot_escape_quoted_nodes() -> None:
    trace = (
        '{"timestamp":"2026-01-01T00:00:00Z","type":"file-read",'
        '"process":"demo","target":"safe\\"] --> INJECTED[\\"owned"}'
    )
    graph = behavior_graph(replay_jsonl(trace))
    assert 'INJECTED["owned' not in graph
    assert "&quot;] --&gt; INJECTED[&quot;owned" in graph


def test_stix_bundle_is_valid_deterministic_json() -> None:
    report = triage_bytes(b"https://example.invalid/path", sample_name="sample.bin")
    first = stix_bundle(report)
    second = stix_bundle(report)
    assert first == second
    document = json.loads(first)
    assert document["type"] == "bundle"
    assert document["objects"][0]["type"] == "file"
    indicators = [item for item in document["objects"] if item["type"] == "indicator"]
    assert indicators
    assert all("needs-validation" in item["labels"] for item in indicators)
    assert all("indicator_types" not in item for item in indicators)
    assert all(item["pattern_type"] == "stix" for item in indicators)
