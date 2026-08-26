# Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30 dan Jembatan Homologi, Derajat, dan Kompleks Seluler §1.1–1.13

Versi: `0.30.7`  
Tanggal: 26 Agustus 2026  
Status: **Roberts lengkap 30/30; Fomberg O012-FOM-001–007 lengkap untuk seluruh bentang terpilih; kursus komposit tetap parsial**

Checkpoint ini mencakup dua sumber dengan identitas edisi yang tetap terpisah:

- seluruh Kuliah 1–30 dari *Algebraic Topology* karya David Michael Roberts,
  `Notes.tex` baris 134–6368 pada komit
  `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`; dan
- O012-FOM-001–007 dari *Algebraic Topology* karya Yeheli Fomberg,
  berdasarkan kuliah Nir Lazarovich, `algebraic_topology.tex` baris 31–4185,
  Bagian 1.1–1.13, pada komit
  `563194fae879178b9a6871b249513bfc27968975`.

Kursor sumber berikutnya adalah baris 4186, setelah bentang Fomberg terpilih;
Bagian 1.13 tentang homologi seluler telah selesai. Tujuh komponen
Fomberg mempertahankan ID edisi O012-FOM-001 hingga
O012-FOM-007 dan dipetakan secara terpisah ke D60-R08, D60-R09, D60-R10,
D60-R11, dan D60-R12 (tiga komponen); semuanya bukan tambahan pada 30 kuliah
Roberts. Kursus komposit masih parsial karena sisa lapisan penguasaan
kumulatif, empat laboratorium komputasi, serta capstone lintas-invarian belum
lengkap.

## Mulai membaca

1. `00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_READER.pdf`
   adalah pembaca A4 utama untuk pengunduhan. Dokumen ini berjumlah 472 halaman;
   font tersemat dan mempunyai peta ToUnicode, tetapi PDF belum bertag secara
   struktural.
2. `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_READER.html`
   adalah permukaan akses utama: mandiri/offline, terpusat, reflowable pada
   desktop dan seluler, dan memakai MathML asli tanpa dependensi runtime.

Identitas byte, jumlah halaman PDF, dan statistik backend final dicatat dalam
`release-manifest.json`, `SHA256SUMS`, dan receipt QA yang dihasilkan setelah
seluruh gate lokal lulus.

## Sumber yang dapat dilanjutkan dan QA

- `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_EDITABLE_SOURCE_BACKEND.zip`
  memuat sumber Markdown, saksi sumber resmi dan lisensi komponen, backend
  JSONL ber-ID stabil, stylesheet, build/validator, dan kontrol terminologi
  minimum yang diperlukan untuk melanjutkan pekerjaan.
- `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_007_QA_PROVENANCE.zip`
  memuat audit sumber, review independen, receipt build/visual/backend,
  manifest pembaca, dan ledger input beku untuk boundary ini.
- `LICENSE.md`, `RELEASE_RIGHTS.md`, `release-manifest.json`, dan
  `SHA256SUMS` memberi lisensi, atribusi, inventaris byte, dan ikatan hash.

Kesembilan berkas payload tidak memuat kredensial, cache, dump koordinasi,
jalur lokal absolut, data pribadi pengguna, atau salinan ganda pembaca.

## Atribusi, lisensi, dan provenance

Komponen Roberts berasal dari David Michael Roberts, © 2019 David Michael
Roberts, dan tetap berlisensi [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Komponen Fomberg berasal dari Yeheli Fomberg, berdasarkan kuliah Nir
Lazarovich, dan tetap berlisensi
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Pembaca dan paket terpadu tersedia di bawah CC BY-SA 4.0; rincian pemisahan
komponen, perubahan, dan kewajiban share-alike terdapat dalam
`RELEASE_RIGHTS.md`.

Penerjemahan, restrukturisasi semantik, materi penguasaan yang ditandai,
perbaikan pembuktian yang ditandai, QA, rekayasa build, dan persiapan rilis
dilakukan dengan **OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna.
Catatan proses ini tidak menggantikan kredit penulis sumber atau kontributor
manusia. Edisi ini independen dan tidak menyiratkan sponsor, dukungan,
endorsement, atau status resmi dari penulis, dosen asal, maupun institusi
mereka.
