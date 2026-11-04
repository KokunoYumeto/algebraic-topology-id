# Topologi Aljabar: edisi Bahasa Indonesia

Edisi Bahasa Indonesia yang lengkap dari *Algebraic Topology* (Pure Mathematics Topic D) karya David Michael Roberts,
seluruh 30 kuliah, digabung dengan jembatan dari catatan *Algebraic Topology* karya Yeheli Fomberg (Bagian 1.1–1.13)
serta materi latihan baru: tiga asesmen kumulatif, 108 butir penguasaan dengan petunjuk dan solusi lengkap, empat
laboratorium komputasi, dan proyek puncak D60. Tersedia sebagai pembaca HTML, PDF A4 (564 halaman), sumber, dan backend
kurikulum modular.

## Mulai membaca

- [Pembaca HTML lengkap](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04-capstone/): satu berkas mandiri, reflow, tanpa JavaScript atau akses jaringan, dengan
  matematika MathML; [salinan di repositori](output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04-capstone/index.html) untuk dibaca luring.
- [PDF A4](output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04-capstone-id.pdf): semua font tersemat dan memiliki peta ToUnicode; PDF belum memiliki
  struktur tag.

## Cara pembuatan

Terjemahan, restrukturisasi semantik, pemeriksaan, build, dan persiapan rilis dikerjakan oleh AI: OpenAI Codex
gpt-5.6-sol, Ultra. Koreksi sumber didokumentasikan secara terpisah, dan diagram digambar ulang atau dideskripsikan
secara semantik. Build kumulatif memakai epoch tetap dan dua build bersih yang harus identik byte demi byte; bukti
unit, audit sumber, QA terminologi, build, peramban, visual, dan backend ada di [`qa/`](qa/).

## Status

Edisi lengkap (versi 0.31.7): Roberts 30/30 hingga `Notes.tex:6368`; bentang Fomberg terpilih 1.1–1.13
(`algebraic_topology.tex:31–4185`); Asesmen Kumulatif 1–3 (24 soal, 24 petunjuk, 24 solusi); lapisan penguasaan 108/108;
Laboratorium Komputasi 1–4 dengan program Python luring, uji, dan keluaran acuan; empat perbaikan bukti; dan capstone
D60. Masih mungkin ada kesalahan.

## Isi

- Topik: topologi dasar, homotopi, ruang penutup dan monodromi, grup dan grupoid fundamental, Seifert–van Kampen,
  grup homotopi lebih tinggi, bundel serat, kompleks-Δ, kompleks simplisial dan CW, homologi simplisial, singular, dan
  seluler, eksisi, Mayer–Vietoris, derajat pemetaan, kohomologi, dan aplikasi klasik.
- [`source/id-ID/`](source/id-ID/): sumber semantik; [`output/`](output/): pembaca HTML dan PDF;
  [`00_control/`](00_control/): status produksi dan identitas otoritas.
- [`backend/`](backend/): graf `curriculum.interop 0.1.0` yang netral-lokal (8.338 rekaman, 10.040.043 byte; digest
  bundel `8a3ffc9618e56dfce048c41e938aabef4ffbfd3db20a03a4f52f218985230dbb`) untuk otoritas, unit, segmen, konsep,
  istilah, relasi, latihan–solusi, hak, koreksi, QA, dan artefak.
- Pembaca untuk cakupan sebelumnya tetap tersedia tanpa perubahan, misalnya
  [Unit 1–25](https://kokunoyumeto.github.io/algebraic-topology-id/units-001-025/) dan [Roberts 30/30 + Fomberg 1.1–1.12](https://kokunoyumeto.github.io/algebraic-topology-id/roberts-001-030-fomberg-001-006/).

Validasi dan build (pada checkout lengkap repositori ini):

```powershell
python -B scripts/census-proof-repairs-final.py
python -B scripts/validate-final-capstone-rev3-backend.py
python -B scripts/build-final-capstone.py
python -B scripts/finalize-build-final-capstone.py
```

## Sumber dan atribusi

- David Michael Roberts, *Algebraic Topology*, © 2019, commit
  [`b947ad2e`](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/tree/b947ad2e9f9e301bfe24590a9db653bc54fa1a53)
  ([CC BY 4.0](authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/LICENSE.md)).
- Yeheli Fomberg, *Algebraic Topology*, berdasarkan kuliah Nir Lazarovich (musim semi 2025), commit
  [`563194fa`](https://git.sr.ht/~yp/math-notes/tree/563194fae879178b9a6871b249513bfc27968975/item/algebraic_topology.tex)
  ([CC BY-SA 4.0](authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/tree/LICENSE)).
- Atribusi dan catatan perubahan: [ATTRIBUTION.md](ATTRIBUTION.md); keputusan sumber:
  [00_control/SOURCE_DECISION.md](00_control/SOURCE_DECISION.md). Edisi ini independen dan tidak disahkan oleh para
  penulis sumber atau lembaga mereka.

## Lisensi

Terjemahan dan pendamping yang hanya memuat komponen Roberts tersedia menurut CC BY 4.0; adaptasi Fomberg, pembaca
terintegrasi, dan materi baru tersedia menurut CC BY-SA 4.0. Lihat [matriks cakupan lisensi](LICENSE.md).
