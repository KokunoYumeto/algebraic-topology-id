# Tinjauan independen Unit 15

Tanggal tinjauan: 22 Agustus 2026  
Status: **LULUS; P1 = 0, P2 = 0, P3 = 0 yang masih terbuka**

## Identitas beku

- Sumber: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`, baris 3210--3286 (inklusif). Baris 3287, awal Kuliah 16, tidak termasuk.
- Commit hulu: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- `Notes.tex`: 331.447 byte; 6.368 baris; SHA-256 `cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7`.
- Unit yang ditinjau: `source/id-ID/units/unit-015-lecture-015.md`.
- Unit final: **28.485 byte; 835 baris; SHA-256 `140f1dbc182b5406dbbdadde59bb6dcdf51f86bd6cf4c50c676e0b88d60540f4`**.

## Penutupan sumber dan semantik

Sensus sumber lengkap: penanda Kuliah 15; 2 lema; 2 bukti; 2 contoh; 1 catatan; 1 pertanyaan; 6 lingkungan matematika tampil; 2 diagram Xy-pic vertikal; dan 3 catatan pinggir. Seluruh prosa penghubung, faktorisasi funktor serat, dekomposisi ruang penutup, contoh lingkaran, peta surjektif serat, identifikasi orbit, reduksi ke aksi transitif, contoh torsor, dan pertanyaan realisasi subgrup hadir dalam urutan sumber.

Kedua diagram Xy-pic direflow menjadi Diagram 15.1--15.2 yang dapat dibaca tanpa gambar dan menyatakan ruang total, ruang basis, serta arah panah. Ketiga catatan pinggir masuk ke alur utama: syarat basis lingkungan, latihan komponen ruang total beserta buktinya, dan pengingat hasil-bagi aksi grup dengan hipotesis aksi penutup yang benar. Tidak ada aset eksternal.

Tujuh pemeriksaan penguasaan mempunyai tujuh solusi lengkap dan tetap berada di sisi aman batas sumber. Yang sengaja ditunda dinyatakan tepat: keberadaan penutup terhubung sederhana/universal; kelengkapan daftar penutup lingkaran; realisasi subgrup atau semua aksi transitif; surjektivitas esensial; serta kepenuhan dan kesetiaan funktor monodromi.

## Disposisi P1/P2/P3

P1 yang telah diperbaiki dan diverifikasi:

1. Salah ketik `in_j^*X` menjadi `in_j^*Z = X_j\times_X Z`.
2. Dengan produk loop kronologis, transpor langsung konsisten sebagai aksi kanan; semua orbit bertitik memakai koset kanan `H\backslash G`, bukan `G/H`.
3. Semua grup fundamental ruang total yang diperlakukan sebagai subgrup ditulis melalui citra `p_*\pi_1(Z,z)`.
4. Bukti orbit juga membuktikan `Stab_G(z)=p_*\pi_1(Z,z)` melalui kriteria pengangkatan tertutup.
5. Catatan hasil-bagi mensyaratkan aksi penutup (bukan kebebasan topologis saja).

P2 yang telah diperbaiki dan diverifikasi: asumsi terhubung dan SLSC versi mata kuliah dinyatakan; keterbukaan komponen, keterhubungan lintasan, dan kesurjektifan pembatasan dibuktikan; argumen kategori, produk, orbit, dan torsor lengkap; serta batas hasil kemudian tidak dilompati. Tinjauan final menutup dua celah bukti tambahan: lingkungan yang diliputi merata terlebih dahulu diperhalus menjadi lingkungan terhubung lintasan sebelum lembar digunakan, dan bukti penstabil kini membedakan kesamaan kelas homotopi dari kesamaan wakil loop.

P3 yang telah diperbaiki dan diverifikasi: indeks komponen basis dan ruang total dibedakan; contoh lingkaran mengizinkan banyak salinan sebarang untuk setiap derajat; notasi koproduk, kategori, dan titik basis yang cacat diperbaiki; 2 diagram serta 3 catatan pinggir direflow secara aksesibel. Tinjauan final juga mengganti frasa tidak alami “pada titik sumber 3239” dengan “sampai baris 3239 pada sumber”. Tidak ditemukan kebocoran prosa Inggris.

## Validasi mekanis

- 34 pengenal stabil didefinisikan, semuanya unik.
- 19 fenced-div pembuka dan 19 penutup; seimbang.
- 7 latihan penguasaan dan 7 judul solusi; lengkap satu-ke-satu.
- Dua antarmuka masuk Unit 14, `o012-rbt-l14-eq-fibre-functor` dan `o012-rbt-l14-rem-001`, benar-benar terdefinisi pada Unit 14; tidak ada rujukan fragmen lokal yang hilang.
- Pandoc 3.9.0.2, parser Markdown ke native dengan `--fail-if-warnings`: exit 0.
- Pandoc HTML5 mandiri dengan MathML dan `--fail-if-warnings`: exit 0.
- Pencarian terbatas atas prosa Inggris dan penyebutan TTP: tidak menemukan pelanggaran.

## Asal-usul materi

Terjemahan/adaptasi menunjuk langsung ke Roberts dan CC BY 4.0 pada unit. Tambahan penguasaan diberi `data-origin="edition-original"` dan dinyatakan sebagai karya asli edisi. Tinjauan perbandingan menunjukkan tidak ada kutipan, solusi, diagram gambar, atau materi pihak ketiga tanpa atribusi. Pernyataan non-endorsement tetap eksplisit.
