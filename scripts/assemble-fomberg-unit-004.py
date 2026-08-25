#!/usr/bin/env python3
"""Deterministically assemble the two reviewed Unit 004 translation halves."""
from __future__ import annotations

import hashlib
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
PART_A = LANE / "source/id-ID/fomberg/drafts/fomberg-unit-004-part-a.md"
PART_B = LANE / "source/id-ID/fomberg/drafts/fomberg-unit-004-part-b.md"
TARGET = LANE / (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-004-excision-mayer-vietoris-naturality-comparison.md"
)

EXPECTED = {
    PART_A: (50396, "6e390ef9b0d2567c2a7028e84a40b9d0407f7254b224a98109a0fcd87f7bf383"),
    PART_B: (37058, "24383978b2c8cdb9bf14c50250b90125ffcfe250f7062464e85a945ffcce5225"),
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
        for number in range(1, 5):
            old = f"{number:03d}"
            for kind in ("mcheck", "hint", "sol"):
                text = text.replace(
                    f"o012-fom-u004-part-a-{kind}-{old}",
                    f"o012-fom-u004-{kind}-{old}",
                )
            text = text.replace(f"F4A.{number}", f"F4.{number}")
    elif source == "b":
        for number in range(1, 4):
            final_number = number + 4
            for kind in ("mcheck", "hint", "sol"):
                text = text.replace(
                    f"o012-fom-u004b-{kind}-{number:03d}",
                    f"o012-fom-u004-{kind}-{final_number:03d}",
                )
            text = text.replace(f"F4B.{number}", f"F4.{final_number}")
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

a_source_marker = '# Eksisi {#o012-fom-u004-s07 data-source-lines="1923-2440"}'
a_mastery_marker = (
    '## Pemeriksaan penguasaan bagian A '
    '{#o012-fom-u004-part-a-mastery data-origin="edition-original" '
    'data-course-route-unit-id="D60-R11"}'
)
b_mastery_marker = (
    '## Pemeriksaan penguasaan '
    '{#o012-fom-u004b-mastery data-origin="edition-original" '
    'data-course-route-unit-id="D60-R11"}'
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
a_source = "## Eksisi {#o012-fom-u004-s07 data-source-lines=\"1923-2440\"}\n\n" + a_source.lstrip()
a_mastery = before_boundary(a_mastery.lstrip(), "o012-fom-u004-part-a-boundary-001")

b_source, b_mastery = part_b.split(b_mastery_marker, 1)
b_source = b_source.rstrip() + "\n"
b_mastery = before_boundary(b_mastery.lstrip(), "o012-fom-u004b-boundary-001")

a_mastery = normalize_mastery(a_mastery, "a")
b_mastery = normalize_mastery(b_mastery, "b")

front = '''---
title: "Topologi Aljabar"
subtitle: "Komponen Fomberg 4: Eksisi, Mayer–Vietoris, Kealamian, dan Pembandingan Homologi"
author:
  - "Yeheli Fomberg (catatan sumber; berdasarkan kuliah Nir Lazarovich)"
  - "Edisi Bahasa Indonesia dengan perbaikan bukti dan pendamping penguasaan"
date: "25 Agustus 2026"
lang: id-ID
rights: "Sumber dan adaptasi: CC BY-SA 4.0; lihat atribusi dan catatan perubahan di bawah."
source_component: "Fomberg Algebraic Topology, Sections 1.7-1.10"
source_lines: "1923-2846"
edition_unit_id: "O012-FOM-004"
course_route_unit_id: "D60-R11"
status: "terjemahan kontigu dengan perbaikan bukti dan penguasaan lengkap"
---

# Tentang komponen ini {.unnumbered #o012-fom-u004-notice data-course-route-unit-id="D60-R11"}

Komponen ini merupakan terjemahan dan adaptasi bahasa Indonesia atas Bagian
1.7–1.10 *Algebraic Topology* karya Yeheli Fomberg, berdasarkan kuliah Nir
Lazarovich pada musim semi 2025. Otoritas sumber dibekukan pada commit
[563194fae879178b9a6871b249513bfc27968975](https://git.sr.ht/~yp/math-notes/tree/563194fae879178b9a6871b249513bfc27968975/item/algebraic_topology.tex).
Rentang yang diterjemahkan ialah `algebraic_topology.tex` baris 1923–2846:
924 baris fisik, 38.503 byte setelah normalisasi LF dan satu LF penutup,
dengan SHA-256
`ddde995b54154623ccc565117aee63cce8361d2ada1c3c9f2852775b1aaac638`.

Catatan sumber tersedia di bawah
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
Terjemahan, pemformatan semantik, koreksi terbatas, gambar ulang mandiri,
perbaikan bukti, dan materi penguasaan asli di bawah ini diterbitkan dengan
lisensi yang sama. Semua perbaikan FOM-PR-05 sampai FOM-PR-11 dibedakan dari
teks sumber. Tidak ada prosa dari bank soal Fomberg terpisah maupun materi
MIT yang disalin ke dalam komponen ini.

Edisi ini independen dan tidak menyiratkan dukungan, pengesahan, atau
afiliasi dengan Yeheli Fomberg, Nir Lazarovich, ataupun institusi mereka.
Produksi terjemahan, struktur semantik, dan QA dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna.

# Eksisi, Mayer–Vietoris, Kealamian, dan Pembandingan Homologi {#o012-fom-u004 data-source-lines="1923-2846" data-course-route-unit-id="D60-R11"}

'''

mastery_heading = '''## Pemeriksaan penguasaan {#o012-fom-u004-mastery data-origin="edition-original" data-course-route-unit-id="D60-R11"}

Tujuh pemeriksaan berikut membentuk lapisan penguasaan asli edisi. Setiap
soal mempunyai petunjuk dan solusi lengkap; soal-soal ini tidak berasal dari
bank soal Fomberg yang tidak dipilih.

'''

boundary = '''
::: {.boundary #o012-fom-u004-boundary-001}
**Batas sumber komponen.** Unit ini menerjemahkan
`algebraic_topology.tex` baris 1923–2846 secara kontigu, mencakup Bagian
1.7–1.10 tentang eksisi, Mayer–Vietoris, kealamian, serta pembandingan
homologi simpleksial dan singular. Unit ini menutup FOM-PR-05 sampai
FOM-PR-11 dan menyediakan tujuh soal penguasaan dengan petunjuk serta solusi
lengkap. Kursor komponen berikutnya adalah baris 2847,
`\\subsection{Degree maps}`, awal Bagian 1.11.
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

if "part-a" in assembled or "u004b" in assembled or "F4A." in assembled or "F4B." in assembled:
    raise SystemExit("draft-only identifier leaked into canonical assembly")
if "TTP" in assembled or "Translation and Transcription Project" in assembled:
    raise SystemExit("forbidden organization prose leaked into canonical assembly")
if not assembled.endswith("\n") or "\r" in assembled:
    raise SystemExit("assembled newline discipline failed")

TARGET.parent.mkdir(parents=True, exist_ok=True)
TARGET.write_bytes(assembled.encode("utf-8"))
raw = TARGET.read_bytes()
print(
    f"{TARGET.relative_to(LANE).as_posix()}\t{len(raw)} bytes\t"
    f"{raw.count(bytes([10]))} LF lines\t{hashlib.sha256(raw).hexdigest()}"
)
