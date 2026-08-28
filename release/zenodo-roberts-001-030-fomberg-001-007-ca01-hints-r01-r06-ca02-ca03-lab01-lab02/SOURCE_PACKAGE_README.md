# Paket sumber yang dapat diedit dan backend modular

Paket ini adalah sumber ringkas yang dapat dilanjutkan untuk versi `0.31.4`.
Roberts lengkap 30/30; bentang Fomberg terpilih Bagian 1.1–1.13 lengkap;
D60-CA01/02/03 lengkap 24/24; lapisan petunjuk asli menutup kuota penguasaan
biasa 84/84; total penguasaan berbasis solusi lengkap 108/108; dan
D60-LAB01–02 lengkap 2/4.

Pembaca PDF, pembaca HTML, dan paket QA/provenans merupakan berkas saudara
dalam rilis yang sama dan tidak diduplikasi di ZIP ini.

## Tata letak

- `source/id-ID/` memuat sumber semantik Bahasa Indonesia, termasuk ketiga
  asesmen kumulatif, lapisan petunjuk, serta pembaca/program/uji/keluaran
  D60-LAB01 dan D60-LAB02 sebagai materi asli edisi.
- `backend/` memuat 7.546 rekaman append-only dengan skema
  `curriculum.interop 0.1.0`.
- `scripts/` memuat build, QA, sensus, produsen append-only, validator,
  finalizer, packager, dan penerbit lineage.
- `00_control/` memuat otoritas, terminologi, hak per komponen, rute, kursor,
  dan kontrol minimum untuk melanjutkan.
- `authority/upstream/` memuat sumber otoritatif beku dan lisensinya.

## Build dan pemeriksaan

Jalankan dari akar hasil ekstraksi:

```powershell
python -B scripts/qa-computation-lab-002.py
python -B scripts/validate-backend-append-only-computation-lab-002.py
python -B scripts/build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02.py
python -B scripts/finalize-build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02.py
```

Build HTML, appendix PDF, dan PDF gabungan byte-identik pada dua putaran. Paket
QA saudara memuat ikatan sumber, review independen, replay backend, audit
tautan, QA browser, inspeksi visual, dan sensus 108/108.

Komponen Roberts tetap CC BY 4.0. Komponen Fomberg, D60-CA01/02/03,
D60-LAB01/02, petunjuk asli, dan paket terpadu berada di bawah CC BY-SA 4.0
sebagaimana dirinci dalam `LICENSE.md` dan `RELEASE_RIGHTS.md`. Produksi
menggunakan **OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna; kredit
penulis sumber tetap utama.

