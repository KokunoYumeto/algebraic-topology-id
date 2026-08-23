---
title: "Topologi Aljabar"
subtitle: "Unit 21: Realisasi Geometrik dan Triangulasi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "23 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l21-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 4346--4500 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L4346-L4500)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang aktif itu terdiri atas 155 baris fisik. Setelah dinormalisasi dengan
LF dan mempertahankan baris kosong penutupnya, ukurannya 7.267 byte dan
SHA-256-nya adalah
`281ba27f0f52f35fd9842954c223546e84ce1a0909ee84c14b2081c38c11f150`.
Kuliah 22 dimulai pada Notes.tex baris 4501, sehingga kursor berikutnya ialah
baris 4501. Materi sumber dan adaptasi Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Perubahan edisi mencakup penerjemahan, pemformatan ulang, pemberian pengenal
stabil, dan pemindahan empat catatan pinggir ke urutan bacaan utama. Dua panel
TikZ sumber ditulis ulang sebagai dua gambar semantik terpusat yang menyebutkan
ruang ambien, titik sudut, sisi, dan persamaan afinnya; tidak ada makna yang
bergantung pada posisi, ketebalan garis, atau warna. Edisi juga memperjelas
derajat kohomologi yang nol, mengetik relasi pelekatan graf dan permukaan,
memperbaiki notasi pembentuk himpunan simpleks standar, serta membedakan
ortan nonnegatif dari ortan positif.

Rentang sumber memuat tepat satu catatan, dua lingkungan konstruksi, tiga
definisi, empat contoh, empat catatan pinggir, dua gambar TikZ, satu label
sumber, lima tampilan `\[...\]`, satu `align*`, dua `cases`, dan satu
`enumerate`. Tidak ada latihan sumber, lema, bukti, Xy-pic, sitasi, rujukan
silang, gambar eksternal, `input`, atau `include`. Identifikasi geometrik
$|\partial\Delta[3]|\cong S^2$ dan $|T_\bullet|\cong S^1\times S^1$
ditandai jujur sebagai fakta geometrik standar yang disebut sumber; unit ini
tidak menyamarkan keduanya sebagai teorema yang telah dibuktikan oleh sumber.

Enam pemeriksaan penguasaan, enam petunjuk, dan enam solusi lengkap merupakan
materi asli edisi dan tersedia di bawah CC BY 4.0. Edisi ini bersifat
independen; edisi ini tidak disponsori, didukung, disahkan, ataupun diberi
status resmi oleh David Michael Roberts atau institusinya. Produksi edisi ini
dibantu oleh **OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini menambah
transparansi proses dan tidak mengurangi kredit penulis sumber ataupun kredit
kontributor manusia.

# Kuliah 21 {#o012-rbt-l21}

## Kohomologi permukaan kombinatorik {#o012-rbt-l21-s01}

