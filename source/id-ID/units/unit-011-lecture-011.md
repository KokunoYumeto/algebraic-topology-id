---
title: "Topologi Aljabar"
subtitle: "Unit 11: Produk Bebas, Pushout, dan Teorema Seifert–van Kampen"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l11-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts (2019), tepatnya [Notes.tex baris
2273--2494 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L2273-L2494).
Rentang itu dimulai dengan penanda Kuliah 11 dan definisi grup bebas, lalu
berakhir sesudah langkah pemanasan lokal dalam bukti teorema
Seifert--van Kampen. Baris 2495 memulai Kuliah 12 dan melanjutkan bukti
tersebut; baris itu tidak termasuk dalam unit ini. Karena itu bukti pada unit
ini sengaja ditandai **belum selesai**, bukan diberi tanda akhir bukti. Karya
sumber tersedia di bawah [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah
dibaca, pemberian pengenal stabil, dan pemindahan keenam unsur pinggir ke
urutan bacaan utama. Kesebelas diagram sumber ditulis ulang sebagai diagram
semantik, daftar panah, atau rumus parametrik yang dapat dibaca tanpa
mengandalkan posisi visual. Dua gambar terakhir, yang membandingkan lintasan
sepanjang sisi persegi dan deformasinya, diganti dengan parameter eksplisit
bagi kedua lintasan dan homotopi berujung tetap di antaranya.

Beberapa cacat sumber diperbaiki secara independen. Dalam sifat universal
produk bebas, persamaan yang tidak bertipe
$\phi=i\circ\kappa$ dan $\psi=j\circ\kappa$ diperbaiki menjadi
$\phi=\kappa\circ i$ dan $\psi=\kappa\circ j$. Kalimat tentang presentasi
yang menukar peran $G$ dan $H$ diselaraskan dengan rumusnya. Deskripsi unsur
grup bebas dilengkapi dengan reduksi pasangan invers; kata mentah tidak dapat
langsung menjadi unsur grup karena $x_ix_i^{-1}$ harus sama dengan kata
kosong. Dalam konstruksi fungtor pada bukti van Kampen, notasi sumber
$F_1(\gamma)$ dan $G_1(\gamma)$ diperbaiki menjadi
$F_1([\gamma])$ dan $G_1([\gamma])$, sebab domain fungtor adalah kelas
homotopi lintasan, bukan lintasan mentah. Edisi juga membedakan fungsi
sementara $\widetilde K_1$ pada lintasan mentah dari fungsi $K_1$ pada kelas
homotopi yang baru dapat diturunkan setelah invariansi homotopi terbukti.
Beberapa ketidakteraturan tata bahasa dan singkatan juga dinormalkan tanpa
mengubah isi matematis.

Rentang sumber tidak memuat latihan. Bagian pendamping penguasaan menambahkan
tiga pemeriksaan dengan solusi lengkap: sifat universal grup bebas dan produk
bebas; verifikasi pushout topologis dan ruang vektor; serta kemandirian
subdivisi bersama homotopi eksplisit antara dua lintasan batas persegi. Bagian
terakhir juga mencatat dengan tepat langkah global mana yang belum tersedia
sebelum Kuliah 12. Seluruh materi pendamping yang ditambahkan tersedia di
bawah CC BY 4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan
atau pengesahan dari penulis sumber.

# Kuliah 11 {#o012-rbt-l11}

## Grup bebas dan produk bebas {#o012-rbt-l11-s01}

::: {.definition #o012-rbt-l11-def-001}
**Definisi 11.1 (grup bebas).** *Grup bebas pada $n$ simbol* adalah grup
$F_n$ dengan presentasi

$$
F_n
=
\langle x_1,\ldots,x_n\mid\ \rangle.
$$

Jadi $x_1,\ldots,x_n$ merupakan pembangkit dan tidak dikenai relasi tambahan.
:::

Nama simbol-simbol itu tentu saja dapat diganti. Setiap unsur $F_n$ diwakili
oleh kata berhingga dalam huruf

$$
x_1^{\pm1},\ldots,x_n^{\pm1}.
$$

Dua kata mewakili unsur yang sama bila dapat dihubungkan dengan penyisipan
atau penghapusan pasangan bersebelahan $x_ix_i^{-1}$ atau
$x_i^{-1}x_i$. Dengan menghapus semua pasangan semacam itu, setiap unsur
mempunyai wakil berupa kata tereduksi. Kata kosong $()$ mewakili identitas,
dan perkalian dilakukan dengan mengonkatenasikan kata lalu mereduksi hasilnya.

::: {.definition #o012-rbt-l11-def-002}
**Definisi 11.2 (produk bebas).** Diberikan grup $G$ dan $H$, *produk bebas*
$G*H$ adalah grup yang dilengkapi homomorfisma

$$
i\colon G\longrightarrow G*H,
\qquad
j\colon H\longrightarrow G*H,
$$

dengan sifat berikut. Untuk setiap grup $K$ dan setiap pasangan homomorfisma

$$
\phi\colon G\longrightarrow K,
\qquad
\psi\colon H\longrightarrow K,
$$

terdapat tepat satu homomorfisma

$$
\kappa\colon G*H\longrightarrow K
$$

yang memenuhi

$$
\kappa\circ i=\phi,
\qquad
\kappa\circ j=\psi.
$$
:::

::: {.figure #o012-rbt-l11-fig-001}
**Diagram 11.1 (sifat universal produk bebas).** Data dan pemetaan universal
dapat dibaca dari diagram komutatif

$$
\begin{array}{ccccc}
G&\xrightarrow{\ i\ }&G*H&\xleftarrow{\ j\ }&H\\
&\searrow_{\phi}&\mathrel{\phantom{G*H}}\downarrow{\scriptstyle\exists!\,\kappa}
&\swarrow_{\psi}&\\
&&K&&
\end{array}
$$

dengan dua lintasan komposit
$G\xrightarrow{i}G*H\xrightarrow{\kappa}K$ dan
$H\xrightarrow{j}G*H\xrightarrow{\kappa}K$. Keduanya masing-masing harus
sama dengan $\phi$ dan $\psi$.
:::

Keberadaan dan keunikan $\kappa$ setelah $\phi$ serta $\psi$ diberikan
disebut *sifat universal* produk bebas.

Misalkan

$$
G=\langle g_1,\ldots,g_m\mid R_1,\ldots,R_n\rangle
$$

dan

$$
H=\langle h_1,\ldots,h_k\mid Q_1,\ldots,Q_l\rangle
$$

masing-masing merupakan presentasi $G$ dan $H$. Setiap $R_i$ dan $Q_j$
adalah relasi, yakni persamaan yang melibatkan pembangkit grup terkait. Produk
bebasnya mempunyai presentasi

$$
G*H
=
\langle
g_1,\ldots,g_m,h_1,\ldots,h_k
\mid
R_1,\ldots,R_n,Q_1,\ldots,Q_l
\rangle.
$$

Produk bebas grup merupakan kasus khusus konstruksi yang lebih umum, yaitu
*produk bebas dengan amalgamasi*. Keduanya pada gilirannya merupakan contoh
dari sebuah konstruksi yang masuk akal dalam kategori sebarang.

## Pushout dalam suatu kategori {#o012-rbt-l11-s02}

::: {.definition #o012-rbt-l11-def-003}
**Definisi 11.3 (persegi pushout).** Misalkan $\mathcal C$ suatu kategori.
Sebuah *persegi pushout* adalah persegi komutatif

$$
\begin{array}{ccc}
W&\xrightarrow{\ b\ }&Y\\
{\scriptstyle a}\downarrow&&\downarrow{\scriptstyle d}\\
X&\xrightarrow{\ c\ }&P
\end{array}
$$

di $\mathcal C$ dengan sifat universal berikut. Untuk setiap pasangan
morfisma

$$
X\xrightarrow{f}Z\xleftarrow{g}Y
$$

yang kompatibel pada $W$, yakni

$$
f\circ a=g\circ b,
$$

terdapat tepat satu morfisma $k\colon P\to Z$ yang memenuhi

$$
f=k\circ c,
\qquad
g=k\circ d.
$$
:::

::: {.figure #o012-rbt-l11-fig-002}
**Diagram 11.2 (pemetaan keluar dari pushout).** Persegi pada Definisi 11.3
menyatakan $c\circ a=d\circ b$. Sifat universal menambahkan dua panah
$f\colon X\to Z$ dan $g\colon Y\to Z$ yang sepakat setelah didahului oleh
$a$ dan $b$, lalu menghasilkan satu-satunya panah
$k\colon P\to Z$. Dengan demikian kedua segitiga

$$
X\xrightarrow{c}P\xrightarrow{k}Z,
\qquad
Y\xrightarrow{d}P\xrightarrow{k}Z
$$

masing-masing sama dengan $f$ dan $g$. Keberadaan unik inilah sifat universal
pushout.
:::

Berikut beberapa contoh dalam kategori yang berbeda.

::: {.example #o012-rbt-l11-exa-001}
**Contoh 11.1 (merekatkan subruang).** Misalkan $X$ ruang topologis dan
$U,V\subseteq X$ subruang sedemikian sehingga

$$
\{U^\circ,V^\circ\}
$$

merupakan sampul terbuka dari $X$. Maka persegi semua pemetaan inklusi

$$
\begin{array}{ccc}
U\cap V&\longrightarrow&V\\
\downarrow&&\downarrow\\
U&\longrightarrow&X
\end{array}
$$

merupakan persegi pushout di $\mathbf{Top}$.
:::

::: {.figure #o012-rbt-l11-fig-003}
**Diagram 11.3 (fungsi diagram perekatan).** Panah atas dan kiri memasukkan
$U\cap V$ ke $V$ dan $U$. Panah kanan dan bawah memasukkan $V$ dan $U$ ke
$X$. Jadi persegi itu menyatakan bahwa $U$ dan $V$ direkatkan sepanjang
$U\cap V$ untuk menghasilkan $X$.
:::

Dalam situasi ini, $\{U,V\}$ disebut *sampul $X$ oleh lingkungan*: setiap
titik di $X$ mempunyai setidaknya salah satu dari $U$ dan $V$ sebagai
lingkungan. Syarat tersebut ekuivalen dengan pernyataan bahwa interior
$U^\circ$ dan $V^\circ$ menyampuli $X$.

::: {.example #o012-rbt-l11-exa-002}
**Contoh 11.2 (baji ruang bertitik).** Untuk setiap pasangan ruang bertitik
$(X,x)$ dan $(Y,y)$, persegi

$$
\begin{array}{ccc}
(*,*)&\longrightarrow&(Y,y)\\
\downarrow&&\downarrow{\scriptstyle\operatorname{in}_R}\\
(X,x)&\xrightarrow{\ \operatorname{in}_L\ }&(X\vee Y,*)
\end{array}
$$

merupakan persegi pushout di $\mathbf{Top}_*$.
:::

::: {.figure #o012-rbt-l11-fig-004}
**Diagram 11.4 (fungsi diagram baji).** Dua panah keluar dari ruang bertitik
satu-titik memilih $x$ dan $y$. Pushout mengidentifikasi kedua titik pilihan
itu, sedangkan $\operatorname{in}_L$ dan $\operatorname{in}_R$ memasukkan
kedua faktor ke baji. Sifat universalnya tepat sifat universal baji pada
Unit 10.
:::

::: {.example #o012-rbt-l11-exa-003}
**Contoh 11.3 (produk bebas grup).** Untuk grup sebarang $G$ dan $H$,
persegi

$$
\begin{array}{ccc}
1&\longrightarrow&H\\
\downarrow&&\downarrow{\scriptstyle j}\\
G&\xrightarrow{\ i\ }&G*H
\end{array}
$$

merupakan persegi pushout di $\mathbf{Grp}$.
:::

::: {.figure #o012-rbt-l11-fig-005}
**Diagram 11.5 (fungsi diagram produk bebas).** Kedua panah keluar dari grup
trivial $1$ adalah homomorfisma unik. Memberikan homomorfisma yang kompatibel
dari $G$ dan $H$ ke grup $K$ kemudian sama persis dengan memberikan pasangan
$\phi,\psi$ pada Definisi 11.2; pemetaan universal dari pushout adalah
$\kappa\colon G*H\to K$.
:::

::: {.example #o012-rbt-l11-exa-004}
**Contoh 11.4 (menghasilkan satu loop dari satu panah).** Ingat grupoid
$\mathbf 2$ yang mempunyai dua objek $0,1$ dan tepat satu panah di antara
setiap pasangan objek terurut. Tuliskan
$\operatorname{Disc}(\{0,1\})$ bagi grupoid diskret pada kedua objek itu,
$*$ bagi grupoid satu-objek trivial, dan $\mathbf B\mathbb Z$ bagi grupoid
satu-objek dengan grup automorfisma $\mathbb Z$. Persegi

$$
\begin{array}{ccc}
\operatorname{Disc}(\{0,1\})&\longrightarrow&\mathbf 2\\
\downarrow&&\downarrow\\
*&\longrightarrow&\mathbf B\mathbb Z
\end{array}
$$

merupakan pushout di $\mathbf{Gpd}$.
:::

::: {.figure #o012-rbt-l11-fig-006}
**Diagram 11.6 (semua data panah pada pushout grupoid).** Panah atas adalah
identitas pada himpunan objek $\{0,1\}$. Panah kiri menyatukan kedua objek
menjadi objek tunggal $\bullet$. Panah kanan juga mengirim $0$ dan $1$ ke
$\bullet$, serta mengirim panah unik

$$
0\longrightarrow1
$$

ke automorfisma $1\in\mathbb Z$ dari $\bullet$; panah baliknya dikirim ke
$-1$. Panah bawah adalah fungtor unik dari grupoid satu-objek trivial. Dengan
menyatukan kedua objek, panah $0\to1$ menjadi satu loop bebas, sehingga
pushoutnya adalah $\mathbf B\mathbb Z$.
:::

Sifat universal contoh ini dapat diperiksa langsung. Misalkan $\Gamma$
sebuah grupoid, dan diberikan fungtor kompatibel

$$
A\colon\mathbf 2\longrightarrow\Gamma,
\qquad
B\colon *\longrightarrow\Gamma.
$$

Kompatibilitas pada $\operatorname{Disc}(\{0,1\})$ memaksa

$$
A(0)=B(*)=A(1)=:x.
$$

Karena itu $a:=A(0\to1)$ merupakan automorfisma $x$. Terdapat tepat satu
fungtor

$$
L\colon\mathbf B\mathbb Z\longrightarrow\Gamma
$$

yang mengirim objek tunggal ke $x$ dan mengirim $n\in\mathbb Z$ ke $a^n$.
Fungtor ini membatasi menjadi $A$ dan $B$: khususnya, $1$ dikirim ke $a$ dan
$-1$ ke $a^{-1}$. Sebaliknya, setiap fungtor yang memperluas $A$ dan $B$
harus mempunyai nilai-nilai tersebut, sehingga $L$ unik. Inilah sifat
universal pushout, bukan sekadar kemiripan bentuk diagram.

::: {.example #o012-rbt-l11-exa-005}
**Contoh 11.5 (pushout ruang vektor).** Dalam kategori $\mathbf{Vect}$ ruang
vektor di atas sebuah lapangan tetap, misalkan

$$
L_1\colon W\longrightarrow V_1,
\qquad
L_2\colon W\longrightarrow V_2
$$

pemetaan linear. Definisikan

$$
\begin{aligned}
J\colon W&\longrightarrow V_1\oplus V_2,\\
w&\longmapsto\bigl(L_1(w),-L_2(w)\bigr).
\end{aligned}
$$

Maka persegi

$$
\begin{array}{ccc}
W&\xrightarrow{\ L_2\ }&V_2\\
{\scriptstyle L_1}\downarrow&&\downarrow\\
V_1&\longrightarrow&(V_1\oplus V_2)/J(W)
\end{array}
$$

merupakan pushout.
:::

::: {.figure #o012-rbt-l11-fig-007}
**Diagram 11.7 (pemetaan kanonik pada pushout ruang vektor).** Panah bawah
dan kanan diberikan oleh

$$
v_1\longmapsto[(v_1,0)],
\qquad
v_2\longmapsto[(0,v_2)].
$$

Kedua komposit dari $W$ sama karena

$$
[(L_1(w),0)]-[(0,L_2(w))]
=
[(L_1(w),-L_2(w))]
=0
$$

dalam hasil bagi tersebut.
:::

## Teorema Seifert--van Kampen dalam bentuk grupoid {#o012-rbt-l11-s03}

::: {.theorem #o012-rbt-l11-thm-001}
**Teorema 11.1 (Seifert--van Kampen).** Misalkan $X$ suatu ruang dan
$\{U,V\}$ sampul $X$ oleh lingkungan. Maka persegi fungtor yang diinduksi
oleh inklusi

$$
\begin{array}{ccc}
\Pi_1(U\cap V)&\xrightarrow{\ i_V\ }&\Pi_1(V)\\
{\scriptstyle i_U}\downarrow&&\downarrow\\
\Pi_1(U)&\longrightarrow&\Pi_1(X)
\end{array}
$$

merupakan persegi pushout di $\mathbf{Gpd}$.
:::

::: {.figure #o012-rbt-l11-fig-008}
**Diagram 11.8 (fungsi diagram van Kampen).** Objek kiri atas merekam titik
dan kelas lintasan yang seluruhnya berada dalam $U\cap V$. Fungtor $i_U$ dan
$i_V$ memandang data yang sama masing-masing di dalam $U$ dan $V$. Kedua
fungtor berikutnya memandangnya di dalam $X$. Pernyataan pushout mengatakan
bahwa setiap pasangan fungtor kompatibel keluar dari $\Pi_1(U)$ dan
$\Pi_1(V)$ dapat, secara unik, direkatkan menjadi fungtor keluar dari
$\Pi_1(X)$.
:::

Sampul oleh lingkungan pada teorema itu dapat secara ekuivalen dinyatakan
dengan syarat bahwa $\{U^\circ,V^\circ\}$ merupakan sampul terbuka.

::: {.remark #o012-rbt-l11-rem-001}
**Catatan 11.1.** Kesimpulan teorema tidak langsung mengikuti hanya dari
kenyataan bahwa persegi ruang

$$
\begin{array}{ccc}
U\cap V&\longrightarrow&V\\
\downarrow&&\downarrow\\
U&\longrightarrow&X
\end{array}
$$

merupakan pushout di $\mathbf{Top}$. Sifat universal masih harus diperiksa
terhadap **setiap** grupoid $\Gamma$ dan setiap pasangan fungtor kompatibel

$$
\Pi_1(U)\longrightarrow\Gamma\longleftarrow\Pi_1(V).
$$
:::

## Konstruksi fungtor universal: bagian pertama bukti {#o012-rbt-l11-s04}

::: {.proof #o012-rbt-l11-proof-001}
**Bukti Teorema 11.1 (bagian pertama; berlanjut pada Kuliah 12).** Mulailah
dengan persegi komutatif sebarang

$$
\begin{array}{ccc}
\Pi_1(U\cap V)&\xrightarrow{\ i_V\ }&\Pi_1(V)\\
{\scriptstyle i_U}\downarrow&&\downarrow{\scriptstyle G}\\
\Pi_1(U)&\xrightarrow{\ F\ }&\Gamma.
\end{array}
$$

Kita harus membangun fungtor

$$
K\colon\Pi_1(X)\longrightarrow\Gamma
$$

yang kompatibel dengan $F$ dan $G$. Secara konkret, kita perlu membangun
fungsi pada objek dan morfisma

$$
K_0\colon\Pi_1(X)_0=X\longrightarrow\Gamma_0,
\qquad
K_1\colon\Pi_1(X)_1\longrightarrow\Gamma_1
$$

yang bersama-sama memenuhi hukum fungtor.

::: {.figure #o012-rbt-l11-fig-009}
**Diagram 11.9 (masalah universal yang harus diselesaikan).** Fungtor $F$ dan
$G$ telah diberikan dan memenuhi

$$
F\circ i_U=G\circ i_V.
$$

Fungtor yang dicari harus membuat kedua segitiga

$$
\Pi_1(U)\longrightarrow\Pi_1(X)\xrightarrow{K}\Gamma,
\qquad
\Pi_1(V)\longrightarrow\Pi_1(X)\xrightarrow{K}\Gamma
$$

masing-masing sama dengan $F$ dan $G$.
:::

### Fungsi pada objek {#o012-rbt-l11-proof-objects}

Ambil $x\in X$. Jika $x\in U$, definisikan $K_0(x)=F(x)$; jika $x\in V$,
definisikan $K_0(x)=G(x)$. Setiap titik tercakup oleh setidaknya salah satu
dari $U,V$. Jika $x\in U\cap V$, komutativitas persegi memberi

$$
F(x)=G(x),
$$

sehingga $K_0$ terdefinisi baik.

### Fungsi pada lintasan yang berada dalam satu anggota sampul {#o012-rbt-l11-proof-local-paths}

Tuliskan $\mathcal P(X)$ bagi himpunan semua lintasan kontinu $I\to X$.
Kita mula-mula membangun fungsi sementara

$$
\widetilde K_1\colon\mathcal P(X)\longrightarrow\Gamma_1
$$

pada lintasan nyata, lalu akan menunjukkan bahwa nilainya tidak berubah pada
kelas homotopi berujung tetap. Hanya setelah itu fungsi pada morfisma dapat
didefinisikan oleh $K_1([\gamma]):=\widetilde K_1(\gamma)$.
Misalkan $\gamma\colon I\to X$ mempunyai citra di $U$. Definisikan

$$
\widetilde K_1(\gamma):=F_1([\gamma]_U).
$$

Serupa dengan itu, jika citra $\gamma$ berada di $V$, definisikan

$$
\widetilde K_1(\gamma):=G_1([\gamma]_V).
$$

Jika citranya berada di $U\cap V$, kedua nilai sama karena persegi fungtor
yang diberikan komutatif. Definisi itu kompatibel dengan sumber dan sasaran:
titik awal serta akhir lintasan di $U$ juga berada di $U$, dan hal yang sama
berlaku bagi $V$. Definisi juga kompatibel dengan konkatenasi lintasan yang
seluruhnya berada di $U$ atau seluruhnya berada di $V$, karena $F$ dan $G$
adalah fungtor. Lintasan konstan dikirim ke morfisma identitas di $\Gamma$.

Jika $\sigma\colon I\to I$ suatu pemetaan kontinu dengan
$\sigma(0)=0$ dan $\sigma(1)=1$, maka $\gamma\circ\sigma$ homotopik berujung
tetap dengan $\gamma$, melalui interpolasi lurus antara $\sigma$ dan
$\operatorname{id}_I$. Karena itu

$$
\widetilde K_1(\gamma\circ\sigma)=\widetilde K_1(\gamma)
$$

ketika $\gamma$ berada dalam $U$ atau dalam $V$. Jadi nilai lokal tidak
bergantung pada parameter lintasan.

### Lintasan umum dan subdivisi {#o012-rbt-l11-proof-subdivision}

Sekarang ambil lintasan umum $\gamma\colon I\to X$. Tarik balik sampul
terbuka $\{U^\circ,V^\circ\}$ sepanjang $\gamma$ menjadi sampul terbuka

$$
\mathcal U_\gamma
:=
\{\gamma^{-1}(U^\circ),\gamma^{-1}(V^\circ)\}
$$

dari interval metrik kompak $I$. Lema bilangan Lebesgue memberi
$\delta>0$ sedemikian sehingga setiap himpunan bagian dari $I$ yang
berdiameter kurang dari $\delta$ termuat dalam satu anggota
$\mathcal U_\gamma$. Pilih partisi yang setiap subintervalnya berpanjang
kurang dari $\delta$,

$$
0=t_0<t_1<\cdots<t_n<t_{n+1}=1
$$

sedemikian sehingga untuk setiap $i=0,\ldots,n$, pembatasan

$$
\gamma|_{[t_i,t_{i+1}]}
$$

mempunyai citra seluruhnya di $U$ atau seluruhnya di $V$ (atau keduanya).
Definisikan lintasan berparameter baku

$$
\gamma_i(s)
:=
\gamma\bigl((1-s)t_i+s t_{i+1}\bigr),
\qquad 0\leq s\leq1.
$$

Lintasan $\gamma$ merupakan reparameterisasi dari konkatenasi kronologis

$$
\gamma_0\#\gamma_1\#\cdots\#\gamma_n.
$$

Semua $\widetilde K_1(\gamma_i)$ sudah terdefinisi, maka tetapkan

$$
\widetilde K_1(\gamma)
:=
\widetilde K_1(\gamma_0)\widetilde K_1(\gamma_1)\cdots
\widetilde K_1(\gamma_n)
\in\Gamma_1.
$$

Di sini perkalian morfisma mengikuti urutan komposisi aljabar yang sudah
ditetapkan: faktor paling kiri ditempuh terlebih dahulu.

Jika partisi diperhalus, satu ruas lama diganti oleh beberapa ruas yang masih
berada dalam anggota sampul yang sama. Fungtorialitas $F$ atau $G$ membuat
komposit nilai ruas-ruas baru sama dengan nilai ruas lama. Jika suatu ruas
berada dalam $U\cap V$, komutativitas persegi memastikan tidak ada pilihan
ambigu. Setiap dua partisi memiliki perhalusan bersama. Karena itu nilai
$\widetilde K_1(\gamma)$ tidak bergantung pada partisi yang dipilih.

Keterangan pinggir sumber pada langkah ini menyebut secara eksplisit bahwa
partisi tersebut diperoleh dari lema bilangan Lebesgue.

Untuk menurunkan fungsi ini dari lintasan nyata ke morfisma
$\Pi_1(X)$, kita sekarang harus membuktikan bahwa setiap homotopi berujung
tetap $H\colon I^2\to X$ dari lintasan $\gamma$ ke lintasan $\eta$ memenuhi

$$
\widetilde K_1(\gamma)=\widetilde K_1(\eta).
$$

Langkah berikut menyiapkan kesamaan lokal yang kelak akan ditempelkan untuk
membuktikan pernyataan tersebut.

### Pemanasan: dua lintasan batas sebuah persegi {#o012-rbt-l11-proof-square-warmup}

Ambil pemetaan sebarang

$$
h\colon I^2\longrightarrow X.
$$

Definisikan dua lintasan dari $h(0,0)$ ke $h(1,1)$:

$$
\begin{aligned}
\gamma_0&:=h(-,0)\#h(1,-),\\
\gamma_1&:=h(0,-)\#h(-,1).
\end{aligned}
$$

Lintasan pertama menempuh sisi bawah lalu sisi kanan persegi; lintasan kedua
menempuh sisi kiri lalu sisi atas.

::: {.figure #o012-rbt-l11-fig-010}
**Diagram 11.10 (dua rute batas).** Di dalam persegi koordinat $I^2$, kedua
rute sebelum diterapkan $h$ diparameterkan oleh

$$
p_0(s)=
\begin{cases}
(2s,0),&0\leq s\leq\tfrac12,\\
(1,2s-1),&\tfrac12\leq s\leq1,
\end{cases}
$$

dan

$$
p_1(s)=
\begin{cases}
(0,2s),&0\leq s\leq\tfrac12,\\
(2s-1,1),&\tfrac12\leq s\leq1.
\end{cases}
$$

Jadi $\gamma_0=h\circ p_0$ dan $\gamma_1=h\circ p_1$. Kedua rute berawal
di $(0,0)$ dan berakhir di $(1,1)$.
:::

Terdapat homotopi berujung tetap $\gamma_0\simeq\gamma_1$. Cukup membangun
homotopi berujung tetap antara $p_0$ dan $p_1$ di $I^2$, lalu
mengomposisikannya dengan $h$.

::: {.figure #o012-rbt-l11-fig-011}
**Diagram 11.11 (deformasi kedua rute).** Pengganti parametrik bagi keluarga
garis pada gambar sumber adalah

$$
P(s,u):=(1-u)p_0(s)+u p_1(s),
\qquad (s,u)\in I^2.
$$

Karena $I^2$ konveks, $P(s,u)$ selalu berada di $I^2$. Selain itu,

$$
P(s,0)=p_0(s),
\qquad
P(s,1)=p_1(s),
$$

serta kedua sisi parameter ujung tetap konstan:

$$
P(0,u)=(0,0),
\qquad
P(1,u)=(1,1).
$$

Jadi $h\circ P$ adalah homotopi berujung tetap yang diminta. Pada tiap
$u$, rutenya bergerak melalui persegi sambil mempertahankan kedua simpul
ujung; inilah fungsi matematis gambar deformasi dalam sumber.
:::

Jika $h$ mempunyai citra seluruhnya di salah satu dari $U$ atau $V$, homotopi
tersebut juga berada di subruang itu. Maka

$$
[\gamma_0]=[\gamma_1]
$$

di $\Pi_1(U)$ atau $\Pi_1(V)$ yang sesuai, sehingga

$$
\widetilde K_1(\gamma_0)=\widetilde K_1(\gamma_1).
$$

Sampai batas Kuliah 11, inilah langkah lokal yang telah dibuktikan. Untuk
homotopi umum $H\colon I^2\to X$, masih harus dipilih kisi kecil yang setiap
selnya dipetakan seluruhnya ke $U$ atau ke $V$, lalu kesamaan lokal di atas
harus ditempelkan sel demi sel. Kelanjutan juga harus membuktikan bahwa fungsi
yang turun ke kelas homotopi mempertahankan identitas dan komposisi, membatasi
menjadi $F$ serta $G$, dan merupakan satu-satunya fungtor dengan pembatasan
itu. Argumen global dimulai pada baris pertama Kuliah 12 dan tidak termasuk
dalam unit ini. Sumber sampai akhir buktinya menyatakan fungtorialitas dari
konstruksi, tetapi tidak menuliskan argumen keunikan $K$ secara eksplisit;
edisi harus memasok argumen itu ketika bukti ditutup.
:::

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l11-mastery}

Bagian ini menambahkan tiga pemeriksaan yang mengisi rincian universal dan
langkah lokal yang hanya dinyatakan singkat dalam sumber.

::: {.exercise #o012-rbt-l11-mcheck-001}
**Pemeriksaan penguasaan 11.1 (pemetaan keluar dari grup bebas dan produk
bebas).**

1. Diberikan unsur $k_1,\ldots,k_n$ dari grup $K$, bangun homomorfisma unik
   $\theta\colon F_n\to K$ dengan $\theta(x_i)=k_i$.
2. Diberikan $\phi\colon G\to K$ dan $\psi\colon H\to K$, jelaskan nilai
   homomorfisma universal $\kappa\colon G*H\to K$ pada sebuah kata yang
   huruf-hurufnya berasal bergantian dari $G$ dan $H$.
3. Periksa tipe kedua persamaan universal dan jelaskan mengapa
   $i\circ\kappa$ tidak dapat menggantikan $\kappa\circ i$.
:::

## Solusi Pemeriksaan 11.1 {#o012-rbt-l11-sol-001}

Untuk kata

$$
w=x_{i_1}^{\varepsilon_1}\cdots x_{i_r}^{\varepsilon_r},
\qquad
\varepsilon_j\in\{1,-1\},
$$

definisikan

$$
\theta(w)
:=
k_{i_1}^{\varepsilon_1}\cdots k_{i_r}^{\varepsilon_r}.
$$

Penyisipan atau penghapusan pasangan invers tidak mengubah nilai itu, jadi
$\theta$ terdefinisi baik pada unsur $F_n$. Konkatenasi kata dipetakan ke
perkalian di $K$, sehingga $\theta$ homomorfisma. Setiap homomorfisma dengan
nilai $x_i\mapsto k_i$ harus mempunyai rumus tersebut pada semua kata, maka
$\theta$ unik.

Untuk produk bebas, sebuah kata khas dapat ditulis

$$
g_1h_1g_2h_2\cdots g_rh_r,
$$

dengan faktor awal atau akhir boleh tidak hadir dan dengan unsur identitas
dihapus. Pemetaan universal harus memenuhi

$$
\kappa(g_1h_1\cdots g_rh_r)
=
\phi(g_1)\psi(h_1)\cdots\phi(g_r)\psi(h_r).
$$

Relasi internal $G$ dihormati karena $\phi$ homomorfisma, dan relasi internal
$H$ dihormati karena $\psi$ homomorfisma. Presentasi produk bebas tidak
menambahkan relasi silang, sehingga rumus itu menentukan homomorfisma. Ia
unik karena citra semua pembangkit dari kedua faktor sudah ditentukan.

Terakhir,

$$
i\colon G\to G*H,
\qquad
\kappa\colon G*H\to K,
$$

sehingga komposit bertipe dari $G$ ke $K$ adalah $\kappa\circ i$, dan ini
harus sama dengan $\phi$. Ekspresi $i\circ\kappa$ akan memerlukan kodomain
$\kappa$ sama dengan domain $i$, yakni $K=G$, yang tidak diberikan dan bahkan
tidak benar secara umum; sekalipun kebetulan $K=G$, domain komposit itu tetap
$G*H$, bukan domain $G$ milik $\phi$. Argumen identik memberi
$\kappa\circ j=\psi$.

::: {.exercise #o012-rbt-l11-mcheck-002}
**Pemeriksaan penguasaan 11.2 (dua verifikasi pushout).**

1. Dalam Contoh 11.1, misalkan $f\colon U\to Z$ dan $g\colon V\to Z$
   kontinu serta $f|_{U\cap V}=g|_{U\cap V}$. Bangun pemetaan universal
   $k\colon X\to Z$ dan buktikan kekontinuannya.
2. Dalam Contoh 11.5, misalkan $A\colon V_1\to Z$ dan
   $B\colon V_2\to Z$ linear serta $A\circ L_1=B\circ L_2$. Bangun pemetaan
   universal dari $(V_1\oplus V_2)/J(W)$ ke $Z$ dan buktikan bahwa ia
   terdefinisi baik serta unik.
:::

## Solusi Pemeriksaan 11.2 {#o012-rbt-l11-sol-002}

Definisikan fungsi $k\colon X=U\cup V\to Z$ dengan

$$
k(x)=
\begin{cases}
f(x),&x\in U,\\
g(x),&x\in V.
\end{cases}
$$

Kesepakatan pada $U\cap V$ membuat fungsi ini terdefinisi baik. Pembatasannya
ke sampul terbuka $\{U^\circ,V^\circ\}$ masing-masing adalah pembatasan
fungsi kontinu $f$ dan $g$. Lema perekatan untuk sampul terbuka karena itu
menunjukkan bahwa $k$ kontinu. Nilainya pada semua titik $U$ dan $V$ sudah
dipaksa oleh $f$ serta $g$, jadi $k$ unik.

Untuk ruang vektor, definisikan

$$
T\colon V_1\oplus V_2\longrightarrow Z,
\qquad
T(v_1,v_2):=A(v_1)+B(v_2).
$$

Untuk setiap $w\in W$,

$$
T(J(w))
=
A(L_1(w))-B(L_2(w))
=0.
$$

Jadi $J(W)\subseteq\ker T$, dan $T$ turun secara unik menjadi pemetaan linear

$$
\overline T\colon(V_1\oplus V_2)/J(W)\longrightarrow Z.
$$

Pemetaan itu memenuhi

$$
\overline T([(v_1,0)])=A(v_1),
\qquad
\overline T([(0,v_2)])=B(v_2).
$$

Setiap kelas $[(v_1,v_2)]$ adalah jumlah kedua jenis pembangkit tersebut,
sehingga linearitas memaksa nilai $\overline T$ pada seluruh hasil bagi.
Karena itu pemetaan universal tersebut unik.

::: {.exercise #o012-rbt-l11-mcheck-003}
**Pemeriksaan penguasaan 11.3 (subdivisi dan homotopi persegi).**

1. Buktikan langsung bahwa menyisipkan satu titik baru ke dalam partisi
   lintasan tidak mengubah $\widetilde K_1(\gamma)$.
2. Verifikasi kekontinuan rumus $P(s,u)$ pada Diagram 11.11 dan periksa semua
   syarat homotopi berujung tetap.
3. Jelaskan mengapa hasil lokal itu belum, pada batas unit ini, membuktikan
   bahwa $\widetilde K_1(\gamma)=\widetilde K_1(\eta)$ untuk setiap homotopi
   berujung tetap
   $H\colon\gamma\simeq\eta$ yang citranya melintasi kedua subruang.
:::

## Solusi Pemeriksaan 11.3 {#o012-rbt-l11-sol-003}

Misalkan satu ruas $\gamma_i$ berada dalam $U$ dan dipotong pada satu titik
menjadi $\alpha\#\beta$. Dengan konvensi komposisi aljabar, fungtorialitas
$F$ memberi

$$
F_1([\gamma_i]_U)
=
F_1([\alpha]_U[\beta]_U)
=
F_1([\alpha]_U)F_1([\beta]_U).
$$

Jadi satu faktor lama dalam produk $\widetilde K_1(\gamma)$ diganti oleh dua
faktor dengan produk yang sama. Argumen bagi ruas dalam $V$ identik. Jika ruas
berada dalam irisan, komutativitas persegi membuat pilihan $F$ atau $G$
memberi hasil yang sama. Setiap perhalusan berhingga diperoleh dengan
mengulang langkah ini, dan setiap dua partisi mempunyai perhalusan bersama;
maka hasilnya bebas dari partisi.

Fungsi $p_0$ dan $p_1$ kontinu karena kedua rumus bagi masing-masing fungsi
sepakat pada $s=\tfrac12$. Penjumlahan serta perkalian skalar di
$\mathbb R^2$ kontinu, sehingga

$$
P(s,u)=(1-u)p_0(s)+up_1(s)
$$

kontinu. Persegi $I^2$ konveks, jadi citra $P$ tetap di dalam domain $h$.
Substitusi $u=0$ dan $u=1$ memberi $p_0$ dan $p_1$, sedangkan substitusi
$s=0$ dan $s=1$ memberi titik konstan $(0,0)$ dan $(1,1)$. Dengan demikian
$h\circ P$ benar-benar homotopi berujung tetap dari $\gamma_0$ ke
$\gamma_1$.

Namun, bila citra $H$ melintasi $U$ dan $V$, tidak ada alasan bahwa seluruh
homotopi persegi berada dalam satu anggota sampul. Kesamaan kelas di satu
$\Pi_1(U)$ atau satu $\Pi_1(V)$ karena itu belum dapat diterapkan sekaligus.
Masih diperlukan bilangan Lebesgue bagi sampul prapeta pada $I^2$, kisi cukup
halus, dan penempelan kesamaan satu sel pada satu waktu. Itulah langkah yang
dimulai pada Kuliah 12. Membatasi kesimpulan di sini mencegah bagian pertama
bukti disalahartikan sebagai bukti lengkap teorema.
