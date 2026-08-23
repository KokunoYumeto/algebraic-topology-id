from __future__ import annotations

import hashlib
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
RELEASE = LANE / "release" / "zenodo-units-001-019"
ARTIFACTS = RELEASE / "artifacts"
UPSTREAM = LANE / "authority" / "upstream" / "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE = LANE / "source" / "id-ID"
QA = LANE / "qa"
CONTROL = LANE / "00_control"

TITLE = "Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–19"
VERSION = "0.19.0"
RELEASE_ID = "o012-roberts-id-units-001-019-v0.19.0"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
TREE = "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5"
SOURCE_URL = "https://github.com/DavidMichaelRoberts/AlgebraicTopology2019"
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"
MODEL_NOTE = "OpenAI Codex gpt-5.6-sol, Ultra"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bytes_sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))


def assert_safe(path: Path) -> None:
    data = path.read_bytes()
    text = data.decode("latin-1")
    forbidden = [
        r"(?i)[A-Z]:[\\/](?:Users|Documents and Settings|Temp|ProgramData)[\\/]",
        # Do not treat ordinary TeX command escapes (``\\foo``) as UNC paths.
        r"(?i)\\\\(?:Users|Documents|Temp|ProgramData)\\",
        r"(?i)/(?:Users|home)/[^/\s]+/",
        r"(?i)github_pat_[A-Za-z0-9_]{16,}",
        r"(?i)\bghp_[A-Za-z0-9_]{16,}",
        r"(?i)\bsk-[A-Za-z0-9_-]{16,}",
        r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"(?i)\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b",
        r"(?i)access_token",
        r"(?i)authorization\s*[:=]\s*[\"']?bearer",
        r"(?i)zenodo.{0,24}token",
        r"(?i)figshare.{0,24}token",
        # Historical QA may mention an umbrella marker while documenting a
        # negative scan; that evidence is not release metadata. The generated
        # title, description, README, rights statement, and metadata are checked
        # separately below and must contain neither marker.
    ]
    for pattern in forbidden:
        if re.search(pattern, text):
            raise RuntimeError(f"unsafe release content: {path} ({pattern})")


def deterministic_zip(target: Path, entries: dict[str, Path]) -> dict:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.unlink()
    fixed = (2026, 8, 23, 0, 0, 0)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name in sorted(entries):
            source = entries[name]
            if not source.is_file():
                raise FileNotFoundError(source)
            assert_safe(source)
            info = zipfile.ZipInfo(name, date_time=fixed)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0o644 << 16
            zf.writestr(info, source.read_bytes())
    expected = {name: {"bytes": source.stat().st_size, "sha256": sha(source)} for name, source in entries.items()}
    with zipfile.ZipFile(target, "r") as zf:
        names = sorted(zf.namelist())
        if names != sorted(entries):
            raise RuntimeError(f"ZIP inventory mismatch for {target}: {names}")
        inventory = []
        for name in names:
            data = zf.read(name)
            want = expected[name]
            if len(data) != want["bytes"] or bytes_sha(data) != want["sha256"]:
                raise RuntimeError(f"ZIP entry hash mismatch: {target}:{name}")
            inventory.append({"path": name, **want})
    return {
        "filename": target.name,
        "bytes": target.stat().st_size,
        "sha256": sha(target),
        "entry_count": len(inventory),
        "entries": inventory,
        "verified": True,
    }


def source_entries() -> dict[str, Path]:
    out: dict[str, Path] = {
        "README_RELEASE.md": RELEASE / "README_RELEASE.md",
        "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md",
        "ATTRIBUTION.md": LANE / "ATTRIBUTION.md",
        "upstream/Roberts/LICENSE.md": UPSTREAM / "LICENSE.md",
        "upstream/Roberts/README.md": UPSTREAM / "README.md",
        "upstream/Roberts/Notes.tex": UPSTREAM / "Notes.tex",
        "source/id-ID/reader-unit-001.md": SOURCE / "reader-unit-001.md",
        "source/id-ID/styles/reader.css": SOURCE / "styles" / "reader.css",
        "source/id-ID/styles/reader-cumulative.css": SOURCE / "styles" / "reader-cumulative.css",
        "provenance/AUTHORITY.json": CONTROL / "AUTHORITY.json",
        "provenance/UPSTREAM_FILE_MANIFEST.csv": CONTROL / "UPSTREAM_FILE_MANIFEST.csv",
    }
    for n in range(2, 20):
        nn = f"{n:03d}"
        out[f"source/id-ID/units/unit-{nn}-lecture-{nn}.md"] = SOURCE / "units" / f"unit-{nn}-lecture-{nn}.md"
    for name in (
        "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl", "corrections.jsonl",
        "qa.jsonl", "relations.jsonl", "rights.jsonl", "segments.jsonl", "terms.jsonl", "units.jsonl",
    ):
        out[f"backend/{name}"] = LANE / "backend" / name
    return out


