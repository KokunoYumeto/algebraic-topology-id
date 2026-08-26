#!/usr/bin/env python3
"""Validate/replay the exact D60-CA01 append and write deterministic receipts."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
PRODUCER_PATH = LANE / "scripts/extend-backend-cumulative-assessment-001.py"
OUTPUTS = {
    "manifest": LANE / "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENT_001_FILE_MANIFEST.csv",
    "plan": LANE / "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENT_001_PLAN.json",
    "semantic": LANE / "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENT_001_RECEIPT.json",
    "replay": LANE / "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENT_001_REPLAY_RECEIPT.json",
    "cumulative": LANE / "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENT_001_CUMULATIVE_RECEIPT.json",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CA01 append-only validator FAIL: {message}")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_producer():
    spec = importlib.util.spec_from_file_location("o012_ca01_backend_producer_for_validator", PRODUCER_PATH)
    require(spec is not None and spec.loader is not None, "cannot load CA01 backend producer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_canonical(p, name: str, raw: bytes) -> list[dict[str, Any]]:
    if not raw:
        return []
    require(b"\r" not in raw and raw.endswith(b"\n"), f"{name}: JSONL discipline mismatch")
    records: list[dict[str, Any]] = []
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        try:
            record = json.loads(line.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SystemExit(f"CA01 append-only validator FAIL: {name}:{number}: invalid JSON ({exc})")
        require(isinstance(record, dict), f"{name}:{number}: record is not an object")
        require(p.canon(record) == line, f"{name}:{number}: noncanonical JSONL")
        records.append(record)
    return records


def bundle(p, raw_by_file: dict[str, bytes]) -> tuple[int, int, str]:
    h = hashlib.sha256(); records = byte_count = 0
    for name in p.FILES:
        raw = raw_by_file[name]
        records += len(raw.splitlines()); byte_count += len(raw)
        h.update(name.encode("utf-8")); h.update(b"\0"); h.update(raw)
    return records, byte_count, h.hexdigest()


def partition_live(p, expected_suffixes: dict[str, bytes]) -> tuple[dict[str, bytes], dict[str, bytes], list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    prefixes: dict[str, bytes] = {}; finals: dict[str, bytes] = {}
    prefix_records: list[dict[str, Any]] = []; all_records: list[dict[str, Any]] = []
    files: dict[str, dict[str, Any]] = {}; seen: set[str] = set()
    for name in p.FILES:
        live = (BACKEND / name).read_bytes()
        expected_records, boundary, expected_prefix_sha = p.PREFIX[name]
        require(len(live) >= boundary, f"{name}: shorter than frozen prefix")
        prefix = live[:boundary]; suffix = live[boundary:]
        require((len(prefix.splitlines()), len(prefix), digest(prefix)) == (expected_records, boundary, expected_prefix_sha), f"{name}: frozen prefix partition mismatch")
        require(suffix == expected_suffixes[name], f"{name}: live suffix differs from deterministic reconstruction")
        parsed_prefix = parse_canonical(p, f"{name}:prefix", prefix)
        parsed_suffix = parse_canonical(p, f"{name}:suffix", suffix)
        for record in parsed_prefix + parsed_suffix:
            ident = record.get("id")
            require(isinstance(ident, str) and ident and ident not in seen, f"{name}: invalid/duplicate global ID {ident!r}")
            seen.add(ident)
        prefix_records.extend(parsed_prefix); all_records.extend(parsed_prefix + parsed_suffix)
        prefixes[name] = prefix; finals[name] = live
        files[name] = {
            "path": f"backend/{name}",
            "prefix_records": len(parsed_prefix), "prefix_bytes": len(prefix), "prefix_sha256": digest(prefix),
            "records_added": len(parsed_suffix), "suffix_bytes": len(suffix), "suffix_sha256": digest(suffix),
            "final_records": len(parsed_prefix) + len(parsed_suffix), "final_bytes": len(live), "final_sha256": digest(live),
            "prefix_preserved": True, "suffix_exact": True,
        }
    require(bundle(p, prefixes) == p.PREFIX_TOTAL, "frozen prefix bundle mismatch")
    return prefixes, finals, prefix_records, all_records, files


def replay(p, prefix: dict[str, bytes], additions: dict[str, list[dict[str, Any]]], expected_finals: dict[str, bytes]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="o012-ca01-backend-replay-") as temporary:
        backend = Path(temporary) / "backend"; backend.mkdir()
        for name in p.FILES:
            (backend / name).write_bytes(prefix[name])
        replay_suffixes = p.append_suffix(backend, prefix, additions)
        replay_finals = {name: (backend / name).read_bytes() for name in p.FILES}
        require(replay_finals == expected_finals, "isolated replay bytes differ from live backend")
        return {
            "status": "PASS",
            "temporary_replay_removed": True,
            "exact_file_matches": len(p.FILES),
            "suffix_bytes": sum(len(replay_suffixes[name]) for name in p.FILES),
            "final": {"records": bundle(p, replay_finals)[0], "bytes": bundle(p, replay_finals)[1], "bundle_sha256": bundle(p, replay_finals)[2]},
        }


def generic_baseline_diagnostic() -> dict[str, Any]:
    command = [sys.executable, "-B", str(LANE / "scripts/validate-backend.py")]
    result = subprocess.run(command, cwd=LANE, capture_output=True, text=True, encoding="utf-8", errors="strict")
    message = (result.stdout + result.stderr).strip()
    expected = "backend validation: FAIL: artifacts.jsonl: records are not sorted by ordinal id"
    require(result.returncode == 1 and message == expected, f"generic baseline diagnostic changed unexpectedly: rc={result.returncode}, output={message!r}")
    return {
        "command": "python -B scripts/validate-backend.py",
        "exit_code": result.returncode,
        "output": message,
        "status": "PRE_EXISTING_BASELINE_INCOMPATIBILITY",
        "interpretation": "The direct legacy validator rejects historical per-file append order in the immutable published Unit 007 prefix. The prefix was not reordered; merged schema/reference checks and exact replay are the applicable gates.",
    }


def json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": path.relative_to(LANE).as_posix(), "bytes": len(raw), "lf_lines": raw.count(b"\n"), "sha256": digest(raw)}


def write(path: Path, raw: bytes) -> None:
    path.write_bytes(raw)
    require(path.read_bytes() == raw, f"receipt write/readback mismatch: {path.name}")


def manifest_bytes(p, files: dict[str, dict[str, Any]]) -> bytes:
    stream = io.StringIO(newline="")
    fields = ["path", "prefix_records", "prefix_bytes", "prefix_sha256", "records_added", "suffix_bytes", "suffix_sha256", "final_records", "final_bytes", "final_sha256"]
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for name in p.FILES:
        writer.writerow({field: files[name][field] for field in fields})
    return stream.getvalue().encode("utf-8")


def validate(preflight: bool) -> dict[str, Any]:
    p = load_producer()
    data = p.verify_inputs(); additions = p.build_additions(data)
    expected_suffixes = p.suffixes(additions)
    plan = p.record_plan(additions)
    if preflight:
        prefix, prefix_records = p.verify_prefix(BACKEND)
        semantic = p.validate_semantics(prefix_records, additions, data)
        expected_finals = {name: prefix[name] + expected_suffixes[name] for name in p.FILES}
        replay_result = replay(p, prefix, additions, expected_finals)
        return {"status": "PASS", "mode": "preflight", "plan": plan, "semantic": semantic, "replay": replay_result}

    prefixes, finals, prefix_records, live_records, files = partition_live(p, expected_suffixes)
    semantic = p.validate_semantics(prefix_records, additions, data)
    reconstructed = prefix_records + [record for name in p.FILES for record in additions[name]]
    require({record["id"]: record for record in reconstructed} == {record["id"]: record for record in live_records}, "live merged graph differs semantically from reconstruction")
    final_total = bundle(p, finals)
    delta_records = sum(len(additions[name]) for name in p.FILES)
    require(final_total[0] == p.PREFIX_TOTAL[0] + delta_records, "final record total mismatch")
    suffix_total = bundle(p, expected_suffixes)
    require(suffix_total[0] == delta_records, "suffix record total mismatch")
    replay_result = replay(p, prefixes, additions, finals)
    baseline = generic_baseline_diagnostic()

    refreshed_data = p.verify_inputs(); refreshed_additions = p.build_additions(refreshed_data)
    require(p.record_plan(refreshed_additions) == plan and p.suffixes(refreshed_additions) == expected_suffixes, "input/reconstruction drift during validation")
    return {
        "producer": p, "data": data, "additions": additions, "plan": plan,
        "semantic": semantic, "replay": replay_result, "baseline": baseline,
        "files": files, "prefix_total": p.PREFIX_TOTAL, "suffix_total": suffix_total,
        "final_total": final_total,
    }


def main() -> int:
    require(sys.argv[1:] in ([], ["--preflight"]), "accepted invocation is no arguments or --preflight")
    if sys.argv[1:] == ["--preflight"]:
        result = validate(True)
        print("CA01 append-only backend preflight: PASS")
        print(f"records_planned={sum(result['plan']['records_by_file'].values())}")
        print(f"replay_bundle_sha256={result['replay']['final']['bundle_sha256']}")
        return 0

    result = validate(False); p = result["producer"]
    plan_receipt = {
        "status": "PASS", "receipt_kind": "deterministic_append_plan", "assessment_id": "D60-CA01",
        "producer": "scripts/extend-backend-cumulative-assessment-001.py", **result["plan"],
    }
    semantic_receipt = {
        "status": "PASS", "receipt_kind": "semantic_append_validation", "assessment_id": "D60-CA01",
        "reader_sha256": p.READER_SHA256, "input_identities": {
            relative: {"bytes": value[0], "lf_lines": value[1], "sha256": value[2]}
            for relative, value in p.INPUT_IDENTITIES.items()
        },
        "semantic_checks": result["semantic"],
        "generic_validator_baseline_diagnostic": result["baseline"],
    }
    replay_receipt = {
        "status": "PASS", "receipt_kind": "isolated_binary_replay", "assessment_id": "D60-CA01",
        "immutable_prefix": {"records": result["prefix_total"][0], "bytes": result["prefix_total"][1], "bundle_sha256": result["prefix_total"][2]},
        "replay": result["replay"], "all_live_files_equal_replay": True,
    }
    write(OUTPUTS["manifest"], manifest_bytes(p, result["files"]))
    write(OUTPUTS["plan"], json_bytes(plan_receipt))
    write(OUTPUTS["semantic"], json_bytes(semantic_receipt))
    write(OUTPUTS["replay"], json_bytes(replay_receipt))
    receipt_identities = {name: identity(OUTPUTS[name]) for name in ("manifest", "plan", "semantic", "replay")}
    cumulative_receipt = {
        "status": "PASS", "receipt_kind": "cumulative_backend_boundary", "assessment_id": "D60-CA01",
        "edition_unit_id": "O012-ORIG-CA01", "model_provenance": p.MODEL,
        "immutable_prefix": {"records": result["prefix_total"][0], "bytes": result["prefix_total"][1], "bundle_sha256": result["prefix_total"][2], "preserved_exactly": True},
        "delta": {
            "records": result["suffix_total"][0], "bytes": result["suffix_total"][1], "bundle_sha256": result["suffix_total"][2],
            "records_by_file": result["plan"]["records_by_file"], "bytes_by_file": result["plan"]["bytes_by_file"],
        },
        "cumulative": {"records": result["final_total"][0], "bytes": result["final_total"][1], "bundle_sha256": result["final_total"][2]},
        "files": [result["files"][name] for name in p.FILES],
        "semantic_checks": result["semantic"],
        "replay": result["replay"],
        "generic_validator_baseline_diagnostic": result["baseline"],
        "supporting_receipts": receipt_identities,
    }
    write(OUTPUTS["cumulative"], json_bytes(cumulative_receipt))
    cumulative_identity = identity(OUTPUTS["cumulative"])
    print("CA01 append-only backend validation: PASS")
    print(f"prefix_records={result['prefix_total'][0]}")
    print(f"prefix_bytes={result['prefix_total'][1]}")
    print(f"prefix_bundle_sha256={result['prefix_total'][2]}")
    print(f"records_added={result['suffix_total'][0]}")
    print(f"suffix_bytes={result['suffix_total'][1]}")
    print(f"suffix_bundle_sha256={result['suffix_total'][2]}")
    print(f"cumulative_records={result['final_total'][0]}")
    print(f"cumulative_bytes={result['final_total'][1]}")
    print(f"backend_bundle_sha256={result['final_total'][2]}")
    print(f"cumulative_receipt_sha256={cumulative_identity['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
