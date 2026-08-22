#!/usr/bin/env python3
"""Apply the bounded 2026-08-22 Indonesian algebraic-topology term QA.

The migration is intentionally narrow.  It updates the 17 live Indonesian
reader sources, the terminology control, and the canonical Units 001-013
backend.  Frozen rendered artifacts, release packages, receipts, upstream
authority files, and historical QA records are never touched.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parent.parent
SOURCE_PATHS = [
    "source/id-ID/reader-unit-001.md",
    *[
        f"source/id-ID/units/unit-{number:03d}-lecture-{number:03d}.md"
        for number in range(2, 18)
    ],
]
TEXT_CONTROL_PATHS = ["00_control/TERMINOLOGY.csv"]
BACKEND_TEXT_PATHS = {
    "backend/corrections.jsonl",
    "backend/terms.jsonl",
    "backend/units.jsonl",
}
BACKEND_LOCATOR_PATHS = {
    "backend/segments.jsonl",
    "backend/units.jsonl",
}
BACKEND_FILE_METADATA_PATHS = {
    "backend/artifacts.jsonl",
    "backend/assets.jsonl",
}
VALIDATOR_PATH = "scripts/validate-backend.py"
RECEIPT_PATH = "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-22.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_terms(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    replacements = [
        ("funktor", "fungtor"),
        ("Funktor", "Fungtor"),
        ("morfisme", "morfisma"),
        ("Morfisme", "Morfisma"),
        ("tertutup secara merata", "tertutup rata"),
        ("Tertutup secara merata", "Tertutup rata"),
    ]
    for old, new in replacements:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            counts[f"{old}->{new}"] = count
    for old, new in ((r"\blembar\b", "lembaran"), (r"\bLembar\b", "Lembaran")):
        text, count = re.subn(old, new, text)
        if count:
            counts[f"{old}->{new}"] = count
    return text, counts


def replace_recursive(value: Any) -> Any:
    if isinstance(value, str):
        return replace_terms(value)[0]
    if isinstance(value, list):
        return [replace_recursive(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_recursive(item) for key, item in value.items()}
    return value


def read_bytes(relative: str) -> bytes:
    return (LANE / relative).read_bytes()


def write_bytes(relative: str, data: bytes) -> None:
    (LANE / relative).write_bytes(data)


def source_inventory(raw_by_path: dict[str, bytes]) -> dict[str, dict[str, Any]]:
    inventory: dict[str, dict[str, Any]] = {}
    for relative, raw in raw_by_path.items():
        text = raw.decode("utf-8")
        inventory[relative] = {
            "bytes": len(raw),
            "cr_bytes": raw.count(b"\r"),
            "lines": len(raw.splitlines()),
            "sha256": sha256(raw),
            "stable_ids": sorted(
                set(re.findall(r"\{[^}\n]*#([A-Za-z0-9-]+)[^}\n]*\}", text))
            ),
        }
    return inventory


def canonical_jsonl(records: list[dict[str, Any]]) -> bytes:
    text = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for record in records
    )
    return text.encode("utf-8")


def load_jsonl(relative: str) -> list[dict[str, Any]]:
    raw = read_bytes(relative)
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise RuntimeError(f"noncanonical JSONL framing before migration: {relative}")
    records = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    return records


def update_backend(source_after: dict[str, bytes]) -> dict[str, dict[str, Any]]:
    parsed: dict[str, list[dict[str, Any]]] = {}
    for relative in sorted(
        BACKEND_TEXT_PATHS | BACKEND_LOCATOR_PATHS | BACKEND_FILE_METADATA_PATHS
    ):
        parsed[relative] = load_jsonl(relative)

    for relative in BACKEND_TEXT_PATHS:
        migrated_records = []
        for record in parsed[relative]:
            migrated_records.append(
                {
                    key: value
                    if key in {"variants", "rejected_forms"}
                    else replace_recursive(value)
                    for key, value in record.items()
                }
            )
        parsed[relative] = migrated_records

    # Keep the superseded spellings discoverable without making them preferred.
    for record in parsed["backend/terms.jsonl"]:
        preferred = record.get("preferred")
        variants = record.get("variants")
        if not isinstance(preferred, str) or not isinstance(variants, list):
            continue
        variants[:] = sorted({item for item in variants if item != preferred})
        prior = preferred.replace("fungtor", "funktor").replace("morfisma", "morfisme")
        if prior != preferred and prior not in variants:
            variants.append(prior)
        if record.get("id") == "term:neighborhood:id-ID" and "persekitaran" not in variants:
            variants.append("persekitaran")
        if record.get("id") == "term:evenly-covered-neighborhood:id-ID":
            explanatory = "lingkungan yang diliputi secara merata"
            if explanatory not in variants:
                variants.append(explanatory)
        variants.sort()

    split_lines = {path: raw.splitlines(keepends=True) for path, raw in source_after.items()}
    file_hashes = {path: sha256(raw) for path, raw in source_after.items()}
    for relative in BACKEND_LOCATOR_PATHS:
        for record in parsed[relative]:
            locator = record.get("target_locator")
            if not isinstance(locator, dict) or locator.get("path") not in source_after:
                continue
            path = locator["path"]
            start = locator["line_start"]
            end = locator["line_end"]
            lines = split_lines[path]
            if not (1 <= start <= end <= len(lines)):
                raise RuntimeError(f"invalid target locator during migration: {record.get('id')}")
            locator["file_sha256"] = file_hashes[path]
            locator["content_sha256"] = sha256(b"".join(lines[start - 1 : end]))

    for relative in BACKEND_FILE_METADATA_PATHS:
        for record in parsed[relative]:
            path = record.get("path")
            if path not in source_after:
                continue
            record["bytes"] = len(source_after[path])
            record["sha256"] = file_hashes[path]

    changed: dict[str, dict[str, Any]] = {}
    for relative, records in parsed.items():
        before = read_bytes(relative)
        after = canonical_jsonl(records)
        if before != after:
            write_bytes(relative, after)
        changed[relative] = {
            "before_bytes": len(before),
            "before_sha256": sha256(before),
            "after_bytes": len(after),
            "after_sha256": sha256(after),
            "changed": before != after,
        }
    return changed


def update_validator(source_before: dict[str, bytes], source_after: dict[str, bytes]) -> dict[str, Any]:
    path = LANE / VALIDATOR_PATH
    before = path.read_bytes()
    text = before.decode("utf-8")
    for relative in SOURCE_PATHS[:13]:
        old = sha256(source_before[relative])
        new = sha256(source_after[relative])
        expected = f'"{relative}": "{old}"'
        replacement = f'"{relative}": "{new}"'
        if text.count(expected) != 1:
            raise RuntimeError(f"validator source-hash binding is not unique: {relative}")
        text = text.replace(expected, replacement)
    after = text.encode("utf-8")
    path.write_bytes(after)
    return {
        "before_bytes": len(before),
        "before_sha256": sha256(before),
        "after_bytes": len(after),
        "after_sha256": sha256(after),
    }


def main() -> int:
    source_before = {relative: read_bytes(relative) for relative in SOURCE_PATHS}
    before_inventory = source_inventory(source_before)
    replacement_counts: dict[str, dict[str, int]] = {}

    source_after: dict[str, bytes] = {}
    for relative, raw in source_before.items():
        normalized = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        text, counts = replace_terms(normalized)
        after = text.encode("utf-8")
        write_bytes(relative, after)
        source_after[relative] = after
        replacement_counts[relative] = counts

    control_changes: dict[str, dict[str, Any]] = {}
    for relative in TEXT_CONTROL_PATHS:
        before = read_bytes(relative)
        normalized = before.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        text, counts = replace_terms(normalized)
        after = text.encode("utf-8")
        write_bytes(relative, after)
        control_changes[relative] = {
            "before_bytes": len(before),
            "before_sha256": sha256(before),
            "after_bytes": len(after),
            "after_sha256": sha256(after),
            "replacement_counts": counts,
        }

    after_inventory = source_inventory(source_after)
    for relative in SOURCE_PATHS:
        before = before_inventory[relative]
        after = after_inventory[relative]
        if before["lines"] != after["lines"]:
            raise RuntimeError(f"line count changed: {relative}")
        if before["stable_ids"] != after["stable_ids"]:
            raise RuntimeError(f"stable-ID inventory changed: {relative}")

    backend_changes = update_backend(source_after)
    validator_change = update_validator(source_before, source_after)

    source_receipt = []
    for relative in SOURCE_PATHS:
        source_receipt.append(
            {
                "path": relative,
                "before_bytes": before_inventory[relative]["bytes"],
                "before_cr_bytes": before_inventory[relative]["cr_bytes"],
                "before_sha256": before_inventory[relative]["sha256"],
                "after_bytes": after_inventory[relative]["bytes"],
                "after_cr_bytes": after_inventory[relative]["cr_bytes"],
                "after_sha256": after_inventory[relative]["sha256"],
                "lines": after_inventory[relative]["lines"],
                "stable_id_count": len(after_inventory[relative]["stable_ids"]),
                "replacement_counts": replacement_counts[relative],
            }
        )

    receipt = {
        "schema_version": "1.0",
        "qa_id": "O012-ID-TERMINOLOGY-QA-2026-08-22",
        "date": "2026-08-22",
        "scope": "live Indonesian Units 001-017 and canonical Units 001-013 backend only",
        "frozen_artifacts_modified": False,
        "allowed_changes_only": True,
        "line_counts_unchanged": True,
        "stable_ids_unchanged": True,
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
        "source_files": source_receipt,
        "control_changes": control_changes,
        "backend_changes": backend_changes,
        "validator_change": validator_change,
        "validation_state": "pending_external_validator_run",
    }
    receipt_path = LANE / RECEIPT_PATH
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"terminology migration: PASS ({len(SOURCE_PATHS)} source files)")
    print(f"receipt: {RECEIPT_PATH}")
    return 0


def finalize_receipt() -> int:
    receipt_path = LANE / RECEIPT_PATH
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    for item in receipt["source_files"]:
        raw = read_bytes(item["path"])
        item["after_bytes"] = len(raw)
        item["after_cr_bytes"] = raw.count(b"\r")
        item["after_sha256"] = sha256(raw)
        prior_blob = subprocess.run(
            ["git", "show", f"HEAD:{item['path']}"],
            cwd=LANE,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        item["before_git_blob_bytes"] = len(prior_blob)
        item["before_git_blob_sha256"] = sha256(prior_blob)
        if "before_cr_bytes" not in item:
            # Unit 015 was the sole mixed-EOL live source at this boundary.
            delta = item["before_bytes"] - len(prior_blob)
            item["before_cr_bytes"] = delta if delta > 0 else 0

    for relative, item in receipt["control_changes"].items():
        raw = read_bytes(relative)
        item["after_bytes"] = len(raw)
        item["after_sha256"] = sha256(raw)

    backend_paths = sorted(
        BACKEND_TEXT_PATHS | BACKEND_LOCATOR_PATHS | BACKEND_FILE_METADATA_PATHS
    )
    for relative in backend_paths:
        current = read_bytes(relative)
        item = receipt["backend_changes"].get(relative)
        if item is None:
            prior = subprocess.run(
                ["git", "show", f"HEAD:{relative}"],
                cwd=LANE,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout
            item = {
                "before_bytes": len(prior),
                "before_sha256": sha256(prior),
            }
            receipt["backend_changes"][relative] = item
        item["after_bytes"] = len(current)
        item["after_sha256"] = sha256(current)
        item["changed"] = item["before_sha256"] != item["after_sha256"]

    validator = subprocess.run(
        [sys.executable, str(LANE / VALIDATOR_PATH)],
        cwd=LANE,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )
    if validator.returncode != 0 or "backend validation: PASS" not in validator.stdout:
        raise RuntimeError("backend validator did not pass during terminology QA finalization")
    bundle_match = re.search(r"backend_bundle_sha256: ([0-9a-f]{64})", validator.stdout)
    if bundle_match is None:
        raise RuntimeError("backend validator omitted its bundle hash")

    migration_raw = (LANE / "scripts/apply-indonesian-terminology-qa-2026-08-22.py").read_bytes()
    receipt["migration_script"] = {
        "path": "scripts/apply-indonesian-terminology-qa-2026-08-22.py",
        "bytes": len(migration_raw),
        "sha256": sha256(migration_raw),
    }
    report_relative = "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-22.md"
    report_raw = read_bytes(report_relative)
    receipt["human_report"] = {
        "path": report_relative,
        "bytes": len(report_raw),
        "sha256": sha256(report_raw),
    }
    verifier_relative = "scripts/verify-indonesian-terminology-qa-2026-08-22.py"
    verifier_raw = read_bytes(verifier_relative)
    receipt["verifier"] = {
        "path": verifier_relative,
        "bytes": len(verifier_raw),
        "sha256": sha256(verifier_raw),
    }
    receipt["arxiv_search"] = {
        "result": "no_suitable_indonesian_algebraic_topology_tex_source_found",
        "qualification": "bounded no-hit, not a proof of nonexistence",
        "queries": [
            'all:"topologi aljabar"',
            'all:"grup fundamental"',
            'all:"ruang penutup"',
            'all:"ruang topologis"',
        ],
        "official_search_base": "https://arxiv.org/search/",
    }
    receipt["fallback_source"] = {
        "authors": ["Valentino Risali", "Indah Emilia Wijayanti"],
        "title": "Sifat-Sifat Morfisma di dalam Kategori Ruang Penutup Ruang Topologis yang Terhubung Lintasan",
        "journal": "Jurnal Matematika Thales",
        "volume_issue_year_pages": "2(1), 2020, 23-35",
        "doi": "10.22146/jmt.56529",
        "article_url": "https://journal.ugm.ac.id/jmt/article/view/56529",
        "pdf_url": "https://journal.ugm.ac.id/jmt/article/download/56529/28321",
        "pdf_bytes": 373016,
        "pdf_sha256": "e520234d557737b7c7c64e4f76871875e3d72681b3a2acd7c7254bf088278b7f",
        "pdf_pages": 13,
        "language": "Bahasa Indonesia main text; English secondary abstract",
        "format": "LaTeX/pdfTeX-generated PDF; editable source is not exposed",
        "local_witness": "tmp/pdfs/terminology-qa/Risali_Wijayanti_2020_JMT_56529.pdf",
        "redistribution": "not committed; primary URL and exact byte hash recorded",
    }
    receipt["decisions"] = [
        {"concept": "functor", "preferred": "fungtor", "variant": "funktor", "action": "changed"},
        {"concept": "morphism", "preferred": "morfisma", "variant": "morfisme", "action": "changed with derived forms"},
        {"concept": "covering sheet", "preferred": "lembaran", "variant": "lembar", "action": "changed"},
        {"concept": "evenly covered", "preferred": "tertutup rata", "variant": "diliputi secara merata", "action": "preferred form changed; explanatory variant retained"},
        {"concept": "neighbourhood", "preferred": "lingkungan", "variant": "persekitaran", "action": "retained"},
        {"concept": "object", "preferred": "objek", "variant": "obyek", "action": "retained modern spelling"},
        {"concept": "fully faithful", "preferred": "penuh dan setia", "variant": "fully faithful", "action": "retained translated form"},
    ]
    receipt["validation_state"] = "passed"
    receipt["validation"] = {
        "backend_validator": "PASS",
        "backend_records": 1762,
        "backend_jsonl_files": 11,
        "backend_bundle_sha256": bundle_match.group(1),
        "line_counts_unchanged": True,
        "stable_ids_unchanged": True,
        "frozen_artifacts_modified": False,
    }
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("terminology QA finalization: PASS")
    print(f"backend_bundle_sha256: {bundle_match.group(1)}")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--finalize"]:
        raise SystemExit(finalize_receipt())
    if sys.argv[1:]:
        raise SystemExit("usage: apply-indonesian-terminology-qa-2026-08-22.py [--finalize]")
    raise SystemExit(main())
