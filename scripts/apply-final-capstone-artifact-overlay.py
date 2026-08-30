#!/usr/bin/env python3
"""Resume-safely append final reader/evidence records and bind cumulative backend identity."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
OVERLAY = ROOT / "qa/capstone-final-artifacts-backend-20260829"
SEMANTIC_RECEIPT = ROOT / "qa/BACKEND_CAPSTONE_FINAL_REV2_SEMANTIC_RECEIPT.json"
OUT = ROOT / "qa/BACKEND_CAPSTONE_FINAL_CUMULATIVE_RECEIPT.json"
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
    a = json.loads((OVERLAY / "run-a/RECEIPT.json").read_text(encoding="utf-8"))
    b = json.loads((OVERLAY / "run-b/RECEIPT.json").read_text(encoding="utf-8"))
    require(a == b and a["status"] == "PASS_CANDIDATE", "final artifact candidate replay drift")
    suffix: dict[str, bytes] = {}
    prefix: dict[str, bytes] = {}
    expected: dict[str, bytes] = {}
    state_before: dict[str, str] = {}
    for name in FILES:
        one = (OVERLAY / "run-a" / name).read_bytes()
        two = (OVERLAY / "run-b" / name).read_bytes()
        require(one == two, f"candidate byte drift: {name}")
        require({"records": len(one.splitlines()), "bytes": len(one), "sha256": sha(one)} == a["suffix"][name], f"candidate identity drift: {name}")
        live = (BACKEND / name).read_bytes()
        if one and live.endswith(one):
            prefix[name] = live[:-len(one)]
            state_before[name] = "already_appended"
        else:
            prefix[name] = live
            state_before[name] = "baseline"
        suffix[name] = one
        expected[name] = prefix[name] + one
    require(bundle(prefix) == a["baseline"], "live semantic prefix drift")
    require(bundle(expected) == a["final"], "final artifact candidate bundle drift")

    promoted: list[str] = []
    already: list[str] = []
    for name in FILES:
        path = BACKEND / name
        current = path.read_bytes()
        if current == expected[name]:
            already.append(name)
            continue
        require(current == prefix[name], f"live file is neither exact prefix nor exact final: {name}")
        pending = path.with_name(f".{path.name}.capstone-final-artifacts.pending")
        require(not pending.exists(), f"pending collision: {pending}")
        with pending.open("wb") as stream:
            stream.write(expected[name])
            stream.flush()
            os.fsync(stream.fileno())
        require(pending.read_bytes() == expected[name], f"staged final artifact append drift: {name}")
        os.replace(pending, path)
        promoted.append(name)

    final_raw = {name: (BACKEND / name).read_bytes() for name in FILES}
    require(all(final_raw[name] == expected[name] for name in FILES), "post-append final artifact file drift")
    require(bundle(final_raw) == a["final"], "post-append final artifact bundle drift")
    semantic_raw = SEMANTIC_RECEIPT.read_bytes()
    semantic = json.loads(semantic_raw)
    require(semantic["status"] == "PASS" and semantic["final"] == a["baseline"], "semantic receipt does not bind the artifact-overlay prefix")
    receipt = {
        "status": "PASS",
        "receipt_kind": "final_capstone_complete_backend_cumulative",
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        "semantic_proof_boundary": a["baseline"],
        "semantic_receipt": {"path": SEMANTIC_RECEIPT.relative_to(ROOT).as_posix(), "bytes": len(semantic_raw), "sha256": sha(semantic_raw)},
        "artifact_suffix": a["suffix_total"],
        "final": a["final"],
        "state_before": state_before,
        "files_promoted": promoted,
        "files_already_complete": already,
        "prefix_preserved_byte_for_byte": True,
        "proof_census_scope_note": "PROOF_REPAIR_CENSUS.json binds the complete semantic proof graph at the immediately preceding 8,168-record boundary; this final suffix adds only its reader/evidence artifact records and QA bindings.",
    }
    atomic_json(OUT, receipt)
    raw = OUT.read_bytes()
    print(json.dumps({"status": "PASS", "receipt": {"path": OUT.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}, "final": a["final"]}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
