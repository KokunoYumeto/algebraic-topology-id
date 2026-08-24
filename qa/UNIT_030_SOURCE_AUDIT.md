# Audit sumber Unit 30 — Kuliah 30 Roberts

## Otoritas dan batas

- Repositori resmi: `DavidMichaelRoberts/AlgebraicTopology2019`.
- Commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Tree: `aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5`.
- Berkas: `Notes.tex`.
- Rentang aktif: baris fisik **6271–6368**, inklusif. Baris 6271 memuat
  `\lecturenum{30}` di tengah kalimat; baris 6368 adalah `\end{document}`.
  Tidak ada sumber setelah baris itu.
- Rentang aktif terdiri atas **98 baris**. Setelah digabung dengan LF dan satu
  terminator LF penutup dipertahankan, rentang berukuran **8.290 byte** UTF-8
  dengan SHA-256
  `c522b5ec0ba7d4c938be6588a070be648263d841e1db4f9905c9b388619b64b1`.
- Berkas otoritas lengkap berukuran 331.447 byte dan 6.368 baris, dengan
  SHA-256
  `cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7`.
- Lisensi komponen sumber: CC BY 4.0.

## Sensus literal

Rentang memuat satu penanda kuliah, tiga teorema, satu definisi, satu lema,
satu korolari, satu catatan, tiga lingkungan bukti, satu daftar empat butir,
enam catatan pinggir, satu catatan sisi, satu gambar TikZ, satu label, dan satu
rujukan silang. Tidak ada latihan atau pertanyaan formal sumber, diagram
Xy-pic, gambar eksternal, perintah `\cite`, `input`, ataupun `include`. Ada
dua rujukan bibliografis tekstual kepada Hatcher.

Selain definisi formal derajat, prosa sumber juga mendefinisikan secara
eksplisit fungsi-diri *bebas* sebagai fungsi-diri tanpa titik tetap. Edisi
mempromosikan definisi inline itu menjadi objek semantik tanpa mengubah
statusnya sebagai materi sumber.

## Penutupan semantik dan koreksi wajib

1. **`UNIT030-SRC-001`, Notes.tex:6273 — contoh banyak titik tetap
   diperbaiki.** Baris 6273 menyatakan bahwa fungsi
   yang konstan pada suatu daerah kecil mempunyai banyak titik tetap. Fungsi
   konstan mempunyai paling banyak satu titik tetap pada daerah itu. Contoh
   yang benar ialah fungsi yang sama dengan identitas pada daerah tersebut;
   itulah formulasi edisi.
2. **`UNIT030-SRC-002`, Notes.tex:6279–6297 — hipotesis kontradiksi dan
   retraksi ditulis lengkap.** Bukti Brouwer baru
   dapat mendefinisikan $g_f$ setelah mengandaikan bahwa $f$ bebas, sehingga
   $x-f(x)\neq0$. Edisi memberi rumus perpotongan sinar
   $f(x)+t(x-f(x))$ dengan $S^{n-1}$, membuktikan kontinuitasnya dari rumus,
   dan memeriksa $g_f|_{S^{n-1}}=\mathrm{id}$. Gambar TikZ sumber direflow
   sebagai tiga titik terurut dan sinar berarah yang tetap dapat dibaca tanpa
   kanvas tetap.
3. **`UNIT030-SRC-003`, Notes.tex:6297–6301 — bukti Brouwer memakai kohomologi
   tereduksi dan arah kontravarian yang benar.** Sumber menulis
   `H^(n-1)(S^(n-1)) --i*--> H^(n-1)(D^n) --g_f*--> ...`.
   Untuk $i:S^{n-1}\to D^n$ dan $g_f:D^n\to S^{n-1}$, arah yang benar ialah
   `H~(S) --g_f*--> H~(D) --i*--> H~(S)`. Tilde wajib untuk $n=1$, sebab
   $H^0(D^1;Z)\neq0$ tetapi $\widetilde H^0(D^1;Z)=0$. Kasus $n=0$ ditutup
   langsung karena $D^0$ singleton.
4. **`UNIT030-SRC-004`, Notes.tex:6308 — karakterisasi medan tertutup-real
   dilengkapi.** Catatan baris 6308 hanya
   menyebut keterurutan dan akar bagi polinom berderajat ganjil. Karakterisasi
   standar juga mensyaratkan setiap elemen positif merupakan kuadrat. Edisi
   memuat ketiga syarat sebelum menyatakan bahwa $k[\sqrt{-1}]$ tertutup
   aljabar.
5. **`UNIT030-SRC-005`, Notes.tex:6314–6316 — pendekatan pada bukti teorema
   dasar aljabar dibuat kuantitatif.** Simbol
   informal `p_R≈R^ne^{inθ}` diganti dengan pilihan
   `Σ_{j<n}|a_j|R^j<R^n`. Homotopi garis lurus lalu tetap di $\mathbb C^×$
   menurut pertaksamaan segitiga terbalik. Kata sumber “contraction” pada akhir
   argumen diperbaiki menjadi “contradiction”.
