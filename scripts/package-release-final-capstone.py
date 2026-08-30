#!/usr/bin/env python3
"""Seal and package the complete D60 Bahasa Indonesia edition (local only)."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any


SCRIPT = Path(__file__).resolve()
LANE = SCRIPT.parents[1]
PRIOR_SLUG = "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04"
SLUG = PRIOR_SLUG + "-capstone"
TOKEN = "ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_CAPSTONE"
TEMPLATE_PATH = SCRIPT.with_name(f"package-release-{PRIOR_SLUG}.py")
template_raw = TEMPLATE_PATH.read_bytes()
if (len(template_raw), hashlib.sha256(template_raw).hexdigest()) != (
    33229,
    "41a8e52c0465fbfe45ed95803a1b3b49f1da2a9709e70f28f7acf83f4fe07827",
):
    raise RuntimeError("frozen Lab 4 packager identity drift")
spec = importlib.util.spec_from_file_location("o012_lab4_packager", TEMPLATE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load the proved Lab 4 packager")
template = importlib.util.module_from_spec(spec)
spec.loader.exec_module(template)
base = template.base

TITLE = (
    "Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30, "
    "Jembatan Homologi §1.1–1.13, Penguasaan 108/108, "
    "Laboratorium 1–4, dan Capstone D60"
)
VERSION = "0.31.7"
RELEASE_ID = f"o012-composite-id-{SLUG}-v{VERSION}"
CONCEPT_DOI = "10.5281/zenodo.22061489"
PREVIOUS_RECORD_ID = 22_161_294
PREVIOUS_DOI = "10.5281/zenodo.22161294"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
RELEASE = LANE / "release" / f"zenodo-{SLUG}"
ARTIFACTS = RELEASE / "artifacts"
STAGING = RELEASE / ".package-staging"
FROZEN_LEDGER = RELEASE / "frozen-inputs.json"
PACKAGE_RECEIPT = RELEASE / "PACKAGE_PREPARATION_RECEIPT.json"
FROZEN_LEDGER_SHA256 = "ba15bc1ec1ad44fd23a10643806d0582dbb53cc41d2ddfd7c9c3672b1a3ffa3a"

PDF_INPUT = f"output/pdf/topologi-aljabar-{SLUG}-id.pdf"
HTML_INPUT = f"output/html/{SLUG}/index.html"
ARTIFACT_MANIFEST = f"output/ARTIFACT_MANIFEST_{TOKEN}.csv"
BUILD_DRAFT = f"qa/{TOKEN}_BUILD_DRAFT.json"
BUILD_RECEIPT = f"qa/{TOKEN}_BUILD_RECEIPT.json"
VISUAL_QA = "qa/capstone/VISUAL_QA.json"
BROWSER_QA = "qa/capstone/BROWSER_QA.json"
SOURCE = "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md"
PROOF_CENSUS = "qa/PROOF_REPAIR_CENSUS.json"
SEMANTIC_RECEIPT = "qa/BACKEND_CAPSTONE_FINAL_REV3_SEMANTIC_RECEIPT.json"
CUMULATIVE_RECEIPT = "qa/BACKEND_CAPSTONE_FINAL_REV3_CUMULATIVE_RECEIPT.json"
BACKEND_VALIDATION = "qa/BACKEND_CAPSTONE_FINAL_REV3_VALIDATION.json"
SEMANTIC = (8325, 10028356, "8aff3dbc16e4f3552d2a16eecf043a6fe7c783c31200dce29bc8f61374504acb")
FINAL_BACKEND = (8338, 10040043, "8a3ffc9618e56dfce048c41e938aabef4ffbfd3db20a03a4f52f218985230dbb")

PDF_NAME = f"00_TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.pdf"
HTML_NAME = f"TOPOLOGI_ALJABAR_ID_{TOKEN}_READER.html"
SOURCE_ZIP_NAME = f"TOPOLOGI_ALJABAR_ID_{TOKEN}_EDITABLE_SOURCE_BACKEND.zip"
QA_ZIP_NAME = f"TOPOLOGI_ALJABAR_ID_{TOKEN}_QA_PROVENANCE.zip"
SUBSTANTIVE_ORDER = [PDF_NAME, HTML_NAME, SOURCE_ZIP_NAME, QA_ZIP_NAME, "LICENSE.md", "README_RELEASE.md", "RELEASE_RIGHTS.md"]
FILE_NAMES = SUBSTANTIVE_ORDER + ["release-manifest.json", "SHA256SUMS"]
MANIFEST_STATUS = (
    "roberts_complete_fomberg_001_007_complete_mastery_108_complete_"
    "laboratories_001_004_complete_proof_graph_complete_capstone_complete_"
    "composite_course_complete"
)
CONTROL_NAMES = (
    "metadata.json", "publication-plan.json", "README_RELEASE.md",
    "SOURCE_PACKAGE_README.md", "LICENSE.md", "RELEASE_RIGHTS.md",
    "release-manifest.template.json", "SHA256SUMS.template",
    "frozen-inputs.template.json",
)

for name, value in {
    "RELEASE": RELEASE, "ARTIFACTS": ARTIFACTS, "STAGING": STAGING,
    "FROZEN_LEDGER": FROZEN_LEDGER, "PACKAGE_RECEIPT": PACKAGE_RECEIPT,
    "FROZEN_LEDGER_SHA256": FROZEN_LEDGER_SHA256,
}.items():
    setattr(base, name, value)


def lane_path(relative: str) -> Path:
    path = (LANE / relative).resolve()
    if LANE.resolve() not in path.parents:
        raise RuntimeError(f"path escaped lane: {relative}")
    return path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(relative: str) -> dict[str, Any]:
    path = lane_path(relative)
    if not path.is_file() or path.stat().st_size <= 0:
        raise FileNotFoundError(path)
    return {"path": relative, "bytes": path.stat().st_size, "sha256": digest(path)}


def load_json(relative: str) -> dict[str, Any]:
    return json.loads(lane_path(relative).read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def init_controls() -> None:
    if RELEASE.exists():
        raise RuntimeError(f"refusing to overwrite release controls: {RELEASE}")
    RELEASE.mkdir(parents=True)
    organization = "Translation and " + "Transcription Project"
    metadata = {
        "metadata": {
            "upload_type": "publication", "publication_type": "book",
            "title": TITLE, "version": VERSION, "publication_date": "2026-08-29",
            "creators": [{"name": "Roberts, David Michael"}, {"name": "Fomberg, Yeheli"}],
            "contributors": [
                {"name": "Lazarovich, Nir", "type": "Other"},
                {"name": "Editor edisi Bahasa Indonesia", "type": "Editor"},
                {"name": organization, "type": "Other"},
            ],
            "description": (
                "<p><strong>Status: edisi kursus komposit lengkap.</strong> Roberts 30/30, "
                "jembatan homologi Fomberg Bagian 1.1–1.13, penguasaan biasa 84/84, "
                "asesmen kumulatif 24/24, keseluruhan penguasaan berbasis solusi 108/108, "
                "D60-LAB01, D60-LAB02, D60-LAB03, D60-LAB04, empat grafik "
                "perbaikan bukti, dan capstone D60 telah lengkap.</p>"
                "<p>PDF A4 564 halaman adalah berkas pembaca pertama. HTML mandiri/offline "
                "terpusat dan reflowable memakai MathML asli tanpa dependensi runtime. Paket "
                "menyertakan sumber yang dapat diedit, backend JSONL ber-ID stabil, lisensi, "
                "manifest, checksum, QA, dan provenance ringkas.</p>"
                "<p>Cakupan Roberts ialah <code>Notes.tex</code> baris 134–6368 pada komit "
                "<code>b947ad2e9f9e301bfe24590a9db653bc54fa1a53</code>. Cakupan Fomberg ialah "
                "<code>algebraic_topology.tex</code> baris 31–4185 pada komit "
                "<code>563194fae879178b9a6871b249513bfc27968975</code>. Materi penguasaan, "
                "laboratorium, perbaikan, dan capstone yang ditandai adalah materi asli edisi.</p>"
                "<p>Paket terpadu berlisensi <strong>CC BY-SA 4.0</strong>; komponen Roberts "
                "tetap CC BY 4.0, sedangkan komponen Fomberg dan materi asli edisi tetap CC "
                "BY-SA 4.0. Produksi menggunakan <strong>OpenAI Codex gpt-5.6-sol, Ultra</strong> "
                "atas arahan pengguna. Edisi independen ini tidak menyiratkan dukungan atau "
                "pengesahan penulis maupun institusi sumber.</p>"
            ),
            "keywords": [
                "topologi aljabar", "Bahasa Indonesia", "homotopi", "ruang penutup",
                "grup fundamental", "homologi", "kohomologi", "homologi seluler",
                "produk cup", "laboratorium komputasi", "capstone", "MathML",
                "machine-readable textbook",
            ],
            "language": "ind", "license": "cc-by-sa-4.0", "access_right": "open",
            "notes": (
                f"ID rilis: {RELEASE_ID}. Kursus komposit lengkap: Roberts 30/30; "
                "Fomberg O012-FOM-001–007; penguasaan 108/108; D60-LAB01, "
                "D60-LAB02, D60-LAB03, D60-LAB04; "
                "empat grafik perbaikan bukti; capstone D60. Versi ini melanjutkan konsep "
                f"Zenodo {CONCEPT_DOI} dan pendahulu langsung {PREVIOUS_DOI}; tidak membuat konsep pesaing."
            ),
            "related_identifiers": [
                {"identifier": "https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/tree/b947ad2e9f9e301bfe24590a9db653bc54fa1a53", "relation": "isDerivedFrom", "scheme": "url"},
                {"identifier": "https://git.sr.ht/~yp/math-notes/tree/563194fae879178b9a6871b249513bfc27968975", "relation": "isDerivedFrom", "scheme": "url"},
                {"identifier": CONCEPT_DOI, "relation": "isVersionOf", "scheme": "doi"},
                {"identifier": PREVIOUS_DOI, "relation": "isNewVersionOf", "scheme": "doi"},
            ],
        }
    }
    base.write_json(RELEASE / "metadata.json", metadata)
    plan = {
        "schema_version": "1.0", "state": "prepared_not_published",
        "release_id": RELEASE_ID, "version": VERSION,
        "existing_concept_doi": CONCEPT_DOI,
        "current_public_record_id": PREVIOUS_RECORD_ID, "current_public_doi": PREVIOUS_DOI,
        "new_concept_allowed": False, "new_deposition_created": False,
        "credentials_used": False, "publish_not_draft": True,
        "anonymous_byte_readback_required": True,
        "reader_first_filename": PDF_NAME, "metadata_payload": "metadata.json",
        "payload_directory": "artifacts", "artifact_identities_known": True,
        "publication_route": f"create and publish exactly one new version from public record {PREVIOUS_RECORD_ID}",
        "backend_binding": {
            "final_identity_source": CUMULATIVE_RECEIPT, "expected_records": FINAL_BACKEND[0],
            "hardcoded_final_identity": False,
            "verified_snapshot": {"total_records": FINAL_BACKEND[0], "total_bytes": FINAL_BACKEND[1], "bundle_sha256": FINAL_BACKEND[2]},
        },
        "final_reader_artifacts": {
            "pdf": {**identity(PDF_INPUT), "pages": 564},
            "html": identity(HTML_INPUT),
        },
    }
    base.write_json(RELEASE / "publication-plan.json", plan)
    write_text(RELEASE / "README_RELEASE.md", f"""# {TITLE}

