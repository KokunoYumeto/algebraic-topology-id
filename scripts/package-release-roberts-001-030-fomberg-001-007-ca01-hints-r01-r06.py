#!/usr/bin/env python3
"""Prepare the sealed Roberts/Fomberg/CA01 Zenodo checkpoint.

This local-only packager reuses the proved Unit007 deterministic ZIP, input
freezing, path-safety, privacy, hashing, and source-link-closure machinery.  It
performs no Git, network, credential, deposition, or publication action.  It
fails closed until the final CA01 reader, backend, visual, browser, review, and
census evidence exists and the exact input ledger is bound below.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any


SCRIPT = Path(__file__).resolve()
BASE_PATH = SCRIPT.with_name(
    "package-release-roberts-001-030-fomberg-001-007.py"
)
SPEC = importlib.util.spec_from_file_location("o012_unit007_packager", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the proved Unit007 packager")
previous = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(previous)
base = previous.base

LANE = SCRIPT.parents[1]
RELEASE = LANE / "release" / "zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06"
ARTIFACTS = RELEASE / "artifacts"
STAGING = RELEASE / ".package-staging"
FROZEN_LEDGER = RELEASE / "frozen-inputs.json"
PACKAGE_RECEIPT = RELEASE / "PACKAGE_PREPARATION_RECEIPT.json"

TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30, "
    "Jembatan Homologi §1.1–1.13, Asesmen Kumulatif 1, dan Petunjuk Rute 1–6"
)
VERSION = "0.31.1"
RELEASE_ID = "o012-composite-id-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-v0.31.1"
CONCEPT_DOI = "10.5281/zenodo.22061489"
PREVIOUS_RECORD_ID = 22105179
PREVIOUS_DOI = "10.5281/zenodo.22105179"
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

# Apply-patch this to the SHA-256 printed by --seal-frozen-inputs only after
# every final gate and the sealed publication plan mutually agree.
FROZEN_LEDGER_SHA256 = "9c805c1682873c00b87a715d9fc5010a09398ad5853e7088fec23c8b7ffc7bf2"

PDF_INPUT = "output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-id.pdf"
HTML_INPUT = "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06/index.html"
ARTIFACT_MANIFEST = "output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06.csv"
BUILD_RECEIPT = "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_BUILD_RECEIPT.json"
VISUAL_QA = "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_VISUAL_QA.md"
RENDER_INVENTORY = "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_RENDER_INVENTORY.csv"
BROWSER_QA = "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_BROWSER_QA.json"
BACKEND_CUMULATIVE = "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_CUMULATIVE_RECEIPT.json"
CA01_QA = "qa/CUMULATIVE_ASSESSMENT_001_QA.json"
CA01_MATH_REVIEW = "qa/cumulative-assessment-001/INDEPENDENT_MATH_REVIEW.json"
CA01_LANGUAGE_REVIEW = "qa/cumulative-assessment-001/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
HINT_SOURCE = "source/id-ID/mastery/ordinary-hints-r01-r06.md"
HINT_QA = "qa/ORDINARY_HINTS_R01_R06_QA.json"
HINT_MATH_REVIEW = "qa/ordinary-hints-r01-r06/INDEPENDENT_MATH_REVIEW.json"
HINT_LANGUAGE_REVIEW = "qa/ordinary-hints-r01-r06/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
ROUTE_CENSUS = "qa/ROUTE_MASTERY_CENSUS.json"
PROOF_CENSUS = "qa/PROOF_REPAIR_CENSUS.json"
CA01_SOURCE = "source/id-ID/mastery/cumulative-assessment-001-foundations-coverings-homotopy.md"

PDF_NAME = "00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_READER.pdf"
HTML_NAME = "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_READER.html"
SOURCE_ZIP_NAME = "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_EDITABLE_SOURCE_BACKEND.zip"
QA_ZIP_NAME = "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_QA_PROVENANCE.zip"

FINAL_BOUNDARY_PATHS = {
    PDF_INPUT,
    HTML_INPUT,
    ARTIFACT_MANIFEST,
    BUILD_RECEIPT,
    VISUAL_QA,
    RENDER_INVENTORY,
    BROWSER_QA,
    BACKEND_CUMULATIVE,
    HINT_QA,
    ROUTE_CENSUS,
    PROOF_CENSUS,
}

_previous_source_entries = previous.source_entries
_previous_qa_path_inventory = previous.qa_path_inventory
_previous_assert_safe_bytes = previous.assert_safe_bytes

# Rebind inherited generic helpers to this release.  Those helpers resolve
# module globals at call time and therefore retain their proved behavior.
for name, value in {
    "__file__": str(SCRIPT),
    "RELEASE": RELEASE,
    "ARTIFACTS": ARTIFACTS,
    "STAGING": STAGING,
    "FROZEN_LEDGER": FROZEN_LEDGER,
    "PACKAGE_RECEIPT": PACKAGE_RECEIPT,
    "TITLE": TITLE,
    "VERSION": VERSION,
    "RELEASE_ID": RELEASE_ID,
    "CONCEPT_DOI": CONCEPT_DOI,
    "PREVIOUS_RECORD_ID": PREVIOUS_RECORD_ID,
    "PREVIOUS_DOI": PREVIOUS_DOI,
    "FROZEN_LEDGER_SHA256": FROZEN_LEDGER_SHA256,
    "PDF_INPUT": PDF_INPUT,
    "HTML_INPUT": HTML_INPUT,
    "ARTIFACT_MANIFEST": ARTIFACT_MANIFEST,
    "BUILD_RECEIPT": BUILD_RECEIPT,
    "VISUAL_QA": VISUAL_QA,
    "RENDER_INVENTORY": RENDER_INVENTORY,
    "BACKEND_CUMULATIVE_JSON": BACKEND_CUMULATIVE,
    "BACKEND_CUMULATIVE_MD": BACKEND_CUMULATIVE,
    "PDF_NAME": PDF_NAME,
    "HTML_NAME": HTML_NAME,
    "SOURCE_ZIP_NAME": SOURCE_ZIP_NAME,
    "QA_ZIP_NAME": QA_ZIP_NAME,
    "FINAL_BOUNDARY_PATHS": FINAL_BOUNDARY_PATHS,
}.items():
    setattr(base, name, value)


def assert_safe_bytes(
    data: bytes,
    label: str,
    *,
    allow_generic_privacy_test_markers: bool = False,
) -> None:
    """Permit one literal privacy assertion in the exact CA01 producer only."""
    normalized = label.replace("\\", "/")
    producers = {
        "scripts/extend-backend-cumulative-assessment-001.py",
        "scripts/extend-backend-ordinary-hints-r01-r06.py",
        "scripts/qa-ordinary-hints-r01-r06.py",
    }
    producer = next((item for item in producers if normalized.endswith(item) or normalized.endswith(f"{item} as {item}")), None)
    if producer is not None:
        marker = b"authoriza" + b"tion: bearer"
        if data.lower().count(marker) != 1:
            raise RuntimeError(f"producer credential-test marker census drift: {producer}")
        data = data.lower().replace(marker, b"authorization test marker")
    _previous_assert_safe_bytes(
        data,
        label,
        allow_generic_privacy_test_markers=allow_generic_privacy_test_markers,
    )


base.assert_safe_bytes = assert_safe_bytes


def source_entries() -> dict[str, Path]:
    """Return the compact, complete, resumable source/backend closure."""
    entries = _previous_source_entries()
    entries.update(
        {
            CA01_SOURCE: base.lane_path(CA01_SOURCE),
            HINT_SOURCE: base.lane_path(HINT_SOURCE),
            "scripts/qa-cumulative-assessment-001.py": LANE / "scripts/qa-cumulative-assessment-001.py",
            "scripts/census-route-mastery.py": LANE / "scripts/census-route-mastery.py",
            "scripts/census-proof-repairs.py": LANE / "scripts/census-proof-repairs.py",
            "scripts/extend-backend-cumulative-assessment-001.py": LANE / "scripts/extend-backend-cumulative-assessment-001.py",
            "scripts/validate-backend-append-only-cumulative-assessment-001.py": LANE / "scripts/validate-backend-append-only-cumulative-assessment-001.py",
            "scripts/qa-ordinary-hints-r01-r06.py": LANE / "scripts/qa-ordinary-hints-r01-r06.py",
            "scripts/extend-backend-ordinary-hints-r01-r06.py": LANE / "scripts/extend-backend-ordinary-hints-r01-r06.py",
            "scripts/validate-backend-append-only-ordinary-hints-r01-r06.py": LANE / "scripts/validate-backend-append-only-ordinary-hints-r01-r06.py",
            "scripts/build-roberts-001-030-fomberg-001-007-ca01.ps1": LANE / "scripts/build-roberts-001-030-fomberg-001-007-ca01.ps1",
            "scripts/finalize-build-roberts-001-030-fomberg-001-007-ca01.py": LANE / "scripts/finalize-build-roberts-001-030-fomberg-001-007-ca01.py",
            "scripts/build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.ps1": LANE / "scripts/build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.ps1",
            "scripts/finalize-build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.py": LANE / "scripts/finalize-build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.py",
            "scripts/package-release-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.py": SCRIPT,
            "scripts/publish-zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.py": LANE / "scripts/publish-zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.py",
        }
    )
    return entries


def source_path_inventory() -> set[str]:
    paths = set(source_entries())
    # The final ledger digest is apply-patch-bound in this file; its final
    # identity is instead recorded in the package receipt.
    paths.remove("scripts/package-release-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.py")
    return paths


def qa_path_inventory() -> set[str]:
    paths = set(_previous_qa_path_inventory())
    paths.update(
        {
            CA01_QA,
            CA01_MATH_REVIEW,
            CA01_LANGUAGE_REVIEW,
            HINT_QA,
            HINT_MATH_REVIEW,
            HINT_LANGUAGE_REVIEW,
            ROUTE_CENSUS,
            PROOF_CENSUS,
            "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_FILE_MANIFEST.csv",
            "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_PLAN.json",
            "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_RECEIPT.json",
            "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_REPLAY_RECEIPT.json",
            "qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_BUILD_DRAFT.json",
            BACKEND_CUMULATIVE,
            BUILD_RECEIPT,
            VISUAL_QA,
            RENDER_INVENTORY,
            BROWSER_QA,
        }
    )
    return paths


def release_control_inventory() -> set[str]:
    prefix = "release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06/"
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
    return FINAL_BOUNDARY_PATHS | source_path_inventory() | qa_path_inventory() | release_control_inventory()


def qa_entries() -> dict[str, Path]:
    entries = {relative: base.lane_path(relative) for relative in sorted(qa_path_inventory())}
    entries.update(
        {
            "release/frozen-inputs.json": FROZEN_LEDGER,
            "release/frozen-inputs.template.json": RELEASE / "frozen-inputs.template.json",
            "release/release-manifest.template.json": RELEASE / "release-manifest.template.json",
            "release/SHA256SUMS.template": RELEASE / "SHA256SUMS.template",
        }
    )
    return entries


def _identity(path: str) -> dict[str, Any]:
    return base.identity(base.lane_path(path))


def verify_controls() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[str]]:
    names = (
        "metadata.json", "publication-plan.json", "README_RELEASE.md",
        "SOURCE_PACKAGE_README.md", "LICENSE.md", "RELEASE_RIGHTS.md",
        "release-manifest.template.json", "SHA256SUMS.template",
        "frozen-inputs.template.json",
    )
    for name in names:
        path = RELEASE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        base.assert_safe_text(path)
    joined = "\n".join((RELEASE / name).read_text(encoding="utf-8") for name in names)
    for marker in (
        "30/30", "O012-FOM-001–007", "baris 31–4185", "D60-CA01", "8/8",
        "84/84", "92/108", "D60-CA02", "D60-CA03", "empat laboratorium",
        "capstone", "CC BY 4.0", "CC BY-SA 4.0", MODEL_NOTE,
    ):
        if marker not in joined:
            raise RuntimeError(f"release controls omit exact scope marker: {marker}")
    if joined.count(ORGANIZATION_NAME) != 1:
        raise RuntimeError("organization must occur exactly once, only in contributor metadata")

    metadata_payload = json.loads((RELEASE / "metadata.json").read_text(encoding="utf-8"))
    metadata = metadata_payload.get("metadata", {})
    expected_creators = [{"name": "Roberts, David Michael"}, {"name": "Fomberg, Yeheli"}]
    expected_contributors = [
        {"name": "Lazarovich, Nir", "type": "Other"},
        {"name": "Editor edisi Bahasa Indonesia", "type": "Editor"},
        {"name": ORGANIZATION_NAME, "type": "Other"},
    ]
    if (
        metadata.get("title") != TITLE or metadata.get("version") != VERSION
        or metadata.get("license") != "cc-by-sa-4.0"
        or metadata.get("language") != "ind" or metadata.get("access_right") != "open"
        or metadata.get("creators") != expected_creators
        or metadata.get("contributors") != expected_contributors
    ):
        raise RuntimeError("metadata identity, rights, creator, or contributor drift")
    if not str(metadata.get("description", "")).startswith(
        "<p><strong>Status: checkpoint parsial kursus komposit; Roberts lengkap 30/30"
    ):
        raise RuntimeError("metadata description does not lead with exact status truth")
    prose = "\n".join(str(metadata.get(k, "")) for k in ("title", "description", "notes"))
    prose += "\n" + "\n".join(str(v) for v in metadata.get("keywords", []))
    if ORGANIZATION_PATTERN.search(prose):
        raise RuntimeError("organization marker leaked into title or prose metadata")

    plan = json.loads((RELEASE / "publication-plan.json").read_text(encoding="utf-8"))
    if plan.get("state") != "prepared_not_published" or plan.get("artifact_identities_known") is not True:
        raise RuntimeError("release is unsealed: final reader/backend identities are required")
    if (
        plan.get("release_id") != RELEASE_ID or plan.get("version") != VERSION
        or plan.get("existing_concept_doi") != CONCEPT_DOI
        or plan.get("current_public_record_id") != PREVIOUS_RECORD_ID
        or plan.get("current_public_doi") != PREVIOUS_DOI
        or plan.get("reader_first_filename") != PDF_NAME
        or plan.get("metadata_payload") != "metadata.json"
        or plan.get("payload_directory") != "artifacts"
        or plan.get("publish_not_draft") is not True
        or plan.get("anonymous_byte_readback_required") is not True
        or plan.get("new_concept_allowed") is not False
        or plan.get("new_deposition_created") is not False
        or plan.get("credentials_used") is not False
    ):
        raise RuntimeError("publication plan escaped the exact existing concept lineage")
    backend = plan.get("backend_binding", {})
    snapshot = backend.get("verified_snapshot")
    if (
        backend.get("final_identity_source") != BACKEND_CUMULATIVE
        or backend.get("hardcoded_final_identity") is not False
        or not isinstance(backend.get("expected_records"), int)
        or backend.get("expected_records") != 7012
        or not isinstance(snapshot, dict)
        or snapshot.get("total_records") != backend.get("expected_records")
        or not isinstance(snapshot.get("total_bytes"), int)
        or not re.fullmatch(r"[0-9a-f]{64}", str(snapshot.get("bundle_sha256", "")))
    ):
        raise RuntimeError("publication plan backend binding is not sealed")
    readers = plan.get("final_reader_artifacts")
    if not isinstance(readers, dict) or set(readers) != {"html", "pdf"}:
        raise RuntimeError("publication plan reader identities are not sealed")
    for role, relative in (("html", HTML_INPUT), ("pdf", PDF_INPUT)):
        row = readers.get(role, {})
        if row.get("path") != relative or not base.identity_matches(row, base.lane_path(relative)):
            raise RuntimeError(f"publication plan does not bind final {role} bytes")
    if readers["pdf"].get("pages") != 482:
        raise RuntimeError("publication plan must bind the 482-page hint successor")

    template = json.loads((RELEASE / "release-manifest.template.json").read_text(encoding="utf-8"))
    expected_status = "roberts_complete_fomberg_units_001_007_complete_ca01_complete_ordinary_mastery_84_complete_composite_course_partial"
    if (
        template.get("release_id") != RELEASE_ID or template.get("title") != TITLE
        or template.get("version") != VERSION or template.get("status") != expected_status
    ):
        raise RuntimeError("release manifest template identity/scope drift")
    numbering = template.get("component_numbering", {})
    if (
        numbering.get("roberts_edition_units") != "001-030"
        or numbering.get("assessment_ids") != ["D60-CA01"]
        or numbering.get("original_edition_unit_ids") != ["O012-ORIG-CA01", "O012-ORIG-HINTS-R01-R06"]
        or numbering.get("fomberg_is_not_roberts_units_031_037") is not True
    ):
        raise RuntimeError("release manifest component numbering drift")
    expected_upload = [PDF_NAME, HTML_NAME, SOURCE_ZIP_NAME, QA_ZIP_NAME, "LICENSE.md", "README_RELEASE.md", "RELEASE_RIGHTS.md"]
    if template.get("artifact_order") != expected_upload:
        raise RuntimeError("release manifest is not reader-first")

    checksum_names: list[str] = []
    for line in (RELEASE / "SHA256SUMS.template").read_text(encoding="utf-8").splitlines():
        marker, separator, name = line.partition("  ")
        if marker != "<sha256>" or not separator or not name:
            raise RuntimeError("malformed SHA256SUMS.template")
        checksum_names.append(name)
    if checksum_names != expected_upload + ["release-manifest.json"]:
        raise RuntimeError("checksum template inventory/order mismatch")
    frozen_template = json.loads((RELEASE / "frozen-inputs.template.json").read_text(encoding="utf-8"))
    if (
        frozen_template.get("release_id") != RELEASE_ID
        or frozen_template.get("state") != "template_unsealed_do_not_package"
        or frozen_template.get("entries") != []
        or set(frozen_template.get("final_boundary_paths", [])) != FINAL_BOUNDARY_PATHS
    ):
        raise RuntimeError("frozen-input template identity/boundary drift")
    return metadata, plan, template, checksum_names


def verify_ca01() -> dict[str, Any]:
    qa = json.loads(base.lane_path(CA01_QA).read_text(encoding="utf-8"))
    if (
        qa.get("status") != "PASS" or qa.get("qa_id") != "O012-D60-CUMULATIVE-ASSESSMENT-001"
        or qa.get("assessment_id") != "D60-CA01" or qa.get("edition_unit_id") != "O012-ORIG-CA01"
        or qa.get("model_provenance") != MODEL_NOTE
    ):
        raise RuntimeError("CA01 QA identity/status mismatch")
    reader = qa.get("reader", {})
    if (
        not base.identity_matches(reader.get("identity"), base.lane_path(CA01_SOURCE))
        or reader.get("stable_ids") != 34
        or reader.get("exercise_hint_solution_triples") != 8
        or reader.get("complete_checked_solutions") != 8
        or reader.get("primary_route_coverage") != [f"D60-R{i:02d}" for i in range(1, 8)]
    ):
        raise RuntimeError("CA01 source/mastery/route boundary drift")
    reviews = qa.get("independent_reviews", {})
    for key, path in (("mathematics", CA01_MATH_REVIEW), ("source_language", CA01_LANGUAGE_REVIEW)):
        row = reviews.get(key, {})
        if row.get("status") != "PASS" or not base.identity_matches(row, base.lane_path(path)):
            raise RuntimeError(f"CA01 {key} review binding drift")
        review = json.loads(base.lane_path(path).read_text(encoding="utf-8"))
        if review.get("status") != "PASS" or review.get("severity_census") != {"P1": 0, "P2": 0, "P3": 0}:
            raise RuntimeError(f"CA01 {key} review has unresolved findings")
    if any(value != "PASS" for value in qa.get("checks", {}).values()):
        raise RuntimeError("CA01 static QA gate is incomplete")
    return qa


def verify_hints() -> dict[str, Any]:
    qa = json.loads(base.lane_path(HINT_QA).read_text(encoding="utf-8"))
    if (
        qa.get("status") != "PASS"
        or qa.get("qa_id") != "O012-D60-ORDINARY-HINTS-R01-R06"
        or qa.get("edition_unit_id") != "O012-ORIG-HINTS-R01-R06"
        or qa.get("model_provenance") != MODEL_NOTE
        or not base.identity_matches(qa.get("source"), base.lane_path(HINT_SOURCE))
        or qa.get("source", {}).get("hint_blocks") != 36
        or qa.get("source", {}).get("stable_ids") != 43
    ):
        raise RuntimeError("ordinary-hint QA identity/scope mismatch")
    binding = qa.get("binding_census", {})
    if (
        binding.get("distinct_target_exercises") != 36
        or binding.get("distinct_existing_solutions") != 36
        or binding.get("exact_existing_solve_edges") != 36
        or binding.get("prompt_records_changed") != 0
        or binding.get("solution_records_changed") != 0
        or binding.get("solves_relations_changed") != 0
        or binding.get("routes") != {f"D60-R{i:02d}": 6 for i in range(1, 7)}
        or any(value != "PASS" for value in qa.get("checks", {}).values())
    ):
        raise RuntimeError("ordinary-hint binding/static QA drift")
    for key, path in (("mathematics", HINT_MATH_REVIEW), ("source_language", HINT_LANGUAGE_REVIEW)):
        row = qa.get("independent_reviews", {}).get(key, {})
        review = json.loads(base.lane_path(path).read_text(encoding="utf-8"))
        if (
            row.get("status") != "PASS"
            or not base.identity_matches(row, base.lane_path(path))
            or review.get("status") != "PASS"
            or review.get("severity_census") != {"P1": 0, "P2": 0, "P3": 0}
            or review.get("unresolved_findings") != []
        ):
            raise RuntimeError(f"ordinary-hint {key} review drift")
    return qa


def verify_backend_receipt(backend_facts: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
    receipt = json.loads(base.lane_path(BACKEND_CUMULATIVE).read_text(encoding="utf-8"))
    current = receipt.get("cumulative", {})
    if (
        receipt.get("status") != "PASS"
        or receipt.get("edition_unit_id") != "O012-ORIG-HINTS-R01-R06"
        or receipt.get("model_provenance") != MODEL_NOTE
        or current.get("records") != backend_facts["total_records"]
        or current.get("bytes") != backend_facts["total_bytes"]
        or current.get("bundle_sha256") != backend_facts["bundle_sha256"]
    ):
        raise RuntimeError("ordinary-hint cumulative backend receipt/live backend mismatch")
    prefix = receipt.get("immutable_prefix", {})
    if (
        prefix.get("preserved_exactly") is not True or prefix.get("records") != 6854
        or prefix.get("bytes") != 8345799
        or prefix.get("bundle_sha256") != "51e75d06e620762e629e9e7408da4b0c32b3e337817d9d140fbbdfa438de2f57"
    ):
        raise RuntimeError("published CA01 backend prefix was not preserved")
    semantic = receipt.get("semantic_checks", {})
    if (
        receipt.get("replay", {}).get("status") != "PASS"
        or receipt.get("replay", {}).get("temporary_replay_removed") is not True
        or semantic.get("prompt_solution_solves_immutability") != "PASS"
        or semantic.get("rights_closure") != "PASS"
        or semantic.get("route_mapping") != "PASS"
        or semantic.get("added_records") != 158
        or semantic.get("graph_postconditions", {}).get("ordinary_capped_route_credit") != 84
        or semantic.get("graph_postconditions", {}).get("credited_total") != 92
        or semantic.get("graph_postconditions", {}).get("duplicate_or_reused_solution_ids") != 0
    ):
        raise RuntimeError("ordinary-hint backend semantic/replay gates are incomplete")
    binding = plan["backend_binding"]
    if (
        binding.get("expected_records") != current.get("records")
        or binding.get("verified_snapshot") != {
            "total_records": current.get("records"),
            "total_bytes": current.get("bytes"),
            "bundle_sha256": current.get("bundle_sha256"),
        }
    ):
        raise RuntimeError("publication plan/backend receipt binding drift")
    return receipt


def verify_censuses() -> tuple[dict[str, Any], dict[str, Any]]:
    route = json.loads(base.lane_path(ROUTE_CENSUS).read_text(encoding="utf-8"))
    if route.get("status") != "PASS":
        raise RuntimeError("route mastery census did not pass")
    assessments = route.get("assessments", {})
    source_ca01 = assessments.get("source_ca01", {})
    backend = assessments.get("backend", {})
    deficits = route.get("next_deficits", {})
    if (
        source_ca01.get("admissible_complete") is not True
        or source_ca01.get("hash_matches_reviewed_boundary") is not True
        or backend.get("complete_assessment_ids") != ["D60-CA01"]
        or backend.get("credited_items") != 8
        or deficits.get("source_assessments_to_create") != ["D60-CA02", "D60-CA03"]
        or deficits.get("source_assessment_items_to_create") != 16
        or deficits.get("ordinary_missing_triples") != 0
        or route.get("ordinary_mastery", {}).get("quota", {}).get("capped_route_credit") != 84
        or route.get("ordinary_mastery", {}).get("quota", {}).get("met") is not True
        or route.get("compliance", {}).get("backend_admitted", {}).get("total_slots_covered") != 92
        or route.get("graph_validation", {}).get("validation_error_count") != 0
        or route.get("graph_validation", {}).get("duplicate_or_reused_triple_solution_ids") != []
    ):
        raise RuntimeError("route mastery census does not prove 84/84 ordinary, CA01, or remaining scope")
    proof = json.loads(base.lane_path(PROOF_CENSUS).read_text(encoding="utf-8"))
    if proof.get("status") not in {"PASS", "FAIL_CLOSED"}:
        raise RuntimeError("proof-repair census has an unknown status")
    summary = proof.get("summary", {})
    mandatory = summary.get("mandatory_dossier", {})
    later = summary.get("later_admitted_repairs", {})
    if (
        mandatory.get("status") != "PASS" or mandatory.get("actual_missing_repairs") != []
        or later.get("mathematical_content_status") != "PASS"
        or later.get("actual_missing_repair_content") != []
    ):
        raise RuntimeError("proof census identifies missing mathematical repair content")
    if proof.get("status") == "FAIL_CLOSED" and not proof.get("findings"):
        raise RuntimeError("fail-closed proof census has no explicit findings")
    return route, proof


def verify_build_receipt(artifact_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    receipt = json.loads(base.lane_path(BUILD_RECEIPT).read_text(encoding="utf-8"))
    if (
        receipt.get("status") != "PASS"
        or receipt.get("qa_id") != "O012-RBT-001-030-FOM-001-007-CA01-HINTS-R01-R06-COMPOSITE-BUILD"
        or receipt.get("model_provenance") != MODEL_NOTE
    ):
        raise RuntimeError("final ordinary-hint build receipt identity/status mismatch")
    artifacts = receipt.get("artifacts", {})
    for role, relative in (("pdf", PDF_INPUT), ("html", HTML_INPUT), ("manifest", ARTIFACT_MANIFEST)):
        if not base.identity_matches(artifacts.get(role), base.lane_path(relative)):
            raise RuntimeError(f"build receipt {role} does not bind final bytes")
    for relative, row in artifact_rows.items():
        actual = base.lane_path(relative)
        if actual.stat().st_size != row.get("bytes") or base.sha(actual) != row.get("sha256"):
            raise RuntimeError(f"reader artifact/CSV mismatch: {relative}")
    if artifacts.get("pdf", {}).get("pages") != 482 or artifacts.get("pdf", {}).get("tagged") is not False:
        raise RuntimeError("final hint-successor PDF boundary/limitation drift")
    hints = receipt.get("ordinary_hints", {})
    if (
        hints.get("edition_unit_id") != "O012-ORIG-HINTS-R01-R06"
        or hints.get("census", {}).get("hint_blocks") != 36
        or hints.get("census", {}).get("exercise_solution_pairs") != 36
        or hints.get("census", {}).get("visible_predecessor_links") != 72
        or not base.identity_matches(hints.get("source"), base.lane_path(HINT_SOURCE))
        or not base.identity_matches(hints.get("static_qa"), base.lane_path(HINT_QA))
    ):
        raise RuntimeError("final build receipt ordinary-hint scope drift")
    html = receipt.get("html_checks", {})
    if (
        html.get("status") != "PASS" or html.get("self_contained") is not True
        or html.get("unresolved_fragment_links") != 0
        or html.get("hint_blocks_added") != 36
        or html.get("visible_predecessor_links_added") != 72
        or html.get("centered_reflow") is not True
    ):
        raise RuntimeError("final HTML gate is incomplete")
    pdf = receipt.get("pdf_checks", {})
    if (
        pdf.get("status") not in {"PASS", "PASS_STRUCTURAL"}
        or pdf.get("pages") != 482 or pdf.get("appended_hint_pages") != 5
        or pdf.get("all_pages_a4") is not True
        or pdf.get("all_fonts_embedded_subset_tounicode") is not True
        or pdf.get("merged_outline_entries") != 396
        or pdf.get("merged_named_destinations") != 2988
        or pdf.get("all_source_stable_ids_resolve") is not True
        or pdf.get("visible_links_to_predecessor_resolve") is not True
        or pdf.get("independent_link_page_audit", {}).get("links_checked") != 72
        or pdf.get("independent_link_page_audit", {}).get("wrong_pages") != 0
    ):
        raise RuntimeError("final PDF structural gate is incomplete")
    reproduction = receipt.get("reproducibility", {})
    for key in (
        "frozen_inputs_fail_closed", "html_builds_byte_identical",
        "hint_pdf_builds_byte_identical", "merged_pdf_builds_byte_identical",
        "build_scratch_removed_after_finalizer",
    ):
        if reproduction.get(key) is not True:
            raise RuntimeError(f"final reproducibility gate is incomplete: {key}")
    visual = receipt.get("visual_checks", {})
    if (
        visual.get("status") != "PASS"
        or not base.identity_matches(visual.get("visual_receipt"), base.lane_path(VISUAL_QA))
        or not base.identity_matches(visual.get("render_inventory"), base.lane_path(RENDER_INVENTORY))
    ):
        raise RuntimeError("final visual QA gate is incomplete")
    browser = receipt.get("browser_checks", {})
    if (
        browser.get("status") != "PASS" or browser.get("desktop") != "PASS"
        or browser.get("mobile") != "PASS" or browser.get("offline") != "PASS"
        or browser.get("unresolved_fragment_links") != 0
        or not base.identity_matches(browser.get("browser_receipt"), base.lane_path(BROWSER_QA))
    ):
        raise RuntimeError("final desktop/mobile/offline browser gate is incomplete")
    if receipt.get("qa_not_claimed"):
        raise RuntimeError("final build receipt still carries pending-QA claims")
    return receipt


def verify_browser_qa() -> dict[str, Any]:
    receipt = json.loads(base.lane_path(BROWSER_QA).read_text(encoding="utf-8"))
    if (
        receipt.get("qa_id") != "O012-RBT-001-030-FOM-001-007-CA01-HINTS-R01-R06-BROWSER-QA"
        or receipt.get("status") != "PASS" or receipt.get("model_provenance") != MODEL_NOTE
        or not base.identity_matches(receipt.get("artifact"), base.lane_path(HTML_INPUT))
        or receipt.get("desktop", {}).get("status") != "PASS"
        or receipt.get("desktop", {}).get("centered_and_page_filling") is not True
        or receipt.get("desktop", {}).get("page_level_horizontal_overflow") is not False
        or receipt.get("mobile", {}).get("status") != "PASS"
        or receipt.get("mobile", {}).get("page_level_horizontal_overflow") is not False
        or receipt.get("mobile", {}).get("hint_blocks_escaping_body") != 0
    ):
        raise RuntimeError("independent desktop/mobile browser QA is incomplete")
    semantic = receipt.get("semantic_and_binding_checks", {})
    if (
        semantic.get("live_dom_ids") != semantic.get("unique_live_dom_ids")
        or semantic.get("unresolved_fragment_links") != 0
        or semantic.get("hint_blocks") != 36 or semantic.get("hint_links") != 72
        or semantic.get("hint_blocks_missing_required_attributes") != 0
        or semantic.get("runtime_external_asset_references") != 0
        or semantic.get("self_contained_offline_surface") is not True
        or receipt.get("console", {}).get("errors") != 0
        or receipt.get("severity_census") != {"P1": 0, "P2": 0, "P3": 0}
    ):
        raise RuntimeError("independent browser semantic/offline gate is incomplete")
    return receipt


def verify_visual_qa() -> dict[str, Any]:
    visual_path = base.lane_path(VISUAL_QA)
    inventory_path = base.lane_path(RENDER_INVENTORY)
    text = visual_path.read_text(encoding="utf-8")
    base.assert_safe_text(visual_path)
    pdf_path = base.lane_path(PDF_INPUT)
    required_markers = (
        "Status: **PASS**", "482 A4 pages", f"SHA-256 `{base.sha(pdf_path)}`",
        "72/72 PASS", "2,988 named destinations", "396 outline entries",
        "P1 (release-blocking missing, unreadable, blank, clipped, or mislinked content): **0**",
        "P2 (material layout, transition, font, formula, hierarchy, or navigation defect): **0**",
        "P3 (minor visible cosmetic defect): **0**",
        "Overall disposition: **PASS",
    )
    if any(marker not in text for marker in required_markers):
        raise RuntimeError("visual QA does not bind the repaired zero-severity PDF boundary")
    with inventory_path.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if (
        len(rows) != 6 or [int(row["physical_page"]) for row in rows] != list(range(477, 483))
        or any(row.get("visual_status") != "PASS" for row in rows)
        or any(int(row.get("width_px", 0)) != 1323 or int(row.get("height_px", 0)) != 1871 for row in rows)
        or any(not re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")) for row in rows)
    ):
        raise RuntimeError("visual render inventory boundary/status drift")
    return {
        "status": "PASS",
        "visual_receipt": base.identity(visual_path),
        "render_inventory": base.identity(inventory_path),
        "pages_inspected": [int(row["physical_page"]) for row in rows],
    }


def seal_frozen_inputs() -> None:
    if FROZEN_LEDGER.exists():
        raise RuntimeError("frozen-inputs.json already exists; refusing to overwrite")
    metadata, plan, _, _ = verify_controls()
    del metadata
    artifacts = base.parse_artifact_manifest()
    verify_ca01()
    verify_hints()
    backend_facts = base.verify_backend()
    verify_backend_receipt(backend_facts, plan)
    verify_censuses()
    verify_browser_qa()
    verify_visual_qa()
    verify_build_receipt(artifacts)
    rows = []
    for relative in sorted(required_frozen_paths()):
        path = base.lane_path(relative)
        if not path.is_file():
            raise FileNotFoundError(path)
        base.assert_safe_bytes(
            path.read_bytes(),
            f"{relative} as {relative}" if relative.startswith("scripts/") else relative,
            allow_generic_privacy_test_markers=relative.startswith("scripts/"),
        )
        rows.append({"path": relative, "bytes": path.stat().st_size, "sha256": base.sha(path)})
    payload = {
        "schema_version": "1.0",
        "release_id": RELEASE_ID,
        "state": "final_inputs_sealed_local_only",
        "final_boundary_paths": sorted(FINAL_BOUNDARY_PATHS),
        "entries": rows,
    }
    base.write_json(FROZEN_LEDGER, payload)
    print(json.dumps({"status": "SEALED_LEDGER_REQUIRES_APPLY_PATCH_BINDING", **base.identity(FROZEN_LEDGER), "entries": len(rows)}, indent=2))


def write_package_receipt(frozen: dict[str, dict[str, Any]], source_zip: dict[str, Any], qa_zip: dict[str, Any]) -> None:
    files = [
        {"filename": path.name, "bytes": path.stat().st_size, "sha256": base.sha(path)}
        for path in sorted(ARTIFACTS.iterdir(), key=lambda item: item.name) if path.is_file()
    ]
    archives = []
    for row in (source_zip, qa_zip):
        archives.append(
            {
                "filename": row["filename"], "bytes": row["bytes"], "sha256": row["sha256"],
                "entry_count": row["entry_count"], "uncompressed_bytes": row["uncompressed_bytes"],
                "crc_status": "PASS", "first_entry": row["entries"][0]["path"],
                "last_entry": row["entries"][-1]["path"],
            }
        )
    payload = {
        "schema_version": "1.0", "status": "PASS_PREPARED_NOT_PUBLISHED",
        "release_id": RELEASE_ID,
        "scope": "Roberts 30/30 complete; selected Fomberg 1.1-1.13 complete; D60-CA01 complete 8/8; ordinary mastery complete 84/84; total required mastery 92/108; composite course partial",
        "release_directory": RELEASE.relative_to(LANE).as_posix(),
        "reader_first_filename": PDF_NAME,
        "frozen_input_ledger": {**base.identity(FROZEN_LEDGER), "entries": len(frozen)},
        "packager": base.identity(SCRIPT), "files": files, "file_count": len(files),
        "total_payload_bytes": sum(int(row["bytes"]) for row in files), "archives": archives,
        "verification": {
            "manifest_artifact_identities_match": True, "sha256sums_match": True,
            "zip_crc_and_inventory_pass": True, "source_archive_local_link_closure_pass": True,
            "rights_component_scope_consistent": True, "reader_first": True,
            "final_build_visual_browser_gates": True, "ca01_independent_reviews": True,
            "ordinary_hint_independent_reviews": True,
            "ordinary_hints_static_independent_reviews": True,
            "ordinary_mastery_84_complete": True,
            "route_and_proof_censuses_included": True, "integrated_license": "CC BY-SA 4.0",
            "roberts_component_license": "CC BY 4.0", "fomberg_component_license": "CC BY-SA 4.0",
            "original_ca01_license": "CC BY-SA 4.0", "original_hint_license": "CC BY-SA 4.0",
            "new_concept_created": False,
            "network_actions": 0, "git_actions": 0, "credentials_used": False, "published": False,
        },
    }
    base.write_json(PACKAGE_RECEIPT, payload)


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
    ca01 = verify_ca01()
    hints = verify_hints()
    backend_facts = base.verify_backend()
    backend_receipt = verify_backend_receipt(backend_facts, plan)
    route_census, proof_census = verify_censuses()
    build_receipt = verify_build_receipt(artifact_rows)
    browser_receipt = verify_browser_qa()
    visual_receipt = verify_visual_qa()

    source = source_entries()
    qa = qa_entries()
    base.assert_source_archive_link_closure(source)
    for archive_name, entries in ((SOURCE_ZIP_NAME, source), (QA_ZIP_NAME, qa)):
        for name, path in entries.items():
            relative = path.relative_to(LANE).as_posix()
            if path.resolve() in {SCRIPT.resolve(), FROZEN_LEDGER.resolve()}:
                continue
            if relative not in frozen:
                raise RuntimeError(f"unfrozen {archive_name} input: {name} <- {relative}")

    STAGING.mkdir(parents=False)
    try:
        source_zip = base.deterministic_zip(STAGING / SOURCE_ZIP_NAME, source)
        qa_zip = base.deterministic_zip(STAGING / QA_ZIP_NAME, qa)
        copies = {
            PDF_NAME: base.lane_path(PDF_INPUT), HTML_NAME: base.lane_path(HTML_INPUT),
            "LICENSE.md": RELEASE / "LICENSE.md", "README_RELEASE.md": RELEASE / "README_RELEASE.md",
            "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md",
        }
        base.assert_safe_text(copies[HTML_NAME])
        for name, source_path in copies.items():
            shutil.copyfile(source_path, STAGING / name)

        manifest = dict(manifest_template)
        manifest.pop("template_state", None)
        manifest.pop("generated_fields", None)
        manifest.update(
            {
                "metadata_sha256": base.sha(RELEASE / "metadata.json"),
                "publication_plan_sha256": base.sha(RELEASE / "publication-plan.json"),
                "frozen_input_ledger": {**base.identity(FROZEN_LEDGER), "entries": len(frozen), "final_boundary_paths": sorted(FINAL_BOUNDARY_PATHS)},
                "sources": {
                    "roberts": {"author": "David Michael Roberts", "commit": ROBERTS_COMMIT, "tree": ROBERTS_TREE, "path": "Notes.tex", "line_start": 134, "line_end": 6368, "edition_units": 30, "complete": True, "license": "CC BY 4.0"},
                    "fomberg": {"author": "Yeheli Fomberg", "lecture_credit": "Nir Lazarovich", "commit": FOMBERG_COMMIT, "tree": FOMBERG_TREE, "path": "algebraic_topology.tex", "line_start": 31, "line_end": 4185, "sections": "1.1-1.13", "component_ids": [f"O012-FOM-{i:03d}" for i in range(1, 8)], "next_source_line": 4186, "complete_at_selected_boundary": True, "license": "CC BY-SA 4.0"},
                    "composite_course_complete": False,
                },
                "assessment": {
                    "assessment_id": "D60-CA01", "edition_unit_id": "O012-ORIG-CA01",
                    "origin": "edition_original", "license": "CC BY-SA 4.0",
                    "source_problem_bank_used": False, "complete": True,
                    "exercises": 8, "hints": 8, "complete_solutions": 8,
                    "primary_routes": [f"D60-R{i:02d}" for i in range(1, 8)],
                    "source": ca01["reader"]["identity"],
                },
                "ordinary_hints": {
                    "edition_unit_id": "O012-ORIG-HINTS-R01-R06",
                    "origin": "edition_original", "license": "CC BY-SA 4.0",
                    "source_problem_bank_used": False, "complete": True,
                    "hints": 36, "bound_existing_exercises": 36,
                    "bound_existing_complete_solutions": 36,
                    "hint_count": 36, "hints_per_route": 6,
                    "duplicate_exercises": 0, "duplicate_solutions": 0,
                    "routes": [f"D60-R{i:02d}" for i in range(1, 7)],
                    "ordinary_mastery_closed": "84/84",
                    "source": hints["source"],
                },
                "course_closure": {
                    "composite_course_complete": False,
                    "ordinary_mastery_complete": True,
                    "ordinary_mastery_items": 84,
                    "ordinary_mastery_required": 84,
                    "completed_assessments": ["D60-CA01"],
                    "completed_assessment_items": 8,
                    "total_solution_bearing_items": 92,
                    "total_solution_bearing_items_required": 108,
                    "remaining_assessments": ["D60-CA02", "D60-CA03"],
                    "remaining_assessment_items": 16,
                    "ordinary_hint_triples_remaining": route_census["next_deficits"]["ordinary_missing_triples"],
                    "computation_labs_remaining": 4, "capstone_remaining": 1,
                    "proof_repair_census_status": proof_census["status"],
                    "proof_repair_graph_findings": len(proof_census.get("findings", [])),
                },
                "reader_qa": {
                    "status": "PASS", "pdf_pages": 482, "pdf_tagged": False,
                    "pdf_all_fonts_embedded_subset_tounicode": True,
                    "html_unique_dom_ids": build_receipt["html_checks"]["live_browser_unique_dom_ids"],
                    "html_fragment_links": build_receipt["html_checks"]["fragment_links"],
                    "html_mathml_nodes": build_receipt["html_checks"]["mathml_nodes"],
                    "html_self_contained": True, "ca01_stable_ids": 34,
                    "ca01_exercise_hint_solution_triples": 8,
                    "ordinary_hint_blocks": 36, "visible_predecessor_links": 72,
                    "visual_status": visual_receipt["status"], "browser_status": browser_receipt["status"],
                    "pdf_untagged_limitation_disclosed": True,
                },
                "backend": {**backend_facts, "cumulative_receipt": base.identity(base.lane_path(BACKEND_CUMULATIVE)), "latest_edition_unit_id": backend_receipt["edition_unit_id"]},
                "archives": [source_zip, qa_zip], "artifacts": [],
                "privacy": {"credential_material": False, "absolute_local_paths": False, "user_personal_name": False, "cache_or_temp_render_payload": False, "raw_coordination_dump": False},
                "production_provenance": MODEL_NOTE, "credentials_used": False, "network_actions": 0,
            }
        )
        for name in manifest_template["artifact_order"]:
            path = STAGING / name
            manifest["artifacts"].append({"filename": name, "bytes": path.stat().st_size, "sha256": base.sha(path)})
        base.write_json(STAGING / "release-manifest.json", manifest)
        sums = "\n".join(f"{base.sha(STAGING / name)}  {name}" for name in checksum_names) + "\n"
        (STAGING / "SHA256SUMS").write_text(sums, encoding="utf-8", newline="\n")

        expected_names = sorted(checksum_names + ["SHA256SUMS"])
        actual_names = sorted(path.name for path in STAGING.iterdir() if path.is_file())
        if actual_names != expected_names:
            raise RuntimeError(f"staged payload inventory mismatch: {actual_names}")
        for name in actual_names:
            path = STAGING / name
            if path.suffix.lower() not in {".pdf", ".zip"}:
                base.assert_safe_text(path)
        parsed = {}
        for line in (STAGING / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
            digest, name = line.split("  ", 1)
            if name in parsed:
                raise RuntimeError(f"duplicate checksum row: {name}")
            parsed[name] = digest
        if parsed != {name: base.sha(STAGING / name) for name in checksum_names}:
            raise RuntimeError("SHA256SUMS does not bind every payload file")
        STAGING.replace(ARTIFACTS)
    except Exception:
        if STAGING.exists():
            shutil.rmtree(STAGING)
        raise
    write_package_receipt(frozen, source_zip, qa_zip)
    print(json.dumps({"status": "PASS_PREPARED_NOT_PUBLISHED", "release_id": RELEASE_ID, "files": [base.identity(path) | {"filename": path.name} for path in sorted(ARTIFACTS.iterdir())]}, ensure_ascii=False, indent=2))


for name, value in {
    "source_entries": source_entries, "source_path_inventory": source_path_inventory,
    "qa_path_inventory": qa_path_inventory, "release_control_inventory": release_control_inventory,
    "required_frozen_paths": required_frozen_paths, "qa_entries": qa_entries,
}.items():
    setattr(base, name, value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-required-inputs", action="store_true")
    parser.add_argument("--seal-frozen-inputs", action="store_true")
    args = parser.parse_args()
    if args.list_required_inputs:
        base.list_required_inputs()
    elif args.seal_frozen_inputs:
        seal_frozen_inputs()
    else:
        package()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise
