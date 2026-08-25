#!/usr/bin/env python3
"""Read-only validator for the exact Fomberg Unit 006 append-only suffix."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
PRODUCER_PATH = LANE / "scripts/extend-backend-fomberg-unit-006.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Fomberg Unit 006 backend validator FAIL: {message}")


def load_producer():
    spec = importlib.util.spec_from_file_location("o012_fomberg_u006_producer_for_validator", PRODUCER_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load Fomberg Unit 006 producer")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def parse_canonical_records(c, name: str, raw: bytes) -> list[dict[str, Any]]:
    if not raw:
        return []
    require(b"\r" not in raw and raw.endswith(b"\n"), f"{name}: LF discipline mismatch")
    records: list[dict[str, Any]] = []
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        try:
            record = json.loads(line.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SystemExit(f"{name}:{number}: invalid canonical JSON ({exc})")
        require(isinstance(record, dict), f"{name}:{number}: record is not an object")
        require(c.canon(record) == line, f"{name}:{number}: noncanonical JSONL")
        records.append(record)
    return records


def load_exact_partition(c, expected_suffixes: dict[str, bytes], counts: dict[str, int]):
    prefix_records: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    seen: set[str] = set(); file_results: dict[str, dict[str, Any]] = {}
    prefix_bundle = hashlib.sha256(); final_bundle = hashlib.sha256()
    prefix_count = prefix_bytes = final_count = final_bytes = 0
    for name in c.FILES:
        live = (BACKEND / name).read_bytes()
        expected_count, boundary, prefix_sha = c.PREFIX[name]
        require(len(live) >= boundary, f"{name}: shorter than immutable prefix")
        prefix = live[:boundary]; suffix = live[boundary:]
        require(
            (len(prefix.splitlines()), len(prefix), c.digest(prefix)) == (expected_count, boundary, prefix_sha),
            f"{name}: immutable Unit 005 prefix partition mismatch",
        )
        require(suffix == expected_suffixes[name], f"{name}: live suffix differs from deterministic reconstruction")
        require(len(suffix.splitlines()) == counts[name], f"{name}: suffix count mismatch")
        parsed_prefix = parse_canonical_records(c, f"{name}:prefix", prefix)
        parsed_suffix = parse_canonical_records(c, f"{name}:suffix", suffix)
        prefix_records.extend(parsed_prefix)
        for record in parsed_prefix + parsed_suffix:
            ident = record.get("id")
            require(isinstance(ident, str) and ident and ident not in seen, f"{name}: invalid or duplicate ID {ident!r}")
            seen.add(ident); all_records.append(record)
        file_results[name] = {
            "prefix_records": expected_count, "prefix_bytes": boundary,
            "prefix_sha256": prefix_sha, "records_added": counts[name],
            "final_records": len(parsed_prefix) + len(parsed_suffix),
            "final_bytes": len(live), "final_sha256": c.digest(live),
            "prefix_preserved": True, "suffix_exact": True,
        }
        prefix_bundle.update(name.encode("utf-8")); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        final_bundle.update(name.encode("utf-8")); final_bundle.update(b"\0"); final_bundle.update(live)
        prefix_count += len(parsed_prefix); prefix_bytes += len(prefix)
        final_count += len(parsed_prefix) + len(parsed_suffix); final_bytes += len(live)
    require((prefix_count, prefix_bytes, prefix_bundle.hexdigest()) == c.PREFIX_TOTAL, "immutable prefix bundle mismatch")
    final = (final_count, final_bytes, final_bundle.hexdigest())
    require(final_count == c.PREFIX_TOTAL[0] + sum(counts.values()), "cumulative record count mismatch")
    return prefix_records, all_records, file_results, final


def main() -> int:
    require(not sys.argv[1:], "validator accepts no write or replacement modes")
    producer = load_producer(); c = producer.load_common()
    identities = c.discover_identities(); data = c.verify_all_inputs(identities)
    additions = c.build_additions(data); counts = c.delta(additions)
    producer.validate_record_plan(c, data, additions)
    expected_suffixes = {name: b"".join(c.canon(record) for record in additions[name]) for name in c.FILES}
    prefix_records, all_records, files, final = load_exact_partition(c, expected_suffixes, counts)
    _, reconstructed = producer.validate_merged(c, data, identities, prefix_records, additions)
    require(
        {record["id"]: record for record in reconstructed} == {record["id"]: record for record in all_records},
        "live records differ semantically from reconstruction",
    )
    for name in c.FILES:
        suffix = (BACKEND / name).read_bytes()[c.PREFIX[name][1]:]
        parsed = parse_canonical_records(c, f"{name}:suffix-recheck", suffix)
        require([record["id"] for record in parsed] == [record["id"] for record in additions[name]], f"{name}: suffix ID order mismatch")
    refreshed_identities = c.discover_identities()
    require(refreshed_identities == identities, "input identities changed during validation")
    refreshed = c.verify_all_inputs(refreshed_identities); refreshed_additions = c.build_additions(refreshed)
    producer.validate_record_plan(c, refreshed, refreshed_additions)
    for name in c.FILES:
        refreshed_suffix = b"".join(c.canon(record) for record in refreshed_additions[name])
        require((BACKEND / name).read_bytes()[c.PREFIX[name][1]:] == refreshed_suffix, f"{name}: live suffix/evidence binding changed")
    print("Fomberg Unit 006 append-only backend validation: PASS")
    print(f"prefix_records={c.PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={c.PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={c.PREFIX_TOTAL[2]}")
    print(f"records_added={sum(counts.values())}")
    print(f"cumulative_records={final[0]}")
    print(f"cumulative_bytes={final[1]}")
    print(f"backend_bundle_sha256={final[2]}")
    for name in c.FILES:
        result = files[name]
        print(f"{name}: records={result['final_records']} bytes={result['final_bytes']} sha256={result['final_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
