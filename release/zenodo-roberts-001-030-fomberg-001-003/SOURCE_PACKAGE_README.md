# Paket sumber yang dapat diedit dan backend modular

Paket ini adalah sumber ringkas yang dapat dilanjutkan untuk checkpoint
*Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30 dan Jembatan Homologi
§1.1–1.6*, versi 0.30.3. Komponen Roberts lengkap 30/30 sampai
`Notes.tex:6368`. Komponen Fomberg mencakup
`algebraic_topology.tex:31–1922` (Bagian 1.1–1.6, `O012-FOM-001–003`); jalur
komposit masih parsial dan kursor berikutnya adalah baris 1923.

Pembaca PDF, pembaca HTML, dan paket QA/provenans merupakan berkas saudara
dalam rilis yang sama dan sengaja tidak diduplikasi di dalam ZIP ini.

## Tata letak paket

- `source/id-ID/` memuat sumber semantik pembaca berbahasa Indonesia. Unit
  Fomberg mempertahankan identitas edisinya sendiri dan tidak dinomori ulang
  sebagai Kuliah Roberts 31–33.
- `backend/` memuat 5.747 rekaman append-only dengan skema `curriculum.interop
  0.1.0`, berjumlah 6.649.486 byte dengan SHA-256 bundel
  `9e416c70e69dea1601bd79a259c278a9cfdfe5dca10d40b7bbc8e67d9ffba76b`.
  Packager tidak mempercayai angka tertulis ini sebagai ikatan final; ia
  membaca identitas backend secara dinamis dari receipt kumulatif yang beku.
- `scripts/` memuat build pembaca, QA unit, produsen append-only, dan validator.
- `00_control/` memuat identitas otoritas, terminologi, keputusan sumber, hak
  per komponen, dan rute kurikulum yang diperlukan untuk melanjutkan pekerjaan.
- `authority/upstream/` memuat sumber otoritatif beku dan lisensi yang digunakan.

## Build dan pemeriksaan

Jalankan dari akar hasil ekstraksi dengan PowerShell dan Python luring:

```powershell
python -B scripts/qa-fomberg-unit-003.py
python -B scripts/validate-backend-append-only-fomberg-unit-003-cumulative.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-roberts-001-030-fomberg-001-003.ps1
```

Build memakai epoch tetap dan menghasilkan dua build HTML serta PDF yang
byte-identik. Bukti build, browser, visual, backend, dan provenance terdapat
dalam paket QA/provenans saudara pada rilis yang sama.

## Hak, atribusi, dan provenance

`LICENSE.md`, `ATTRIBUTION.md`, lisensi otoritas beku, dan
`00_control/RIGHTS_AND_COMPONENTS.csv` mempertahankan identitas dan hak setiap
lapisan secara terpisah. Pembaca terintegrasi dan lapisan baru yang memuat
komponen Fomberg tersedia di bawah CC BY-SA 4.0. Komponen Roberts-only yang
dapat dipisahkan tetap CC BY 4.0. Edisi ini independen dan tidak menyiratkan
dukungan atau afiliasi dengan penulis sumber atau institusinya. Produksi
terjemahan, restrukturisasi semantik, QA, build, dan persiapan rilis dilakukan
dengan **OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna, tanpa
menggantikan kredit penulis sumber.
