---
title: "Topologi Aljabar"
subtitle: "Unit 8: Grupoid Fundamental dan Keterhubungan Sederhana"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l08-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic Topology* karya David Michael Roberts (2019), tepatnya [Notes.tex baris 1771--1946 pada commit b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L1771-L1946). Rentang itu dimulai dengan penanda Kuliah 8 dan motivasi bagi grupoid, lalu berakhir setelah pembuktian bahwa ruang kontraktil terhubung sederhana. Baris 1947 memulai Kuliah 9 dan tidak termasuk dalam unit ini. Karya sumber tersedia di bawah [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah dibaca, pemberian pengenal stabil, serta pemindahan semua keterangan dan diagram pinggir ke urutan bacaan utama. Beberapa cacat sumber diperbaiki secara independen: pada lema konjugasi, arah morfisma $a$ diubah dari $\Gamma(y,x)$ menjadi $\Gamma(x,y)$ agar semua komposit bertipe benar menurut urutan komposisi aljabar yang dinyatakan sumber; salah eja “groupids” diperbaiki; dua kemunculan $\Pi$ yang kehilangan subskrip $1$ pada rumus produk dan koproduk dipulihkan menjadi $\Pi_1$; frasa “such an cover” diperbaiki; dan dalam contoh kontraksi, $h(0,x)=x_0$ diperbaiki menjadi $h(1,x)=x_0$, sesuai $H|_{\{1\}\times X}$ yang konstan. Ada pula ketidakselarasan cakupan: definisi sumber memakai $\pi_0$ hanya untuk ruang SLSC, sedangkan proposisi berikutnya mengklaim fungtor pada semua pasangan ruang. Edisi ini mempertahankan rumus $\pi_0$ pada kasus SLSC dan memakai kelas homotopi berujung tetap $[\{*\},P_x^yX]$ untuk perluasan ke semua pasangan, konsisten dengan definisi umum $\pi_1$ pada Kuliah 7. Diagram komutatif ditulis ulang sebagai susunan rumus dengan uraian tekstual agar hubungan panahnya tetap dapat diakses.

Rentang sumber memuat satu latihan, tentang daerah berbentuk bintang, tetapi tidak memberikan solusinya. Lema struktur grupoid dan proposisi fungtorialitas grupoid fundamental juga diberikan tanpa bukti. Bagian pendamping penguasaan mempertahankan latihan sumber tersebut dan menambahkan empat pemeriksaan edisi, semuanya dengan solusi lengkap: lema konjugasi dan aksi bebas-transitif; keabsahan komposisi, fungtorialitas $\Pi_1$, serta fungtor monodromi dan aksi kanan; kriteria keterhubungan sederhana dan penutup; serta argumen kontraksi melalui grupoid. Seluruh materi pendamping yang ditambahkan tersedia di bawah CC BY 4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

# Kuliah 8 {#o012-rbt-l08}

## Dari transpor lintasan menuju grupoid {#o012-rbt-l08-s01}

Seperti telah kita lihat, ruang penutup tidak hanya memberikan aksi
$\pi_1(X,x)$ pada serat $Z_x$. Lintasan di antara titik-titik berbeda juga
bertindak: suatu lintasan dari $x$ ke $y$ membawa titik-titik pada $Z_x$ ke
titik-titik pada $Z_y$. Jika $X$ sejak awal tidak dilengkapi titik dasar, atau
jika ada beberapa pilihan alami tanpa satu pun pilihan kanonik, kita dapat
membentuk invarian yang lebih kaya, yaitu sebuah *grupoid*.

::: {.definition #o012-rbt-l08-def-001}
**Definisi 8.1 (grupoid).** Grupoid adalah kategori yang setiap morfismanya
memiliki invers.
:::

Untuk mengenali jenis-jenis grupoid yang muncul, mari kita lihat beberapa
contoh. Kita hanya akan mempertimbangkan grupoid *kecil*. Artinya, grupoid
$\Gamma$ bersifat kecil secara lokal—setiap himpunan morfisma
$\Gamma(x,y)$ benar-benar merupakan himpunan—dan koleksi objeknya juga
merupakan suatu himpunan $\Gamma_0$. Dengan demikian, himpunan semua
morfisma dapat dibentuk sebagai gabungan lepas

$$
\Gamma_1
=
\bigsqcup_{x,y\in\Gamma_0}\Gamma(x,y).
$$

Terdapat peta sumber dan sasaran

$$
s,t\colon\Gamma_1\rightrightarrows\Gamma_0.
$$

Grupoid beserta fungtor di antaranya membentuk kategori
$\mathbf{Gpd}$.

::: {.example #o012-rbt-l08-exa-001}
**Contoh 8.1 (tiga grupoid dasar).**

1. Setiap himpunan $S$ menentukan grupoid $\operatorname{Disc}(S)$:
   himpunan objeknya adalah $S$, dan satu-satunya morfisma adalah morfisma
   identitas. Konstruksi ini memberikan penyertaan subkategori penuh

   $$
   \operatorname{Disc}\colon\mathbf{Set}\hookrightarrow\mathbf{Gpd}.
   $$

   Grupoid seperti ini disebut *diskret*.

2. Setiap himpunan $C$ juga menentukan grupoid
   $\operatorname{Codisc}(C)$. Objeknya adalah unsur-unsur $C$, tetapi sekarang
   terdapat tepat satu morfisma dari setiap objek menuju setiap objek lain.
   Himpunan morfismanya dapat diidentifikasi dengan $C\times C$, dan setiap
   $c\in C$ mempunyai grup automorfisma trivial. Grupoid seperti ini disebut
   *kodiskret*.

3. Misalkan grup $G$ beraksi di kanan pada himpunan $Y$. Ada grupoid aksi
   $Y/\!/G$ dengan himpunan objek $Y$ dan himpunan morfisma $Y\times G$.
   Morfisma $(y,g)$ mempunyai sumber dan sasaran

   $$
   s(y,g)=y,
   \qquad
   t(y,g)=yg,
   $$

   sedangkan komposisinya adalah

   $$
   (y,g)(yg,h)=(y,gh).
   $$

   Morfisma identitas pada $y$ adalah $(y,e)$, dan inversnya adalah

   $$
   (y,g)^{-1}=(yg,g^{-1}).
   $$

   Rumus-rumus ini langsung memenuhi hukum identitas, invers, dan asosiativitas
   karena hukum grup pada $G$.

   Jika $G=1$, konstruksi ini kembali menjadi grupoid diskret pada $Y$. Jika
   $Y=\{*\}$, informasi grupoid tersebut pada hakikatnya sama dengan informasi
   grup $G$. Grupoid satu objek ini dilambangkan $\mathbf{B}G$, dan

   $$
   \mathbf{B}\colon\mathbf{Grp}\hookrightarrow\mathbf{Gpd}
   $$

   merupakan penyertaan subkategori penuh.
:::

Slogan yang kadang dipakai adalah bahwa grupoid menyerupai grup dengan
“banyak identitas”. Pandangan lain yang berguna ialah bahwa grupoid
memperumum aksi grup: grup-grup yang berbeda dapat bertindak pada bagian-bagian
yang berbeda dari himpunan objek.

Pada lema berikut kita memakai *urutan komposisi aljabar*: jika
$f\colon x\to y$ dan $g\colon y\to z$, komposit “pertama $f$, lalu $g$”
ditulis $fg\colon x\to z$.

::: {.lemma #o012-rbt-l08-lem-001}
**Lema 8.1 (konjugasi dan aksi pada himpunan-hom).** Untuk setiap grupoid $\Gamma$, objek
$x,y\in\Gamma_0$, dan morfisma $a\in\Gamma(x,y)$, pemetaan

$$
\begin{aligned}
\operatorname{Ad}_a\colon\Gamma(x,x)&\xrightarrow{\;\cong\;}\Gamma(y,y),\\
g&\longmapsto a^{-1}ga
\end{aligned}
$$

merupakan isomorfisma grup, dengan invers

$$
(\operatorname{Ad}_a)^{-1}
=
\operatorname{Ad}_{a^{-1}}.
$$

Selain itu, fungsi

$$
\begin{aligned}
\Gamma(x,x)\times\Gamma(x,y)&\longrightarrow\Gamma(x,y),\\
(g,a)&\longmapsto ga
\end{aligned}
$$

mendefinisikan aksi bebas dan transitif dari grup $\Gamma(x,x)$ pada
$\Gamma(x,y)$.
:::

Jika $\Gamma(x,y)$ tidak kosong, pernyataan terakhir mengatakan bahwa
$\Gamma(x,y)$ merupakan torsor kiri bagi $\Gamma(x,x)$. Jika himpunan-hom
itu kosong, kebebasan dan transitivitas dalam bentuk berkuantor di atas
berlaku secara vakum, tetapi istilah *torsor* biasanya mensyaratkan
himpunan tak kosong.

Sebagai pengingat, aksi $G\times S\to S$ disebut *bebas* jika
$g\cdot p=p$ mengakibatkan $g$ adalah unsur identitas. Aksi itu disebut
*transitif* jika untuk setiap $p,q\in S$ terdapat $g\in G$ dengan
$g\cdot p=q$. Dalam Lema 8.1, jika $a,b\in\Gamma(x,y)$, unsur
$ba^{-1}\in\Gamma(x,x)$ membawa $a$ ke $b$ karena

$$
(ba^{-1})a=b.
$$

Kebebasan mengikuti dari

$$
ga=a
\quad\Longrightarrow\quad
g=gaa^{-1}=aa^{-1}=\operatorname{id}_x.
$$

## Grupoid fundamental {#o012-rbt-l08-s02}

::: {.definition #o012-rbt-l08-def-002}
**Definisi 8.2 (grupoid fundamental bertumpu pada suatu himpunan).** Misalkan
$X$ adalah ruang SLSC dan $A\subseteq X$ suatu subruang. *Grupoid fundamental
bertumpu pada $A$* adalah grupoid $\Pi_1(X,A)$ yang himpunan objeknya $A$ dan
yang himpunan morfismanya dari $x$ ke $y$ adalah

$$
\Pi_1(X,A)(x,y)
:=
\pi_0(P_x^yX).
$$

Komposisi diinduksi oleh konkatenasi lintasan:

$$
\pi_0(P_x^yX)\times\pi_0(P_y^zX)
\xrightarrow{\;\cong\;}
\pi_0(P_x^yX\times P_y^zX)
\longrightarrow
\pi_0(P_x^zX),
$$

dan lintasan konstan menjadi morfisma identitas.
:::

Dalam rumus sumber, $\pi_0$ berarti komponen **terhubung**, bukan komponen
lintasan. Untuk ruang SLSC, Teorema 6.2 membuat ruang-ruang lintasan di atas
terhubung lintasan secara lokal. Karena itu pemetaan alami

$$
[\{*\},P_x^yX]\longrightarrow\pi_0(P_x^yX)
$$

adalah bijeksi: kelas homotopi berujung tetap sama dengan komponen terhubung.
Konvensi SLSC Unit 6 juga mencakup keterhubungan lintasan lokal.

Proposisi berikut berbicara tentang **semua** pasangan ruang, bukan hanya
pasangan SLSC. Agar cakupannya tepat, untuk ruang topologis sebarang kita
memakai perluasan standar

$$
\Pi_1(X,A)(x,y):=[\{*\},P_x^yX],
$$

yaitu kelas homotopi lintasan yang mempertahankan titik ujung. Definisi ini
berlaku tanpa hipotesis lokal apa pun dan, pada ruang SLSC, berimpit dengan
rumus $\pi_0$ yang ditampilkan dalam Definisi 8.2.

Seperti invarian-invarian lain, grupoid fundamental bersifat fungtorial.
Definisikan $\mathbf{Top}^{(2)}$ sebagai kategori yang objeknya pasangan
$(X,A)$, dengan $X$ ruang topologis dan $A\subseteq X$ subruang. Morfisma

$$
f\colon(X,A)\longrightarrow(Y,B)
$$

adalah fungsi kontinu $f\colon X\to Y$ yang memenuhi $f(A)\subseteq B$.
Pengiriman ruang bertitik $(X,x)$ ke pasangan $(X,\{x\})$ memberi penyertaan
subkategori penuh

$$
\mathbf{Top}_*\hookrightarrow\mathbf{Top}^{(2)}.
$$

::: {.proposition #o012-rbt-l08-prop-001}
**Proposisi 8.1 (fungtorialitas grupoid fundamental).** Grupoid fundamental
memberikan fungtor

$$
\Pi_1\colon\mathbf{Top}^{(2)}\longrightarrow\mathbf{Gpd}
$$

sehingga diagram berikut komutatif:

$$
\begin{array}{ccc}
\mathbf{Top}_*
&\xrightarrow{\ \pi_1\ }&
\mathbf{Grp}\\[3pt]
\downarrow
&&
\downarrow\,\mathbf B\\[3pt]
\mathbf{Top}^{(2)}
&\xrightarrow{\ \Pi_1\ }&
\mathbf{Gpd}.
\end{array}
$$

Panah vertikal kiri mengirim $(X,x)$ ke $(X,\{x\})$, sedangkan panah
vertikal kanan mengirim grup $G$ ke grupoid satu objek $\mathbf{B}G$.
Komutativitas berarti

$$
\Pi_1(X,\{x\})
\cong
\mathbf{B}\pi_1(X,x).
$$

Selain itu, terdapat isomorfisma alami

$$
\Pi_1(X\times Y,A\times B)
\xrightarrow{\;\cong\;}
\Pi_1(X,A)\times\Pi_1(Y,B)
$$

dan

$$
\Pi_1(X,A)\sqcup\Pi_1(Y,B)
\xrightarrow{\;\cong\;}
\Pi_1(X\sqcup Y,A\sqcup B).
$$
:::

Produk grupoid pada proposisi ini dibentuk dengan mengambil produk himpunan
objek dan produk himpunan morfisma. Koproduk atau gabungan lepas grupoid
dibentuk dengan mengambil gabungan lepas himpunan objek dan gabungan lepas
himpunan morfisma.

Ruang tanpa titik dasar juga dapat dimasukkan ke dalam kategori pasangan
melalui

$$
X\longmapsto(X,X).
$$

Ini memberikan fungtor penuh dan setia
$\mathbf{Top}\to\mathbf{Top}^{(2)}$. Jadi, meskipun $X$ sama sekali tidak
memiliki titik dasar pilihan, kita tetap dapat mendefinisikan

$$
\Pi_1(X):=\Pi_1(X,X).
$$

Konstruksi tersebut merupakan fungtor
$\mathbf{Top}\to\mathbf{Gpd}$.

## Ruang terhubung sederhana {#o012-rbt-l08-s03}

Kita belum menghitung grup atau grupoid fundamental dalam banyak contoh.
Pertama-tama kita beri nama bagi ruang yang grupoid fundamentalnya trivial
dalam arti kodiskret.

::: {.definition #o012-rbt-l08-def-003}
**Definisi 8.3 (terhubung sederhana).** Ruang $X$ disebut *terhubung
sederhana* jika fungtor kanonik

$$
\Pi_1(X)\longrightarrow\operatorname{Codisc}(X)
$$

merupakan isomorfisma; dengan kata lain,

$$
\Pi_1(X)\cong\operatorname{Codisc}(X)
$$

secara identik pada objek.
:::

Menurut definisi kategoris ini, ruang kosong juga memenuhi syarat secara
vakum. Jika konvensi lain mendefinisikan “terhubung sederhana” hanya untuk
ruang tak kosong, tambahkan syarat $X\ne\varnothing$; semua hasil berikut
untuk ruang yang mempunyai titik tidak berubah.

Ruang semacam itu juga memenuhi

$$
\Pi_1(X,A)\cong\operatorname{Codisc}(A)
$$

untuk setiap $A\subseteq X$.

Untuk $X\ne\varnothing$, Definisi 8.3 dapat diuraikan menjadi dua syarat. Pertama, untuk setiap
$x,y\in X$ terdapat lintasan $x\rightsquigarrow y$, sehingga $X$ terhubung
lintasan. Kedua, semua lintasan di antara dua titik yang telah ditentukan
homotopik dengan titik ujung tetap. Jadi terdapat tepat satu morfisma dalam
grupoid fundamental di antara dua objek mana pun. Khususnya,

$$
\pi_1(X,x)=\Pi_1(X)(x,x)
$$

adalah grup trivial.

::: {.example #o012-rbt-l08-exa-002}
**Contoh 8.2 (himpunan konveks).** Setiap himpunan konveks
$C\subseteq\mathbb R^n$ terhubung sederhana. Setiap dua titik
$v,w\in C$ dapat dihubungkan oleh ruas garis. Jika
$\gamma,\eta\colon v\rightsquigarrow w$ adalah dua lintasan, maka

$$
H(s,t)=s\gamma(t)+(1-s)\eta(t)
$$

merupakan homotopi di dalam $C$ dari $\eta$ ke $\gamma$. Titik ujungnya tetap
karena

$$
H(s,0)=v,
\qquad
H(s,1)=w.
$$
:::

Secara khusus, interval $I$ terhubung sederhana. Grupoid

$$
\Pi_1(I,\{0,1\})
$$

cukup penting untuk diberi nama tersendiri, yaitu $\mathbf 2$. Grupoid ini
kadang ditulis

$$
0\xrightarrow{\;\cong\;}1.
$$

Ia mempunyai dua objek, $0$ dan $1$, serta tepat satu isomorfisma dalam
setiap arah di antara keduanya.

::: {.exercise #o012-rbt-l08-ex-001 data-origin="Roberts Notes.tex:1894-1900"}
**Latihan sumber 8.1 (daerah berbentuk bintang).** Dalam ruang vektor riil
atau kompleks $V$, definisikan *daerah berbentuk bintang* sebagai himpunan
$K\subseteq V$ yang mempunyai suatu $v_0\in K$ sedemikian sehingga, untuk
setiap $v\in K$ dan $t\in I$,

$$
tv_0+(1-t)v\in K.
$$

Buktikan bahwa setiap daerah berbentuk bintang terhubung sederhana.
:::

Sebagai contoh yang tidak konveks, ambil setengah bidang atas terbuka

$$
\mathcal H=\{z\in\mathbb C\mid\operatorname{Im}z>0\}.
$$

Himpunan $\mathcal H\cup\mathbb Q\subset\mathbb C$ berbentuk bintang dengan
pusat, misalnya, $i\in\mathcal H$: untuk $t>0$, titik
$ti+(1-t)v$ berada di $\mathcal H$, sedangkan pada $t=0$ ia sama dengan
$v$. Himpunan ini tidak konveks.

Ruang terhubung sederhana istimewa karena hubungannya dengan ruang penutup.

::: {.proposition #o012-rbt-l08-prop-002}
**Proposisi 8.2 (penutup terhubung di atas ruang terhubung sederhana).** Jika
$X$ terhubung sederhana, maka setiap ruang penutup terhubung lintasan

$$
\pi\colon Z\longrightarrow X
$$

bersifat trivial, dalam arti $\pi$ merupakan homeomorfisma.
:::

::: {.proof #o012-rbt-l08-proof-001}
**Bukti.** Kita memakai konvensi lazim bahwa ruang terhubung lintasan tidak
kosong. Pilih $z_0\in Z$ dan tuliskan $x_0=\pi(z_0)$. Karena $X$ terhubung
lintasan, untuk setiap $x\in X$ terdapat lintasan dari $x_0$ ke $x$;
pengangkatannya yang berawal di $z_0$ berakhir pada suatu titik $z_x\in Z_x$.
Jadi setiap serat tidak kosong. Karena $Z$ terhubung lintasan, pemetaan orbit

$$
\pi_1(X,x)\longrightarrow Z_x,
\qquad
[\gamma]\longmapsto\gamma_*(z_x),
$$

surjektif. Karena $X$ terhubung sederhana, $\pi_1(X,x)$ trivial. Jadi
$Z_x$ hanya mempunyai satu titik. Argumen yang sama berlaku bagi setiap
$x\in X$, sehingga $\pi$ bijektif.

Syarat trivialitas lokal suatu ruang penutup menyatakan bahwa setiap
$x\in X$ mempunyai lingkungan terbuka $U\ni x$ sedemikian sehingga

$$
\pi^{-1}(U)\longrightarrow U
$$

adalah homeomorfisma. Ambil semua lingkungan semacam itu sebagai suatu
penutup terbuka $\{U_\alpha\}$ bagi $X$. Invers-invers lokal
$U_\alpha\to\pi^{-1}(U_\alpha)$ berimpit pada setiap irisan karena
$\pi$ bijektif. Lema penempelan menggabungkannya menjadi invers kontinu
$X\to Z$ bagi $\pi$. Jadi $\pi$ adalah homeomorfisma. $\square$
:::

::: {.example #o012-rbt-l08-exa-003}
**Contoh 8.3 (ruang kontraktil).** Jika $X$ kontraktil, maka $X$
terhubung sederhana. Ambil kontraksi

$$
H\colon I\times X\longrightarrow X
$$

menuju $x_0\in X$, dengan

$$
H(0,x)=x,
\qquad
H(1,x)=x_0.
$$

Fungtor terinduksi

$$
h=\Pi_1(H)\colon
\Pi_1(I\times X,\{0,1\}\times X)
\longrightarrow
\Pi_1(X)
$$

mempunyai domain yang, menurut Proposisi 8.1, dapat ditulis

$$
\Pi_1(I,\{0,1\})\times\Pi_1(X)
=
\mathbf 2\times\Pi_1(X).
$$

Pada salinan $\{0\}\times\Pi_1(X)$, fungtor $h$ adalah identitas karena
$H|_{\{0\}\times X}=\operatorname{id}_X$. Pada salinan
$\{1\}\times\Pi_1(X)$, ia mengirim setiap objek ke $x_0$ dan setiap lintasan
ke lintasan konstan di $x_0$, karena
$H|_{\{1\}\times X}$ konstan. Khususnya,

$$
h(1,x)=x_0
$$

untuk setiap $x\in X$.

Kontraksi juga menunjukkan bahwa $X$ terhubung lintasan: lintasan
$s\mapsto H(s,x)$ menghubungkan $x$ dengan $x_0$. Sekarang ambil lintasan
$\gamma\colon x\rightsquigarrow y$. Di dalam
$\mathbf 2\times\Pi_1(X)$ terdapat persegi komutatif

$$
\begin{array}{ccc}
(0,x)
&\xrightarrow{\;(\operatorname{id}_0,[\gamma])\;}&
(0,y)\\[4pt]
\downarrow
&&
\uparrow\\[4pt]
(1,x)
&\xrightarrow{\;(\operatorname{id}_1,[\gamma])\;}&
(1,y).
\end{array}
$$

Panah vertikal adalah isomorfisma tunggal yang diberikan faktor
$\mathbf 2$ (dipasangkan dengan morfisma identitas pada objek yang
bersesuaian). Di bawah $h$, persegi itu menjadi

$$
\begin{array}{ccc}
x
&\xrightarrow{\;[\gamma]\;}&
y\\[4pt]
\downarrow
&&
\uparrow\\[4pt]
x_0
&\xrightarrow{\;\operatorname{id}_{x_0}\;}&
x_0.
\end{array}
$$

Citra kedua panah vertikal hanya bergantung pada $x$, $y$, dan kontraksi
$H$, bukan pada kelas $[\gamma]$. Komutativitas menunjukkan bahwa
$[\gamma]$ sama dengan komposit melalui $x_0$. Karena komposit tersebut
tidak bergantung pada pilihan $\gamma$, semua lintasan dari $x$ ke $y$
homotopik dengan titik ujung tetap. Maka
$\Pi_1(X)\cong\operatorname{Codisc}(X)$, sehingga $X$ terhubung sederhana.
:::

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l08-mastery}

Latihan Sumber 8.1 di atas berasal dari Roberts. Pemeriksaan 8.2--8.5 dan
seluruh solusi berikut merupakan materi asli edisi ini, ditambahkan di bawah
CC BY 4.0 untuk menutup langkah yang tidak dibuktikan dalam rentang sumber.

## Solusi Latihan Sumber 8.1 {#o012-rbt-l08-sol-001}

Pilih pusat bintang $v_0\in K$. Definisikan

$$
F\colon I\times K\longrightarrow K,
\qquad
F(s,v)=sv_0+(1-s)v.
$$

Definisi daerah berbentuk bintang menjamin bahwa citra $F$ berada di $K$.
Pemetaan itu kontinu dan memenuhi

$$
F(0,v)=v,
\qquad
F(1,v)=v_0.
$$

Jadi $K$ kontraktil. Kita dapat langsung memperoleh dua syarat pada
Definisi 8.3. Pertama, setiap $v\in K$ dihubungkan ke $v_0$ oleh
$s\mapsto F(s,v)$, sehingga $K$ terhubung lintasan.

Kedua, jika $\gamma,\eta\colon v\rightsquigarrow w$, definisikan lintasan
kanonik melalui pusat bintang

$$
\lambda_{v,w}
=
\bigl(s\mapsto F(s,v)\bigr)
\#
\overline{\bigl(s\mapsto F(s,w)\bigr)}.
$$

Homotopi kontraksi mengubah setiap lintasan $\gamma$ menjadi
$\lambda_{v,w}$ dengan titik ujung tetap; hal ini juga merupakan kasus
khusus argumen persegi pada Contoh 8.3. Hal yang sama berlaku bagi $\eta$.
Maka $\gamma\simeq\lambda_{v,w}\simeq\eta$ relatif terhadap titik ujung.
Jadi terdapat tepat satu kelas lintasan dari $v$ ke $w$, dan $K$ terhubung
sederhana.

::: {.exercise #o012-rbt-l08-mcheck-002}
**Pemeriksaan penguasaan 8.2 (struktur grupoid).** Buktikan seluruh Lema 8.1.
Kemudian tentukan orbit dan stabilisator dalam grupoid aksi $Y/\!/G$, serta
tentukan kapan grupoid itu diskret dan kapan ia kodiskret.
:::

## Solusi Pemeriksaan 8.2 {#o012-rbt-l08-sol-002}

Untuk $a\colon x\to y$ dan $g\colon x\to x$, komposit
$a^{-1}ga$ bertipe $y\to y$. Bagi $g,h\in\Gamma(x,x)$,

$$
\operatorname{Ad}_a(gh)
=a^{-1}gha
=(a^{-1}ga)(a^{-1}ha),
$$

karena $aa^{-1}=\operatorname{id}_x$ dalam urutan komposisi aljabar.
Selain itu,

$$
\operatorname{Ad}_{a^{-1}}\!\left(\operatorname{Ad}_a(g)\right)
=
a(a^{-1}ga)a^{-1}
=g,
$$

dan perhitungan sebaliknya sama. Jadi
$\operatorname{Ad}_a$ adalah isomorfisma grup dengan invers
$\operatorname{Ad}_{a^{-1}}$.

Rumus $g\cdot b=gb$ memenuhi

$$
\operatorname{id}_x\cdot b=b,
\qquad
(gh)\cdot b=g\cdot(h\cdot b),
$$

sehingga merupakan aksi. Jika $g\cdot b=b$, maka

$$
g=gbb^{-1}=bb^{-1}=\operatorname{id}_x,
$$

jadi aksi bebas. Jika $b,c\in\Gamma(x,y)$, ambil

$$
g=cb^{-1}\in\Gamma(x,x).
$$

Lalu $g\cdot b=(cb^{-1})b=c$, sehingga aksi transitif.

Dalam $Y/\!/G$, dua objek berada pada komponen grupoid yang sama tepat jika
mereka berada pada orbit $G$ yang sama. Grup automorfisma objek $y$ adalah
stabilisator

$$
G_y=\{g\in G\mid yg=y\}.
$$

Grupoid aksi diskret tepat ketika satu-satunya morfisma pada setiap objek
adalah identitas. Ini terjadi tepat ketika setiap orbit berupa satu titik
dan setiap stabilisator trivial, yakni ketika $G$ sendiri trivial apabila
$Y\neq\varnothing$. Untuk $Y=\varnothing$, grupoid kosong tentu diskret
untuk setiap $G$. Grupoid aksi kodiskret tepat ketika di antara setiap dua
objek terdapat tepat satu morfisma. Artinya, aksi $G$ pada $Y$ bebas dan
transitif. Dengan kata lain, jika $Y\neq\varnothing$, maka grupoid aksi
kodiskret tepat ketika $Y$ adalah torsor kanan bagi $G$. Jika
$Y=\varnothing$, maka $Y\mathbin{\!\sslash\!}G=\operatorname{Codisc}(\varnothing)$
untuk setiap $G$.

::: {.exercise #o012-rbt-l08-mcheck-003}
**Pemeriksaan penguasaan 8.3 (keabsahan dan fungtorialitas
$\Pi_1$).** Buktikan bahwa konkatenasi pada Definisi 8.2 terdefinisi baik
pada kelas, memenuhi aksioma grupoid, dan fungtorial terhadap morfisma
pasangan. Buktikan pula kedua isomorfisma pada Proposisi 8.1. Terakhir,
tunjukkan bahwa setiap ruang penutup $\pi\colon Z\to X$ menentukan fungtor
monodromi $\rho_Z\colon\Pi_1(X)\to\mathbf{Set}$ dan jelaskan bagaimana
restriksinya pada loop menghasilkan aksi kanan Unit 7.
:::

## Solusi Pemeriksaan 8.3 {#o012-rbt-l08-sol-003}

Untuk ruang sebarang, ambil kelas homotopi berujung tetap

$$
[\gamma]\in[\{*\},P_x^yX],
\qquad
[\eta]\in[\{*\},P_y^zX].
$$

Konkatenasi kontinu sebagai pemetaan ruang lintasan menurut Pemeriksaan
Penguasaan 7.2. Karena itu, homotopi berujung tetap pada $\gamma$ atau
$\eta$ menghasilkan homotopi berujung tetap pada $\gamma\#\eta$. Maka

$$
[\gamma][\eta]:=[\gamma\#\eta]
$$

tidak bergantung pada wakil. Homotopi reparameterisasi dari Unit 7
menunjukkan asosiativitas pada kelas. Kelas lintasan konstan $[c_x]$
menjadi identitas, dan kelas lintasan balik $[\bar\gamma]$ menjadi invers.
Jadi struktur ini benar-benar suatu grupoid.

Untuk morfisma pasangan $f\colon(X,A)\to(Y,B)$, definisikan

$$
\Pi_1(f)(x)=f(x),
\qquad
\Pi_1(f)([\gamma])=[f\circ\gamma].
$$

Komposisi dengan $f$ membawa homotopi berujung tetap ke homotopi berujung
tetap. Ia juga memenuhi

$$
f\circ(\gamma\#\eta)
=(f\circ\gamma)\#(f\circ\eta),
\qquad
f\circ c_x=c_{f(x)}.
$$

Jadi $\Pi_1(f)$ adalah fungtor grupoid. Rumus tersebut jelas mempertahankan
identitas dan komposisi pemetaan pasangan, sehingga $\Pi_1$ adalah fungtor.
Pada pasangan $(X,\{x\})$, hanya ada satu objek dan grup automorfismanya
adalah $\pi_1(X,x)$. Ini membuktikan komutativitas diagram Proposisi 8.1.

Selanjutnya, pemetaan

$$
P_{(x,y)}^{(x',y')}(X\times Y)
\longrightarrow
P_x^{x'}X\times P_y^{y'}Y,
\qquad
\gamma\longmapsto
(\operatorname{pr}_X\circ\gamma,\operatorname{pr}_Y\circ\gamma)
$$

adalah homeomorfisma, dengan invers yang memasangkan kedua lintasan titik
demi titik. Setelah mengambil kelas homotopi dan memakai bijeksi alami

$$
[\{*\},M\times N]
\cong
[\{*\},M]\times[\{*\},N],
$$

kita memperoleh isomorfisma produk pada objek maupun morfisma. Pada ruang
SLSC, ini juga dapat dibaca sebagai rumus $\pi_0$ dalam Definisi 8.2.
Rumus tersebut menghormati konkatenasi koordinat demi koordinat.

Terakhir, setiap lintasan $I\to X\sqcup Y$ seluruhnya berada di $X$ atau
seluruhnya berada di $Y$, karena $I$ terhubung dan kedua bagian gabungan
lepas itu terbuka sekaligus tertutup. Jadi tidak ada morfisma yang melintasi
kedua bagian, sedangkan semua morfisma di dalam masing-masing bagian tetap ada. Ini
memberikan isomorfisma koproduk pada Proposisi 8.1.

Untuk ruang penutup $\pi\colon Z\to X$, definisikan fungtor monodromi pada
objek dan morfisma dengan

$$
\rho_Z(x)=Z_x,
\qquad
\rho_Z([\gamma])=\gamma_*\colon Z_x\longrightarrow Z_y
$$

bagi $[\gamma]\colon x\to y$. Invariansi transpor terhadap homotopi berujung
tetap membuat rumus ini terdefinisi baik. Lintasan konstan menginduksi
identitas, sedangkan Lema 7.1 memberi

$$
\rho_Z([\gamma][\eta])
=(\gamma\#\eta)_*
=\eta_*\circ\gamma_*
=\rho_Z([\eta])\circ\rho_Z([\gamma]).
$$

Ini tepat hukum fungtor untuk konvensi komposisi aljabar, yakni pertama
$[\gamma]$ lalu $[\eta]$. Pada grup automorfisma objek $x$, tuliskan
$z\cdot[\gamma]=\gamma_*(z)$. Persamaan yang sama menjadi

$$
z\cdot([\gamma][\eta])
=(z\cdot[\gamma])\cdot[\eta],
$$

yaitu aksi kanan pada serat $Z_x$. Jika aksi kiri lebih disukai, balik setiap
loop sebagaimana dijelaskan pada Unit 7.

::: {.exercise #o012-rbt-l08-mcheck-004}
**Pemeriksaan penguasaan 8.4 (kriteria keterhubungan sederhana dan
penutup).** Untuk ruang terhubung lintasan $X$, buktikan bahwa syarat-syarat
berikut ekuivalen:

1. $X$ terhubung sederhana;
2. $\pi_1(X,x)$ trivial untuk satu titik $x\in X$;
3. $\pi_1(X,y)$ trivial untuk setiap titik $y\in X$.

Jelaskan pula dengan contoh mengapa kata “terhubung lintasan” pada Proposisi
8.2 tidak boleh dihapus dari hipotesis ruang atas $Z$.
:::

## Solusi Pemeriksaan 8.4 {#o012-rbt-l08-sol-004}

Implikasi (1)$\Rightarrow$(3) langsung dari Definisi 8.3, dan
(3)$\Rightarrow$(2) langsung. Untuk (2)$\Rightarrow$(3), pilih lintasan
$a\colon x\rightsquigarrow y$. Lema 8.1 memberi isomorfisma konjugasi

$$
\pi_1(X,x)\xrightarrow{\;\cong\;}\pi_1(X,y).
$$

Jadi trivialitas pada $x$ mengakibatkan trivialitas pada $y$.

Untuk membuktikan (2)$\Rightarrow$(1), ambil dua lintasan
$\gamma,\eta\colon y\rightsquigarrow z$. Karena $X$ terhubung lintasan,
pilih $a\colon x\rightsquigarrow y$. Komposit

$$
a\#\gamma\#\bar\eta\#\bar a
$$

adalah loop pada $x$. Kelasnya trivial, sehingga pembatalan kelas
$[a]$ dan $[\bar a]$ di dalam grupoid memberi
$[\gamma]=[\eta]$. Maka di antara setiap dua objek terdapat tepat satu
morfisma, sehingga $\Pi_1(X)$ kodiskret.

Sekarang ambil ruang terhubung sederhana $X$ dan himpunan diskret $S$ yang
mempunyai sedikitnya dua unsur. Proyeksi penutup trivial

$$
S\times X\longrightarrow X
$$

bukan homeomorfisma, sebab setiap serat mempunyai $|S|>1$ titik. Ruang atas
$S\times X$ bukan terhubung lintasan: setiap $\{s\}\times X$ adalah komponen
lintasannya. Jadi hipotesis keterhubungan lintasan pada $Z$ tepat menyingkirkan
penutup trivial dengan lebih dari satu lembaran.

::: {.exercise #o012-rbt-l08-mcheck-005}
**Pemeriksaan penguasaan 8.5 (argumen kontraksi tanpa diagram).** Misalkan
$H(0,u)=u$ dan $H(1,u)=x_0$. Untuk setiap $u\in X$, definisikan
$\rho_u(s)=H(s,u)$. Tunjukkan langsung bahwa setiap lintasan
$\gamma\colon x\rightsquigarrow y$ homotopik dengan titik ujung tetap
terhadap $\rho_x\#\bar\rho_y$. Deduksikan kembali bahwa $X$ terhubung
sederhana dan cocokkan perhitungan ini dengan persegi pada Contoh 8.3.
:::

## Solusi Pemeriksaan 8.5 {#o012-rbt-l08-sol-005}

Definisikan

$$
K\colon I\times I\longrightarrow X,
\qquad
K(s,t)=H(s,\gamma(t)).
$$

Untuk $s=0$, kita memperoleh

$$
K(0,t)=\gamma(t).
$$

Untuk $s=1$, lintasan itu konstan:

$$
K(1,t)=x_0.
$$

Namun $K$ belum merupakan homotopi berujung tetap, sebab sisi-sisinya
bergerak menurut

$$
K(s,0)=\rho_x(s),
\qquad
K(s,1)=\rho_y(s).
$$

Menelusuri batas mulai dari $(0,0)$, pertama-tama dalam arah $t$ meningkat,
memberikan loop

$$
\gamma\#\rho_y\#\bar c_{x_0}\#\bar\rho_x,
$$

yang null-homotopik melalui $K$. Karena $c_{x_0}$ adalah identitas pada
kelas lintasan, persamaan batas di dalam grupoid fundamental adalah

$$
[\gamma][\rho_y][\bar\rho_x]
=
[c_x].
$$

Kalikan dengan kelas invers yang sesuai, atau baca kembali arah batas
persegi, untuk mendapatkan

$$
[\gamma]
=
[\rho_x][\bar\rho_y].
$$

Dengan demikian

$$
\gamma\simeq\rho_x\#\bar\rho_y
\quad\text{relatif terhadap }\{0,1\}.
$$

Ruas kanan hanya bergantung pada $x$, $y$, dan kontraksi $H$, bukan pada
$\gamma$. Jadi setiap dua lintasan $x\rightsquigarrow y$ berada dalam kelas
yang sama. Karena $\rho_x\#\bar\rho_y$ juga memperlihatkan adanya lintasan
dari $x$ ke $y$, $X$ terhubung lintasan dan grupoid fundamentalnya
kodiskret.

Dalam persegi Contoh 8.3, citra panah vertikal kiri adalah
$[\rho_x]$, sedangkan citra panah vertikal kanan yang diarahkan ke atas
adalah $[\bar\rho_y]$. Panah bawah menjadi
$[\operatorname{id}_{x_0}]$. Maka “jalan memutar” dari $x$ ke $y$ tepat
$[\rho_x][\bar\rho_y]$, sama dengan perhitungan langsung di atas.
