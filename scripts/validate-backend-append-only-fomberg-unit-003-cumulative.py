#!/usr/bin/env python3
"""Replay Unit 003 and write deterministic semantic/cumulative backend receipts.

This script cannot pass before the exact Unit 003 suffix has been appended and
the common module's audit/QA identities have been armed.  It never changes the
backend.  Its only writes are the six declared QA manifest/receipt outputs.
"""
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
PRODUCER_PATH = LANE / "scripts/extend-backend-fomberg-unit-003.py"
VALIDATOR_PATH = LANE / "scripts/validate-backend-append-only-fomberg-unit-003.py"
OUTPUTS = {
    "manifest": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_003_FILE_MANIFEST.csv",
    "semantic_json": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_003_RECEIPT.json",
    "semantic_md": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_003_RECEIPT.md",
    "cumulative_json": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_003_CUMULATIVE_RECEIPT.json",
    "cumulative_md": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_003_CUMULATIVE_RECEIPT.md",
    "replay_json": LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_003_REPLAY_RECEIPT.json",
}
ROBERTS_BOUNDARY = (
    4761, 5213679,
    "51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920",
)
FOMBERG_UNIT_001_BOUNDARY = (
    5060, 5658648,
    "17f57575a062025e434e79f7f3797d05de1a41e520202521ae39a409d4b6450d",
)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Fomberg Unit 003 cumulative validator FAIL: {message}")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pretty(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"


def backend_snapshot(c) -> tuple[list[dict[str, Any]], tuple[int, int, str]]:
    rows: list[dict[str, Any]] = []
    bundle = hashlib.sha256()
    records = total_bytes = 0
    for name in c.FILES:
        raw = (BACKEND / name).read_bytes()
        count = len(raw.splitlines())
        rows.append({"filename": name, "records": count, "bytes": len(raw), "sha256": digest(raw)})
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
        records += count; total_bytes += len(raw)
    return rows, (records, total_bytes, bundle.hexdigest())


def replay_producer(producer, c) -> tuple[int, int, str]:
    with tempfile.TemporaryDirectory(prefix="o012-fom-u003-backend-replay-") as temporary:
        stage = Path(temporary)
        for name in c.FILES:
            raw = (BACKEND / name).read_bytes()
            (stage / name).write_bytes(raw[:c.PREFIX[name][1]])
        old_backend = producer.BACKEND
        old_argv = list(sys.argv)
        producer.BACKEND = stage
        sys.argv = [str(PRODUCER_PATH)]
        captured = io.StringIO()
        try:
            with contextlib.redirect_stdout(captured):
                result = producer.main()
        finally:
            producer.BACKEND = old_backend
            sys.argv = old_argv
        require(result == 0, "producer replay returned nonzero")
        require("Fomberg Unit 003 semantic backend extension: PASS" in captured.getvalue(), "producer replay PASS marker absent")
        bundle = hashlib.sha256(); records = total_bytes = 0
        for name in c.FILES:
            replay = (stage / name).read_bytes()
            live = (BACKEND / name).read_bytes()
            require(replay == live, f"producer replay diverged: {name}")
            records += len(replay.splitlines()); total_bytes += len(replay)
            bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(replay)
        return records, total_bytes, bundle.hexdigest()


