#!/usr/bin/env python3
"""Validate the append-only Unit 020 backend boundary.

The historical 001-019 JSONL prefixes are immutable.  This validator checks
their exact line counts and byte hashes, validates every canonical appended
record, accepts separate sorted append batches (rather than requiring global
lexical order), and runs the existing shape/reference/manifest checks without
rewriting or loading a Git index.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import csv
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE = LANE / "source/id-ID/units/unit-020-lecture-020.md"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
BASELINE = {
    "artifacts.jsonl": (82, 64645, "c0b0624b523e285b1a4c88143b44a06e28a80a9d38dd49ad4026ab80687517f0"),
    "assets.jsonl": (20, 12317, "756e93660931a20be8a8ea2048126e6f963184f3ac6fbb18c615fd58dbe385ae"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (284, 89269, "b3afa6260276c68fe0d0bd8cbccaf55196caa05fa41acc4f1c58ea62001c1295"),
    "corrections.jsonl": (268, 259451, "769d7f611b07396465791d0d9a2319a18ce76da111ffbe10717f11b2c22f9512"),
    "qa.jsonl": (86, 49428, "e7c13ac6bb006b4adb20dca233fb528a0b140226799d32606f7539f4c6c9826f"),
    "relations.jsonl": (219, 87238, "d8756f6d556d40986c3c8212a2e8f378950f2de1cb184463df5eb183e82bfbb5"),
    "rights.jsonl": (47, 42349, "db374a45045aa674e68d9d104c736d55d874adbd9fa87bd0a7d5189e07e6f21c"),
    "segments.jsonl": (710, 825283, "ad3f8b3c45a2235e72af5fcfaa78cc639d601a0f6256df65e8d66cf83774025a"),
    "terms.jsonl": (277, 167971, "6111794432f311984a3b4f2fbe4250d78873968f696ff66da867868fbc73b2ec"),
    "units.jsonl": (729, 879865, "e88c8dfca31e77a115e6251db21f4e485d569beec8d9f1909dafa9ad0a485cf3"),
}
FINAL_SOURCE_SHA = "ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3"

def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"

def load_generic_validator():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_backend_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load existing generic validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def sorted_runs(ids: list[str]) -> list[tuple[int, int]]:
    """Return monotone runs in an append suffix.

    Each producer transaction appends a sorted batch.  A later transaction may
    legitimately begin with a lexically earlier ID; that is a boundary, not a
    historical rewrite.
    """
    if not ids:
        return []
    runs: list[tuple[int, int]] = []
    start = 0
    for i in range(1, len(ids)):
        if ids[i] < ids[i - 1]:
            runs.append((start, i))
            start = i
    runs.append((start, len(ids)))
    return runs

def main() -> int:
    records: list[dict[str, Any]] = []
    raw_by_file: dict[str, bytes] = {}
    ids_by_file: dict[str, list[str]] = {}
    append_runs: dict[str, list[tuple[int, int]]] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        raw_by_file[name] = raw
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: non-LF or unterminated JSONL")
        lines = raw.splitlines(keepends=True)
        baseline_count, baseline_bytes, baseline_sha = BASELINE[name]
        prefix = b"".join(lines[:baseline_count])
        if len(prefix) != baseline_bytes or hashlib.sha256(prefix).hexdigest() != baseline_sha:
            raise SystemExit(f"{name}: immutable baseline prefix mismatch")
        ids: list[str] = []
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line or not isinstance(obj.get("id"), str):
                raise SystemExit(f"{name}:{number}: noncanonical appended/historical line")
            ids.append(obj["id"])
            records.append(obj)
        if len(ids) != len(set(ids)):
            raise SystemExit(f"{name}: duplicate IDs")
        suffix_ids = ids[baseline_count:]
        runs = sorted_runs(suffix_ids)
        for start, end in runs:
            if suffix_ids[start:end] != sorted(suffix_ids[start:end]):
                raise SystemExit(f"{name}: append batch {start}:{end} is not sorted")
        ids_by_file[name] = ids
        append_runs[name] = runs
    by_id: dict[str, dict[str, Any]] = {}
    for obj in records:
        if obj["id"] in by_id:
            raise SystemExit(f"duplicate global ID: {obj['id']}")
        by_id[obj["id"]] = obj
    generic = load_generic_validator()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)
    source = SOURCE.read_bytes()
    if hashlib.sha256(source).hexdigest() != FINAL_SOURCE_SHA:
        raise SystemExit("final Unit 020 source hash mismatch")
    final_artifact = by_id.get("artifact:o012-u020-source-final-ed086")
    if not final_artifact or final_artifact.get("sha256") != FINAL_SOURCE_SHA:
        raise SystemExit("final source artifact is missing or unbound")
    if by_id.get("qa:o012-u020-final-source-integrity", {}).get("result") != "passed":
        raise SystemExit("final source-integrity QA is not passed")
    with LEDGER.open(encoding="utf-8", newline="") as stream:
        ledger = {row["event_id"]: row for row in csv.DictReader(stream)}
    for number, status in ((288, "corrected_after_cumulative_pdf_gate"),
                           (289, "corrected_after_cumulative_pdf_gate")):
        event = f"O012-ADV-{number:04d}"
        correction = by_id.get(f"correction:o012-u020-adv-{number:04d}")
        if not correction or correction.get("adverse_ledger_id") != event:
            raise SystemExit(f"missing backend closure for {event}")
        if event not in ledger or ledger[event].get("status") != status:
            raise SystemExit(f"ledger tail mismatch for {event}")
    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw_by_file[name])
    counts = {name: len(ids_by_file[name]) for name in FILES}
    print("append-only Unit 020 backend validation: PASS")
    print("records=" + json.dumps(counts, sort_keys=True))
    print("append_runs=" + json.dumps({n: len(v) for n, v in append_runs.items()}, sort_keys=True))
    print(f"total_records={len(records)}")
    print(f"backend_bytes={sum(len(x) for x in raw_by_file.values())}")
    print(f"backend_bundle_sha256={bundle.hexdigest()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
