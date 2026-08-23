---
title: "Topologi Aljabar"
subtitle: "Unit 20: Kompleks Kombinatorik dan Kohomologi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "23 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l20-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 3948--4346 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L3948-L4346)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Sebelum penanda berikutnya, slice fisik mentahnya terdiri atas 399 baris,
dimulai pada baris 3948 dan mencakup pembukaan catatan di baris 4346;
penanda Kuliah 21 muncul pada baris 4347. Jika 399 baris mentah tersebut
digabung dengan LF tanpa baris akhir, ukurannya 17.657 byte dan hash
SHA-256-nya adalah
`6af488776f936d7a3ef17a30a8af94e6955df91e3a3057b92b048e1b38ca1917`.
Lingkungan lengkap yang diterjemahkan berakhir pada baris 4345 (398 baris;
hash LF-normalisasi
`1fa7d0ea4ecd567ae8975da5b9b41495a1757913942102f223d1234168366e88`).
Baris 4346 hanya membuka lingkungan catatan yang baru berlanjut setelah
penanda Kuliah 21; demi batas lingkungan yang sah, pembukaan itu dicatat
sebagai batas tertunda dan isi catatan akan dimulai pada unit berikutnya.
Materi sumber dan adaptasi Indonesia ini tersedia di bawah [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Perubahan edisi mencakup penerjemahan, pemformatan ulang, pemberian pengenal
stabil, dan pemindahan sebelas catatan pinggir ke urutan bacaan utama. Tujuh
gambar TikZ ditulis ulang sebagai deskripsi semantik dan tabel terpusat yang
menyebutkan semua simpul, sisi, muka, label, dan orientasi; tidak ada makna
yang bergantung pada warna atau posisi. Edisi memperbaiki matriks graf dengan
menyatakan konvensi vektor baris/kolom, melengkapi panah yang hilang pada
kompleks bintang, memperbaiki indeks face map dan rumus komposisi, serta
menuliskan definisi kohomologi dengan kernel dan citra yang bertipe benar.
Salah eja, salah tata bahasa, dan ekspansi bukti kompleks yang terduplikasi
juga diperbaiki. Semua ruang fungsi $R^S$ tetap dimaknai sebagai produk
semua fungsi, bukan sebagai modul berdukungan hingga.

Rentang aktif sebelum pembukaan catatan yang tertunda memuat delapan contoh,
empat catatan lengkap, dua definisi, dua lema, dua bukti (salah satunya
ditandai “Exercise”), dan empat lingkungan latihan sumber (lima butir karena
lingkungan pertama memiliki dua bagian). Ia memuat delapan tampilan
`\[...\]`, dua tampilan `align*`, satu tampilan `align`, tiga `cases`, enam
label sumber, dan tujuh gambar TikZ inline yang semuanya direflow. Tidak ada
Xy-pic, gambar eksternal, `input`, atau `include`. Fakta bahwa model
kompleks kombinatorik menangkap topologi ruang aktual hanya disajikan sebagai
motivasi; tidak ada ekuivalensi realisasi yang diklaim atau dibuktikan di
unit ini.

Enam pemeriksaan penguasaan, enam petunjuk, dan enam solusi lengkap merupakan
materi asli edisi dan tersedia di bawah CC BY 4.0. Edisi ini bersifat
independen; edisi ini tidak disponsori, didukung, disahkan, ataupun diberi
status resmi oleh David Michael Roberts atau institusinya. Produksi edisi ini
dibantu oleh **OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini menambah
transparansi proses dan tidak mengurangi kredit penulis sumber ataupun kredit
kontributor manusia.

# Kuliah 20 {#o012-rbt-l20}

## Contoh konkret kompleks graf {#o012-rbt-l20-s01}

Berikut beberapa contoh konkret dari kompleks yang dibangun pada akhir Unit
19 dari graf berarah.

::: {.example #o012-rbt-l20-exa-001}
**Contoh 20.1 (graf trivial satu simpul).** Ambil graf dengan satu simpul dan
tanpa sisi. Maka $V=\{v\}$, $E=\varnothing$, dan kompleksnya adalah

$$
0\longrightarrow\mathbb Z
\xrightarrow{\delta}0\longrightarrow0.
$$

Pemetaan $\delta$ adalah peta nol, sehingga

$$
\ker(\delta)=\mathbb Z,
\qquad
\operatorname{coker}(\delta)=0.
$$
:::

::: {.example #o012-rbt-l20-exa-002 data-source-ref="eg:triangle_graph"}
**Contoh 20.2 (kompleks segitiga berarah).** Kompleks yang berasal dari
$\partial\Delta[2]$ pada Contoh 19.12 adalah

$$
0\longrightarrow\mathbb Z^3
\xrightarrow{\delta}\mathbb Z^3
\longrightarrow0.
$$

Untuk setiap $X\in\{A,B,C\}$, tuliskan fungsi basis

$$
\underline X\colon\{A,B,C\}\longrightarrow\mathbb Z,
\qquad
\underline X(v)=
\begin{cases}
1,&v=X,\\
0,&v\neq X.
\end{cases}
$$

Dengan basis simpul $(\underline A,\underline B,\underline C)$ dan basis
sisi $(a,b,c)$, konvensi Unit 19 memberi

$$
\begin{aligned}
\delta(\underline A)(a)&=-1,&
\delta(\underline A)(b)&=0,&
\delta(\underline A)(c)&=-1,\\
\delta(\underline B)(a)&=1,&
\delta(\underline B)(b)&=-1,&
\delta(\underline B)(c)&=0,\\
\delta(\underline C)(a)&=0,&
\delta(\underline C)(b)&=1,&
\delta(\underline C)(c)&=1.
\end{aligned}
$$

Memang, $A$ adalah sumber sisi $a$ dan $c$ serta tidak bersinggungan dengan
$b$, sedangkan $B$ adalah target sisi $a$. Jika koordinat ditulis sebagai
**vektor baris** dan fungsi basis menjadi baris-baris matriks, matriks sumber
adalah

$$
D=\begin{pmatrix}
-1&0&-1\\
1&-1&0\\
0&1&1
\end{pmatrix}.
$$

Dengan konvensi vektor kolom yang lebih umum, matriks pemetaan yang sama
adalah $M=D^{\mathsf T}$; kolom-kolom $M$ adalah citra fungsi basis simpul.
Kernel dan citra harus ditulis dalam basis sisi $(a,b,c)$ agar tidak
mencampur nama simpul dengan elemen kodomain:

$$
M=D^{\mathsf T}=\begin{pmatrix}
-1&1&0\\
0&-1&1\\
-1&0&1
\end{pmatrix},
\qquad
\ker\delta=\ker M=\mathbb Z(\underline A+\underline B+\underline C)\cong\mathbb Z,
$$

sedangkan

$$
\operatorname{im}\delta
=\mathbb Z(-a-c)+\mathbb Z(a-b)+\mathbb Z(b+c)
=\mathbb Z(-a-c)+\mathbb Z(a-b),
\qquad
\operatorname{coker}\delta\cong\mathbb Z.
$$

Memang, menambahkan $b$ pada dua pembangkit pertama menghasilkan seluruh
modul sisi: dari $a-b$ dan $b$ diperoleh $a$, lalu dari $-a-c$ diperoleh $c$.

Dengan demikian karakteristik Eulernya adalah

$$
\chi=|V|-|E|=3-3=0.
$$
:::

::: {.source-audit #o012-rbt-l20-audit-001}
**Audit sumber 20.1.** Matriks pada Notes.tex baris 3974--3980 menampilkan
koordinat citra fungsi basis sebagai baris, sedangkan banyak pembaca memakai
vektor kolom. Edisi menyatakan konvensi itu secara eksplisit dan memakai
$M=D^{\mathsf T}$ untuk vektor kolom. Karena
$\delta f(e)=f(d_0e)-f(d_1e)$, fungsi konstan harus berada di kernel:
$\ker\delta=\mathbb Z(\underline A+\underline B+\underline C)$, bukan
generator dengan tanda minus seperti tercetak di sumber. Citra yang benar
adalah $\langle-a-c,a-b,b+c\rangle$; nama simpul tidak dipakai sebagai
elemen kodomain.
:::

::: {.remark #o012-rbt-l20-rem-001 data-source-label="remark:finite_complexes_basis"}
**Catatan 20.1 (basis hingga).** Untuk setiap graf berhingga (dan nanti objek
kombinatorik berhingga yang lebih umum), simpul dan sisi dapat dipakai sebagai
himpunan pembangkit bagi $\mathbb Z^V$ dan $\mathbb Z^E$: sebuah unsur
$x\in V$ mewakili fungsi yang bernilai $1$ pada $x$ dan $0$ di tempat lain.
Untuk graf tak berhingga, ruang fungsi adalah produk dan bukan modul bebas
berdukungan hingga; basis koordinat naif tidak lagi tersedia secara umum.
:::

::: {.example #o012-rbt-l20-exa-003 data-source-label="eg:triangle_graph_cplx"}
**Contoh 20.3 (graf bintang empat simpul).** Pertimbangkan graf dengan

$$
V=\{A,B,C,D\},
\qquad E=\{b,c,d\},
$$

dan tiga sisi yang semuanya berawal di $A$:

::: {.source-margin #o012-rbt-l20-margin-001}
> **Catatan pinggir sumber.** Diagram pada Notes.tex baris 3989 menempatkan
> $A$ di pusat dan mengarahkan $b,c,d$ menuju $B,C,D$. Tabel insidensi di
> bawah mempertahankan informasi arah tanpa bergantung pada posisi gambar.
:::

::: {.figure #o012-rbt-l20-fig-001 data-source-format="tikz"}
**Diagram 20.1 (deskripsi semantik graf bintang).** Empat simpulnya adalah
$A,B,C,D$ dan tiga sisi berarah keluar dari $A$:

| Sisi | Sumber $d_1$ | Target $d_0$ |
|:---:|:---:|:---:|
| $b$ | $A$ | $B$ |
| $c$ | $A$ | $C$ |
| $d$ | $A$ | $D$ |

Gambar sumber menempatkan $A$ di pusat dan $B,C,D$ di tiga arah berbeda.
Tabel ini mempertahankan semua label dan orientasi tanpa bergantung pada
posisi radialnya.
:::

Dengan basis fungsi simpul dan sisi, kompleksnya adalah

$$
0\longrightarrow\mathbb Z^4
\xrightarrow{\delta}\mathbb Z^3
\longrightarrow0,
$$

dan matriks dengan vektor kolom ialah

$$
D=\begin{pmatrix}
-1&1&0&0\\
-1&0&1&0\\
-1&0&0&1
\end{pmatrix}.
$$

Matriks ini surjektif, sehingga kokernel nol. Maka

$$
\ker\delta
=\{(t,t,t,t):t\in\mathbb Z\}\cong\mathbb Z,
\qquad
\chi=4-3=1.
$$
:::

::: {.source-audit #o012-rbt-l20-audit-002}
**Audit sumber 20.2.** Pada baris 4004 sumber mencetak `0\mathbb Z^4`,
yang kehilangan panah awal. Edisi memperbaikinya menjadi
$0\to\mathbb Z^4$ dan menyatakan arah setiap sisi secara eksplisit.
:::

Tidak perlu membatasi diri pada graf terhubung.

::: {.example #o012-rbt-l20-exa-004}
**Contoh 20.4 (graf tak terhubung).** Ambil

$$
V=\{A,B,C\},
\qquad E=\{b\},
\qquad d_1(b)=C,
\quad d_0(b)=B,
$$

sehingga $b$ berarah dari $C$ ke $B$ dan $A$ terisolasi.

::: {.source-margin #o012-rbt-l20-margin-002}
> **Catatan pinggir sumber.** Sketsa Notes.tex baris 4020 memiliki satu simpul
> terisolasi dan satu panah $C\to B$; ketinggian simpul pada sketsa bukan data
> matematis.
:::

::: {.figure #o012-rbt-l20-fig-002 data-source-format="tikz"}
**Diagram 20.2 (deskripsi semantik graf tak terhubung).** Data insidensinya
adalah satu simpul terisolasi $A$ dan satu sisi $b$ dengan orientasi
$C\xrightarrow{b}B$:

| Objek | Sumber | Target |
|:---:|:---:|:---:|
| $b$ | $C$ | $B$ |

Posisi vertikal pada gambar sumber tidak menambah data; tabel ini menyatakan
arah secara eksplisit.
:::

Kompleksnya

$$
0\longrightarrow\mathbb Z^3
\xrightarrow{\delta}\mathbb Z
\longrightarrow0
$$

memiliki $\delta(f)=f_B-f_C$, yang surjektif. Maka

$$
\operatorname{coker}(\delta)=0,
\qquad
\ker(\delta)=\{(t,s,s):t,s\in\mathbb Z\}\cong\mathbb Z^2,
$$

dan $\chi=3-1=2$.
:::

::: {.exercise #o012-rbt-l20-ex-001 data-origin="source" data-source-environment="ex"}
**Latihan Sumber 20.1 (dua bagian: koproduk dan poliedron).**

1. Untuk dua graf berarah sederhana $G_1$ dan $G_2$, bentuk gabungan saling
   lepas $G_1\sqcup G_2$ dengan mengambil gabungan saling lepas himpunan
   simpul dan sisi serta fungsi $d_0,d_1$ yang diinduksi. Tunjukkan

   $$
   \ker\delta_{G_1\sqcup G_2}
   \cong
   \ker\delta_{G_1}\oplus\ker\delta_{G_2}.
   $$

2. Untuk graf berarah **berhingga** $G$ yang bentuk dasarnya adalah poliedron
   satu-siklus dan yang
   terhubung, tunjukkan bahwa kernel dan kokernel pemetaan terkait
   $\delta_G$ keduanya isomorfik dengan $\mathbb Z$.

Solusi lengkap kedua bagian diberikan kembali dalam Pemeriksaan Penguasaan
20.1 dan 20.2. Untuk graf tak berhingga, produk ruang fungsi menggantikan
jumlah langsung; untuk graf dengan beberapa siklus, rank kokernel lebih besar.
:::

::: {.exercise #o012-rbt-l20-ex-002 data-origin="source"}
**Latihan Sumber 20.2 (dua siklus).** Hitung kernel dan kokernel graf berarah
sederhana yang terhubung dan mempunyai dua siklus. Solusi lengkapnya diberikan
dalam Pemeriksaan Penguasaan 20.3.
:::

::: {.source-audit #o012-rbt-l20-audit-003}
**Audit sumber 20.3.** Klaim Notes.tex baris 4043--4050 terlalu luas bila
dibaca untuk semua graf terhubung berbentuk poliedron: rank kokernel sama
dengan banyak siklus independen, bukan selalu satu. Edisi membatasi pembacaan
latihan kedua pada kasus satu-siklus yang dimaksudkan, lalu menghitung kasus
dua-siklus secara terpisah. Untuk modul-$\mathbb Z$, istilah yang tepat ialah
**rank**, bukan dimensi sebagai ruang vektor.
:::

::: {.source-audit #o012-rbt-l20-audit-004}
**Audit sumber 20.3b.** Rujukan silang Notes.tex baris 4069 menunjuk label
`eg:triangle_graph_cplx`, padahal contoh yang baru saja dibahas adalah gelang
satu-simpul, bukan graf pohon empat-simpul. Edisi mengganti rujukan itu dengan
uraian mandiri dan mempertahankan konvensi graf berarah
$d_1(e)\to d_0(e)$.
:::

::: {.remark #o012-rbt-l20-rem-002}
**Catatan 20.2 (graf berarah umum).** Kita tidak harus membatasi diri pada
graf berarah sederhana. Definisi kompleks graf hanya memakai rumus

$$
\delta(f)=f\circ d_0-f\circ d_1,
$$

bukan injektivitas $(d_0,d_1)$ atau larangan diagonal. Karena itu boleh ada
satu simpul dan satu sisi yang merupakan model kombinatorik lingkaran:

::: {.source-margin #o012-rbt-l20-margin-003}
> **Catatan pinggir sumber.** Lingkaran satu-simpul pada Notes.tex baris 4059
> digambar sebagai satu gelang dengan simpul $v$ dan sisi $e$. Dalam adaptasi
> ini orientasinya dinyatakan oleh $d_0(e)=d_1(e)=v$.
:::

::: {.figure #o012-rbt-l20-fig-003 data-source-format="tikz"}
**Diagram 20.3 (deskripsi semantik gelang satu-simpul).** Ada tepat satu
simpul $v$ dan satu sisi $e$ dengan kedua ujung pada $v$; panahnya dapat
dipilih searah dari $v$ kembali ke $v$. Data ini, bukan arah gambar, yang
menentukan model kombinatorik lingkaran.
:::

$$
0\longrightarrow\mathbb Z
\xrightarrow{\delta=0}\mathbb Z
\longrightarrow0.
$$

Baik kernel maupun kokernelnya isomorfik dengan $\mathbb Z$.
:::

## Permukaan kombinatorik dan kompleks dua dimensi {#o012-rbt-l20-s02}

Namun, objek satu dimensi saja belum cukup. Kita ingin memikirkan sesuatu
yang memainkan peran graf berarah berdimensi dua: himpunan simpul, sisi, dan
muka segitiga, beserta fungsi yang menjelaskan bagaimana mereka saling
menempel. Istilah **permukaan kombinatorik** di sini berarti objek berdimensi
paling tinggi dua, bukan permukaan manifold yang harus bebas degenerasi.

::: {.source-margin #o012-rbt-l20-margin-004}
> **Catatan pinggir sumber.** Istilah yang lebih luas untuk data sampai
> dimensi dua ini adalah *himpunan semisimplicial 2-skeletal*; Mike Hopkins
> menyebut objek semacam ini *kompleks $\Delta$-kombinatorik*. Di kuliah ini
> istilah yang dipakai adalah *permukaan kombinatorik*.
:::

::: {.example #o012-rbt-l20-exa-005 data-source-label="eg:triangle_Delta_complex"}
**Contoh 20.5 (satu segitiga terisi).** Pertimbangkan satu segitiga terisi.
Simpulnya dinamai $v_0,v_1,v_2$, sisinya $e_0,e_1,e_2$, dan mukanya $f$.

::: {.source-margin #o012-rbt-l20-margin-005}
> **Catatan pinggir sumber.** Arsiran pada gambar Notes.tex baris 4082 hanya
> menandai bahwa $f$ terisi. Data yang menentukan objek adalah tiga simpul,
> tiga sisi berorientasi, dan satu muka seperti pada tabel berikut.
:::

::: {.figure #o012-rbt-l20-fig-004 data-source-format="tikz"}
**Diagram 20.4 (deskripsi semantik segitiga terisi).** Orientasi sisi dan
labelnya adalah

| Sisi | Sumber $d_1^1$ | Target $d_0^1$ | Keterangan |
|:---:|:---:|:---:|:---|
| $e_2$ | $v_0$ | $v_1$ | sisi berhadapan dengan $v_2$ |
| $e_0$ | $v_1$ | $v_2$ | sisi berhadapan dengan $v_0$ |
| $e_1$ | $v_0$ | $v_2$ | sisi berhadapan dengan $v_1$ |

Satu muka $f$ dibatasi oleh ketiga sisi, dengan $e_0$ menghubungkan
$v_1\to v_2$, $e_1$ menghubungkan $v_0\to v_2$, dan $e_2$ menghubungkan
$v_0\to v_1$. Tabel ini menggantikan gambar posisi dan kepala panah sumber.
:::
:::

Dengan $e_i$ sisi yang berhadapan dengan $v_i$, identitas muka yang terlihat
langsung pada segitiga ialah

$$
d_0^1(e_2)=d_1^1(e_0),
\qquad
d_0^1(e_1)=d_0^1(e_0),
\qquad
d_1^1(e_2)=d_1^1(e_1).
$$

Kombinatorika ini dirangkum oleh definisi berikut.

::: {.definition #o012-rbt-l20-def-001 data-source-label="eq:simpl_ids_surf"}
**Definisi 20.1 (permukaan kombinatorik).** Sebuah *permukaan kombinatorik*
$X_\bullet$ terdiri atas himpunan simpul, sisi, dan muka, masing-masing

$$
X_0,\qquad X_1,\qquad X_2,
$$

serta fungsi *face map*

$$
d_i^n\colon X_n\longrightarrow X_{n-1}
\qquad
(0\leq i\leq n,\;0<n\leq2),
$$

yang memenuhi identitas

$$
\begin{aligned}
d_0^1\circ d_2^2&=d_1^1\circ d_0^2,\\
d_0^1\circ d_1^2&=d_0^1\circ d_0^2,\\
d_1^1\circ d_2^2&=d_1^1\circ d_1^2.
\end{aligned}
$$

Jika dimensinya jelas, superskrip pada $d_i^n$ boleh dihilangkan. *1-skeleton*
$X_\bullet$ adalah graf berarah yang diperoleh dengan melupakan $X_2$ dan
mempertahankan $X_0,X_1,d_0^1,d_1^1$.
:::

::: {.source-margin #o012-rbt-l20-margin-006}
> **Catatan pinggir sumber.** Notasi $X_i$ berarti himpunan muka berdimensi
> $i$, sedangkan $d_i^n$ disebut *face map* dari dimensi $n$.
:::

::: {.source-margin #o012-rbt-l20-margin-007}
> **Catatan pinggir sumber.** Cara termudah mengingat ketiga identitas ialah
> menggambar satu segitiga: menghapus dua muka berturut-turut dengan dua
> urutan yang berbeda menghasilkan sisi atau simpul yang sama.
:::

Istilah “permukaan” di sini berarti “berdimensi paling tinggi dua”. Tidak ada
syarat bahwa $X_2$ tidak kosong. Bahkan boleh ada komponen berdimensi nol atau
satu; objeknya boleh degenerat tanpa segitiga dan tanpa sisi, walaupun bila
ada satu segitiga maka pasti ada sedikitnya satu sisi dan satu simpul.

::: {.source-margin #o012-rbt-l20-margin-008}
> **Catatan pinggir sumber.** Gambar sumber mengilustrasikan satu segitiga
> dan beberapa simpul atau sisi terpisah untuk menekankan bahwa komponen
> berdimensi lebih rendah diizinkan. Deskripsi ini menggantikan gambar
> tersebut dengan data insidensi yang eksplisit.
:::

::: {.figure #o012-rbt-l20-fig-005 data-source-format="tikz"}
**Diagram 20.5 (deskripsi semantik komponen degenerat).** Satu komponen
memuat segitiga terisi dengan tiga sisi dan tiga simpul; komponen lain boleh
berupa sisi tunggal atau simpul-simpul terisolasi. Tidak ada panah tambahan
yang tersirat oleh jarak antar-komponen, dan keberadaan komponen rendah
dimensi tidak mengubah syarat tiga identitas *face map*.
:::

::: {.example #o012-rbt-l20-exa-006}
**Contoh 20.6 (simpleks kombinatorik $\Delta[2]$).** Segitiga pada Contoh
20.5 dinamai $\Delta[2]$, dengan

$$
\Delta[2]_0=\{v_0,v_1,v_2\},
\qquad
\Delta[2]_1=\{e_0,e_1,e_2\},
\qquad
\Delta[2]_2=\{f\}.
$$

Peta muka atas memenuhi

$$
d_i^2(f)=e_i,
$$

sedangkan peta muka tingkat satu adalah

$$
\begin{array}{c|ccc}
 &e_0&e_1&e_2\\ \hline
d_0^1&v_2&v_2&v_1\\
d_1^1&v_1&v_0&v_0
\end{array}
$$

sesuai orientasi Contoh 20.5. 1-skeleton $\Delta[2]$ adalah graf berarah
$\partial\Delta[2]$.
:::

::: {.example #o012-rbt-l20-exa-007 data-source-label="eg:combinatorial_torus"}
**Contoh 20.7 (model kombinatorik torus).** Ambil

$$
T_0=\{v\},
\qquad
T_1=\{e_1,e_2,e_3\},
\qquad
T_2=\{f_1,f_2\}.
$$

::: {.figure #o012-rbt-l20-fig-006 data-source-format="tikz"}
**Diagram 20.6 (deskripsi semantik torus kombinatorik).** Gambar sumber
adalah persegi dengan keempat sudut diidentifikasi dengan satu simpul
$v$. Sisi vertikal yang searah diberi label $e_1$, sisi horizontal yang
searah diberi label $e_2$, dan diagonal penghubung diberi label $e_3$;
persegi dibagi menjadi dua muka $f_1$ dan $f_2$. Data face map lengkap yang
menentukan orientasi adalah

$$
\begin{array}{c|ccc}
 &d_0^2&d_1^2&d_2^2\\ \hline
f_1&e_3&e_1&e_2\\
f_2&e_2&e_1&e_3
\end{array}
\qquad
d_0^1(e_i)=v=d_1^1(e_i)\quad(i=1,2,3).
$$

Jadi diagram dapat dibaca tanpa mengandalkan identifikasi visual sudut atau
arah kepala panah.
:::

Untuk $f_1$ berlaku

$$
d_0^2(f_1)=e_3,\quad d_1^2(f_1)=e_1,\quad d_2^2(f_1)=e_2,
$$

dan untuk $f_2$ berlaku

$$
d_0^2(f_2)=e_2,\quad d_1^2(f_2)=e_1,\quad d_2^2(f_2)=e_3.
$$
:::

::: {.source-audit #o012-rbt-l20-audit-005}
**Audit sumber 20.4.** Notes.tex baris 4122 kehilangan kata “superskrip”
dalam kalimat tentang penghilangan superskrip; edisi menyatakannya lengkap.
Baris 4196 salah menulis indeks sisi sebagai `e=1,2,3`; edisi memperbaikinya
menjadi $i=1,2,3$. Pada baris 4228, indeks $d_1$ harus bertipe $d_1^1$;
dan pada baris 4251, komposisi pertama dalam tanda kurung harus
$g d_1^1 d_0^2$. Kedua perbaikan tercermin dalam definisi dan bukti di atas.
:::

Untuk setiap permukaan kombinatorik $X_\bullet$, kita sekarang dapat
membentuk barisan grup abelian dengan cara yang sama seperti pada graf
berarah. Kita memakai $R=\mathbb Z$ agar notasi ringkas; penggantian
$\mathbb Z$ dengan gelanggang komutatif berunsur satu $R$ bekerja dengan cara
yang sama.

$$
0\longrightarrow\mathbb Z^{X_0}
\xrightarrow{\delta_0}\mathbb Z^{X_1}
\xrightarrow{\delta_1}\mathbb Z^{X_2}
\longrightarrow0.
$$

Untuk $g\in\mathbb Z^{X_0}$ dan $g'\in\mathbb Z^{X_1}$, definisikan

$$
\delta_0(g)=g\circ d_0^1-g\circ d_1^1,
$$

dan

$$
\delta_1(g')
=g'\circ d_0^2-g'\circ d_1^2+g'\circ d_2^2.
$$

Dengan kata lain, untuk $x\in X_2$,

$$
\delta_1(g')(x)
=g'(d_0^2(x))-g'(d_1^2(x))+g'(d_2^2(x)).
$$

Nanti kita buktikan bahwa komposit $\delta_1\delta_0$ memang nol.

::: {.source-margin #o012-rbt-l20-margin-009}
> **Catatan pinggir sumber.** Pemakaian $\mathbb Z$ di sini hanya untuk
> kesederhanaan. Definisi umum dengan gelanggang komutatif berunsur satu
> $R$ mempunyai rumus yang sama.
:::

::: {.remark #o012-rbt-l20-rem-003 data-source-label="rem:basis_finite_complex"}
**Catatan 20.3 (basis pada kompleks berhingga).** Jika setiap
$X_0,X_1,X_2$ berhingga, himpunan $X_i$ dapat dipakai sebagai basis bagi
$\mathbb Z^{X_i}$ dengan mengidentifikasi $x\in X_i$ dengan fungsi
karakteristik yang bernilai $1$ pada $x$ dan $0$ di tempat lain. Beberapa
sumber memakai hanya fungsi berdukungan hingga, tetapi itu bukan ruang
$\mathbb Z^{X_i}$ yang digunakan di sini. Pada kompleks tak berhingga,
penulisan matriks berbasis dapat gagal—misalnya tak hingga banyak sisi dapat
bertemu pada satu simpul—sehingga deskripsi abstrak pemetaan menjadi penting.
:::

::: {.example #o012-rbt-l20-exa-008}
**Contoh 20.8 (kompleks torus).** Untuk $T_\bullet$ pada Contoh 20.7,
barisannya adalah

$$
0\longrightarrow\mathbb Z
\xrightarrow{\delta_0}\mathbb Z^3
\xrightarrow{\delta_1}\mathbb Z^2
\longrightarrow0.
$$

Karena $d_0^1(e_i)=d_1^1(e_i)=v$, maka

$$
\delta_0(g)(e_i)=g(v)-g(v)=0
$$

untuk setiap sisi, sehingga $\delta_0$ adalah peta nol. Dengan basis
$(e_1,e_2,e_3)$ pada $\mathbb Z^{T_1}$ dan $(f_1,f_2)$ pada
$\mathbb Z^{T_2}$, peta $\delta_1$ direpresentasikan (dengan vektor kolom)
oleh

$$
\begin{pmatrix}
-1&1&1\\
-1&1&1
\end{pmatrix}.
$$

Kedua baris sama, tetapi komposit $\delta_1\delta_0$ jelas nol. Jadi ini
memang sebuah kompleks. Kelak kita akan memperoleh

$$
\ker\delta_0\cong\mathbb Z,
\qquad
\ker\delta_1/\operatorname{im}\delta_0\cong\mathbb Z^2,
\qquad
\operatorname{coker}\delta_1\cong\mathbb Z.
$$
:::

::: {.lemma #o012-rbt-l20-lem-001}
**Lema 20.1 (kompleks permukaan kombinatorik).** Untuk setiap permukaan
kombinatorik $X_\bullet$, barisan

$$
C^\bullet(X_\bullet):
0\longrightarrow\mathbb Z^{X_0}
\xrightarrow{\delta_0}\mathbb Z^{X_1}
\xrightarrow{\delta_1}\mathbb Z^{X_2}
\longrightarrow0
$$

adalah kompleks.
:::

::: {.proof #o012-rbt-l20-proof-001}
**Bukti.** Ambil $g\colon X_0\to\mathbb Z$ dan $x\in X_2$. Dengan rumus
definisi,

$$
\begin{aligned}
\delta_1(\delta_0(g))(x)
&=\delta_0(g)(d_0^2x)-\delta_0(g)(d_1^2x)+\delta_0(g)(d_2^2x)\\
&=\bigl(gd_0^1d_0^2-gd_1^1d_0^2\bigr)(x)
 -\bigl(gd_0^1d_1^2-gd_1^1d_1^2\bigr)(x)\\
&\qquad+\bigl(gd_0^1d_2^2-gd_1^1d_2^2\bigr)(x)\\
&=g(d_0^1d_2^2x)-g(d_1^1d_0^2x)
 -g(d_0^1d_1^2x)+g(d_1^1d_1^2x)\\
&\qquad+g(d_0^1d_0^2x)-g(d_1^1d_2^2x)\\
&=0.
\end{aligned}
$$

Pada langkah terakhir dipakai tiga identitas face map:

$$
d_0^1d_2^2=d_1^1d_0^2,
\qquad
d_0^1d_1^2=d_0^1d_0^2,
\qquad
d_1^1d_2^2=d_1^1d_1^2.
$$

Enam suku saling berpasangan dengan tanda berlawanan, sehingga
$\delta_1\circ\delta_0=0$. Ekspansi sumber mengulang satu komposisi dan
menghilangkan komposisi lain; rumus di atas adalah pembetulan bertipe yang
tetap membuktikan klaim yang dimaksud.
\square$
:::

Karakteristik Euler torus kombinatorik adalah

$$
\chi=1-3+2=0.
$$

Kegagalan kompleks ini untuk eksak memberi

$$
\ker\delta_0\cong\mathbb Z,
\qquad
\operatorname{coker}\delta_1\cong\mathbb Z,
\qquad
\ker\delta_1/\operatorname{im}\delta_0\cong\mathbb Z^2.
$$

::: {.source-margin #o012-rbt-l20-margin-010}
> **Catatan pinggir sumber.** Untuk latihan tetrahedron (Notes.tex baris 4270),
> labeli simpul dengan $0,1,2,3$, urutkan tiap sisi dari label lebih rendah ke
> lebih tinggi, lalu ambil peta muka dari model $\Delta[2]$. Teks sumber
> menggandakan kata “from”; pengulangan itu dihapus.
:::

::: {.remark #o012-rbt-l20-rem-004}
**Catatan 20.4 (gelanggang koefisien).** Kita dapat mengganti $\mathbb Z$
dengan gelanggang komutatif berunsur satu $R$. Kernel dan kokernel kemudian
menjadi modul-$R$. Untuk $R=\mathbb Z$, modul tersebut adalah grup abelian;
untuk $R=\mathbb Z/2\mathbb Z$, ia tetap grup abelian tetapi juga membawa
struktur modul yang lebih kaya atas gelanggang tersebut.
:::

::: {.exercise #o012-rbt-l20-ex-003 data-origin="source"}
**Latihan Sumber 20.4 (tetrahedron).** Hitung kompleks grup abelian yang
berasal dari tetrahedron yang dipandang sebagai permukaan kombinatorik, lalu
hitung $\ker\delta_0$ dan

$$
\ker\delta_1/\operatorname{im}\delta_0.
$$

Petunjuk sumber: labeli simpul dengan $0,1,2,3$, urutkan sisi dari label
lebih rendah ke lebih tinggi, lalu definisikan peta muka segitiga memakai
$\Delta[2]$ sebagai model. Solusi lengkap diberikan dalam Pemeriksaan
Penguasaan 20.4.
:::

::: {.exercise #o012-rbt-l20-ex-004 data-origin="source"}
**Latihan Sumber 20.5 (botol Klein).** Pertimbangkan model kombinatorik
botol Klein $K_\bullet$ dengan dua segitiga, tiga sisi, dan satu simpul.

::: {.figure #o012-rbt-l20-fig-007 data-source-format="tikz"}
**Diagram 20.7 (deskripsi semantik botol Klein).** Ada satu simpul $v$,
tiga sisi $e_1,e_2,e_3$, dan dua muka terisi $f_1,f_2$. Semua sisi berawal
dan berakhir di $v$ sebagai data face map tingkat satu. Orientasi muka adalah

$$
\begin{array}{c|ccc}
 &d_0^2&d_1^2&d_2^2\\ \hline
f_1&e_3&e_2&e_1\\
f_2&e_1&e_3&e_2
\end{array}
\qquad
d_0^1(e_i)=v=d_1^1(e_i)\quad(i=1,2,3).
$$

Gambar sumber memiliki dua sisi yang ditempel dengan pembalikan orientasi;
tabel ini mempertahankan seluruh data tanpa mengandalkan arsiran atau
arah kepala panah.
:::

Segitiga dipandang terisi walaupun gambar sumber tidak diberi arsiran. Solusi
lengkap diberikan dalam Pemeriksaan Penguasaan 20.5.
:::

::: {.source-margin #o012-rbt-l20-margin-011}
> **Catatan pinggir sumber.** Pada gambar botol Klein, dua sisi ditempel
> dengan orientasi berlawanan. Data face map di atas adalah penentu mandiri;
> bentuk botol Klein tidak perlu disimpulkan dari posisi gambar.
:::

::: {.source-audit #o012-rbt-l20-audit-006}
**Audit sumber 20.5.** Notes.tex baris 4305 menulis
$d_1^2(f_2)=e_2$, yang mengulang $d_2^2(f_2)$. Edisi memperbaikinya menjadi
$d_1^2(f_2)=e_3$ dan mempertahankan $d_2^2(f_2)=e_2$, konsisten dengan
orientasi model dan menghasilkan kokernel $\mathbb Z/2$.
:::

::: {.source-audit #o012-rbt-l20-audit-007}
**Ledger penyuntingan bahasa.** Notes.tex baris 4040--4041 memakai
“prove” ketika subjeknya tunggal, sehingga edisi memperbaikinya menjadi
“proves”; baris 4044 menambahkan kata kerja “are”; baris 4057 menambahkan
“general” agar memodifikasi “directed graphs”; baris 4151 menambahkan
konjungsi “that” dalam frasa “so degenerate that it has”; dan baris 4341
menambahkan tanda baca setelah “caveats”. Semua diperbaiki dalam alur
Indonesia tanpa mengubah urutan atau isi matematis. Salah eja `simplicty`
(4201), `explicity` (4219), serta pengulangan `from from` (4270) juga
dibetulkan. Pada baris 4273, penyebut latihan dibaca sebagai
$\operatorname{im}\delta_0$, bukan $\ker\delta_0$.
:::

::: {.definition #o012-rbt-l20-def-002}
**Definisi 20.2 (kohomologi kompleks).** Diberikan kompleks $A_\bullet$ dari
modul-$R$ dan bilangan bulat $n$, definisikan modul kohomologi ke-$n$ sebagai

$$
H^n(A_\bullet)
=\frac{\ker\bigl(d_n\colon A_n\to A_{n+1}\bigr)}
{\operatorname{im}\bigl(d_{n-1}\colon A_{n-1}\to A_n\bigr)}.
$$

Karena $d_n d_{n-1}=0$, citra pada penyebut memang merupakan submodul dari
kernel pada pembilang. Gradasinya tetap kohomologis: $d_n$ menaikkan indeks.
:::

::: {.source-audit #o012-rbt-l20-audit-008}
**Audit sumber 20.6.** Fraksi pada Notes.tex baris 4311--4317 menulis
$\ker A_n\xrightarrow{d_n}A_{n+1}$, bukan submodul kernel yang bertipe di
$A_n$. Edisi menulis kernel dan citra sebagai kernel/citra pemetaan yang
eksplisit.
:::

::: {.lemma #o012-rbt-l20-lem-002}
**Lema 20.2 (fungtorialitas kohomologi).** Untuk setiap bilangan bulat $n$,
penetapan

$$
H^n\colon\mathbf{Cplx}_R\longrightarrow R\mathbf{Mod}
$$

adalah fungtor.
:::

::: {.proof #o012-rbt-l20-proof-002 data-source-exercise="true"}
**Bukti (latihan sumber, diselesaikan edisi).** Misalkan
$f\colon A_\bullet\to B_\bullet$ morfisma kompleks. Karena

$$
f_{n+1}d_n^A=d_n^Bf_n,
$$

jika $a\in\ker d_n^A$, maka

$$
d_n^B(f_n(a))=f_{n+1}(d_n^A(a))=0.
$$

Jadi $f_n$ membatasi menjadi pemetaan

$$
\ker d_n^A\longrightarrow\ker d_n^B.
$$

Jika $a=d_{n-1}^A(b)$ adalah coboundary, maka

$$
f_n(a)=f_nd_{n-1}^A(b)=d_{n-1}^Bf_{n-1}(b),
$$

sehingga pemetaan kernel itu mengirim citra $d_{n-1}^A$ ke citra
$d_{n-1}^B$. Dengan sifat universal modul hasil bagi, kita memperoleh

$$
H^n(f)\colon H^n(A_\bullet)\longrightarrow H^n(B_\bullet),
\qquad
[a]\longmapsto[f_n(a)].
$$

Rumus ini terdefinisi baik karena perbedaan dua wakil di dalam citra
$d_{n-1}^A$ dikirim ke citra $d_{n-1}^B$. Untuk identitas,

$$
H^n(\operatorname{id}_{A_\bullet})=\operatorname{id}_{H^n(A_\bullet)}.
$$

Untuk morfisma berurutan $A_\bullet\xrightarrow{f}B_\bullet
\xrightarrow{g}C_\bullet$,

$$
H^n(g\circ f)([a])=[g_nf_n(a)]
=H^n(g)H^n(f)([a]).
$$

Maka $H^n(g\circ f)=H^n(g)\circ H^n(f)$ dan $H^n$ adalah fungtor.
\square$
:::

## Dari ruang ke kompleks: gagasan besar dan batas unit {#o012-rbt-l20-s04}

Gagasan besarnya adalah: ruang dan grup homotopinya sulit, jadi ubah ruang
menjadi kompleks lalu pelajari grup kohomologinya. Kita juga menginginkan
konstruksi ini fungtorial. Sejauh ini, misalnya, kita mengetahui (sebagian
sebagai fakta eksternal) bahwa

$$
\pi_i(S^2,*)=
\begin{cases}
*,&i=0\text{ (terhubung)},\\
0,&i=1\text{ (oleh Seifert--van Kampen)},\\
\mathbb Z,&i=2\text{ (tanpa bukti di sini)},\\
\mathbb Z,&i=3\text{ (juga tanpa bukti di sini)},\\
\vdots&
\end{cases}
$$

Untuk permukaan kombinatorik $T_\bullet$, perhitungan kohomologi hanya
memerlukan aljabar linear dan tampak menangkap sebagian informasi itu dengan
usaha jauh lebih kecil. Namun ada dua kehati-hatian: unit ini belum
membangun fungtor geometris dari setiap permukaan kombinatorik ke ruang
aktual, dan belum ada jaminan bahwa tetrahedron kombinatorik (berbeda dari
ruang aktual) benar-benar menangkap topologi $S^2$. Hasilnya adalah petunjuk
menuju pendekatan berbeda, bukan teorema realisasi.

# Pendamping penguasaan: pemeriksaan, petunjuk, dan solusi lengkap {.unnumbered #o012-rbt-l20-mastery}

Enam paket berikut adalah soal, petunjuk, dan solusi yang ditambahkan oleh
edisi ini. Masing-masing berdiri sendiri; notasi dan arah sisi mengikuti
konvensi $d_1(e)\to d_0(e)$ yang dipakai di seluruh unit.

::: {.exercise #o012-rbt-l20-mcheck-001 data-origin="edition-original"}
**Pemeriksaan Penguasaan 20.1 (koproduk dan arti produk fungsi).** Misalkan
$G_1$ dan $G_2$ graf berarah hingga, dan bentuk $G_1\sqcup G_2$ dengan
gabungan saling lepas pada simpul, sisi, dan *face map*. Buktikan

$$
\ker\delta_{G_1\sqcup G_2}
\cong
\ker\delta_{G_1}\oplus\ker\delta_{G_2}.
$$

Lalu jelaskan secara tepat apa yang berubah bila keluarga grafnya tak hingga,
dan gunakan graf segitiga pada Contoh 20.2 untuk memeriksa bahwa fungsi
konstan memang menghasilkan elemen kernel.
:::

::: {.hint #o012-rbt-l20-hint-001 data-origin="edition-original"}
**Petunjuk.** Untuk himpunan saling lepas, fungsi pada gabungan adalah pasangan
fungsi pada kedua komponen. Tulis $δ$ sebagai matriks blok diagonal. Ingat
bahwa $R^S$ berarti **semua** fungsi $S\to R$, yakni produk; produk dan jumlah
langsung berimpit untuk banyak komponen hingga (atau bila dipilih konvensi
dukungan hingga).
:::

::: {.solution #o012-rbt-l20-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 20.1.** Karena
$V(G_1\sqcup G_2)=V(G_1)\sqcup V(G_2)$, pembatasan dan penggabungan fungsi
memberi isomorfisma

$$
\mathbb Z^{V(G_1\sqcup G_2)}
\xrightarrow{\ \cong\ }
\mathbb Z^{V(G_1)}\times\mathbb Z^{V(G_2)},
\qquad
f\longmapsto(f|_{V(G_1)},f|_{V(G_2)}).
$$

Isomorfisma yang sama berlaku untuk himpunan sisi. Tidak ada sisi yang
menyeberang dari satu komponen ke komponen lain, sehingga

$$
\delta_{G_1\sqcup G_2}(f_1,f_2)
 =(\delta_{G_1}f_1,\delta_{G_2}f_2).
$$

Maka

$$
\ker\delta_{G_1\sqcup G_2}
 =\ker\delta_{G_1}\times\ker\delta_{G_2}.
$$

Karena kedua graf hingga, produk dua modul sama dengan jumlah langsung,
sehingga klaim diperoleh. Untuk keluarga tak hingga $\{G_i\}_{i\in I}$,
identitas yang benar dengan ruang fungsi yang dipakai unit ini adalah

$$
\ker\delta_{\bigsqcup_{i\in I}G_i}
\cong\prod_{i\in I}\ker\delta_{G_i},
$$

bukan jumlah langsung pada umumnya. Jumlah langsung hanya muncul bila $I$
hingga atau bila sejak awal dipilih modul fungsi berdukungan hingga.

Sebagai pemeriksaan, pada segitiga $A,B,C$ matriks kolomnya ialah

$$
M=\begin{pmatrix}-1&1&0\\0&-1&1\\-1&0&1\end{pmatrix}.
$$

Jelas $M(1,1,1)^T=0$, sehingga fungsi konstan
$\underline A+\underline B+\underline C$ berada di kernel. Ini juga
menunjukkan mengapa tanda minus pada generator yang tercetak di sumber tidak
benar.
:::

::: {.exercise #o012-rbt-l20-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 20.2 (graf hingga satu-siklus).** Misalkan $G$ graf
berarah hingga yang terhubung dan graf tak berarah di bawahnya mempunyai tepat
satu siklus. Tunjukkan secara integral bahwa

$$
\ker\delta_G\cong\mathbb Z,
\qquad
\operatorname{coker}\delta_G\cong\mathbb Z.
$$

Jelaskan pula mengapa hipotesis hingga diperlukan bila kita ingin memakai
basis simpul dan sisi serta karakteristik Euler biasa.
:::

::: {.hint #o012-rbt-l20-hint-002 data-origin="edition-original"}
**Petunjuk.** Pilih pohon merentang $T$ dan satu sisi $e_*$ di luar $T$.
Tetapkan akar pada $T$, lalu tentukan nilai fungsi simpul secara berurutan
dari nilai pada sisi-sisi pohon. Untuk kokernel, jumlahkan koordinat sisi pada
siklus unik dengan tanda $+1$ atau $-1$ sesuai orientasi siklus.
:::

::: {.solution #o012-rbt-l20-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 20.2.** Karena $G$ terhubung, jika
$\delta f=0$ maka $f(d_0e)=f(d_1e)$ pada setiap sisi. Nilai fungsi sama di
sepanjang setiap lintasan, jadi $f$ konstan. Sebaliknya fungsi konstan jelas
berada di kernel. Dengan demikian

$$
\ker\delta_G=\mathbb Z\cdot\mathbf 1\cong\mathbb Z.
$$

Ambil pohon merentang $T$. Karena hanya ada satu siklus, tepat satu sisi
$e_*$ tidak berada di $T$, dan $T\cup\{e_*\}$ memuat siklus unik $C$.
Orientasi $C$ dipilih sebarang; tulis $\varepsilon_e=1$ bila orientasi sisi
$e\in C$ searah dengan $C$ dan $\varepsilon_e=-1$ bila berlawanan. Definisikan

$$
\Phi\colon\mathbb Z^E\longrightarrow\mathbb Z,
\qquad
\Phi(y)=\sum_{e\in C}\varepsilon_e y_e.
$$

Untuk $y=\delta f$, suku-suku pada siklus bertelescop karena setiap simpul
muncul sekali sebagai target dan sekali sebagai sumber; jadi
$\Phi(\delta f)=0$. Sebaliknya, ambil $y$ dengan $\Phi(y)=0$. Akarilah $T$
di satu simpul $r$ dan tetapkan $f(r)=0$. Berjalan menjauh dari akar,
tentukan $f$ secara unik agar $\delta f$ sama dengan $y$ pada setiap sisi
pohon (jika arah sisi terbalik, gunakan persamaan yang sama dengan tanda yang
sesuai). Pada sisi $e_*$, selisih $y_{e_*}-\delta f(e_*)$ adalah tepat
$\pm\Phi(y)$, sehingga nol. Jadi $y=\delta f$ dan

$$
\operatorname{im}\delta_G=\ker\Phi.
$$

Peta $\Phi$ surjektif: koordinat pada $e_*$ dapat dipilih $1$ dan koordinat
lain nol, lalu tanda dapat disesuaikan. Teorema isomorfisma pertama memberi

$$
\operatorname{coker}\delta_G
 =\mathbb Z^E/\operatorname{im}\delta_G
 \cong\mathbb Z.
$$

Untuk graf hingga, $|E|=|V|$ pada kasus satu-siklus, sehingga
$\chi=|V|-|E|=0$. Tanpa keterhinggaan, $\mathbb Z^V$ dan $\mathbb Z^E$
adalah produk fungsi; basis koordinat hingga dan hitungan Euler tersebut tidak
boleh dipakai tanpa hipotesis tambahan.
:::

::: {.exercise #o012-rbt-l20-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 20.3 (dua siklus).** Ambil graf sederhana berarah
terhubung dengan simpul $A,B,C,D$ dan sisi

$$
a\colon A\to B,\quad b\colon B\to C,\quad c\colon C\to D,
\quad d\colon D\to A,\quad e\colon A\to C.
$$

Hitung matriks $\delta$, kernel, dan kokernel atas $\mathbb Z$. Tunjukkan
secara eksplisit bahwa hasilnya mencerminkan dua siklus independen.
:::

::: {.hint #o012-rbt-l20-hint-003 data-origin="edition-original"}
**Petunjuk.** Gunakan basis simpul $(A,B,C,D)$ dan sisi $(a,b,c,d,e)$.
Sisi $a,b,c$ membentuk pohon merentang. Setelah koordinat pada tiga sisi itu
dinolkan dengan suatu coboundary, dua koordinat yang tersisa memberikan
invarian bebas.
:::

::: {.solution #o012-rbt-l20-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 20.3.** Dengan aturan target dikurangi sumber, matriks
kolom (baris diindeks oleh sisi) ialah

$$
M=\begin{pmatrix}
-1&1&0&0\\
0&-1&1&0\\
0&0&-1&1\\
1&0&0&-1\\
-1&0&1&0
\end{pmatrix}.
$$

Jika $Mf=0$, sisi $a,b,c$ berturut-turut memberi
$f_B=f_A$, $f_C=f_B$, dan $f_D=f_C$; dua baris terakhir lalu otomatis nol.
Jadi

$$
\ker\delta=\mathbb Z(1,1,1,1)\cong\mathbb Z.
$$

Untuk kokernel, gunakan pohon $T=\{a,b,c\}$. Bagi setiap vektor
$y\in\mathbb Z^5$, pilih $f$ secara berurutan sehingga
$(\delta f)_a=y_a$, $(\delta f)_b=y_b$, dan
$(\delta f)_c=y_c$. Dengan mengurangkan $\delta f$, tersisa hanya koordinat
pada $d$ dan $e$. Tidak ada coboundary yang dapat mengubah kedua koordinat
itu secara independen setelah koordinat pohon dibuat nol: jika semua lima
koordinat $\delta f$ nol, maka $f$ konstan. Karena itu kelas $[d]$ dan $[e]$
adalah pembangkit bebas untuk hasil bagi, dan tidak ada relasi integral di
antaranya. Secara formal, pemetaan

$$
\Psi\colon\mathbb Z^5\longrightarrow\mathbb Z^2,
\qquad
\Psi(y)=(y_d+y_a+y_b+y_c,\;y_e-y_a-y_b),
$$

yang masing-masing mengukur jumlah berarah pada siklus persegi dan segitiga.
Operasi baris dan kolom unimodular (atau konstruksi pohon pada petunjuk)
mengirim $M$ ke bentuk dengan tiga kolom pivot dan dua koordinat bebas. Maka
$\ker\Psi=\operatorname{im}M$ dan

$$
\operatorname{coker}\delta\cong\mathbb Z^2.
$$

Secara topologis, $d$ menutup siklus persegi dan $e$ bersama $a,b$ menutup
siklus segitiga; keduanya bebas setelah memilih pohon. Dengan demikian
$\operatorname{rank}\ker\delta=1$ dan
$\operatorname{rank}\operatorname{coker}\delta=2$, sesuai
$\chi=4-5=-1$.
:::

::: {.exercise #o012-rbt-l20-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 20.4 (batas tetrahedron).** Labeli simpul batas
tetrahedron dengan $0,1,2,3$, orientasikan setiap sisi $ij$ dari $i$ ke $j$
untuk $i<j$, dan orientasikan muka dengan urutan naik. Tuliskan $\delta_0$
dan $\delta_1$ untuk kompleks kohomologisnya, lalu hitung

$$
\ker\delta_0,
\qquad
\ker\delta_1/\operatorname{im}\delta_0,
\qquad
\operatorname{coker}\delta_1.
$$
:::

::: {.hint #o012-rbt-l20-hint-004 data-origin="edition-original"}
**Petunjuk.** Urutkan basis sebagai
$(01,02,03,12,13,23)$ dan $(012,013,023,123)$. Pada muka $ijk$ gunakan
$\delta_1g(ijk)=g_{jk}-g_{ik}+g_{ij}$. Untuk membuktikan semua cocycle
adalah coboundary, tetapkan $f_0=0$ dan $f_i=g_{0i}$.
:::

::: {.solution #o012-rbt-l20-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 20.4.** Dalam basis yang diminta,

$$
\delta_0=
\begin{pmatrix}
-1&1&0&0\\-1&0&1&0\\-1&0&0&1\\
0&-1&1&0\\0&-1&0&1\\0&0&-1&1
\end{pmatrix},
$$

dan

$$
\delta_1=
\begin{pmatrix}
1&-1&0&1&0&0\\
1&0&-1&0&1&0\\
0&1&-1&0&0&1\\
0&0&0&1&-1&1
\end{pmatrix}.
$$

Kolom-kolom $\delta_0$ menunjukkan bahwa $\delta_0 f(ij)=f_j-f_i$.
Karena graf 1-skeleton terhubung, $\delta_0f=0$ tepat ketika $f$ konstan;
jadi

$$
\ker\delta_0=\mathbb Z(1,1,1,1)\cong\mathbb Z,
\qquad \operatorname{rank}\delta_0=3.
$$

Sekarang ambil $g\in\ker\delta_1$. Tetapkan
$f_0=0$, $f_1=g_{01}$, $f_2=g_{02}$, dan $f_3=g_{03}$. Persamaan pada
muka $012,013,023$ masing-masing memberi

$$
g_{12}=g_{02}-g_{01},\qquad
g_{13}=g_{03}-g_{01},\qquad
g_{23}=g_{03}-g_{02}.
$$

Maka $g=\delta_0f$ pada keenam sisi. (Persamaan muka $123$ otomatis
mengikuti tiga persamaan tersebut, atau mengikuti $\delta_1\delta_0=0$.)
Dengan demikian

$$
\ker\delta_1=\operatorname{im}\delta_0,
\qquad
\ker\delta_1/\operatorname{im}\delta_0=0.
$$

Peta $\delta_1$ ber-rank $3$, sehingga, karena kodomainnya $\mathbb Z^4$ dan
semua relasi di atas primitif, bentuk normal Smithnya memiliki tiga pivot
$1$. Akibatnya

$$
\operatorname{coker}\delta_1\cong\mathbb Z.
$$

Jadi batas tetrahedron memiliki $H^0\cong\mathbb Z$, $H^1=0$, dan
$H^2\cong\mathbb Z$ dalam konvensi kohomologis unit ini.
:::

::: {.exercise #o012-rbt-l20-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 20.5 (botol Klein dan tanda orientasi).** Gunakan
model $K_\bullet$ dengan satu simpul, sisi $(e_1,e_2,e_3)$, dan muka
$(f_1,f_2)$, dengan

$$
(d_0^2,d_1^2,d_2^2)(f_1)=(e_3,e_2,e_1),
\qquad
(d_0^2,d_1^2,d_2^2)(f_2)=(e_1,e_3,e_2).
$$

Hitung $\delta_0$, $\delta_1$, dan semua grup kohomologi. Jelaskan mengapa
menukar $d_1^2(f_2)$ menjadi $e_2$ akan mengubah hasil.
:::

::: {.hint #o012-rbt-l20-hint-005 data-origin="edition-original"}
**Petunjuk.** Karena semua sisi berawal dan berakhir di simpul yang sama,
$\delta_0=0$. Tulis vektor sisi sebagai $(x_1,x_2,x_3)$ dan evaluasi
$\delta_1$ pada $f_1$ dan $f_2$; lalu gunakan dua determinan minor untuk bentuk
normal Smith.
:::

::: {.solution #o012-rbt-l20-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 20.5.** Dari $d_0^1(e_i)=v=d_1^1(e_i)$ diperoleh
$\delta_0=0\colon\mathbb Z\to\mathbb Z^3$. Untuk
$g=(x_1,x_2,x_3)$,

$$
\delta_1(g)=
\begin{pmatrix}
1&-1&1\\
1&1&-1
\end{pmatrix}
\begin{pmatrix}x_1\\x_2\\x_3\end{pmatrix}.
$$

Kernel memenuhi
$x_1-x_2+x_3=0$ dan $x_1+x_2-x_3=0$. Menjumlahkan kedua persamaan
memberi $2x_1=0$, sehingga di atas $\mathbb Z$ berlaku $x_1=0$ dan
$x_2=x_3$. Jadi

$$
\ker\delta_1=\mathbb Z(0,1,1),
\qquad H^1(K_\bullet)=\ker\delta_1/\operatorname{im}\delta_0
\cong\mathbb Z.
$$

Untuk kokernel, semua entri matriks mempunyai gcd $1$, sedangkan gcd semua
minor $2\times2$ yang tak nol adalah $2$ (misalnya minor kolom pertama-kedua
bernilai $2$). Bentuk normal Smithnya adalah $\operatorname{diag}(1,2)$,
sehingga

$$
\operatorname{coker}\delta_1\cong\mathbb Z/2\mathbb Z.
$$

Karena $\delta_0=0$, $H^0(K_\bullet)=\mathbb Z$; dan karena tidak ada suku
derajat $3$, $H^2(K_\bullet)=\operatorname{coker}\delta_1$.
Dengan demikian

$$
H^0\cong\mathbb Z,\qquad H^1\cong\mathbb Z,\qquad
H^2\cong\mathbb Z/2\mathbb Z.
$$

Jika mengikuti salah cetak sumber $d_1^2(f_2)=e_2$, baris kedua menjadi
$(1,0,0)$ dan bukan $(1,1,-1)$; kernel serta kokernel yang diperoleh tidak
lagi merupakan model yang dimaksud. Koreksi $e_3$ mempertahankan pembalikan
orientasi dan menghasilkan faktor torsion $\mathbb Z/2$.
:::

::: {.exercise #o012-rbt-l20-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 20.6 (kohomologi, morfisma, dan derajat tinggi).**
Untuk morfisma kompleks $f\colon A_\bullet\to B_\bullet$ atas gelanggang
komutatif berunsur satu $R$, buktikan bahwa peta yang diinduksi pada

$$
H^n(A_\bullet)=\ker(d_n)/\operatorname{im}(d_{n-1})
$$

terdefinisi baik dan funktorial untuk setiap bilangan bulat $n$. Sebagai
aplikasi, hitung $H^n$ dari kompleks torus Unit 20 atas $R$ untuk semua $n$,
termasuk $n\geq3$.
:::

::: {.hint #o012-rbt-l20-hint-006 data-origin="edition-original"}
**Petunjuk.** Gunakan komutativitas
$f_{n+1}d_n^A=d_n^Bf_n$. Persamaan itu mengirim kernel ke kernel dan citra
$d_{n-1}^A$ ke citra $d_{n-1}^B$. Untuk torus, $\delta_0=0$ dan $\delta_1$
memiliki dua baris sama, yaitu $(-1,1,1)$.
:::

::: {.solution #o012-rbt-l20-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 20.6.** Jika $a\in\ker d_n^A$, komutativitas memberi

$$
d_n^Bf_n(a)=f_{n+1}d_n^A(a)=0,
$$

sehingga $f_n$ membatasi ke peta $\ker d_n^A\to\ker d_n^B$. Jika
$a=d_{n-1}^A(b)$, maka

$$
f_n(a)=f_nd_{n-1}^A(b)=d_{n-1}^Bf_{n-1}(b),
$$

jadi citra dikirim ke citra. Oleh karena itu ada peta hasil bagi yang
terdefinisi baik,

$$
H^n(f)\colon H^n(A_\bullet)\longrightarrow H^n(B_\bullet),
\qquad [a]\longmapsto[f_n(a)].
$$

Untuk morfisma identitas, rumus ini adalah identitas. Jika
$A\xrightarrow{f}B\xrightarrow{g}C$, maka pada setiap kelas

$$
H^n(g\circ f)([a])=[g_nf_n(a)]
 =H^n(g)(H^n(f)([a])),
$$

sehingga $H^n(g\circ f)=H^n(g)\circ H^n(f)$. Ini membuktikan
fungtorisitas dan sekaligus menunjukkan bahwa komutativitas morfisma, bukan
sekadar pemetaan modul derajat demi derajat, adalah syarat yang diperlukan.

Untuk torus, dengan basis $(e_1,e_2,e_3)$ dan $(f_1,f_2)$,

$$
0\longrightarrow R\xrightarrow{0}R^3
\xrightarrow{\left(\begin{smallmatrix}-1&1&1\\-1&1&1\end{smallmatrix}\right)}R^2
\longrightarrow0.
$$

Kernel peta terakhir adalah
$\{(x,y,z):-x+y+z=0\}\cong R^2$, misalnya dengan parameter $(y,z)$
dan $x=y+z$. Citra peta terakhir adalah diagonal
$R(1,1)\subset R^2$, karena $-x+y+z$ dapat berupa sembarang unsur $R$.
Maka

$$
H^0(T_\bullet;R)\cong R,
\qquad
H^1(T_\bullet;R)\cong R^2,
\qquad
H^2(T_\bullet;R)\cong R^2/R(1,1)\cong R.
$$

Semua suku kompleks di luar derajat $0,1,2$ nol, sehingga
$H^n(T_\bullet;R)=0$ untuk $n<0$ maupun $n\geq3$. Pernyataan terakhir
adalah konsekuensi dari grading $d_n:A_n\to A_{n+1}$ dan tidak boleh diganti
dengan konvensi homologi yang menurunkan indeks.
:::

::: {.boundary #o012-rbt-l20-boundary-001}
**Batas ke Unit 21.** Notes.tex baris 4346 membuka lingkungan `rem`, lalu
penanda Kuliah 21 muncul pada baris 4347 dan menutup catatan tersebut di unit
berikutnya. Pembukaan itu tidak dipalsukan sebagai catatan lengkap di Unit
20; Unit 21 harus mengambilnya bersama isi dan penutupnya. Kursor sumber
berikutnya yang aman adalah baris 4346.
:::
