---
title: "Topologi Aljabar"
subtitle: "Unit 15: Komponen Ruang Penutup, Orbit Monodromi, dan Koset Kanan"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l15-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 3210--3286 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L3210-L3286)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang itu dimulai dengan penanda Kuliah 15 dan berakhir dengan dua baris
kosong setelah pertanyaan realisasi subgrup. Kuliah 16 dimulai di tengah
berkas sumber pada baris 3287 dan tidak termasuk dalam unit ini. Materi
sumber dan adaptasi Indonesia ini tersedia di bawah [Creative Commons
Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/).

Perubahan edisi mencakup penerjemahan, pemformatan ulang agar mudah dibaca,
pemberian pengenal stabil, dan pemindahan ketiga catatan pinggir sumber ke
urutan bacaan utama. Kedua diagram Xy-pic vertikal ditulis ulang sebagai
diagram semantik yang menyebut ruang total, ruang basis, dan arah peta.
Keenam tampilan matematis sumber dipertahankan, dengan rumus peta ditambahkan
ketika sumber hanya menyatakan kesurjektifan tanpa memberi nilai unsur.

Konvensi aksi diperjelas dan diperbaiki secara menyeluruh. Karena produk loop
dalam kuliah ini dibaca kronologis, transpor serat langsung adalah **aksi
kanan**:

$$
z\mathbin{\cdot}[\gamma]=\gamma_*(z).
$$

Oleh karena itu orbit bertitik diidentifikasi dengan ruang koset kanan
$H\backslash G$, bukan $G/H$. Setiap kemunculan grup fundamental ruang total
sebagai subgrup juga diberi peta yang hilang, yakni
$\pi_*\pi_1(Z,z)\leq\pi_1(X,x_0)$. Penerapan tarik balik yang salah ketik
$\mathrm{in}_j^*X$ dikoreksi menjadi $\mathrm{in}_j^*Z$, dan bukti orbit
dilengkapi dengan identifikasi penstabil melalui kriteria pengangkatan loop
tertutup.

Konvensi SLSC mata kuliah dipertahankan: istilah itu sudah mencakup basis
lingkungan terhubung lintasan. Karena itu komponen ruang basis dan ruang total
penutup bersifat terbuka, komponen terhubung sama dengan komponen lintasan,
dan pembatasan ke setiap komponen ruang total benar-benar merupakan ruang
penutup surjektif. Indeks komponen ruang basis dan ruang total dibedakan agar
tidak bertabrakan. Catatan sumber tentang aksi bebas juga diperketat: agar
$Y\to Y/G$ menjadi peta penutup, yang diperlukan adalah aksi penutup, bukan
kebebasan saja.

Sumber menunda keberadaan ruang penutup terhubung sederhana, realisasi setiap
subgrup, dan kepenuhan-setiaan funktor monodromi. Edisi ini mempertahankan
batas logis itu. Tujuh pemeriksaan penguasaan asli edisi hanya menyelesaikan
langkah yang sudah menjadi kewajiban Unit 15: pemisahan menurut komponen,
aksi kanan, orbit, penstabil, contoh lingkaran, dan sifat torsor yang bersifat
kondisional. Materi pendamping tersedia di bawah CC BY 4.0 dan tidak meminjam
solusi eksternal. Edisi ini bersifat independen; edisi ini tidak disponsori,
didukung, disahkan, ataupun diberi status resmi oleh David Michael Roberts,
MIT, Haynes Miller, Sanath Devalapurkar, Yeheli Fomberg, Nir Lazarovich, atau
institusi mereka.

# Kuliah 15 {#o012-rbt-l15}

Kita memakai dua konvensi tetap. Pertama, hasil kali loop
$[\gamma][\eta]$ dibaca **kronologis**: $\gamma$ ditempuh dahulu, lalu
$\eta$. Kedua, bila $p\colon Z\to X$ ruang penutup dan $z\in Z_x$, transpor
langsung didefinisikan oleh

$$
z\cdot[\gamma]:=\gamma_*(z).
$$

Keunikan pengangkatan memberi

$$
(z\cdot[\gamma])\cdot[\eta]
=z\cdot([\gamma][\eta]),
$$

jadi ini aksi kanan. Untuk grup $G$, notasi $\mathbf{Set}_G$ berarti kategori
himpunan dengan aksi kanan $G$ dan pemetaan ekuivarian kanan. Dengan
konvensi ini, ruang koset $H\backslash G=\{Hg:g\in G\}$ membawa aksi kanan
$(Hg)\cdot k=H(gk)$.

## Memisahkan ruang penutup menurut komponen basis {#o012-rbt-l15-s01}

