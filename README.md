# Topologi Aljabar — edisi Bahasa Indonesia

Edisi Bahasa Indonesia yang sedang diproduksi dari *Algebraic Topology* karya David Michael Roberts. Materi sumber dibekukan pada commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53` dan tersedia di bawah [CC BY 4.0](LICENSE.md). Edisi ini bersifat independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

## Baca

- [Pembaca HTML Unit 1](https://kokunoyumeto.github.io/algebraic-topology-id/) — permukaan utama yang semantik, mandiri, dan memakai MathML asli.
- [PDF Unit 1](output/pdf/topologi-aljabar-unit-001-id.pdf) — permukaan sekunder A4, 5 halaman.
- [Sumber semantik Unit 1](source/id-ID/reader-unit-001.md).

Unit 1 mencakup `Notes.tex` baris 134–348: pengantar topologi aljabar, ruang topologis, basis lingkungan, kontinuitas, homeomorfisme, topologi awal, serta sifat universalnya. Kedua latihan sumber mempunyai solusi lengkap. Pendamping penguasaan juga memuat pemeriksaan lema dan contoh penciutan radial.

## Backend modular

Direktori [`backend/`](backend/) memuat graf `curriculum.interop 0.1.0` yang locale-neutral: otoritas, edisi, unit, segmen, konsep, istilah, relasi, latihan–solusi, hak, koreksi, QA, dan artefak. Unit 1 saat ini mempunyai 139 rekaman kanonis dalam 11 berkas JSONL. Validasi offline:

```powershell
python scripts/validate-backend.py
```

Backend bukan pengganti pembaca; ia memungkinkan unit yang sama dipilih, diaudit, dan ditransposisikan ke bahasa lain tanpa menebak struktur dari prosa Bahasa Indonesia.

## Bangun dan verifikasi

```powershell
powershell -NoProfile -File scripts/build-unit-001.ps1
python scripts/qa-unit-001.py
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

Pembaca lengkap masih dalam produksi. Inti Roberts akan diterjemahkan secara berurutan; materi homologi/metode seluler dan lapisan penguasaan yang tidak tersedia dalam inti akan ditulis tersendiri dan ditandai sebagai materi edisi.
