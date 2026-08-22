---
title: "Topologi Aljabar"
subtitle: "Unit 5: Tarik Balik, Trivialisasi Interval, dan Pengangkatan Lintasan"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l05-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic Topology* karya David Michael Roberts (2019), tepatnya [`Notes.tex` baris 1132--1304 pada commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex). Rentang itu dimulai dengan penanda Kuliah 5 dan bukti pertama bagi Proposisi 4.3, lalu berakhir dengan invariansi transpor serat terhadap reparameterisasi lintasan. Baris 1305 memulai Kuliah 6 dan tidak termasuk dalam unit ini. Karya sumber tersedia di bawah [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah dibaca, pemberian pengenal stabil, serta pemindahan keterangan dari catatan pinggir ke badan teks. Beberapa koreksi dan klarifikasi matematis terbatas juga diterapkan: sampul pada bukti serat diganti dengan subdivisi interval yang tunduk pada sampul trivial; notasi ruang penutup bertitik diperbaiki; konvensi serat kosong dan ketergantungan identifikasi pada pilihan dijelaskan; morfisme kategori ruang penutup dinyatakan lengkap; contoh analisis kompleks dibatasi pada klaim monodromi yang memang didukung; argumen trivialisasi interval memakai rantai subinterval dan lema penempelan; trivialisasi dinormalisasi pada serat awal; kesalahan tipe pada fungsi transisi diperbaiki; serta notasi dan bukti keunikan pengangkatan diperjelas. Semua perubahan substantif tersebut merupakan bagian dari adaptasi, bukan kutipan dari sumber lain.

Sumber tidak memuat lingkungan latihan dalam rentang ini. Karena itu, bagian pendamping penguasaan di akhir unit menambahkan empat pemeriksaan penguasaan beserta solusi lengkap, juga bukti bagi lema kekompakan dan proposisi tarik balik yang tidak dibuktikan dalam sumber. Seluruh materi baru itu tersedia di bawah CC BY 4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

# Kuliah 5 {#o012-rbt-l05}

## Serat ruang penutup di sepanjang lintasan {#o012-rbt-l05-s01}

Kita mulai dengan bukti pertama bagi pernyataan terakhir Unit 4.

::: {.proof #o012-rbt-l05-proof-001}
**Bukti pertama Proposisi 4.3.** Ambil lintasan

$$
\gamma\colon I\longrightarrow X,
\qquad
\gamma(0)=x_0,
\quad
\gamma(1)=x_1,
$$

dan suatu sampul terbuka $\{V_\alpha\}$ dari $X$ yang memberikan trivialisasi bagi ruang penutup $Z\xrightarrow{\pi}X$. Prapeta $\{\gamma^{-1}(V_\alpha)\}$ merupakan sampul terbuka dari interval kompak $I$. Dengan lema bilangan Lebesgue, kita dapat memilih subdivisi

$$
0=t_0<t_1<\cdots<t_N=1
$$

dan anggota-anggota sampul terbuka $V_1,\ldots,V_N$ yang mentrivialkan ruang penutup serta memenuhi

$$
\gamma([t_{i-1},t_i])\subseteq V_i
\qquad (1\leq i\leq N).
$$

Untuk setiap $i$, pilih trivialisasi

$$
\varphi_i\colon\pi^{-1}(V_i)
\xrightarrow{\cong}
V_i\times F_i,
$$

dengan $F_i$ diskret. Trivialisasi itu mengidentifikasi setiap serat di atas titik $V_i$ dengan $F_i$. Karena titik sambung $\gamma(t_i)$ berada dalam $V_i\cap V_{i+1}$, kita memperoleh rangkaian bijeksi

$$
Z_{x_0}
\cong F_1
\cong Z_{\gamma(t_1)}
\cong F_2
\cong\cdots\cong
F_N
\cong Z_{x_1}.
$$

Komposisinya memberikan bijeksi $Z_{x_0}\cong Z_{x_1}$, yang sekaligus merupakan homeomorfisme karena kedua serat diskret. Argumen ini membuktikan keberadaan; pada tahap ini ia belum memberikan identifikasi yang dinyatakan bebas dari pilihan subdivisi dan trivialisasi. $\square$
:::

Jadi, jika $X$ bersifat SLPC, maka untuk setiap $\alpha\in\pi_0(X)$, sebuah ruang penutup $Z\xrightarrow{\pi}X$ menentukan satu kelas isomorfisme himpunan pada komponen terhubung $X_\alpha\subseteq X$. Kelas isomorfisme ini disebut *serat tipikal* di atas $X_\alpha$. Karena komponen terhubung dan komponen lintasan berimpit dalam ruang SLPC, setiap dua serat pada $X_\alpha$ memang isomorfik, tetapi belum ada identifikasi yang lebih disukai tanpa data tambahan.

**Catatan tentang serat kosong.** Unit ini mengikuti konvensi sumber bahwa serat boleh kosong; dengan kata lain, pemetaan penutup tidak diwajibkan surjektif. Sebagian buku memasukkan surjektivitas ke dalam definisi pemetaan penutup. Jika $X$ bertitik di $x$, sebuah ruang penutup bertitik ditulis

$$
(Z,z)\longrightarrow(X,x),
\qquad
\pi(z)=x.
$$

Data titik di atas itu persis merupakan pilihan $z\in Z_x$. Jika $X$ terhubung dan SLPC, setiap $x'\in X$ dapat dihubungkan ke $x$ oleh suatu lintasan. Identifikasi serat di sepanjang lintasan tersebut membawa $z$ ke suatu titik di $Z_{x'}$, sehingga setiap serat tidak kosong. Identifikasi itu bergantung pada pilihan lintasan; pengangkatan lintasan di bawah akan membuat konstruksinya eksplisit.

Terdapat kategori $\mathbf{Cov}_X$ yang objeknya adalah ruang-ruang penutup
$\pi_i\colon Z_i\to X$. Sebuah morfisme dari $\pi_1$ ke $\pi_2$ adalah pemetaan kontinu $h\colon Z_1\to Z_2$ di atas $X$, yaitu yang membuat segitiga

$$
\begin{array}{ccccc}
Z_1&\xrightarrow{\ h\ }&Z_2\\
&\searrow_{\pi_1}&\downarrow\pi_2\\
&&X
\end{array}
$$

komutatif, atau setara dengan $\pi_2\circ h=\pi_1$. Demikian pula, kategori $\mathbf{Cov}_{(X,x)}$ mempunyai objek ruang penutup bertitik $(Z,z)\to(X,x)$ dan morfisme di atas $X$ yang juga mempertahankan titik terpilih di ruang atas. Kita akan mempelajari kategori-kategori ini untuk melihat informasi apa yang dikandungnya tentang topologi $X$.

::: {.example #o012-rbt-l05-exa-001}
**Contoh 5.1 (monodromi pada bidang kompleks berlubang).** Untuk

$$
X=\mathbb{C}\setminus\{p_1,\ldots,p_n\},
$$

kategori $\mathbf{Cov}_X$ mengodekan data penutup tak bercabang dan monodromi. Setiap penutup topologis dari $X$ memperoleh struktur permukaan Riemann yang ditarik balik sehingga proyeksinya holomorfik dan merupakan biholomorfisme lokal. Untuk penutup berlembar hingga, tiap lubang dapat diisi menurut siklus-siklus monodromi lokal sehingga diperoleh pemetaan bercabang; lubang itu menjadi nilai cabang hanya jika monodromi lokalnya tidak trivial. Untuk penutup berlembar tak hingga, pengisian semacam itu memerlukan syarat tambahan pada orbit monodromi atau ujung-ujung ruang. Jadi, data penutup saja tidak membenarkan klaim bahwa semua dan hanya titik $p_i$ pasti merupakan nilai kritis.
:::

Jika $X$ terhubung dan SLPC, bukti pertama di atas hanya mengatakan bahwa untuk $x_0,x_1\in X$ *terdapat* suatu bijeksi $Z_{x_0}\cong Z_{x_1}$. Kita akan memperkuat pernyataan ini. Sebelum itu, kita memerlukan sebuah konstruksi untuk ruang penutup.

## Tarik balik ruang penutup {#o012-rbt-l05-s02}

::: {.definition #o012-rbt-l05-def-001}
**Definisi 5.1 (tarik balik).** Diberikan ruang penutup
$Z\xrightarrow{\pi}X$ dan pemetaan $Y\xrightarrow{f}X$, *tarik balik* $Z$ sepanjang $f$ adalah subruang

$$
f^*Z:=Y\times_X Z
=\{(y,z)\in Y\times Z\mid f(y)=\pi(z)\}
\subseteq Y\times Z.
$$

Ia berada dalam persegi komutatif

$$
\begin{array}{ccc}
f^*Z&\xrightarrow{\ \operatorname{pr}_2\ }&Z\\
p=\operatorname{pr}_1\downarrow&&\downarrow\pi\\
Y&\xrightarrow{\ f\ }&X.
\end{array}
$$

Ruang hasil kali serat $Y\times_X Z$ sebenarnya dapat didefinisikan untuk sembarang pasangan pemetaan menuju $X$; pada definisi ini, asumsi bahwa $\pi$ merupakan pemetaan penutup diperlukan untuk menyimpulkan bahwa proyeksi $p$ juga merupakan pemetaan penutup.
:::

::: {.proposition #o012-rbt-l05-prop-001}
**Proposisi 5.1.** Dalam situasi Definisi 5.1, berlaku hal-hal berikut.

1. Pemetaan $p\colon f^*Z\to Y$ merupakan ruang penutup.
2. Tarik balik mendefinisikan funktor
   $$
   f^*\colon\mathbf{Cov}_X\longrightarrow\mathbf{Cov}_Y.
   $$
3. Jika $Y_2\xrightarrow{g}Y_1\xrightarrow{f}X$ dan $Z\xrightarrow{\pi}X$, terdapat isomorfisme kanonik dalam $\mathbf{Cov}_{Y_2}$,
   $$
   (f\circ g)^*Z\cong g^*(f^*Z).
   $$

Hanya butir pertama yang memakai asumsi bahwa $\pi$ adalah pemetaan penutup. Butir kedua dan ketiga berlaku bagi tarik balik umum dalam kategori irisan $\mathbf{Top}/X$, yang objeknya adalah pemetaan menuju $X$ dan morfismenya adalah segitiga-segitiga komutatif.
:::

::: {.corollary #o012-rbt-l05-cor-001}
**Akibat 5.1.** Untuk setiap $y\in Y$, terdapat isomorfisme kanonik

$$
(f^*Z)_y\cong Z_{f(y)},
$$

yang diberikan oleh $(y,z)\mapsto z$.
:::

Sekarang, untuk suatu lintasan $\gamma\colon I\to X$ dan ruang penutup $Z\xrightarrow{\pi}X$, kita dapat membentuk ruang penutup tarik balik

$$
\gamma^*Z\longrightarrow I.
$$

Karena itu, kita perlu memahami ruang-ruang penutup dari $I$. Untuk setiap ruang diskret $S$, proyeksi $S\times I\to I$ jelas merupakan ruang penutup.

## Ruang penutup dari interval {#o012-rbt-l05-s03}

::: {.proposition #o012-rbt-l05-prop-002}
**Proposisi 5.2.** Setiap ruang penutup $Z\xrightarrow{\pi}I$ isomorfik dalam $\mathbf{Cov}_I$ dengan ruang penutup trivial

$$
Z_0\times I\xrightarrow{\operatorname{pr}_2}I,
\qquad
Z_0:=\pi^{-1}(0).
$$

Isomorfisme dapat dipilih agar pada $Z_0\times\{0\}$ merupakan identitas serat $Z_0$.
:::

Kita memerlukan lema bantu kecil berikut.

::: {.lemma #o012-rbt-l05-lem-001}
**Lema 5.1.** Jika $X$ kompak dan $Z\to X$ merupakan ruang penutup, maka terdapat sampul berhingga $X$ oleh lingkungan-lingkungan yang di atasnya ruang penutup tersebut trivial. Lingkungan-lingkungan itu dapat dipilih terbuka.
:::

::: {.proof #o012-rbt-l05-proof-002}
**Bukti Proposisi 5.2.** Terapkan Lema 5.1 pada $I$. Dengan memperhalus sampul berhingga menggunakan bilangan Lebesgue dan sedikit memperbesar subinterval-subinterval pembagian, kita dapat memilih rantai subinterval tertutup

$$
[0,t_1],\ [s_2,t_2],\ \ldots,\ [s_N,1]
$$

yang menutupi $I$, masing-masing termuat dalam suatu lingkungan trivial, dan memenuhi $s_{i+1}<t_i$ untuk setiap pasangan berturutan. Argumen induksi pada $N$ mereduksi penempelan menjadi kasus dua bagian.

Jadi, andaikan $I=[0,t]\cup[s,1]$ dengan $s<t$. Tuliskan $Z_A:=\pi^{-1}(A)$. Kita mempunyai trivialisasi

$$
\tau\colon Z_0\times[0,t]\xrightarrow{\cong}Z_{[0,t]}
$$

dan

$$
\sigma\colon F\times[s,1]\xrightarrow{\cong}Z_{[s,1]},
$$

dengan $F$ diskret. Trivialisasi pertama dapat dinormalisasi: jika pembatasannya pada $Z_0\times\{0\}$ menginduksi permutasi $b\colon Z_0\to Z_0$, prakomposisikan $\tau$ dengan $b^{-1}\times\operatorname{id}$. Setelah itu,

$$
\tau(z,0)=z
\qquad(z\in Z_0).
$$

Pada irisan $[s,t]$, pertimbangkan komposisi

$$
Z_0\times[s,t]
\xrightarrow{\ \tau\ }
Z_{[s,t]}
\xrightarrow{\ \sigma^{-1}\ }
F\times[s,t]
\xrightarrow{\ \operatorname{pr}_1\ }
F.
$$

Jika $z\in Z_0$ ditetapkan, komposisi itu memberi pemetaan kontinu
$\{z\}\times[s,t]\to F$. Karena $[s,t]$ terhubung dan $F$ diskret, pemetaan ini konstan. Tuliskan nilai konstannya sebagai $p_z$. Secara eksplisit, untuk sembarang $r\in[s,t]$,

$$
p_z
=\operatorname{pr}_1\!\left(\sigma^{-1}(\tau(z,r))\right).
$$

Pada setiap $r$ tetap, fungsi transisi di atas serat merupakan bijeksi. Karena itu,

$$
\phi\colon Z_0\longrightarrow F,
\qquad
z\longmapsto p_z,
$$

merupakan bijeksi, dan juga homeomorfisme karena kedua ruang diskret.

Sekarang terdapat pemetaan

$$
Z_0\times[0,t]\xrightarrow{\ \tau\ }Z
$$

dan

$$
Z_0\times[s,1]
\xrightarrow{\ \phi\times\operatorname{id}\ }
F\times[s,1]
\xrightarrow{\ \sigma\ }Z.
$$

Keduanya sama pada $Z_0\times[s,t]$ menurut konstruksi $\phi$. Lema penempelan untuk sampul tertutup $[0,t]\cup[s,1]$ menghasilkan pemetaan kontinu

$$
T\colon Z_0\times I\longrightarrow Z
$$

di atas $I$. Dengan menempelkan pemetaan-pemetaan balik pada
$Z_{[0,t]}$ dan $Z_{[s,1]}$, kita memperoleh pemetaan kontinu

$$
S\colon Z\longrightarrow Z_0\times I
$$

di atas $I$. Evaluasi titik demi titik menunjukkan
$S\circ T=\operatorname{id}$ dan $T\circ S=\operatorname{id}$. Jadi $T$ merupakan isomorfisme dalam $\mathbf{Cov}_I$ dan, berkat normalisasi $\tau$, memenuhi $T(z,0)=z$.

Langkah dua bagian ini dapat diterapkan berulang sepanjang rantai subinterval. Maka diperoleh isomorfisme ternormalisasi
$Z_0\times I\cong Z$ untuk sampul berhingga semula. $\square$
:::

::: {.corollary #o012-rbt-l05-cor-002}
**Akibat 5.2 (penampang tunggal dengan nilai awal).** Diberikan ruang penutup $Z\xrightarrow{\pi}I$ dan titik $z\in Z_0$, terdapat tepat satu lintasan

$$
\eta_z\colon I\longrightarrow Z
$$

sedemikian sehingga

$$
\eta_z(0)=z,
\qquad
\pi\circ\eta_z=\operatorname{id}_I.
$$

Dengan kata lain, terdapat tepat satu penampang $\pi$ yang bernilai $z$ pada $0$.
:::

::: {.proof #o012-rbt-l05-proof-003}
**Bukti.** Pilih isomorfisme ternormalisasi

$$
T\colon Z_0\times I\xrightarrow{\cong}Z
$$

dari Proposisi 5.2. Definisikan

$$
\eta_z(t)=T(z,t).
$$

Karena $T$ berada di atas $I$, pemetaan ini memenuhi
$\pi\circ\eta_z=\operatorname{id}_I$, dan normalisasi memberikan
$\eta_z(0)=z$.

Untuk keunikan, jika $\eta'$ merupakan penampang lain dengan nilai awal $z$, tuliskan

$$
T^{-1}(\eta'(t))=(a(t),t).
$$

Fungsi $a\colon I\to Z_0$ kontinu. Karena $I$ terhubung dan $Z_0$ diskret, $a$ konstan. Nilai awal memaksa $a(t)=z$ untuk semua $t$, sehingga
$\eta'(t)=T(z,t)=\eta_z(t)$. $\square$
:::

## Pengangkatan lintasan dan transpor serat {#o012-rbt-l05-s04}

Sekarang kita memperoleh salah satu sifat terpenting ruang penutup.

::: {.theorem #o012-rbt-l05-thm-001}
**Teorema 5.1 (pengangkatan lintasan tunggal).** Diberikan ruang penutup apa pun
$Z\xrightarrow{\pi}X$, lintasan $\gamma\colon I\to X$, dan titik
$z\in Z_{\gamma(0)}$, terdapat tepat satu pengangkatan

$$
\widetilde{\gamma}_z\colon I\longrightarrow Z
$$

yang memenuhi

$$
\widetilde{\gamma}_z(0)=z,
\qquad
\pi\circ\widetilde{\gamma}_z=\gamma.
$$

Tidak diperlukan asumsi bahwa $X$ terhubung atau SLPC.
:::

::: {.proof #o012-rbt-l05-proof-004}
**Bukti.** Bentuk tarik balik

$$
p\colon\gamma^*Z\longrightarrow I.
$$

Seratnya di $0$ teridentifikasi secara kanonik dengan $Z_{\gamma(0)}$, sehingga titik awal yang sesuai adalah $(0,z)$. Menurut Akibat 5.2, terdapat tepat satu penampang

$$
\eta_{(0,z)}\colon I\longrightarrow\gamma^*Z
$$

dengan

$$
\eta_{(0,z)}(0)=(0,z),
\qquad
p\circ\eta_{(0,z)}=\operatorname{id}_I.
$$

Definisikan

$$
\widetilde{\gamma}_z
=\operatorname{pr}_2\circ\eta_{(0,z)}
\colon I\longrightarrow Z.
$$

Persegi tarik balik memberikan

$$
\pi\circ\widetilde{\gamma}_z
=\pi\circ\operatorname{pr}_2\circ\eta_{(0,z)}
=\gamma\circ p\circ\eta_{(0,z)}
=\gamma,
$$

dan nilai awalnya adalah $z$.

Sebaliknya, setiap pengangkatan lain $\lambda\colon I\to Z$ dengan
$\lambda(0)=z$ menentukan penampang kedua dari $p$ melalui

$$
t\longmapsto(t,\lambda(t)).
$$

Penampang itu mempunyai nilai awal $(0,z)$, sehingga oleh keunikan pada Akibat 5.2 ia sama dengan $\eta_{(0,z)}$. Maka
$\lambda=\widetilde{\gamma}_z$. $\square$
:::

Teorema ini memberi bukti kedua yang lebih eksplisit bagi Proposisi 4.3.

::: {.corollary #o012-rbt-l05-cor-003}
**Akibat 5.3 (transpor sepanjang lintasan).** Setiap lintasan
$\gamma\colon I\to X$ mendefinisikan bijeksi

$$
\gamma_*
\colon Z_{\gamma(0)}
\xrightarrow{\cong}
Z_{\gamma(1)},
\qquad
\gamma_*(z)=\widetilde{\gamma}_z(1).
$$
:::

::: {.proof #o012-rbt-l05-proof-005}
**Bukti.** Pertama, $\gamma_*$ memang merupakan fungsi ke
$Z_{\gamma(1)}$ karena

$$
\pi(\widetilde{\gamma}_z(1))=\gamma(1).
$$

Definisikan lintasan balik

$$
\bar\gamma(t)=\gamma(1-t).
$$

Jika $z\in Z_{\gamma(0)}$, lintasan balik dari
$\widetilde{\gamma}_z$ dimulai di $\gamma_*(z)$ dan merupakan pengangkatan
$\bar\gamma$. Oleh keunikan pengangkatan,

$$
\bar\gamma_*\bigl(\gamma_*(z)\bigr)=z.
$$

Argumen simetris, dimulai dari $w\in Z_{\gamma(1)}$, memberikan

$$
\gamma_*\bigl(\bar\gamma_*(w)\bigr)=w.
$$

Jadi $\bar\gamma_*$ adalah invers $\gamma_*$, sehingga $\gamma_*$ bijektif. $\square$
:::

Pengamatan pertama tentang transpor ini adalah invariansinya terhadap reparameterisasi. Jika

$$
\psi\colon I\xrightarrow{\cong}I,
\qquad
\psi(0)=0,
\quad
\psi(1)=1,
$$

maka

$$
(\gamma\circ\psi)_*=\gamma_*
\colon Z_{\gamma(0)}\longrightarrow Z_{\gamma(1)}.
$$

Memang, $\widetilde{\gamma}_z\circ\psi$ adalah pengangkatan
$\gamma\circ\psi$ yang berawal di $z$. Keunikan pengangkatan menyatakan bahwa itulah
$\widetilde{(\gamma\circ\psi)}_z$, dan kedua lintasan terangkat mempunyai titik akhir yang sama. Pernyataan ini baru membuktikan invariansi terhadap reparameterisasi, belum invariansi terhadap homotopi lintasan.

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l05-mastery}

Bagian ini merupakan materi baru untuk edisi bahasa Indonesia dan tersedia di bawah CC BY 4.0. Tidak ada latihan eksplisit dalam rentang sumber Kuliah 5 ini. Empat pemeriksaan berikut menutup langkah-langkah pembuktian dan penerapan yang paling penting; semuanya langsung disertai solusi lengkap. Bukti Lema 5.1 yang tidak dituliskan dalam sumber juga diberikan.

::: {.exercise #o012-rbt-l05-mcheck-001}
**Pemeriksaan penguasaan 5.1 (serat tipikal dan transpor).** Jelaskan perbedaan logis antara pernyataan “semua serat di atas satu komponen lintasan mempunyai tipe isomorfisme yang sama” dan “suatu lintasan $\gamma$ menentukan transpor $\gamma_*$”. Mengapa Akibat 5.3 lebih kuat daripada bukti pertama Proposisi 4.3, tetapi belum memberikan identifikasi yang bebas dari pilihan lintasan?
:::

## Solusi Pemeriksaan 5.1 {#o012-rbt-l05-sol-001}

Bukti pertama hanya menghasilkan keberadaan setidaknya satu bijeksi di antara dua serat, melalui pilihan sampul, subdivisi, dan trivialisasi. Kesimpulan yang dapat dicatat tanpa mempertahankan semua pilihan itu hanyalah kelas isomorfisme serat pada setiap komponen lintasan.

Sebaliknya, setelah lintasan tertentu $\gamma$ dan titik awal $z$ diberikan, Teorema 5.1 memilih tepat satu lintasan terangkat. Karena itu rumus

$$
z\longmapsto\widetilde{\gamma}_z(1)
$$

memberikan fungsi yang ditentukan oleh $\gamma$, bukan sekadar bukti bahwa suatu bijeksi ada. Namun, dua lintasan berbeda dari $x_0$ ke $x_1$ dapat menghasilkan permutasi serat yang berbeda. Unit ini baru membuktikan bahwa reparameterisasi berujung tetap tidak mengubah transpor; belum dibuktikan bahwa deformasi lain pada lintasan tidak mengubahnya.

::: {.exercise #o012-rbt-l05-mcheck-002}
**Pemeriksaan penguasaan 5.2 (struktur tarik balik).** Buktikan ketiga butir Proposisi 5.1 dan isomorfisme serat pada Akibat 5.1 secara eksplisit.
:::

## Solusi Pemeriksaan 5.2 {#o012-rbt-l05-sol-002}

Untuk butir pertama, tetapkan $y_0\in Y$. Pilih lingkungan terbuka $V\ni f(y_0)$ yang di atasnya $Z$ trivial, dengan

$$
\pi^{-1}(V)\cong V\times F
$$

di atas $V$. Himpunan $W=f^{-1}(V)$ merupakan lingkungan terbuka $y_0$. Dengan mengambil hasil kali serat, diperoleh

$$
p^{-1}(W)
=W\times_V\pi^{-1}(V)
\cong W\times_V(V\times F)
\cong W\times F
$$

di atas $W$. Jadi $p\colon f^*Z\to Y$ adalah pemetaan penutup.

Untuk butir kedua, jika $h\colon Z_1\to Z_2$ merupakan morfisme di atas $X$, definisikan

$$
f^*h\colon f^*Z_1\longrightarrow f^*Z_2,
\qquad
(y,z)\longmapsto(y,h(z)).
$$

Karena $\pi_2(h(z))=\pi_1(z)=f(y)$, pasangan di ruas kanan memang berada dalam $f^*Z_2$. Rumus ini mempertahankan proyeksi ke $Y$, bersifat kontinu, serta memenuhi

$$
f^*(\operatorname{id})=\operatorname{id},
\qquad
f^*(h_2\circ h_1)=f^*h_2\circ f^*h_1.
$$

Jadi $f^*$ adalah funktor.

Untuk butir ketiga, kedua ruang dapat ditulis sebagai

$$
(f\circ g)^*Z
=\{(y_2,z)\mid f(g(y_2))=\pi(z)\}
$$

dan

$$
g^*(f^*Z)
=\{(y_2,(y_1,z))\mid g(y_2)=y_1, f(y_1)=\pi(z)\}.
$$

Isomorfisme kanoniknya adalah

$$
(y_2,z)
\longmapsto
\bigl(y_2,(g(y_2),z)\bigr),
$$

dengan invers $(y_2,(y_1,z))\mapsto(y_2,z)$. Kedua pemetaan kontinu, berada di atas $Y_2$, dan tidak melibatkan pilihan apa pun.

Terakhir,

$$
(f^*Z)_y
=\{(y,z)\mid\pi(z)=f(y)\}.
$$

Pemetaan $(y,z)\mapsto z$ merupakan bijeksi kanonik ke
$Z_{f(y)}$, dan homeomorfisme karena serat-serat ruang penutup diskret. Inversnya adalah $z\mapsto(y,z)$.

## Bukti Lema 5.1 {#o012-rbt-l05-check-001}

Untuk setiap $x\in X$, definisi ruang penutup memberikan lingkungan terbuka $V_x\ni x$ yang di atasnya $Z\to X$ trivial. Keluarga $\{V_x\}_{x\in X}$ merupakan sampul terbuka dari $X$. Karena $X$ kompak, terdapat subkeluarga berhingga

$$
V_{x_1},\ldots,V_{x_m}
$$

yang masih menutupi $X$. Setiap anggotanya tetap merupakan lingkungan terbuka tempat ruang penutup itu trivial. Inilah sampul berhingga yang diminta.

::: {.exercise #o012-rbt-l05-mcheck-003}
**Pemeriksaan penguasaan 5.3 (mengangkat satu putaran lingkaran).** Untuk $n\geq1$, pertimbangkan pemetaan penutup

$$
p_n\colon S^1\longrightarrow S^1,
\qquad
p_n(z)=z^n,
$$

dan lintasan $\gamma(t)=e^{2\pi i t}$. Tentukan pengangkatan yang berawal di
$z_k=e^{2\pi i k/n}$, dengan $k\in\{0,\ldots,n-1\}$, lalu hitung transpor $\gamma_*(z_k)$.
:::

## Solusi Pemeriksaan 5.3 {#o012-rbt-l05-sol-003}

Definisikan

$$
\widetilde{\gamma}_{z_k}(t)
=e^{2\pi i(t+k)/n}.
$$

Nilai awalnya adalah $e^{2\pi i k/n}=z_k$, dan

$$
p_n\!\left(\widetilde{\gamma}_{z_k}(t)\right)
=\left(e^{2\pi i(t+k)/n}\right)^n
=e^{2\pi i(t+k)}
=e^{2\pi i t}
=\gamma(t).
$$

Oleh keunikan pengangkatan, inilah pengangkatan yang diminta. Titik akhirnya adalah

$$
\gamma_*(z_k)
=e^{2\pi i(k+1)/n}
=z_{k+1\bmod n}.
$$

Jadi satu putaran positif pada ruang dasar menggerakkan serat dengan siklus
$z_0\mapsto z_1\mapsto\cdots\mapsto z_{n-1}\mapsto z_0$.

::: {.exercise #o012-rbt-l05-mcheck-004}
**Pemeriksaan penguasaan 5.4 (naturalitas transpor).** Misalkan
$h\colon Z_1\to Z_2$ merupakan morfisme ruang penutup di atas $X$, dan $\gamma$ lintasan dalam $X$. Buktikan bahwa diagram transpor serat

$$
\begin{array}{ccc}
(Z_1)_{\gamma(0)}&\xrightarrow{\ \gamma_*^{Z_1}\ }&(Z_1)_{\gamma(1)}\\
h\downarrow&&\downarrow h\\
(Z_2)_{\gamma(0)}&\xrightarrow{\ \gamma_*^{Z_2}\ }&(Z_2)_{\gamma(1)}
\end{array}
$$

komutatif.
:::

## Solusi Pemeriksaan 5.4 {#o012-rbt-l05-sol-004}

Ambil $z\in(Z_1)_{\gamma(0)}$. Karena $h$ berada di atas $X$, kita mempunyai

$$
\pi_2\circ h=\pi_1.
$$

Maka komposisi

$$
h\circ\widetilde{\gamma}^{Z_1}_z\colon I\longrightarrow Z_2
$$

merupakan pengangkatan $\gamma$ dan berawal di $h(z)$. Teorema 5.1 memberikan hanya satu pengangkatan dengan nilai awal itu, sehingga

$$
h\circ\widetilde{\gamma}^{Z_1}_z
=\widetilde{\gamma}^{Z_2}_{h(z)}.
$$

Evaluasi pada $t=1$ menghasilkan

$$
h\bigl(\gamma_*^{Z_1}(z)\bigr)
=h\bigl(\widetilde{\gamma}^{Z_1}_z(1)\bigr)
=\widetilde{\gamma}^{Z_2}_{h(z)}(1)
=\gamma_*^{Z_2}(h(z)).
$$

Karena persamaan berlaku untuk setiap $z$, diagram tersebut komutatif.
