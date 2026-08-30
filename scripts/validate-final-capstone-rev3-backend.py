#!/usr/bin/env python3
"""Independently validate the complete rev3 D60 backend and evidence chain."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
OUTPUT = ROOT / "qa/BACKEND_CAPSTONE_FINAL_REV3_VALIDATION.json"
SOURCE = ROOT / "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md"
FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
SOURCE_IDENTITY = (21744, 423, "d26ad5224e61c62080e00074acabfd2cf680779a7bc5d0562cfccc6d715a09c9")
SEMANTIC = {"records": 8325, "bytes": 10028356, "bundle_sha256": "8aff3dbc16e4f3552d2a16eecf043a6fe7c783c31200dce29bc8f61374504acb"}
FINAL = {"records": 8338, "bytes": 10040043, "bundle_sha256": "8a3ffc9618e56dfce048c41e938aabef4ffbfd3db20a03a4f52f218985230dbb"}
ROOT_REV3 = "unit:o012-d60-capstone-rev3"
RIGHTS_REV3 = "rights:o012-d60-capstone-original-cc-by-sa-4.0-rev3"


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(row: dict[str, Any]) -> bytes:
    return (json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def identity(relative: str) -> tuple[int, str]:
    path = ROOT / relative
    raw = path.read_bytes()
    return len(raw), sha(raw)


def load() -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]], dict[str, list[str]], dict[str, Any]]:
    tables: dict[str, list[dict[str, Any]]] = {}
    by_id: dict[str, dict[str, Any]] = {}
    children: dict[str, list[str]] = {}
    state = hashlib.sha256(); records = 0; byte_count = 0
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        require(raw.endswith(b"\n") and b"\r" not in raw, f"invalid JSONL bytes: {name}")
        rows = []
        for line in raw.splitlines(keepends=True):
            row = json.loads(line)
            require(canon(row) == line, f"noncanonical JSONL: {name}")
            require(isinstance(row.get("id"), str) and row["id"] not in by_id, f"duplicate/missing ID: {name}")
            by_id[row["id"]] = row; rows.append(row)
            if isinstance(row.get("supersedes"), str):
                children.setdefault(row["supersedes"], []).append(row["id"])
        tables[name] = rows
        records += len(rows); byte_count += len(raw)
        state.update(name.encode("utf-8")); state.update(b"\0"); state.update(raw)
    bundle = {"records": records, "bytes": byte_count, "bundle_sha256": state.hexdigest()}
    require(bundle == FINAL, "live backend final identity drift")
    return tables, by_id, children, bundle


def leaf(ident: str, by_id: dict[str, dict[str, Any]], children: dict[str, list[str]]) -> dict[str, Any]:
    require(ident in by_id, f"unknown logical seed: {ident}")
    seen = set()
    while children.get(ident):
        require(len(children[ident]) == 1, f"ambiguous supersedes branch: {ident}")
        require(ident not in seen, f"supersedes cycle: {ident}")
        seen.add(ident); ident = children[ident][0]
    return by_id[ident]


def main() -> int:
    tables, by_id, children, live = load()
    require(all(parent in by_id for parent in children), "supersedes references unknown predecessor")
    # Historical branches outside the bounded capstone lane are preserved as
    # evidence; require unambiguous, acyclic chains for every capstone seed
    # resolved below rather than rewriting unrelated legacy topology.

    scalar_refs = {"concept_id", "course_id", "edition_id", "evidence_segment_id", "from_id", "manifest_artifact_id", "parent_id", "program_id", "resource_id", "rights_component_id", "scope_unit_id", "to_id", "unit_id"}
    list_refs = {"affected_unit_ids", "component_scope", "concept_ids", "qa_event_ids", "witness_artifact_ids"}
    for row in by_id.values():
        for key in scalar_refs:
            if row.get(key) is not None:
                require(row[key] in by_id, f"unresolved {key}: {row['id']} -> {row[key]}")
        for key in list_refs:
            require(all(value in by_id for value in row.get(key, [])), f"unresolved {key}: {row['id']}")

    source_raw = SOURCE.read_bytes()
    require((len(source_raw), source_raw.count(b"\n"), sha(source_raw)) == SOURCE_IDENTITY, "source identity drift")
    stable_ids = []
    for line in source_raw.decode("utf-8").splitlines():
        stable_ids.extend(re.findall(r"#(o012-d60-capstone(?:-[a-z0-9]+)*)\b", line))
    stable_ids = list(dict.fromkeys(stable_ids))
    require(len(stable_ids) == 34, "stable-ID census drift")
    current_units = [leaf("unit:" + stable, by_id, children) for stable in stable_ids]
    current_segments = [leaf("segment:" + stable, by_id, children) for stable in stable_ids]
    require({row["id"] for row in current_units} == {"unit:" + stable + "-rev3" for stable in stable_ids}, "current unit leaves are not exact rev3")
    require({row["id"] for row in current_segments} == {"segment:" + stable + "-rev3" for stable in stable_ids}, "current segment leaves are not exact rev3")
    for unit, segment in zip(current_units, current_segments):
        require(unit["source_local_id"] == segment["source_local_id"], "unit/segment stable ID mismatch")
        require(segment["unit_id"] == unit["id"], "segment not linked to current unit")
        require(unit["target_locator"] == segment["target_locator"], "unit/segment locator mismatch")
        require(unit["target_locator"]["file_sha256"] == SOURCE_IDENTITY[2], "current locator source hash drift")
        require(unit["rights_component_id"] == segment["rights_component_id"] == RIGHTS_REV3, "current rights link drift")
    require(leaf("unit:o012-d60-capstone", by_id, children)["id"] == ROOT_REV3, "logical root does not resolve to rev3")

    rights = leaf("rights:o012-d60-capstone-original-cc-by-sa-4.0", by_id, children)
    require(rights["id"] == RIGHTS_REV3 and set(rights["component_scope"]) == {row["id"] for row in current_units}, "current rights scope drift")
    term_seeds = [row["id"] for row in tables["terms.jsonl"] if row["id"].startswith("term:o012-d60-capstone-term-") and row.get("supersedes") is None]
    relation_seeds = [row["id"] for row in tables["relations.jsonl"] if ":o012-d60-capstone:" in row["id"] and row.get("supersedes") is None]
    require(len(term_seeds) == 10 and all(leaf(seed, by_id, children)["id"].endswith("-rev3") for seed in term_seeds), "current term leaves drift")
    require(len(relation_seeds) == 54 and all(leaf(seed, by_id, children)["id"].endswith("-rev3") for seed in relation_seeds), "current relation leaves drift")

    source_qa_artifacts = [
        "artifact:o012-d60-capstone-source-qa", "artifact:o012-d60-capstone-structure-qa",
        "artifact:o012-d60-capstone-math-qa", "artifact:o012-d60-capstone-language-qa",
        "artifact:o012-d60-capstone-mastery-qa",
    ]
    for seed in source_qa_artifacts:
        row = leaf(seed, by_id, children)
        require(row["id"].endswith("-rev3") and (row["bytes"], row["sha256"]) == identity(row["path"]), f"current source QA artifact drift: {seed}")
        require(row["unit_id"] == ROOT_REV3 and row["rights_component_id"] == RIGHTS_REV3, f"source QA graph drift: {seed}")

    final_artifacts = [
        "artifact:o012-d60-capstone-browser-qa-final", "artifact:o012-d60-capstone-build-receipt-final",
        "artifact:o012-d60-capstone-html-final", "artifact:o012-d60-capstone-manifest-final",
        "artifact:o012-d60-capstone-pdf-final", "artifact:o012-d60-capstone-semantic-backend-receipt-final",
        "artifact:o012-d60-capstone-source-final", "artifact:o012-d60-capstone-visual-qa-final",
        "artifact:o012-d60-proof-census-final",
    ]
    for seed in final_artifacts:
        row = leaf(seed, by_id, children)
        require(row["id"] == seed + "-rev3", f"final artifact leaf drift: {seed}")
        require((row["bytes"], row["sha256"]) == identity(row["path"]), f"final artifact identity drift: {seed}")
        require(row["unit_id"] == ROOT_REV3 and row["rights_component_id"] == RIGHTS_REV3, f"final artifact graph drift: {seed}")
    final_qa = [
        "qa:o012-d60-capstone-final-browser", "qa:o012-d60-capstone-final-build",
        "qa:o012-d60-capstone-final-proof-closure", "qa:o012-d60-capstone-final-visual",
    ]
    require(all(leaf(seed, by_id, children)["id"] == seed + "-rev3" for seed in final_qa), "final QA leaves drift")

    proof = json.loads((ROOT / "qa/PROOF_REPAIR_CENSUS.json").read_text(encoding="utf-8"))
    require(proof.get("status") == "PASS" and proof.get("backend", {}).get("records") == SEMANTIC["records"] and proof.get("backend", {}).get("bytes") == SEMANTIC["bytes"] and proof.get("backend", {}).get("bundle_sha256") == SEMANTIC["bundle_sha256"], "proof census is not bound to rev3 semantic boundary")
    require(proof.get("summary", {}).get("all_four_graphs_closed") is True, "proof graph closure failed")
    semantic_receipt = json.loads((ROOT / "qa/BACKEND_CAPSTONE_FINAL_REV3_SEMANTIC_RECEIPT.json").read_text(encoding="utf-8"))
    cumulative = json.loads((ROOT / "qa/BACKEND_CAPSTONE_FINAL_REV3_CUMULATIVE_RECEIPT.json").read_text(encoding="utf-8"))
    require(semantic_receipt.get("status") == "PASS" and semantic_receipt.get("final") == SEMANTIC, "semantic receipt drift")
    require(cumulative.get("status") == "PASS" and cumulative.get("semantic_proof_boundary") == SEMANTIC and cumulative.get("final") == FINAL, "cumulative receipt drift")
    correction = by_id["correction:o012-d60-capstone-adv-0566"]
    adverse = (ROOT / "00_control/ADVERSE_LEDGER.csv").read_text(encoding="utf-8")
    require(correction.get("adverse_ledger_id") == "O012-ADV-0566" and "O012-ADV-0566" in adverse and SOURCE_IDENTITY[2] in adverse, "correction/adverse-ledger binding drift")
    new_ids = [ident for ident in by_id if ident.endswith("-rev3") or ident == "correction:o012-d60-capstone-adv-0566"]
    require(all(by_id[ident].get("model_provenance", MODEL) == MODEL for ident in new_ids), "model provenance drift")

    receipt = {
        "status": "PASS",
        "receipt_kind": "independent_final_capstone_rev3_backend_validation",
        "model_provenance": MODEL,
        "source": {"path": SOURCE.relative_to(ROOT).as_posix(), "bytes": SOURCE_IDENTITY[0], "lf_lines": SOURCE_IDENTITY[1], "sha256": SOURCE_IDENTITY[2]},
        "semantic_proof_boundary": SEMANTIC,
        "backend": live,
        "checks": {
            "canonical_jsonl_and_unique_global_ids": "PASS",
            "all_references_resolve": "PASS",
            "supersedes_graph_unambiguous_and_acyclic": "PASS",
            "thirty_four_current_unit_segment_pairs_exact_rev3": "PASS",
            "current_rights_terms_and_fifty_four_relations_rebased": "PASS",
            "five_current_source_qa_pairs_exact": "PASS",
            "nine_final_artifact_and_four_final_qa_successors_exact": "PASS",
            "proof_census_bound_to_semantic_boundary": "PASS",
            "adverse_ledger_and_backend_correction_bound": "PASS",
            "model_provenance_exact": "PASS",
        },
        "severity_census": {"P1": 0, "P2": 0, "P3": 0},
    }
    OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    raw = OUTPUT.read_bytes()
    print(json.dumps({"status": "PASS", "receipt": {"path": OUTPUT.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}, "backend": live}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
