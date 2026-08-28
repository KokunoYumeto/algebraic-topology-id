#!/usr/bin/env python3
"""Preflight, live validation, and exact replay for the Lab 1 backend append."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
OUTPUTS = {
    "plan": QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_PLAN.json",
    "semantic": QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_RECEIPT.json",
    "replay": QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_REPLAY_RECEIPT.json",
    "manifest": QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_FILE_MANIFEST.csv",
    "cumulative": QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_CUMULATIVE_RECEIPT.json",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Lab 1 backend validator FAIL: {message}")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_producer():
    path = ROOT / "scripts/extend-backend-computation-lab-001.py"
    spec = importlib.util.spec_from_file_location("o012_lab01_backend_producer", path)
    require(spec is not None and spec.loader is not None, "cannot load Lab 1 producer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def file_identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(raw),
        "lf_lines": raw.count(b"\n"),
        "sha256": digest(raw),
    }


def partition_live(producer, expected_suffix: dict[str, bytes], require_suffix: bool) -> tuple[dict[str, bytes], dict[str, bytes], dict[str, bytes]]:
    prefix: dict[str, bytes] = {}
    suffix: dict[str, bytes] = {}
    live: dict[str, bytes] = {}
    for name in producer.FILES:
        raw = (producer.BACKEND / name).read_bytes()
        prefix_bytes = producer.PREFIX[name][1]
        require(len(raw) >= prefix_bytes, f"live backend shorter than immutable prefix: {name}")
        prefix[name] = raw[:prefix_bytes]
        suffix[name] = raw[prefix_bytes:]
        live[name] = raw
        observed_prefix = (len(prefix[name].splitlines()), len(prefix[name]), digest(prefix[name]))
        require(observed_prefix == producer.PREFIX[name], f"immutable prefix mismatch: {name}")
        expected = expected_suffix[name] if require_suffix else b""
        require(suffix[name] == expected, f"live suffix mismatch: {name}")
    require(producer.bundle(prefix) == producer.PREFIX_TOTAL, "immutable prefix bundle mismatch")
    return prefix, suffix, live


def manifest_bytes(producer, prefix: dict[str, bytes], suffix: dict[str, bytes], live: dict[str, bytes]) -> bytes:
    rows = [
        "path,prefix_records,prefix_bytes,prefix_sha256,records_added,suffix_bytes,suffix_sha256,final_records,final_bytes,final_sha256"
    ]
    for name in producer.FILES:
        rows.append(
            ",".join(
                (
                    f"backend/{name}",
                    str(len(prefix[name].splitlines())),
                    str(len(prefix[name])),
                    digest(prefix[name]),
                    str(len(suffix[name].splitlines())),
                    str(len(suffix[name])),
                    digest(suffix[name]),
                    str(len(live[name].splitlines())),
                    str(len(live[name])),
                    digest(live[name]),
                )
            )
        )
    return ("\n".join(rows) + "\n").encode("utf-8")


def build_state(producer) -> dict[str, Any]:
    producer.validate_terminology_csv()
    data = producer.verify_inputs()
    parsed = producer.parse_reader(data["raw"][producer.SOURCE_PATH])
    prefix, prefix_records = producer.verify_prefix()
    additions = producer.build_additions(data, parsed)
    semantic = producer.validate_semantics(prefix_records, additions, data, parsed)
    plan = producer.record_plan(additions, data, semantic)
    return {
        "data": data,
        "parsed": parsed,
        "prefix": prefix,
        "prefix_records": prefix_records,
        "additions": additions,
        "suffix": producer.suffixes(additions),
        "semantic": semantic,
        "plan": plan,
    }


def preflight(producer) -> dict[str, Any]:
    state = build_state(producer)
    partition_live(producer, state["suffix"], require_suffix=False)
    receipt = {
        "schema_version": "1.0",
        "status": "PASS_PREFLIGHT",
        "receipt_kind": "append_only_backend_semantic_preflight",
        "laboratory_id": producer.LAB_ID,
        "edition_unit_id": producer.EDITION_UNIT_ID,
        "immutable_prefix": {
            "records": producer.PREFIX_TOTAL[0],
            "bytes": producer.PREFIX_TOTAL[1],
            "bundle_sha256": producer.PREFIX_TOTAL[2],
        },
        "delta": {
            "records": state["semantic"]["added_records"],
            "bytes": sum(len(state["suffix"][name]) for name in producer.FILES),
            "records_by_file": {name: len(state["additions"][name]) for name in producer.FILES},
            "bytes_by_file": {name: len(state["suffix"][name]) for name in producer.FILES},
        },
        "semantic_checks": state["semantic"],
        "sealed_inputs": state["plan"]["input_identities"],
        "model_provenance": producer.MODEL,
    }
    write(OUTPUTS["plan"], json_bytes(state["plan"]))
    write(OUTPUTS["semantic"], json_bytes(receipt))
    return receipt


def validate_live(producer) -> dict[str, Any]:
    data = producer.verify_inputs()
    parsed = producer.parse_reader(data["raw"][producer.SOURCE_PATH])
    additions = producer.build_additions(data, parsed)
    expected_suffix = producer.suffixes(additions)
    prefix, suffix, live = partition_live(producer, expected_suffix, require_suffix=True)
    prefix_records = producer.parse_records(prefix)
    semantic = producer.validate_semantics(prefix_records, additions, data, parsed)
    plan = producer.record_plan(additions, data, semantic)
    final = producer.bundle(live)
    delta_records = sum(len(suffix[name].splitlines()) for name in producer.FILES)
    delta_bytes = sum(len(suffix[name]) for name in producer.FILES)
    require(delta_records == semantic["added_records"], "delta record-count mismatch")
    require(final[0] == producer.PREFIX_TOTAL[0] + delta_records, "final record-count mismatch")

    replay_removed = False
    replay_final: tuple[int, int, str] | None = None
    scratch_parent = QA / ".bounded-replay"
    scratch_parent.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="lab01-", dir=scratch_parent))
    try:
        for name in producer.FILES:
            (scratch / name).write_bytes(prefix[name] + suffix[name])
        replay_raw = {name: (scratch / name).read_bytes() for name in producer.FILES}
        require(all(replay_raw[name] == live[name] for name in producer.FILES), "isolated replay differs from live backend")
        replay_final = producer.bundle(replay_raw)
        require(replay_final == final, "isolated replay bundle differs")
    finally:
        shutil.rmtree(scratch)
        replay_removed = not scratch.exists()
        try:
            scratch_parent.rmdir()
        except OSError:
            pass
    require(replay_removed and replay_final is not None, "temporary replay was not removed")

    replay_receipt = {
        "schema_version": "1.0",
        "status": "PASS",
        "receipt_kind": "isolated_exact_backend_replay",
        "laboratory_id": producer.LAB_ID,
        "exact_file_matches": len(producer.FILES),
        "suffix_bytes": delta_bytes,
        "final": {"records": final[0], "bytes": final[1], "bundle_sha256": final[2]},
        "temporary_replay_removed": True,
    }
    semantic_receipt = {
        "schema_version": "1.0",
        "status": "PASS",
        "receipt_kind": "append_only_backend_semantic_validation",
        "laboratory_id": producer.LAB_ID,
        "edition_unit_id": producer.EDITION_UNIT_ID,
        "immutable_prefix": {"records": producer.PREFIX_TOTAL[0], "bytes": producer.PREFIX_TOTAL[1], "bundle_sha256": producer.PREFIX_TOTAL[2]},
        "delta": {
            "records": delta_records,
            "bytes": delta_bytes,
            "records_by_file": {name: len(additions[name]) for name in producer.FILES},
            "bytes_by_file": {name: len(suffix[name]) for name in producer.FILES},
        },
        "cumulative": {"records": final[0], "bytes": final[1], "bundle_sha256": final[2]},
        "semantic_checks": semantic,
        "model_provenance": producer.MODEL,
    }
    write(OUTPUTS["plan"], json_bytes(plan))
    write(OUTPUTS["semantic"], json_bytes(semantic_receipt))
    write(OUTPUTS["replay"], json_bytes(replay_receipt))
    write(OUTPUTS["manifest"], manifest_bytes(producer, prefix, suffix, live))

    file_rows = []
    for name in producer.FILES:
        file_rows.append({
            "path": f"backend/{name}",
            "prefix_records": len(prefix[name].splitlines()),
            "prefix_bytes": len(prefix[name]),
            "prefix_sha256": digest(prefix[name]),
            "records_added": len(suffix[name].splitlines()),
            "suffix_bytes": len(suffix[name]),
            "suffix_sha256": digest(suffix[name]),
            "final_records": len(live[name].splitlines()),
            "final_bytes": len(live[name]),
            "final_sha256": digest(live[name]),
            "prefix_preserved": True,
            "suffix_exact": True,
        })
    supporting = {key: file_identity(OUTPUTS[key]) for key in ("plan", "semantic", "replay", "manifest")}
    cumulative = {
        "schema_version": "1.0",
        "status": "PASS",
        "receipt_kind": "cumulative_backend_boundary",
        "laboratory_id": producer.LAB_ID,
        "edition_unit_id": producer.EDITION_UNIT_ID,
        "immutable_prefix": {"records": producer.PREFIX_TOTAL[0], "bytes": producer.PREFIX_TOTAL[1], "bundle_sha256": producer.PREFIX_TOTAL[2], "preserved_exactly": True},
        "delta": {
            "records": delta_records,
            "bytes": delta_bytes,
            "records_by_file": {name: len(additions[name]) for name in producer.FILES},
            "bytes_by_file": {name: len(suffix[name]) for name in producer.FILES},
            "bundle_sha256": digest(b"".join(name.encode("utf-8") + b"\0" + suffix[name] for name in producer.FILES)),
        },
        "cumulative": {"records": final[0], "bytes": final[1], "bundle_sha256": final[2], "computation_laboratories_complete": 1, "computation_laboratories_required": 4},
        "files": file_rows,
        "semantic_checks": semantic,
        "replay": replay_receipt,
        "supporting_receipts": supporting,
        "generic_validator_baseline_diagnostic": {
            "status": "PRE_EXISTING_BASELINE_INCOMPATIBILITY",
            "interpretation": "The historical append-only files are not globally ordinal-sorted. The immutable prefix was not reordered; merged schema/reference validation and exact isolated replay are the applicable gates.",
        },
        "model_provenance": producer.MODEL,
    }
    write(OUTPUTS["cumulative"], json_bytes(cumulative))
    return cumulative


def main() -> int:
    require(sys.argv[1:] in (["--preflight"], []), "accepted invocation is --preflight or no arguments")
    producer = load_producer()
    receipt = preflight(producer) if sys.argv[1:] else validate_live(producer)
    print(json.dumps({
        "status": receipt["status"],
        "laboratory_id": producer.LAB_ID,
        "receipt": file_identity(OUTPUTS["semantic"] if sys.argv[1:] else OUTPUTS["cumulative"]),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
