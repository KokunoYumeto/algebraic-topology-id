#!/usr/bin/env python3
"""Deterministically assemble the two independently reviewed Unit 005 halves."""
from __future__ import annotations

import hashlib
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
PART_A = LANE / "source/id-ID/fomberg/drafts/fomberg-unit-005-part-a.md"
PART_B = LANE / "source/id-ID/fomberg/drafts/fomberg-unit-005-part-b.md"
TARGET = LANE / (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-005-degree-maps-local-degree.md"
)

EXPECTED = {
    PART_A: (20997, "f895e1558d1e603d9059eca62e0c81905422c359ddabcdedba3cab6185e1d798"),
    PART_B: (19710, "5de4135fe5a293c652182e728cd74a85e177e5b6f1e560f3bd9b6ac8d630f2f8"),
}


def read_frozen(path: Path) -> str:
    raw = path.read_bytes()
    actual = (len(raw), hashlib.sha256(raw).hexdigest())
    if actual != EXPECTED[path]:
        raise SystemExit(f"draft identity mismatch: {path}: {actual}")
    if b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"draft newline discipline failed: {path}")
    return raw.decode("utf-8")


def before_boundary(text: str, boundary_id: str) -> str:
    marker = f"\n::: {{.boundary #{boundary_id}"
    if marker not in text:
        raise SystemExit(f"missing draft boundary: {boundary_id}")
    return text.split(marker, 1)[0].rstrip() + "\n"


def normalize_mastery(text: str, source: str) -> str:
    if source == "a":
        for number in range(1, 4):
            for kind in ("mcheck", "hint", "sol"):
                text = text.replace(
                    f"o012-fom-u005-part-a-{kind}-{number:03d}",
                    f"o012-fom-u005-{kind}-{number:03d}",
                )
            text = text.replace(f"F5A.{number}", f"F5.{number}")
        stale_intro = (
            "Tiga pemeriksaan berikut merupakan lapisan penguasaan asli edisi. Semuanya\n"
            "disusun untuk melengkapi, bukan mengulang, soal-soal Roberts Unit 30. Setiap\n"
            "soal memiliki petunjuk dan solusi lengkap.\n\n"
        )
        if stale_intro not in text:
            raise SystemExit("Part A mastery introduction changed")
        text = text.replace(stale_intro, "")
    elif source == "b":
        for number in range(1, 4):
            final_number = number + 3
            for kind in ("mcheck", "hint", "sol"):
                text = text.replace(
                    f"o012-fom-u005b-{kind}-{number:03d}",
                    f"o012-fom-u005-{kind}-{final_number:03d}",
                )
            text = text.replace(f"F5B.{number}", f"F5.{final_number}")
    else:
        raise ValueError(source)
    return text


part_a = read_frozen(PART_A)
part_b = read_frozen(PART_B)

if not part_a.startswith("---\n"):
    raise SystemExit("Part A front matter missing")
try:
    _, _, part_a_body = part_a.split("---\n", 2)
except ValueError as exc:
    raise SystemExit("Part A front matter malformed") from exc

a_source_marker = (
    '## Derajat pemetaan {#o012-fom-u005-s11a data-origin="source-derived" '
    'data-source-lines="2847-2940"}'
)
a_mastery_marker = (
    '## Pemeriksaan penguasaan '
    '{#o012-fom-u005-part-a-mastery data-origin="edition-original" '
    'data-course-route-unit-id="D60-R12"}'
)
b_mastery_marker = (
    '## Pemeriksaan penguasaan '
    '{#o012-fom-u005b-mastery data-origin="edition-original" '
    'data-course-route-unit-id="D60-R12"}'
)

for marker, text in (
    (a_source_marker, part_a_body),
    (a_mastery_marker, part_a_body),
    (b_mastery_marker, part_b),
):
    if marker not in text:
        raise SystemExit(f"assembly marker missing: {marker}")

a_source = part_a_body.split(a_source_marker, 1)[1]
a_source, a_mastery = a_source.split(a_mastery_marker, 1)
a_source = a_source_marker + "\n\n" + a_source.lstrip()
a_mastery = before_boundary(
    a_mastery.lstrip(), "o012-fom-u005-part-a-boundary-001"
)

b_source, b_mastery = part_b.split(b_mastery_marker, 1)
b_source = b_source.rstrip() + "\n"
b_mastery = before_boundary(
    b_mastery.lstrip(), "o012-fom-u005b-boundary-001"
)

a_mastery = normalize_mastery(a_mastery, "a")
b_mastery = normalize_mastery(b_mastery, "b")

