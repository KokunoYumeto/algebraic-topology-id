#!/usr/bin/env python3
"""Prepare and verify the reader-first Units 001–020 Zenodo payload.

This script is deliberately local-only.  It creates no deposition, reads no
credential, makes no network request, and changes no source/backend/control
file.  It writes only under release/zenodo-units-001-020/artifacts.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
RELEASE = LANE / "release" / "zenodo-units-001-020"
ARTIFACTS = RELEASE / "artifacts"
UPSTREAM = LANE / "authority" / "upstream" / "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE = LANE / "source" / "id-ID"
QA = LANE / "qa"
CONTROL = LANE / "00_control"
BACKEND = LANE / "backend"

TITLE = "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–20"
VERSION = "0.20.0"
RELEASE_ID = "o012-roberts-id-units-001-020-v0.20.0"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
TREE = "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5"
CONCEPT_DOI = "10.5281/zenodo.22061489"
PREVIOUS_DOI = "10.5281/zenodo.22070794"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"
TERMINOLOGY_MAX_ID = 289
TERMINOLOGY_FROZEN_BYTES = 28876
TERMINOLOGY_FROZEN_SHA256 = "f5f9749704e02713b3e6748356359760dc71d533f8dd0193708769cd8ecbf107"

PDF_NAME = "00_TOPOLOGI_ALJABAR_ID_UNITS_001_020_READER.pdf"
HTML_NAME = "TOPOLOGI_ALJABAR_ID_UNITS_001_020_READER.html"
SOURCE_ZIP_NAME = "TOPOLOGI_ALJABAR_ID_UNITS_001_020_EDITABLE_SOURCE_BACKEND.zip"
QA_ZIP_NAME = "TOPOLOGI_ALJABAR_ID_UNITS_001_020_QA_PROVENANCE.zip"

BACKEND_NAMES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)

EXPECTED = {
    LANE / "output/pdf/topologi-aljabar-unit-001-020-id.pdf": (1598235, "30fdde6ddfc937df3e93bb59d58e72e593c87262d6a2535214113e5ebab64457"),
    LANE / "output/html/units-001-020/index.html": (3190086, "59cb765f2291fc835ca629c774505303745983baacf5379efc97c49da6205c03"),
    LANE / "output/ARTIFACT_MANIFEST_UNITS_001_020.csv": (249, "d69c37838da4174ebb7dc4576392e813040d7f6ebbe1a13fe1c922e1271672da"),
    SOURCE / "units/unit-020-lecture-020.md": (45786, "ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3"),
    QA / "UNIT_020_QA.json": (3717, "4638ac3e2a01c1f212c2b60133f78f1fdd4a1f9c21a9a4cb12e32ff10ba8653e"),
    QA / "UNITS_001_020_BUILD_RECEIPT.json": (2812, "3c39b5546b2aced0a443c753e69824807c8e2f8c91903fe4eb3cca04741ecef1"),
    QA / "UNITS_001_020_VISUAL_QA.md": (1392, "6a8b4d8e31c4adf38fcf51606542f59366f6c5f58d878df65e49677376bf58f9"),
    QA / "BACKEND_APPEND_ONLY_UNIT_020_FINAL_RECEIPT.md": (2113, "6f64eebb653fadb1dd34f0d802f1bda55d482ce9ac47df2c8a88715a100c26c9"),
    CONTROL / "AUTHORITY.json": (1806, "26762fcd01115450fe2ad650b91af69736af0996a322b38fc1c57e0275351158"),
    UPSTREAM / "Notes.tex": (331447, "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"),
    UPSTREAM / "LICENSE.md": (18696, "2ecfbc56ead071b6a93908f50b59c4186db6d139c8b7d0c56156bb0ad5fad3f5"),
}

EXPECTED_BACKEND = {
    "total_records": 2959,
    "total_bytes": 2738760,
    "bundle_sha256": "7abd10e468c5f8b75853a67fcfb67d09f0470720fa88efcc84f5c3647cbb1fe5",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assert_identity(path: Path, size: int, digest: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.stat().st_size != size or sha(path) != digest:
        raise RuntimeError(f"frozen input mismatch: {path}")


def assert_safe_text(path: Path) -> None:
    assert_safe_bytes(path.read_bytes(), str(path))


def assert_safe_bytes(data: bytes, label: str) -> None:
    text = data.decode("latin-1")
    patterns = (
        r"(?i)[A-Z]:[\\/](?:Users|Documents and Settings|Temp|ProgramData)[\\/]",
        r"(?i)\\\\(?:Users|Documents|Temp|ProgramData)\\",
        r"(?i)/(?:Users|home)/[^/\s]+/",
        r"(?i)github_pat_[A-Za-z0-9_]{16,}",
        r"(?i)\bghp_[A-Za-z0-9_]{16,}",
        r"(?i)\bsk-[A-Za-z0-9_-]{16,}",
        r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"(?i)\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b",
        r"(?i)authorization\s*[:=]\s*[\"']?bearer",
        r"(?i)access_token",
        r"(?i)zenodo.{0,24}token",
        r"(?i)figshare.{0,24}token",
    )
    for pattern in patterns:
        if re.search(pattern, text):
            raise RuntimeError(f"unsafe release content: {label} ({pattern})")


def release_entry_bytes(name: str, source: Path) -> bytes:
    raw = source.read_bytes()
    if name != "controls/TERMINOLOGY.csv":
        return raw
    kept = []
    for index, line in enumerate(raw.splitlines(keepends=True)):
        marker = line.find(b"O012-TERM-")
        if index == 0 or (marker >= 0 and int(line[marker + 10:marker + 14]) <= TERMINOLOGY_MAX_ID):
            kept.append(line)
    frozen = b"".join(kept)
    if len(kept) != TERMINOLOGY_MAX_ID + 1:
        raise RuntimeError("frozen Unit 020 terminology row count mismatch")
    if len(frozen) != TERMINOLOGY_FROZEN_BYTES or sha_bytes(frozen) != TERMINOLOGY_FROZEN_SHA256:
        raise RuntimeError("frozen Unit 020 terminology identity mismatch")
    return frozen


def verify_backend() -> dict[str, object]:
    digest = hashlib.sha256()
    total_bytes = 0
    total_records = 0
    rows = []
    for name in sorted(BACKEND_NAMES):
        path = BACKEND / name
        if not path.is_file():
            raise FileNotFoundError(path)
        raw = path.read_bytes()
        if not raw.endswith(b"\n"):
            raise RuntimeError(f"backend JSONL missing final LF: {path}")
        records = raw.count(b"\n")
        total_records += records
        total_bytes += len(raw)
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(raw)
        rows.append({"filename": name, "records": records, "bytes": len(raw), "sha256": sha_bytes(raw)})
    facts = {"total_records": total_records, "total_bytes": total_bytes, "bundle_sha256": digest.hexdigest()}
    if facts != EXPECTED_BACKEND:
        raise RuntimeError(f"backend boundary mismatch: {facts}")
    return {**facts, "files": rows}


def source_entries() -> dict[str, Path]:
    entries: dict[str, Path] = {
        "ATTRIBUTION.md": LANE / "ATTRIBUTION.md",
        "upstream/Roberts/LICENSE.md": UPSTREAM / "LICENSE.md",
        "upstream/Roberts/README.md": UPSTREAM / "README.md",
        "upstream/Roberts/Notes.tex": UPSTREAM / "Notes.tex",
        "source/id-ID/reader-unit-001.md": SOURCE / "reader-unit-001.md",
        "source/id-ID/styles/reader.css": SOURCE / "styles/reader.css",
        "source/id-ID/styles/reader-cumulative.css": SOURCE / "styles/reader-cumulative.css",
        "controls/AUTHORITY.json": CONTROL / "AUTHORITY.json",
        "controls/UPSTREAM_FILE_MANIFEST.csv": CONTROL / "UPSTREAM_FILE_MANIFEST.csv",
        "controls/TERMINOLOGY.csv": CONTROL / "TERMINOLOGY.csv",
    }
    for number in range(2, 21):
        nn = f"{number:03d}"
        entries[f"source/id-ID/units/unit-{nn}-lecture-{nn}.md"] = SOURCE / "units" / f"unit-{nn}-lecture-{nn}.md"
    for name in BACKEND_NAMES:
        entries[f"backend/{name}"] = BACKEND / name
    return entries


def qa_entries() -> dict[str, Path]:
    return {
        "qa/UNITS_001_019_QA.json": QA / "UNITS_001_019_QA.json",
        "qa/UNITS_001_019_VISUAL_QA.md": QA / "UNITS_001_019_VISUAL_QA.md",
        "qa/UNIT_020_QA.json": QA / "UNIT_020_QA.json",
        "qa/UNIT_020_INDEPENDENT_REVIEW.md": QA / "UNIT_020_INDEPENDENT_REVIEW.md",
        "qa/UNIT_020_SOURCE_AUDIT.md": QA / "UNIT_020_SOURCE_AUDIT.md",
        "qa/UNITS_001_020_BUILD_RECEIPT.json": QA / "UNITS_001_020_BUILD_RECEIPT.json",
        "qa/UNITS_001_020_VISUAL_QA.md": QA / "UNITS_001_020_VISUAL_QA.md",
        "qa/BACKEND_APPEND_ONLY_UNIT_020_FINAL_RECEIPT.md": QA / "BACKEND_APPEND_ONLY_UNIT_020_FINAL_RECEIPT.md",
        "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-23.json": QA / "INDONESIAN_TERMINOLOGY_QA_2026-08-23.json",
        "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-23.md": QA / "INDONESIAN_TERMINOLOGY_QA_2026-08-23.md",
        "output/ARTIFACT_MANIFEST_UNITS_001_020.csv": LANE / "output/ARTIFACT_MANIFEST_UNITS_001_020.csv",
    }


def deterministic_zip(target: Path, entries: dict[str, Path]) -> dict[str, object]:
    expected = {}
    payload = {}
    for name, source in entries.items():
        if not source.is_file():
            raise FileNotFoundError(source)
        data = release_entry_bytes(name, source)
        assert_safe_bytes(data, f"{source} as {name}")
        payload[name] = data
        expected[name] = {"bytes": len(data), "sha256": sha_bytes(data)}
    target.parent.mkdir(parents=True, exist_ok=True)
    fixed_time = (2026, 8, 23, 0, 0, 0)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0o644 << 16
            archive.writestr(info, payload[name])
    inventory = []
    with zipfile.ZipFile(target, "r") as archive:
        if sorted(archive.namelist()) != sorted(entries):
            raise RuntimeError(f"ZIP inventory mismatch: {target}")
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC failure: {target}")
        for name in sorted(entries):
            data = archive.read(name)
            want = expected[name]
            if len(data) != want["bytes"] or sha_bytes(data) != want["sha256"]:
                raise RuntimeError(f"ZIP entry mismatch: {target.name}:{name}")
            inventory.append({"path": name, **want})
    return {
        "filename": target.name,
        "bytes": target.stat().st_size,
        "sha256": sha(target),
        "entry_count": len(inventory),
        "uncompressed_bytes": sum(row["bytes"] for row in inventory),
        "entries": inventory,
        "verified": True,
    }


def write_generated(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main() -> None:
    if not RELEASE.is_dir():
        raise RuntimeError(f"release controls were not created with apply_patch: {RELEASE}")
    for path in (RELEASE / "README_RELEASE.md", RELEASE / "RELEASE_RIGHTS.md", RELEASE / "metadata.json", RELEASE / "publication-plan.json"):
        if not path.is_file():
            raise FileNotFoundError(path)
        assert_safe_text(path)
    public_controls = "\n".join((RELEASE / name).read_text(encoding="utf-8") for name in ("README_RELEASE.md", "RELEASE_RIGHTS.md", "metadata.json"))
    if re.search(r"(?i)\bTTP\b|Translation and Transcription Project", public_controls):
        raise RuntimeError("forbidden umbrella marker in public release controls")

    metadata = json.loads((RELEASE / "metadata.json").read_text(encoding="utf-8"))["metadata"]
    plan = json.loads((RELEASE / "publication-plan.json").read_text(encoding="utf-8"))
    if metadata["title"] != TITLE or metadata["version"] != VERSION or metadata["license"] != "cc-by-4.0":
        raise RuntimeError("metadata title/version/license mismatch")
    if plan["state"] != "prepared_not_published" or plan["existing_concept_doi"] != CONCEPT_DOI or plan["latest_published_doi"] != PREVIOUS_DOI:
        raise RuntimeError("publication plan does not preserve the existing concept lineage")
    if plan["new_concept_allowed"] or plan["new_deposition_created"] or plan["credentials_used"]:
        raise RuntimeError("publication plan claims a forbidden network/deposition action")

    for path, (size, digest) in EXPECTED.items():
        assert_identity(path, size, digest)
    backend_facts = verify_backend()

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    allowed = {PDF_NAME, HTML_NAME, SOURCE_ZIP_NAME, QA_ZIP_NAME, "README_RELEASE.md", "RELEASE_RIGHTS.md", "release-manifest.json", "SHA256SUMS"}
    unexpected = sorted(path.name for path in ARTIFACTS.iterdir() if path.name not in allowed)
    if unexpected:
        raise RuntimeError(f"unexpected artifact(s); refusing to erase: {unexpected}")

    source_zip = deterministic_zip(ARTIFACTS / SOURCE_ZIP_NAME, source_entries())
    qa_zip = deterministic_zip(ARTIFACTS / QA_ZIP_NAME, qa_entries())
    copies = {
        PDF_NAME: LANE / "output/pdf/topologi-aljabar-unit-001-020-id.pdf",
        HTML_NAME: LANE / "output/html/units-001-020/index.html",
        "README_RELEASE.md": RELEASE / "README_RELEASE.md",
        "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md",
    }
    for name, source in copies.items():
        shutil.copyfile(source, ARTIFACTS / name)

    upload_files = [PDF_NAME, HTML_NAME, SOURCE_ZIP_NAME, QA_ZIP_NAME, "README_RELEASE.md", "RELEASE_RIGHTS.md"]
    manifest = {
        "schema_version": "1.0",
        "release_id": RELEASE_ID,
        "title": TITLE,
        "version": VERSION,
        "status": "incomplete_checkpoint",
        "scope_truth": "Roberts Notes.tex lines 134-4345, lectures 1-20 of 30; line 4346 deferred to Unit 21; Fomberg bridge and original closure pending",
        "publication_lineage": {"route": "new_version_in_existing_concept", "existing_concept_doi": CONCEPT_DOI, "previous_version_doi": PREVIOUS_DOI, "new_concept_created": False},
        "metadata_sha256": sha(RELEASE / "metadata.json"),
        "publication_plan_sha256": sha(RELEASE / "publication-plan.json"),
        "source": {"author": "David Michael Roberts", "repository": "https://github.com/DavidMichaelRoberts/AlgebraicTopology2019", "commit": COMMIT, "tree": TREE, "path": "Notes.tex", "line_start": 134, "line_end": 4345, "units": 20, "license": "CC BY 4.0"},
        "reader_qa": {"status": "pass", "pdf_pages": 237, "pdf_tagged": False, "html_unique_dom_ids": 1030, "html_mathml_nodes": 7944, "unit_020_stable_ids": 73, "visual_review": "representative_pages_pass"},
        "backend": backend_facts,
        "archives": [source_zip, qa_zip],
        "artifacts": [],
        "privacy": {"credential_material": False, "absolute_local_paths": False, "cache_or_temp_render_payload": False, "raw_coordination_dump": False},
        "production_provenance": MODEL_NOTE,
    }
    for name in upload_files:
        path = ARTIFACTS / name
        manifest["artifacts"].append({"filename": name, "bytes": path.stat().st_size, "sha256": sha(path)})
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    write_generated(ARTIFACTS / "release-manifest.json", manifest_bytes)

    checksum_names = upload_files + ["release-manifest.json"]
    sums = "\n".join(f"{sha(ARTIFACTS / name)}  {name}" for name in checksum_names) + "\n"
    write_generated(ARTIFACTS / "SHA256SUMS", sums.encode("utf-8"))

    actual_names = sorted(path.name for path in ARTIFACTS.iterdir() if path.is_file())
    if actual_names != sorted(allowed):
        raise RuntimeError(f"final payload inventory mismatch: {actual_names}")
    for name in actual_names:
        path = ARTIFACTS / name
        if path.suffix.lower() not in {".pdf", ".zip"}:
            assert_safe_text(path)
    for row in manifest["artifacts"]:
        path = ARTIFACTS / row["filename"]
        if path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
            raise RuntimeError(f"manifest binding failure: {path.name}")
    parsed_sums = {}
    for line in (ARTIFACTS / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        parsed_sums[name] = digest
    if parsed_sums != {name: sha(ARTIFACTS / name) for name in checksum_names}:
        raise RuntimeError("SHA256SUMS binding failure")

    print(json.dumps({
        "status": "PASS_PREPARED_NOT_PUBLISHED",
        "release_directory": str(RELEASE),
        "metadata": {"path": str(RELEASE / "metadata.json"), "bytes": (RELEASE / "metadata.json").stat().st_size, "sha256": sha(RELEASE / "metadata.json")},
        "publication_plan": {"path": str(RELEASE / "publication-plan.json"), "bytes": (RELEASE / "publication-plan.json").stat().st_size, "sha256": sha(RELEASE / "publication-plan.json")},
        "files": [{"filename": name, "bytes": (ARTIFACTS / name).stat().st_size, "sha256": sha(ARTIFACTS / name)} for name in actual_names],
        "total_payload_bytes": sum((ARTIFACTS / name).stat().st_size for name in actual_names),
        "source_zip": {key: value for key, value in source_zip.items() if key != "entries"},
        "qa_zip": {key: value for key, value in qa_zip.items() if key != "entries"},
        "backend": {key: value for key, value in backend_facts.items() if key != "files"},
        "network_actions": 0,
        "credentials_used": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
