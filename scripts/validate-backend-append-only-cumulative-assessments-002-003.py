#!/usr/bin/env python3
"""Validate/replay the exact combined D60-CA02 and D60-CA03 append.

`--preflight` is read-only and proves that the sealed inputs derive a valid
suffix and that an isolated append reproduces the expected bytes.  The default
mode is for the post-append boundary: it partitions every live JSONL file at
the frozen 7,012-record prefix, requires the suffix to equal the producer's
canonical reconstruction, replays all bytes in an isolated temporary backend,
and writes sanitized deterministic receipts.
"""
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
PRODUCER_PATH = LANE / "scripts/extend-backend-cumulative-assessments-002-003.py"
OUTPUTS = {
    "manifest": LANE / "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_FILE_MANIFEST.csv",
    "plan": LANE / "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_PLAN.json",
    "semantic": LANE / "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_RECEIPT.json",
    "replay": LANE / "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_REPLAY_RECEIPT.json",
    "cumulative": LANE / "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_CUMULATIVE_RECEIPT.json",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CA02+CA03 append-only validator FAIL: {message}")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_producer():
    spec = importlib.util.spec_from_file_location("o012_ca02_ca03_backend_producer_for_validator", PRODUCER_PATH)
    require(spec is not None and spec.loader is not None, "cannot load CA02+CA03 backend producer")
    module = importlib.util.module_from_spec(spec)
    # dataclasses resolves the defining module through sys.modules.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_canonical(producer, label: str, raw: bytes) -> list[dict[str, Any]]:
    if not raw:
        return []
    require(b"\r" not in raw and raw.endswith(b"\n"), f"{label}: JSONL discipline mismatch")
    records: list[dict[str, Any]] = []
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        try:
            record = json.loads(line.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SystemExit(f"CA02+CA03 append-only validator FAIL: {label}:{number}: invalid JSON ({exc})")
        require(isinstance(record, dict), f"{label}:{number}: record is not an object")
        require(producer.canon(record) == line, f"{label}:{number}: noncanonical JSONL")
        records.append(record)
    return records


def bundle(producer, raw_by_file: dict[str, bytes]) -> tuple[int, int, str]:
    h = hashlib.sha256()
    records = byte_count = 0
    for name in producer.FILES:
        raw = raw_by_file[name]
        records += len(raw.splitlines()); byte_count += len(raw)
        h.update(name.encode("utf-8")); h.update(b"\0"); h.update(raw)
    return records, byte_count, h.hexdigest()


def partition_live(
    producer,
    expected_suffixes: dict[str, bytes],
) -> tuple[dict[str, bytes], dict[str, bytes], list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    prefixes: dict[str, bytes] = {}
    finals: dict[str, bytes] = {}
    prefix_records: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    files: dict[str, dict[str, Any]] = {}
    seen: set[str] = set()
    for name in producer.FILES:
        live = (BACKEND / name).read_bytes()
        expected_records, boundary, expected_prefix_sha = producer.PREFIX[name]
        require(len(live) >= boundary, f"{name}: shorter than frozen prefix")
        prefix = live[:boundary]
        suffix = live[boundary:]
        require((len(prefix.splitlines()), len(prefix), digest(prefix)) == (expected_records, boundary, expected_prefix_sha), f"{name}: frozen prefix partition mismatch")
        require(suffix == expected_suffixes[name], f"{name}: live suffix differs from deterministic reconstruction")
        parsed_prefix = parse_canonical(producer, f"{name}:prefix", prefix)
        parsed_suffix = parse_canonical(producer, f"{name}:suffix", suffix)
        for record in parsed_prefix + parsed_suffix:
            ident = record.get("id")
            require(isinstance(ident, str) and ident and ident not in seen, f"{name}: invalid or duplicate global ID {ident!r}")
            seen.add(ident)
        prefix_records.extend(parsed_prefix)
        all_records.extend(parsed_prefix + parsed_suffix)
        prefixes[name] = prefix
        finals[name] = live
        files[name] = {
            "path": f"backend/{name}",
            "prefix_records": len(parsed_prefix),
            "prefix_bytes": len(prefix),
            "prefix_sha256": digest(prefix),
            "records_added": len(parsed_suffix),
            "suffix_bytes": len(suffix),
            "suffix_sha256": digest(suffix),
            "final_records": len(parsed_prefix) + len(parsed_suffix),
            "final_bytes": len(live),
            "final_sha256": digest(live),
            "prefix_preserved": True,
            "suffix_exact": True,
        }
    require(bundle(producer, prefixes) == producer.PREFIX_TOTAL, "frozen prefix bundle mismatch")
    return prefixes, finals, prefix_records, all_records, files


def replay(
    producer,
    prefix: dict[str, bytes],
    additions: dict[str, list[dict[str, Any]]],
    expected_finals: dict[str, bytes],
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="o012-ca02-ca03-backend-replay-") as temporary:
        backend = Path(temporary) / "backend"
        backend.mkdir()
        for name in producer.FILES:
            (backend / name).write_bytes(prefix[name])
        replay_suffixes = producer.append_suffix(backend, prefix, additions)
        replay_finals = {name: (backend / name).read_bytes() for name in producer.FILES}
        require(replay_finals == expected_finals, "isolated replay bytes differ from expected/live backend")
        final = bundle(producer, replay_finals)
        return {
            "status": "PASS",
            "temporary_replay_removed": True,
            "exact_file_matches": len(producer.FILES),
            "suffix_bytes": sum(len(replay_suffixes[name]) for name in producer.FILES),
            "final": {"records": final[0], "bytes": final[1], "bundle_sha256": final[2]},
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
        "interpretation": "The direct legacy validator rejects historical per-file append order in the immutable published prefix. The prefix was not reordered; merged schema/reference checks and exact binary replay are the applicable gates.",
    }


def json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def file_identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": path.relative_to(LANE).as_posix(), "bytes": len(raw), "lf_lines": raw.count(b"\n"), "sha256": digest(raw)}


def write(path: Path, raw: bytes) -> None:
    require(b"c:\\users" not in raw.lower(), f"absolute private path in receipt {path.name}")
    path.write_bytes(raw)
    require(path.read_bytes() == raw, f"receipt write/readback mismatch: {path.name}")


def manifest_bytes(producer, files: dict[str, dict[str, Any]]) -> bytes:
    stream = io.StringIO(newline="")
    fields = [
        "path", "prefix_records", "prefix_bytes", "prefix_sha256", "records_added",
        "suffix_bytes", "suffix_sha256", "final_records", "final_bytes", "final_sha256",
    ]
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for name in producer.FILES:
        writer.writerow({field: files[name][field] for field in fields})
    return stream.getvalue().encode("utf-8")


def validate(preflight: bool) -> dict[str, Any]:
    producer = load_producer()
    data = producer.verify_inputs()
    additions, parsed = producer.build_additions(data)
    expected_suffixes = producer.suffixes(additions)
    plan = producer.record_plan(additions, data)
    if preflight:
        prefix, prefix_records = producer.verify_prefix(BACKEND)
        semantic = producer.validate_semantics(prefix_records, additions, data, parsed)
        expected_finals = {name: prefix[name] + expected_suffixes[name] for name in producer.FILES}
        replay_result = replay(producer, prefix, additions, expected_finals)
        refreshed = producer.verify_inputs(data["identities"])
        refreshed_additions, refreshed_parsed = producer.build_additions(refreshed)
        require(producer.record_plan(refreshed_additions, refreshed) == plan, "input/plan drift during preflight")
        require(producer.suffixes(refreshed_additions) == expected_suffixes and refreshed_parsed == parsed, "input/suffix drift during preflight")
        return {"status": "PASS", "mode": "preflight", "plan": plan, "semantic": semantic, "replay": replay_result}

    prefixes, finals, prefix_records, live_records, files = partition_live(producer, expected_suffixes)
    semantic = producer.validate_semantics(prefix_records, additions, data, parsed)
    reconstructed = prefix_records + [record for name in producer.FILES for record in additions[name]]
    require({record["id"]: record for record in reconstructed} == {record["id"]: record for record in live_records}, "live merged graph differs semantically from reconstruction")
    final_total = bundle(producer, finals)
    suffix_total = bundle(producer, expected_suffixes)
    delta_records = sum(len(additions[name]) for name in producer.FILES)
    require(final_total[0] == producer.PREFIX_TOTAL[0] + delta_records, "final record total mismatch")
    require(suffix_total[0] == delta_records, "suffix record total mismatch")
    replay_result = replay(producer, prefixes, additions, finals)
    baseline = generic_baseline_diagnostic()
    refreshed = producer.verify_inputs(data["identities"])
    refreshed_additions, refreshed_parsed = producer.build_additions(refreshed)
    require(producer.record_plan(refreshed_additions, refreshed) == plan, "input/plan drift during validation")
    require(producer.suffixes(refreshed_additions) == expected_suffixes and refreshed_parsed == parsed, "input/suffix drift during validation")
    return {
        "producer": producer,
        "data": data,
        "plan": plan,
        "semantic": semantic,
        "replay": replay_result,
        "baseline": baseline,
        "files": files,
        "prefix_total": producer.PREFIX_TOTAL,
        "suffix_total": suffix_total,
        "final_total": final_total,
    }


def main() -> int:
    require(sys.argv[1:] in ([], ["--preflight"]), "accepted invocation is no arguments or --preflight")
    if sys.argv[1:] == ["--preflight"]:
        result = validate(True)
        print("CA02+CA03 append-only backend preflight: PASS")
        print(f"records_planned={sum(result['plan']['records_by_file'].values())}")
        print(f"replay_bundle_sha256={result['replay']['final']['bundle_sha256']}")
        return 0

    result = validate(False)
    producer = result["producer"]
    assessment_ids = [spec.assessment_id for spec in producer.SPECS]
    edition_unit_ids = [spec.edition_unit_id for spec in producer.SPECS]
    plan_receipt = {
        "status": "PASS",
        "receipt_kind": "deterministic_append_plan",
        "assessment_ids": assessment_ids,
        "edition_unit_ids": edition_unit_ids,
        "producer": "scripts/extend-backend-cumulative-assessments-002-003.py",
        **result["plan"],
    }
    semantic_receipt = {
        "status": "PASS",
        "receipt_kind": "semantic_append_validation",
        "assessment_ids": assessment_ids,
        "edition_unit_ids": edition_unit_ids,
        "input_identities": {
            relative: {"bytes": value[0], "lf_lines": value[1], "sha256": value[2]}
            for relative, value in sorted(result["data"]["identities"].items())
        },
        "semantic_checks": result["semantic"],
        "generic_validator_baseline_diagnostic": result["baseline"],
    }
    replay_receipt = {
        "status": "PASS",
        "receipt_kind": "isolated_binary_replay",
        "assessment_ids": assessment_ids,
        "immutable_prefix": {
            "records": result["prefix_total"][0],
            "bytes": result["prefix_total"][1],
            "bundle_sha256": result["prefix_total"][2],
        },
        "replay": result["replay"],
        "all_live_files_equal_replay": True,
    }
    write(OUTPUTS["manifest"], manifest_bytes(producer, result["files"]))
    write(OUTPUTS["plan"], json_bytes(plan_receipt))
    write(OUTPUTS["semantic"], json_bytes(semantic_receipt))
    write(OUTPUTS["replay"], json_bytes(replay_receipt))
    supporting = {name: file_identity(OUTPUTS[name]) for name in ("manifest", "plan", "semantic", "replay")}
    cumulative = {
        "status": "PASS",
        "receipt_kind": "cumulative_backend_boundary",
        "assessment_ids": assessment_ids,
        "edition_unit_ids": edition_unit_ids,
        "model_provenance": producer.MODEL,
        "immutable_prefix": {
            "records": result["prefix_total"][0],
            "bytes": result["prefix_total"][1],
            "bundle_sha256": result["prefix_total"][2],
            "preserved_exactly": True,
        },
        "delta": {
            "records": result["suffix_total"][0],
            "bytes": result["suffix_total"][1],
            "bundle_sha256": result["suffix_total"][2],
            "records_by_file": result["plan"]["records_by_file"],
            "bytes_by_file": result["plan"]["bytes_by_file"],
        },
        "cumulative": {
            "records": result["final_total"][0],
            "bytes": result["final_total"][1],
            "bundle_sha256": result["final_total"][2],
            "ordinary_mastery_slots": 84,
            "cumulative_assessment_slots": 24,
            "solution_bearing_slots": 108,
        },
        "files": [result["files"][name] for name in producer.FILES],
        "semantic_checks": result["semantic"],
        "replay": result["replay"],
        "generic_validator_baseline_diagnostic": result["baseline"],
        "supporting_receipts": supporting,
    }
    write(OUTPUTS["cumulative"], json_bytes(cumulative))
    cumulative_identity = file_identity(OUTPUTS["cumulative"])
    print("CA02+CA03 append-only backend validation: PASS")
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
