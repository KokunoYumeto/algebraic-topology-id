#!/usr/bin/env python3
"""Prepare and verify the reader-first Roberts Units 001-030 Zenodo payload.

This script is deliberately local-only. It creates no deposition, reads no
credential, makes no network or Git request, and changes no source, backend,
QA, or control file. It writes only under
release/zenodo-units-001-030/artifacts.

The package remains fail-closed until FROZEN_LEDGER_SHA256 is replaced with
the SHA-256 of a final, apply_patch-created frozen-inputs.json ledger. The
ledger may be sealed only after the final Unit 30 cumulative PDF, self-
contained HTML, build receipt, and backend cumulative receipts exist.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import shutil
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


LANE = Path(__file__).resolve().parents[1]
RELEASE = LANE / "release" / "zenodo-units-001-030"
ARTIFACTS = RELEASE / "artifacts"
FROZEN_LEDGER = RELEASE / "frozen-inputs.json"
UPSTREAM = LANE / "authority" / "upstream" / "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE = LANE / "source" / "id-ID"
QA = LANE / "qa"
CONTROL = LANE / "00_control"
BACKEND = LANE / "backend"

TITLE = "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–30"
VERSION = "0.30.0"
RELEASE_ID = "o012-roberts-id-units-001-030-v0.30.0"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
TREE = "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5"
CONCEPT_DOI = "10.5281/zenodo.22061489"
PREVIOUS_RECORD_ID = 22074233
PREVIOUS_DOI = "10.5281/zenodo.22074233"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"

# Deliberately invalid until every final boundary input exists and a frozen
# ledger is created with apply_patch. Do not replace this with a guessed hash.
FROZEN_LEDGER_SHA256 = "e79f810d2106b95f4496471d0d3578e7f22571a579241e74d7f684add2f65fe6"

PDF_INPUT = "output/pdf/topologi-aljabar-unit-001-030-id.pdf"
HTML_INPUT = "output/html/units-001-030/index.html"
BUILD_RECEIPT = "qa/UNITS_001_030_BUILD_RECEIPT.json"
BACKEND_CUMULATIVE_JSON = "qa/BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.json"
BACKEND_CUMULATIVE_MD = "qa/BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.md"

PDF_NAME = "00_TOPOLOGI_ALJABAR_ID_UNITS_001_030_READER.pdf"
HTML_NAME = "TOPOLOGI_ALJABAR_ID_UNITS_001_030_READER.html"
SOURCE_ZIP_NAME = "TOPOLOGI_ALJABAR_ID_UNITS_001_030_EDITABLE_SOURCE_BACKEND.zip"
QA_ZIP_NAME = "TOPOLOGI_ALJABAR_ID_UNITS_001_030_QA_PROVENANCE.zip"

BACKEND_NAMES = (
    "artifacts.jsonl",
    "assets.jsonl",
    "authority.jsonl",
    "concepts.jsonl",
    "corrections.jsonl",
    "qa.jsonl",
    "relations.jsonl",
    "rights.jsonl",
    "segments.jsonl",
    "terms.jsonl",
    "units.jsonl",
)

FINAL_BOUNDARY_PATHS = {
    PDF_INPUT,
    HTML_INPUT,
    BUILD_RECEIPT,
    BACKEND_CUMULATIVE_JSON,
    BACKEND_CUMULATIVE_MD,
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lane_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or str(pure) != relative:
        raise RuntimeError(f"unsafe or non-canonical frozen path: {relative!r}")
    path = LANE.joinpath(*pure.parts)
    try:
        path.resolve().relative_to(LANE.resolve())
    except ValueError as error:
        raise RuntimeError(f"frozen path escapes lane: {relative!r}") from error
    return path


def assert_identity(path: Path, size: int, digest: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    actual_size = path.stat().st_size
    actual_digest = sha(path)
    if actual_size != size or actual_digest != digest:
        raise RuntimeError(
            f"frozen input mismatch: {path.relative_to(LANE)} "
            f"expected ({size}, {digest}) got ({actual_size}, {actual_digest})"
        )


def assert_safe_bytes(
    data: bytes,
    label: str,
    *,
    allow_generic_privacy_test_markers: bool = False,
) -> None:
    text = data.decode("latin-1")
    patterns = [
        r"(?i)github_pat_[A-Za-z0-9_]{16,}",
        r"(?i)\bghp_[A-Za-z0-9_]{16,}",
        r"(?i)\bsk-[A-Za-z0-9_-]{16,}",
        r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"(?i)\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b",
        r"(?i)authorization\s*[:=]\s*[\"']?bearer",
    ]
    if not allow_generic_privacy_test_markers:
        patterns.extend(
            (
                r"(?i)[A-Z]:[\\/](?:Users[\\/][^\\/\s\"']+[\\/]|Documents and Settings[\\/][^\\/\s\"']+[\\/]|Temp[\\/]|ProgramData[\\/])",
                r"(?i)\\\\(?:Users|Documents|Temp|ProgramData)\\",
                r"(?i)/(?:Users|home)/[^/\s]+/",
                r"(?i)access_token",
                r"(?i)zenodo.{0,24}token",
                r"(?i)figshare.{0,24}token",
            )
        )
    for pattern in patterns:
        if re.search(pattern, text):
            raise RuntimeError(f"unsafe release content: {label}")
    local_account_name = Path.home().name
    if len(local_account_name) >= 3 and re.search(
        rf"(?i)\b{re.escape(local_account_name)}\b", text
    ):
        raise RuntimeError(f"local account name leaked into release content: {label}")


def assert_safe_text(path: Path) -> None:
    assert_safe_bytes(path.read_bytes(), str(path.relative_to(LANE)))


def required_frozen_paths() -> set[str]:
    paths = {
        PDF_INPUT,
        HTML_INPUT,
        "output/ARTIFACT_MANIFEST_UNITS_001_030.csv",
        "scripts/build-units-001-030.ps1",
        "scripts/extend-backend-unit-030.py",
        "scripts/validate-backend-append-only-unit-030.py",
        "scripts/validate-backend-append-only-unit-030-cumulative.py",
        "qa/UNIT_029_QA.json",
        "qa/UNIT_029_INDEPENDENT_REVIEW.md",
        "qa/UNIT_029_SOURCE_AUDIT.md",
        "qa/UNIT_030_QA.json",
        "qa/UNIT_030_INDEPENDENT_REVIEW.md",
        "qa/UNIT_030_SOURCE_AUDIT.md",
        BUILD_RECEIPT,
        "qa/UNITS_001_030_VISUAL_QA.md",
        "qa/UNITS_001_030_RENDER_INVENTORY.csv",
        "qa/BACKEND_APPEND_ONLY_UNIT_030_FILE_MANIFEST.csv",
        "qa/BACKEND_APPEND_ONLY_UNIT_030_RECEIPT.json",
        "qa/BACKEND_APPEND_ONLY_UNIT_030_RECEIPT.md",
        BACKEND_CUMULATIVE_JSON,
        BACKEND_CUMULATIVE_MD,
        "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-23.json",
        "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-23.md",
        "00_control/AUTHORITY.json",
        "00_control/UPSTREAM_FILE_MANIFEST.csv",
        "00_control/TERMINOLOGY.csv",
        "ATTRIBUTION.md",
        f"authority/upstream/AlgebraicTopology2019-{COMMIT}/Notes.tex",
        f"authority/upstream/AlgebraicTopology2019-{COMMIT}/LICENSE.md",
        f"authority/upstream/AlgebraicTopology2019-{COMMIT}/README.md",
        "source/id-ID/reader-unit-001.md",
        "source/id-ID/styles/reader.css",
        "source/id-ID/styles/reader-cumulative.css",
        "release/zenodo-units-001-030/metadata.json",
        "release/zenodo-units-001-030/publication-plan.json",
        "release/zenodo-units-001-030/README_RELEASE.md",
        "release/zenodo-units-001-030/RELEASE_RIGHTS.md",
    }
    for number in range(2, 31):
        nn = f"{number:03d}"
        paths.add(f"source/id-ID/units/unit-{nn}-lecture-{nn}.md")
    for name in BACKEND_NAMES:
        paths.add(f"backend/{name}")
    return paths


def load_frozen_inputs() -> dict[str, dict[str, Any]]:
    if not re.fullmatch(r"[0-9a-f]{64}", FROZEN_LEDGER_SHA256):
        raise RuntimeError(
            "final Unit 30 input ledger is not sealed; refusing to guess identities"
        )
    if not FROZEN_LEDGER.is_file():
        raise FileNotFoundError(FROZEN_LEDGER)
    if sha(FROZEN_LEDGER) != FROZEN_LEDGER_SHA256:
        raise RuntimeError("frozen-inputs.json hash does not match the sealed script binding")
    payload = json.loads(FROZEN_LEDGER.read_text(encoding="utf-8"))
    if (
        payload.get("schema_version") != "1.0"
        or payload.get("release_id") != RELEASE_ID
        or payload.get("state") != "final_inputs_sealed_local_only"
    ):
        raise RuntimeError("frozen input ledger identity/state mismatch")
    if set(payload.get("final_boundary_paths", [])) != FINAL_BOUNDARY_PATHS:
        raise RuntimeError("frozen input ledger does not name the exact final boundary")
    rows = payload.get("entries")
    if not isinstance(rows, list):
        raise RuntimeError("frozen input ledger entries are not a list")
    entries: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"}:
            raise RuntimeError("malformed frozen input entry")
        relative = row["path"]
        size = row["bytes"]
        digest = row["sha256"]
        if (
            not isinstance(relative, str)
            or not isinstance(size, int)
            or size < 0
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
        ):
            raise RuntimeError(f"invalid frozen input identity: {row!r}")
        lane_path(relative)
        if relative in entries:
            raise RuntimeError(f"duplicate frozen input path: {relative}")
        entries[relative] = row
    expected = required_frozen_paths()
    if set(entries) != expected:
        missing = sorted(expected - set(entries))
        extra = sorted(set(entries) - expected)
        raise RuntimeError(f"frozen input inventory mismatch; missing={missing}, extra={extra}")
    for relative in sorted(entries):
        row = entries[relative]
        assert_identity(lane_path(relative), row["bytes"], row["sha256"])
    return entries


def identity(path: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(LANE).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha(path),
    }


def identity_matches(row: dict[str, Any], path: Path) -> bool:
    return (
        row.get("path") == path.relative_to(LANE).as_posix()
        and row.get("bytes") == path.stat().st_size
        and row.get("sha256") == sha(path)
    )


def parse_artifact_manifest() -> dict[str, dict[str, Any]]:
    path = LANE / "output" / "ARTIFACT_MANIFEST_UNITS_001_030.csv"
    with path.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    expected_paths = {PDF_INPUT, HTML_INPUT}
    if {row.get("path") for row in rows} != expected_paths or len(rows) != 2:
        raise RuntimeError("final reader artifact manifest must contain exactly PDF and HTML")
    parsed: dict[str, dict[str, Any]] = {}
    for row in rows:
        relative = row["path"]
        try:
            size = int(row["bytes"])
        except (TypeError, ValueError) as error:
            raise RuntimeError("invalid byte count in reader artifact manifest") from error
        digest = row.get("sha256", "")
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise RuntimeError("invalid digest in reader artifact manifest")
        assert_identity(lane_path(relative), size, digest)
        parsed[relative] = {"bytes": size, "sha256": digest}
    return parsed


def verify_backend() -> dict[str, Any]:
    digest = hashlib.sha256()
    total_bytes = 0
    total_records = 0
    rows = []
    for name in sorted(BACKEND_NAMES):
        path = BACKEND / name
        if not path.is_file():
            raise FileNotFoundError(path)
        raw = path.read_bytes()
        if not raw.endswith(b"\n"):
            raise RuntimeError(f"backend JSONL missing final LF: {name}")
        records = raw.count(b"\n")
        total_records += records
        total_bytes += len(raw)
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(raw)
        rows.append(
            {
                "filename": name,
                "records": records,
                "bytes": len(raw),
                "sha256": sha_bytes(raw),
            }
        )
    return {
        "total_records": total_records,
        "total_bytes": total_bytes,
        "bundle_sha256": digest.hexdigest(),
        "files": rows,
    }


def verify_build_receipt(artifact_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    path = lane_path(BUILD_RECEIPT)
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS" or receipt.get("scope") != "Roberts Indonesian reader Units 001-030":
        raise RuntimeError("final build receipt status/scope mismatch")
    authority = receipt.get("source_authority", {})
    if (
        authority.get("commit") != COMMIT
        or authority.get("tree") != TREE
        or authority.get("cumulative_source_span") != "134-6368"
        or authority.get("terminal_source_eof") is not True
        or authority.get("next_nominal_line") != 6369
    ):
        raise RuntimeError("final build receipt does not bind the terminal Roberts source boundary")
    artifacts = receipt.get("artifacts", {})
    for role, relative in (
        ("pdf", PDF_INPUT),
        ("html", HTML_INPUT),
        ("manifest", "output/ARTIFACT_MANIFEST_UNITS_001_030.csv"),
    ):
        if not identity_matches(artifacts.get(role, {}), lane_path(relative)):
            raise RuntimeError(f"final build receipt {role} identity mismatch")
    for relative in (PDF_INPUT, HTML_INPUT):
        actual = lane_path(relative)
        row = artifact_rows[relative]
        if actual.stat().st_size != row["bytes"] or sha(actual) != row["sha256"]:
            raise RuntimeError(f"artifact CSV binding mismatch: {relative}")
    html_checks = receipt.get("html_checks", {})
    if (
        html_checks.get("self_contained") is not True
        or html_checks.get("runtime_external_asset_references") != 0
        or html_checks.get("raw_tex_math_fallbacks") != 0
        or html_checks.get("duplicate_dom_ids") != 0
        or html_checks.get("unresolved_fragment_links") != 0
    ):
        raise RuntimeError("final HTML is not a verified self-contained reader")
    reproducibility = receipt.get("reproducibility", {})
    if (
        reproducibility.get("html_two_builds_byte_identical") is not True
        or reproducibility.get("pdf_two_builds_byte_identical") is not True
        or reproducibility.get("build_scratch_removed") is not True
    ):
        raise RuntimeError("final reader reproducibility gate is not closed")
    rights = receipt.get("rights", {})
    if (
        rights.get("license") != "CC BY 4.0"
        or rights.get("non_endorsement") is not True
        or rights.get("human_contributor_credit_preserved") is not True
    ):
        raise RuntimeError("final build receipt rights/nonendorsement controls mismatch")
    visual = receipt.get("visual_checks", {})
    if not identity_matches(
        {
            "path": visual.get("receipt"),
            "bytes": visual.get("receipt_bytes"),
            "sha256": visual.get("receipt_sha256"),
        },
        LANE / "qa" / "UNITS_001_030_VISUAL_QA.md",
    ):
        raise RuntimeError("final visual receipt identity mismatch")
    if not identity_matches(
        {
            "path": visual.get("render_inventory"),
            "bytes": visual.get("render_inventory_bytes"),
            "sha256": visual.get("render_inventory_sha256"),
        },
        LANE / "qa" / "UNITS_001_030_RENDER_INVENTORY.csv",
    ):
        raise RuntimeError("final render inventory identity mismatch")
    if not str(visual.get("result", "")).startswith("PASS"):
        raise RuntimeError("final visual QA did not pass")
    return receipt


def verify_backend_receipt(backend_facts: dict[str, Any]) -> dict[str, Any]:
    path = lane_path(BACKEND_CUMULATIVE_JSON)
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS":
        raise RuntimeError("final backend cumulative receipt did not pass")
    scope = str(receipt.get("scope", ""))
    if "001-030" not in scope:
        raise RuntimeError("final backend cumulative receipt scope mismatch")
    current = receipt.get("current", {})
    expected = {
        key: backend_facts[key]
        for key in ("total_records", "total_bytes", "bundle_sha256")
    }
    if {key: current.get(key) for key in expected} != expected:
        raise RuntimeError("final backend receipt does not bind the live backend boundary")
    if current.get("next_source_line") != 6369:
        raise RuntimeError("final backend receipt does not bind EOF after Notes.tex:6368")
    human = receipt.get("human_receipt", {})
    if not identity_matches(human, lane_path(BACKEND_CUMULATIVE_MD)):
        raise RuntimeError("final backend human receipt identity mismatch")
    return receipt


def verify_controls() -> tuple[dict[str, Any], dict[str, Any]]:
    controls = tuple(
        RELEASE / name
        for name in (
            "README_RELEASE.md",
            "RELEASE_RIGHTS.md",
            "metadata.json",
            "publication-plan.json",
        )
    )
    for path in controls:
        if not path.is_file():
            raise FileNotFoundError(path)
        assert_safe_text(path)
    public_controls = "\n".join(path.read_text(encoding="utf-8") for path in controls)
    if re.search(r"(?i)\bTTP\b|Translation and Transcription Project", public_controls):
        raise RuntimeError("forbidden umbrella marker in public release controls")
    if "Fomberg" not in public_controls or "30/30" not in public_controls:
        raise RuntimeError("public controls omit the exact composite-partial/Roberts-complete status")

    metadata_payload = json.loads((RELEASE / "metadata.json").read_text(encoding="utf-8"))
    metadata = metadata_payload.get("metadata", {})
    plan = json.loads((RELEASE / "publication-plan.json").read_text(encoding="utf-8"))
    if (
        metadata.get("title") != TITLE
        or metadata.get("version") != VERSION
        or metadata.get("license") != "cc-by-4.0"
        or metadata.get("language") != "ind"
    ):
        raise RuntimeError("metadata identity/license/language mismatch")
    if not str(metadata.get("description", "")).startswith(
        "<p><strong>Status: checkpoint parsial kursus komposit; korpus Roberts lengkap 30/30.</strong>"
    ):
        raise RuntimeError("metadata description does not lead with exact scope truth")
    if metadata.get("creators") != [{"name": "Roberts, David Michael"}] or metadata.get("contributors") != [
        {"name": "Editor edisi Bahasa Indonesia", "type": "Editor"}
    ]:
        raise RuntimeError("metadata authorship/contributor controls drifted")
    if (
        plan.get("state") != "prepared_not_published"
        or plan.get("existing_concept_doi") != CONCEPT_DOI
        or plan.get("current_public_record_id") != PREVIOUS_RECORD_ID
        or plan.get("current_public_doi") != PREVIOUS_DOI
    ):
        raise RuntimeError("publication plan does not preserve the existing concept lineage")
    if plan.get("new_concept_allowed") or plan.get("new_deposition_created") or plan.get("credentials_used"):
        raise RuntimeError("publication plan claims a forbidden action")
    if plan.get("reader_first_filename") != PDF_NAME:
        raise RuntimeError("publication plan does not put the PDF first")
    return metadata, plan


def source_entries() -> dict[str, Path]:
    entries: dict[str, Path] = {
        "ATTRIBUTION.md": LANE / "ATTRIBUTION.md",
        "upstream/Roberts/LICENSE.md": UPSTREAM / "LICENSE.md",
        "upstream/Roberts/README.md": UPSTREAM / "README.md",
        "upstream/Roberts/Notes.tex": UPSTREAM / "Notes.tex",
        "source/id-ID/reader-unit-001.md": SOURCE / "reader-unit-001.md",
        "source/id-ID/styles/reader.css": SOURCE / "styles" / "reader.css",
        "source/id-ID/styles/reader-cumulative.css": SOURCE / "styles" / "reader-cumulative.css",
        "controls/AUTHORITY.json": CONTROL / "AUTHORITY.json",
        "controls/UPSTREAM_FILE_MANIFEST.csv": CONTROL / "UPSTREAM_FILE_MANIFEST.csv",
        "controls/TERMINOLOGY.csv": CONTROL / "TERMINOLOGY.csv",
        "scripts/build-units-001-030.ps1": LANE / "scripts" / "build-units-001-030.ps1",
        "scripts/extend-backend-unit-030.py": LANE / "scripts" / "extend-backend-unit-030.py",
        "scripts/validate-backend-append-only-unit-030.py": LANE / "scripts" / "validate-backend-append-only-unit-030.py",
        "scripts/validate-backend-append-only-unit-030-cumulative.py": LANE / "scripts" / "validate-backend-append-only-unit-030-cumulative.py",
    }
    for number in range(2, 31):
        nn = f"{number:03d}"
        entries[f"source/id-ID/units/unit-{nn}-lecture-{nn}.md"] = (
            SOURCE / "units" / f"unit-{nn}-lecture-{nn}.md"
        )
    for name in BACKEND_NAMES:
        entries[f"backend/{name}"] = BACKEND / name
    return entries


def qa_entries() -> dict[str, Path]:
    names = (
        "UNIT_029_QA.json",
        "UNIT_029_INDEPENDENT_REVIEW.md",
        "UNIT_029_SOURCE_AUDIT.md",
        "UNIT_030_QA.json",
        "UNIT_030_INDEPENDENT_REVIEW.md",
        "UNIT_030_SOURCE_AUDIT.md",
        "UNITS_001_030_BUILD_RECEIPT.json",
        "UNITS_001_030_VISUAL_QA.md",
        "UNITS_001_030_RENDER_INVENTORY.csv",
        "BACKEND_APPEND_ONLY_UNIT_030_FILE_MANIFEST.csv",
        "BACKEND_APPEND_ONLY_UNIT_030_RECEIPT.json",
        "BACKEND_APPEND_ONLY_UNIT_030_RECEIPT.md",
        "BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.json",
        "BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.md",
        "INDONESIAN_TERMINOLOGY_QA_2026-08-23.json",
        "INDONESIAN_TERMINOLOGY_QA_2026-08-23.md",
    )
    entries = {f"qa/{name}": QA / name for name in names}
    entries["output/ARTIFACT_MANIFEST_UNITS_001_030.csv"] = (
        LANE / "output" / "ARTIFACT_MANIFEST_UNITS_001_030.csv"
    )
    entries["release/frozen-inputs.json"] = FROZEN_LEDGER
    return entries


def assert_archive_scope(entries: dict[str, Path], label: str) -> None:
    forbidden_parts = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules"}
    forbidden_fragments = ("raw-dump", "raw_dump", "temporary-render", "temp-render", "screenshots/")
    for name in entries:
        pure = PurePosixPath(name)
        lowered = name.lower()
        if any(part.lower() in forbidden_parts for part in pure.parts):
            raise RuntimeError(f"cache or repository control in {label}: {name}")
        if any(fragment in lowered for fragment in forbidden_fragments):
            raise RuntimeError(f"raw dump or temporary render in {label}: {name}")
        if "fomberg" in lowered:
            raise RuntimeError(f"Fomberg file forbidden from Roberts checkpoint: {name}")


def build_zip_bytes(entries: dict[str, Path]) -> tuple[bytes, list[dict[str, Any]]]:
    expected: dict[str, dict[str, Any]] = {}
    payload: dict[str, bytes] = {}
    for name, source in entries.items():
        if not source.is_file():
            raise FileNotFoundError(source)
        data = source.read_bytes()
        assert_safe_bytes(
            data,
            f"{source.relative_to(LANE)} as {name}",
            allow_generic_privacy_test_markers=name.startswith("scripts/"),
        )
        payload[name] = data
        expected[name] = {"bytes": len(data), "sha256": sha_bytes(data)}
    fixed_time = (2026, 8, 24, 0, 0, 0)
    output = io.BytesIO()
    with zipfile.ZipFile(
        output,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        archive.comment = b""
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0o644 << 16
            info.internal_attr = 0
            info.extra = b""
            info.comment = b""
            archive.writestr(info, payload[name])
    inventory = [{"path": name, **expected[name]} for name in sorted(entries)]
    return output.getvalue(), inventory


def deterministic_zip(target: Path, entries: dict[str, Path]) -> dict[str, Any]:
    assert_archive_scope(entries, target.name)
    first, inventory = build_zip_bytes(entries)
    second, second_inventory = build_zip_bytes(entries)
    if first != second or inventory != second_inventory:
        raise RuntimeError(f"ZIP rebuild is not byte deterministic: {target.name}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(first)
    with zipfile.ZipFile(target, "r") as archive:
        if archive.namelist() != [row["path"] for row in inventory]:
            raise RuntimeError(f"ZIP inventory/order mismatch: {target.name}")
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC failure: {target.name}")
        for row in inventory:
            data = archive.read(row["path"])
            if len(data) != row["bytes"] or sha_bytes(data) != row["sha256"]:
                raise RuntimeError(f"ZIP entry mismatch: {target.name}:{row['path']}")
    return {
        "filename": target.name,
        "bytes": target.stat().st_size,
        "sha256": sha(target),
        "entry_count": len(inventory),
        "uncompressed_bytes": sum(int(row["bytes"]) for row in inventory),
        "entries": inventory,
        "verified_inventory": True,
        "verified_crc": True,
        "verified_byte_deterministic_rebuild": True,
    }


def write_generated(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main() -> None:
    if not RELEASE.is_dir():
        raise RuntimeError(f"release controls were not created with apply_patch: {RELEASE.name}")
    metadata, plan = verify_controls()
    frozen = load_frozen_inputs()
    if not FINAL_BOUNDARY_PATHS.issubset(frozen):
        raise RuntimeError("final Unit 30 boundary identities are not all frozen")

    artifact_rows = parse_artifact_manifest()
    build_receipt = verify_build_receipt(artifact_rows)
    backend_facts = verify_backend()
    backend_receipt = verify_backend_receipt(backend_facts)

    allowed = {
        PDF_NAME,
        HTML_NAME,
        SOURCE_ZIP_NAME,
        QA_ZIP_NAME,
        "LICENSE.md",
        "README_RELEASE.md",
        "RELEASE_RIGHTS.md",
        "release-manifest.json",
        "SHA256SUMS",
    }
    if ARTIFACTS.exists():
        unexpected = sorted(path.name for path in ARTIFACTS.iterdir() if path.name not in allowed)
        if unexpected:
            raise RuntimeError(f"unexpected artifact(s); refusing to erase: {unexpected}")
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    source_zip = deterministic_zip(ARTIFACTS / SOURCE_ZIP_NAME, source_entries())
    qa_zip = deterministic_zip(ARTIFACTS / QA_ZIP_NAME, qa_entries())
    copies = {
        PDF_NAME: lane_path(PDF_INPUT),
        HTML_NAME: lane_path(HTML_INPUT),
        "LICENSE.md": UPSTREAM / "LICENSE.md",
        "README_RELEASE.md": RELEASE / "README_RELEASE.md",
        "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md",
    }
    assert_safe_text(copies[HTML_NAME])
    for name, source in copies.items():
        shutil.copyfile(source, ARTIFACTS / name)

    upload_files = [
        PDF_NAME,
        HTML_NAME,
        SOURCE_ZIP_NAME,
        QA_ZIP_NAME,
        "LICENSE.md",
        "README_RELEASE.md",
        "RELEASE_RIGHTS.md",
    ]
    pdf = build_receipt["artifacts"]["pdf"]
    html = build_receipt["html_checks"]
    unit_gate = build_receipt["unit_030_gate"]
    visual = build_receipt["visual_checks"]
    manifest = {
        "schema_version": "1.0",
        "release_id": RELEASE_ID,
        "title": TITLE,
        "version": VERSION,
        "status": "roberts_complete_composite_course_partial_checkpoint",
        "scope_truth": "Roberts Notes.tex lines 134-6368, lectures 1-30 of 30 complete through end{document}; Fomberg homology bridge and original proof/mastery/lab/capstone course closure pending",
        "publication_lineage": {
            "route": "new_version_in_existing_concept",
            "existing_concept_doi": CONCEPT_DOI,
            "previous_record_id": PREVIOUS_RECORD_ID,
            "previous_version_doi": PREVIOUS_DOI,
            "new_concept_created": False,
            "publication_performed_by_this_package_run": False,
        },
        "artifact_order": upload_files,
        "metadata_sha256": sha(RELEASE / "metadata.json"),
        "publication_plan_sha256": sha(RELEASE / "publication-plan.json"),
        "frozen_input_ledger": {
            "path": "release/zenodo-units-001-030/frozen-inputs.json",
            "bytes": FROZEN_LEDGER.stat().st_size,
            "sha256": sha(FROZEN_LEDGER),
            "entries": len(frozen),
            "final_boundary_paths": sorted(FINAL_BOUNDARY_PATHS),
        },
        "source": {
            "author": "David Michael Roberts",
            "repository": "https://github.com/DavidMichaelRoberts/AlgebraicTopology2019",
            "commit": COMMIT,
            "tree": TREE,
            "path": "Notes.tex",
            "line_start": 134,
            "line_end": 6368,
            "terminal": "end{document}; no Lecture 31 in the frozen source",
            "units": 30,
            "roberts_complete": True,
            "composite_course_complete": False,
            "license": "CC BY 4.0",
        },
        "reader_qa": {
            "status": "pass",
            "pdf_pages": pdf["pages"],
            "pdf_tagged": pdf["tagged"],
            "pdf_all_fonts_embedded_subset_tounicode": pdf[
                "all_fonts_embedded_subset_tounicode"
            ],
            "html_unique_dom_ids": html["unique_dom_ids"],
            "html_fragment_links": html["fragment_links"],
            "html_mathml_nodes": html["mathml_nodes"],
            "html_raw_tex_math_fallbacks": html["raw_tex_math_fallbacks"],
            "html_self_contained": html["self_contained"],
            "semantic_figures": html["semantic_figures"],
            "unit_030_stable_ids": unit_gate["stable_ids"],
            "visual_review": visual["result"],
        },
        "backend": {
            **backend_facts,
            "cumulative_receipt": identity(lane_path(BACKEND_CUMULATIVE_JSON)),
            "cumulative_human_receipt": identity(lane_path(BACKEND_CUMULATIVE_MD)),
            "receipt_id": backend_receipt.get("receipt_id"),
        },
        "archives": [source_zip, qa_zip],
        "artifacts": [],
        "privacy": {
            "credential_material": False,
            "absolute_local_paths": False,
            "user_personal_name": False,
            "cache_or_temp_render_payload": False,
            "raw_coordination_dump": False,
            "fomberg_files": False,
        },
        "rights": {
            "license": metadata["license"],
            "source_author_preserved": True,
            "nonendorsement_preserved": True,
        },
        "production_provenance": MODEL_NOTE,
        "credentials_used": plan["credentials_used"],
        "network_actions": 0,
    }
    for name in upload_files:
        path = ARTIFACTS / name
        manifest["artifacts"].append(
            {"filename": name, "bytes": path.stat().st_size, "sha256": sha(path)}
        )
    write_generated(
        ARTIFACTS / "release-manifest.json",
        (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )

    checksum_names = upload_files + ["release-manifest.json"]
    sums = "\n".join(
        f"{sha(ARTIFACTS / name)}  {name}" for name in checksum_names
    ) + "\n"
    write_generated(ARTIFACTS / "SHA256SUMS", sums.encode("utf-8"))

    actual_names = sorted(path.name for path in ARTIFACTS.iterdir() if path.is_file())
    if actual_names != sorted(allowed):
        raise RuntimeError(f"final payload inventory mismatch: {actual_names}")
    for name in actual_names:
        path = ARTIFACTS / name
        if path.suffix.lower() not in {".pdf", ".zip"}:
            assert_safe_text(path)
    for row in manifest["artifacts"]:
        path = ARTIFACTS / row["filename"]
        if path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
            raise RuntimeError(f"manifest binding failure: {path.name}")
    parsed_sums = {}
    for line in (ARTIFACTS / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        parsed_sums[name] = digest
    expected_sums = {name: sha(ARTIFACTS / name) for name in checksum_names}
    if parsed_sums != expected_sums:
        raise RuntimeError("SHA256SUMS binding failure")

    print(
        json.dumps(
            {
                "status": "PASS_PREPARED_NOT_PUBLISHED",
                "release_directory": "release/zenodo-units-001-030",
                "scope": "Roberts 30/30 complete; composite course partial",
                "metadata": identity(RELEASE / "metadata.json"),
                "publication_plan": identity(RELEASE / "publication-plan.json"),
                "frozen_input_ledger": identity(FROZEN_LEDGER),
                "files": [
                    {
                        "filename": name,
                        "bytes": (ARTIFACTS / name).stat().st_size,
                        "sha256": sha(ARTIFACTS / name),
                    }
                    for name in actual_names
                ],
                "total_payload_bytes": sum(
                    (ARTIFACTS / name).stat().st_size for name in actual_names
                ),
                "source_zip": {
                    key: value for key, value in source_zip.items() if key != "entries"
                },
                "qa_zip": {
                    key: value for key, value in qa_zip.items() if key != "entries"
                },
                "backend": {
                    key: value for key, value in backend_facts.items() if key != "files"
                },
                "network_actions": 0,
                "credentials_used": False,
                "published": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
