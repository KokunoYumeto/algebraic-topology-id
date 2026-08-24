#!/usr/bin/env python3
"""Validate and deterministically replay the cumulative Fomberg Unit 001 backend."""
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
PREFIX_TOTAL = (4761, 5213679, "51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920")
FINAL_TOTAL = (5060, 5658648, "17f57575a062025e434e79f7f3797d05de1a41e520202521ae39a409d4b6450d")
DELTA = {"artifacts.jsonl": 6, "assets.jsonl": 3, "authority.jsonl": 2,
         "concepts.jsonl": 28, "corrections.jsonl": 18, "qa.jsonl": 4,
         "relations.jsonl": 31, "rights.jsonl": 5, "segments.jsonl": 87,
         "terms.jsonl": 28, "units.jsonl": 87}
PATHS = {
    "common": ("scripts/fomberg-unit-001-common.py", 39866, "f0743dfabccff457a5e48dfdc5969ee581ff859e85a54485d079a936a71a46b8"),
    "qa_script": ("scripts/qa-fomberg-unit-001.py", 6189, "9273df48dcf579f0ff9c9c9d0db921a160b938b9e64d806064449d3f48bb94d4"),
    "producer": ("scripts/extend-backend-fomberg-unit-001.py", 10214, "5893666483f88a27e53dcd576add31c8266bca78d5b9f1c0b12ce2725bb53155"),
    "semantic_validator": ("scripts/validate-backend-append-only-fomberg-unit-001.py", 23735, "742241eddaf47e70e33b693fc58f5694b91688d2297aa1a6016822e2c6a60417"),
    "qa": ("qa/FOMBERG_UNIT_001_QA.json", 21253, "b3b0ebc9430b80d45c64a6c528e0e36f46ca0d646a50e7b9c9c5d68285369b7a"),
    "manifest": ("qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_FILE_MANIFEST.csv", 2105, "f06bd66e47dfce8d8aaad470568579e30a3d193ea045c94bc84e9b3efa42961e"),
    "semantic_receipt": ("qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_RECEIPT.json", 4704, "6b116c6615a721f097809ed8fc1a2bce485ea912ead5770983ba906bb2533cc7"),
    "semantic_human": ("qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_RECEIPT.md", 772, "fc6494e2f0be479caec16278537331e14a2b59fbf2e11ff5e45802c2b60c03b1"),
}
CUMULATIVE = LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_CUMULATIVE_RECEIPT.json"
CUMULATIVE_HUMAN = LANE / "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_CUMULATIVE_RECEIPT.md"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def bound(name: str) -> bytes:
    relative, size, sha = PATHS[name]; raw = (LANE / relative).read_bytes()
    if (len(raw), digest(raw)) != (size, sha):
        raise SystemExit(f"bound identity mismatch: {relative}")
    return raw


