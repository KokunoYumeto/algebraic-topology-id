---
title: "Topologi Aljabar"
subtitle: "Unit 9: Kesetiaan, Invariansi Homotopi, dan Pengangkatan Homotopi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l09-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts (2019), tepatnya [Notes.tex baris
1947--2093 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L1947-L2093).
Rentang itu dimulai dengan penanda Kuliah 9 dan teorema kesetiaan fungtor
grupoid fundamental suatu ruang penutup, lalu berakhir tepat setelah
pernyataan teorema yang mengidentifikasi serat dengan ruang koset. Baris 2094
memulai Kuliah 10 dan tidak termasuk dalam unit ini. Bukti sumber bagi teorema
ruang koset baru dimulai pada kuliah berikutnya. Karya sumber tersedia di
bawah [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah
dibaca, pemberian pengenal stabil, dan pemindahan ketiga unsur pinggir ke
urutan bacaan utama: keterangan tentang fungtor setia, latihan kontraksi, dan
diagram pengangkatan homotopi. Diagram tersebut ditulis ulang sebagai diagram
linear beserta uraian semua panahnya. Beberapa cacat sumber diperbaiki secara
independen: salah eja “funtor”, “trivisalisable”, dan “resuls” diperbaiki;
fragmen kalimat sebelum pemetaan ke ruang lintasan dilengkapi dengan hukum
eksponensial yang memang dipakai; salah variabel
$(t,z):=\pi(z)$ diperbaiki menjadi $(t,x):=\pi(z)$; serta “are path” dan
“map in injective” diperbaiki menjadi bentuk yang bertipe dan gramatikal.
Rumus bagi $\tau$ dan $\sigma$ juga menampilkan titik awal lintasan secara
eksplisit, sehingga produk serat yang tersirat dalam sumber dapat diperiksa.

Ada satu persoalan konvensi yang substantif. Sumber menuliskan ruang koset
$G/H$, yang membawa aksi kiri alami. Unit 7--8 menggunakan transpor penutup
sebagai aksi kanan, sebagaimana dituntut oleh urutan konkatenasi yang sudah
ditetapkan. Karena itu teorema penutup unit ini menyatakan kedua bentuk yang
ekuivalen: $G/H$ untuk aksi kiri yang diperoleh dengan membalik unsur grup,
dan $H\backslash G$ untuk aksi kanan monodromi. Subgrup $H$ ditulis sebagai
citra $\pi_*\pi_1(Z,z)$, bukan disamakan secara diam-diam dengan grup asalnya.

Rentang sumber memuat satu latihan pinggir tetapi tidak menyediakan
solusinya. Bagian pendamping penguasaan mempertahankan latihan itu dan
menambahkan empat pemeriksaan edisi dengan solusi lengkap: perbedaan antara
setia dan penuh; invers eksplisit bagi trivialitas di atas $I\times X$;
konstruksi pengangkatan homotopi dari sebuah penampang; serta identifikasi
orbit--stabilisator dengan kedua konvensi koset. Solusi terakhir memberi bukti
mandiri bagi teorema penutup tanpa menyalin ungkapan bukti pada kuliah
berikutnya. Seluruh materi pendamping yang ditambahkan tersedia di bawah CC BY
4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan atau
pengesahan dari penulis sumber.

# Kuliah 9 {#o012-rbt-l09}

Dalam satu arti, kita terutama tertarik pada ruang yang terhubung lintasan.
Meskipun demikian, grupoid fundamental juga berguna ketika ruang dibangun
dari komponen-komponen yang saling lepas. Sekarang kita akan melihat cara lain
untuk memperoleh informasi tentang grupoid fundamental sebuah ruang dari
grupoid fundamental ruang lain.

## Ruang penutup menginduksi fungtor setia {#o012-rbt-l09-s01}

::: {.theorem #o012-rbt-l09-thm-001 data-source-label="thm:cov_space_gives_faithful_functor"}
**Teorema 9.1 (kesetiaan bagi ruang penutup).** Misalkan
$\pi\colon Z\to X$ suatu ruang penutup. Untuk setiap $z_1,z_2\in Z$,
pemetaan

$$
\begin{aligned}
\Pi_1(Z)(z_1,z_2)
&\longrightarrow
\Pi_1(X)(\pi(z_1),\pi(z_2)),\\
[\gamma]&\longmapsto[\pi\circ\gamma]
\end{aligned}
$$

bersifat injektif. Dengan kata lain, fungtor
$\Pi_1(\pi)\colon\Pi_1(Z)\to\Pi_1(X)$ bersifat *setia*.
:::

Bukti teorema ini akan diberikan setelah kita membuktikan sifat pengangkatan
homotopi. Untuk sekarang, kita mencatat satu akibat penting.

::: {.corollary #o012-rbt-l09-cor-001}
**Akibat 9.1 (grup fundamental ruang atas sebagai subgrup).** Untuk ruang
penutup bertitik

$$
\pi\colon(Z,z)\longrightarrow(X,x),
$$

homomorfisma terinduksi

$$
\pi_*\colon\pi_1(Z,z)\longrightarrow\pi_1(X,x)
$$

mengidentifikasi $\pi_1(Z,z)$ secara isomorfik dengan subgrup
$\pi_*(\pi_1(Z,z))\leq\pi_1(X,x)$.
:::

Jadi, jika grupoid fundamental ruang atas suatu penutup diketahui, ukuran
grup fundamental ruang atas memberi batas bawah bagi ukuran grup fundamental
ruang dasar. Secara ekuivalen,

$$
|\pi_1(Z,z)|\leq|\pi_1(X,x)|.
$$

Dengan demikian, jika $\pi_1(X,x)$ berhingga, maka $\pi_1(Z,z)$ juga
berhingga.

## Trivialitas penutup di sepanjang interval {#o012-rbt-l09-s02}

::: {.proposition #o012-rbt-l09-prop-001 data-source-label="prop:cov_space_of_IxX"}
**Proposisi 9.1 (penutup di atas $I\times X$).** Misalkan
$\pi\colon Z\to I\times X$ suatu ruang penutup dan definisikan

$$
Z_0:=Z_{\{0\}\times X}=\pi^{-1}(\{0\}\times X).
$$

Terdapat isomorfisma ruang penutup

$$
Z\xrightarrow{\;\cong\;}I\times Z_0
$$

di atas $I\times X$, dengan $I\times Z_0\to I\times X$ diberikan oleh

$$
(t,z_0)\longmapsto(t,x)
\quad\text{jika}\quad
\pi(z_0)=(0,x).
$$
:::

::: {.proof #o012-rbt-l09-proof-001}
**Bukti.** Pemetaan dari $Z$ menuju $I\times Z_0$ akan berbentuk

$$
\Phi=(\operatorname{pr}_1\circ\pi,\tau),
$$

untuk suatu pemetaan $\tau\colon Z\to Z_0$ yang masih harus dibangun.
Gagasannya sama dengan trivialitas ruang penutup di atas $I$; kasus itu
tepat merupakan kasus khusus $X=\{*\}$.

Untuk setiap $x\in X$, pembatasan

$$
Z_{I\times\{x\}}\longrightarrow I\times\{x\}\cong I
$$

merupakan ruang penutup yang dapat ditrivialkan. Karena itu terdapat pemetaan

$$
\tau_x\colon
Z_{I\times\{x\}}\longrightarrow
I\times Z_{(0,x)}
\xrightarrow{\operatorname{pr}_2}
Z_{(0,x)}.
$$

Pemetaan-pemetaan $\tau_x$ menentukan sebuah fungsi himpunan
$Z\to Z_0$, tetapi kekontinuannya belum langsung terlihat. Kita akan
membangun versi globalnya dari pemetaan-pemetaan yang sudah diketahui
kontinu.

Untuk $(t,x)\in I\times X$, definisikan lintasan

$$
\eta_{(t,x)}\colon I\longrightarrow I\times X,
\qquad
\eta_{(t,x)}(s)=(ts,x).
$$

Lintasan ini berjalan dari $(0,x)$ menuju $(t,x)$ dan berubah secara kontinu
terhadap $(t,x)$. Memang, pemetaan

$$
I\times I\times X\longrightarrow I\times X,
\qquad
(s,t,x)\longmapsto(ts,x)
$$

kontinu. Hukum eksponensial bagi ruang lintasan kemudian memberi pemetaan
kontinu

$$
\begin{aligned}
E\colon I\times X&\longrightarrow(I\times X)^I,\\
(t,x)&\longmapsto\eta_{(t,x)}.
\end{aligned}
$$

Tuliskan $\bar\eta_{(t,x)}(s)=\eta_{(t,x)}(1-s)$ bagi lintasan balik. Pemetaan
$(t,x)\mapsto\bar\eta_{(t,x)}$ kontinu karena, menurut hukum eksponensial,
ia bersesuaian dengan pemetaan kontinu

$$
(s,t,x)\longmapsto((1-s)t,x).
$$

Pemetaan ke kedua produk serat di bawah ini karena itu kontinu; untuk
$\sigma$, koordinat $x$ diperoleh secara kontinu dari pembatasan
$Z_0\to\{0\}\times X$. Dengan operator pengangkatan lintasan kontinu
$\operatorname{Lift}$, definisikan komposit

$$
\begin{aligned}
\tau\colon Z
&\xrightarrow{\;\cong\;}
(I\times X)\times_{I\times X}Z\\
&\longrightarrow
(I\times X)^I\times_{I\times X}Z
\xrightarrow{\operatorname{Lift}}
Z^I
\xrightarrow{\operatorname{ev}_1}
Z,
\end{aligned}
$$

yang pada suatu titik diberikan oleh

$$
z\longmapsto(\pi(z),z)
\longmapsto
(\bar\eta_{\pi(z)},z)
\longmapsto
\widetilde{\bar\eta}_{\pi(z),z}(1).
$$

Produk serat di sini memasangkan suatu lintasan di $I\times X$ dengan titik
di $Z$ di atas titik awal lintasan itu. Jika
$\pi(z)=(t,x)$, maka $\bar\eta_{(t,x)}$ berjalan dari $(t,x)$ menuju
$(0,x)$. Karena itu titik akhir pengangkatannya berada di $Z_{(0,x)}$;
jadi $\tau$ benar-benar memfaktor melalui $Z_0$. Semua pemetaan dalam
komposit tersebut kontinu, sehingga $\tau$ kontinu.

Sekarang bangun invers kontinu bagi $\Phi$. Jika $z_0\in Z_0$ dan
$\pi(z_0)=(0,x)$, angkat lintasan $\eta_{(t,x)}$ mulai dari $z_0$, lalu ambil
titik akhirnya. Dengan kata lain,

$$
\begin{aligned}
\sigma\colon I\times Z_0
&\longrightarrow
(I\times X)^I\times_{I\times X}Z
\xrightarrow{\operatorname{Lift}}
Z^I
\xrightarrow{\operatorname{ev}_1}
Z,\\
(t,z_0)&\longmapsto(\eta_{(t,x)},z_0)
\longmapsto
\widetilde\eta_{(t,x),z_0}(1).
\end{aligned}
$$

Pemetaan ini kontinu. Untuk setiap $x$, pembatasannya merupakan trivialitas
kanonik ruang penutup di atas $I\times\{x\}$. Mengangkat suatu lintasan lalu
lintasan baliknya mengembalikan titik awal, berdasarkan keunikan
pengangkatan lintasan. Akibatnya

$$
\sigma\circ\Phi=\operatorname{id}_Z,
\qquad
\Phi\circ\sigma=\operatorname{id}_{I\times Z_0}.
$$

Jadi $\Phi$ merupakan isomorfisma di atas $I\times X$. $\square$
:::

::: {.corollary #o012-rbt-l09-cor-002 data-source-label="prop:pullback_by_homotopic_maps_iso"}
**Akibat 9.2 (invariansi homotopi bagi tarik balik).** Misalkan
$f,g\colon X\to Y$ homotopik melalui
$H\colon I\times X\to Y$, dengan

$$
H(0,u)=f(u),
\qquad
H(1,u)=g(u).
$$

Jika $Z\to Y$ suatu ruang penutup, maka terdapat isomorfisma ruang penutup

$$
f^*Z\cong g^*Z
$$

di atas $X$.
:::

::: {.proof #o012-rbt-l09-proof-002}
**Bukti.** Bentuk tarik balik

$$
H^*Z\longrightarrow I\times X.
$$

Menurut Proposisi 9.1,

$$
H^*Z\cong I\times f^*Z.
$$

Di sisi lain, pembatasan $H^*Z$ ke $\{1\}\times X$ isomorfik dengan
$g^*Z$. Membatasi isomorfisma di atas ke $\{1\}\times X$ memberikan

$$
g^*Z
\cong
(H^*Z)_{\{1\}\times X}
\cong
(I\times f^*Z)_{\{1\}\times X}
\cong
f^*Z.
$$

Semua isomorfisma ini berada di atas $X$. $\square$
:::

Isomorfisma $f^*Z\cong g^*Z$ yang dihasilkan umumnya bergantung pada homotopi
$H$ yang dipilih; akibat ini menyatakan keberadaan isomorfisma, bukan
kanonisitas yang hanya ditentukan oleh kedua pemetaan ujung.

Kita segera memperoleh kriteria yang menjamin bahwa suatu ruang tidak
memiliki ruang penutup nontrivial.

::: {.corollary #o012-rbt-l09-cor-003}
**Akibat 9.3 (penutup di atas ruang kontraktil).** Jika $X$ kontraktil,
maka untuk setiap $x\in X$ dan setiap ruang penutup $Z\to X$ terdapat
isomorfisma

$$
Z\cong X\times Z_x
$$

di atas $X$.
:::

::: {.proof #o012-rbt-l09-proof-003}
**Bukti.** Pilih kontraksi $H\colon I\times X\to X$ menuju $x$, dan
tuliskan $c_x\colon X\to X$ bagi pemetaan konstan bernilai $x$. Karena
$H$ merupakan homotopi dari $\operatorname{id}_X$ menuju $c_x$, Akibat 9.2
memberi

$$
Z
=
\operatorname{id}_X^*Z
\cong
c_x^*Z
=
X\times Z_x.
$$

Ini adalah isomorfisma ruang penutup di atas $X$. $\square$
:::

::: {.exercise #o012-rbt-l09-ex-001 data-origin="Roberts Notes.tex:2032-2036 marginal exercise"}
**Latihan sumber 9.1 (mengubah titik tujuan kontraksi).** Definisi
kontraktil hanya menjamin kontraksi menuju suatu titik. Buktikan bahwa jika
$X$ kontraktil, maka untuk setiap $x\in X$ terdapat kontraksi
$X$ menuju $x$.
:::

::: {.example #o012-rbt-l09-exa-001}
**Contoh 9.1 (ruang tanpa penutup nontrivial).** Setiap ruang vektor
topologis yang konveks lokal tidak mempunyai ruang penutup nontrivial;
hal yang sama berlaku bagi setiap daerah konveks, bahkan setiap daerah
berbentuk bintang di dalamnya. Dengan “tidak mempunyai ruang penutup
nontrivial” dimaksudkan bahwa setiap penutup isomorfik dengan produk
$X\times S\to X$ untuk suatu himpunan diskret $S$.

Sfera satuan di ruang Hilbert separabel berdimensi tak hingga juga tidak
mempunyai ruang penutup nontrivial. Demikian pula halnya dengan manifold
Stiefel berdimensi tak hingga. Dua pernyataan terakhir memakai fakta
kontraktilitas tingkat lanjut. Sumber tidak membuktikan fakta itu dan tidak
menentukan model maupun topologi bagi manifold Stiefel berdimensi tak hingga;
karena itu keduanya dicatat di sini sebagai klaim sumber, bukan sebagai akibat
yang telah dibuktikan dalam unit ini.
:::

## Sifat pengangkatan homotopi {#o012-rbt-l09-s03}

::: {.corollary #o012-rbt-l09-cor-004}
**Akibat 9.4 (pengangkatan homotopi).** Misalkan
$\pi\colon Z\to Y$ suatu ruang penutup,
$f,g\colon X\to Y$, dan

$$
H\colon I\times X\longrightarrow Y
$$

suatu homotopi dari $f$ menuju $g$. Jika

$$
\widetilde f\colon\{0\}\times X\longrightarrow Z
$$

merupakan pengangkatan $f$, maka terdapat tepat satu homotopi

$$
\widetilde H\colon I\times X\longrightarrow Z
$$

yang mengangkat $H$, membatasi ke $\widetilde f$ pada
$\{0\}\times X$, dan pada $\{1\}\times X$ memberikan suatu pengangkatan
dari $g$.

Diagram yang harus dipenuhi adalah

$$
\begin{array}{ccc}
\{0\}\times X
&\xrightarrow{\ \widetilde f\ }&
Z\\[3pt]
{\scriptstyle i_0}\downarrow
&&
{\scriptstyle\pi}\downarrow\\[3pt]
I\times X
&\xrightarrow{\ H\ }&
Y,
\end{array}
$$

dan panah diagonal yang dicari ialah
$\widetilde H\colon I\times X\to Z$, dengan
$\pi\circ\widetilde H=H$ dan
$\widetilde H\circ i_0=\widetilde f$.
:::

::: {.proof #o012-rbt-l09-proof-004}
**Bukti.** Pengangkatan $\widetilde f$ bersesuaian dengan sebuah penampang

$$
s_f\colon X\longrightarrow f^*Z.
$$

Proposisi 9.1 memberi isomorfisma, yang dinormalisasi pada
$\{0\}\times X$,

$$
I\times f^*Z\xrightarrow{\;\cong\;}H^*Z.
$$

Komposisikan penampang produk

$$
I\times X\longrightarrow I\times f^*Z,
\qquad
(t,u)\longmapsto(t,s_f(u)),
$$

dengan isomorfisma tersebut, lalu dengan proyeksi $H^*Z\to Z$. Hasilnya
adalah pemetaan

$$
\widetilde H\colon I\times X\longrightarrow Z
$$

yang menutupi $H$ dan membatasi ke $\widetilde f$ pada waktu $0$. Pada waktu
$1$, persamaan $\pi\circ\widetilde H=H$ menunjukkan bahwa
$\widetilde H|_{\{1\}\times X}$ mengangkat $g$.

Untuk keunikan, tetapkan $u\in X$. Lintasan $H(-,u)$ di $Y$ mempunyai titik
awal $f(u)$. Setiap pengangkatan $\widetilde H'$ yang memenuhi syarat akan
memberikan lintasan $\widetilde H'(-,u)$ yang mengangkat $H(-,u)$ dan berawal
di $\widetilde f(0,u)$. Keunikan pengangkatan lintasan memaksa

$$
\widetilde H'(-,u)=\widetilde H(-,u).
$$

Ini berlaku bagi setiap $u$, sehingga
$\widetilde H'=\widetilde H$. $\square$
:::

Sekarang kita dapat memberikan bukti Teorema 9.1 yang sebelumnya ditunda.

::: {.proof #o012-rbt-l09-proof-005}
**Bukti Teorema 9.1.** Ambil lintasan
$\gamma,\eta\colon z_1\rightsquigarrow z_2$ di $Z$, dan anggap bahwa
$\pi\circ\gamma$ dan $\pi\circ\eta$ mewakili morfisma yang sama di
$\Pi_1(X)$. Jadi terdapat homotopi berujung tetap

$$
H\colon I\times I\longrightarrow X
$$

dari $\pi\circ\gamma$ menuju $\pi\circ\eta$. Akibat 9.4 mengangkat $H$
menjadi homotopi $\widetilde H$ yang pada sisi waktu awal sama dengan
$\gamma$ dan pada sisi waktu akhir merupakan suatu pengangkatan
$\pi\circ\eta$.

Secara eksplisit, dengan $s$ sebagai parameter homotopi dan $t$ sebagai
parameter lintasan,

$$
H(0,t)=\pi(\gamma(t)),
\qquad
H(1,t)=\pi(\eta(t)),
$$

sedangkan syarat titik ujung tetap adalah

$$
H(s,0)=\pi(z_1),
\qquad
H(s,1)=\pi(z_2).
$$

Karena $H$ mempertahankan titik ujung, kedua pembatasan

$$
H|_{I\times\{i\}},
\qquad i=0,1,
$$

merupakan lintasan konstan. Pembatasan-pembatasan
$\widetilde H|_{I\times\{i\}}$ adalah lintasan di dalam serat-serat ruang
penutup, yang merupakan ruang diskret. Oleh sebab itu kedua lintasan tersebut
konstan. Jadi $\widetilde H$ juga mempertahankan titik ujung.

Lintasan $\widetilde H(1,-)$ dan $\eta$ sama-sama mengangkat
$\pi\circ\eta$ dan mempunyai titik awal $z_1$. Keunikan pengangkatan lintasan
memberi

$$
\widetilde H(1,-)=\eta.
$$

Dengan demikian $\gamma$ dan $\eta$ homotopik relatif terhadap titik-titik
ujung. Keduanya menentukan unsur yang sama di
$\Pi_1(Z)(z_1,z_2)$, sehingga pemetaan pada Teorema 9.1 injektif. $\square$
:::

## Serat sebagai ruang koset {#o012-rbt-l09-s04}

Sejauh ini, banyak hasil kita hanya memberikan batas atau perkiraan yang
menghubungkan serat suatu ruang penutup dengan grup fundamental ruang
dasarnya. Jika ruang atas terhubung lintasan, kita memperoleh deskripsi yang
tepat.

::: {.theorem #o012-rbt-l09-thm-002}
**Teorema 9.2 (serat penutup terhubung sebagai ruang koset).** Misalkan

$$
\pi\colon(Z,z)\longrightarrow(X,x)
$$

suatu ruang penutup dengan $Z$ terhubung lintasan. Tuliskan

$$
G:=\pi_1(X,x),
\qquad
H:=\pi_*\bigl(\pi_1(Z,z)\bigr)\leq G.
$$

Jika aksi monodromi kanan dari Unit 7--8 digunakan, terdapat isomorfisma
himpunan-$G$ kanan

$$
Z_x\cong H\backslash G.
$$

Jika aksi itu diubah menjadi aksi kiri melalui
$g\star u:=u\mathbin{\cdot}g^{-1}$, bentuk yang sama adalah isomorfisma
himpunan-$G$ kiri

$$
Z_x\cong G/H
=
\pi_1(X,x)\big/\pi_*\bigl(\pi_1(Z,z)\bigr).
$$

Bentuk terakhir adalah konvensi yang ditampilkan dalam sumber.
:::

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l09-mastery}

Bagian ini memuat solusi latihan sumber dan empat pemeriksaan tambahan yang
menutup langkah-langkah yang paling mudah terlewat ketika unit dipelajari
secara mandiri.

## Solusi Latihan Sumber 9.1 {#o012-rbt-l09-sol-001}

Karena $X$ kontraktil, terdapat suatu $x_0\in X$ dan homotopi

$$
F\colon I\times X\longrightarrow X
$$

dengan

$$
F(0,u)=u,
\qquad
F(1,u)=x_0.
$$

Tetapkan titik sembarang $x\in X$. Definisikan

$$
K(t,u)=
\begin{cases}
F(2t,u),&0\leq t\leq\frac12,\\[3pt]
F(2-2t,x),&\frac12\leq t\leq1.
\end{cases}
$$

Pada $t=\frac12$, kedua rumus bernilai $x_0$, sehingga lema penempelan
menunjukkan bahwa $K$ kontinu. Selain itu,

$$
K(0,u)=u,
\qquad
K(1,u)=x.
$$

Jadi $K$ merupakan homotopi dari $\operatorname{id}_X$ menuju pemetaan
konstan $c_x$. Karena $x$ dipilih sembarang, kontraksi dapat diarahkan menuju
setiap titik di $X$.

::: {.exercise #o012-rbt-l09-mcheck-002}
**Pemeriksaan penguasaan 9.2 (setia tidak berarti penuh).**

1. Turunkan Akibat 9.1 langsung dari Teorema 9.1.
2. Berikan ruang penutup yang fungtor
   $\Pi_1(Z)\to\Pi_1(X)$-nya setia tetapi tidak penuh.
3. Jelaskan dengan tepat kesimpulan keterhinggaan yang dapat ditarik dari
   penyertaan $\pi_1(Z,z)\hookrightarrow\pi_1(X,x)$.
:::

## Solusi Pemeriksaan 9.2 {#o012-rbt-l09-sol-002}

Untuk $z_1=z_2=z$, himpunan-hom pada Teorema 9.1 adalah grup automorfisma

$$
\Pi_1(Z)(z,z)=\pi_1(Z,z),
\qquad
\Pi_1(X)(x,x)=\pi_1(X,x).
$$

Pemetaan terinduksi tepat $\pi_*$. Karena pemetaan itu injektif dan juga
homomorfisma, ia mengidentifikasi domainnya dengan citranya sebagai subgrup.

Untuk melihat bahwa fungtor tersebut tidak harus penuh, ambil ruang tak kosong
$X$, himpunan diskret $S$ dengan sedikitnya dua unsur, dan penutup trivial

$$
\pi\colon S\times X\longrightarrow X.
$$

Pilih $s_1\ne s_2$ dan $x\in X$, lalu tetapkan
$z_i=(s_i,x)$. Tidak ada lintasan dari $z_1$ menuju $z_2$, sehingga

$$
\Pi_1(S\times X)(z_1,z_2)=\varnothing.
$$

Namun $\Pi_1(X)(x,x)$ tidak kosong karena memuat kelas lintasan konstan.
Pemetaan dari himpunan kosong menuju himpunan tak kosong memang injektif,
tetapi tidak surjektif. Jadi fungtor itu setia tetapi tidak penuh.

Terakhir, injeksi memberi pertidaksamaan kardinal

$$
|\pi_1(Z,z)|\leq|\pi_1(X,x)|.
$$

Jika grup kanan berhingga, grup kiri berhingga dan ordonya membagi ordo grup
kanan menurut Teorema Lagrange. Kebalikannya tidak berlaku: sebuah grup tak
hingga dapat mempunyai subgrup berhingga, bahkan subgrup trivial. Karena itu
keterhinggaan $\pi_1(Z,z)$ saja tidak memaksa keterhinggaan
$\pi_1(X,x)$.

::: {.exercise #o012-rbt-l09-mcheck-003}
**Pemeriksaan penguasaan 9.3 (memeriksa kedua invers trivialitas).** Dengan
notasi Proposisi 9.1, buktikan secara titik demi titik bahwa
$\sigma\circ\Phi=\operatorname{id}_Z$ dan
$\Phi\circ\sigma=\operatorname{id}_{I\times Z_0}$. Periksa pula bahwa kedua
pemetaan berada di atas $I\times X$.
:::

## Solusi Pemeriksaan 9.3 {#o012-rbt-l09-sol-003}

Ambil $z\in Z$ dengan $\pi(z)=(t,x)$, dan tuliskan

$$
z_0:=\tau(z)
=
\widetilde{\bar\eta}_{(t,x),z}(1).
$$

Jadi $z_0$ berada di atas $(0,x)$. Pemetaan $\Phi$ memberi
$\Phi(z)=(t,z_0)$. Pemetaan $\sigma$ kemudian mengangkat
$\eta_{(t,x)}$ mulai dari $z_0$.

Lintasan
$\widetilde{\bar\eta}_{(t,x),z}$ yang dibalik merupakan pengangkatan
$\eta_{(t,x)}$ mulai dari $z_0$ dan berakhir di $z$. Menurut keunikan
pengangkatan lintasan, itulah tepat lintasan yang dipakai oleh $\sigma$.
Karena itu

$$
\sigma(\Phi(z))=z.
$$

Sebaliknya, ambil $(t,z_0)\in I\times Z_0$ dengan
$\pi(z_0)=(0,x)$ dan definisikan

$$
z:=\sigma(t,z_0)
=
\widetilde\eta_{(t,x),z_0}(1).
$$

Pengangkatan balik $\bar\eta_{(t,x)}$ mulai dari $z$ adalah kebalikan dari
pengangkatan $\eta_{(t,x)}$ tadi. Maka titik akhirnya adalah $z_0$, sehingga

$$
\Phi(\sigma(t,z_0))=(t,z_0).
$$

Untuk sifat di atas ruang dasar, jika $\pi(z)=(t,x)$, maka

$$
(I\times Z_0\to I\times X)(\Phi(z))=(t,x)=\pi(z).
$$

Jika $\pi(z_0)=(0,x)$, pengangkatan $\eta_{(t,x)}$ berakhir di atas
$(t,x)$, sehingga

$$
\pi(\sigma(t,z_0))=(t,x).
$$

Jadi kedua pemetaan merupakan pemetaan di atas $I\times X$, dan perhitungan
sebelumnya membuktikan bahwa keduanya saling invers.

::: {.exercise #o012-rbt-l09-mcheck-004}
**Pemeriksaan penguasaan 9.4 (dari penampang menuju pengangkatan
homotopi).** Tulis tarik balik $H^*Z$ sebagai himpunan pasangan, lalu:

1. jelaskan mengapa pengangkatan $\widetilde f$ sama dengan penampang
   $s_f\colon X\to f^*Z$;
2. bangun $\widetilde H$ secara eksplisit melalui trivialitas Proposisi 9.1;
3. buktikan bahwa nilai $\widetilde H(t,u)$ juga dapat dicirikan sebagai titik
   akhir pengangkatan lintasan $s\mapsto H(st,u)$ yang berawal di
   $\widetilde f(0,u)$.
:::

## Solusi Pemeriksaan 9.4 {#o012-rbt-l09-sol-004}

Tarik balik dapat ditulis

$$
H^*Z
=
\{((t,u),w)\in(I\times X)\times Z
\mid H(t,u)=\pi(w)\}.
$$

Serupa dengan itu,

$$
f^*Z
=
\{(u,w)\in X\times Z\mid f(u)=\pi(w)\}.
$$

Karena $\pi\circ\widetilde f(0,-)=f$, rumus

$$
s_f(u)=(u,\widetilde f(0,u))
$$

memberi penampang proyeksi $f^*Z\to X$. Sebaliknya, komponen kedua dari
setiap penampang memberi pengangkatan $f$, sehingga kedua data tersebut
ekuivalen.

Terapkan Proposisi 9.1 pada $H^*Z\to I\times X$. Trivialitas eksplisitnya
memberi isomorfisma

$$
\Theta\colon I\times f^*Z\xrightarrow{\;\cong\;}H^*Z
$$

yang pada $t=0$ adalah identitas. Definisikan

$$
\widetilde H(t,u)
:=
\operatorname{pr}_Z\bigl(\Theta(t,s_f(u))\bigr).
$$

Karena $\Theta(t,s_f(u))$ berada dalam $H^*Z$, secara otomatis

$$
\pi(\widetilde H(t,u))=H(t,u).
$$

Normalisasi pada $t=0$ memberi
$\widetilde H(0,u)=\widetilde f(0,u)$.

Dalam konstruksi Proposisi 9.1, $\Theta$ mengangkat lintasan radial dalam
koordinat interval. Untuk $(t,u)$ tetap, lintasan dasar itu adalah

$$
\lambda_{t,u}(s)=H(st,u),
\qquad 0\leq s\leq1.
$$

Ia berawal di $f(u)$ dan berakhir di $H(t,u)$. Karena itu
$\widetilde H(t,u)$ adalah titik akhir satu-satunya pengangkatan
$\lambda_{t,u}$ yang berawal di $\widetilde f(0,u)$. Karakterisasi ini juga
menjelaskan keunikan: setiap pengangkatan homotopi lain dengan nilai awal yang
sama harus memakai pengangkatan lintasan yang sama untuk setiap $(t,u)$.

::: {.exercise #o012-rbt-l09-mcheck-005}
**Pemeriksaan penguasaan 9.5 (orbit, stabilisator, dan sisi koset).** Dalam
situasi Teorema 9.2, gunakan aksi kanan monodromi

$$
u\mathbin{\cdot}[\gamma]:=\gamma_*(u)
$$

untuk membuktikan bahwa:

1. aksi $G$ pada $Z_x$ transitif;
2. stabilisator $z$ tepat $H=\pi_*\pi_1(Z,z)$;
3. pemetaan $H\backslash G\to Z_x$, $Hg\mapsto z\cdot g$, merupakan
   isomorfisma himpunan-$G$ kanan;
4. setelah aksi kiri didefinisikan oleh $g\star u=u\cdot g^{-1}$, pemetaan
   $G/H\to Z_x$, $gH\mapsto z\cdot g^{-1}$, merupakan isomorfisma
   himpunan-$G$ kiri.
:::

## Solusi Pemeriksaan 9.5 {#o012-rbt-l09-sol-005}

Ambil $u\in Z_x$. Karena $Z$ terhubung lintasan, terdapat lintasan
$\delta\colon z\rightsquigarrow u$ di $Z$. Proyeksinya
$\pi\circ\delta$ adalah loop pada $x$, dan keunikan pengangkatan menunjukkan
bahwa

$$
z\mathbin{\cdot}[\pi\circ\delta]=u.
$$

Jadi orbit $z$ adalah seluruh $Z_x$; aksi tersebut transitif.

Selanjutnya, $[\gamma]\in G$ menstabilkan $z$ jika dan hanya jika
pengangkatan $\gamma$ yang berawal di $z$ juga berakhir di $z$. Dalam hal
itu pengangkatan tersebut merupakan loop di $Z$, dan proyeksi kelasnya adalah
$[\gamma]$. Sebaliknya, proyeksi setiap loop pada $z$ mempunyai transpor yang
mempertahankan $z$. Invariansi transpor terhadap homotopi berujung tetap
menunjukkan bahwa pernyataan ini hanya bergantung pada kelas. Jadi

$$
\operatorname{Stab}_G(z)
=
\pi_*\bigl(\pi_1(Z,z)\bigr)
=H.
$$

Definisikan

$$
\varphi\colon H\backslash G\longrightarrow Z_x,
\qquad
\varphi(Hg)=z\cdot g.
$$

Jika $Hg_1=Hg_2$, maka $g_1=hg_2$ untuk suatu $h\in H$, sehingga

$$
z\cdot g_1
=
(z\cdot h)\cdot g_2
=
z\cdot g_2.
$$

Jadi $\varphi$ terdefinisi baik. Transitivitas membuktikan surjektivitas.
Jika $z\cdot g_1=z\cdot g_2$, maka

$$
z\cdot(g_1g_2^{-1})=z,
$$

sehingga $g_1g_2^{-1}\in H$ dan $Hg_1=Hg_2$. Jadi $\varphi$ injektif.
Selain itu,

$$
\varphi((Hg)\cdot k)
=
\varphi(Hgk)
=
z\cdot(gk)
=
(z\cdot g)\cdot k,
$$

sehingga $\varphi$ ekuivarian untuk aksi kanan.

Untuk konvensi kiri, definisikan $g\star u=u\cdot g^{-1}$. Pemetaan inversi

$$
G/H\longrightarrow H\backslash G,
\qquad
gH\longmapsto Hg^{-1}
$$

terdefinisi baik dan bijektif. Komposisinya dengan $\varphi$ adalah

$$
gH\longmapsto z\cdot g^{-1}.
$$

Untuk $k\in G$,

$$
z\cdot(kg)^{-1}
=
z\cdot g^{-1}k^{-1}
=
k\star(z\cdot g^{-1}),
$$

yang membuktikan ekuivariansi kiri. Dengan demikian kedua bentuk koset pada
Teorema 9.2 menyatakan klasifikasi yang sama, dengan sisi aksi yang dinyatakan
secara eksplisit.
