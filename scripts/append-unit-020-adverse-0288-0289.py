#!/usr/bin/env python3
"""Append the two cumulative-PDF-gate Unit 020 corrections, fail-closed."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
SOURCE = LANE / "source/id-ID/units/unit-020-lecture-020.md"
SHA = "ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3"
ROOT = "unit:o012-rbt-u020"
EDITION = "edition:roberts-at-2019-b947ad2"
RESOURCE = "resource:roberts-algebraic-topology-2019"
STAMP = "2026-08-23T00:00:00Z"
WORKFLOW = "o012-d60-id-reader-production"
SCHEMA = "curriculum.interop"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")

def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode() + b"\n"

def common(kind: str, ident: str) -> dict[str, Any]:
    return {"entity_type": kind, "id": ident, "schema": SCHEMA, "schema_version": "0.1.0",
            "status": "active", "supersedes": None, "timestamp": STAMP, "workflow": WORKFLOW}

def main() -> None:
    raw_source = SOURCE.read_bytes()
    if len(raw_source) != 45786 or hashlib.sha256(raw_source).hexdigest() != SHA:
        raise SystemExit("final Unit 020 source identity changed")
    records: dict[str, dict[str, dict[str, Any]]] = {}
    raws: dict[str, bytes] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        raws[name] = raw
        records[name] = {}
        for line in raw.splitlines(keepends=True):
            obj = json.loads(line.decode())
            if canon(obj) != line or obj["id"] in records[name]:
                raise SystemExit(f"{name}: malformed historical JSONL")
            records[name][obj["id"]] = obj
    all_ids = {x for t in records.values() for x in t}
    if "correction:o012-u020-adv-0287" not in all_ids or "correction:o012-u020-pre-portability-snapshot" not in all_ids:
        raise SystemExit("required predecessor correction records missing")
    with LEDGER.open(encoding="utf-8", newline="") as stream:
        rows = {r["event_id"]: r for r in csv.DictReader(stream)}
    expected = {
        288: ("P1", "corrected_after_cumulative_pdf_gate", "Notes.tex:4228-4251; Unit20 reader lines 737,923"),
        289: ("P1", "corrected_after_cumulative_pdf_gate", "Unit20 reader line 976; mastery hint 20.1"),
    }
    targets = {
        288: ["o012-rbt-l20-proof-001", "o012-rbt-l20-proof-002"],
        289: ["o012-rbt-l20-hint-001"],
    }
    additions: list[dict[str, Any]] = []
    for n, (severity, status, location) in expected.items():
        eid = f"O012-ADV-{n:04d}"
        row = rows.get(eid)
        if not row or row["severity"] != severity or row["status"] != status or row["source_location"] != location:
            raise SystemExit(f"ledger row mismatch: {eid}")
        affected = [f"unit:{x}" for x in targets[n]]
        if any(x not in all_ids for x in affected):
            raise SystemExit(f"target missing: {eid}")
        c = common("correction", f"correction:o012-u020-adv-{n:04d}")
        c.update({"adverse_ledger_id": eid, "affected_unit_ids": affected,
                  "correction_type": "mathematical_correction", "edition_id": EDITION,
                  "evidence": row["source_location"], "evidence_segment_id": "segment:o012-rbt-l20-notice",
                  "severity": severity, "rationale": row["rationale"], "resource_id": RESOURCE,
                  "source_defect": row["observed"], "target_change": row["action"], "unit_id": ROOT,
                  "upstream_report_disposition": "not_contacted",
                  "supersedes": "correction:o012-u020-adv-0287" if n == 288 else "correction:o012-u020-adv-0288"})
        additions.append(c)
    if any(x["id"] in all_ids for x in additions):
        raise SystemExit("Unit 020 cumulative corrections already present")
    out = raws["corrections.jsonl"] + b"".join(canon(x) for x in sorted(additions, key=lambda x: x["id"]))
    if not out.startswith(raws["corrections.jsonl"]):
        raise SystemExit("historical corrections prefix changed")
    (BACKEND / "corrections.jsonl").write_bytes(out)
    print("Unit 020 adverse 0288-0289 append: PASS")
    print(f"records_added={len(additions)}")
    print(f"corrections_bytes={len(out)}")
    print(f"corrections_sha256={hashlib.sha256(out).hexdigest()}")

if __name__ == "__main__":
    main()
