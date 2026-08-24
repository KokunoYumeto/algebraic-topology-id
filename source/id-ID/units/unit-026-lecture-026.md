---
title: "Topologi Aljabar"
subtitle: "Unit 26: Korantai Singular, Kohomologi Tereduksi, dan Invariansi Homotopi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l26-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 5612--5823 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L5612-L5823)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang aktif itu terdiri atas 212 baris fisik. Dengan normalisasi LF dan
terminator LF penutup dipertahankan, ukurannya 9.763 byte dan SHA-256-nya
adalah
`52663b3e60d5d6f3041b8ede449c52a04700ee670c201ef5674c4aa3973203a9`.
Baris 5824, yang memulai Kuliah 27, tidak termasuk. Materi sumber dan adaptasi
Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Rentang sumber memuat satu penanda kuliah, tiga definisi, dua proposisi, dua
teorema, satu lema, tiga korolari, satu catatan, dua contoh, tiga lingkungan
bukti, tiga catatan pinggir, dua label, dan dua rujukan silang. Tidak ada
latihan atau pertanyaan formal sumber, diagram Xy-pic atau TikZ, gambar
eksternal, sitasi, `input`, ataupun `include`.

Edisi memindahkan ketiga catatan pinggir ke urutan bacaan utama. Edisi juga
memperketat hipotesis keteraturan pada penggunaan Teorema Stokes, membuktikan
bahwa diferensial singular memang berkuadrat nol, melengkapi
argumen eksaknya barisan pasangan, memperbaiki kesimpulan kohomologi tereduksi
derajat satu, menyatakan syarat keterhubungan yang tersembunyi dalam argumen
koproduk, dan memberi pembuktian penuh invariansi homotopi melalui operator
prisma. Salah ketik pada pembatas pasangan, argumen ruang pemetaan, derajat
kohomologi ruang kontraktil, dan nama peubah dalam bukti homotopi korantai
diperbaiki serta dicatat di tempatnya.

Enam pemeriksaan penguasaan, enam petunjuk, seluruh penutupan bukti edisi, dan
enam solusi lengkap merupakan materi asli edisi dan tersedia di bawah CC BY
4.0. Edisi ini bersifat independen; edisi ini tidak disponsori, didukung,
disahkan, ataupun diberi status resmi oleh David Michael Roberts atau
institusinya. Produksi edisi ini dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini menambah transparansi proses dan tidak mengurangi
kredit penulis sumber ataupun kredit kontributor manusia.

# Kuliah 26 {#o012-rbt-l26}

## Dari realisasi geometrik menuju simpleks singular {#o012-rbt-l26-s01}

Ingat kembali realisasi geometrik suatu himpunan-$\Delta$ $X_\bullet$:

$$
|X_\bullet|
=
\left(
\bigsqcup_{n=0}^{\infty}
\operatorname{disc}(X_n)\times\Delta^n
\right)\!\big/\!\sim.
$$

Ruang ini dilengkapi sekumpulan pemetaan terpilih
$\Delta^n\to|X_\bullet|$. Untuk setiap $x\in X_n$, pemetaan tersebut ialah
komposisi

$$
\Delta^n
\longrightarrow \operatorname{disc}(X_n)\times\Delta^n
\hookrightarrow
\bigsqcup_{m=0}^{\infty}\operatorname{disc}(X_m)\times\Delta^m
\longrightarrow |X_\bullet|,
$$

dengan pemetaan pertama mengirim $t$ ke $(x,t)$. Jika pemetaan itu
diprakomposisikan dengan inklusi sisi
$\partial_i\colon\Delta^{n-1}\hookrightarrow\Delta^n$, hasilnya kembali
termasuk kelas terpilih: ia adalah pemetaan yang bersesuaian dengan
$d_i(x)\in X_{n-1}$.

Ada motivasi kedua yang berasal dari bentuk diferensial. Misalkan $M$ sebuah
manifold mulus—misalnya, himpunan terbuka di $\mathbb R^n$—dan $\omega$
sebuah bentuk-$k$ diferensial pada $M$. Integrasi mendefinisikan fungsi

$$
\begin{aligned}
C^\infty(\Delta^k,M)&\longrightarrow\mathbb R,\\
(f\colon\Delta^k\to M)&\longmapsto
\int_{\Delta^k}f^*\omega.
\end{aligned}
$$

Jadi setiap bentuk-$k$ menentukan unsur ruang vektor
$\mathbb R^{C^\infty(\Delta^k,M)}$.

::: {.aside #o012-rbt-l26-aside-001}
**Konvensi keteraturan pada simpleks.** Sumber membolehkan “mulus pada
$\Delta^k$” berarti mulus pada bagian dalam simpleks dan mempunyai
perpanjangan kontinu ke batasnya. Konvensi lemah ini cukup untuk menyatakan
nilai batas pemetaan, tetapi tidak dengan sendirinya menjamin hipotesis
Teorema Stokes. Untuk identitas integral di bawah, kita mengandaikan $f$ mulus
hingga batas (misalnya, merupakan restriksi pemetaan mulus pada suatu
lingkungan $\Delta^k$).
:::

Hubungan dengan diferensial eksterior dinyatakan tepat oleh Teorema Stokes.
Untuk $f\colon\Delta^{k+1}\to M$ yang mulus hingga batas,

$$
\int_{\Delta^{k+1}}f^*(d\omega)
=
\int_{\partial\Delta^{k+1}}f^*\omega
=
\sum_{i=0}^{k+1}(-1)^i
\int_{\Delta^k}(f\circ\partial_i)^*\omega.
$$

Dengan kata lain, diferensial eksterior pada bentuk cocok dengan jumlah
berganti tanda atas sisi-sisi simpleks.

::: {.source-audit #o012-rbt-l26-audit-001}
**Audit sumber 26.1.** Notes.tex baris 5632--5633 menyebut secara samar
“restriksi primitif suatu bentuk eksak ke batas.” Edisi menuliskan identitas
Stokes yang dimaksud dan membedakan keteraturan yang diperlukan untuknya dari
konvensi lemah pada catatan pinggir sumber. Ini memperjelas motivasi, tanpa
menambahkan hipotesis baru pada definisi topologis berikutnya.
:::

Untuk ruang topologis umum $X$, kedua gagasan tadi bertemu. Kita biasanya
tidak mempunyai kelas terpilih pemetaan $\Delta^n\to X$, sehingga kita
mempertimbangkan **semua** pemetaan kontinu tersebut, lalu mengambil fungsi
bernilai $R$ pada himpunannya.

## Kompleks korantai singular {#o012-rbt-l26-s02}

::: {.definition #o012-rbt-l26-def-001}
**Definisi 26.1 (korantai dan kohomologi singular).** Misalkan $X$ ruang
topologis dan $R$ sebuah gelanggang. **Kompleks korantai singular** $X$ dengan
koefisien dalam $R$, yang dilambangkan $C^\bullet(X;R)$, ialah

$$
0\longrightarrow
R^{\operatorname{Top}(\Delta^0,X)}
\xrightarrow{\delta}
R^{\operatorname{Top}(\Delta^1,X)}
\xrightarrow{\delta}
R^{\operatorname{Top}(\Delta^2,X)}
\xrightarrow{\delta}\cdots.
$$

Jika $g\colon\operatorname{Top}(\Delta^n,X)\to R$ dan
$\sigma\colon\Delta^{n+1}\to X$, diferensialnya diberikan oleh

$$
(\delta g)(\sigma)
=
\sum_{i=0}^{n+1}(-1)^i g(\sigma\circ\partial_i).
$$

Kohomologi singular $X$ dengan koefisien dalam $R$ ialah

$$
H^n(X;R):=H^n\!\left(C^\bullet(X;R)\right).
$$

Konstruksi ini memberi fungtor kontravarian

$$
C^\bullet(-;R)\colon
\operatorname{Top}^{\mathrm{op}}\longrightarrow\operatorname{Cplx}_R,
\qquad
H^n(-;R)\colon
\operatorname{Top}^{\mathrm{op}}\longrightarrow\operatorname{Mod}_R.
$$
:::

Untuk melihat kontravariansinya dengan tepat, ambil pemetaan $f\colon X\to
Y$. Pascakomposisi memberi

$$
f_\#\colon
\operatorname{Top}(\Delta^k,X)\longrightarrow
\operatorname{Top}(\Delta^k,Y),
\qquad \sigma\longmapsto f\circ\sigma.
$$

Prakomposisi fungsi dengan $f_\#$ kemudian memberi

$$
f^*\colon C^k(Y;R)\longrightarrow C^k(X;R),
\qquad (f^*\varphi)(\sigma)=\varphi(f\circ\sigma).
$$

::: {.proposition #o012-rbt-l26-prop-001}
**Proposisi 26.1 (identitas kompleks dan kealamian).** Diferensial pada
Definisi 26.1 memenuhi $\delta^2=0$. Untuk setiap $f\colon X\to Y$ berlaku
$\delta f^*=f^*\delta$, sehingga $f^*$ memang pemetaan kompleks korantai.
:::

::: {.proof #o012-rbt-l26-proof-001 data-origin="edition-proof-closure"}
**Bukti.** Ambil $g\in C^n(X;R)$ dan simpleks singular
$\sigma\colon\Delta^{n+2}\to X$. Dalam ekspansi $(\delta^2g)(\sigma)$,
setiap pembatasan ke sisi berdimensi $n$ muncul tepat dua kali. Identitas
inklusi sisi

$$
\partial_j\partial_i
=
\partial_i\partial_{j-1}
\qquad (i<j)
$$

memasangkan kedua kemunculan itu. Tanda pasangannya adalah
$(-1)^{i+j}$ dan $(-1)^{i+j-1}$, sehingga jumlahnya nol. Semua suku
berpasangan, jadi $\delta^2g=0$.

Selanjutnya, untuk $\varphi\in C^k(Y;R)$ dan
$\sigma\colon\Delta^{k+1}\to X$,

$$
\begin{aligned}
(\delta f^*\varphi)(\sigma)
&=\sum_i(-1)^i\varphi(f\circ\sigma\circ\partial_i)\\
&=(f^*\delta\varphi)(\sigma).
\end{aligned}
$$

Maka $f^*$ komutatif dengan diferensial. Identitas dan komposisi juga
terpelihara langsung:
$\operatorname{id}_X^*=\operatorname{id}_{C^\bullet(X;R)}$ dan
$(g\circ f)^*=f^*\circ g^*$. Jadi konstruksi tersebut benar-benar fungtorial
dan kontravarian.
:::

::: {.source-audit #o012-rbt-l26-audit-002}
**Audit sumber 26.2.** Notes.tex baris 5646 menghilangkan koma dalam
$\operatorname{Top}(\Delta^k,Y)$ dan meninggalkan kalimat pemetaan terinduksi
tanpa predikat yang lengkap. Edisi memberi kedua arah pemetaan secara
eksplisit. Sumber juga langsung menyebut “kompleks”; Proposisi 26.1 menutup
pemeriksaan $\delta^2=0$ yang diperlukan oleh istilah itu.
:::

Modul-modul korantai tersebut biasanya **sangat besar**. Sebagai contoh,
ambil $X=I$ dan $R=\mathbb Z/2$. Karena himpunan pemetaan kontinu
$\Delta^1\to I$ mempunyai kardinalitas $|\mathbb R|$,

$$
\left|C^1(I;\mathbb Z/2)\right|
=2^{|\operatorname{Top}(\Delta^1,I)|}
=2^{|\mathbb R|}.
$$

Namun, seperti akan diperoleh dari invariansi homotopi, $H^1(I;\mathbb
Z/2)=0$. Berbeda dari kohomologi himpunan-$\Delta$ berdimensi hingga, kita
karena itu benar-benar memerlukan teorema untuk menghitung kohomologi
singular.

Hanya sedikit contoh yang nyaman dihitung langsung dari definisi. Berikut
contoh dasarnya.

::: {.example #o012-rbt-l26-exa-001}
**Contoh 26.1 (satu titik).** Untuk $X=\mathrm{pt}$, terdapat tepat satu
pemetaan $\Delta^k\to\mathrm{pt}$ pada setiap $k$. Kompleks korantai singular
menjadi

$$
0\longrightarrow R\xrightarrow{0}R
\xrightarrow{\operatorname{id}}R
\xrightarrow{0}R
\xrightarrow{\operatorname{id}}\cdots.
$$

Memang, jumlah $\sum_{i=0}^{n+1}(-1)^i$ adalah nol jika $n$ genap dan satu
jika $n$ ganjil. Oleh sebab itu,

$$
H^0(\mathrm{pt};R)=R,
\qquad
H^k(\mathrm{pt};R)=0\quad(k>0).
$$
:::

::: {.aside #o012-rbt-l26-aside-002}
**Pola yang sudah dikenal.** Kompleks berganti antara nol dan identitas ini
sama dengan kompleks “titik tebal” yang muncul sebelumnya. Catatan pinggir
sumber “kita pernah melihat ini” ditempatkan di sini agar hubungan tersebut
terbaca dalam alur utama.
:::

## Kohomologi relatif dan tereduksi {#o012-rbt-l26-s03}

Seperti pada himpunan-$\Delta$, kohomologi relatif memberi keluwesan tambahan.

::: {.definition #o012-rbt-l26-def-002}
**Definisi 26.2 (kohomologi singular relatif).** Untuk pasangan ruang $(X,A)$
dengan inklusi $i\colon A\hookrightarrow X$, **kompleks korantai singular
relatif** ialah

$$
C^\bullet(X,A;R)
:=
\ker\!\left(
i^*\colon C^\bullet(X;R)\longrightarrow C^\bullet(A;R)
\right).
$$

Ini memberi fungtor

$$
C^\bullet(-,-;R)\colon
\operatorname{Top}^{(2),\mathrm{op}}
\longrightarrow\operatorname{Cplx}_R.
$$

Kohomologi singular relatif didefinisikan oleh

$$
H^k(X,A;R):=H^k\!\left(C^\bullet(X,A;R)\right),
$$

dan bersifat fungtorial terhadap pemetaan pasangan ruang.
:::

Kohomologi singular biasa diperoleh kembali dengan mengambil
$A=\varnothing$.

::: {.proposition #o012-rbt-l26-prop-002 data-source-label="prop:les_of_pair_of_spaces"}
**Proposisi 26.2 (barisan eksak panjang pasangan).** Untuk setiap pasangan
ruang $(X,A)$ terdapat barisan eksak panjang alami modul-$R$

$$
\begin{aligned}
0&\longrightarrow H^0(X,A;R)
\longrightarrow H^0(X;R)
\longrightarrow H^0(A;R)\\
&\xrightarrow{\partial^0}H^1(X,A;R)
\longrightarrow H^1(X;R)
\longrightarrow H^1(A;R)
\xrightarrow{\partial^1}\cdots.
\end{aligned}
$$
:::

::: {.proof #o012-rbt-l26-proof-002 data-origin="source-proof-completed-by-edition"}
**Bukti.** Pada setiap derajat $k$, pemetaan restriksi
$i^*\colon C^k(X;R)\to C^k(A;R)$ surjektif. Memang, suatu fungsi pada
simpleks singular yang mendarat di $A$ dapat diperpanjang menjadi fungsi pada
semua simpleks singular di $X$ dengan memberi nilai nol pada simpleks lain.
Menurut definisi, kernelnya ialah $C^k(X,A;R)$. Karena restriksi komutatif
dengan $\delta$, kita memperoleh barisan eksak pendek kompleks korantai

$$
0\longrightarrow C^\bullet(X,A;R)
\longrightarrow C^\bullet(X;R)
\xrightarrow{i^*}C^\bullet(A;R)
\longrightarrow0.
$$

[Teorema 24.1](#o012-rbt-l24-thm-001), yaitu Teorema Mayer--Vietoris aljabar
yang dirujuk dalam sumber, memberi barisan pada pernyataan.
Secara konkret, jika $[a]\in H^k(A;R)$ diwakili oleh kosiklus $a$, pilih
perpanjangan $\widetilde a\in C^k(X;R)$. Karena
$i^*(\delta\widetilde a)=\delta a=0$, unsur
$\delta\widetilde a$ berada dalam $C^{k+1}(X,A;R)$, dan

$$
\partial^k[a]=[\delta\widetilde a].
$$

Perubahan pilihan perpanjangan hanya mengubah kelas ini dengan kobatas
relatif, sehingga pemetaan penghubung terdefinisi baik. Konstruksi pengangkat
ini komutatif dengan pemetaan pasangan; karena itu seluruh barisan alami.
:::

Sekarang ambil ruang bertitik dasar $(X,x)$ dan pasangan
$(X,\{x\})$. Karena kohomologi positif satu titik nol, awal barisan eksak
panjangnya ialah

$$
\begin{aligned}
0&\longrightarrow H^0(X,\{x\};R)
\longrightarrow H^0(X;R)
\xrightarrow{i_x^*}H^0(\{x\};R)=R\\
&\xrightarrow{\partial^0}H^1(X,\{x\};R)
\longrightarrow H^1(X;R)
\longrightarrow0,
\end{aligned}
$$

dan untuk $k>1$ terdapat isomorfisma
$H^k(X,\{x\};R)\cong H^k(X;R)$.

Pemetaan $i_x^*$ pada derajat nol selalu surjektif: unsur $r\in R$ diangkat
oleh kosiklus konstan bernilai $r$ pada $X$. Maka
$\partial^0=0$, sehingga pernyataan yang lebih kuat berlaku:

$$
H^k(X,\{x\};R)\cong H^k(X;R)
\qquad(k\ge1).
$$

Pada derajat nol,

$$
H^0(X,\{x\};R)
=
\ker\!\left(H^0(X;R)\xrightarrow{i_x^*}R\right).
$$

Untuk ringkasnya, kita menulis $H^k(X,x;R)$ bagi
$H^k(X,\{x\};R)$ dan menyebutnya **kohomologi tereduksi** ruang bertitik
dasar $(X,x)$.

::: {.remark #o012-rbt-l26-rem-001}
**Catatan 26.1 (apa yang terjadi pada derajat satu).** Secara formal, potongan
barisan eksak mengatakan bahwa $H^1(X;R)$ adalah hasil bagi
$H^1(X,x;R)$ oleh citra pemetaan

$$
R\xrightarrow{\partial^0}H^1(X,x;R).
$$

Untuk menentukan hasil bagi ini, kita memang harus mengetahui pemetaan
penghubungnya. Dalam kasus ini penentuannya sederhana: pemetaan sebelumnya
$H^0(X;R)\to R$ surjektif karena setiap skalar diangkat oleh kosiklus
konstan. Eksakitas memberi $\operatorname{im}\partial^0=0$. Jadi hasil bagi
tersebut adalah $H^1(X,x;R)$ sendiri, dan pemetaan
$H^1(X,x;R)\to H^1(X;R)$ merupakan isomorfisma.
:::

::: {.source-audit #o012-rbt-l26-audit-003}
**Audit sumber 26.3.** Notes.tex baris 5703 hanya menyatakan isomorfisma
relatif--biasa untuk $k>1$, lalu baris 5711--5713 meninggalkan citra
$R\to H^1(X,x;R)$ tanpa keputusan. Kosiklus konstan membuktikan bahwa pemetaan
sebelumnya $H^0(X;R)\to R$ surjektif. Oleh eksakitas, citra tersebut nol dan
isomorfisma berlaku juga untuk $k=1$. Edisi menutup langkah ini secara
eksplisit.
:::

::: {.example #o012-rbt-l26-exa-002}
**Contoh 26.2 (ruang diskret bertitik dasar).** Jika $S$ ruang diskret dan
$p\in S$ titik dasar terpilih, maka kosiklus derajat nol adalah semua fungsi
$S\to R$, sedangkan restriksi ke $p$ adalah evaluasi. Jadi

$$
H^0(S,p;R)
\cong R^{S\setminus\{p\}}.
$$

Khususnya,

$$
H^0(\mathrm{pt},\mathrm{pt};R)
=R^\varnothing=0.
$$
:::

::: {.proposition #o012-rbt-l26-prop-003 data-origin="edition-proof-closure"}
**Proposisi 26.3 (fungtorialitas bertitik dasar).** Untuk setiap $k$,
kohomologi tereduksi mendefinisikan fungtor

$$
H^k(-,-;R)\colon
\operatorname{Top}_*^{\mathrm{op}}
\longrightarrow\operatorname{Mod}_R.
$$
:::

::: {.proof #o012-rbt-l26-proof-003 data-origin="edition-proof-closure"}
**Bukti.** Pemetaan bertitik dasar
$f\colon(X,x)\to(Y,y)$ memenuhi $f(x)=y$, sehingga ia tepat merupakan
pemetaan pasangan $(X,\{x\})\to(Y,\{y\})$. Fungtorialitas kontravarian
kohomologi relatif memberi

$$
f^*\colon H^k(Y,y;R)\longrightarrow H^k(X,x;R).
$$

Hukum identitas dan komposisi diwarisi langsung dari fungtor kompleks
relatif. Syarat titik dasar diperlukan agar prakomposisi membawa korantai yang
lenyap pada $\{y\}$ ke korantai yang lenyap pada $\{x\}$.
:::

::: {.aside #o012-rbt-l26-aside-003}
**Catatan tentang catatan pinggir sumber.** Fungtorialitas ini ditandai
“Latihan!” dalam margin Notes.tex. Edisi mempertahankan tugas matematisnya,
tetapi menempatkan hasil dan buktinya dalam alur utama agar sifat penting ini
tidak tersembunyi. Perhatikan khususnya bahwa fungtorialitas relatif tersebut
secara langsung berlaku untuk pemetaan bertitik dasar.
:::

## Koproduk ruang {#o012-rbt-l26-s04}

Hasil pertama berikut membantu menghitung kohomologi relatif.

::: {.proposition #o012-rbt-l26-prop-004}
**Proposisi 26.4 (kohomologi koproduk hingga).** Untuk pasangan ruang
$(X,A)$ dan $(Y,B)$, terdapat isomorfisma kanonik kompleks

$$
C^\bullet(X\sqcup Y,A\sqcup B;R)
\xrightarrow{\ \cong\ }
C^\bullet(X,A;R)\oplus C^\bullet(Y,B;R).
$$

Setelah mengambil kohomologi, isomorfisma ini memberi, untuk setiap $k$,

$$
H^k(X\sqcup Y,A\sqcup B;R)
\xrightarrow{\ \cong\ }
H^k(X,A;R)\oplus H^k(Y,B;R).
$$
:::

::: {.proof #o012-rbt-l26-proof-004}
**Bukti.** Simpleks standar $\Delta^k$ terhubung. Karena $X$ dan $Y$ terbuka
sekaligus tertutup di $X\sqcup Y$, citra kontinu suatu
$\sigma\colon\Delta^k\to X\sqcup Y$ harus seluruhnya berada di salah satu
komponen. Jadi

$$
\operatorname{Top}(\Delta^k,X\sqcup Y)
=
\operatorname{Top}(\Delta^k,X)
\sqcup
\operatorname{Top}(\Delta^k,Y).
$$

Untuk dua himpunan $P,Q$, pembatasan fungsi memberi isomorfisma

$$
R^{P\sqcup Q}\cong R^P\oplus R^Q.
$$

Di bawah isomorfisma ini, setiap pemetaan sisi dan diferensial $\delta$
bertindak komponen demi komponen. Pemetaan restriksi menuju $A\sqcup B$ juga
menjadi jumlah langsung pemetaan restriksi menuju $A$ dan menuju $B$.
Kernelnya karena itu ialah

$$
\ker(i_{A\sqcup B}^*)
\cong \ker(i_A^*)\oplus\ker(i_B^*),
$$

yang tepat merupakan isomorfisma kompleks relatif pada pernyataan. Kohomologi
jumlah langsung dua kompleks adalah jumlah langsung kohomologinya, sehingga
isomorfisma kedua mengikuti.
:::

Dengan mengambil pasangan $(X,\varnothing)$ dan $(Y,\varnothing)$, kita
memperoleh hasil yang sama untuk kohomologi biasa:

$$
H^k(X\sqcup Y;R)
\cong H^k(X;R)\oplus H^k(Y;R).
$$

::: {.source-audit #o012-rbt-l26-audit-004}
**Audit sumber 26.4.** Dua tampilan pada Notes.tex baris 5731 dan 5735
menuliskan pembatas pasangan sebagai $(X,A:R)$; edisi mengembalikan titik koma
yang bertipe benar, $(X,A;R)$. Kesamaan ruang pemetaan pada baris 5741 juga
memerlukan keterhubungan $\Delta^k$. Alasan itu dinyatakan eksplisit; tanpa
keterhubungan domain, suatu pemetaan ke $X\sqcup Y$ dapat mengenai kedua
komponen dan dekomposisi serupa tidak berlaku dalam bentuk tersebut.
:::

## Invariansi homotopi {#o012-rbt-l26-s05}

Kita menulis $f^*$ bagi pemetaan $H^k(f)$ yang diinduksi oleh pemetaan ruang
$f$.

::: {.theorem #o012-rbt-l26-thm-001 data-source-label="thm:homotopy_invariance_cohom"}
**Teorema 26.1 (invariansi homotopi kohomologi singular).** Jika
$f,g\colon X\to Y$ homotopik, maka

$$
f^*=g^*\colon H^k(Y;R)\longrightarrow H^k(X;R)
$$

untuk setiap $k$.
:::

Pembuktian pada tingkat kompleks akan diberikan setelah beberapa akibat
langsung. Ketiga bukti berikut hanya memakai fungtorialitas dan Teorema 26.1.

::: {.corollary #o012-rbt-l26-cor-001}
**Korolari 26.1 (ekuivalensi homotopi).** Misalkan
$f\colon X\to Y$ dan $g\colon Y\to X$ saling invers hingga homotopi.
Maka

$$
f^*=(g^*)^{-1},
$$

dan $H^k(X;R)\cong H^k(Y;R)$ untuk setiap $k$.
:::

::: {.proof #o012-rbt-l26-proof-005 data-origin="edition-proof-closure"}
**Bukti.** Kita mempunyai $g\circ f\simeq\operatorname{id}_X$ dan
$f\circ g\simeq\operatorname{id}_Y$. Karena kohomologi kontravarian,

$$
(g\circ f)^*=f^*\circ g^*,
\qquad
(f\circ g)^*=g^*\circ f^*.
$$

Teorema 26.1 menyamakan kedua pemetaan ini masing-masing dengan identitas pada
$H^k(X;R)$ dan $H^k(Y;R)$. Jadi $f^*$ dan $g^*$ saling invers.
:::

::: {.corollary #o012-rbt-l26-cor-002}
**Korolari 26.2 (ruang kontraktil).** Jika $X$ kontraktil, maka

$$
H^0(X;R)\cong R,
\qquad
H^k(X;R)=0\quad(k>0).
$$

Lebih tepatnya, jika $X$ berkontraksi ke $x\in X$, pemetaan yang diinduksi
inklusi $\{x\}\hookrightarrow X$,

$$
H^k(X;R)\longrightarrow H^k(\{x\};R),
$$

merupakan isomorfisma untuk setiap $k$. Akibatnya,
$H^k(X,x;R)=0$ untuk setiap $k$.
:::

::: {.proof #o012-rbt-l26-proof-006 data-origin="edition-proof-closure"}
**Bukti.** Misalkan $i\colon\{x\}\hookrightarrow X$ dan
$r\colon X\to\{x\}$ pemetaan konstan. Kita mempunyai
$r\circ i=\operatorname{id}_{\{x\}}$ dan
$i\circ r\simeq\operatorname{id}_X$ melalui kontraksi yang diberikan.
Korolari 26.1 membuat $i^*$ dan $r^*$ saling invers. Perhitungan Contoh 26.1
lalu memberi kohomologi biasa yang dinyatakan.

Pada barisan eksak panjang pasangan $(X,\{x\})$, pemetaan
$H^k(X;R)\to H^k(\{x\};R)$ adalah isomorfisma pada setiap derajat. Eksakitas
memaksa setiap suku relatif $H^k(X,x;R)$ menjadi nol.
:::

::: {.source-audit #o012-rbt-l26-audit-005}
**Audit sumber 26.5.** Notes.tex baris 5768 menyatakan
$H^k(X;R)=0$ untuk $k>0$, lalu menulis $H^k(X;R)\cong R$ tanpa menentukan
derajat. Edisi mengembalikan maksud yang konsisten:
$H^0(X;R)\cong R$.
:::

::: {.corollary #o012-rbt-l26-cor-003}
**Korolari 26.3 (perubahan titik dasar sepanjang lintasan).** Misalkan $X$
ruang bertitik dasar dan $\gamma\colon x\rightsquigarrow x'$ sebuah lintasan.
Dua pemetaan

$$
H^0(X;R)\longrightarrow H^0(\mathrm{pt};R)=R
$$

yang diinduksi oleh inklusi $x$ dan $x'$ adalah sama. Karena itu,

$$
H^0(X,x;R)=H^0(X,x';R).
$$

Jadi kohomologi tereduksi derajat nol hanya bergantung pada komponen lintasan
titik dasar, bukan pada wakil titik dasarnya.
:::

::: {.proof #o012-rbt-l26-proof-007 data-origin="edition-proof-closure"}
**Bukti.** Lintasan $\gamma$ tepat merupakan homotopi antara kedua inklusi
$i_x,i_{x'}\colon\mathrm{pt}\to X$. Teorema 26.1 memberi
$i_x^*=i_{x'}^*$. Kedua modul relatif derajat nol adalah kernel pemetaan yang
sama dari $H^0(X;R)$ ke $R$, sehingga keduanya sama.
:::

Untuk kompleks, kuasi-isomorfisma memainkan peran yang menyerupai ekuivalensi
homotopi lemah. Namun, homotopi antarpemetaan ruang mempunyai analog aljabar
yang lebih kuat.

::: {.definition #o012-rbt-l26-def-003}
**Definisi 26.3 (homotopi korantai).** Misalkan
$f,g\colon A^\bullet\to B^\bullet$ pemetaan kompleks korantai. Sebuah
**homotopi korantai** dari $f$ ke $g$ ialah keluarga homomorfisma modul-$R$
berderajat $-1$

$$
\{h_n\colon A^n\longrightarrow B^{n-1}\}_{n\in\mathbb Z}
$$

yang memenuhi

$$
\delta^B_{n-1}h_n+h_{n+1}\delta^A_n=f_n-g_n
$$

untuk setiap $n$.
:::

::: {.lemma #o012-rbt-l26-lem-001}
**Lema 26.1 (pemetaan yang homotopik pada tingkat korantai).** Jika terdapat
homotopi korantai dari $f$ ke $g$, maka

$$
H^k(f)=H^k(g)
$$

untuk setiap $k$.
:::

::: {.proof #o012-rbt-l26-proof-008 data-origin="source-proof-repaired-by-edition"}
**Bukti.** Ambil kelas $[c]\in H^k(A^\bullet)$ dengan wakil kosiklus
$c\in A^k$, sehingga $\delta^A_k(c)=0$. Identitas homotopi memberi

$$
f_k(c)
=
g_k(c)+\delta^B_{k-1}(h_k(c))
+h_{k+1}(\delta^A_k(c)).
$$

Suku terakhir nol karena $c$ kosiklus, sedangkan suku tengah merupakan
kobatas. Jadi

$$
\begin{aligned}
H^k(f)([c])
&=[f_k(c)]\\
&=[g_k(c)+\delta^B_{k-1}(h_k(c))]\\
&=[g_k(c)]\\
&=H^k(g)([c]).
\end{aligned}
$$

Kesamaan ini berlaku pada setiap kelas, sehingga kedua pemetaan kohomologi
sama.
:::

::: {.source-audit #o012-rbt-l26-audit-006}
**Audit sumber 26.6.** Pada Notes.tex baris 5801, kosiklus telah dinamai $c$
tetapi suku terakhir ditulis $h_{k+1}(\delta^A_k(x))$. Edisi mengganti $x$
dengan $c$ dan menyatakan secara eksplisit mengapa suku kobatas lenyap
setelah mengambil kelas kohomologi.
:::

Versi tingkat-kompleks berikut lebih kuat daripada Teorema 26.1.

::: {.theorem #o012-rbt-l26-thm-002}
**Teorema 26.2 (homotopi ruang menginduksi homotopi korantai).** Jika
$f,g\colon X\to Y$ homotopik, maka terdapat homotopi korantai antara dua
pemetaan terinduksi

$$
f^*,g^*\colon C^\bullet(Y;R)\longrightarrow C^\bullet(X;R).
$$
:::

::: {.proof #o012-rbt-l26-proof-009 data-origin="source-sketch-completed-by-edition"}
**Bukti.** Pilih homotopi
$H\colon X\times I\to Y$ dengan $H(-,0)=f$ dan $H(-,1)=g$. Agar tanda dapat
diperiksa, gunakan terlebih dahulu kompleks rantai singular
$S_n(X;R)$, yaitu modul bebas atas semua simpleks singular
$\sigma\colon\Delta^n\to X$, dengan batas berganti tanda.

Reduksi dalam sketsa sumber dapat dilihat langsung. Jika
$j_0,j_1\colon X\to X\times I$ adalah kedua inklusi ujung, maka
$f=H\circ j_0$ dan $g=H\circ j_1$. Fungtorialitas karena itu mereduksi masalah
ke homotopi silinder antara $j_0$ dan $j_1$. Selanjutnya, karena rantai
singular bebas atas pemetaan $\sigma\colon\Delta^n\to X$, pemeriksaan dapat
dilakukan pada satu $\Delta^n$ pada satu waktu. Inilah alasan triangulasi
$\Delta^n\times I$ cukup untuk kasus umum.

Triangulasi standar prisma $\Delta^n\times I$ mempunyai $n+1$ simpleks
berorientasi. Untuk $0\le i\le n$, definisikan pemetaan afin
$q_i\colon\Delta^{n+1}\to\Delta^n\times I$ melalui daftar titik sudut
berurutan

$$
(v_0,0),\ldots,(v_i,0),(v_i,1),\ldots,(v_n,1).
$$

Untuk generator $\sigma$ tentukan operator prisma

$$
P_n(\sigma)
=
\sum_{i=0}^{n}(-1)^i
H\circ(\sigma\times\operatorname{id}_I)\circ q_i,
$$

dan perluas secara $R$-linear. Pengembangan batas setiap simpleks prisma
memberi identitas

$$
\partial P+P\partial=g_\#-f_\#.
$$

Berikut pemeriksaan kombinasinya. Sisi bawah hanya muncul pada simpleks
prisma terakhir dan menyumbang $-f_\#\sigma$; sisi atas hanya muncul pada
simpleks pertama dan menyumbang $g_\#\sigma$. Setiap sisi diagonal di bagian
dalam muncul pada dua simpleks prisma yang bersebelahan dengan orientasi
berlawanan, sehingga saling meniadakan. Sisi-sisi lainnya adalah prisma atas
sisi-sisi $\partial_j\sigma$; setelah tanda $(-1)^j$ dari batas singular
diperhitungkan, jumlahnya tepat $-P(\partial\sigma)$. Memindahkan suku itu ke
ruas kiri memberi identitas di atas. Ini adalah “kombinatorika berantakan”
yang disebut dalam sketsa sumber, kini dengan semua jenis sisi dan tanda
penutupnya dinyatakan.

Korantai singular dapat dipandang sebagai

$$
C^n(Y;R)=\operatorname{Hom}_R(S_n(Y;R),R).
$$

Tetapkan $h_0=0$. Untuk $n\ge1$ dan $\varphi\in C^n(Y;R)$, definisikan
pemetaan derajat $-1$

$$
h_n\varphi:=-\,\varphi\circ P_{n-1}
\in C^{n-1}(X;R).
$$

Jika $c\in S_n(X;R)$, dualitas antara $\delta$ dan $\partial$ memberi

$$
\begin{aligned}
\bigl((\delta h+h\delta)\varphi\bigr)(c)
&=-\varphi(P\partial c)-(\delta\varphi)(Pc)\\
&=-\varphi(P\partial c+\partial Pc)\\
&=-\varphi((g_\#-f_\#)c)\\
&=(f^*\varphi-g^*\varphi)(c).
\end{aligned}
$$

Jadi $\delta h+h\delta=f^*-g^*$, tepat identitas homotopi korantai pada
Definisi 26.3. Lema 26.1 kemudian memberi $H^k(f)=H^k(g)$, sehingga sekaligus
menyelesaikan bukti [Teorema 26.1](#o012-rbt-l26-thm-001).
:::

::: {.source-audit #o012-rbt-l26-audit-007}
**Audit sumber 26.7.** Notes.tex baris 5815--5821 hanya menguraikan reduksi
ke $I\times X$, simpleks $X=\Delta^k$, dan suatu triangulasi prisma, lalu
menyerahkan identitas yang diperlukan pada kombinatorika. Edisi membangun
operator prisma, memeriksa pembatalan semua jenis sisi, mengatur tanda agar
sesuai dengan konvensi $f^*-g^*$ sumber, dan mendualisasikannya. Tidak ada
teorema dalam unit ini yang tersisa tanpa bukti.
:::

## Pemeriksaan penguasaan {#o012-rbt-l26-mastery}

Enam soal berikut merupakan materi asli edisi. Setiap soal mempunyai petunjuk
dan solusi lengkap yang dapat diperiksa secara mandiri.

::: {.exercise #o012-rbt-l26-mcheck-001 data-origin="edition-original"}
**Pemeriksaan Penguasaan 26.1 (mengapa $\delta^2=0$).** Misalkan
$g\in C^n(X;R)$.

1. Tuliskan $(\delta^2g)(\sigma)$ untuk
   $\sigma\colon\Delta^{n+2}\to X$ sebagai jumlah ganda.
2. Pasangkan setiap suku yang membatasi $\sigma$ ke muka kodimensi dua yang
   sama.
3. Periksa secara eksplisit kasus $n=0$.
:::

::: {.hint #o012-rbt-l26-hint-001 data-origin="edition-original"}
**Petunjuk.** Gunakan
$\partial_j\partial_i=\partial_i\partial_{j-1}$ untuk $i<j$. Dalam kasus
$n=0$, tulis tiga sisi dari $\Delta^2$ dan enam evaluasi pada titik sudut
sebelum melakukan pembatalan.
:::

::: {.solution #o012-rbt-l26-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 26.1.** Dari definisi,

$$
(\delta^2g)(\sigma)
=
\sum_{j=0}^{n+2}\sum_{i=0}^{n+1}
(-1)^{i+j}
g(\sigma\circ\partial_j\circ\partial_i).
$$

Untuk $i<j$, identitas sisi
$\partial_j\partial_i=\partial_i\partial_{j-1}$ menunjukkan bahwa suku
berindeks $(i,j)$ mempunyai muka kodimensi dua yang sama dengan suku pada
urutan penghapusan sebaliknya. Tanda keduanya berbeda satu faktor $-1$:
satu tanda adalah $(-1)^{i+j}$, dan tanda pasangannya adalah
$(-1)^{i+j-1}$. Jadi semua suku saling meniadakan.

Untuk $n=0$, tulis $g$ sebagai fungsi pada titik-titik singular dan
$\sigma\colon\Delta^2\to X$. Maka

$$
\begin{aligned}
(\delta^2g)(\sigma)
={}&
\bigl[g(\sigma(v_2))-g(\sigma(v_1))\bigr]\\
&-\bigl[g(\sigma(v_2))-g(\sigma(v_0))\bigr]\\
&+\bigl[g(\sigma(v_1))-g(\sigma(v_0))\bigr]
=0.
\end{aligned}
$$

Setiap nilai titik sudut muncul dua kali dengan tanda berlawanan. Kasus ini
adalah bayangan berdimensi rendah dari pasangan muka pada argumen umum.
:::

::: {.exercise #o012-rbt-l26-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 26.2 (titik, interval, dan kontraktilitas).**

1. Hitung diferensial $C^n(\mathrm{pt};R)\to C^{n+1}(\mathrm{pt};R)$ dari
   jumlah berganti tanda.
2. Gunakan kontraksi $I\to\{0\}$ untuk menentukan $H^k(I;R)$ pada semua
   derajat.
3. Jelaskan mengapa hasil bagian 2 tidak bertentangan dengan besarnya
   $C^1(I;R)$.
:::

::: {.hint #o012-rbt-l26-hint-002 data-origin="edition-original"}
**Petunjuk.** Hitung
$\sum_{i=0}^{n+1}(-1)^i$. Untuk interval, inklusi titik dan pemetaan konstan
adalah invers hingga homotopi. Kohomologi adalah hasil bagi kernel dengan
citra, bukan ukuran modul korantai.
:::

::: {.solution #o012-rbt-l26-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 26.2.** Ada satu simpleks singular
$\Delta^n\to\mathrm{pt}$ pada setiap derajat, sehingga setiap modul korantai
adalah $R$. Diferensial derajat $n$ adalah perkalian dengan

$$
\sum_{i=0}^{n+1}(-1)^i
=
\begin{cases}
0,&n\ \text{genap},\\
1,&n\ \text{ganjil}.
\end{cases}
$$

Jadi kompleksnya berganti antara pemetaan nol dan identitas. Kohomologinya
adalah $R$ pada derajat nol dan nol pada derajat positif.

Interval berkontraksi ke $0$. Jika $i\colon\{0\}\hookrightarrow I$ dan
$r\colon I\to\{0\}$, maka $ri=\operatorname{id}$ dan
$ir\simeq\operatorname{id}_I$. Invariansi homotopi membuat $i^*$ dan $r^*$
saling invers, sehingga

$$
H^0(I;R)=R,
\qquad H^k(I;R)=0\quad(k>0).
$$

Tidak ada pertentangan dengan besarnya $C^1(I;R)$. Modul itu memang memuat
semua fungsi dari himpunan sangat besar simpleks singular ke $R$, tetapi
kohomologi hanya menyimpan kosiklus modulo kobatas. Invariansi homotopi
menunjukkan bahwa pada derajat positif semua kosiklus tersebut sudah merupakan
kobatas.
:::

::: {.exercise #o012-rbt-l26-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 26.3 (pasangan interval dan batasnya).** Ambil
$\partial I=\{0,1\}$. Gunakan barisan eksak panjang pasangan, bukan suatu
kompleks selular, untuk menghitung $H^k(I,\partial I;R)$ pada semua derajat.
Identifikasi secara eksplisit kokernel pemetaan pada derajat nol.
:::

::: {.hint #o012-rbt-l26-hint-003 data-origin="edition-original"}
**Petunjuk.** Kita mempunyai $H^0(I;R)=R$ dan
$H^0(\partial I;R)=R\oplus R$, sedangkan semua kohomologi positif kedua ruang
itu nol. Pemetaan restriksi mengirim $a$ ke $(a,a)$.
:::

::: {.solution #o012-rbt-l26-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 26.3.** Bagian relevan barisan eksak panjang ialah

$$
0\longrightarrow H^0(I,\partial I;R)
\longrightarrow R
\xrightarrow{\Delta}R\oplus R
\xrightarrow{\partial^0}H^1(I,\partial I;R)
\longrightarrow0,
$$

dengan $\Delta(a)=(a,a)$. Pemetaan diagonal injektif, sehingga
$H^0(I,\partial I;R)=0$. Eksakitas memberi

$$
H^1(I,\partial I;R)
\cong
(R\oplus R)/\Delta(R).
$$

Pemetaan $(a,b)\mapsto b-a$ surjektif dan kernelnya tepat $\Delta(R)$, maka
ia menginduksi isomorfisma

$$
H^1(I,\partial I;R)\cong R.
$$

Pada derajat $k>1$, semua suku biasa yang mengapit suku relatif nol, sehingga
$H^k(I,\partial I;R)=0$. Dengan demikian,

$$
H^k(I,\partial I;R)
\cong
\begin{cases}
R,&k=1,\\
0,&k\ne1.
\end{cases}
$$

Pemetaan penghubung mengukur selisih nilai pada kedua ujung interval.
:::

::: {.exercise #o012-rbt-l26-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 26.4 (ruang diskret dan pemetaan bertitik dasar).**
Misalkan $S=\{p,s_1,\ldots,s_m\}$ dan
$T=\{q,t_1,\ldots,t_n\}$ diskret dengan titik dasar $p$ dan $q$.

1. Hitung $H^k(S,p;R)$.
2. Untuk pemetaan bertitik dasar $\phi\colon(S,p)\to(T,q)$, tuliskan
   $\phi^*\colon H^0(T,q;R)\to H^0(S,p;R)$ pada fungsi.
3. Buktikan bahwa hasilnya tetap lenyap di titik dasar.
:::

::: {.hint #o012-rbt-l26-hint-004 data-origin="edition-original"}
**Petunjuk.** Korantai relatif derajat nol adalah fungsi yang bernilai nol di
titik dasar. Pemetaan terinduksi adalah prakomposisi dengan $\phi$.
:::

::: {.solution #o012-rbt-l26-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 26.4.** Karena $S$ diskret, komponen lintasannya adalah
titik-titik tunggal. Maka

$$
H^0(S;R)=R^S,
$$

dan evaluasi di $p$ mempunyai kernel semua fungsi yang lenyap di $p$:

$$
H^0(S,p;R)
=
\{a\colon S\to R:a(p)=0\}
\cong R^{\{s_1,\ldots,s_m\}}\cong R^m.
$$

Kohomologi positif ruang diskret nol; melalui isomorfisma relatif--biasa pada
derajat positif, $H^k(S,p;R)=0$ untuk $k>0$.

Jika $a\in H^0(T,q;R)$, maka

$$
(\phi^*a)(s)=a(\phi(s)).
$$

Karena $\phi$ bertitik dasar, $\phi(p)=q$. Oleh sebab itu,

$$
(\phi^*a)(p)=a(\phi(p))=a(q)=0.
$$

Jadi prakomposisi memang membawa korantai relatif ke korantai relatif. Ini
juga memperlihatkan secara konkret mengapa syarat bertitik dasar diperlukan.
:::

::: {.exercise #o012-rbt-l26-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 26.5 (koproduk dan keterhubungan domain).**

1. Buktikan bahwa setiap pemetaan kontinu
   $\Delta^k\to X\sqcup Y$ mendarat seluruhnya di $X$ atau seluruhnya di $Y$.
2. Jika $X_1,\ldots,X_m$ semuanya kontraktil dan takkosong, hitung
   $H^k(\bigsqcup_{j=1}^mX_j;R)$.
3. Berikan contoh domain takterhubung $K$ dan pemetaan
   $K\to X\sqcup Y$ yang mengenai kedua komponen koproduk, untuk menunjukkan
   letak
   penggunaan keterhubungan.
:::

::: {.hint #o012-rbt-l26-hint-005 data-origin="edition-original"}
**Petunjuk.** Pracitra $X$ dan $Y$ terbuka sekaligus tertutup dan mempartisi
$\Delta^k$. Iterasikan Proposisi 26.4. Untuk bagian terakhir, pakai ruang dua
titik diskret.
:::

::: {.solution #o012-rbt-l26-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 26.5.** Dalam $X\sqcup Y$, kedua komponen koproduk terbuka dan
tertutup. Jika $\sigma\colon\Delta^k\to X\sqcup Y$, maka
$\sigma^{-1}(X)$ dan $\sigma^{-1}(Y)$ adalah dua himpunan buka-tertutup yang
saling lepas dan menutupi $\Delta^k$. Karena $\Delta^k$ terhubung, salah
satunya kosong. Jadi seluruh citra berada dalam tepat satu komponen koproduk.

Dengan mengiterasikan dekomposisi koproduk dan memakai kontraktilitas,

$$
\begin{aligned}
H^0\!\left(\bigsqcup_{j=1}^mX_j;R\right)
&\cong\bigoplus_{j=1}^mH^0(X_j;R)
\cong R^m,\\
H^k\!\left(\bigsqcup_{j=1}^mX_j;R\right)
&=0\qquad(k>0).
\end{aligned}
$$

Untuk memperlihatkan kegagalan tanpa keterhubungan, ambil
$K=\{a,b\}$ diskret, pilih $x\in X$ dan $y\in Y$, lalu definisikan
$u(a)=x$ dan $u(b)=y$. Pemetaan kontinu $u$ mengenai kedua komponen. Jadi
dekomposisi ruang pemetaan yang dipakai dalam bukti bergantung secara esensial
pada keterhubungan simpleks standar.
:::

::: {.exercise #o012-rbt-l26-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 26.6 (operator prisma pada derajat rendah).**
Misalkan $H\colon X\times I\to Y$ adalah homotopi dari $f$ ke $g$.

1. Untuk titik singular $\sigma\colon\Delta^0\to X$, tuliskan
   $P_0(\sigma)$ dan periksa
   $\partial P_0(\sigma)=g_\#\sigma-f_\#\sigma$.
2. Untuk lintasan singular $\sigma\colon\Delta^1\to X$, gambarkan dua
   segitiga berorientasi yang membagi $\Delta^1\times I$ dan jelaskan
   pembatalan diagonal bersama.
3. Dualisasikan identitas prisma dan buktikan bahwa $f^*$ dan $g^*$ memberi
   pemetaan kohomologi yang sama.
:::

::: {.hint #o012-rbt-l26-hint-006 data-origin="edition-original"}
**Petunjuk.** Pada derajat nol, prisma adalah lintasan
$t\mapsto H(\sigma,t)$. Pada derajat satu, gunakan urutan titik sudut
$(v_0,0),(v_0,1),(v_1,1)$ dan
$(v_0,0),(v_1,0),(v_1,1)$ dengan tanda berlawanan. Untuk dualisasi, tetapkan
$h\varphi=-\varphi\circ P$.
:::

::: {.solution #o012-rbt-l26-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 26.6.** Jika $\sigma$ sebuah titik singular, hanya ada
satu simpleks pada triangulasi $\Delta^0\times I$. Jadi

$$
P_0(\sigma)(t)=H(\sigma,t).
$$

Batas lintasan berorientasi adalah titik akhir dikurangi titik awal:

$$
\partial P_0(\sigma)
=H(\sigma,1)-H(\sigma,0)
=g_\#\sigma-f_\#\sigma.
$$

Untuk $\sigma\colon\Delta^1\to X$, persegi
$\Delta^1\times I$ dibagi sepanjang diagonal dari $(v_0,0)$ ke $(v_1,1)$.
Dua segitiganya mempunyai daftar titik sudut

$$
(v_0,0),(v_0,1),(v_1,1)
\quad\text{dan}\quad
(v_0,0),(v_1,0),(v_1,1).
$$

Dalam $P_1$ keduanya masuk dengan tanda bergantian. Diagonal bersama muncul
dengan orientasi berlawanan dan lenyap. Sisi atas menyisakan
$g_\#\sigma$, sisi bawah menyisakan $-f_\#\sigma$, dan kedua sisi vertikal
menyusun $-P_0(\partial\sigma)$. Jadi

$$
\partial P_1(\sigma)+P_0(\partial\sigma)
=g_\#\sigma-f_\#\sigma.
$$

Pada semua derajat, identitas yang sama ialah
$\partial P+P\partial=g_\#-f_\#$. Untuk
$\varphi\in C^n(Y;R)$ definisikan
$h_n\varphi=-\varphi\circ P_{n-1}$. Jika $c\in S_n(X;R)$, maka

$$
\begin{aligned}
\bigl((\delta h+h\delta)\varphi\bigr)(c)
&=-\varphi(P\partial c+\partial Pc)\\
&=-\varphi((g_\#-f_\#)c)\\
&=(f^*\varphi-g^*\varphi)(c).
\end{aligned}
$$

Jadi $f^*-g^*=\delta h+h\delta$. Untuk kosiklus $\varphi$, selisih
$f^*\varphi-g^*\varphi$ adalah kobatas $\delta(h\varphi)$, sehingga kedua
korantai menentukan kelas kohomologi yang sama. Dengan demikian,
$H^n(f)=H^n(g)$ untuk setiap $n$.
:::

::: {.boundary #o012-rbt-l26-boundary-001}
**Batas ke Unit 27.** Unit 26 menerjemahkan Notes.tex baris 5612--5823 secara
kontigu dan menutup seluruh objek sumber pada rentang itu. Baris 5824 berbunyi
`Let\lecturenum{27} us consider for a short time again the reduced cohomology
...`, memulai Kuliah 27, dan tidak dimasukkan. Kursor sumber berikutnya yang
tepat adalah **Notes.tex baris 5824**.
:::
