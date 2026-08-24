# Paket sumber yang dapat diedit dan backend modular

Paket ini adalah sumber ringkas yang dapat dilanjutkan untuk checkpoint
*Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30 dan Jembatan Homologi
§1.1–1.4*, versi 0.30.2. Komponen Roberts lengkap 30/30 sampai
`Notes.tex:6368`. Komponen Fomberg mencakup
`algebraic_topology.tex:31–1290` (Bagian 1.1–1.4, `O012-FOM-001–002`); jalur
komposit masih parsial dan kursor berikutnya adalah baris 1291.

Pembaca PDF, pembaca HTML, dan paket QA/provenans merupakan berkas saudara
dalam rilis yang sama dan sengaja tidak diduplikasi di dalam ZIP ini.

## Tata letak paket

- `source/id-ID/` memuat sumber semantik pembaca berbahasa Indonesia. Unit
  Fomberg mempertahankan identitas edisinya sendiri dan tidak dinomori ulang
  sebagai Kuliah Roberts 31–32.
- `backend/` memuat 5.342 rekaman append-only dengan skema
  `curriculum.interop 0.1.0`; digest bundelnya
  `83d98f1b271c5e62334a072354f1be1c4a1535ed26c8a403223e89773bb1eba1`.
- `scripts/` memuat build pembaca, QA unit, produsen append-only, dan validator.
- `00_control/` memuat identitas otoritas, terminologi, keputusan sumber, hak
  per komponen, dan rute kurikulum yang diperlukan untuk melanjutkan pekerjaan.
- `authority/upstream/` memuat sumber otoritatif beku dan lisensi yang digunakan.

## Build dan pemeriksaan

Jalankan dari akar hasil ekstraksi dengan PowerShell dan Python luring:

```powershell
python -B scripts/qa-fomberg-unit-002.py
python -B scripts/validate-backend-append-only-fomberg-unit-002.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-roberts-001-030-fomberg-001-002.ps1
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
