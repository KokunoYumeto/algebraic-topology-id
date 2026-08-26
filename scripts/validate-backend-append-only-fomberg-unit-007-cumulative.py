#!/usr/bin/env python3
"""Replay Unit 007 and write deterministic semantic/cumulative receipts."""
from __future__ import annotations

import contextlib
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
PRODUCER_PATH = LANE / "scripts/extend-backend-fomberg-unit-007.py"
VALIDATOR_PATH = LANE / "scripts/validate-backend-append-only-fomberg-unit-007.py"
OUTPUTS = {
    "manifest": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_007_FILE_MANIFEST.csv",
    "semantic_json": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_007_RECEIPT.json",
    "semantic_md": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_007_RECEIPT.md",
    "cumulative_json": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_007_CUMULATIVE_RECEIPT.json",
    "cumulative_md": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_007_CUMULATIVE_RECEIPT.md",
    "replay_json": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_007_REPLAY_RECEIPT.json",
}
ROBERTS_BOUNDARY = (
    4761, 5213679,
    "51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920",
)
PRIOR_FOMBERG_STABLE_IDS = 531


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Fomberg Unit 007 cumulative validator FAIL: {message}")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def pretty(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"


def backend_snapshot(c) -> tuple[list[dict[str, Any]], tuple[int, int, str]]:
    rows: list[dict[str, Any]] = []
    bundle = hashlib.sha256(); records = total_bytes = 0
    for name in c.FILES:
        raw = (BACKEND / name).read_bytes(); count = len(raw.splitlines())
        rows.append({"filename": name, "records": count, "bytes": len(raw), "sha256": digest(raw)})
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
        records += count; total_bytes += len(raw)
    return rows, (records, total_bytes, bundle.hexdigest())


def replay_producer(producer, c) -> tuple[int, int, str]:
    with tempfile.TemporaryDirectory(prefix="o012-fom-u007-backend-replay-") as temporary:
        stage = Path(temporary)
        for name in c.FILES:
            raw = (BACKEND / name).read_bytes()
            (stage / name).write_bytes(raw[:c.PREFIX[name][1]])
        old_backend = producer.BACKEND; old_argv = list(sys.argv)
        producer.BACKEND = stage; sys.argv = [str(PRODUCER_PATH)]
        captured = io.StringIO()
        try:
            with contextlib.redirect_stdout(captured):
                result = producer.main()
        finally:
            producer.BACKEND = old_backend; sys.argv = old_argv
        require(result == 0, "producer replay returned nonzero")
        require("Fomberg Unit 007 semantic backend extension: PASS" in captured.getvalue(), "producer replay PASS marker absent")
        bundle = hashlib.sha256(); records = total_bytes = 0
        for name in c.FILES:
            replay = (stage / name).read_bytes(); live = (BACKEND / name).read_bytes()
            require(replay == live, f"producer replay diverged: {name}")
            records += len(replay.splitlines()); total_bytes += len(replay)
            bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(replay)
        return records, total_bytes, bundle.hexdigest()


