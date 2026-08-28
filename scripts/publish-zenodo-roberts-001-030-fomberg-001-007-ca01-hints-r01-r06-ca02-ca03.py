#!/usr/bin/env python3
"""Publish v0.31.2 in the existing Zenodo concept and verify every byte twice.

With no arguments this uses the proved transaction engine: it reads the token
only at runtime, creates one new version from public record 22106133, uploads
the exact reader-first package, publishes (never merely drafts), and performs
two credential-free public readbacks.  `--plan` is strictly read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import time
import zipfile
from pathlib import Path
from typing import Any


SCRIPT = Path(__file__).resolve()
TEMPLATE_PATH = SCRIPT.with_name(
    "publish-zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.py"
)
SPEC = importlib.util.spec_from_file_location("o012_v0311_publisher_template", TEMPLATE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the proved v0.31.1 publisher")
template = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(template)
engine = template.engine
base = template.base

SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03"
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03"
base.RELEASE = base.LANE / "release" / f"zenodo-{SLUG}"
base.ARTIFACTS = base.RELEASE / "artifacts"
base.METADATA = base.RELEASE / "metadata.json"
base.MANIFEST = base.ARTIFACTS / "release-manifest.json"
base.TRANSACTION = base.RELEASE / "transaction.json"
base.RECEIPT = base.RELEASE / "publication-receipt.json"
base.SEED_RECORD = 22106133
base.CONCEPT_DOI = "10.5281/zenodo.22061489"
base.MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"
engine.PREVIOUS_RECORD_ID = 22106133
engine.PREVIOUS_DOI = "10.5281/zenodo.22106133"
base.RELEASE_ID = f"o012-composite-id-{SLUG}-v0.31.2"
base.TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30, "
    "Jembatan Homologi §1.1–1.13, Asesmen Kumulatif 1–3, dan Petunjuk Rute 1–6"
)
base.VERSION = "0.31.2"
base.PDF_NAME = f"00_TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.pdf"
base.FILE_NAMES = [
    base.PDF_NAME,
    f"TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.html",
    f"TOPOLOGI_ALJABAR_ID_{TOKEN}_EDITABLE_SOURCE_BACKEND.zip",
    f"TOPOLOGI_ALJABAR_ID_{TOKEN}_QA_PROVENANCE.zip",
    "LICENSE.md", "README_RELEASE.md", "RELEASE_RIGHTS.md",
    "release-manifest.json", "SHA256SUMS",
]

PACKAGE_RECEIPT = base.RELEASE / "PACKAGE_PREPARATION_RECEIPT.json"
PUBLICATION_PLAN = base.RELEASE / "publication-plan.json"
FINAL_BACKEND_RECEIPT = "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_CUMULATIVE_RECEIPT.json"
MANIFEST_STATUS = (
    "roberts_complete_fomberg_units_001_007_complete_ca01_ca02_ca03_complete_"
    "ordinary_mastery_84_complete_solution_bearing_mastery_108_complete_composite_course_partial"
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


def normalized_people(rows: list[dict], contributor: bool) -> list[tuple]:
    return template.normalized_people(rows, contributor=contributor)


def normalized_related(rows: list[dict]) -> set[tuple]:
    return template.normalized_related(rows)


def verify_zip(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None or not archive.infolist():
            raise RuntimeError(f"ZIP CRC/inventory failed: {path.name}")
        names = [row.filename for row in archive.infolist()]
        if len(names) != len(set(names)) or any(name.startswith(("/", "\\")) or ".." in Path(name).parts for name in names):
            raise RuntimeError(f"unsafe ZIP inventory: {path.name}")


def assert_metadata(metadata: dict[str, Any], *, exact_people: bool = True) -> None:
    license_id = metadata.get("license")
    if isinstance(license_id, dict):
        license_id = license_id.get("id")
    if not (
        metadata.get("title") == base.TITLE and metadata.get("version") == base.VERSION
        and license_id == "cc-by-sa-4.0"
        and metadata.get("language") == "ind" and metadata.get("access_right") == "open"
    ):
        raise RuntimeError("metadata identity/rights/people drift")
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
    for marker in ("108/108", "D60-CA01", "D60-CA02", "D60-CA03", "empat laboratorium", "capstone", base.MODEL_NOTE):
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
        raise RuntimeError("publication plan escaped the exact v0.31.1 predecessor")
    binding = plan.get("backend_binding", {})
    snapshot = binding.get("verified_snapshot", {})
    if not (
        binding.get("final_identity_source") == FINAL_BACKEND_RECEIPT
        and binding.get("expected_records") == 7273
        and snapshot.get("total_records") == 7273
        and snapshot.get("total_bytes") == 8840132
        and snapshot.get("bundle_sha256") == "97edc6371a0bf670ebdaaa4fab8618ec138ae25c4bf54ca9172139934ba0b464"
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
    closure = manifest.get("course_closure", {})
    backend = manifest.get("backend", {})
    if not (
        assessments.get("completed") == ["D60-CA01", "D60-CA02", "D60-CA03"]
        and assessments.get("items") == assessments.get("hints") == assessments.get("complete_solutions") == 24
        and assessments.get("license") == "CC BY-SA 4.0"
        and closure.get("ordinary_mastery_items") == 84
        and closure.get("total_solution_bearing_items") == closure.get("total_solution_bearing_items_required") == 108
        and closure.get("cumulative_assessment_mastery_complete") is True
        and closure.get("computation_labs_remaining") == 4
        and closure.get("capstone_remaining") == 1
        and closure.get("composite_course_complete") is False
        and backend.get("records") == 7273 and backend.get("bytes") == 8840132
        and backend.get("bundle_sha256") == "97edc6371a0bf670ebdaaa4fab8618ec138ae25c4bf54ca9172139934ba0b464"
    ):
        raise RuntimeError("manifest assessment/mastery/backend closure drift")
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
    rows = [{"filename": p.name, "bytes": p.stat().st_size, "sha256": digest(p), "md5": digest(p, "md5")} for p in files]
    if [p.name for p in files] != base.FILE_NAMES or files[0].name != base.PDF_NAME:
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
        checksum, name = line.split("  ", 1); sums[name] = checksum
    if sums != {p.name: digest(p) for p in files if p.name != "SHA256SUMS"}:
        raise RuntimeError("SHA256SUMS mismatch")
    for name in base.FILE_NAMES[2:4]:
        verify_zip(base.ARTIFACTS / name)
    return metadata_payload, {
        "files": rows, "metadata_sha256": digest(base.METADATA),
        "manifest_sha256": digest(base.MANIFEST),
        "package_receipt_sha256": digest(PACKAGE_RECEIPT),
        "upload_order": list(base.FILE_NAMES),
    }


def fetch_record(record_id: int, pass_index: int) -> dict[str, Any]:
    for _ in range(40):
        response = base.requests.get(
            f"{base.API}/records/{record_id}", timeout=180,
            headers={"Accept": "application/json", "Cache-Control": "no-cache", "User-Agent": f"Codex-anonymous-readback-pass-{pass_index}"},
        )
        if response.status_code == 200:
            return response.json()
        time.sleep(2)
    raise RuntimeError(f"published record unavailable anonymously on pass {pass_index}")


def verify_public_metadata(public: dict[str, Any], metadata_payload: dict[str, Any]) -> None:
    if not base.concept_matches(public):
        raise RuntimeError("published record escaped the existing concept")
    actual = public.get("metadata", {}); expected = metadata_payload["metadata"]
    license_id = actual.get("license")
    if isinstance(license_id, dict): license_id = license_id.get("id")
    resource_type = actual.get("resource_type", {})
    if not (
        actual.get("title") == expected["title"] and actual.get("version") == expected["version"]
        and license_id == expected["license"] and actual.get("language") == expected["language"]
        and actual.get("access_right") == "open"
        and resource_type.get("type") == expected["upload_type"]
        and resource_type.get("subtype") == expected["publication_type"]
        and actual.get("description") == expected.get("description")
        and actual.get("notes") == expected.get("notes")
        and actual.get("keywords", []) == expected.get("keywords", [])
        and normalized_people(actual.get("creators", []), False) == normalized_people(expected.get("creators", []), False)
        and normalized_people(actual.get("contributors", []), True) == normalized_people(expected.get("contributors", []), True)
        and normalized_related(actual.get("related_identifiers", [])) == normalized_related(expected.get("related_identifiers", []))
    ):
        raise RuntimeError("public metadata drift")
    assert_metadata(actual, exact_people=False)


def verify_public(record_id: int, metadata_payload: dict, local: dict) -> tuple[dict, list[dict]]:
    local_by_name = {row["filename"]: row for row in local["files"]}
    history = {name: [] for name in base.FILE_NAMES}; first = None
    for pass_index in range(1, READBACK_PASSES + 1):
        public = fetch_record(record_id, pass_index)
        verify_public_metadata(public, metadata_payload)
        remote = {(row.get("key") or row.get("filename")): row for row in public.get("files", [])}
        if set(remote) != set(base.FILE_NAMES) or len(remote) != 9:
            raise RuntimeError(f"public inventory mismatch on pass {pass_index}")
        for name in base.FILE_NAMES:
            url = remote[name]["links"]["self"]
            response = base.requests.get(url, timeout=180, headers={"Cache-Control": "no-cache", "User-Agent": f"Codex-anonymous-byte-readback-pass-{pass_index}"})
            data = response.content; sha = hashlib.sha256(data).hexdigest(); local_row = local_by_name[name]
            if response.status_code != 200 or len(data) != local_row["bytes"] or sha != local_row["sha256"]:
                raise RuntimeError(f"anonymous byte mismatch pass {pass_index}: {name}")
            history[name].append({"pass": pass_index, "status": 200, "bytes": len(data), "sha256": sha, "url": url})
        if first is None: first = public
        elif (public.get("doi"), public.get("conceptdoi")) != (first.get("doi"), first.get("conceptdoi")):
            raise RuntimeError("DOI identity changed between readback passes")
    if first is None:
        raise RuntimeError("no public record read back")
    rows = [{"filename": name, "bytes": history[name][-1]["bytes"], "sha256": history[name][-1]["sha256"], "url": history[name][-1]["url"], "anonymous_readbacks": history[name]} for name in base.FILE_NAMES]
    return first, rows


def make_receipt(public: dict, rows: list[dict], metadata_payload: dict, local: dict) -> dict:
    receipt = {
        "schema_version": "1.0", "status": "PUBLISHED_AND_TWICE_ANONYMOUSLY_VERIFIED",
        "release_id": base.RELEASE_ID, "title": base.TITLE, "version": base.VERSION,
        "license": "cc-by-sa-4.0",
        "scope": "Roberts 30/30; Fomberg 1.1-1.13; ordinary mastery 84/84; assessments D60-CA01/02/03 24/24; solution-bearing mastery 108/108; four labs and capstone pending",
        "record_id": int(public["id"]), "doi": public.get("doi"), "concept_doi": public.get("conceptdoi"),
        "previous_record_id": engine.PREVIOUS_RECORD_ID, "previous_doi": engine.PREVIOUS_DOI,
        "public_record_url": f"https://zenodo.org/records/{int(public['id'])}",
        "metadata_sha256": local["metadata_sha256"], "manifest_sha256": local["manifest_sha256"],
        "package_receipt_sha256": local["package_receipt_sha256"], "upload_order": local["upload_order"], "files": rows,
        "verification": {"exact_public_inventory": True, "reader_first_by_filename": True, "pdf_uploaded_first": True, "anonymous_byte_readback": True, "anonymous_readback_passes": 2, "all_nine_files_read_twice": True, "all_sha256_match_local_on_both_passes": True, "existing_concept_reused": True, "published_not_draft": True, "credentials_recorded": False, "authorization_header_recorded": False, "bucket_url_recorded": False, "absolute_local_paths_recorded": False, "user_personal_name_recorded": False},
        "provenance": f"Published by Codex at the user's direction; production note: {base.MODEL_NOTE}; source authors and human direction remain credited.",
        "non_endorsement": "Independent Indonesian edition; no source-author or institutional endorsement is implied.",
    }
    public_text_is_safe(json.dumps(receipt, ensure_ascii=False))
    return receipt


def finalize_transaction() -> None:
    receipt = load(base.RECEIPT); transaction = load(base.TRANSACTION)
    if receipt.get("status") != "PUBLISHED_AND_TWICE_ANONYMOUSLY_VERIFIED" or transaction.get("state") != "published_and_anonymously_verified":
        raise RuntimeError("publication/readback transaction did not close")
    transaction.update({"anonymous_readback_reproduced": True, "anonymous_readback_passes": 2, "publication_receipt_sha256": digest(base.RECEIPT), "sanitized": True, "credentials_recorded": False, "authorization_header_recorded": False, "bucket_url_recorded": False, "absolute_local_paths_recorded": False})
    public_text_is_safe(json.dumps(transaction, ensure_ascii=False)); base.save_json(base.TRANSACTION, transaction)


base.public_text_is_safe = public_text_is_safe
engine.verify_local = verify_local; engine.verify_public = verify_public; engine.make_receipt = make_receipt
base.verify_local = verify_local; base.verify_public = verify_public; base.make_receipt = make_receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", action="store_true")
    args = parser.parse_args()
    if args.plan:
        print(json.dumps({"status": "PREPARED_SCRIPT_NOT_EXECUTED", "release_id": base.RELEASE_ID, "version": base.VERSION, "existing_concept_doi": base.CONCEPT_DOI, "previous_record_id": engine.PREVIOUS_RECORD_ID, "reader_first_filename": base.PDF_NAME, "publish_not_draft": True, "anonymous_readback_passes": 2, "token": "runtime_only_not_logged"}, indent=2))
        return
    engine.publish_main()
    finalize_transaction()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise
