#!/usr/bin/env python3
"""Fail-closed census of proof repairs in the frozen Unit 007 backend prefix.

The live backend may have later append-only records.  This program deliberately
reads only the exact byte prefixes sealed by the Unit 007 cumulative receipt.
It accepts mathematical closure only from structured backend fields and
hash-bound structured QA; it never infers closure from prose.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
OUTPUT = ROOT / "qa" / "PROOF_REPAIR_CENSUS.json"
UPSTREAM = (
    ROOT
    / "authority"
    / "upstream"
    / "math-notes-563194fae879178b9a6871b249513bfc27968975"
    / "tree"
    / "algebraic_topology.tex"
)
UPSTREAM_SHA256 = "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483"
UNIT007_RECEIPT = ROOT / "qa" / "BACKEND_APPEND_ONLY_FOMBERG_UNIT_007_CUMULATIVE_RECEIPT.json"
UNIT007_BUNDLE_SHA256 = "523b570517eb54720c50007aacc5d4eea525ea252b9ca1f6f45b027182354765"
UNIT007_TOTAL_RECORDS = 6742
UNIT007_TOTAL_BYTES = 8213649

FROZEN = {
    "artifacts.jsonl": (189, 153754, "7294792526f75a1ea2409f797fa25c28694e115c95541387482602447e6ba646"),
    "assets.jsonl": (87, 64692, "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (483, 152695, "720d96a10a3c2abebab164e2181486743ef99efb50c6ef419faefbf528b8ead3"),
    "corrections.jsonl": (564, 594720, "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb"),
    "qa.jsonl": (162, 88999, "da5c09949d53c4f77ca0c4089d99ca6ba178bdc4b7a463eb8bf68a55e9853e19"),
    "relations.jsonl": (784, 329688, "1aea5c4f3e619718bda4c065f9d70d3281b4b35bcd712e8c98fcfbcf7509fefa"),
    "rights.jsonl": (103, 93018, "212673ced3907e59f8a38603f1c625a263a95656908c656a86e0d881b77f93b6"),
    "segments.jsonl": (1929, 3130165, "6078880c58c6b3194e874c85b4f2716b5436f0559f607f1b7551cd5140ffa376"),
    "terms.jsonl": (476, 315218, "4b82f9d582ba747829373a7935fcc3cae56b96fd6b7486969ebb6d54cf927c50"),
    "units.jsonl": (1959, 3286326, "e2855fe4bb13ce55f48b29bd7d3279d5db7023ef6207fd07bf7b98385d5ddb63"),
}

COMPLETE_PROOF_STATUSES = {
    "complete_original_repair",
    "complete_edition_repair_of_source_argument",
}


def spec(
    repair_id: str,
    tier: str,
    route: str,
    qa_unit_id: str,
    proof_ids: list[str],
    target_ids: list[str],
    source_ids: list[str],
    selection_loci: list[dict[str, Any]],
    review_path: str,
    review_mode: str,
    correction_ids: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "repair_id": repair_id,
        "tier": tier,
        "route": route,
        "qa_unit_id": qa_unit_id,
        "proof_ids": proof_ids,
        "target_ids": target_ids,
        "source_ids": source_ids,
        "selection_loci": selection_loci,
        "review_path": review_path,
        "review_mode": review_mode,
        "correction_ids": correction_ids or [],
    }


SPECS = [
    spec(
        "FOM-U001-PR-001", "additional_pre_dossier", "D60-R08", "unit:o012-fom-u001",
        ["segment:o012-fom-u001-proof-001"],
        ["segment:o012-fom-u001-lem-boundary-square"], [],
        [{"path": "algebraic_topology.tex", "line_start": 517, "line_end": 548, "note": "statement and repaired source proof"}],
        "qa/FOMBERG_UNIT_001_QA.json", "unit001_proof_closure",
    ),
    spec(
        "FOM-PR-01", "mandatory", "D60-R09", "unit:o012-fom-u002",
        ["segment:o012-fom-u002-proof-chain-map"],
        ["segment:o012-fom-u002-prop-chain-map"],
        ["segment:o012-fom-u002-omission-pr01"],
        [{"path": "algebraic_topology.tex", "line_start": 1001, "line_end": 1003}],
        "qa/FOMBERG_UNIT_002_QA.json", "unit002_proof_closure",
    ),
    spec(
        "FOM-PR-02", "mandatory", "D60-R09", "unit:o012-fom-u002",
        ["segment:o012-fom-u002-proof-induced-map-homomorphism"],
        ["segment:o012-fom-u002-prop-induced-map"],
        ["segment:o012-fom-u002-omission-pr02"],
        [{"path": "algebraic_topology.tex", "line_start": 1034, "line_end": 1034}],
        "qa/FOMBERG_UNIT_002_QA.json", "unit002_proof_closure",
    ),
    spec(
        "FOM-PR-03", "mandatory", "D60-R09", "unit:o012-fom-u002",
        ["segment:o012-fom-u002-proof-homotopy-equivalent"],
        ["segment:o012-fom-u002-cor-homotopy-equivalent"],
        ["segment:o012-fom-u002-omission-pr03"],
        [{"path": "algebraic_topology.tex", "line_start": 1121, "line_end": 1128}],
        "qa/FOMBERG_UNIT_002_QA.json", "unit002_proof_closure",
    ),
    spec(
        "FOM-PR-04", "mandatory", "D60-R10", "unit:o012-fom-u003",
        ["segment:o012-fom-u003-proof-long-exact-repair"],
        ["segment:o012-fom-u003-thm-long-exact"],
        ["segment:o012-fom-u003-omission-pr04"],
        [{"path": "algebraic_topology.tex", "line_start": 1869, "line_end": 1872}],
        "qa/FOMBERG_UNIT_003_QA.json", "unit003_proof_closure",
    ),
    spec(
        "FOM-PR-05", "mandatory", "D60-R11", "unit:o012-fom-u004",
        ["segment:o012-fom-u004-proof-pr05a", "segment:o012-fom-u004-proof-pr05b"],
        ["segment:o012-fom-u004-prop-small-chains", "segment:o012-fom-u004-prop-small-chains"],
        ["segment:o012-fom-u004-omission-pr05a", "segment:o012-fom-u004-omission-pr05b"],
        [
            {"path": "algebraic_topology.tex", "line_start": 2050, "line_end": 2070, "dossier_focus": "geometric subdivision and diameter iteration"},
            {"path": "algebraic_topology.tex", "line_start": 2071, "line_end": 2152, "dossier_focus": "arbitrarily small chains and chain homotopy"},
        ],
        "qa/fomberg-unit-004/INDEPENDENT_REVIEW_FINAL.json", "unit004_repair_list",
        ["correction:o012-fom-u004-adv-0500"],
    ),
    spec(
        "FOM-PR-06", "mandatory", "D60-R11", "unit:o012-fom-u004",
        ["segment:o012-fom-u004-proof-pr06"],
        ["segment:o012-fom-u004-thm-excision-cover"],
        ["segment:o012-fom-u004-omission-pr06"],
        [{"path": "algebraic_topology.tex", "line_start": 2160, "line_end": 2178, "dossier_focus": "excision; omission begins at 2160-2161"}],
        "qa/fomberg-unit-004/INDEPENDENT_REVIEW_FINAL.json", "unit004_repair_list",
    ),
    spec(
        "FOM-PR-07", "mandatory", "D60-R11", "unit:o012-fom-u004",
        ["segment:o012-fom-u004-proof-five-lemma-repair"],
        ["segment:o012-fom-u004-lem-five"],
        ["segment:o012-fom-u004-omission-pr07"],
        [{"path": "algebraic_topology.tex", "line_start": 2807, "line_end": 2810}],
        "qa/fomberg-unit-004/INDEPENDENT_REVIEW_FINAL.json", "unit004_repair_list",
    ),
    spec(
        "FOM-PR-08", "mandatory", "D60-R11", "unit:o012-fom-u004",
        ["segment:o012-fom-u004-proof-injectivity-comparison-repair"],
        ["segment:o012-fom-u004-prop-sing-simp"],
        ["segment:o012-fom-u004-omission-pr08"],
        [{"path": "algebraic_topology.tex", "line_start": 2838, "line_end": 2844}],
        "qa/fomberg-unit-004/INDEPENDENT_REVIEW_FINAL.json", "unit004_repair_list",
    ),
    spec(
        "FOM-PR-09", "later_admitted", "D60-R11", "unit:o012-fom-u004",
        ["segment:o012-fom-u004-proof-naturality-repair"],
        ["segment:o012-fom-u004-rem-naturality-chain-complexes"],
        ["segment:o012-fom-u004-omission-pr09"],
        [{"path": "algebraic_topology.tex", "line_start": 2617, "line_end": 2665}],
        "qa/fomberg-unit-004/INDEPENDENT_REVIEW_FINAL.json", "unit004_repair_list",
    ),
    spec(
        "FOM-PR-10", "later_admitted", "D60-R11", "unit:o012-fom-u004",
        ["segment:o012-fom-u004-proof-relative-generator-repair"],
        ["segment:o012-fom-u004-prop-sing-simp"],
        ["segment:o012-fom-u004-omission-pr10"],
        [{"path": "algebraic_topology.tex", "line_start": 2747, "line_end": 2778}],
        "qa/fomberg-unit-004/INDEPENDENT_REVIEW_FINAL.json", "unit004_repair_list",
    ),
    spec(
        "FOM-PR-11", "later_admitted", "D60-R11", "unit:o012-fom-u004",
        ["segment:o012-fom-u004-proof-compact-finite-simplices-repair"],
        ["segment:o012-fom-u004-lem-compact-finite-simplices"],
        ["segment:o012-fom-u004-omission-pr11"],
        [{"path": "algebraic_topology.tex", "line_start": 2818, "line_end": 2827}],
        "qa/fomberg-unit-004/INDEPENDENT_REVIEW_FINAL.json", "unit004_repair_list",
    ),
    spec(
        "FOM-PR-12", "later_admitted", "D60-R12", "unit:o012-fom-u005",
        ["segment:o012-fom-u005-proof-local-degree-independence", "segment:o012-fom-u005-proof-local-to-global"],
        ["segment:o012-fom-u005-def-local-degree", "segment:o012-fom-u005-prop-local-to-global"],
        ["segment:o012-fom-u005-omission-pr12"],
        [
            {"path": "algebraic_topology.tex", "line_start": 2984, "line_end": 3019, "dossier_focus": "local-degree choice independence"},
            {"path": "algebraic_topology.tex", "line_start": 3037, "line_end": 3074, "dossier_focus": "typed local-to-global argument"},
        ],
        "qa/fomberg-unit-005/INDEPENDENT_REVIEW_FINAL.json", "unit005_repair_list",
    ),
    spec(
        "FOM-PR-13", "later_admitted", "D60-R12", "unit:o012-fom-u007",
        ["segment:o012-fom-u007-proof-pr13"],
        ["segment:o012-fom-u007-thm-skeleton-stabilization"], [],
        [{"path": "algebraic_topology.tex", "line_start": 3525, "line_end": 3594}],
        "qa/fomberg-unit-007/INDEPENDENT_MATH_REVIEW_FINAL.json", "unit007_exact_math_review",
        ["correction:o012-fom-u007-adv-0556"],
    ),
    spec(
        "FOM-PR-14", "later_admitted", "D60-R12", "unit:o012-fom-u007",
        ["segment:o012-fom-u007-proof-pr14"],
        ["segment:o012-fom-u007-thm-cellular-homology"], [],
        [
            {"path": "algebraic_topology.tex", "line_start": 3596, "line_end": 3640},
            {"path": "algebraic_topology.tex", "line_start": 3684, "line_end": 4184},
        ],
        "qa/fomberg-unit-007/INDEPENDENT_MATH_REVIEW_FINAL.json", "unit007_exact_math_review",
        ["correction:o012-fom-u007-adv-0557"],
    ),
    spec(
        "FOM-PR-15", "later_admitted", "D60-R12", "unit:o012-fom-u007",
        ["segment:o012-fom-u007-proof-pr15"],
        ["segment:o012-fom-u007-thm-cellular-incidence"], [],
        [{"path": "algebraic_topology.tex", "line_start": 3642, "line_end": 3664}],
        "qa/fomberg-unit-007/INDEPENDENT_MATH_REVIEW_FINAL.json", "unit007_exact_math_review",
        ["correction:o012-fom-u007-adv-0558"],
    ),
]

# This is a structured forward-proof tag, not a canonical FOM-PR dossier ID.
# It is nevertheless audited because it occupies the repair_id field.
FORWARD_SPEC = spec(
    "FOM-U003-QUOTIENT-LES", "forward_marker", "D60-R10", "unit:o012-fom-u004",
    ["segment:o012-fom-u004-proof-relative-quotient"],
    ["segment:o012-fom-u004-thm-relative-quotient"],
    ["segment:o012-fom-u003-forward-quotient-les"],
    [
        {"path": "source/id-ID/fomberg/units/fomberg-unit-003-exact-sequences-relative-homology.md", "line_start": 197, "line_end": 205, "note": "forward marker"},
        {"path": "algebraic_topology.tex", "line_start": 2182, "line_end": 2233, "note": "later theorem and proof"},
    ],
    "qa/fomberg-unit-004/INDEPENDENT_REVIEW_FINAL.json", "forward_marker_general_review",
)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    raw = path.read_bytes()
    return {"path": relative, "bytes": len(raw), "sha256": sha256(raw)}


def load_frozen_backend() -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    tables: dict[str, list[dict[str, Any]]] = {}
    inventory: list[dict[str, Any]] = []
    bundle = hashlib.sha256()
    seen: set[str] = set()
    for name, (expected_records, expected_bytes, expected_sha) in FROZEN.items():
        live = (BACKEND / name).read_bytes()
        if len(live) < expected_bytes:
            raise ValueError(f"{name}: shorter than frozen Unit 007 byte prefix")
        raw = live[:expected_bytes]
        observed = (len(raw.splitlines()), len(raw), sha256(raw))
        expected = (expected_records, expected_bytes, expected_sha)
        if observed != expected:
            raise ValueError(f"{name}: frozen Unit 007 prefix mismatch: {observed!r}")
        if not raw.endswith(b"\n") or b"\r" in raw:
            raise ValueError(f"{name}: invalid frozen LF boundary")
        records: list[dict[str, Any]] = []
        for line_number, line in enumerate(raw.splitlines(keepends=True), 1):
            record = json.loads(line.decode("utf-8"))
            canonical = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
            if canonical != line:
                raise ValueError(f"{name}:{line_number}: noncanonical JSONL")
            if record["id"] in seen:
                raise ValueError(f"{name}:{line_number}: duplicate id {record['id']}")
            seen.add(record["id"])
            records.append(record)
        tables[name] = records
        inventory.append({"filename": name, "records": expected_records, "bytes": expected_bytes, "sha256": expected_sha})
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
    observed_total = (sum(len(v) for v in tables.values()), sum(x[1] for x in FROZEN.values()), bundle.hexdigest())
    expected_total = (UNIT007_TOTAL_RECORDS, UNIT007_TOTAL_BYTES, UNIT007_BUNDLE_SHA256)
    if observed_total != expected_total:
        raise ValueError(f"Unit 007 bundle mismatch: {observed_total!r}")
    return tables, inventory


def locator_view(locator: Any) -> Any:
    if not isinstance(locator, dict):
        return locator
    return {k: locator[k] for k in sorted(locator)}


def segment_view(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record["id"],
        "segment_kind": record.get("segment_kind"),
        "proof_status": record.get("proof_status"),
        "repair_id": record.get("repair_id"),
        "course_route_unit_id": record.get("course_route_unit_id"),
        "source_locator": locator_view(record.get("source_locator")),
        "target_locator": locator_view(record.get("target_locator")),
    }


def relation_view(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record["id"],
        "relation_type": record.get("relation_type"),
        "repair_id": record.get("repair_id"),
        "from_id": record.get("from_id"),
        "to_id": record.get("to_id"),
    }


def artifact_view(record: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / record["path"]
    exists = path.is_file()
    observed_bytes = path.stat().st_size if exists else None
    observed_sha = sha256(path.read_bytes()) if exists else None
    return {
        "id": record["id"],
        "path": record["path"],
        "declared_bytes": record.get("bytes"),
        "declared_sha256": record.get("sha256"),
        "exists": exists,
        "bytes_match": exists and observed_bytes == record.get("bytes"),
        "sha256_match": exists and observed_sha == record.get("sha256"),
    }


def target_file_valid(record: dict[str, Any]) -> bool:
    locator = record.get("target_locator")
    if not isinstance(locator, dict) or not isinstance(locator.get("path"), str):
        return False
    path = ROOT / locator["path"]
    if not path.is_file() or sha256(path.read_bytes()) != locator.get("file_sha256"):
        return False
    lines = path.read_text(encoding="utf-8").splitlines()
    start, end = locator.get("line_start"), locator.get("line_end")
    return isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= len(lines)


def review_pass(repair_id: str, mode: str, review: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    if mode == "unit001_proof_closure":
        closure = review.get("proof_closure", {})
        passed = (
            review.get("status") == "PASS"
            and closure.get("repair_id") == repair_id
            and closure.get("proof_status") in COMPLETE_PROOF_STATUSES
        )
        return passed, {"status": review.get("status"), "proof_closure": closure}
    if mode == "unit002_proof_closure":
        closure = review.get("proof_closure", {}).get(repair_id, {})
        passed = review.get("status") == "PASS" and closure.get("proof_status") in COMPLETE_PROOF_STATUSES
        return passed, {"status": review.get("status"), "proof_closure": closure}
    if mode == "unit003_proof_closure":
        closure = review.get("proof_closure_detail", {}).get(repair_id, {})
        passed = review.get("status") == "PASS" and closure.get("proof_status") in COMPLETE_PROOF_STATUSES
        return passed, {"status": review.get("status"), "proof_closure": closure}
    if mode in {"unit004_repair_list", "unit005_repair_list"}:
        closure = review.get("checks", {}).get("proof_repairs", {})
        passed = (
            review.get("status") == "PASS_P1_P2_P3_ZERO"
            and closure.get("status") == "PASS"
            and repair_id in closure.get("repair_ids", [])
        )
        return passed, {"status": review.get("status"), "proof_repairs": closure}
    if mode == "unit007_exact_math_review":
        matches = [x for x in review.get("proof_repair_checks", []) if x.get("repair_id") == repair_id]
        passed = review.get("status") == "PASS" and review.get("pass") is True and len(matches) == 1 and matches[0].get("status") == "PASS"
        return passed, {"status": review.get("status"), "review_id": review.get("review_id"), "proof_repair_check": matches[0] if len(matches) == 1 else None}
    if mode == "forward_marker_general_review":
        math = review.get("checks", {}).get("mathematics", {})
        passed = review.get("status") == "PASS_P1_P2_P3_ZERO" and math.get("status") == "PASS"
        return False, {
            "status": review.get("status"),
            "mathematics": math,
            "note": "The review passes Unit 004 generally but does not identify FOM-U003-QUOTIENT-LES; fail closed for repair-specific closure.",
            "general_review_pass": passed,
        }
    raise ValueError(f"unknown review mode {mode}")


def audit_one(
    entry: dict[str, Any],
    segments: dict[str, dict[str, Any]],
    units: dict[str, dict[str, Any]],
    relations: list[dict[str, Any]],
    qa_events: list[dict[str, Any]],
    artifacts: dict[str, dict[str, Any]],
    corrections: dict[str, dict[str, Any]],
    unit007_receipt: dict[str, Any],
) -> dict[str, Any]:
    rid = entry["repair_id"]
    proof_records = [segments.get(x) for x in entry["proof_ids"]]
    target_records = [segments.get(x) for x in entry["target_ids"]]
    source_records = [segments.get(x) for x in entry["source_ids"]]
    correction_records = [corrections.get(x) for x in entry["correction_ids"]]
    missing_records = [
        item
        for label, records_ in (("proof", proof_records), ("target", target_records), ("source", source_records), ("correction", correction_records))
        for item, value in zip([f"{label}:{x}" for x in entry[f"{label}_ids"]], records_)
        if value is None
    ]

    proof_records_ok = not missing_records and all(x is not None and target_file_valid(x) for x in proof_records)
    target_records_ok = all(x is not None and target_file_valid(x) for x in target_records)
    source_records_ok = all(x is not None and target_file_valid(x) for x in source_records)
    route_ids = sorted({x.get("course_route_unit_id") for x in [*proof_records, *target_records, *source_records] if x is not None})
    route_ok = route_ids == [entry["route"]]

    explicit_proof_status = bool(proof_records) and all(
        x is not None and x.get("proof_status") in COMPLETE_PROOF_STATUSES for x in proof_records
    )
    explicit_proof_repair_id = bool(proof_records) and all(x is not None and x.get("repair_id") == rid for x in proof_records)
    source_binding_expected = entry["tier"] in {"mandatory", "later_admitted", "forward_marker"}
    explicit_source_repair_id = (not source_binding_expected) or (
        bool(source_records) and all(x is not None and x.get("repair_id") == rid for x in source_records)
    )

    expected_pairs = [
        (proof_id.replace("segment:", "unit:", 1), target_id.replace("segment:", "unit:", 1))
        for proof_id, target_id in zip(entry["proof_ids"], entry["target_ids"])
    ]
    repair_relations = [x for x in relations if x.get("repair_id") == rid and x.get("relation_type") == "proves"]
    relation_pairs = sorted((x.get("from_id"), x.get("to_id")) for x in repair_relations)
    relation_ok = relation_pairs == sorted(expected_pairs)

    unit_pairs_ok = True
    for record in [*proof_records, *target_records, *source_records]:
        if record is None:
            unit_pairs_ok = False
            continue
        unit_id = record["id"].replace("segment:", "unit:", 1)
        unit = units.get(unit_id)
        unit_pairs_ok = unit_pairs_ok and unit is not None and unit.get("course_route_unit_id") == record.get("course_route_unit_id") and unit.get("target_locator") == record.get("target_locator")

    math_events = [
        x for x in qa_events
        if x.get("unit_id") == entry["qa_unit_id"] and x.get("qa_type") == "math" and x.get("status") == "active"
    ]
    qa_event_ok = len(math_events) == 1 and math_events[0].get("result") == "passed"
    witness_artifacts: list[dict[str, Any]] = []
    if len(math_events) == 1:
        for artifact_id in math_events[0].get("witness_artifact_ids", []):
            record = artifacts.get(artifact_id)
            witness_artifacts.append(artifact_view(record) if record else {"id": artifact_id, "missing_backend_artifact": True})
    witness_hashes_ok = bool(witness_artifacts) and all(x.get("bytes_match") and x.get("sha256_match") for x in witness_artifacts)

    review_identity = identity(entry["review_path"])
    review = json.loads((ROOT / entry["review_path"]).read_text(encoding="utf-8"))
    review_ok, review_excerpt = review_pass(rid, entry["review_mode"], review)
    review_is_direct_backend_witness = any(x.get("path") == entry["review_path"] for x in witness_artifacts)
    receipt_bound = unit007_receipt.get("bound_inputs", {}).get(entry["review_path"])
    receipt_binding_ok = bool(receipt_bound) and receipt_bound.get("bytes") == review_identity["bytes"] and receipt_bound.get("sha256") == review_identity["sha256"]

    structured_qa_closure = review_ok and qa_event_ok and witness_hashes_ok
    if entry["review_mode"] == "unit007_exact_math_review":
        structured_qa_closure = structured_qa_closure and receipt_binding_ok
    direct_review_witness_required = entry["review_mode"] == "unit007_exact_math_review"

    # Unit 007 has exact structured mathematical review, so its content is
    # closed despite missing repair fields in the backend graph.  That explicit
    # exception does not make the backend graph pass.
    content_closed = (
        proof_records_ok
        and target_records_ok
        and source_records_ok
        and route_ok
        and unit_pairs_ok
        and structured_qa_closure
        and (explicit_proof_status or entry["review_mode"] == "unit007_exact_math_review")
    )
    backend_graph_closed = (
        content_closed
        and explicit_proof_status
        and explicit_proof_repair_id
        and explicit_source_repair_id
        and relation_ok
        and (review_is_direct_backend_witness or not direct_review_witness_required)
    )

    missing_backend_evidence: list[str] = []
    if not explicit_proof_status:
        missing_backend_evidence.append("proof record lacks an explicit complete proof_status")
    if not explicit_proof_repair_id:
        missing_backend_evidence.append("proof record lacks the exact repair_id binding")
    if not explicit_source_repair_id:
        missing_backend_evidence.append("source-locus record lacks the exact repair_id binding")
    if not relation_ok:
        missing_backend_evidence.append("exact proves relation(s) from repair proof to repaired result are absent or mismatched")
    if direct_review_witness_required and not review_is_direct_backend_witness:
        missing_backend_evidence.append("repair-specific structured review is not directly named by the backend math QA event")
    if not content_closed:
        missing_backend_evidence.append("structured evidence does not prove mathematical content closure")

    explicit_occurrences = []
    for table_name, table in (("segments", segments.values()), ("units", units.values()), ("relations", relations)):
        explicit_occurrences.extend({"table": table_name, "id": x["id"]} for x in table if x.get("repair_id") == rid)

    return {
        "repair_id": rid,
        "tier": entry["tier"],
        "selection_source_loci": entry["selection_loci"],
        "course_route_unit_ids": route_ids,
        "expected_course_route_unit_id": entry["route"],
        "id_preservation": {
            "renamed": False,
            "aliases": [],
            "exact_explicit_backend_occurrences": explicit_occurrences,
            "proof_records_explicitly_bound": explicit_proof_repair_id,
        },
        "source_locus_records": [segment_view(x) for x in source_records if x is not None],
        "proof_records": [segment_view(x) for x in proof_records if x is not None],
        "repaired_result_records": [segment_view(x) for x in target_records if x is not None],
        "correction_records": [
            {
                "id": x["id"],
                "evidence": x.get("evidence"),
                "resolution_status": x.get("resolution_status"),
                "evidence_segment_id": x.get("evidence_segment_id"),
            }
            for x in correction_records if x is not None
        ],
        "proves_relations": [relation_view(x) for x in repair_relations],
        "qa_witness": {
            "math_event": math_events[0] if len(math_events) == 1 else None,
            "backend_artifacts": witness_artifacts,
            "repair_specific_review": review_identity,
            "repair_specific_review_excerpt": review_excerpt,
            "direct_backend_witness": review_is_direct_backend_witness,
            "unit007_cumulative_receipt_binding": receipt_binding_ok,
        },
        "checks": {
            "all_expected_records_present": not missing_records,
            "proof_target_files_hash_and_span_valid": proof_records_ok,
            "repaired_result_target_files_hash_and_span_valid": target_records_ok,
            "source_locus_target_files_hash_and_span_valid": source_records_ok,
            "unit_segment_pairs_exact": unit_pairs_ok,
            "course_route_exact": route_ok,
            "explicit_complete_proof_status": explicit_proof_status,
            "explicit_repair_id_on_proof": explicit_proof_repair_id,
            "explicit_repair_id_on_source_locus": explicit_source_repair_id,
            "exact_proves_relations": relation_ok,
            "backend_math_qa_event_passed": qa_event_ok,
            "backend_math_qa_artifact_hashes_valid": witness_hashes_ok,
            "structured_repair_review_passed": review_ok,
        },
        "mathematical_content_status": "CLOSED" if content_closed else "UNPROVEN_FAIL_CLOSED",
        "backend_graph_status": "CLOSED" if backend_graph_closed else "FAIL_CLOSED",
        "missing_backend_evidence": missing_backend_evidence,
    }


def main() -> int:
    try:
        tables, inventory = load_frozen_backend()
        if sha256(UPSTREAM.read_bytes()) != UPSTREAM_SHA256:
            raise ValueError("frozen Fomberg algebraic_topology.tex identity mismatch")
        unit007_receipt = json.loads(UNIT007_RECEIPT.read_text(encoding="utf-8"))
        if unit007_receipt.get("current", {}).get("bundle_sha256") != UNIT007_BUNDLE_SHA256:
            raise ValueError("Unit 007 cumulative receipt does not bind the frozen bundle")

        segments = {x["id"]: x for x in tables["segments.jsonl"]}
        units = {x["id"]: x for x in tables["units.jsonl"]}
        relations = tables["relations.jsonl"]
        qa_events = tables["qa.jsonl"]
        artifacts = {x["id"]: x for x in tables["artifacts.jsonl"]}
        corrections = {x["id"]: x for x in tables["corrections.jsonl"]}

        repairs = [
            audit_one(x, segments, units, relations, qa_events, artifacts, corrections, unit007_receipt)
            for x in SPECS
        ]
        forward = audit_one(FORWARD_SPEC, segments, units, relations, qa_events, artifacts, corrections, unit007_receipt)

        discovered = sorted(
            {
                x.get("repair_id")
                for name in ("segments.jsonl", "units.jsonl", "relations.jsonl")
                for x in tables[name]
                if isinstance(x.get("repair_id"), str)
            }
            | set(unit007_receipt.get("current", {}).get("proof_repairs_closed", []))
            | {
                match
                for x in tables["corrections.jsonl"]
                for match in re.findall(r"FOM-PR-[0-9]+", x.get("source_defect", ""))
            }
        )
        configured = sorted({x["repair_id"] for x in SPECS} | {FORWARD_SPEC["repair_id"]})
        unknown_ids = sorted(set(discovered) - set(configured))
        missing_configured_ids = sorted(set(configured) - set(discovered))

        mandatory = [x for x in repairs if x["tier"] == "mandatory"]
        later = [x for x in repairs if x["tier"] == "later_admitted"]
        additional = [x for x in repairs if x["tier"] == "additional_pre_dossier"]
        mandatory_pass = all(x["mathematical_content_status"] == "CLOSED" and x["backend_graph_status"] == "CLOSED" for x in mandatory)
        later_content_pass = all(x["mathematical_content_status"] == "CLOSED" for x in later)
        later_graph_pass = all(x["backend_graph_status"] == "CLOSED" for x in later)
        inventory_pass = not unknown_ids and not missing_configured_ids
        overall_pass = mandatory_pass and later_content_pass and later_graph_pass and inventory_pass and forward["backend_graph_status"] == "CLOSED"

        findings: list[dict[str, Any]] = []
        if not later_graph_pass:
            findings.append({
                "code": "UNIT007_REPAIRS_13_15_BACKEND_GRAPH_INCOMPLETE",
                "severity": "fail_closed",
                "repair_ids": [x["repair_id"] for x in later if x["backend_graph_status"] != "CLOSED"],
                "detail": "FOM-PR-13 through FOM-PR-15 have hash-bound passing mathematical reviews and exact proof spans, but their frozen segment/unit records omit repair_id and proof_status and have no proves relations.",
            })
        if any(not x["qa_witness"]["direct_backend_witness"] for x in later if x["repair_id"] in {"FOM-PR-13", "FOM-PR-14", "FOM-PR-15"}):
            findings.append({
                "code": "UNIT007_MATH_QA_WITNESS_MISBOUND",
                "severity": "fail_closed",
                "repair_ids": ["FOM-PR-13", "FOM-PR-14", "FOM-PR-15"],
                "detail": "qa:o012-fom-u007-math points to the source/language review artifact. The actual independent math review is hash-bound by the cumulative receipt but has no backend artifact record and is not the QA event's direct witness.",
            })
        if forward["backend_graph_status"] != "CLOSED":
            findings.append({
                "code": "FORWARD_QUOTIENT_LES_NOT_LINKED_BACK",
                "severity": "fail_closed",
                "repair_ids": ["FOM-U003-QUOTIENT-LES"],
                "detail": "The forward marker and later relative-quotient theorem/proof exist at exact locators, but the backend has no repair-specific proof status, repair_id linkage, or proves/closes relation connecting them.",
            })
        if unknown_ids or missing_configured_ids:
            findings.append({
                "code": "REPAIR_ID_INVENTORY_MISMATCH",
                "severity": "fail_closed",
                "unknown_ids": unknown_ids,
                "missing_configured_ids": missing_configured_ids,
            })

        report = {
            "audit_id": "O012-D60-PROOF-REPAIR-CENSUS-UNIT007-PREFIX",
            "schema_version": "1.0.0",
            "status": "PASS" if overall_pass else "FAIL_CLOSED",
            "scope": {
                "description": "Exact append-only backend prefix sealed after Roberts Units 001-030 and Fomberg Units 001-007",
                "backend_bundle_sha256": UNIT007_BUNDLE_SHA256,
                "backend_total_records": UNIT007_TOTAL_RECORDS,
                "backend_total_bytes": UNIT007_TOTAL_BYTES,
                "backend_file_prefixes": inventory,
                "unit007_cumulative_receipt": identity("qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_007_CUMULATIVE_RECEIPT.json"),
                "fomberg_authority": {"path": str(UPSTREAM.relative_to(ROOT)).replace("\\", "/"), "sha256": UPSTREAM_SHA256},
                "script": identity("scripts/census-proof-repairs.py"),
            },
            "method": {
                "no_loose_text_inference": True,
                "accepted_evidence": [
                    "exact Unit 007 byte-prefix hashes and canonical JSONL records",
                    "exact stable record IDs, repair_id/proof_status fields, target locators, and proves relations",
                    "passed backend QA events with artifact byte/hash readback",
                    "repair-specific structured QA whose bytes are backend- or cumulative-receipt-bound",
                ],
                "fail_closed_rule": "Missing explicit bindings never count as backend graph closure, even when a structured independent review proves the mathematical content.",
            },
            "summary": {
                "mandatory_dossier": {
                    "repair_ids": [f"FOM-PR-{i:02d}" for i in range(1, 9)],
                    "source_loci": 9,
                    "status": "PASS" if mandatory_pass else "FAIL_CLOSED",
                    "actual_missing_repairs": [x["repair_id"] for x in mandatory if x["mathematical_content_status"] != "CLOSED"],
                },
                "later_admitted_repairs": {
                    "repair_ids": [f"FOM-PR-{i:02d}" for i in range(9, 16)],
                    "mathematical_content_status": "PASS" if later_content_pass else "FAIL_CLOSED",
                    "backend_graph_status": "PASS" if later_graph_pass else "FAIL_CLOSED",
                    "actual_missing_repair_content": [x["repair_id"] for x in later if x["mathematical_content_status"] != "CLOSED"],
                },
                "additional_pre_dossier_repairs": {
                    "repair_ids": [x["repair_id"] for x in additional],
                    "status": "PASS" if all(x["backend_graph_status"] == "CLOSED" for x in additional) else "FAIL_CLOSED",
                },
                "forward_markers": {
                    "repair_ids": [FORWARD_SPEC["repair_id"]],
                    "status": forward["backend_graph_status"],
                },
                "repair_id_inventory": {
                    "discovered": discovered,
                    "configured": configured,
                    "unknown": unknown_ids,
                    "configured_but_not_discovered": missing_configured_ids,
                    "status": "PASS" if inventory_pass else "FAIL_CLOSED",
                },
                "id_renames_detected": [],
            },
            "repairs": repairs,
            "forward_marker_audit": forward,
            "findings": findings,
        }
    except Exception as error:  # still leave a deterministic fail-closed artifact
        report = {
            "audit_id": "O012-D60-PROOF-REPAIR-CENSUS-UNIT007-PREFIX",
            "schema_version": "1.0.0",
            "status": "FAIL_CLOSED",
            "fatal_error": f"{type(error).__name__}: {error}",
        }
        overall_pass = False

    OUTPUT.write_bytes(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")
    print(f"proof_repair_census_status={report['status']}")
    print(f"output={OUTPUT.relative_to(ROOT).as_posix()}")
    print(f"bytes={OUTPUT.stat().st_size}")
    print(f"sha256={sha256(OUTPUT.read_bytes())}")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
