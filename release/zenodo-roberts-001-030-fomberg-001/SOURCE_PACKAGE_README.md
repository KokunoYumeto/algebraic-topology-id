# Paket sumber yang dapat diedit dan backend modular

Paket ini adalah sumber ringkas yang dapat dilanjutkan untuk checkpoint
*Topologi Aljabar: Edisi Bahasa Indonesia — Roberts 1–30 dan Jembatan Homologi
§1.1–1.2*, versi 0.30.1. Komponen Roberts lengkap 30/30 sampai
`Notes.tex:6368`. Komponen Fomberg saat ini mencakup
`algebraic_topology.tex:31–614` (Bagian 1.1–1.2, `O012-FOM-001`); jalur komposit
masih parsial dan kursor berikutnya adalah baris 615.

Pembaca PDF, pembaca HTML, serta paket QA/provenans merupakan berkas saudara
dalam rilis yang sama dan sengaja tidak diduplikasi di dalam ZIP ini:

- `00_TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_READER.pdf`
- `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_READER.html`
- `TOPOLOGI_ALJABAR_ID_ROBERTS_001_030_FOMBERG_001_QA_PROVENANCE.zip`

## Tata letak paket

- [`source/id-ID/reader-unit-001.md`](source/id-ID/reader-unit-001.md) dan
  unit-unit di bawah `source/id-ID/units/` memuat sumber semantik pembaca berbahasa
  Indonesia. Unit Fomberg tetap memakai identitas edisi sendiri dan tidak
  dinomori ulang sebagai Kuliah Roberts 31.
- [`backend/units.jsonl`](backend/units.jsonl) dan berkas JSONL sejawat memuat
  5.060 rekaman append-only dengan skema
  `curriculum.interop 0.1.0`; digest bundelnya
  `17f57575a062025e434e79f7f3797d05de1a41e520202521ae39a409d4b6450d`.
- [`scripts/build-roberts-001-030-fomberg-001.ps1`](scripts/build-roberts-001-030-fomberg-001.ps1)
  serta skrip sejawat memuat build pembaca dan validator unit/backend.
- [`00_control/AUTHORITY.json`](00_control/AUTHORITY.json) dan kontrol sejawat
  memuat identitas otoritas, terminologi, keputusan
  sumber, hak per komponen, dan kursor kurikulum yang diperlukan untuk
  melanjutkan pekerjaan.
- Direktori `authority/upstream/` memuat sumber otoritatif beku yang benar-benar
  digunakan pada checkpoint ini; kedua lisensinya ditautkan secara tepat di
  bawah.

## Build dan pemeriksaan

Jalankan dari akar hasil ekstraksi dengan PowerShell dan Python yang tersedia
secara luring:

```powershell
python -B scripts/qa-fomberg-unit-001.py
python -B scripts/validate-backend-append-only-fomberg-unit-001.py
python -B scripts/validate-backend-append-only-fomberg-unit-001-cumulative.py
pwsh -NoProfile -File scripts/build-roberts-001-030-fomberg-001.ps1
```

Build memakai epoch tetap dan harus menghasilkan dua build bersih yang
byte-identik. Bukti build, browser, visual, backend, dan provenans yang mengikat
checkpoint berada dalam paket QA/provenans saudara pada rilis yang sama.

## Hak, atribusi, dan provenans

- [`LICENSE.md`](LICENSE.md) menjelaskan cakupan lisensi per komponen.
- [`ATTRIBUTION.md`](ATTRIBUTION.md) mempertahankan kredit, catatan perubahan,
  dan non-pengesahan.
- Teks lisensi Roberts CC BY 4.0 dipertahankan di
  [`authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/LICENSE.md`](authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/LICENSE.md).
- Teks lisensi Fomberg CC BY-SA 4.0 dipertahankan di
  [`authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/tree/LICENSE`](authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/tree/LICENSE).
- [`00_control/RIGHTS_AND_COMPONENTS.csv`](00_control/RIGHTS_AND_COMPONENTS.csv)
  mempertahankan identitas dan hak setiap lapisan secara terpisah.

Pembaca terintegrasi dan lapisan baru yang memuat komponen Fomberg tersedia di
bawah CC BY-SA 4.0. Komponen Roberts-only yang dapat dipisahkan tetap CC BY 4.0.
Edisi ini independen dan tidak menyiratkan dukungan atau afiliasi dengan
penulis sumber atau institusinya. Produksi terjemahan, restrukturisasi semantik,
QA, build, dan persiapan rilis dilakukan dengan **OpenAI Codex gpt-5.6-sol,
Ultra** atas arahan pengguna, tanpa menggantikan kredit penulis sumber.