::: {.lemma #o012-rbt-l15-lem-001}
**Lema 15.1.** Jika ruang $X$ merupakan koproduk topologis

$$
X=\bigsqcup_{i\in I}X_i,
$$

maka terdapat ekuivalensi kategori

$$
\operatorname{Cov}_X
\simeq
\prod_{i\in I}\operatorname{Cov}_{X_i}.
$$
:::

::: {.proof #o012-rbt-l15-proof-001}
**Bukti.** Tuliskan
$\mathrm{in}_j\colon X_j\to\bigsqcup_{i\in I}X_i$ untuk inklusi. Ruang
penutup $p\colon Z\to X$ memberi ruang penutup hasil tarik balik

$$
Z_{X_j}
:=\mathrm{in}_j^*Z
=X_j\times_X Z
\longrightarrow X_j
$$

untuk setiap $j\in I$. Pemetaan ruang penutup $f\colon Z\to Z'$ di atas
$X$ membatasi menjadi pemetaan
$f|_{X_j}\colon Z_{X_j}\to Z'_{X_j}$ di atas $X_j$. Jadi diperoleh funktor

$$
R\colon\operatorname{Cov}_X
\longrightarrow
\prod_{i\in I}\operatorname{Cov}_{X_i}.
$$

Sebaliknya, dari keluarga ruang penutup $p_i\colon Z_i\to X_i$ diperoleh
ruang penutup

$$
\bigsqcup_{i\in I}Z_i
\longrightarrow
\bigsqcup_{i\in I}X_i.
$$

Koproduk pemetaan $Z_i\to Z'_i$ memberi pemetaan ruang penutup di atas
$X$. Ini mendefinisikan funktor $C$ dalam arah sebaliknya.

Tarik balik koproduk $\bigsqcup_i Z_i$ ke $X_j$ secara kanonik isomorfik
dengan $Z_j$, sehingga $RC\cong\mathrm{id}$. Di arah lain, himpunan terbuka
$p^{-1}(X_i)$ membentuk partisi $Z$, dan pemetaan kanonik
$\bigsqcup_i p^{-1}(X_i)\to Z$ adalah homeomorfisme di atas $X$; maka
$CR\cong\mathrm{id}$. Kedua isomorfisme itu natural pada pemetaan ruang
penutup. Jadi $R$ dan $C$ merupakan ekuivalensi kategori.
:::

Funktor serat dari Unit 14---antarmuka masuknya bernama stabil
`o012-rbt-l14-eq-fibre-functor`---karenanya memfaktor sebagai

$$
\operatorname{Cov}_X
\xrightarrow{\ \simeq\ }
\prod_{i\in I}\operatorname{Cov}_{X_i}
\longrightarrow
\prod_{i\in I}\mathbf{Set}_{\pi_1(X_i,a_i)}.
$$

::: {.diagram #o012-rbt-l15-dia-001}
**Diagram 15.1 (objek sebelum pembatasan).** Data awal adalah satu panah
vertikal

$$
\begin{array}{c}
Z\\[-2pt]
\downarrow p\\[-2pt]
X.
\end{array}
$$

Panah mengarah dari ruang total $Z$ ke ruang basis $X$.
:::

::: {.diagram #o012-rbt-l15-dia-002}
**Diagram 15.2 (keluarga sesudah pembatasan).** Untuk setiap $i\in I$, data
hasil pembatasan adalah panah vertikal

$$
\begin{array}{c}
Z_{X_i}=X_i\times_XZ\\[-2pt]
\downarrow p_i\\[-2pt]
X_i.
\end{array}
$$

Tahap berikutnya mengambil serat $(Z_{X_i})_{a_i}=Z_{a_i}$ beserta aksi
kanan langsung $\pi_1(X_i,a_i)$ pada serat itu. Jadi pemetaan objek lengkapnya
adalah

$$
(Z\to X)
\longmapsto
(Z_{X_i}\to X_i)_{i\in I}
\longmapsto
\bigl(Z_{a_i},\rho_i\bigr)_{i\in I},
$$

dengan $\rho_i$ ditentukan oleh
$z\cdot[\gamma]=\gamma_*(z)$.
:::

Karena itu, jika setiap funktor
$\operatorname{Cov}_{X_i}\to\mathbf{Set}_{\pi_1(X_i,a_i)}$ dipahami, maka
kasus umum juga dipahami komponen demi komponen.

## Komponen terhubung dan contoh lingkaran {#o012-rbt-l15-s02}

Mulai sekarang, anggap $X$ terhubung dan SLSC dalam konvensi mata kuliah,
serta pilih $x_0\in X$. Karena SLSC mencakup basis lingkungan terhubung
lintasan, $X$ terhubung lintasan. Untuk $z\in Z$, pilih lingkungan $W$ dari
$p(z)$ yang diliputi secara merata, lalu pilih lingkungan basis terhubung
lintasan $U$ dengan $p(z)\in U\subseteq W$. Pembatasan lembar-lembar di atas
$W$ ke $U$ memberi basis lingkungan terhubung lintasan pada $Z$. Jadi $Z$
terhubung lintasan lokal, komponen terhubungnya sama dengan komponen
lintasannya, dan setiap komponen bersifat terbuka.

Dengan $J$ sebagai himpunan indeks komponen ruang total, tuliskan

$$
Z=\bigsqcup_{\alpha\in J}Z_\alpha.
$$

Setiap pembatasan $p_\alpha\colon Z_\alpha\to X$ merupakan ruang penutup
terhubung. Memang, di sekitar setiap $x\in X$ pilih lingkungan terhubung
lintasan $U$ yang diliputi secara merata. Setiap lembar di atas $U$ terhubung
lintasan, sehingga seluruh lembar itu terletak dalam tepat satu komponen ruang
total. Akibatnya $p^{-1}(U)\cap Z_\alpha$ merupakan gabungan lembar-lembar
utuh, dan $U$ diliputi secara merata oleh pembatasan tersebut. Untuk
kesurjektifan, pilih $u\in Z_\alpha$. Bagi $x\in X$, pilih lintasan dari
$p(u)$ ke $x$ dan angkat lintasan itu mulai dari $u$. Seluruh pengangkatan
berada di $Z_\alpha$, sehingga titik akhirnya terletak di atas $x$.

::: {.remark #o012-rbt-l15-rem-001}
**Catatan 15.1 (hipotesis yang dipakai).** Sumber menempatkan dua catatan di
pinggir pada langkah ini: satu menyebut perlunya basis lingkungan terhubung
lintasan dan satu lagi menandai dekomposisi komponen sebagai latihan. Dalam
konvensi mata kuliah, syarat basis itu sudah menjadi bagian definisi SLSC;
argumen pada paragraf sebelumnya menyelesaikan latihan tersebut. Jika istilah
“terhubung sederhana semilokal” dipakai dalam arti standar yang lebih lemah,
keterhubungan lintasan lokal harus ditambahkan sebagai hipotesis terpisah.
Antarmuka masuk dari Unit 14 untuk fakta ini bernama stabil
`o012-rbt-l14-rem-001`.
:::

::: {.example #o012-rbt-l15-exa-001}
**Contoh 15.1 (ruang penutup lingkaran yang telah dikenal).** Ambil
$X=S^1$. Untuk ruang diskret $F$, ada ruang penutup trivial

$$
S^1\times F
\cong
\bigsqcup_{f\in F}S^1
\longrightarrow S^1.
$$

Ada pula peta eksponensial

$$
\mathbb R\longrightarrow S^1,
\qquad
t\longmapsto e^{2\pi it},
$$

dan, untuk setiap $n>1$, ruang penutup

$$
q_n\colon S^1_n\longrightarrow S^1,
\qquad
q_n(z)=z^n.
$$

Subskrip pada $S^1_n$ mengingatkan kita pada petanya; ruang totalnya sendiri
homeomorfik dengan $S^1$. Kita dapat mengambil gabungan saling lepas dengan
banyak salinan yang sebarang. Jika $A_\infty$ mengindeks salinan penutup
eksponensial dan $A_n$ mengindeks salinan penutup derajat $n$, salah satu
bentuk umumnya adalah

$$
S^1\times F
\;\sqcup\;
\bigsqcup_{\alpha\in A_\infty}\mathbb R_\alpha
\;\sqcup\;
\bigsqcup_{n\geq2}\ \bigsqcup_{\beta\in A_n}S^1_{n,\beta}
\longrightarrow S^1.
$$

Pada titik ini masih harus ditentukan apakah ada ruang penutup $S^1$ yang
tidak isomorfik dengan bentuk tersebut. Unit ini mempertahankan pertanyaan
itu sebagai hasil yang ditunda.
:::

## Orbit serat dan koset kanan {#o012-rbt-l15-s03}

Ambil ruang penutup $p\colon Z\to X$ dan dekomposisi
$Z=\bigsqcup_{\alpha\in J}Z_\alpha$ di atas. Pilih

$$
z_\alpha\in Z_{x_0}\cap Z_\alpha
$$

untuk setiap $\alpha\in J$; titik semacam itu ada karena
$Z_\alpha\to X$ surjektif. Hasil dari Kuliah 6 memberi peta surjektif

$$
\Omega_{x_0}X\times\{z_\alpha:\alpha\in J\}
\longrightarrow Z_{x_0},
\qquad
(\gamma,z_\alpha)
\longmapsto
\widetilde\gamma_{z_\alpha}(1).
$$

Peta ini hanya bergantung pada kelas homotopi loop yang mempertahankan titik
ujung. Karena itu ia turun menjadi peta surjektif

$$
\begin{aligned}
\pi_1(X,x_0)\times\{z_\alpha:\alpha\in J\}
&\cong
\bigsqcup_{\alpha\in J}
\pi_1(X,x_0)\times\{z_\alpha\}\\
&\longrightarrow
Z_{x_0}
=
\bigsqcup_{\alpha\in J}
(Z_{x_0}\cap Z_\alpha),\\
([\gamma],z_\alpha)
&\longmapsto
z_\alpha\cdot[\gamma].
\end{aligned}
$$

::: {.lemma #o012-rbt-l15-lem-002}
**Lema 15.2 (komponen adalah orbit).** Di bawah asumsi tetap bahwa $X$
terhubung dan SLSC, letakkan

$$
G:=\pi_1(X,x_0),
\qquad
H_\alpha:=
(p_\alpha)_*\pi_1(Z_\alpha,z_\alpha)
\leq G.
$$

Untuk setiap pilihan $z_\alpha\in Z_{x_0}\cap Z_\alpha$, terdapat
isomorfisme himpunan-$G$ kanan

$$
Z_{x_0}
=
\bigsqcup_{\alpha\in J}(Z_{x_0}\cap Z_\alpha)
\cong
\bigsqcup_{\alpha\in J}H_\alpha\backslash G.
$$
:::

::: {.proof #o012-rbt-l15-proof-002}
**Bukti.** Pertama kita identifikasi orbit. Jika
$z\in Z_{x_0}\cap Z_\alpha$, keterhubungan lintasan $Z_\alpha$ memberi
lintasan $\delta\colon z_\alpha\rightsquigarrow z$. Proyeksinya
$p\circ\delta$ adalah loop di $x_0$, dan pengangkatan uniknya mulai dari
$z_\alpha$ adalah $\delta$. Jadi

$$
z_\alpha\cdot[p\circ\delta]=z.
$$

Maka $Z_{x_0}\cap Z_\alpha$ termuat dalam orbit $z_\alpha$. Sebaliknya,
jika $z=z_\alpha\cdot[\eta]$, pengangkatan $\eta$ mulai dari $z_\alpha$
merupakan lintasan di $Z$ dari $z_\alpha$ ke $z$. Jadi $z$ berada di
komponen $Z_\alpha$. Dengan demikian orbit $z_\alpha$ tepat
$Z_{x_0}\cap Z_\alpha$.

Sekarang kita identifikasi penstabil. Kelas $[\eta]\in G$ menetapkan
$z_\alpha$ tepat ketika pengangkatan $\eta$ mulai dari $z_\alpha$ berakhir
kembali di $z_\alpha$. Dalam hal itu pengangkatannya adalah loop di
$Z_\alpha$, sehingga

$$
[\eta]\in(p_\alpha)_*\pi_1(Z_\alpha,z_\alpha)=H_\alpha.
$$

Sebaliknya, proyeksi setiap loop di $(Z_\alpha,z_\alpha)$ jelas terangkat
kembali ke loop tersebut, sehingga kelas proyeksinya menetapkan
$z_\alpha$. Jadi

$$
\operatorname{Stab}_G(z_\alpha)=H_\alpha.
$$

Akhirnya, peta orbit

$$
H_\alpha g
\longmapsto
z_\alpha\cdot g
$$

terdefinisi baik, bijektif, dan ekuivarian kanan. Mengambil gabungan saling
lepas atas semua $\alpha$ memberi isomorfisme yang dinyatakan.
:::

Akibatnya, funktor
$\operatorname{Cov}_X\to\mathbf{Set}_G$ mempertahankan gabungan saling
lepas: ruang penutup $\bigsqcup_{\alpha\in J}Z_\alpha\to X$ dikirim ke
gabungan saling lepas orbit

$$
\bigsqcup_{\alpha\in J}(Z_{x_0}\cap Z_\alpha).
$$

::: {.remark #o012-rbt-l15-rem-002}
**Catatan 15.2 (aksi sebagai keluarga aksi transitif).** Jika himpunan-$G$
kanan $S$ terurai menjadi orbit

$$
S=\bigsqcup_{\alpha\in J}S_\alpha,
$$

maka setiap operator $\rho_g(s):=s\cdot g$ mempertahankan setiap
$S_\alpha$. Karena itu semua operator aksi berada dalam subgrup

$$
\prod_{\alpha\in J}\operatorname{Aut}(S_\alpha)
\leq
\operatorname{Aut}\!\left(
\bigsqcup_{\alpha\in J}S_\alpha
\right).
$$

Dengan kata lain, aksi itu tepat keluarga
$(\rho_\alpha)_{\alpha\in J}$ dari aksi kanan transitif pada
$S_\alpha$. Dalam notasi operator, hukum aksi kanan berbunyi
$\rho_{gh}=\rho_h\circ\rho_g$; ekuivalen dengan sebuah funktor
$G^{\mathrm{op}}\to\mathbf{Set}$.
:::

## Reduksi ke ruang penutup terhubung dan aksi transitif {#o012-rbt-l15-s04}

Ingat pertanyaan asalnya: representasi grupoid fundamental mana yang berasal
dari ruang penutup? Setelah reduksi menurut komponen basis dan orbit, untuk
$X$ terhubung kita dapat membandingkan dua subkategori penuh:

- $\operatorname{Cov}_X^{\mathrm{conn}}$, ruang penutup dengan ruang total
  terhubung;
- $\mathbf{Set}_G^{\mathrm{tr}}$, himpunan-$G$ kanan dengan aksi transitif.

Lema 15.2 menunjukkan bahwa funktor monodromi membatasi menjadi

$$
\operatorname{Cov}_X^{\mathrm{conn}}
\longrightarrow
\mathbf{Set}_G^{\mathrm{tr}}.
$$

Setiap ruang penutup merupakan gabungan saling lepas komponen terhubungnya,
dan setiap himpunan-$G$ merupakan gabungan saling lepas orbitnya. Karena itu,
untuk menentukan **objek** mana yang berada dalam citra esensial funktor
monodromi, cukup ditanyakan apakah setiap himpunan-$G$ kanan transitif berasal
dari suatu ruang penutup terhubung. Reduksi ini belum membuktikan bahwa
funktor penuh atau setia pada morfisme.

Sekarang ambil himpunan-$G$ kanan transitif $S$ dan titik $p\in S$. Grup $G$
sendiri, dengan aksi perkalian kanan, bebas dan transitif. Peta orbit

$$
\begin{aligned}
G&\longrightarrow
S\cong\operatorname{Stab}(p)\backslash G,\\
g&\longmapsto p\cdot g
\end{aligned}
$$

surjektif dan ekuivarian kanan. Secara lebih umum, jika $T$ adalah
himpunan-$G$ kanan dengan aksi bebas dan transitif, pilih $t_0\in T$ dan
definisikan

$$
t_0\cdot g\longmapsto p\cdot g.
$$

Karena aksi pada $T$ bebas dan transitif, setiap unsur $T$ mempunyai bentuk
$t_0\cdot g$ secara unik. Jadi rumus itu memberi peta ekuivarian surjektif
$T\to S$. Pilihan $t_0$ membuat peta ini tidak kanonik.

::: {.example #o012-rbt-l15-exa-002}
**Contoh 15.2 (serat penutup terhubung sederhana).** Misalkan telah diberikan
ruang penutup terhubung sederhana $p\colon Z\to X$. Serat $Z_{x_0}$ adalah
himpunan-$G$ kanan yang bebas dan transitif.

Transitivitas mengikuti dari keterhubungan lintasan $Z$: lintasan antara dua
titik serat memproyeksi menjadi loop yang mentranspor titik pertama ke titik
kedua. Jika $[\gamma]$ menetapkan $z\in Z_{x_0}$, pengangkatannya mulai dari
$z$ adalah loop di $Z$. Karena $Z$ terhubung sederhana, proyeksi loop itu
trivial di $G$; jadi aksi bebas. Pernyataan ini bersifat kondisional: Unit 15
belum membangun atau membuktikan keberadaan ruang penutup seperti itu.
:::

## Pertanyaan realisasi subgrup {#o012-rbt-l15-s05}

Untuk ruang penutup terhubung lintasan $p\colon Z\to X$ dan
$z\in Z_{x_0}$, Lema 15.2 memberi isomorfisme himpunan-$G$ kanan

$$
Z_{x_0}
\cong
p_*\pi_1(Z,z)\backslash\pi_1(X,x_0).
$$

Jika ruang penutupnya bertitik, titik $z$ sudah menjadi bagian data sehingga
tidak perlu dipilih lagi. Sebaliknya, setiap ruang penutup terhubung dari
ruang bertitik dapat dijadikan bertitik dengan memilih satu titik di atas
$x_0$; melupakan titik itu mengembalikan ruang penutup semula.

::: {.question #o012-rbt-l15-q-001}
**Pertanyaan 15.1 (pertanyaan akhir sumber).** Diberikan subgrup

$$
H<\pi_1(X,x_0),
$$

adakah ruang penutup bertitik

$$
p\colon(Z,z_0)\longrightarrow(X,x_0)
$$

sedemikian sehingga

$$
p_*\pi_1(Z,z_0)=H
$$

sebagai subgrup dari $\pi_1(X,x_0)$?
:::

Catatan pinggir sumber mengingat kembali contoh terdahulu: jika ruang
terhubung sederhana $Y$ membawa aksi penutup bebas oleh $G$, maka
$Y\to Y/G$ adalah ruang penutup dan, setelah memilih titik basis yang
sesuai, $\pi_1(Y/G,*)\cong G$. Hipotesis “aksi penutup” penting; aksi bebas
topologis semata belum menjamin peta hasil bagi merupakan peta penutup.

::: {.note #o012-rbt-l15-note-001 data-origin="edition-original"}
**Batas hasil Unit 15.** Pertanyaan 15.1 sengaja belum dijawab di sini.
Kuliah 16, yang mulai pada `Notes.tex:3287`, akan mencoba membangun ruang
penutup terhubung sederhana dan mengambil hasil baginya oleh subgrup. Unit 15
juga belum membuktikan bahwa semua pemetaan ekuivarian serat berasal dari
pemetaan ruang penutup; jadi kepenuhan, kesetiaan, dan ekuivalensi kategori
tetap merupakan hasil kemudian.
:::

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l15-mastery}

Tujuh pemeriksaan berikut adalah materi asli edisi. Semuanya terbatas pada
hasil yang telah tersedia di Unit 15. Tidak satu pun mengasumsikan atau
membuktikan keberadaan ruang penutup universal, realisasi subgrup umum, atau
kepenuhan-setiaan funktor monodromi.

::: {.exercise #o012-rbt-l15-mcheck-001 data-origin="edition-original"}
**Pemeriksaan penguasaan 15.1 (ekuivalensi pada koproduk).** Definisikan
kedua funktor pada Lema 15.1, termasuk tindakannya pada morfisme, lalu tulis
isomorfisme natural yang menunjukkan bahwa keduanya saling invers hingga
isomorfisme.
:::

## Solusi Pemeriksaan 15.1 {#o012-rbt-l15-sol-001}

Funktor pembatasan adalah

$$
R(Z\xrightarrow{p}X)
=
\bigl(X_i\times_XZ\to X_i\bigr)_{i\in I},
$$

dan pada morfisme $f\colon Z\to Z'$ ia memakai
$\mathrm{id}_{X_i}\times_Xf$. Funktor koproduk adalah

$$
C((Z_i\to X_i)_i)
=
\left(\bigsqcup_iZ_i\to\bigsqcup_iX_i\right),
$$

dan pada morfisme ia mengambil koproduk semua pemetaan komponen.

Untuk keluarga $(Z_i\to X_i)_i$, tarik balik koproduknya ke $X_j$ hanya
menyisakan $Z_j$, sehingga komponen isomorfisme natural
$RC\Rightarrow\mathrm{id}$ adalah

$$
X_j\times_X\left(\bigsqcup_iZ_i\right)
\xrightarrow{\ \cong\ }Z_j.
$$

Untuk $Z\to X$, komponen isomorfisme natural
$CR\Rightarrow\mathrm{id}$ adalah

$$
\bigsqcup_i(X_i\times_XZ)
\longrightarrow Z,
\qquad
(x,z)\longmapsto z.
$$

Ia bijektif dan merupakan homeomorfisme karena $X_i$ terbuka dan tertutup
dalam koproduk, sehingga $p^{-1}(X_i)$ juga terbuka dan tertutup dalam $Z$.
Kedua rumus jelas berkomutasi dengan morfisme ruang penutup; jadi keduanya
natural.

::: {.exercise #o012-rbt-l15-mcheck-002 data-origin="edition-original"}
**Pemeriksaan penguasaan 15.2 (komponen ruang total).** Misalkan $X$
terhubung dan SLSC serta $p\colon Z\to X$ ruang penutup. Buktikan bahwa
setiap komponen terhubung $Z_\alpha$ terbuka, terhubung lintasan, dan bahwa
$p|_{Z_\alpha}\colon Z_\alpha\to X$ merupakan ruang penutup surjektif.
:::

## Solusi Pemeriksaan 15.2 {#o012-rbt-l15-sol-002}

Konvensi SLSC memberi basis lingkungan terbuka terhubung lintasan pada $X$.
Untuk $z\in Z$, pilih lingkungan $W$ dari $p(z)$ yang diliputi secara merata,
lalu ambil lingkungan basis terhubung lintasan $U$ dengan
$p(z)\in U\subseteq W$. Pembatasan setiap lembar di atas $W$ ke $U$
homeomorfik dengan $U$. Lembar-lembar semacam itu membentuk basis lingkungan
terhubung lintasan pada $Z$. Maka $Z$ terhubung lintasan lokal; komponen
terhubungnya terbuka dan sama dengan komponen lintasannya.

Sekarang, di sekitar setiap $x\in X$, pilih $U$ yang sekaligus terhubung
lintasan dan diliputi secara merata. Setiap lembar di atas $U$ terhubung
lintasan, jadi termuat dalam tepat satu komponen $Z_\alpha$. Dengan demikian
$p^{-1}(U)\cap Z_\alpha$ adalah gabungan lembar-lembar utuh; ini membuktikan
bahwa $p|_{Z_\alpha}$ merupakan peta penutup ke citranya. Untuk menunjukkan
citranya seluruh $X$, pilih $u\in Z_\alpha$. Karena $X$ terhubung dan
terhubung lintasan lokal, $X$ terhubung lintasan. Bagi $x\in X$, pilih
lintasan dari $p(u)$ ke $x$. Pengangkatannya mulai dari $u$ tetap berada dalam
komponen lintasan $Z_\alpha$ dan berakhir di atas $x$. Jadi pembatasan itu
surjektif dan merupakan ruang penutup terhubung.

::: {.exercise #o012-rbt-l15-mcheck-003 data-origin="edition-original"}
**Pemeriksaan penguasaan 15.3 (aksi pada contoh lingkaran).** Dengan
$\pi_1(S^1,1)\cong\mathbb Z$, hitung aksi kanan pada serat penutup trivial,
penutup eksponensial, dan penutup $q_n(z)=z^n$. Tentukan penstabil dan orbit
masing-masing. Jelaskan apa yang belum dibuktikan oleh perhitungan ini.
:::

## Solusi Pemeriksaan 15.3 {#o012-rbt-l15-sol-003}

Tuliskan unsur grup sebagai $m\in\mathbb Z$, dengan penjumlahan kronologis.
Pada satu komponen penutup trivial $S^1\to S^1$, seratnya satu titik dan
setiap $m$ menetapkannya. Penstabilnya seluruh $\mathbb Z$, sehingga orbitnya

$$
\mathbb Z\backslash\mathbb Z
$$

adalah satu titik. Faktor diskret $F$ hanya memberi satu orbit semacam ini
untuk setiap $f\in F$.

Untuk penutup eksponensial, identifikasi serat di atas $1$ dengan
$\mathbb Z$. Pengangkatan loop berderajat $m$ mengirim

$$
k\cdot m=k+m.
$$

Aksi ini bebas dan transitif; penstabil $0$, dan orbitnya
$\{0\}\backslash\mathbb Z\cong\mathbb Z$.

Untuk $q_n$, serat diidentifikasi dengan $\mathbb Z/n\mathbb Z$, dan

$$
[k]\cdot m=[k+m].
$$

Penstabil $[0]$ adalah $n\mathbb Z$, sehingga orbitnya
$n\mathbb Z\backslash\mathbb Z\cong\mathbb Z/n\mathbb Z$. Gabungan saling
lepas penutup memberi gabungan saling lepas orbit-orbit tersebut.

Perhitungan ini menentukan monodromi semua contoh yang telah ditampilkan,
tetapi sampai baris 3239 pada sumber belum dibuktikan bahwa setiap ruang
penutup $S^1$ harus muncul dalam daftar. Klaim kelengkapan memerlukan argumen
klasifikasi tambahan.

::: {.exercise #o012-rbt-l15-mcheck-004 data-origin="edition-original"}
**Pemeriksaan penguasaan 15.4 (mengapa koset kanan).** Misalkan $S$ adalah
himpunan-$G$ kanan transitif, $p\in S$, dan
$H=\operatorname{Stab}_G(p)$. Buktikan langsung bahwa

$$
H\backslash G\longrightarrow S,
\qquad
Hg\longmapsto p\cdot g
$$

adalah isomorfisme himpunan-$G$ kanan. Tunjukkan pula mengapa $G/H$ tidak
membawa rumus yang sama tanpa mengubah konvensi aksi.
:::

## Solusi Pemeriksaan 15.4 {#o012-rbt-l15-sol-004}

Jika $Hg'=Hg$, ada $h\in H$ dengan $g'=hg$. Karena $p\cdot h=p$,

$$
p\cdot g'
=p\cdot(hg)
=(p\cdot h)\cdot g
=p\cdot g,
$$

jadi peta terdefinisi baik. Ia surjektif karena aksi transitif. Jika
$p\cdot g'=p\cdot g$, aksi kanan dengan $g^{-1}$ memberi

$$
p\cdot(g'g^{-1})=p,
$$

sehingga $g'g^{-1}\in H$ dan $Hg'=Hg$; jadi peta injektif. Ekuivariansinya
mengikuti dari

$$
(Hg)\cdot k=H(gk)
\longmapsto
p\cdot(gk)=(p\cdot g)\cdot k.
$$

Sebaliknya, $G/H$ terdiri atas koset kiri $gH$. Perkalian kanan
$gH\mapsto gkH$ tidak terdefinisi baik untuk subgrup umum karena mengganti
wakil $g$ dapat mengubah koset hasil. Ruang $G/H$ sesuai secara langsung
dengan aksi **kiri**. Konversi melalui invers memang mungkin, tetapi itu
merupakan konvensi tambahan dan bukan transpor serat langsung yang dipakai
di unit ini.

::: {.exercise #o012-rbt-l15-mcheck-005 data-origin="edition-original"}
**Pemeriksaan penguasaan 15.5 (penstabil dan pengangkatan tertutup).** Untuk
ruang penutup terhubung $p\colon(Z,z)\to(X,x_0)$, buktikan

$$
\operatorname{Stab}_{\pi_1(X,x_0)}(z)
=p_*\pi_1(Z,z).
$$
:::

## Solusi Pemeriksaan 15.5 {#o012-rbt-l15-sol-005}

Kelas loop $[\gamma]$ berada dalam penstabil $z$ tepat ketika

$$
z\cdot[\gamma]=z.
$$

Menurut definisi transpor, ini berarti pengangkatan unik
$\widetilde\gamma_z$ berawal dan berakhir di $z$, jadi merupakan loop di
$(Z,z)$. Proyeksinya adalah $\gamma$, sehingga
$[\gamma]\in p_*\pi_1(Z,z)$.

Sebaliknya, jika $[\gamma]=p_*[\delta]=[p\circ\delta]$ untuk suatu loop
$\delta$ di $(Z,z)$, maka transpor hanya bergantung pada kelas homotopi dan

$$
z\cdot[\gamma]
=z\cdot[p\circ\delta]
=z,
$$

sebab $\delta$ adalah pengangkatan $p\circ\delta$ yang mulai sekaligus
berakhir di $z$. Kedua inklusi terbukti.

::: {.exercise #o012-rbt-l15-mcheck-006 data-origin="edition-original"}
**Pemeriksaan penguasaan 15.6 (torsor serat, secara kondisional).** Andaikan
ruang penutup terhubung sederhana $p\colon Z\to X$ **sudah diberikan**.
Buktikan bahwa $Z_{x_0}$ adalah himpunan-$G$ kanan bebas dan transitif tanpa
membuktikan keberadaan ruang penutup tersebut.
:::

## Solusi Pemeriksaan 15.6 {#o012-rbt-l15-sol-006}

Karena “terhubung sederhana” mencakup keterhubungan lintasan, bagi
$z,z'\in Z_{x_0}$ ada lintasan $\delta\colon z\rightsquigarrow z'$ di $Z$.
Proyeksi $p\circ\delta$ adalah loop di $x_0$, dan keunikan pengangkatan
memberi

$$
z\cdot[p\circ\delta]=z'.
$$

Jadi aksi transitif.

Menurut Pemeriksaan 15.5,

$$
\operatorname{Stab}_G(z)=p_*\pi_1(Z,z).
$$

Karena $Z$ terhubung sederhana, grup pada ruas kanan trivial. Semua
penstabil trivial, jadi aksi bebas. Argumen ini hanya membuktikan sifat serat
**jika** penutup terhubung sederhana tersedia; ia tidak membangun penutup
tersebut.

::: {.exercise #o012-rbt-l15-mcheck-007 data-origin="edition-original"}
**Pemeriksaan penguasaan 15.7 (audit batas logis).** Putuskan mana dari
pernyataan berikut yang sudah dibuktikan pada akhir Unit 15 dan mana yang
masih ditunda:

1. ruang penutup terurai menjadi gabungan saling lepas penutup terhubung;
2. serat penutup terhubung adalah aksi transitif;
3. setiap aksi transitif direalisasikan oleh penutup terhubung;
4. setiap subgrup direalisasikan sebagai $p_*\pi_1(Z,z)$;
5. funktor monodromi surjektif secara esensial;
6. funktor monodromi penuh dan setia;
7. jika penutup terhubung sederhana diberikan, seratnya bebas dan transitif.
:::

## Solusi Pemeriksaan 15.7 {#o012-rbt-l15-sol-007}

Pernyataan 1 sudah dibuktikan dengan keterhubungan lintasan lokal ruang total
dan pengangkatan lintasan. Pernyataan 2 adalah isi Lema 15.2 untuk satu
komponen. Pernyataan 7 adalah Contoh 15.2 dan Pemeriksaan 15.6; sifatnya
kondisional pada keberadaan penutup terhubung sederhana.

Pernyataan 3 belum dibuktikan. Unit ini hanya mereduksi masalah objek umum
ke masalah aksi transitif. Pernyataan 4 tepat Pertanyaan 15.1, jadi masih
terbuka pada batas unit. Karena 3 dan 4 belum diselesaikan, pernyataan 5 juga
belum diperoleh. Pernyataan 6 merupakan masalah morfisme yang berbeda:
bahkan setelah semua objek direalisasikan, masih harus dibuktikan bahwa
setiap pemetaan ekuivarian berasal dari tepat satu pemetaan ruang penutup.
Jadi 6 pun ditunda.

Ringkasnya, Unit 15 menyelesaikan dekomposisi dan identifikasi orbit, lalu
merumuskan masalah realisasi yang tepat. Ia tidak melompati konstruksi ruang
penutup universal atau bagian morfisme dari teorema klasifikasi.