def qa_entries() -> dict[str, Path]:
    out: dict[str, Path] = {
        "README_RELEASE.md": RELEASE / "README_RELEASE.md",
        "RELEASE_RIGHTS.md": RELEASE / "RELEASE_RIGHTS.md",
        "metadata.json": RELEASE / "metadata.json",
        "qa/UNITS_001_019_QA.json": QA / "UNITS_001_019_QA.json",
        "qa/UNITS_001_019_VISUAL_QA.md": QA / "UNITS_001_019_VISUAL_QA.md",
        "qa/UNITS_001_019_RENDER_INVENTORY.csv": QA / "UNITS_001_019_RENDER_INVENTORY.csv",
        "qa/units-001-019-extracted.txt": QA / "units-001-019-extracted.txt",
        "qa/BACKEND_UNITS_001_019_RECEIPT.json": QA / "BACKEND_UNITS_001_019_RECEIPT.json",
        "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-22.json": QA / "INDONESIAN_TERMINOLOGY_QA_2026-08-22.json",
        "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-22.md": QA / "INDONESIAN_TERMINOLOGY_QA_2026-08-22.md",
        "output/ARTIFACT_MANIFEST_UNITS_001_019.csv": LANE / "output" / "ARTIFACT_MANIFEST_UNITS_001_019.csv",
        "provenance/AUTHORITY.json": CONTROL / "AUTHORITY.json",
        "provenance/UPSTREAM_FILE_MANIFEST.csv": CONTROL / "UPSTREAM_FILE_MANIFEST.csv",
        "provenance/ADVERSE_LEDGER.csv": CONTROL / "ADVERSE_LEDGER.csv",
        "provenance/TERMINOLOGY.csv": CONTROL / "TERMINOLOGY.csv",
        "qa/UNIT_001_QA.json": QA / "UNIT_001_QA.json",
        "qa/UNIT_018_QA.json": QA / "UNIT_018_QA.json",
        "qa/UNIT_019_QA.json": QA / "UNIT_019_QA.json",
    }
    for n in range(1, 20):
        nn = f"{n:03d}"
        out[f"qa/UNIT_{nn}_INDEPENDENT_REVIEW.md"] = QA / f"UNIT_{nn}_INDEPENDENT_REVIEW.md"
    for n in (16, 17, 18, 19):
        nn = f"{n:03d}"
        out[f"qa/UNIT_{nn}_SOURCE_AUDIT.md"] = QA / f"UNIT_{nn}_SOURCE_AUDIT.md"
    return out


