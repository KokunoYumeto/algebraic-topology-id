# Paket sumber yang dapat diedit dan backend modular

Paket ini adalah sumber ringkas yang dapat dilanjutkan untuk checkpoint
*Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30 dan Jembatan Homologi,
Derajat, dan Kompleks Seluler §1.1–1.12*, versi 0.30.6. Komponen Roberts lengkap
30/30 sampai `Notes.tex:6368`. Komponen Fomberg mencakup
`algebraic_topology.tex:31–3517` (Bagian 1.1–1.12,
`O012-FOM-001–006`); jalur komposit masih parsial dan kursor berikutnya adalah
baris 3518.

Pembaca PDF, pembaca HTML, dan paket QA/provenans merupakan berkas saudara
dalam rilis yang sama dan sengaja tidak diduplikasi di dalam ZIP ini.

## Tata letak paket

- `source/id-ID/` memuat sumber semantik pembaca berbahasa Indonesia. Unit
  Fomberg mempertahankan identitas edisinya sendiri, terpisah dari 30 kuliah
  Roberts, serta membawa pemetaan rute D60-R08, D60-R09, D60-R10, D60-R11,
  dan D60-R12.
- `backend/` memuat backend append-only dengan skema `curriculum.interop
  0.1.0`. Boundary ini mempunyai 6.512 rekaman, 7.855.910 byte, dan hash bundel
  `377be644a38e6db06f8992113ea47b8fc172953254c9b1005493e0ad3b7bd4ad`.
- `scripts/` memuat build pembaca, QA unit, produsen append-only, dan validator.
- `00_control/` memuat identitas otoritas, terminologi, keputusan sumber, hak
  per komponen, dan rute kurikulum yang diperlukan untuk melanjutkan pekerjaan.
- `authority/upstream/` memuat sumber otoritatif beku dan lisensi yang digunakan.

## Build dan pemeriksaan

Jalankan dari akar hasil ekstraksi dengan PowerShell dan Python luring:

```powershell
python -B scripts/qa-fomberg-unit-006.py
python -B scripts/validate-backend-append-only-fomberg-unit-006-cumulative.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-roberts-001-030-fomberg-001-006.ps1
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
