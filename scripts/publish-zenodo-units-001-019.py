from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from urllib.parse import quote

import requests


LANE = Path(__file__).resolve().parents[1]
RELEASE = LANE / "release" / "zenodo-units-001-019"
ARTIFACTS = RELEASE / "artifacts"
METADATA = RELEASE / "metadata.json"
MANIFEST = ARTIFACTS / "release-manifest.json"
TRANSACTION = RELEASE / "transaction.json"
RECEIPT = LANE / "00_control" / "ZENODO_PUBLICATION_RECEIPT_UNITS_001_019.json"
TOKEN_FILE = LANE.parents[3] / "Obsidian notes" / "New zenodo token.md"
API = "https://zenodo.org/api"
PARENT_DEPOSITION = 22061490
CONCEPT = "22061489"
RELEASE_ID = "o012-roberts-id-units-001-019-v0.19.0"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def request(session: requests.Session, method: str, url: str, **kwargs) -> requests.Response:
    response = session.request(method, url, timeout=120, **kwargs)
    if response.status_code >= 400:
        # Never include headers or credential material in the persisted error.
        raise RuntimeError(f"Zenodo HTTP {response.status_code} for {method} {url}")
    time.sleep(0.35)
    return response


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def local_files() -> list[Path]:
    names = [
        "00_TOPOLOGI_ALJABAR_ID_UNITS_001_019_READER.pdf",
        "README_RELEASE.md",
        "release-manifest.json",
        "RELEASE_RIGHTS.md",
        "SHA256SUMS",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_019_EDITABLE_SOURCE_BACKEND.zip",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_019_QA_PROVENANCE.zip",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_019_READER.html",
    ]
    paths = [ARTIFACTS / n for n in names]
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
    return paths


def verify_local() -> tuple[dict, dict]:
    metadata = load_json(METADATA)
    manifest = load_json(MANIFEST)
    md = metadata["metadata"]
    if md["title"] != "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–19":
        raise RuntimeError("metadata title mismatch")
    if md["version"] != "0.19.0" or md["license"] != "cc-by-4.0" or md["language"] != "ind":
        raise RuntimeError("metadata identity/license/language mismatch")
    public_text = METADATA.read_text(encoding="utf-8") + (RELEASE / "README_RELEASE.md").read_text(encoding="utf-8") + (RELEASE / "RELEASE_RIGHTS.md").read_text(encoding="utf-8")
    if "TTP" in public_text or "Translation and Transcription Project" in public_text:
        raise RuntimeError("forbidden umbrella marker in Zenodo public metadata")
    if "Kuliah 20–30" not in public_text or "belum" not in public_text:
        raise RuntimeError("partial-scope language is missing")
    files = local_files()
    rows = []
    for path in files:
        rows.append({"filename": path.name, "bytes": path.stat().st_size, "sha256": digest(path)})
    manifest_names = {row["filename"] for row in manifest["artifacts"]}
    if manifest_names != {p.name for p in files if p.name not in {"release-manifest.json", "SHA256SUMS"}}:
        # The manifest deliberately covers the six substantive artifacts; the
        # checksum and manifest files are bound by SHA256SUMS and this receipt.
        expected = {"00_TOPOLOGI_ALJABAR_ID_UNITS_001_019_READER.pdf", "TOPOLOGI_ALJABAR_ID_UNITS_001_019_READER.html", "TOPOLOGI_ALJABAR_ID_UNITS_001_019_EDITABLE_SOURCE_BACKEND.zip", "TOPOLOGI_ALJABAR_ID_UNITS_001_019_QA_PROVENANCE.zip", "README_RELEASE.md", "RELEASE_RIGHTS.md"}
        if manifest_names != expected:
            raise RuntimeError("manifest inventory mismatch")
    return metadata, {"files": rows, "metadata_sha256": digest(METADATA), "manifest_sha256": digest(MANIFEST)}


