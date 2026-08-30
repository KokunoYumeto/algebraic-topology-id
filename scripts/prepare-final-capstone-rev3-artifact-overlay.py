#!/usr/bin/env python3
"""Prepare two byte-identical final-evidence suffixes for capstone rev3."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
OUT = ROOT / "qa/capstone-final-rev3-artifacts-backend-20260829"
FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
BASELINE = {
    "records": 8325,
    "bytes": 10028356,
    "bundle_sha256": "8aff3dbc16e4f3552d2a16eecf043a6fe7c783c31200dce29bc8f61374504acb",
}
ROOT_UNIT = "unit:o012-d60-capstone-rev3"
RIGHTS = "rights:o012-d60-capstone-original-cc-by-sa-4.0-rev3"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
TIMESTAMP = "2026-08-29T00:00:00Z"
SEMANTIC_RECEIPT = "qa/BACKEND_CAPSTONE_FINAL_REV3_SEMANTIC_RECEIPT.json"


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
        state.update(name.encode("utf-8")); state.update(b"\0"); state.update(raw)
    return {"records": records, "bytes": byte_count, "bundle_sha256": state.hexdigest()}


def load_backend() -> tuple[dict[str, bytes], dict[str, dict[str, Any]]]:
    raw_by_file: dict[str, bytes] = {}
    by_id: dict[str, dict[str, Any]] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        require(raw.endswith(b"\n") and b"\r" not in raw, f"invalid JSONL: {name}")
        for line in raw.splitlines(keepends=True):
            row = json.loads(line)
            require(canon(row) == line, f"noncanonical JSONL: {name}")
            require(row["id"] not in by_id, f"duplicate ID: {row['id']}")
            by_id[row["id"]] = row
        raw_by_file[name] = raw
    require(bundle(raw_by_file) == BASELINE, "live backend is not the exact rev3 semantic boundary")
    return raw_by_file, by_id


def identity(relative: str) -> tuple[int, str]:
    path = ROOT / relative
    require(path.is_file() and path.stat().st_size > 0, f"missing final evidence: {relative}")
    raw = path.read_bytes()
    if path.suffix == ".json":
        require(json.loads(raw).get("status") == "PASS", f"final JSON evidence is not PASS: {relative}")
    return len(raw), sha(raw)


def clone(row: dict[str, Any], new_id: str) -> dict[str, Any]:
    result = copy.deepcopy(row)
    result["id"] = new_id
    result["supersedes"] = row["id"]
    result["timestamp"] = TIMESTAMP
    return result


def additions(by_id: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    result = {name: [] for name in FILES}
    artifact_paths = {
        "artifact:o012-d60-capstone-browser-qa-final": "qa/capstone/BROWSER_QA.json",
        "artifact:o012-d60-capstone-build-receipt-final": "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_CAPSTONE_BUILD_RECEIPT.json",
        "artifact:o012-d60-capstone-html-final": "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04-capstone/index.html",
        "artifact:o012-d60-capstone-manifest-final": "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_CAPSTONE.csv",
        "artifact:o012-d60-capstone-pdf-final": "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04-capstone-id.pdf",
        "artifact:o012-d60-capstone-semantic-backend-receipt-final": SEMANTIC_RECEIPT,
        "artifact:o012-d60-capstone-source-final": "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md",
        "artifact:o012-d60-capstone-visual-qa-final": "qa/capstone/VISUAL_QA.json",
        "artifact:o012-d60-proof-census-final": "qa/PROOF_REPAIR_CENSUS.json",
    }
    artifact_map = {old: old + "-rev3" for old in artifact_paths}
    qa_ids = (
        "qa:o012-d60-capstone-final-browser",
        "qa:o012-d60-capstone-final-build",
        "qa:o012-d60-capstone-final-proof-closure",
        "qa:o012-d60-capstone-final-visual",
    )
    qa_map = {old: old + "-rev3" for old in qa_ids}
    artifact_qa_map = {
        **qa_map,
        "qa:o012-d60-capstone-source-rev2": "qa:o012-d60-capstone-source-rev3",
    }
    for old_id, relative in artifact_paths.items():
        old = by_id[old_id]
        new = clone(old, artifact_map[old_id])
        size, digest = identity(relative)
        new["path"] = relative
        new["bytes"] = size
        new["sha256"] = digest
        new["unit_id"] = ROOT_UNIT
        new["rights_component_id"] = RIGHTS
        new["qa_event_ids"] = [artifact_qa_map[item] for item in old["qa_event_ids"]]
        new["manifest_artifact_id"] = artifact_map.get(old.get("manifest_artifact_id"), old.get("manifest_artifact_id"))
        new["toolchain"] = "Final D60 capstone rev3 reader/evidence closure; OpenAI Codex gpt-5.6-sol, Ultra."
        if old_id == "artifact:o012-d60-capstone-source-final":
            new["qa_event_ids"] = ["qa:o012-d60-capstone-source-rev3", qa_map["qa:o012-d60-capstone-final-build"]]
        result["artifacts.jsonl"].append(new)
    for old_id in qa_ids:
        old = by_id[old_id]
        new = clone(old, qa_map[old_id])
        new["unit_id"] = ROOT_UNIT
        new["witness_artifact_ids"] = [artifact_map[item] for item in old["witness_artifact_ids"]]
        new["note"] = old["note"].rstrip(".") + "; rerun against the corrected rev3 source and semantic boundary."
        result["qa.jsonl"].append(new)
    for name in FILES:
        result[name].sort(key=lambda row: row["id"])
    return result


def validate(add: dict[str, list[dict[str, Any]]], existing: dict[str, dict[str, Any]]) -> None:
    require(len(add["artifacts.jsonl"]) == 9 and len(add["qa.jsonl"]) == 4, "final-evidence suffix census drift")
    require(sum(len(rows) for rows in add.values()) == 13, "final-evidence total record drift")
    rows = [row for group in add.values() for row in group]
    ids = [row["id"] for row in rows]
    require(len(ids) == len(set(ids)) and not set(ids).intersection(existing), "final-evidence ID collision")
    all_ids = set(existing).union(ids)
    for row in rows:
        require(row.get("supersedes") in existing, f"missing historical predecessor: {row['id']}")
        for key in ("manifest_artifact_id", "rights_component_id", "unit_id"):
            value = row.get(key)
            if value is not None:
                require(value in all_ids, f"unknown {key}: {value}")
        for key in ("qa_event_ids", "witness_artifact_ids"):
            require(all(value in all_ids for value in row.get(key, [])), f"unknown {key}: {row['id']}")
    require(all(row["unit_id"] == ROOT_UNIT for row in rows), "final evidence is not bound to the rev3 root")


def write_run(name: str, baseline: dict[str, bytes], add: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    target = OUT / name
    require(not target.exists(), f"candidate collision: {target}")
    target.mkdir(parents=True)
    suffix_raw: dict[str, bytes] = {}
    final_raw: dict[str, bytes] = {}
    identities: dict[str, dict[str, Any]] = {}
    for filename in FILES:
        raw = b"".join(canon(row) for row in add[filename])
        suffix_raw[filename] = raw
        final_raw[filename] = baseline[filename] + raw
        (target / filename).write_bytes(raw)
        identities[filename] = {"records": len(raw.splitlines()), "bytes": len(raw), "sha256": sha(raw)}
    receipt = {
        "status": "PASS_CANDIDATE",
        "receipt_kind": "final_capstone_rev3_artifact_evidence_candidate",
        "model_provenance": MODEL,
        "timestamp": TIMESTAMP,
        "baseline": bundle(baseline),
        "suffix": identities,
        "suffix_total": bundle(suffix_raw),
        "final": bundle(final_raw),
        "semantic_receipt": {"path": SEMANTIC_RECEIPT, "bytes": (ROOT / SEMANTIC_RECEIPT).stat().st_size, "sha256": sha((ROOT / SEMANTIC_RECEIPT).read_bytes())},
    }
    (target / "RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    return receipt


def main() -> int:
    require(not OUT.exists(), f"candidate output already exists: {OUT}")
    baseline, existing = load_backend()
    add = additions(existing)
    validate(add, existing)
    OUT.mkdir(parents=True)
    first = write_run("run-a", baseline, add)
    second = write_run("run-b", baseline, add)
    require(first == second, "final-evidence candidate receipts differ")
    for filename in (*FILES, "RECEIPT.json"):
        require((OUT / "run-a" / filename).read_bytes() == (OUT / "run-b" / filename).read_bytes(), f"candidate bytes differ: {filename}")
    print(json.dumps({"status": "PASS", "candidate": first}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
