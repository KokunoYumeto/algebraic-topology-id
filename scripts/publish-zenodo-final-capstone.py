#!/usr/bin/env python3
"""Publish final D60 v0.31.7 in its existing Zenodo concept and verify twice."""
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
    "publish-zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01-lab02-lab03-lab04.py"
)
TEMPLATE_ID = (
    16_996,
    "5221bb03871a2a50b916b2cec2bc35e9a296ccf1dfe52947706d1d628e7d4ff6",
)
template_raw = TEMPLATE_PATH.read_bytes()
if (len(template_raw), hashlib.sha256(template_raw).hexdigest()) != TEMPLATE_ID:
    raise RuntimeError("frozen Lab 4 publisher identity drift")
spec = importlib.util.spec_from_file_location("o012_v0316_publisher_template", TEMPLATE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load the proved v0.31.6 publisher")
template = importlib.util.module_from_spec(spec)
spec.loader.exec_module(template)
engine = template.engine
base = template.base

SLUG = (
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-"
    "lab01-lab02-lab03-lab04-capstone"
)
TOKEN = (
    "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_"
    "LAB01_LAB02_LAB03_LAB04_CAPSTONE"
)
TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30, "
    "Jembatan Homologi §1.1–1.13, Penguasaan 108/108, "
    "Laboratorium 1–4, dan Capstone D60"
)
VERSION = "0.31.7"
RELEASE_ID = f"o012-composite-id-{SLUG}-v{VERSION}"
PREVIOUS_RECORD_ID = 22_161_294
PREVIOUS_DOI = "10.5281/zenodo.22161294"
CONCEPT_DOI = "10.5281/zenodo.22061489"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"

base.RELEASE = base.LANE / "release" / f"zenodo-{SLUG}"
base.ARTIFACTS = base.RELEASE / "artifacts"
base.METADATA = base.RELEASE / "metadata.json"
base.MANIFEST = base.ARTIFACTS / "release-manifest.json"
base.TRANSACTION = base.RELEASE / "transaction.json"
base.RECEIPT = base.RELEASE / "publication-receipt.json"
base.SEED_RECORD = PREVIOUS_RECORD_ID
base.CONCEPT_DOI = CONCEPT_DOI
base.MODEL_NOTE = MODEL_NOTE
engine.PREVIOUS_RECORD_ID = PREVIOUS_RECORD_ID
engine.PREVIOUS_DOI = PREVIOUS_DOI
base.RELEASE_ID = RELEASE_ID
base.TITLE = TITLE
base.VERSION = VERSION

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
FINAL_BACKEND_RECEIPT = "qa/BACKEND_CAPSTONE_FINAL_REV3_CUMULATIVE_RECEIPT.json"
MANIFEST_STATUS = (
    "roberts_complete_fomberg_001_007_complete_mastery_108_complete_"
    "laboratories_001_004_complete_proof_graph_complete_capstone_complete_"
    "composite_course_complete"
)
FINAL_BACKEND = (
    8_338,
    10_040_043,
    "8a3ffc9618e56dfce048c41e938aabef4ffbfd3db20a03a4f52f218985230dbb",
)
READBACK_PASSES = 2
ORGANIZATION_NAME = "Translation and " + "Transcription Project"
ORGANIZATION_ABBREVIATION = "".join(("T", "T", "P"))
ORGANIZATION_PATTERN = re.compile(
    rf"(?i)\b{re.escape(ORGANIZATION_ABBREVIATION)}\b|{re.escape(ORGANIZATION_NAME)}"
)
EXPECTED_CREATORS = [
    {"name": "Roberts, David Michael"},
    {"name": "Fomberg, Yeheli"},
]
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
        metadata.get("title") == TITLE
        and metadata.get("version") == VERSION
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
    prose = "\n".join(
        str(metadata.get(key, "")) for key in ("title", "description", "notes")
    )
    prose += "\n" + "\n".join(str(value) for value in metadata.get("keywords", []))
    if ORGANIZATION_PATTERN.search(prose):
        raise RuntimeError("organization marker leaked outside contributor metadata")
    joined = json.dumps(metadata, ensure_ascii=False)
    if joined.count(ORGANIZATION_NAME) != 1:
        raise RuntimeError("organization contributor must occur exactly once")
    for marker in (
        "108/108",
        "D60-LAB01",
        "D60-LAB04",
        "capstone D60",
        MODEL_NOTE,
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
        and plan.get("reader_first_filename") == base.PDF_NAME
    ):
        raise RuntimeError("publication plan escaped the v0.31.6 predecessor")
    binding = plan.get("backend_binding", {})
    snapshot = binding.get("verified_snapshot", {})
    if not (
        binding.get("final_identity_source") == FINAL_BACKEND_RECEIPT
        and binding.get("expected_records") == FINAL_BACKEND[0]
        and (
            snapshot.get("total_records"),
            snapshot.get("total_bytes"),
            snapshot.get("bundle_sha256"),
        )
        == FINAL_BACKEND
    ):
        raise RuntimeError("publication plan backend binding drift")

    manifest = load(base.MANIFEST)
    closure = manifest.get("course_closure", {})
    backend = manifest.get("backend", {})
    if not (
        manifest.get("release_id") == RELEASE_ID
        and manifest.get("title") == TITLE
        and manifest.get("version") == VERSION
        and manifest.get("status") == MANIFEST_STATUS
        and manifest.get("artifact_order") == base.FILE_NAMES[:7]
        and manifest.get("production_provenance") == MODEL_NOTE
        and closure.get("ordinary_mastery_items") == 84
        and closure.get("cumulative_assessment_items") == 24
        and closure.get("total_solution_bearing_items")
        == closure.get("total_solution_bearing_items_required")
        == 108
        and closure.get("computation_laboratories_complete")
        == closure.get("computation_laboratories_required")
        == 4
        and closure.get("proof_repair_graphs_closed") == 4
        and closure.get("capstone_complete") is True
        and closure.get("composite_course_complete") is True
        and (backend.get("records"), backend.get("bytes"), backend.get("bundle_sha256"))
        == FINAL_BACKEND
    ):
        raise RuntimeError("manifest final course/backend closure drift")
    lineage = manifest.get("publication_lineage", {})
    if not (
        lineage.get("existing_concept_doi") == CONCEPT_DOI
        and lineage.get("previous_record_id") == PREVIOUS_RECORD_ID
        and lineage.get("previous_version_doi") == PREVIOUS_DOI
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
        and receipt.get("release_id") == RELEASE_ID
        and receipt.get("reader_first_filename") == base.PDF_NAME
        and receipt.get("file_count") == 9
        and {row.get("filename") for row in receipt.get("files", [])}
        == set(base.FILE_NAMES)
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
    expected_sums = {
        path.name: digest(path) for path in files if path.name != "SHA256SUMS"
    }
    if sums != expected_sums:
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
        "release_id": RELEASE_ID,
        "title": TITLE,
        "version": VERSION,
        "license": "cc-by-sa-4.0",
        "scope": (
            "Roberts 30/30; Fomberg 1.1-1.13; ordinary mastery 84/84; "
            "cumulative assessments 24/24; solution-bearing mastery 108/108; "
            "Labs 1-4; four proof-repair graphs; D60 capstone; composite course complete"
        ),
        "record_id": int(public["id"]),
        "doi": public.get("doi"),
        "concept_doi": public.get("conceptdoi"),
        "previous_record_id": PREVIOUS_RECORD_ID,
        "previous_doi": PREVIOUS_DOI,
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
            f"{MODEL_NOTE}; source authors and human direction remain credited."
        ),
        "non_endorsement": (
            "Independent Indonesian edition; no source-author or institutional endorsement is implied."
        ),
    }
    public_text_is_safe(json.dumps(receipt, ensure_ascii=False))
    return receipt


# Propagate final-release assertions through every proved inherited verifier layer.
public_verifier = template.template.template.template.template
for verifier_layer in (
    template,
    template.template,
    template.template.template,
    template.template.template.template,
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
                    "release_id": RELEASE_ID,
                    "version": VERSION,
                    "existing_concept_doi": CONCEPT_DOI,
                    "previous_record_id": PREVIOUS_RECORD_ID,
                    "previous_doi": PREVIOUS_DOI,
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
