#!/usr/bin/env python3
"""Prepare the Roberts 001-030 + Fomberg 001-005 Zenodo payload.

This packager is local-only.  It performs no Git, network, credential,
deposition, or publication action.  It reuses the proved deterministic ZIP,
path-safety, hashing, and frozen-input machinery from the prior checkpoint,
but binds the new Fomberg source boundary independently.

The script is deliberately unsealed while ``publication-plan.json`` has
``artifact_identities_known: false`` or ``FROZEN_LEDGER_SHA256`` is not a
digest.  Use ``--list-required-inputs`` at any time; packaging itself succeeds
only after final backend/build/visual receipts and a complete frozen-input
ledger bind the exact bytes.
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
BASE_PATH = SCRIPT.with_name(
    "package-release-roberts-001-030-fomberg-001-004.py"
)
SPEC = importlib.util.spec_from_file_location("o012_fomberg_004_packager", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the proved Fomberg 001-004 packager")
previous = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(previous)
base = previous.base

LANE = SCRIPT.parents[1]
RELEASE = LANE / "release" / "zenodo-roberts-001-030-fomberg-001-005"
ARTIFACTS = RELEASE / "artifacts"
STAGING = RELEASE / ".package-staging"
FROZEN_LEDGER = RELEASE / "frozen-inputs.json"
PACKAGE_RECEIPT = RELEASE / "PACKAGE_PREPARATION_RECEIPT.json"

TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30 dan "
    "Jembatan Homologi dan Derajat §1.1–1.11"
)
VERSION = "0.30.5"
RELEASE_ID = "o012-composite-id-roberts-001-030-fomberg-001-005-v0.30.5"
CONCEPT_DOI = "10.5281/zenodo.22061489"
PREVIOUS_RECORD_ID = 22097007
PREVIOUS_DOI = "10.5281/zenodo.22097007"
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

# Bound only after all 187 required inputs existed, the final build/backend/
# visual receipts passed, and frozen-inputs.json was generated from live bytes.
FROZEN_LEDGER_SHA256 = "0e70627c22d0b0d2e6432517f413dc890b4a4e47fa9b5661b96a10fc500f3ba4"

PDF_INPUT = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-005-id.pdf"
HTML_INPUT = "output/html/roberts-001-030-fomberg-001-005/index.html"
ARTIFACT_MANIFEST = "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_005.csv"
BUILD_RECEIPT = "qa/ROBERTS_001_030_FOMBERG_001_005_BUILD_RECEIPT.json"
VISUAL_QA = "qa/ROBERTS_001_030_FOMBERG_001_005_VISUAL_QA.md"
RENDER_INVENTORY = "qa/ROBERTS_001_030_FOMBERG_001_005_RENDER_INVENTORY.csv"
BACKEND_CUMULATIVE_JSON = (
    "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_005_CUMULATIVE_RECEIPT.json"
)
BACKEND_CUMULATIVE_MD = (
    "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_005_CUMULATIVE_RECEIPT.md"
)
FOMBERG_QA_005 = "qa/FOMBERG_UNIT_005_QA.json"
FOMBERG_SOURCE_AUDIT_005 = "qa/FOMBERG_UNIT_005_SOURCE_AUDIT.json"
FOMBERG_REVIEW_005 = "qa/fomberg-unit-005/INDEPENDENT_REVIEW_FINAL.json"
FOMBERG_READER_005 = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-005-degree-maps-local-degree.md"
)
FOMBERG_READER_005_SHA256 = (
    "ad6e31291e3df97b81f7e5a30144ca27157f907291e74f4d49c09a0620487075"
)
FOMBERG_UNIT_005_SOURCE_SHA256 = (
    "9ac1d27872a09134b75bb077ad113716a9e828c2177ac296e7bf3331395da85a"
)
FOMBERG_ASSETS_005: tuple[str, ...] = ()

PDF_NAME = (
    "00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_"
    "FOMBERG_001_005_READER.pdf"
)
HTML_NAME = (
    "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_"
    "FOMBERG_001_005_READER.html"
)
SOURCE_ZIP_NAME = (
    "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_005_"
    "EDITABLE_SOURCE_BACKEND.zip"
)
QA_ZIP_NAME = (
    "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_005_"
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

_previous_source_entries = previous.source_entries
_previous_qa_path_inventory = previous.qa_path_inventory

# Rebind generic helper state.  Imported helper functions resolve these globals
# dynamically, preserving the proved path and frozen-ledger checks.
base.__file__ = str(SCRIPT)
base.RELEASE = RELEASE
base.ARTIFACTS = ARTIFACTS
base.STAGING = STAGING
base.FROZEN_LEDGER = FROZEN_LEDGER
base.PACKAGE_RECEIPT = PACKAGE_RECEIPT
base.TITLE = TITLE
base.VERSION = VERSION
base.RELEASE_ID = RELEASE_ID
base.CONCEPT_DOI = CONCEPT_DOI
base.PREVIOUS_RECORD_ID = PREVIOUS_RECORD_ID
base.PREVIOUS_DOI = PREVIOUS_DOI
base.FROZEN_LEDGER_SHA256 = FROZEN_LEDGER_SHA256
base.PDF_INPUT = PDF_INPUT
base.HTML_INPUT = HTML_INPUT
base.ARTIFACT_MANIFEST = ARTIFACT_MANIFEST
base.BUILD_RECEIPT = BUILD_RECEIPT
base.VISUAL_QA = VISUAL_QA
base.RENDER_INVENTORY = RENDER_INVENTORY
base.BACKEND_CUMULATIVE_JSON = BACKEND_CUMULATIVE_JSON
base.BACKEND_CUMULATIVE_MD = BACKEND_CUMULATIVE_MD
base.PDF_NAME = PDF_NAME
base.HTML_NAME = HTML_NAME
base.SOURCE_ZIP_NAME = SOURCE_ZIP_NAME
base.QA_ZIP_NAME = QA_ZIP_NAME
base.FINAL_BOUNDARY_PATHS = FINAL_BOUNDARY_PATHS


def source_entries() -> dict[str, Path]:
    """Compact resumable source/backend inventory, including Unit005 once."""
    entries = _previous_source_entries()
    entries.update(
        {
            FOMBERG_READER_005: base.lane_path(FOMBERG_READER_005),
            **{
                relative: base.lane_path(relative)
                for relative in FOMBERG_ASSETS_005
            },
            "scripts/build-roberts-001-030-fomberg-001-005.ps1": (
                LANE / "scripts" / "build-roberts-001-030-fomberg-001-005.ps1"
            ),
            "scripts/assemble-fomberg-unit-005.py": (
                LANE / "scripts" / "assemble-fomberg-unit-005.py"
            ),
            "scripts/fomberg-unit-005-common.py": (
                LANE / "scripts" / "fomberg-unit-005-common.py"
            ),
            "scripts/qa-fomberg-unit-005.py": (
                LANE / "scripts" / "qa-fomberg-unit-005.py"
            ),
            "scripts/extend-backend-fomberg-unit-005.py": (
                LANE / "scripts" / "extend-backend-fomberg-unit-005.py"
            ),
            "scripts/validate-backend-append-only-fomberg-unit-005.py": (
                LANE
                / "scripts"
                / "validate-backend-append-only-fomberg-unit-005.py"
            ),
            "scripts/validate-backend-append-only-fomberg-unit-005-cumulative.py": (
                LANE
                / "scripts"
                / "validate-backend-append-only-fomberg-unit-005-cumulative.py"
            ),
            "scripts/package-release-roberts-001-030-fomberg-001-005.py": SCRIPT,
            "scripts/publish-zenodo-roberts-001-030-fomberg-001-005.py": (
                LANE
                / "scripts"
                / "publish-zenodo-roberts-001-030-fomberg-001-005.py"
            ),
        }
    )
    return entries


def source_path_inventory() -> set[str]:
    paths = set(source_entries())
    # Binding the frozen-ledger hash necessarily changes this script; its final
    # identity is recorded by the package receipt instead.
    paths.remove("scripts/package-release-roberts-001-030-fomberg-001-005.py")
    return paths


def qa_path_inventory() -> set[str]:
    paths = set(_previous_qa_path_inventory())
    paths.update(
        {
            FOMBERG_QA_005,
            FOMBERG_SOURCE_AUDIT_005,
            FOMBERG_REVIEW_005,
            "qa/fomberg-unit-005/TERMINOLOGY_ROWS_DRAFT.csv",
            "qa/fomberg-unit-005/ADVERSE_ROWS_DRAFT.csv",
            "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_005_FILE_MANIFEST.csv",
            "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_005_RECEIPT.json",
            "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_005_RECEIPT.md",
            BACKEND_CUMULATIVE_JSON,
            BACKEND_CUMULATIVE_MD,
            "qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_005_REPLAY_RECEIPT.json",
            BUILD_RECEIPT,
            VISUAL_QA,
            RENDER_INVENTORY,
        }
    )
    return paths


def release_control_inventory() -> set[str]:
    prefix = "release/zenodo-roberts-001-030-fomberg-001-005/"
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
        relative: base.lane_path(relative)
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
        base.assert_safe_text(path)
    joined = "\n".join(
        (RELEASE / name).read_text(encoding="utf-8") for name in names
    )
    if re.search(
        r"(?i)(?:Roberts(?:\s+(?:Units?|Lectures?))?|Kuliah Roberts)\s*"
        r"(?:0*1\s*[-–]\s*0*3[1-5]|0*3[1-5]\s*/\s*0*3[1-5])",
        joined,
    ):
        raise RuntimeError("Fomberg was incorrectly renumbered as Roberts 31-35")
    for marker in (
        "30/30",
        "O012-FOM-001",
        "O012-FOM-002",
        "O012-FOM-003",
        "O012-FOM-004",
        "O012-FOM-005",
        "baris 31–3122",
        "baris 3123",
        "D60-R11",
        "D60-R12",
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
        or metadata.get("access_right") != "open"
        or metadata.get("creators") != expected_creators
        or metadata.get("contributors") != expected_contributors
    ):
        raise RuntimeError("metadata identity, rights, creator, or contributor drift")
    if not str(metadata.get("description", "")).startswith(
        "<p><strong>Status: checkpoint parsial kursus komposit; korpus Roberts lengkap 30/30"
    ):
        raise RuntimeError("metadata description does not lead with scope truth")
    prose = "\n".join(
        str(metadata.get(field, ""))
        for field in ("title", "description", "notes")
    ) + "\n" + "\n".join(str(item) for item in metadata.get("keywords", []))
    if ORGANIZATION_PATTERN.search(prose):
        raise RuntimeError("organization marker leaked into title or prose metadata")
    if joined.count(ORGANIZATION_NAME) != 1:
        raise RuntimeError("organization must appear exactly once in contributor metadata")

    plan = json.loads(
        (RELEASE / "publication-plan.json").read_text(encoding="utf-8")
    )
    if (
        plan.get("state") != "prepared_not_published"
        or plan.get("artifact_identities_known") is not True
    ):
        raise RuntimeError(
            "release remains intentionally unsealed: final reader/backend "
            "identities and passing receipts must be bound first"
        )
    if (
        plan.get("release_id") != RELEASE_ID
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
        raise RuntimeError("publication plan escaped the exact concept lineage")
    if (
        plan.get("new_concept_allowed")
        or plan.get("new_deposition_created")
        or plan.get("credentials_used")
    ):
        raise RuntimeError("publication plan claims forbidden external action")
    backend_binding = plan.get("backend_binding", {})
    snapshot = backend_binding.get("verified_snapshot")
    if (
        backend_binding.get("final_identity_source") != BACKEND_CUMULATIVE_JSON
        or backend_binding.get("hardcoded_final_identity") is not False
        or not isinstance(backend_binding.get("expected_records"), int)
        or backend_binding.get("expected_records") <= 6113
        or not isinstance(snapshot, dict)
        or snapshot.get("total_records") != backend_binding.get("expected_records")
        or not isinstance(snapshot.get("total_bytes"), int)
        or not re.fullmatch(r"[0-9a-f]{64}", str(snapshot.get("bundle_sha256", "")))
    ):
        raise RuntimeError("publication plan backend binding is not sealed")
    readers = plan.get("final_reader_artifacts")
    if not isinstance(readers, dict) or set(readers) != {"html", "pdf"}:
        raise RuntimeError("publication plan reader identities are not sealed")
    for role, relative in (("html", HTML_INPUT), ("pdf", PDF_INPUT)):
        row = readers.get(role, {})
        if row.get("path") != relative or not base.identity_matches(
            row, base.lane_path(relative)
        ):
            raise RuntimeError(f"publication plan does not bind final {role} bytes")
    if not isinstance(readers["pdf"].get("pages"), int) or readers["pdf"]["pages"] <= 424:
        raise RuntimeError("publication plan PDF page count is not final")

    template = json.loads(
        (RELEASE / "release-manifest.template.json").read_text(encoding="utf-8")
    )
    if (
        template.get("release_id") != RELEASE_ID
        or template.get("title") != TITLE
        or template.get("version") != VERSION
        or template.get("status")
        != "roberts_complete_fomberg_units_001_005_complete_composite_course_partial"
    ):
        raise RuntimeError("release manifest template identity/scope drift")
    numbering = template.get("component_numbering", {})
    if (
        numbering.get("roberts_edition_units") != "001-030"
        or numbering.get("fomberg_component_ids")
        != [
            "O012-FOM-001",
            "O012-FOM-002",
            "O012-FOM-003",
            "O012-FOM-004",
            "O012-FOM-005",
        ]
        or numbering.get("course_route_unit_ids")
        != ["D60-R08", "D60-R09", "D60-R10", "D60-R11", "D60-R12"]
        or numbering.get("fomberg_is_not_roberts_units_031_035") is not True
    ):
        raise RuntimeError("release manifest component numbering drift")
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
        or set(frozen_template.get("final_boundary_paths", []))
        != FINAL_BOUNDARY_PATHS
    ):
        raise RuntimeError("frozen-input template identity/boundary drift")
    return metadata, plan, template, checksum_names


def verify_build_receipt(artifact_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    receipt = json.loads(base.lane_path(BUILD_RECEIPT).read_text(encoding="utf-8"))
    if (
        receipt.get("status") != "PASS"
        or receipt.get("qa_id")
        != "O012-RBT-001-030-FOM-001-005-COMPOSITE-BUILD"
    ):
        raise RuntimeError("composite build receipt identity/status mismatch")
    numbering = receipt.get("component_numbering", {})
    if (
        numbering.get("roberts_edition_units") != "001-030"
        or numbering.get("fomberg_component_ids")
        != [
            "O012-FOM-001",
            "O012-FOM-002",
            "O012-FOM-003",
            "O012-FOM-004",
            "O012-FOM-005",
        ]
        or numbering.get("course_route_unit_ids")
        != ["D60-R08", "D60-R09", "D60-R10", "D60-R11", "D60-R12"]
        or numbering.get("fomberg_is_not_roberts_units_031_035") is not True
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
        or fomberg.get("selected_source_span") != "31-3122"
        or fomberg.get("selected_span_lines") != 3092
        or fomberg.get("next_source_line") != 3123
        or fomberg.get("license") != "CC BY-SA 4.0"
    ):
        raise RuntimeError("composite build authority/span/license mismatch")
    artifacts = receipt.get("artifacts", {})
    for role, relative in (
        ("pdf", PDF_INPUT),
        ("html", HTML_INPUT),
        ("manifest", ARTIFACT_MANIFEST),
    ):
        if not base.identity_matches(artifacts.get(role), base.lane_path(relative)):
            raise RuntimeError(f"build receipt {role} does not bind final bytes")
    for relative, row in artifact_rows.items():
        actual = base.lane_path(relative)
        if actual.stat().st_size != row["bytes"] or base.sha(actual) != row["sha256"]:
            raise RuntimeError(f"reader artifact/CSV mismatch: {relative}")
    html = receipt.get("html_checks", {})
    if (
        html.get("status") != "PASS"
        or html.get("self_contained") is not True
        or html.get("runtime_external_asset_references") != 0
        or html.get("raw_tex_math_fallbacks") != 0
        or html.get("live_browser_dom_ids")
        != html.get("live_browser_unique_dom_ids")
        or html.get("unresolved_fragment_links") != 0
        or html.get("missing_fomberg_stable_ids") != 0
    ):
        raise RuntimeError("offline HTML gate is incomplete")
    reproducibility = receipt.get("reproducibility", {})
    if (
        reproducibility.get("html_builds_byte_identical") is not True
        or reproducibility.get("pdf_builds_byte_identical") is not True
        or reproducibility.get("build_scratch_removed") is not True
        or reproducibility.get("protected_prior_composite_unchanged") is not True
        or reproducibility.get("backend_append_only_prefix_unchanged") is not True
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
    if not base.identity_matches(
        visual.get("render_inventory"), base.lane_path(RENDER_INVENTORY)
    ):
        raise RuntimeError("render inventory identity mismatch")
    if not base.identity_matches(
        visual.get("visual_receipt"), base.lane_path(VISUAL_QA)
    ):
        raise RuntimeError("visual QA identity mismatch")
    plan = json.loads((RELEASE / "publication-plan.json").read_text(encoding="utf-8"))
    readers = plan["final_reader_artifacts"]
    if (
        readers["pdf"].get("pages") != artifacts["pdf"].get("pages")
        or not base.identity_matches(readers["pdf"], base.lane_path(PDF_INPUT))
        or not base.identity_matches(readers["html"], base.lane_path(HTML_INPUT))
    ):
        raise RuntimeError("publication plan/build receipt reader identity drift")
    return receipt


def verify_fomberg_qa() -> dict[str, Any]:
    qa = json.loads(base.lane_path(FOMBERG_QA_005).read_text(encoding="utf-8"))
    if (
        qa.get("status") != "PASS"
        or qa.get("qa_id") != "O012-FOMBERG-UNIT-005-STATIC-QA"
        or qa.get("model_provenance") != MODEL_NOTE
    ):
        raise RuntimeError("Fomberg Unit005 static QA did not pass")
    source = qa.get("source", {})
    span = source.get("selected_span", {})
    if (
        source.get("commit") != FOMBERG_COMMIT
        or source.get("tree") != FOMBERG_TREE
        or source.get("next_line") != 3123
        or source.get("next_line_text") != r"\subsection{Cellular complexes}"
        or span.get("line_start") != 2847
        or span.get("line_end") != 3122
        or span.get("lf_lines") != 276
        or span.get("sha256") != FOMBERG_UNIT_005_SOURCE_SHA256
    ):
        raise RuntimeError("Fomberg Unit005 source boundary mismatch")
    reader = qa.get("reader", {})
    if not base.identity_matches(reader.get("identity"), base.lane_path(FOMBERG_READER_005)):
        raise RuntimeError("Fomberg QA does not bind translated Unit005")
    if reader.get("identity", {}).get("sha256") != FOMBERG_READER_005_SHA256:
        raise RuntimeError("Fomberg Unit005 canonical reader identity drift")
    if (
        reader.get("stable_ids") != 52
        or reader.get("stable_ids_unique") != 52
        or reader.get("mastery", {}).get("exercise_hint_solution_triples") != 6
        or reader.get("mastery", {}).get("complete_solutions") != 6
        or reader.get("assets", {}).get("raster_redraws") != 0
        or reader.get("assets", {}).get("semantic_figures") != 1
        or reader.get("assets", {}).get("semantic_reflow_provenance_present")
        is not True
        or reader.get("assets", {}).get("source_tikzcd_occurrences") != 2
        or reader.get("proof_repairs") != ["FOM-PR-12"]
    ):
        raise RuntimeError("Fomberg Unit005 structure/mastery/proof closure drift")
    if any(value != "PASS" for value in qa.get("gates", {}).values()):
        raise RuntimeError("Fomberg Unit005 QA gate is incomplete")
    if qa.get("independent_review", {}).get("severity_census") != {
        "P1": 0,
        "P2": 0,
        "P3": 0,
    }:
        raise RuntimeError("Fomberg Unit005 independent review is not zero-severity")
    if FOMBERG_ASSETS_005:
        raise RuntimeError("Unit005 must not introduce external raster/vector assets")
    if not base.identity_matches(qa.get("source_audit"), base.lane_path(FOMBERG_SOURCE_AUDIT_005)):
        raise RuntimeError("Fomberg Unit005 source-audit identity drift")
    if not base.identity_matches(
        qa.get("independent_review", {}).get("identity"),
        base.lane_path(FOMBERG_REVIEW_005),
    ):
        raise RuntimeError("Fomberg Unit005 independent-review identity drift")
    return qa


def verify_backend_receipt(backend_facts: dict[str, Any]) -> dict[str, Any]:
    receipt = json.loads(
        base.lane_path(BACKEND_CUMULATIVE_JSON).read_text(encoding="utf-8")
    )
    if (
        receipt.get("status") != "PASS"
        or receipt.get("receipt_id")
        != "O012-BACKEND-THROUGH-FOMBERG-UNIT-005-CUMULATIVE-SEMANTIC"
    ):
        raise RuntimeError("Fomberg Unit005 cumulative backend receipt failed")
    current = receipt.get("current", {})
    expected = {
        key: backend_facts[key]
        for key in ("total_records", "total_bytes", "bundle_sha256")
    }
    if {key: current.get(key) for key in expected} != expected:
        raise RuntimeError("backend receipt does not bind the live backend")
    plan = json.loads((RELEASE / "publication-plan.json").read_text(encoding="utf-8"))
    binding = plan.get("backend_binding", {})
    if (
        binding.get("expected_records") != current.get("total_records")
        or binding.get("verified_snapshot")
        != {
            "total_records": current.get("total_records"),
            "total_bytes": current.get("total_bytes"),
            "bundle_sha256": current.get("bundle_sha256"),
        }
    ):
        raise RuntimeError("publication plan/backend receipt identity drift")
    if (
        current.get("next_source_line") != 3123
        or current.get("terminal_source_eof") is not False
        or current.get("stable_ids") != 476
        or current.get("mastery_triples") != 31
        or current.get("redraw_files") != 18
        or current.get("proof_repairs_closed")
        != [f"FOM-PR-{number:02d}" for number in range(1, 13)]
    ):
        raise RuntimeError("cumulative backend semantic boundary mismatch")
    prefix = receipt.get("nested_immutability", {}).get(
        "fomberg_unit_004_boundary", {}
    )
    if (
        prefix.get("preserved_byte_for_byte") is not True
        or prefix.get("records") != 6113
        or prefix.get("bundle_sha256")
        != "902eb71aa8a8b25e824ebe9ddae556e914e370d603382f28860392d6e186baba"
    ):
        raise RuntimeError("Fomberg Unit004 backend boundary was not preserved")
    if not base.identity_matches(
        receipt.get("human_receipt"), base.lane_path(BACKEND_CUMULATIVE_MD)
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
            "sha256": base.sha(path),
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
            "Roberts 30/30 complete; Fomberg O012-FOM-001 through "
            "O012-FOM-005 (Sections 1.1-1.11, lines 31-3122) complete; "
            "next Fomberg line 3123; composite course partial"
        ),
        "release_directory": RELEASE.relative_to(LANE).as_posix(),
        "reader_first_filename": PDF_NAME,
        "frozen_input_ledger": {**base.identity(FROZEN_LEDGER), "entries": len(frozen)},
        "packager": base.identity(SCRIPT),
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
    base.write_json(temporary, payload)
    temporary.replace(PACKAGE_RECEIPT)


def package() -> None:
    if not RELEASE.is_dir():
        raise RuntimeError("release controls must exist before packaging")
    if ARTIFACTS.exists():
        raise RuntimeError("artifacts directory already exists; refusing to overwrite")
    if STAGING.exists():
        raise RuntimeError("stale package staging exists; inspect it explicitly")

    metadata, plan, manifest_template, checksum_names = verify_controls()
    frozen = base.load_frozen_inputs()
    artifact_rows = base.parse_artifact_manifest()
    build_receipt = verify_build_receipt(artifact_rows)
    fomberg_qa = verify_fomberg_qa()
    backend_facts = base.verify_backend()
    backend_receipt = verify_backend_receipt(backend_facts)

    source = source_entries()
    qa = qa_entries()
    base.assert_source_archive_link_closure(source)
    frozen_paths = set(frozen)
    for archive_name, entries in ((SOURCE_ZIP_NAME, source), (QA_ZIP_NAME, qa)):
        for name, path in entries.items():
            relative = path.relative_to(LANE).as_posix()
            if path.resolve() in {SCRIPT.resolve(), FROZEN_LEDGER.resolve()}:
                continue
            if relative not in frozen_paths:
                raise RuntimeError(f"unfrozen {archive_name} input: {name} <- {relative}")

    STAGING.mkdir(parents=False)
    try:
        source_zip = base.deterministic_zip(STAGING / SOURCE_ZIP_NAME, source)
        qa_zip = base.deterministic_zip(STAGING / QA_ZIP_NAME, qa)
        copies = {
            PDF_NAME: base.lane_path(PDF_INPUT),
            HTML_NAME: base.lane_path(HTML_INPUT),
            "LICENSE.md": RELEASE / "LICENSE.md",
            "README_RELEASE.md": RELEASE / "README_RELEASE.md",
            "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md",
        }
        base.assert_safe_text(copies[HTML_NAME])
        for name, source_path in copies.items():
            shutil.copyfile(source_path, STAGING / name)

        upload_files = list(manifest_template["artifact_order"])
        manifest = dict(manifest_template)
        manifest.pop("template_state", None)
        manifest.pop("generated_fields", None)
        manifest.update(
            {
                "metadata_sha256": base.sha(RELEASE / "metadata.json"),
                "publication_plan_sha256": base.sha(RELEASE / "publication-plan.json"),
                "frozen_input_ledger": {
                    **base.identity(FROZEN_LEDGER),
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
                        "line_end": 3122,
                        "sections": "1.1-1.11",
                        "component_ids": [
                            "O012-FOM-001",
                            "O012-FOM-002",
                            "O012-FOM-003",
                            "O012-FOM-004",
                            "O012-FOM-005",
                        ],
                        "course_route_unit_ids": [
                            "D60-R08",
                            "D60-R09",
                            "D60-R10",
                            "D60-R11",
                            "D60-R12",
                        ],
                        "component_boundaries": {
                            "O012-FOM-001": "31-614",
                            "O012-FOM-002": "615-1290",
                            "O012-FOM-003": "1291-1922",
                            "O012-FOM-004": "1923-2846",
                            "O012-FOM-005": "2847-3122",
                        },
                        "next_source_line": 3123,
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
                    "html_unique_dom_ids": build_receipt["html_checks"]
                    ["live_browser_unique_dom_ids"],
                    "html_fragment_links": build_receipt["html_checks"]["fragment_links"],
                    "html_mathml_nodes": build_receipt["html_checks"]["mathml_nodes"],
                    "html_self_contained": build_receipt["html_checks"]["self_contained"],
                    "fomberg_stable_ids_total": backend_receipt["current"]["stable_ids"],
                    "fomberg_unit_005_stable_ids": fomberg_qa["reader"]["stable_ids"],
                    "mastery_triples_total": backend_receipt["current"]
                    ["mastery_triples"],
                    "fomberg_unit_005_mastery_triples": fomberg_qa["reader"]["mastery"]
                    ["exercise_hint_solution_triples"],
                    "fomberg_unit_005_semantic_figures": fomberg_qa["reader"]
                    ["assets"]["semantic_figures"],
                    "fomberg_unit_005_external_assets": 0,
                    "visual_status": build_receipt["visual_checks"]["status"],
                    "browser_checks": build_receipt.get("browser_checks", {}),
                    "pdf_untagged_limitation_disclosed": True,
                },
                "backend": {
                    **backend_facts,
                    "cumulative_receipt": base.identity(
                        base.lane_path(BACKEND_CUMULATIVE_JSON)
                    ),
                    "cumulative_human_receipt": base.identity(
                        base.lane_path(BACKEND_CUMULATIVE_MD)
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
                {"filename": name, "bytes": path.stat().st_size, "sha256": base.sha(path)}
            )
        base.write_json(STAGING / "release-manifest.json", manifest)

        sums = "\n".join(
            f"{base.sha(STAGING / name)}  {name}" for name in checksum_names
        ) + "\n"
        (STAGING / "SHA256SUMS").write_text(sums, encoding="utf-8", newline="\n")

        expected_names = sorted(checksum_names + ["SHA256SUMS"])
        actual_names = sorted(path.name for path in STAGING.iterdir() if path.is_file())
        if actual_names != expected_names:
            raise RuntimeError(f"staged payload inventory mismatch: {actual_names}")
        for name in actual_names:
            path = STAGING / name
            if path.suffix.lower() not in {".pdf", ".zip"}:
                base.assert_safe_text(path)
        parsed_sums: dict[str, str] = {}
        for line in (STAGING / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
            digest, name = line.split("  ", 1)
            if name in parsed_sums:
                raise RuntimeError(f"duplicate checksum row: {name}")
            parsed_sums[name] = digest
        expected_sums = {name: base.sha(STAGING / name) for name in checksum_names}
        if parsed_sums != expected_sums:
            raise RuntimeError("SHA256SUMS does not bind every payload file")
        for row in manifest["artifacts"]:
            path = STAGING / row["filename"]
            if path.stat().st_size != row["bytes"] or base.sha(path) != row["sha256"]:
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
                    "Roberts 30/30 + Fomberg O012-FOM-001/002/003/004/005 "
                    "through line 3122; next line 3123; composite course partial"
                ),
                "files": [
                    {
                        "filename": name,
                        "bytes": (ARTIFACTS / name).stat().st_size,
                        "sha256": base.sha(ARTIFACTS / name),
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


base.source_entries = source_entries
base.source_path_inventory = source_path_inventory
base.qa_path_inventory = qa_path_inventory
base.release_control_inventory = release_control_inventory
base.required_frozen_paths = required_frozen_paths
base.qa_entries = qa_entries
base.verify_controls = verify_controls
base.verify_build_receipt = verify_build_receipt
base.verify_fomberg_qa = verify_fomberg_qa
base.verify_backend_receipt = verify_backend_receipt
base.write_package_receipt = write_package_receipt
base.package = package


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list-required-inputs",
        action="store_true",
        help="print the exact frozen-input inventory without writing files",
    )
    args = parser.parse_args()
    if args.list_required_inputs:
        base.list_required_inputs()
        return
    package()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise
