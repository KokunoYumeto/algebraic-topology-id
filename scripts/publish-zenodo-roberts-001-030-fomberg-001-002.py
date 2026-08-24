#!/usr/bin/env python3
"""Publish the sealed Roberts 001-030 + Fomberg 001-002 checkpoint.

The transaction is locked to Zenodo concept DOI 10.5281/zenodo.22061489 and
public predecessor 22084021 (version 0.30.1).  It creates one new version,
never a new concept.  It inherits the proved resumable transaction and
runtime-only credential route, uploads the exact reader-first nine-file
payload, publishes it, and then anonymously reads back every file and verifies
its byte count and SHA-256.  Credentials and authorization data are never
written to receipts or output.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import time
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve()
BASE_PATH = SCRIPT.with_name("publish-zenodo-roberts-001-030-fomberg-001.py")
SPEC = importlib.util.spec_from_file_location("o012_fomberg_001_publisher", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the proved Fomberg 001 publisher")
prior = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prior)
previous = prior.previous
base = prior.base

base.RELEASE = (
    base.LANE / "release" / "zenodo-roberts-001-030-fomberg-001-002"
)
base.ARTIFACTS = base.RELEASE / "artifacts"
base.METADATA = base.RELEASE / "metadata.json"
base.MANIFEST = base.ARTIFACTS / "release-manifest.json"
base.TRANSACTION = base.RELEASE / "transaction.json"
base.RECEIPT = base.RELEASE / "publication-receipt.json"
base.SEED_RECORD = 22084021
previous.PREVIOUS_RECORD_ID = 22084021
previous.PREVIOUS_DOI = "10.5281/zenodo.22084021"
base.RELEASE_ID = "o012-composite-id-roberts-001-030-fomberg-001-002-v0.30.2"
base.TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30 dan "
    "Jembatan Homologi §1.1–1.4"
)
base.VERSION = "0.30.2"
base.PDF_NAME = (
    "00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_"
    "FOMBERG_001_002_READER.pdf"
)
base.FILE_NAMES = [
    base.PDF_NAME,
    "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_002_READER.html",
    (
        "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_002_"
        "EDITABLE_SOURCE_BACKEND.zip"
    ),
    (
        "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_002_"
        "QA_PROVENANCE.zip"
    ),
    "LICENSE.md",
    "README_RELEASE.md",
    "RELEASE_RIGHTS.md",
    "release-manifest.json",
    "SHA256SUMS",
]

PACKAGE_RECEIPT = base.RELEASE / "PACKAGE_PREPARATION_RECEIPT.json"
PUBLICATION_PLAN = base.RELEASE / "publication-plan.json"
ORGANIZATION_NAME = "Translation and " + "Transcription Project"
ORGANIZATION_ABBREVIATION = "".join(("T", "T", "P"))
ORGANIZATION_PATTERN = re.compile(
    rf"(?i)\b{re.escape(ORGANIZATION_ABBREVIATION)}\b|"
    rf"{re.escape(ORGANIZATION_NAME)}"
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
MANIFEST_STATUS = (
    "roberts_complete_fomberg_units_001_002_complete_composite_course_partial"
)


def file_digest(path: Path, algorithm: str) -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def public_text_is_safe(text: str) -> None:
    local_account_name = Path.home().name
    if len(local_account_name) >= 3 and re.search(
        rf"(?i)\b{re.escape(local_account_name)}\b", text
    ):
        raise RuntimeError("local account name leaked into public material")
    patterns = (
        r"(?i)[A-Z]:[\\/](?:Users|Documents and Settings|Temp|ProgramData)[\\/]",
        r"(?i)\\\\(?:Users|Documents|Temp|ProgramData)\\",
        r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"(?i)authorization\s*[:=]\s*[\"']?bearer",
        r"(?i)\b(?:access|api)[_-]?token\s*[:=]",
        r"(?i)\bsk-[A-Za-z0-9_-]{16,}",
    )
    if any(re.search(pattern, text) for pattern in patterns):
        raise RuntimeError("private path or credential marker in public material")


def assert_organization_rule(metadata: dict) -> None:
    prose = "\n".join(
        str(metadata.get(key, ""))
        for key in ("title", "description", "notes")
    ) + "\n" + "\n".join(str(item) for item in metadata.get("keywords", []))
    if ORGANIZATION_PATTERN.search(prose):
        raise RuntimeError("organization marker leaked into title or prose")
    creators = metadata.get("creators", [])
    contributors = metadata.get("contributors", [])
    if any(ORGANIZATION_NAME in str(row) for row in creators):
        raise RuntimeError("organization marker was placed in creator metadata")
    occurrences = sum(
        1 for row in contributors if row.get("name") == ORGANIZATION_NAME
    )
    semantic_contributors = [
        {"name": row.get("name"), "type": row.get("type")}
        for row in contributors
    ]
    if occurrences != 1 or semantic_contributors != EXPECTED_CONTRIBUTORS:
        raise RuntimeError(
            "organization must appear exactly once as the exact contributor"
        )


def normalized_people(rows: list[dict], *, contributor: bool) -> list[tuple]:
    return previous.normalized_people(rows, contributor=contributor)


def normalized_related(rows: list[dict]) -> set[tuple]:
    return previous.normalized_related(rows)


def verify_zip(path: Path) -> None:
    with zipfile.ZipFile(path, "r") as archive:
        names = archive.namelist()
        if not names or len(names) != len(set(names)):
            raise RuntimeError(f"ZIP inventory is empty or duplicated: {path.name}")
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC failure: {path.name}")


def verify_local() -> tuple[dict, dict]:
    expected_names = base.FILE_NAMES
    actual_entries = sorted(base.ARTIFACTS.iterdir(), key=lambda path: path.name)
    if any(not path.is_file() for path in actual_entries):
        raise RuntimeError("release artifacts directory contains a subdirectory")
    actual_names = [path.name for path in actual_entries]
    if (
        len(actual_names) != len(set(actual_names))
        or set(actual_names) != set(expected_names)
    ):
        raise RuntimeError(f"exact nine-file local inventory mismatch: {actual_names}")

    metadata_payload = base.load_json(base.METADATA)
    metadata = metadata_payload.get("metadata", {})
    manifest = base.load_json(base.MANIFEST)
    receipt = base.load_json(PACKAGE_RECEIPT)
    plan = base.load_json(PUBLICATION_PLAN)

    if metadata.get("title") != base.TITLE or metadata.get("version") != base.VERSION:
        raise RuntimeError("metadata title/version mismatch")
    if (
        metadata.get("license") != "cc-by-sa-4.0"
        or metadata.get("language") != "ind"
        or metadata.get("access_right") != "open"
    ):
        raise RuntimeError("metadata license/language/access mismatch")
    if metadata.get("creators") != EXPECTED_CREATORS:
        raise RuntimeError("source creator metadata drift")
    assert_organization_rule(metadata)

    public_prose_paths = (
        base.RELEASE / "README_RELEASE.md",
        base.RELEASE / "RELEASE_RIGHTS.md",
        base.RELEASE / "LICENSE.md",
        base.MANIFEST,
    )
    for path in public_prose_paths:
        text = path.read_text(encoding="utf-8")
        public_text_is_safe(text)
        if ORGANIZATION_PATTERN.search(text):
            raise RuntimeError(f"organization marker repeated in prose: {path.name}")
    public_text_is_safe(json.dumps(metadata_payload, ensure_ascii=False))

    if manifest.get("release_id") != base.RELEASE_ID:
        raise RuntimeError("release manifest ID mismatch")
    if manifest.get("status") != MANIFEST_STATUS:
        raise RuntimeError("release manifest status drift")
    if "published" in manifest:
        raise RuntimeError("immutable upload manifest contains a publication claim")
    sources = manifest.get("sources", {})
    roberts = sources.get("roberts", {})
    fomberg = sources.get("fomberg", {})
    if not (
        roberts.get("line_start") == 134
        and roberts.get("line_end") == 6368
        and roberts.get("edition_units") == 30
        and roberts.get("complete") is True
        and fomberg.get("line_start") == 31
        and fomberg.get("line_end") == 1290
        and fomberg.get("sections") == "1.1-1.4"
        and fomberg.get("component_ids")
        == ["O012-FOM-001", "O012-FOM-002"]
        and fomberg.get("course_route_unit_ids") == ["D60-R08", "D60-R09"]
        and fomberg.get("next_source_line") == 1291
        and sources.get("composite_course_complete") is False
    ):
        raise RuntimeError("manifest source/cursor closure drift")
    rights = manifest.get("rights", {})
    if (
        rights.get("integrated_payload") != "CC BY-SA 4.0"
        or rights.get("roberts_component") != "CC BY 4.0"
        or rights.get("fomberg_component") != "CC BY-SA 4.0"
    ):
        raise RuntimeError("manifest component-rights drift")
    lineage = manifest.get("publication_lineage", {})
    if (
        lineage.get("existing_concept_doi") != base.CONCEPT_DOI
        or lineage.get("previous_record_id") != previous.PREVIOUS_RECORD_ID
        or lineage.get("new_concept_created") is not False
    ):
        raise RuntimeError("manifest escaped the existing concept lineage")
    if manifest.get("metadata_sha256") != base.digest(base.METADATA):
        raise RuntimeError("manifest metadata hash drift")
    if manifest.get("publication_plan_sha256") != base.digest(PUBLICATION_PLAN):
        raise RuntimeError("manifest publication-plan hash drift")

    if (
        plan.get("state") != "prepared_not_published"
        or plan.get("release_id") != base.RELEASE_ID
        or plan.get("version") != base.VERSION
        or plan.get("existing_concept_doi") != base.CONCEPT_DOI
        or plan.get("current_public_record_id") != previous.PREVIOUS_RECORD_ID
        or plan.get("current_public_doi") != previous.PREVIOUS_DOI
        or plan.get("new_concept_allowed") is not False
        or plan.get("new_deposition_created") is not False
        or plan.get("credentials_used") is not False
        or plan.get("reader_first_filename") != base.PDF_NAME
        or plan.get("metadata_payload") != "metadata.json"
        or plan.get("payload_directory") != "artifacts"
        or plan.get("publish_not_draft") is not True
        or plan.get("anonymous_byte_readback_required") is not True
    ):
        raise RuntimeError("publication plan escaped the frozen predecessor")

    files = base.local_files()
    rows = [
        {
            "filename": path.name,
            "bytes": path.stat().st_size,
            "sha256": base.digest(path),
            "md5": file_digest(path, "md5"),
        }
        for path in files
    ]
    if files[0].name != base.PDF_NAME:
        raise RuntimeError("local upload order is not reader-first")
    if manifest.get("artifact_order") != base.FILE_NAMES[:7]:
        raise RuntimeError("manifest substantive order is not reader-first")
    substantive = set(base.FILE_NAMES[:7])
    if {row.get("filename") for row in manifest.get("artifacts", [])} != substantive:
        raise RuntimeError("manifest substantive inventory mismatch")
    local_by_name = {row["filename"]: row for row in rows}
    for row in manifest["artifacts"]:
        local = local_by_name[row["filename"]]
        if local["bytes"] != row["bytes"] or local["sha256"] != row["sha256"]:
            raise RuntimeError(f"manifest byte binding mismatch: {row['filename']}")

    sums: dict[str, str] = {}
    for line in (base.ARTIFACTS / "SHA256SUMS").read_text(
        encoding="utf-8"
    ).splitlines():
        checksum, name = line.split("  ", 1)
        if name in sums:
            raise RuntimeError(f"duplicate SHA256SUMS row: {name}")
        sums[name] = checksum
    expected_sums = {
        path.name: base.digest(path)
        for path in files
        if path.name != "SHA256SUMS"
    }
    if sums != expected_sums:
        raise RuntimeError("SHA256SUMS does not bind the exact first eight files")

    receipt_rows = {row["filename"]: row for row in receipt.get("files", [])}
    if (
        receipt.get("status") != "PASS_PREPARED_NOT_PUBLISHED"
        or receipt.get("release_id") != base.RELEASE_ID
        or receipt.get("reader_first_filename") != base.PDF_NAME
        or receipt.get("file_count") != 9
        or receipt.get("total_payload_bytes")
        != sum(int(row["bytes"]) for row in rows)
        or set(receipt_rows) != set(local_by_name)
    ):
        raise RuntimeError("package receipt scope/inventory drift")
    for name, local in local_by_name.items():
        recorded = receipt_rows[name]
        if local["bytes"] != recorded["bytes"] or local["sha256"] != recorded["sha256"]:
            raise RuntimeError(f"package receipt byte binding mismatch: {name}")
    verification = receipt.get("verification", {})
    if not all(
        verification.get(key) is True
        for key in (
            "manifest_artifact_identities_match",
            "sha256sums_match",
            "zip_crc_and_inventory_pass",
            "source_archive_local_link_closure_pass",
            "rights_component_scope_consistent",
            "reader_first",
        )
    ):
        raise RuntimeError("package receipt omits preparation gates")
    for name in base.FILE_NAMES[2:4]:
        verify_zip(base.ARTIFACTS / name)

    return metadata_payload, {
        "files": rows,
        "metadata_sha256": base.digest(base.METADATA),
        "manifest_sha256": base.digest(base.MANIFEST),
        "package_receipt_sha256": base.digest(PACKAGE_RECEIPT),
        "upload_order": list(base.FILE_NAMES),
    }


def verify_public(
    record_id: int, metadata_payload: dict, local: dict
) -> tuple[dict, list[dict]]:
    public = None
    for _ in range(40):
        response = base.requests.get(
            f"{base.API}/records/{record_id}",
            timeout=180,
            headers={
                "Accept": "application/json",
                "User-Agent": "Codex-anonymous-readback",
            },
        )
        if response.status_code == 200:
            public = response.json()
            break
        time.sleep(2)
    if public is None:
        raise RuntimeError("published record did not become anonymously readable")
    if not base.concept_matches(public):
        raise RuntimeError("published record escaped the existing concept")

    actual = public.get("metadata", {})
    expected = metadata_payload["metadata"]
    actual_license = actual.get("license")
    if isinstance(actual_license, dict):
        actual_license = actual_license.get("id")
    resource_type = actual.get("resource_type", {})
    if (
        actual.get("title") != expected["title"]
        or actual.get("version") != expected["version"]
        or actual_license != expected["license"]
        or actual.get("language") != expected["language"]
        or resource_type.get("type") != expected["upload_type"]
        or resource_type.get("subtype") != expected["publication_type"]
        or actual.get("access_right") != expected["access_right"]
        or actual.get("publication_date") != expected["publication_date"]
        or actual.get("keywords", []) != expected.get("keywords", [])
        or actual.get("notes") != expected.get("notes")
        or actual.get("description") != expected.get("description")
    ):
        raise RuntimeError("public Zenodo scalar/type metadata drift")
    if normalized_people(
        actual.get("creators", []), contributor=False
    ) != normalized_people(expected.get("creators", []), contributor=False):
        raise RuntimeError("public source creator drift")
    if normalized_people(
        actual.get("contributors", []), contributor=True
    ) != normalized_people(expected.get("contributors", []), contributor=True):
        raise RuntimeError("public contributor drift")
    if normalized_related(actual.get("related_identifiers", [])) != normalized_related(
        expected.get("related_identifiers", [])
    ):
        raise RuntimeError("public related-identifier lineage drift")
    assert_organization_rule(actual)
    public_text_is_safe(json.dumps(actual, ensure_ascii=False))
    description = str(actual.get("description", ""))
    for marker in (
        "Roberts lengkap 30/30",
        "O012-FOM-001",
        "O012-FOM-002",
        "baris 31–1290",
        "baris 1291",
        "CC BY 4.0",
        "CC BY-SA 4.0",
        base.MODEL_NOTE,
        "tidak disponsori atau disahkan",
    ):
        if marker not in description:
            raise RuntimeError(f"public description omits scope marker: {marker}")

    remote_names = [
        item.get("key") or item.get("filename") for item in public.get("files", [])
    ]
    if (
        len(remote_names) != len(base.FILE_NAMES)
        or len(set(remote_names)) != len(remote_names)
        or set(remote_names) != set(base.FILE_NAMES)
    ):
        raise RuntimeError(f"public Zenodo inventory mismatch: {remote_names}")
    if sorted(remote_names)[0] != base.PDF_NAME:
        raise RuntimeError("public filenames do not sort reader-first")

    local_by_name = {row["filename"]: row for row in local["files"]}
    remote = {
        (item.get("key") or item.get("filename")): item
        for item in public.get("files", [])
    }
    rows = []
    for name in base.FILE_NAMES:
        url = remote[name]["links"]["self"]
        response = base.requests.get(
            url,
            timeout=180,
            headers={"User-Agent": "Codex-anonymous-readback"},
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"anonymous file readback failed: {name} ({response.status_code})"
            )
        data = response.content
        local_row = local_by_name[name]
        digest = hashlib.sha256(data).hexdigest()
        if len(data) != local_row["bytes"] or digest != local_row["sha256"]:
            raise RuntimeError(f"anonymous byte/hash readback mismatch: {name}")
        rows.append(
            {
                "filename": name,
                "status": response.status_code,
                "bytes": len(data),
                "sha256": digest,
                "url": url,
            }
        )
    return public, rows


def make_receipt(
    public: dict, rows: list[dict], metadata_payload: dict, local: dict
) -> dict:
    record_id = int(public["id"])
    return {
        "schema_version": "1.0",
        "status": "PUBLISHED_AND_ANONYMOUSLY_VERIFIED",
        "release_id": base.RELEASE_ID,
        "title": metadata_payload["metadata"]["title"],
        "version": metadata_payload["metadata"]["version"],
        "license": metadata_payload["metadata"]["license"],
        "scope": (
            "Roberts Notes.tex lines 134-6368, lectures 1-30 complete; "
            "Fomberg algebraic_topology.tex lines 31-1290, Sections 1.1-1.4, "
            "O012-FOM-001/002 complete; next line 1291; composite course partial"
        ),
        "record_id": record_id,
        "doi": public.get("doi"),
        "concept_doi": public.get("conceptdoi"),
        "public_record_url": f"https://zenodo.org/records/{record_id}",
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
            "all_sha256_match_local": True,
            "existing_concept_reused": True,
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
            "Independent Indonesian edition; no source-author or institutional "
            "endorsement is implied."
        ),
    }


base.public_text_is_safe = public_text_is_safe
previous.verify_local = verify_local
previous.verify_public = verify_public
previous.make_receipt = make_receipt
base.verify_local = verify_local
base.verify_public = verify_public
base.make_receipt = make_receipt


if __name__ == "__main__":
    previous.publish_main()