front = '''---
title: "Topologi Aljabar"
subtitle: "Komponen Fomberg 5: Derajat Pemetaan dan Derajat Lokal"
author:
  - "Yeheli Fomberg (catatan sumber; berdasarkan kuliah Nir Lazarovich)"
  - "Edisi Bahasa Indonesia dengan perbaikan bukti dan pendamping penguasaan"
date: "25 Agustus 2026"
lang: id-ID
rights: "Sumber dan adaptasi: CC BY-SA 4.0; lihat atribusi dan catatan perubahan di bawah."
source_component: "Fomberg Algebraic Topology, Section 1.11"
source_lines: "2847-3122"
edition_unit_id: "O012-FOM-005"
course_route_unit_id: "D60-R12"
route_status: "pembandingan derajat opsional; jembatan derajat lokal aditif"
status: "terjemahan kontigu dengan perbaikan bukti dan penguasaan lengkap"
---

# Tentang komponen ini {.unnumbered #o012-fom-u005-notice data-course-route-unit-id="D60-R12"}

Komponen ini merupakan terjemahan dan adaptasi bahasa Indonesia atas Bagian
1.11 *Algebraic Topology* karya Yeheli Fomberg, berdasarkan kuliah Nir
Lazarovich pada musim semi 2025. Otoritas sumber dibekukan pada commit
[563194fae879178b9a6871b249513bfc27968975](https://git.sr.ht/~yp/math-notes/tree/563194fae879178b9a6871b249513bfc27968975/item/algebraic_topology.tex).
Rentang yang diterjemahkan ialah `algebraic_topology.tex` baris 2847–3122:
276 baris fisik, 12.203 byte setelah normalisasi LF dan satu LF penutup,
dengan SHA-256
`9ac1d27872a09134b75bb077ad113716a9e828c2177ac296e7bf3331395da85a`.

Catatan sumber tersedia di bawah
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
Terjemahan, pemformatan semantik, koreksi terbatas, perbaikan bukti FOM-PR-12,
dan materi penguasaan asli di bawah ini diterbitkan dengan lisensi yang sama.
Semua perbaikan dibedakan dari teks sumber. Tidak ada prosa dari bank soal
Fomberg terpisah maupun materi MIT yang disalin ke dalam komponen ini.

Jalur wajib Roberts Unit 30 sudah memuat
[definisi derajat](#o012-rbt-l30-def-002),
[sifat-sifatnya](#o012-rbt-l30-prop-001),
[lema teknis](#o012-rbt-l30-lem-001),
[akibatnya](#o012-rbt-l30-cor-001),
[teorema sfera berbulu](#o012-rbt-l30-thm-003), dan
[buktinya](#o012-rbt-l30-proof-004).
Karena itu, bagian derajat Fomberg dipertahankan sebagai pembandingan opsional;
definisi derajat lokal, rumus lokal-ke-global, dan enam pemeriksaan penguasaan
memberi lapisan aditif. Rujukan teorema dasar aljabar diarahkan ke
[bukti mandiri Roberts](#o012-rbt-l30-proof-002).

Sumber mengulang satu TikZ-CD besar pada definisi dan bukti derajat lokal.
Edisi memecahnya menjadi satu diagram lokal yang dapat direflow dan satu
inventaris peta pusat yang bertipe jelas; tidak ada aset raster baru atau
informasi matematis yang dibuang.

Edisi ini independen dan tidak menyiratkan dukungan, pengesahan, atau
afiliasi dengan Yeheli Fomberg, Nir Lazarovich, ataupun institusi mereka.
Produksi terjemahan, struktur semantik, dan QA dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna.

# Derajat Pemetaan dan Derajat Lokal {#o012-fom-u005 data-source-lines="2847-3122" data-course-route-unit-id="D60-R12"}

'''

mastery_heading = '''## Pemeriksaan penguasaan {#o012-fom-u005-mastery data-origin="edition-original" data-course-route-unit-id="D60-R12"}

Enam pemeriksaan berikut membentuk lapisan penguasaan asli edisi. Setiap soal
mempunyai petunjuk dan solusi lengkap; soal-soal ini tidak berasal dari bank
soal Fomberg yang tidak dipilih.

'''

boundary = '''
::: {.boundary #o012-fom-u005-boundary-001}
**Batas sumber komponen.** Unit ini menerjemahkan
`algebraic_topology.tex` baris 2847–3122 secara kontigu, mencakup Bagian 1.11
tentang derajat pemetaan, teorema sfera berbulu, derajat lokal, rumus
lokal-ke-global, dan pemetaan pangkat pada lingkaran. Unit ini menutup
FOM-PR-12 dan menyediakan enam soal penguasaan dengan petunjuk serta solusi
lengkap. Kursor komponen berikutnya adalah baris 3123,
`\\subsection{Cellular complexes}`, awal Bagian 1.12.
:::
'''

assembled = (
    front
    + a_source.rstrip() + "\n\n"
    + b_source.rstrip() + "\n\n"
    + mastery_heading
    + a_mastery.rstrip() + "\n\n"
    + b_mastery.rstrip() + "\n"
    + boundary
)

for forbidden in (
    "part-a",
    "u005b",
    "F5A.",
    "F5B.",
    "TTP",
    "Translation and Transcription Project",
):
    if forbidden in assembled:
        raise SystemExit(f"forbidden draft or organization string leaked: {forbidden}")
if not assembled.endswith("\n") or "\r" in assembled:
    raise SystemExit("assembled newline discipline failed")

TARGET.parent.mkdir(parents=True, exist_ok=True)
TARGET.write_bytes(assembled.encode("utf-8"))
raw = TARGET.read_bytes()
print(
    f"{TARGET.relative_to(LANE).as_posix()}\t{len(raw)} bytes\t"
    f"{raw.count(bytes([10]))} LF lines\t{hashlib.sha256(raw).hexdigest()}"
)
