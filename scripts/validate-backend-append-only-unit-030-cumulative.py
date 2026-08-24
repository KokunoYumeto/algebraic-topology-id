#!/usr/bin/env python3
"""Validate and deterministically replay the final Units 001--030 semantic backend."""
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

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX_TOTAL = (4596, 5001266,
                "49c599010ebee2223225f643cd09a53bea882b8064024d5189e6e15f648195d8")
FINAL_TOTAL = (4761, 5213679,
               "51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920")
DELTA = {"artifacts.jsonl": 3, "assets.jsonl": 2, "authority.jsonl": 0,
         "concepts.jsonl": 10, "corrections.jsonl": 10, "qa.jsonl": 3,
         "relations.jsonl": 29, "rights.jsonl": 3, "segments.jsonl": 47,
         "terms.jsonl": 10, "units.jsonl": 48}
MANIFEST = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_030_FILE_MANIFEST.csv"
MANIFEST_IDENTITY = (2105,
                     "c6cdf74c7a63d3cb399b527f28c5e6fa4822bb207a96c5d1584e8314e3f912b8")
SEMANTIC_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_030_RECEIPT.json"
SEMANTIC_RECEIPT_IDENTITY = (7808,
                            "407811c2483c3b5e5dfeda13436029394bbb086ab8337841eda3a476e22387f4")
SEMANTIC_HUMAN = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_030_RECEIPT.md"
SEMANTIC_HUMAN_IDENTITY = (2033,
                          "2b9b5255e44d9843fdf12ccac346dabf4a0db4485075736dc0f8178c3a5f3216")
CUMULATIVE_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.json"
CUMULATIVE_HUMAN = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.md"
CUMULATIVE_HUMAN_IDENTITY = (1323,
                            "de5a6d0456fa5c43a3171b362f9b01e6ed4464414527cc3f0c55264899f18c5d")
PRODUCER = LANE / "scripts/extend-backend-unit-030.py"
PRODUCER_IDENTITY = (46866,
                     "c9a0e2fee2616cab1f34e881ca69e40802dbf354128eed652dc99dc8cfddcb3c")
SEMANTIC_VALIDATOR = LANE / "scripts/validate-backend-append-only-unit-030.py"
SEMANTIC_VALIDATOR_IDENTITY = (27928,
                               "1e4244e4765cf0f5c248b14d88dfcc7d5b63d73858ef833a3f17c77d4c76e4b0")
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity(path: Path, expected: tuple[int, str]) -> bytes:
    raw = path.read_bytes()
    if (len(raw), digest(raw)) != expected:
        raise SystemExit(f"identity mismatch: {path.relative_to(LANE).as_posix()}")
    return raw


def verify_manifest() -> list[dict[str, str]]:
    raw = identity(MANIFEST, MANIFEST_IDENTITY)
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    header = ["path", "prefix_records", "prefix_bytes", "prefix_sha256",
              "records_added", "final_records", "final_bytes", "final_sha256",
              "prefix_preserved"]
    if len(rows) != 11 or list(rows[0]) != header:
        raise SystemExit("Unit 30 manifest shape mismatch")
    if [row["path"] for row in rows] != [f"backend/{name}" for name in FILES]:
        raise SystemExit("Unit 30 manifest path order mismatch")
    prefix_bundle = hashlib.sha256(); final_bundle = hashlib.sha256()
    prefix_records = prefix_bytes = final_records = final_bytes = 0
    for name, row in zip(FILES, rows, strict=True):
        live = (BACKEND / name).read_bytes(); boundary = int(row["prefix_bytes"])
        prefix = live[:boundary]
        if (digest(prefix) != row["prefix_sha256"]
                or len(prefix.splitlines()) != int(row["prefix_records"])
                or int(row["records_added"]) != DELTA[name]
                or len(live[boundary:].splitlines()) != DELTA[name]
                or len(live) != int(row["final_bytes"])
                or len(live.splitlines()) != int(row["final_records"])
                or digest(live) != row["final_sha256"]
                or row["prefix_preserved"] != "true"):
            raise SystemExit(f"Unit 30 manifest/live mismatch: {name}")
        prefix_records += int(row["prefix_records"]); prefix_bytes += boundary
        final_records += int(row["final_records"]); final_bytes += len(live)
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        final_bundle.update(name.encode()); final_bundle.update(b"\0"); final_bundle.update(live)
    if (prefix_records, prefix_bytes, prefix_bundle.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("Unit 30 prefix bundle mismatch")
    if (final_records, final_bytes, final_bundle.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 30 final bundle mismatch")
    return rows


def verify_semantic_receipt(rows: list[dict[str, str]]) -> None:
    receipt = json.loads(identity(SEMANTIC_RECEIPT,
                                  SEMANTIC_RECEIPT_IDENTITY).decode("utf-8"))
    identity(SEMANTIC_HUMAN, SEMANTIC_HUMAN_IDENTITY)
    identity(PRODUCER, PRODUCER_IDENTITY)
    identity(SEMANTIC_VALIDATOR, SEMANTIC_VALIDATOR_IDENTITY)
    source = receipt.get("source", {})
    closure = receipt.get("closure", {})
    controls = receipt.get("controls", {})
    evidence = receipt.get("evidence", {})
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") != "O012-BACKEND-UNIT-030-SEMANTIC-APPEND-ONLY"
            or (receipt.get("immutability", {}).get("prefix_records"),
                receipt.get("immutability", {}).get("prefix_bytes"),
                receipt.get("immutability", {}).get("prefix_bundle_sha256")) != PREFIX_TOTAL
            or not receipt.get("immutability", {}).get("prefix_preserved_byte_for_byte")
            or receipt.get("append", {}).get("records_added") != 165
            or receipt.get("append", {}).get("records_by_file") != DELTA
            or (receipt.get("current", {}).get("total_records"),
                receipt.get("current", {}).get("total_bytes"),
                receipt.get("current", {}).get("bundle_sha256")) != FINAL_TOTAL
            or source.get("stable_ids") != 47
            or source.get("identified_headings") != 7
            or source.get("fenced_semantic_objects") != 40
            or source.get("terminal_source_eof") is not True
            or source.get("next_source_line") != 6369
            or closure.get("proof_objects") != 4
            or closure.get("mastery_triples") != 6
            or closure.get("source_diagrams_semantically_reflowed") != 1
            or len(closure.get("source_aliases", {})) != 1
            or len(closure.get("resolved_pre_admission_findings", [])) != 2
            or controls.get("adverse_ledger", {}).get("through") != "O012-ADV-0407"
            or controls.get("terminology", {}).get("through") != "O012-TERM-0365"
            or evidence.get("qa", {}).get("sha256")
                != "bef6fe6704084ac02386bb477b7b0082e02921d3d722955e1366e7d0b9247753"
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("Unit 30 semantic receipt content mismatch")
    files = receipt.get("current", {}).get("files", {})
    for name, row in zip(FILES, rows, strict=True):
        declared = files.get(name, {})
        if (declared.get("records"), declared.get("bytes"), declared.get("sha256")) != (
                int(row["final_records"]), int(row["final_bytes"]), row["final_sha256"]):
            raise SystemExit(f"Unit 30 receipt/manifest mismatch: {name}")


def verify_cumulative_receipt() -> None:
    receipt = json.loads(CUMULATIVE_RECEIPT.read_text(encoding="utf-8"))
    identity(CUMULATIVE_HUMAN, CUMULATIVE_HUMAN_IDENTITY)
    self_raw = Path(__file__).read_bytes()
    prefix = receipt.get("nested_immutability", {}).get("units_001_029_prefix", {})
    suffix = receipt.get("nested_immutability", {}).get("unit_030_semantic_suffix", {})
    current = receipt.get("current", {})
    producer = receipt.get("validators", {}).get("producer", {})
    semantic = receipt.get("validators", {}).get("semantic", {})
    cumulative = receipt.get("validators", {}).get("cumulative", {})
    manifest = receipt.get("file_manifest", {})
    human = receipt.get("human_receipt", {})
    transaction = receipt.get("semantic_transaction", {})
    scope = receipt.get("scope", "")
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") != "O012-BACKEND-UNITS-001-030-CUMULATIVE-SEMANTIC"
            or "001-030" not in scope
            or (transaction.get("path"), transaction.get("bytes"),
                transaction.get("sha256")) != (
                    "qa/BACKEND_APPEND_ONLY_UNIT_030_RECEIPT.json",
                    *SEMANTIC_RECEIPT_IDENTITY)
            or (prefix.get("records"), prefix.get("bytes"),
                prefix.get("bundle_sha256")) != PREFIX_TOTAL
            or not prefix.get("preserved_byte_for_byte")
            or suffix.get("records") != 165
            or suffix.get("records_by_file") != DELTA
            or (current.get("total_records"), current.get("total_bytes"),
                current.get("bundle_sha256")) != FINAL_TOTAL
            or current.get("stable_ids_in_unit_030") != 47
            or current.get("proof_objects_in_unit_030") != 4
            or current.get("mastery_solution_triples_in_unit_030") != 6
            or current.get("source_diagrams_in_unit_030") != 1
            or current.get("resolved_findings_in_unit_030") != 2
            or current.get("terminal_source_eof") is not True
            or current.get("next_source_line") != 6369
            or producer.get("sha256") != PRODUCER_IDENTITY[1]
            or producer.get("deterministic_replay") != "PASS"
            or semantic.get("sha256") != SEMANTIC_VALIDATOR_IDENTITY[1]
            or semantic.get("live_replay") != "PASS"
            or cumulative.get("bytes") != len(self_raw)
            or cumulative.get("lines") != len(self_raw.splitlines())
            or cumulative.get("sha256") != digest(self_raw)
            or cumulative.get("live_replay") != "PASS"
            or (manifest.get("path"), manifest.get("bytes"), manifest.get("sha256")) != (
                "qa/BACKEND_APPEND_ONLY_UNIT_030_FILE_MANIFEST.csv", *MANIFEST_IDENTITY)
            or (human.get("path"), human.get("bytes"), human.get("sha256")) != (
                "qa/BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.md",
                *CUMULATIVE_HUMAN_IDENTITY)
            or receipt.get("build_boundary", {}).get("unit_030_html_record")
            or receipt.get("build_boundary", {}).get("unit_030_pdf_record")
            or receipt.get("build_boundary", {}).get("unit_030_build_qa_record")
            or receipt.get("build_boundary", {}).get("unit_030_visual_qa_record")
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("Unit 30 cumulative receipt content/self-binding mismatch")


def replay_producer(rows: list[dict[str, str]]) -> None:
    spec = importlib.util.spec_from_file_location("o012_u030_replay", PRODUCER)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load Unit 30 producer for replay")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix="o012-u030-replay-") as temp:
        stage = Path(temp)
        for name, row in zip(FILES, rows, strict=True):
            live = (BACKEND / name).read_bytes()
            (stage / name).write_bytes(live[:int(row["prefix_bytes"])])
        module.BACKEND = stage
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            result = module.main()
        if (result != 0
                or "Unit 030 semantic backend extension: PASS" not in captured.getvalue()
                or f"backend_bundle_sha256={FINAL_TOTAL[2]}" not in captured.getvalue()):
            raise SystemExit("Unit 30 producer replay failed")
        for name in FILES:
            if (stage / name).read_bytes() != (BACKEND / name).read_bytes():
                raise SystemExit(f"Unit 30 producer replay diverged: {name}")


def rerun_semantic() -> None:
    result = subprocess.run([sys.executable, "-B", str(SEMANTIC_VALIDATOR)], cwd=LANE,
                            capture_output=True, text=True, encoding="utf-8")
    if (result.returncode != 0
            or "Unit 030 semantic append-only backend validation: PASS" not in result.stdout
            or f"final_bundle_sha256={FINAL_TOTAL[2]}" not in result.stdout):
        raise SystemExit("Unit 30 semantic replay failed:\n" + result.stdout + result.stderr)


def reject_premature_build_claims() -> None:
    needles = (b"artifact:o012-units-001-030-html",
               b"artifact:o012-units-001-030-pdf",
               b"qa:o012-units-001-030-build", b"qa:o012-units-001-030-visual")
    combined = b"".join((BACKEND / name).read_bytes() for name in FILES)
    if any(needle in combined for needle in needles):
        raise SystemExit("premature Unit 30 build claim detected")


def main() -> int:
    rows = verify_manifest(); verify_semantic_receipt(rows)
    verify_cumulative_receipt(); replay_producer(rows); rerun_semantic()
    reject_premature_build_claims()
    print("Cumulative Units 001-030 semantic backend validation: PASS")
    print(f"unit29_prefix_records={PREFIX_TOTAL[0]}")
    print(f"unit29_prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"unit29_prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print("unit30_records_added=165")
    print(f"cumulative_records={FINAL_TOTAL[0]}")
    print(f"cumulative_bytes={FINAL_TOTAL[1]}")
    print(f"cumulative_bundle_sha256={FINAL_TOTAL[2]}")
    print("producer_deterministic_replay=PASS")
    print("semantic_validator_replay=PASS")
    print("terminal_source_eof=true")
    print("next_source_line=6369")
    print("cumulative_html_pdf_claim=ABSENT_BY_DESIGN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
