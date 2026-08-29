#!/usr/bin/env python3
"""Preflight, live validation, and exact replay for the Lab 3 backend append.

This thin adapter reuses the frozen Lab 2 validator while replacing every
release-specific input/output binding.  It also advances the cumulative
laboratory count only after the inherited exact-prefix and isolated-replay
checks have passed.
"""
from __future__ import annotations

import importlib.util
import hashlib
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/validate-backend-append-only-computation-lab-002.py"
BASE_RAW = BASE.read_bytes()
BASE_IDENTITY = (
    len(BASE_RAW),
    BASE_RAW.count(b"\n"),
    hashlib.sha256(BASE_RAW).hexdigest(),
)
if BASE_IDENTITY != (
    12_402,
    289,
    "8c48e30dc232f4b5491d83c7ef2d7f68a3321663cadaac8ffd3c0d815ccf97d8",
):
    raise RuntimeError("frozen Lab 2 backend validator identity drift")
SPEC = importlib.util.spec_from_file_location("o012_lab03_backend_validator_base", BASE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load the frozen Lab 2 backend validator")
v = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = v
SPEC.loader.exec_module(v)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Lab 3 backend validator FAIL: {message}")


v.require = require

v.OUTPUTS = {
    "plan": ROOT / "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_PLAN.json",
    "semantic": ROOT / "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_RECEIPT.json",
    "replay": ROOT / "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_REPLAY_RECEIPT.json",
    "manifest": ROOT / "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_FILE_MANIFEST.csv",
    "cumulative": ROOT / "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_CUMULATIVE_RECEIPT.json",
}


def load_producer():
    path = ROOT / "scripts/extend-backend-computation-lab-003.py"
    spec = importlib.util.spec_from_file_location("o012_lab03_backend_producer", path)
    v.require(spec is not None and spec.loader is not None, "cannot load Lab 3 producer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    # The Lab 3 producer intentionally patches and delegates to its frozen
    # Lab 2 producer module; the validator needs that fully populated module,
    # not merely the thin command-line wrapper namespace.
    return module.m


v.load_producer = load_producer
inherited_validate_live = v.validate_live


def validate_live(producer):
    final_path = v.OUTPUTS["cumulative"]
    pending = final_path.with_name(f".{final_path.name}.pending")
    v.require(not pending.exists(), "atomic cumulative-receipt temporary collision")
    v.OUTPUTS["cumulative"] = pending
    try:
        receipt = inherited_validate_live(producer)
    except BaseException:
        pending.unlink(missing_ok=True)
        raise
    finally:
        v.OUTPUTS["cumulative"] = final_path
    cumulative = receipt.get("cumulative", {})
    v.require(
        cumulative.get("computation_laboratories_complete") == 2
        and cumulative.get("computation_laboratories_required") == 4,
        "inherited cumulative laboratory count drift",
    )
    cumulative["computation_laboratories_complete"] = 3
    pending.write_bytes(v.json_bytes(receipt))
    os.replace(pending, final_path)
    return receipt


v.validate_live = validate_live


if __name__ == "__main__":
    raise SystemExit(v.main())
