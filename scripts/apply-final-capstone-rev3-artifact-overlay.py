#!/usr/bin/env python3
"""Apply the final-capstone rev3 evidence suffix append-only and resumably."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
CANDIDATE = ROOT / "qa/capstone-final-rev3-artifacts-backend-20260829"
OUT = ROOT / "qa/BACKEND_CAPSTONE_FINAL_REV3_CUMULATIVE_RECEIPT.json"
SEMANTIC_RECEIPT = ROOT / "qa/BACKEND_CAPSTONE_FINAL_REV3_SEMANTIC_RECEIPT.json"
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


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def bundle(raw_by_file: dict[str, bytes]) -> dict[str, Any]:
    state = hashlib.sha256(); records = 0; byte_count = 0
    for name in FILES:
        raw = raw_by_file[name]
        records += len(raw.splitlines()); byte_count += len(raw)
        state.update(name.encode("utf-8")); state.update(b"\0"); state.update(raw)
    return {"records": records, "bytes": byte_count, "bundle_sha256": state.hexdigest()}


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(raw); os.replace(temp, path)


def main() -> int:
    first = json.loads((CANDIDATE / "run-a/RECEIPT.json").read_text(encoding="utf-8"))
    second = json.loads((CANDIDATE / "run-b/RECEIPT.json").read_text(encoding="utf-8"))
    require(first == second and first.get("status") == "PASS_CANDIDATE", "artifact candidate receipts failed or differ")
    require(first.get("baseline") == BASELINE, "artifact candidate baseline drift")
    require(first.get("suffix_total", {}).get("records") == 13, "artifact suffix count drift")
    require(first.get("final", {}).get("records") == 8338, "final cumulative record count drift")
    semantic_raw = SEMANTIC_RECEIPT.read_bytes()
    require((len(semantic_raw), sha(semantic_raw)) == (first["semantic_receipt"]["bytes"], first["semantic_receipt"]["sha256"]), "semantic receipt identity drift")

    suffix_raw: dict[str, bytes] = {}
    baseline_raw: dict[str, bytes] = {}
    final_raw: dict[str, bytes] = {}
    state_before: dict[str, str] = {}
    for name in FILES:
        one = (CANDIDATE / "run-a" / name).read_bytes()
        two = (CANDIDATE / "run-b" / name).read_bytes()
        require(one == two, f"artifact candidate bytes differ: {name}")
        require({"records": len(one.splitlines()), "bytes": len(one), "sha256": sha(one)} == first["suffix"][name], f"artifact suffix identity drift: {name}")
        suffix_raw[name] = one
        live = (BACKEND / name).read_bytes()
        if one and live.endswith(one):
            baseline = live[:-len(one)]
            state_before[name] = "already_appended"
        else:
            baseline = live
            state_before[name] = "baseline"
        baseline_raw[name] = baseline
        final_raw[name] = baseline + one
    require(bundle(baseline_raw) == BASELINE, "live backend is neither exact semantic boundary nor safe resumed state")
    require(bundle(final_raw) == first["final"], "reconstructed final backend drift")
    for name in FILES:
        if state_before[name] == "already_appended":
            continue
        target = BACKEND / name
        temp = target.with_name(target.name + ".rev3-evidence.tmp")
        temp.write_bytes(final_raw[name]); os.replace(temp, target)
    actual = {name: (BACKEND / name).read_bytes() for name in FILES}
    require(actual == final_raw and bundle(actual) == first["final"], "post-apply final backend drift")
    receipt = {
        "status": "PASS",
        "receipt_kind": "final_capstone_rev3_complete_backend_cumulative",
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        "semantic_proof_boundary": BASELINE,
        "semantic_receipt": {"path": SEMANTIC_RECEIPT.relative_to(ROOT).as_posix(), "bytes": len(semantic_raw), "sha256": sha(semantic_raw)},
        "artifact_suffix": first["suffix_total"],
        "final": first["final"],
        "prefix_preserved_byte_for_byte": True,
        "candidate_runs_byte_identical": True,
        "files_promoted": [name for name in FILES if suffix_raw[name]],
        "files_already_complete": [name for name in FILES if not suffix_raw[name]],
        "state_before": state_before,
        "proof_census_scope_note": "PROOF_REPAIR_CENSUS.json binds the complete semantic proof graph at the immediately preceding 8,325-record rev3 boundary; this suffix adds only nine reader/evidence artifact successors and four final-QA successors.",
    }
    atomic_json(OUT, receipt)
    raw = OUT.read_bytes()
    print(json.dumps({"status": "PASS", "receipt": {"path": OUT.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}, "final": first["final"]}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
