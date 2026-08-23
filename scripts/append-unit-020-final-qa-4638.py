#!/usr/bin/env python3
"""Append the final Unit 020 QA witness after ADV-0288/0289 closure."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
QA_PATH = LANE / "qa/UNIT_020_QA.json"
SOURCE = LANE / "source/id-ID/units/unit-020-lecture-020.md"
QA_SHA = "4638ac3e2a01c1f212c2b60133f78f1fdd4a1f9c21a9a4cb12e32ff10ba8653e"
SOURCE_SHA = "ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3"
ROOT = "unit:o012-rbt-u020"
RIGHTS = "rights:o012-units-001-020-composite-cc-by-4.0-final-ed086"
STAMP = "2026-08-23T00:00:00Z"
WORKFLOW = "o012-d60-id-reader-production"
SCHEMA = "curriculum.interop"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")

def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def canon(o: dict[str, Any]) -> bytes:
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode() + b"\n"

def common(kind: str, ident: str) -> dict[str, Any]:
    return {"entity_type": kind, "id": ident, "schema": SCHEMA, "schema_version": "0.1.0",
            "status": "active", "supersedes": None, "timestamp": STAMP, "workflow": WORKFLOW}

def main() -> None:
    qa = QA_PATH.read_bytes()
    source = SOURCE.read_bytes()
    if len(qa) != 3717 or digest(qa) != QA_SHA:
        raise SystemExit(f"QA JSON identity mismatch: {len(qa)} {digest(qa)}")
    if len(source) != 45786 or digest(source) != SOURCE_SHA:
        raise SystemExit("source identity mismatch")
    qobj = json.loads(qa.decode("utf-8"))
    if qobj.get("status") != "PASS" or qobj.get("unit", {}).get("sha256") != SOURCE_SHA:
        raise SystemExit("QA JSON does not PASS/bind final source")
    checks = {c.get("check"): c for c in qobj.get("checks", [])}
    if checks.get("terminology_and_ledger", {}).get("detail") != "TERM tail=289; ADV tail=289; new controls present":
        raise SystemExit("QA JSON does not bind ledger tail 289")
    tables: dict[str, dict[str, dict[str, Any]]] = {}
    raws: dict[str, bytes] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        raws[name] = raw
        table: dict[str, dict[str, Any]] = {}
        for line in raw.splitlines(keepends=True):
            obj = json.loads(line.decode())
            if canon(obj) != line or obj["id"] in table:
                raise SystemExit(f"{name}: malformed historical JSONL")
            table[obj["id"]] = obj
        tables[name] = table
    all_ids = {x for t in tables.values() for x in t}
    for ident in ("artifact:o012-u020-qa-final-ed086", "qa:o012-u020-final-qa",
                  "rights:o012-units-001-020-composite-cc-by-4.0-final-ed086", ROOT):
        if ident not in all_ids:
            raise SystemExit(f"required predecessor missing: {ident}")
    additions = {name: [] for name in FILES}
    def add(name: str, obj: dict[str, Any]) -> None:
        if obj["id"] in all_ids or any(obj["id"] == x["id"] for xs in additions.values() for x in xs):
            raise SystemExit(f"duplicate final QA ID: {obj['id']}")
        additions[name].append(obj)
    aid = "artifact:o012-u020-qa-final-4638"
    art = common("artifact", aid)
    art.update({"bytes": 3717, "locale": "id-ID", "manifest_artifact_id": None,
                "media_type": "application/json", "path": "qa/UNIT_020_QA.json",
                "qa_event_ids": ["qa:o012-u020-final-qa-4638"],
                "rights_component_id": RIGHTS, "sha256": QA_SHA,
                "toolchain": "Final Unit 020 QA JSON after ADV-0288/0289 closure.",
                "translation_state": "built", "unit_id": ROOT,
                "supersedes": "artifact:o012-u020-qa-final-ed086"})
    add("artifacts.jsonl", art)
    qid = "qa:o012-u020-final-qa-4638"
    q = common("qa_event", qid)
    q.update({"note": "Final Unit 020 QA JSON PASS binds ed086 and terminology/adverse ledger tails TERM-0289 and ADV-0289.",
              "qa_type": "source", "result": "passed", "unit_id": ROOT,
              "witness_artifact_ids": [aid, "artifact:o012-u020-source-final-ed086"]})
    add("qa.jsonl", q)
    def relation(ident: str, source_id: str, typ: str, target_id: str, note: str) -> None:
        r = common("relation", ident)
        r.update({"from_id": source_id, "note": note, "relation_type": typ, "to_id": target_id})
        add("relations.jsonl", r)
    relation("relation:supersedes:o012-u020-qa-4638", aid, "supersedes",
             "artifact:o012-u020-qa-final-ed086", "QA witness updated after ADV-0288/0289 closure.")
    relation("relation:qa:o012-u020-final-qa-4638", qid, "illustrates", aid,
             "Final QA event is witnessed by the exact 4638ac artifact.")
    merged = all_ids | {x["id"] for xs in additions.values() for x in xs}
    for xs in additions.values():
        for obj in xs:
            for field in ("from_id", "to_id", "unit_id", "rights_component_id", "supersedes"):
                if obj.get(field) is not None and obj[field] not in merged:
                    raise SystemExit(f"unknown ref {obj['id']}.{field}")
            for field in ("witness_artifact_ids", "qa_event_ids"):
                if any(x not in merged for x in obj.get(field, [])):
                    raise SystemExit(f"unknown list ref {obj['id']}.{field}")
    out = {}
    for name in FILES:
        if (BACKEND / name).read_bytes() != raws[name]:
            raise SystemExit(f"historical bytes changed: {name}")
        out[name] = raws[name] + b"".join(canon(x) for x in sorted(additions[name], key=lambda x: x["id"]))
    for name, raw in out.items():
        (BACKEND / name).write_bytes(raw)
    h = hashlib.sha256()
    for name in FILES:
        h.update(name.encode()); h.update(b"\0"); h.update(out[name])
    print("Unit 020 final QA 4638 append: PASS")
    print("new_records=4 (artifact, QA, 2 relations)")
    print(f"backend_bytes={sum(len(x) for x in out.values())}")
    print(f"backend_bundle_sha256={h.hexdigest()}")

if __name__ == "__main__":
    main()
