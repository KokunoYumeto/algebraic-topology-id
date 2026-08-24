#!/usr/bin/env python3
"""Validate the cumulative Units 001--028 source/semantic backend."""
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
PREFIX_TOTAL = (4264, 4532994,
                "09aa16e8d9387171445c4d465d00a5399e39517a210cb347e30d2d285c703f8c")
FINAL_TOTAL = (4425, 4765453,
               "3a7492ee9755c85e89139bd6af84121747caa85f1f6421c7ec2e133b010a0b9f")
DELTA = {"artifacts.jsonl": 3, "assets.jsonl": 1, "authority.jsonl": 0,
         "concepts.jsonl": 6, "corrections.jsonl": 17, "qa.jsonl": 3,
         "relations.jsonl": 27, "rights.jsonl": 3, "segments.jsonl": 47,
         "terms.jsonl": 6, "units.jsonl": 48}
MANIFEST = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_028_FILE_MANIFEST.csv"
MANIFEST_IDENTITY = (2103,
                     "92dfb7100b71c3a1c4f1f010406f32e8b27a4ce0f05c228293ecc649238b470f")
SEMANTIC_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_028_RECEIPT.json"
SEMANTIC_RECEIPT_IDENTITY = (7168,
                            "175c8781189c94f026f9a793aaebcc70de2ac43cef0bb53e14e338b9e2cf84a0")
SEMANTIC_HUMAN = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_028_RECEIPT.md"
SEMANTIC_HUMAN_IDENTITY = (1705,
                          "d874b22bf6beb75879722a576a720850ad7a943e6ce6ea102e7ca90bb3261fe9")
CUMULATIVE_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_028_CUMULATIVE_RECEIPT.json"
CUMULATIVE_HUMAN = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_028_CUMULATIVE_RECEIPT.md"
CUMULATIVE_HUMAN_IDENTITY = (1083,
                            "2c8ed486291520bde6c3cfa4b3a7b663f35b9ec31431f7526e7eaa8d0c5d65bf")
PRODUCER = LANE / "scripts/extend-backend-unit-028.py"
PRODUCER_IDENTITY = (45781,
                     "f0aa78d1655112eaf9384371bcf49ebb25fb19ec8d772d56b2ce409e0cd9e0a2")
