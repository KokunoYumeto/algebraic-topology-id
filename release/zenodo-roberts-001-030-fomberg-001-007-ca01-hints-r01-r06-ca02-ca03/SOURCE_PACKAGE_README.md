# Paket sumber yang dapat diedit dan backend modular

Paket ini adalah sumber ringkas yang dapat dilanjutkan untuk versi `0.31.2`.
Roberts lengkap 30/30; bentang Fomberg terpilih Bagian 1.1–1.13 lengkap;
D60-CA01, D60-CA02, dan D60-CA03 lengkap 24/24; dan lapisan petunjuk asli
menutup kuota penguasaan biasa 84/84. Total penguasaan berbasis solusi yang
lengkap adalah 108/108.

Pembaca PDF, pembaca HTML, dan paket QA/provenans merupakan berkas saudara
dalam rilis yang sama dan tidak diduplikasi di ZIP ini.

## Tata letak

- `source/id-ID/` memuat sumber semantik Bahasa Indonesia, termasuk ketiga
  asesmen kumulatif dan `ordinary-hints-r01-r06.md` sebagai lapisan asli edisi.
- `backend/` memuat 7.273 rekaman append-only dengan skema
  `curriculum.interop 0.1.0`.
- `scripts/` memuat build, QA, sensus, produsen append-only, validator,
  finalizer, packager, dan penerbit lineage.
- `00_control/` memuat otoritas, terminologi, hak per komponen, rute, kursor,
  dan kontrol minimum untuk melanjutkan.
- `authority/upstream/` memuat sumber otoritatif beku dan lisensinya.

## Build dan pemeriksaan

Jalankan dari akar hasil ekstraksi:

```powershell
python -B scripts/qa-cumulative-assessments-002-003.py
python -B scripts/validate-backend-append-only-cumulative-assessments-002-003.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03.ps1
python -B scripts/finalize-build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03.py
```

Build HTML dan PDF byte-identik pada dua putaran. Paket QA saudara memuat
ikatan sumber, review independen, replay backend, audit tautan, QA browser,
inspeksi visual, dan sensus 108/108.

Komponen Roberts tetap CC BY 4.0. Komponen Fomberg, D60-CA01, D60-CA02,
D60-CA03, petunjuk asli, dan paket terpadu berada di bawah CC BY-SA 4.0
sebagaimana dirinci dalam `LICENSE.md` dan `RELEASE_RIGHTS.md`. Produksi
menggunakan **OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna; kredit
penulis sumber tetap utama.
