from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from urllib.parse import quote

import requests


LANE = Path(__file__).resolve().parents[1]
RELEASE = LANE / "release" / "zenodo-units-001-020"
ARTIFACTS = RELEASE / "artifacts"
METADATA = RELEASE / "metadata.json"
MANIFEST = ARTIFACTS / "release-manifest.json"
TRANSACTION = RELEASE / "transaction.json"
RECEIPT = LANE / "00_control" / "ZENODO_PUBLICATION_RECEIPT_UNITS_001_020.json"
TOKEN_FILE = LANE.parents[3] / "Obsidian notes" / "New zenodo token.md"
API = "https://zenodo.org/api"
PARENT_DEPOSITION = 22070794
CONCEPT = "22061489"
RELEASE_ID = "o012-roberts-id-units-001-020-v0.20.0"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def api_request(session: requests.Session, method: str, url: str, **kwargs) -> requests.Response:
    response = session.request(method, url, timeout=180, **kwargs)
    if response.status_code >= 400:
        raise RuntimeError(f"Zenodo HTTP {response.status_code} for {method} {url}")
    time.sleep(0.35)
    return response


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def local_files() -> list[Path]:
    names = [
        "00_TOPOLOGI_ALJABAR_ID_UNITS_001_020_READER.pdf",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_020_READER.html",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_020_EDITABLE_SOURCE_BACKEND.zip",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_020_QA_PROVENANCE.zip",
        "README_RELEASE.md",
        "RELEASE_RIGHTS.md",
        "release-manifest.json",
        "SHA256SUMS",
    ]
    paths = [ARTIFACTS / name for name in names]
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
    return paths