def write_outputs(c, identities, rows, final, script_results) -> None:
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
            "path": f"backend/{name}",
            "prefix_records": c.PREFIX[name][0],
            "prefix_bytes": c.PREFIX[name][1],
            "prefix_sha256": c.PREFIX[name][2],
            "records_added": c.DELTA[name],
            "final_records": row["records"],
            "final_bytes": row["bytes"],
            "final_sha256": row["sha256"],
            "prefix_preserved": "true",
            "suffix_exact": "true",
        })
    manifest_raw = manifest_buffer.getvalue().encode("utf-8")
    OUTPUTS["manifest"].write_bytes(manifest_raw)

    backend_files = [
        {"filename": row["filename"], "records": row["records"], "bytes": row["bytes"], "sha256": row["sha256"]}
        for row in rows
    ]
    bound_inputs = {}
    for key, path in (
        ("common", LANE / "scripts/fomberg-unit-003-common.py"),
        ("producer", PRODUCER_PATH),
        ("validator", VALIDATOR_PATH),
        ("cumulative_validator", Path(__file__)),
    ):
        raw = path.read_bytes()
        bound_inputs[key] = {"path": path.relative_to(LANE).as_posix(), "bytes": len(raw), "sha256": digest(raw)}
    for relative, expected in identities.items():
        raw = (LANE / relative).read_bytes()
        require((len(raw), digest(raw)) == expected, f"sealed input changed before receipt: {relative}")
        bound_inputs[relative] = {"path": relative, "bytes": len(raw), "sha256": digest(raw)}

    semantic_md = (
        "# Fomberg Unit 003 append-only backend receipt\n\n"
        "Status: **PASS**\n\n"
        f"- Immutable Unit 002 boundary: {c.PREFIX_TOTAL[0]:,} records / {c.PREFIX_TOTAL[1]:,} bytes / `{c.PREFIX_TOTAL[2]}`.\n"
        f"- Unit 003 semantic suffix: {sum(c.DELTA.values())} records, including 125 unit and 125 segment records.\n"
        f"- Current backend: {final[0]:,} records / {final[1]:,} bytes / `{final[2]}`.\n"
        "- Exact reconstruction, generic schema/reference checks, artifact binding, and independent producer replay: **PASS**.\n"
        "- Reader: 125 stable IDs; source diagrams: 29; semantic figure blocks: 26; linked redraw files: 12; mastery: six solved triples.\n"
        "- FOM-PR-04 is complete. Cursor: source line 1923; source EOF: false.\n"
        "- The quotient-space long-exact-sequence forward obligation remains explicitly tracked for the excision unit; no later-unit or publication claim is made.\n"
    ).encode("utf-8")
    OUTPUTS["semantic_md"].write_bytes(semantic_md)
    semantic = {
        "schema_version": "1.0.0",
        "receipt_id": "O012-BACKEND-FOMBERG-UNIT-003-SEMANTIC-APPEND-ONLY",
        "status": "PASS",
        "model_provenance": c.MODEL,
        "immutability": {
            "prefix_records": c.PREFIX_TOTAL[0], "prefix_bytes": c.PREFIX_TOTAL[1],
            "prefix_bundle_sha256": c.PREFIX_TOTAL[2], "prefix_preserved_byte_for_byte": True,
        },
        "append": {"records": sum(c.DELTA.values()), "records_by_file": c.DELTA},
        "current": {"total_records": final[0], "total_bytes": final[1], "bundle_sha256": final[2], "backend_files": backend_files},
        "closure": {
            "stable_ids": 125, "unit_records": 125, "segment_records": 125,
            "source_diagrams": 29, "semantic_figure_blocks": 26,
            "redraw_files": 12, "mastery_triples": 6,
            "proof_repair": "FOM-PR-04", "next_source_line": 1923,
            "terminal_source_eof": False, "review_counts": {"P1": 0, "P2": 0, "P3": 0},
        },
        "validation": script_results,
        "bound_inputs": bound_inputs,
        "file_manifest": {"path": OUTPUTS["manifest"].relative_to(LANE).as_posix(), "bytes": len(manifest_raw), "sha256": digest(manifest_raw)},
        "human_receipt": {"path": OUTPUTS["semantic_md"].relative_to(LANE).as_posix(), "bytes": len(semantic_md), "sha256": digest(semantic_md)},
    }
    semantic_raw = pretty(semantic)
    OUTPUTS["semantic_json"].write_bytes(semantic_raw)

    cumulative_md = (
        "# Cumulative backend receipt through Fomberg Unit 003\n\n"
        "Status: **PASS**\n\n"
        f"- Preserved Fomberg Unit 002 boundary: {c.PREFIX_TOTAL[0]:,} records / {c.PREFIX_TOTAL[1]:,} bytes / `{c.PREFIX_TOTAL[2]}`.\n"
        f"- Fomberg Unit 003 append-only suffix: {sum(c.DELTA.values())} records.\n"
        f"- Cumulative backend: {final[0]:,} records / {final[1]:,} bytes / `{final[2]}`.\n"
        "- Fomberg Units 001–003: 307 stable reader IDs mirrored one-to-one as unit and segment records; 57 source diagrams; 50 semantic figure blocks; 18 solved mastery triples.\n"
        "- Closed proof repairs: FOM-PR-01 through FOM-PR-04. Cursor: source line 1923; source EOF: false.\n"
        "- Deterministic producer replay and semantic append-only validation: **PASS**.\n"
    ).encode("utf-8")
    OUTPUTS["cumulative_md"].write_bytes(cumulative_md)
    cumulative = {
        "schema_version": "1.0.0",
        "receipt_id": "O012-BACKEND-THROUGH-FOMBERG-UNIT-003-CUMULATIVE-SEMANTIC",
        "status": "PASS",
        "scope": "Roberts Units 001-030 immutable prefix plus Fomberg Units 001-003 append-only semantic suffixes",
        "model_provenance": c.MODEL,
        "nested_immutability": {
            "roberts_units_001_030_prefix": {
                "records": ROBERTS_BOUNDARY[0], "bytes": ROBERTS_BOUNDARY[1],
                "bundle_sha256": ROBERTS_BOUNDARY[2], "preserved_byte_for_byte": True,
            },
            "fomberg_unit_001_boundary": {
                "records": FOMBERG_UNIT_001_BOUNDARY[0], "bytes": FOMBERG_UNIT_001_BOUNDARY[1],
                "bundle_sha256": FOMBERG_UNIT_001_BOUNDARY[2], "preserved_byte_for_byte": True,
            },
            "fomberg_unit_002_boundary": {
                "records": c.PREFIX_TOTAL[0], "bytes": c.PREFIX_TOTAL[1],
                "bundle_sha256": c.PREFIX_TOTAL[2], "preserved_byte_for_byte": True,
            },
            "fomberg_unit_003_suffix": {"records": sum(c.DELTA.values()), "records_by_file": c.DELTA},
        },
        "current": {
            "total_records": final[0], "total_bytes": final[1], "bundle_sha256": final[2],
            "backend_files": backend_files, "stable_ids": 307,
            "unit_records": 307, "segment_records": 307,
            "source_diagrams": 57, "semantic_figure_blocks": 50,
            "redraw_files": 12, "mastery_triples": 18,
            "proof_repairs_closed": ["FOM-PR-01", "FOM-PR-02", "FOM-PR-03", "FOM-PR-04"],
            "next_source_line": 1923, "terminal_source_eof": False,
            "review_counts": {"P1": 0, "P2": 0, "P3": 0},
        },
        "replay": script_results,
        "bound_inputs": bound_inputs,
        "semantic_receipt": {"path": OUTPUTS["semantic_json"].relative_to(LANE).as_posix(), "bytes": len(semantic_raw), "sha256": digest(semantic_raw)},
        "human_receipt": {"path": OUTPUTS["cumulative_md"].relative_to(LANE).as_posix(), "bytes": len(cumulative_md), "sha256": digest(cumulative_md)},
    }
    cumulative_raw = pretty(cumulative)
    OUTPUTS["cumulative_json"].write_bytes(cumulative_raw)
    replay = {
        "schema_version": "1.0.0",
        "receipt_id": "O012-BACKEND-FOMBERG-UNIT-003-DETERMINISTIC-REPLAY",
        "status": "PASS",
        "backend": {"records": final[0], "bytes": final[1], "bundle_sha256": final[2]},
        "checks": script_results,
        "outputs": {
            key: {"path": path.relative_to(LANE).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path.read_bytes())}
            for key, path in OUTPUTS.items() if key != "replay_json"
        },
    }
    OUTPUTS["replay_json"].write_bytes(pretty(replay))

    # Exact readback of every declared output.
    for path in OUTPUTS.values():
        require(path.is_file() and path.stat().st_size > 0, f"receipt output missing/empty: {path.name}")
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    require(not sys.argv[1:], "cumulative validator accepts no modes")
    producer = load(PRODUCER_PATH, "o012_fomberg_u003_producer_cumulative")
    c = producer.load_common()
    identities = c.sealed_identities()
    # Run the independent semantic validator first; it is read-only.
    result = subprocess.run(
        [sys.executable, "-B", str(VALIDATOR_PATH)], cwd=LANE,
        capture_output=True, text=True, encoding="utf-8",
    )
    require(result.returncode == 0, "semantic validator failed:\n" + result.stdout + result.stderr)
    require("Fomberg Unit 003 append-only backend validation: PASS" in result.stdout, "semantic validator PASS marker absent")
    rows, final = backend_snapshot(c)
    require(final[0] == 5747, "unexpected final record total")
    replay = replay_producer(producer, c)
    require(replay == final, "producer replay bundle differs from live backend")
    script_results = {
        "semantic_validator": "PASS",
        "producer_deterministic": "PASS",
        "generic_schema_and_references": "PASS",
        "exact_record_plan": "PASS",
        "every_backend_file_byte_identical": True,
    }
    write_outputs(c, identities, rows, final, script_results)
    print("Cumulative backend validation through Fomberg Unit 003: PASS")
    print(f"unit002_prefix_records={c.PREFIX_TOTAL[0]}")
    print(f"unit003_records_added={sum(c.DELTA.values())}")
    print(f"cumulative_records={final[0]}")
    print(f"cumulative_bytes={final[1]}")
    print(f"cumulative_bundle_sha256={final[2]}")
    print("semantic_validator=PASS")
    print("producer_deterministic_replay=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
