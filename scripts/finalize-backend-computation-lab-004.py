#!/usr/bin/env python3
"""Resume-safe orchestration for the D60-LAB04 backend transaction.

With --preflight this runs only the independent candidate validation.  With no
arguments it accepts exactly one of two live states: the frozen Lab 3 prefix,
or the already complete deterministic Lab 4 suffix.  In the former state it
runs the producer once; in the latter it skips the append.  Both paths finish
with independent live validation and an atomic finalization receipt.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/validate-backend-append-only-computation-lab-004.py"
PRODUCER_PATH = ROOT / "scripts/extend-backend-computation-lab-004.py"
RECEIPT_PATH = ROOT / "qa/BACKEND_COMPUTATION_LAB_004_FINALIZATION_RECEIPT.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Lab 4 backend finalizer FAIL: {message}")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def file_identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(raw),
        "lf_lines": raw.count(b"\n"),
        "sha256": digest(raw),
    }


def load_validator():
    require(VALIDATOR_PATH.is_file(), "independent validator is missing")
    spec = importlib.util.spec_from_file_location("o012_lab04_independent_backend_validator_for_finalization", VALIDATOR_PATH)
    require(spec is not None and spec.loader is not None, "cannot load independent validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    required = ("load_producer", "read_prefix", "candidate_state", "preflight", "validate_live", "FILES", "OUTPUTS")
    require(all(hasattr(module, name) for name in required), "independent validator interface is incomplete")
    return module


def live_state(validator, candidate: dict[str, bytes]) -> tuple[str, dict[str, bytes], dict[str, bytes], dict[str, bytes]]:
    prefix, suffix, live = validator.read_prefix()
    states = {
        name: "prefix" if suffix[name] == b"" else "candidate" if suffix[name] == candidate[name] else "invalid"
        for name in validator.FILES
    }
    require("invalid" not in states.values(), "a live backend file is neither exact Lab 3 prefix nor exact Lab 4 candidate")
    if all(state == "prefix" for state in states.values()):
        label = "LAB3_PREFIX"
    elif all(state == "candidate" for state in states.values()):
        label = "LAB4_ALREADY_APPENDED"
    else:
        label = "LAB4_SAFE_PARTIAL_CANDIDATE"
    return label, prefix, suffix, live


def promote_candidate(validator, prefix: dict[str, bytes], candidate: dict[str, bytes]) -> dict[str, Any]:
    promoted: list[str] = []
    already_complete: list[str] = []
    for name in validator.FILES:
        path = validator.BACKEND / name
        expected = prefix[name] + candidate[name]
        current = path.read_bytes()
        if current == expected:
            already_complete.append(name)
            continue
        require(current == prefix[name], f"backend changed before exact promotion: {name}")
        pending = path.with_name(f".{path.name}.lab04.pending")
        require(not pending.exists(), f"promotion temporary collision: {name}")
        with pending.open("wb") as stream:
            stream.write(expected)
            stream.flush()
            os.fsync(stream.fileno())
        require(pending.read_bytes() == expected, f"staged candidate verification failed: {name}")
        os.replace(pending, path)
        require(path.read_bytes() == expected, f"atomic candidate promotion failed: {name}")
        promoted.append(name)
    require(all((validator.BACKEND / name).read_bytes() == prefix[name] + candidate[name] for name in validator.FILES), "post-promotion backend mismatch")
    return {
        "status": "PASS",
        "promotion_kind": "exact_resume_safe_per_file_atomic_replacement",
        "files_promoted": promoted,
        "files_already_complete": already_complete,
        "final_file_count": len(validator.FILES),
    }


def write_atomic(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_name(f".{path.name}.pending")
    require(not pending.exists(), "atomic receipt temporary collision")
    pending.write_bytes(raw)
    os.replace(pending, path)


def main() -> int:
    require(sys.argv[1:] in ([], ["--preflight"]), "accepted invocation is no arguments or --preflight")
    validator = load_validator()
    producer = validator.load_producer()
    if sys.argv[1:] == ["--preflight"]:
        receipt = validator.preflight(producer)
        print(json.dumps({
            "status": receipt["status"],
            "laboratory_id": validator.LAB_ID,
            "receipt": file_identity(validator.OUTPUTS["semantic"]),
        }, ensure_ascii=False, sort_keys=True))
        return 0

    prefix, _suffix, _live = validator.read_prefix()
    candidate = validator.candidate_state(producer, prefix)
    state_before, _prefix, _suffix, _live = live_state(validator, candidate["candidate"]["raw"])
    promotion: dict[str, Any] | None = None
    if state_before == "LAB3_PREFIX":
        validator.preflight(producer)
    if state_before != "LAB4_ALREADY_APPENDED":
        promotion = promote_candidate(validator, prefix, candidate["candidate"]["raw"])

    receipt = validator.validate_live(producer)
    _prefix, live_suffix, live = validator.read_prefix()
    require(all(live_suffix[name] == candidate["candidate"]["raw"][name] for name in validator.FILES), "post-validation suffix drift")
    require(validator.bundle(live) == candidate["final_identity"], "post-validation cumulative identity drift")
    cumulative_path = validator.OUTPUTS["cumulative"]
    cumulative = json.loads(cumulative_path.read_bytes())
    require(
        receipt.get("status") == "PASS"
        and cumulative.get("status") == "PASS"
        and cumulative.get("laboratory_id") == validator.LAB_ID
        and cumulative.get("cumulative", {}).get("computation_laboratories_complete") == 4
        and cumulative.get("cumulative", {}).get("computation_laboratories_required") == 4,
        "independent cumulative receipt does not close four of four laboratories",
    )
    finalization = {
        "schema_version": "1.0",
        "status": "PASS",
        "receipt_kind": "resume_safe_backend_finalization",
        "laboratory_id": validator.LAB_ID,
        "edition_unit_id": validator.EDITION_UNIT_ID,
        "state_before": state_before,
        "promotion": promotion,
        "producer_skipped_as_already_complete": state_before == "LAB4_ALREADY_APPENDED",
        "producer_two_run_replay_receipt": candidate["producer_replay"],
        "candidate": {
            "records": candidate["candidate_identity"][0],
            "bytes": candidate["candidate_identity"][1],
            "bundle_sha256": candidate["candidate_identity"][2],
        },
        "cumulative": {
            "records": candidate["final_identity"][0],
            "bytes": candidate["final_identity"][1],
            "bundle_sha256": candidate["final_identity"][2],
            "computation_laboratories_complete": 4,
            "computation_laboratories_required": 4,
        },
        "independent_cumulative_receipt": file_identity(cumulative_path),
        "validator": file_identity(VALIDATOR_PATH),
        "producer": file_identity(PRODUCER_PATH),
        "model_provenance": validator.MODEL,
    }
    write_atomic(RECEIPT_PATH, json_bytes(finalization))
    print(json.dumps({
        "status": "PASS",
        "laboratory_id": validator.LAB_ID,
        "state_before": state_before,
        "receipt": file_identity(RECEIPT_PATH),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