::: {.remark #o012-rbt-l21-rem-001}
**Catatan 21.1 (hubungan dengan Unit 20).** Kuliah ini semula dimulai dengan
rekap panjang Kuliah 20. Materi rekap tersebut telah dimasukkan ke Unit 20,
sehingga kita dapat langsung melanjutkan dari kompleks permukaan
kombinatorik.
:::

Untuk permukaan kombinatorik $X_\bullet$ dan gelanggang komutatif berunsur
satu $R$, kompleks

$$
0\longrightarrow R^{X_0}
\xrightarrow{\delta_0}R^{X_1}
\xrightarrow{\delta_1}R^{X_2}
\longrightarrow0
$$

memberikan modul kohomologi

$$
\begin{aligned}
H^0(X_\bullet;R)&:=\ker\delta_0,\\
H^1(X_\bullet;R)&:=\frac{\ker\delta_1}{\operatorname{im}\delta_0},\\
H^2(X_\bullet;R)&:=\frac{R^{X_2}}{\operatorname{im}\delta_1}
=\operatorname{coker}\delta_1.
\end{aligned}
$$

Secara formal $H^n(X_\bullet;R)$ terdefinisi untuk setiap bilangan bulat
$n$. Karena kompleks di atas hanya mempunyai suku pada derajat $0,1,2$,

$$
H^n(X_\bullet;R)=0
\qquad\text{untuk }n<0\text{ atau }n>2.
$$

Jika $X_2=\varnothing$, maka
$R^{X_2}=R^\varnothing=\{0\}$, sehingga $H^2(X_\bullet;R)=0$.

::: {.source-audit #o012-rbt-l21-audit-001}
**Audit sumber 21.1.** Notes.tex baris 4358--4360 mengatakan bahwa
$H^n$ terdefinisi untuk semua $n$, lalu menyebut “semuanya” modul nol. Yang
dimaksud hanyalah derajat di luar $0,1,2$; tiga derajat yang baru saja
ditampilkan tidak nol pada umumnya. Edisi menyatakan rentang nol itu secara
eksplisit.
:::

Untuk torus kombinatorik $T_\bullet$ dan $R=\mathbb Z$, perhitungan Unit 20
memberikan

$$
H^n(T_\bullet;\mathbb Z)=
\begin{cases}
\mathbb Z,&n=0,\\
\mathbb Z^2,&n=1,\\
\mathbb Z,&n=2,\\
0,&n\notin\{0,1,2\}.
\end{cases}
$$

Namun $T_\bullet$ sendiri jelas bukan ruang topologis
$S^1\times S^1$: ia hanya data himpunan dan *face map*. Kita memerlukan cara
mengubah data kombinatorik itu menjadi ruang topologis.

## Dua upaya merealisasikan graf {#o012-rbt-l21-s02}

Graf berarah $\partial\Delta[2]$ tampak seperti lingkaran. Secara topologis,
kita dapat membuat lingkaran aktual dari tiga salinan interval $[0,1]$ yang
titik-titik ujungnya diidentifikasi sesuai insidensi graf. Gagasan ini disebut
**realisasi geometrik**.

::: {.construction #o012-rbt-l21-constr-001}
**Konstruksi 21.1 (Upaya 1).** Untuk graf berarah
$X_1\rightrightarrows X_0$, mula-mula kita mungkin mencoba hasil bagi

$$
\left(\bigsqcup_{e\in X_1} I_e\right)\big/\!\sim,
$$

dengan titik-titik ujung salinan interval diidentifikasi menurut insidensi
sisi. Akan tetapi, konstruksi ini mempunyai dua masalah. Pertama, informasi
insidensi sebenarnya disimpan oleh $d_0,d_1$. Kedua, simpul terisolasi tidak
muncul sama sekali karena tidak mengindeks salinan interval. Karena itu
$X_0$ harus dimasukkan secara tersendiri.
:::

::: {.construction #o012-rbt-l21-constr-002}
**Konstruksi 21.2 (Upaya 2).** Ambil ruang diskret pada himpunan simpul dan
lekatkan satu interval untuk setiap sisi. Dengan menulis
$\Delta^0=\{\ast\}$ dan $I=\Delta^1$, definisikan pemetaan titik ujung

$$
\partial_0,\partial_1\colon\Delta^0\longrightarrow I,
\qquad
\partial_0(\ast)=1,
\quad
\partial_1(\ast)=0.
$$

::: {.source-margin #o012-rbt-l21-margin-001}
> **Catatan pinggir sumber.** Pemetaan $\partial_0,\partial_1$ dalam topologi
> ini dalam suatu arti “dual” terhadap fungsi titik ujung kombinatorik
> $d_0,d_1$. Konvensinya serasi: $d_1(e)$ adalah sumber yang dilekatkan pada
> $0=\partial_1(\ast)$, sedangkan $d_0(e)$ adalah target yang dilekatkan pada
> $1=\partial_0(\ast)$.
:::

Realisasi kandidat bagi graf adalah

$$
\left(
\bigsqcup_{v\in X_0}\{v\}\times\Delta^0
\;\sqcup\;
\bigsqcup_{e\in X_1}\{e\}\times I
\right)\Big/\!\sim,
$$

dengan relasi pembangkit

$$
(e,\partial_i(\ast))\sim(d_i(e),\ast)
\qquad(e\in X_1,\ i=0,1).
$$

Jadi titik ujung ke-$i$ dari interval berlabel $e$ dilekatkan pada simpul
berlabel $d_i(e)$. Simpul terisolasi tetap hadir melalui suku yang diindeks
oleh $X_0$.
:::

::: {.source-audit #o012-rbt-l21-audit-002}
**Audit sumber 21.2.** Notes.tex baris 4398--4400 memakai variabel $v$ tanpa
menyatakan bahwa ia adalah satu-satunya titik pada $\Delta^0$, dan kalimat
berikutnya dapat dibaca seolah titik ujung dilekatkan pada sembarang simpul.
Edisi memakai $\ast$ dan menulis relasi bertipe
$(e,\partial_i\ast)\sim(d_i(e),\ast)$.
:::

Konstruksi kasar ini segera digantikan oleh definisi yang lebih formal dan
sistematis, tetapi ia telah menangkap gagasan pokoknya.

::: {.example #o012-rbt-l21-exa-001 data-source-label="eg:join_interval_geom_real"}
**Contoh 21.1 (dua sisi berurutan).** Ambil

$$
X_0=\{v_1,v_2,v_3\},
\qquad
X_1=\{e_1,e_2\},
$$

dengan

$$
d_1(e_1)=v_1,
\quad d_0(e_1)=v_2=d_1(e_2),
\quad d_0(e_2)=v_3.
$$

Realisasi geometriknya homeomorfik dengan

$$
\bigl(\{v_1,v_2,v_3\}\sqcup[0,1]\sqcup[2,3]\bigr)\big/\!\sim,
$$

dengan

$$
0\sim v_1,
\qquad
1\sim v_2\sim2,
\qquad
3\sim v_3.
$$

Maka

$$
\bigl([0,1]\sqcup[2,3]\bigr)/(1\sim2)
\cong[0,2]
\cong[0,1].
$$
:::

## Simpleks standar dan pemetaan inklusi {#o012-rbt-l21-s03}

Untuk membuat konstruksi serupa bagi permukaan kombinatorik, kita memerlukan
model topologis seragam bagi simpul, sisi, dan muka segitiga.

::: {.definition #o012-rbt-l21-def-001}
**Definisi 21.1 (simpleks standar).** *Simpleks-$n$ standar* ialah subruang
dari $\mathbb R^{n+1}$

$$
\Delta^n:=
\left\{
(v_0,v_1,\ldots,v_n)\in\mathbb R^{n+1}
\ \middle|\
v_i\geq0\ (0\leq i\leq n),\quad
v_0+\cdots+v_n=1
\right\}.
$$

Untuk $0\leq i\leq n+1$, pemetaan inklusi standar

$$
\partial_i\colon\Delta^n\longrightarrow\Delta^{n+1}
$$

didefinisikan dengan menyisipkan koordinat nol pada posisi ke-$i$:

$$
\partial_i(v_0,\ldots,v_n)
=(v_0,\ldots,v_{i-1},0,v_i,\ldots,v_n).
$$
:::

::: {.example #o012-rbt-l21-exa-002}
**Contoh 21.2 (dimensi nol, satu, dan dua).** Simpleks-$0$ standar adalah
satu titik,

$$
\Delta^0=\{(1)\}\subset\mathbb R.
$$

Simpleks-$1$ standar adalah ruas garis

$$
\Delta^1=
\{(v_0,v_1)\in\mathbb R^2\mid
v_0,v_1\geq0,\ v_0+v_1=1\}.
$$

::: {.source-margin #o012-rbt-l21-margin-002}
> **Catatan pinggir sumber.** Notes.tex menempatkan dua gambar berikut di
> margin: satu ruas $\Delta^1$ pada bidang koordinat dan satu segitiga
> $\Delta^2$ di bidang afin dalam $\mathbb R^3$. Keduanya direflow secara
> terpisah agar setiap titik sudut dan persamaan dapat dibaca tanpa posisi.
:::

::: {.figure #o012-rbt-l21-fig-001 data-source-format="tikz"}
**Diagram 21.1 (deskripsi semantik $\Delta^1$).** Di dalam
$\mathbb R^2$, ruas $\Delta^1$ menghubungkan titik sudut
$(1,0)$ dan $(0,1)$ serta terdiri tepat atas titik
$(t,1-t)$ untuk $0\leq t\leq1$. Gambar sumber menunjukkan ruas miring pada
sumbu koordinat; kemiringannya tidak membawa informasi tambahan.
:::

Simpleks-$2$ standar ialah perpotongan bidang
$v_0+v_1+v_2=1$ dengan ortan **nonnegatif** di $\mathbb R^3$.

::: {.figure #o012-rbt-l21-fig-002 data-source-format="tikz"}
**Diagram 21.2 (deskripsi semantik $\Delta^2$).** Simpleks ini adalah
segitiga terisi dengan titik sudut

$$
(1,0,0),\qquad(0,1,0),\qquad(0,0,1).
$$

Ketiga sisinya diperoleh dengan membuat satu dari $v_0,v_1,v_2$ sama dengan
nol. Garis bantu abu-abu pada gambar sumber hanya menunjukkan ruang ambien
tiga dimensi; warna dan sudut pandang bukan bagian dari definisi.
:::
:::

::: {.source-audit #o012-rbt-l21-audit-003}
**Audit sumber 21.3.** Rumus $\Delta^1$ pada Notes.tex baris 4442 kehilangan
tanda kurung tutup setelah pasangan koordinat, sehingga pembentuk himpunannya
tidak bertipe. Edisi menulis $(v_0,v_1)\in\mathbb R^2$. Sumber juga menyebut
“ortan positif”, padahal ketaksamaan $v_i\geq0$ memasukkan batas; istilah yang
tepat ialah ortan nonnegatif.
:::

::: {.example #o012-rbt-l21-exa-003}
**Contoh 21.3 (pemetaan inklusi muka).** Dua pemetaan yang telah dipakai pada
graf adalah

$$
\partial_0,\partial_1\colon\Delta^0\longrightarrow\Delta^1,
\qquad
\partial_0(1)=(0,1),
\quad
\partial_1(1)=(1,0).
$$

Sekarang terdapat tiga pemetaan
$\partial_i\colon\Delta^1\to\Delta^2$, $i=0,1,2$, yaitu

$$
\partial_i(v_0,v_1)=
\begin{cases}
(0,v_0,v_1),&i=0,\\
(v_0,0,v_1),&i=1,\\
(v_0,v_1,0),&i=2.
\end{cases}
$$

Masing-masing mengidentifikasi $\Delta^1$ dengan sisi $\Delta^2$ yang
koordinat ke-$i$-nya nol.
:::

## Realisasi geometrik dan triangulasi {#o012-rbt-l21-s04}

::: {.definition #o012-rbt-l21-def-002}
**Definisi 21.2 (realisasi geometrik).** Realisasi geometrik permukaan
kombinatorik $X_\bullet$ ialah ruang hasil bagi

$$
|X_\bullet|:=
\left(
\bigsqcup_{n=0}^{2}
\operatorname{disc}(X_n)\times\Delta^n
\right)\Big/\!\sim,
$$

dengan relasi ekuivalensi yang dibangkitkan oleh

$$
(d_i(x),\mathbf v)\sim(x,\partial_i(\mathbf v)),
$$

untuk

$$
x\in X_n,
\qquad
\mathbf v\in\Delta^{n-1},
\qquad
1\leq n\leq2,
\qquad
0\leq i\leq n.
$$

Di ruas kiri, $(d_i(x),\mathbf v)$ berada pada salinan
$\{d_i(x)\}\times\Delta^{n-1}$; di ruas kanan,
$(x,\partial_i\mathbf v)$ berada pada batas salinan
$\{x\}\times\Delta^n$.
:::

::: {.source-audit #o012-rbt-l21-audit-004}
**Audit sumber 21.4.** Notes.tex baris 4466--4467 menulis relasi pelekatan
tanpa mengetik $x$, $\mathbf v$, $n$, dan $i$. Edisi menambahkan seluruh
domain dan rentangnya, sehingga kedua ruas relasi memang berada di koproduk
yang didefinisikan.
:::

Sebagai contoh utama,

$$
\begin{aligned}
|\Delta[2]|
&=\Bigl(
(\Delta^0\sqcup\Delta^0\sqcup\Delta^0)
\sqcup
(\Delta^1\sqcup\Delta^1\sqcup\Delta^1)
\sqcup\Delta^2
\Bigr)\Big/\!\sim\\
&\cong(\partial\Delta^2\sqcup\Delta^2)\big/\!\sim
\cong\Delta^2.
\end{aligned}
$$

::: {.source-margin #o012-rbt-l21-margin-003}
> **Catatan pinggir sumber.** Dalam dimensi lebih rendah berlaku pula
> $|\Delta[1]|\cong\Delta^1$ dan
> $|\Delta[0]|\cong\Delta^0$.
:::

Untuk definisi berikut, kata “permukaan” dipakai secara sengaja dalam arti
luas: sedikitnya mencakup manifold topologis berdimensi paling tinggi dua dan
juga ruang berdimensi campuran, misalnya gabungan saling lepas sebuah
lingkaran dan sebuah torus. Yang penting, “permukaan” di sini adalah ruang
topologis, bukan objek kombinatorik.

::: {.definition #o012-rbt-l21-def-003}
**Definisi 21.3 (triangulasi).** Sebuah *triangulasi* dari permukaan
$\Sigma$ ialah permukaan kombinatorik $X_\bullet$ yang dilengkapi dengan
homeomorfisma

$$
\tau\colon\Sigma\xrightarrow{\ \cong\ }|X_\bullet|.
$$
:::

::: {.source-margin #o012-rbt-l21-margin-004}
> **Catatan pinggir sumber.** Dalam pembahasan selanjutnya, homeomorfisma
> $\tau$ biasanya dibiarkan implisit. Namun triangulasi mencakup pilihan atau
> setidaknya data keberadaan homeomorfisma itu; ia bukan sekadar daftar sel.
:::

::: {.example #o012-rbt-l21-exa-004}
**Contoh 21.4 (triangulasi dasar).** Sumber mencatat contoh-contoh berikut.

1. $\Delta^2$ ditriangulasi oleh $\Delta[2]$.
2. Lebih umum, $|X_\bullet|$ ditriangulasi oleh $X_\bullet$.
3. $S^2$ ditriangulasi oleh $\partial\Delta[3]$.
4. $S^1$ ditriangulasi oleh $\partial\Delta[2]$, oleh setiap graf berarah
   berbentuk poligon, dan bahkan oleh graf dengan satu simpul serta satu sisi
   gelang.
5. $S^1\times S^1$ ditriangulasi oleh torus kombinatorik $T_\bullet$.

Butir 3 dan 5 menggunakan identifikasi geometrik standar: batas tetrahedron
homeomorfik dengan $S^2$, sedangkan persegi yang sisi berhadapannya dilekatkan
dan dibagi oleh satu diagonal merealisasikan torus. Sumber menyebutkan fakta
itu tanpa bukti di rentang ini; edisi mempertahankan status tersebut secara
jujur.
:::

::: {.source-audit #o012-rbt-l21-audit-005}
**Audit sumber 21.5.** Edisi memperbaiki salah eja dan tata bahasa
deterministik pada Notes.tex baris 4379, 4403, 4414, dan 4451 (“We” tanpa
tanda baca, `superceded`, “how do so”, dan `imporantly`). Pada definisi
triangulasi, simbol samar $\simeq$ diganti dengan homeomorfisma bertipe
eksplisit karena itulah data yang disebut dalam prosa sumber.
:::

# Pendamping penguasaan: pemeriksaan, petunjuk, dan solusi lengkap {.unnumbered #o012-rbt-l21-mastery}

Enam paket berikut adalah materi asli edisi. Semuanya terbatas pada sasaran
beku Unit 21: kohomologi kompleks yang terpotong, realisasi graf, simpleks dan
pemetaan inklusinya, relasi pelekatan, serta perbedaan antara data
kombinatorik dan ruang yang ditriangulasi.

::: {.exercise #o012-rbt-l21-mcheck-001 data-origin="edition-original"}
**Pemeriksaan Penguasaan 21.1 (derajat kohomologi).** Misalkan

$$
0\longrightarrow R^{X_0}
\xrightarrow{\delta_0}R^{X_1}
\xrightarrow{\delta_1}R^{X_2}
\longrightarrow0
$$

adalah kompleks permukaan kombinatorik. Turunkan rumus $H^n$ untuk semua
$n\in\mathbb Z$. Kemudian buktikan bahwa $X_2=\varnothing$ memaksa
$H^2=0$, tetapi, untuk gelanggang koefisien taknol, tidak memaksa $H^0$ atau
$H^1$ nol.
:::

::: {.hint #o012-rbt-l21-hint-001 data-origin="edition-original"}
**Petunjuk.** Perpanjang kompleks dengan modul nol pada semua derajat di luar
$0,1,2$. Ingat bahwa $R^\varnothing$ adalah modul nol. Untuk klaim terakhir,
gunakan graf satu simpul dengan satu sisi gelang.
:::

::: {.solution #o012-rbt-l21-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 21.1.** Tuliskan $A_n=0$ untuk $n<0$ dan $n>2$,
$A_n=R^{X_n}$ untuk $0\leq n\leq2$. Diferensial sebelum $A_0$ dan sesudah
$A_2$ adalah peta nol. Maka

$$
\begin{aligned}
H^0&=\ker(\delta_0)/\operatorname{im}(0)=\ker\delta_0,\\
H^1&=\ker\delta_1/\operatorname{im}\delta_0,\\
H^2&=\ker(0\colon R^{X_2}\to0)/\operatorname{im}\delta_1
=R^{X_2}/\operatorname{im}\delta_1.
\end{aligned}
$$

Jika $n<0$ atau $n>2$, pembilang dan penyebut berada pada modul nol, jadi
$H^n=0$. Bila $X_2=\varnothing$, hanya ada satu fungsi
$\varnothing\to R$, yaitu fungsi nol; karena itu
$R^{X_2}=0$ dan $H^2=0$.

Sebagai contoh tandingan bagi dua derajat lain, ambil gelanggang taknol,
misalnya $R=\mathbb Z$, lalu satu simpul $v$ dan satu sisi gelang $e$ dengan
$d_0(e)=d_1(e)=v$. Maka

$$
0\longrightarrow R\xrightarrow{0}R\longrightarrow0,
$$

sehingga $H^0\cong R$ dan $H^1\cong R$, walaupun $X_2=\varnothing$.
:::

::: {.exercise #o012-rbt-l21-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 21.2 (graf dengan komponen terisolasi).** Ambil graf
dengan simpul $a,b,c,z$, sisi $p\colon a\to b$ dan $q\colon b\to c$, serta
simpul terisolasi $z$. Bangun realisasi geometriknya langsung dari Upaya 2
dan tentukan tipe homeomorfismanya.
:::

::: {.hint #o012-rbt-l21-hint-002 data-origin="edition-original"}
**Petunjuk.** Petakan salinan interval untuk $p$ secara linear ke
$[0,\tfrac12]$ dan salinan untuk $q$ ke $[\tfrac12,1]$. Simpul $z$ tidak
terlibat dalam satu pun relasi pelekatan.
:::

::: {.solution #o012-rbt-l21-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 21.2.** Sebelum mengambil hasil bagi, ruangnya ialah

$$
\{a,b,c,z\}\sqcup I_p\sqcup I_q.
$$

Relasinya adalah

$$
(p,0)\sim a,
\quad(p,1)\sim b,
\quad(q,0)\sim b,
\quad(q,1)\sim c.
$$

Definisikan pemetaan dari ruang sebelum hasil bagi ke
$[0,1]\sqcup\{z\}$ dengan

$$
(p,t)\longmapsto\frac t2,
\qquad
(q,t)\longmapsto\frac{1+t}{2},
$$

dan $a\mapsto0$, $b\mapsto\tfrac12$, $c\mapsto1$, sementara $z$ dipetakan
ke komponen titik tersendiri. Pemetaan itu konstan tepat pada kelas-kelas
relasi di atas, sehingga turun menjadi bijeksi kontinu dari hasil bagi.
Domainnya kompak dan kodomainnya Hausdorff, maka bijeksi tersebut
homeomorfisma. Jadi

$$
|X_\bullet|\cong[0,1]\sqcup\{z\}.
$$

Inilah alasan Upaya 1 gagal: tanpa suku $X_0$, komponen $\{z\}$ akan hilang.
:::

::: {.exercise #o012-rbt-l21-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 21.3 (identitas pemetaan inklusi).** Buktikan bahwa
pemetaan penyisipan nol memenuhi

$$
\partial_j\circ\partial_i
=\partial_i\circ\partial_{j-1}
\qquad(0\leq i<j\leq n+2).
$$

Periksa secara eksplisit ketiga kasus dari $\Delta^0$ ke $\Delta^2$ dan
jelaskan mengapa identitas ini cocok dengan identitas *face map* pada
permukaan kombinatorik.
:::

::: {.hint #o012-rbt-l21-hint-003 data-origin="edition-original"}
**Petunjuk.** Kedua komposit menyisipkan nol pada dua posisi yang sama. Untuk
$n=0$, pasangan $(i,j)$ adalah $(0,1)$, $(0,2)$, dan $(1,2)$.
:::

::: {.solution #o012-rbt-l21-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 21.3.** Ambil
$\mathbf v=(v_0,\ldots,v_n)$. Komposit kiri mula-mula menyisipkan nol pada
posisi $i$. Karena $i<j$, penyisipan kedua pada posisi $j$ tidak mengubah
posisi nol pertama. Komposit kanan mula-mula menyisipkan nol pada posisi
$j-1$, lalu menyisipkan nol pada posisi $i$; penyisipan kedua menggeser nol
pertama dari posisi $j-1$ ke $j$. Jadi kedua hasil mempunyai koordinat nol
pada posisi $i$ dan $j$, dengan koordinat $\mathbf v$ yang lain tetap
berurutan. Ini membuktikan identitas.

Untuk titik tunggal $(1)\in\Delta^0$,

$$
\begin{array}{c|c|c}
(i,j)&\partial_j\partial_i(1)&
\partial_i\partial_{j-1}(1)\\ \hline
(0,1)&(0,0,1)&(0,0,1)\\
(0,2)&(0,1,0)&(0,1,0)\\
(1,2)&(1,0,0)&(1,0,0)
\end{array}
$$

Pemetaan $d_i$ menghapus muka kombinatorik, sedangkan $\partial_i$
memasukkan muka topologis sebagai koordinat ke-$i$ nol. Identitas keduanya
berarah dual: dua cara menuju muka kodimensi dua menghasilkan bagian yang
sama. Karena itu relasi realisasi tidak bergantung pada urutan pelekatan.
:::

::: {.exercise #o012-rbt-l21-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 21.4 (realisasi satu segitiga).** Bangun pemetaan
kanonik

$$
|\Delta[2]|\longrightarrow\Delta^2
$$

dari definisi hasil bagi dan buktikan bahwa ia homeomorfisma. Sertakan peran
tiga simpul dan tiga sisi dalam relasi pelekatan.
:::

::: {.hint #o012-rbt-l21-hint-004 data-origin="edition-original"}
**Petunjuk.** Pada salinan $\Delta^2$ yang diindeks oleh muka tunggal,
gunakan identitas. Pada setiap salinan $\Delta^1$, gunakan $\partial_i$ yang
sesuai; pada setiap $\Delta^0$, gunakan titik sudut terkait. Lalu gunakan
sifat universal hasil bagi dan argumen kompak-ke-Hausdorff.
:::

::: {.solution #o012-rbt-l21-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 21.4.** Misalkan $f$ muka tunggal, $e_i=d_i(f)$, dan
$v_j$ ketiga simpul. Pada komponen $\{f\}\times\Delta^2$, definisikan
$F(f,\mathbf v)=\mathbf v$. Pada komponen
$\{e_i\}\times\Delta^1$, definisikan

$$
F(e_i,\mathbf u)=\partial_i(\mathbf u),
$$

dan pada komponen simpul, kirim $v_j$ ke titik sudut standar ke-$j$.
Identitas pemetaan inklusi dari Pemeriksaan 21.3 memastikan bahwa nilai pada
titik ujung setiap sisi sama dengan nilai pada simpul yang ditempelkan.
Demikian pula,

$$
F(d_i(f),\mathbf u)
=\partial_i(\mathbf u)
=F(f,\partial_i\mathbf u),
$$

jadi $F$ konstan pada relasi pembangkit. Ia turun menjadi pemetaan kontinu

$$
\overline F\colon|\Delta[2]|\longrightarrow\Delta^2.
$$

Pemetaan ini surjektif karena komponen muka dipetakan dengan identitas. Setiap
titik pada komponen sisi atau simpul telah diidentifikasi dengan titik yang
sama pada batas komponen muka; karena itu tidak ada kelas tambahan dan
$\overline F$ injektif. Ruang sebelum hasil bagi adalah gabungan berhingga
ruang kompak, sehingga hasil baginya kompak; $\Delta^2$ Hausdorff. Bijeksi
kontinu kompak-ke-Hausdorff adalah homeomorfisma. Jadi
$|\Delta[2]|\cong\Delta^2$.
:::

::: {.exercise #o012-rbt-l21-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 21.5 (dua triangulasi lingkaran).** Buktikan bahwa
graf satu simpul dan satu sisi gelang merealisasikan $S^1$. Kemudian buktikan
hal yang sama bagi graf poligon berarah dengan $m\geq2$ sisi, tanpa
mengasumsikan semua orientasi sisinya seragam.
:::

::: {.hint #o012-rbt-l21-hint-005 data-origin="edition-original"}
**Petunjuk.** Kasus satu gelang adalah $I/(0\sim1)$. Untuk poligon, orientasi
hanya menentukan titik ujung interval mana yang bernama $0$ atau $1$; ia
tidak mengubah ruang hasil bagi tak berarah yang diperoleh setelah semua titik
ujung ditempelkan secara siklik.
:::

::: {.solution #o012-rbt-l21-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 21.5.** Untuk satu simpul $v$ dan satu sisi $e$ dengan
$d_0(e)=d_1(e)=v$, definisi memberi

$$
|X_\bullet|
=\bigl(\{v\}\sqcup I_e\bigr)/
\bigl((e,0)\sim v\sim(e,1)\bigr)
\cong I/(0\sim1).
$$

Pemetaan $t\mapsto e^{2\pi i t}$ dari $I$ ke $S^1$ mengidentifikasi tepat
titik ujungnya dan menginduksi homeomorfisma $I/(0\sim1)\cong S^1$.

Untuk poligon dengan simpul siklik $v_0,\ldots,v_{m-1}$, setiap sisi
menghubungkan $v_k$ dan $v_{k+1}$, dengan indeks modulo $m$. Pilih
homeomorfisma dari salinan interval sisi itu ke busur

$$
\left\{e^{2\pi i t}:\frac{k}{m}\leq t\leq\frac{k+1}{m}\right\}.
$$

Jika orientasi sisi berlawanan dengan arah parameter lingkaran, gunakan
$t\mapsto1-t$ pada interval tersebut. Nilai pada titik ujung tetap cocok
dengan simpul yang ditentukan oleh $d_0,d_1$, sehingga pemetaan-pemetaan busur
turun menjadi bijeksi kontinu dari realisasi ke $S^1$. Lagi-lagi domain
kompak dan $S^1$ Hausdorff, jadi bijeksi itu homeomorfisma. Dengan demikian
orientasi kombinatorik tidak mengubah tipe homeomorfisma realisasinya.
:::

::: {.exercise #o012-rbt-l21-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 21.6 (data kombinatorik versus ruang).** Jelaskan
perbedaan antara $X_\bullet$, $|X_\bullet|$, dan triangulasi
$\tau\colon\Sigma\cong|X_\bullet|$. Lalu hitung karakteristik Euler dari
$\partial\Delta[3]$ dan $T_\bullet$, dan jelaskan secara logis apa yang
dibuktikan—serta apa yang tidak dibuktikan—oleh kedua hitungan itu.
:::

::: {.hint #o012-rbt-l21-hint-006 data-origin="edition-original"}
**Petunjuk.** Batas tetrahedron mempunyai $4$ simpul, $6$ sisi, dan $4$
muka; torus kombinatorik Unit 20 mempunyai $1$, $3$, dan $2$. Karakteristik
Euler adalah invarian yang perlu dilestarikan oleh homeomorfisma, tetapi
kesamaan nilainya bukan bukti homeomorfisma pada kelas ruang sembarang.
:::

::: {.solution #o012-rbt-l21-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 21.6.** Objek $X_\bullet$ adalah data kombinatorik:
tiga himpunan $X_0,X_1,X_2$ beserta *face map*. Realisasi
$|X_\bullet|$ adalah ruang topologis yang diperoleh dengan mengganti setiap
elemen $X_n$ oleh salinan $\Delta^n$ lalu melekatkan muka-mukanya. Sebuah
triangulasi dari $\Sigma$ menambahkan data geometrik

$$
\tau\colon\Sigma\xrightarrow{\cong}|X_\bullet|.
$$

Jadi $X_\bullet$ tidak boleh disamakan secara literal dengan ruang
$\Sigma$.

Untuk batas tetrahedron,

$$
\chi(\partial\Delta[3])=4-6+4=2.
$$

Untuk torus kombinatorik,

$$
\chi(T_\bullet)=1-3+2=0.
$$

Hitungan itu membuktikan nilai karakteristik Euler dari kedua kompleks
berhingga. Nilai tersebut konsisten dengan $\chi(S^2)=2$ dan
$\chi(S^1\times S^1)=0$, sehingga tidak membantah identifikasi geometrik yang
diklaim. Namun hitungan Euler saja tidak membangun homeomorfisma: banyak ruang
yang tidak homeomorfik dapat mempunyai karakteristik Euler sama. Untuk
menyebut $X_\bullet$ triangulasi dari $\Sigma$, masih diperlukan
homeomorfisma $\tau$. Dalam contoh sumber, homeomorfisma batas tetrahedron
dengan sfera dan homeomorfisma model persegi bersegi-diagonal dengan torus
adalah fakta geometrik tambahan, bukan konsekuensi dari bilangan Euler saja.
:::

::: {.boundary #o012-rbt-l21-boundary-001}
**Batas ke Unit 22.** Notes.tex baris 4501 memulai Kuliah 22 dengan kalimat
tentang perilaku fungtorial dan pemetaan permukaan kombinatorik. Tidak ada
lingkungan sumber yang terbelah pada batas ini. Kursor sumber berikutnya yang
aman adalah baris 4501.
:::