def verify_manifest() -> list[dict[str, str]]:
    raw = bound("manifest")
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    expected_header = ["path", "prefix_records", "prefix_bytes", "prefix_sha256",
                       "records_added", "final_records", "final_bytes", "final_sha256",
                       "prefix_preserved"]
    if len(rows) != 11 or list(rows[0]) != expected_header:
        raise SystemExit("file manifest shape mismatch")
    pb = hashlib.sha256(); fb = hashlib.sha256(); pr = pbytes = fr = fbytes = 0
    for name, row in zip(FILES, rows, strict=True):
        if row["path"] != f"backend/{name}":
            raise SystemExit("manifest path order mismatch")
        live = (BACKEND / name).read_bytes(); boundary = int(row["prefix_bytes"]); prefix = live[:boundary]
        if (len(prefix.splitlines()) != int(row["prefix_records"])
                or digest(prefix) != row["prefix_sha256"]
                or int(row["records_added"]) != DELTA[name]
                or len(live[boundary:].splitlines()) != DELTA[name]
                or len(live.splitlines()) != int(row["final_records"])
                or len(live) != int(row["final_bytes"])
                or digest(live) != row["final_sha256"]
                or row["prefix_preserved"] != "true"):
            raise SystemExit(f"manifest/live mismatch: {name}")
        pb.update(name.encode()); pb.update(b"\0"); pb.update(prefix)
        fb.update(name.encode()); fb.update(b"\0"); fb.update(live)
        pr += int(row["prefix_records"]); pbytes += boundary
        fr += int(row["final_records"]); fbytes += len(live)
    if (pr, pbytes, pb.hexdigest()) != PREFIX_TOTAL or (fr, fbytes, fb.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("manifest bundle totals mismatch")
    return rows


def verify_semantic_receipt() -> None:
    receipt = json.loads(bound("semantic_receipt").decode("utf-8")); bound("semantic_human")
    if (receipt.get("status") != "PASS"
            or receipt.get("receipt_id") != "O012-BACKEND-FOMBERG-UNIT-001-SEMANTIC-APPEND-ONLY"
            or (receipt.get("immutability", {}).get("prefix_records"),
                receipt.get("immutability", {}).get("prefix_bytes"),
                receipt.get("immutability", {}).get("prefix_bundle_sha256")) != PREFIX_TOTAL
            or not receipt.get("immutability", {}).get("prefix_preserved_byte_for_byte")
            or receipt.get("append", {}).get("records_by_file") != DELTA
            or (receipt.get("current", {}).get("total_records"),
                receipt.get("current", {}).get("total_bytes"),
                receipt.get("current", {}).get("bundle_sha256")) != FINAL_TOTAL
            or receipt.get("source", {}).get("stable_ids") != 87
            or receipt.get("source", {}).get("next_source_line") != 615
            or receipt.get("source", {}).get("terminal_source_eof") is not False
            or receipt.get("closure", {}).get("unit_records") != 87
            or receipt.get("closure", {}).get("segment_records") != 87
            or receipt.get("closure", {}).get("source_diagrams") != 14
            or receipt.get("closure", {}).get("semantic_figure_blocks") != 10
            or receipt.get("closure", {}).get("mastery_triples") != 6
            or receipt.get("closure", {}).get("proof_repair") != "FOM-U001-PR-001"
            or receipt.get("closure", {}).get("review_final_counts") != {"P1": 0, "P2": 0, "P3": 0}
            or receipt.get("model_provenance") != MODEL):
        raise SystemExit("semantic receipt content mismatch")


def rerun_qa() -> None:
    script = LANE / PATHS["qa_script"][0]
    result = subprocess.run([sys.executable, "-B", str(script)], cwd=LANE,
                            capture_output=True, text=True, encoding="utf-8")
    if result.returncode or "Fomberg Unit 001 static QA: PASS" not in result.stdout:
        raise SystemExit("static QA deterministic replay failed:\n" + result.stdout + result.stderr)
    bound("qa")


def replay_producer(rows: list[dict[str, str]]) -> None:
    producer_path = LANE / PATHS["producer"][0]
    spec = importlib.util.spec_from_file_location("o012_fom_u001_replay", producer_path)
    if spec is None or spec.loader is None: raise SystemExit("cannot load producer for replay")
    producer = importlib.util.module_from_spec(spec); spec.loader.exec_module(producer)
    with tempfile.TemporaryDirectory(prefix="o012-fom-u001-replay-") as temp:
        stage = Path(temp)
        for name, row in zip(FILES, rows, strict=True):
            live = (BACKEND / name).read_bytes()
            (stage / name).write_bytes(live[:int(row["prefix_bytes"])])
        producer.BACKEND = stage
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            result = producer.main()
        if (result != 0 or "Fomberg Unit 001 semantic backend extension: PASS" not in captured.getvalue()
                or f"backend_bundle_sha256={FINAL_TOTAL[2]}" not in captured.getvalue()):
            raise SystemExit("producer deterministic replay failed")
        for name in FILES:
            if (stage / name).read_bytes() != (BACKEND / name).read_bytes():
                raise SystemExit(f"producer replay diverged: {name}")


def rerun_semantic() -> None:
    script = LANE / PATHS["semantic_validator"][0]
    result = subprocess.run([sys.executable, "-B", str(script)], cwd=LANE,
                            capture_output=True, text=True, encoding="utf-8")
    if (result.returncode or "Fomberg Unit 001 semantic append-only backend validation: PASS" not in result.stdout
            or f"final_bundle_sha256={FINAL_TOTAL[2]}" not in result.stdout):
        raise SystemExit("semantic validator replay failed:\n" + result.stdout + result.stderr)
    bound("manifest"); bound("semantic_receipt"); bound("semantic_human")


def reject_premature_claims() -> None:
    suffix = b""
    rows = verify_manifest()
    for name, row in zip(FILES, rows, strict=True):
        raw = (BACKEND / name).read_bytes(); suffix += raw[int(row["prefix_bytes"]):]
    needles = (b"published", b"fomberg-unit-001-html", b"fomberg-unit-001-pdf",
               b"FOM-PR-01", b"FOM-PR-08", b"C:\\Users")
    if any(needle in suffix for needle in needles):
        raise SystemExit("premature build/publication/later-repair/private-path claim")


def write_cumulative_receipt() -> None:
    human = ("# Cumulative backend receipt through Fomberg Unit 001\n\n"
             "Status: **PASS**\n\n"
             f"- Immutable Roberts Units 001-030 prefix: {PREFIX_TOTAL[0]:,} records / {PREFIX_TOTAL[1]:,} bytes / `{PREFIX_TOTAL[2]}`.\n"
             f"- Fomberg Unit 001 semantic suffix: {sum(DELTA.values())} records.\n"
             f"- Cumulative backend: {FINAL_TOTAL[0]:,} records / {FINAL_TOTAL[1]:,} bytes / `{FINAL_TOTAL[2]}`.\n"
             "- Deterministic static-QA, producer, and semantic-validator replay: **PASS**.\n"
             "- Reader IDs: 87 unit/segment pairs; diagrams: 14 source diagrams in ten semantic blocks; mastery: six solved triples.\n"
             "- Review P1/P2/P3: 0/0/0. Cursor: source line 615; source EOF: false.\n"
             "- No HTML, PDF, release, publication, later-unit, or later-proof-repair claim is admitted.\n")
    human_raw = human.encode("utf-8"); CUMULATIVE_HUMAN.write_bytes(human_raw)
    script_raw = Path(__file__).read_bytes()
    receipt = {
        "schema_version": "1.0.0", "receipt_id": "O012-BACKEND-THROUGH-FOMBERG-UNIT-001-CUMULATIVE-SEMANTIC",
        "status": "PASS", "scope": "Roberts Units 001-030 immutable prefix plus Fomberg Unit 001 semantic suffix",
        "nested_immutability": {
            "roberts_units_001_030_prefix": {"records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1],
                                             "bundle_sha256": PREFIX_TOTAL[2], "preserved_byte_for_byte": True},
            "fomberg_unit_001_suffix": {"records": sum(DELTA.values()), "records_by_file": DELTA}},
        "current": {"total_records": FINAL_TOTAL[0], "total_bytes": FINAL_TOTAL[1],
                    "bundle_sha256": FINAL_TOTAL[2], "stable_ids": 87,
                    "unit_records": 87, "segment_records": 87, "source_diagrams": 14,
                    "semantic_figure_blocks": 10, "mastery_triples": 6,
                    "proof_repair": "FOM-U001-PR-001", "next_source_line": 615,
                    "terminal_source_eof": False, "review_counts": {"P1": 0, "P2": 0, "P3": 0}},
        "bound_inputs": {key: {"path": value[0], "bytes": value[1], "sha256": value[2]}
                         for key, value in PATHS.items()},
        "replay": {"static_qa": "PASS", "producer_deterministic": "PASS",
                   "semantic_validator": "PASS", "every_backend_file_byte_identical": True},
        "cumulative_validator": {"path": Path(__file__).relative_to(LANE).as_posix(),
                                 "bytes": len(script_raw), "lines": len(script_raw.splitlines()),
                                 "sha256": digest(script_raw)},
        "human_receipt": {"path": CUMULATIVE_HUMAN.relative_to(LANE).as_posix(),
                          "bytes": len(human_raw), "sha256": digest(human_raw)},
        "model_provenance": MODEL,
    }
    raw = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    CUMULATIVE.write_bytes(raw)
    reread = json.loads(CUMULATIVE.read_text(encoding="utf-8"))
    if (reread.get("status") != "PASS"
            or reread.get("current", {}).get("bundle_sha256") != FINAL_TOTAL[2]
            or reread.get("cumulative_validator", {}).get("sha256") != digest(script_raw)
            or reread.get("human_receipt", {}).get("sha256") != digest(human_raw)):
        raise SystemExit("generated cumulative receipt self-binding mismatch")


def main() -> int:
    for name in ("common", "qa_script", "producer", "semantic_validator", "qa",
                 "manifest", "semantic_receipt", "semantic_human"):
        bound(name)
    rows = verify_manifest(); verify_semantic_receipt(); rerun_qa()
    replay_producer(rows); rerun_semantic(); reject_premature_claims()
    write_cumulative_receipt()
    print("Cumulative backend validation through Fomberg Unit 001: PASS")
    print(f"roberts_prefix_records={PREFIX_TOTAL[0]}")
    print(f"fomberg_unit001_records_added={sum(DELTA.values())}")
    print(f"cumulative_records={FINAL_TOTAL[0]}")
    print(f"cumulative_bytes={FINAL_TOTAL[1]}")
    print(f"cumulative_bundle_sha256={FINAL_TOTAL[2]}")
    print("static_qa_replay=PASS")
    print("producer_deterministic_replay=PASS")
    print("semantic_validator_replay=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