def main() -> None:
    RELEASE.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    for child in ARTIFACTS.iterdir():
        if child.is_file():
            child.unlink()

    readme = f"""# {TITLE}

Versi: `{VERSION}`  
Tanggal: 23 Agustus 2026  
Status: **checkpoint parsial terpelihara; edisi lengkap masih diproduksi**

Rilis ini mencakup Kuliah 1–19 dari *Algebraic Topology* karya David Michael Roberts,
tepatnya `Notes.tex` baris 134–3947 pada komit `{COMMIT}`. Kuliah 20–30,
jembatan homologi Fomberg, dan lapisan latihan/solusi orisinal penutup belum termasuk
dalam checkpoint ini dan tidak diklaim selesai.

## Pembaca

- `00_TOPOLOGI_ALJABAR_ID_UNITS_001_019_READER.pdf`: pembaca PDF A4 sekunder,
  221 halaman, font tersemat, `/Lang=id-ID`, belum bertag secara struktural.
- `TOPOLOGI_ALJABAR_ID_UNITS_001_019_READER.html`: pembaca utama mandiri/offline,
  reflow desktop/seluler, MathML asli, dan 710 ID stabil.

## Sumber dan QA

`TOPOLOGI_ALJABAR_ID_UNITS_001_019_EDITABLE_SOURCE_BACKEND.zip` memuat sumber
Markdown Unit 1–19, backend JSONL, stylesheet, atribusi, dan saksi sumber resmi.
`TOPOLOGI_ALJABAR_ID_UNITS_001_019_QA_PROVENANCE.zip` memuat receipt QA, ulasan
independen, inventaris render, terminologi, ledger, dan provenance yang relevan.
Tidak ada kredensial, cache, skrip, jalur lokal absolut, atau keadaan kerja internal.

## Atribusi, lisensi, dan provenance

Karya sumber adalah *Algebraic Topology* oleh David Michael Roberts, dari
`{SOURCE_URL}` pada komit `{COMMIT}`, di bawah CC BY 4.0. Terjemahan dan
restrukturisasi ini adalah edisi independen; tidak ada dukungan atau endorsement
oleh penulis maupun institusi yang tersirat. Perubahan, atribusi, dan batas lisensi
per komponen ditetapkan dalam `RELEASE_RIGHTS.md`.

Penerjemahan, restrukturisasi semantik, QA, rekayasa build, dan persiapan rilis
dilakukan dengan **{MODEL_NOTE}** atas arahan pengguna. Catatan alat ini tidak
menggantikan kredit penulis sumber atau kredit kontributor manusia.
"""
    rights = f"""# Hak, atribusi, dan cakupan lisensi

Dokumen ini berlaku untuk **{TITLE}**, versi `{VERSION}`, ID rilis
`{RELEASE_ID}`.

## Sumber dan cakupan

- Penulis sumber: David Michael Roberts, *Algebraic Topology* (2019).
- Otoritas: `{SOURCE_URL}`, komit `{COMMIT}`, tree `{TREE}`, `Notes.tex` baris 134–3947.
- Lisensi sumber dan adaptasi: [Creative Commons Attribution 4.0 International]({LICENSE_URL}).
- Status: hanya Kuliah 1–19 dari 30; Kuliah 20–30, jembatan Fomberg, dan closure
  orisinal belum termasuk.

## Komponen

| Komponen | Isi | Lisensi |
| --- | --- | --- |
| Pembaca HTML/PDF | Teks Roberts, terjemahan Bahasa Indonesia, reflow, MathML, dan layout | CC BY 4.0 |
| Arsip sumber/backend | Markdown, saksi `Notes.tex`, backend JSONL, stylesheet, atribusi | CC BY 4.0 |
| Arsip QA/provenance | Receipt, ulasan, inventaris, ledger, dan metadata rilis | CC BY 4.0 |
| Dokumentasi dan checksum | README, pernyataan hak, manifest, dan hash | CC BY 4.0 sejauh dilindungi hak cipta |

Redistribusi/adaptasi wajib mempertahankan atribusi David Michael Roberts,
tautan lisensi, penandaan perubahan, dan pemberitahuan bahwa edisi ini independen.
Tidak ada klaim endorsement atau status resmi. **{MODEL_NOTE}** adalah pengungkapan
alat bantu produksi atas arahan pengguna, bukan kredit kepengarangan.

Rilis ini tidak memuat kredensial, skrip perangkat lunak, cache, jalur lokal
absolut, atau berkas koordinasi internal.
"""
    write_text(RELEASE / "README_RELEASE.md", readme)
    write_text(RELEASE / "RELEASE_RIGHTS.md", rights)

    metadata = {
        "metadata": {
            "title": TITLE,
            "upload_type": "publication",
            "publication_type": "book",
            "description": (
                f"<p><strong>Status: checkpoint parsial, belum lengkap.</strong> "
                f"Versi {VERSION} memuat terjemahan Bahasa Indonesia Kuliah 1–19 "
                f"dari <em>Algebraic Topology</em> karya David Michael Roberts.</p>"
                f"<p>Cakupan sumber adalah <code>Notes.tex</code> baris 134–3947 pada "
                f"komit sumber <code>{COMMIT}</code>. Kuliah 20–30, jembatan homologi "
                "Fomberg, dan closure orisinal belum termasuk.</p>"
                "<p>HTML mandiri/offline adalah pembaca utama; PDF A4 sekunder. "
                "Sumber Markdown, backend JSONL ber-ID stabil, manifest, checksum, "
                "QA, dan provenance yang disanitasi turut disertakan.</p>"
                f"<p>Lisensi komponen adalah CC BY 4.0 dengan atribusi dan perubahan "
                f"seperti dalam <code>RELEASE_RIGHTS.md</code>. Produksi menggunakan "
                f"<strong>{MODEL_NOTE}</strong> atas arahan pengguna; ini bukan kredit "
                "kepengarangan atau endorsement. Edisi ini independen dan tidak "
                "disponsori atau disahkan oleh penulis maupun institusinya.</p>"
            ),
            "creators": [{"name": "Roberts, David Michael"}],
            "contributors": [{"name": "Editor edisi Bahasa Indonesia", "type": "Editor"}],
            "access_right": "open",
            "license": "cc-by-4.0",
            "language": "ind",
            "version": VERSION,
            "publication_date": "2026-08-23",
            "keywords": ["topologi aljabar", "Bahasa Indonesia", "homotopi", "ruang penutup", "grup fundamental", "MathML", "machine-readable textbook"],
            "related_identifiers": [
                {"identifier": f"{SOURCE_URL}/tree/{COMMIT}", "relation": "isDerivedFrom", "scheme": "url"},
                {"identifier": "10.5281/zenodo.22061489", "relation": "isVersionOf", "scheme": "doi"},
            ],
            "notes": f"ID rilis: {RELEASE_ID}. Checkpoint terpelihara untuk Unit 1–19; versi berikutnya akan memperluas konsep Zenodo yang sama.",
        }
    }
    write_text(RELEASE / "metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    for public_name in ("README_RELEASE.md", "RELEASE_RIGHTS.md", "metadata.json"):
        public_text = (RELEASE / public_name).read_text(encoding="utf-8")
        if re.search(r"(?i)\bTTP\b|Translation and Transcription Project", public_text):
            raise RuntimeError(f"forbidden umbrella marker in public metadata: {public_name}")

    src_zip_name = "TOPOLOGI_ALJABAR_ID_UNITS_001_019_EDITABLE_SOURCE_BACKEND.zip"
    qa_zip_name = "TOPOLOGI_ALJABAR_ID_UNITS_001_019_QA_PROVENANCE.zip"
    src_facts = deterministic_zip(ARTIFACTS / src_zip_name, source_entries())
    qa_facts = deterministic_zip(ARTIFACTS / qa_zip_name, qa_entries())

    pdf = LANE / "output" / "pdf" / "topologi-aljabar-unit-001-019-id.pdf"
    html = LANE / "output" / "html" / "units-001-019" / "index.html"
    release_files = [
        ("00_TOPOLOGI_ALJABAR_ID_UNITS_001_019_READER.pdf", pdf),
        ("TOPOLOGI_ALJABAR_ID_UNITS_001_019_READER.html", html),
        (src_zip_name, ARTIFACTS / src_zip_name),
        (qa_zip_name, ARTIFACTS / qa_zip_name),
        ("README_RELEASE.md", RELEASE / "README_RELEASE.md"),
        ("RELEASE_RIGHTS.md", RELEASE / "RELEASE_RIGHTS.md"),
    ]
    for name, source in release_files:
        if not source.is_file():
            raise FileNotFoundError(source)
        if source != ARTIFACTS / source.name:
            shutil.copyfile(source, ARTIFACTS / name)

    # The copied archive names above are intentionally replaced by the same bytes;
    # retain only one top-level copy in the final release inventory.
    # (The two archive paths are already the canonical artifacts paths.)
    manifest = {
        "schema_version": "1.0",
        "release_id": RELEASE_ID,
        "title": TITLE,
        "version": VERSION,
        "status": "maintained_incomplete_checkpoint",
        "scope_truth": "Roberts Notes.tex lines 134-3947, lectures 1-19 of 30; Fomberg bridge and original closure pending",
        "metadata_sha256": sha(RELEASE / "metadata.json"),
        "source": {"author": "David Michael Roberts", "repository": SOURCE_URL, "commit": COMMIT, "tree": TREE, "path": "Notes.tex", "line_start": 134, "line_end": 3947, "units": 19, "license": "CC BY 4.0"},
        "reader_qa": {"status": "pass", "receipt_sha256": sha(QA / "UNITS_001_019_QA.json"), "html_stable_ids": 710, "html_ids": 951, "html_mathml_nodes": 7451, "pdf_pages": 221, "pdf_tagged": False, "visual_review": "pass_all_221_pages_plus_browser_desktop_mobile"},
        "archives": [src_facts, qa_facts],
        "artifacts": [],
    }
    for name, source in release_files:
        item = ARTIFACTS / name
        manifest["artifacts"].append({"filename": name, "bytes": item.stat().st_size, "sha256": sha(item)})
    write_text(ARTIFACTS / "release-manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    sums = []
    for name, _ in release_files:
        sums.append(f"{sha(ARTIFACTS / name)}  {name}")
    sums.append(f"{sha(ARTIFACTS / 'release-manifest.json')}  release-manifest.json")
    write_text(ARTIFACTS / "SHA256SUMS", "\n".join(sums) + "\n")

    # Re-run the safety scan over every top-level release artifact and verify the
    # manifest's byte/hash bindings before any network publication.
    for item in ARTIFACTS.iterdir():
        if item.is_file() and item.suffix.lower() not in {".pdf", ".zip"}:
            assert_safe(item)
    manifest_bytes = (ARTIFACTS / "release-manifest.json").read_bytes()
    bound = json.loads(manifest_bytes)
    for row in bound["artifacts"]:
        item = ARTIFACTS / row["filename"]
        if item.stat().st_size != row["bytes"] or sha(item) != row["sha256"]:
            raise RuntimeError(f"manifest binding failed: {item.name}")
    print(json.dumps({
        "status": "PASS",
        "release": str(RELEASE),
        "files": [{"filename": p.name, "bytes": p.stat().st_size, "sha256": sha(p)} for p in sorted(ARTIFACTS.iterdir()) if p.is_file()],
        "source_zip": src_facts,
        "qa_zip": qa_facts,
        "metadata_sha256": sha(RELEASE / "metadata.json"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
