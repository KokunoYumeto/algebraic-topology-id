---
title: "Topologi Aljabar"
subtitle: "Unit 1 — Pengantar dan Ruang Topologis"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "21 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-u001-notice}

Unit ini merupakan terjemahan dan adaptasi Bahasa Indonesia atas *Algebraic Topology* karya David Michael Roberts (2019), tepatnya `Notes.tex` baris 134–348 pada commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`. Karya sumber tersedia di bawah [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah dibaca, pemberian pengenal stabil, pemindahan satu latihan dari catatan pinggir ke blok latihan, penjelasan kasus keluarga kosong pada topologi awal, dan koreksi identitas invers sumber dari $g\circ f=\operatorname{id}_X$ dan $g\circ f=\operatorname{id}_Y$ menjadi $g\circ f=\operatorname{id}_X$ dan $f\circ g=\operatorname{id}_Y$. Materi pendamping penguasaan setelah teks inti ditulis khusus untuk edisi ini dan juga tersedia di bawah CC BY 4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

# Kuliah 1 {#o012-rbt-l01}

## Apa yang dipelajari oleh topologi aljabar? {#o012-rbt-l01-s01}

Topologi aljabar mempelajari pemetaan

$$
\{\text{Ruang}\}\longrightarrow\{\text{Objek aljabar}\},
$$

atau, lebih tepatnya, pemetaan semacam itu yang “berperilaku baik”. Pemetaan tersebut juga harus mengirim fungsi kontinu antarruang ke pemetaan aljabar dengan tetap menghormati komposisi (jadi, pemetaan itu berupa *fungtor*). Selain itu, ruang yang dibangun dari ruang-ruang yang lebih sederhana semestinya dikirim ke objek aljabar yang dibangun secara serasi dari komponen-komponen yang lebih sederhana.

Di sini, “ruang” secara kasar berarti ruang topologis hingga deformasi—biasanya hingga homotopi, meskipun tidak selalu demikian. Kelas-kelas ekuivalensi semacam ini disebut *tipe homotopi*. “Objek aljabar” dapat berarti grup (abelian), gelanggang, modul, atau bahkan kompleks rantai dari objek-objek tersebut.

::: {.note #o012-rbt-l01-note-chain-complex}
**Catatan.** Kompleks rantai adalah suatu jenis barisan pemetaan tertentu,
$\cdots\to V_0\to V_1\to V_2\to\cdots$.
:::

::: {.example #o012-rbt-l01-exa-001}
**Contoh 1.1.** Bagaimana kita dapat menentukan apakah permukaan bola $S^2$ dan torus $S^1\times S^1$ dapat dideformasikan satu sama lain? Bagaimana kita membuktikan bahwa deformasi semacam itu tidak mungkin?
:::

::: {.example #o012-rbt-l01-exa-002}
**Contoh 1.2.** Sebagai contoh positif, kita *dapat* menciutkan
$\mathbb{R}^3\setminus\{0\}\to S^2\hookrightarrow\mathbb{R}^3\setminus\{0\}$
dengan mengirim $x\mapsto\frac{x}{|x|}$. Pemetaan komposit ini dapat dideformasikan secara kontinu menjadi pemetaan identitas. Jadi, dimensi tidak selalu dipertahankan.
:::

::: {.example #o012-rbt-l01-exa-003}
**Contoh 1.3.** Mungkinkah $S^1\sim S^2$?
:::

Pertama-tama kita perlu memahami bagaimana ruang dibangun.

## Ruang topologis {#o012-rbt-l01-s02}

Ingat kembali definisi berikut.

::: {.note #o012-rbt-l01-note-prerequisite}
**Prasyarat sumber.** Topologi dan Analisis III.
:::

::: {.definition #o012-rbt-l01-def-001}
**Definisi 1.1 (topologi).** Suatu *topologi* pada himpunan $X$ adalah koleksi $\mathcal{T}$ yang terdiri atas subset-subset $X$ dan memenuhi:

1. $\emptyset,X\in\mathcal{T}$;
2. jika $U,V\in\mathcal{T}$, maka $U\cap V\in\mathcal{T}$;
3. jika $\{U_\alpha\}_{\alpha\in I}$ adalah sembarang keluarga himpunan dalam $\mathcal{T}$, maka $\bigcup_{\alpha\in I}U_\alpha\in\mathcal{T}$.

Di sini $I$ adalah himpunan indeks. Jika $U\in\mathcal{T}$, kita mengatakan bahwa $U$ *terbuka*. Suatu *ruang topologis* adalah himpunan $X$ yang dilengkapi dengan topologi $\mathcal{T}$.
:::

::: {.example #o012-rbt-l01-exa-004}
**Contoh 1.4.** Pada himpunan bilangan real, *topologi Euklides* (atau topologi “biasa”) didefinisikan dengan menyatakan bahwa suatu himpunan terbuka jika dan hanya jika himpunan itu merupakan gabungan selang-selang terbuka $(a,b)$. Gabungan kosong juga diperbolehkan dan menghasilkan $\emptyset$.

*Topologi diskret* pada himpunan $X$ diperoleh dengan mengambil $\mathcal{T}$ sebagai koleksi semua subset $X$. *Topologi indiskret* diperoleh dengan mengambil $\mathcal{T}=\{\emptyset,X\}$.
:::

Definisi tersebut ringkas, tetapi bukan selalu cara terbaik untuk mendefinisikan topologi. Kita juga akan menggunakan *lingkungan*.

::: {.definition #o012-rbt-l01-def-002}
**Definisi 1.2 (lingkungan).** Dalam topologi $\mathcal{T}$ pada $X$, suatu himpunan $N\subseteq X$ disebut *lingkungan* dari titik $x\in X$ jika terdapat himpunan terbuka $U\subseteq N$ dengan $x\in U$.
:::

::: {.example #o012-rbt-l01-exa-005}
**Contoh 1.5.** Ambil $\mathbb{R}$ dengan topologi Euklides. Himpunan $(-1,1)$, $[-1,1]$, dan $[-1,1)$ semuanya merupakan lingkungan dari setiap $-1<x<1$, tetapi $[0,1)$ bukan lingkungan dari $0$. Sebagai contoh yang sedikit lebih rumit, $[0,1]\cup\{2\}\cup[5,6]$ merupakan lingkungan dari setiap $0<x<1$ dan setiap $5<x<6$.
:::

::: {.example #o012-rbt-l01-exa-006}
**Contoh 1.6.** Misalkan $(X,d)$ adalah ruang metrik. *Topologi metrik* didefinisikan dengan menyatakan bahwa subset $U\subseteq X$ terbuka jika dan hanya jika, untuk setiap $x\in U$, terdapat $\varepsilon_x>0$ sehingga bola terbuka $B(x,\varepsilon_x)\subseteq U$. Bola terbuka yang berpusat di $x$ merupakan lingkungan dari $x$; demikian pula bola tertutup berjari-jari positif.
:::

Pendekatan berikut lebih konkret dan memungkinkan kita mendefinisikan topologi secara ringkas.

::: {.definition #o012-rbt-l01-def-003}
**Definisi 1.3 (basis lingkungan).** Suatu *basis lingkungan* $\mathcal{N}$ pada himpunan $X$ adalah keluarga $\{\mathcal{N}(x)\}_{x\in X}$, dengan setiap $\mathcal{N}(x)$ merupakan koleksi tak kosong yang terdiri atas subset-subset $X$, sehingga untuk setiap $x\in X$ berlaku:

1. untuk setiap $N\in\mathcal{N}(x)$, berlaku $x\in N$;
2. untuk setiap $N_1,N_2\in\mathcal{N}(x)$, terdapat $N\in\mathcal{N}(x)$ dengan $N\subseteq N_1\cap N_2$;
3. untuk setiap $N\in\mathcal{N}(x)$, terdapat subset $U\subseteq N$ sehingga $x\in U$ dan, untuk setiap $y\in U$, terdapat $V\in\mathcal{N}(y)$ dengan $V\subseteq U$.

Himpunan-himpunan dalam $\mathcal{N}(x)$ disebut *lingkungan dasar* dari $x$.
:::

Sebagai contoh, jika $(X,\mathcal{T})$ adalah ruang topologis, kita memperoleh basis lingkungan dengan mendefinisikan $\mathcal{N}(x)$ sebagai koleksi semua lingkungan dari $x$. Kita juga memperoleh basis lingkungan dengan mendefinisikan $\mathcal{N}'(x)$ sebagai koleksi semua himpunan terbuka yang memuat $x$.

Jika $\mathcal{N}$ adalah basis lingkungan pada $X$, definisikan subset $U\subseteq X$ sebagai *$\mathcal{N}$-terbuka* jika dan hanya jika, untuk setiap $x\in U$, terdapat $N\in\mathcal{N}(x)$ dengan $N\subseteq U$.

::: {.proposition #o012-rbt-l01-prop-001}
**Proposisi 1.1.** Himpunan-himpunan $\mathcal{N}$-terbuka membentuk suatu topologi pada $X$.
:::

::: {.proof #o012-rbt-l01-proof-001}
**Bukti.** Kita memeriksa ketiga aksioma topologi.

1. Syarat bahwa $\emptyset$ bersifat $\mathcal{N}$-terbuka benar secara vakum. Karena $\mathcal{N}(x)$ tidak kosong, di setiap titik terdapat lingkungan dasar; akibatnya $X$ bersifat $\mathcal{N}$-terbuka.
2. Misalkan $U$ dan $V$ keduanya $\mathcal{N}$-terbuka. Ambil $x\in U\cap V$. Terdapat $N_U,N_V\in\mathcal{N}(x)$ dengan $N_U\subseteq U$ dan $N_V\subseteq V$. Selain itu, $x\in N_U\cap N_V$. Jadi terdapat $N\in\mathcal{N}(x)$ dengan $N\subseteq N_U\cap N_V\subseteq U\cap V$. Hal ini berlaku untuk setiap $x\in U\cap V$, sehingga $U\cap V$ bersifat $\mathcal{N}$-terbuka.
3. Misalkan setiap $U_\alpha$, $\alpha\in I$, bersifat $\mathcal{N}$-terbuka, dan tetapkan $U=\bigcup_{\alpha\in I}U_\alpha$. Ambil $x\in U$. Ada $\alpha_0$ dengan $x\in U_{\alpha_0}$. Karena $U_{\alpha_0}$ bersifat $\mathcal{N}$-terbuka, terdapat lingkungan dasar $N$ dari $x$ dengan $N\subseteq U_{\alpha_0}\subseteq U$. Maka $U$ bersifat $\mathcal{N}$-terbuka. $\square$
:::

Topologi pada proposisi ini disebut topologi yang *dibangkitkan oleh* $\mathcal{N}$. Lingkungan dalam topologi ini adalah himpunan yang memuat suatu lingkungan dasar: $V$ merupakan lingkungan dari $x$ jika terdapat $N\in\mathcal{N}(x)$ dengan $N\subseteq V$.

Dengan basis lingkungan $\mathcal{N}$ pada $X$, kita dapat mengenali *penutupan* suatu himpunan $S\subset X$ sebagai koleksi titik $x\in X$ yang memenuhi: untuk setiap $N\in\mathcal{N}(x)$, terdapat $s\in N\cap S$.

::: {.example #o012-rbt-l01-exa-007}
**Contoh 1.7.** Pada ruang metrik $(X,d)$, bola-bola terbuka membentuk basis lingkungan pada $X$, dan topologi yang dibangkitkannya adalah topologi metrik.
:::

Dengan demikian, banyak definisi yang dikenal dari ruang metrik tetap berlaku untuk ruang topologis asalkan dapat dirumuskan menggunakan lingkungan dasar. Salah satu yang terpenting adalah kontinuitas.

::: {.definition #o012-rbt-l01-def-004}
**Definisi 1.4 (kontinuitas).** Misalkan $\mathcal{N}_X$ dan $\mathcal{N}_Y$ masing-masing merupakan basis lingkungan pada himpunan $X$ dan $Y$. Fungsi $f\colon X\to Y$ disebut *kontinu* jika, untuk setiap $x\in X$ dan $N\in\mathcal{N}_Y(f(x))$, himpunan $f^{-1}(N)$ memuat suatu lingkungan dasar dari $x$.
:::

Definisi ini merupakan perumuman besar dari definisi kontinuitas $\varepsilon$–$\delta$.

::: {.exercise #o012-rbt-l01-ex-001}
**Latihan 1.1.** Buktikan bahwa jika $f\colon(X,\mathcal{N}_X)\to(Y,\mathcal{N}_Y)$ kontinu menurut definisi di atas, maka $f$ kontinu untuk topologi yang dibangkitkan oleh basis lingkungan pada $X$ dan $Y$.

Ingat bahwa kontinuitas untuk topologi berarti $f^{-1}(U)$ terbuka untuk setiap himpunan terbuka $U$.
:::

Sebagai pemeriksaan kewajaran, fungsi identitas $\operatorname{id}_X$ pada ruang $X$ memang kontinu. Setiap fungsi *menuju* ruang indiskret juga kontinu, demikian pula setiap fungsi *dari* ruang diskret.

::: {.definition #o012-rbt-l01-def-005}
**Definisi 1.5 (homeomorfisma).** Fungsi kontinu $f\colon X\to Y$ disebut *homeomorfisma* jika terdapat fungsi kontinu $g\colon Y\to X$ dengan
$g\circ f=\operatorname{id}_X$ dan $f\circ g=\operatorname{id}_Y$.
Dalam keadaan ini, $X$ dan $Y$ disebut *homeomorfik*.
:::

Sekarang kita perlu menjelaskan cara membangun ruang baru serta pemetaan kontinu yang menghubungkannya dengan ruang asal.

::: {.definition #o012-rbt-l01-def-006}
**Definisi 1.6 (topologi awal).** Misalkan $X$ adalah himpunan; $(Y_\alpha,\mathcal{N}_\alpha)$, $\alpha\in I$, adalah keluarga himpunan yang dilengkapi basis lingkungan; dan $f_\alpha\colon X\to Y_\alpha$ adalah keluarga fungsi. *Topologi awal* pada $X$ dibangkitkan oleh basis lingkungan berikut: suatu himpunan bagian $B\subseteq X$ merupakan lingkungan dasar dari $x$ jika dan hanya jika $B$ berbentuk

$$
f_{\alpha_1}^{-1}(N_1)\cap\cdots\cap f_{\alpha_k}^{-1}(N_k),
$$

untuk beberapa $\alpha_1,\ldots,\alpha_k$ dan $N_i\in\mathcal{N}_{\alpha_i}(f_{\alpha_i}(x))$. Untuk keluarga kosong, irisan kosong ditafsirkan sebagai $X$.
:::

::: {.exercise #o012-rbt-l01-ex-002}
**Latihan 1.2.** Buktikan bahwa koleksi pada Definisi 1.6 benar-benar merupakan basis lingkungan.
:::

Konstruksi ini merangkum topologi produk. Untuk $X=Y_1\times Y_2$ dan proyeksi $f_i\colon X\to Y_i$, $f_i(y_1,y_2)=y_i$, topologi awal adalah topologi produk. Konstruksi yang sama juga menghasilkan topologi subruang: ambil injeksi $f\colon X\hookrightarrow Y$ lalu berikan $X$ topologi awal.

::: {.lemma #o012-rbt-l01-lem-001}
**Lema 1.1 (sifat universal topologi awal).** Setelah $X$ diberi topologi awal, setiap fungsi $f_\alpha\colon X\to Y_\alpha$ kontinu. Selain itu, fungsi $k\colon Z\to X$ kontinu jika dan hanya jika $f_\alpha\circ k\colon Z\to Y_\alpha$ kontinu untuk setiap $\alpha$.
:::

# Pendamping penguasaan terpecahkan {.unnumbered #o012-rbt-u001-mastery}

Bagian ini merupakan materi baru untuk edisi Bahasa Indonesia. Tujuannya bukan mengganti latihan sumber, melainkan menyediakan bukti lengkap, pemeriksaan konsep, dan satu perhitungan deformasi yang menutup hasil belajar Unit 1.

## Solusi Latihan 1.1 {#o012-rbt-l01-sol-001}

Misalkan $U$ terbuka dalam topologi pada $Y$ yang dibangkitkan oleh $\mathcal{N}_Y$. Kita harus membuktikan bahwa $f^{-1}(U)$ terbuka dalam topologi pada $X$ yang dibangkitkan oleh $\mathcal{N}_X$.

Ambil $x\in f^{-1}(U)$. Karena $f(x)\in U$ dan $U$ bersifat $\mathcal{N}_Y$-terbuka, terdapat $N\in\mathcal{N}_Y(f(x))$ dengan $N\subseteq U$. Kontinuitas menurut Definisi 1.4 memberi lingkungan dasar $M\in\mathcal{N}_X(x)$ yang memenuhi

$$
M\subseteq f^{-1}(N)\subseteq f^{-1}(U).
$$

Jadi setiap titik $x\in f^{-1}(U)$ memiliki lingkungan dasar yang termuat dalam $f^{-1}(U)$. Artinya, $f^{-1}(U)$ bersifat $\mathcal{N}_X$-terbuka. Karena hal ini berlaku untuk setiap $U$ terbuka, $f$ kontinu untuk topologi-topologi yang dibangkitkan tersebut.

## Solusi Latihan 1.2 {#o012-rbt-l01-sol-002}

Tuliskan anggota calon basis di $x$ sebagai
$B=\bigcap_{i=1}^{k}f_{\alpha_i}^{-1}(N_i)$, dengan
$N_i\in\mathcal{N}_{\alpha_i}(f_{\alpha_i}(x))$.

1. Karena $f_{\alpha_i}(x)\in N_i$ untuk setiap $i$, berlaku $x\in B$.
2. Jika $B_1$ dan $B_2$ adalah dua lingkungan dasar di $x$, irisannya kembali merupakan irisan berhingga dari prabayangan lingkungan dasar. Apabila indeks yang sama muncul dua kali, aksioma kedua basis lingkungan di $Y_\alpha$ memberi lingkungan dasar yang lebih kecil di dalam irisan keduanya. Jadi terdapat lingkungan dasar $B_3\subseteq B_1\cap B_2$.
3. Untuk setiap $N_i$ pada representasi $B$, aksioma ketiga basis lingkungan di $Y_{\alpha_i}$ memberi $U_i\subseteq N_i$ yang memuat $f_{\alpha_i}(x)$ dan mempunyai sifat penyempurnaan lokal. Tetapkan $U=\bigcap_i f_{\alpha_i}^{-1}(U_i)\subseteq B$. Jika $y\in U$, untuk setiap $i$ pilih $V_i\in\mathcal{N}_{\alpha_i}(f_{\alpha_i}(y))$ dengan $V_i\subseteq U_i$. Maka $\bigcap_i f_{\alpha_i}^{-1}(V_i)$ adalah lingkungan dasar dari $y$ yang termuat dalam $U$.

Ketiga aksioma basis lingkungan terpenuhi. Jika $I$ kosong, satu-satunya irisan yang diperlukan adalah irisan kosong $X$, dan argumen yang sama tetap berlaku.

## Pemeriksaan Lema 1.1 {#o012-rbt-l01-check-001}

Untuk $N\in\mathcal{N}_\alpha(f_\alpha(x))$, prabayangan $f_\alpha^{-1}(N)$ adalah salah satu lingkungan dasar pembangkit di $x$. Jadi setiap $f_\alpha$ kontinu.

Jika $k\colon Z\to X$ kontinu, komposisi $f_\alpha\circ k$ kontinu karena komposisi fungsi kontinu bersifat kontinu. Sebaliknya, anggap setiap $f_\alpha\circ k$ kontinu. Untuk lingkungan dasar
$B=\bigcap_{i=1}^m f_{\alpha_i}^{-1}(N_i)$ di sekitar $k(z)$, kita mempunyai

$$
k^{-1}(B)=\bigcap_{i=1}^m(f_{\alpha_i}\circ k)^{-1}(N_i).
$$

Setiap faktor di ruas kanan memuat suatu lingkungan dasar dari $z$. Dengan aksioma irisan berhingga untuk basis lingkungan di $Z$, irisannya juga memuat suatu lingkungan dasar dari $z$. Jadi $k$ kontinu.

## Contoh terpecahkan: penciutan radial {#o012-rbt-l01-worked-001}

Definisikan $r\colon\mathbb{R}^3\setminus\{0\}\to S^2$ dengan
$r(x)=x/\lVert x\rVert$, dan misalkan $i\colon S^2\hookrightarrow\mathbb{R}^3\setminus\{0\}$ adalah inklusi. Jelas $r\circ i=\operatorname{id}_{S^2}$.

Untuk membandingkan $i\circ r$ dengan identitas pada $\mathbb{R}^3\setminus\{0\}$, gunakan

$$
H(x,t)=\left((1-t)+\frac{t}{\lVert x\rVert}\right)x,
\qquad 0\le t\le1.
$$

Koefisien di dalam kurung selalu positif, sehingga $H(x,t)\ne0$. Selain itu,
$H(x,0)=x$ dan $H(x,1)=x/\lVert x\rVert=i(r(x))$. Jadi $H$ adalah homotopi dari identitas ke $i\circ r$. Jika $x\in S^2$, maka $\lVert x\rVert=1$ dan $H(x,t)=((1-t)+t)x=x$ untuk setiap $t$. Homotopi ini menetapkan $S^2$ titik demi titik. Dengan demikian, $S^2$ memang merupakan retrak deformasi dari $\mathbb{R}^3\setminus\{0\}$.

**Pemeriksaan konsep.** Contoh ini tidak mengatakan bahwa homeomorfisma boleh mengubah dimensi. Contoh ini mengatakan bahwa *tipe homotopi* dapat sama walaupun dimensi ruang berbeda. Perbedaan antara homeomorfisma dan ekuivalensi homotopi akan menjadi pusat unit berikutnya.
