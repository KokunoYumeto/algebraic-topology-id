#!/usr/bin/env python3
"""Verify the bounded 2026-08-22 Indonesian terminology migration."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


LANE = Path(__file__).resolve().parent.parent
RECEIPT = LANE / "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-22.json"
MODEL_ID = "OpenAI Codex gpt-5.6-sol, Ultra"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise RuntimeError(message)


def main() -> int:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if receipt.get("validation_state") != "passed":
        fail("terminology receipt is not closed as passed")
    if receipt.get("model_provenance") != MODEL_ID:
        fail("exact model provenance is missing from the machine receipt")

    forbidden = {
        "funktor family": re.compile(r"funktor", re.IGNORECASE),
        "morfisme family": re.compile(r"morfisme", re.IGNORECASE),
        "bare lembar": re.compile(r"\blembar\b", re.IGNORECASE),
        "superseded evenly-covered form": re.compile(r"tertutup secara merata", re.IGNORECASE),
    }
    for item in receipt["source_files"]:
        path = LANE / item["path"]
        raw = path.read_bytes()
        if len(raw) != item["after_bytes"] or hashlib.sha256(raw).hexdigest() != item["after_sha256"]:
            fail(f"source byte identity mismatch: {item['path']}")
        if len(raw.splitlines()) != item["lines"]:
            fail(f"source line count mismatch: {item['path']}")
        text = raw.decode("utf-8")
        ids = set(re.findall(r"\{[^}\n]*#([A-Za-z0-9-]+)[^}\n]*\}", text))
        if len(ids) != item["stable_id_count"]:
            fail(f"stable-ID count mismatch: {item['path']}")
        for label, pattern in forbidden.items():
            if pattern.search(text):
                fail(f"{item['path']}: retained {label}")

    with (LANE / "00_control/TERMINOLOGY.csv").open(
        "r", encoding="utf-8", newline=""
    ) as stream:
        terms = {row["source_term"]: row for row in csv.DictReader(stream)}
    expected = {
        "functor": "fungtor",
        "functoriality": "fungtorialitas",
        "morphism": "morfisma",
        "evenly covered": "tertutup rata",
        "sheet (of a covering)": "lembaran",
        "neighbourhood": "lingkungan",
        "object": "objek",
    }
    for source_term, preferred in expected.items():
        if terms.get(source_term, {}).get("id_ID") != preferred:
            fail(f"terminology control mismatch for {source_term}")

    for relative in ("README.md", "ATTRIBUTION.md"):
        if MODEL_ID not in (LANE / relative).read_text(encoding="utf-8"):
            fail(f"exact model provenance missing from {relative}")

    for key in ("human_report", "migration_script", "verifier"):
        item = receipt[key]
        path = LANE / item["path"]
        if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            fail(f"{key} byte identity mismatch")

    validator = subprocess.run(
        [sys.executable, str(LANE / "scripts/validate-backend.py")],
        cwd=LANE,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )
    if validator.returncode != 0:
        fail("backend validator failed")
    match = re.search(r"backend_bundle_sha256: ([0-9a-f]{64})", validator.stdout)
    expected_bundle = receipt["validation"]["backend_bundle_sha256"]
    if match is None or match.group(1) != expected_bundle:
        fail("backend bundle hash differs from terminology receipt")

    witness = LANE / receipt["fallback_source"]["local_witness"]
    if witness.exists():
        if witness.stat().st_size != receipt["fallback_source"]["pdf_bytes"]:
            fail("local fallback PDF byte count mismatch")
        if sha256(witness) != receipt["fallback_source"]["pdf_sha256"]:
            fail("local fallback PDF hash mismatch")

    print("Indonesian terminology QA verification: PASS")
    print(f"source_files: {len(receipt['source_files'])}")
    print(f"backend_bundle_sha256: {expected_bundle}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Indonesian terminology QA verification: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
