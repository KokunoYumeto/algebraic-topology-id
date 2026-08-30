#!/usr/bin/env python3
"""Current, append-only proof-graph census for the D60 lane.

Unlike the historical Unit-007 census, this successor reads the complete
current backend and resolves append-only records through ``supersedes``.  The
old JSONL lines remain immutable; the logical view is explicit in the receipt.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
OUTPUT = ROOT / "qa" / "PROOF_REPAIR_CENSUS.json"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl", "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl", "segments.jsonl", "terms.jsonl", "units.jsonl")
COMPLETE = {"complete_original_repair", "complete_edition_repair_of_source_argument"}
OVERLAY_RECEIPT = ROOT / "qa" / "proof-repair-overlay-20260829" / "run-a" / "RECEIPT.json"
OLD_CENSUS = ROOT / "qa" / "PROOF_REPAIR_CENSUS.json"

SPECS = [
    {
        "repair_id": "FOM-PR-13", "tier": "later_admitted", "route": "D60-R12", "qa_unit_id": "unit:o012-fom-u007",
        "proof_ids": ["segment:o012-fom-u007-proof-pr13"], "target_ids": ["segment:o012-fom-u007-thm-skeleton-stabilization"], "source_ids": [],
        "selection_loci": [{"path": "algebraic_topology.tex", "line_start": 3525, "line_end": 3594}],
        "review_path": "qa/fomberg-unit-007/INDEPENDENT_MATH_REVIEW_FINAL.json", "review_kind": "unit007",
    },
    {
        "repair_id": "FOM-PR-14", "tier": "later_admitted", "route": "D60-R12", "qa_unit_id": "unit:o012-fom-u007",
        "proof_ids": ["segment:o012-fom-u007-proof-pr14"], "target_ids": ["segment:o012-fom-u007-thm-cellular-homology"], "source_ids": [],
        "selection_loci": [{"path": "algebraic_topology.tex", "line_start": 3596, "line_end": 3640}, {"path": "algebraic_topology.tex", "line_start": 3684, "line_end": 4184}],
        "review_path": "qa/fomberg-unit-007/INDEPENDENT_MATH_REVIEW_FINAL.json", "review_kind": "unit007",
    },
    {
        "repair_id": "FOM-PR-15", "tier": "later_admitted", "route": "D60-R12", "qa_unit_id": "unit:o012-fom-u007",
        "proof_ids": ["segment:o012-fom-u007-proof-pr15"], "target_ids": ["segment:o012-fom-u007-thm-cellular-incidence"], "source_ids": [],
        "selection_loci": [{"path": "algebraic_topology.tex", "line_start": 3642, "line_end": 3664}],
        "review_path": "qa/fomberg-unit-007/INDEPENDENT_MATH_REVIEW_FINAL.json", "review_kind": "unit007",
    },
    {
        "repair_id": "FOM-U003-QUOTIENT-LES", "tier": "forward_marker", "route": "D60-R10", "qa_unit_id": "unit:o012-fom-u004",
        "proof_ids": ["segment:o012-fom-u004-proof-relative-quotient"], "target_ids": ["segment:o012-fom-u004-thm-relative-quotient"], "source_ids": ["segment:o012-fom-u003-forward-quotient-les"],
        "selection_loci": [{"path": "source/id-ID/fomberg/units/fomberg-unit-003-exact-sequences-relative-homology.md", "line_start": 197, "line_end": 205, "note": "forward marker"}, {"path": "algebraic_topology.tex", "line_start": 2182, "line_end": 2233, "note": "supporting theorem and proof"}],
        "review_path": "qa/fomberg-unit-004/INDEPENDENT_REVIEW_QUOTIENT_LES_FINAL.json", "review_kind": "forward",
    },
]

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def canon(row: dict[str, Any]) -> bytes:
    return (json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

def load() -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    tables: dict[str, list[dict[str, Any]]] = {}
    by_id: dict[str, dict[str, Any]] = {}
    superseders: dict[str, list[dict[str, Any]]] = {}
    for name in FILES:
        rows = []
        raw = (BACKEND / name).read_bytes()
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise RuntimeError(f"invalid JSONL bytes: {name}")
        for line in raw.splitlines(keepends=True):
            row = json.loads(line.decode("utf-8"))
            if canon(row) != line:
                raise RuntimeError(f"noncanonical JSONL: {name}")
            ident = row.get("id")
            if not isinstance(ident, str) or ident in by_id:
                raise RuntimeError(f"duplicate or missing ID: {name}:{ident}")
            by_id[ident] = row; rows.append(row)
            parent = row.get("supersedes")
            if isinstance(parent, str): superseders.setdefault(parent, []).append(row)
        tables[name] = rows
    return tables, by_id, superseders

def logical(ident: str, by_id: dict[str, dict[str, Any]], superseders: dict[str, list[dict[str, Any]]]) -> dict[str, Any] | None:
    row = by_id.get(ident)
    seen = {ident}
    while superseders.get(ident):
        choices = superseders[ident]
        row = choices[-1]
        ident = row["id"]
        if ident in seen: raise RuntimeError("supersedes cycle")
        seen.add(ident)
    return row

def span_hash(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return sha(b"".join(lines[start - 1:end]))

def target_ok(row: dict[str, Any] | None) -> bool:
    if row is None: return False
    loc = row.get("target_locator")
    if not isinstance(loc, dict) or not isinstance(loc.get("path"), str): return False
    path = ROOT / loc["path"]
    if not path.is_file() or sha(path.read_bytes()) != loc.get("file_sha256"): return False
    start, end = loc.get("line_start"), loc.get("line_end")
    if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start: return False
    lines = path.read_bytes().splitlines(keepends=True)
    if end > len(lines): return False
    declared = loc.get("content_sha256")
    return not declared or declared == span_hash(path, start, end)

def locator_view(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None: return None
    return {k: row.get(k) for k in ("id", "segment_kind", "proof_status", "repair_id", "course_route_unit_id", "source_locator", "target_locator")}

def artifact_witness(artifact: dict[str, Any] | None) -> dict[str, Any]:
    if artifact is None: return {"exists": False}
    path = ROOT / artifact["path"]
    exists = path.is_file()
    raw = path.read_bytes() if exists else b""
    return {"id": artifact["id"], "path": artifact["path"], "declared_bytes": artifact.get("bytes"), "declared_sha256": artifact.get("sha256"), "exists": exists, "bytes_match": exists and len(raw) == artifact.get("bytes"), "sha256_match": exists and sha(raw) == artifact.get("sha256")}

def review_check(spec: dict[str, Any], review: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    if spec["review_kind"] == "unit007":
        matches = [x for x in review.get("proof_repair_checks", []) if x.get("repair_id") == spec["repair_id"]]
        ok = review.get("status") == "PASS" and review.get("pass") is True and len(matches) == 1 and matches[0].get("status") == "PASS"
        return ok, {"status": review.get("status"), "proof_repair_check": matches[0] if matches else None}
    closure = review.get("proof_closure", {})
    checks = review.get("checks", {})
    ok = review.get("status") == "PASS_P1_P2_P3_ZERO" and review.get("pass") is True and closure.get("repair_id") == spec["repair_id"] and closure.get("proof_status") in COMPLETE and all(v == "PASS" for v in checks.values())
    return ok, {"status": review.get("status"), "proof_closure": closure, "checks": checks}

def audit(spec: dict[str, Any], by_id: dict[str, dict[str, Any]], superseders: dict[str, list[dict[str, Any]]], tables: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    rid = spec["repair_id"]
    proofs = [logical(x, by_id, superseders) for x in spec["proof_ids"]]
    targets = [logical(x, by_id, superseders) for x in spec["target_ids"]]
    sources = [logical(x, by_id, superseders) for x in spec["source_ids"]]
    all_records = [x for x in (*proofs, *targets, *sources) if x is not None]
    target_valid = all(target_ok(x) for x in (*proofs, *targets, *sources))
    proof_status = bool(proofs) and all(x.get("proof_status") in COMPLETE for x in proofs if x)
    proof_repair = bool(proofs) and all(x.get("repair_id") == rid for x in proofs if x)
    source_repair = (not spec["source_ids"]) or (bool(sources) and all(x.get("repair_id") == rid for x in sources if x))
    routes = sorted({x.get("course_route_unit_id") for x in all_records})
    route_ok = routes == [spec["route"]] if spec["review_kind"] != "forward" else routes == ["D60-R10", "D60-R11"] and sources and sources[0].get("course_route_unit_id") == "D60-R10"
    unit_pairs = True
    for segment in (*proofs, *targets, *sources):
        if segment is None: unit_pairs = False; continue
        unit = by_id.get(segment.get("unit_id"))
        unit_pairs = unit_pairs and unit is not None and unit.get("target_locator") == segment.get("target_locator")
    expected_pairs = sorted((x.replace("segment:", "unit:", 1), y.replace("segment:", "unit:", 1)) for x, y in zip(spec["proof_ids"], spec["target_ids"]))
    relations = [x for x in tables["relations.jsonl"] if x.get("repair_id") == rid and x.get("relation_type") == "proves"]
    relation_pairs = sorted((x.get("from_id"), x.get("to_id")) for x in relations)
    relation_ok = relation_pairs == expected_pairs
    # Resolve the superseding QA event for the unit and require a direct
    # artifact whose path is the repair-specific review.
    events = []
    for event in tables["qa.jsonl"]:
        if event.get("unit_id") == spec["qa_unit_id"] and event.get("qa_type") == "math" and event.get("status") == "active":
            if rid in str(event.get("repair_id", "")) or event.get("id") == logical(event.get("id"), by_id, superseders).get("id"):
                current = logical(event["id"], by_id, superseders)
                if current and (rid in str(current.get("repair_id", ""))): events.append(current)
    event_ok = len(events) == 1 and events[0].get("result") == "passed"
    witnesses = []
    if event_ok:
        for aid in events[0].get("witness_artifact_ids", []): witnesses.append(artifact_witness(by_id.get(aid)))
    witness_ok = bool(witnesses) and all(x["exists"] and x["bytes_match"] and x["sha256_match"] for x in witnesses)
    review_path = ROOT / spec["review_path"]
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review_ok, review_excerpt = review_check(spec, review)
    direct_review = any(x.get("path") == spec["review_path"] for x in witnesses)
    backend_closed = all((target_valid, proof_status, proof_repair, source_repair, route_ok, unit_pairs, relation_ok, event_ok, witness_ok, review_ok, direct_review))
    return {
        "repair_id": rid, "tier": spec["tier"], "backend_graph_status": "CLOSED" if backend_closed else "FAIL_CLOSED", "mathematical_content_status": "PASS" if review_ok else "FAIL_CLOSED",
        "checks": {"all_expected_records_present": all(x is not None for x in (*proofs, *targets, *sources)), "proof_target_files_hash_and_span_valid": target_valid, "explicit_complete_proof_status": proof_status, "explicit_repair_id_on_proof": proof_repair, "explicit_repair_id_on_source_locus": source_repair, "course_route_closure": route_ok, "unit_segment_pairs_exact": unit_pairs, "exact_proves_relations": relation_ok, "repair_specific_qa_event": event_ok, "qa_artifact_hashes_valid": witness_ok, "repair_review_passed": review_ok, "direct_review_witness": direct_review},
        "course_route_unit_ids": routes, "expected_course_route_unit_id": spec["route"], "proof_records": [locator_view(x) for x in proofs], "repaired_result_records": [locator_view(x) for x in targets], "source_locus_records": [locator_view(x) for x in sources], "proves_relations": [{"id": x.get("id"), "relation_type": x.get("relation_type"), "repair_id": x.get("repair_id"), "from_id": x.get("from_id"), "to_id": x.get("to_id")} for x in relations], "qa_witness": {"math_event": events[0] if event_ok else None, "backend_artifacts": witnesses, "direct_backend_witness": direct_review, "review_path": spec["review_path"], "review_excerpt": review_excerpt}, "selection_source_loci": spec["selection_loci"], "missing_backend_evidence": [] if backend_closed else [k for k, v in {"proof_status": proof_status, "proof_repair_id": proof_repair, "source_repair_id": source_repair, "route": route_ok, "unit_pairs": unit_pairs, "proves": relation_ok, "qa_event": event_ok, "qa_witness": witness_ok, "review": review_ok, "direct_review": direct_review}.items() if not v],
    }

def main() -> int:
    tables, by_id, superseders = load()
    results = [audit(spec, by_id, superseders, tables) for spec in SPECS]
    backend_inv = []
    bundle = hashlib.sha256()
    for name in FILES:
        raw = (BACKEND / name).read_bytes(); item = {"filename": name, "records": len(raw.splitlines()), "bytes": len(raw), "sha256": sha(raw)}; backend_inv.append(item); bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    old_hash = sha(OLD_CENSUS.read_bytes()) if OLD_CENSUS.is_file() else None
    overlay = json.loads(OVERLAY_RECEIPT.read_text(encoding="utf-8")) if OVERLAY_RECEIPT.is_file() else None
    status = "PASS" if all(x["backend_graph_status"] == "CLOSED" for x in results) else "FAIL_CLOSED"
    receipt = {"audit_id": "O012-D60-PROOF-REPAIR-CENSUS-CURRENT", "status": status, "timestamp": "2026-08-29T00:00:00Z", "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra", "scope": "Complete current D60 backend with append-only proof-repair overlay; historical failed census is superseded, never treated as evidence of closure.", "backend": {"files": backend_inv, "records": sum(x["records"] for x in backend_inv), "bytes": sum(x["bytes"] for x in backend_inv), "bundle_sha256": bundle.hexdigest()}, "overlay_receipt": overlay, "superseded_historical_census_sha256": old_hash, "repairs": results, "summary": {"all_four_graphs_closed": status == "PASS", "repair_ids": [x["repair_id"] for x in results], "proof_repairs_closed": [x["repair_id"] for x in results if x["backend_graph_status"] == "CLOSED"]}}
    OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": status, "records": receipt["backend"]["records"], "bytes": receipt["backend"]["bytes"], "bundle_sha256": receipt["backend"]["bundle_sha256"], "repairs": receipt["summary"]["proof_repairs_closed"]}, ensure_ascii=False, sort_keys=True))
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
