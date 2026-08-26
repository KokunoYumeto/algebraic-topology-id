# Paket sumber yang dapat diedit dan backend modular

Paket ini adalah sumber ringkas yang dapat dilanjutkan untuk checkpoint
*Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30, Jembatan Homologi
§1.1–1.13, dan Asesmen Kumulatif 1*, versi 0.31.0.

Komponen Roberts lengkap 30/30 sampai `Notes.tex:6368`. Komponen Fomberg
mencakup `algebraic_topology.tex:31–4185` (Bagian 1.1–1.13,
`O012-FOM-001–007`) dan telah selesai pada bentang terpilih. D60-CA01 lengkap
dengan delapan soal, delapan petunjuk, dan delapan solusi penuh. Kursus
komposit tetap parsial.

Pembaca PDF, pembaca HTML, dan paket QA/provenans merupakan berkas saudara
dalam rilis yang sama dan sengaja tidak diduplikasi di dalam ZIP ini.

## Tata letak paket

- `source/id-ID/` memuat sumber semantik pembaca berbahasa Indonesia, termasuk
  D60-CA01 sebagai materi asli edisi yang terpisah dari teks Roberts dan
  Fomberg.
- `backend/` memuat backend append-only dengan skema `curriculum.interop
  0.1.0`; identitas byte, jumlah rekaman, dan hash bundel boundary ini terdapat
  dalam `release-manifest.json` dan receipt backend di paket QA saudara.
- `scripts/` memuat build pembaca, QA asesmen, produsen append-only, sensus,
  validator, packager, dan publisher.
- `00_control/` memuat identitas otoritas, terminologi, keputusan sumber, hak
  per komponen, rute kurikulum, kursor, dan workflow yang diperlukan untuk
  melanjutkan pekerjaan.
- `authority/upstream/` memuat sumber otoritatif beku dan lisensi yang digunakan.

## Build dan pemeriksaan

Jalankan dari akar hasil ekstraksi dengan PowerShell dan Python luring:

```powershell
python -B scripts/qa-cumulative-assessment-001.py
python -B scripts/validate-backend-append-only-cumulative-assessment-001.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-roberts-001-030-fomberg-001-007-ca01.ps1
```

Build memakai epoch tetap dan menghasilkan dua build HTML serta PDF yang
byte-identik. Bukti build, browser, visual, backend, dan provenance terdapat
dalam paket QA/provenans saudara pada rilis yang sama.

## Hak, atribusi, dan provenance

`LICENSE.md`, `ATTRIBUTION.md`, lisensi otoritas beku, dan
`00_control/RIGHTS_AND_COMPONENTS.csv` mempertahankan identitas dan hak setiap
lapisan secara terpisah. Pembaca terintegrasi, komponen Fomberg, dan D60-CA01
tersedia di bawah CC BY-SA 4.0. Komponen Roberts-only yang dapat dipisahkan
tetap CC BY 4.0. Edisi ini independen dan tidak menyiratkan dukungan atau
afiliasi dengan penulis sumber atau institusinya. Produksi dilakukan dengan
**OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna, tanpa menggantikan
kredit penulis sumber.