def main() -> None:
    metadata, local = verify_local()
    if not TOKEN_FILE.is_file():
        raise FileNotFoundError(TOKEN_FILE)
    token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    if len(token) < 30 or any(ch.isspace() for ch in token):
        raise RuntimeError("Zenodo token file is not one unambiguous token")
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/json"})
    token = None

    tx = load_json(TRANSACTION) if TRANSACTION.exists() else None
    if tx is not None:
        if tx.get("release_id") != RELEASE_ID or tx.get("metadata_sha256") != local["metadata_sha256"] or tx.get("manifest_sha256") != local["manifest_sha256"]:
            raise RuntimeError("existing Zenodo transaction does not bind this exact release")

    parent = request(session, "GET", f"{API}/deposit/depositions/{PARENT_DEPOSITION}").json()
    if str(parent.get("conceptrecid")) != CONCEPT or parent.get("metadata", {}).get("title") != "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–13":
        raise RuntimeError("existing Zenodo lineage is not the expected O012 concept")

    deposition_id = int(tx["deposition_id"]) if tx and tx.get("deposition_id") else None
    if deposition_id:
        draft = request(session, "GET", f"{API}/deposit/depositions/{deposition_id}").json()
    else:
        response = request(session, "POST", f"{API}/deposit/depositions/{PARENT_DEPOSITION}/actions/newversion")
        draft = response.json()
        deposition_id = int(draft["id"])
        tx = {"schema_version": "1.0", "release_id": RELEASE_ID, "deposition_id": deposition_id, "parent_deposition_id": PARENT_DEPOSITION, "concept_key": CONCEPT, "metadata_sha256": local["metadata_sha256"], "manifest_sha256": local["manifest_sha256"], "state": "newversion_requested"}
        save_json(TRANSACTION, tx)

    if draft.get("submitted"):
        raise RuntimeError("bound deposition is already submitted; inspect before another publication request")
    request(session, "PUT", f"{API}/deposit/depositions/{deposition_id}", json=metadata)
    draft = request(session, "GET", f"{API}/deposit/depositions/{deposition_id}").json()
    bucket = draft.get("links", {}).get("bucket")
    if not bucket:
        raise RuntimeError("Zenodo draft has no bucket URL")

    expected_names = {p.name for p in local_files()}
    # Zenodo's new-version draft inherits the prior version's files. This draft
    # is bound to this lane's persisted transaction, so remove only its inherited
    # files before uploading the exact new eight-file inventory.
    for file_obj in list(draft.get("files", [])):
        file_id = file_obj.get("id")
        if not file_id:
            raise RuntimeError("Zenodo draft file lacks a deletion identity")
        request(session, "DELETE", f"{API}/deposit/depositions/{deposition_id}/files/{file_id}")
    draft = request(session, "GET", f"{API}/deposit/depositions/{deposition_id}").json()
    if draft.get("files"):
        raise RuntimeError("Zenodo draft did not empty after deleting inherited files")
    for path in local_files():
        upload_url = bucket.rstrip("/") + "/" + quote(path.name)
        request(session, "PUT", upload_url, data=path.open("rb"), headers={"Content-Type": "application/octet-stream"})
    draft = request(session, "GET", f"{API}/deposit/depositions/{deposition_id}").json()
    remote_names = {f.get("filename") or f.get("key") for f in draft.get("files", [])}
    if remote_names != expected_names:
        raise RuntimeError(f"Zenodo draft inventory mismatch: {sorted(remote_names)}")
    tx["state"] = "draft_verified_publish_requested"
    save_json(TRANSACTION, tx)
    request(session, "POST", f"{API}/deposit/depositions/{deposition_id}/actions/publish")

    public = None
    for _ in range(30):
        response = requests.get(f"https://zenodo.org/api/records/{deposition_id}", timeout=120)
        if response.status_code == 200:
            public = response.json()
            break
        time.sleep(2)
    if public is None:
        raise RuntimeError("published Zenodo record did not become anonymously readable")
    md = public.get("metadata", {})
    if md.get("title") != metadata["metadata"]["title"] or md.get("version") != metadata["metadata"]["version"] or md.get("license") not in ("cc-by-4.0", {"id": "cc-by-4.0"}):
        raise RuntimeError("public Zenodo metadata drift")
    remote = {f.get("key") or f.get("filename"): f for f in public.get("files", [])}
    local_by_name = {row["filename"]: row for row in local["files"]}
    if set(remote) != set(local_by_name):
        raise RuntimeError("public Zenodo inventory does not match local eight-file release")
    rows = []
    for name in sorted(remote):
        url = remote[name]["links"]["self"]
        response = requests.get(url, timeout=120)
        if response.status_code != 200:
            raise RuntimeError(f"anonymous file readback failed: {name} ({response.status_code})")
        data = response.content
        local_row = local_by_name[name]
        if len(data) != local_row["bytes"] or hashlib.sha256(data).hexdigest() != local_row["sha256"]:
            raise RuntimeError(f"anonymous byte/hash readback mismatch: {name}")
        rows.append({"filename": name, "status": response.status_code, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "url": url})
    tx.update({"state": "published_and_anonymously_verified", "record_id": deposition_id, "doi": public.get("doi"), "concept_doi": public.get("conceptdoi")})
    save_json(TRANSACTION, tx)
    receipt = {
        "schema_version": "1.0",
        "status": "PUBLISHED_AND_ANONYMOUSLY_VERIFIED",
        "release_id": RELEASE_ID,
        "title": metadata["metadata"]["title"],
        "version": metadata["metadata"]["version"],
        "license": metadata["metadata"]["license"],
        "incomplete_checkpoint": True,
        "scope": "Roberts Notes.tex lines 134-3947, lectures 1-19 of 30; Fomberg bridge and original closure pending",
        "record_id": deposition_id,
        "doi": public.get("doi"),
        "concept_doi": public.get("conceptdoi"),
        "public_record_url": public.get("links", {}).get("self") or f"https://zenodo.org/records/{deposition_id}",
        "metadata_sha256": local["metadata_sha256"],
        "manifest_sha256": local["manifest_sha256"],
        "files": rows,
        "verification": {"exact_public_inventory": True, "anonymous_byte_readback": True, "all_sha256_match_local": True, "credentials_recorded": False},
        "provenance": f"Published by Codex at the user's direction; production note: {MODEL_NOTE}; source author and human direction remain credited.",
        "non_endorsement": "Independent Indonesian edition; no source-author or institutional endorsement is implied.",
    }
    save_json(RECEIPT, receipt)
    print(json.dumps({"status": receipt["status"], "record_id": deposition_id, "doi": public.get("doi"), "concept_doi": public.get("conceptdoi"), "files": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
