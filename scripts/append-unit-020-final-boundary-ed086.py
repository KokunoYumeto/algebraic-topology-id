#!/usr/bin/env python3
"""Append the final Unit 020 portability boundary after the cda9 snapshot.

This is intentionally a second, append-only transaction.  The first Unit 020
records remain immutable historical evidence; this transaction adds a final
source/QA witness and explicit supersession relations, without duplicating any
stable unit or segment IDs.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE = LANE / "source/id-ID/units/unit-020-lecture-020.md"
QA_JSON = LANE / "qa/UNIT_020_QA.json"
WORKFLOW = "o012-d60-id-reader-production"
SCHEMA = "curriculum.interop"
VERSION = "0.1.0"
STAMP = "2026-08-23T00:00:00Z"
ROOT = "unit:o012-rbt-u020"
EDITION = "edition:roberts-at-2019-b947ad2"
RESOURCE = "resource:roberts-algebraic-topology-2019"
OLD_ASSET = "asset:o012-u020-source-markdown"
OLD_CUMULATIVE = "rights:o012-units-001-020-composite-cc-by-4.0"
FINAL_CUMULATIVE = "rights:o012-units-001-020-composite-cc-by-4.0-final-ed086"
SOURCE_BYTES = 45786
SOURCE_LINES = 1425
SOURCE_SHA = "ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3"
QA_BYTES = 3717
QA_SHA = "05bc5a51420d15e044ae1c113616e9c371728593b6666886dba1cbf39beac24f"
REVIEW = LANE / "qa/UNIT_020_INDEPENDENT_REVIEW.md"
REVIEW_BYTES = 2663
REVIEW_SHA = "2599d076e43ea8d826f3bfc98a68c9ec9eee3c1a1ca505cc9e53f5d4a7bbae3f"
HANDOFF = LANE / "qa/UNIT_020_TRANSLATION_HANDOFF.md"
HANDOFF_BYTES = 1803
HANDOFF_SHA = "8fe483bedde0b69044fc0f1be6d5cd6d16055bea361920719520f162e84ce7a8"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"

def common(kind: str, ident: str) -> dict[str, Any]:
    return {"entity_type": kind, "id": ident, "schema": SCHEMA, "schema_version": VERSION,
            "status": "active", "supersedes": None, "timestamp": STAMP, "workflow": WORKFLOW}

def load() -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, bytes]]:
    tables: dict[str, dict[str, dict[str, Any]]] = {}
    raws: dict[str, bytes] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: malformed JSONL")
        table: dict[str, dict[str, Any]] = {}
        for line in raw.splitlines(keepends=True):
            obj = json.loads(line.decode("utf-8"))
            ident = obj.get("id")
            if not isinstance(ident, str) or ident in table or canon(obj) != line:
                raise SystemExit(f"{name}: duplicate/noncanonical historical line")
            table[ident] = obj
        tables[name] = table
        raws[name] = raw
    return tables, raws

def main() -> None:
    tables, raws = load()
    all_ids = {ident for table in tables.values() for ident in table}
    required = {
        OLD_ASSET,
        "artifact:o012-u020-independent-review",
        "artifact:o012-u020-qa",
        "qa:o012-u020-source-integrity",
        "rights:o012-units-001-020-composite-cc-by-4.0",
        ROOT,
    }
    if not required <= all_ids:
        raise SystemExit(f"pre-final boundary records missing: {sorted(required - all_ids)}")
    old_asset = tables["assets.jsonl"][OLD_ASSET]
    if old_asset.get("sha256") != "cda9ba7d3651feb45a4fa9b595a29772d86ef2c8dc5a5b799489b76b14032595":
        raise SystemExit("cda9 historical asset does not bind the expected snapshot")
    source = SOURCE.read_bytes()
    if len(source) != SOURCE_BYTES or digest(source) != SOURCE_SHA or len(source.splitlines()) != SOURCE_LINES:
        raise SystemExit(f"final source identity mismatch: {len(source)} bytes {digest(source)}")
    qa = QA_JSON.read_bytes()
    if len(qa) != QA_BYTES or digest(qa) != QA_SHA:
        raise SystemExit(f"final QA JSON identity mismatch: {len(qa)} bytes {digest(qa)}")
    qobj = json.loads(qa.decode("utf-8"))
    if qobj.get("status") != "PASS" or qobj.get("unit", {}).get("sha256") != SOURCE_SHA:
        raise SystemExit("final QA JSON is not a PASS bound to ed086")
    review = REVIEW.read_bytes()
    handoff = HANDOFF.read_bytes()
    if len(review) != REVIEW_BYTES or digest(review) != REVIEW_SHA:
        raise SystemExit(f"final review identity mismatch: {len(review)} bytes {digest(review)}")
    if len(handoff) != HANDOFF_BYTES or digest(handoff) != HANDOFF_SHA:
        raise SystemExit(f"final handoff identity mismatch: {len(handoff)} bytes {digest(handoff)}")
    new: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    def add(name: str, obj: dict[str, Any]) -> None:
        ident = obj["id"]
        if ident in all_ids or any(ident == x["id"] for xs in new.values() for x in xs):
            raise SystemExit(f"duplicate final-boundary id: {ident}")
        new[name].append(obj)
    # A final source asset and evidence artifact bind the bytes that are
    # release-authoritative after the delimiter/portability repair.
    asset = common("asset", "asset:o012-u020-source-markdown-ed086")
    asset.update({"bytes": SOURCE_BYTES, "edition_id": EDITION,
                  "media_type": "text/markdown; charset=utf-8",
                  "path": "source/id-ID/units/unit-020-lecture-020.md",
                  "resource_id": RESOURCE, "rights_component_id": OLD_CUMULATIVE,
                  "role": "canonical_reader_source_final",
                  "sha256": SOURCE_SHA, "supersedes": OLD_ASSET})
    add("assets.jsonl", asset)
    witness = common("artifact", "artifact:o012-u020-source-final-ed086")
    witness.update({"bytes": SOURCE_BYTES, "locale": "id-ID", "manifest_artifact_id": None,
                    "media_type": "text/markdown; charset=utf-8",
                    "path": "source/id-ID/units/unit-020-lecture-020.md",
                    "qa_event_ids": ["qa:o012-u020-final-source-integrity", "qa:o012-u020-final-qa"],
                    "rights_component_id": OLD_CUMULATIVE, "sha256": SOURCE_SHA,
                    "toolchain": "Final Unit 020 source witness after portability delimiter repair.",
                    "translation_state": "source_frozen", "unit_id": ROOT,
                    "supersedes": "artifact:o012-u020-qa"})
    add("artifacts.jsonl", witness)
    qa_art = common("artifact", "artifact:o012-u020-qa-final-ed086")
    qa_art.update({"bytes": QA_BYTES, "locale": "id-ID", "manifest_artifact_id": None,
                   "media_type": "application/json", "path": "qa/UNIT_020_QA.json",
                   "qa_event_ids": ["qa:o012-u020-final-source-integrity", "qa:o012-u020-final-qa"],
                   "rights_component_id": OLD_CUMULATIVE, "sha256": QA_SHA,
                   "toolchain": "Bounded Unit 020 QA JSON with math delimiter sanity.",
                   "translation_state": "built", "unit_id": ROOT,
                   "supersedes": "artifact:o012-u020-qa"})
    add("artifacts.jsonl", qa_art)
    review_art = common("artifact", "artifact:o012-u020-independent-review-final-ed086")
    review_art.update({"bytes": REVIEW_BYTES, "locale": "id-ID", "manifest_artifact_id": None,
                       "media_type": "text/markdown; charset=utf-8",
                       "path": "qa/UNIT_020_INDEPENDENT_REVIEW.md",
                       "qa_event_ids": ["qa:o012-u020-final-source-integrity", "qa:o012-u020-final-qa"],
                       "rights_component_id": OLD_CUMULATIVE, "sha256": REVIEW_SHA,
                       "toolchain": "Final Unit 020 independent review witness after portability repair.",
                       "translation_state": "mathematically_reviewed", "unit_id": ROOT,
                       "supersedes": "artifact:o012-u020-independent-review"})
    add("artifacts.jsonl", review_art)
    handoff_art = common("artifact", "artifact:o012-u020-translation-handoff-final-ed086")
    handoff_art.update({"bytes": HANDOFF_BYTES, "locale": "id-ID", "manifest_artifact_id": None,
                        "media_type": "text/markdown; charset=utf-8",
                        "path": "qa/UNIT_020_TRANSLATION_HANDOFF.md",
                        "qa_event_ids": ["qa:o012-u020-final-source-integrity", "qa:o012-u020-final-qa"],
                        "rights_component_id": OLD_CUMULATIVE, "sha256": HANDOFF_SHA,
                        "toolchain": "Final Unit 020 translation handoff witness after portability repair.",
                        "translation_state": "source_frozen", "unit_id": ROOT,
                        "supersedes": "artifact:o012-u020-translation-handoff"})
    add("artifacts.jsonl", handoff_art)
    # Explicitly record why the cda9 snapshot remains in the ledger but is not
    # release-authoritative.
    corr = common("correction", "correction:o012-u020-pre-portability-snapshot")
    corr.update({"adverse_ledger_id": "O012-ADV-UNIT20-SNAPSHOT",
                 "affected_unit_ids": [ROOT], "correction_type": "source_boundary",
                 "edition_id": EDITION,
                 "evidence": "Unit 020 cda9 snapshot asset/artifact records; final source witness ed086",
                 "evidence_segment_id": "segment:o012-rbt-l20-notice", "severity": "P1",
                 "rationale": "Portability delimiter repair changed the release-boundary bytes while preserving all 73 stable IDs.",
                 "resource_id": RESOURCE, "source_defect": "The cda9 snapshot predates the final math-delimiter portability repair.",
                 "target_change": "Use ed086 as release-authoritative and retain cda9 only as superseded historical evidence.",
                 "unit_id": ROOT, "upstream_report_disposition": "not_contacted",
                 "supersedes": "correction:o012-u020-adv-0287"})
    add("corrections.jsonl", corr)
    # Final QA events.
    q = common("qa_event", "qa:o012-u020-final-source-integrity")
    q.update({"note": "Final Unit 020 reader is 45,786 bytes/1,425 LF lines, SHA-256 ed086dfe; source, stable IDs, and QA JSON bind this exact boundary.",
              "qa_type": "source", "result": "passed", "unit_id": ROOT,
              "witness_artifact_ids": ["artifact:o012-u020-source-final-ed086", "artifact:o012-u020-qa-final-ed086"]})
    add("qa.jsonl", q)
    q = common("qa_event", "qa:o012-u020-final-qa")
    q.update({"note": "Final Unit 020 QA JSON reports PASS, including math_delimiter_sanity and source_review_handoff_binding.",
              "qa_type": "build", "result": "passed", "unit_id": ROOT,
              "witness_artifact_ids": ["artifact:o012-u020-qa-final-ed086", "artifact:o012-u020-source-final-ed086"]})
    add("qa.jsonl", q)
    # Final cumulative rights pointer; the previous 001-020 record remains a
    # historical cda9 boundary and is not rewritten.
    rights = common("rights", FINAL_CUMULATIVE)
    rights.update({"attribution": "Cumulative Roberts Units 001-020 Indonesian reader; final Unit 020 source boundary ed086.",
                   "change_notice": "Final portability-corrected boundary; component records remain separately identifiable.",
                   "component_scope": [f"unit:o012-rbt-u{n:03d}" for n in range(1, 21)],
                   "license_expression": "CC-BY-4.0",
                   "license_url": "https://creativecommons.org/licenses/by/4.0/",
                   "non_endorsement": "Independent edition; no source-author endorsement.",
                   "third_party_status": "Component-scoped rights records control.",
                   "supersedes": OLD_CUMULATIVE})
    add("rights.jsonl", rights)
    def relation(ident: str, source_id: str, typ: str, target_id: str, note: str) -> None:
        r = common("relation", ident)
        r.update({"from_id": source_id, "note": note, "relation_type": typ, "to_id": target_id})
        add("relations.jsonl", r)
    relation("relation:supersedes:o012-u020-source-ed086", "asset:o012-u020-source-markdown-ed086",
             "supersedes", OLD_ASSET, "Final ed086 source asset supersedes the cda9 pre-portability snapshot.")
    relation("relation:supersedes:o012-u020-qa-ed086", "artifact:o012-u020-qa-final-ed086",
             "supersedes", "artifact:o012-u020-qa", "Final QA JSON supersedes the cda9-bound QA witness.")
    relation("relation:supersedes:o012-u020-review-ed086", "artifact:o012-u020-independent-review-final-ed086",
             "supersedes", "artifact:o012-u020-independent-review", "Final independent review supersedes the pre-portability witness.")
    relation("relation:supersedes:o012-u020-handoff-ed086", "artifact:o012-u020-translation-handoff-final-ed086",
             "supersedes", "artifact:o012-u020-translation-handoff", "Final handoff supersedes the pre-portability witness.")
    relation("relation:boundary:o012-u020-final-ed086", FINAL_CUMULATIVE, "contains",
             "artifact:o012-u020-source-final-ed086", "Final release-authoritative Unit 020 source boundary.")
    relation("relation:qa:o012-u020-final-ed086", "artifact:o012-u020-qa-final-ed086",
             "supersedes", "artifact:o012-u020-qa", "Final QA artifact supersedes the pre-portability witness.")
    # Referential closure for additions.
    merged_ids = set(all_ids) | {x["id"] for xs in new.values() for x in xs}
    for xs in new.values():
        for obj in xs:
            for field in ("from_id", "to_id", "unit_id", "edition_id", "resource_id",
                          "rights_component_id", "evidence_segment_id", "supersedes"):
                if obj.get(field) and obj[field] not in merged_ids:
                    raise SystemExit(f"unknown final reference {obj['id']}.{field}")
            for field in ("affected_unit_ids", "component_scope", "witness_artifact_ids"):
                if field in obj and any(x not in merged_ids for x in obj[field]):
                    raise SystemExit(f"unknown final list reference {obj['id']}.{field}")
    # Append only; compare the complete historical byte prefix immediately
    # before each write.
    out: dict[str, bytes] = {}
    for name in FILES:
        if (BACKEND / name).read_bytes() != raws[name]:
            raise SystemExit(f"historical prefix changed before write: {name}")
        out[name] = raws[name] + b"".join(canon(x) for x in sorted(new[name], key=lambda x: x["id"]))
    for name, raw in out.items():
        (BACKEND / name).write_bytes(raw)
    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(out[name])
    counts = {name: len(new[name]) for name in FILES}
    print("Unit 020 final ed086 boundary: PASS")
    print("new_records_by_file=" + json.dumps(counts, sort_keys=True))
    print(f"new_records={sum(counts.values())}")
    print(f"backend_bytes={sum(len(x) for x in out.values())}")
    print(f"backend_bundle_sha256={bundle.hexdigest()}")
    print(f"final_source_sha256={SOURCE_SHA}")
    print(f"final_qa_sha256={QA_SHA}")

if __name__ == "__main__":
    main()
