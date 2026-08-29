#!/usr/bin/env python3
"""Seal and package the computation-Labs-1-4 successor (local only).

This fail-closed successor reuses the proved Lab 3 deterministic ZIP/privacy
helpers. It never uses Git, credentials, or the network. The exact Lab 4 QA,
backend-receipt, and cumulative-backend identities are mandatory runtime
inputs for sealing and packaging. Read-only planning remains available before
the release controls exist.
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
PRIOR_SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03"
SLUG = PRIOR_SLUG + "-lab04"
TEMPLATE_PATH = SCRIPT.with_name(f"package-release-{PRIOR_SLUG}.py")
raw_template = TEMPLATE_PATH.read_bytes()
if (
    len(raw_template),
    raw_template.count(b"\n"),
    __import__("hashlib").sha256(raw_template).hexdigest(),
) != (
    31_206,
    751,
    "c9ae97325fd2ef0d4b18b4ec6e71b70441c28f21d1b6ac0b5e89032c8c7d7ca0",
):
    raise RuntimeError("frozen Lab 3 packager identity drift")
SPEC = importlib.util.spec_from_file_location("o012_lab03_packager_template", TEMPLATE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the proved Lab 3 packager")
template = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(template)
base = template.base

INHERITED_SOURCE_ENTRIES = template.source_entries
INHERITED_QA_INVENTORY = template.qa_inventory
INHERITED_VERIFY_ASSESSMENTS = template.INHERITED_VERIFY_ASSESSMENTS
INHERITED_ASSERT_SAFE_BYTES = base.assert_safe_bytes


def assert_safe_bytes(
    data: bytes,
    label: str,
    *,
    allow_generic_privacy_test_markers: bool = False,
) -> None:
    """Permit one exact fail-closed credential-test literal in the Lab 4 validator."""
    normalized = label.replace("\\", "/")
    validator = "scripts/validate-backend-append-only-computation-lab-004.py"
    if normalized.endswith(validator) or normalized.endswith(f"{validator} as {validator}"):
        marker = b"authoriza" + b"tion: bearer"
        if data.lower().count(marker) != 1:
            raise RuntimeError("Lab 4 validator credential-test marker census drift")
        data = data.lower().replace(marker, b"authorization test marker")
    INHERITED_ASSERT_SAFE_BYTES(
        data,
        label,
        allow_generic_privacy_test_markers=allow_generic_privacy_test_markers,
    )


base.assert_safe_bytes = assert_safe_bytes

LANE = SCRIPT.parents[1]
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04"
RELEASE = LANE / "release" / f"zenodo-{SLUG}"
ARTIFACTS = RELEASE / "artifacts"
STAGING = RELEASE / ".package-staging"
FROZEN_LEDGER = RELEASE / "frozen-inputs.json"
PACKAGE_RECEIPT = RELEASE / "PACKAGE_PREPARATION_RECEIPT.json"

TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30, "
    "Jembatan Homologi §1.1–1.13, Asesmen Kumulatif 1–3, "
    "Petunjuk Rute 1–6, dan Laboratorium Komputasi 1–4"
)
VERSION = "0.31.6"
RELEASE_ID = f"o012-composite-id-{SLUG}-v{VERSION}"
CONCEPT_DOI = "10.5281/zenodo.22061489"
PREVIOUS_RECORD_ID = 22_151_513
PREVIOUS_DOI = "10.5281/zenodo.22151513"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"

# Root must replace this with the SHA-256 printed by --seal-frozen-inputs.
# The packager excludes itself from the ledger, so that one apply_patch does
# not invalidate any sealed input.
FROZEN_LEDGER_SHA256 = "b1a48e31213800433102d7fd8733fab32dea6686162604e8eccfb10add4e0388"

PDF_INPUT = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
HTML_INPUT = f"output/html/{SLUG}/index.html"
ARTIFACT_MANIFEST = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
BUILD_DRAFT = f"qa/{TOKEN}_BUILD_DRAFT.json"
BUILD_RECEIPT = f"qa/{TOKEN}_BUILD_RECEIPT.json"
VISUAL_QA = f"qa/{TOKEN}_VISUAL_QA.md"
RENDER_INVENTORY = f"qa/{TOKEN}_RENDER_INVENTORY.csv"
BROWSER_QA = f"qa/{TOKEN}_BROWSER_QA.json"

LAB_QA = "qa/COMPUTATION_LAB_004_QA.json"
LAB_STATIC_QA = "qa/computation-lab-004/STATIC_QA.json"
LAB_MATH_REVIEW = "qa/computation-lab-004/INDEPENDENT_MATH_REVIEW.json"
LAB_LANGUAGE_REVIEW = "qa/computation-lab-004/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
LAB_CODE_REVIEW = "qa/computation-lab-004/INDEPENDENT_CODE_REVIEW.json"
LAB_EXECUTION_RECEIPT = "qa/computation-lab-004/EXECUTION_RECEIPT.json"
BACKEND_CUMULATIVE = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_CUMULATIVE_RECEIPT.json"

LAB_SOURCE = "source/id-ID/labs/computation-lab-004-cross-invariant-comparison.md"
LAB_PROGRAM = "source/id-ID/labs/o012_d60_lab04_cross_invariants.py"
LAB_TESTS = "source/id-ID/labs/test_o012_d60_lab04_cross_invariants.py"
LAB_EXPECTED = "source/id-ID/labs/expected-output-lab04.txt"
ROUTES = ["D60-R04", "D60-R05", "D60-R12", "D60-R13", "D60-R14"]
BACKEND_PREFIX = (7_694, 9_280_385, "cddd65499da547e0c4f01b8a880f68d1c3d314c078a9179528e4a28b2c5f65a2")

PDF_NAME = f"00_TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.pdf"
HTML_NAME = f"TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.html"
SOURCE_ZIP_NAME = f"TOPOLOGI_ALJABAR_ID_{TOKEN}_EDITABLE_SOURCE_BACKEND.zip"
QA_ZIP_NAME = f"TOPOLOGI_ALJABAR_ID_{TOKEN}_QA_PROVENANCE.zip"
SUBSTANTIVE_ORDER = [
    PDF_NAME,
    HTML_NAME,
    SOURCE_ZIP_NAME,
    QA_ZIP_NAME,
    "LICENSE.md",
    "README_RELEASE.md",
    "RELEASE_RIGHTS.md",
]
FILE_NAMES = SUBSTANTIVE_ORDER + ["release-manifest.json", "SHA256SUMS"]
MANIFEST_STATUS = (
    "roberts_complete_fomberg_units_001_007_complete_ca01_ca02_ca03_complete_"
    "ordinary_mastery_84_complete_solution_bearing_mastery_108_complete_"
    "computation_labs_001_002_003_004_complete_composite_course_partial"
)
FINAL_BOUNDARY_PATHS = {
    PDF_INPUT,
    HTML_INPUT,
    ARTIFACT_MANIFEST,
    BUILD_RECEIPT,
    VISUAL_QA,
    RENDER_INVENTORY,
    BROWSER_QA,
    LAB_QA,
    BACKEND_CUMULATIVE,
    "qa/ROUTE_MASTERY_CENSUS.json",
    "qa/PROOF_REPAIR_CENSUS.json",
}
CONTROL_NAMES = (
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

for name, value in {
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


def lane_path(relative: str) -> Path:
    result = (LANE / relative).resolve()
    if LANE.resolve() not in result.parents:
        raise RuntimeError(f"path escaped lane: {relative}")
    return result


def load_json(relative: str) -> dict[str, Any]:
    result = lane_path(relative)
    if not result.is_file():
        raise FileNotFoundError(result)
    return json.loads(result.read_text(encoding="utf-8"))


def identity(relative: str) -> dict[str, Any]:
    result = lane_path(relative)
    if not result.is_file() or result.stat().st_size <= 0:
        raise FileNotFoundError(result)
    return {"path": relative, "bytes": result.stat().st_size, "sha256": base.sha(result)}


def runtime_identity(relative: str, size: int, checksum: str, label: str) -> dict[str, Any]:
    if size <= 0 or re.fullmatch(r"[0-9a-f]{64}", checksum or "") is None:
        raise RuntimeError(f"invalid runtime identity: {label}")
    actual = identity(relative)
    if (actual["bytes"], actual["sha256"]) != (size, checksum):
        raise RuntimeError(f"runtime identity drift: {label}")
    return actual


def require_runtime(args: argparse.Namespace) -> None:
    values = (
        args.lab_qa_bytes,
        args.lab_qa_sha256,
        args.backend_receipt_bytes,
        args.backend_receipt_sha256,
        args.backend_cumulative_records,
        args.backend_cumulative_bytes,
        args.backend_cumulative_sha256,
    )
    if any(value is None for value in values):
        raise RuntimeError("sealing/packaging requires all seven Lab 4 runtime identity arguments")
    runtime_identity(LAB_QA, args.lab_qa_bytes, args.lab_qa_sha256, "Lab 4 QA")
    runtime_identity(BACKEND_CUMULATIVE, args.backend_receipt_bytes, args.backend_receipt_sha256, "Lab 4 backend receipt")
    if args.backend_cumulative_records <= BACKEND_PREFIX[0] or args.backend_cumulative_bytes <= BACKEND_PREFIX[1]:
        raise RuntimeError("Lab 4 cumulative backend did not advance")
    if re.fullmatch(r"[0-9a-f]{64}", args.backend_cumulative_sha256 or "") is None:
        raise RuntimeError("invalid Lab 4 cumulative backend SHA-256")


def source_entries() -> dict[str, Path]:
    entries = INHERITED_SOURCE_ENTRIES()
    additions = {
        LAB_SOURCE,
        LAB_PROGRAM,
        LAB_TESTS,
        LAB_EXPECTED,
        "scripts/merge-computation-lab-004.py",
        "scripts/qa-computation-lab-004.py",
        "scripts/finalize-computation-lab-004-qa.py",
        "scripts/extend-backend-computation-lab-004.py",
        "scripts/validate-backend-append-only-computation-lab-004.py",
        f"scripts/build-{SLUG}.py",
        f"scripts/finalize-build-{SLUG}.py",
        f"scripts/package-release-{SLUG}.py",
        f"scripts/publish-zenodo-{SLUG}.py",
    }
    entries.update({relative: lane_path(relative) for relative in additions})
    return entries


def qa_inventory() -> set[str]:
    paths = set(INHERITED_QA_INVENTORY())
    paths.update(
        {
            LAB_QA,
            LAB_STATIC_QA,
            LAB_CODE_REVIEW,
            LAB_MATH_REVIEW,
            LAB_LANGUAGE_REVIEW,
            LAB_EXECUTION_RECEIPT,
            "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_FILE_MANIFEST.csv",
            "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_PLAN.json",
            "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_RECEIPT.json",
            "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_REPLAY_RECEIPT.json",
            BACKEND_CUMULATIVE,
            BUILD_DRAFT,
            BUILD_RECEIPT,
            VISUAL_QA,
            RENDER_INVENTORY,
            BROWSER_QA,
        }
    )
    return paths


def control_inventory() -> set[str]:
    prefix = RELEASE.relative_to(LANE).as_posix() + "/"
    return {prefix + name for name in CONTROL_NAMES}


def required_paths() -> set[str]:
    source = set(source_entries())
    source.discard(f"scripts/package-release-{SLUG}.py")
    return FINAL_BOUNDARY_PATHS | source | qa_inventory() | control_inventory()


def verify_lab(args: argparse.Namespace) -> dict[str, Any]:
    runtime_identity(LAB_QA, args.lab_qa_bytes, args.lab_qa_sha256, "Lab 4 QA")
    qa = load_json(LAB_QA)
    checks = qa.get("checks", {})
    if not (
        qa.get("status") == "PASS"
        and qa.get("receipt_kind") == "computation_laboratory_source_execution_review_closure"
        and qa.get("laboratory_id") == "D60-LAB04"
        and qa.get("edition_unit_id") == "O012-ORIG-LAB04"
        and qa.get("course_route_unit_ids") == ROUTES
        and checks.get("stable_ids_25_unique") == "PASS"
        and checks.get("tasks_6_with_hint_and_complete_solution") == "PASS"
        and checks.get("offline_program_and_tests") == "PASS"
        and checks.get("expected_output_exact") == "PASS"
        and checks.get("two_program_runs_byte_identical") == "PASS"
        and checks.get("two_test_runs_6_of_6") == "PASS"
        and checks.get("independent_code") == "PASS"
        and checks.get("independent_mathematics") == "PASS"
        and checks.get("independent_source_language") == "PASS"
        and checks.get("excluded_fomberg_problem_bank_used") is False
        and qa.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}
    ):
        raise RuntimeError("computation Lab 4 source/execution/review closure mismatch")
    indexed = {row.get("path"): row for row in qa.get("inputs", [])}
    for relative in (LAB_SOURCE, LAB_PROGRAM, LAB_TESTS, LAB_EXPECTED):
        if relative not in indexed or not base.identity_matches(indexed[relative], lane_path(relative)):
            raise RuntimeError(f"Lab 4 QA has a stale source identity: {relative}")
    for relative in (LAB_STATIC_QA, LAB_CODE_REVIEW, LAB_MATH_REVIEW, LAB_LANGUAGE_REVIEW, LAB_EXECUTION_RECEIPT):
        if not str(load_json(relative).get("status", "")).startswith("PASS"):
            raise RuntimeError(f"Lab 4 review/execution receipt failed: {relative}")
    return qa


def verify_backend(args: argparse.Namespace) -> dict[str, Any]:
    runtime_identity(BACKEND_CUMULATIVE, args.backend_receipt_bytes, args.backend_receipt_sha256, "Lab 4 backend receipt")
    receipt = load_json(BACKEND_CUMULATIVE)
    prefix, final, replay = receipt.get("immutable_prefix", {}), receipt.get("cumulative", {}), receipt.get("replay", {})
    expected_final = (args.backend_cumulative_records, args.backend_cumulative_bytes, args.backend_cumulative_sha256)
    if not (
        receipt.get("status") == "PASS"
        and receipt.get("receipt_kind") == "cumulative_backend_boundary"
        and receipt.get("laboratory_id") == "D60-LAB04"
        and receipt.get("edition_unit_id") == "O012-ORIG-LAB04"
        and prefix.get("preserved_exactly") is True
        and (prefix.get("records"), prefix.get("bytes"), prefix.get("bundle_sha256")) == BACKEND_PREFIX
        and (final.get("records"), final.get("bytes"), final.get("bundle_sha256")) == expected_final
        and final.get("computation_laboratories_complete") == 4
        and final.get("computation_laboratories_required") == 4
        and replay.get("status") == "PASS"
        and replay.get("temporary_replay_removed") is True
        and (replay.get("final", {}).get("records"), replay.get("final", {}).get("bytes"), replay.get("final", {}).get("bundle_sha256")) == expected_final
        and isinstance(receipt.get("files"), list)
        and len(receipt.get("files", [])) == 11
        and all(row.get("prefix_preserved") is True and row.get("suffix_exact") is True for row in receipt.get("files", []))
    ):
        raise RuntimeError("Lab 4 cumulative backend boundary mismatch")
    return receipt


def verify_controls(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    for name in CONTROL_NAMES:
        result = RELEASE / name
        if not result.is_file():
            raise FileNotFoundError(result)
        base.assert_safe_text(result)
    metadata_payload = json.loads((RELEASE / "metadata.json").read_text(encoding="utf-8"))
    metadata = metadata_payload.get("metadata", {})
    expected_contributors = [
        {"name": "Lazarovich, Nir", "type": "Other"},
        {"name": "Editor edisi Bahasa Indonesia", "type": "Editor"},
        {"name": "Translation and Transcription Project", "type": "Other"},
    ]
    if not (
        metadata.get("title") == TITLE
        and metadata.get("version") == VERSION
        and metadata.get("license") == "cc-by-sa-4.0"
        and metadata.get("language") == "ind"
        and metadata.get("access_right") == "open"
        and metadata.get("creators") == [{"name": "Roberts, David Michael"}, {"name": "Fomberg, Yeheli"}]
        and metadata.get("contributors") == expected_contributors
    ):
        raise RuntimeError("Lab 4 successor metadata identity/rights/creator drift")
    prose = "\n".join(str(metadata.get(key, "")) for key in ("title", "description", "notes"))
    prose += "\n" + "\n".join(str(value) for value in metadata.get("keywords", []))
    if re.search(r"(?i)\bTTP\b|Translation and Transcription Project", prose):
        raise RuntimeError("organization marker leaked into title/prose metadata")
    controls = "\n".join((RELEASE / name).read_text(encoding="utf-8") for name in CONTROL_NAMES)
    for marker in ("108/108", "D60-CA01", "D60-CA02", "D60-CA03", "D60-LAB01", "D60-LAB02", "D60-LAB03", "D60-LAB04", "CC BY 4.0", "CC BY-SA 4.0", MODEL_NOTE):
        if marker not in controls:
            raise RuntimeError(f"release controls omit exact marker: {marker}")
    if controls.count("Translation and Transcription Project") != 1:
        raise RuntimeError("organization must occur exactly once across release controls")

    plan = json.loads((RELEASE / "publication-plan.json").read_text(encoding="utf-8"))
    if not (
        plan.get("state") == "prepared_not_published"
        and plan.get("release_id") == RELEASE_ID
        and plan.get("version") == VERSION
        and plan.get("existing_concept_doi") == CONCEPT_DOI
        and plan.get("current_public_record_id") == PREVIOUS_RECORD_ID
        and plan.get("current_public_doi") == PREVIOUS_DOI
        and plan.get("new_concept_allowed") is False
        and plan.get("new_deposition_created") is False
        and plan.get("credentials_used") is False
        and plan.get("publish_not_draft") is True
        and plan.get("anonymous_byte_readback_required") is True
        and plan.get("reader_first_filename") == PDF_NAME
    ):
        raise RuntimeError("publication plan escaped the existing concept or Lab 3 predecessor")
    binding = plan.get("backend_binding", {})
    snapshot = binding.get("verified_snapshot", {})
    if not (
        binding.get("final_identity_source") == BACKEND_CUMULATIVE
        and binding.get("expected_records") == args.backend_cumulative_records
        and snapshot.get("total_records") == args.backend_cumulative_records
        and snapshot.get("total_bytes") == args.backend_cumulative_bytes
        and snapshot.get("bundle_sha256") == args.backend_cumulative_sha256
    ):
        raise RuntimeError("publication plan does not bind the runtime Lab 4 backend")
    readers = plan.get("final_reader_artifacts", {})
    for role, relative in (("pdf", PDF_INPUT), ("html", HTML_INPUT)):
        row = readers.get(role, {})
        if row.get("path") != relative or not base.identity_matches(row, lane_path(relative)):
            raise RuntimeError(f"publication plan lacks exact final {role} identity")

    manifest = json.loads((RELEASE / "release-manifest.template.json").read_text(encoding="utf-8"))
    original_ids = manifest.get("component_numbering", {}).get("original_edition_unit_ids", [])
    if not (
        manifest.get("release_id") == RELEASE_ID
        and manifest.get("version") == VERSION
        and manifest.get("status") == MANIFEST_STATUS
        and manifest.get("artifact_order") == SUBSTANTIVE_ORDER
        and all(value in original_ids for value in ("O012-ORIG-LAB01", "O012-ORIG-LAB02", "O012-ORIG-LAB03", "O012-ORIG-LAB04"))
    ):
        raise RuntimeError("release-manifest template drift")
    sums = [line.split("  ", 1)[1] for line in (RELEASE / "SHA256SUMS.template").read_text(encoding="utf-8").splitlines()]
    if sums != SUBSTANTIVE_ORDER + ["release-manifest.json"]:
        raise RuntimeError("checksum template is not exact and reader-first")
    return metadata_payload, plan, manifest


def verify_final_gates(args: argparse.Namespace, plan: dict[str, Any]) -> dict[str, Any]:
    build, browser = load_json(BUILD_RECEIPT), load_json(BROWSER_QA)
    visual_text = lane_path(VISUAL_QA).read_text(encoding="utf-8")
    if build.get("status") != "PASS":
        raise RuntimeError("final Lab 4 build receipt did not pass")
    pdf, html = build.get("pdf", {}), build.get("html", {})
    if not base.identity_matches(pdf, lane_path(PDF_INPUT)) or not base.identity_matches(html, lane_path(HTML_INPUT)):
        raise RuntimeError("build receipt does not bind the final Lab 4 readers")
    pdf_pages = pdf.get("pages")
    if not isinstance(pdf_pages, int) or pdf_pages <= 545 or pdf.get("page_size") != "A4":
        raise RuntimeError("Lab 4 PDF identity/page boundary drift")
    if plan.get("final_reader_artifacts", {}).get("pdf", {}).get("pages") != pdf_pages:
        raise RuntimeError("publication plan PDF page count differs from final build")
    lab, backend = build.get("source_execution_review", {}), build.get("backend_boundary", {})
    if not (
        lab.get("status") == "PASS"
        and lab.get("tasks") == 6
        and lab.get("tests") == 6
        and lab.get("stable_ids") == 25
        and backend.get("cumulative_records") == args.backend_cumulative_records
        and backend.get("cumulative_bytes") == args.backend_cumulative_bytes
        and backend.get("cumulative_bundle_sha256") == args.backend_cumulative_sha256
        and backend.get("laboratories_complete") == 4
        and backend.get("laboratories_required") == 4
    ):
        raise RuntimeError("final build does not bind the Lab 4 source/backend closure")
    if not (
        browser.get("status") == "PASS"
        and base.identity_matches(browser.get("artifact", {}), lane_path(HTML_INPUT))
        and browser.get("desktop", {}).get("page_level_horizontal_overflow") is False
        and browser.get("mobile", {}).get("page_level_horizontal_overflow") is False
        and browser.get("semantic_and_binding_checks", {}).get("unresolved_fragment_links") == 0
        and browser.get("console", {}).get("errors") == 0
    ):
        raise RuntimeError("Lab 4 browser QA did not pass")
    if "Status: **PASS**" not in visual_text or pdf["sha256"] not in visual_text:
        raise RuntimeError("Lab 4 visual QA does not bind the final PDF")
    for relative, row in (
        (VISUAL_QA, build.get("visual_checks", {}).get("visual_receipt", {})),
        (RENDER_INVENTORY, build.get("visual_checks", {}).get("render_inventory", {})),
        (BROWSER_QA, build.get("browser_checks", {}).get("browser_receipt", {})),
        (LAB_QA, build.get("source_execution_review", {}).get("receipt", {})),
    ):
        if not base.identity_matches(row, lane_path(relative)):
            raise RuntimeError(f"final build has a stale QA binding: {relative}")
    if build.get("remaining", {}).get("computation_labs") != []:
        raise RuntimeError("Lab 4 build has dishonest remaining-laboratory state")
    if not lane_path(ARTIFACT_MANIFEST).is_file():
        raise FileNotFoundError(lane_path(ARTIFACT_MANIFEST))
    return build


def qa_entries() -> dict[str, Path]:
    entries = {relative: lane_path(relative) for relative in sorted(qa_inventory())}
    entries.update(
        {
            "release/frozen-inputs.json": FROZEN_LEDGER,
            "release/frozen-inputs.template.json": RELEASE / "frozen-inputs.template.json",
            "release/release-manifest.template.json": RELEASE / "release-manifest.template.json",
            "release/SHA256SUMS.template": RELEASE / "SHA256SUMS.template",
        }
    )
    return entries


def seal(args: argparse.Namespace) -> None:
    require_runtime(args)
    if FROZEN_LEDGER.exists():
        raise RuntimeError("frozen-inputs.json already exists; refusing to overwrite")
    _, plan, _ = verify_controls(args)
    INHERITED_VERIFY_ASSESSMENTS()
    verify_lab(args)
    verify_backend(args)
    verify_final_gates(args, plan)
    rows = []
    for relative in sorted(required_paths()):
        result = lane_path(relative)
        if not result.is_file():
            raise FileNotFoundError(result)
        base.assert_safe_bytes(result.read_bytes(), relative, allow_generic_privacy_test_markers=relative.startswith("scripts/"))
        rows.append(identity(relative))
    base.write_json(FROZEN_LEDGER, {"schema_version": "1.0", "release_id": RELEASE_ID, "state": "final_inputs_sealed_local_only", "runtime_boundary_bindings": {"lab_qa": identity(LAB_QA), "backend_receipt": identity(BACKEND_CUMULATIVE), "backend_cumulative": {"records": args.backend_cumulative_records, "bytes": args.backend_cumulative_bytes, "bundle_sha256": args.backend_cumulative_sha256}}, "final_boundary_paths": sorted(FINAL_BOUNDARY_PATHS), "entries": rows})
    print(json.dumps({"status": "SEALED_LEDGER_REQUIRES_APPLY_PATCH_BINDING", **base.identity(FROZEN_LEDGER), "entries": len(rows)}, indent=2))


def package(args: argparse.Namespace) -> None:
    require_runtime(args)
    if re.fullmatch(r"[0-9a-f]{64}", FROZEN_LEDGER_SHA256) is None:
        raise RuntimeError("FROZEN_LEDGER_SHA256 must be apply-patch-bound after sealing")
    if ARTIFACTS.exists() or STAGING.exists():
        raise RuntimeError("refusing to overwrite artifacts or stale staging")
    metadata, plan, manifest_template = verify_controls(args)
    INHERITED_VERIFY_ASSESSMENTS()
    lab_qa, backend = verify_lab(args), verify_backend(args)
    build = verify_final_gates(args, plan)
    base.required_frozen_paths = required_paths
    frozen = base.load_frozen_inputs()
    source, qa = source_entries(), qa_entries()
    base.assert_source_archive_link_closure(source)
    for entries in (source, qa):
        for result in entries.values():
            if result.resolve() not in {SCRIPT.resolve(), FROZEN_LEDGER.resolve()}:
                relative = result.relative_to(LANE).as_posix()
                if relative not in frozen:
                    raise RuntimeError(f"unfrozen archive input: {relative}")

    STAGING.mkdir(parents=False)
    try:
        source_zip = base.deterministic_zip(STAGING / SOURCE_ZIP_NAME, source)
        qa_zip = base.deterministic_zip(STAGING / QA_ZIP_NAME, qa)
        copies = {PDF_NAME: lane_path(PDF_INPUT), HTML_NAME: lane_path(HTML_INPUT), "LICENSE.md": RELEASE / "LICENSE.md", "README_RELEASE.md": RELEASE / "README_RELEASE.md", "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md"}
        for name, result in copies.items():
            shutil.copyfile(result, STAGING / name)
        manifest = dict(manifest_template)
        manifest.pop("template_state", None)
        manifest.pop("generated_fields", None)
        manifest.update(
            {
                "metadata_sha256": base.sha(RELEASE / "metadata.json"),
                "publication_plan_sha256": base.sha(RELEASE / "publication-plan.json"),
                "frozen_input_ledger": {**base.identity(FROZEN_LEDGER), "entries": len(frozen)},
                "runtime_boundary_bindings": {"lab_qa": identity(LAB_QA), "backend_receipt": identity(BACKEND_CUMULATIVE), "backend_cumulative": {"records": args.backend_cumulative_records, "bytes": args.backend_cumulative_bytes, "bundle_sha256": args.backend_cumulative_sha256}},
                "assessments": {"completed": ["D60-CA01", "D60-CA02", "D60-CA03"], "edition_unit_ids": ["O012-ORIG-CA01", "O012-ORIG-CA02", "O012-ORIG-CA03"], "items": 24, "hints": 24, "complete_solutions": 24, "origin": "edition_original", "license": "CC BY-SA 4.0", "source_problem_bank_used": False},
                "laboratories": {"completed": ["D60-LAB01", "D60-LAB02", "D60-LAB03", "D60-LAB04"], "edition_unit_ids": ["O012-ORIG-LAB01", "O012-ORIG-LAB02", "O012-ORIG-LAB03", "O012-ORIG-LAB04"], "required": 4, "completed_count": 4, "remaining": [], "tasks": 24, "tests": 24, "stable_ids": 99, "offline_reproducible": True, "origin": "edition_original", "license": "CC BY-SA 4.0", "qa_receipts": [identity("qa/COMPUTATION_LAB_001_QA.json"), identity("qa/COMPUTATION_LAB_002_QA.json"), identity("qa/COMPUTATION_LAB_003_QA.json"), identity(LAB_QA)]},
                "course_closure": {"ordinary_mastery_complete": True, "ordinary_mastery_items": 84, "cumulative_assessment_items": 24, "total_solution_bearing_items": 108, "total_solution_bearing_items_required": 108, "cumulative_assessment_mastery_complete": True, "computation_laboratories_complete": 4, "computation_laboratories_required": 4, "computation_labs_remaining": 0, "proof_metadata_closure_pending": True, "capstone_remaining": 1, "composite_course_complete": False},
                "backend": {**backend["cumulative"], "cumulative_receipt": identity(BACKEND_CUMULATIVE)},
                "reader_qa": {"status": "PASS", "pdf_pages": build["pdf"]["pages"], "pdf_all_fonts_embedded_subset_tounicode": True, "html_self_contained": True, "html_centered_reflow": True, "laboratory_stable_ids_added": 25, "laboratory_tasks_added": 6, "source_execution_review_status": lab_qa["status"]},
                "archives": [source_zip, qa_zip],
                "artifacts": [],
                "rights": {"integrated_payload": "CC BY-SA 4.0", "roberts_component": "CC BY 4.0", "fomberg_component": "CC BY-SA 4.0", "original_assessment_components": "CC BY-SA 4.0", "original_hint_component": "CC BY-SA 4.0", "original_laboratory_component": "CC BY-SA 4.0", "non_endorsement_preserved": True},
                "publication_lineage": {"existing_concept_doi": CONCEPT_DOI, "previous_record_id": PREVIOUS_RECORD_ID, "previous_version_doi": PREVIOUS_DOI, "new_concept_created": False},
                "production_provenance": MODEL_NOTE,
                "privacy": {"credential_material": False, "absolute_local_paths": False, "user_personal_name": False},
            }
        )
        for name in SUBSTANTIVE_ORDER:
            result = STAGING / name
            manifest["artifacts"].append({"filename": name, "bytes": result.stat().st_size, "sha256": base.sha(result)})
        base.write_json(STAGING / "release-manifest.json", manifest)
        checksum_names = SUBSTANTIVE_ORDER + ["release-manifest.json"]
        (STAGING / "SHA256SUMS").write_text("\n".join(f"{base.sha(STAGING / name)}  {name}" for name in checksum_names) + "\n", encoding="utf-8", newline="\n")
        if sorted(result.name for result in STAGING.iterdir()) != sorted(FILE_NAMES):
            raise RuntimeError("staged payload inventory mismatch")
        STAGING.replace(ARTIFACTS)
    except Exception:
        if STAGING.exists():
            shutil.rmtree(STAGING)
        raise
    files = [{"filename": result.name, "bytes": result.stat().st_size, "sha256": base.sha(result)} for result in sorted(ARTIFACTS.iterdir())]
    base.write_json(PACKAGE_RECEIPT, {"schema_version": "1.0", "status": "PASS_PREPARED_NOT_PUBLISHED", "release_id": RELEASE_ID, "version": VERSION, "reader_first_filename": PDF_NAME, "scope": "Roberts 30/30; Fomberg 1.1–1.13; ordinary mastery 84/84; cumulative assessments 24/24; solution-bearing mastery 108/108; computation Labs 1–4 complete; proof-metadata closure and capstone pending", "frozen_input_ledger": base.identity(FROZEN_LEDGER), "files": files, "file_count": len(files), "total_payload_bytes": sum(row["bytes"] for row in files), "archives": [source_zip, qa_zip], "verification": {"reader_first": True, "zip_crc_and_inventory_pass": True, "final_build_visual_browser_gates": True, "laboratory_source_execution_reviews": True, "backend_exact_replay": True, "rights_component_scope_consistent": True, "network_actions": 0, "credentials_used": False, "published": False}})
    print(json.dumps({"status": "PASS_PREPARED_NOT_PUBLISHED", "release_id": RELEASE_ID, "files": files}, ensure_ascii=False, indent=2))


def plan() -> None:
    print(json.dumps({"status": "PREPARED_SCRIPT_NOT_EXECUTED", "release_id": RELEASE_ID, "version": VERSION, "concept_doi": CONCEPT_DOI, "previous_record_id": PREVIOUS_RECORD_ID, "previous_doi": PREVIOUS_DOI, "reader_first_filename": PDF_NAME, "release_directory": RELEASE.relative_to(LANE).as_posix(), "final_boundary_paths": sorted(FINAL_BOUNDARY_PATHS), "runtime_bindings_required": ["exact Lab 4 QA receipt bytes/SHA-256", "exact Lab 4 cumulative backend receipt bytes/SHA-256", "exact cumulative backend records/bytes/bundle SHA-256"], "post_build_bindings_required": ["final Lab 4 build receipt and exact PDF/HTML identities/pages", "visual, render-inventory, and browser QA receipts", "Lab 4 source/execution/review and exact backend replay receipts", "v0.31.6 release controls and checksum template", "sealed frozen-input ledger SHA-256 apply-patch binding"]}, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--list-required-inputs", action="store_true")
    parser.add_argument("--seal-frozen-inputs", action="store_true")
    parser.add_argument("--lab-qa-bytes", type=int)
    parser.add_argument("--lab-qa-sha256")
    parser.add_argument("--backend-receipt-bytes", type=int)
    parser.add_argument("--backend-receipt-sha256")
    parser.add_argument("--backend-cumulative-records", type=int)
    parser.add_argument("--backend-cumulative-bytes", type=int)
    parser.add_argument("--backend-cumulative-sha256")
    args = parser.parse_args()
    if args.plan:
        plan()
    elif args.list_required_inputs:
        print("\n".join(sorted(required_paths())))
    elif args.seal_frozen_inputs:
        seal(args)
    else:
        package(args)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise
