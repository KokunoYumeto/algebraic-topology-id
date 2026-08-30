#!/usr/bin/env python3
"""Resume-safely append the reviewed final capstone semantic revision."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
OVERLAY = ROOT / "qa/capstone-final-rev2-backend-20260829"
RECEIPT = ROOT / "qa/BACKEND_CAPSTONE_FINAL_REV2_SEMANTIC_RECEIPT.json"
FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)


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


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    pending = path.with_name(f".{path.name}.pending")
    require(not pending.exists(), f"pending collision: {pending}")
    pending.write_bytes(raw)
    require(json.loads(pending.read_text(encoding="utf-8"))["status"] == "PASS", "pending receipt invalid")
    os.replace(pending, path)


def main() -> int:
    run_a = json.loads((OVERLAY / "run-a/RECEIPT.json").read_text(encoding="utf-8"))
    run_b = json.loads((OVERLAY / "run-b/RECEIPT.json").read_text(encoding="utf-8"))
    require(run_a == run_b and run_a["status"] == "PASS_CANDIDATE", "candidate replay receipt drift")
    suffix: dict[str, bytes] = {}
    before: dict[str, bytes] = {}
    expected_final: dict[str, bytes] = {}
    state_before: dict[str, str] = {}
    for name in FILES:
        a = (OVERLAY / "run-a" / name).read_bytes()
        b = (OVERLAY / "run-b" / name).read_bytes()
        require(a == b, f"candidate byte drift: {name}")
        ident = run_a["suffix"][name]
        require({"records": len(a.splitlines()), "bytes": len(a), "sha256": sha(a)} == ident, f"suffix identity drift: {name}")
        live = (BACKEND / name).read_bytes()
        suffix[name] = a
        if len(a) and live.endswith(a):
            prefix = live[:-len(a)]
            state_before[name] = "already_appended"
        else:
            prefix = live
            state_before[name] = "baseline"
        before[name] = prefix
        expected_final[name] = prefix + a
    require(bundle(before) == run_a["baseline"], "live prefix is not the frozen candidate baseline")
    require(bundle(expected_final) == run_a["final"], "candidate final identity drift")

    promoted: list[str] = []
    already: list[str] = []
    for name in FILES:
        path = BACKEND / name
        current = path.read_bytes()
        if current == expected_final[name]:
            already.append(name)
            continue
        require(current == before[name], f"live file is neither baseline nor exact final: {name}")
        pending = path.with_name(f".{path.name}.capstone-rev2.pending")
        require(not pending.exists(), f"pending collision: {pending}")
        with pending.open("wb") as stream:
            stream.write(expected_final[name])
            stream.flush()
            os.fsync(stream.fileno())
        require(pending.read_bytes() == expected_final[name], f"staged append drift: {name}")
        os.replace(pending, path)
        promoted.append(name)

    final_raw = {name: (BACKEND / name).read_bytes() for name in FILES}
    require(all(final_raw[name] == expected_final[name] for name in FILES), "post-append file drift")
    require(bundle(final_raw) == run_a["final"], "post-append bundle drift")
    receipt = {
        "status": "PASS",
        "receipt_kind": "final_capstone_semantic_rev2_append_only_finalization",
        "model_provenance": run_a["model_provenance"],
        "source": run_a["source"],
        "baseline": run_a["baseline"],
        "suffix": run_a["suffix_total"],
        "final": run_a["final"],
        "state_before": state_before,
        "files_promoted": promoted,
        "files_already_complete": already,
        "candidate_directory": "qa/capstone-final-rev2-backend-20260829",
        "prefix_preserved_byte_for_byte": True,
    }
    atomic_json(RECEIPT, receipt)
    raw = RECEIPT.read_bytes()
    print(json.dumps({"status": "PASS", "receipt": {"path": RECEIPT.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}, "final": run_a["final"]}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