Versi: `{VERSION}`  
Tanggal: 29 Agustus 2026  
Status: **edisi kursus komposit lengkap**

Roberts Kuliah 1–30, jembatan homologi Fomberg Bagian 1.1–1.13, penguasaan
108/108, D60-LAB01–04, empat grafik perbaikan bukti, dan capstone D60 telah
lengkap. Capstone memadukan botol Klein, selubung orientasi, grup fundamental,
homologi, kohomologi, derajat, dan batas inferensi melalui enam pasangan
soal–petunjuk–solusi serta rubrik rekonstruksi oral.

## Mulai membaca

1. `{PDF_NAME}` adalah pembaca A4 utama, 564 halaman. Semua font tersemat,
   subset, dan memiliki peta ToUnicode; PDF belum bertag secara struktural.
2. `{HTML_NAME}` adalah permukaan akses mandiri/offline yang terpusat,
   reflowable, dan memakai MathML asli tanpa dependensi runtime.

Arsip sumber memuat sumber Markdown, program/uji laboratorium, backend JSONL
8.338 rekaman, lisensi, build, dan validator. Arsip QA memuat review, sensus
108/108, sensus bukti, replay append-only, inspeksi visual, QA browser, dan
ledger input beku. Produksi menggunakan **{MODEL}** atas arahan pengguna.
Edisi ini independen dan tidak menyiratkan endorsement atau afiliasi resmi.
""")
    write_text(RELEASE / "SOURCE_PACKAGE_README.md", f"""# Paket sumber yang dapat diedit dan backend modular

