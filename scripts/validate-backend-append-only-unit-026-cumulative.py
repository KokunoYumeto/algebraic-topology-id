#!/usr/bin/env python3
"""Validate the cumulative Units 001--026 semantic backend boundary.

The Unit 26 transaction has no separately admitted HTML/PDF suffix.  This
validator therefore seals the cumulative source/semantic boundary: it checks
the exact live bundle, proves every file's Units 001--025 prefix from the CSV
manifest, binds the semantic receipt and transaction scripts, reruns the deep
semantic validator, and rejects any premature Unit 26 cumulative build claim.
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX_TOTAL = (3913, 4007903,
                "8b50629f25c5fcbedb6d5547f8f7151c622aa90e04f71583008bd176058a4f78")
FINAL_TOTAL = (4105, 4305218,
               "89556c5fa2224820837fc8956b1a48797929f28bef013baf9a613e73e6cf28eb")
DELTA = {"artifacts.jsonl": 3, "assets.jsonl": 1, "authority.jsonl": 0,
         "concepts.jsonl": 8, "corrections.jsonl": 13, "qa.jsonl": 3,
         "relations.jsonl": 28, "rights.jsonl": 3, "segments.jsonl": 62,
         "terms.jsonl": 8, "units.jsonl": 63}
MANIFEST = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_026_FILE_MANIFEST.csv"
MANIFEST_IDENTITY = (2103,
                     "5bda6abedc855b54d681345b2083c1e6236c58f68a6ad11f3bba5285ac257662")
SEMANTIC_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_026_RECEIPT.json"
SEMANTIC_RECEIPT_IDENTITY = (7411,
                            "7fc3adea0bcafb1ebdfb1d14c6ff100ebe9766836a858111f072c0c7bf44eb72")
HUMAN_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_026_RECEIPT.md"
HUMAN_RECEIPT_IDENTITY = (2286,
                         "439283f0c9aad7dcc033a3f304f4e7426c18e3daf3c3a058cdfbb058860cb9f3")
CUMULATIVE_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_026_CUMULATIVE_RECEIPT.json"
CUMULATIVE_HUMAN_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_026_CUMULATIVE_RECEIPT.md"
CUMULATIVE_HUMAN_IDENTITY = (1446,
                            "1db73285d941800056f8beacc56f16ede7931d57411c120628dfce2abb7104c5")
PRODUCER = LANE / "scripts/extend-backend-unit-026.py"
PRODUCER_IDENTITY = (44620,
                     "a43f8a68707f112c27e6504a9724788c761b9cceaf7c0a174ff185c8fa9534b5")
SEMANTIC_VALIDATOR = LANE / "scripts/validate-backend-append-only-unit-026.py"
SEMANTIC_VALIDATOR_IDENTITY = (20887,
                               "58fab216c7c7aa09c4f4fd12ea4c56147ea15d9ef018f371580eceb026effd89")
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
    expected_header = ["path", "prefix_records", "prefix_bytes", "prefix_sha256",
                       "records_added", "final_records", "final_bytes",
                       "final_sha256", "prefix_preserved"]
    if len(rows) != 11 or list(rows[0]) != expected_header:
        raise SystemExit("Unit 26 backend manifest shape mismatch")
    if [row["path"] for row in rows] != [f"backend/{name}" for name in FILES]:
        raise SystemExit("Unit 26 backend manifest path order mismatch")
    prefix_bundle = hashlib.sha256()
    final_bundle = hashlib.sha256()
    prefix_records = prefix_bytes_total = final_records = final_bytes_total = 0
    for name, row in zip(FILES, rows, strict=True):
        live = (BACKEND / name).read_bytes()
        prefix_bytes = int(row["prefix_bytes"])
        prefix = live[:prefix_bytes]
        if (digest(prefix) != row["prefix_sha256"]
                or len(prefix.splitlines()) != int(row["prefix_records"])
                or int(row["records_added"]) != DELTA[name]
                or len(live) != int(row["final_bytes"])
                or len(live.splitlines()) != int(row["final_records"])
                or digest(live) != row["final_sha256"]
                or row["prefix_preserved"] != "true"):
            raise SystemExit(f"Unit 26 manifest/live mismatch: {name}")
        suffix_lines = live[prefix_bytes:].splitlines()
        if len(suffix_lines) != DELTA[name]:
            raise SystemExit(f"Unit 26 suffix-count mismatch: {name}")
        prefix_records += int(row["prefix_records"])
        prefix_bytes_total += prefix_bytes
        final_records += int(row["final_records"])
        final_bytes_total += len(live)
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        final_bundle.update(name.encode()); final_bundle.update(b"\0"); final_bundle.update(live)
    if (prefix_records, prefix_bytes_total, prefix_bundle.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("Unit 26 cumulative prefix bundle mismatch")
    if (final_records, final_bytes_total, final_bundle.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 26 cumulative live bundle mismatch")
    return rows


def verify_receipt(rows: list[dict[str, str]]) -> None:
    receipt = json.loads(identity(SEMANTIC_RECEIPT,
                                  SEMANTIC_RECEIPT_IDENTITY).decode("utf-8"))
    identity(HUMAN_RECEIPT, HUMAN_RECEIPT_IDENTITY)
    identity(PRODUCER, PRODUCER_IDENTITY)
    identity(SEMANTIC_VALIDATOR, SEMANTIC_VALIDATOR_IDENTITY)
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") != "O012-BACKEND-UNIT-026-SEMANTIC-APPEND-ONLY"
            or receipt.get("immutability", {}).get("prefix_records") != PREFIX_TOTAL[0]
            or receipt.get("immutability", {}).get("prefix_bytes") != PREFIX_TOTAL[1]
            or receipt.get("immutability", {}).get("prefix_bundle_sha256") != PREFIX_TOTAL[2]
            or not receipt.get("immutability", {}).get("prefix_preserved_byte_for_byte")
            or receipt.get("append", {}).get("records_added") != 192
            or receipt.get("append", {}).get("records_by_file") != DELTA
            or receipt.get("current", {}).get("total_records") != FINAL_TOTAL[0]
            or receipt.get("current", {}).get("total_bytes") != FINAL_TOTAL[1]
            or receipt.get("current", {}).get("bundle_sha256") != FINAL_TOTAL[2]
            or receipt.get("source", {}).get("stable_ids") != 62
            or receipt.get("source", {}).get("next_source_line") != 5824
            or receipt.get("closure", {}).get("proof_objects") != 9
            or receipt.get("closure", {}).get("mastery_triples") != 6
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("Unit 26 semantic receipt content mismatch")
    files = receipt.get("current", {}).get("files", {})
    for name, row in zip(FILES, rows, strict=True):
        declared = files.get(name, {})
        if (declared.get("records"), declared.get("bytes"), declared.get("sha256")) != (
                int(row["final_records"]), int(row["final_bytes"]), row["final_sha256"]):
            raise SystemExit(f"Unit 26 receipt/manifest mismatch: {name}")
    if receipt.get("file_manifest", {}).get("sha256") != MANIFEST_IDENTITY[1]:
        raise SystemExit("Unit 26 receipt does not bind the manifest")


def verify_cumulative_receipt() -> None:
    receipt = json.loads(CUMULATIVE_RECEIPT.read_text(encoding="utf-8"))
    identity(CUMULATIVE_HUMAN_RECEIPT, CUMULATIVE_HUMAN_IDENTITY)
    self_raw = Path(__file__).read_bytes()
    validators = receipt.get("validators", {})
    cumulative = validators.get("cumulative", {})
    semantic = validators.get("semantic", {})
    current = receipt.get("current", {})
    prefix = receipt.get("nested_immutability", {}).get(
        "units_001_025_cumulative_prefix", {})
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") !=
            "O012-BACKEND-UNITS-001-026-CUMULATIVE-SEMANTIC"
            or (prefix.get("records"), prefix.get("bytes"),
                prefix.get("bundle_sha256")) != PREFIX_TOTAL
            or not prefix.get("preserved_byte_for_byte")
            or (current.get("total_records"), current.get("total_bytes"),
                current.get("bundle_sha256")) != FINAL_TOTAL
            or semantic.get("sha256") != SEMANTIC_VALIDATOR_IDENTITY[1]
            or semantic.get("live_replay") != "PASS"
            or cumulative.get("bytes") != len(self_raw)
            or cumulative.get("lines") != len(self_raw.splitlines())
            or cumulative.get("sha256") != digest(self_raw)
            or cumulative.get("live_replay") != "PASS"
            or receipt.get("build_boundary", {}).get("unit_026_html_record")
            or receipt.get("build_boundary", {}).get("unit_026_pdf_record")
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("Unit 26 cumulative receipt content/self-binding mismatch")


def rerun_semantic_validator() -> None:
    result = subprocess.run([sys.executable, str(SEMANTIC_VALIDATOR)], cwd=LANE,
                            capture_output=True, text=True, encoding="utf-8")
    if (result.returncode != 0
            or "Unit 026 semantic append-only backend validation: PASS" not in result.stdout
            or f"final_bundle_sha256={FINAL_TOTAL[2]}" not in result.stdout):
        raise SystemExit("Unit 26 semantic validator replay failed:\n" +
                         result.stdout + result.stderr)


def reject_premature_build_claims() -> None:
    needles = (b"artifact:o012-units-001-026-html",
               b"artifact:o012-units-001-026-pdf",
               b"qa:o012-units-001-026-build",
               b"qa:o012-units-001-026-visual")
    combined = b"".join((BACKEND / name).read_bytes() for name in FILES)
    if any(needle in combined for needle in needles):
        raise SystemExit("premature Unit 26 cumulative HTML/PDF claim detected")


def main() -> int:
    rows = verify_manifest()
    verify_receipt(rows)
    verify_cumulative_receipt()
    rerun_semantic_validator()
    reject_premature_build_claims()
    print("Cumulative Units 001-026 semantic backend validation: PASS")
    print(f"unit25_cumulative_prefix_records={PREFIX_TOTAL[0]}")
    print(f"unit25_cumulative_prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"unit25_cumulative_prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print("unit26_records_added=192")
    print(f"cumulative_records={FINAL_TOTAL[0]}")
    print(f"cumulative_bytes={FINAL_TOTAL[1]}")
    print(f"cumulative_bundle_sha256={FINAL_TOTAL[2]}")
    print("semantic_validator_replay=PASS")
    print("cumulative_html_pdf_claim=ABSENT_BY_DESIGN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
