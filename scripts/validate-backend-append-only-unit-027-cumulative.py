#!/usr/bin/env python3
"""Validate the cumulative Units 001--027 source/semantic backend."""
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
PREFIX_TOTAL = (4105, 4305218,
                "89556c5fa2224820837fc8956b1a48797929f28bef013baf9a613e73e6cf28eb")
FINAL_TOTAL = (4264, 4532994,
               "09aa16e8d9387171445c4d465d00a5399e39517a210cb347e30d2d285c703f8c")
DELTA = {"artifacts.jsonl": 3, "assets.jsonl": 1, "authority.jsonl": 0,
         "concepts.jsonl": 8, "corrections.jsonl": 16, "qa.jsonl": 3,
         "relations.jsonl": 24, "rights.jsonl": 3, "segments.jsonl": 46,
         "terms.jsonl": 8, "units.jsonl": 47}
MANIFEST = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_027_FILE_MANIFEST.csv"
MANIFEST_IDENTITY = (2103,
                     "ebb8ab35f6ea673b3865c834cf3d1c806deb58daf5cf6a702a8a7a9c77cc93e2")
SEMANTIC_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_027_RECEIPT.json"
SEMANTIC_RECEIPT_IDENTITY = (7708,
                            "c99b386e61bbcefeee5218767a332c6e958cfa0e73865470a08db9dc0ba270e1")
SEMANTIC_HUMAN = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_027_RECEIPT.md"
SEMANTIC_HUMAN_IDENTITY = (1980,
                          "0c95c1c012d093a22a7d1226bbd66b04e7ac5f7672877ea82be99f79b6d8fafe")
CUMULATIVE_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_027_CUMULATIVE_RECEIPT.json"
CUMULATIVE_HUMAN = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_027_CUMULATIVE_RECEIPT.md"
CUMULATIVE_HUMAN_IDENTITY = (1228,
                            "8d6470fae13573cefae93de047c84dd9b605a5dc30d864a0300efbfbf6740114")
PRODUCER = LANE / "scripts/extend-backend-unit-027.py"
PRODUCER_IDENTITY = (45032,
                     "5f3bfcb579d78680148f43d445f94ffe262d76b85d9f62aecaa570bb74520704")
