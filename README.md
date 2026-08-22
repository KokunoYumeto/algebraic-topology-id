# Topologi Aljabar — edisi Bahasa Indonesia

Edisi Bahasa Indonesia yang sedang diproduksi dari *Algebraic Topology* karya David Michael Roberts. Materi sumber dibekukan pada commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53` dan tersedia di bawah [CC BY 4.0](LICENSE.md). Edisi ini bersifat independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

## Baca

- [Pembaca HTML kumulatif Unit 1–7](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-007/) — permukaan utama terbaru yang semantik, mandiri, dan memakai MathML asli; URL akan kembali tersedia setelah akses akun GitHub dipulihkan.
- [PDF kumulatif Unit 1–7](output/pdf/topologi-aljabar-unit-001-007-id.pdf) — permukaan sekunder A4, 66 halaman.
- [Pembaca HTML kumulatif Unit 1–5](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-005/) dan [PDF Unit 1–5](output/pdf/topologi-aljabar-unit-001-005-id.pdf) tetap dipertahankan sebagai batas kelima.
- [Pembaca HTML kumulatif Unit 1–4](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-004/) dan [PDF Unit 1–4](output/pdf/topologi-aljabar-unit-001-004-id.pdf) tetap dipertahankan sebagai batas publikasi keempat.
- [Pembaca HTML kumulatif Unit 1–3](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-003/) dan [PDF Unit 1–3](output/pdf/topologi-aljabar-unit-001-003-id.pdf) tetap dipertahankan sebagai batas publikasi ketiga.
- [Pembaca HTML kumulatif Unit 1–2](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-002/) dan [PDF Unit 1–2](output/pdf/topologi-aljabar-unit-001-002-id.pdf) tetap dipertahankan sebagai batas publikasi kedua.
- [Pembaca HTML Unit 1](https://kokunoyumeto.github.io/algebraic-topology-id/) dan [PDF Unit 1](output/pdf/topologi-aljabar-unit-001-id.pdf) tetap dipertahankan sebagai batas publikasi pertama.
- Sumber semantik: [Unit 1](source/id-ID/reader-unit-001.md), [Unit 2](source/id-ID/units/unit-002-lecture-002.md), [Unit 3](source/id-ID/units/unit-003-lecture-003.md), [Unit 4](source/id-ID/units/unit-004-lecture-004.md), [Unit 5](source/id-ID/units/unit-005-lecture-005.md), [Unit 6](source/id-ID/units/unit-006-lecture-006.md), [Unit 7](source/id-ID/units/unit-007-lecture-007.md), [Unit 8](source/id-ID/units/unit-008-lecture-008.md), [Unit 9](source/id-ID/units/unit-009-lecture-009.md), dan [Unit 10](source/id-ID/units/unit-010-lecture-010.md). Unit 1–7 sudah termasuk dalam pembaca kumulatif; Unit 8–10 sudah ditinjau independen dan menjadi batas sumber berikutnya.

Unit 1–7 mencakup `Notes.tex` baris 134–1770: pengantar topologi aljabar, ruang topologis, topologi awal dan akhir, perekatan, keterhubungan, homotopi, funktor dan kategori homotopi, transformasi natural, ruang SLPC, ruang bertitik, ruang penutup, tarik balik, pengangkatan lintasan, transpor serat, topologi kompak-terbuka pada ruang lintasan, ruang loop, dan grup fundamental. Ketiga puluh latihan mempunyai solusi lengkap; kedua pertanyaan sumber juga dijawab. Pendamping penguasaan menutup bukti sifat universal, lema perekatan, penciutan radial, funktorialitas, argumen kurva sinus topolog, komposisi pemetaan penutup, struktur tarik balik, lema kekompakan, naturalitas transpor, basis ruang lintasan, kekontinuan operator pengangkatan, serta naturalitas funktor ruang loop dan grup fundamental.

## Backend modular

Direktori [`backend/`](backend/) memuat graf `curriculum.interop 0.1.0` yang locale-neutral: otoritas, edisi, unit, segmen, konsep, istilah, relasi, latihan–solusi, hak, koreksi, QA, dan artefak. Validasi offline:

```powershell
python scripts/validate-backend.py
```

Backend bukan pengganti pembaca; ia memungkinkan unit yang sama dipilih, diaudit, dan ditransposisikan ke bahasa lain tanpa menebak struktur dari prosa Bahasa Indonesia.

## Bangun dan verifikasi

```powershell
pwsh -NoProfile -File scripts/build-unit-001.ps1
python scripts/qa-unit-001.py
pwsh -NoProfile -File scripts/build-units-001-002.ps1
python scripts/qa-units-001-002.py
pwsh -NoProfile -File scripts/build-units-001-003.ps1
python scripts/qa-units-001-003.py
pwsh -NoProfile -File scripts/build-units-001-004.ps1
python scripts/qa-units-001-004.py
pwsh -NoProfile -File scripts/build-units-001-005.ps1
python scripts/qa-units-001-005.py
pwsh -NoProfile -File scripts/build-units-001-007.ps1
python scripts/qa-units-001-007.py
python scripts/validate-backend.py
```

Build PDF ganda dengan epoch tetap menghasilkan byte identik. HTML memakai CSS tersemat, tidak memerlukan JavaScript atau jaringan, dan menjadi permukaan aksesibilitas utama. PDF memiliki `/Lang=id-ID`, font tersemat, dan peta Unicode, tetapi belum ditandai secara struktural.

## Provenans

- [Atribusi dan perubahan](ATTRIBUTION.md)
- [Keputusan sumber](00_control/SOURCE_DECISION.md)
- [Identitas otoritas](00_control/AUTHORITY.json)
- [Status produksi](00_control/CURRENT_STATE.md)
- [QA Unit 1](qa/UNIT_001_QA.json)
- [Rereview independen](qa/UNIT_001_INDEPENDENT_REVIEW.md)
- [QA kumulatif Unit 1–2](qa/UNITS_001_002_QA.json)
- [Rereview independen Unit 2](qa/UNIT_002_INDEPENDENT_REVIEW.md)
- [QA kumulatif Unit 1–3](qa/UNITS_001_003_QA.json)
- [Rereview independen Unit 3](qa/UNIT_003_INDEPENDENT_REVIEW.md)
- [QA kumulatif Unit 1–4](qa/UNITS_001_004_QA.json)
- [Rereview independen Unit 4](qa/UNIT_004_INDEPENDENT_REVIEW.md)
- [QA kumulatif Unit 1–5](qa/UNITS_001_005_QA.json)
- [Rereview independen Unit 5](qa/UNIT_005_INDEPENDENT_REVIEW.md)
- [Rereview independen Unit 6](qa/UNIT_006_INDEPENDENT_REVIEW.md)
- [Rereview independen Unit 7](qa/UNIT_007_INDEPENDENT_REVIEW.md)
- [QA kumulatif Unit 1–7](qa/UNITS_001_007_QA.json)
- [QA visual Unit 1–7](qa/UNITS_001_007_VISUAL_QA.md)
- [Rereview independen Unit 8](qa/UNIT_008_INDEPENDENT_REVIEW.md)
- [Rereview independen Unit 9](qa/UNIT_009_INDEPENDENT_REVIEW.md)
- [Rereview independen Unit 10](qa/UNIT_010_INDEPENDENT_REVIEW.md)

Pembaca lengkap masih dalam produksi. Inti Roberts akan diterjemahkan secara berurutan; materi homologi/metode seluler dan lapisan penguasaan yang tidak tersedia dalam inti akan ditulis tersendiri dan ditandai sebagai materi edisi.
