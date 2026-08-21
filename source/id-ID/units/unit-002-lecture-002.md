---
title: "Topologi Aljabar"
subtitle: "Unit 2 — Topologi Akhir, Perekatan, dan Keterhubungan"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "21 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l02-notice}

Unit ini merupakan terjemahan dan adaptasi Bahasa Indonesia atas *Algebraic Topology* karya David Michael Roberts (2019), tepatnya `Notes.tex` baris 349–584 pada commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`. Penanda `\lecturenum{3}` muncul di tengah baris 585, sesudah kata “This”; seluruh kalimat pada baris 585 dan seterusnya disisihkan untuk unit berikutnya agar batas kuliah tidak menghasilkan fragmen kalimat. Karya sumber tersedia di bawah [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah dibaca, pemberian pengenal stabil, pemindahan satu latihan dari catatan pinggir ke blok latihan, pelengkapan bukti yang hanya diisyaratkan oleh sumber, dan tujuh koreksi terbatas: tanda pembentuk himpunan pada definisi $D^n$, faktor koordinat dalam pemeriksaan kontinuitas kontraksi, argumen nilai antara untuk ruang diskret, peubah terikat yang hilang pada syarat surjektif bersama, kasus ruang kosong dalam definisi keterhubungan, serta dua syarat kontinuitas yang hilang pada klaim tentang lintasan dan pemetaan ke ruang diskret. Materi pendamping penguasaan setelah teks inti ditulis khusus untuk edisi ini dan juga tersedia di bawah CC BY 4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

# Kuliah 2 {#o012-rbt-l02}

## Kelanjutan topologi awal {#o012-rbt-l02-s01}

::: {.example #o012-rbt-l02-exa-001}
**Contoh 2.1 (topologi subruang).** Misalkan keluarga fungsi hanya terdiri atas satu pemetaan *injektif*, yaitu
$\iota\colon X\hookrightarrow Y$, dengan $Y$ suatu ruang topologis. Topologi awal pada $X$ adalah topologi subruang: lingkungan dasar dari $x$ berbentuk

$$
\iota^{-1}(N),
$$

dengan $N$ lingkungan dasar dari $\iota(x)$. Jika $X$ dipandang sebagai himpunan bagian dari $Y$, himpunan ini pada dasarnya adalah $N\cap X$.
:::

::: {.example #o012-rbt-l02-exa-002}
**Contoh 2.2 (fungsi konstan).** Sebaliknya, misalkan
$c_{y_0}\colon X\to Y$ adalah fungsi konstan yang mengirim setiap $x\in X$ ke $y_0\in Y$. Untuk setiap lingkungan $N$ dari $y_0$,

$$
c_{y_0}^{-1}(N)=X.
$$

Jadi satu-satunya lingkungan dari setiap $x\in X$ dalam topologi awal tersebut adalah $X$ sendiri. Dengan demikian, topologi awal yang dihasilkan oleh fungsi konstan adalah topologi indiskret.
:::

Secara umum, suatu keluarga fungsi $f_\alpha\colon X\to Y_\alpha$ menentukan fungsi tunggal

$$
(f_\alpha)\colon X\longrightarrow\prod_\alpha Y_\alpha,
\qquad
x\longmapsto\bigl(f_\alpha(x)\bigr)_\alpha.
$$

Jika $\prod_\alpha Y_\alpha$ diberi topologi produk, topologi awal pada $X$ yang dibangkitkan oleh keluarga $\{f_\alpha\}$ sama dengan topologi awal yang dibangkitkan oleh fungsi tunggal $(f_\alpha)$. Oleh karena itu, jika $(f_\alpha)$ injektif, $X$ mewarisi topologi subruang dari ruang produk tersebut. Inilah penggunaan utama topologi awal yang akan kita jumpai.

::: {.example #o012-rbt-l02-exa-003}
**Contoh 2.3 (submanifold).** Suatu submanifold $M\subseteq\mathbb{R}^n$ memperoleh topologinya dari fungsi-fungsi koordinat

$$
M\hookrightarrow\mathbb{R}^n\xrightarrow{\operatorname{pr}_i}\mathbb{R}.
$$

Suatu pemetaan menuju $M$ kontinu jika dan hanya jika komposisinya dengan setiap fungsi koordinat kontinu.
:::

::: {.exercise #o012-rbt-l02-ex-001}
**Latihan 2.1.** Diberikan suatu himpunan $X$, ruang topologis $Y$, dan fungsi $f\colon X\to Y$. Andaikan $x_1,x_2\in X$ memenuhi $f(x_1)=f(x_2)$. Buktikan bahwa, dalam topologi awal pada $X$, subset $V\subseteq X$ merupakan lingkungan dari $x_1$ jika dan hanya jika $V$ merupakan lingkungan dari $x_2$.
:::

## Topologi akhir dan ruang hasil bagi {#o012-rbt-l02-s02}

Konstruksi berikut akan lebih penting bagi kita dan mungkin belum dikenal oleh sebagian besar pembaca.

::: {.definition #o012-rbt-l02-def-001}
**Definisi 2.1 (topologi akhir).** Misalkan $X$ adalah suatu himpunan; $(Z_\beta,\mathcal{N}_\beta)$, $\beta\in J$, adalah keluarga ruang topologis, dengan ruang yang sama boleh muncul lebih dari sekali; dan
$g_\beta\colon Z_\beta\to X$ adalah keluarga fungsi. Perhatikan bahwa arah fungsi-fungsi ini berlawanan dengan arah fungsi pada topologi awal.

*Topologi akhir* pada $X$ didefinisikan sebagai berikut: subset $U\subseteq X$ terbuka jika dan hanya jika

$$
g_\beta^{-1}(U)\text{ terbuka dalam }Z_\beta
\quad\text{untuk setiap }\beta\in J.
$$

Topologi akhir lebih mudah dirumuskan dengan himpunan terbuka daripada dengan lingkungan.
:::

::: {.lemma #o012-rbt-l02-lem-001}
**Lema 2.1 (sifat universal topologi akhir).** Setelah $X$ diberi topologi akhir, semua fungsi $g_\beta\colon Z_\beta\to X$ kontinu. Selain itu, suatu fungsi $h\colon X\to W$ kontinu jika dan hanya jika
$h\circ g_\beta\colon Z_\beta\to W$ kontinu untuk setiap $\beta\in J$.
:::

Kita akan sering menggunakan dua kasus khusus berikut.

::: {.example #o012-rbt-l02-exa-004}
**Contoh 2.4 (topologi hasil bagi).** Misalkan $Z$ adalah ruang topologis dan $\sim$ suatu relasi ekuivalensi pada $Z$. Definisikan
$X=Z/{\sim}$ dan pemetaan hasil bagi

$$
\pi\colon Z\to X,
\qquad
y\longmapsto[y].
$$

Topologi akhir pada $X$ terdiri atas subset-subset $U\subseteq X$ yang memenuhi

$$
U\text{ terbuka dalam }X
\quad\Longleftrightarrow\quad
\pi^{-1}(U)\text{ terbuka dalam }Z.
$$
:::

Sebagai contoh, berikan $S^2$ topologi awal yang dibangkitkan oleh fungsi-fungsi koordinat

$$
x_i\colon S^2\hookrightarrow\mathbb{R}^3
\xrightarrow{\operatorname{pr}_i}\mathbb{R};
$$

ini adalah topologi biasa pada $S^2$. Bentuk relasi ekuivalensi yang dibangkitkan oleh
$x\sim -x$ untuk setiap $x\in S^2$. Ruang hasil baginya adalah bidang projektif real
$\mathbb{RP}^2$. Kita memberinya topologi akhir yang berasal dari
$S^2\to\mathbb{RP}^2$; topologi inilah yang dimilikinya sebagai manifold. Sebagai catatan, pemetaan ini menjadikan $S^2$ suatu *ruang penutup* dari $\mathbb{RP}^2$. Ruang penutup akan dipelajari pada bagian pertama mata kuliah ini.

## Gabungan saling lepas dan sifat universalnya {#o012-rbt-l02-s03}

Ingat kembali gabungan saling lepas dari himpunan-himpunan. Untuk keluarga himpunan
$\{Z_\beta\}_{\beta\in J}$ terdapat injeksi

$$
\operatorname{in}_\gamma\colon Z_\gamma
\hookrightarrow\bigsqcup_\beta Z_\beta,
$$

dengan salinan-salinan $Z_\beta$ saling lepas. Jika setiap $Z_\beta$ adalah ruang topologis, kita memberikan
$\bigsqcup_\beta Z_\beta$ topologi akhir yang dibangkitkan oleh semua pemetaan
$\operatorname{in}_\gamma$. Topologi ini disebut *topologi gabungan saling lepas* atau *topologi jumlah*, dan ruangnya kadang-kadang disebut *jumlah topologis*. Suatu titik di dalamnya dapat ditulis sebagai pasangan $(\beta,z)$ dengan $z\in Z_\beta$.

::: {.exercise #o012-rbt-l02-ex-002}
**Latihan 2.2 (latihan pinggir pada sumber).** Buktikan bahwa pemetaan kanonik

$$
\Phi\colon\bigsqcup_\beta(X\times Z_\beta)
\longrightarrow X\times\bigsqcup_\beta Z_\beta,
\qquad
\Phi\bigl(\beta,(x,z)\bigr)=\bigl(x,(\beta,z)\bigr),
$$

adalah suatu homeomorfisme.
:::

::: {.exercise #o012-rbt-l02-ex-003}
**Latihan 2.3 (pemetaan keluar dari suatu jumlah).** Diberikan fungsi-fungsi kontinu
$h_\beta\colon Z_\beta\to W$, buktikan bahwa terdapat tepat satu fungsi kontinu

$$
h=\langle h_\beta\rangle\colon\bigsqcup_\beta Z_\beta\to W
$$

yang memenuhi $h_\beta=h\circ\operatorname{in}_\beta$ untuk setiap $\beta$. Dengan kata lain, diagram berikut komutatif:

$$
\begin{array}{ccc}
Z_\gamma & \xrightarrow{\operatorname{in}_\gamma}
& \displaystyle\bigsqcup_\beta Z_\beta\\[4pt]
& \searrow_{h_\gamma} & \downarrow h\\[-2pt]
& & W
\end{array}
$$
:::

::: {.lemma #o012-rbt-l02-lem-002}
**Lema 2.2.** Topologi akhir pada $X$ yang dibangkitkan oleh
$g_\beta\colon Z_\beta\to X$ sama dengan topologi akhir yang dibangkitkan oleh fungsi tunggal

$$
g=\langle g_\beta\rangle\colon
\bigsqcup_\beta Z_\beta\to X,
$$

dengan domain diberi topologi jumlah.
:::

::: {.proof #o012-rbt-l02-proof-001}
**Bukti.** Untuk setiap $U\subseteq X$,

$$
\begin{aligned}
U\text{ terbuka}
&\Longleftrightarrow
g_\beta^{-1}(U)\text{ terbuka untuk setiap }\beta\\
&\Longleftrightarrow
(g\circ\operatorname{in}_\beta)^{-1}(U)
=\operatorname{in}_\beta^{-1}\bigl(g^{-1}(U)\bigr)
\text{ terbuka untuk setiap }\beta\\
&\Longleftrightarrow
g^{-1}(U)\text{ terbuka dalam topologi jumlah}.
\end{aligned}
$$

Kondisi pertama mendefinisikan topologi akhir untuk keluarga $\{g_\beta\}$, sedangkan kondisi terakhir mendefinisikan topologi akhir untuk $g$. Jadi kedua topologi itu sama. $\square$
:::

Jika keluarga $g_\beta\colon Z_\beta\to X$ *surjektif secara bersama-sama*, artinya

$$
\forall x\in X\;\exists\beta\in J\;\exists z\in Z_\beta
\quad g_\beta(z)=x,
$$

kita dapat menafsirkan topologi akhir sebagai topologi perekatan. Berikan relasi ekuivalensi pada
$\bigsqcup_\beta Z_\beta$ dengan

$$
(\beta_1,z_1)\sim(\beta_2,z_2)
\quad\Longleftrightarrow\quad
g_{\beta_1}(z_1)=g_{\beta_2}(z_2)\in X.
$$

Sebagai himpunan, $X$ adalah himpunan kelas ekuivalensi dari relasi ini. Jadi kita dapat memandang $X$ sebagai hasil perekatan himpunan-himpunan yang mendasari ruang-ruang $Z_\beta$. Topologi akhir adalah topologi alami pada ruang yang diperoleh dengan merekatkan ruang-ruang tersebut.

## Sampul dan lema perekatan {#o012-rbt-l02-s04}

::: {.exercise #o012-rbt-l02-ex-004}
**Latihan 2.4 (sampul terbuka).** Misalkan $\{U_\alpha\}$ adalah suatu sampul terbuka dari ruang $X$. Buktikan bahwa topologi $X$ adalah topologi akhir yang dibangkitkan oleh semua inklusi

$$
U_\alpha\hookrightarrow X,
$$

atau, secara ekuivalen, oleh pemetaan

$$
\bigsqcup_\alpha U_\alpha\longrightarrow X.
$$
:::

::: {.example #o012-rbt-l02-exa-005}
**Contoh 2.5 (atlas manifold).** Setiap manifold $M$ mempunyai topologi akhir yang berasal dari sembarang atlas yang dipilih untuknya.
:::

::: {.exercise #o012-rbt-l02-ex-005}
**Latihan 2.5 (sampul tertutup berhingga).** Misalkan
$\{V_i\}_{i=1}^n$ adalah sampul tertutup berhingga dari $X$. Buktikan bahwa topologi $X$ adalah topologi akhir yang dibangkitkan oleh

$$
\bigsqcup_{i=1}^nV_i\longrightarrow X.
$$
:::

::: {.example #o012-rbt-l02-exa-006}
**Contoh 2.6 (selang yang dipecah).** Setiap selang tertutup
$[a,b]\subset\mathbb{R}$ dengan topologi subruang mempunyai topologi akhir yang berasal dari koleksi subselang

$$
[a,t_1],\ [t_1,t_2],\ \ldots,\ [t_k,b],
$$

yang masing-masing diberi topologi subruang dari $\mathbb{R}$.
:::

Latihan-latihan tersebut menghasilkan pernyataan yang biasanya disebut *lema perekatan* atau *lema penempelan*.

::: {.lemma #o012-rbt-l02-lem-003}
**Lema 2.3 (lema perekatan).** Misalkan $X$ adalah ruang topologis dan
$\{U_\alpha\}_{\alpha\in I}$ suatu sampul terbuka sembarang, atau
$\{V_i\}_{i=1}^n$ suatu sampul tertutup berhingga. Misalkan pula $Y$ adalah ruang topologis. Jika pembatasan fungsi $f\colon X\to Y$ ke setiap $U_\alpha$ kontinu—atau, dalam kasus kedua, pembatasannya ke setiap $V_i$ kontinu—maka $f$ kontinu pada $X$.
:::

Kelak kita akan menjumpai ruang-ruang yang dibangun dengan merekatkan banyak ruang “sederhana”, misalnya cakram

$$
D^n:=\bigl\{x\in\mathbb{R}^n\mid\lVert x\rVert\le 1\bigr\},
$$

dengan topologi subruang dari $\mathbb{R}^n$. Dalam konteks ini, “sederhana” secara kasar berarti “dapat diciutkan menjadi satu titik”.

## Homotopi dan kontraktibilitas {#o012-rbt-l02-s05}

“Dapat diciutkan” menyatakan suatu proses kontinu yang berlangsung sepanjang waktu. Ambil
$I=[0,1]$ dan definisikan

$$
\begin{aligned}
H\colon I\times D^n&\longrightarrow D^n,\\
(t,\mathbf{x})&\longmapsto(1-t)\mathbf{x}.
\end{aligned}
$$

Pemetaan ini memang bernilai di $D^n$, sebab
$\lVert(1-t)\mathbf{x}\rVert=(1-t)\lVert\mathbf{x}\rVert\le1$
untuk $0\le t\le1$ dan $\mathbf{x}\in D^n$.

Untuk setiap $t\in I$, fungsi ini memberi pemetaan
$H_t\colon D^n\to D^n$. Pada kedua ujung selang,

$$
H_0=\operatorname{id}_{D^n},
\qquad
H_1(\mathbf{x})=0.
$$

Fungsi $H$ kontinu. Untuk melihatnya, ingat bahwa $D^n\subset\mathbb{R}^n$ dan
$I\subset\mathbb{R}$ diberi topologi subruang, sedangkan $\mathbb{R}^n$ diberi topologi produk. Karena topologi pada $D^n$ adalah topologi awal untuk fungsi-fungsi koordinat
$x_i\colon D^n\to\mathbb{R}$, kontinuitas $H$ dapat diperiksa koordinat demi koordinat. Komposisi koordinat ke-$i$ adalah

$$
\begin{aligned}
I\times D^n
&\xrightarrow{\operatorname{id}_I\times x_i} I\times\mathbb{R}
\longrightarrow\mathbb{R}\times\mathbb{R}
\xrightarrow{\ \mu\ }\mathbb{R},\\
(t,\mathbf{x})
&\longmapsto(t,x_i)
\longmapsto(1-t,x_i)
\longmapsto(1-t)x_i,
\end{aligned}
$$

dengan $\mu(a,b)=ab$.

::: {.exercise #o012-rbt-l02-ex-006}
**Latihan 2.6 (produk pemetaan).** Jika
$f\colon X\to W$ dan $g\colon Y\to Z$ kontinu, buktikan bahwa

$$
f\times g\colon X\times Y\to W\times Z,
\qquad
(x,y)\longmapsto(f(x),g(y)),
$$

juga kontinu. Jika $X$ dan $Y$ masing-masing mempunyai sekurang-kurangnya satu titik, buktikan pula implikasi sebaliknya: kontinuitas $f\times g$ mengakibatkan kontinuitas $f$ dan $g$.
:::

Jadi, untuk membuktikan $H$ kontinu, tinggal membuktikan bahwa perkalian
$\mu\colon\mathbb{R}\times\mathbb{R}\to\mathbb{R}$ kontinu. Topologi biasa pada $\mathbb{R}$ berasal dari metrik, sehingga kita dapat memakai kriteria barisan untuk kontinuitas. Jika
$(a_n,b_n)\to(a,b)$ dalam $\mathbb{R}\times\mathbb{R}$, maka

$$
\begin{aligned}
|a_nb_n-ab|
&=|a_nb_n-ab_n+ab_n-ab|\\
&\le |a_n-a|\,|b_n|+|a|\,|b_n-b|\\
&\le |a_n-a|\sup_n|b_n|+|a|\,|b_n-b|\\
&\longrightarrow0+0=0.
\end{aligned}
$$

Barisan $(b_n)$ terbatas karena konvergen. Maka perkalian kontinu, sehingga setiap fungsi koordinat dari $H$ kontinu dan akhirnya $H$ sendiri kontinu.

::: {.definition #o012-rbt-l02-def-002}
**Definisi 2.2 (ruang kontraktil).** Ruang $X$ disebut *kontraktil*—atau *dapat dikontraksikan ke* $x_0\in X$—jika terdapat titik $x_0\in X$ dan fungsi kontinu

$$
H\colon I\times X\to X
$$

yang memenuhi, untuk setiap $x\in X$,

$$
H(0,x)=x,
\qquad
H(1,x)=x_0.
$$

Fungsi $H$ disebut suatu *kontraksi*.
:::

Kita telah membuktikan bahwa $D^n$ kontraktil.

::: {.exercise #o012-rbt-l02-ex-007}
**Latihan 2.7.** Buktikan bahwa $\mathbb{R}$ kontraktil. Buktikan pula bahwa produk sembarang dari ruang-ruang kontraktil adalah kontraktil.
:::

::: {.example #o012-rbt-l02-exa-007}
**Contoh 2.7 (ruang diskret yang kontraktil).** Misalkan ruang diskret $S$ kontraktil ke suatu titik $*\in S$ melalui
$h\colon I\times S\to S$. Untuk $s\in S$, batasi $h$ pada $I\times\{s\}$ sehingga diperoleh lintasan

$$
h_s\colon I\to S,
\qquad
h_s(0)=s,
\quad
h_s(1)=*.
$$

Andaikan $s\ne *$. Karena $S$ diskret, fungsi karakteristik

$$
\chi_{\{*\}}\colon S\to\mathbb{R},
\qquad
\chi_{\{*\}}(*)=1,
\quad
\chi_{\{*\}}(u)=0\text{ untuk }u\ne *,
$$

kontinu. Komposisi
$\widetilde h=\chi_{\{*\}}\circ h_s\colon I\to\mathbb{R}$ juga kontinu, mempunyai
$\widetilde h(0)=0$ dan $\widetilde h(1)=1$, tetapi citranya termuat dalam $\{0,1\}$. Teorema nilai antara menyatakan bahwa citranya harus memuat setiap nilai di antara $0$ dan $1$, suatu kontradiksi. Jadi tidak ada $s\ne *$, dan $S$ tepat mempunyai satu anggota.
:::

::: {.question #o012-rbt-l02-q-001}
**Pertanyaan 2.1.** Jika $X$ kontraktil, apakah pilihan titik $x_0\in X$ berpengaruh? Jika $X$ dapat dikontraksikan ke $x_0$, apakah $X$ juga dapat dikontraksikan ke setiap $x\ne x_0$?
:::

Suatu selang hanya dapat dipetakan secara kontinu ke ruang diskret jika pemetaannya konstan; secara ekuivalen, citranya hanya terdiri atas satu titik. Sifat ini cukup penting untuk diberi nama.

::: {.definition #o012-rbt-l02-def-003}
**Definisi 2.3 (keterhubungan).** Ruang $X$ disebut *terhubung* jika setiap pemetaan kontinu dari $X$ ke suatu ruang diskret mempunyai citra yang memuat paling banyak satu titik.

Definisi ini ekuivalen dengan definisi keterhubungan yang biasa dan, seperti definisi biasa itu, menggolongkan ruang kosong sebagai ruang terhubung. Untuk ruang tak kosong, “paling banyak satu titik” tentu berarti “tepat satu titik”.
:::

Selang $I$ merupakan contoh ruang terhubung. Lebih kuat lagi, jika dua titik $x,y\in X$ dihubungkan oleh suatu *lintasan*, yaitu pemetaan kontinu

$$
\gamma\colon I\to X,
\qquad
\gamma(0)=x,
\quad
\gamma(1)=y,
$$

maka setiap fungsi kontinu $f\colon X\to S$ ke ruang diskret memenuhi $f(x)=f(y)$.

::: {.example #o012-rbt-l02-exa-008}
**Contoh 2.8.** Setiap ruang kontraktil terhubung. Memang, jika $X$ kontraktil melalui $H$ ke $x_0$, maka untuk setiap $y\in X$ pemetaan
$t\mapsto H(t,y)$ adalah lintasan dari $y$ ke $x_0$. Karena itu, untuk setiap pemetaan kontinu
$f\colon X\to S$ ke ruang diskret,

$$
f(y)=f(x_0)
$$

untuk semua $y\in X$. Jadi citra $f$ hanya mempunyai satu titik.
:::

Ada banyak ruang yang terhubung tetapi tidak kontraktil, namun kita belum dapat membuktikannya pada tahap ini.

# Pendamping penguasaan terpecahkan {.unnumbered #o012-rbt-l02-mastery}

Bagian ini merupakan materi baru untuk edisi Bahasa Indonesia. Setiap latihan dan pertanyaan pada Kuliah 2 dijawab lengkap; dua sifat universal yang menjadi penghubung utama argumen perekatan juga dibuktikan secara eksplisit.

## Solusi Latihan 2.1 {#o012-rbt-l02-sol-001}

Dalam topologi awal yang dibangkitkan oleh $f$, lingkungan dasar dari $x\in X$ berbentuk
$f^{-1}(N)$, dengan $N$ lingkungan dari $f(x)$ dalam $Y$.

Andaikan $V$ merupakan lingkungan dari $x_1$. Maka terdapat lingkungan $N$ dari
$f(x_1)$ dengan

$$
f^{-1}(N)\subseteq V.
$$

Karena $f(x_1)=f(x_2)$, himpunan $N$ juga merupakan lingkungan dari $f(x_2)$, sehingga
$f^{-1}(N)$ adalah lingkungan dasar dari $x_2$. Jadi $V$ merupakan lingkungan dari $x_2$.
Argumen yang sama dengan menukar $x_1$ dan $x_2$ memberi implikasi sebaliknya.

**Makna.** Topologi awal tidak dapat membedakan dua titik yang mempunyai citra sama di bawah semua pemetaan pembangkit. Untuk suatu keluarga $\{f_\alpha\}$, argumen yang sama berlaku jika
$f_\alpha(x_1)=f_\alpha(x_2)$ untuk setiap $\alpha$.

## Bukti lengkap Lema 2.1 {#o012-rbt-l02-check-001}

Ambil $U\subseteq X$ terbuka dalam topologi akhir. Menurut definisi,
$g_\beta^{-1}(U)$ terbuka dalam $Z_\beta$ untuk setiap $\beta$. Jadi setiap $g_\beta$ kontinu.

Jika $h\colon X\to W$ kontinu, maka setiap komposisi $h\circ g_\beta$ kontinu. Sebaliknya, andaikan semua $h\circ g_\beta$ kontinu. Untuk setiap himpunan terbuka $O\subseteq W$ dan setiap $\beta$,

$$
g_\beta^{-1}\bigl(h^{-1}(O)\bigr)
=(h\circ g_\beta)^{-1}(O)
$$

terbuka dalam $Z_\beta$. Definisi topologi akhir lalu menyatakan bahwa $h^{-1}(O)$ terbuka dalam $X$. Karena hal ini berlaku untuk setiap $O$, fungsi $h$ kontinu.

## Solusi Latihan 2.2 {#o012-rbt-l02-sol-002}

Pemetaan $\Phi$ jelas bijektif, dengan invers

$$
\Psi\bigl(x,(\beta,z)\bigr)=\bigl(\beta,(x,z)\bigr).
$$

Untuk setiap $\beta$, pembatasan $\Phi$ pada komponen $X\times Z_\beta$ adalah

$$
X\times Z_\beta
\xrightarrow{\operatorname{id}_X\times\operatorname{in}_\beta}
X\times\bigsqcup_\gamma Z_\gamma,
$$

yang kontinu menurut Latihan 2.6. Karena domain $\Phi$ diberi topologi jumlah, sifat universal topologi akhir menunjukkan bahwa $\Phi$ kontinu.

Untuk kontinuitas $\Psi$, perhatikan bahwa setiap komponen
$\operatorname{in}_\beta(Z_\beta)$ terbuka dalam $\bigsqcup_\gamma Z_\gamma$: prabayangannya pada suatu komponen $Z_\gamma$ adalah $Z_\gamma$ jika $\gamma=\beta$ dan kosong jika tidak. Oleh karena itu,

$$
X\times\operatorname{in}_\beta(Z_\beta)
$$

membentuk sampul terbuka dari $X\times\bigsqcup_\gamma Z_\gamma$. Pada komponen ini, pembatasan $\Psi$ adalah komposisi invers homeomorfisme kanonik
$X\times Z_\beta\to X\times\operatorname{in}_\beta(Z_\beta)$ dengan inklusi komponen
$X\times Z_\beta\hookrightarrow\bigsqcup_\gamma(X\times Z_\gamma)$, sehingga kontinu. Lema perekatan memberi bahwa $\Psi$ kontinu secara global. Jadi $\Phi$ adalah homeomorfisme.

## Solusi Latihan 2.3 {#o012-rbt-l02-sol-003}

Definisikan fungsi $h$ pada gabungan saling lepas dengan

$$
h(\beta,z)=h_\beta(z).
$$

Fungsi ini unik dengan sifat
$h\circ\operatorname{in}_\beta=h_\beta$, sebab setiap titik pada gabungan saling lepas berada pada tepat satu komponen. Karena topologi jumlah adalah topologi akhir bagi pemetaan-pemetaan inklusi tersebut, Lema 2.1 memberi

$$
h\text{ kontinu}
\quad\Longleftrightarrow\quad
h\circ\operatorname{in}_\beta=h_\beta
\text{ kontinu untuk setiap }\beta.
$$

Syarat di ruas kanan telah diberikan, sehingga $h$ kontinu.

## Solusi Latihan 2.4 {#o012-rbt-l02-sol-004}

Misalkan $A\subseteq X$ memenuhi bahwa $A\cap U_\alpha$ terbuka dalam $U_\alpha$ untuk setiap $\alpha$. Karena $U_\alpha$ terbuka dalam $X$, setiap subset yang terbuka dalam $U_\alpha$ juga terbuka dalam $X$. Jadi semua $A\cap U_\alpha$ terbuka dalam $X$. Karena $\{U_\alpha\}$ menutupi $X$,

$$
A=A\cap X
=A\cap\bigcup_\alpha U_\alpha
=\bigcup_\alpha(A\cap U_\alpha),
$$

yang terbuka dalam $X$. Sebaliknya, jika $A$ terbuka dalam $X$, maka
$A\cap U_\alpha$ terbuka dalam $U_\alpha$. Inilah persis syarat topologi akhir untuk semua inklusi $U_\alpha\hookrightarrow X$.

## Solusi Latihan 2.5 {#o012-rbt-l02-sol-005}

Misalkan $A\subseteq X$ dan $A\cap V_i$ terbuka dalam $V_i$ untuk setiap $i$. Tetapkan
$F=X\setminus A$. Maka

$$
F\cap V_i=V_i\setminus(A\cap V_i)
$$

tertutup dalam $V_i$. Karena $V_i$ tertutup dalam $X$, himpunan $F\cap V_i$ juga tertutup dalam $X$. Sampulnya berhingga, sehingga

$$
F=\bigcup_{i=1}^n(F\cap V_i)
$$

adalah gabungan berhingga himpunan tertutup dan karenanya tertutup dalam $X$. Jadi $A$ terbuka. Implikasi sebaliknya langsung dari definisi topologi subruang. Dengan demikian, topologi $X$ adalah topologi akhir untuk pemetaan inklusi $V_i\hookrightarrow X$.

Syarat “berhingga” tidak boleh dihapus dari argumen ini: gabungan tak berhingga himpunan tertutup tidak harus tertutup.

## Bukti Lema 2.3 {#o012-rbt-l02-check-002}

Untuk sampul terbuka, Latihan 2.4 mengatakan bahwa $X$ mempunyai topologi akhir bagi pemetaan inklusi $U_\alpha\hookrightarrow X$. Pembatasan $f|_{U_\alpha}$ adalah komposisi

$$
U_\alpha\hookrightarrow X\xrightarrow{f}Y.
$$

Jika semua komposisi ini kontinu, sifat universal pada Lema 2.1 menyatakan bahwa $f$ kontinu. Untuk sampul tertutup berhingga, gunakan Latihan 2.5 dengan argumen yang sama.

## Solusi Latihan 2.6 {#o012-rbt-l02-sol-006}

Topologi produk pada $W\times Z$ adalah topologi awal untuk proyeksi
$\operatorname{pr}_W$ dan $\operatorname{pr}_Z$. Karena

$$
\operatorname{pr}_W\circ(f\times g)=f\circ\operatorname{pr}_X,
\qquad
\operatorname{pr}_Z\circ(f\times g)=g\circ\operatorname{pr}_Y,
$$

dan semua fungsi di ruas kanan kontinu, sifat universal topologi awal menunjukkan bahwa
$f\times g$ kontinu.

Sekarang andaikan $f\times g$ kontinu serta pilih $y_0\in Y$ dan $x_0\in X$. Pemetaan

$$
i_X\colon X\to X\times Y,
\qquad
x\longmapsto(x,y_0)
$$

kontinu karena kedua fungsi koordinatnya—identitas pada $X$ dan fungsi konstan ke $y_0$—kontinu. Maka

$$
f=\operatorname{pr}_W\circ(f\times g)\circ i_X
$$

kontinu. Dengan cara yang sama, pemetaan $i_Y(y)=(x_0,y)$ memberi

$$
g=\operatorname{pr}_Z\circ(f\times g)\circ i_Y,
$$

sehingga $g$ kontinu. Kebutuhan akan $x_0$ dan $y_0$ menjelaskan syarat bahwa kedua domain tidak kosong.

## Solusi Latihan 2.7 {#o012-rbt-l02-sol-007}

Kontraksi $\mathbb{R}$ ke $0$ diberikan oleh

$$
H\colon I\times\mathbb{R}\to\mathbb{R},
\qquad
H(t,x)=(1-t)x.
$$

Fungsi ini kontinu, $H(0,x)=x$, dan $H(1,x)=0$.

Untuk setiap $\alpha\in A$, misalkan $X_\alpha$ kontraktil ke $x_\alpha^0$ melalui

$$
H_\alpha\colon I\times X_\alpha\to X_\alpha.
$$

Definisikan

$$
\begin{aligned}
H\colon I\times\prod_{\alpha\in A}X_\alpha
&\longrightarrow\prod_{\alpha\in A}X_\alpha,\\
H\bigl(t,(x_\alpha)_\alpha\bigr)
&=\bigl(H_\alpha(t,x_\alpha)\bigr)_\alpha.
\end{aligned}
$$

Untuk setiap proyeksi $\operatorname{pr}_\alpha$,

$$
\operatorname{pr}_\alpha\circ H
=H_\alpha\circ
(\operatorname{id}_I\times\operatorname{pr}_\alpha),
$$

yang kontinu. Sifat universal topologi produk menyatakan bahwa $H$ kontinu. Selain itu,

$$
H\bigl(0,(x_\alpha)_\alpha\bigr)=(x_\alpha)_\alpha,
\qquad
H\bigl(1,(x_\alpha)_\alpha\bigr)=(x_\alpha^0)_\alpha.
$$

Jadi produk sembarang tersebut kontraktil.

## Jawaban Pertanyaan 2.1 {#o012-rbt-l02-answer-001}

Pilihan titik kontraksi tidak berpengaruh: jika $X$ dapat dikontraksikan ke $x_0$, maka $X$ dapat dikontraksikan ke setiap $x_1\in X$.

Misalkan $H$ adalah kontraksi ke $x_0$. Definisikan

$$
K(t,y)=
\begin{cases}
H(2t,y),&0\le t\le\tfrac12,\\[4pt]
H(2-2t,x_1),&\tfrac12\le t\le1.
\end{cases}
$$

Pada $t=\tfrac12$, kedua rumus bernilai $x_0$, sebab
$H(1,y)=x_0=H(1,x_1)$. Masing-masing rumus kontinu pada subruang tertutup
$[0,\tfrac12]\times X$ dan $[\tfrac12,1]\times X$; Lema perekatan menunjukkan bahwa $K$ kontinu. Akhirnya,

$$
K(0,y)=H(0,y)=y,
\qquad
K(1,y)=H(0,x_1)=x_1.
$$

Jadi $K$ adalah kontraksi $X$ ke $x_1$.
