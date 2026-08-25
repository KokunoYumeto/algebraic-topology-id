# Topologi Aljabar — edisi Bahasa Indonesia

Edisi Bahasa Indonesia independen dari *Pure Mathematics Topic D: Algebraic
Topology* karya David Michael Roberts. Ketiga puluh kuliah Roberts sudah
diterjemahkan secara berurutan sampai akhir sumber; edisi sumber Roberts dengan
demikian lengkap **30/30**. Jalur kuliah komposit O012/D60 masih **parsial**:
jembatan homologi Fomberg kini mencakup Bagian 1.1–1.10
(`algebraic_topology.tex:31–2846`), sedangkan Bagian 1.11–1.13 serta lapisan
pembuktian, latihan bersolusi, laboratorium, dan proyek puncak edisi masih harus
diselesaikan.

## Mulai membaca

- [Pembaca HTML terbaru: Roberts 30/30 + Fomberg 1.1–1.10](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-004/)
  adalah permukaan utama: satu berkas mandiri, reflow, tanpa JavaScript atau
  akses jaringan, dengan matematika MathML asli.
- [HTML checkpoint komposit terbaru di repositori](output/html/roberts-001-030-fomberg-001-004/index.html) dapat
  diunduh dan dibuka secara luring.
- [PDF A4 checkpoint komposit terbaru](output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-004-id.pdf)
  adalah permukaan cetak sekunder sepanjang 424 halaman. PDF memakai font
  tersemat dan peta Unicode, tetapi belum ditandai secara struktural.
- [Konsep Zenodo edisi ini](https://doi.org/10.5281/zenodo.22061489)
  mempertahankan garis versi preservasi; nomor konsep tetap sama ketika
  checkpoint baru diterbitkan.
- [Checkpoint Zenodo 0.30.4](https://doi.org/10.5281/zenodo.22097007)
  mempertahankan tepat byte pembaca dan paket sumber/backend untuk cakupan
  Roberts 30/30 + Fomberg 1.1–1.10 ini.

Checkpoint ini mencakup seluruh 30 kuliah Roberts hingga `Notes.tex:6368`:
topologi dasar, homotopi, ruang penutup dan monodromi, grup/grupoid fundamental,
Seifert–van Kampen, klasifikasi ruang penutup, grup homotopi lebih tinggi,
bundel serat, kompleks, kohomologi, barisan eksak, teori relatif dan tereduksi,
perbandingan, aksioma, derajat, serta aplikasi klasik. Empat komponen Fomberg
menambahkan kompleks-Δ, kompleks simplisial, rantai, batas, siklus, homologi
simplisial dan singular, funktorialitas, invariansi homotopi, barisan eksak,
homologi relatif, eksisi, Mayer–Vietoris, kealamian, serta pembandingan
simpleksial–singular dari `algebraic_topology.tex:31–2846`, beserta latihan
penguasaan dengan petunjuk dan solusi lengkap. Status 30/30 hanya menyatakan
kelengkapan komponen Roberts,
bukan kelengkapan jalur komposit.

Sumber semantik berada di [`source/id-ID/`](source/id-ID/). Batas historis
tetap dipertahankan tanpa mengubah byte atau resinya, antara lain
[Roberts 30/30 + Fomberg 1.1–1.2](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001/),
[Roberts 30/30 + Fomberg 1.1–1.4](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-002/),
[Roberts 30/30 + Fomberg 1.1–1.6](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-003/),
[Unit 1](https://kokunoyumeto.github.io/algebraic-topology-id/),
[Unit 1–13](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-013/),
[Unit 1–19](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-019/),
dan [Unit 1–25](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-025/).

## Backend modular

Direktori [`backend/`](backend/) memuat graf `curriculum.interop 0.1.0` yang
locale-neutral: identitas otoritas dan edisi, unit, segmen, konsep, istilah,
relasi, latihan–solusi, hak, koreksi, QA, dan artefak. Checkpoint komposit
mempertahankan awalan Roberts 4.761 rekaman secara byte-identik lalu menambahkan
1.352 rekaman Fomberg, sehingga berisi 6.113 rekaman append-only (7.284.299 byte)
dengan digest bundel
`902eb71aa8a8b25e824ebe9ddae556e914e370d603382f28860392d6e186baba`.
Backend ini melengkapi—bukan menggantikan—pembaca manusia.

Validasi dan build aktif:

```powershell
python -B scripts/qa-fomberg-unit-004.py
python -B scripts/validate-backend-append-only-fomberg-unit-004.py
python -B scripts/validate-backend-append-only-fomberg-unit-004-cumulative.py
pwsh -NoProfile -File scripts/build-roberts-001-030-fomberg-001-004.ps1
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
- Sumber Fomberg dibekukan pada commit
  [`563194fae879178b9a6871b249513bfc27968975`](https://git.sr.ht/~yp/math-notes/tree/563194fae879178b9a6871b249513bfc27968975/item/algebraic_topology.tex)
  dan dilisensikan di bawah [CC BY-SA 4.0](authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/tree/LICENSE).
- Pembaca terintegrasi Roberts–Fomberg beserta materi penguasaan baru
  didistribusikan di bawah CC BY-SA 4.0, sambil mempertahankan identitas dan
  atribusi komponen Roberts CC BY 4.0 serta Fomberg CC BY-SA 4.0.
- [Matriks cakupan lisensi repositori](LICENSE.md) membedakan terjemahan dan
  pendamping Roberts-only CC BY 4.0 dari adaptasi Fomberg serta susunan pembaca
  terintegrasi CC BY-SA 4.0.
- [Atribusi dan catatan perubahan](ATTRIBUTION.md),
  [keputusan sumber](00_control/SOURCE_DECISION.md), dan
  [identitas otoritas](00_control/AUTHORITY.json) dipertahankan bersama edisi.
- Edisi ini bersifat independen dan tidak menyiratkan dukungan, pengesahan,
  atau afiliasi dengan penulis sumber.
- Produksi terjemahan, restrukturisasi semantik, QA, build, dan persiapan rilis
  dilakukan dengan **OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna.
  Catatan proses ini tidak menggantikan kredit David Michael Roberts atau hak
  dan atribusi komponen sumber.

Produksi berikutnya dimulai tepat pada Fomberg `algebraic_topology.tex:2847`,
melanjutkan jembatan §§1.11–1.13, kemudian lapisan perbaikan
pembuktian/penguasaan/laboratorium/proyek puncak yang ditandai jelas sebagai
materi edisi.
Hak dan atribusi Roberts, Fomberg, serta materi asli tetap dapat dibedakan pada
backend dan artefak rilis.