def write_outputs(c, identities, additions, rows, final, script_results) -> None:
    counts = c.delta(additions)
    header = [
        "path", "prefix_records", "prefix_bytes", "prefix_sha256",
        "records_added", "final_records", "final_bytes", "final_sha256",
        "prefix_preserved", "suffix_exact",
    ]
    manifest_buffer = io.StringIO(newline="")
    writer = csv.DictWriter(manifest_buffer, fieldnames=header, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        name = row["filename"]
        writer.writerow({
            "path": f"backend/{name}", "prefix_records": c.PREFIX[name][0],
            "prefix_bytes": c.PREFIX[name][1], "prefix_sha256": c.PREFIX[name][2],
            "records_added": counts[name], "final_records": row["records"],
            "final_bytes": row["bytes"], "final_sha256": row["sha256"],
            "prefix_preserved": "true", "suffix_exact": "true",
        })
    manifest_raw = manifest_buffer.getvalue().encode("utf-8")
    OUTPUTS["manifest"].write_bytes(manifest_raw)

    backend_files = [
        {"filename": row["filename"], "records": row["records"], "bytes": row["bytes"], "sha256": row["sha256"]}
        for row in rows
    ]
    bound_inputs: dict[str, dict[str, Any]] = {}
    for key, path in (
        ("common", LANE / "scripts/fomberg-unit-007-common.py"),
        ("producer", PRODUCER_PATH),
        ("validator", VALIDATOR_PATH),
        ("cumulative_validator", Path(__file__)),
        ("generic_validator", LANE / "scripts/validate-backend.py"),
    ):
        raw = path.read_bytes()
        bound_inputs[key] = {"path": path.relative_to(LANE).as_posix(), "bytes": len(raw), "sha256": digest(raw)}
    for relative, expected in identities.items():
        raw = (LANE / relative).read_bytes()
        require((len(raw), digest(raw)) == expected, f"sealed input changed before receipt: {relative}")
        bound_inputs[relative] = {"path": relative, "bytes": len(raw), "sha256": digest(raw)}

    semantic_md = (
        "# Fomberg Unit 007 append-only backend receipt\n\n"
        "Status: **PASS**\n\n"
        f"- Immutable Unit 006 boundary: {c.PREFIX_TOTAL[0]:,} records / {c.PREFIX_TOTAL[1]:,} bytes / {c.PREFIX_TOTAL[2]}.\n"
        f"- Unit 007 semantic suffix: {sum(counts.values())} records, including {c.EXPECTED_STABLE_IDS} unit and {c.EXPECTED_STABLE_IDS} segment records.\n"
        f"- Current backend: {final[0]:,} records / {final[1]:,} bytes / {final[2]}.\n"
        "- Exact reconstruction, schema/reference checks, artifact binding, and independent producer replay: **PASS**.\n"
        f"- Reader: {c.EXPECTED_STABLE_IDS} stable IDs; seventeen source diagram functions; fourteen semantic displays; six paired redraw asset files; mastery: six solved triples.\n"
        "- Closed proof repairs: FOM-PR-13 through FOM-PR-15. Cursor: source line 4186; source EOF: false.\n"
    ).encode("utf-8")
    OUTPUTS["semantic_md"].write_bytes(semantic_md)
    semantic = {
        "schema_version": "1.0.0",
        "receipt_id": "O012-BACKEND-FOMBERG-UNIT-007-SEMANTIC-APPEND-ONLY",
        "status": "PASS", "model_provenance": c.MODEL,
        "immutability": {
            "prefix_records": c.PREFIX_TOTAL[0], "prefix_bytes": c.PREFIX_TOTAL[1],
            "prefix_bundle_sha256": c.PREFIX_TOTAL[2], "prefix_preserved_byte_for_byte": True,
        },
        "append": {"records": sum(counts.values()), "records_by_file": counts},
        "current": {
            "total_records": final[0], "total_bytes": final[1],
            "bundle_sha256": final[2], "backend_files": backend_files,
        },
        "closure": {
            "stable_ids": c.EXPECTED_STABLE_IDS, "unit_records": c.EXPECTED_STABLE_IDS,
            "segment_records": c.EXPECTED_STABLE_IDS,
            "source_diagram_functions": 17, "semantic_figure_blocks": 14,
            "redraw_files": 6, "mastery_triples": 6,
            "proof_repairs": ["FOM-PR-13", "FOM-PR-14", "FOM-PR-15"], "next_source_line": 4186,
            "terminal_source_eof": False,
            "review_counts": {"P1": 0, "P2": 0, "P3": 0},
        },
        "validation": script_results, "bound_inputs": bound_inputs,
        "file_manifest": {
            "path": OUTPUTS["manifest"].relative_to(LANE).as_posix(),
            "bytes": len(manifest_raw), "sha256": digest(manifest_raw),
        },
        "human_receipt": {
            "path": OUTPUTS["semantic_md"].relative_to(LANE).as_posix(),
            "bytes": len(semantic_md), "sha256": digest(semantic_md),
        },
    }
    semantic_raw = pretty(semantic); OUTPUTS["semantic_json"].write_bytes(semantic_raw)

    cumulative_md = (
        "# Cumulative backend receipt through Fomberg Unit 007\n\n"
        "Status: **PASS**\n\n"
        f"- Preserved Fomberg Unit 006 boundary: {c.PREFIX_TOTAL[0]:,} records / {c.PREFIX_TOTAL[1]:,} bytes / {c.PREFIX_TOTAL[2]}.\n"
        f"- Fomberg Unit 007 append-only suffix: {sum(counts.values())} records.\n"
        f"- Cumulative backend: {final[0]:,} records / {final[1]:,} bytes / {final[2]}.\n"
        f"- Fomberg Units 001–007: {PRIOR_FOMBERG_STABLE_IDS + c.EXPECTED_STABLE_IDS} stable reader IDs mirrored one-to-one as unit and segment records; 101 source diagram functions; 84 semantic figure blocks; 43 solved mastery triples.\n"
        "- Closed proof repairs remain FOM-PR-01 through FOM-PR-15. Cursor: source line 4186; source EOF: false.\n"
        "- Deterministic producer replay and semantic append-only validation: **PASS**.\n"
    ).encode("utf-8")
    OUTPUTS["cumulative_md"].write_bytes(cumulative_md)
    cumulative = {
        "schema_version": "1.0.0",
        "receipt_id": "O012-BACKEND-THROUGH-FOMBERG-UNIT-007-CUMULATIVE-SEMANTIC",
        "status": "PASS",
        "scope": "Roberts Units 001-030 immutable prefix plus Fomberg Units 001-007 append-only semantic suffixes",
        "model_provenance": c.MODEL,
        "nested_immutability": {
            "roberts_units_001_030_prefix": {
                "records": ROBERTS_BOUNDARY[0], "bytes": ROBERTS_BOUNDARY[1],
                "bundle_sha256": ROBERTS_BOUNDARY[2], "preserved_by_published_nested_receipts": True,
            },
            "fomberg_unit_005_boundary": {
                "records": c.PREFIX_TOTAL[0], "bytes": c.PREFIX_TOTAL[1],
                "bundle_sha256": c.PREFIX_TOTAL[2], "preserved_byte_for_byte": True,
            },
            "fomberg_unit_007_suffix": {"records": sum(counts.values()), "records_by_file": counts},
        },
        "current": {
            "total_records": final[0], "total_bytes": final[1],
            "bundle_sha256": final[2], "backend_files": backend_files,
            "stable_ids": PRIOR_FOMBERG_STABLE_IDS + c.EXPECTED_STABLE_IDS,
            "unit_records": PRIOR_FOMBERG_STABLE_IDS + c.EXPECTED_STABLE_IDS,
            "segment_records": PRIOR_FOMBERG_STABLE_IDS + c.EXPECTED_STABLE_IDS,
            "source_diagram_functions": 101, "semantic_figure_blocks": 84,
            "redraw_files": 46, "mastery_triples": 43,
            "proof_repairs_closed": [f"FOM-PR-{number:02d}" for number in range(1, 16)],
            "next_source_line": 4186, "terminal_source_eof": False,
            "review_counts": {"P1": 0, "P2": 0, "P3": 0},
        },
        "replay": script_results, "bound_inputs": bound_inputs,
        "semantic_receipt": {
            "path": OUTPUTS["semantic_json"].relative_to(LANE).as_posix(),
            "bytes": len(semantic_raw), "sha256": digest(semantic_raw),
        },
        "human_receipt": {
            "path": OUTPUTS["cumulative_md"].relative_to(LANE).as_posix(),
            "bytes": len(cumulative_md), "sha256": digest(cumulative_md),
        },
    }
    cumulative_raw = pretty(cumulative); OUTPUTS["cumulative_json"].write_bytes(cumulative_raw)
    replay = {
        "schema_version": "1.0.0",
        "receipt_id": "O012-BACKEND-FOMBERG-UNIT-007-DETERMINISTIC-REPLAY",
        "status": "PASS",
        "backend": {"records": final[0], "bytes": final[1], "bundle_sha256": final[2]},
        "checks": script_results,
        "outputs": {
            key: {"path": path.relative_to(LANE).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path.read_bytes())}
            for key, path in OUTPUTS.items() if key != "replay_json"
        },
    }
    OUTPUTS["replay_json"].write_bytes(pretty(replay))
    for path in OUTPUTS.values():
        require(path.is_file() and path.stat().st_size > 0, f"receipt output missing/empty: {path.name}")
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    require(not sys.argv[1:], "cumulative validator accepts no modes")
    producer = load(PRODUCER_PATH, "o012_fomberg_u007_producer_cumulative")
    c = producer.load_common(); identities = c.discover_identities()
    data = c.verify_all_inputs(identities); additions = c.build_additions(data)
    counts = c.delta(additions)
    result = subprocess.run(
        [sys.executable, "-B", str(VALIDATOR_PATH)], cwd=LANE,
        capture_output=True, text=True, encoding="utf-8",
    )
    require(result.returncode == 0, "semantic validator failed:\n" + result.stdout + result.stderr)
    require("Fomberg Unit 007 append-only backend validation: PASS" in result.stdout, "semantic validator PASS marker absent")
    rows, final = backend_snapshot(c)
    require(final[0] == c.PREFIX_TOTAL[0] + sum(counts.values()), "unexpected final record total")
    replay = replay_producer(producer, c)
    require(replay == final, "producer replay bundle differs from live backend")
    script_results = {
        "semantic_validator": "PASS", "producer_deterministic": "PASS",
        "generic_schema_and_references": "PASS", "exact_record_plan": "PASS",
        "every_backend_file_byte_identical": True,
    }
    write_outputs(c, identities, additions, rows, final, script_results)
    print("Cumulative backend validation through Fomberg Unit 007: PASS")
    print(f"unit006_prefix_records={c.PREFIX_TOTAL[0]}")
    print(f"unit007_records_added={sum(counts.values())}")
    print(f"cumulative_records={final[0]}")
    print(f"cumulative_bytes={final[1]}")
    print(f"cumulative_bundle_sha256={final[2]}")
    print("semantic_validator=PASS")
    print("producer_deterministic_replay=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
