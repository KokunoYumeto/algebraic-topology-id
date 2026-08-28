---
title: "Laboratorium Komputasi 1 — Monodromi Ruang Penutup dan Presentasi Grup"
lang: id-ID
course_id: "D60"
laboratory_id: "D60-LAB01"
license: "CC BY-SA 4.0"
edition_unit_id: "O012-ORIG-LAB01"
course_route_unit_ids: ["D60-R04", "D60-R05", "D60-R06"]
origin: "Materi asli edisi; bukan bagian dari sumber Roberts atau Fomberg."
model_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
---

# Laboratorium Komputasi 1 — Monodromi Ruang Penutup dan Presentasi Grup {#o012-d60-lab01}

## Status dan keluaran laboratorium {#o012-d60-lab01-status}

Laboratorium ini adalah materi asli edisi. Ia menghubungkan tiga sudut pandang
yang mudah tercampur bila hanya dihitung dengan tangan:

1. aksi monodromi kanan pada serat suatu penutup graf;
2. citra hingga aksi tersebut sebagai grup permutasi;
3. subgrup stabilisator yang isomorfik dengan grup fundamental ruang atas.

Semua perhitungan memakai pustaka standar Python saja dan dapat dijalankan
tanpa jaringan. Paket laboratorium memuat program, enam uji deterministik,
keluaran acuan, interpretasi matematis, dan solusi lengkap. Kode tidak
menggantikan pembuktian: keluaran program menjadi data yang kemudian
dijustifikasi dengan orbit--stabilisator, presentasi grup, dan argumen pohon
merentang.

## Prasyarat yang dipakai {#o012-d60-lab01-prerequisites}

