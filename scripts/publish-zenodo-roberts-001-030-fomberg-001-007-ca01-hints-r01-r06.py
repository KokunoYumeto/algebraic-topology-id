#!/usr/bin/env python3
"""Publish and twice anonymously verify the sealed 84/84-hints checkpoint.

The transaction is locked to Zenodo concept DOI 10.5281/zenodo.22061489 and
public predecessor 22105179 (version 0.31.0).  It creates exactly one new
version, never a new concept; uploads the exact reader-first nine-file payload;
publishes rather than leaving a draft; and performs two anonymous byte/hash
readback passes over every public file.  The inherited transaction engine reads
the authorized credential only at runtime and never writes it to output.
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
BASE_PATH = SCRIPT.with_name(
    "publish-zenodo-roberts-001-030-fomberg-001-007-ca01.py"
)
SPEC = importlib.util.spec_from_file_location("o012_ca01_publisher", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the proved CA01 publisher")
previous = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(previous)
engine = previous.engine
base = previous.base

base.RELEASE = (
    base.LANE
    / "release"
    / "zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06"
)
base.ARTIFACTS = base.RELEASE / "artifacts"
base.METADATA = base.RELEASE / "metadata.json"
base.MANIFEST = base.ARTIFACTS / "release-manifest.json"
base.TRANSACTION = base.RELEASE / "transaction.json"
base.RECEIPT = base.RELEASE / "publication-receipt.json"
base.SEED_RECORD = 22105179
base.CONCEPT_DOI = "10.5281/zenodo.22061489"
base.MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"
engine.PREVIOUS_RECORD_ID = 22105179
engine.PREVIOUS_DOI = "10.5281/zenodo.22105179"
base.RELEASE_ID = (
    "o012-composite-id-roberts-001-030-fomberg-001-007-ca01-"
    "hints-r01-r06-v0.31.1"
)
base.TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30, "
    "Jembatan Homologi §1.1–1.13, Asesmen Kumulatif 1, dan "
    "Petunjuk Rute 1–6"
)
base.VERSION = "0.31.1"
base.PDF_NAME = (
    "00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_"
    "CA01_HINTS_R01_R06_READER.pdf"
)
base.FILE_NAMES = [
    base.PDF_NAME,
    (
        "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_"
        "CA01_HINTS_R01_R06_READER.html"
    ),
    (
        "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_"
        "CA01_HINTS_R01_R06_EDITABLE_SOURCE_BACKEND.zip"
    ),
    (
        "TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_"
        "CA01_HINTS_R01_R06_QA_PROVENANCE.zip"
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
    "roberts_complete_fomberg_units_001_007_complete_ca01_complete_"
    "ordinary_mastery_84_complete_composite_course_partial"
)
FINAL_BACKEND_RECEIPT = (
    "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_CUMULATIVE_RECEIPT.json"
)
READBACK_PASSES = 2


def file_digest(path: Path, algorithm: str) -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def public_text_is_safe(text: str) -> None:
    previous.public_text_is_safe(text)


def assert_organization_rule(metadata: dict) -> None:
    prose = "\n".join(
        str(metadata.get(key, ""))
        for key in ("title", "description", "notes")
    ) + "\n" + "\n".join(str(item) for item in metadata.get("keywords", []))
    if ORGANIZATION_PATTERN.search(prose):
        raise RuntimeError("organization marker leaked into title or prose metadata")
    if any(ORGANIZATION_NAME in str(row) for row in metadata.get("creators", [])):
        raise RuntimeError("organization marker was placed in creator metadata")
    semantic = [
        {"name": row.get("name"), "type": row.get("type")}
        for row in metadata.get("contributors", [])
    ]
    if semantic != EXPECTED_CONTRIBUTORS:
        raise RuntimeError("organization must appear exactly once as final contributor")


def normalized_people(rows: list[dict], *, contributor: bool) -> list[tuple]:
    return engine.normalized_people(rows, contributor=contributor)


def normalized_related(rows: list[dict]) -> set[tuple]:
    return engine.normalized_related(rows)


def verify_zip(path: Path) -> None:
    with zipfile.ZipFile(path, "r") as archive:
        names = archive.namelist()
        if not names or len(names) != len(set(names)) or archive.testzip() is not None:
            raise RuntimeError(f"ZIP inventory/CRC failure: {path.name}")
        for info in archive.infolist():
            if (
                info.is_dir()
                or info.filename.startswith(("/", "../"))
                or "/../" in info.filename
                or "\\..\\" in info.filename
            ):
                raise RuntimeError(f"unsafe ZIP member: {path.name}:{info.filename}")


def verify_scope_metadata(metadata: dict) -> None:
    license_value = metadata.get("license")
    if isinstance(license_value, dict):
        license_value = license_value.get("id")
    if (
        metadata.get("title") != base.TITLE
        or metadata.get("version") != base.VERSION
        or license_value != "cc-by-sa-4.0"
        or metadata.get("language") != "ind"
        or metadata.get("access_right") != "open"
        or normalized_people(metadata.get("creators", []), contributor=False)
        != normalized_people(EXPECTED_CREATORS, contributor=False)
    ):
        raise RuntimeError("metadata identity/rights/creators drift")
    assert_organization_rule(metadata)
    description = str(metadata.get("description", ""))
    for marker in (
        "Roberts lengkap 30/30",
        "O012-FOM-001–007 lengkap",
        "D60-CA01",
        "lengkap 8/8",
        "84/84",
        "92/108",
        "D60-CA02 dan D60-CA03",
        "16 butir",
        "empat laboratorium",
        "capstone",
        "CC BY 4.0",
        "CC BY-SA 4.0",
        "Lazarovich, Nir",
        base.MODEL_NOTE,
        "tidak disponsori atau disahkan",
    ):
        if marker not in description and marker != "Lazarovich, Nir":
            raise RuntimeError(f"metadata description omits scope marker: {marker}")
    # The exact lecture credit is represented as a Zenodo contributor rather
    # than prose authorship; require that representation explicitly.
    if not any(
        row.get("name") == "Lazarovich, Nir" and row.get("type") == "Other"
        for row in metadata.get("contributors", [])
    ):
        raise RuntimeError("Nir Lazarovich lecture credit is absent")


def verify_local() -> tuple[dict, dict]:
    actual = sorted(base.ARTIFACTS.iterdir(), key=lambda path: path.name)
    if any(not path.is_file() for path in actual):
        raise RuntimeError("release artifacts directory contains a subdirectory")
    names = [path.name for path in actual]
    if len(names) != len(set(names)) or set(names) != set(base.FILE_NAMES):
        raise RuntimeError(f"exact nine-file local inventory mismatch: {names}")

    metadata_payload = base.load_json(base.METADATA)
    metadata = metadata_payload.get("metadata", {})
    verify_scope_metadata(metadata)
    public_text_is_safe(json.dumps(metadata_payload, ensure_ascii=False))

    manifest = base.load_json(base.MANIFEST)
    receipt = base.load_json(PACKAGE_RECEIPT)
    plan = base.load_json(PUBLICATION_PLAN)
    if manifest.get("release_id") != base.RELEASE_ID or manifest.get("status") != MANIFEST_STATUS:
        raise RuntimeError("release manifest identity/status drift")
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
        and fomberg.get("line_end") == 4185
        and fomberg.get("sections") == "1.1-1.13"
        and fomberg.get("next_source_line") == 4186
        and fomberg.get("complete_at_selected_boundary") is True
        and sources.get("composite_course_complete") is False
    ):
        raise RuntimeError("manifest source/cursor closure drift")

    assessment = manifest.get("assessment", {})
    if not (
        assessment.get("assessment_id") == "D60-CA01"
        and assessment.get("edition_unit_id") == "O012-ORIG-CA01"
        and assessment.get("origin") == "edition_original"
        and assessment.get("license") == "CC BY-SA 4.0"
        and assessment.get("complete") is True
        and assessment.get("exercises")
        == assessment.get("hints")
        == assessment.get("complete_solutions")
        == 8
        and assessment.get("source_problem_bank_used") is False
    ):
        raise RuntimeError("manifest CA01 closure drift")

    hints = manifest.get("ordinary_hints", {})
    if not (
        hints.get("edition_unit_id") == "O012-ORIG-HINTS-R01-R06"
        and hints.get("origin") == "edition_original"
        and hints.get("license") == "CC BY-SA 4.0"
        and hints.get("complete") is True
        and hints.get("hint_count") == 36
        and hints.get("routes") == [
            "D60-R01", "D60-R02", "D60-R03",
            "D60-R04", "D60-R05", "D60-R06",
        ]
        and hints.get("hints_per_route") == 6
        and hints.get("duplicate_exercises") == 0
        and hints.get("duplicate_solutions") == 0
    ):
        raise RuntimeError("manifest ordinary-hint closure drift")

    closure = manifest.get("course_closure", {})
    if not (
        closure.get("composite_course_complete") is False
        and closure.get("ordinary_mastery_complete") is True
        and closure.get("ordinary_mastery_items") == 84
        and closure.get("ordinary_mastery_required") == 84
        and closure.get("completed_assessments") == ["D60-CA01"]
        and closure.get("completed_assessment_items") == 8
        and closure.get("total_solution_bearing_items") == 92
        and closure.get("total_solution_bearing_items_required") == 108
        and closure.get("remaining_assessments") == ["D60-CA02", "D60-CA03"]
        and closure.get("remaining_assessment_items") == 16
        and closure.get("ordinary_hint_triples_remaining") == 0
        and closure.get("computation_labs_remaining") == 4
        and closure.get("capstone_remaining") == 1
    ):
        raise RuntimeError("manifest 84/84 and 92/108 course closure drift")

    rights = manifest.get("rights", {})
    if not (
        rights.get("integrated_payload") == "CC BY-SA 4.0"
        and rights.get("roberts_component") == "CC BY 4.0"
        and rights.get("fomberg_component") == "CC BY-SA 4.0"
        and rights.get("original_ca01_component") == "CC BY-SA 4.0"
        and rights.get("original_hint_component") == "CC BY-SA 4.0"
        and rights.get("non_endorsement_preserved") is True
    ):
        raise RuntimeError("manifest component-rights drift")

    lineage = manifest.get("publication_lineage", {})
    if not (
        lineage.get("existing_concept_doi") == base.CONCEPT_DOI
        and lineage.get("previous_record_id") == engine.PREVIOUS_RECORD_ID
        and lineage.get("previous_version_doi") == engine.PREVIOUS_DOI
        and lineage.get("new_concept_created") is False
    ):
        raise RuntimeError("manifest escaped the existing concept lineage")
    if (
        manifest.get("metadata_sha256") != base.digest(base.METADATA)
        or manifest.get("publication_plan_sha256") != base.digest(PUBLICATION_PLAN)
    ):
        raise RuntimeError("manifest control-file hash drift")

    if not (
        plan.get("state") == "prepared_not_published"
        and plan.get("artifact_identities_known") is True
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
        and plan.get("metadata_payload") == "metadata.json"
        and plan.get("payload_directory") == "artifacts"
    ):
        raise RuntimeError("publication plan escaped the frozen predecessor")
    binding = plan.get("backend_binding", {})
    manifest_backend = manifest.get("backend", {})
    if not (
        binding.get("final_identity_source") == FINAL_BACKEND_RECEIPT
        and binding.get("hardcoded_final_identity") is False
        and binding.get("expected_records") == manifest_backend.get("total_records") == 7012
        and binding.get("verified_snapshot") == {
            "total_records": manifest_backend.get("total_records"),
            "total_bytes": manifest_backend.get("total_bytes"),
            "bundle_sha256": manifest_backend.get("bundle_sha256"),
        }
        and manifest_backend.get("total_bytes") == 8545732
        and manifest_backend.get("bundle_sha256")
        == "7d723f9ef163303c7dde63d646dc8d5917c2450b1da5d24c87ef77bf4e4d664b"
    ):
        raise RuntimeError("publication plan/backend manifest binding drift")

    for path in (
        base.RELEASE / "README_RELEASE.md",
        base.RELEASE / "RELEASE_RIGHTS.md",
        base.RELEASE / "LICENSE.md",
        base.MANIFEST,
    ):
        text = path.read_text(encoding="utf-8")
        public_text_is_safe(text)
        if ORGANIZATION_PATTERN.search(text):
            raise RuntimeError(f"organization marker repeated in prose: {path.name}")

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
    if files[0].name != base.PDF_NAME or sorted(row["filename"] for row in rows)[0] != base.PDF_NAME:
        raise RuntimeError("local payload is not reader-first")
    substantive = set(base.FILE_NAMES[:7])
    if (
        manifest.get("artifact_order") != base.FILE_NAMES[:7]
        or {row.get("filename") for row in manifest.get("artifacts", [])}
        != substantive
    ):
        raise RuntimeError("manifest substantive inventory/order mismatch")
    local_by_name = {row["filename"]: row for row in rows}
    for row in manifest.get("artifacts", []):
        local = local_by_name[row["filename"]]
        if local["bytes"] != row["bytes"] or local["sha256"] != row["sha256"]:
            raise RuntimeError(f"manifest byte binding mismatch: {row['filename']}")

    sums = {}
    for line in (base.ARTIFACTS / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
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
    if not (
        receipt.get("status") == "PASS_PREPARED_NOT_PUBLISHED"
        and receipt.get("release_id") == base.RELEASE_ID
        and receipt.get("reader_first_filename") == base.PDF_NAME
        and receipt.get("file_count") == 9
        and receipt.get("total_payload_bytes") == sum(row["bytes"] for row in rows)
        and set(receipt_rows) == set(local_by_name)
    ):
        raise RuntimeError("package receipt scope/inventory drift")
    for name, local in local_by_name.items():
        recorded = receipt_rows[name]
        if local["bytes"] != recorded["bytes"] or local["sha256"] != recorded["sha256"]:
            raise RuntimeError(f"package receipt byte binding mismatch: {name}")
    gates = receipt.get("verification", {})
    for key in (
        "manifest_artifact_identities_match",
        "sha256sums_match",
        "zip_crc_and_inventory_pass",
        "source_archive_local_link_closure_pass",
        "rights_component_scope_consistent",
        "reader_first",
        "final_build_visual_browser_gates",
        "ca01_independent_reviews",
        "route_and_proof_censuses_included",
        "ordinary_hints_static_independent_reviews",
        "ordinary_mastery_84_complete",
    ):
        if gates.get(key) is not True:
            raise RuntimeError(f"package receipt omits gate: {key}")
    for name in base.FILE_NAMES[2:4]:
        verify_zip(base.ARTIFACTS / name)

    return metadata_payload, {
        "files": rows,
        "metadata_sha256": base.digest(base.METADATA),
        "manifest_sha256": base.digest(base.MANIFEST),
        "package_receipt_sha256": base.digest(PACKAGE_RECEIPT),
        "upload_order": list(base.FILE_NAMES),
    }


def _fetch_public_record(record_id: int, pass_index: int) -> dict:
    for _ in range(40):
        response = base.requests.get(
            f"{base.API}/records/{record_id}",
            timeout=180,
            headers={
                "Accept": "application/json",
                "Cache-Control": "no-cache",
                "User-Agent": f"Codex-anonymous-readback-pass-{pass_index}",
            },
        )
        if response.status_code == 200:
            return response.json()
        time.sleep(2)
    raise RuntimeError(
        f"published record did not become anonymously readable on pass {pass_index}"
    )


def _verify_public_metadata(public: dict, metadata_payload: dict) -> None:
    if not base.concept_matches(public):
        raise RuntimeError("published record escaped the existing concept")
    actual = public.get("metadata", {})
    expected = metadata_payload["metadata"]
    actual_license = actual.get("license")
    if isinstance(actual_license, dict):
        actual_license = actual_license.get("id")
    resource_type = actual.get("resource_type", {})
    if not (
        actual.get("title") == expected["title"]
        and actual.get("version") == expected["version"]
        and actual_license == expected["license"]
        and actual.get("language") == expected["language"]
        and resource_type.get("type") == expected["upload_type"]
        and resource_type.get("subtype") == expected["publication_type"]
        and actual.get("access_right") == expected["access_right"]
        and actual.get("publication_date") == expected["publication_date"]
        and actual.get("keywords", []) == expected.get("keywords", [])
        and actual.get("notes") == expected.get("notes")
        and actual.get("description") == expected.get("description")
    ):
        raise RuntimeError("public Zenodo scalar/type metadata drift")
    if normalized_people(actual.get("creators", []), contributor=False) != normalized_people(
        expected.get("creators", []), contributor=False
    ):
        raise RuntimeError("public source creator drift")
    if normalized_people(actual.get("contributors", []), contributor=True) != normalized_people(
        expected.get("contributors", []), contributor=True
    ):
        raise RuntimeError("public contributor drift")
    if normalized_related(actual.get("related_identifiers", [])) != normalized_related(
        expected.get("related_identifiers", [])
    ):
        raise RuntimeError("public related-identifier lineage drift")
    verify_scope_metadata(actual)
    public_text_is_safe(json.dumps(actual, ensure_ascii=False))


def verify_public(
    record_id: int, metadata_payload: dict, local: dict
) -> tuple[dict, list[dict]]:
    local_by_name = {row["filename"]: row for row in local["files"]}
    readbacks_by_name = {name: [] for name in base.FILE_NAMES}
    first_public = None
    for pass_index in range(1, READBACK_PASSES + 1):
        public = _fetch_public_record(record_id, pass_index)
        _verify_public_metadata(public, metadata_payload)
        if int(public.get("id", -1)) != record_id:
            raise RuntimeError(f"public record identity drift on pass {pass_index}")
        remote_names = [
            item.get("key") or item.get("filename")
            for item in public.get("files", [])
        ]
        if not (
            len(remote_names) == 9
            and len(set(remote_names)) == 9
            and set(remote_names) == set(base.FILE_NAMES)
            and sorted(remote_names)[0] == base.PDF_NAME
        ):
            raise RuntimeError(
                f"public Zenodo inventory mismatch on pass {pass_index}: {remote_names}"
            )
        remote = {
            (item.get("key") or item.get("filename")): item
            for item in public.get("files", [])
        }
        for name in base.FILE_NAMES:
            url = remote[name]["links"]["self"]
            response = base.requests.get(
                url,
                timeout=180,
                headers={
                    "Cache-Control": "no-cache",
                    "User-Agent": f"Codex-anonymous-byte-readback-pass-{pass_index}",
                },
            )
            if response.status_code != 200:
                raise RuntimeError(
                    f"anonymous file readback pass {pass_index} failed: "
                    f"{name} ({response.status_code})"
                )
            data = response.content
            digest = hashlib.sha256(data).hexdigest()
            local_row = local_by_name[name]
            if len(data) != local_row["bytes"] or digest != local_row["sha256"]:
                raise RuntimeError(
                    f"anonymous byte/hash readback pass {pass_index} mismatch: {name}"
                )
            readbacks_by_name[name].append(
                {
                    "pass": pass_index,
                    "status": response.status_code,
                    "bytes": len(data),
                    "sha256": digest,
                    "url": url,
                }
            )
        if first_public is None:
            first_public = public
        elif (
            public.get("doi") != first_public.get("doi")
            or public.get("conceptdoi") != first_public.get("conceptdoi")
        ):
            raise RuntimeError("public DOI/concept identity changed between readback passes")

    rows = []
    for name in base.FILE_NAMES:
        passes = readbacks_by_name[name]
        if len(passes) != READBACK_PASSES or passes[0]["sha256"] != passes[1]["sha256"]:
            raise RuntimeError(f"two-pass readback closure failed: {name}")
        rows.append(
            {
                "filename": name,
                "bytes": passes[-1]["bytes"],
                "sha256": passes[-1]["sha256"],
                "url": passes[-1]["url"],
                "anonymous_readbacks": passes,
            }
        )
    if first_public is None:
        raise RuntimeError("anonymous readback produced no public record")
    return first_public, rows


def make_receipt(
    public: dict, rows: list[dict], metadata_payload: dict, local: dict
) -> dict:
    record_id = int(public["id"])
    receipt = {
        "schema_version": "1.0",
        "status": "PUBLISHED_AND_TWICE_ANONYMOUSLY_VERIFIED",
        "release_id": base.RELEASE_ID,
        "title": metadata_payload["metadata"]["title"],
        "version": base.VERSION,
        "license": metadata_payload["metadata"]["license"],
        "scope": (
            "Roberts 30/30 complete; selected Fomberg Sections 1.1-1.13 "
            "complete; ordinary mastery 84/84 complete; D60-CA01 complete "
            "with 8 solved items; 92/108 required items complete; D60-CA02/03 "
            "(16 items), four computation labs, and capstone pending"
        ),
        "record_id": record_id,
        "doi": public.get("doi"),
        "concept_doi": public.get("conceptdoi"),
        "previous_record_id": engine.PREVIOUS_RECORD_ID,
        "previous_doi": engine.PREVIOUS_DOI,
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
            "anonymous_readback_passes": READBACK_PASSES,
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
            "Independent Indonesian edition; no source-author or institutional "
            "endorsement is implied."
        ),
    }
    public_text_is_safe(json.dumps(receipt, ensure_ascii=False))
    return receipt


def finalize_sanitized_transaction() -> None:
    receipt = base.load_json(base.RECEIPT)
    if not (
        receipt.get("status") == "PUBLISHED_AND_TWICE_ANONYMOUSLY_VERIFIED"
        and receipt.get("verification", {}).get("anonymous_readback_passes")
        == READBACK_PASSES
        and receipt.get("verification", {}).get("all_nine_files_read_twice") is True
    ):
        raise RuntimeError("publication receipt does not prove two complete readback passes")
    transaction = base.load_json(base.TRANSACTION)
    if transaction.get("state") != "published_and_anonymously_verified":
        raise RuntimeError("transaction did not reach published/readback state")
    transaction.update(
        {
            "anonymous_readback_reproduced": True,
            "anonymous_readback_passes": READBACK_PASSES,
            "publication_receipt_sha256": base.digest(base.RECEIPT),
            "sanitized": True,
            "credentials_recorded": False,
            "authorization_header_recorded": False,
            "bucket_url_recorded": False,
            "absolute_local_paths_recorded": False,
        }
    )
    public_text_is_safe(json.dumps(transaction, ensure_ascii=False))
    base.save_json(base.TRANSACTION, transaction)


base.public_text_is_safe = public_text_is_safe
engine.verify_local = verify_local
engine.verify_public = verify_public
engine.make_receipt = make_receipt
base.verify_local = verify_local
base.verify_public = verify_public
base.make_receipt = make_receipt


if __name__ == "__main__":
    engine.publish_main()
    finalize_sanitized_transaction()
