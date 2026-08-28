# Topologi Aljabar — edisi Bahasa Indonesia

Edisi Bahasa Indonesia independen dari *Pure Mathematics Topic D: Algebraic
Topology* karya David Michael Roberts. Ketiga puluh kuliah Roberts sudah
diterjemahkan secara berurutan sampai akhir sumber; edisi sumber Roberts dengan
demikian lengkap **30/30**. Jalur kuliah komposit O012/D60 masih **parsial**:
jembatan Fomberg mencakup seluruh bentang terpilih Bagian 1.1–1.13
(`algebraic_topology.tex:31–4185`). Ketiga asesmen kumulatif kini lengkap:
24 soal lintas-rute, 24 petunjuk, dan 24 solusi lengkap. Bersama 84 butir
penguasaan biasa, lapisan penguasaan berbasis solusi telah mencapai **108/108**.
Laboratorium Komputasi 1—monodromi ruang penutup dan presentasi grup—serta
Laboratorium Komputasi 2—matriks rantai dan bentuk normal Smith—sudah lengkap
dengan program luring, uji, keluaran acuan, interpretasi, dan solusi.
Dua laboratorium komputasi, proyek puncak lintas-invarian, dan penutupan
metadata grafik bukti yang tercatat masih harus diselesaikan.

## Mulai membaca

- [Pembaca HTML terbaru: Roberts 30/30 + Fomberg 1.1–1.13 + Asesmen Kumulatif 1–3 + Laboratorium 1–2](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02/)
  adalah permukaan utama: satu berkas mandiri, reflow, tanpa JavaScript atau
  akses jaringan, dengan matematika MathML asli.
- [HTML checkpoint komposit terbaru di repositori](output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02/index.html) dapat
  diunduh dan dibuka secara luring.
- [PDF A4 checkpoint komposit terbaru](output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-id.pdf)
  adalah permukaan cetak sekunder sepanjang 529 halaman. Semua font tersemat,
  subset, dan memiliki peta ToUnicode; PDF belum ditandai secara struktural.
