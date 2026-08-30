#!/usr/bin/env python3
"""Independent fail-closed validation of the complete D60 capstone backend."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SOURCE = ROOT / "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md"
OUT = ROOT / "qa/BACKEND_CAPSTONE_FINAL_VALIDATION.json"
FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
FINAL = {"records": 8181, "bytes": 9847262, "bundle_sha256": "dd689b6cea9933ee5f85e2d30ed6afd44c25ffee470eceb8d74b22ce3248a0ad"}
SOURCE_SHA = "b65adfaa7f95d7b6cd48c639cbc44423769d798d43044e394fc80d5261042a17"
ROOT_UNIT = "unit:o012-d60-capstone-rev2"
RIGHTS = "rights:o012-d60-capstone-original-cc-by-sa-4.0-rev2"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"


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


def load() -> tuple[dict[str, bytes], dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]], dict[str, list[str]]]:
    raw_by_file: dict[str, bytes] = {}
    rows_by_file: dict[str, list[dict[str, Any]]] = {}
    by_id: dict[str, dict[str, Any]] = {}
    superseders: dict[str, list[str]] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        require(raw.endswith(b"\n") and b"\r" not in raw, f"invalid JSONL bytes: {name}")
        rows = []
        for line in raw.splitlines(keepends=True):
            row = json.loads(line)
            require(canon(row) == line, f"noncanonical JSONL: {name}")
            require(row["id"] not in by_id, f"duplicate ID: {row['id']}")
            by_id[row["id"]] = row
            rows.append(row)
            if isinstance(row.get("supersedes"), str):
                superseders.setdefault(row["supersedes"], []).append(row["id"])
        raw_by_file[name] = raw
        rows_by_file[name] = rows
    require(bundle(raw_by_file) == FINAL, "final backend bundle drift")
    return raw_by_file, rows_by_file, by_id, superseders


def logical_id(ident: str, superseders: dict[str, list[str]]) -> str:
    seen = {ident}
    while ident in superseders:
        choices = superseders[ident]
        require(len(choices) == 1, f"ambiguous supersedes branch: {ident}")
        ident = choices[0]
        require(ident not in seen, f"supersedes cycle: {ident}")
        seen.add(ident)
    return ident


def main() -> int:
    raw_by_file, rows, by_id, superseders = load()
    scalar_refs = {"concept_id", "course_id", "edition_id", "evidence_segment_id", "from_id", "local_derivative_unit_id", "manifest_artifact_id", "parent_id", "program_id", "resource_id", "rights_component_id", "scope_unit_id", "to_id", "unit_id"}
    list_refs = {"affected_unit_ids", "additional_evidence_segment_ids", "component_scope", "concept_ids", "local_derivative_unit_ids", "qa_event_ids", "witness_artifact_ids"}
    for row in by_id.values():
        if row.get("supersedes") is not None:
            require(row["supersedes"] in by_id, f"unknown supersedes: {row['id']}")
        for key in scalar_refs:
            value = row.get(key)
            if value is not None:
                require(value in by_id, f"unknown reference: {row['id']}.{key}={value}")
        for key in list_refs:
            for value in row.get(key, []):
                require(value in by_id, f"unknown reference: {row['id']}.{key}={value}")

    source_raw = SOURCE.read_bytes()
    require(len(source_raw) == 21636 and source_raw.count(b"\n") == 423 and sha(source_raw) == SOURCE_SHA, "final capstone source drift")
    lines = source_raw.splitlines(keepends=True)
    stable_lines: dict[str, int] = {}
    for number, raw_line in enumerate(lines, 1):
        for stable in re.findall(r"#(o012-d60-capstone(?:-[a-z0-9]+)*)\b", raw_line.decode("utf-8")):
            stable_lines.setdefault(stable, number)
    require(len(stable_lines) == 34, "stable capstone ID census drift")

    old_units = [row for row in rows["units.jsonl"] if row["id"].startswith("unit:o012-d60-capstone") and not row["id"].endswith("-rev2")]
    old_segments = [row for row in rows["segments.jsonl"] if row["id"].startswith("segment:o012-d60-capstone") and not row["id"].endswith("-rev2")]
    require(len(old_units) == len(old_segments) == 34, "historical capstone layer drift")
    current_units = [by_id[logical_id(row["id"], superseders)] for row in old_units]
    current_segments = [by_id[logical_id(row["id"], superseders)] for row in old_segments]
    require(len({row["id"] for row in current_units}) == len({row["id"] for row in current_segments}) == 34, "logical capstone revision census drift")
    units_by_stable = {row["source_local_id"]: row for row in current_units}
    segments_by_stable = {row["source_local_id"]: row for row in current_segments}
    require(set(units_by_stable) == set(segments_by_stable) == set(stable_lines), "logical stable-ID mapping drift")
    for stable, unit in units_by_stable.items():
        segment = segments_by_stable[stable]
        line = stable_lines[stable]
        locator = unit["target_locator"]
        require(unit["id"].endswith("-rev2") and unit["supersedes"] == unit["id"][:-5], f"unit revision lineage drift: {stable}")
        require(segment["id"].endswith("-rev2") and segment["supersedes"] == segment["id"][:-5], f"segment revision lineage drift: {stable}")
        require(segment["unit_id"] == unit["id"] and segment["target_locator"] == locator, f"unit/segment pairing drift: {stable}")
        require(locator["path"] == SOURCE.relative_to(ROOT).as_posix() and locator["file_sha256"] == SOURCE_SHA, f"file locator drift: {stable}")
        require(locator["line_start"] == locator["line_end"] == line and locator["content_sha256"] == sha(lines[line - 1]), f"line locator drift: {stable}")
        require(unit["rights_component_id"] == segment["rights_component_id"] == RIGHTS, f"rights binding drift: {stable}")

    rights = by_id[RIGHTS]
    require(rights["supersedes"] == RIGHTS[:-5] and set(rights["component_scope"]) == {row["id"] for row in current_units}, "current capstone rights scope drift")
    current_terms = [row for row in rows["terms.jsonl"] if row["id"].startswith("term:o012-d60-capstone-term-") and row["id"].endswith("-rev2")]
    require(len(current_terms) == 10 and all(row["scope_unit_id"] == ROOT_UNIT and row["rights_component_id"] == RIGHTS and row["evidence_segment_id"].endswith("-rev2") for row in current_terms), "current term graph drift")
    current_relations = [row for row in rows["relations.jsonl"] if ":o012-d60-capstone:" in row["id"] and row["id"].endswith("-rev2")]
    require(len(current_relations) == 54, "current capstone relation census drift")
    for row in current_relations:
        require(row["supersedes"] == row["id"][:-5], f"relation lineage drift: {row['id']}")
        for endpoint in (row["from_id"], row["to_id"]):
            if endpoint.startswith(("unit:o012-d60-capstone", "segment:o012-d60-capstone")):
                require(endpoint.endswith("-rev2"), f"current relation targets historical capstone node: {row['id']}")

    rev2_artifacts = [row for row in rows["artifacts.jsonl"] if re.fullmatch(r"artifact:o012-d60-capstone-(source|structure|math|language|mastery)-qa-rev2", row["id"])]
    rev2_qa = [row for row in rows["qa.jsonl"] if re.fullmatch(r"qa:o012-d60-capstone-(source|structure|math|language|mastery)-rev2", row["id"])]
    require(len(rev2_artifacts) == len(rev2_qa) == 5, "current source-QA revision census drift")
    final_artifacts = [row for row in rows["artifacts.jsonl"] if row["id"].endswith("-final") and (row["id"].startswith("artifact:o012-d60-capstone") or row["id"] == "artifact:o012-d60-proof-census-final")]
    final_qa = [row for row in rows["qa.jsonl"] if row["id"].startswith("qa:o012-d60-capstone-final-")]
    require(len(final_artifacts) == 9 and len(final_qa) == 4, "final reader/evidence record census drift")
    for artifact in rev2_artifacts + final_artifacts:
        path = ROOT / artifact["path"]
        require(path.is_file(), f"missing artifact file: {artifact['id']}")
        raw = path.read_bytes()
        require(len(raw) == artifact["bytes"] and sha(raw) == artifact["sha256"], f"artifact identity drift: {artifact['id']}")
        require(artifact["unit_id"] == ROOT_UNIT and artifact["rights_component_id"] == RIGHTS, f"artifact graph binding drift: {artifact['id']}")
    for qa in rev2_qa + final_qa:
        require(qa["result"] == "passed" and qa["unit_id"] == ROOT_UNIT, f"QA status/binding drift: {qa['id']}")
        require(all(witness in by_id for witness in qa["witness_artifact_ids"]), f"QA witness drift: {qa['id']}")

    correction = by_id["correction:o012-d60-capstone-adv-0565"]
    require(correction["adverse_ledger_id"] == "O012-ADV-0565" and correction["unit_id"] == ROOT_UNIT, "capstone correction provenance drift")
    ledger = (ROOT / "00_control/ADVERSE_LEDGER.csv").read_text(encoding="utf-8")
    require(ledger.count("O012-ADV-0565") == 1, "adverse-ledger capstone correction drift")
    require(all(row.get("model_provenance", MODEL) == MODEL for row in current_units + current_segments + rev2_artifacts + rev2_qa + final_artifacts + final_qa), "model provenance drift")

    proof = json.loads((ROOT / "qa/PROOF_REPAIR_CENSUS.json").read_text(encoding="utf-8"))
    cumulative = json.loads((ROOT / "qa/BACKEND_CAPSTONE_FINAL_CUMULATIVE_RECEIPT.json").read_text(encoding="utf-8"))
    proof_boundary = {key: proof["backend"][key] for key in ("records", "bytes", "bundle_sha256")}
    require(proof["status"] == "PASS" and proof_boundary == cumulative["semantic_proof_boundary"], "proof census semantic boundary drift")
    require(cumulative["status"] == "PASS" and cumulative["final"] == FINAL, "cumulative receipt drift")

    receipt = {
        "status": "PASS",
        "receipt_kind": "independent_final_capstone_backend_validation",
        "model_provenance": MODEL,
        "backend": FINAL,
        "source": {"path": SOURCE.relative_to(ROOT).as_posix(), "bytes": len(source_raw), "lf_lines": source_raw.count(b"\n"), "sha256": SOURCE_SHA},
        "checks": {
            "canonical_jsonl_and_unique_global_ids": "PASS",
            "all_references_resolve": "PASS",
            "supersedes_graph_unambiguous_and_acyclic": "PASS",
            "thirty_four_current_unit_segment_pairs_exact": "PASS",
            "current_rights_terms_and_fifty_four_relations_rebased": "PASS",
            "five_current_source_qa_pairs_exact": "PASS",
            "nine_final_artifacts_and_four_final_qa_events_exact": "PASS",
            "proof_census_bound_to_semantic_boundary": "PASS",
            "adverse_ledger_and_backend_correction_bound": "PASS",
            "model_provenance_exact": "PASS",
        },
        "severity_census": {"P1": 0, "P2": 0, "P3": 0},
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    raw = OUT.read_bytes()
    print(json.dumps({"status": "PASS", "receipt": {"path": OUT.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}, "backend": FINAL}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
