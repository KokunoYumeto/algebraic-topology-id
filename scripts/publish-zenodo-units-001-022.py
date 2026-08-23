#!/usr/bin/env python3
"""Publish the prepared Units 001-022 payload as the next Zenodo version.

The script is resumable and concept-lineage locked. It publishes rather than
leaving a draft, then anonymously reads every public file back byte-for-byte.
It writes only sanitized transaction/receipt files under the release folder.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests


LANE = Path(__file__).resolve().parents[1]
RELEASE = LANE / "release" / "zenodo-units-001-022"
ARTIFACTS = RELEASE / "artifacts"
METADATA = RELEASE / "metadata.json"
MANIFEST = ARTIFACTS / "release-manifest.json"
TRANSACTION = RELEASE / "transaction.json"
RECEIPT = RELEASE / "publication-receipt.json"
TOKEN_FILE = LANE.parents[3] / "Obsidian notes" / "New zenodo token.md"
API = "https://zenodo.org/api"
SEED_RECORD = 22071667
CONCEPT_RECORD = "22061489"
CONCEPT_DOI = "10.5281/zenodo.22061489"
RELEASE_ID = "o012-roberts-id-units-001-022-v0.22.0"
TITLE = "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–22"
VERSION = "0.22.0"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"

PDF_NAME = "00_TOPOLOGI_ALJABAR_ID_UNITS_001_022_READER.pdf"
FILE_NAMES = [
    PDF_NAME,
    "TOPOLOGI_ALJABAR_ID_UNITS_001_022_READER.html",
    "TOPOLOGI_ALJABAR_ID_UNITS_001_022_EDITABLE_SOURCE_BACKEND.zip",
    "TOPOLOGI_ALJABAR_ID_UNITS_001_022_QA_PROVENANCE.zip",
    "README_RELEASE.md",
    "RELEASE_RIGHTS.md",
    "release-manifest.json",
    "SHA256SUMS",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def local_files() -> list[Path]:
    paths = [ARTIFACTS / name for name in FILE_NAMES]
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
    return paths


def public_text_is_safe(text: str) -> None:
    if re.search(r"(?i)\bTTP\b|Translation and Transcription Project", text):
        raise RuntimeError("forbidden umbrella marker in public Zenodo material")
    local_account_name = Path.home().name
    if len(local_account_name) >= 3 and re.search(rf"(?i)\b{re.escape(local_account_name)}\b", text):
        raise RuntimeError("local account name leaked into public Zenodo material")
    if re.search(r"(?i)[A-Z]:[\\/](?:Users|Documents and Settings|Temp|ProgramData)[\\/]", text):
        raise RuntimeError("absolute local path leaked into public Zenodo material")


def verify_local() -> tuple[dict, dict]:
    metadata_payload = load_json(METADATA)
    manifest = load_json(MANIFEST)
    metadata = metadata_payload["metadata"]
    if metadata["title"] != TITLE or metadata["version"] != VERSION:
        raise RuntimeError("metadata title/version mismatch")
    if metadata["license"] != "cc-by-4.0" or metadata["language"] != "ind":
        raise RuntimeError("metadata license/language mismatch")
    if metadata["creators"] != [{"name": "Roberts, David Michael"}]:
        raise RuntimeError("source creator metadata drift")
    if metadata["contributors"] != [{"name": "Editor edisi Bahasa Indonesia", "type": "Editor"}]:
        raise RuntimeError("generic editor metadata drift")
    public_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (METADATA, RELEASE / "README_RELEASE.md", RELEASE / "RELEASE_RIGHTS.md", MANIFEST)
    )
    public_text_is_safe(public_text)
    if "Kuliah 23–30" not in public_text or "belum" not in public_text:
        raise RuntimeError("partial-scope language is missing")
    if "Notes.tex" not in public_text or "134-4938" not in public_text.replace("–", "-"):
        raise RuntimeError("exact source coverage is missing")
    if MODEL_NOTE not in public_text:
        raise RuntimeError("required model provenance is missing")
    if manifest.get("status") != "incomplete_checkpoint":
        raise RuntimeError("release manifest has a stale completion claim")
    lineage = manifest.get("publication_lineage", {})
    if lineage.get("existing_concept_doi") != CONCEPT_DOI or lineage.get("new_concept_created"):
        raise RuntimeError("release manifest escaped the existing concept lineage")

    files = local_files()
    rows = [{"filename": path.name, "bytes": path.stat().st_size, "sha256": digest(path)} for path in files]
    substantive = set(FILE_NAMES[:6])
    if {row["filename"] for row in manifest["artifacts"]} != substantive:
        raise RuntimeError("manifest substantive inventory mismatch")
    for row in manifest["artifacts"]:
        local = next(item for item in rows if item["filename"] == row["filename"])
        if local["bytes"] != row["bytes"] or local["sha256"] != row["sha256"]:
            raise RuntimeError(f"manifest byte binding mismatch: {row['filename']}")
    sums = {}
    for line in (ARTIFACTS / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        checksum, name = line.split("  ", 1)
        sums[name] = checksum
    expected_sums = {path.name: digest(path) for path in files if path.name != "SHA256SUMS"}
    if sums != expected_sums:
        raise RuntimeError("SHA256SUMS does not bind the seven preceding release files")
    if files[0].name != PDF_NAME:
        raise RuntimeError("local upload inventory is not reader-first")
    return metadata_payload, {
        "files": rows,
        "metadata_sha256": digest(METADATA),
        "manifest_sha256": digest(MANIFEST),
    }


def anonymous_json(url: str, *, params=None) -> dict:
    response = requests.get(
        url,
        params=params,
        timeout=180,
        headers={"Accept": "application/json", "User-Agent": "Codex-anonymous-lineage-check"},
    )
    if response.status_code != 200:
        raise RuntimeError(f"anonymous Zenodo HTTP {response.status_code}")
    return response.json()


def concept_matches(record: dict) -> bool:
    return str(record.get("conceptrecid")) == CONCEPT_RECORD or record.get("conceptdoi") == CONCEPT_DOI


def resolve_latest_public() -> dict:
    seed = anonymous_json(f"{API}/records/{SEED_RECORD}")
    if not concept_matches(seed):
        raise RuntimeError("seed record is outside the required concept")
    latest_link = seed.get("links", {}).get("latest")
    if latest_link:
        latest = anonymous_json(latest_link)
        if not concept_matches(latest):
            raise RuntimeError("Zenodo latest link escaped the required concept")
        return latest
    search = anonymous_json(
        f"{API}/records",
        params={"q": f"conceptrecid:{CONCEPT_RECORD}", "sort": "mostrecent", "size": 25},
    )
    hits = [hit for hit in search.get("hits", {}).get("hits", []) if concept_matches(hit)]
    if not hits:
        return seed
    return hits[0]


def parse_version(value: str | None) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value or "")
    if not match:
        raise RuntimeError("latest public record has no comparable semantic version")
    return tuple(int(part) for part in match.groups())


def read_token() -> str:
    if not TOKEN_FILE.is_file():
        raise FileNotFoundError(TOKEN_FILE)
    candidates = set()
    for raw_line in TOKEN_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip().strip("`").strip().strip('"').strip("'")
        if not line or line.startswith("#") or line in {"---", "```"}:
            continue
        if ":" in line:
            line = line.split(":", 1)[1].strip().strip("`").strip().strip('"').strip("'")
        if re.fullmatch(r"[A-Za-z0-9._~-]{30,}", line):
            candidates.add(line)
    if len(candidates) != 1:
        raise RuntimeError("Zenodo credential file does not contain one unambiguous token")
    return candidates.pop()


def api_request(session: requests.Session, method: str, url: str, **kwargs) -> requests.Response:
    response = session.request(method, url, timeout=180, **kwargs)
    if response.status_code >= 400:
        raise RuntimeError(f"Zenodo HTTP {response.status_code} for {method}")
    time.sleep(0.35)
    return response


def verify_public(record_id: int, metadata_payload: dict, local: dict) -> tuple[dict, list[dict]]:
    public = None
    for _ in range(40):
        response = requests.get(
            f"{API}/records/{record_id}",
            timeout=180,
            headers={"User-Agent": "Codex-anonymous-readback", "Accept": "application/json"},
        )
        if response.status_code == 200:
            public = response.json()
            break
        time.sleep(2)
    if public is None:
        raise RuntimeError("published Zenodo record did not become anonymously readable")
    if not concept_matches(public):
        raise RuntimeError("published record escaped the existing concept lineage")
    metadata = public.get("metadata", {})
    public_license = metadata.get("license")
    if isinstance(public_license, dict):
        public_license = public_license.get("id")
    expected = metadata_payload["metadata"]
    if metadata.get("title") != expected["title"] or metadata.get("version") != expected["version"] or public_license != "cc-by-4.0":
        raise RuntimeError("public Zenodo metadata drift")
    remote_names = [item.get("key") or item.get("filename") for item in public.get("files", [])]
    local_by_name = {row["filename"]: row for row in local["files"]}
    if set(remote_names) != set(local_by_name):
        raise RuntimeError("public Zenodo inventory does not match the local eight-file release")
    if not remote_names or sorted(remote_names)[0] != PDF_NAME:
        raise RuntimeError("public Zenodo filenames do not sort reader-first")
    remote = {(item.get("key") or item.get("filename")): item for item in public.get("files", [])}
    rows = []
    for name in FILE_NAMES:
        url = remote[name]["links"]["self"]
        response = requests.get(url, timeout=180, headers={"User-Agent": "Codex-anonymous-readback"})
        if response.status_code != 200:
            raise RuntimeError(f"anonymous file readback failed: {name} ({response.status_code})")
        data = response.content
        local_row = local_by_name[name]
        sha256 = hashlib.sha256(data).hexdigest()
        if len(data) != local_row["bytes"] or sha256 != local_row["sha256"]:
            raise RuntimeError(f"anonymous byte/hash readback mismatch: {name}")
        rows.append({"filename": name, "status": response.status_code, "bytes": len(data), "sha256": sha256, "url": url})
    return public, rows


def make_receipt(public: dict, rows: list[dict], metadata_payload: dict, local: dict) -> dict:
    record_id = int(public["id"])
    return {
        "schema_version": "1.0",
        "status": "PUBLISHED_AND_ANONYMOUSLY_VERIFIED",
        "release_id": RELEASE_ID,
        "title": metadata_payload["metadata"]["title"],
        "version": metadata_payload["metadata"]["version"],
        "license": metadata_payload["metadata"]["license"],
        "incomplete_checkpoint": True,
        "scope": "Roberts Notes.tex lines 134-4938, lectures 1-22 of 30; lectures 23-30, Fomberg bridge, and original proof/mastery/lab/capstone closure pending",
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
        "provenance": f"Published by Codex at the user's direction; production note: {MODEL_NOTE}; source author and human direction remain credited.",
        "non_endorsement": "Independent Indonesian edition; no source-author or institutional endorsement is implied.",
    }


def main() -> None:
    metadata_payload, local = verify_local()
    latest = resolve_latest_public()
    latest_metadata = latest.get("metadata", {})
    latest_id = int(latest["id"])
    if latest_metadata.get("title") == TITLE and latest_metadata.get("version") == VERSION:
        public, rows = verify_public(latest_id, metadata_payload, local)
        if TRANSACTION.exists():
            sanitized_transaction = load_json(TRANSACTION)
            sanitized_transaction["anonymous_readback_reproduced"] = True
            save_json(TRANSACTION, sanitized_transaction)
        receipt = make_receipt(public, rows, metadata_payload, local)
        save_json(RECEIPT, receipt)
        print(json.dumps({"status": receipt["status"], "record_id": latest_id, "doi": receipt["doi"], "already_public": True, "files": rows}, ensure_ascii=False, indent=2))
        return
    if not str(latest_metadata.get("title", "")).startswith("Topologi Aljabar: Edisi Bahasa Indonesia"):
        raise RuntimeError("latest concept record is not the expected Indonesian Roberts edition")
    if parse_version(latest_metadata.get("version")) >= parse_version(VERSION):
        raise RuntimeError("latest concept version is not older than the prepared release")

    token = read_token()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/json", "User-Agent": "Codex-O012-publication"})
    token = None

    transaction = load_json(TRANSACTION) if TRANSACTION.exists() else None
    if transaction is not None:
        if transaction.get("release_id") != RELEASE_ID or transaction.get("metadata_sha256") != local["metadata_sha256"] or transaction.get("manifest_sha256") != local["manifest_sha256"]:
            raise RuntimeError("existing Zenodo transaction does not bind this exact release")

    deposition_id = int(transaction["deposition_id"]) if transaction and transaction.get("deposition_id") else None
    parent_id = int(transaction["parent_record_id"]) if transaction and transaction.get("parent_record_id") else latest_id
    if deposition_id is None:
        parent = api_request(session, "GET", f"{API}/deposit/depositions/{parent_id}").json()
        if not concept_matches(parent) or not parent.get("submitted"):
            raise RuntimeError("latest parent deposition is not a published record in the required concept")
        draft = api_request(session, "POST", f"{API}/deposit/depositions/{parent_id}/actions/newversion").json()
        deposition_id = int(draft["id"])
        transaction = {
            "schema_version": "1.0",
            "release_id": RELEASE_ID,
            "deposition_id": deposition_id,
            "parent_record_id": parent_id,
            "concept_key": CONCEPT_RECORD,
            "metadata_sha256": local["metadata_sha256"],
            "manifest_sha256": local["manifest_sha256"],
            "state": "newversion_requested",
        }
        save_json(TRANSACTION, transaction)
    else:
        draft = api_request(session, "GET", f"{API}/deposit/depositions/{deposition_id}").json()

    if not draft.get("submitted"):
        api_request(session, "PUT", f"{API}/deposit/depositions/{deposition_id}", json=metadata_payload)
        draft = api_request(session, "GET", f"{API}/deposit/depositions/{deposition_id}").json()
        bucket = draft.get("links", {}).get("bucket")
        if not bucket:
            raise RuntimeError("Zenodo draft has no bucket URL")
        for file_object in list(draft.get("files", [])):
            file_id = file_object.get("id")
            if not file_id:
                raise RuntimeError("Zenodo draft file lacks a deletion identity")
            api_request(session, "DELETE", f"{API}/deposit/depositions/{deposition_id}/files/{file_id}")
        if api_request(session, "GET", f"{API}/deposit/depositions/{deposition_id}").json().get("files"):
            raise RuntimeError("Zenodo draft did not empty after deleting inherited files")
        for path in local_files():
            upload_url = bucket.rstrip("/") + "/" + quote(path.name)
            with path.open("rb") as stream:
                api_request(session, "PUT", upload_url, data=stream, headers={"Content-Type": "application/octet-stream"})
        draft = api_request(session, "GET", f"{API}/deposit/depositions/{deposition_id}").json()
        draft_names = [item.get("filename") or item.get("key") for item in draft.get("files", [])]
        if set(draft_names) != set(FILE_NAMES):
            raise RuntimeError(f"Zenodo draft inventory mismatch: {sorted(draft_names)}")
        draft_sizes = {item.get("filename") or item.get("key"): int(item.get("filesize") or item.get("size") or 0) for item in draft.get("files", [])}
        local_sizes = {row["filename"]: row["bytes"] for row in local["files"]}
        if draft_sizes != local_sizes:
            raise RuntimeError("Zenodo draft byte-size inventory mismatch")
        transaction["state"] = "draft_verified_publish_requested"
        save_json(TRANSACTION, transaction)
        api_request(session, "POST", f"{API}/deposit/depositions/{deposition_id}/actions/publish")

    public, rows = verify_public(deposition_id, metadata_payload, local)
    transaction.update({
        "state": "published_and_anonymously_verified",
        "record_id": deposition_id,
        "doi": public.get("doi"),
        "concept_doi": public.get("conceptdoi"),
    })
    save_json(TRANSACTION, transaction)
    receipt = make_receipt(public, rows, metadata_payload, local)
    save_json(RECEIPT, receipt)
    print(json.dumps({"status": receipt["status"], "record_id": deposition_id, "doi": public.get("doi"), "concept_doi": public.get("conceptdoi"), "already_public": False, "files": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
