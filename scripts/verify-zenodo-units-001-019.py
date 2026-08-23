from __future__ import annotations

import hashlib
import json
from pathlib import Path

import requests


LANE = Path(__file__).resolve().parents[1]
RELEASE = LANE / "release" / "zenodo-units-001-019"
ARTIFACTS = RELEASE / "artifacts"
TRANSACTION = RELEASE / "transaction.json"
RECEIPT = LANE / "00_control" / "ZENODO_PUBLICATION_RECEIPT_UNITS_001_019.json"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def main() -> None:
    tx = json.loads(TRANSACTION.read_text(encoding="utf-8"))
    if tx.get("state") != "published_and_anonymously_verified":
        raise RuntimeError("Zenodo transaction is not in its published state")
    local_names = [
        "00_TOPOLOGI_ALJABAR_ID_UNITS_001_019_READER.pdf",
        "README_RELEASE.md",
        "release-manifest.json",
        "RELEASE_RIGHTS.md",
        "SHA256SUMS",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_019_EDITABLE_SOURCE_BACKEND.zip",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_019_QA_PROVENANCE.zip",
        "TOPOLOGI_ALJABAR_ID_UNITS_001_019_READER.html",
    ]
    local = {name: ARTIFACTS / name for name in local_names}
    for path in local.values():
        if not path.is_file():
            raise FileNotFoundError(path)
    record_id = tx["record_id"]
    response = requests.get(f"https://zenodo.org/api/records/{record_id}", timeout=120)
    if response.status_code != 200:
        raise RuntimeError(f"anonymous Zenodo record readback failed: {response.status_code}")
    record = response.json()
    md = record.get("metadata", {})
    if md.get("title") != "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–19" or md.get("version") != "0.19.0" or md.get("license") not in ("cc-by-4.0", {"id": "cc-by-4.0"}):
        raise RuntimeError("public Zenodo metadata does not match this checkpoint")
    public_text = json.dumps(md, ensure_ascii=False)
    if "TTP" in public_text or "Translation and Transcription Project" in public_text:
        raise RuntimeError("forbidden umbrella marker in public Zenodo metadata")
    remote = {f.get("key") or f.get("filename"): f for f in record.get("files", [])}
    if set(remote) != set(local):
        raise RuntimeError(f"public Zenodo inventory mismatch: {sorted(remote)}")
    rows = []
    for name in sorted(local):
        url = remote[name]["links"]["self"]
        r = requests.get(url, timeout=120)
        if r.status_code != 200:
            raise RuntimeError(f"anonymous file readback failed: {name} ({r.status_code})")
        data = r.content
        want = local[name]
        digest = sha_bytes(data)
        if len(data) != want.stat().st_size or digest != sha(want):
            raise RuntimeError(f"public byte/hash mismatch: {name}")
        rows.append({"filename": name, "status": r.status_code, "bytes": len(data), "sha256": digest, "url": url})
    receipt = {
        "schema_version": "1.0",
        "status": "PUBLISHED_AND_ANONYMOUSLY_VERIFIED",
        "release_id": tx["release_id"],
        "title": md["title"],
        "version": md["version"],
        "license": "cc-by-4.0",
        "incomplete_checkpoint": True,
        "scope": "Roberts Notes.tex lines 134-3947, lectures 1-19 of 30; Fomberg bridge and original closure pending",
        "record_id": record_id,
        "doi": record.get("doi"),
        "concept_doi": record.get("conceptdoi"),
        "public_record_url": record.get("links", {}).get("self") or f"https://zenodo.org/records/{record_id}",
        "metadata_sha256": tx["metadata_sha256"],
        "manifest_sha256": tx["manifest_sha256"],
        "files": rows,
        "verification": {"exact_public_inventory": True, "anonymous_byte_readback": True, "all_sha256_match_local": True, "credentials_recorded": False},
        "provenance": f"Published by Codex at the user's direction; production note: {MODEL_NOTE}; source author and human direction remain credited.",
        "non_endorsement": "Independent Indonesian edition; no source-author or institutional endorsement is implied.",
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "record_id": record_id, "doi": record.get("doi"), "concept_doi": record.get("conceptdoi"), "files": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
