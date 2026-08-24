#!/usr/bin/env python3
"""Prepare the unpublished Roberts 001-030 + Fomberg 001 release payload.

The program is local-only: it performs no Git, network, credential, deposition,
or publication action.  It is deliberately unsealed in source control until all
reader, backend, and QA artifacts at this boundary agree byte-for-byte.

Safe preparation sequence:

1. Run ``--list-required-inputs`` to obtain the exact frozen inventory.
2. After every final gate passes, create ``frozen-inputs.json`` with exact byte
   counts and SHA-256 values, using state ``final_inputs_sealed_local_only``.
3. Bind that ledger's SHA-256 below with apply_patch.
4. Run without arguments.  All validation completes before a staging directory
   is created; the final ``artifacts`` directory is installed only after every
   package check passes.

Fomberg O012-FOM-001 remains a distinct edition component mapped to D60-R08;
the script rejects any representation of it as Roberts Unit/Lecture 31.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import posixpath
import re
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


LANE = Path(__file__).resolve().parents[1]
RELEASE = LANE / "release" / "zenodo-roberts-001-030-fomberg-001"
ARTIFACTS = RELEASE / "artifacts"
STAGING = RELEASE / ".package-staging"
FROZEN_LEDGER = RELEASE / "frozen-inputs.json"
PACKAGE_RECEIPT = RELEASE / "PACKAGE_PREPARATION_RECEIPT.json"
BACKEND = LANE / "backend"
QA = LANE / "qa"
CONTROL = LANE / "00_control"
SOURCE = LANE / "source" / "id-ID"
ROBERTS = (
    LANE
    / "authority"
    / "upstream"
    / "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
)
FOMBERG = (
    LANE
    / "authority"
    / "upstream"
    / "math-notes-563194fae879178b9a6871b249513bfc27968975"
    / "tree"
)

TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30 dan "
    "Jembatan Homologi §1.1–1.2"
)
VERSION = "0.30.1"
RELEASE_ID = "o012-composite-id-roberts-001-030-fomberg-001-v0.30.1"
CONCEPT_DOI = "10.5281/zenodo.22061489"
PREVIOUS_RECORD_ID = 22077025
PREVIOUS_DOI = "10.5281/zenodo.22077025"
ROBERTS_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
ROBERTS_TREE = "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5"
FOMBERG_COMMIT = "563194fae879178b9a6871b249513bfc27968975"
FOMBERG_TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"

# Deliberately invalid.  Replace only after final-input ledger creation; never
# copy a digest from conversation state or a stale receipt.
FROZEN_LEDGER_SHA256 = "e9c860ad786d4c7ed455fff6bc733496fdae3309c9ad65a8002540f4d1b95e16"

PDF_INPUT = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-id.pdf"
HTML_INPUT = "output/html/roberts-001-030-fomberg-001/index.html"
ARTIFACT_MANIFEST = "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001.csv"
BUILD_RECEIPT = "qa/ROBERTS_001_030_FOMBERG_001_BUILD_RECEIPT.json"
VISUAL_QA = "qa/ROBERTS_001_030_FOMBERG_001_VISUAL_QA.md"
RENDER_INVENTORY = "qa/ROBERTS_001_030_FOMBERG_001_RENDER_INVENTORY.csv"
BACKEND_CUMULATIVE_JSON = (
    "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_CUMULATIVE_RECEIPT.json"
)
BACKEND_CUMULATIVE_MD = (
    "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_CUMULATIVE_RECEIPT.md"
)
FOMBERG_QA = "qa/FOMBERG_UNIT_001_QA.json"
FOMBERG_READER = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-001-delta-complexes-simplicial-homology.md"
)

PDF_NAME = "00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_READER.pdf"
HTML_NAME = "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_READER.html"
SOURCE_ZIP_NAME = (
    "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_"
    "EDITABLE_SOURCE_BACKEND.zip"
)
QA_ZIP_NAME = (
    "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_QA_PROVENANCE.zip"
)

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
    ARTIFACT_MANIFEST,
    BUILD_RECEIPT,
    BACKEND_CUMULATIVE_JSON,
    BACKEND_CUMULATIVE_MD,
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def lane_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or str(pure) != relative:
        raise RuntimeError(f"unsafe or non-canonical lane path: {relative!r}")
    path = LANE.joinpath(*pure.parts)
    try:
        path.resolve().relative_to(LANE.resolve())
    except ValueError as error:
        raise RuntimeError(f"lane path escapes task root: {relative!r}") from error
    return path


def identity(path: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(LANE).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha(path),
    }


def identity_matches(row: Any, path: Path) -> bool:
    if not isinstance(row, dict):
        return False
    actual = identity(path)
    return all(row.get(key) == actual[key] for key in ("path", "bytes", "sha256"))


def assert_identity(path: Path, size: int, digest: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.stat().st_size != size or sha(path) != digest:
        raise RuntimeError(
            f"frozen input mismatch: {path.relative_to(LANE)}; "
            f"expected ({size}, {digest}), got "
            f"({path.stat().st_size}, {sha(path)})"
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


def source_path_inventory() -> set[str]:
    paths = {
        "ATTRIBUTION.md",
        "LICENSE.md",
        "release/zenodo-roberts-001-030-fomberg-001/SOURCE_PACKAGE_README.md",
        f"authority/upstream/AlgebraicTopology2019-{ROBERTS_COMMIT}/Notes.tex",
        f"authority/upstream/AlgebraicTopology2019-{ROBERTS_COMMIT}/LICENSE.md",
        f"authority/upstream/AlgebraicTopology2019-{ROBERTS_COMMIT}/README.md",
        f"authority/upstream/math-notes-{FOMBERG_COMMIT}/tree/algebraic_topology.tex",
        f"authority/upstream/math-notes-{FOMBERG_COMMIT}/tree/header.tex",
        f"authority/upstream/math-notes-{FOMBERG_COMMIT}/tree/LICENSE",
        "source/id-ID/reader-unit-001.md",
        FOMBERG_READER,
        "source/id-ID/styles/reader.css",
        "source/id-ID/styles/reader-cumulative.css",
        "00_control/AUTHORITY.json",
        "00_control/SOURCE_DECISION.md",
        "00_control/RIGHTS_AND_COMPONENTS.csv",
        "00_control/UPSTREAM_FILE_MANIFEST.csv",
        "00_control/TERMINOLOGY.csv",
        "00_control/ADVERSE_LEDGER.csv",
        "00_control/CURRICULUM_ROUTE_AND_FOMBERG_HANDOFF.md",
        "scripts/build-roberts-001-030-fomberg-001.ps1",
        "scripts/fomberg-unit-001-common.py",
        "scripts/qa-fomberg-unit-001.py",
        "scripts/extend-backend-fomberg-unit-001.py",
        "scripts/validate-backend-append-only-fomberg-unit-001.py",
        "scripts/validate-backend-append-only-fomberg-unit-001-cumulative.py",
    }
    for number in range(2, 31):
        paths.add(f"source/id-ID/units/unit-{number:03d}-lecture-{number:03d}.md")
    for name in BACKEND_NAMES:
        paths.add(f"backend/{name}")
    return paths


def qa_path_inventory() -> set[str]:
    return {
        ARTIFACT_MANIFEST,
        BUILD_RECEIPT,
        VISUAL_QA,
        RENDER_INVENTORY,
        FOMBERG_QA,
        "qa/FOMBERG_UNIT_001_INDEPENDENT_REVIEW.md",
        "qa/FOMBERG_UNIT_001_SOURCE_AUDIT.json",
        "qa/FOMBERG_UNIT_001_SOURCE_AUDIT.md",
        "qa/FOMBERG_UNIT_001_BACKEND_CONTRACT.md",
        "qa/fomberg-unit-001/TRANSLATION_LEDGER_AND_PROPOSED_TERMINOLOGY.md",
        "qa/FOMBERG_AUTHORITY_BUILD_GATE_QA.json",
        "qa/FOMBERG_AUTHORITY_BUILD_GATE_FILE_MANIFEST.csv",
        "qa/FOMBERG_AUTHORITY_BUILD_GATE_VISUAL_QA.md",
        "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_FILE_MANIFEST.csv",
        "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_RECEIPT.json",
        "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_RECEIPT.md",
        BACKEND_CUMULATIVE_JSON,
        BACKEND_CUMULATIVE_MD,
        "qa/UNITS_001_030_BUILD_RECEIPT.json",
        "qa/BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.json",
        "qa/BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.md",
        "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-23.json",
        "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-23.md",
    }


def release_control_inventory() -> set[str]:
    prefix = "release/zenodo-roberts-001-030-fomberg-001/"
    return {
        prefix + name
        for name in (
            "metadata.json",
            "publication-plan.json",
            "README_RELEASE.md",
            "SOURCE_PACKAGE_README.md",
            "LICENSE.md",
            "RELEASE_RIGHTS.md",
            "release-manifest.template.json",
            "SHA256SUMS.template",
            "frozen-inputs.template.json",
        )
    }


def required_frozen_paths() -> set[str]:
    return (
        FINAL_BOUNDARY_PATHS
        | source_path_inventory()
        | qa_path_inventory()
        | release_control_inventory()
    )


def list_required_inputs() -> None:
    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "release_id": RELEASE_ID,
                "state": "inventory_only_not_sealed",
                "final_boundary_paths": sorted(FINAL_BOUNDARY_PATHS),
                "required_paths": sorted(required_frozen_paths()),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def load_frozen_inputs() -> dict[str, dict[str, Any]]:
    if not re.fullmatch(r"[0-9a-f]{64}", FROZEN_LEDGER_SHA256):
        raise RuntimeError(
            "release is intentionally unsealed; final frozen-inputs.json and "
            "its apply_patch-bound SHA-256 are required before packaging"
        )
    if not FROZEN_LEDGER.is_file():
        raise FileNotFoundError(FROZEN_LEDGER)
    if sha(FROZEN_LEDGER) != FROZEN_LEDGER_SHA256:
        raise RuntimeError("frozen-inputs.json does not match the sealed packager binding")
    payload = json.loads(FROZEN_LEDGER.read_text(encoding="utf-8"))
    if (
        payload.get("schema_version") != "1.0"
        or payload.get("release_id") != RELEASE_ID
        or payload.get("state") != "final_inputs_sealed_local_only"
    ):
        raise RuntimeError("frozen input ledger identity/state mismatch")
    if set(payload.get("final_boundary_paths", [])) != FINAL_BOUNDARY_PATHS:
        raise RuntimeError("frozen ledger does not bind the exact final boundary")
    rows = payload.get("entries")
    if not isinstance(rows, list):
        raise RuntimeError("frozen ledger entries are not a list")
    entries: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"}:
            raise RuntimeError("malformed frozen input row")
        relative, size, digest = row["path"], row["bytes"], row["sha256"]
        if (
            not isinstance(relative, str)
            or not isinstance(size, int)
            or size < 0
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
        ):
            raise RuntimeError(f"invalid frozen identity: {row!r}")
        lane_path(relative)
        if relative in entries:
            raise RuntimeError(f"duplicate frozen input: {relative}")
        entries[relative] = row
    expected = required_frozen_paths()
    if set(entries) != expected:
        raise RuntimeError(
            "frozen inventory mismatch; "
            f"missing={sorted(expected - set(entries))}, "
            f"extra={sorted(set(entries) - expected)}"
        )
    for relative, row in sorted(entries.items()):
        assert_identity(lane_path(relative), row["bytes"], row["sha256"])
    return entries


def verify_controls() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[str]]:
    names = (
        "metadata.json",
        "publication-plan.json",
        "README_RELEASE.md",
        "LICENSE.md",
        "RELEASE_RIGHTS.md",
        "release-manifest.template.json",
        "SHA256SUMS.template",
    )
    for name in names:
        path = RELEASE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        assert_safe_text(path)
    joined = "\n".join((RELEASE / name).read_text(encoding="utf-8") for name in names)
    if re.search(
        r"(?i)(?:Roberts(?:\s+(?:Units?|Lectures?))?|Kuliah Roberts)\s*"
        r"(?:0*1\s*[-–]\s*0*31|0*31\s*/\s*0*31)",
        joined,
    ):
        raise RuntimeError("Fomberg was incorrectly renumbered as Roberts 31")
    for marker in ("30/30", "O012-FOM-001", "baris 615", "CC BY-SA 4.0"):
        if marker not in joined:
            raise RuntimeError(f"public controls omit exact scope/rights marker: {marker}")

    metadata_payload = json.loads((RELEASE / "metadata.json").read_text(encoding="utf-8"))
    metadata = metadata_payload.get("metadata", {})
    expected_creators = [
        {"name": "Roberts, David Michael"},
        {"name": "Fomberg, Yeheli"},
    ]
    expected_contributors = [
        {"name": "Lazarovich, Nir", "type": "Other"},
        {"name": "Editor edisi Bahasa Indonesia", "type": "Editor"},
        {"name": "Translation and Transcription Project", "type": "Other"},
    ]
    if (
        metadata.get("title") != TITLE
        or metadata.get("version") != VERSION
        or metadata.get("license") != "cc-by-sa-4.0"
        or metadata.get("language") != "ind"
        or metadata.get("creators") != expected_creators
        or metadata.get("contributors") != expected_contributors
    ):
        raise RuntimeError(
            "metadata title/version/license/language/creator/contributor drift"
        )
    if not str(metadata.get("description", "")).startswith(
        "<p><strong>Status: checkpoint parsial kursus komposit; korpus Roberts lengkap 30/30"
    ):
        raise RuntimeError("metadata description does not lead with exact scope truth")
    prose = "\n".join(
        str(metadata.get(field, "")) for field in ("title", "description", "notes")
    )
    if re.search(r"(?i)\bTTP\b|Translation and Transcription Project", prose):
        raise RuntimeError("umbrella marker leaked into title or prose metadata")
    if len(re.findall(r"Translation and Transcription Project", joined)) != 1:
        raise RuntimeError(
            "umbrella organization must appear exactly once in contributor metadata"
        )

    plan = json.loads((RELEASE / "publication-plan.json").read_text(encoding="utf-8"))
    if (
        plan.get("state") != "prepared_not_published"
        or plan.get("release_id") != RELEASE_ID
        or plan.get("existing_concept_doi") != CONCEPT_DOI
        or plan.get("current_public_record_id") != PREVIOUS_RECORD_ID
        or plan.get("current_public_doi") != PREVIOUS_DOI
        or plan.get("reader_first_filename") != PDF_NAME
    ):
        raise RuntimeError("publication plan does not preserve exact existing lineage")
    if plan.get("new_concept_allowed") or plan.get("new_deposition_created") or plan.get("credentials_used"):
        raise RuntimeError("publication plan claims forbidden external action")

    template = json.loads(
        (RELEASE / "release-manifest.template.json").read_text(encoding="utf-8")
    )
    if (
        template.get("release_id") != RELEASE_ID
        or template.get("title") != TITLE
        or template.get("version") != VERSION
        or template.get("status")
        != "roberts_complete_fomberg_unit_001_complete_composite_course_partial"
    ):
        raise RuntimeError("release manifest template identity/scope drift")
    artifact_order = template.get("artifact_order")
    expected_upload = [
        PDF_NAME,
        HTML_NAME,
        SOURCE_ZIP_NAME,
        QA_ZIP_NAME,
        "LICENSE.md",
        "README_RELEASE.md",
        "RELEASE_RIGHTS.md",
    ]
    if artifact_order != expected_upload:
        raise RuntimeError("release manifest template does not preserve reader-first order")

    checksum_lines = (RELEASE / "SHA256SUMS.template").read_text(encoding="utf-8").splitlines()
    checksum_names = []
    for line in checksum_lines:
        marker, separator, name = line.partition("  ")
        if marker != "<sha256>" or not separator or not name:
            raise RuntimeError("malformed SHA256SUMS.template")
        checksum_names.append(name)
    if checksum_names != expected_upload + ["release-manifest.json"]:
        raise RuntimeError("checksum template inventory/order mismatch")
    return metadata, plan, template, checksum_names


def parse_artifact_manifest() -> dict[str, dict[str, Any]]:
    path = lane_path(ARTIFACT_MANIFEST)
    with path.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    expected_paths = {PDF_INPUT, HTML_INPUT}
    if len(rows) != 2 or {row.get("path") for row in rows} != expected_paths:
        raise RuntimeError("reader artifact manifest must contain exactly PDF and HTML")
    parsed: dict[str, dict[str, Any]] = {}
    for row in rows:
        relative = row["path"]
        try:
            size = int(row["bytes"])
        except (TypeError, ValueError) as error:
            raise RuntimeError("invalid reader manifest byte count") from error
        digest = row.get("sha256", "")
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise RuntimeError("invalid reader manifest SHA-256")
        assert_identity(lane_path(relative), size, digest)
        parsed[relative] = {"bytes": size, "sha256": digest}
    return parsed


def verify_build_receipt(artifact_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    receipt = json.loads(lane_path(BUILD_RECEIPT).read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS" or receipt.get("qa_id") != "O012-RBT-001-030-FOM-001-COMPOSITE-BUILD":
        raise RuntimeError("composite build receipt did not pass or has wrong identity")
    numbering = receipt.get("component_numbering", {})
    if numbering != {
        "roberts_edition_units": "001-030",
        "fomberg_component_id": "O012-FOM-001",
        "course_route_unit_id": "D60-R08",
        "fomberg_is_not_roberts_unit_031": True,
    }:
        raise RuntimeError("component numbering/route mapping drift")
    authorities = receipt.get("authorities", {})
    roberts = authorities.get("roberts", {})
    fomberg = authorities.get("fomberg", {})
    if (
        roberts.get("commit") != ROBERTS_COMMIT
        or roberts.get("tree") != ROBERTS_TREE
        or roberts.get("license") != "CC BY 4.0"
        or fomberg.get("commit") != FOMBERG_COMMIT
        or fomberg.get("tree") != FOMBERG_TREE
        or fomberg.get("selected_source_span") != "31-614"
        or fomberg.get("selected_span_lines") != 584
        or fomberg.get("next_source_line") != 615
        or fomberg.get("license") != "CC BY-SA 4.0"
    ):
        raise RuntimeError("composite build authority/span/license mismatch")
    artifacts = receipt.get("artifacts", {})
    for role, relative in (("pdf", PDF_INPUT), ("html", HTML_INPUT), ("manifest", ARTIFACT_MANIFEST)):
        if not identity_matches(artifacts.get(role), lane_path(relative)):
            raise RuntimeError(f"build receipt {role} does not bind live final bytes")
    for relative, row in artifact_rows.items():
        actual = lane_path(relative)
        if actual.stat().st_size != row["bytes"] or sha(actual) != row["sha256"]:
            raise RuntimeError(f"reader artifact/CSV mismatch: {relative}")
    html = receipt.get("html_checks", {})
    if (
        html.get("status") != "PASS"
        or html.get("self_contained") is not True
        or html.get("runtime_external_asset_references") != 0
        or html.get("raw_tex_math_fallbacks") != 0
        or html.get("duplicate_dom_ids") != 0
        or html.get("unresolved_fragment_links") != 0
        or html.get("missing_fomberg_stable_ids") != 0
    ):
        raise RuntimeError("self-contained HTML gate is incomplete")
    reproducibility = receipt.get("reproducibility", {})
    if (
        reproducibility.get("html_two_builds_byte_identical") is not True
        or reproducibility.get("pdf_two_builds_byte_identical") is not True
        or reproducibility.get("build_scratch_removed") is not True
        or reproducibility.get("reader_and_backend_unchanged") is not True
    ):
        raise RuntimeError("composite reproducibility gate is incomplete")
    rights = receipt.get("rights_and_provenance", {})
    if (
        rights.get("integrated_reader_license") != "CC BY-SA 4.0"
        or rights.get("roberts_component_license") != "CC BY 4.0"
        or rights.get("fomberg_component_license") != "CC BY-SA 4.0"
        or rights.get("component_attribution_preserved") is not True
        or rights.get("changes_disclosed") is not True
        or rights.get("non_endorsement_disclosed") is not True
    ):
        raise RuntimeError("composite rights/provenance gate is incomplete")
    visual = receipt.get("visual_checks", {})
    if visual.get("status") != "PASS":
        raise RuntimeError("composite visual QA did not pass")
    if not identity_matches(visual.get("render_inventory"), lane_path(RENDER_INVENTORY)):
        raise RuntimeError("render inventory identity mismatch")
    if not identity_matches(visual.get("visual_receipt"), lane_path(VISUAL_QA)):
        raise RuntimeError("visual QA receipt identity mismatch")
    return receipt


def verify_fomberg_qa() -> dict[str, Any]:
    qa = json.loads(lane_path(FOMBERG_QA).read_text(encoding="utf-8"))
    if qa.get("status") != "PASS" or qa.get("qa_id") != "O012-FOMBERG-UNIT-001-STATIC-QA":
        raise RuntimeError("Fomberg Unit 001 static QA did not pass")
    authority = qa.get("authority", {})
    span = authority.get("unit_span", {})
    if (
        authority.get("commit") != FOMBERG_COMMIT
        or authority.get("tree") != FOMBERG_TREE
        or authority.get("next_source_line") != 615
        or span.get("line_start") != 31
        or span.get("line_end") != 614
        or authority.get("terminal_source_eof") is not False
    ):
        raise RuntimeError("Fomberg QA source boundary mismatch")
    if not identity_matches(qa.get("reader"), lane_path(FOMBERG_READER)):
        raise RuntimeError("Fomberg QA does not bind the live translated reader")
    checks = qa.get("checks", {})
    required = (
        "authority_gate_55_of_55",
        "component_rights_partition",
        "exact_87_ids",
        "independent_review_p1_p2_p3_zero",
        "immutable_unit30_prefix",
        "ledgers_closed",
        "proof_repair_complete",
        "six_mastery_triples_complete",
        "source_span_and_cursor",
    )
    if any(checks.get(name) is not True for name in required):
        raise RuntimeError("Fomberg Unit 001 static QA gate is incomplete")
    rights = qa.get("rights", {})
    if (
        rights.get("integrated_route_license") != "CC-BY-SA-4.0"
        or rights.get("roberts_component_preserved_as") != "CC-BY-4.0"
    ):
        raise RuntimeError("Fomberg QA rights partition mismatch")
    return qa


def verify_backend() -> dict[str, Any]:
    digest = hashlib.sha256()
    total_bytes = 0
    total_records = 0
    files = []
    for name in sorted(BACKEND_NAMES):
        path = BACKEND / name
        if not path.is_file():
            raise FileNotFoundError(path)
        raw = path.read_bytes()
        if not raw.endswith(b"\n"):
            raise RuntimeError(f"backend JSONL lacks final LF: {name}")
        records = raw.count(b"\n")
        total_records += records
        total_bytes += len(raw)
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(raw)
        files.append(
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
        "files": files,
    }


def verify_backend_receipt(backend_facts: dict[str, Any]) -> dict[str, Any]:
    receipt = json.loads(lane_path(BACKEND_CUMULATIVE_JSON).read_text(encoding="utf-8"))
    if (
        receipt.get("status") != "PASS"
        or receipt.get("receipt_id")
        != "O012-BACKEND-THROUGH-FOMBERG-UNIT-001-CUMULATIVE-SEMANTIC"
    ):
        raise RuntimeError("Fomberg cumulative backend receipt did not pass")
    current = receipt.get("current", {})
    expected = {
        key: backend_facts[key]
        for key in ("total_records", "total_bytes", "bundle_sha256")
    }
    if {key: current.get(key) for key in expected} != expected:
        raise RuntimeError("cumulative backend receipt does not bind live backend")
    if (
        current.get("next_source_line") != 615
        or current.get("terminal_source_eof") is not False
        or current.get("stable_ids") != 87
        or current.get("mastery_triples") != 6
    ):
        raise RuntimeError("cumulative backend semantic boundary mismatch")
    prefix = receipt.get("nested_immutability", {}).get("roberts_units_001_030_prefix", {})
    if (
        prefix.get("preserved_byte_for_byte") is not True
        or prefix.get("records") != 4761
        or prefix.get("bundle_sha256")
        != "51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920"
    ):
        raise RuntimeError("Roberts backend prefix was not preserved byte-for-byte")
    if not identity_matches(receipt.get("human_receipt"), lane_path(BACKEND_CUMULATIVE_MD)):
        raise RuntimeError("cumulative backend human receipt identity mismatch")
    return receipt


def source_entries() -> dict[str, Path]:
    entries: dict[str, Path] = {
        "ATTRIBUTION.md": LANE / "ATTRIBUTION.md",
        "LICENSE.md": LANE / "LICENSE.md",
        "README.md": RELEASE / "SOURCE_PACKAGE_README.md",
        f"authority/upstream/AlgebraicTopology2019-{ROBERTS_COMMIT}/Notes.tex": ROBERTS / "Notes.tex",
        f"authority/upstream/AlgebraicTopology2019-{ROBERTS_COMMIT}/LICENSE.md": ROBERTS / "LICENSE.md",
        f"authority/upstream/AlgebraicTopology2019-{ROBERTS_COMMIT}/README.md": ROBERTS / "README.md",
        f"authority/upstream/math-notes-{FOMBERG_COMMIT}/tree/algebraic_topology.tex": FOMBERG / "algebraic_topology.tex",
        f"authority/upstream/math-notes-{FOMBERG_COMMIT}/tree/header.tex": FOMBERG / "header.tex",
        f"authority/upstream/math-notes-{FOMBERG_COMMIT}/tree/LICENSE": FOMBERG / "LICENSE",
        "source/id-ID/reader-unit-001.md": SOURCE / "reader-unit-001.md",
        FOMBERG_READER: lane_path(FOMBERG_READER),
        "source/id-ID/styles/reader.css": SOURCE / "styles" / "reader.css",
        "source/id-ID/styles/reader-cumulative.css": SOURCE / "styles" / "reader-cumulative.css",
        "00_control/AUTHORITY.json": CONTROL / "AUTHORITY.json",
        "00_control/SOURCE_DECISION.md": CONTROL / "SOURCE_DECISION.md",
        "00_control/RIGHTS_AND_COMPONENTS.csv": CONTROL / "RIGHTS_AND_COMPONENTS.csv",
        "00_control/UPSTREAM_FILE_MANIFEST.csv": CONTROL / "UPSTREAM_FILE_MANIFEST.csv",
        "00_control/TERMINOLOGY.csv": CONTROL / "TERMINOLOGY.csv",
        "00_control/ADVERSE_LEDGER.csv": CONTROL / "ADVERSE_LEDGER.csv",
        "00_control/CURRICULUM_ROUTE_AND_FOMBERG_HANDOFF.md": CONTROL / "CURRICULUM_ROUTE_AND_FOMBERG_HANDOFF.md",
        "scripts/build-roberts-001-030-fomberg-001.ps1": LANE / "scripts" / "build-roberts-001-030-fomberg-001.ps1",
        "scripts/package-release-roberts-001-030-fomberg-001.py": Path(__file__).resolve(),
        "scripts/fomberg-unit-001-common.py": LANE / "scripts" / "fomberg-unit-001-common.py",
        "scripts/qa-fomberg-unit-001.py": LANE / "scripts" / "qa-fomberg-unit-001.py",
        "scripts/extend-backend-fomberg-unit-001.py": LANE / "scripts" / "extend-backend-fomberg-unit-001.py",
        "scripts/validate-backend-append-only-fomberg-unit-001.py": LANE / "scripts" / "validate-backend-append-only-fomberg-unit-001.py",
        "scripts/validate-backend-append-only-fomberg-unit-001-cumulative.py": LANE / "scripts" / "validate-backend-append-only-fomberg-unit-001-cumulative.py",
    }
    for number in range(2, 31):
        name = f"unit-{number:03d}-lecture-{number:03d}.md"
        entries[f"source/id-ID/units/{name}"] = SOURCE / "units" / name
    for name in BACKEND_NAMES:
        entries[f"backend/{name}"] = BACKEND / name
    return entries


def qa_entries() -> dict[str, Path]:
    entries = {relative: lane_path(relative) for relative in sorted(qa_path_inventory())}
    entries.update(
        {
            "release/frozen-inputs.json": FROZEN_LEDGER,
            "release/frozen-inputs.template.json": RELEASE / "frozen-inputs.template.json",
            "release/release-manifest.template.json": RELEASE / "release-manifest.template.json",
            "release/SHA256SUMS.template": RELEASE / "SHA256SUMS.template",
        }
    )
    return entries


def assert_archive_scope(entries: dict[str, Path], label: str) -> None:
    forbidden_parts = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules"}
    forbidden_fragments = (
        "raw-dump",
        "raw_dump",
        "temporary-render",
        "temp-render",
        "screenshots/",
        "publication-receipt",
        "transaction.json",
    )
    for name in entries:
        pure = PurePosixPath(name)
        lowered = name.lower()
        if any(part.lower() in forbidden_parts for part in pure.parts):
            raise RuntimeError(f"cache/repository control in {label}: {name}")
        if any(fragment in lowered for fragment in forbidden_fragments):
            raise RuntimeError(f"raw/transient/publication payload in {label}: {name}")


def assert_source_archive_link_closure(entries: dict[str, Path]) -> None:
    """Fail closed when a reader-facing root document links outside the ZIP."""
    archive_names = set(entries)
    for archive_name in ("README.md", "ATTRIBUTION.md", "LICENSE.md"):
        source = entries[archive_name]
        text = source.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip().split("#", 1)[0]
            if not target or re.match(r"^(?:https?://|mailto:)", target, re.I):
                continue
            resolved = posixpath.normpath(
                posixpath.join(posixpath.dirname(archive_name), target)
            )
            if resolved.startswith("../") or resolved == "..":
                raise RuntimeError(
                    f"source ZIP link escapes archive: {archive_name} -> {target}"
                )
            if resolved not in archive_names and not any(
                name.startswith(resolved.rstrip("/") + "/") for name in archive_names
            ):
                raise RuntimeError(
                    f"source ZIP link target absent: {archive_name} -> {target}"
                )


def build_zip_bytes(entries: dict[str, Path]) -> tuple[bytes, list[dict[str, Any]]]:
    assert_archive_scope(entries, "deterministic ZIP")
    payload: dict[str, bytes] = {}
    inventory = []
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
        inventory.append({"path": name, "bytes": len(data), "sha256": sha_bytes(data)})
    inventory.sort(key=lambda row: row["path"])
    fixed_time = (2026, 8, 24, 0, 0, 0)
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.comment = b""
        for row in inventory:
            name = row["path"]
            info = zipfile.ZipInfo(name, date_time=fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0o644 << 16
            info.internal_attr = 0
            info.extra = b""
            info.comment = b""
            archive.writestr(info, payload[name])
    return output.getvalue(), inventory


def deterministic_zip(target: Path, entries: dict[str, Path]) -> dict[str, Any]:
    first, inventory = build_zip_bytes(entries)
    second, second_inventory = build_zip_bytes(entries)
    if first != second or inventory != second_inventory:
        raise RuntimeError(f"ZIP rebuild is not byte deterministic: {target.name}")
    target.write_bytes(first)
    with zipfile.ZipFile(target, "r") as archive:
        if archive.namelist() != [row["path"] for row in inventory]:
            raise RuntimeError(f"ZIP entry order mismatch: {target.name}")
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC failure: {target.name}")
        for row in inventory:
            data = archive.read(row["path"])
            if len(data) != row["bytes"] or sha_bytes(data) != row["sha256"]:
                raise RuntimeError(f"ZIP entry identity mismatch: {target.name}:{row['path']}")
    return {
        "filename": target.name,
        "bytes": target.stat().st_size,
        "sha256": sha(target),
        "entry_count": len(inventory),
        "uncompressed_bytes": sum(int(row["bytes"]) for row in inventory),
        "entries": inventory,
        "verified_crc": True,
        "verified_inventory": True,
        "verified_byte_deterministic_rebuild": True,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_package_receipt(
    frozen: dict[str, dict[str, Any]],
    source_zip: dict[str, Any],
    qa_zip: dict[str, Any],
) -> None:
    files = [
        {
            "filename": path.name,
            "bytes": path.stat().st_size,
            "sha256": sha(path),
        }
        for path in sorted(ARTIFACTS.iterdir(), key=lambda item: item.name)
        if path.is_file()
    ]
    archives = []
    for row in (source_zip, qa_zip):
        entries = row["entries"]
        archives.append(
            {
                "filename": row["filename"],
                "bytes": row["bytes"],
                "sha256": row["sha256"],
                "entry_count": row["entry_count"],
                "uncompressed_bytes": row["uncompressed_bytes"],
                "crc_status": "PASS",
                "first_entry": entries[0]["path"],
                "last_entry": entries[-1]["path"],
            }
        )
    payload = {
        "schema_version": "1.0",
        "status": "PASS_PREPARED_NOT_PUBLISHED",
        "release_id": RELEASE_ID,
        "scope": (
            "Roberts 30/30 complete; Fomberg O012-FOM-001 (Sections 1.1-1.2, "
            "lines 31-614) complete; composite course partial; next Fomberg line 615"
        ),
        "release_directory": RELEASE.relative_to(LANE).as_posix(),
        "reader_first_filename": PDF_NAME,
        "frozen_input_ledger": {
            **identity(FROZEN_LEDGER),
            "entries": len(frozen),
        },
        "packager": identity(Path(__file__).resolve()),
        "files": files,
        "file_count": len(files),
        "total_payload_bytes": sum(int(row["bytes"]) for row in files),
        "archives": archives,
        "verification": {
            "manifest_artifact_identities_match": True,
            "sha256sums_match": True,
            "zip_crc_and_inventory_pass": True,
            "source_archive_local_link_closure_pass": True,
            "rights_component_scope_consistent": True,
            "reader_first": True,
            "integrated_license": "CC BY-SA 4.0",
            "roberts_component_license": "CC BY 4.0",
            "fomberg_component_license": "CC BY-SA 4.0",
            "new_concept_created": False,
            "network_actions": 0,
            "git_actions": 0,
            "credentials_used": False,
            "published": False,
        },
    }
    temporary = PACKAGE_RECEIPT.with_suffix(".json.tmp")
    write_json(temporary, payload)
    temporary.replace(PACKAGE_RECEIPT)


def package() -> None:
    if not RELEASE.is_dir():
        raise RuntimeError("release controls must exist before packaging")
    if ARTIFACTS.exists():
        raise RuntimeError("artifacts directory already exists; refusing to overwrite")
    if STAGING.exists():
        raise RuntimeError("stale package staging directory exists; inspect it explicitly")

    metadata, plan, manifest_template, checksum_names = verify_controls()
    frozen = load_frozen_inputs()
    artifact_rows = parse_artifact_manifest()
    build_receipt = verify_build_receipt(artifact_rows)
    fomberg_qa = verify_fomberg_qa()
    backend_facts = verify_backend()
    backend_receipt = verify_backend_receipt(backend_facts)

    source = source_entries()
    qa = qa_entries()
    assert_source_archive_link_closure(source)
    frozen_paths = set(frozen)
    for archive_name, entries in ((SOURCE_ZIP_NAME, source), (QA_ZIP_NAME, qa)):
        for name, path in entries.items():
            relative = path.relative_to(LANE).as_posix()
            if path.resolve() == Path(__file__).resolve() or path.resolve() == FROZEN_LEDGER.resolve():
                continue
            if relative not in frozen_paths:
                raise RuntimeError(f"unfrozen {archive_name} input: {name} <- {relative}")

    STAGING.mkdir(parents=False)
    try:
        source_zip = deterministic_zip(STAGING / SOURCE_ZIP_NAME, source)
        qa_zip = deterministic_zip(STAGING / QA_ZIP_NAME, qa)
        copies = {
            PDF_NAME: lane_path(PDF_INPUT),
            HTML_NAME: lane_path(HTML_INPUT),
            "LICENSE.md": RELEASE / "LICENSE.md",
            "README_RELEASE.md": RELEASE / "README_RELEASE.md",
            "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md",
        }
        assert_safe_text(copies[HTML_NAME])
        for name, source_path in copies.items():
            shutil.copyfile(source_path, STAGING / name)

        upload_files = list(manifest_template["artifact_order"])
        manifest = dict(manifest_template)
        manifest.pop("template_state", None)
        manifest.pop("generated_fields", None)
        manifest.update(
            {
                "metadata_sha256": sha(RELEASE / "metadata.json"),
                "publication_plan_sha256": sha(RELEASE / "publication-plan.json"),
                "frozen_input_ledger": {
                    **identity(FROZEN_LEDGER),
                    "entries": len(frozen),
                    "final_boundary_paths": sorted(FINAL_BOUNDARY_PATHS),
                },
                "sources": {
                    "roberts": {
                        "author": "David Michael Roberts",
                        "commit": ROBERTS_COMMIT,
                        "tree": ROBERTS_TREE,
                        "path": "Notes.tex",
                        "line_start": 134,
                        "line_end": 6368,
                        "edition_units": 30,
                        "complete": True,
                        "license": "CC BY 4.0",
                    },
                    "fomberg": {
                        "author": "Yeheli Fomberg",
                        "lecture_credit": "Nir Lazarovich",
                        "commit": FOMBERG_COMMIT,
                        "tree": FOMBERG_TREE,
                        "path": "algebraic_topology.tex",
                        "line_start": 31,
                        "line_end": 614,
                        "sections": "1.1-1.2",
                        "component_id": "O012-FOM-001",
                        "course_route_unit_id": "D60-R08",
                        "next_source_line": 615,
                        "complete_at_selected_boundary": True,
                        "license": "CC BY-SA 4.0",
                    },
                    "composite_course_complete": False,
                },
                "reader_qa": {
                    "status": "PASS",
                    "pdf_pages": build_receipt["artifacts"]["pdf"]["pages"],
                    "pdf_tagged": build_receipt["artifacts"]["pdf"]["tagged"],
                    "pdf_all_fonts_embedded_subset_tounicode": build_receipt["artifacts"]["pdf"]["all_fonts_embedded_subset_tounicode"],
                    "html_unique_dom_ids": build_receipt["html_checks"]["unique_dom_ids"],
                    "html_fragment_links": build_receipt["html_checks"]["fragment_links"],
                    "html_mathml_nodes": build_receipt["html_checks"]["mathml_nodes"],
                    "html_self_contained": build_receipt["html_checks"]["self_contained"],
                    "fomberg_stable_ids": fomberg_qa["structure"]["stable_id_count"],
                    "mastery_triples": fomberg_qa["mastery"]["triples"],
                    "visual_status": build_receipt["visual_checks"]["status"],
                    "browser_checks": build_receipt.get("browser_checks", {}),
                    "pdf_untagged_limitation_disclosed": True,
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
                },
                "production_provenance": MODEL_NOTE,
                "credentials_used": plan["credentials_used"],
                "network_actions": 0,
            }
        )
        for name in upload_files:
            path = STAGING / name
            manifest["artifacts"].append(
                {"filename": name, "bytes": path.stat().st_size, "sha256": sha(path)}
            )
        write_json(STAGING / "release-manifest.json", manifest)

        sums = "\n".join(
            f"{sha(STAGING / name)}  {name}" for name in checksum_names
        ) + "\n"
        (STAGING / "SHA256SUMS").write_text(sums, encoding="utf-8", newline="\n")

        expected_names = sorted(checksum_names + ["SHA256SUMS"])
        actual_names = sorted(path.name for path in STAGING.iterdir() if path.is_file())
        if actual_names != expected_names:
            raise RuntimeError(f"staged payload inventory mismatch: {actual_names}")
        for name in actual_names:
            path = STAGING / name
            if path.suffix.lower() not in {".pdf", ".zip"}:
                assert_safe_text(path)
        parsed_sums: dict[str, str] = {}
        for line in (STAGING / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
            digest, name = line.split("  ", 1)
            parsed_sums[name] = digest
        expected_sums = {name: sha(STAGING / name) for name in checksum_names}
        if parsed_sums != expected_sums:
            raise RuntimeError("generated SHA256SUMS does not bind every payload file")
        for row in manifest["artifacts"]:
            path = STAGING / row["filename"]
            if path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
                raise RuntimeError(f"release manifest artifact mismatch: {path.name}")

        STAGING.replace(ARTIFACTS)
    except Exception:
        if STAGING.exists():
            shutil.rmtree(STAGING)
        raise

    write_package_receipt(frozen, source_zip, qa_zip)

    print(
        json.dumps(
            {
                "status": "PASS_PREPARED_NOT_PUBLISHED",
                "release_directory": RELEASE.relative_to(LANE).as_posix(),
                "scope": "Roberts 30/30 + Fomberg O012-FOM-001; composite course partial",
                "files": [
                    {
                        "filename": name,
                        "bytes": (ARTIFACTS / name).stat().st_size,
                        "sha256": sha(ARTIFACTS / name),
                    }
                    for name in sorted(path.name for path in ARTIFACTS.iterdir())
                ],
                "network_actions": 0,
                "credentials_used": False,
                "published": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list-required-inputs",
        action="store_true",
        help="print the exact frozen-input inventory without writing any file",
    )
    args = parser.parse_args()
    if args.list_required_inputs:
        list_required_inputs()
        return
    package()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise
