# Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30 dan Jembatan Homologi §1.1–1.2

Versi: `0.30.1`  
Tanggal: 24 Agustus 2026  
Status: **Roberts lengkap 30/30; Fomberg O012-FOM-001 lengkap; kursus komposit tetap parsial**

Checkpoint ini mencakup dua komponen yang penomorannya tetap terpisah:

- seluruh Kuliah 1–30 dari *Algebraic Topology* karya David Michael Roberts,
  yaitu `Notes.tex` baris 134–6368 pada komit
  `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`; dan
- O012-FOM-001 dari *Algebraic Topology* karya Yeheli Fomberg, berdasarkan
  kuliah Nir Lazarovich, yaitu `algebraic_topology.tex` baris 31–614,
  Bagian 1.1–1.2, pada komit
  `563194fae879178b9a6871b249513bfc27968975`.

Kursor Fomberg berikutnya adalah baris 615, awal Bagian 1.3 tentang homologi
singular. O012-FOM-001 **bukan** Kuliah Roberts 31. Kursus komposit masih
parsial karena jembatan Fomberg selanjutnya dan lapisan pembuktian, penguasaan,
laboratorium, serta capstone lintas-rute belum lengkap.

## Mulai membaca

1. `00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_READER.pdf` adalah
   berkas pembaca pertama dan utama untuk pengunduhan. PDF A4 memakai font
   tersemat dan `/Lang=id-ID`, tetapi belum bertag secara struktural.
2. `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_READER.html` adalah
   permukaan akses utama: mandiri/offline, terpusat, reflowable pada layar
   desktop dan seluler, serta memakai MathML asli tanpa dependensi runtime
   eksternal.

Jumlah halaman dan metrik HTML tidak ditebak di dalam kontrol statis ini.
Nilai final diambil dari receipt build yang lulus dan dibekukan dalam
`release-manifest.json`.

## Sumber yang dapat dilanjutkan dan QA

- `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_EDITABLE_SOURCE_BACKEND.zip`
  memuat sumber Markdown kedua komponen, saksi sumber resmi dan lisensi
  komponennya, backend JSONL ber-ID stabil, stylesheet, build/validator, serta
  kontrol terminologi minimum yang diperlukan untuk melanjutkan pekerjaan.
- `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_QA_PROVENANCE.zip` memuat
  QA, audit sumber, review independen, receipt build/visual, receipt backend
  append-only, manifest pembaca, dan ledger input beku pada boundary ini.
- `LICENSE.md`, `RELEASE_RIGHTS.md`, `release-manifest.json`, dan `SHA256SUMS`
  memberi lisensi, atribusi, inventaris byte, dan ikatan hash paket.

Paket tidak memuat kredensial, cache, render sementara, dump koordinasi,
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