- aksi monodromi kanan dan urutan kronologis kata:
  [Kuliah 7](#o012-rbt-l07-s03);
- serat sebagai ruang koset kanan dan subgrup stabilisator:
  [Teorema 9.2](#o012-rbt-l09-thm-002);
- penutup graf berhingga sebagai daftar transisi berlabel:
  [penutup tiga lembaran](#o012-rbt-l10-s03);
- grup bebas pada dua pembangkit: [Kuliah 11](#o012-rbt-l11-s01);
- presentasi grup dan kompleks presentasi:
  [Kuliah 13](#o012-rbt-l13-s05).

## Tujuan {#o012-d60-lab01-objectives}

Sesudah menyelesaikan laboratorium ini, pembaca dapat:

1. memeriksa apakah dua baris transisi benar-benar mendefinisikan penutup
   graf berhingga;
2. menghitung orbit serat dan memutuskan keterhubungan ruang atas;
3. mengenali citra monodromi dari relasi permutasinya;
4. membangun transversal Schreier deterministik dan basis bebas subgrup
   stabilisator;
5. membedakan presentasi **citra monodromi** dari presentasi
   **grup fundamental ruang penutup**;
6. mengikat klaim tersebut pada uji dan keluaran yang dapat direproduksi.

## Konvensi kata dan aksi kanan {#o012-d60-lab01-conventions}

Tuliskan

$$
X=S^1_a\vee S^1_b,
\qquad
\pi_1(X,*)\cong F(a,b).
$$

Huruf kapital menyatakan invers:

$$
A=a^{-1},
\qquad
B=b^{-1}.
$$

Kata dibaca dari kiri ke kanan sebagai urutan perjalanan. Jika $R_w$ adalah
operator titik akhir pada serat, maka

$$
R_{uv}=R_v\circ R_u.
$$

Jadi program menerapkan huruf pertama lebih dahulu. Ini adalah aksi kanan
langsung, bukan homomorfisma kiri ke grup permutasi dengan konvensi komposisi
fungsi biasa. Bila homomorfisma kiri diperlukan, gunakan
$\rho(g)=R_{g^{-1}}$ seperti pada pembaca utama.

## Data penutup empat lembaran {#o012-d60-lab01-data}

Serat di atas titik baji adalah

$$
S=\{0,1,2,3\}.
$$

Tabel transisi positifnya ialah

$$
\begin{array}{c|cccc}
s&0&1&2&3\\ \hline
s\mathbin{\cdot}a&1&2&3&0\\
s\mathbin{\cdot}b&0&3&2&1.
\end{array}
$$

Dengan notasi siklus,

$$
R_a=(0\ 1\ 2\ 3),
\qquad
R_b=(1\ 3).
$$

Setiap baris adalah permutasi. Karena itu dari setiap simpul terdapat tepat
satu sisi keluar dan satu sisi masuk untuk setiap label $a$ dan $b$; inilah
syarat lokal penutup graf. Terdapat empat pengangkatan berorientasi positif dari setiap
sel-$1$ dasar, sehingga graf ruang atas mempunyai $4$ simpul dan $8$ sisi
geometris berorientasi positif. Fakta bahwa $R_b$ suatu involusi dalam
**citra permutasi** tidak mengidentifikasi sisi positif $b$ dengan sisi
baliknya di grup bebas.

::: {.exercise #o012-d60-lab01-task-001}
**Tugas 1 — jalankan bukti komputasional.** Dari akar repositori, jalankan

```text
python -B source/id-ID/labs/test_o012_d60_lab01_monodromy.py
python -B source/id-ID/labs/o012_d60_lab01_monodromy.py
```

Pastikan keenam uji lulus dan keluaran program sama byte demi byte dengan
`expected-output-lab01.txt`.
:::

::: {.exercise #o012-d60-lab01-task-002}
**Tugas 2 — orbit, keterhubungan, dan citra.** Hitung orbit lembaran $0$.
Daftarkan semua permutasi dalam citra monodromi. Periksa bahwa kata
$a^4$, $b^2$, dan $baba$ bertindak trivial.
:::

::: {.exercise #o012-d60-lab01-task-003}
**Tugas 3 — presentasi citra.** Buktikan bahwa citra monodromi mempunyai
presentasi

$$
\langle a,b\mid a^4,\ b^2,\ baba\rangle
$$

dan isomorfik dengan grup dihedral berorde $8$. Jelaskan mengapa presentasi
ini bukan presentasi $F(a,b)$ dan tidak langsung memberikan presentasi grup
fundamental ruang atas.
:::

::: {.exercise #o012-d60-lab01-task-004}
**Tugas 4 — transversal dan basis bebas.** Mulai pada lembaran $0$ dan
lakukan pencarian lebar-pertama dengan urutan huruf $a,A,b,B$. Untuk setiap
lembaran $s$, catat kata transversal $t_s$. Kemudian hitung kata

$$
t_sx\,t_{s\cdot x}^{-1}
\qquad
(s\in S,\ x\in\{a,b\}),
$$

reduksi bebas, dan buang kata identitas. Verifikasi bahwa lima kata sisanya
memperbaiki lembaran $0$.
:::

::: {.exercise #o012-d60-lab01-task-005}
**Tugas 5 — presentasi ruang atas.** Gunakan pohon merentang yang tersirat
oleh transversal untuk menghitung rank grup fundamental graf ruang atas.
Tuliskan presentasi bebasnya dan hubungkan grup itu dengan stabilisator
$\operatorname{Stab}_{F(a,b)}(0)$.
:::

::: {.exercise #o012-d60-lab01-task-006}
**Tugas 6 — uji negatif.** Ganti transisi dengan

$$
R_a=(0\ 1)(2\ 3),
\qquad
R_b=\operatorname{id}.
$$

Prediksikan dekomposisi orbit sebelum menjalankan uji. Jelaskan mengapa rutin
pembentuk basis bebas laboratorium menolak data ini sebagai satu penutup terhubung,
meskipun kedua baris tetap merupakan permutasi yang sah.
:::

::: {.hint #o012-d60-lab01-hint}
**Petunjuk.** Orbit $0$ sudah memuat $1,2,3$ dengan mengulang $a$. Untuk
presentasi citra, ubah $baba=1$ menjadi $bab=a^{-1}$ dan dorong setiap $b$
ke satu sisi kata. Untuk subgrup ruang atas, jangan memakai relasi $b^2=1$:
relasi itu berlaku pada citra permutasi, bukan pada grup bebas dasar. Pembangkit
Schreier yang tersisa akan membentuk basis bebas. Pohon
merentang mempunyai $V-1$ sisi, sedangkan graf mempunyai $8$ sisi positif.
:::

## Program lengkap {#o012-d60-lab01-program}

Berkas kanonis:
[`o012_d60_lab01_monodromy.py`](o012_d60_lab01_monodromy.py).
Proses pembuatan pembaca mengganti penanda berikut dengan byte sumber tersebut agar
HTML dan PDF tetap mandiri dan agar salinan tampilan tidak dapat menyimpang
dari berkas yang diuji.

O012_LAB01_INCLUDE_PROGRAM

## Uji deterministik lengkap {#o012-d60-lab01-tests}

Berkas kanonis:
[`test_o012_d60_lab01_monodromy.py`](test_o012_d60_lab01_monodromy.py).

O012_LAB01_INCLUDE_TESTS

## Keluaran acuan {#o012-d60-lab01-expected-output}

Berkas kanonis:
[`expected-output-lab01.txt`](expected-output-lab01.txt).

O012_LAB01_INCLUDE_EXPECTED

## Membaca keluaran tanpa menyamakan tiga grup {#o012-d60-lab01-interpretation}

Tiga grup yang muncul adalah:

1. grup dasar $F(a,b)=\pi_1(X,*)$;
2. citra permutasi $\operatorname{im}(\rho)$, yang berorde $8$, untuk
   homomorfisma $\rho(g)=R_{g^{-1}}$;
3. stabilisator
   $H=\operatorname{Stab}_{F(a,b)}(0)$, yang berindeks $4$ dan isomorfik
   dengan $\pi_1(Z,0)$.

Citra adalah hasil bagi $F(a,b)/\ker\rho$. Kumpulan operator yang diperoleh
sama dengan kumpulan operator aksi kanan langsung $R$; mengambil invers hanya
memperbaiki arah komposisi. Stabilisator adalah subgrup, bukan hasil bagi itu.
Karena $b$ memperbaiki lembaran $0$, kata $b$ berada di $H$;
namun $b$ tetap berorde tak hingga di grup bebas $F(a,b)$. Hanya bayangannya
di citra permutasi yang memenuhi $b^2=1$. Pemisahan ini adalah pemeriksaan
konseptual utama laboratorium.

# Solusi lengkap {#o012-d60-lab01-solution}

## Orbit dan citra monodromi {#o012-d60-lab01-sol-monodromy}

Pengulangan $a$ memberi

$$
0\xrightarrow{a}1\xrightarrow{a}2\xrightarrow{a}3
\xrightarrow{a}0.
$$

Jadi orbit $0$ adalah seluruh $S$. Orbit aksi monodromi sama dengan komponen
lintasan ruang atas; penutup ini terhubung. Pendaftaran semua unsur melalui
penutupan di bawah
$a,A,b,B$ menghasilkan delapan permutasi.

Secara langsung $R_a^4=1$ dan $R_b^2=1$. Refleksi $R_b$ membalik siklus
$R_a$, sehingga

$$
R_bR_aR_b=R_a^{-1}.
$$

Dalam urutan kata aksi kanan, kata `baba` juga memberi operator identitas.
Program menguji ketiga relator titik demi titik pada seluruh serat, bukan
hanya pada lembaran $0$.

## Presentasi citra {#o012-d60-lab01-sol-image-presentation}

Dari relasi $baba=1$ diperoleh $ba=a^{-1}b$. Dengan relasi ini, setiap kata
dalam grup yang dipresentasikan dapat ditulis sebagai

$$
a^i b^j,
\qquad
0\le i<4,
\quad
j\in\{0,1\}.
$$

Jadi grup yang dipresentasikan mempunyai paling banyak delapan unsur. Permutasi
$R_a,R_b$ menghasilkan delapan unsur yang berbeda, sehingga homomorfisma dari
grup yang dipresentasikan ke citra adalah surjektif antara dua grup berukuran delapan dan
karena itu isomorfisma. Inilah grup dihedral simetri persegi.

Argumen tersebut tidak menambahkan relasi ke $F(a,b)$. Ia hanya menghitung
hasil bagi yang terlihat oleh aksi empat lembaran ini. Secara khusus,
$F(a,b)$ tetap tak hingga dan bebas.

## Transversal, pembangkit Schreier, dan basis bebas {#o012-d60-lab01-sol-schreier}

Pencarian lebar-pertama dengan urutan $a,A,b,B$ memilih

$$
t_0=1,
\qquad
t_1=a,
\qquad
t_2=aa,
\qquad
t_3=A.
$$

Delapan calon pembangkit Schreier adalah sebagai berikut. Kolom terakhir sudah
direduksi bebas.

$$
\begin{array}{c|c|c|c|c}
s&x&s\mathbin{\cdot}x&t_{s\cdot x}&t_sx t_{s\cdot x}^{-1}\\ \hline
0&a&1&a&1\\
0&b&0&1&b\\
1&a&2&aa&1\\
1&b&3&A&aba\\
2&a&3&A&aaaa\\
2&b&2&aa&aabAA\\
3&a&0&1&1\\
3&b&1&a&AbA
\end{array}
$$

Tiga kata identitas adalah sisi pohon merentang. Lima kata nontrivial

$$
b,
\quad aba,
\quad aaaa,
\quad aabAA,
\quad AbA
$$

semuanya memperbaiki lembaran $0$, sebagaimana diperiksa program.

Graf terhubung mempunyai $V=4$ simpul dan $E=8$ sisi positif. Maka

$$
\operatorname{rank}\pi_1(Z,0)=E-V+1=8-4+1=5.
$$

Mengontraksikan pohon merentang meninggalkan lima loop bebas, tepat lima kata
Schreier di atas. Jadi

$$
\pi_1(Z,0)
\cong
H=\operatorname{Stab}_{F(a,b)}(0)
\cong F_5
$$

dengan presentasi

$$
\langle b,\ aba,\ aaaa,\ aabAA,\ AbA\mid\ \rangle.
$$

Kesamaan dengan stabilisator memakai Teorema 9.2 dan injektivitas pemetaan
grup fundamental yang diinduksi suatu ruang penutup.

## Uji negatif dan arti kegagalan {#o012-d60-lab01-sol-negative}

Untuk data uji negatif, $a$ menukar $0$ dengan $1$ dan menukar $2$ dengan
$3$, sedangkan $b$ tidak memindahkan lembaran. Orbitnya adalah

$$
\{0,1\},
\qquad
\{2,3\}.
$$

Data uji itu masih mendefinisikan penutup empat lembaran, tetapi ruang atasnya
mempunyai dua komponen. Rutin `schreier_basis(0)` sengaja menolak permintaan
basis tunggal bagi seluruh graf: transversal dari $0$ hanya mencapai komponen
pertama. Masing-masing komponen dapat dianalisis sendiri dengan titik basisnya.

## Pemeriksaan reproduktibilitas {#o012-d60-lab01-reproducibility}

Uji otomatis memeriksa:

1. tabel transisi bijektif dan operator invers benar;
2. reduksi bebas serta penolakan huruf kata yang tidak sah;
3. orbit terhubung, orde citra, dan ketiga relator;
4. transversal, lima pembangkit Schreier, dan rumus rank;
5. setiap pembangkit basis memperbaiki lembaran $0$;
6. data uji dua orbit ditolak oleh rutin yang mensyaratkan transitivitas;
7. keluaran CLI sama byte demi byte dengan keluaran acuan UTF-8 berakhiran LF.

Dengan demikian keluaran bukan tangkapan layar atau hasil yang diketik ulang:
ia terikat pada kode yang sama dengan kode yang disajikan dalam pembaca.

## Hak, atribusi, dan provenans {#o012-d60-lab01-rights}

Laboratorium, program, uji, keluaran acuan, interpretasi, dan solusi ini adalah
materi asli edisi dan didistribusikan di bawah CC BY-SA 4.0. Materi ini
menggunakan hasil matematika yang sudah dikembangkan dalam edisi Roberts dan
lapisan rute komposit, tetapi tidak menyalin ekspresi dari bank masalah yang
dikecualikan. Produksi dilakukan dengan **OpenAI Codex gpt-5.6-sol, Ultra**
atas arahan pengguna. Kredit, lisensi, dan hubungan sumber David Michael
Roberts serta Yeheli Fomberg tetap dibedakan; laboratorium ini tidak menyiratkan
dukungan atau pengesahan dari penulis sumber.
