#!/usr/bin/env python3
"""Append the verified cumulative Units 001–020 build/visual boundary."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
WORKFLOW = "o012-d60-id-reader-production"
SCHEMA = "curriculum.interop"
STAMP = "2026-08-23T00:00:00Z"
ROOT = "unit:o012-rbt-u020"
RIGHTS = "rights:o012-units-001-020-composite-cc-by-4.0-final-ed086"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
ARTIFACT_SPECS = {
    "artifact:o012-units-001-020-html": ("output/html/units-001-020/index.html", 3190086, "59cb765f2291fc835ca629c774505303745983baacf5379efc97c49da6205c03", "text/html; charset=utf-8", "built"),
    "artifact:o012-units-001-020-pdf": ("output/pdf/topologi-aljabar-unit-001-020-id.pdf", 1598235, "30fdde6ddfc937df3e93bb59d58e72e593c87262d6a2535214113e5ebab64457", "application/pdf", "built"),
    "artifact:o012-units-001-020-manifest": ("output/ARTIFACT_MANIFEST_UNITS_001_020.csv", 249, "d69c37838da4174ebb7dc4576392e813040d7f6ebbe1a13fe1c922e1271672da", "text/csv; charset=utf-8", "built"),
    "artifact:o012-units-001-020-build-receipt": ("qa/UNITS_001_020_BUILD_RECEIPT.json", 2812, "3c39b5546b2aced0a443c753e69824807c8e2f8c91903fe4eb3cca04741ecef1", "application/json", "built"),
    "artifact:o012-units-001-020-visual-receipt": ("qa/UNITS_001_020_VISUAL_QA.md", 1392, "6a8b4d8e31c4adf38fcf51606542f59366f6c5f58d878df65e49677376bf58f9", "text/markdown; charset=utf-8", "visually_checked"),
}

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode() + b"\n"

def common(kind: str, ident: str) -> dict[str, Any]:
    return {"entity_type": kind, "id": ident, "schema": SCHEMA, "schema_version": "0.1.0",
            "status": "active", "supersedes": None, "timestamp": STAMP, "workflow": WORKFLOW}

def main() -> None:
    # Validate build receipts before touching backend bytes.
    for ident, (relative, size, expected, _media, _state) in ARTIFACT_SPECS.items():
        path = LANE / relative
        raw = path.read_bytes()
        if len(raw) != size or digest(raw) != expected:
            raise SystemExit(f"artifact mismatch: {relative}")
    receipt = json.loads((LANE / "qa/UNITS_001_020_BUILD_RECEIPT.json").read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS" or receipt.get("artifacts", {}).get("pdf", {}).get("pages") != 237:
        raise SystemExit("cumulative build receipt is not PASS/237 pages")
    if receipt.get("source_authority", {}).get("unit_020_sha256") != "ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3":
        raise SystemExit("build receipt is not bound to final Unit 020 source")
    visual = (LANE / "qa/UNITS_001_020_VISUAL_QA.md").read_text(encoding="utf-8")
    if "Status: **PASS**" not in visual or "237 A4 pages" not in visual:
        raise SystemExit("cumulative visual receipt is not the expected PASS boundary")
    tables: dict[str, dict[str, dict[str, Any]]] = {}
    raws: dict[str, bytes] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        raws[name] = raw
        tables[name] = {}
        for line in raw.splitlines(keepends=True):
            obj = json.loads(line.decode())
            if canon(obj) != line or obj["id"] in tables[name]:
                raise SystemExit(f"{name}: malformed historical JSONL")
            tables[name][obj["id"]] = obj
    all_ids = {x for t in tables.values() for x in t}
    if RIGHTS not in all_ids or ROOT not in all_ids:
        raise SystemExit("final cumulative rights or Unit 020 root is missing")
    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    def add(name: str, obj: dict[str, Any]) -> None:
        if obj["id"] in all_ids or any(obj["id"] == x["id"] for xs in additions.values() for x in xs):
            raise SystemExit(f"duplicate cumulative id: {obj['id']}")
        additions[name].append(obj)
    manifest_id = "artifact:o012-units-001-020-manifest"
    build_id = "qa:o012-units-001-020-build"
    visual_id = "qa:o012-units-001-020-visual"
    for ident, (relative, size, expected, media, state) in ARTIFACT_SPECS.items():
        a = common("artifact", ident)
        if ident.endswith("-html") or ident.endswith("-pdf"):
            manifest = manifest_id
        else:
            manifest = None
        qas = []
        if state == "visually_checked":
            qas.append(visual_id)
        else:
            qas.append(build_id)
            if ident.endswith("-pdf"):
                qas.append(visual_id)
        a.update({"bytes": size, "locale": "id-ID", "manifest_artifact_id": manifest,
                  "media_type": media, "path": relative, "qa_event_ids": qas,
                  "rights_component_id": RIGHTS, "sha256": expected,
                  "toolchain": "Deterministic Units 001-020 builder; Pandoc 3.9.0.2; SOURCE_DATE_EPOCH=1787443200.",
                  "translation_state": state, "unit_id": ROOT})
        add("artifacts.jsonl", a)
    q = common("qa_event", build_id)
    q.update({"note": "Cumulative Units 001-020 HTML and PDF each passed two-build byte identity; manifest and build receipt are exact.",
              "qa_type": "build", "result": "passed", "unit_id": ROOT,
              "witness_artifact_ids": [manifest_id, "artifact:o012-units-001-020-html",
                                       "artifact:o012-units-001-020-pdf",
                                       "artifact:o012-units-001-020-build-receipt"]})
    add("qa.jsonl", q)
    q = common("qa_event", visual_id)
    q.update({"note": "Representative visual QA passed on seven pages of the 237-page A4 PDF; no clipping, overlap, or positional-figure dependence observed.",
              "qa_type": "visual", "result": "passed", "unit_id": ROOT,
              "witness_artifact_ids": ["artifact:o012-units-001-020-pdf",
                                       "artifact:o012-units-001-020-visual-receipt"]})
    add("qa.jsonl", q)
    def relation(ident: str, source: str, typ: str, target: str, note: str) -> None:
        r = common("relation", ident)
        r.update({"from_id": source, "note": note, "relation_type": typ, "to_id": target})
        add("relations.jsonl", r)
    relation("relation:contains:o012-units-001-020-manifest:html", manifest_id, "contains",
             "artifact:o012-units-001-020-html", "Manifest entry for the cumulative HTML reader.")
    relation("relation:contains:o012-units-001-020-manifest:pdf", manifest_id, "contains",
             "artifact:o012-units-001-020-pdf", "Manifest entry for the cumulative PDF reader.")
    relation("relation:boundary:o012-units-001-020-build", RIGHTS, "contains",
             "artifact:o012-units-001-020-pdf", "Final cumulative release boundary points to the verified PDF reader.")
    relation("relation:qa:o012-units-001-020-build", build_id, "illustrates",
             "artifact:o012-units-001-020-build-receipt", "Build QA event is witnessed by its exact receipt.")
    relation("relation:qa:o012-units-001-020-visual", visual_id, "illustrates",
             "artifact:o012-units-001-020-visual-receipt", "Visual QA event is witnessed by its exact receipt.")
    merged_ids = all_ids | {x["id"] for xs in additions.values() for x in xs}
    for xs in additions.values():
        for obj in xs:
            for field in ("from_id", "to_id", "unit_id", "rights_component_id", "manifest_artifact_id"):
                if obj.get(field) is not None and obj[field] not in merged_ids:
                    raise SystemExit(f"unknown reference {obj['id']}.{field}")
            for field in ("witness_artifact_ids", "qa_event_ids"):
                if any(x not in merged_ids for x in obj.get(field, [])):
                    raise SystemExit(f"unknown list reference {obj['id']}.{field}")
    out: dict[str, bytes] = {}
    for name in FILES:
        if (BACKEND / name).read_bytes() != raws[name]:
            raise SystemExit(f"historical prefix changed before write: {name}")
        out[name] = raws[name] + b"".join(canon(x) for x in sorted(additions[name], key=lambda x: x["id"]))
    for name, raw in out.items():
        (BACKEND / name).write_bytes(raw)
    h = hashlib.sha256()
    for name in FILES:
        h.update(name.encode()); h.update(b"\0"); h.update(out[name])
    print("Cumulative Units 001-020 artifacts append: PASS")
    print("new_records_by_file=" + json.dumps({k: len(v) for k, v in additions.items()}, sort_keys=True))
    print(f"new_records={sum(len(v) for v in additions.values())}")
    print(f"backend_bytes={sum(len(x) for x in out.values())}")
    print(f"backend_bundle_sha256={h.hexdigest()}")

if __name__ == "__main__":
    main()