def verify_local() -> tuple[dict, dict]:
    metadata = load_json(METADATA)
    manifest = load_json(MANIFEST)
    md = metadata["metadata"]
    if md["title"] != "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–20":
        raise RuntimeError("metadata title mismatch")
    if md["version"] != "0.20.0" or md["license"] != "cc-by-4.0" or md["language"] != "ind":
        raise RuntimeError("metadata identity/license/language mismatch")
    public_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (METADATA, RELEASE / "README_RELEASE.md", RELEASE / "RELEASE_RIGHTS.md", MANIFEST)
    )
    if "TTP" in public_text or "Translation and Transcription Project" in public_text:
        raise RuntimeError("forbidden umbrella marker in Zenodo public metadata")
    if "Kuliah 21–30" not in public_text or "belum" not in public_text:
        raise RuntimeError("partial-scope language is missing")
    if MODEL_NOTE not in public_text:
        raise RuntimeError("required model provenance is missing")
    if manifest.get("status") != "incomplete_checkpoint":
        raise RuntimeError("release manifest has a stale publication-state claim")
    if manifest.get("publication_lineage", {}).get("existing_concept_doi") != "10.5281/zenodo.22061489":
        raise RuntimeError("release manifest does not preserve the concept lineage")
    files = local_files()
    rows = [{"filename": path.name, "bytes": path.stat().st_size, "sha256": digest(path)} for path in files]
    expected = {
        "00_TOPOLOGI_ALJABAR_ID_UNITS_001_020_READER.pdf",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_020_READER.html",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_020_EDITABLE_SOURCE_BACKEND.zip",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_020_QA_PROVENANCE.zip",
        "README_RELEASE.md",
        "RELEASE_RIGHTS.md",
    }
    if {row["filename"] for row in manifest["artifacts"]} != expected:
        raise RuntimeError("manifest substantive inventory mismatch")
    sums = {}
    for line in (ARTIFACTS / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        checksum, name = line.split("  ", 1)
        sums[name] = checksum
    expected_sums = {path.name: digest(path) for path in files if path.name != "SHA256SUMS"}
    if sums != expected_sums:
        raise RuntimeError("SHA256SUMS does not bind the seven preceding release files")
    return metadata, {"files": rows, "metadata_sha256": digest(METADATA), "manifest_sha256": digest(MANIFEST)}


def verify_public(deposition_id: int, metadata: dict, local: dict) -> tuple[dict, list[dict]]:
    public = None
    for _ in range(40):
        response = requests.get(f"{API}/records/{deposition_id}", timeout=180, headers={"User-Agent": "Codex-anonymous-readback"})
        if response.status_code == 200:
            public = response.json()
            break
        time.sleep(2)
    if public is None:
        raise RuntimeError("published Zenodo record did not become anonymously readable")
    md = public.get("metadata", {})
    public_license = md.get("license")
    if isinstance(public_license, dict):
        public_license = public_license.get("id")
    if md.get("title") != metadata["metadata"]["title"] or md.get("version") != metadata["metadata"]["version"] or public_license != "cc-by-4.0":
        raise RuntimeError("public Zenodo metadata drift")
    if str(public.get("conceptrecid")) != CONCEPT and public.get("conceptdoi") != "10.5281/zenodo.22061489":
        raise RuntimeError("published record escaped the existing concept lineage")
    remote = {item.get("key") or item.get("filename"): item for item in public.get("files", [])}
    local_by_name = {row["filename"]: row for row in local["files"]}
    if set(remote) != set(local_by_name):
        raise RuntimeError("public Zenodo inventory does not match the local eight-file release")
    rows = []
    for name in sorted(remote):
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


def main() -> None:
    metadata, local = verify_local()
    if not TOKEN_FILE.is_file():
        raise FileNotFoundError(TOKEN_FILE)
    token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    if len(token) < 30 or any(character.isspace() for character in token):
        raise RuntimeError("Zenodo token file is not one unambiguous token")
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/json", "User-Agent": "Codex-O012-publication"})
    token = None

    transaction = load_json(TRANSACTION) if TRANSACTION.exists() else None
    if transaction is not None:
        if transaction.get("release_id") != RELEASE_ID or transaction.get("metadata_sha256") != local["metadata_sha256"] or transaction.get("manifest_sha256") != local["manifest_sha256"]:
            raise RuntimeError("existing Zenodo transaction does not bind this exact release")

    parent = api_request(session, "GET", f"{API}/deposit/depositions/{PARENT_DEPOSITION}").json()
    if str(parent.get("conceptrecid")) != CONCEPT or parent.get("metadata", {}).get("title") != "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–19":
        raise RuntimeError("latest Zenodo lineage record is not the expected O012 Unit 1–19 checkpoint")

    deposition_id = int(transaction["deposition_id"]) if transaction and transaction.get("deposition_id") else None
    if deposition_id is None:
        draft = api_request(session, "POST", f"{API}/deposit/depositions/{PARENT_DEPOSITION}/actions/newversion").json()
        deposition_id = int(draft["id"])
        transaction = {
            "schema_version": "1.0",
            "release_id": RELEASE_ID,
            "deposition_id": deposition_id,
            "parent_deposition_id": PARENT_DEPOSITION,
            "concept_key": CONCEPT,
            "metadata_sha256": local["metadata_sha256"],
            "manifest_sha256": local["manifest_sha256"],
            "state": "newversion_requested",
        }
        save_json(TRANSACTION, transaction)
    else:
        draft = api_request(session, "GET", f"{API}/deposit/depositions/{deposition_id}").json()

    if not draft.get("submitted"):
        api_request(session, "PUT", f"{API}/deposit/depositions/{deposition_id}", json=metadata)
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
        remote_names = {item.get("filename") or item.get("key") for item in draft.get("files", [])}
        if remote_names != {path.name for path in local_files()}:
            raise RuntimeError(f"Zenodo draft inventory mismatch: {sorted(remote_names)}")
        transaction["state"] = "draft_verified_publish_requested"
        save_json(TRANSACTION, transaction)
        api_request(session, "POST", f"{API}/deposit/depositions/{deposition_id}/actions/publish")

    public, rows = verify_public(deposition_id, metadata, local)
    transaction.update(
        {
            "state": "published_and_anonymously_verified",
            "record_id": deposition_id,
            "doi": public.get("doi"),
            "concept_doi": public.get("conceptdoi"),
        }
    )
    save_json(TRANSACTION, transaction)
    receipt = {
        "schema_version": "1.0",
        "status": "PUBLISHED_AND_ANONYMOUSLY_VERIFIED",
        "release_id": RELEASE_ID,
        "title": metadata["metadata"]["title"],
        "version": metadata["metadata"]["version"],
        "license": metadata["metadata"]["license"],
        "incomplete_checkpoint": True,
        "scope": "Roberts Notes.tex lines 134-4345, lectures 1-20 of 30; line 4346, lectures 21-30, Fomberg bridge, and original closure pending",
        "record_id": deposition_id,
        "doi": public.get("doi"),
        "concept_doi": public.get("conceptdoi"),
        "public_record_url": f"https://zenodo.org/records/{deposition_id}",
        "metadata_sha256": local["metadata_sha256"],
        "manifest_sha256": local["manifest_sha256"],
        "files": rows,
        "verification": {
            "exact_public_inventory": True,
            "anonymous_byte_readback": True,
            "all_sha256_match_local": True,
            "credentials_recorded": False,
        },
        "provenance": f"Published by Codex at the user's direction; production note: {MODEL_NOTE}; source author and human direction remain credited.",
        "non_endorsement": "Independent Indonesian edition; no source-author or institutional endorsement is implied.",
    }
    save_json(RECEIPT, receipt)
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "record_id": deposition_id,
                "doi": public.get("doi"),
                "concept_doi": public.get("conceptdoi"),
                "files": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