Paket ini adalah sumber lengkap yang dapat dilanjutkan untuk versi `{VERSION}`.
Ia memuat Roberts 30/30, Fomberg Bagian 1.1–1.13, penguasaan 108/108,
D60-LAB01–04, empat grafik perbaikan bukti, dan capstone D60.

- `source/id-ID/` memuat sumber semantik Bahasa Indonesia.
- `backend/` memuat 8.338 rekaman append-only `curriculum.interop 0.1.0`.
- `scripts/` memuat build, QA, validator, packager, dan penerbit lineage.
- `00_control/` memuat otoritas, hak, terminologi, rute, kursor, dan logbook.
- `authority/upstream/` memuat sumber otoritatif beku dan lisensinya.

Jalankan `python -B scripts/census-proof-repairs-final.py`, lalu
`python -B scripts/build-final-capstone.py`; gunakan receipt visual/browser yang
disertakan sebelum `python -B scripts/finalize-build-final-capstone.py`.
Komponen Roberts tetap CC BY 4.0; komponen Fomberg dan materi asli edisi tetap
CC BY-SA 4.0. Produksi menggunakan **{MODEL}** atas arahan pengguna.
""")
    write_text(RELEASE / "LICENSE.md", f"""# Lisensi paket terpadu

Pembaca dan paket terpadu **{TITLE}**, versi `{VERSION}`, dilisensikan di bawah
**Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**:
<https://creativecommons.org/licenses/by-sa/4.0/legalcode>