SEMANTIC_VALIDATOR = LANE / "scripts/validate-backend-append-only-unit-027.py"
SEMANTIC_VALIDATOR_IDENTITY = (19658,
                               "179a24ecf31372e0968ed8331d3e014189797ea6bb91f9d4a63a249c836a975b")
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
        raise SystemExit("Unit 27 manifest shape mismatch")
    if [row["path"] for row in rows] != [f"backend/{name}" for name in FILES]:
        raise SystemExit("Unit 27 manifest path order mismatch")
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
            raise SystemExit(f"Unit 27 manifest/live mismatch: {name}")
        pr += int(row["prefix_records"]); pbytes += n
        fr += int(row["final_records"]); fbytes += len(live)
        pb.update(name.encode()); pb.update(b"\0"); pb.update(prefix)
        fb.update(name.encode()); fb.update(b"\0"); fb.update(live)
    if (pr, pbytes, pb.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("Unit 27 prefix bundle mismatch")
    if (fr, fbytes, fb.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 27 final bundle mismatch")
    return rows


def verify_semantic_receipt(rows: list[dict[str, str]]) -> None:
    receipt = json.loads(identity(SEMANTIC_RECEIPT,
                                  SEMANTIC_RECEIPT_IDENTITY).decode("utf-8"))
    identity(SEMANTIC_HUMAN, SEMANTIC_HUMAN_IDENTITY)
    identity(PRODUCER, PRODUCER_IDENTITY)
    identity(SEMANTIC_VALIDATOR, SEMANTIC_VALIDATOR_IDENTITY)
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") != "O012-BACKEND-UNIT-027-SEMANTIC-APPEND-ONLY"
            or (receipt.get("immutability", {}).get("prefix_records"),
                receipt.get("immutability", {}).get("prefix_bytes"),
                receipt.get("immutability", {}).get("prefix_bundle_sha256")) != PREFIX_TOTAL
            or not receipt.get("immutability", {}).get("prefix_preserved_byte_for_byte")
            or receipt.get("append", {}).get("records_added") != 159
            or receipt.get("append", {}).get("records_by_file") != DELTA
            or (receipt.get("current", {}).get("total_records"),
                receipt.get("current", {}).get("total_bytes"),
                receipt.get("current", {}).get("bundle_sha256")) != FINAL_TOTAL
            or receipt.get("source", {}).get("stable_ids") != 46
            or receipt.get("source", {}).get("next_source_line") != 5924
            or receipt.get("closure", {}).get("proof_objects") != 3
            or receipt.get("closure", {}).get("mastery_triples") != 6
            or len(receipt.get("closure", {}).get("source_aliases", {})) != 4
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("Unit 27 semantic receipt content mismatch")
    files = receipt.get("current", {}).get("files", {})
    for name, row in zip(FILES, rows, strict=True):
        declared = files.get(name, {})
        if (declared.get("records"), declared.get("bytes"), declared.get("sha256")) != (
                int(row["final_records"]), int(row["final_bytes"]), row["final_sha256"]):
            raise SystemExit(f"Unit 27 receipt/manifest mismatch: {name}")


def verify_cumulative_receipt() -> None:
    receipt = json.loads(CUMULATIVE_RECEIPT.read_text(encoding="utf-8"))
    identity(CUMULATIVE_HUMAN, CUMULATIVE_HUMAN_IDENTITY)
    self_raw = Path(__file__).read_bytes()
    prefix = receipt.get("nested_immutability", {}).get("units_001_026_prefix", {})
    current = receipt.get("current", {})
    semantic = receipt.get("validators", {}).get("semantic", {})
    cumulative = receipt.get("validators", {}).get("cumulative", {})
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") != "O012-BACKEND-UNITS-001-027-CUMULATIVE-SEMANTIC"
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
            or receipt.get("build_boundary", {}).get("unit_027_html_record")
            or receipt.get("build_boundary", {}).get("unit_027_pdf_record")
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("Unit 27 cumulative receipt content/self-binding mismatch")


def rerun_semantic() -> None:
    result = subprocess.run([sys.executable, str(SEMANTIC_VALIDATOR)], cwd=LANE,
                            capture_output=True, text=True, encoding="utf-8")
    if (result.returncode != 0
            or "Unit 027 semantic append-only backend validation: PASS" not in result.stdout
            or f"final_bundle_sha256={FINAL_TOTAL[2]}" not in result.stdout):
        raise SystemExit("Unit 27 semantic replay failed:\n" + result.stdout + result.stderr)


def reject_premature_build_claims() -> None:
    needles = (b"artifact:o012-units-001-027-html",
               b"artifact:o012-units-001-027-pdf",
               b"qa:o012-units-001-027-build", b"qa:o012-units-001-027-visual")
    combined = b"".join((BACKEND / name).read_bytes() for name in FILES)
    if any(needle in combined for needle in needles):
        raise SystemExit("premature Unit 27 build claim detected")


def main() -> int:
    rows = verify_manifest(); verify_semantic_receipt(rows)
    verify_cumulative_receipt(); rerun_semantic(); reject_premature_build_claims()
    print("Cumulative Units 001-027 semantic backend validation: PASS")
    print(f"unit26_prefix_records={PREFIX_TOTAL[0]}")
    print(f"unit26_prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"unit26_prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print("unit27_records_added=159")
    print(f"cumulative_records={FINAL_TOTAL[0]}")
    print(f"cumulative_bytes={FINAL_TOTAL[1]}")
    print(f"cumulative_bundle_sha256={FINAL_TOTAL[2]}")
    print("semantic_validator_replay=PASS")
    print("cumulative_html_pdf_claim=ABSENT_BY_DESIGN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
