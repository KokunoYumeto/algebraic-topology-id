#!/usr/bin/env python3
"""Prepare the Roberts 001-030 + Fomberg 001-002 Zenodo payload.

This local-only packager adapts the proved Fomberg 001 packager.  It performs
no Git, network, credential, deposition, or publication action.  The final
reader and backend do not exist when this script is authored, so packaging is
deliberately fail-closed until a final ``frozen-inputs.json`` is created and
its exact SHA-256 is bound below.

The resulting payload has exactly nine files and is reader-first: PDF, offline
HTML, compact editable-source/backend ZIP, compact QA/provenance ZIP, three
rights/reader documents, the generated manifest, and SHA256SUMS.  Fomberg
O012-FOM-001 and O012-FOM-002 remain distinct edition components mapped to
D60-R08 and D60-R09; neither is renumbered as a Roberts lecture.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any


SCRIPT = Path(__file__).resolve()
BASE_PATH = SCRIPT.with_name("package-release-roberts-001-030-fomberg-001.py")
SPEC = importlib.util.spec_from_file_location("o012_fomberg_001_packager", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the proved Fomberg 001 packager")
prior = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prior)

LANE = SCRIPT.parents[1]
RELEASE = LANE / "release" / "zenodo-roberts-001-030-fomberg-001-002"
ARTIFACTS = RELEASE / "artifacts"
STAGING = RELEASE / ".package-staging"
FROZEN_LEDGER = RELEASE / "frozen-inputs.json"
PACKAGE_RECEIPT = RELEASE / "PACKAGE_PREPARATION_RECEIPT.json"

TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30 dan "
    "Jembatan Homologi §1.1–1.4"
)
VERSION = "0.30.2"
RELEASE_ID = "o012-composite-id-roberts-001-030-fomberg-001-002-v0.30.2"
CONCEPT_DOI = "10.5281/zenodo.22061489"
PREVIOUS_RECORD_ID = 22084021
PREVIOUS_DOI = "10.5281/zenodo.22084021"
ROBERTS_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
ROBERTS_TREE = "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5"
FOMBERG_COMMIT = "563194fae879178b9a6871b249513bfc27968975"
FOMBERG_TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"
ORGANIZATION_NAME = "Translation and " + "Transcription Project"
ORGANIZATION_ABBREVIATION = "".join(("T", "T", "P"))
ORGANIZATION_PATTERN = re.compile(
    rf"(?i)\b{re.escape(ORGANIZATION_ABBREVIATION)}\b|"
    rf"{re.escape(ORGANIZATION_NAME)}"
)

# Replace only after the final reader build, backend append, receipts, release
# controls, and all QA are immutable.  A non-digest sentinel makes an
# accidental packaging attempt fail before any staging directory is created.
FROZEN_LEDGER_SHA256 = "06c6f82a770fdbe0f44c3e7ac983c783beb5b1d8fd294b73ae4a66c212e569e4"

PDF_INPUT = (
    "output/pdf/"
    "topologi-aljabar-roberts-001-030-fomberg-001-002-id.pdf"
)
HTML_INPUT = (
    "output/html/roberts-001-030-fomberg-001-002/index.html"
)
ARTIFACT_MANIFEST = (
    "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_002.csv"
)
BUILD_RECEIPT = "qa/ROBERTS_001_030_FOMBERG_001_002_BUILD_RECEIPT.json"
VISUAL_QA = "qa/ROBERTS_001_030_FOMBERG_001_002_VISUAL_QA.md"
RENDER_INVENTORY = (
    "qa/ROBERTS_001_030_FOMBERG_001_002_RENDER_INVENTORY.csv"
)
BACKEND_CUMULATIVE_JSON = (
    "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_002_CUMULATIVE_RECEIPT.json"
)
BACKEND_CUMULATIVE_MD = (
    "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_002_CUMULATIVE_RECEIPT.md"
)
FOMBERG_QA_002 = "qa/FOMBERG_UNIT_002_QA.json"
FOMBERG_READER_001 = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-001-delta-complexes-simplicial-homology.md"
)
FOMBERG_READER_002 = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-002-singular-homology-homotopy-invariance.md"
)

PDF_NAME = (
    "00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_"
    "FOMBERG_001_002_READER.pdf"
)
HTML_NAME = (
    "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_"
    "FOMBERG_001_002_READER.html"
)
SOURCE_ZIP_NAME = (
    "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_002_"
    "EDITABLE_SOURCE_BACKEND.zip"
)
QA_ZIP_NAME = (
    "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_002_"
    "QA_PROVENANCE.zip"
)

FINAL_BOUNDARY_PATHS = {
    PDF_INPUT,
    HTML_INPUT,
    ARTIFACT_MANIFEST,
    BUILD_RECEIPT,
    BACKEND_CUMULATIVE_JSON,
    BACKEND_CUMULATIVE_MD,
}

# Save the proved implementations before replacing release-specific hooks.
_prior_source_entries = prior.source_entries
_prior_qa_path_inventory = prior.qa_path_inventory

# Rebind all generic helpers to the new release lane.  Function global lookups
# in the imported module are dynamic, so its path-safety, hashing, deterministic
# ZIP, frozen-ledger, and parsing implementations remain reusable.
prior.__file__ = str(SCRIPT)
prior.RELEASE = RELEASE
prior.ARTIFACTS = ARTIFACTS
prior.STAGING = STAGING
prior.FROZEN_LEDGER = FROZEN_LEDGER
prior.PACKAGE_RECEIPT = PACKAGE_RECEIPT
prior.TITLE = TITLE
prior.VERSION = VERSION
prior.RELEASE_ID = RELEASE_ID
prior.CONCEPT_DOI = CONCEPT_DOI
prior.PREVIOUS_RECORD_ID = PREVIOUS_RECORD_ID
prior.PREVIOUS_DOI = PREVIOUS_DOI
prior.FROZEN_LEDGER_SHA256 = FROZEN_LEDGER_SHA256
prior.PDF_INPUT = PDF_INPUT
prior.HTML_INPUT = HTML_INPUT
prior.ARTIFACT_MANIFEST = ARTIFACT_MANIFEST
prior.BUILD_RECEIPT = BUILD_RECEIPT
prior.VISUAL_QA = VISUAL_QA
prior.RENDER_INVENTORY = RENDER_INVENTORY
prior.BACKEND_CUMULATIVE_JSON = BACKEND_CUMULATIVE_JSON
prior.BACKEND_CUMULATIVE_MD = BACKEND_CUMULATIVE_MD
prior.PDF_NAME = PDF_NAME
prior.HTML_NAME = HTML_NAME
prior.SOURCE_ZIP_NAME = SOURCE_ZIP_NAME
prior.QA_ZIP_NAME = QA_ZIP_NAME
prior.FINAL_BOUNDARY_PATHS = FINAL_BOUNDARY_PATHS


def source_entries() -> dict[str, Path]:
    """Return the compact, resumable source/backend archive inventory."""
    entries = _prior_source_entries()
    entries.pop("scripts/package-release-roberts-001-030-fomberg-001.py", None)
    entries.update(
        {
            FOMBERG_READER_001: prior.lane_path(FOMBERG_READER_001),
            FOMBERG_READER_002: prior.lane_path(FOMBERG_READER_002),
            "scripts/build-roberts-001-030-fomberg-001-002.ps1": (
                LANE / "scripts" / "build-roberts-001-030-fomberg-001-002.ps1"
            ),
            "scripts/package-release-roberts-001-030-fomberg-001-002.py": SCRIPT,
            "scripts/fomberg-unit-002-common.py": (
                LANE / "scripts" / "fomberg-unit-002-common.py"
            ),
            "scripts/qa-fomberg-unit-002.py": (
                LANE / "scripts" / "qa-fomberg-unit-002.py"
            ),
            "scripts/extend-backend-fomberg-unit-002.py": (
                LANE / "scripts" / "extend-backend-fomberg-unit-002.py"
            ),
            "scripts/validate-backend-append-only-fomberg-unit-002.py": (
                LANE
                / "scripts"
                / "validate-backend-append-only-fomberg-unit-002.py"
            ),
        }
    )
    return entries


def source_path_inventory() -> set[str]:
    # The packager embeds itself in the source ZIP, but cannot be part of the
    # frozen ledger: binding the ledger digest below necessarily changes this
    # file.  Its final identity is recorded in the package receipt instead.
    paths = set(source_entries())
    paths.remove("scripts/package-release-roberts-001-030-fomberg-001-002.py")
    return paths


def qa_path_inventory() -> set[str]:
    paths = set(_prior_qa_path_inventory())
    paths.difference_update(
        {
            "qa/FOMBERG_UNIT_002_SOURCE_AUDIT.md",
            "qa/FOMBERG_UNIT_002_INDEPENDENT_REVIEW.md",
            "qa/FOMBERG_UNIT_002_REVIEW_PART_A.md",
            "qa/FOMBERG_UNIT_002_REVIEW_PART_B.md",
        }
    )
    paths.update(
        {
            FOMBERG_QA_002,
            "qa/FOMBERG_UNIT_002_SOURCE_AUDIT.json",
            "qa/FOMBERG_UNIT_002_INDEPENDENT_REVIEW_DRAFT.md",
            "qa/FOMBERG_UNIT_002_REVIEW_PART_A_DRAFT.md",
            "qa/FOMBERG_UNIT_002_REVIEW_PART_B_DRAFT.md",
            "qa/FOMBERG_UNIT_002_BACKEND_CONTRACT_DRAFT.md",
            "qa/FOMBERG_UNIT_001_QA.json",
            "qa/FOMBERG_UNIT_001_INDEPENDENT_REVIEW.md",
            "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_CUMULATIVE_RECEIPT.json",
            "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_CUMULATIVE_RECEIPT.md",
        }
    )
    return paths


def release_control_inventory() -> set[str]:
    prefix = "release/zenodo-roberts-001-030-fomberg-001-002/"
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


def qa_entries() -> dict[str, Path]:
    entries = {
        relative: prior.lane_path(relative)
        for relative in sorted(qa_path_inventory())
    }
    entries.update(
        {
            "release/frozen-inputs.json": FROZEN_LEDGER,
            "release/frozen-inputs.template.json": (
                RELEASE / "frozen-inputs.template.json"
            ),
            "release/release-manifest.template.json": (
                RELEASE / "release-manifest.template.json"
            ),
            "release/SHA256SUMS.template": RELEASE / "SHA256SUMS.template",
        }
    )
    return entries


def verify_controls() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[str]]:
    names = (
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
    for name in names:
        path = RELEASE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        prior.assert_safe_text(path)
    joined = "\n".join(
        (RELEASE / name).read_text(encoding="utf-8") for name in names
    )
    if re.search(
        r"(?i)(?:Roberts(?:\s+(?:Units?|Lectures?))?|Kuliah Roberts)\s*"
        r"(?:0*1\s*[-–]\s*0*(?:31|32)|0*(?:31|32)\s*/\s*0*(?:31|32))",
        joined,
    ):
        raise RuntimeError("Fomberg was incorrectly renumbered as Roberts 31/32")
    for marker in (
        "30/30",
        "O012-FOM-001",
        "O012-FOM-002",
        "baris 31–1290",
        "baris 1291",
        "CC BY 4.0",
        "CC BY-SA 4.0",
        MODEL_NOTE,
    ):
        if marker not in joined:
            raise RuntimeError(f"public controls omit exact scope marker: {marker}")

    metadata_payload = json.loads(
        (RELEASE / "metadata.json").read_text(encoding="utf-8")
    )
    metadata = metadata_payload.get("metadata", {})
    expected_creators = [
        {"name": "Roberts, David Michael"},
        {"name": "Fomberg, Yeheli"},
    ]
    expected_contributors = [
        {"name": "Lazarovich, Nir", "type": "Other"},
        {"name": "Editor edisi Bahasa Indonesia", "type": "Editor"},
        {"name": ORGANIZATION_NAME, "type": "Other"},
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
        raise RuntimeError("metadata description does not lead with scope truth")
    prose = "\n".join(
        str(metadata.get(field, ""))
        for field in ("title", "description", "notes")
    )
    if ORGANIZATION_PATTERN.search(prose):
        raise RuntimeError("organization marker leaked into title or prose metadata")
    if joined.count(ORGANIZATION_NAME) != 1:
        raise RuntimeError(
            "organization must appear exactly once in contributor metadata"
        )

    plan = json.loads(
        (RELEASE / "publication-plan.json").read_text(encoding="utf-8")
    )
    if (
        plan.get("state") != "prepared_not_published"
        or plan.get("release_id") != RELEASE_ID
        or plan.get("version") != VERSION
        or plan.get("existing_concept_doi") != CONCEPT_DOI
        or plan.get("current_public_record_id") != PREVIOUS_RECORD_ID
        or plan.get("current_public_doi") != PREVIOUS_DOI
        or plan.get("reader_first_filename") != PDF_NAME
        or plan.get("metadata_payload") != "metadata.json"
        or plan.get("payload_directory") != "artifacts"
        or plan.get("publish_not_draft") is not True
        or plan.get("anonymous_byte_readback_required") is not True
    ):
        raise RuntimeError("publication plan does not preserve exact lineage")
    if (
        plan.get("new_concept_allowed")
        or plan.get("new_deposition_created")
        or plan.get("credentials_used")
    ):
        raise RuntimeError("publication plan claims forbidden external action")

    template = json.loads(
        (RELEASE / "release-manifest.template.json").read_text(encoding="utf-8")
    )
    if (
        template.get("release_id") != RELEASE_ID
        or template.get("title") != TITLE
        or template.get("version") != VERSION
        or template.get("status")
        != "roberts_complete_fomberg_units_001_002_complete_composite_course_partial"
    ):
        raise RuntimeError("release manifest template identity/scope drift")
    expected_generated_fields = [
        "metadata_sha256",
        "publication_plan_sha256",
        "frozen_input_ledger",
        "sources",
        "reader_qa",
        "backend",
        "archives",
        "artifacts",
        "privacy",
        "production_provenance",
        "credentials_used",
        "network_actions",
    ]
    if template.get("generated_fields") != expected_generated_fields:
        raise RuntimeError("release manifest generated-field inventory drift")
    expected_upload = [
        PDF_NAME,
        HTML_NAME,
        SOURCE_ZIP_NAME,
        QA_ZIP_NAME,
        "LICENSE.md",
        "README_RELEASE.md",
        "RELEASE_RIGHTS.md",
    ]
    if template.get("artifact_order") != expected_upload:
        raise RuntimeError("release manifest is not reader-first")

    checksum_names: list[str] = []
    for line in (RELEASE / "SHA256SUMS.template").read_text(
        encoding="utf-8"
    ).splitlines():
        marker, separator, name = line.partition("  ")
        if marker != "<sha256>" or not separator or not name:
            raise RuntimeError("malformed SHA256SUMS.template")
        checksum_names.append(name)
    if checksum_names != expected_upload + ["release-manifest.json"]:
        raise RuntimeError("checksum template inventory/order mismatch")

    frozen_template = json.loads(
        (RELEASE / "frozen-inputs.template.json").read_text(encoding="utf-8")
    )
    if (
        frozen_template.get("schema_version") != "1.0"
        or frozen_template.get("release_id") != RELEASE_ID
        or frozen_template.get("state") != "template_unsealed_do_not_package"
        or frozen_template.get("entries") != []
        or len(frozen_template.get("final_boundary_paths", []))
        != len(FINAL_BOUNDARY_PATHS)
        or set(frozen_template.get("final_boundary_paths", []))
        != FINAL_BOUNDARY_PATHS
    ):
        raise RuntimeError("frozen-input template identity/boundary drift")
    return metadata, plan, template, checksum_names


def verify_build_receipt(
    artifact_rows: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    receipt = json.loads(prior.lane_path(BUILD_RECEIPT).read_text(encoding="utf-8"))
    if (
        receipt.get("status") != "PASS"
        or receipt.get("qa_id")
        != "O012-RBT-001-030-FOM-001-002-COMPOSITE-BUILD"
    ):
        raise RuntimeError("composite build receipt identity/status mismatch")
    numbering = receipt.get("component_numbering", {})
    if (
        numbering.get("roberts_edition_units") != "001-030"
        or numbering.get("fomberg_component_ids")
        != ["O012-FOM-001", "O012-FOM-002"]
        or numbering.get("course_route_unit_ids") != ["D60-R08", "D60-R09"]
        or numbering.get("fomberg_is_not_roberts_units_031_032") is not True
    ):
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
        or fomberg.get("selected_source_span") != "31-1290"
        or fomberg.get("selected_span_lines") != 1260
        or fomberg.get("next_source_line") != 1291
        or fomberg.get("license") != "CC BY-SA 4.0"
    ):
        raise RuntimeError("composite build authority/span/license mismatch")
    artifacts = receipt.get("artifacts", {})
    for role, relative in (
        ("pdf", PDF_INPUT),
        ("html", HTML_INPUT),
        ("manifest", ARTIFACT_MANIFEST),
    ):
        if not prior.identity_matches(artifacts.get(role), prior.lane_path(relative)):
            raise RuntimeError(f"build receipt {role} does not bind final bytes")
    for relative, row in artifact_rows.items():
        actual = prior.lane_path(relative)
        if actual.stat().st_size != row["bytes"] or prior.sha(actual) != row["sha256"]:
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
        raise RuntimeError("offline HTML gate is incomplete")
    reproducibility = receipt.get("reproducibility", {})
    if any(
        reproducibility.get(key) is not True
        for key in (
            "html_two_builds_byte_identical",
            "pdf_two_builds_byte_identical",
            "build_scratch_removed",
            "reader_and_backend_unchanged",
        )
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
        or rights.get("model_provenance") != MODEL_NOTE
    ):
        raise RuntimeError("composite rights/provenance gate is incomplete")
    visual = receipt.get("visual_checks", {})
    if visual.get("status") != "PASS":
        raise RuntimeError("composite visual QA did not pass")
    if not prior.identity_matches(
        visual.get("render_inventory"), prior.lane_path(RENDER_INVENTORY)
    ):
        raise RuntimeError("render inventory identity mismatch")
    if not prior.identity_matches(
        visual.get("visual_receipt"), prior.lane_path(VISUAL_QA)
    ):
        raise RuntimeError("visual QA identity mismatch")
    return receipt


def verify_fomberg_qa() -> dict[str, Any]:
    qa = json.loads(prior.lane_path(FOMBERG_QA_002).read_text(encoding="utf-8"))
    if (
        qa.get("status") != "PASS"
        or qa.get("qa_id") != "O012-FOMBERG-UNIT-002-STATIC-QA"
    ):
        raise RuntimeError("Fomberg Unit 002 static QA did not pass")
    authority = qa.get("authority", {})
    span = authority.get("unit_span", {})
    if (
        authority.get("commit") != FOMBERG_COMMIT
        or authority.get("tree") != FOMBERG_TREE
        or authority.get("next_source_line") != 1291
        or span.get("line_start") != 615
        or span.get("line_end") != 1290
        or authority.get("terminal_source_eof") is not False
    ):
        raise RuntimeError("Fomberg Unit 002 source boundary mismatch")
    if not prior.identity_matches(
        qa.get("reader"), prior.lane_path(FOMBERG_READER_002)
    ):
        raise RuntimeError("Fomberg QA does not bind the translated reader")
    checks = qa.get("checks", {})
    required = (
        "reader_identity_44407_bytes_1342_lf_lines",
        "reader_sha256_0851ab7d",
        "source_full_and_span_identity",
        "cursor_line_1291",
        "unique_95_stable_ids",
        "balanced_90_fenced_divs",
        "fourteen_diagram_functions_and_blocks",
        "fom_pr_01_02_03_closed",
        "six_exercise_hint_solution_triples",
        "three_reviews_p1_p2_p3_zero_and_pass",
        "pandoc_parse_available_and_pass",
        "inputs_not_modified",
        "backend_write_deferred",
    )
    if any(checks.get(name) is not True for name in required):
        raise RuntimeError("Fomberg Unit 002 static QA gate is incomplete")
    if (
        qa.get("structure", {}).get("stable_id_count") != 95
        or qa.get("mastery", {}).get("triples") != 6
        or qa.get("model_provenance") != MODEL_NOTE
    ):
        raise RuntimeError("Fomberg Unit 002 QA structure/provenance drift")
    return qa


def verify_backend_receipt(backend_facts: dict[str, Any]) -> dict[str, Any]:
    receipt = json.loads(
        prior.lane_path(BACKEND_CUMULATIVE_JSON).read_text(encoding="utf-8")
    )
    if (
        receipt.get("status") != "PASS"
        or receipt.get("receipt_id")
        != "O012-BACKEND-THROUGH-FOMBERG-UNIT-002-CUMULATIVE-SEMANTIC"
    ):
        raise RuntimeError("Fomberg Unit 002 cumulative backend receipt failed")
    current = receipt.get("current", {})
    expected = {
        key: backend_facts[key]
        for key in ("total_records", "total_bytes", "bundle_sha256")
    }
    if {key: current.get(key) for key in expected} != expected:
        raise RuntimeError("backend receipt does not bind the live backend")
    if (
        current.get("next_source_line") != 1291
        or current.get("terminal_source_eof") is not False
        or current.get("stable_ids") != 182
        or current.get("mastery_triples") != 12
    ):
        raise RuntimeError("cumulative backend semantic boundary mismatch")
    prefix = receipt.get("nested_immutability", {}).get(
        "roberts_units_001_030_prefix", {}
    )
    if (
        prefix.get("preserved_byte_for_byte") is not True
        or prefix.get("records") != 4761
        or prefix.get("bundle_sha256")
        != "51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920"
    ):
        raise RuntimeError("Roberts backend prefix was not preserved")
    if not prior.identity_matches(
        receipt.get("human_receipt"), prior.lane_path(BACKEND_CUMULATIVE_MD)
    ):
        raise RuntimeError("backend human receipt identity mismatch")
    return receipt


def write_package_receipt(
    frozen: dict[str, dict[str, Any]],
    source_zip: dict[str, Any],
    qa_zip: dict[str, Any],
) -> None:
    files = [
        {
            "filename": path.name,
            "bytes": path.stat().st_size,
            "sha256": prior.sha(path),
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
            "Roberts 30/30 complete; Fomberg O012-FOM-001 and "
            "O012-FOM-002 (Sections 1.1-1.4, lines 31-1290) complete; "
            "next Fomberg line 1291; composite course partial"
        ),
        "release_directory": RELEASE.relative_to(LANE).as_posix(),
        "reader_first_filename": PDF_NAME,
        "frozen_input_ledger": {
            **prior.identity(FROZEN_LEDGER),
            "entries": len(frozen),
        },
        "packager": prior.identity(SCRIPT),
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
    prior.write_json(temporary, payload)
    temporary.replace(PACKAGE_RECEIPT)


def package() -> None:
    if not RELEASE.is_dir():
        raise RuntimeError("release controls must exist before packaging")
    if ARTIFACTS.exists():
        raise RuntimeError("artifacts directory already exists; refusing to overwrite")
    if STAGING.exists():
        raise RuntimeError("stale package staging exists; inspect it explicitly")

    metadata, plan, manifest_template, checksum_names = verify_controls()
    frozen = prior.load_frozen_inputs()
    artifact_rows = prior.parse_artifact_manifest()
    build_receipt = verify_build_receipt(artifact_rows)
    fomberg_qa = verify_fomberg_qa()
    backend_facts = prior.verify_backend()
    backend_receipt = verify_backend_receipt(backend_facts)

    source = source_entries()
    qa = qa_entries()
    prior.assert_source_archive_link_closure(source)
    frozen_paths = set(frozen)
    for archive_name, entries in ((SOURCE_ZIP_NAME, source), (QA_ZIP_NAME, qa)):
        for name, path in entries.items():
            relative = path.relative_to(LANE).as_posix()
            if path.resolve() in {SCRIPT.resolve(), FROZEN_LEDGER.resolve()}:
                continue
            if relative not in frozen_paths:
                raise RuntimeError(
                    f"unfrozen {archive_name} input: {name} <- {relative}"
                )

    STAGING.mkdir(parents=False)
    try:
        source_zip = prior.deterministic_zip(STAGING / SOURCE_ZIP_NAME, source)
        qa_zip = prior.deterministic_zip(STAGING / QA_ZIP_NAME, qa)
        copies = {
            PDF_NAME: prior.lane_path(PDF_INPUT),
            HTML_NAME: prior.lane_path(HTML_INPUT),
            "LICENSE.md": RELEASE / "LICENSE.md",
            "README_RELEASE.md": RELEASE / "README_RELEASE.md",
            "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md",
        }
        prior.assert_safe_text(copies[HTML_NAME])
        for name, source_path in copies.items():
            shutil.copyfile(source_path, STAGING / name)

        upload_files = list(manifest_template["artifact_order"])
        manifest = dict(manifest_template)
        manifest.pop("template_state", None)
        manifest.pop("generated_fields", None)
        manifest.update(
            {
                "metadata_sha256": prior.sha(RELEASE / "metadata.json"),
                "publication_plan_sha256": prior.sha(
                    RELEASE / "publication-plan.json"
                ),
                "frozen_input_ledger": {
                    **prior.identity(FROZEN_LEDGER),
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
                        "line_end": 1290,
                        "sections": "1.1-1.4",
                        "component_ids": ["O012-FOM-001", "O012-FOM-002"],
                        "course_route_unit_ids": ["D60-R08", "D60-R09"],
                        "component_boundaries": {
                            "O012-FOM-001": "31-614",
                            "O012-FOM-002": "615-1290",
                        },
                        "next_source_line": 1291,
                        "complete_at_selected_boundary": True,
                        "license": "CC BY-SA 4.0",
                    },
                    "composite_course_complete": False,
                },
                "reader_qa": {
                    "status": "PASS",
                    "pdf_pages": build_receipt["artifacts"]["pdf"]["pages"],
                    "pdf_tagged": build_receipt["artifacts"]["pdf"]["tagged"],
                    "pdf_all_fonts_embedded_subset_tounicode": build_receipt[
                        "artifacts"
                    ]["pdf"]["all_fonts_embedded_subset_tounicode"],
                    "html_unique_dom_ids": build_receipt["html_checks"][
                        "unique_dom_ids"
                    ],
                    "html_fragment_links": build_receipt["html_checks"][
                        "fragment_links"
                    ],
                    "html_mathml_nodes": build_receipt["html_checks"][
                        "mathml_nodes"
                    ],
                    "html_self_contained": build_receipt["html_checks"][
                        "self_contained"
                    ],
                    "fomberg_stable_ids_total": 182,
                    "fomberg_unit_002_stable_ids": fomberg_qa["structure"][
                        "stable_id_count"
                    ],
                    "mastery_triples_total": 12,
                    "fomberg_unit_002_mastery_triples": fomberg_qa["mastery"][
                        "triples"
                    ],
                    "visual_status": build_receipt["visual_checks"]["status"],
                    "browser_checks": build_receipt.get("browser_checks", {}),
                    "pdf_untagged_limitation_disclosed": True,
                },
                "backend": {
                    **backend_facts,
                    "cumulative_receipt": prior.identity(
                        prior.lane_path(BACKEND_CUMULATIVE_JSON)
                    ),
                    "cumulative_human_receipt": prior.identity(
                        prior.lane_path(BACKEND_CUMULATIVE_MD)
                    ),
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
                {
                    "filename": name,
                    "bytes": path.stat().st_size,
                    "sha256": prior.sha(path),
                }
            )
        prior.write_json(STAGING / "release-manifest.json", manifest)

        sums = "\n".join(
            f"{prior.sha(STAGING / name)}  {name}" for name in checksum_names
        ) + "\n"
        (STAGING / "SHA256SUMS").write_text(
            sums, encoding="utf-8", newline="\n"
        )

        expected_names = sorted(checksum_names + ["SHA256SUMS"])
        actual_names = sorted(
            path.name for path in STAGING.iterdir() if path.is_file()
        )
        if actual_names != expected_names:
            raise RuntimeError(f"staged payload inventory mismatch: {actual_names}")
        for name in actual_names:
            path = STAGING / name
            if path.suffix.lower() not in {".pdf", ".zip"}:
                prior.assert_safe_text(path)
        parsed_sums: dict[str, str] = {}
        for line in (STAGING / "SHA256SUMS").read_text(
            encoding="utf-8"
        ).splitlines():
            digest, name = line.split("  ", 1)
            if name in parsed_sums:
                raise RuntimeError(f"duplicate checksum row: {name}")
            parsed_sums[name] = digest
        expected_sums = {
            name: prior.sha(STAGING / name) for name in checksum_names
        }
        if parsed_sums != expected_sums:
            raise RuntimeError("SHA256SUMS does not bind every payload file")
        for row in manifest["artifacts"]:
            path = STAGING / row["filename"]
            if (
                path.stat().st_size != row["bytes"]
                or prior.sha(path) != row["sha256"]
            ):
                raise RuntimeError(f"manifest artifact mismatch: {path.name}")

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
                "scope": (
                    "Roberts 30/30 + Fomberg O012-FOM-001/002 through line "
                    "1290; composite course partial"
                ),
                "files": [
                    {
                        "filename": name,
                        "bytes": (ARTIFACTS / name).stat().st_size,
                        "sha256": prior.sha(ARTIFACTS / name),
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


# Install release-specific hooks for the imported frozen-ledger helpers.
prior.source_entries = source_entries
prior.source_path_inventory = source_path_inventory
prior.qa_path_inventory = qa_path_inventory
prior.release_control_inventory = release_control_inventory
prior.required_frozen_paths = required_frozen_paths
prior.qa_entries = qa_entries
prior.verify_controls = verify_controls
prior.verify_build_receipt = verify_build_receipt
prior.verify_fomberg_qa = verify_fomberg_qa
prior.verify_backend_receipt = verify_backend_receipt
prior.write_package_receipt = write_package_receipt
prior.package = package


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list-required-inputs",
        action="store_true",
        help="print the exact frozen-input inventory without writing files",
    )
    args = parser.parse_args()
    if args.list_required_inputs:
        prior.list_required_inputs()
        return
    package()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise
