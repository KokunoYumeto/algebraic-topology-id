# Topologi Aljabar — edisi Bahasa Indonesia

Edisi Bahasa Indonesia independen dari *Pure Mathematics Topic D: Algebraic
Topology* karya David Michael Roberts. Ketiga puluh kuliah Roberts sudah
diterjemahkan secara berurutan sampai akhir sumber; edisi sumber Roberts dengan
demikian lengkap **30/30**. Jalur kuliah komposit O012/D60 masih **parsial**:
jembatan homologi Fomberg serta lapisan pembuktian, latihan bersolusi,
laboratorium, dan proyek puncak edisi belum digabungkan.

## Mulai membaca

- [Pembaca HTML Unit 1–30](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-030/)
  adalah permukaan utama: satu berkas mandiri, reflow, tanpa JavaScript atau
  akses jaringan, dengan matematika MathML asli.
- [HTML Unit 1–30 di repositori](output/html/units-001-030/index.html) dapat
  diunduh dan dibuka secara luring.
- [PDF A4 Unit 1–30](output/pdf/topologi-aljabar-unit-001-030-id.pdf) adalah
  permukaan cetak sekunder sepanjang 351 halaman. PDF memakai font tersemat dan
  peta Unicode, tetapi belum ditandai secara struktural.
- [Konsep Zenodo edisi ini](https://doi.org/10.5281/zenodo.22061489)
  mempertahankan garis versi preservasi; nomor konsep tetap sama ketika
  checkpoint baru diterbitkan.

Checkpoint Roberts ini mencakup seluruh 30 kuliah hingga `Notes.tex:6368`:
topologi dasar, homotopi, ruang penutup dan monodromi, grup/grupoid fundamental,
Seifert–van Kampen, klasifikasi ruang penutup, grup homotopi lebih tinggi,
bundel serat, kompleks, kohomologi, barisan eksak, teori relatif dan tereduksi,
perbandingan, aksioma, derajat, serta aplikasi klasik. Status 30/30 hanya
menyatakan kelengkapan komponen Roberts, bukan kelengkapan jalur komposit.

Sumber semantik berada di [`source/id-ID/`](source/id-ID/). Batas historis
tetap dipertahankan tanpa mengubah byte atau resinya, antara lain
[Unit 1](https://kokunoyumeto.github.io/algebraic-topology-id/),
[Unit 1–13](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-013/),
[Unit 1–19](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-019/),
dan [Unit 1–25](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-025/).

## Backend modular

Direktori [`backend/`](backend/) memuat graf `curriculum.interop 0.1.0` yang
locale-neutral: identitas otoritas dan edisi, unit, segmen, konsep, istilah,
relasi, latihan–solusi, hak, koreksi, QA, dan artefak. Batas Unit 30 berisi
4.761 rekaman backend append-only (5.213.679 byte) dengan digest bundel
`51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920`.
Backend ini melengkapi—bukan menggantikan—pembaca manusia.

Validasi dan build aktif:

```powershell
python -B scripts/validate-backend-append-only-unit-030.py
python -B scripts/validate-backend-append-only-unit-030-cumulative.py
pwsh -NoProfile -File scripts/build-units-001-030.ps1
```

Build kumulatif memakai epoch tetap dan dua build bersih yang harus identik
byte. GitHub Pages memeriksa ukuran serta SHA-256 setiap pembaca HTML beku
sebelum deployment. Bukti unit, audit sumber, QA terminologi, build, browser,
visual, dan backend disimpan di [`qa/`](qa/); status produksi dan identitas
otoritas disimpan di [`00_control/`](00_control/).

## Sumber, hak, dan provenans

- Sumber Roberts dibekukan pada commit
  [`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/tree/b947ad2e9f9e301bfe24590a9db653bc54fa1a53)
  dan dilisensikan di bawah [CC BY 4.0](authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/LICENSE.md).
- [Atribusi dan catatan perubahan](ATTRIBUTION.md),
  [keputusan sumber](00_control/SOURCE_DECISION.md), dan
  [identitas otoritas](00_control/AUTHORITY.json) dipertahankan bersama edisi.
- Edisi ini bersifat independen dan tidak menyiratkan dukungan, pengesahan,
  atau afiliasi dengan penulis sumber.
- Produksi terjemahan, restrukturisasi semantik, QA, build, dan persiapan rilis
  dilakukan dengan **OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna.
  Catatan proses ini tidak menggantikan kredit David Michael Roberts atau hak
  dan atribusi komponen sumber.

Setelah batas Roberts 30/30, produksi berlanjut dalam urutan yang sudah
ditetapkan: jembatan Fomberg §§1.1–1.13, kemudian lapisan perbaikan
pembuktian/penguasaan/laboratorium/proyek puncak yang ditandai jelas sebagai
materi edisi.
Hak dan atribusi Roberts, Fomberg, serta materi asli tetap dapat dibedakan pada
backend dan artefak rilis.
