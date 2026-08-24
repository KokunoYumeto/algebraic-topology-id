#!/usr/bin/env python3
"""Prepare and verify the reader-first Units 001-024 Zenodo payload.

This script is deliberately local-only. It creates no deposition, reads no
credential, makes no network request, and changes no source/backend/control
file. It writes only under release/zenodo-units-001-024/artifacts.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
RELEASE = LANE / "release" / "zenodo-units-001-024"
ARTIFACTS = RELEASE / "artifacts"
UPSTREAM = LANE / "authority" / "upstream" / "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE = LANE / "source" / "id-ID"
QA = LANE / "qa"
CONTROL = LANE / "00_control"
BACKEND = LANE / "backend"

TITLE = "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–24"
VERSION = "0.24.0"
RELEASE_ID = "o012-roberts-id-units-001-024-v0.24.0"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
TREE = "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5"
CONCEPT_DOI = "10.5281/zenodo.22061489"
PREVIOUS_DOI = "10.5281/zenodo.22072347"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"

PDF_NAME = "00_TOPOLOGI_ALJABAR_ID_UNITS_001_024_READER.pdf"
HTML_NAME = "TOPOLOGI_ALJABAR_ID_UNITS_001_024_READER.html"
SOURCE_ZIP_NAME = "TOPOLOGI_ALJABAR_ID_UNITS_001_024_EDITABLE_SOURCE_BACKEND.zip"
QA_ZIP_NAME = "TOPOLOGI_ALJABAR_ID_UNITS_001_024_QA_PROVENANCE.zip"

BACKEND_NAMES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)

FROZEN_INPUTS = {
    LANE / "output/pdf/topologi-aljabar-unit-001-024-id.pdf": (1907368, "5189b04f2f28d7e8192c16e8ef070e23bbf98085d150d1f2124d15c071ccf9b8"),
    LANE / "output/html/units-001-024/index.html": (3927104, "28a84406de9e196070965920a7f7937177197977f9ddf118f0f8b07d464cbf0f"),
    LANE / "output/ARTIFACT_MANIFEST_UNITS_001_024.csv": (249, "23d2b33dd8eb08ba82bb020e3607abbf24925d79e774ca177be228656800a0ff"),
    LANE / "scripts/build-units-001-024.ps1": (21976, "8e62da597b783f56e0a9174a7822ee453de6de8be01fc5493cb2ab93c41a3c44"),
    LANE / "scripts/qa-unit-023.py": (36367, "54f03a9546c5db116fc68e2c9ada6d208a5850d8975ff571e9cc6fb08f8fd1dc"),
    LANE / "scripts/qa-unit-024.py": (21663, "6b8711eb783e356b9dea1ccfad8ed9c6dcea0238639f9b733a94121cf9f9b552"),
    CONTROL / "AUTHORITY.json": (1806, "26762fcd01115450fe2ad650b91af69736af0996a322b38fc1c57e0275351158"),
    CONTROL / "UPSTREAM_FILE_MANIFEST.csv": (613, "3a88ce28e8d0d1062f2c32ff77506fb53fa590eec90b4fbf80fc3d70fa64e1af"),
    CONTROL / "TERMINOLOGY.csv": (34734, "7c93504218d0d352a2c03f8836bdc5b7e4c824d385b04416db84c16f712ae8b1"),
    LANE / "ATTRIBUTION.md": (1498, "1e4cdbfe1639ac28d47a06b0d054cfc806477ba7173d935b2a52a9b531e87b71"),
    UPSTREAM / "Notes.tex": (331447, "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"),
    UPSTREAM / "LICENSE.md": (18696, "2ecfbc56ead071b6a93908f50b59c4186db6d139c8b7d0c56156bb0ad5fad3f5"),
    UPSTREAM / "README.md": (696, "56f1aab6ad14c6b2f3bba4f16471183c8e43c66c40678d80a2f78efc196f5726"),
    SOURCE / "styles/reader.css": (1297, "e5184827600116bc54e28df6822c5a98691d5edf88b7b102443b56024733cbe5"),
    SOURCE / "styles/reader-cumulative.css": (203, "b0012d9f93e603997d48d49705ec9ccae2d3cd2d062b8b9f8717e908df1f5344"),
    QA / "UNIT_023_QA.json": (6412, "f4a156b709158e9a6312d0fe604b7ab7c60a70d7f7c6fb1423014df4d49f820b"),
    QA / "UNIT_023_INDEPENDENT_REVIEW.md": (3149, "dce8f82872186285c85a42b61b1bbf8fb9fd8e809eea5bccd6367dc87958c880"),
    QA / "UNIT_023_SOURCE_AUDIT.md": (5254, "4777f7c14d35e5fb977955818ff7ab133ecc91adb3575867f0e97f8ff00d28b3"),
    QA / "UNIT_024_QA.json": (6556, "dad49400f3f19367cbcab119fcdeb95e6365e5995f2403c32881ddc35bfaff99"),
    QA / "UNIT_024_INDEPENDENT_REVIEW.md": (5570, "d06dc4a2d76eabbb8f4c115fd8f311c81e974415a186f8bff8269d30cb1672b2"),
    QA / "UNIT_024_SOURCE_AUDIT.md": (4384, "0aeb3beae1b52099e97538083ef349590cca62b473ff1455b8c1fdaffbe2ba6b"),
    QA / "UNITS_001_024_BUILD_RECEIPT.json": (7560, "a050b3d282d43033ccdd7565bc6ee301eee6c30014ef6d8b84c5ec490406129a"),
    QA / "UNITS_001_024_VISUAL_QA.md": (4928, "7aff942b47ec489a56923879aee189fc3911e0eded232a511de66aff8ee01a27"),
    QA / "BACKEND_APPEND_ONLY_UNIT_024_CUMULATIVE_RECEIPT.json": (6692, "4f77c57c62eba9b031873898cb073be9c9c3772b472088c4fd8c5ee8cc20648e"),
    QA / "BACKEND_APPEND_ONLY_UNIT_024_CUMULATIVE_RECEIPT.md": (2531, "5c3b7e471d35ea5a417d70f6cec558faf638a07cf4ffd4357ba82d99a5c2c853"),
    QA / "INDONESIAN_TERMINOLOGY_QA_2026-08-23.json": (3802, "52cc8b4da52bccb9db9e7f492412d8235c53e62faaf286e5c65372e0eee54592"),
    QA / "INDONESIAN_TERMINOLOGY_QA_2026-08-23.md": (3956, "00af36c1eea14c5fc56203c76825a198e06ca3b49038b13dec77fc71cdba18c6"),
}

SOURCE_FROZEN = (
    ("reader-unit-001.md", 16179, "dccc7b727695d26d0b425c0eae22db1697cea93e295391fa7685fbca2d011dc7"),
    ("units/unit-002-lecture-002.md", 25090, "9aa5063c167cc0b2bc8a5edbc81cb36995606d5073a1afe22db608609ad29377"),
    ("units/unit-003-lecture-003.md", 25822, "f757bc58ea6f0d0dbe37ebdb2e44da7d3814b32052d8e23a39331d66d1f025b2"),
    ("units/unit-004-lecture-004.md", 24546, "35aa8adfec6f7652f9a9f21f2c6b6656347309f866689a0939d6f0c517974ea3"),
    ("units/unit-005-lecture-005.md", 22662, "9d25dc7cd89c0c9f69841850b03489e742e8dc50c2e68ca405aff593ec128f90"),
    ("units/unit-006-lecture-006.md", 32116, "2276a34177100bc14e3e9f96461f6a7ab3bf27a25f652af4cc2d27493f420c8e"),
    ("units/unit-007-lecture-007.md", 22107, "f93659dd290272ad3d526b74565f7bdc7316c366c09f1efaac599abde4cbc59d"),
    ("units/unit-008-lecture-008.md", 28468, "4b5c579a1891a99ddff89c458f9d653ec03973e0aaa32839c87be5896ab653a8"),
    ("units/unit-009-lecture-009.md", 25524, "c6076a71d38ab54553a0bf5ed42289063044ebcbeb29689df220081e5621a8a1"),
    ("units/unit-010-lecture-010.md", 26448, "ef76aedb378cb8a3d18a20f672082ee976561a877270082968e7df0a1514a8d5"),
    ("units/unit-011-lecture-011.md", 28465, "7acb205dd9f760631f7548208d77470e22cd208849439e2ad2a8eb4b2465b0f8"),
    ("units/unit-012-lecture-012.md", 32850, "b7ba7cad3d12605628693d57d50a41e06f40a6b7da1109752fe05d870b4b28f0"),
    ("units/unit-013-lecture-013.md", 41196, "f3827dc052a70930ad31cc6f9b1a745bf8a17bac31b4f9249cd178b06ac302b6"),
    ("units/unit-014-lecture-014.md", 28488, "da6f18b455d76adafd8b9b648ed7c277958eca95c0b7d76a8bd9895d79ec6677"),
    ("units/unit-015-lecture-015.md", 27725, "e9ab0565ae460236a69c77389b76d32405873156fc451be9cf95c3749e7fe9d1"),
    ("units/unit-016-lecture-016.md", 33919, "31dfc4c3647f7d6a1d398d2123efe1faa82348428df0180eee2a2358572f9054"),
    ("units/unit-017-lecture-017.md", 29933, "47576d7c26a436ba915c276b692e2bc0ead6fae038295fee3a82a50426ed9a96"),
    ("units/unit-018-lecture-018.md", 44415, "9d0564f6a074441332e42755d46d9a0e858189a5ff4d8b5be52b1def12532598"),
    ("units/unit-019-lecture-019.md", 57277, "ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c"),
    ("units/unit-020-lecture-020.md", 45786, "ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3"),
    ("units/unit-021-lecture-021.md", 26237, "47fa3994dc59370fc464e9d150d62512a4602a3cffa5996f1027f93a427e0eec"),
    ("units/unit-022-lecture-022.md", 44066, "0857e51568d77c811d5d79255ac75bfddc87a04b27356ae457d4e66eeffb7d0d"),
    ("units/unit-023-lecture-023.md", 39176, "6f05ddbe6a720109797976c6929b0535f21a38353673cb42d9646a3196f56bd2"),
    ("units/unit-024-lecture-024.md", 43085, "993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647"),
)

EXPECTED_BACKEND = {
    "total_records": 3723,
    "total_bytes": 3726427,
    "bundle_sha256": "ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25",
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
        raise RuntimeError(f"frozen input mismatch: {path.relative_to(LANE)}")


def assert_safe_bytes(data: bytes, label: str, *, allow_generic_privacy_test_markers: bool = False) -> None:
    text = data.decode("latin-1")
    patterns = [
        r"(?i)github_pat_[A-Za-z0-9_]{16,}",
        r"(?i)\bghp_[A-Za-z0-9_]{16,}",
        r"(?i)\bsk-[A-Za-z0-9_-]{16,}",
        r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"(?i)\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b",
        r"(?i)authorization\s*[:=]\s*[\"']?bearer",
    ]
    if not allow_generic_privacy_test_markers:
        patterns.extend((
            r"(?i)[A-Z]:[\\/](?:Users[\\/][^\\/\s\"']+[\\/]|Documents and Settings[\\/][^\\/\s\"']+[\\/]|Temp[\\/]|ProgramData[\\/])",
            r"(?i)\\\\(?:Users|Documents|Temp|ProgramData)\\",
            r"(?i)/(?:Users|home)/[^/\s]+/",
            r"(?i)access_token",
            r"(?i)zenodo.{0,24}token",
            r"(?i)figshare.{0,24}token",
        ))
    for pattern in patterns:
        if re.search(pattern, text):
            raise RuntimeError(f"unsafe release content: {label}")
    local_account_name = Path.home().name
    if len(local_account_name) >= 3 and re.search(rf"(?i)\b{re.escape(local_account_name)}\b", text):
        raise RuntimeError(f"local account name leaked into release content: {label}")


def assert_safe_text(path: Path) -> None:
    assert_safe_bytes(path.read_bytes(), str(path.relative_to(LANE)))


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
            raise RuntimeError(f"backend JSONL missing final LF: {name}")
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
        "scripts/build-units-001-024.ps1": LANE / "scripts/build-units-001-024.ps1",
        "scripts/qa-unit-023.py": LANE / "scripts/qa-unit-023.py",
        "scripts/qa-unit-024.py": LANE / "scripts/qa-unit-024.py",
    }
    for number in range(2, 25):
        nn = f"{number:03d}"
        entries[f"source/id-ID/units/unit-{nn}-lecture-{nn}.md"] = SOURCE / "units" / f"unit-{nn}-lecture-{nn}.md"
    for name in BACKEND_NAMES:
        entries[f"backend/{name}"] = BACKEND / name
    return entries


def qa_entries() -> dict[str, Path]:
    names = (
        "UNIT_023_QA.json", "UNIT_023_INDEPENDENT_REVIEW.md", "UNIT_023_SOURCE_AUDIT.md",
        "UNIT_024_QA.json", "UNIT_024_INDEPENDENT_REVIEW.md", "UNIT_024_SOURCE_AUDIT.md",
        "UNITS_001_024_BUILD_RECEIPT.json", "UNITS_001_024_VISUAL_QA.md",
        "BACKEND_APPEND_ONLY_UNIT_024_CUMULATIVE_RECEIPT.json",
        "BACKEND_APPEND_ONLY_UNIT_024_CUMULATIVE_RECEIPT.md",
        "INDONESIAN_TERMINOLOGY_QA_2026-08-23.json",
        "INDONESIAN_TERMINOLOGY_QA_2026-08-23.md",
    )
    entries = {f"qa/{name}": QA / name for name in names}
    entries["output/ARTIFACT_MANIFEST_UNITS_001_024.csv"] = LANE / "output/ARTIFACT_MANIFEST_UNITS_001_024.csv"
    return entries


def deterministic_zip(target: Path, entries: dict[str, Path]) -> dict[str, object]:
    expected: dict[str, dict[str, object]] = {}
    payload: dict[str, bytes] = {}
    for name, source in entries.items():
        if not source.is_file():
            raise FileNotFoundError(source)
        data = source.read_bytes()
        assert_safe_bytes(
            data,
            f"{source.relative_to(LANE)} as {name}",
            allow_generic_privacy_test_markers=name.startswith("scripts/"),
        )
        payload[name] = data
        expected[name] = {"bytes": len(data), "sha256": sha_bytes(data)}
    target.parent.mkdir(parents=True, exist_ok=True)
    fixed_time = (2026, 8, 24, 0, 0, 0)
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
            raise RuntimeError(f"ZIP inventory mismatch: {target.name}")
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC failure: {target.name}")
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
        "uncompressed_bytes": sum(int(row["bytes"]) for row in inventory),
        "entries": inventory,
        "verified": True,
    }


def write_generated(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main() -> None:
    if not RELEASE.is_dir():
        raise RuntimeError(f"release controls were not created with apply_patch: {RELEASE.name}")
    controls = tuple(RELEASE / name for name in ("README_RELEASE.md", "RELEASE_RIGHTS.md", "metadata.json", "publication-plan.json"))
    for path in controls:
        if not path.is_file():
            raise FileNotFoundError(path)
        assert_safe_text(path)
    public_controls = "\n".join(path.read_text(encoding="utf-8") for path in controls)
    if re.search(r"(?i)\bTTP\b|Translation and Transcription Project", public_controls):
        raise RuntimeError("forbidden umbrella marker in public release controls")

    metadata_payload = json.loads((RELEASE / "metadata.json").read_text(encoding="utf-8"))
    metadata = metadata_payload["metadata"]
    plan = json.loads((RELEASE / "publication-plan.json").read_text(encoding="utf-8"))
    if metadata["title"] != TITLE or metadata["version"] != VERSION or metadata["license"] != "cc-by-4.0" or metadata["language"] != "ind":
        raise RuntimeError("metadata identity/license/language mismatch")
    if not metadata["description"].startswith("<p><strong>Status: checkpoint parsial, belum lengkap.</strong>"):
        raise RuntimeError("metadata description does not lead with exact partial status")
    if metadata["creators"] != [{"name": "Roberts, David Michael"}] or metadata["contributors"] != [{"name": "Editor edisi Bahasa Indonesia", "type": "Editor"}]:
        raise RuntimeError("metadata authorship/contributor controls drifted")
    if plan["state"] != "prepared_not_published" or plan["existing_concept_doi"] != CONCEPT_DOI or plan["current_public_record_id"] != 22072347:
        raise RuntimeError("publication plan does not preserve the existing concept lineage")
    if plan["new_concept_allowed"] or plan["new_deposition_created"] or plan["credentials_used"]:
        raise RuntimeError("publication plan claims a forbidden action")

    for path, (size, digest) in FROZEN_INPUTS.items():
        assert_identity(path, size, digest)
    for relative, size, digest in SOURCE_FROZEN:
        assert_identity(SOURCE / relative, size, digest)
    backend_facts = verify_backend()

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    allowed = {PDF_NAME, HTML_NAME, SOURCE_ZIP_NAME, QA_ZIP_NAME, "README_RELEASE.md", "RELEASE_RIGHTS.md", "release-manifest.json", "SHA256SUMS"}
    unexpected = sorted(path.name for path in ARTIFACTS.iterdir() if path.name not in allowed)
    if unexpected:
        raise RuntimeError(f"unexpected artifact(s); refusing to erase: {unexpected}")

    source_zip = deterministic_zip(ARTIFACTS / SOURCE_ZIP_NAME, source_entries())
    qa_zip = deterministic_zip(ARTIFACTS / QA_ZIP_NAME, qa_entries())
    copies = {
        PDF_NAME: LANE / "output/pdf/topologi-aljabar-unit-001-024-id.pdf",
        HTML_NAME: LANE / "output/html/units-001-024/index.html",
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
        "scope_truth": "Roberts Notes.tex lines 134-5369, lectures 1-24 of 30; line 5370 and lectures 25-30, Fomberg bridge, and original proof/mastery/lab/capstone closure pending",
        "publication_lineage": {"route": "new_version_in_existing_concept", "existing_concept_doi": CONCEPT_DOI, "previous_record_id": 22072347, "previous_version_doi": PREVIOUS_DOI, "new_concept_created": False},
        "metadata_sha256": sha(RELEASE / "metadata.json"),
        "publication_plan_sha256": sha(RELEASE / "publication-plan.json"),
        "source": {"author": "David Michael Roberts", "repository": "https://github.com/DavidMichaelRoberts/AlgebraicTopology2019", "commit": COMMIT, "tree": TREE, "path": "Notes.tex", "line_start": 134, "line_end": 5369, "units": 24, "license": "CC BY 4.0"},
        "reader_qa": {"status": "pass", "pdf_pages": 286, "pdf_tagged": False, "html_unique_dom_ids": 1295, "html_fragment_links": 288, "html_mathml_nodes": 9669, "html_raw_tex_math_fallbacks": 0, "semantic_figures": 60, "unit_024_stable_ids": 60, "visual_review": "every_new_unit_page_plus_title_and_transition_pass"},
        "backend": backend_facts,
        "archives": [source_zip, qa_zip],
        "artifacts": [],
        "privacy": {"credential_material": False, "absolute_local_paths": False, "user_personal_name": False, "cache_or_temp_render_payload": False, "raw_coordination_dump": False},
        "production_provenance": MODEL_NOTE,
    }
    for name in upload_files:
        path = ARTIFACTS / name
        manifest["artifacts"].append({"filename": name, "bytes": path.stat().st_size, "sha256": sha(path)})
    write_generated(ARTIFACTS / "release-manifest.json", (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

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
        "release_directory": "release/zenodo-units-001-024",
        "metadata": {"path": "release/zenodo-units-001-024/metadata.json", "bytes": (RELEASE / "metadata.json").stat().st_size, "sha256": sha(RELEASE / "metadata.json")},
        "publication_plan": {"path": "release/zenodo-units-001-024/publication-plan.json", "bytes": (RELEASE / "publication-plan.json").stat().st_size, "sha256": sha(RELEASE / "publication-plan.json")},
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