SEMANTIC_VALIDATOR = LANE / "scripts/validate-backend-append-only-unit-028.py"
SEMANTIC_VALIDATOR_IDENTITY = (22577,
                               "b433a22502644c01b959cb1ad69ae22f0f9977fef83eee3882c66dc3a3f7aa29")
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
        raise SystemExit("Unit 28 manifest shape mismatch")
    if [row["path"] for row in rows] != [f"backend/{name}" for name in FILES]:
        raise SystemExit("Unit 28 manifest path order mismatch")
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
            raise SystemExit(f"Unit 28 manifest/live mismatch: {name}")
        pr += int(row["prefix_records"]); pbytes += n
        fr += int(row["final_records"]); fbytes += len(live)
        pb.update(name.encode()); pb.update(b"\0"); pb.update(prefix)
        fb.update(name.encode()); fb.update(b"\0"); fb.update(live)
    if (pr, pbytes, pb.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("Unit 28 prefix bundle mismatch")
    if (fr, fbytes, fb.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 28 final bundle mismatch")
    return rows


def verify_semantic_receipt(rows: list[dict[str, str]]) -> None:
    receipt = json.loads(identity(SEMANTIC_RECEIPT,
                                  SEMANTIC_RECEIPT_IDENTITY).decode("utf-8"))
    identity(SEMANTIC_HUMAN, SEMANTIC_HUMAN_IDENTITY)
    identity(PRODUCER, PRODUCER_IDENTITY)
    identity(SEMANTIC_VALIDATOR, SEMANTIC_VALIDATOR_IDENTITY)
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") != "O012-BACKEND-UNIT-028-SEMANTIC-APPEND-ONLY"
            or (receipt.get("immutability", {}).get("prefix_records"),
                receipt.get("immutability", {}).get("prefix_bytes"),
                receipt.get("immutability", {}).get("prefix_bundle_sha256")) != PREFIX_TOTAL
            or not receipt.get("immutability", {}).get("prefix_preserved_byte_for_byte")
            or receipt.get("append", {}).get("records_added") != 161
            or receipt.get("append", {}).get("records_by_file") != DELTA
            or (receipt.get("current", {}).get("total_records"),
                receipt.get("current", {}).get("total_bytes"),
                receipt.get("current", {}).get("bundle_sha256")) != FINAL_TOTAL
            or receipt.get("source", {}).get("stable_ids") != 47
            or receipt.get("source", {}).get("next_source_line") != 6053
            or receipt.get("closure", {}).get("proof_objects") != 4
            or receipt.get("closure", {}).get("mastery_triples") != 6
            or len(receipt.get("closure", {}).get("source_aliases", {})) != 1
            or len(receipt.get("closure", {}).get("resolved_pre_admission_findings", [])) != 6
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("Unit 28 semantic receipt content mismatch")
    files = receipt.get("current", {}).get("files", {})
    for name, row in zip(FILES, rows, strict=True):
        declared = files.get(name, {})
        if (declared.get("records"), declared.get("bytes"), declared.get("sha256")) != (
                int(row["final_records"]), int(row["final_bytes"]), row["final_sha256"]):
            raise SystemExit(f"Unit 28 receipt/manifest mismatch: {name}")


def verify_cumulative_receipt() -> None:
    receipt = json.loads(CUMULATIVE_RECEIPT.read_text(encoding="utf-8"))
    identity(CUMULATIVE_HUMAN, CUMULATIVE_HUMAN_IDENTITY)
    self_raw = Path(__file__).read_bytes()
    prefix = receipt.get("nested_immutability", {}).get("units_001_027_prefix", {})
    suffix = receipt.get("nested_immutability", {}).get("unit_028_semantic_suffix", {})
    current = receipt.get("current", {})
    semantic = receipt.get("validators", {}).get("semantic", {})
    cumulative = receipt.get("validators", {}).get("cumulative", {})
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") != "O012-BACKEND-UNITS-001-028-CUMULATIVE-SEMANTIC"
            or (prefix.get("records"), prefix.get("bytes"),
                prefix.get("bundle_sha256")) != PREFIX_TOTAL
            or not prefix.get("preserved_byte_for_byte")
            or suffix.get("records") != 161
            or suffix.get("records_by_file") != DELTA
            or (current.get("total_records"), current.get("total_bytes"),
                current.get("bundle_sha256")) != FINAL_TOTAL
            or current.get("stable_ids_in_unit_028") != 47
            or current.get("proof_objects_in_unit_028") != 4
            or current.get("mastery_solution_triples_in_unit_028") != 6
            or current.get("resolved_findings_in_unit_028") != 6
            or current.get("next_source_line") != 6053
            or semantic.get("sha256") != SEMANTIC_VALIDATOR_IDENTITY[1]
            or semantic.get("live_replay") != "PASS"
            or cumulative.get("bytes") != len(self_raw)
            or cumulative.get("lines") != len(self_raw.splitlines())
            or cumulative.get("sha256") != digest(self_raw)
            or cumulative.get("live_replay") != "PASS"
            or receipt.get("build_boundary", {}).get("unit_028_html_record")
            or receipt.get("build_boundary", {}).get("unit_028_pdf_record")
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("Unit 28 cumulative receipt content/self-binding mismatch")


def rerun_semantic() -> None:
    result = subprocess.run([sys.executable, "-B", str(SEMANTIC_VALIDATOR)], cwd=LANE,
                            capture_output=True, text=True, encoding="utf-8")
    if (result.returncode != 0
            or "Unit 028 semantic append-only backend validation: PASS" not in result.stdout
            or f"final_bundle_sha256={FINAL_TOTAL[2]}" not in result.stdout):
        raise SystemExit("Unit 28 semantic replay failed:\n" + result.stdout + result.stderr)


def reject_premature_build_claims() -> None:
    needles = (b"artifact:o012-units-001-028-html",
               b"artifact:o012-units-001-028-pdf",
               b"qa:o012-units-001-028-build", b"qa:o012-units-001-028-visual")
    combined = b"".join((BACKEND / name).read_bytes() for name in FILES)
    if any(needle in combined for needle in needles):
        raise SystemExit("premature Unit 28 build claim detected")


def main() -> int:
    rows = verify_manifest(); verify_semantic_receipt(rows)
    verify_cumulative_receipt(); rerun_semantic(); reject_premature_build_claims()
    print("Cumulative Units 001-028 semantic backend validation: PASS")
    print(f"unit27_prefix_records={PREFIX_TOTAL[0]}")
    print(f"unit27_prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"unit27_prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print("unit28_records_added=161")
    print(f"cumulative_records={FINAL_TOTAL[0]}")
    print(f"cumulative_bytes={FINAL_TOTAL[1]}")
    print(f"cumulative_bundle_sha256={FINAL_TOTAL[2]}")
    print("semantic_validator_replay=PASS")
    print("cumulative_html_pdf_claim=ABSENT_BY_DESIGN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
