# Paket sumber yang dapat diedit dan backend modular

Paket ini adalah sumber ringkas yang dapat dilanjutkan untuk versi `0.31.1`.
Roberts lengkap 30/30; bentang Fomberg terpilih Bagian 1.1–1.13 lengkap;
D60-CA01 lengkap 8/8; dan 36 petunjuk asli menutup kuota penguasaan biasa
84/84. Total wajib yang lengkap adalah 92/108.

Pembaca PDF, pembaca HTML, dan paket QA/provenans merupakan berkas saudara
dalam rilis yang sama dan tidak diduplikasi di ZIP ini.

## Tata letak

- `source/id-ID/` memuat sumber semantik Bahasa Indonesia, termasuk D60-CA01
  dan `ordinary-hints-r01-r06.md` sebagai lapisan asli edisi.
- `backend/` memuat 7.012 rekaman append-only dengan skema
  `curriculum.interop 0.1.0`.
- `scripts/` memuat build, QA, sensus, produsen append-only, validator, dan
  packager.
- `00_control/` memuat otoritas, terminologi, hak per komponen, rute, kursor,
  dan kontrol minimum untuk melanjutkan.
- `authority/upstream/` memuat sumber otoritatif beku dan lisensinya.

## Build dan pemeriksaan

Jalankan dari akar hasil ekstraksi:

```powershell
python -B scripts/qa-ordinary-hints-r01-r06.py
python -B scripts/validate-backend-append-only-ordinary-hints-r01-r06.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.ps1
```

Build HTML dan PDF byte-identik pada dua putaran. Paket QA saudara memuat
ikatan sumber, review independen, replay backend, audit tautan, QA browser,
dan inspeksi visual.

Komponen Roberts tetap CC BY 4.0. Komponen Fomberg, D60-CA01, petunjuk asli,
dan paket terpadu berada di bawah CC BY-SA 4.0 sebagaimana dirinci dalam
`LICENSE.md` dan `RELEASE_RIGHTS.md`. Produksi menggunakan **OpenAI Codex
gpt-5.6-sol, Ultra** atas arahan pengguna; kredit penulis sumber tetap utama.
