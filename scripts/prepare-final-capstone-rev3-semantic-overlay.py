#!/usr/bin/env python3
"""Prepare two byte-identical append-only rev3 candidates for the final capstone."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SOURCE = ROOT / "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md"
SOURCE_REL = "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md"
OUT = ROOT / "qa/capstone-final-rev3-backend-20260829"
FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
TIMESTAMP = "2026-08-29T00:00:00Z"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
OLD_SOURCE_SHA = "b65adfaa7f95d7b6cd48c639cbc44423769d798d43044e394fc80d5261042a17"
FINAL_SOURCE_SHA = "d26ad5224e61c62080e00074acabfd2cf680779a7bc5d0562cfccc6d715a09c9"
BASELINE = {
    "records": 8181,
    "bytes": 9847262,
    "bundle_sha256": "dd689b6cea9933ee5f85e2d30ed6afd44c25ffee470eceb8d74b22ce3248a0ad",
}
OLD_RIGHTS = "rights:o012-d60-capstone-original-cc-by-sa-4.0-rev2"
NEW_RIGHTS = "rights:o012-d60-capstone-original-cc-by-sa-4.0-rev3"
ROOT_OLD = "unit:o012-d60-capstone-rev2"
ROOT_NEW = "unit:o012-d60-capstone-rev3"


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(row: dict[str, Any]) -> bytes:
    return (json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def bundle(raw_by_file: dict[str, bytes]) -> dict[str, Any]:
    state = hashlib.sha256()
    records = 0
    byte_count = 0
    for name in FILES:
        raw = raw_by_file[name]
        records += len(raw.splitlines())
        byte_count += len(raw)
        state.update(name.encode("utf-8"))
        state.update(b"\0")
        state.update(raw)
    return {"records": records, "bytes": byte_count, "bundle_sha256": state.hexdigest()}


def load_backend() -> tuple[dict[str, bytes], dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    raw_by_file: dict[str, bytes] = {}
    rows_by_file: dict[str, list[dict[str, Any]]] = {}
    by_id: dict[str, dict[str, Any]] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        require(raw.endswith(b"\n") and b"\r" not in raw, f"invalid JSONL bytes: {name}")
        rows = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
        for row in rows:
            require(row["id"] not in by_id, f"duplicate live ID: {row['id']}")
            by_id[row["id"]] = row
        raw_by_file[name] = raw
        rows_by_file[name] = rows
    require(bundle(raw_by_file) == BASELINE, "live backend is not the exact final rev2/artifact boundary")
    return raw_by_file, rows_by_file, by_id


def source_state() -> tuple[list[bytes], dict[str, int]]:
    raw = SOURCE.read_bytes()
    require((len(raw), raw.count(b"\n"), sha(raw)) == (21744, 423, FINAL_SOURCE_SHA), "rev3 source identity drift")
    require(raw.endswith(b"\n") and b"\r" not in raw, "capstone source is not canonical LF")
    lines = raw.splitlines(keepends=True)
    found: dict[str, int] = {}
    for number, raw_line in enumerate(lines, 1):
        for ident in re.findall(r"#(o012-d60-capstone(?:-[a-z0-9]+)*)\b", raw_line.decode("utf-8")):
            found.setdefault(ident, number)
    require(len(found) == 34, f"expected 34 stable capstone IDs, got {len(found)}")
    return lines, found


def locator(lines: list[bytes], stable_lines: dict[str, int], ident: str) -> dict[str, Any]:
    line_number = stable_lines[ident]
    return {
        "content_sha256": sha(lines[line_number - 1]),
        "file_sha256": FINAL_SOURCE_SHA,
        "line_end": line_number,
        "line_start": line_number,
        "path": SOURCE_REL,
    }


def rev3_id(old_id: str) -> str:
    require(old_id.endswith("-rev2"), f"not an exact rev2 ID: {old_id}")
    return old_id[:-5] + "-rev3"


def clone_revision(row: dict[str, Any], new_id: str) -> dict[str, Any]:
    result = copy.deepcopy(row)
    result["id"] = new_id
    result["supersedes"] = row["id"]
    result["timestamp"] = TIMESTAMP
    return result


def make_additions(rows: dict[str, list[dict[str, Any]]], by_id: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    lines, stable_lines = source_state()
    additions = {name: [] for name in FILES}
    old_units = [r for r in rows["units.jsonl"] if r["id"].startswith("unit:o012-d60-capstone") and r["id"].endswith("-rev2")]
    old_segments = [r for r in rows["segments.jsonl"] if r["id"].startswith("segment:o012-d60-capstone") and r["id"].endswith("-rev2")]
    require(len(old_units) == len(old_segments) == 34, "expected exact 34-unit/34-segment rev2 capstone layer")
    require({r["source_local_id"] for r in old_units} == set(stable_lines), "rev2 unit stable-ID inventory drift")
    require({r["source_local_id"] for r in old_segments} == set(stable_lines), "rev2 segment stable-ID inventory drift")
    require({r["target_locator"]["file_sha256"] for r in old_units + old_segments} == {OLD_SOURCE_SHA}, "rev2 source hash drift")
    unit_map = {r["id"]: rev3_id(r["id"]) for r in old_units}
    segment_map = {r["id"]: rev3_id(r["id"]) for r in old_segments}
    require(unit_map[ROOT_OLD] == ROOT_NEW, "rev3 root mapping drift")

    old_rights = by_id[OLD_RIGHTS]
    new_rights = clone_revision(old_rights, NEW_RIGHTS)
    new_rights["component_scope"] = [unit_map[item] for item in old_rights["component_scope"]]
    new_rights["change_notice"] = (
        "Final original capstone revision after correction of the laboratory count, source-locus wording, "
        "and id-ID terminology; Roberts and Fomberg components remain separately attributed."
    )
    additions["rights.jsonl"].append(new_rights)

    for old in old_units:
        new = clone_revision(old, unit_map[old["id"]])
        stable = old["source_local_id"]
        new["target_locator"] = locator(lines, stable_lines, stable)
        new["rights_component_id"] = NEW_RIGHTS
        new["parent_id"] = unit_map.get(old.get("parent_id"), old.get("parent_id"))
        new["path"] = [unit_map.get(item, item) for item in old.get("path", [])]
        additions["units.jsonl"].append(new)
    for old in old_segments:
        new = clone_revision(old, segment_map[old["id"]])
        stable = old["source_local_id"]
        new["target_locator"] = locator(lines, stable_lines, stable)
        new["source_locator"]["line_start"] = stable_lines[stable]
        new["source_locator"]["line_end"] = stable_lines[stable]
        new["unit_id"] = unit_map[old["unit_id"]]
        new["rights_component_id"] = NEW_RIGHTS
        additions["segments.jsonl"].append(new)

    old_terms = [r for r in rows["terms.jsonl"] if r["id"].startswith("term:o012-d60-capstone-term-") and r["id"].endswith("-rev2")]
    require(len(old_terms) == 10, "expected ten current rev2 capstone terms")
    for old in old_terms:
        new = clone_revision(old, rev3_id(old["id"]))
        new["evidence_segment_id"] = segment_map[old["evidence_segment_id"]]
        new["scope_unit_id"] = unit_map[old["scope_unit_id"]]
        new["rights_component_id"] = NEW_RIGHTS
        additions["terms.jsonl"].append(new)

    old_relations = [r for r in rows["relations.jsonl"] if ":o012-d60-capstone:" in r["id"] and r["id"].endswith("-rev2")]
    require(len(old_relations) == 54, f"expected 54 current rev2 capstone relations, got {len(old_relations)}")
    reference_map = {**unit_map, **segment_map}
    for old in old_relations:
        new = clone_revision(old, rev3_id(old["id"]))
        new["from_id"] = reference_map.get(old["from_id"], old["from_id"])
        new["to_id"] = reference_map.get(old["to_id"], old["to_id"])
        additions["relations.jsonl"].append(new)

    qa_kinds = ("source", "structure", "math", "language", "mastery")
    artifact_map = {
        f"artifact:o012-d60-capstone-{kind}-qa-rev2": f"artifact:o012-d60-capstone-{kind}-qa-rev3"
        for kind in qa_kinds
    }
    qa_map = {
        f"qa:o012-d60-capstone-{kind}-rev2": f"qa:o012-d60-capstone-{kind}-rev3"
        for kind in qa_kinds
    }
    for old_id, new_id in artifact_map.items():
        old = by_id[old_id]
        path = ROOT / old["path"]
        raw = path.read_bytes()
        require(json.loads(raw).get("status") == "PASS", f"capstone QA is not PASS: {path}")
        new = clone_revision(old, new_id)
        new["bytes"] = len(raw)
        new["sha256"] = sha(raw)
        new["qa_event_ids"] = [qa_map[item] for item in old["qa_event_ids"]]
        new["unit_id"] = ROOT_NEW
        new["rights_component_id"] = NEW_RIGHTS
        new["toolchain"] = "Final D60 capstone rev3 source/QA; OpenAI Codex gpt-5.6-sol, Ultra."
        additions["artifacts.jsonl"].append(new)
    for old_id, new_id in qa_map.items():
        old = by_id[old_id]
        new = clone_revision(old, new_id)
        new["unit_id"] = ROOT_NEW
        new["witness_artifact_ids"] = [artifact_map[item] for item in old["witness_artifact_ids"]]
        new["note"] = old["note"].rstrip(".") + "; rev3 count, scope, and language correction verified."
        additions["qa.jsonl"].append(new)

    additions["corrections.jsonl"].append({
        "adverse_ledger_id": "O012-ADV-0566",
        "affected_unit_ids": sorted(unit_map.values()),
        "correction_type": "edition_original_pre_publication_scope_and_language_correction",
        "edition_id": "edition:fomberg-at-2025-563194f",
        "entity_type": "correction",
        "evidence": "final capstone source; refreshed static, mathematics, and source-language QA; adverse ledger O012-ADV-0566",
        "evidence_segment_id": "segment:o012-d60-capstone-rev3",
        "id": "correction:o012-d60-capstone-adv-0566",
        "rationale": "match the exact four-laboratory course scope, avoid an unsupported source-locus count, and use natural id-ID terminology",
        "resolution_status": "resolved_before_publication",
        "resource_id": "resource:fomberg-algebraic-topology-2025",
        "schema": "curriculum.interop",
        "schema_version": "0.1.0",
        "source_defect": "The pre-publication capstone named six laboratories although D60 has four, used an ambiguous count of nine source loci, and retained avoidable untranslated prose terms.",
        "status": "active",
        "supersedes": None,
        "target_change": "State four laboratories, refer to every recorded incomplete source locus without a false count, and normalize the listed Indonesian terms while preserving exact identifiers.",
        "timestamp": TIMESTAMP,
        "unit_id": ROOT_NEW,
        "upstream_report_disposition": "not_applicable_edition_original_pre_publication",
        "workflow": "o012-d60-id-reader-production",
    })
    for name in FILES:
        additions[name].sort(key=lambda row: row["id"])
    return additions


def validate(additions: dict[str, list[dict[str, Any]]], existing: dict[str, dict[str, Any]]) -> None:
    expected = {"artifacts.jsonl": 5, "corrections.jsonl": 1, "qa.jsonl": 5, "relations.jsonl": 54, "rights.jsonl": 1, "segments.jsonl": 34, "terms.jsonl": 10, "units.jsonl": 34}
    require({name: len(value) for name, value in additions.items() if value} == expected, "rev3 record census drift")
    new_rows = [row for values in additions.values() for row in values]
    new_ids = [row["id"] for row in new_rows]
    require(len(new_ids) == len(set(new_ids)) and not set(new_ids).intersection(existing), "rev3 ID collision")
    all_ids = set(existing).union(new_ids)
    scalar_refs = {"concept_id", "course_id", "edition_id", "evidence_segment_id", "from_id", "manifest_artifact_id", "parent_id", "program_id", "resource_id", "rights_component_id", "scope_unit_id", "to_id", "unit_id"}
    list_refs = {"affected_unit_ids", "component_scope", "concept_ids", "qa_event_ids", "witness_artifact_ids"}
    for row in new_rows:
        require(row.get("supersedes") is None or row["supersedes"] in existing, f"invalid supersedes: {row['id']}")
        for key in scalar_refs:
            if row.get(key) is not None:
                require(row[key] in all_ids, f"unknown reference {row[key]} from {row['id']}.{key}")
        for key in list_refs:
            for value in row.get(key, []):
                require(value in all_ids, f"unknown reference {value} from {row['id']}.{key}")
    units = {row["source_local_id"]: row for row in additions["units.jsonl"]}
    segments = {row["source_local_id"]: row for row in additions["segments.jsonl"]}
    require(set(units) == set(segments) and len(units) == 34, "rev3 unit/segment pairing drift")
    for stable in units:
        require(segments[stable]["unit_id"] == units[stable]["id"], f"rev3 unit link drift: {stable}")
        require(segments[stable]["target_locator"] == units[stable]["target_locator"], f"rev3 locator pairing drift: {stable}")
        require(units[stable]["target_locator"]["file_sha256"] == FINAL_SOURCE_SHA, f"rev3 source hash drift: {stable}")


def write_run(name: str, baseline_raw: dict[str, bytes], additions: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    target = OUT / name
    require(not target.exists(), f"candidate collision: {target}")
    target.mkdir(parents=True)
    suffix_raw: dict[str, bytes] = {}
    final_raw: dict[str, bytes] = {}
    identities: dict[str, dict[str, Any]] = {}
    for filename in FILES:
        raw = b"".join(canon(row) for row in additions[filename])
        suffix_raw[filename] = raw
        final_raw[filename] = baseline_raw[filename] + raw
        (target / filename).write_bytes(raw)
        identities[filename] = {"records": len(raw.splitlines()), "bytes": len(raw), "sha256": sha(raw)}
    receipt = {
        "status": "PASS_CANDIDATE",
        "receipt_kind": "final_capstone_semantic_rev3_append_only_candidate",
        "timestamp": TIMESTAMP,
        "model_provenance": MODEL,
        "source": {"path": SOURCE_REL, "bytes": SOURCE.stat().st_size, "lf_lines": SOURCE.read_bytes().count(b"\n"), "sha256": FINAL_SOURCE_SHA},
        "baseline": bundle(baseline_raw),
        "suffix": identities,
        "suffix_total": bundle(suffix_raw),
        "final": bundle(final_raw),
    }
    (target / "RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    return receipt


def main() -> int:
    require(not OUT.exists(), f"candidate output already exists: {OUT}")
    baseline_raw, rows, existing = load_backend()
    additions = make_additions(rows, existing)
    validate(additions, existing)
    OUT.mkdir(parents=True)
    first = write_run("run-a", baseline_raw, additions)
    second = write_run("run-b", baseline_raw, additions)
    require(first == second, "rev3 candidate receipts differ")
    for filename in (*FILES, "RECEIPT.json"):
        require((OUT / "run-a" / filename).read_bytes() == (OUT / "run-b" / filename).read_bytes(), f"rev3 candidate bytes differ: {filename}")
    print(json.dumps({"status": "PASS", "candidate": first}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
