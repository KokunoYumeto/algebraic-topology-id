#!/usr/bin/env python3
"""Seal and package the v0.31.2 CA02/CA03 successor (local only).

This is the fail-closed successor of the proved v0.31.1 packager.  It never
uses Git, credentials, or the network.  `--plan` and `--list-required-inputs`
are read-only; sealing and packaging are explicit operations and refuse
unbound build/QA/control bytes.
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
TEMPLATE_PATH = SCRIPT.with_name(
    "package-release-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.py"
)
SPEC = importlib.util.spec_from_file_location("o012_v0311_packager_template", TEMPLATE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the proved v0.31.1 packager")
template = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(template)
base = template.base

LANE = SCRIPT.parents[1]
SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03"
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03"
RELEASE = LANE / "release" / f"zenodo-{SLUG}"
ARTIFACTS = RELEASE / "artifacts"
STAGING = RELEASE / ".package-staging"
FROZEN_LEDGER = RELEASE / "frozen-inputs.json"
PACKAGE_RECEIPT = RELEASE / "PACKAGE_PREPARATION_RECEIPT.json"

TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30, "
    "Jembatan Homologi §1.1–1.13, Asesmen Kumulatif 1–3, dan Petunjuk Rute 1–6"
)
VERSION = "0.31.2"
RELEASE_ID = f"o012-composite-id-{SLUG}-v{VERSION}"
CONCEPT_DOI = "10.5281/zenodo.22061489"
PREVIOUS_RECORD_ID = 22106133
PREVIOUS_DOI = "10.5281/zenodo.22106133"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"
FROZEN_LEDGER_SHA256 = "845ea9496fbf6d6f31354df18e8f8c938a1faf9024c7c5911c6e94699b5d42ef"

PDF_INPUT = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
HTML_INPUT = f"output/html/{SLUG}/index.html"
ARTIFACT_MANIFEST = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
BUILD_RECEIPT = f"qa/{TOKEN}_BUILD_RECEIPT.json"
VISUAL_QA = f"qa/{TOKEN}_VISUAL_QA.md"
RENDER_INVENTORY = f"qa/{TOKEN}_RENDER_INVENTORY.csv"
BROWSER_QA = f"qa/{TOKEN}_BROWSER_QA.json"
BACKEND_CUMULATIVE = "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_CUMULATIVE_RECEIPT.json"
COMBINED_QA = "qa/CUMULATIVE_ASSESSMENTS_002_003_QA.json"
CA02_SOURCE = "source/id-ID/mastery/cumulative-assessment-002-homology-excision-cellular.md"
CA03_SOURCE = "source/id-ID/mastery/cumulative-assessment-003-cohomology-degree-synthesis.md"
CA02_MATH = "qa/cumulative-assessment-002/INDEPENDENT_MATH_REVIEW.json"
CA02_LANGUAGE = "qa/cumulative-assessment-002/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
CA03_MATH = "qa/cumulative-assessment-003/INDEPENDENT_MATH_REVIEW.json"
CA03_LANGUAGE = "qa/cumulative-assessment-003/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
ROUTE_CENSUS = "qa/ROUTE_MASTERY_CENSUS.json"
PROOF_CENSUS = "qa/PROOF_REPAIR_CENSUS.json"

PDF_NAME = f"00_TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.pdf"
HTML_NAME = f"TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.html"
SOURCE_ZIP_NAME = f"TOPOLOGI_ALJABAR_ID_{TOKEN}_EDITABLE_SOURCE_BACKEND.zip"
QA_ZIP_NAME = f"TOPOLOGI_ALJABAR_ID_{TOKEN}_QA_PROVENANCE.zip"
SUBSTANTIVE_ORDER = [
    PDF_NAME, HTML_NAME, SOURCE_ZIP_NAME, QA_ZIP_NAME,
    "LICENSE.md", "README_RELEASE.md", "RELEASE_RIGHTS.md",
]
FILE_NAMES = SUBSTANTIVE_ORDER + ["release-manifest.json", "SHA256SUMS"]
MANIFEST_STATUS = (
    "roberts_complete_fomberg_units_001_007_complete_ca01_ca02_ca03_complete_"
    "ordinary_mastery_84_complete_solution_bearing_mastery_108_complete_composite_course_partial"
)

FINAL_BOUNDARY_PATHS = {
    PDF_INPUT, HTML_INPUT, ARTIFACT_MANIFEST, BUILD_RECEIPT, VISUAL_QA,
    RENDER_INVENTORY, BROWSER_QA, BACKEND_CUMULATIVE, COMBINED_QA,
    ROUTE_CENSUS, PROOF_CENSUS,
}
CONTROL_NAMES = (
    "metadata.json", "publication-plan.json", "README_RELEASE.md",
    "SOURCE_PACKAGE_README.md", "LICENSE.md", "RELEASE_RIGHTS.md",
    "release-manifest.template.json", "SHA256SUMS.template",
    "frozen-inputs.template.json",
)

# Rebind inherited deterministic ZIP/privacy/path helpers to this release.
for name, value in {
    "RELEASE": RELEASE, "ARTIFACTS": ARTIFACTS, "STAGING": STAGING,
    "FROZEN_LEDGER": FROZEN_LEDGER, "PACKAGE_RECEIPT": PACKAGE_RECEIPT,
    "TITLE": TITLE, "VERSION": VERSION, "RELEASE_ID": RELEASE_ID,
    "CONCEPT_DOI": CONCEPT_DOI, "PREVIOUS_RECORD_ID": PREVIOUS_RECORD_ID,
    "PREVIOUS_DOI": PREVIOUS_DOI, "FROZEN_LEDGER_SHA256": FROZEN_LEDGER_SHA256,
    "PDF_INPUT": PDF_INPUT, "HTML_INPUT": HTML_INPUT,
    "ARTIFACT_MANIFEST": ARTIFACT_MANIFEST, "BUILD_RECEIPT": BUILD_RECEIPT,
    "VISUAL_QA": VISUAL_QA, "RENDER_INVENTORY": RENDER_INVENTORY,
    "BACKEND_CUMULATIVE_JSON": BACKEND_CUMULATIVE,
    "BACKEND_CUMULATIVE_MD": BACKEND_CUMULATIVE,
    "PDF_NAME": PDF_NAME, "HTML_NAME": HTML_NAME,
    "SOURCE_ZIP_NAME": SOURCE_ZIP_NAME, "QA_ZIP_NAME": QA_ZIP_NAME,
    "FINAL_BOUNDARY_PATHS": FINAL_BOUNDARY_PATHS,
}.items():
    setattr(base, name, value)


def lane_path(relative: str) -> Path:
    path = (LANE / relative).resolve()
    if LANE.resolve() not in path.parents:
        raise RuntimeError(f"path escaped lane: {relative}")
    return path


def load_json(relative: str) -> dict[str, Any]:
    path = lane_path(relative)
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def identity(relative: str) -> dict[str, Any]:
    path = lane_path(relative)
    return {"path": relative, "bytes": path.stat().st_size, "sha256": base.sha(path)}


def source_entries() -> dict[str, Path]:
    entries = template.source_entries()
    additions = {
        CA02_SOURCE, CA03_SOURCE,
        "scripts/merge-cumulative-assessments-002-003.py",
        "scripts/qa-cumulative-assessments-002-003.py",
        "scripts/extend-backend-cumulative-assessments-002-003.py",
        "scripts/validate-backend-append-only-cumulative-assessments-002-003.py",
        f"scripts/build-{SLUG}.ps1",
        f"scripts/finalize-build-{SLUG}.py",
        f"scripts/package-release-{SLUG}.py",
        f"scripts/publish-zenodo-{SLUG}.py",
    }
    entries.update({relative: lane_path(relative) for relative in additions})
    return entries


def qa_inventory() -> set[str]:
    paths = set(template.qa_path_inventory())
    paths.update({
        COMBINED_QA, CA02_MATH, CA02_LANGUAGE, CA03_MATH, CA03_LANGUAGE,
        "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_FILE_MANIFEST.csv",
        "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_PLAN.json",
        "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_RECEIPT.json",
        "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_REPLAY_RECEIPT.json",
        BACKEND_CUMULATIVE, f"qa/{TOKEN}_BUILD_DRAFT.json", BUILD_RECEIPT,
        VISUAL_QA, RENDER_INVENTORY, BROWSER_QA,
    })
    return paths


def control_inventory() -> set[str]:
    prefix = RELEASE.relative_to(LANE).as_posix() + "/"
    return {prefix + name for name in CONTROL_NAMES}


def required_paths() -> set[str]:
    source = set(source_entries())
    source.discard(f"scripts/package-release-{SLUG}.py")
    return FINAL_BOUNDARY_PATHS | source | qa_inventory() | control_inventory()


def verify_assessments() -> dict[str, Any]:
    qa = load_json(COMBINED_QA)
    if not (
        qa.get("status") == "PASS"
        and qa.get("cumulative_items_added") == 16
        and qa.get("exercise_hint_solution_triples") == 16
        and qa.get("complete_checked_solutions") == 16
        and qa.get("mastery_postcondition", {}).get("total") == 108
    ):
        raise RuntimeError("CA02/CA03 combined QA closure mismatch")
    for code, source, math, language in (
        ("D60-CA02", CA02_SOURCE, CA02_MATH, CA02_LANGUAGE),
        ("D60-CA03", CA03_SOURCE, CA03_MATH, CA03_LANGUAGE),
    ):
        raw = lane_path(source).read_bytes()
        text = raw.decode("utf-8")
        if raw.count(b"\n") < 100 or text.count("::: {.exercise") != 8 or text.count("::: {.hint") != 8 or text.count("::: {.solution") != 8:
            raise RuntimeError(f"{code} reader triple census mismatch")
        source_sha = base.sha(lane_path(source))
        for review_path in (math, language):
            review = load_json(review_path)
            if not str(review.get("status", "")).startswith("PASS") or review.get("reader_sha256") != source_sha:
                raise RuntimeError(f"{code} stale/failing review: {review_path}")
    return qa


def verify_backend() -> dict[str, Any]:
    receipt = load_json(BACKEND_CUMULATIVE)
    prefix = receipt.get("immutable_prefix", {})
    final = receipt.get("cumulative", {})
    if not (
        receipt.get("status") == "PASS"
        and prefix.get("preserved_exactly") is True
        and prefix.get("records") == 7012
        and prefix.get("bytes") == 8545732
        and prefix.get("bundle_sha256") == "7d723f9ef163303c7dde63d646dc8d5917c2450b1da5d24c87ef77bf4e4d664b"
        and final.get("records") == 7273
        and final.get("bytes") == 8840132
        and final.get("bundle_sha256") == "97edc6371a0bf670ebdaaa4fab8618ec138ae25c4bf54ca9172139934ba0b464"
        and final.get("solution_bearing_slots") == 108
        and receipt.get("replay", {}).get("status") == "PASS"
    ):
        raise RuntimeError("CA02/CA03 cumulative backend boundary mismatch")
    return receipt


def verify_controls() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    for name in CONTROL_NAMES:
        path = RELEASE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        base.assert_safe_text(path)
    metadata_payload = json.loads((RELEASE / "metadata.json").read_text(encoding="utf-8"))
    metadata = metadata_payload.get("metadata", {})
    expected_contributors = [
        {"name": "Lazarovich, Nir", "type": "Other"},
        {"name": "Editor edisi Bahasa Indonesia", "type": "Editor"},
        {"name": "Translation and Transcription Project", "type": "Other"},
    ]
    if not (
        metadata.get("title") == TITLE and metadata.get("version") == VERSION
        and metadata.get("license") == "cc-by-sa-4.0"
        and metadata.get("language") == "ind" and metadata.get("access_right") == "open"
        and metadata.get("creators") == [{"name": "Roberts, David Michael"}, {"name": "Fomberg, Yeheli"}]
        and metadata.get("contributors") == expected_contributors
    ):
        raise RuntimeError("v0.31.2 metadata identity/rights/creator drift")
    prose = "\n".join(str(metadata.get(key, "")) for key in ("title", "description", "notes"))
    prose += "\n" + "\n".join(str(value) for value in metadata.get("keywords", []))
    if re.search(r"(?i)\bTTP\b|Translation and Transcription Project", prose):
        raise RuntimeError("organization marker leaked into title/prose metadata")
    controls = "\n".join((RELEASE / name).read_text(encoding="utf-8") for name in CONTROL_NAMES)
    for marker in ("108/108", "D60-CA01", "D60-CA02", "D60-CA03", "CC BY 4.0", "CC BY-SA 4.0", MODEL_NOTE):
        if marker not in controls:
            raise RuntimeError(f"release controls omit exact marker: {marker}")
    if controls.count("Translation and Transcription Project") != 1:
        raise RuntimeError("organization must occur exactly once across release controls")
    plan = json.loads((RELEASE / "publication-plan.json").read_text(encoding="utf-8"))
    if not (
        plan.get("state") == "prepared_not_published"
        and plan.get("release_id") == RELEASE_ID and plan.get("version") == VERSION
        and plan.get("existing_concept_doi") == CONCEPT_DOI
        and plan.get("current_public_record_id") == PREVIOUS_RECORD_ID
        and plan.get("current_public_doi") == PREVIOUS_DOI
        and plan.get("new_concept_allowed") is False
        and plan.get("publish_not_draft") is True
        and plan.get("anonymous_byte_readback_required") is True
        and plan.get("reader_first_filename") == PDF_NAME
    ):
        raise RuntimeError("publication plan escaped the existing lineage")
    binding = plan.get("backend_binding", {})
    if binding.get("final_identity_source") != BACKEND_CUMULATIVE or binding.get("expected_records") != 7273:
        raise RuntimeError("publication plan does not bind the CA02/CA03 backend")
    readers = plan.get("final_reader_artifacts", {})
    for role, relative in (("pdf", PDF_INPUT), ("html", HTML_INPUT)):
        row = readers.get(role, {})
        if row.get("path") != relative or not base.identity_matches(row, lane_path(relative)):
            raise RuntimeError(f"publication plan lacks exact final {role} identity")
    manifest = json.loads((RELEASE / "release-manifest.template.json").read_text(encoding="utf-8"))
    if not (
        manifest.get("release_id") == RELEASE_ID and manifest.get("version") == VERSION
        and manifest.get("status") == MANIFEST_STATUS
        and manifest.get("artifact_order") == SUBSTANTIVE_ORDER
    ):
        raise RuntimeError("release-manifest template drift")
    sums = [line.split("  ", 1)[1] for line in (RELEASE / "SHA256SUMS.template").read_text(encoding="utf-8").splitlines()]
    if sums != SUBSTANTIVE_ORDER + ["release-manifest.json"]:
        raise RuntimeError("checksum template is not exact and reader-first")
    return metadata_payload, plan, manifest


def verify_final_gates(plan: dict[str, Any]) -> dict[str, Any]:
    build = load_json(BUILD_RECEIPT)
    browser = load_json(BROWSER_QA)
    visual_text = lane_path(VISUAL_QA).read_text(encoding="utf-8")
    if not str(build.get("status", "")).startswith("PASS"):
        raise RuntimeError("final build receipt did not pass")
    pdf = build.get("pdf", {})
    html = build.get("html", {})
    if not base.identity_matches(pdf, lane_path(PDF_INPUT)) or not base.identity_matches(html, lane_path(HTML_INPUT)):
        raise RuntimeError("build receipt does not bind final readers")
    if not isinstance(pdf.get("pages"), int) or pdf["pages"] <= 482:
        raise RuntimeError("successor PDF page count is not a genuine extension")
    if plan["final_reader_artifacts"]["pdf"].get("pages") != pdf["pages"]:
        raise RuntimeError("publication plan PDF pages differ from build receipt")
    if not str(browser.get("status", "")).startswith("PASS") or "PASS" not in visual_text:
        raise RuntimeError("browser or visual QA did not pass")
    if not lane_path(RENDER_INVENTORY).is_file():
        raise FileNotFoundError(lane_path(RENDER_INVENTORY))
    return build


def qa_entries() -> dict[str, Path]:
    entries = {relative: lane_path(relative) for relative in sorted(qa_inventory())}
    entries.update({
        "release/frozen-inputs.json": FROZEN_LEDGER,
        "release/frozen-inputs.template.json": RELEASE / "frozen-inputs.template.json",
        "release/release-manifest.template.json": RELEASE / "release-manifest.template.json",
        "release/SHA256SUMS.template": RELEASE / "SHA256SUMS.template",
    })
    return entries


def seal() -> None:
    if FROZEN_LEDGER.exists():
        raise RuntimeError("frozen-inputs.json already exists; refusing to overwrite")
    _, plan, _ = verify_controls()
    verify_assessments(); verify_backend(); verify_final_gates(plan)
    rows = []
    for relative in sorted(required_paths()):
        path = lane_path(relative)
        if not path.is_file():
            raise FileNotFoundError(path)
        base.assert_safe_bytes(path.read_bytes(), relative, allow_generic_privacy_test_markers=relative.startswith("scripts/"))
        rows.append(identity(relative))
    base.write_json(FROZEN_LEDGER, {
        "schema_version": "1.0", "release_id": RELEASE_ID,
        "state": "final_inputs_sealed_local_only",
        "final_boundary_paths": sorted(FINAL_BOUNDARY_PATHS), "entries": rows,
    })
    print(json.dumps({"status": "SEALED_LEDGER_REQUIRES_APPLY_PATCH_BINDING", **base.identity(FROZEN_LEDGER), "entries": len(rows)}, indent=2))


def package() -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", FROZEN_LEDGER_SHA256):
        raise RuntimeError("FROZEN_LEDGER_SHA256 must be apply-patch-bound after sealing")
    if ARTIFACTS.exists() or STAGING.exists():
        raise RuntimeError("refusing to overwrite artifacts or stale staging")
    metadata, plan, manifest_template = verify_controls()
    verify_assessments(); backend = verify_backend(); build = verify_final_gates(plan)
    # The inherited loader resolves its expected-inventory function in the
    # proved base module. Rebind that one global to this successor's exact
    # sealed inventory before loading; all path/hash checks remain inherited.
    base.required_frozen_paths = required_paths
    frozen = base.load_frozen_inputs()
    source = source_entries(); qa = qa_entries()
    base.assert_source_archive_link_closure(source)
    for entries in (source, qa):
        for path in entries.values():
            if path.resolve() not in {SCRIPT.resolve(), FROZEN_LEDGER.resolve()}:
                relative = path.relative_to(LANE).as_posix()
                if relative not in frozen:
                    raise RuntimeError(f"unfrozen archive input: {relative}")
    STAGING.mkdir(parents=False)
    try:
        source_zip = base.deterministic_zip(STAGING / SOURCE_ZIP_NAME, source)
        qa_zip = base.deterministic_zip(STAGING / QA_ZIP_NAME, qa)
        copies = {
            PDF_NAME: lane_path(PDF_INPUT), HTML_NAME: lane_path(HTML_INPUT),
            "LICENSE.md": RELEASE / "LICENSE.md", "README_RELEASE.md": RELEASE / "README_RELEASE.md",
            "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md",
        }
        for name, path in copies.items():
            shutil.copyfile(path, STAGING / name)
        manifest = dict(manifest_template)
        manifest.pop("template_state", None); manifest.pop("generated_fields", None)
        manifest.update({
            "metadata_sha256": base.sha(RELEASE / "metadata.json"),
            "publication_plan_sha256": base.sha(RELEASE / "publication-plan.json"),
            "frozen_input_ledger": {**base.identity(FROZEN_LEDGER), "entries": len(frozen)},
            "assessments": {
                "completed": ["D60-CA01", "D60-CA02", "D60-CA03"],
                "edition_unit_ids": ["O012-ORIG-CA01", "O012-ORIG-CA02", "O012-ORIG-CA03"],
                "items": 24, "hints": 24, "complete_solutions": 24,
                "origin": "edition_original", "license": "CC BY-SA 4.0",
                "source_problem_bank_used": False,
            },
            "course_closure": {
                "ordinary_mastery_complete": True, "ordinary_mastery_items": 84,
                "cumulative_assessment_items": 24, "total_solution_bearing_items": 108,
                "total_solution_bearing_items_required": 108,
                "cumulative_assessment_mastery_complete": True,
                "computation_labs_remaining": 4, "capstone_remaining": 1,
                "composite_course_complete": False,
            },
            "backend": {
                **backend["cumulative"], "cumulative_receipt": identity(BACKEND_CUMULATIVE),
            },
            "reader_qa": {
                "status": "PASS", "pdf_pages": build["pdf"]["pages"],
                "pdf_all_fonts_embedded_subset_tounicode": True,
                "html_self_contained": True, "assessment_stable_ids_added": 68,
                "assessment_triples_added": 16,
            },
            "archives": [source_zip, qa_zip], "artifacts": [],
            "rights": {
                "integrated_payload": "CC BY-SA 4.0", "roberts_component": "CC BY 4.0",
                "fomberg_component": "CC BY-SA 4.0", "original_assessment_components": "CC BY-SA 4.0",
                "original_hint_component": "CC BY-SA 4.0", "non_endorsement_preserved": True,
            },
            "publication_lineage": {
                "existing_concept_doi": CONCEPT_DOI, "previous_record_id": PREVIOUS_RECORD_ID,
                "previous_version_doi": PREVIOUS_DOI, "new_concept_created": False,
            },
            "production_provenance": MODEL_NOTE,
            "privacy": {"credential_material": False, "absolute_local_paths": False, "user_personal_name": False},
        })
        for name in SUBSTANTIVE_ORDER:
            path = STAGING / name
            manifest["artifacts"].append({"filename": name, "bytes": path.stat().st_size, "sha256": base.sha(path)})
        base.write_json(STAGING / "release-manifest.json", manifest)
        checksum_names = SUBSTANTIVE_ORDER + ["release-manifest.json"]
        (STAGING / "SHA256SUMS").write_text("\n".join(f"{base.sha(STAGING / name)}  {name}" for name in checksum_names) + "\n", encoding="utf-8", newline="\n")
        if sorted(path.name for path in STAGING.iterdir()) != sorted(FILE_NAMES):
            raise RuntimeError("staged payload inventory mismatch")
        STAGING.replace(ARTIFACTS)
    except Exception:
        if STAGING.exists(): shutil.rmtree(STAGING)
        raise
    files = [{"filename": p.name, "bytes": p.stat().st_size, "sha256": base.sha(p)} for p in sorted(ARTIFACTS.iterdir())]
    base.write_json(PACKAGE_RECEIPT, {
        "schema_version": "1.0", "status": "PASS_PREPARED_NOT_PUBLISHED",
        "release_id": RELEASE_ID, "version": VERSION, "reader_first_filename": PDF_NAME,
        "scope": "Roberts 30/30; Fomberg 1.1–1.13; ordinary mastery 84/84; cumulative assessments 24/24; solution-bearing mastery 108/108; labs and capstone pending",
        "frozen_input_ledger": base.identity(FROZEN_LEDGER), "files": files,
        "file_count": len(files), "total_payload_bytes": sum(row["bytes"] for row in files),
        "archives": [source_zip, qa_zip],
        "verification": {"reader_first": True, "zip_crc_and_inventory_pass": True, "final_build_visual_browser_gates": True, "assessment_independent_reviews": True, "backend_exact_replay": True, "rights_component_scope_consistent": True, "network_actions": 0, "credentials_used": False, "published": False},
    })
    print(json.dumps({"status": "PASS_PREPARED_NOT_PUBLISHED", "release_id": RELEASE_ID, "files": files}, ensure_ascii=False, indent=2))


def plan() -> None:
    print(json.dumps({
        "status": "PREPARED_SCRIPT_NOT_EXECUTED", "release_id": RELEASE_ID,
        "version": VERSION, "concept_doi": CONCEPT_DOI,
        "previous_record_id": PREVIOUS_RECORD_ID, "reader_first_filename": PDF_NAME,
        "release_directory": RELEASE.relative_to(LANE).as_posix(),
        "final_boundary_paths": sorted(FINAL_BOUNDARY_PATHS),
        "post_build_bindings_required": [
            "final build receipt and exact PDF/HTML identities/pages",
            "visual, render-inventory, and browser QA receipts",
            "v0.31.2 release controls and checksum template",
            "sealed frozen-input ledger SHA-256 apply-patch binding",
        ],
    }, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--list-required-inputs", action="store_true")
    parser.add_argument("--seal-frozen-inputs", action="store_true")
    args = parser.parse_args()
    if args.plan: plan()
    elif args.list_required_inputs: print("\n".join(sorted(required_paths())))
    elif args.seal_frozen_inputs: seal()
    else: package()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise
