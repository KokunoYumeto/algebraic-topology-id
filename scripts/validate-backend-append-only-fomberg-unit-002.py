#!/usr/bin/env python3
"""Read-only validator for the exact Fomberg Unit 002 append-only suffix."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
PRODUCER_PATH = LANE / "scripts/extend-backend-fomberg-unit-002.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Fomberg Unit 002 backend validator FAIL: {message}")


def load_producer():
    spec = importlib.util.spec_from_file_location(
        "o012_fomberg_u002_producer_for_validator", PRODUCER_PATH
    )
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load Fomberg Unit 002 producer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_canonical_records(c, name: str, raw: bytes) -> list[dict[str, Any]]:
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


def load_exact_partition(
    c, expected_suffixes: dict[str, bytes]
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    tuple[int, int, str],
]:
    prefix_records: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    seen: set[str] = set()
    file_results: dict[str, dict[str, Any]] = {}
    prefix_bundle = hashlib.sha256()
    final_bundle = hashlib.sha256()
    prefix_record_count = prefix_bytes = 0
    final_record_count = final_bytes = 0

    for name in c.FILES:
        path = BACKEND / name
        require(path.is_file(), f"missing backend file {name}")
        live = path.read_bytes()
        prefix_count, prefix_size, prefix_sha = c.PREFIX[name]
        require(len(live) >= prefix_size, f"{name}: shorter than frozen prefix")
        prefix = live[:prefix_size]
        suffix = live[prefix_size:]
        require(
            (
                len(prefix.splitlines()),
                len(prefix),
                c.digest(prefix),
            )
            == (prefix_count, prefix_size, prefix_sha),
            f"{name}: immutable 5,060-record prefix partition mismatch",
        )
        require(
            suffix == expected_suffixes[name],
            f"{name}: live suffix differs from deterministic common/evidence reconstruction",
        )
        require(
            len(suffix.splitlines()) == c.DELTA[name],
            f"{name}: suffix record count mismatch",
        )

        parsed_prefix = parse_canonical_records(c, f"{name}:prefix", prefix)
        parsed_suffix = (
            parse_canonical_records(c, f"{name}:suffix", suffix)
            if suffix else []
        )
        prefix_records.extend(parsed_prefix)
        for record in parsed_prefix + parsed_suffix:
            ident = record.get("id")
            require(isinstance(ident, str) and ident, f"{name}: missing record ID")
            require(ident not in seen, f"duplicate global backend ID: {ident}")
            seen.add(ident)
            all_records.append(record)

        full_count = len(parsed_prefix) + len(parsed_suffix)
        file_results[name] = {
            "prefix_records": prefix_count,
            "prefix_bytes": prefix_size,
            "prefix_sha256": prefix_sha,
            "records_added": c.DELTA[name],
            "final_records": full_count,
            "final_bytes": len(live),
            "final_sha256": c.digest(live),
            "prefix_preserved": True,
            "suffix_exact": True,
        }
        prefix_bundle.update(name.encode("utf-8"))
        prefix_bundle.update(b"\0")
        prefix_bundle.update(prefix)
        final_bundle.update(name.encode("utf-8"))
        final_bundle.update(b"\0")
        final_bundle.update(live)
        prefix_record_count += len(parsed_prefix)
        prefix_bytes += len(prefix)
        final_record_count += full_count
        final_bytes += len(live)

    observed_prefix = (
        prefix_record_count,
        prefix_bytes,
        prefix_bundle.hexdigest(),
    )
    require(
        observed_prefix == c.PREFIX_TOTAL,
        f"immutable prefix bundle mismatch: {observed_prefix!r}",
    )
    final = (final_record_count, final_bytes, final_bundle.hexdigest())
    require(
        final_record_count == c.PREFIX_TOTAL[0] + sum(c.DELTA.values()) == 5342,
        "cumulative record count mismatch",
    )
    return prefix_records, all_records, file_results, final


def validate_live_semantics(
    c,
    producer,
    data: dict[str, Any],
    frozen: dict[str, Any],
    prefix_records: list[dict[str, Any]],
    all_records: list[dict[str, Any]],
    additions: dict[str, list[dict[str, Any]]],
) -> None:
    expected_suffixes, reconstructed_records = producer.validate_merged(
        c, data, frozen, prefix_records, additions
    )
    require(
        len(reconstructed_records) == len(all_records)
        and {
            record["id"]: record for record in reconstructed_records
        }
        == {
            record["id"]: record for record in all_records
        },
        "live records differ semantically from exact reconstructed records",
    )
    for name in c.FILES:
        live = (BACKEND / name).read_bytes()
        prefix_size = c.PREFIX[name][1]
        require(
            live[prefix_size:] == expected_suffixes[name],
            f"{name}: suffix changed during semantic validation",
        )

    by_id = {record["id"]: record for record in all_records}
    generic = c.load_generic()
    generic.validate_shapes(all_records)
    generic.validate_references(all_records, by_id)
    generic.validate_artifact_manifests(all_records, c.LANE)

    suffix_ids = {
        name: {record["id"] for record in additions[name]}
        for name in c.FILES
    }
    for name in c.FILES:
        prefix_size = c.PREFIX[name][1]
        suffix_records = parse_canonical_records(
            c, f"{name}:suffix-recheck", (BACKEND / name).read_bytes()[prefix_size:]
        ) if c.DELTA[name] else []
        require(
            [record["id"] for record in suffix_records]
                == sorted(suffix_ids[name])
            and {record["id"] for record in suffix_records} == suffix_ids[name],
            f"{name}: suffix ID order/set mismatch",
        )

    unit_ids = {
        record["source_local_id"]
        for record in additions["units.jsonl"]
    }
    segment_ids = {
        record["source_local_id"]
        for record in additions["segments.jsonl"]
    }
    reader_ids = {node["id"] for node in data["nodes"]}
    require(
        unit_ids == segment_ids == reader_ids and len(reader_ids) == 95,
        "one-to-one reader/unit/segment closure mismatch",
    )
    require(
        len(additions["corrections.jsonl"]) == 31
        and len(additions["relations.jsonl"]) == 34
        and len(additions["artifacts.jsonl"]) == 5,
        "correction/relation/artifact suffix census mismatch",
    )

    for artifact in additions["artifacts.jsonl"]:
        relative = artifact.get("path")
        require(
            relative in producer.EVIDENCE_PATHS,
            f"artifact uses an unbound evidence path: {relative!r}",
        )
        raw = (LANE / relative).read_bytes()
        require(
            (artifact.get("bytes"), artifact.get("sha256"))
                == (len(raw), c.digest(raw)),
            f"artifact bytes changed after evidence freeze: {artifact['id']}",
        )


def main() -> int:
    require(not sys.argv[1:], "validator accepts no write or replacement modes")
    producer = load_producer()
    c = producer.load_common()
    frozen = producer.freeze_evidence(c)
    data = c.verify_all_inputs(frozen["identities"])
    producer.validate_evidence(c, data, frozen)
    additions = c.build_additions(data, frozen["identities"])
    producer.validate_record_plan(c, frozen, additions)
    expected_suffixes = {
        name: b"".join(c.canon(record) for record in additions[name])
        for name in c.FILES
    }
    require(
        sum(len(records) for records in additions.values()) == 282,
        "common module did not reconstruct exactly 282 suffix records",
    )

    prefix_records, all_records, files, final = load_exact_partition(
        c, expected_suffixes
    )
    validate_live_semantics(
        c, producer, data, frozen, prefix_records, all_records, additions
    )

    # Evidence must remain byte-identical through the complete read-only pass.
    for relative, expected in frozen["identities"].items():
        c.require_identity(relative, expected)
    refreshed_data = c.verify_all_inputs(frozen["identities"])
    producer.validate_evidence(c, refreshed_data, frozen)
    refreshed_additions = c.build_additions(
        refreshed_data, frozen["identities"]
    )
    producer.validate_record_plan(c, frozen, refreshed_additions)
    refreshed_suffixes = {
        name: b"".join(c.canon(record) for record in refreshed_additions[name])
        for name in c.FILES
    }
    for name in c.FILES:
        prefix_size = c.PREFIX[name][1]
        require(
            (BACKEND / name).read_bytes()[prefix_size:] == refreshed_suffixes[name],
            f"{name}: live suffix/evidence binding changed during validation",
        )

    print("Fomberg Unit 002 append-only backend validation: PASS")
    print(f"prefix_records={c.PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={c.PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={c.PREFIX_TOTAL[2]}")
    print(f"records_added={sum(c.DELTA.values())}")
    print(f"cumulative_records={final[0]}")
    print(f"cumulative_bytes={final[1]}")
    print(f"backend_bundle_sha256={final[2]}")
    for name in c.FILES:
        result = files[name]
        print(
            f"{name}: records={result['final_records']} "
            f"bytes={result['final_bytes']} sha256={result['final_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
