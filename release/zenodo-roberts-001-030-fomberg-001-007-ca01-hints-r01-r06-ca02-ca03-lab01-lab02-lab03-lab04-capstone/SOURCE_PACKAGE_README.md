# Paket sumber yang dapat diedit dan backend modular

Paket ini adalah sumber lengkap yang dapat dilanjutkan untuk versi `0.31.7`.
Ia memuat Roberts 30/30, Fomberg Bagian 1.1–1.13, penguasaan 108/108,
D60-LAB01–04, empat grafik perbaikan bukti, dan capstone D60.

- `source/id-ID/` memuat sumber semantik Bahasa Indonesia.
- `backend/` memuat 8.338 rekaman append-only `curriculum.interop 0.1.0`.
- `scripts/` memuat build, QA, validator, packager, dan penerbit lineage.
- `00_control/` memuat otoritas, hak, terminologi, rute, kursor, dan logbook.
- `authority/upstream/` memuat sumber otoritatif beku dan lisensinya.

Jalankan `python -B scripts/census-proof-repairs-final.py`, lalu
`python -B scripts/build-final-capstone.py`; gunakan receipt visual/browser yang
disertakan sebelum `python -B scripts/finalize-build-final-capstone.py`.
Komponen Roberts tetap CC BY 4.0; komponen Fomberg dan materi asli edisi tetap
CC BY-SA 4.0. Produksi menggunakan **OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna.
