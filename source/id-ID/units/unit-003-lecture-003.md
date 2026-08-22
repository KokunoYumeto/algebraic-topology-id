---
title: "Topologi Aljabar"
subtitle: "Unit 3: Komponen Terhubung, Homotopi, dan Fungtor"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l03-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic Topology* karya David Michael Roberts (2019), tepatnya `Notes.tex` baris 585-877 pada commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`. Baris 878 membuka proposisi yang penandanya, `\lecturenum{4}`, baru muncul pada baris 879; karena itu baris 878 disisihkan bersama isi proposisi untuk Unit 4 agar tidak ada lingkungan LaTeX yang terpotong. Karya sumber tersedia di bawah [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah dibaca, pemberian pengenal stabil, pemindahan empat tugas dari catatan pinggir atau prosa ke blok latihan, dan sepuluh koreksi atau klarifikasi terbatas: ketak-kosongan komponen terhubung; syarat jari-jari positif pada homotopi anulus; ketak-kosongan pada klaim $\pi_0(X)=*$; titik akhir homotopi gabungan; subinterval bagi paruh kedua homotopi gabungan; nama homotopi balik; ketak-kosongan dalam definisi keterhubungan lintasan; kategori asal objek pada definisi fungtor; kasus citra kosong pada bukti keterhubungan citra; dan asumsi keterhubungan lokal pada bukti kedua fungtorialitas $\pi_0$. Materi pendamping penguasaan menjawab seluruh lima latihan dan melengkapi bukti bahwa keterhubungan lintasan mengakibatkan keterhubungan. Materi baru ini juga tersedia di bawah CC BY 4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

# Kuliah 3 {#o012-rbt-l03}

## Komponen terhubung dan himpunan $\pi_0$ {#o012-rbt-l03-s01}

Inilah contoh pertama kita tentang suatu invarian ruang: apakah sebuah ruang terhubung atau tidak. Ruang terhubung $X$ tidak mungkin homeomorfik dengan ruang $Z$ yang tidak terhubung. Namun, bagaimana kita membedakan dua ruang yang sama-sama tidak terhubung?

::: {.exercise #o012-rbt-l03-ex-001}
**Latihan 3.1 (invariansi keterhubungan).** Misalkan $h\colon X\xrightarrow{\cong}Z$ adalah homeomorfisma dan $S$ ruang diskret. Tunjukkan bahwa setiap fungsi kontinu $u\colon X\to S$ berkorespondensi dengan tepat satu fungsi kontinu $v\colon Z\to S$ yang memenuhi $u=v\circ h$. Simpulkan bahwa $X$ terhubung jika dan hanya jika $Z$ terhubung.
:::

::: {.definition #o012-rbt-l03-def-001}
**Definisi 3.1 (komponen terhubung dan $\pi_0$).** Untuk suatu ruang $X$:

1. Subset tak kosong $Y\subseteq X$ disebut *komponen terhubung* dari $X$ jika $Y$ terhubung dan maksimal terhadap sifat itu: apabila $Y'$ terhubung dan $Y\subseteq Y'\subseteq X$, maka $Y=Y'$.

2. Definisikan relasi pada $X$ dengan

   $$
   x_1\sim x_2
   \quad\Longleftrightarrow\quad
   \text{$x_1$ dan $x_2$ termuat bersama dalam suatu subset terhubung $C\subseteq X$.}
   $$

   Relasi ini merupakan relasi ekuivalensi, dan kelas-kelas ekuivalensinya adalah komponen-komponen terhubung $X$. Himpunan kelas tersebut dinotasikan dengan

   $$
   \pi_0(X)=X/{\sim}
   $$

   dan disebut *himpunan komponen terhubung*.
:::

::: {.exercise #o012-rbt-l03-ex-002}
**Latihan 3.2.** Buktikan dua pernyataan yang dipakai dalam Definisi 3.1:

1. Jika $C,D\subseteq X$ terhubung dan $C\cap D\ne\varnothing$, maka $C\cup D$ terhubung.
2. Relasi $\sim$ di atas adalah relasi ekuivalensi dan kelas-kelas ekuivalensinya tepat merupakan komponen-komponen terhubung $X$.
:::

Setiap ruang terhubung tak kosong $X$ memenuhi $\pi_0(X)=*$. Untuk ruang yang tidak terhubung, kita dapat membandingkan himpunan $\pi_0$-nya.

Semua ruang yang akan dipertimbangkan dalam mata kuliah ini dapat ditulis sebagai

$$
X=\bigsqcup_{\alpha\in\pi_0(X)}X_\alpha,
$$

dengan setiap $X_\alpha$ terhubung, dan mempunyai fungsi kontinu
$X\to\pi_0(X)$ ketika $\pi_0(X)$ diberi topologi diskret. Sifat ini berlaku, khususnya, bagi ruang yang terhubung secara lokal. Perlu diingat bahwa $\mathbb{Q}$ dengan topologi Euklides tidak terhubung secara lokal; banyak contoh menarik lainnya juga tidak. Karena itu, kita perlu memahami ruang terhubung, walaupun ruang yang tidak terhubung tetap akan digunakan.

## Homotopi dan ekuivalensi homotopi {#o012-rbt-l03-s02}

Dapatkah kita memperoleh lebih banyak dari gagasan kontraksi? Untuk homotopi
$H\colon I\times X\to X$, pemetaan ujungnya adalah $H_0=\operatorname{id}_X$ dan pemetaan konstan $H_1$ ke $x_0$. Apa yang terjadi jika $H_0$ dan $H_1$ merupakan pemetaan kontinu lain?

::: {.example #o012-rbt-l03-exa-001}
**Contoh 3.1 (anulus).** Ambil $0<r<R$ dan anulus

$$
A(r,R)=\{x\in\mathbb{R}^2\mid r\le \lVert x\rVert\le R\}.
$$

Definisikan

$$
H(t,x)=\bigl((1-t)r+tR\bigr)\frac{x}{\lVert x\rVert}.
$$

Karena $\lVert x\rVert\ge r>0$, rumus ini terdefinisi dan kontinu. Jari-jari $H(t,x)$ adalah $(1-t)r+tR$, sehingga citranya tetap di dalam $A(r,R)$. Pada $t=0$ ia memetakan setiap titik secara radial ke lingkaran dalam dan menetapkan lingkaran itu titik demi titik; pada $t=1$ ia melakukan hal yang sama terhadap lingkaran luar. Jadi kedua pemetaan ujung benar-benar merupakan retraksi.
:::

Bagaimana jika kita mempertimbangkan pemetaan kontinu umum $X\to Y$, bukan hanya pemetaan $X\to X$?

::: {.definition #o012-rbt-l03-def-002}
**Definisi 3.2 (homotopi).** Suatu *homotopi* adalah pemetaan kontinu

$$
H\colon I\times X\longrightarrow Y.
$$

Jika $f=H(0,-)$ dan $g=H(1,-)$, maka $H$ disebut *homotopi dari $f$ ke $g$*, dan $f$ serta $g$ disebut *homotopik*, ditulis $f\simeq g$.

Secara diagramatik, jika $i_0(x)=(0,x)$ dan $i_1(x)=(1,x)$, syarat ujungnya ialah

$$
H\circ i_0=f,
\qquad
H\circ i_1=g.
$$
:::

Contoh 3.1 memberikan homotopi antara dua pemetaan “retraksi”
$A(r,R)\to A(r,R)$ yang masing-masing mengirim titik ke lingkaran dalam dan lingkaran luar.

Topologi aljabar hampir selalu mempertimbangkan pemetaan *hingga homotopi* dan, demikian pula, “ruang hingga homotopi”.

::: {.definition #o012-rbt-l03-def-003}
**Definisi 3.3 (ekuivalensi homotopi).** Pemetaan kontinu
$f\colon X\to Y$ disebut *ekuivalensi homotopi* jika terdapat pemetaan kontinu
$g\colon Y\to X$ sedemikian sehingga

$$
g\circ f\simeq\operatorname{id}_X,
\qquad
f\circ g\simeq\operatorname{id}_Y.
$$

Dalam keadaan ini, $X$ dan $Y$ disebut *ekuivalen secara homotopi*.
:::

::: {.example #o012-rbt-l03-exa-002}
**Contoh 3.2.** Setiap ruang kontraktil ekuivalen secara homotopi dengan ruang satu titik.
:::

Ekuivalensi homotopi dapat dipandang sebagai versi isomorfisma yang lebih kasar. Pemetaan

$$
\{\text{ruang}\}\longrightarrow\{\text{objek aljabar}\}
$$

yang menjadi sasaran topologi aljabar seharusnya mengirim ruang-ruang yang ekuivalen secara homotopi ke objek-objek aljabar yang isomorfik. Bahasa teori kategori akan membuat gagasan ini lebih tepat.

Sifat homotopi berikut sangat penting dan akan terus digunakan.

::: {.proposition #o012-rbt-l03-prop-001}
**Proposisi 3.1 (penggabungan dan pembalikan homotopi).** Misalkan
$H,H'\colon I\times X\to Y$ adalah homotopi dengan
$H_1=H'_0$. Maka terdapat homotopi $H''$ dari $H_0$ ke $H'_1$. Selain itu, terdapat homotopi $\widetilde H$ dari $H_1$ ke $H_0$.
:::

::: {.proof #o012-rbt-l03-proof-001}
**Bukti.** Definisikan

$$
H''(t,x)=
\begin{cases}
H(2t,x),&0\le t\le\tfrac12,\\[3pt]
H'(2t-1,x),&\tfrac12\le t\le1.
\end{cases}
$$

Kedua rumus memberikan nilai yang sama pada $t=\tfrac12$, karena
$H(1,x)=H'(0,x)$. Masing-masing kontinu pada subruang tertutup
$[0,\tfrac12]\times X$ dan $[\tfrac12,1]\times X$; lema perekatan menunjukkan bahwa $H''$ kontinu. Nilai ujungnya ialah

$$
H''(0,x)=H(0,x),
\qquad
H''(1,x)=H'(1,x),
$$

sehingga $H''$ merupakan homotopi dari $H_0$ ke $H'_1$.

Untuk pembalikan, ambil $c\colon I\to I$, $c(t)=1-t$, dan definisikan

$$
\widetilde H
=H\circ(c\times\operatorname{id}_X).
$$

Maka $\widetilde H(0,x)=H(1,x)$ dan
$\widetilde H(1,x)=H(0,x)$, sebagaimana diperlukan. $\square$
:::

Homotopi pemetaan merupakan relasi ekuivalensi. Refleksivitas disaksikan oleh homotopi konstan $C(t,x)=f(x)$; simetri diberikan oleh pembalikan pada Proposisi 3.1; dan transitivitas diberikan oleh penggabungan pada proposisi yang sama.

Ruang kontraktil menyediakan banyak homotopi.

::: {.lemma #o012-rbt-l03-lem-001}
**Lema 3.1.** Jika $Y$ kontraktil ke $y_0\in Y$, maka setiap pemetaan kontinu
$f\colon X\to Y$ homotopik dengan pemetaan yang citranya termuat dalam $\{y_0\}$.
:::

::: {.proof #o012-rbt-l03-proof-002}
**Bukti.** Misalkan $K\colon I\times Y\to Y$ menyaksikan kontraktilitas $Y$. Komposisi

$$
I\times X
\xrightarrow{\operatorname{id}_I\times f}
I\times Y
\xrightarrow{K}
Y
$$

merupakan homotopi dari $f$ ke pemetaan konstan bernilai $y_0$. $\square$
:::

Sebagai akibatnya, setiap dua pemetaan menuju ruang kontraktil saling homotopik: terapkan Lema 3.1 kepada kedua pemetaan, balik salah satu homotopi menuju pemetaan konstan yang sama, lalu gabungkan keduanya dengan Proposisi 3.1. Karena ruang kontraktil dalam arti tertentu bersifat trivial, pemetaan menuju ruang tersebut juga trivial dalam arti yang sama.

Versi antara yang penting muncul ketika ruang asalnya diskret, atau bahkan hanya ruang satu titik.

::: {.definition #o012-rbt-l03-def-004}
**Definisi 3.4 (terhubung lintasan).** Ruang tak kosong $Y$ disebut *terhubung lintasan* jika setiap dua pemetaan $*\to Y$ saling homotopik.
:::

Dengan menguraikan definisi ini, untuk setiap dua titik $y_0,y_1\in Y$ terdapat lintasan kontinu
$\gamma\colon I\to Y$ dengan $\gamma(0)=y_0$ dan $\gamma(1)=y_1$.

::: {.exercise #o012-rbt-l03-ex-003}
**Latihan 3.3.** Buktikan bahwa ruang tak kosong $Y$ terhubung lintasan jika dan hanya jika, untuk setiap ruang diskret $S$, setiap dua pemetaan kontinu $S\to Y$ saling homotopik.
:::

::: {.proposition #o012-rbt-l03-prop-002}
**Proposisi 3.2.** Setiap ruang terhubung lintasan adalah terhubung.
:::

Untuk ruang $X$ dan $Y$, tuliskan

$$
[X,Y]
=
\{f\colon X\to Y\mid f\text{ kontinu}\}/{\text{homotopi}}.
$$

Himpunan *komponen lintasan* dari $Y$ adalah $[*,Y]$. Ruang $Y$ terhubung lintasan jika dan hanya jika $[*,Y]=*$. Perhatikan bahwa $\pi_0(Y)$ dalam catatan ini berarti himpunan **komponen terhubung**, sedangkan $[*,Y]$ berarti himpunan **komponen lintasan**. Keduanya tidak boleh diidentifikasi tanpa hipotesis tambahan, misalnya keterhubungan lintasan lokal yang sesuai.

## Kategori dan fungtor {#o012-rbt-l03-s03}

Sejauh ini kita membahas ruang topologis dan pemetaan kontinu, tetapi kita juga secara tersirat memakai himpunan dan fungsi yang tidak harus kontinu. Pada kedua konteks tersebut, komposisi bersifat asosiatif dan tersedia pemetaan identitas. Kelak kita akan menggunakan kelas-kelas ruang topologis yang lebih terbatas agar sifat yang dibutuhkan benar-benar berlaku.

::: {.definition #o012-rbt-l03-def-005}
**Definisi 3.5 (kategori).** Suatu *kategori* $\mathcal{C}$ terdiri atas koleksi objek
$W,X,Y,Z,\ldots$ dan, untuk setiap pasangan objek $X,Y$, koleksi morfisma
$\mathcal{C}(X,Y)$, bersama data berikut:

1. Untuk $f\in\mathcal{C}(X,Y)$ dan $g\in\mathcal{C}(Y,Z)$, dipilih morfisma komposit
   $g\circ f\in\mathcal{C}(X,Z)$.
2. Untuk setiap objek $X$, dipilih morfisma identitas
   $\operatorname{id}_X\in\mathcal{C}(X,X)$.

Data tersebut harus memenuhi:

1. Untuk $h\in\mathcal{C}(W,X)$, $f\in\mathcal{C}(X,Y)$, dan
   $g\in\mathcal{C}(Y,Z)$,

   $$
   g\circ(f\circ h)=(g\circ f)\circ h.
   $$

2. Untuk setiap $h\in\mathcal{C}(W,X)$ dan $f\in\mathcal{C}(X,Y)$,

   $$
   \operatorname{id}_X\circ h=h,
   \qquad
   f\circ\operatorname{id}_X=f.
   $$

Untuk $f\in\mathcal{C}(X,Y)$, objek $X$ disebut *sumber* $f$ dan $Y$ disebut *sasaran* $f$; ditulis
$X=s(f)$, $Y=t(f)$, atau $f\colon X\to Y$. Jika setiap
$\mathcal{C}(X,Y)$ merupakan himpunan, maka $\mathcal{C}$ disebut *kecil secara lokal* dan $\mathcal{C}(X,Y)$ disebut *himpunan morfisma* atau *himpunan-hom*.
:::

Banyak kategori mempunyai objek berupa himpunan yang dilengkapi struktur tambahan, misalnya topologi, dan morfisma berupa fungsi yang sesuai dengan struktur tersebut, tetapi tidak semua kategori berbentuk demikian. Kita telah menjumpai $\mathbf{Top}$, kategori ruang topologis dan pemetaan kontinu, serta $\mathbf{Set}$, kategori himpunan dan fungsi. Ruang vektor, grup, grup abelian, manifold, dan gelanggang memberikan contoh lain.

::: {.example #o012-rbt-l03-exa-003}
**Contoh 3.3 (himpunan bertitik).** Kategori $\mathbf{Set}_*$ mempunyai objek berupa himpunan bertitik $(X,x)$, dengan $x\in X$ titik yang ditentukan, dan morfisma berupa pemetaan bertitik

$$
f\colon(X,x)\longrightarrow(Y,y),
\qquad
f(x)=y.
$$

Kategori ini dapat dipandang sebagai kategori objek aljabar dengan struktur yang paling lemah. Bandingkan dengan homomorfisma, transformasi linear, dan homomorfisma gelanggang, yang semuanya mempertahankan unsur tertentu.
:::

Kekuatan utama kategori tampak pada hubungannya satu sama lain; sebuah kategori yang terisolasi hanya dapat memberi informasi terbatas.

::: {.definition #o012-rbt-l03-def-006}
**Definisi 3.6 (fungtor).** Diberikan kategori $\mathcal{C}$ dan $\mathcal{D}$, suatu *fungtor*
$F\colon\mathcal{C}\to\mathcal{D}$ terdiri atas data:

1. Untuk setiap objek $X$ dari $\mathcal{C}$, suatu objek $F(X)$ dari $\mathcal{D}$.
2. Untuk setiap morfisma $f\colon X\to Y$ dalam $\mathcal{C}$, suatu morfisma
   $F(f)\colon F(X)\to F(Y)$ dalam $\mathcal{D}$.

Untuk setiap objek $X$ dari $\mathcal{C}$ dan setiap pasangan morfisma yang dapat dikomposisikan,
$f\colon X\to Y$ dan $g\colon Y\to Z$, data ini memenuhi

$$
F(\operatorname{id}_X)=\operatorname{id}_{F(X)},
\qquad
F(g\circ f)=F(g)\circ F(f).
$$

Sifat kedua disebut *fungtorialitas*. Untuk kategori kecil secara lokal, aturan pada morfisma memberikan fungsi

$$
\mathcal{C}(X,Y)\longrightarrow\mathcal{D}(F(X),F(Y)).
$$
:::

Selain fungtor identitas, kita telah melihat sedikitnya tiga contoh:

- fungtor pelupa, atau fungtor himpunan yang mendasari,
  $U\colon\mathbf{Top}\to\mathbf{Set}$;
- fungtor topologi diskret
  $\operatorname{disc}\colon\mathbf{Set}\to\mathbf{Top}$;
- fungtor komponen terhubung
  $\pi_0\colon\mathbf{Top}\to\mathbf{Set}$.

Topologi indiskret juga menghasilkan fungtor $\mathbf{Set}\to\mathbf{Top}$, tetapi tidak akan kita gunakan. Kita belum membuktikan bahwa $\pi_0$ benar-benar fungtor. Fungtor dapat dikomposisikan, sehingga misalnya diperoleh

$$
\operatorname{disc}\circ U\colon\mathbf{Top}\to\mathbf{Top},
\qquad
\operatorname{disc}\circ\pi_0\colon\mathbf{Top}\to\mathbf{Top}.
$$

Misalkan $\mathcal{C}$ sebuah kategori dan $\mathcal{D}$ suatu *subkategori*: sebagian objek dan sebagian morfisma $\mathcal{C}$ yang dengan sendirinya membentuk kategori. Penyertaan objek dan morfisma membentuk fungtor
$\mathcal{D}\hookrightarrow\mathcal{C}$, yang disebut *inklusi subkategori*. Jika

$$
\mathcal{D}(X,Y)=\mathcal{C}(X,Y)
$$

untuk setiap objek $X,Y$ dari $\mathcal{D}$, maka $\mathcal{D}$ disebut *subkategori penuh*. Secara lebih umum, fungtor yang injektif pada objek dan morfisma dapat dipakai untuk mendeskripsikan subkategori.

::: {.example #o012-rbt-l03-exa-004}
**Contoh 3.4.** Fungtor
$\operatorname{disc}\colon\mathbf{Set}\to\mathbf{Top}$ mengidentifikasi
$\mathbf{Set}$ dengan subkategori penuh ruang-ruang diskret di dalam $\mathbf{Top}$. Fakta ini akan dipakai tanpa komentar lebih lanjut. Kelak kita juga akan membatasi perhatian pada subkategori-subkategori penuh tertentu dari $\mathbf{Top}$.
:::

::: {.lemma #o012-rbt-l03-lem-002}
**Lema 3.2 (citra ruang terhubung).** Misalkan $X$ terhubung dan
$f\colon X\to Y$ kontinu. Maka $\operatorname{im}(f)\subseteq Y$ terhubung.
:::

::: {.proof #o012-rbt-l03-proof-003}
**Bukti.** Ambil ruang diskret $S$ dan pemetaan kontinu
$g\colon\operatorname{im}(f)\to S$. Komposisi

$$
X\xrightarrow{f}\operatorname{im}(f)\xrightarrow{g}S
$$

kontinu. Karena $X$ terhubung, citra komposisi ini memuat paling banyak satu titik. Pemetaan $f\colon X\to\operatorname{im}(f)$ surjektif, sehingga citra $g$ juga memuat paling banyak satu titik. Jadi $\operatorname{im}(f)$ terhubung. $\square$
:::

::: {.proposition #o012-rbt-l03-prop-003}
**Proposisi 3.3.** Aturan $X\mapsto\pi_0(X)$ menentukan fungtor

$$
\pi_0\colon\mathbf{Top}\longrightarrow\mathbf{Set}.
$$
:::

::: {.proof #o012-rbt-l03-proof-004}
**Bukti.** Untuk pemetaan kontinu $f\colon X\to Y$, kita perlu mendefinisikan fungsi

$$
\pi_0(f)\colon\pi_0(X)\longrightarrow\pi_0(Y).
$$

Ambil $\alpha\in\pi_0(X)$ dan komponen terhubung terkait
$X_\alpha\subseteq X$. Menurut Lema 3.2, $f(X_\alpha)$ terhubung, sehingga termuat dalam tepat satu komponen terhubung $Y$. Definisikan $\pi_0(f)(\alpha)$ sebagai komponen tersebut.

Jika $g\colon Y\to Z$ kontinu, komponen yang memuat
$g(f(X_\alpha))$ sama dengan komponen yang diperoleh dengan menerapkan
$\pi_0(g)$ kepada komponen yang memuat $f(X_\alpha)$. Jadi

$$
\pi_0(g\circ f)=\pi_0(g)\circ\pi_0(f).
$$

Selain itu, $\pi_0(\operatorname{id}_X)$ adalah fungsi identitas pada
$\pi_0(X)$. Kedua hukum fungtor terpenuhi. $\square$
:::

::: {.proof #o012-rbt-l03-proof-005}
**Bukti kedua untuk Proposisi 3.3 (kasus terhubung secara lokal).** Andaikan semua objek yang dipakai dalam argumen ini terhubung secara lokal; mula-mula ambil $f\colon X\to Y$. Pemetaan kanonik
$Y\to\pi_0(Y)$ kontinu ketika $\pi_0(Y)$ diberi topologi diskret. Karena komposisi

$$
X\xrightarrow{f}Y\longrightarrow\pi_0(Y)
$$

konstan pada setiap komponen $X_\alpha$, ia turun melalui
$X\to\pi_0(X)$ menjadi fungsi

$$
\pi_0(f)\colon\pi_0(X)\longrightarrow\pi_0(Y),
\qquad
\pi_0(f)(\alpha)=[f(x)]
$$

untuk sembarang $x\in X_\alpha$. Diagram berikut komutatif:

$$
\begin{array}{ccc}
X&\xrightarrow{f}&Y\\
\downarrow&&\downarrow\\
\pi_0(X)&\xrightarrow{\pi_0(f)}&\pi_0(Y).
\end{array}
$$

Pada ruang yang terhubung secara lokal, topologi hasil bagi pada
$\pi_0(X)$ sama dengan topologi diskret; jadi pemetaan di baris bawah kontinu, walaupun di sini kita hanya memandangnya sebagai fungsi himpunan. Untuk memeriksa komposisi di subkategori ruang terhubung lokal, ambil pula ruang terhubung lokal $Z$, pemetaan
$g\colon Y\to Z$, dan titik $x\in X_\alpha$. Maka

$$
\pi_0(g)\bigl(\pi_0(f)(\alpha)\bigr)
=\pi_0(g)([f(x)])
=[g(f(x))]
=\pi_0(g\circ f)(\alpha),
$$

yang sekali lagi membuktikan fungtorialitas.
 $\square$
:::

::: {.exercise #o012-rbt-l03-ex-004}
**Latihan 3.4.** Buktikan bahwa

$$
[*,{-}]\colon\mathbf{Top}\longrightarrow\mathbf{Set}
$$

adalah fungtor. Buktikan pula pernyataan yang lebih umum: untuk setiap ruang tetap $A$, aturan
$[A,{-}]\colon\mathbf{Top}\to\mathbf{Set}$ adalah fungtor.
:::

## Kategori homotopi {#o012-rbt-l03-s04}

Contoh kategori penting lainnya adalah *kategori homotopi*
$\mathbf{Ho}$. Objeknya ialah ruang topologis, sedangkan

$$
\mathbf{Ho}(X,Y)=[X,Y].
$$

Terdapat fungtor $\mathbf{Top}\to\mathbf{Ho}$ yang identik pada objek dan mengirim setiap pemetaan kontinu ke kelas homotopinya. Dua objek isomorfik dalam $\mathbf{Ho}$ jika dan hanya jika keduanya ekuivalen secara homotopi.

::: {.exercise #o012-rbt-l03-ex-005}
**Latihan 3.5.** Buktikan bahwa komposisi kelas homotopi terdefinisi dengan baik, sehingga $\mathbf{Ho}$ benar-benar merupakan kategori. Verifikasi pula pernyataan tentang fungtor $\mathbf{Top}\to\mathbf{Ho}$ dan isomorfisma objek pada paragraf sebelumnya.
:::

# Pendamping penguasaan: solusi lengkap {.unnumbered #o012-rbt-l03-mastery}

Bagian ini merupakan materi baru untuk edisi bahasa Indonesia. Setiap tugas pada Kuliah 3 dijawab lengkap, dan bukti Proposisi 3.2 yang tidak dituliskan dalam sumber diberikan secara eksplisit.

## Solusi Latihan 3.1 {#o012-rbt-l03-sol-001}

Dari $u\colon X\to S$, definisikan

$$
v=u\circ h^{-1}\colon Z\to S.
$$

Pemetaan $v$ kontinu karena $h^{-1}$ dan $u$ kontinu, serta
$v\circ h=u$. Jika $w\colon Z\to S$ juga memenuhi $w\circ h=u$, maka

$$
w=w\circ h\circ h^{-1}=u\circ h^{-1}=v,
$$

sehingga $v$ unik. Konstruksi sebaliknya ialah $v\mapsto v\circ h$; jadi kita memperoleh korespondensi bijektif antara pemetaan kontinu $X\to S$ dan $Z\to S$.

Jika $X$ terhubung, setiap $u\colon X\to S$ mempunyai citra paling banyak satu titik. Karena
$\operatorname{im}(u)=\operatorname{im}(u\circ h^{-1})$, hal yang sama berlaku bagi setiap pemetaan kontinu $Z\to S$, sehingga $Z$ terhubung. Argumen dengan $h^{-1}$ memberikan implikasi sebaliknya.

## Solusi Latihan 3.2 {#o012-rbt-l03-sol-002}

Pertama, ambil pemetaan kontinu $f\colon C\cup D\to S$ ke ruang diskret. Pembatasannya pada $C$ dan $D$ masing-masing mempunyai citra paling banyak satu titik. Pilih $x\in C\cap D$. Jika kedua citra tidak kosong, nilai bersama $f(x)$ memaksa keduanya sama. Maka $f(C\cup D)$ memuat paling banyak satu titik, sehingga $C\cup D$ terhubung.

Untuk relasi $\sim$:

- refleksivitas mengikuti karena singleton $\{x\}$ terhubung;
- simetri langsung dari definisi;
- jika $x_1\sim x_2$ melalui $C$ dan $x_2\sim x_3$ melalui $D$, maka
  $x_2\in C\cap D$, sehingga $C\cup D$ terhubung dan $x_1\sim x_3$.

Jadi $\sim$ merupakan relasi ekuivalensi. Kelas $[x]$ adalah gabungan semua subset terhubung yang memuat $x$. Gabungan ini terhubung: setiap pemetaan kontinu dari gabungan tersebut ke ruang diskret konstan pada tiap anggota keluarga dan semua nilai konstannya sama karena setiap anggota memuat $x$. Kelas $[x]$ juga maksimal, sebab setiap subset terhubung yang memuatnya, dan khususnya memuat $x$, sudah termasuk dalam gabungan yang mendefinisikan $[x]$. Jadi $[x]$ adalah komponen terhubung.

Sebaliknya, jika $C$ komponen terhubung dan $x\in C$, maka
$C\subseteq[x]$. Karena $[x]$ terhubung dan $C$ maksimal, $C=[x]$. Dengan demikian kelas ekuivalensi dan komponen terhubung tepat sama.

## Pemeriksaan Contoh 3.2 {#o012-rbt-l03-check-001}

Misalkan $X$ kontraktil ke $x_0\in X$. Ambil pemetaan tunggal
$p\colon X\to *$ dan pemetaan $i\colon *\to X$ dengan $i(*)=x_0$. Maka

$$
p\circ i=\operatorname{id}_*,
\qquad
i\circ p=c_{x_0}.
$$

Kontraksi memberikan homotopi
$\operatorname{id}_X\simeq c_{x_0}$; dengan membalik homotopi tersebut, diperoleh
$c_{x_0}\simeq\operatorname{id}_X$. Jadi $p$ dan $i$ merupakan invers hingga homotopi, sehingga $X$ ekuivalen secara homotopi dengan ruang satu titik.

## Solusi Latihan 3.3 {#o012-rbt-l03-sol-003}

Andaikan dahulu $Y$ terhubung lintasan. Ambil ruang diskret $S$ dan dua pemetaan
$a,b\colon S\to Y$. Untuk setiap $s\in S$, pilih lintasan
$\gamma_s\colon I\to Y$ dari $a(s)$ ke $b(s)$. Definisikan

$$
H\colon I\times S\longrightarrow Y,
\qquad
H(t,s)=\gamma_s(t).
$$

Karena $S$ diskret, $I\times S$ adalah gabungan saling lepas dari subruang terbuka
$I\times\{s\}$. Pembatasan $H$ pada tiap subruang ini adalah $\gamma_s$ dan kontinu; sifat universal gabungan saling lepas menunjukkan bahwa $H$ kontinu. Nilai ujungnya adalah $a$ dan $b$, sehingga $a\simeq b$.

Sebaliknya, terapkan syarat tersebut pada ruang diskret satu titik $S=*$. Setiap dua pemetaan $*\to Y$ homotopik, sehingga $Y$ terhubung lintasan. Ketak-kosongan $Y$ disyaratkan pada kedua rumusan.

## Bukti Proposisi 3.2 {#o012-rbt-l03-check-002}

Misalkan $Y$ terhubung lintasan dan $f\colon Y\to S$ kontinu, dengan $S$ diskret. Untuk sembarang $y_0,y_1\in Y$, pilih lintasan
$\gamma\colon I\to Y$ dari $y_0$ ke $y_1$. Komposisi

$$
I\xrightarrow{\gamma}Y\xrightarrow{f}S
$$

kontinu. Interval $I$ terhubung, sehingga citranya dalam $S$ memuat paling banyak satu titik. Akibatnya
$f(y_0)=f(y_1)$. Karena kedua titik dipilih sembarang, $f(Y)$ memuat tepat satu titik. Jadi setiap pemetaan kontinu dari $Y$ ke ruang diskret konstan, dan $Y$ terhubung.

## Solusi Latihan 3.4 {#o012-rbt-l03-sol-004}

Untuk ruang tetap $A$, definisikan fungtor $[A,{-}]$ pada objek dengan

$$
Y\longmapsto[A,Y].
$$

Untuk pemetaan kontinu $h\colon Y\to Z$, definisikan

$$
[A,h]\colon[A,Y]\longrightarrow[A,Z],
\qquad
[f]\longmapsto[h\circ f].
$$

Aturan ini terdefinisi dengan baik. Jika $f_0\simeq f_1$ melalui
$H\colon I\times A\to Y$, maka $h\circ H$ merupakan homotopi dari
$h\circ f_0$ ke $h\circ f_1$, sehingga kelas hasil tidak bergantung pada wakil.

Untuk identitas dan komposisi,

$$
[A,\operatorname{id}_Y]([f])=[f],
$$

dan jika $k\colon Z\to W$, maka

$$
[A,k\circ h]([f])=[k\circ h\circ f]
=[A,k]\bigl([A,h]([f])\bigr).
$$

Jadi $[A,{-}]$ adalah fungtor. Kasus $A=*$ memberikan fungtor
$[*,{-}]$ yang diminta.

## Solusi Latihan 3.5 {#o012-rbt-l03-sol-005}

Untuk kelas $[f]\in[X,Y]$ dan $[g]\in[Y,Z]$, definisikan

$$
[g]\circ[f]=[g\circ f].
$$

Kita harus membuktikan bahwa hasil ini tidak bergantung pada wakil. Misalkan
$f_0\simeq f_1$ melalui $H\colon I\times X\to Y$ dan
$g_0\simeq g_1$ melalui $K\colon I\times Y\to Z$. Komposisi

$$
(t,x)\longmapsto g_0(H(t,x))
$$

memberikan homotopi $g_0\circ f_0\simeq g_0\circ f_1$, sedangkan

$$
(t,x)\longmapsto K(t,f_1(x))
$$

memberikan homotopi $g_0\circ f_1\simeq g_1\circ f_1$. Dengan menggabungkan keduanya menggunakan Proposisi 3.1, diperoleh

$$
g_0\circ f_0\simeq g_1\circ f_1.
$$

Jadi komposisi kelas terdefinisi dengan baik. Asosiativitas diwarisi dari komposisi pemetaan, dan $[\operatorname{id}_X]$ bertindak sebagai identitas. Maka $\mathbf{Ho}$ adalah kategori.

Aturan $Q\colon\mathbf{Top}\to\mathbf{Ho}$ dengan
$Q(X)=X$ dan $Q(f)=[f]$ mempertahankan identitas dan komposisi secara langsung, sehingga merupakan fungtor.

Jika $[f]\colon X\to Y$ isomorfik dalam $\mathbf{Ho}$ dengan invers $[g]$, maka

$$
[g\circ f]=[\operatorname{id}_X],
\qquad
[f\circ g]=[\operatorname{id}_Y].
$$

Artinya $g\circ f\simeq\operatorname{id}_X$ dan
$f\circ g\simeq\operatorname{id}_Y$, sehingga $f$ adalah ekuivalensi homotopi. Sebaliknya, setiap ekuivalensi homotopi dengan invers homotopi $g$ memberikan isomorfisma $[f]$ dengan invers $[g]$ dalam $\mathbf{Ho}$.