- [Konsep Zenodo edisi ini](https://doi.org/10.5281/zenodo.22061489)
  mempertahankan garis versi preservasi; nomor konsep tetap sama ketika
  checkpoint baru diterbitkan.
- [Checkpoint Zenodo 0.30.4 sebelumnya](https://doi.org/10.5281/zenodo.22097007)
  mempertahankan tepat byte batas Roberts 30/30 + Fomberg 1.1–1.10. Versi
  [0.30.5](https://doi.org/10.5281/zenodo.22098820) mempertahankan tepat byte
  pembaca dan paket sumber/backend untuk cakupan 1.1–1.11 pada garis konsep
  yang sama. Checkpoint sebelumnya
  [0.30.6](https://doi.org/10.5281/zenodo.22102865) mempertahankan tepat byte
  pembaca, sumber/backend, dan bukti QA untuk cakupan 1.1–1.12. Checkpoint
  berikutnya [0.30.7](https://doi.org/10.5281/zenodo.22104150) mempertahankan
  seluruh cakupan terpilih 1.1–1.13. Versi
  [0.31.0](https://doi.org/10.5281/zenodo.22105179) menambahkan Asesmen
  Kumulatif 1; [0.31.1](https://doi.org/10.5281/zenodo.22106133) menutup
  penguasaan biasa 84/84; versi
  [0.31.2](https://doi.org/10.5281/zenodo.22135136) menambahkan Asesmen
  Kumulatif 2–3, pembaca 501 halaman, dan backend 7.273 rekaman; dan versi
  [0.31.3](https://doi.org/10.5281/zenodo.22142210) menambahkan Laboratorium
  Komputasi 1; dan versi terbaru
  [0.31.4](https://doi.org/10.5281/zenodo.22147224) menambahkan Laboratorium
  Komputasi 2, pembaca 529 halaman, backend 7.546 rekaman, serta bukti build,
  visual, browser, eksekusi, dan provenans pada garis konsep yang sama.

Checkpoint ini mencakup seluruh 30 kuliah Roberts hingga `Notes.tex:6368`:
topologi dasar, homotopi, ruang penutup dan monodromi, grup/grupoid fundamental,
Seifert–van Kampen, klasifikasi ruang penutup, grup homotopi lebih tinggi,
bundel serat, kompleks, kohomologi, barisan eksak, teori relatif dan tereduksi,
perbandingan, aksioma, derajat, serta aplikasi klasik. Tujuh komponen Fomberg
menambahkan kompleks-Δ, kompleks simplisial, rantai, batas, siklus, homologi
simplisial dan singular, funktorialitas, invariansi homotopi, barisan eksak,
homologi relatif, eksisi, Mayer–Vietoris, kealamian, pembandingan
simpleksial–singular, derajat pemetaan, teorema sfera berbulu, derajat lokal,
rumus lokal-ke-global, kompleks CW, topologi lemah, contoh/noncontoh seluler,
filtrasi ruang projektif, pemetaan batas seluler, bilangan insidensi, dan
perhitungan homologi seluler dari `algebraic_topology.tex:31–4185`, beserta
latihan penguasaan dengan petunjuk dan solusi lengkap. Ketiga asesmen
kumulatif menguji seluruh jalur melalui 24 soal asli tanpa menyalin bank
masalah Fomberg. Laboratorium 1 menghubungkan aksi monodromi kanan, citra
permutasi, stabilisator, transversal Schreier, dan presentasi grup melalui
program Python pustaka-standar yang dapat direproduksi tanpa jaringan.
Laboratorium 2 membangun kompleks rantai dari matriks batas integral,
memverifikasi syarat \(d^2=0\), menghitung bentuk normal Smith, dan membaca
bagian bebas serta torsi homologi dengan uji dan keluaran acuan deterministik.
Status
30/30 hanya menyatakan kelengkapan komponen Roberts;
status 108/108 menyatakan kelengkapan lapisan penguasaan berbasis solusi,
bukan kelengkapan laboratorium dan proyek puncak jalur komposit.

Sumber semantik berada di [`source/id-ID/`](source/id-ID/). Batas historis
tetap dipertahankan tanpa mengubah byte atau resinya, antara lain
[Roberts 30/30 + Fomberg 1.1–1.2](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001/),
[Roberts 30/30 + Fomberg 1.1–1.4](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-002/),
[Roberts 30/30 + Fomberg 1.1–1.6](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-003/),
[Roberts 30/30 + Fomberg 1.1–1.10](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-004/),
[Roberts 30/30 + Fomberg 1.1–1.11](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-005/),
[Roberts 30/30 + Fomberg 1.1–1.12](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-006/),
[Unit 1](https://kokunoyumeto.github.io/algebraic-topology-id/),
[Unit 1–13](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-013/),
[Unit 1–19](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-019/),
dan [Unit 1–25](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-025/).

## Backend modular

Direktori [`backend/`](backend/) memuat graf `curriculum.interop 0.1.0` yang
locale-neutral: identitas otoritas dan edisi, unit, segmen, konsep, istilah,
relasi, latihan–solusi, hak, koreksi, QA, dan artefak. Checkpoint komposit
mempertahankan awalan 7.404 rekaman checkpoint 0.31.3 (8.975.700 byte; digest
bundel `4740eb2ff83b4f9df3c0d90c2426ff77e652b23cad0bbe7763c54ebdefa60b4b`)
secara byte-identik, lalu menambahkan 142 rekaman/147.055 byte bagi D60-LAB02.
Backend kumulatif kini berisi 7.546 rekaman append-only (9.122.755 byte) dengan
digest bundel
`ac3a0377861ed2b728f9c7473579fdd4febe43e454a92f3ea06451e13d46c8f8`.
Backend ini melengkapi—bukan menggantikan—pembaca manusia.

Validasi dan build aktif:

```powershell
python -B scripts/qa-computation-lab-002.py
python -B scripts/validate-backend-append-only-computation-lab-002.py
python -B scripts/build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02.py
python -B scripts/finalize-build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02.py
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

Bentang Fomberg terpilih selesai tepat sebelum
`algebraic_topology.tex:4186`; lapisan penguasaan berbasis solusi juga selesai
108/108, dan Laboratorium Komputasi 1–2 telah selesai. Produksi berikutnya
dimulai pada Laboratorium Komputasi 3: pemetaan batas seluler dan derajat,
lalu Laboratorium 4, penutupan metadata bukti, dan proyek puncak yang
ditandai jelas sebagai materi edisi.
Hak dan atribusi Roberts, Fomberg, serta materi asli tetap dapat dibedakan pada
backend dan artefak rilis.
