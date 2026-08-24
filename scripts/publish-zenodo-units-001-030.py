#!/usr/bin/env python3
"""Publish the sealed Roberts Units 001-030 payload in its existing concept.

This reuses the already-proved, resumable Zenodo transaction implementation
from the Units 001-024 release while replacing every release-specific identity
and validation rule.  It never records the credential and always performs an
anonymous byte/SHA-256 readback after publication.
"""
from __future__ import annotations

import importlib.util
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve()
BASE_PATH = SCRIPT.with_name("publish-zenodo-units-001-024.py")
SPEC = importlib.util.spec_from_file_location("o012_zenodo_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the proved Zenodo publication implementation")
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

base.RELEASE = base.LANE / "release" / "zenodo-units-001-030"
base.ARTIFACTS = base.RELEASE / "artifacts"
base.METADATA = base.RELEASE / "metadata.json"
base.MANIFEST = base.ARTIFACTS / "release-manifest.json"
base.TRANSACTION = base.RELEASE / "transaction.json"
base.RECEIPT = base.RELEASE / "publication-receipt.json"
base.SEED_RECORD = 22074233
PREVIOUS_RECORD_ID = 22074233
PREVIOUS_DOI = "10.5281/zenodo.22074233"
base.RELEASE_ID = "o012-roberts-id-units-001-030-v0.30.0"
base.TITLE = "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–30"
base.VERSION = "0.30.0"
base.PDF_NAME = "00_TOPOLOGI_ALJABAR_ID_UNITS_001_030_READER.pdf"
base.FILE_NAMES = [
    base.PDF_NAME,
    "TOPOLOGI_ALJABAR_ID_UNITS_001_030_READER.html",
    "TOPOLOGI_ALJABAR_ID_UNITS_001_030_EDITABLE_SOURCE_BACKEND.zip",
    "TOPOLOGI_ALJABAR_ID_UNITS_001_030_QA_PROVENANCE.zip",
    "LICENSE.md",
    "README_RELEASE.md",
    "RELEASE_RIGHTS.md",
    "release-manifest.json",
    "SHA256SUMS",
]