6. **`UNIT030-NOTE-001`, Notes.tex:6318 — makna translasi grup dibuat
   eksplisit.** “Translating the unit tangent vector at 1” benar jika yang
   dimaksud ialah translasi kiri pada grup lingkaran. Secara koordinat tindakan
   itu sama dengan rotasi dan menghasilkan rumus sumber
   $v(x,y)=(-y,x)$. Edisi memakai rumus tersebut untuk menghindari salah baca
   sebagai translasi Euclidean; tidak ada perubahan matematika.
7. **`UNIT030-SRC-007`, Notes.tex:6324–6325 — sfera satuan serat singgung tidak
   disamakan dengan $S^n$.** Sfera satuan
   dalam $T_xS^n$ berdimensi $n-1$, bukan $n$. Medan satuan tetap dapat dilihat
   sebagai fungsi $v:S^n\to S^n$ ke sfera satuan **ambien**, dengan syarat
   $v(x)\cdot x=0$. Perbedaan serat dan target ambien dinyatakan eksplisit.
8. **`UNIT030-SRC-008`, Notes.tex:6325–6329 — derajat memakai kohomologi
   tereduksi.** Sumber menulis
   $H^n(S^n;\mathbb Z)\cong\mathbb Z$, yang gagal pada $n=0$ karena
   $H^0(S^0;\mathbb Z)\cong\mathbb Z^2$. Edisi memakai
   $\widetilde H^n(S^n;\mathbb Z)\cong\mathbb Z$ untuk semua $n\geq0$ dan
   memilih generator orientasi standar. Untuk $n\geq1$ ini bersepakat dengan
   kohomologi biasa pada derajat positif.
9. **`UNIT030-SRC-009`, Notes.tex:6358–6362 — konstruksi medan berdimensi
   ganjil diperbaiki.** Koordinat terakhir pada baris 6360, `x_{2k=1}`, adalah
   salah ketik untuk `x_{2k-1}`. Baris 6362
   mengklaim $v(x)\cdot x=1$; nilai yang benar adalah $0$, sedangkan
   $\|v(x)\|=1$. Edisi memeriksa kedua identitas pasangan demi pasangan.
10. **`UNIT030-SRC-010`, Notes.tex:6297, 6301, 6324, 6351, 6356 — normalisasi
     salah ketik.** `funtor`, `so such`, `Sinc`, dan frasa terpotong “vector
     field on has” dinormalkan menjadi `fungtor`, “no such”, “Since”, dan
     kalimat lengkap. Notasi salah `\S^n` diganti dengan `S^n`.
11. **`UNIT030-ED-P2-001`, solusi Pemeriksaan 30.4 — perkalian skalar
    diperjelas.** Draf pembaca menulis hasil komposisi pada generator sebagai
    `ed,u`, yang dapat terbaca sebagai daftar atau tanda baca di dalam rumus.
    Edisi final menulis `(ed)u`, sesuai
    $(g\circ f)^*=f^*\circ g^*$ dan
    $f^*(g^*(u))=f^*(eu)=e f^*(u)=(ed)u$. Ini adalah koreksi P2 yang
    diselesaikan sebelum admisi; arah peta dan hasil derajat tidak berubah.

## Bukti dan batas rujukan

Pembuktian Brouwer dan teorema dasar aljabar ditutup secara mandiri. Sumber
secara sengaja memberikan lema derajat refleksi tanpa bukti dan dua kali
menunjuk Hatcher; edisi mempertahankan provenance itu dan memberi konsekuensi
antipodal secara lengkap, tetapi tidak mengklaim bahwa perhitungan triangulasi
Hatcher berasal dari edisi. Catatan orientasi melalui kohomologi de Rham tetap
berada dalam urutan bacaan.

## Lapisan penguasaan edisi

Karena tidak ada latihan sumber, pembaca menambahkan enam pemeriksaan
penguasaan dengan petunjuk dan solusi lengkap: retraksi eksplisit pada bukti
Brouwer; kohomologi tereduksi dan arah peta; homotopi lingkaran dalam teorema
dasar aljabar; sifat derajat dan peta antipodal; obstruksi medan pada dimensi
genap; serta konstruksi medan pada dimensi ganjil. Semua tambahan dilabeli
sebagai materi asli edisi di bawah CC BY 4.0.

## Putusan audit

`ADMISSIBLE_AFTER_REPAIR`. Semua isi Notes.tex baris 6271–6368 dapat
diterjemahkan secara kontigu setelah koreksi di atas. Kursor sesudah unit ialah
**EOF setelah baris 6368** (posisi nominal berikutnya: baris 6369); tidak ada
Kuliah 31 dalam sumber beku.
