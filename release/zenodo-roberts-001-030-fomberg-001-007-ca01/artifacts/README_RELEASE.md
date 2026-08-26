# Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30, Jembatan Homologi §1.1–1.13, dan Asesmen Kumulatif 1

Versi: `0.31.0`  
Tanggal: 26 Agustus 2026  
Status: **Roberts lengkap 30/30; Fomberg O012-FOM-001–007 lengkap untuk seluruh bentang terpilih; D60-CA01 lengkap 8/8; kursus komposit tetap parsial**

Checkpoint ini mencakup tiga lapisan yang identitasnya tetap terpisah:

- seluruh Kuliah 1–30 dari *Algebraic Topology* karya David Michael Roberts,
  `Notes.tex` baris 134–6368 pada komit
  `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`;
- O012-FOM-001–007 dari *Algebraic Topology* karya Yeheli Fomberg,
  berdasarkan kuliah Nir Lazarovich, `algebraic_topology.tex` baris 31–4185,
  Bagian 1.1–1.13, pada komit
  `563194fae879178b9a6871b249513bfc27968975`; dan
- D60-CA01, asesmen kumulatif asli edisi ini yang berisi delapan soal,
  delapan petunjuk, dan delapan solusi lengkap untuk D60-R01–D60-R07.

Bentang Fomberg yang dipilih telah selesai; kursor sumber berikutnya adalah
baris 4186. Kursus komposit masih parsial: Asesmen Kumulatif 2 dan 3 (16
butir), petunjuk rute penguasaan biasa yang belum lengkap, empat laboratorium
komputasi, capstone lintas-invarian, dan setiap normalisasi grafik bukti yang
masih dicatat sensus QA belum ditutup.

## Mulai membaca

1. `00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_READER.pdf`
   adalah pembaca A4 utama untuk pengunduhan. Jumlah halaman dan identitas byte
   final dicatat dalam `release-manifest.json`; font tersemat dan mempunyai
   peta ToUnicode, tetapi PDF belum bertag secara struktural.
2. `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_READER.html`
   adalah permukaan akses utama: mandiri/offline, terpusat, reflowable pada
   desktop dan seluler, serta memakai MathML asli tanpa dependensi runtime.

## Sumber yang dapat dilanjutkan dan QA

- `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_EDITABLE_SOURCE_BACKEND.zip`
  memuat sumber Markdown lengkap sampai boundary ini, backend JSONL append-only,
  lisensi dan saksi otoritas, kontrol minimum, serta build dan validator yang
  diperlukan untuk melanjutkan pekerjaan.
- `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_CA01_QA_PROVENANCE.zip`
  memuat dua review independen D60-CA01, QA unit, sensus penguasaan dan
  perbaikan bukti, receipt backend kumulatif, bukti build/visual/browser,
  manifest pembaca, serta ledger input beku.
- `LICENSE.md`, `RELEASE_RIGHTS.md`, `release-manifest.json`, dan
  `SHA256SUMS` memberi lisensi, atribusi, inventaris byte, dan ikatan hash.

Kesembilan berkas payload tidak memuat kredensial, cache, render mentah, dump
koordinasi, jalur lokal absolut, data pribadi pengguna, atau salinan ganda
pembaca.

## Atribusi, lisensi, dan provenance

Komponen Roberts berasal dari David Michael Roberts dan tetap berlisensi
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Komponen Fomberg
berasal dari Yeheli Fomberg, berdasarkan kuliah Nir Lazarovich, dan tetap
berlisensi [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
D60-CA01 adalah materi pendamping asli edisi yang dirilis di bawah CC BY-SA
4.0. Pembaca dan paket terpadu tersedia di bawah CC BY-SA 4.0; rincian
pemisahan komponen, perubahan, dan kewajiban share-alike terdapat dalam
`RELEASE_RIGHTS.md`.

Penerjemahan, restrukturisasi semantik, materi penguasaan, QA, rekayasa build,
dan persiapan rilis dilakukan dengan **OpenAI Codex gpt-5.6-sol, Ultra** atas
arahan pengguna. Catatan proses ini tidak menggantikan kredit penulis sumber
atau kontributor manusia. Edisi ini independen dan tidak menyiratkan sponsor,
dukungan, endorsement, atau status resmi dari penulis, dosen asal, maupun
institusi mereka.