Komponen David Michael Roberts tetap **CC BY 4.0**. Komponen Yeheli Fomberg,
berdasarkan kuliah Nir Lazarovich, tetap **CC BY-SA 4.0**. D60-CA01/02/03,
O012-ORIG-HINTS-R01-R06, D60-LAB01–04, perbaikan bukti, capstone D60,
integrasi pembaca, backend, dan artefak edisi berada di bawah **CC BY-SA 4.0**
kecuali berkas yang menyatakan lisensi lain. Atribusi, perubahan, share-alike,
dan non-endorsement lengkap terdapat dalam `RELEASE_RIGHTS.md`.
""")
    write_text(RELEASE / "RELEASE_RIGHTS.md", f"""# Hak, atribusi, dan cakupan lisensi

Dokumen ini berlaku untuk versi `{VERSION}`, ID rilis `{RELEASE_ID}`.

## Komponen sumber

- David Michael Roberts, *Algebraic Topology* (2019), `Notes.tex:134–6368`,
  komit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`, CC BY 4.0.
- Yeheli Fomberg, *Algebraic Topology*, berdasarkan kuliah Nir Lazarovich,
  `algebraic_topology.tex:31–4185`, komit
  `563194fae879178b9a6871b249513bfc27968975`, CC BY-SA 4.0.
- Materi asli edisi: D60-CA01/02/03, 36 petunjuk R01–R06, D60-LAB01–04,
  perbaikan bukti, koneksi, sintesis, dan capstone D60; CC BY-SA 4.0.

Perubahan meliputi terjemahan id-ID, reflow, MathML asli, objek ber-ID stabil,
gambar ulang, koreksi terdokumentasi, solusi, laboratorium, bukti perbaikan, dan
capstone. Redistribusi/adaptasi wajib mempertahankan atribusi, tautan lisensi,
penandaan perubahan, serta share-alike. Edisi independen ini tidak disponsori,
didukung, disahkan, atau berstatus resmi dari penulis maupun institusi sumber.
**{MODEL}** adalah pengungkapan alat produksi atas arahan pengguna, bukan
kredit kepengarangan.
""")
    manifest = {
        "schema_version": "1.0", "template_state": "static_controls_unsealed_generated_fields_unset",
        "release_id": RELEASE_ID, "title": TITLE, "version": VERSION,
        "status": MANIFEST_STATUS,
        "scope_truth": "Roberts 1-30 complete; Fomberg Sections 1.1-1.13 complete; mastery 108/108; Labs 1-4 complete; four proof graphs closed; D60 capstone complete; composite course complete",
        "artifact_order": SUBSTANTIVE_ORDER,
        "component_numbering": {
            "roberts_edition_units": "001-030",
            "fomberg_component_ids": [f"O012-FOM-{number:03d}" for number in range(1, 8)],
            "course_route_unit_ids": [f"D60-R{number:02d}" for number in range(1, 15)],
            "assessment_ids": ["D60-CA01", "D60-CA02", "D60-CA03"],
            "laboratory_ids": [f"D60-LAB{number:02d}" for number in range(1, 5)],
            "capstone_id": "D60-CAPSTONE",
            "original_edition_unit_ids": ["O012-ORIG-CA01", "O012-ORIG-CA02", "O012-ORIG-CA03", "O012-ORIG-HINTS-R01-R06", "O012-ORIG-LAB01", "O012-ORIG-LAB02", "O012-ORIG-LAB03", "O012-ORIG-LAB04", "O012-ORIG-CAPSTONE"],
            "fomberg_is_not_roberts_units_031_037": True,
        },
        "rights": {"integrated_payload": "CC BY-SA 4.0", "roberts_component": "CC BY 4.0", "fomberg_component": "CC BY-SA 4.0", "original_components": "CC BY-SA 4.0", "attribution_preserved": True, "changes_disclosed": True, "share_alike_preserved": True, "non_endorsement_preserved": True},
        "publication_lineage": {"existing_concept_doi": CONCEPT_DOI, "previous_record_id": PREVIOUS_RECORD_ID, "previous_version_doi": PREVIOUS_DOI, "new_concept_created": False, "route": "new_version_in_existing_concept", "publication_performed_by_packager": False},
        "generated_fields": ["metadata_sha256", "publication_plan_sha256", "frozen_input_ledger", "course_closure", "backend", "reader_qa", "archives", "artifacts", "privacy", "production_provenance"],
    }
    base.write_json(RELEASE / "release-manifest.template.json", manifest)
    write_text(RELEASE / "SHA256SUMS.template", "\n".join(f"<sha256>  {name}" for name in SUBSTANTIVE_ORDER + ["release-manifest.json"]))
    base.write_json(RELEASE / "frozen-inputs.template.json", {"schema_version": "1.0", "state": "template_unsealed_do_not_package", "release_id": RELEASE_ID, "instructions": "Seal exact path/bytes/SHA-256 rows after every deterministic final gate passes; never infer identities, overwrite the predecessor release, access credentials, or publish from the packager.", "final_boundary_paths": sorted(final_boundary_paths()), "entries": []})
    verify_controls()
    print(json.dumps({"status": "CONTROLS_INITIALIZED", "release": RELEASE.relative_to(LANE).as_posix()}, indent=2))


def source_entries() -> dict[str, Path]:
    entries = template.source_entries()
    additions = {
        SOURCE,
        "scripts/append-capstone-backend.py", "scripts/merge-capstone.py",
        "scripts/build-final-capstone.py", "scripts/finalize-build-final-capstone.py",
        "scripts/census-proof-repairs-final.py",
        "scripts/prepare-final-capstone-semantic-overlay.py", "scripts/apply-final-capstone-semantic-overlay.py",
        "scripts/prepare-final-capstone-artifact-overlay.py", "scripts/apply-final-capstone-artifact-overlay.py",
        "scripts/prepare-final-capstone-rev3-semantic-overlay.py", "scripts/apply-final-capstone-rev3-semantic-overlay.py",
        "scripts/prepare-final-capstone-rev3-artifact-overlay.py", "scripts/apply-final-capstone-rev3-artifact-overlay.py",
        "scripts/validate-final-capstone-backend.py", "scripts/validate-final-capstone-rev3-backend.py",
        "scripts/package-release-final-capstone.py", "scripts/publish-zenodo-final-capstone.py",
        "scripts/verify-github-final-capstone.py",
    }
    entries.update({relative: lane_path(relative) for relative in additions})
    return entries


def qa_inventory() -> set[str]:
    paths = set(template.qa_inventory())
    paths.update({
        "qa/capstone/STATIC_QA.json", "qa/capstone/INDEPENDENT_MATH_REVIEW.json",
        "qa/capstone/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json", "qa/capstone/QA.json",
        VISUAL_QA, BROWSER_QA, BUILD_DRAFT, BUILD_RECEIPT, PROOF_CENSUS,
        SEMANTIC_RECEIPT, CUMULATIVE_RECEIPT, BACKEND_VALIDATION,
        "qa/capstone-final-rev3-backend-20260829/run-a/RECEIPT.json",
        "qa/capstone-final-rev3-backend-20260829/run-b/RECEIPT.json",
        "qa/capstone-final-rev3-artifacts-backend-20260829/run-a/RECEIPT.json",
        "qa/capstone-final-rev3-artifacts-backend-20260829/run-b/RECEIPT.json",
    })
    paths.update({f"qa/capstone/render-rev3-20260829/page-{page}.png" for page in range(558, 565)})
    return paths


def final_boundary_paths() -> set[str]:
    return {PDF_INPUT, HTML_INPUT, ARTIFACT_MANIFEST, SOURCE, BUILD_RECEIPT, VISUAL_QA, BROWSER_QA, PROOF_CENSUS, SEMANTIC_RECEIPT, CUMULATIVE_RECEIPT, BACKEND_VALIDATION, "qa/ROUTE_MASTERY_CENSUS.json"}


def control_inventory() -> set[str]:
    prefix = RELEASE.relative_to(LANE).as_posix() + "/"
    return {prefix + name for name in CONTROL_NAMES}


def required_paths() -> set[str]:
    paths = final_boundary_paths() | set(qa_inventory()) | control_inventory()
    paths.update(path.relative_to(LANE).as_posix() for path in source_entries().values())
    paths.discard(SCRIPT.relative_to(LANE).as_posix())
    return paths


def backend_identity() -> dict[str, Any]:
    state = hashlib.sha256(); records = 0; byte_count = 0
    for path in sorted((LANE / "backend").glob("*.jsonl"), key=lambda item: item.name):
        raw = path.read_bytes(); records += len(raw.splitlines()); byte_count += len(raw)
        state.update(path.name.encode("utf-8")); state.update(b"\0"); state.update(raw)
    return {"records": records, "bytes": byte_count, "bundle_sha256": state.hexdigest()}


def verify_controls() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    for name in CONTROL_NAMES:
        path = RELEASE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        base.assert_safe_text(path)
    metadata_payload = json.loads((RELEASE / "metadata.json").read_text(encoding="utf-8"))
    metadata = metadata_payload["metadata"]
    expected_people = ([{"name": "Roberts, David Michael"}, {"name": "Fomberg, Yeheli"}], [{"name": "Lazarovich, Nir", "type": "Other"}, {"name": "Editor edisi Bahasa Indonesia", "type": "Editor"}, {"name": "Translation and Transcription Project", "type": "Other"}])
    require = lambda value, message: (_ for _ in ()).throw(RuntimeError(message)) if not value else None
    require(metadata.get("title") == TITLE and metadata.get("version") == VERSION and metadata.get("license") == "cc-by-sa-4.0" and metadata.get("language") == "ind" and metadata.get("access_right") == "open", "metadata identity/rights drift")
    require((metadata.get("creators"), metadata.get("contributors")) == expected_people, "metadata creator/contributor drift")
    prose = "\n".join(str(metadata.get(key, "")) for key in ("title", "description", "notes")) + "\n" + "\n".join(metadata.get("keywords", []))
    require(not re.search(r"(?i)\bTTP\b|Translation and Transcription Project", prose), "organization leaked into prose metadata")
    controls = "\n".join((RELEASE / name).read_text(encoding="utf-8") for name in CONTROL_NAMES)
    require(controls.count("Translation and Transcription Project") == 1, "organization must occur exactly once across controls")
    for marker in ("108/108", "D60-LAB01", "D60-LAB04", "D60-CAPSTONE", "CC BY 4.0", "CC BY-SA 4.0", MODEL):
        require(marker in controls, f"release controls omit marker: {marker}")
    plan = json.loads((RELEASE / "publication-plan.json").read_text(encoding="utf-8"))
    require(plan.get("state") == "prepared_not_published" and plan.get("release_id") == RELEASE_ID and plan.get("version") == VERSION and plan.get("existing_concept_doi") == CONCEPT_DOI and plan.get("current_public_record_id") == PREVIOUS_RECORD_ID and plan.get("current_public_doi") == PREVIOUS_DOI and plan.get("new_concept_allowed") is False and plan.get("publish_not_draft") is True and plan.get("reader_first_filename") == PDF_NAME, "publication plan lineage drift")
    snapshot = plan.get("backend_binding", {}).get("verified_snapshot", {})
    require((snapshot.get("total_records"), snapshot.get("total_bytes"), snapshot.get("bundle_sha256")) == FINAL_BACKEND, "publication plan backend drift")
    for role, relative in (("pdf", PDF_INPUT), ("html", HTML_INPUT)):
        require(plan["final_reader_artifacts"][role]["path"] == relative and base.identity_matches(plan["final_reader_artifacts"][role], lane_path(relative)), f"publication plan reader drift: {role}")
    manifest = json.loads((RELEASE / "release-manifest.template.json").read_text(encoding="utf-8"))
    require(manifest.get("release_id") == RELEASE_ID and manifest.get("version") == VERSION and manifest.get("status") == MANIFEST_STATUS and manifest.get("artifact_order") == SUBSTANTIVE_ORDER and manifest.get("component_numbering", {}).get("capstone_id") == "D60-CAPSTONE", "manifest template drift")
    sums = [line.split("  ", 1)[1] for line in (RELEASE / "SHA256SUMS.template").read_text(encoding="utf-8").splitlines()]
    require(sums == SUBSTANTIVE_ORDER + ["release-manifest.json"], "checksum template drift")
    return metadata_payload, plan, manifest


def verify_final_gates() -> dict[str, Any]:
    if backend_identity() != {"records": FINAL_BACKEND[0], "bytes": FINAL_BACKEND[1], "bundle_sha256": FINAL_BACKEND[2]}:
        raise RuntimeError("live final backend identity drift")
    for relative in ("qa/capstone/STATIC_QA.json", "qa/capstone/INDEPENDENT_MATH_REVIEW.json", "qa/capstone/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json", "qa/capstone/QA.json", VISUAL_QA, BROWSER_QA, BUILD_RECEIPT, PROOF_CENSUS, SEMANTIC_RECEIPT, CUMULATIVE_RECEIPT, BACKEND_VALIDATION):
        if load_json(relative).get("status") != "PASS":
            raise RuntimeError(f"final PASS gate failed: {relative}")
    build = load_json(BUILD_RECEIPT); visual = load_json(VISUAL_QA); browser = load_json(BROWSER_QA)
    if not (base.identity_matches(build["source"], lane_path(SOURCE)) and base.identity_matches(build["pdf"], lane_path(PDF_INPUT)) and base.identity_matches(build["html"], lane_path(HTML_INPUT)) and base.identity_matches(build["manifest"], lane_path(ARTIFACT_MANIFEST)) and build["pdf"].get("pages") == 564 and build.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}):
        raise RuntimeError("final build identity/scope drift")
    if not (visual["pdf"]["sha256"] == build["pdf"]["sha256"] and visual["inspection"]["all_six_capstone_pages_559_564"] == "PASS" and all(base.identity_matches(row, lane_path(row["path"])) for row in visual["render"]["files"])):
        raise RuntimeError("final visual QA drift")
    if not (browser["html"]["sha256"] == build["html"]["sha256"] and browser["desktop"]["document_horizontal_overflow"] is False and browser["mobile"]["document_horizontal_overflow"] is False and browser["structure"]["ids"] == browser["structure"]["unique_ids"] and browser["structure"]["unresolved_fragments"] == 0 and browser["structure"]["external_runtime_assets"] == 0 and browser["console"] == {"errors": 0, "warnings": 0} and all(browser["correction_markers"].values())):
        raise RuntimeError("final browser QA drift")
    proof = load_json(PROOF_CENSUS); cumulative = load_json(CUMULATIVE_RECEIPT); validation = load_json(BACKEND_VALIDATION)
    if not (proof["backend"]["records"], proof["backend"]["bytes"], proof["backend"]["bundle_sha256"]) == SEMANTIC or proof["summary"].get("all_four_graphs_closed") is not True:
        raise RuntimeError("proof census semantic boundary drift")
    if (cumulative["final"]["records"], cumulative["final"]["bytes"], cumulative["final"]["bundle_sha256"]) != FINAL_BACKEND or validation["backend"] != {"records": FINAL_BACKEND[0], "bytes": FINAL_BACKEND[1], "bundle_sha256": FINAL_BACKEND[2]}:
        raise RuntimeError("final backend receipts drift")
    template.INHERITED_VERIFY_ASSESSMENTS()
    return build


def qa_entries() -> dict[str, Path]:
    entries = {relative: lane_path(relative) for relative in sorted(qa_inventory())}
    entries.update({
        "release/frozen-inputs.json": FROZEN_LEDGER,
        "release/frozen-inputs.template.json": RELEASE / "frozen-inputs.template.json",
        "release/release-manifest.template.json": RELEASE / "release-manifest.template.json",
        "release/SHA256SUMS.template": RELEASE / "SHA256SUMS.template",
    })
    return entries


def seal() -> None:
    if FROZEN_LEDGER.exists():
        raise RuntimeError("frozen-inputs.json already exists; refusing to overwrite")
    verify_controls(); verify_final_gates()
    rows = []
    for relative in sorted(required_paths()):
        path = lane_path(relative)
        if not path.is_file():
            raise FileNotFoundError(path)
        base.assert_safe_bytes(path.read_bytes(), relative, allow_generic_privacy_test_markers=relative.startswith("scripts/"))
        rows.append(identity(relative))
    base.write_json(FROZEN_LEDGER, {"schema_version": "1.0", "release_id": RELEASE_ID, "state": "final_inputs_sealed_local_only", "backend": {"records": FINAL_BACKEND[0], "bytes": FINAL_BACKEND[1], "bundle_sha256": FINAL_BACKEND[2]}, "final_boundary_paths": sorted(final_boundary_paths()), "entries": rows})
    print(json.dumps({"status": "SEALED_LEDGER_REQUIRES_APPLY_PATCH_BINDING", **base.identity(FROZEN_LEDGER), "entries": len(rows)}, indent=2))


def verify_zip(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        require = lambda value, message: (_ for _ in ()).throw(RuntimeError(message)) if not value else None
        require(archive.testzip() is None and archive.infolist(), f"ZIP CRC/inventory failed: {path.name}")
        names = [row.filename for row in archive.infolist()]
        require(len(names) == len(set(names)) and not any(name.startswith(("/", "\\")) or ".." in Path(name).parts for name in names), f"unsafe ZIP inventory: {path.name}")


def package() -> None:
    if re.fullmatch(r"[0-9a-f]{64}", FROZEN_LEDGER_SHA256) is None:
        raise RuntimeError("FROZEN_LEDGER_SHA256 must be apply-patch-bound after sealing")
    if ARTIFACTS.exists() or STAGING.exists():
        raise RuntimeError("refusing to overwrite artifacts or stale staging")
    metadata, plan, manifest_template = verify_controls()
    build = verify_final_gates()
    base.required_frozen_paths = required_paths
    base.FROZEN_LEDGER_SHA256 = FROZEN_LEDGER_SHA256
    base.RELEASE_ID = RELEASE_ID
    base.FINAL_BOUNDARY_PATHS = final_boundary_paths()
    frozen = base.load_frozen_inputs()
    source, qa = source_entries(), qa_entries()
    base.assert_source_archive_link_closure(source)
    for entries in (source, qa):
        for path in entries.values():
            if path.resolve() not in {SCRIPT.resolve(), FROZEN_LEDGER.resolve()}:
                relative = path.relative_to(LANE).as_posix()
                if relative not in frozen:
                    raise RuntimeError(f"unfrozen archive input: {relative}")
    STAGING.mkdir(parents=False)
    try:
        source_zip = base.deterministic_zip(STAGING / SOURCE_ZIP_NAME, source)
        qa_zip = base.deterministic_zip(STAGING / QA_ZIP_NAME, qa)
        verify_zip(STAGING / SOURCE_ZIP_NAME); verify_zip(STAGING / QA_ZIP_NAME)
        copies = {PDF_NAME: lane_path(PDF_INPUT), HTML_NAME: lane_path(HTML_INPUT), "LICENSE.md": RELEASE / "LICENSE.md", "README_RELEASE.md": RELEASE / "README_RELEASE.md", "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md"}
        for name, path in copies.items():
            shutil.copyfile(path, STAGING / name)
        manifest = dict(manifest_template); manifest.pop("template_state", None); manifest.pop("generated_fields", None)
        manifest.update({
            "metadata_sha256": digest(RELEASE / "metadata.json"),
            "publication_plan_sha256": digest(RELEASE / "publication-plan.json"),
            "frozen_input_ledger": {**base.identity(FROZEN_LEDGER), "entries": len(frozen)},
            "course_closure": {"ordinary_mastery_items": 84, "cumulative_assessment_items": 24, "total_solution_bearing_items": 108, "total_solution_bearing_items_required": 108, "computation_laboratories_complete": 4, "computation_laboratories_required": 4, "proof_repair_graphs_closed": 4, "capstone_complete": True, "composite_course_complete": True},
            "backend": {"records": FINAL_BACKEND[0], "bytes": FINAL_BACKEND[1], "bundle_sha256": FINAL_BACKEND[2], "semantic_proof_boundary": {"records": SEMANTIC[0], "bytes": SEMANTIC[1], "bundle_sha256": SEMANTIC[2]}, "cumulative_receipt": identity(CUMULATIVE_RECEIPT), "independent_validation": identity(BACKEND_VALIDATION)},
            "reader_qa": {"status": "PASS", "pdf_pages": 564, "pdf_all_fonts_embedded_subset_tounicode": True, "html_self_contained": True, "html_centered_reflow": True, "desktop_mobile_no_page_overflow": True, "capstone_exercises": 6, "capstone_hints": 6, "capstone_complete_solutions": 6},
            "archives": [source_zip, qa_zip], "artifacts": [],
            "privacy": {"credential_material": False, "absolute_local_paths": False, "user_personal_name": False},
            "production_provenance": MODEL,
        })
        for name in SUBSTANTIVE_ORDER:
            path = STAGING / name
            manifest["artifacts"].append({"filename": name, "bytes": path.stat().st_size, "sha256": digest(path)})
        base.write_json(STAGING / "release-manifest.json", manifest)
        sums_names = SUBSTANTIVE_ORDER + ["release-manifest.json"]
        write_text(STAGING / "SHA256SUMS", "\n".join(f"{digest(STAGING / name)}  {name}" for name in sums_names))
        if sorted(path.name for path in STAGING.iterdir()) != sorted(FILE_NAMES):
            raise RuntimeError("staged payload inventory mismatch")
        if sum(path.stat().st_size for path in STAGING.iterdir()) > 500_000_000:
            raise RuntimeError("payload exceeds 500 MB cap")
        STAGING.replace(ARTIFACTS)
    except Exception:
        if STAGING.exists():
            shutil.rmtree(STAGING)
        raise
    files = [{"filename": path.name, "bytes": path.stat().st_size, "sha256": digest(path)} for path in sorted(ARTIFACTS.iterdir())]
    base.write_json(PACKAGE_RECEIPT, {"schema_version": "1.0", "status": "PASS_PREPARED_NOT_PUBLISHED", "release_id": RELEASE_ID, "version": VERSION, "reader_first_filename": PDF_NAME, "scope": "complete composite course: Roberts 30/30; Fomberg 1.1-1.13; mastery 108/108; Labs 1-4; four proof graphs; capstone D60", "frozen_input_ledger": base.identity(FROZEN_LEDGER), "files": files, "file_count": len(files), "total_payload_bytes": sum(row["bytes"] for row in files), "archives": [source_zip, qa_zip], "verification": {"reader_first": True, "zip_crc_and_inventory_pass": True, "deterministic_reader_gates": True, "backend_append_only_and_independently_validated": True, "rights_component_scope_consistent": True, "network_actions": 0, "credentials_used": False, "published": False}})
    print(json.dumps({"status": "PASS_PREPARED_NOT_PUBLISHED", "release_id": RELEASE_ID, "files": files}, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init-controls", action="store_true")
    parser.add_argument("--seal-frozen-inputs", action="store_true")
    parser.add_argument("--list-required-inputs", action="store_true")
    parser.add_argument("--plan", action="store_true")
    args = parser.parse_args()
    if args.init_controls:
        init_controls()
    elif args.seal_frozen_inputs:
        seal()
    elif args.list_required_inputs:
        print("\n".join(sorted(required_paths())))
    elif args.plan:
        print(json.dumps({"status": "PREPARED_SCRIPT_NOT_EXECUTED", "release_id": RELEASE_ID, "version": VERSION, "concept_doi": CONCEPT_DOI, "previous_record_id": PREVIOUS_RECORD_ID, "reader_first_filename": PDF_NAME, "final_backend": {"records": FINAL_BACKEND[0], "bytes": FINAL_BACKEND[1], "bundle_sha256": FINAL_BACKEND[2]}}, indent=2))
    else:
        package()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise
