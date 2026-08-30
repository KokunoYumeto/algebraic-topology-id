#!/usr/bin/env python3
"""Apply the proved final-capstone rev3 semantic suffix append-only and resumably."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
CANDIDATE = ROOT / "qa/capstone-final-rev3-backend-20260829"
OUT = ROOT / "qa/BACKEND_CAPSTONE_FINAL_REV3_SEMANTIC_RECEIPT.json"
FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
EXPECTED_BASELINE = {
    "records": 8181,
    "bytes": 9847262,
    "bundle_sha256": "dd689b6cea9933ee5f85e2d30ed6afd44c25ffee470eceb8d74b22ce3248a0ad",
}


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


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


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(raw)
    os.replace(temp, path)


def main() -> int:
    run_a = json.loads((CANDIDATE / "run-a/RECEIPT.json").read_text(encoding="utf-8"))
    run_b = json.loads((CANDIDATE / "run-b/RECEIPT.json").read_text(encoding="utf-8"))
    require(run_a == run_b, "rev3 candidate receipts differ")
    require(run_a.get("status") == "PASS_CANDIDATE", "rev3 candidate did not pass")
    require(run_a.get("baseline") == EXPECTED_BASELINE, "rev3 candidate baseline drift")
    require(run_a.get("suffix_total", {}).get("records") == 144, "rev3 suffix record count drift")
    require(run_a.get("final", {}).get("records") == 8325, "rev3 semantic final record count drift")

    suffix_raw: dict[str, bytes] = {}
    baseline_raw: dict[str, bytes] = {}
    final_raw: dict[str, bytes] = {}
    state_before: dict[str, str] = {}
    for name in FILES:
        one = (CANDIDATE / "run-a" / name).read_bytes()
        two = (CANDIDATE / "run-b" / name).read_bytes()
        require(one == two, f"rev3 candidate bytes differ: {name}")
        require({"records": len(one.splitlines()), "bytes": len(one), "sha256": sha(one)} == run_a["suffix"][name], f"rev3 suffix identity drift: {name}")
        suffix_raw[name] = one
        live = (BACKEND / name).read_bytes()
        suffix = one
        expected_final_records = run_a["final"]["records"]
        if suffix and live.endswith(suffix):
            baseline = live[:-len(suffix)]
            state_before[name] = "already_appended"
        else:
            baseline = live
            state_before[name] = "baseline"
        baseline_raw[name] = baseline
        final_raw[name] = baseline + suffix
    require(bundle(baseline_raw) == EXPECTED_BASELINE, "live backend is neither exact baseline nor safely resumed rev3 state")
    require(bundle(final_raw) == run_a["final"], "rev3 reconstructed final identity drift")

    for name in FILES:
        target = BACKEND / name
        if state_before[name] == "already_appended":
            continue
        temp = target.with_name(target.name + ".rev3.tmp")
        temp.write_bytes(final_raw[name])
        os.replace(temp, target)

    actual = {name: (BACKEND / name).read_bytes() for name in FILES}
    require(actual == final_raw, "rev3 post-apply file bytes drift")
    require(bundle(actual) == run_a["final"], "rev3 post-apply bundle drift")
    receipt = {
        "status": "PASS",
        "receipt_kind": "final_capstone_semantic_rev3_append_only_admission",
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        "source": run_a["source"],
        "baseline": EXPECTED_BASELINE,
        "suffix": run_a["suffix_total"],
        "final": run_a["final"],
        "record_census": {
            "units": 34,
            "segments": 34,
            "terms": 10,
            "relations": 54,
            "rights": 1,
            "source_qa_artifacts": 5,
            "source_qa_events": 5,
            "corrections": 1,
        },
        "correction_id": "O012-ADV-0566",
        "prefix_preserved_byte_for_byte": True,
        "candidate_runs_byte_identical": True,
        "state_before": state_before,
    }
    write_json_atomic(OUT, receipt)
    raw = OUT.read_bytes()
    print(json.dumps({"status": "PASS", "receipt": {"path": OUT.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}, "final": run_a["final"]}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
