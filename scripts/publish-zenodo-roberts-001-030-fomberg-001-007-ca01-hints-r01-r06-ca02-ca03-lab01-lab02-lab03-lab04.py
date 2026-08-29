#!/usr/bin/env python3
"""Publish v0.31.6 in the existing Zenodo concept and verify every byte twice.

With no arguments this uses the proved transaction engine: it reads the token
only at runtime, creates one new version from public record 22151513, uploads
the exact reader-first nine-file package, publishes rather than leaving a
draft, and performs two credential-free public readbacks. ``--plan`` is
strictly read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any


SCRIPT = Path(__file__).resolve()
TEMPLATE_PATH = SCRIPT.with_name(
    "publish-zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03.py"
)
TEMPLATE_ID = (
    17_372,
    "8d12adc91a6a84682683daaac028bcbc3079981aacc0934ff2dddcafa3a8f3ed",
)
template_raw = TEMPLATE_PATH.read_bytes()
if (len(template_raw), hashlib.sha256(template_raw).hexdigest()) != TEMPLATE_ID:
    raise RuntimeError("frozen Lab 3 publisher identity drift")
SPEC = importlib.util.spec_from_file_location("o012_v0315_publisher_template", TEMPLATE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the proved v0.31.5 publisher")
template = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(template)
engine = template.engine
base = template.base

SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04"
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04"
base.RELEASE = base.LANE / "release" / f"zenodo-{SLUG}"
base.ARTIFACTS = base.RELEASE / "artifacts"
base.METADATA = base.RELEASE / "metadata.json"
base.MANIFEST = base.ARTIFACTS / "release-manifest.json"
base.TRANSACTION = base.RELEASE / "transaction.json"
base.RECEIPT = base.RELEASE / "publication-receipt.json"
base.SEED_RECORD = 22_151_513
base.CONCEPT_DOI = "10.5281/zenodo.22061489"
base.MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"
engine.PREVIOUS_RECORD_ID = 22_151_513
engine.PREVIOUS_DOI = "10.5281/zenodo.22151513"
base.RELEASE_ID = f"o012-composite-id-{SLUG}-v0.31.6"
base.TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30, "
    "Jembatan Homologi §1.1–1.13, Asesmen Kumulatif 1–3, "
    "Petunjuk Rute 1–6, dan Laboratorium Komputasi 1–4"
)
base.VERSION = "0.31.6"
base.PDF_NAME = f"00_TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.pdf"
base.FILE_NAMES = [
    base.PDF_NAME,
    f"TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.html",
    f"TOPOLOGI_ALJABAR_ID_{TOKEN}_EDITABLE_SOURCE_BACKEND.zip",
    f"TOPOLOGI_ALJABAR_ID_{TOKEN}_QA_PROVENANCE.zip",
    "LICENSE.md",
    "README_RELEASE.md",
    "RELEASE_RIGHTS.md",
    "release-manifest.json",
    "SHA256SUMS",
]

PACKAGE_RECEIPT = base.RELEASE / "PACKAGE_PREPARATION_RECEIPT.json"
PUBLICATION_PLAN = base.RELEASE / "publication-plan.json"
FINAL_BACKEND_RECEIPT = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_CUMULATIVE_RECEIPT.json"
MANIFEST_STATUS = (
    "roberts_complete_fomberg_units_001_007_complete_ca01_ca02_ca03_complete_"
    "ordinary_mastery_84_complete_solution_bearing_mastery_108_complete_"
    "computation_labs_001_002_003_004_complete_composite_course_partial"
)
READBACK_PASSES = 2
ORGANIZATION_NAME = "Translation and " + "Transcription Project"
ORGANIZATION_ABBREVIATION = "".join(("T", "T", "P"))
ORGANIZATION_PATTERN = re.compile(
    rf"(?i)\b{re.escape(ORGANIZATION_ABBREVIATION)}\b|{re.escape(ORGANIZATION_NAME)}"
)
EXPECTED_CREATORS = [{"name": "Roberts, David Michael"}, {"name": "Fomberg, Yeheli"}]
EXPECTED_CONTRIBUTORS = [
    {"name": "Lazarovich, Nir", "type": "Other"},
    {"name": "Editor edisi Bahasa Indonesia", "type": "Editor"},
    {"name": ORGANIZATION_NAME, "type": "Other"},
]


def digest(path: Path, algorithm: str = "sha256") -> str:
    result = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def public_text_is_safe(text: str) -> None:
    template.public_text_is_safe(text)


def verify_zip(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None or not archive.infolist():
            raise RuntimeError(f"ZIP CRC/inventory failed: {path.name}")
        names = [row.filename for row in archive.infolist()]
        if len(names) != len(set(names)) or any(
            name.startswith(("/", "\\")) or ".." in Path(name).parts for name in names
        ):
            raise RuntimeError(f"unsafe ZIP inventory: {path.name}")


def assert_metadata(metadata: dict[str, Any], *, exact_people: bool = True) -> None:
    license_id = metadata.get("license")
    if isinstance(license_id, dict):
        license_id = license_id.get("id")
    if not (
        metadata.get("title") == base.TITLE
        and metadata.get("version") == base.VERSION
        and license_id == "cc-by-sa-4.0"
        and metadata.get("language") == "ind"
        and metadata.get("access_right") == "open"
    ):
        raise RuntimeError("metadata identity/rights drift")
    if exact_people and (
        metadata.get("creators") != EXPECTED_CREATORS
        or metadata.get("contributors") != EXPECTED_CONTRIBUTORS
    ):
        raise RuntimeError("local metadata creator/contributor drift")
    prose = "\n".join(str(metadata.get(key, "")) for key in ("title", "description", "notes"))
    prose += "\n" + "\n".join(str(value) for value in metadata.get("keywords", []))
    if ORGANIZATION_PATTERN.search(prose):
        raise RuntimeError("organization marker leaked outside the single contributor entry")
    joined = json.dumps(metadata, ensure_ascii=False)
    if joined.count(ORGANIZATION_NAME) != 1:
        raise RuntimeError("organization contributor must occur exactly once")
    for marker in (
        "108/108",
        "D60-LAB01",
        "D60-LAB02",
        "D60-LAB03",
        "D60-LAB04",
        "Laboratorium Komputasi 1–4",
        base.MODEL_NOTE,
    ):
        if marker not in joined:
            raise RuntimeError(f"metadata omits exact scope marker: {marker}")
    public_text_is_safe(joined)


def verify_local() -> tuple[dict, dict]:
    metadata_payload = load(base.METADATA)
    metadata = metadata_payload.get("metadata", {})
    assert_metadata(metadata)
    plan = load(PUBLICATION_PLAN)
    if not (
        plan.get("state") == "prepared_not_published"
        and plan.get("release_id") == base.RELEASE_ID
        and plan.get("version") == base.VERSION
        and plan.get("existing_concept_doi") == base.CONCEPT_DOI
        and plan.get("current_public_record_id") == engine.PREVIOUS_RECORD_ID
        and plan.get("current_public_doi") == engine.PREVIOUS_DOI
        and plan.get("new_concept_allowed") is False
        and plan.get("new_deposition_created") is False
        and plan.get("credentials_used") is False
        and plan.get("publish_not_draft") is True
        and plan.get("anonymous_byte_readback_required") is True
        and plan.get("reader_first_filename") == base.PDF_NAME
    ):
        raise RuntimeError("publication plan escaped the exact v0.31.5 predecessor")
    binding = plan.get("backend_binding", {})
    snapshot = binding.get("verified_snapshot", {})
    if not (
        binding.get("final_identity_source") == FINAL_BACKEND_RECEIPT
        and binding.get("expected_records") == 7_847
        and snapshot.get("total_records") == 7_847
        and snapshot.get("total_bytes") == 9_443_250
        and snapshot.get("bundle_sha256")
        == "2633732fd2fd2b5fb8afb5888b1864b6bcda9dca52eb85a6636c777ac1018c1f"
    ):
        raise RuntimeError("publication plan backend binding drift")

    manifest = load(base.MANIFEST)
    if not (
        manifest.get("release_id") == base.RELEASE_ID
        and manifest.get("title") == base.TITLE
        and manifest.get("version") == base.VERSION
        and manifest.get("status") == MANIFEST_STATUS
        and manifest.get("artifact_order") == base.FILE_NAMES[:7]
        and manifest.get("production_provenance") == base.MODEL_NOTE
    ):
        raise RuntimeError("release manifest identity/scope drift")
    assessments = manifest.get("assessments", {})
    labs = manifest.get("laboratories", {})
    closure = manifest.get("course_closure", {})
    backend = manifest.get("backend", {})
    if not (
        assessments.get("completed") == ["D60-CA01", "D60-CA02", "D60-CA03"]
        and assessments.get("items")
        == assessments.get("hints")
        == assessments.get("complete_solutions")
        == 24
        and labs.get("completed") == ["D60-LAB01", "D60-LAB02", "D60-LAB03", "D60-LAB04"]
        and labs.get("edition_unit_ids")
        == ["O012-ORIG-LAB01", "O012-ORIG-LAB02", "O012-ORIG-LAB03", "O012-ORIG-LAB04"]
        and labs.get("required") == 4
        and labs.get("completed_count") == 4
        and labs.get("remaining") == []
        and labs.get("tasks") == 24
        and labs.get("tests") == 24
        and labs.get("stable_ids") == 99
        and labs.get("offline_reproducible") is True
        and labs.get("license") == "CC BY-SA 4.0"
        and closure.get("ordinary_mastery_items") == 84
        and closure.get("total_solution_bearing_items")
        == closure.get("total_solution_bearing_items_required")
        == 108
        and closure.get("computation_laboratories_complete") == 4
        and closure.get("computation_laboratories_required") == 4
        and closure.get("computation_labs_remaining") == 0
        and closure.get("proof_metadata_closure_pending") is True
        and closure.get("capstone_remaining") == 1
        and closure.get("composite_course_complete") is False
        and backend.get("records") == 7_847
        and backend.get("bytes") == 9_443_250
        and backend.get("bundle_sha256")
        == "2633732fd2fd2b5fb8afb5888b1864b6bcda9dca52eb85a6636c777ac1018c1f"
    ):
        raise RuntimeError("manifest mastery/laboratory/backend closure drift")
    lineage = manifest.get("publication_lineage", {})
    if not (
        lineage.get("existing_concept_doi") == base.CONCEPT_DOI
        and lineage.get("previous_record_id") == engine.PREVIOUS_RECORD_ID
        and lineage.get("previous_version_doi") == engine.PREVIOUS_DOI
        and lineage.get("new_concept_created") is False
    ):
        raise RuntimeError("manifest escaped the existing concept lineage")

    receipt = load(PACKAGE_RECEIPT)
    files = base.local_files()
    rows = [
        {
            "filename": path.name,
            "bytes": path.stat().st_size,
            "sha256": digest(path),
            "md5": digest(path, "md5"),
        }
        for path in files
    ]
    if [path.name for path in files] != base.FILE_NAMES or files[0].name != base.PDF_NAME:
        raise RuntimeError("local payload inventory/order is not exact and reader-first")
    local_by_name = {row["filename"]: row for row in rows}
    if not (
        receipt.get("status") == "PASS_PREPARED_NOT_PUBLISHED"
        and receipt.get("release_id") == base.RELEASE_ID
        and receipt.get("reader_first_filename") == base.PDF_NAME
        and receipt.get("file_count") == 9
        and {row.get("filename") for row in receipt.get("files", [])} == set(base.FILE_NAMES)
    ):
        raise RuntimeError("package receipt inventory drift")
    for row in receipt["files"]:
        local = local_by_name[row["filename"]]
        if (row.get("bytes"), row.get("sha256")) != (local["bytes"], local["sha256"]):
            raise RuntimeError(f"package receipt byte mismatch: {row['filename']}")
    sums = {}
    for line in (base.ARTIFACTS / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        checksum, name = line.split("  ", 1)
        sums[name] = checksum
    if sums != {path.name: digest(path) for path in files if path.name != "SHA256SUMS"}:
        raise RuntimeError("SHA256SUMS mismatch")
    for name in base.FILE_NAMES[2:4]:
        verify_zip(base.ARTIFACTS / name)
    return metadata_payload, {
        "files": rows,
        "metadata_sha256": digest(base.METADATA),
        "manifest_sha256": digest(base.MANIFEST),
        "package_receipt_sha256": digest(PACKAGE_RECEIPT),
        "upload_order": list(base.FILE_NAMES),
    }


def make_receipt(public: dict, rows: list[dict], metadata_payload: dict, local: dict) -> dict:
    receipt = {
        "schema_version": "1.0",
        "status": "PUBLISHED_AND_TWICE_ANONYMOUSLY_VERIFIED",
        "release_id": base.RELEASE_ID,
        "title": base.TITLE,
        "version": base.VERSION,
        "license": "cc-by-sa-4.0",
        "scope": (
            "Roberts 30/30; Fomberg 1.1-1.13; ordinary mastery 84/84; "
            "assessments D60-CA01/02/03 24/24; solution-bearing mastery 108/108; "
            "computation Labs 1-4 complete; proof-metadata closure and capstone pending"
        ),
        "record_id": int(public["id"]),
        "doi": public.get("doi"),
        "concept_doi": public.get("conceptdoi"),
        "previous_record_id": engine.PREVIOUS_RECORD_ID,
        "previous_doi": engine.PREVIOUS_DOI,
        "public_record_url": f"https://zenodo.org/records/{int(public['id'])}",
        "metadata_sha256": local["metadata_sha256"],
        "manifest_sha256": local["manifest_sha256"],
        "package_receipt_sha256": local["package_receipt_sha256"],
        "upload_order": local["upload_order"],
        "files": rows,
        "verification": {
            "exact_public_inventory": True,
            "reader_first_by_filename": True,
            "pdf_uploaded_first": True,
            "anonymous_byte_readback": True,
            "anonymous_readback_passes": 2,
            "all_nine_files_read_twice": True,
            "all_sha256_match_local_on_both_passes": True,
            "existing_concept_reused": True,
            "published_not_draft": True,
            "credentials_recorded": False,
            "authorization_header_recorded": False,
            "bucket_url_recorded": False,
            "absolute_local_paths_recorded": False,
            "user_personal_name_recorded": False,
        },
        "provenance": (
            "Published by Codex at the user's direction; production note: "
            f"{base.MODEL_NOTE}; source authors and human direction remain credited."
        ),
        "non_endorsement": (
            "Independent Indonesian edition; no source-author or institutional endorsement is implied."
        ),
    }
    public_text_is_safe(json.dumps(receipt, ensure_ascii=False))
    return receipt


# Lab 4 adds one inheritance layer beyond the Lab 3 publisher. Propagate all
# release-specific assertions through the deepest proved public verifier.
public_verifier = template.template.template.template
for verifier_layer in (
    template,
    template.template,
    template.template.template,
    public_verifier,
):
    verifier_layer.PACKAGE_RECEIPT = PACKAGE_RECEIPT
    verifier_layer.PUBLICATION_PLAN = PUBLICATION_PLAN
    verifier_layer.FINAL_BACKEND_RECEIPT = FINAL_BACKEND_RECEIPT
    verifier_layer.MANIFEST_STATUS = MANIFEST_STATUS
    verifier_layer.READBACK_PASSES = READBACK_PASSES
    verifier_layer.EXPECTED_CREATORS = EXPECTED_CREATORS
    verifier_layer.EXPECTED_CONTRIBUTORS = EXPECTED_CONTRIBUTORS
    verifier_layer.assert_metadata = assert_metadata
    verifier_layer.verify_local = verify_local
    verifier_layer.make_receipt = make_receipt
engine.verify_local = verify_local
engine.verify_public = public_verifier.verify_public
engine.make_receipt = make_receipt
base.verify_local = verify_local
base.verify_public = public_verifier.verify_public
base.make_receipt = make_receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", action="store_true")
    args = parser.parse_args()
    if args.plan:
        print(
            json.dumps(
                {
                    "status": "PREPARED_SCRIPT_NOT_EXECUTED",
                    "release_id": base.RELEASE_ID,
                    "version": base.VERSION,
                    "existing_concept_doi": base.CONCEPT_DOI,
                    "previous_record_id": engine.PREVIOUS_RECORD_ID,
                    "previous_doi": engine.PREVIOUS_DOI,
                    "reader_first_filename": base.PDF_NAME,
                    "publish_not_draft": True,
                    "anonymous_readback_passes": 2,
                    "token": "runtime_only_not_logged",
                },
                indent=2,
            )
        )
        return
    engine.publish_main()
    public_verifier.finalize_transaction()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise
