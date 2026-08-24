#!/usr/bin/env python3
"""Validate and deterministically replay the final Units 001--029 semantic backend."""
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
PREFIX_TOTAL = (4425, 4765453,
                "3a7492ee9755c85e89139bd6af84121747caa85f1f6421c7ec2e133b010a0b9f")
FINAL_TOTAL = (4596, 5001266,
               "49c599010ebee2223225f643cd09a53bea882b8064024d5189e6e15f648195d8")
DELTA = {"artifacts.jsonl": 3, "assets.jsonl": 2, "authority.jsonl": 0,
         "concepts.jsonl": 7, "corrections.jsonl": 19, "qa.jsonl": 3,
         "relations.jsonl": 28, "rights.jsonl": 3, "segments.jsonl": 49,
         "terms.jsonl": 7, "units.jsonl": 50}
MANIFEST = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_029_FILE_MANIFEST.csv"
MANIFEST_IDENTITY = (2103,
                     "f12d5b3d858caa3ae3054340fc5f927acef5bcc496eeaef3371c438b83d7d268")
SEMANTIC_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_029_RECEIPT.json"
SEMANTIC_RECEIPT_IDENTITY = (7374,
                            "046ba58477e68fa97ef8e4d5747fa413ca8c955d069d7221534f98f34702468e")
SEMANTIC_HUMAN = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_029_RECEIPT.md"
SEMANTIC_HUMAN_IDENTITY = (1781,
                          "60ee61b3545644052c861967bb07caa6b86987002ded20773b02120be6fad35f")
CUMULATIVE_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_029_CUMULATIVE_RECEIPT.json"
CUMULATIVE_HUMAN = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_029_CUMULATIVE_RECEIPT.md"
CUMULATIVE_HUMAN_IDENTITY = (1134,
                            "1ba6e9a5559a7c8c77fd175fc45fb31041233d909d5b9c458bf53da45f9ef3dc")
PRODUCER = LANE / "scripts/extend-backend-unit-029.py"
PRODUCER_IDENTITY = (47084,
                     "ccdcc364e439913cdce93ee9205ebc6e2883d5a55f7416940c9ee7a99c5874ad")
SEMANTIC_VALIDATOR = LANE / "scripts/validate-backend-append-only-unit-029.py"
SEMANTIC_VALIDATOR_IDENTITY = (23608,
                               "e0c01e51605c64dac3fc8a1abffa47e31783a89e0bd75611d9e80141fb1b3f4b")
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
        raise SystemExit("Unit 29 manifest shape mismatch")
    if [row["path"] for row in rows] != [f"backend/{name}" for name in FILES]:
        raise SystemExit("Unit 29 manifest path order mismatch")
    pb = hashlib.sha256(); fb = hashlib.sha256()
    pr = pbytes = fr = fbytes = 0
    for name, row in zip(FILES, rows, strict=True):
        live = (BACKEND / name).read_bytes(); n = int(row["prefix_bytes"])
        prefix = live[:n]
        if (digest(prefix) != row["prefix_sha256"]
                or len(prefix.splitlines()) != int(row["prefix_records"])
                or int(row["records_added"]) != DELTA[name]
                or len(live[n:].splitlines()) != DELTA[name]
                or len(live) != int(row["final_bytes"])
                or len(live.splitlines()) != int(row["final_records"])
                or digest(live) != row["final_sha256"]
                or row["prefix_preserved"] != "true"):
            raise SystemExit(f"Unit 29 manifest/live mismatch: {name}")
        pr += int(row["prefix_records"]); pbytes += n
        fr += int(row["final_records"]); fbytes += len(live)
        pb.update(name.encode()); pb.update(b"\0"); pb.update(prefix)
        fb.update(name.encode()); fb.update(b"\0"); fb.update(live)
    if (pr, pbytes, pb.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("Unit 29 prefix bundle mismatch")
    if (fr, fbytes, fb.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 29 final bundle mismatch")
    return rows


def verify_semantic_receipt(rows: list[dict[str, str]]) -> None:
    receipt = json.loads(identity(SEMANTIC_RECEIPT,
                                  SEMANTIC_RECEIPT_IDENTITY).decode("utf-8"))
    identity(SEMANTIC_HUMAN, SEMANTIC_HUMAN_IDENTITY)
    identity(PRODUCER, PRODUCER_IDENTITY)
    identity(SEMANTIC_VALIDATOR, SEMANTIC_VALIDATOR_IDENTITY)
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") != "O012-BACKEND-UNIT-029-SEMANTIC-APPEND-ONLY"
            or (receipt.get("immutability", {}).get("prefix_records"),
                receipt.get("immutability", {}).get("prefix_bytes"),
                receipt.get("immutability", {}).get("prefix_bundle_sha256")) != PREFIX_TOTAL
            or not receipt.get("immutability", {}).get("prefix_preserved_byte_for_byte")
            or receipt.get("append", {}).get("records_added") != 171
            or receipt.get("append", {}).get("records_by_file") != DELTA
            or (receipt.get("current", {}).get("total_records"),
                receipt.get("current", {}).get("total_bytes"),
                receipt.get("current", {}).get("bundle_sha256")) != FINAL_TOTAL
            or receipt.get("source", {}).get("stable_ids") != 49
            or receipt.get("source", {}).get("identified_headings") != 9
            or receipt.get("source", {}).get("next_source_line") != 6271
            or receipt.get("closure", {}).get("proof_objects") != 4
            or receipt.get("closure", {}).get("mastery_triples") != 6
            or receipt.get("closure", {}).get("source_diagrams_semantically_reflowed") != 5
            or len(receipt.get("closure", {}).get("source_aliases", {})) != 1
            or len(receipt.get("closure", {}).get("resolved_pre_admission_findings", [])) != 8
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("Unit 29 semantic receipt content mismatch")
    files = receipt.get("current", {}).get("files", {})
    for name, row in zip(FILES, rows, strict=True):
        declared = files.get(name, {})
        if (declared.get("records"), declared.get("bytes"), declared.get("sha256")) != (
                int(row["final_records"]), int(row["final_bytes"]), row["final_sha256"]):
            raise SystemExit(f"Unit 29 receipt/manifest mismatch: {name}")


def verify_cumulative_receipt() -> None:
    receipt = json.loads(CUMULATIVE_RECEIPT.read_text(encoding="utf-8"))
    identity(CUMULATIVE_HUMAN, CUMULATIVE_HUMAN_IDENTITY)
    self_raw = Path(__file__).read_bytes()
    prefix = receipt.get("nested_immutability", {}).get("units_001_028_prefix", {})
    suffix = receipt.get("nested_immutability", {}).get("unit_029_semantic_suffix", {})
    current = receipt.get("current", {})
    producer = receipt.get("validators", {}).get("producer", {})
    semantic = receipt.get("validators", {}).get("semantic", {})
    cumulative = receipt.get("validators", {}).get("cumulative", {})
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") != "O012-BACKEND-UNITS-001-029-CUMULATIVE-SEMANTIC"
            or (prefix.get("records"), prefix.get("bytes"),
                prefix.get("bundle_sha256")) != PREFIX_TOTAL
            or not prefix.get("preserved_byte_for_byte")
            or suffix.get("records") != 171
            or suffix.get("records_by_file") != DELTA
            or (current.get("total_records"), current.get("total_bytes"),
                current.get("bundle_sha256")) != FINAL_TOTAL
            or current.get("stable_ids_in_unit_029") != 49
            or current.get("proof_objects_in_unit_029") != 4
            or current.get("mastery_solution_triples_in_unit_029") != 6
            or current.get("source_diagrams_in_unit_029") != 5
            or current.get("resolved_findings_in_unit_029") != 8
            or current.get("next_source_line") != 6271
            or producer.get("sha256") != PRODUCER_IDENTITY[1]
            or producer.get("deterministic_replay") != "PASS"
            or semantic.get("sha256") != SEMANTIC_VALIDATOR_IDENTITY[1]
            or semantic.get("live_replay") != "PASS"
            or cumulative.get("bytes") != len(self_raw)
            or cumulative.get("lines") != len(self_raw.splitlines())
            or cumulative.get("sha256") != digest(self_raw)
            or cumulative.get("live_replay") != "PASS"
            or receipt.get("build_boundary", {}).get("unit_029_html_record")
            or receipt.get("build_boundary", {}).get("unit_029_pdf_record")
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("Unit 29 cumulative receipt content/self-binding mismatch")


def replay_producer(rows: list[dict[str, str]]) -> None:
    spec = importlib.util.spec_from_file_location("o012_u029_replay", PRODUCER)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load Unit 29 producer for replay")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix="o012-u029-replay-") as temp:
        stage = Path(temp)
        for name, row in zip(FILES, rows, strict=True):
            live = (BACKEND / name).read_bytes()
            (stage / name).write_bytes(live[:int(row["prefix_bytes"])])
        module.BACKEND = stage
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            result = module.main()
        if (result != 0
                or "Unit 029 semantic backend extension: PASS" not in captured.getvalue()
                or f"backend_bundle_sha256={FINAL_TOTAL[2]}" not in captured.getvalue()):
            raise SystemExit("Unit 29 producer replay failed")
        for name in FILES:
            if (stage / name).read_bytes() != (BACKEND / name).read_bytes():
                raise SystemExit(f"Unit 29 producer replay diverged: {name}")


def rerun_semantic() -> None:
    result = subprocess.run([sys.executable, "-B", str(SEMANTIC_VALIDATOR)], cwd=LANE,
                            capture_output=True, text=True, encoding="utf-8")
    if (result.returncode != 0
            or "Unit 029 semantic append-only backend validation: PASS" not in result.stdout
            or f"final_bundle_sha256={FINAL_TOTAL[2]}" not in result.stdout):
        raise SystemExit("Unit 29 semantic replay failed:\n" + result.stdout + result.stderr)


def reject_premature_build_claims() -> None:
    needles = (b"artifact:o012-units-001-029-html",
               b"artifact:o012-units-001-029-pdf",
               b"qa:o012-units-001-029-build", b"qa:o012-units-001-029-visual")
    combined = b"".join((BACKEND / name).read_bytes() for name in FILES)
    if any(needle in combined for needle in needles):
        raise SystemExit("premature Unit 29 build claim detected")


def main() -> int:
    rows = verify_manifest(); verify_semantic_receipt(rows)
    verify_cumulative_receipt(); replay_producer(rows); rerun_semantic()
    reject_premature_build_claims()
    print("Cumulative Units 001-029 semantic backend validation: PASS")
    print(f"unit28_prefix_records={PREFIX_TOTAL[0]}")
    print(f"unit28_prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"unit28_prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print("unit29_records_added=171")
    print(f"cumulative_records={FINAL_TOTAL[0]}")
    print(f"cumulative_bytes={FINAL_TOTAL[1]}")
    print(f"cumulative_bundle_sha256={FINAL_TOTAL[2]}")
    print("producer_deterministic_replay=PASS")
    print("semantic_validator_replay=PASS")
    print("cumulative_html_pdf_claim=ABSENT_BY_DESIGN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
