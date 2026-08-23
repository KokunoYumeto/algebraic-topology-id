#!/usr/bin/env python3
"""Add the verified Units 001--019 release/evidence artifacts to the backend.

The prior backend extension intentionally stopped before build artifacts.  This
bounded follow-up adds only exact, already-QA'd files and their QA witnesses;
it preserves every existing JSONL line byte-for-byte and refuses collisions or
hash/size drift.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
TIMESTAMP = "2026-08-23T00:00:00Z"
WORKFLOW = "o012-d60-id-reader-production"
SCHEMA = "curriculum.interop"
SCHEMA_VERSION = "0.1.0"
RIGHTS = "rights:o012-units-001-019-composite-cc-by-4.0"
UNIT = "unit:o012-rbt-u019"

ARTIFACTS = {
    "artifact:o012-indonesian-terminology-qa": ("qa/INDONESIAN_TERMINOLOGY_QA_2026-08-22.json", 18244, "54317e2c8591af9e3f668aa873281ae2c08275c7dc0dc2f1b66a6e314f7152a3", "application/json", None, "built", "Terminology QA and migration witness."),
    "artifact:o012-units-001-019-build-script": ("scripts/build-units-001-019.ps1", 17171, "ce917ab0aa4d16083b33f5f45be83dec8ee0eeeefb34ab7b65d221bf4a7ed5df", "text/plain; charset=utf-8", None, "source_frozen", "Deterministic two-build HTML/PDF build script."),
    "artifact:o012-units-001-019-html": ("output/html/units-001-019/index.html", 2962478, "ea5481b14dc1772408bd1c3e384b94a18eed9f2be3c9b9379fe4f8dd499253e0", "text/html; charset=utf-8", "artifact:o012-units-001-019-manifest", "built", "Primary offline semantic HTML reader with native MathML."),
    "artifact:o012-units-001-019-manifest": ("output/ARTIFACT_MANIFEST_UNITS_001_019.csv", 249, "d5bd6b71b19c9644a33999483c56699f1489aa4270c75a7b58fe2cf4e231ff74", "text/csv; charset=utf-8", None, "built", "Exact manifest for the cumulative HTML/PDF reader artifacts."),
    "artifact:o012-units-001-019-pdf": ("output/pdf/topologi-aljabar-unit-001-019-id.pdf", 1506471, "291e4206b9e58ee8a49108e55b6b894b9cd3362c7701a50cb83a7d79714b7a86", "application/pdf", "artifact:o012-units-001-019-manifest", "built", "Secondary A4 PDF reader; semantic HTML remains primary."),
    "artifact:o012-units-001-019-qa-receipt": ("qa/UNITS_001_019_QA.json", 12097, "38f8f3084f6031fe3670667e7e9a11f2b526a07eb69d32772194c3ff0ffeb02d", "application/json", None, "built", "Fail-closed cumulative source, structure, build, PDF, and browser QA receipt."),
    "artifact:o012-units-001-019-qa-text": ("qa/units-001-019-extracted.txt", 644062, "51e4102823bff9a55abd48b605897f91bda54fc2dbdfe1740bd38f173cf05a2d", "text/plain; charset=utf-8", None, "built", "UTF-8 Poppler text witness for the cumulative PDF."),
    "artifact:o012-units-001-019-render-inventory": ("qa/UNITS_001_019_RENDER_INVENTORY.csv", 26213, "017f151a1bd06a4e2649b37ad551c973789d502897b358967bd216cd74c61783", "text/csv; charset=utf-8", None, "visually_checked", "Ordered SHA-256 inventory of all 221 rendered pages."),
    "artifact:o012-units-001-019-visual-receipt": ("qa/UNITS_001_019_VISUAL_QA.md", 1780, "29d69abe6399976a206ef28c96d01df5fdb3f9f2c8510db95fe73f2b35b0b064", "text/markdown; charset=utf-8", None, "visually_checked", "All-page PDF and desktop/mobile browser visual receipt."),
}

QA_EVENTS = {
    "qa:o012-u019-qa": ("source", "Unit 019 source census, provenance, structural-ID, mastery, repair, review, and ledger checks passed.", ["artifact:o012-u019-qa", "artifact:o012-u019-independent-review", "artifact:o012-u019-source-audit"]),
    "qa:o012-units-001-019-build": ("build", "Cumulative Units 001-019 HTML and PDF passed two-build reproducibility and exact manifest checks.", ["artifact:o012-units-001-019-html", "artifact:o012-units-001-019-pdf", "artifact:o012-units-001-019-manifest", "artifact:o012-units-001-019-qa-receipt"]),
    "qa:o012-units-001-019-accessibility": ("accessibility", "Primary HTML passed native MathML, centered/reflowing desktop and mobile checks, resolving fragments, offline dependency, and clean console gates.", ["artifact:o012-units-001-019-html", "artifact:o012-units-001-019-qa-receipt", "artifact:o012-units-001-019-visual-receipt"]),
    "qa:o012-units-001-019-visual": ("visual", "All 221 rendered pages and browser surfaces passed the recorded visual inspection.", ["artifact:o012-units-001-019-pdf", "artifact:o012-units-001-019-render-inventory", "artifact:o012-units-001-019-visual-receipt"]),
    "qa:o012-units-001-019-terminology": ("language", "Indonesian terminology QA and migration invariants passed against the recorded field-use comparator.", ["artifact:o012-indonesian-terminology-qa", "artifact:o012-units-001-019-qa-receipt"]),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def common(entity_type: str, record_id: str) -> dict:
    return {"entity_type": entity_type, "id": record_id, "schema": SCHEMA, "schema_version": SCHEMA_VERSION, "status": "active", "supersedes": None, "timestamp": TIMESTAMP, "workflow": WORKFLOW}


def canonical(record: dict) -> bytes:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def load(name: str) -> tuple[list[dict], dict[str, bytes]]:
    path = BACKEND / name
    raw = path.read_bytes()
    records, lines = [], {}
    for line in raw.splitlines(keepends=True):
        record = json.loads(line.decode("utf-8"))
        if canonical(record) != line or record["id"] in lines:
            raise SystemExit(f"noncanonical or duplicate existing record in {name}")
        records.append(record)
        lines[record["id"]] = line
    if [record["id"] for record in records] != sorted(lines):
        raise SystemExit(f"existing IDs are not sorted in {name}")
    return records, lines


def main() -> int:
    tables: dict[str, list[dict]] = {}
    old_lines: dict[str, dict[str, bytes]] = {}
    all_ids: set[str] = set()
    for name in ("artifacts.jsonl", "qa.jsonl", "units.jsonl", "relations.jsonl", "rights.jsonl", "authority.jsonl", "assets.jsonl", "concepts.jsonl", "corrections.jsonl", "segments.jsonl", "terms.jsonl"):
        tables[name], old_lines[name] = load(name)
        for record in tables[name]:
            if record["id"] in all_ids:
                raise SystemExit(f"duplicate global ID: {record['id']}")
            all_ids.add(record["id"])
    for record_id in list(ARTIFACTS) + list(QA_EVENTS):
        if record_id in all_ids:
            raise SystemExit(f"refusing to overwrite existing ID: {record_id}")
    for record_id, (relative, expected_bytes, expected_sha, media_type, manifest_id, state, toolchain) in ARTIFACTS.items():
        path = LANE / relative
        if not path.is_file() or path.stat().st_size != expected_bytes or sha256(path) != expected_sha:
            raise SystemExit(f"artifact identity mismatch: {relative}")
    existing_u019_qa = next((record for record in tables["artifacts.jsonl"] if record["id"] == "artifact:o012-u019-qa"), None)
    if existing_u019_qa is None or existing_u019_qa.get("path") != "qa/UNIT_019_QA.json" or existing_u019_qa.get("sha256") != "a2ecc5dcc539c6434d2cb937ad7bb768c6ed434947b4cedcd313ce1bcfe8d1c3":
        raise SystemExit("the bounded Unit 019 QA artifact must already be present from the backend extension")
    artifacts = {record["id"]: record for record in tables["artifacts.jsonl"]}
    qa = {record["id"]: record for record in tables["qa.jsonl"]}
    for record_id, (relative, expected_bytes, expected_sha, media_type, manifest_id, state, toolchain) in ARTIFACTS.items():
        record = common("artifact", record_id)
        record.update({"bytes": expected_bytes, "locale": "id-ID", "manifest_artifact_id": manifest_id, "media_type": media_type, "path": relative, "qa_event_ids": [], "rights_component_id": RIGHTS, "sha256": expected_sha, "toolchain": toolchain, "translation_state": state, "unit_id": UNIT})
        artifacts[record_id] = record
        all_ids.add(record_id)
    for record_id, (qa_type, note, witnesses) in QA_EVENTS.items():
        if any(witness not in all_ids for witness in witnesses):
            raise SystemExit(f"QA witness missing for {record_id}")
        record = common("qa_event", record_id)
        record.update({"note": note, "qa_type": qa_type, "result": "passed", "unit_id": UNIT, "witness_artifact_ids": witnesses})
        qa[record_id] = record
        all_ids.add(record_id)
    for artifact_id, record in artifacts.items():
        if artifact_id in ARTIFACTS:
            record["qa_event_ids"] = sorted(qa_id for qa_id, event in qa.items() if artifact_id in event.get("witness_artifact_ids", []))
    for name, records in tables.items():
        if name == "artifacts.jsonl":
            records = list(artifacts.values())
        elif name == "qa.jsonl":
            records = list(qa.values())
        records.sort(key=lambda record: record["id"])
        output = b"".join(old_lines[name].get(record["id"], canonical(record)) for record in records)
        if b"\r" in output or not output.endswith(b"\n"):
            raise SystemExit(f"generated noncanonical bytes: {name}")
        (BACKEND / name).write_bytes(output)
    print(f"added_artifacts={len(ARTIFACTS)} added_qa_events={len(QA_EVENTS)}")
    print("artifact_backend_extension=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