def verify_local() -> tuple[dict, dict]:
    metadata_payload = base.load_json(base.METADATA)
    manifest = base.load_json(base.MANIFEST)
    metadata = metadata_payload["metadata"]
    if metadata.get("title") != base.TITLE or metadata.get("version") != base.VERSION:
        raise RuntimeError("metadata title/version mismatch")
    if metadata.get("license") != "cc-by-4.0" or metadata.get("language") != "ind":
        raise RuntimeError("metadata license/language mismatch")
    if metadata.get("creators") != [{"name": "Roberts, David Michael"}]:
        raise RuntimeError("source creator metadata drift")
    if metadata.get("contributors") != [
        {"name": "Editor edisi Bahasa Indonesia", "type": "Editor"}
    ]:
        raise RuntimeError("generic editor metadata drift")

    public_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            base.METADATA,
            base.RELEASE / "README_RELEASE.md",
            base.RELEASE / "RELEASE_RIGHTS.md",
            base.MANIFEST,
        )
    )
    base.public_text_is_safe(public_text)
    normalized = public_text.replace("–", "-")
    if "30/30" not in public_text or "kursus komposit" not in public_text:
        raise RuntimeError("Roberts-complete/composite-partial scope is missing")
    if "Fomberg" not in public_text or "belum" not in public_text:
        raise RuntimeError("post-Roberts pending scope is missing")
    if "Notes.tex" not in public_text or "134-6368" not in normalized:
        raise RuntimeError("terminal Roberts source coverage is missing")
    if base.MODEL_NOTE not in public_text:
        raise RuntimeError("required model provenance is missing")
    if manifest.get("status") != "roberts_complete_composite_course_partial_checkpoint":
        raise RuntimeError("release manifest status is not the exact checkpoint status")
    source = manifest.get("source", {})
    if (
        source.get("line_start") != 134
        or source.get("line_end") != 6368
        or source.get("units") != 30
        or not source.get("roberts_complete")
        or source.get("composite_course_complete")
    ):
        raise RuntimeError("release manifest source closure drift")
    lineage = manifest.get("publication_lineage", {})
    if (
        lineage.get("existing_concept_doi") != base.CONCEPT_DOI
        or lineage.get("new_concept_created")
    ):
        raise RuntimeError("release manifest escaped the existing concept lineage")

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
    substantive = set(base.FILE_NAMES[:7])
    if {row["filename"] for row in manifest.get("artifacts", [])} != substantive:
        raise RuntimeError("manifest substantive inventory mismatch")
    by_name = {row["filename"]: row for row in rows}
    for row in manifest["artifacts"]:
        local = by_name[row["filename"]]
        if local["bytes"] != row["bytes"] or local["sha256"] != row["sha256"]:
            raise RuntimeError(f"manifest byte binding mismatch: {row['filename']}")
    sums = {}
    for line in (base.ARTIFACTS / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        checksum, name = line.split("  ", 1)
        sums[name] = checksum
    expected_sums = {
        path.name: base.digest(path) for path in files if path.name != "SHA256SUMS"
    }
    if sums != expected_sums:
        raise RuntimeError("SHA256SUMS does not bind every preceding release file")
    if files[0].name != base.PDF_NAME:
        raise RuntimeError("local upload inventory is not reader-first")
    return metadata_payload, {
        "files": rows,
        "metadata_sha256": base.digest(base.METADATA),
        "manifest_sha256": base.digest(base.MANIFEST),
    }


def make_receipt(public: dict, rows: list[dict], metadata_payload: dict, local: dict) -> dict:
    record_id = int(public["id"])
    return {
        "schema_version": "1.0",
        "status": "PUBLISHED_AND_ANONYMOUSLY_VERIFIED",
        "release_id": base.RELEASE_ID,
        "title": metadata_payload["metadata"]["title"],
        "version": metadata_payload["metadata"]["version"],
        "license": metadata_payload["metadata"]["license"],
        "roberts_complete": True,
        "composite_course_complete": False,
        "scope": (
            "Roberts Notes.tex lines 134-6368, lectures 1-30 of 30 through "
            "end{document}; Fomberg bridge and original proof/mastery/lab/capstone "
            "course closure pending"
        ),
        "record_id": record_id,
        "doi": public.get("doi"),
        "concept_doi": public.get("conceptdoi"),
        "public_record_url": f"https://zenodo.org/records/{record_id}",
        "metadata_sha256": local["metadata_sha256"],
        "manifest_sha256": local["manifest_sha256"],
        "files": rows,
        "verification": {
            "exact_public_inventory": True,
            "reader_first_by_filename": True,
            "pdf_uploaded_first": True,
            "anonymous_byte_readback": True,
            "all_sha256_match_local": True,
            "credentials_recorded": False,
            "user_personal_name_recorded": False,
        },
        "provenance": (
            "Published by Codex at the user's direction; production note: "
            f"{base.MODEL_NOTE}; source author and human direction remain credited."
        ),
        "non_endorsement": (
            "Independent Indonesian edition; no source-author or institutional "
            "endorsement is implied."
        ),
    }


def normalized_people(rows: list[dict], *, contributor: bool) -> list[tuple]:
    if contributor:
        return sorted(
            (row.get("name"), str(row.get("type", "")).lower()) for row in rows
        )
    return sorted((row.get("name"),) for row in rows)


def normalized_related(rows: list[dict]) -> set[tuple]:
    return {
        (row.get("identifier"), row.get("relation"), row.get("scheme"))
        for row in rows
    }


def assert_draft_metadata(actual: dict, expected: dict) -> None:
    scalar_keys = (
        "title",
        "upload_type",
        "publication_type",
        "description",
        "access_right",
        "license",
        "language",
        "version",
        "publication_date",
        "notes",
    )
    for key in scalar_keys:
        if actual.get(key) != expected.get(key):
            raise RuntimeError(f"Zenodo draft metadata drift: {key}")
    if normalized_people(actual.get("creators", []), contributor=False) != normalized_people(
        expected.get("creators", []), contributor=False
    ):
        raise RuntimeError("Zenodo draft creator metadata drift")
    if normalized_people(
        actual.get("contributors", []), contributor=True
    ) != normalized_people(expected.get("contributors", []), contributor=True):
        raise RuntimeError("Zenodo draft contributor metadata drift")
    if actual.get("keywords", []) != expected.get("keywords", []):
        raise RuntimeError("Zenodo draft keyword metadata drift")
    if normalized_related(actual.get("related_identifiers", [])) != normalized_related(
        expected.get("related_identifiers", [])
    ):
        raise RuntimeError("Zenodo draft related-identifier metadata drift")


def verify_public(
    record_id: int, metadata_payload: dict, local: dict
) -> tuple[dict, list[dict]]:
    public = None
    for _ in range(40):
        response = base.requests.get(
            f"{base.API}/records/{record_id}",
            timeout=180,
            headers={
                "User-Agent": "Codex-anonymous-readback",
                "Accept": "application/json",
            },
        )
        if response.status_code == 200:
            public = response.json()
            break
        time.sleep(2)
    if public is None:
        raise RuntimeError("published Zenodo record did not become anonymously readable")
    if not base.concept_matches(public):
        raise RuntimeError("published record escaped the existing concept lineage")

    actual = public.get("metadata", {})
    expected = metadata_payload["metadata"]
    actual_license = actual.get("license")
    if isinstance(actual_license, dict):
        actual_license = actual_license.get("id")
    if (
        actual.get("title") != expected["title"]
        or actual.get("version") != expected["version"]
        or actual_license != expected["license"]
        or actual.get("language") != expected["language"]
    ):
        raise RuntimeError("public Zenodo title/version/license/language drift")
    resource_type = actual.get("resource_type", {})
    if (
        resource_type.get("type") != expected["upload_type"]
        or resource_type.get("subtype") != expected["publication_type"]
        or actual.get("access_right") != expected["access_right"]
        or actual.get("publication_date") != expected["publication_date"]
        or actual.get("keywords", []) != expected.get("keywords", [])
        or actual.get("notes") != expected.get("notes")
    ):
        raise RuntimeError("public Zenodo type/access/date/keyword/notes drift")
    if normalized_people(
        actual.get("creators", []), contributor=False
    ) != normalized_people(expected.get("creators", []), contributor=False):
        raise RuntimeError("public Zenodo source creator drift")
    if normalized_people(
        actual.get("contributors", []), contributor=True
    ) != normalized_people(expected.get("contributors", []), contributor=True):
        raise RuntimeError("public Zenodo editor disclosure drift")
    description = str(actual.get("description", ""))
    base.public_text_is_safe(description)
    if not all(
        marker in description
        for marker in (
            "Roberts lengkap 30/30",
            "Fomberg",
            base.MODEL_NOTE,
            "tidak disponsori atau disahkan",
        )
    ):
        raise RuntimeError("public Zenodo scope/provenance/nonendorsement drift")
    if normalized_related(actual.get("related_identifiers", [])) != normalized_related(
        expected.get("related_identifiers", [])
    ):
        raise RuntimeError("public Zenodo related-identifier lineage drift")

    remote_names = [
        item.get("key") or item.get("filename") for item in public.get("files", [])
    ]
    local_by_name = {row["filename"]: row for row in local["files"]}
    if set(remote_names) != set(local_by_name):
        raise RuntimeError("public Zenodo inventory does not match the local release")
    if not remote_names or sorted(remote_names)[0] != base.PDF_NAME:
        raise RuntimeError("public Zenodo filenames do not sort reader-first")
    remote = {
        (item.get("key") or item.get("filename")): item
        for item in public.get("files", [])
    }
    rows = []
    for name in base.FILE_NAMES:
        url = remote[name]["links"]["self"]
        response = base.requests.get(
            url, timeout=180, headers={"User-Agent": "Codex-anonymous-readback"}
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"anonymous file readback failed: {name} ({response.status_code})"
            )
        data = response.content
        local_row = local_by_name[name]
        digest = base.hashlib.sha256(data).hexdigest()
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


def assert_draft_lineage(draft: dict, deposition_id: int) -> None:
    if int(draft.get("id", -1)) != deposition_id:
        raise RuntimeError("Zenodo draft identity drift")
    if not base.concept_matches(draft):
        raise RuntimeError("Zenodo draft is outside the required concept")


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def file_digest(path: Path, algorithm: str) -> str:
    digest = base.hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_draft_files(draft: dict, local: dict) -> None:
    remote_rows = list(draft.get("files", []))
    remote_names = [row.get("filename") or row.get("key") for row in remote_rows]
    if (
        len(remote_names) != len(base.FILE_NAMES)
        or len(set(remote_names)) != len(remote_names)
        or set(remote_names) != set(base.FILE_NAMES)
    ):
        raise RuntimeError(f"Zenodo draft inventory mismatch: {sorted(remote_names)}")
    local_by_name = {row["filename"]: row for row in local["files"]}
    remote_by_name = {
        (row.get("filename") or row.get("key")): row for row in remote_rows
    }
    for name in base.FILE_NAMES:
        remote = remote_by_name[name]
        local_row = local_by_name[name]
        remote_size = int(remote.get("filesize") or remote.get("size") or 0)
        if remote_size != local_row["bytes"]:
            raise RuntimeError(f"Zenodo draft size mismatch: {name}")
        checksum = str(remote.get("checksum", ""))
        if base.re.fullmatch(r"[0-9a-fA-F]{32}", checksum):
            # Legacy deposition responses expose a bare MD5; public record
            # responses may expose the same value as ``md5:<digest>``.
            algorithm, expected_digest = "md5", checksum.lower()
        elif ":" in checksum:
            algorithm, expected_digest = checksum.lower().split(":", 1)
        else:
            raise RuntimeError(f"Zenodo draft has no recognized checksum: {name}")
        if algorithm not in {"md5", "sha256"}:
            raise RuntimeError(f"unsupported Zenodo draft checksum type: {algorithm}")
        local_path = base.ARTIFACTS / name
        actual_digest = local_row["sha256"] if algorithm == "sha256" else local_row["md5"]
        if expected_digest != actual_digest:
            raise RuntimeError(f"Zenodo draft checksum mismatch: {name}")


def publish_main() -> None:
    metadata_payload, local = verify_local()
    latest = base.resolve_latest_public()
    latest_metadata = latest.get("metadata", {})
    latest_id = int(latest["id"])
    if (
        latest_metadata.get("title") == base.TITLE
        and latest_metadata.get("version") == base.VERSION
    ):
        public, rows = verify_public(latest_id, metadata_payload, local)
        if base.TRANSACTION.exists():
            transaction = base.load_json(base.TRANSACTION)
            transaction.update(
                {
                    "state": "published_and_anonymously_verified",
                    "record_id": latest_id,
                    "doi": public.get("doi"),
                    "concept_doi": public.get("conceptdoi"),
                }
            )
            transaction["anonymous_readback_reproduced"] = True
            base.save_json(base.TRANSACTION, transaction)
        receipt = make_receipt(public, rows, metadata_payload, local)
        base.save_json(base.RECEIPT, receipt)
        print(
            json.dumps(
                {
                    "status": receipt["status"],
                    "record_id": latest_id,
                    "doi": receipt["doi"],
                    "already_public": True,
                    "files": rows,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    if not str(latest_metadata.get("title", "")).startswith(
        "Topologi Aljabar: Edisi Bahasa Indonesia"
    ):
        raise RuntimeError("latest concept record is not the expected Indonesian edition")
    if base.parse_version(latest_metadata.get("version")) >= base.parse_version(
        base.VERSION
    ):
        raise RuntimeError("latest concept version is not older than the prepared release")
    if latest_id != PREVIOUS_RECORD_ID or latest.get("doi") != PREVIOUS_DOI:
        raise RuntimeError("latest public record is not the frozen release predecessor")

    token = base.read_token()
    session = base.requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "Codex-O012-publication",
        }
    )
    token = None

    transaction_preexisted = base.TRANSACTION.exists()
    transaction = base.load_json(base.TRANSACTION) if transaction_preexisted else None
    if transaction is not None:
        if (
            transaction.get("release_id") != base.RELEASE_ID
            or transaction.get("metadata_sha256") != local["metadata_sha256"]
            or transaction.get("manifest_sha256") != local["manifest_sha256"]
            or transaction.get("concept_key") != base.CONCEPT_RECORD
            or int(transaction.get("parent_record_id", -1)) != latest_id
        ):
            raise RuntimeError("existing Zenodo transaction does not bind this release/lineage")
    parent = base.api_request(
        session, "GET", f"{base.API}/deposit/depositions/{latest_id}"
    ).json()
    if not base.concept_matches(parent) or not parent.get("submitted"):
        raise RuntimeError("latest parent is not published in the required concept")

    if transaction is None:
        # A fresh invocation must never adopt or erase someone else's draft.
        # Check before writing our own recovery intent.
        existing_draft_url = parent.get("links", {}).get("latest_draft")
        if existing_draft_url:
            existing = base.api_request(session, "GET", existing_draft_url).json()
            if int(existing.get("id", -1)) != latest_id and not existing.get("submitted"):
                raise RuntimeError("pre-existing Zenodo draft requires separate resolution")
        transaction = {
            "schema_version": "1.0",
            "release_id": base.RELEASE_ID,
            "parent_record_id": latest_id,
            "concept_key": base.CONCEPT_RECORD,
            "metadata_sha256": local["metadata_sha256"],
            "manifest_sha256": local["manifest_sha256"],
            "state": "newversion_request_pending",
            "intent_created_at": datetime.now(timezone.utc).isoformat(),
        }
        # Persist intent before the remote POST.  If the process dies after the
        # POST, the next run can discover latest_draft without creating another.
        base.save_json(base.TRANSACTION, transaction)

    deposition_id = transaction.get("deposition_id")
    draft = None
    if deposition_id is None and transaction_preexisted:
        if transaction.get("state") != "newversion_request_pending":
            raise RuntimeError(
                "existing Zenodo transaction has no persisted deposition_id "
                "and is not a pending new-version intent"
            )
        latest_draft_url = parent.get("links", {}).get("latest_draft")
        if latest_draft_url:
            candidate = base.api_request(session, "GET", latest_draft_url).json()
            candidate_id = int(candidate.get("id", -1))
            if candidate_id != latest_id and not candidate.get("submitted"):
                assert_draft_lineage(candidate, candidate_id)
                raise RuntimeError(
                    "pending new-version intent has no persisted deposition_id, "
                    "but an unpublished same-concept draft exists; refusing to "
                    "adopt or delete it; reconcile the transaction and draft "
                    "explicitly"
                )
    if deposition_id is None:
        if transaction_preexisted:
            intent_age = datetime.now(timezone.utc) - parse_utc(
                transaction["intent_created_at"]
            )
            if intent_age > timedelta(minutes=15):
                raise RuntimeError("pending new-version intent is stale and has no correlated draft")
        draft = base.api_request(
            session,
            "POST",
            f"{base.API}/deposit/depositions/{latest_id}/actions/newversion",
        ).json()
        deposition_id = int(draft["id"])
        assert_draft_lineage(draft, deposition_id)
    transaction["deposition_id"] = int(deposition_id)
    transaction["state"] = "newversion_identified"
    base.save_json(base.TRANSACTION, transaction)

    if draft is None:
        draft = base.api_request(
            session, "GET", f"{base.API}/deposit/depositions/{deposition_id}"
        ).json()
    assert_draft_lineage(draft, int(deposition_id))

    if not draft.get("submitted"):
        base.api_request(
            session,
            "PUT",
            f"{base.API}/deposit/depositions/{deposition_id}",
            json=metadata_payload,
        )
        draft = base.api_request(
            session, "GET", f"{base.API}/deposit/depositions/{deposition_id}"
        ).json()
        assert_draft_lineage(draft, int(deposition_id))
        assert_draft_metadata(draft.get("metadata", {}), metadata_payload["metadata"])
        bucket = draft.get("links", {}).get("bucket")
        if not bucket:
            raise RuntimeError("Zenodo draft has no bucket URL")
        for file_object in list(draft.get("files", [])):
            file_id = file_object.get("id")
            if not file_id:
                raise RuntimeError("Zenodo draft file lacks a deletion identity")
            base.api_request(
                session,
                "DELETE",
                f"{base.API}/deposit/depositions/{deposition_id}/files/{file_id}",
            )
        if base.api_request(
            session, "GET", f"{base.API}/deposit/depositions/{deposition_id}"
        ).json().get("files"):
            raise RuntimeError("Zenodo draft did not empty after inherited-file deletion")
        for path in base.local_files():
            initial = next(
                row for row in local["files"] if row["filename"] == path.name
            )
            if (
                path.stat().st_size != initial["bytes"]
                or base.digest(path) != initial["sha256"]
            ):
                raise RuntimeError(f"local release changed before upload: {path.name}")
            upload_url = bucket.rstrip("/") + "/" + base.quote(path.name)
            with path.open("rb") as stream:
                base.api_request(
                    session,
                    "PUT",
                    upload_url,
                    data=stream,
                    headers={"Content-Type": "application/octet-stream"},
                )
        draft = base.api_request(
            session, "GET", f"{base.API}/deposit/depositions/{deposition_id}"
        ).json()
        assert_draft_lineage(draft, int(deposition_id))
        assert_draft_metadata(draft.get("metadata", {}), metadata_payload["metadata"])
        _, rechecked_local = verify_local()
        if rechecked_local != local:
            raise RuntimeError("local release changed during the Zenodo transaction")
        assert_draft_files(draft, local)
        transaction["state"] = "draft_verified_publish_requested"
        base.save_json(base.TRANSACTION, transaction)
        base.api_request(
            session,
            "POST",
            f"{base.API}/deposit/depositions/{deposition_id}/actions/publish",
        )

    public, rows = verify_public(int(deposition_id), metadata_payload, local)
    transaction.update(
        {
            "state": "published_and_anonymously_verified",
            "record_id": int(deposition_id),
            "doi": public.get("doi"),
            "concept_doi": public.get("conceptdoi"),
        }
    )
    base.save_json(base.TRANSACTION, transaction)
    receipt = make_receipt(public, rows, metadata_payload, local)
    base.save_json(base.RECEIPT, receipt)
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "record_id": int(deposition_id),
                "doi": public.get("doi"),
                "concept_doi": public.get("conceptdoi"),
                "already_public": False,
                "files": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


base.verify_local = verify_local
base.make_receipt = make_receipt
base.verify_public = verify_public


if __name__ == "__main__":
    publish_main()
