---
title: "Topologi Aljabar"
subtitle: "Komponen Fomberg 2: Homologi Singular dan Invariansi Homotopi"
author:
  - "Yeheli Fomberg (catatan sumber; berdasarkan kuliah Nir Lazarovich)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Sumber dan adaptasi: CC BY-SA 4.0; lihat atribusi dan catatan perubahan di bawah."
source_component: "Fomberg Algebraic Topology, Sections 1.3-1.4"
edition_unit_id: "O012-FOM-002"
course_route_unit_id: "D60-R09"
---

# Tentang komponen ini {.unnumbered #o012-fom-u002-notice data-course-route-unit-id="D60-R09"}

Komponen ini merupakan terjemahan dan adaptasi bahasa Indonesia atas Bagian
1.3–1.4 *Algebraic Topology* karya Yeheli Fomberg, berdasarkan kuliah Nir
Lazarovich pada musim semi 2025. Otoritas sumber dibekukan pada commit
[563194fae879178b9a6871b249513bfc27968975](https://git.sr.ht/~yp/math-notes/tree/563194fae879178b9a6871b249513bfc27968975/item/algebraic_topology.tex).
Rentang yang diterjemahkan ialah baris 615–1290: 676 baris fisik, 22.924 byte
setelah normalisasi LF dan satu LF penutup, dengan SHA-256
9b28e159825e020b262a51b9c50372b2fafc26270fab6480d860aaaeefdda84f.

Catatan sumber tersedia di bawah
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
Terjemahan, pemformatan semantik, koreksi terbatas, tiga perbaikan bukti, dan
materi penguasaan asli di bawah ini diterbitkan dengan lisensi yang sama.
Perubahan dicatat secara eksplisit dalam blok audit dan ledger; tidak ada prosa
dari bank soal Fomberg yang dikecualikan ataupun materi MIT yang disalin.

Edisi ini independen dan tidak menyiratkan dukungan, pengesahan, atau afiliasi
dengan Yeheli Fomberg, Nir Lazarovich, ataupun institusi mereka. Produksi
terjemahan, struktur semantik, dan QA dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna.

# Homologi singular dan invariansi homotopi {#o012-fom-u002}

## Homologi singular {#o012-fom-u002-s03 data-source-lines="615-953"}

::: {.definition #o012-fom-u002-def-singular-simplex data-source-lines="616-619"}
**Definisi (simpleks-$n$ singular).** Misalkan $X$ ruang topologis. Sebuah
**simpleks-$n$ singular** di $X$ ialah pemetaan kontinu

$$
\sigma\colon\Delta^n\longrightarrow X.
$$
:::

::: {.remark #o012-fom-u002-rem-singular-chains data-source-lines="621-639"}
**Catatan (rantai, batas, dan homologi singular).** Untuk mendefinisikan
homologi singular, kita membangun kembali grup rantai dan pemetaan batas.
Definisikan $C_n(X)$ sebagai grup abelian bebas dengan basis semua
simpleks-$n$ singular di $X$. Unsurnya disebut **rantai-$n$ singular**. Grup
ini biasanya sangat besar.

Dengan menuliskan himpunan semua simpleks singular sebagai basis, definisi itu
dapat dicatat secara eksplisit sebagai

$$
C_n(X):=
\mathbb Z\left\langle
\left\{\sigma\colon\Delta^n\to X\mid \sigma\text{ kontinu}\right\}
\right\rangle.
$$

Pada sebuah generator $\sigma$, pemetaan batas didefinisikan oleh

$$
\partial_n(\sigma)
=\sum_{i=0}^{n}(-1)^i\,\sigma|_{\partial_i\Delta^n},
$$

dengan pembatasan pada muka dipahami melalui inklusi afin standar
$\partial_i\Delta^n\cong\Delta^{n-1}$. Operator ini diperluas secara linear.
Siklus $Z_n(X)=\ker\partial_n$, batas
$B_n(X)=\operatorname{im}\partial_{n+1}$, dan grup homologi

$$
H_n(X):=Z_n(X)/B_n(X)
$$

didefinisikan seperti pada homologi simpleksial.

:::

::: {.edition-note #o012-fom-u002-note-boundary-square data-origin="edition-original"}
**Catatan edisi.** Identitas
$\partial_{n-1}\partial_n=0$ mengikuti pembatalan berpasangan muka ganda
yang sama seperti pada Unit Fomberg 001. Karena itu
$B_n(X)\subseteq Z_n(X)$ dan hasil bagi di atas memang terdefinisi.
:::

::: {.source-audit #o012-fom-u002-audit-chain-group}
**Audit sumber.** Baris 626–627 membungkus uraian “grup abelian bebas” dengan
notasi himpunan, dan baris 633–635 tidak mencetak batas indeks penjumlahan.
Edisi menuliskan definisi grup yang bertipe benar, rentang $0\leq i\leq n$,
serta identifikasi muka yang diperlukan.
:::

::: {.lemma #o012-fom-u002-lem-point data-source-lines="641-651"}
**Lema.** Untuk ruang satu titik $X=\{*\}$,

$$
H_n(X)\cong
\begin{cases}
\mathbb Z,&n=0,\\
0,&n\geq1.
\end{cases}
$$
:::

::: {.proof #o012-fom-u002-proof-point data-source-lines="652-707"}
**Bukti.** Dalam setiap derajat terdapat tepat satu simpleks singular, yaitu
pemetaan konstan $\sigma^n\colon\Delta^n\to\{*\}$. Karena itu
$C_n(X)=\mathbb Z\sigma^n$. Pada derajat nol,
$\partial_0(\sigma^0)=0$; untuk $n\geq1$,

$$
\begin{aligned}
\partial_n\sigma^n
&=\sum_{i=0}^{n}(-1)^i
  \underbrace{\sigma^n|_{\partial_i\Delta^n}}_{\sigma^{n-1}}\\
&=
\begin{cases}
\sigma^{n-1},&n\text{ genap},\\
0,&n\text{ ganjil}.
\end{cases}
\end{aligned}
$$

Jadi bagian ujung kompleks rantainya ialah

$$
\cdots\longrightarrow
\mathbb Z\xrightarrow{0}\mathbb Z
\xrightarrow{\mathrm{id}}\mathbb Z
\xrightarrow{0}\mathbb Z\longrightarrow0.
$$

::: {.figure #o012-fom-u002-fig-point-chain data-source-lines="670-690"}
**Diagram semantik (kompleks rantai satu titik).** Dari kanan ke kiri dalam
derajat yang menaik, setiap grup rantai adalah $\mathbb Z$. Diferensial dari
derajat ganjil adalah nol, sedangkan diferensial dari derajat genap positif
adalah identitas; setelah $C_0$ terdapat grup nol.
:::

Pada derajat nol,

$$
H_0(X)
=\frac{\ker\partial_0}{\operatorname{im}\partial_1}
=\frac{\mathbb Z}{0}
\cong\mathbb Z.
$$

Untuk $n\geq1$, kedua kemungkinan paritas memberi, secara berturut-turut,

$$
H_n(X)
=\frac{\ker\partial_n}{\operatorname{im}\partial_{n+1}}
=\frac{0}{0}=0
\quad\text{atau}\quad
H_n(X)
=\frac{\mathbb Z}{\mathbb Z}=0.
$$

Jadi $H_n(X)=0$ pada setiap derajat positif. $\square$
:::

::: {.remark #o012-fom-u002-rem-homeomorphism data-source-lines="709-712"}
**Catatan.** Jika $X$ dan $Y$ homeomorfik, maka
$H_n(X)\cong H_n(Y)$.
:::

::: {.lemma #o012-fom-u002-lem-components data-source-lines="714-718"}
**Lema (dekomposisi menurut komponen terhubung).** Misalkan
$X=\bigsqcup_{\alpha}X_\alpha$, dengan $X_\alpha$ komponen-komponen terhubung
$X$. Maka

$$
H_n(X)\cong\bigoplus_{\alpha}H_n(X_\alpha).
$$
:::

::: {.proof #o012-fom-u002-proof-components data-source-lines="719-739"}
**Bukti.** Citra setiap simpleks singular
$\sigma\colon\Delta^n\to X$ terhubung, sehingga seluruh citranya berada dalam
tepat satu komponen terhubung $X_\alpha$. Karena rantai adalah jumlah
berhingga,

$$
C_n(X)=\bigoplus_\alpha C_n(X_\alpha).
$$

Pemetaan batas mempertahankan setiap suku langsung tersebut. Maka

$$
Z_n(X)=\bigoplus_\alpha Z_n(X_\alpha),
\qquad
B_n(X)=\bigoplus_\alpha B_n(X_\alpha),
$$

dan

$$
H_n(X)=Z_n(X)/B_n(X)
\cong\bigoplus_\alpha H_n(X_\alpha).
$$

$\square$
:::

::: {.corollary #o012-fom-u002-cor-path-components data-origin="edition-original"}
**Penguatan edisi (komponen lintasan).** Jika
$X=\bigsqcup_\beta P_\beta$ adalah dekomposisi ke dalam komponen lintasan,
maka

$$
H_n(X)\cong\bigoplus_\beta H_n(P_\beta).
$$

Memang, $\Delta^n$ terhubung lintasan, sehingga citra setiap simpleks singular
termuat dalam tepat satu $P_\beta$; pembuktian jumlah langsung di atas berlaku
tanpa perubahan. $\square$
:::

::: {.source-audit #o012-fom-u002-audit-components}
**Audit sumber.** Pernyataan pada baris 715 menyebut komponen terhubung,
sedangkan bukti pada baris 722 menyebut komponen lintasan. Kedua dekomposisi
sah: keterhubungan citra simpleks membuktikan pernyataan sumber, dan
keterhubungan lintasan citranya memberi penguatan yang diperlukan untuk akibat
$H_0$. Edisi mempertahankan keduanya sebagai objek terpisah. Selain itu, ruas
kiri baris 736 salah tercetak sebagai $H_n(X_\alpha)$; ruas kiri yang benar
ialah $H_n(X)$.
:::

::: {.lemma #o012-fom-u002-lem-hzero data-source-label="lem:path-connected-then-hzero-z" data-source-lines="741-745"}
**Lema.** Jika $X$ tak kosong dan terhubung lintasan, maka
$H_0(X)\cong\mathbb Z$.
:::

::: {.proof #o012-fom-u002-proof-hzero-first data-source-lines="746-762"}
**Bukti pertama.** Karena $\partial_0=0$,

$$
H_0(X)=\frac{\ker\partial_0}{\operatorname{im}\partial_1}
=\frac{C_0(X)}{\operatorname{im}\partial_1}.
$$

Generator $C_0(X)$ adalah titik-titik $X$, dipandang sebagai simpleks-$0$
singular. Untuk setiap dua titik $x,y\in X$, pilih
lintasan $\tau$ dari $x$ ke $y$. Sebagai simpleks-$1$ singular,
$\partial_1\tau=y-x$. Jadi, modulo $\operatorname{im}\partial_1$, semua
generator $C_0(X)$ mewakili satu kelas $u$.

Augmentasi jumlah-koefisien bernilai nol pada setiap batas
$\partial_1\tau$, sehingga menginduksi
$\bar\varepsilon\colon H_0(X)\to\mathbb Z$ dengan
$\bar\varepsilon(u)=1$. Homomorfisma
$\mathbb Z\to H_0(X)$ yang mengirim $1$ ke $u$ surjektif, dan kompositnya
dengan $\bar\varepsilon$ adalah identitas. Karena itu homomorfisma tersebut
juga injektif, dan

$$
H_0(X)=\frac{\ker\partial_0}{\operatorname{im}\partial_1}
\cong\mathbb Z.
$$

$\square$
:::

::: {.corollary #o012-fom-u002-cor-hzero-components data-source-lines="764-768"}
**Akibat.** Untuk setiap ruang topologis $X$, grup $H_0(X)$ adalah jumlah
langsung salinan $\mathbb Z$, satu salinan bagi setiap komponen lintasan $X$.
:::

::: {.remark #o012-fom-u002-rem-augmentation-motivation data-source-lines="770-774"}
**Catatan.** Bukti berikut memberi bentuk yang lebih formal bagi
[lema $H_0$ untuk ruang terhubung lintasan](#o012-fom-u002-lem-hzero)
dan memotivasi homologi tereduksi.
:::

::: {.proof #o012-fom-u002-proof-hzero-augmentation data-source-lines="776-830"}
**Bukti kedua [Lema $H_0$](#o012-fom-u002-lem-hzero).** Pertimbangkan bagian kompleks

$$
C_1(X)\xrightarrow{\partial_1}C_0(X)\longrightarrow0.
$$

::: {.figure #o012-fom-u002-fig-hzero-sequence data-source-lines="778-783"}
**Diagram semantik (ujung kompleks derajat nol).** Panah
$C_1(X)\xrightarrow{\partial_1}C_0(X)$ diikuti pemetaan nol
$C_0(X)\to0$. Karena panah keluar dari $C_0(X)$ nol, seluruh $C_0(X)$ adalah
siklus derajat nol.
:::

Karena $\partial_0=0$,

$$
H_0(X)=C_0(X)/\operatorname{im}\partial_1.
$$

Definisikan homomorfisma augmentasi

$$
\varepsilon\colon C_0(X)\longrightarrow\mathbb Z,
\qquad
\varepsilon\!\left(\sum_i n_i\sigma_i\right)=\sum_i n_i.
$$

Pemetaan ini surjektif karena $X$ tak kosong. Untuk simpleks-$1$ singular
$\tau$,

$$
\varepsilon(\partial_1\tau)
=\varepsilon(\tau(1)-\tau(0))=1-1=0,
$$

sehingga $\operatorname{im}\partial_1\subseteq\ker\varepsilon$.

Sebaliknya, ambil $\sum_i n_i\sigma_i\in\ker\varepsilon$ dan pilih titik basis
$x_0\in X$. Karena $X$ terhubung lintasan, untuk setiap $i$ ada lintasan
$\tau_i$ dari $x_0$ ke titik yang diwakili $\sigma_i$. Jika $\sigma_0$
menyatakan simpleks-$0$ pada $x_0$, maka
$\partial\tau_i=\sigma_i-\sigma_0$. Karena $\sum_i n_i=0$,

$$
\varepsilon\!\left(\sum_i n_i\sigma_i\right)=\sum_i n_i=0,
$$

dan

$$
\partial_1\!\left(\sum_i n_i\tau_i\right)
=\sum_i n_i\sigma_i-\left(\sum_i n_i\right)\sigma_0
=\sum_i n_i\sigma_i.
$$

Jadi $\ker\varepsilon\subseteq\operatorname{im}\partial_1$. Teorema
isomorfisma pertama kini memberi

$$
H_0(X)
=\frac{C_0(X)}{\operatorname{im}\partial_1}
=\frac{C_0(X)}{\ker\varepsilon}
\cong\mathbb Z.
$$

$\square$
:::

::: {.definition #o012-fom-u002-def-chain-complex data-source-lines="832-843"}
**Definisi (kompleks rantai).** Sebuah **kompleks rantai** ialah barisan grup
abelian dan homomorfisma

$$
\cdots\longrightarrow A_2\xrightarrow{\partial_2}
A_1\xrightarrow{\partial_1}A_0\longrightarrow\cdots
$$

sedemikian sehingga
$\partial_n\circ\partial_{n+1}=0$ untuk setiap $n$.
:::

::: {.figure #o012-fom-u002-fig-chain-complex data-source-lines="834-840"}
**Diagram semantik (kompleks rantai umum).** Barisan berarah
$\cdots\to A_2\xrightarrow{\partial_2}A_1
\xrightarrow{\partial_1}A_0\to\cdots$ mempunyai komposit dua panah berturutan
yang selalu nol.
:::

::: {.remark #o012-fom-u002-rem-boundary-square data-source-lines="844-847"}
**Catatan.** Syarat itu sering ditulis $\partial^2=0$.
:::

::: {.remark #o012-fom-u002-rem-image-kernel data-source-lines="848-851"}
**Catatan.** Persamaan $\partial_n\partial_{n+1}=0$ ekuivalen dengan

$$
\operatorname{im}\partial_{n+1}\subseteq\ker\partial_n,
$$

yakni setiap batas merupakan siklus.
:::

::: {.remark #o012-fom-u002-rem-augmented-complex data-source-lines="853-866"}
**Catatan (kompleks teraugmentasi).** Pemetaan $\varepsilon$ yang muncul dalam
[bukti kedua Lema $H_0$](#o012-fom-u002-lem-hzero) memperpanjang
kompleks rantai singular menjadi

$$
\cdots\longrightarrow C_2(X)\xrightarrow{\partial_2}
C_1(X)\xrightarrow{\partial_1}C_0(X)
\xrightarrow{\varepsilon}\mathbb Z\longrightarrow0.
$$

Barisan ini disebut **kompleks rantai teraugmentasi**.
:::

::: {.figure #o012-fom-u002-fig-augmented-chain-1 data-source-lines="857-864"}
**Diagram semantik (augmentasi pertama).** Kompleks singular
$\cdots\to C_2(X)\to C_1(X)\to C_0(X)$ diperpanjang oleh
$C_0(X)\xrightarrow{\varepsilon}\mathbb Z\to0$; jumlah koefisien setiap batas
derajat satu adalah nol.
:::

::: {.definition #o012-fom-u002-def-reduced-homology data-source-lines="868-885"}
**Definisi (grup homologi tereduksi).** Untuk ruang tak kosong $X$, gunakan
augmentasi dari [Lema $H_0$](#o012-fom-u002-lem-hzero). Grup
homologi tereduksi $\widetilde H_n(X)$ didefinisikan sebagai homologi kompleks
rantai teraugmentasi

$$
\cdots\longrightarrow C_2(X)\xrightarrow{\partial_2}
C_1(X)\xrightarrow{\partial_1}C_0(X)
\xrightarrow{\varepsilon}\mathbb Z\longrightarrow0.
$$

Syarat tak kosong menghindari grup homologi
taktrivial pada derajat $-1$. Dalam konvensi ini, ruang satu titik mempunyai
homologi tereduksi nol pada semua derajat.
:::

::: {.figure #o012-fom-u002-fig-augmented-chain-2 data-source-lines="871-878"}
**Diagram semantik (augmentasi dalam definisi).** Ini adalah kemunculan kedua
kompleks teraugmentasi pada sumber: $C_0(X)$ dipetakan ke $\mathbb Z$ oleh
jumlah koefisien dan kemudian ke nol. Homologi kompleks inilah yang
didefinisikan sebagai homologi tereduksi.
:::

::: {.remark #o012-fom-u002-rem-reduced-relation data-source-lines="887-897"}
**Catatan.** Untuk ruang tak kosong $X$,

$$
H_n(X)\cong
\begin{cases}
\widetilde H_n(X),&n\geq1,\\
\widetilde H_0(X)\oplus\mathbb Z,&n=0.
\end{cases}
$$

Khususnya, jika $X$ terhubung lintasan, maka
$\widetilde H_0(X)=0$.
:::

::: {.remark #o012-fom-u002-rem-reduced-splitting data-source-lines="898-904"}
**Catatan (pemisahan pada derajat nol).**
Pada derajat nol, augmentasi menginduksi surjeksi
$\varepsilon_*\colon H_0(X)\to\mathbb Z$ dengan kernel
$\widetilde H_0(X)$. Memilih satu titik basis $x_0\in X$ memberi pemisahan
$1\mapsto[x_0]$; karena itu diperoleh jumlah langsung di atas. Pilihan
pemisahan ini tidak kanonik jika tidak ada titik basis yang telah dipilih.
:::

::: {.source-audit #o012-fom-u002-audit-reduced-splitting}
**Audit sumber.** Baris 899–903 menyatakan pemisahan setelah “beberapa
manipulasi”, tanpa menyebut pemetaan pemisah atau pilihan titik. Edisi
menuliskan barisan augmentasi, kernelnya, dan pemisahan yang diperlukan.
:::

::: {.remark #o012-fom-u002-rem-empty-simplex data-source-lines="906-912"}
**Catatan.** Secara formal, salinan tambahan $\mathbb Z$ dapat dipandang
sebagai grup bebas yang dibangkitkan oleh satu-satunya pemetaan
$[\varnothing]\to X$, dengan $[\varnothing]$ simpleks kosong tanpa simpul.
Augmentasi lalu merupakan pemetaan batas biasa karena
$\partial[v_0]=[\widehat v_0]=[\varnothing]$.
:::

::: {.remark #o012-fom-u002-rem-geometric data-source-lines="914-952"}
**Catatan (interpretasi geometris yang terbatas).** Ambil siklus umum

$$
c=\sum_\sigma n_\sigma\sigma\in Z_n(X).
$$

Sebagai contoh, untuk $n=1$ tulis
$c=\sum_e n_e e\in Z_1(X)$. Persamaan $\partial c=0$ mengatakan bahwa pada
setiap titik, jumlah berarah koefisien sisi yang masuk sama dengan jumlah yang
keluar.

::: {.figure #o012-fom-u002-fig-flow-balance data-source-lines="920-937"}
**Gambar semantik (keseimbangan pada simpul).** Pada sebuah simpul pusat tanpa
label, tiga sisi berorientasi $e'_1,e'_2,e'_3$ masuk dari kiri dan tiga sisi berorientasi
$e_1,e_2,e_3$ keluar ke kanan. Persamaan $\partial c=0$ menyamakan jumlah
koefisien berarah yang masuk dan keluar di simpul tersebut; gambar tidak
mengklaim bahwa lingkungannya merupakan manifold-$1$.
:::

Jika koefisien diambil dalam $\mathbb R$, keseimbangan ini menyerupai hukum
arus Kirchhoff. Namun kondisi itu adalah kondisi aljabar, bukan dengan
sendirinya syarat manifold. Sebuah simpul bercabang dapat memenuhi
$\partial c=0$ tanpa mempunyai lingkungan seperti interval. Demikian pula,
siklus-$2$ umum tidak harus merupakan permukaan tertutup, dan rantai yang bukan
siklus tidak otomatis merealisasikan manifold berbatas; diperlukan syarat
insidensi dan lokal tambahan. Dalam dimensi lebih tinggi, rantai seimbang
sering lebih tepat dipandang sebagai siklus atau pseudomanifold berbobot.
:::

::: {.source-audit #o012-fom-u002-audit-geometric-heuristic}
**Audit sumber.** Baris 938 menyebut “hukum kedua Kirchhoff”, padahal
keseimbangan arus pada simpul adalah hukum arus (hukum pertama) Kirchhoff.
Baris 942–948 juga menyimpulkan bahwa rantai seimbang mesti merupakan
manifold-$1$ tertutup, bahwa siklus-$2$ mesti merupakan permukaan tertutup, dan
bahwa rantai nonsiklus menghasilkan manifold berbatas. Ketiga implikasi gagal
tanpa hipotesis insidensi dan lokal tambahan. Baris 949–951 menyebut hanya
pseudomanifold dalam dimensi lebih tinggi tanpa merumuskan syaratnya. Edisi
mempertahankan intuisi keseimbangan, menghindari insidensi nonmanifold, dan
membatasi klaimnya ke konsekuensi aljabar yang sah.
:::

## Invariansi homotopi {#o012-fom-u002-s04 data-source-lines="954-1290"}

::: {.definition #o012-fom-u002-def-induced-chain-map data-source-lines="956-978"}
**Definisi (pemetaan pada rantai).** Misalkan $f\colon X\to Y$ kontinu. Setiap
simpleks singular $\sigma\colon\Delta^n\to X$ menghasilkan simpleks singular
$f\circ\sigma\colon\Delta^n\to Y$. Definisikan homomorfisma

$$
f_\#\colon C_n(X)\longrightarrow C_n(Y)
$$

pada generator dengan $f_\#(\sigma)=f\circ\sigma$, lalu perluas secara
linear. Untuk semua derajat, pemetaan tersebut tersusun sebagai

$$
\begin{array}{ccccccccc}
\cdots&\longrightarrow&C_{n+1}(X)&\xrightarrow{\partial}&C_n(X)
&\xrightarrow{\partial}&C_{n-1}(X)&\longrightarrow&\cdots\\
&&\downarrow f_\#&&\downarrow f_\#&&\downarrow f_\#&&\\
\cdots&\longrightarrow&C_{n+1}(Y)&\xrightarrow{\partial}&C_n(Y)
&\xrightarrow{\partial}&C_{n-1}(Y)&\longrightarrow&\cdots.
\end{array}
$$
:::

::: {.figure #o012-fom-u002-fig-induced-chain-map-1 data-source-lines="962-977"}
**Diagram semantik (pemetaan derajat demi derajat).** Baris atas adalah
kompleks $C_\bullet(X)$ dan baris bawah $C_\bullet(Y)$. Pada setiap derajat,
panah vertikal $f_\#$ mengirim $\sigma$ ke $f\circ\sigma$; panah horizontal
adalah pemetaan batas.
:::

::: {.proposition #o012-fom-u002-prop-chain-map data-source-lines="980-1000"}
**Proposisi.** Pemetaan $f_\#$ berkomutasi dengan pemetaan batas:

$$
f_\#\circ\partial=\partial\circ f_\#.
$$

Dengan kata lain, setiap persegi pada diagram di atas komutatif.
:::

::: {.figure #o012-fom-u002-fig-induced-chain-map-2 data-source-lines="983-999"}
**Diagram semantik (persegi rantai komutatif).** Sumber mengulang kedua
kompleks dan semua panah $f_\#$ untuk menegaskan bahwa menuruni diagram lalu
mengambil batas sama dengan mengambil batas lalu menuruni diagram:
$\partial f_\#=f_\#\partial$.
:::

::: {.source-omission #o012-fom-u002-omission-pr01 data-source-lines="1001-1003" data-repair-id="FOM-PR-01"}
**Bagian yang dihilangkan dalam sumber.** Bukti sumber hanya berbunyi “Dalam pekerjaan
rumah.” Bukti lengkap edisi diberikan berikut ini.
:::

::: {.proof #o012-fom-u002-proof-chain-map data-origin="edition-original" data-repair-id="FOM-PR-01"}
**Perbaikan bukti FOM-PR-01.** Cukup periksa sebuah generator
$\sigma\colon\Delta^n\to X$. Jika
$\delta_i\colon\Delta^{n-1}\to\Delta^n$ adalah inklusi afin muka ke-$i$,
maka

$$
\begin{aligned}
\partial f_\#(\sigma)
&=\partial(f\circ\sigma)\\
&=\sum_{i=0}^{n}(-1)^i(f\circ\sigma)\circ\delta_i\\
&=f_\#\!\left(\sum_{i=0}^{n}(-1)^i\sigma\circ\delta_i\right)\\
&=f_\#(\partial\sigma).
\end{aligned}
$$

Kedua ruas linear terhadap $\sigma$, sehingga identitas berlaku pada seluruh
$C_n(X)$. $\square$
:::

::: {.definition #o012-fom-u002-def-chain-map data-source-lines="1005-1009"}
**Definisi (pemetaan rantai).** Kumpulan homomorfisma $f_\#$ di semua derajat
disebut **pemetaan rantai**. Secara umum, pemetaan rantai ialah kumpulan homomorfisma
antar-kompleks rantai yang berkomutasi dengan pemetaan batas.
:::

::: {.proposition #o012-fom-u002-prop-induced-map data-source-lines="1011-1014"}
**Proposisi.** Pemetaan rantai $f_\#$ menginduksi homomorfisma yang terdefinisi
dengan baik

$$
f_*\colon H_n(X)\longrightarrow H_n(Y),
\qquad
f_*([z])=[f_\#(z)].
$$
:::

::: {.proof #o012-fom-u002-proof-induced-map-source data-source-lines="1015-1033"}
**Bukti dari sumber, sampai titik yang diberikannya.** Jika
$z\in Z_n(X)$, maka

$$
\partial f_\#(z)=f_\#(\partial z)=f_\#(0)=0,
$$

sehingga $f_\#(z)\in Z_n(Y)$. Jika $b\in B_n(X)$, tulis
$b=\partial c$ untuk suatu $c\in C_{n+1}(X)$. Maka

$$
f_\#(b)=f_\#(\partial c)=\partial f_\#(c)\in B_n(Y).
$$

Jadi siklus dibawa ke siklus dan batas dibawa ke batas. Jika
$[z]=[z']$, maka $z-z'\in B_n(X)$, sehingga
$f_\#(z)-f_\#(z')\in B_n(Y)$; karena itu rumus $f_*([z])=[f_\#(z)]$
tidak bergantung pada wakil.
:::

::: {.source-omission #o012-fom-u002-omission-pr02 data-source-lines="1034-1034" data-repair-id="FOM-PR-02"}
**Bagian yang dihilangkan dalam sumber.** Sumber menyatakan bahwa pemeriksaan
sifat homomorfisma dibiarkan kepada pembaca. Perbaikan lengkap edisi diberikan
berikut ini.
:::

::: {.proof #o012-fom-u002-proof-induced-map-homomorphism data-origin="edition-original" data-repair-id="FOM-PR-02"}
**Perbaikan bukti FOM-PR-02.** Sumber secara eksplisit menghilangkan
pemeriksaan bahwa $f_*$ merupakan homomorfisma. Untuk $[z],[w]\in H_n(X)$,
linearitas $f_\#$ memberi

$$
\begin{aligned}
f_*([z]+[w])
&=f_*([z+w])\\
&=[f_\#(z+w)]\\
&=[f_\#(z)+f_\#(w)]\\
&=f_*([z])+f_*([w]).
\end{aligned}
$$

Pemetaan juga membawa kelas nol ke kelas nol dan invers aditif ke invers
aditif. Jadi $f_*$ adalah homomorfisma. $\square$
:::

::: {.remark #o012-fom-u002-rem-induced-map data-source-lines="1036-1038"}
**Catatan.** Homomorfisma $f_*$ disebut **pemetaan yang diinduksi oleh $f$**.
:::

::: {.proposition #o012-fom-u002-prop-functoriality data-source-label="prp:functoriality-of-induced-maps" data-source-lines="1040-1054"}
**Proposisi (fungtorialitas pemetaan terinduksi).** Untuk pemetaan kontinu
$X\xrightarrow{g}Y\xrightarrow{f}Z$,

1. $(f\circ g)_*=f_*\circ g_*$; dan
2. $(\operatorname{id}_X)_*=\operatorname{id}_{H_n(X)}$.
:::

::: {.figure #o012-fom-u002-fig-functoriality data-source-lines="1043-1048"}
**Diagram semantik (pemetaan yang dapat dikomposisikan).** Tiga ruang tersusun
$X\xrightarrow{g}Y\xrightarrow{f}Z$. Pemetaan pada homologi mengikuti arah
yang sama, dan panah komposit menginduksi $f_*\circ g_*$.
:::

::: {.proof #o012-fom-u002-proof-functoriality data-origin="edition-original"}
**Bukti edisi.** Pada setiap generator $\sigma$,

$$
(f\circ g)_\#(\sigma)=f\circ g\circ\sigma
=f_\#(g_\#(\sigma)),
$$

dan $(\operatorname{id}_X)_\#(\sigma)=\sigma$. Linearitas memberi identitas
yang sama pada rantai, lalu pengambilan kelas homologi memberi kedua rumus
yang diklaim. $\square$
:::

::: {.corollary #o012-fom-u002-cor-homeomorphism data-source-lines="1055-1058"}
**Akibat.** Jika $X$ dan $Y$ homeomorfik, maka
$H_n(X)\cong H_n(Y)$.
:::

::: {.proof #o012-fom-u002-proof-homeomorphism data-origin="edition-original"}
**Bukti edisi.** Jika $h\colon X\to Y$ homeomorfisma dengan invers $k$, maka
fungtorialitas memberi
$k_*h_*=(k\circ h)_*=\operatorname{id}_{H_n(X)}$ dan
$h_*k_*=(h\circ k)_*=\operatorname{id}_{H_n(Y)}$. Jadi $h_*$ isomorfisma
dengan invers $k_*$. $\square$
:::

::: {.corollary #o012-fom-u002-cor-retract data-source-label="cor:injective-i-surjective-r" data-source-lines="1060-1065"}
**Akibat.** Misalkan $A\subseteq X$ suatu retrak dari $X$. Jika
$i\colon A\hookrightarrow X$ adalah inklusi dan $r\colon X\to A$ suatu
retraksi, maka

$$
i_*\colon H_n(A)\longrightarrow H_n(X)
$$

injektif, sedangkan

$$
r_*\colon H_n(X)\longrightarrow H_n(A)
$$

surjektif.
:::

::: {.proof #o012-fom-u002-proof-retract data-source-lines="1066-1088"}
**Bukti.** Inklusi dan retraksi membentuk segitiga berikut.

::: {.figure #o012-fom-u002-fig-retract-spaces data-source-lines="1067-1074"}
**Diagram semantik (segitiga retraksi).** Inklusi
$i\colon A\to X$ diikuti retraksi $r\colon X\to A$ sama dengan
$\operatorname{id}_A$. Segitiga ruang ini komutatif.
:::

Setelah mengambil homologi, diperoleh segitiga yang bersesuaian.

::: {.figure #o012-fom-u002-fig-retract-homology data-source-lines="1077-1083"}
**Diagram semantik (segitiga pada homologi).** Pemetaan
$H_n(A)\xrightarrow{i_*}H_n(X)\xrightarrow{r_*}H_n(A)$ berkomposisi menjadi
identitas $H_n(A)$.
:::

Karena $r\circ i=\operatorname{id}_A$,
[fungtorialitas pemetaan terinduksi](#o012-fom-u002-prop-functoriality) memberi

$$
r_*\circ i_*=(r\circ i)_*
=(\operatorname{id}_A)_*
=\operatorname{id}_{H_n(A)}.
$$

Pemetaan yang mempunyai invers kiri bersifat injektif, jadi $i_*$ injektif;
pemetaan yang mempunyai invers kanan bersifat surjektif, jadi $r_*$
surjektif. $\square$
:::

::: {.corollary #o012-fom-u002-cor-endpoints-not-retract data-source-lines="1090-1092"}
**Akibat.** Subruang $\{0,1\}\subseteq[0,1]$ bukan retrak.
:::

::: {.proof #o012-fom-u002-proof-endpoints-not-retract data-source-lines="1093-1100"}
**Bukti.** Andaikan ada retraksi.
[Akibat tentang retrak](#o012-fom-u002-cor-retract) menyatakan bahwa inklusi
menginduksi monomorfisma

$$
i_*\colon H_0(\{0,1\})\longrightarrow H_0([0,1]).
$$

Namun grup asal isomorfik dengan $\mathbb Z\oplus\mathbb Z$, sedangkan grup
tujuan isomorfik dengan $\mathbb Z$. Tidak ada homomorfisma injektif
$\mathbb Z^2\to\mathbb Z$: setelah ditensor dengan $\mathbb Q$, hal itu akan
memberi pemetaan linear injektif $\mathbb Q^2\to\mathbb Q$. Kontradiksi.
$\square$
:::

::: {.theorem #o012-fom-u002-thm-homotopy-invariance data-source-label="thm:homotopic-maps-induce-same-homomorphism-on-homology" data-source-lines="1102-1107"}
**Teorema (invariansi homotopi).** Jika pemetaan kontinu
$f,g\colon X\to Y$ homotopik, maka

$$
f_*=g_*\colon H_n(X)\longrightarrow H_n(Y)
$$

untuk setiap $n\geq0$.
:::

::: {.definition #o012-fom-u002-def-homotopy-equivalence data-source-lines="1109-1120"}
**Definisi (ekuivalensi homotopi).** Pemetaan kontinu $f\colon X\to Y$
disebut **ekuivalensi homotopi** jika ada pemetaan kontinu $g\colon Y\to X$
sedemikian sehingga

$$
f\circ g\simeq\operatorname{id}_Y,
\qquad
g\circ f\simeq\operatorname{id}_X.
$$

Jika ekuivalensi semacam itu ada, $X$ dan $Y$ disebut **ekuivalen secara
homotopi**, atau mempunyai tipe homotopi yang sama, dan ditulis
$X\simeq Y$.
:::

::: {.corollary #o012-fom-u002-cor-homotopy-equivalent data-source-label="cor:homotopy-equivalent-implies-same-homology" data-source-lines="1121-1125"}
**Akibat.** Jika $X\simeq Y$, maka $H_n(X)\cong H_n(Y)$ untuk setiap $n$.
:::

::: {.source-omission #o012-fom-u002-omission-pr03 data-source-lines="1126-1128" data-repair-id="FOM-PR-03"}
**Bagian yang dihilangkan dalam sumber.** Bukti sumber hanya berbunyi “Dalam pekerjaan
rumah.” Bukti lengkap edisi diberikan berikut ini.
:::

::: {.proof #o012-fom-u002-proof-homotopy-equivalent data-origin="edition-original" data-repair-id="FOM-PR-03"}
**Perbaikan bukti FOM-PR-03.** Pilih ekuivalensi homotopi
$f\colon X\to Y$ dan invers homotopinya $g\colon Y\to X$. Teorema invariansi
homotopi dan fungtorialitas memberi

$$
g_*\circ f_*=(g\circ f)_*
=(\operatorname{id}_X)_*
=\operatorname{id}_{H_n(X)}
$$

serta

$$
f_*\circ g_*=(f\circ g)_*
=(\operatorname{id}_Y)_*
=\operatorname{id}_{H_n(Y)}.
$$

Jadi $f_*$ dan $g_*$ saling invers; khususnya
$H_n(X)\cong H_n(Y)$. $\square$
:::

::: {.example #o012-fom-u002-exa-euclidean data-source-lines="1130-1147"}
**Contoh.** Ruang $\mathbb R^n$ ekuivalen secara homotopi dengan satu titik.
Ambil $f\colon\mathbb R^n\to\{*\}$ sebagai pemetaan tunggal dan
$g\colon\{*\}\to\mathbb R^n$ dengan $g(*)=0$. Menurut
[akibat ekuivalensi homotopi](#o012-fom-u002-cor-homotopy-equivalent), cukup
memeriksa kedua komposit. Komposit $f\circ g$ adalah
identitas pada $\{*\}$, sedangkan $g\circ f$ homotopik ke identitas
$\mathbb R^n$ melalui kontraksi linear $H(x,t)=(1-t)x$. Maka

$$
H_k(\mathbb R^n)\cong H_k(\{*\})\cong
\begin{cases}
\mathbb Z,&k=0,\\
0,&k\geq1.
\end{cases}
$$
:::

::: {.source-audit #o012-fom-u002-audit-euclidean-map}
**Audit sumber.** Baris 1134 memakai tanda $\mapsto$ pada deklarasi pemetaan,
dan baris 1135 mencetak $g\colon\{*\}\to0$ alih-alih
$g\colon\{*\}\to\mathbb R^n$ dengan nilai $0$. Baris 1140–1141 juga memakai
kesamaan literal bagi grup yang hanya diidentifikasi hingga isomorfisma.
Edisi membetulkan tipe pemetaan dan memakai $\cong$.
:::

::: {.remark #o012-fom-u002-rem-return-to-proof data-source-lines="1148-1153"}
**Catatan.** Untuk memakai homologi singular secara efektif, kita sekarang
membuktikan [Teorema invariansi homotopi](#o012-fom-u002-thm-homotopy-invariance).
:::

::: {.proof #o012-fom-u002-proof-homotopy-invariance data-source-lines="1155-1275"}
**Bukti [Teorema invariansi homotopi](#o012-fom-u002-thm-homotopy-invariance).**
Kita akan membangun keluarga homomorfisma berderajat $+1$

$$
P_n\colon C_n(X)\longrightarrow C_{n+1}(Y)
$$

::: {.figure #o012-fom-u002-fig-chain-homotopy data-source-lines="1158-1174"}
**Diagram semantik (homotopi rantai).** Dua baris ialah kompleks
$C_\bullet(X)$ dan $C_\bullet(Y)$. Panah vertikal dari derajat $k$ ke derajat
$k$ berlabel $g_\#-f_\#$, sedangkan panah diagonal
$P_k\colon C_k(X)\to C_{k+1}(Y)$ menaikkan derajat satu. Hubungan seluruh
diagram ialah $g_\#-f_\#=\partial P+P\partial$.
:::

Secara umum, jika $p,q\colon C_\bullet\to D_\bullet$ adalah pemetaan rantai,
keluarga homomorfisma berderajat $+1$,
$P_n\colon C_n\to D_{n+1}$, yang memenuhi

$$
q-p=\partial P+P\partial
$$

disebut **homotopi rantai dari $p$ ke $q$**. Dalam bukti ini,
$p=f_\#$ dan $q=g_\#$, sehingga identitas yang harus dibangun ialah

$$
g_\#-f_\#=\partial P+P\partial.
$$

Jika $z\in Z_n(X)$, maka $\partial z=0$ dan

$$
g_\#(z)-f_\#(z)=\partial P(z)+P(\partial z)=\partial P(z)
\in B_n(Y).
$$

Jadi $g_*([z])=f_*([z])$. Dengan demikian cukup membangun $P$.

Pilih homotopi $H\colon X\times I\to Y$ dengan
$H(x,0)=f(x)$ dan $H(x,1)=g(x)$. Untuk simpleks singular
$\sigma\colon\Delta^n\to X$, pascakomposisi biasa dapat digambarkan sebagai
berikut.

::: {.figure #o012-fom-u002-fig-composition data-source-lines="1198-1204"}
**Diagram semantik (pascakomposisi).** Segitiga komutatif mempunyai
$\Delta^n\xrightarrow{\sigma}X\xrightarrow{f}Y$ pada dua sisinya dan
$\Delta^n\xrightarrow{f\circ\sigma}Y$ pada sisi diagonal.
:::

Homotopi menghasilkan pemetaan

$$
H\circ(\sigma\times\operatorname{id}_I)
\colon\Delta^n\times I\longrightarrow Y
$$

::: {.figure #o012-fom-u002-fig-homotopy-prism data-source-lines="1206-1212"}
**Diagram semantik (prisma homotopi).** Segitiga komutatif mempunyai
$\Delta^n\times I\xrightarrow{\sigma\times\operatorname{id}_I}X\times I$
dan $X\times I\xrightarrow{H}Y$ pada dua sisinya; diagonalnya adalah komposit
$H\circ(\sigma\times\operatorname{id}_I)$.
:::

Domain pemetaan ini adalah sebuah prisma. Tulis
$v_i=(e_i,0)$ dan $w_i=(e_i,1)$. Prisma $\Delta^n\times I$ mempunyai
triangulasi standar oleh $n+1$ simpleks

$$
[v_0,\ldots,v_i,w_i,\ldots,w_n],
\qquad 0\leq i\leq n.
$$

Misalkan
$p_i\colon\Delta^{n+1}\to\Delta^n\times I$ pemetaan afin yang berurutan
membawa simpul-simpul standar ke
$v_0,\ldots,v_i,w_i,\ldots,w_n$. Definisikan **operator prisma**

$$
P_n(\sigma)
=\sum_{i=0}^{n}(-1)^i
H\circ(\sigma\times\operatorname{id}_I)\circ p_i,
$$

lalu perluas secara linear.

Hitung batas pada tiap simpleks prisma:

$$
\partial P_n(\sigma)
=\sum_{i=0}^{n}\sum_{j=0}^{n+1}
(-1)^{i+j}
H\circ(\sigma\times\operatorname{id}_I)\circ p_i\circ\delta_j.
$$

Untuk $1\leq i\leq n$, muka dalam yang dipakai bersama oleh simpleks ke-$i-1$
dan ke-$i$ ialah

$$
[v_0,\ldots,v_{i-1},w_i,\ldots,w_n].
$$

Pada simpleks ke-$i-1$, muka ini diperoleh dengan menghapus $w_{i-1}$ pada
posisi $i$ dan mempunyai tanda total
$(-1)^{i-1}(-1)^i=-1$. Pada simpleks ke-$i$, muka yang sama diperoleh dengan
menghapus $v_i$ pada posisi $i$ dan mempunyai tanda total
$(-1)^i(-1)^i=+1$. Jadi semua muka dalam saling meniadakan berpasangan.

Muka $p_0\circ\delta_0=[w_0,\ldots,w_n]$ mempunyai tanda $+1$ dan memberi
$g_\#(\sigma)$. Muka
$p_n\circ\delta_{n+1}=[v_0,\ldots,v_n]$ mempunyai tanda $-1$ dan memberi
$-f_\#(\sigma)$. Setelah muka-muka tersebut dikeluarkan, untuk setiap
$0\leq j\leq n$ muka yang menghapus $v_j$ atau $w_j$ menyusun tepat prisma
bertanda atas $\sigma\circ\delta_j$; reindeksasi tanda
$(-1)^i(-1)^j$ memberi jumlah
$-P_{n-1}\bigl((-1)^j\sigma\circ\delta_j\bigr)$. Menjumlahkan terhadap $j$
memberi $-P_{n-1}(\partial\sigma)$. Karena itu

$$
\partial P_n(\sigma)
=g_\#(\sigma)-f_\#(\sigma)-P_{n-1}(\partial\sigma),
$$

atau ekuivalen,

$$
\partial P+P\partial=g_\#-f_\#.
$$

Identitas ini berlaku pada generator, maka berlaku pada semua rantai. Argumen
pada awal bukti sekarang memberi $f_*=g_*$ pada setiap derajat. $\square$
:::

::: {.source-audit #o012-fom-u002-audit-prism-indices}
**Audit sumber.** Baris 1210 menuliskan $\sigma\times[0,1]$ seolah-olah
sebuah pemetaan; edisi memakai
$\sigma\times\operatorname{id}_I$. Pada baris 1231–1249, indeks penjumlahan
seperti $\sum_{j\leq i}^{n}$ tidak mempunyai batas bawah dan uraian “ketika
$i=j$ suku-suku hampir saling menghapus” mencampur muka ujung dengan muka
dalam. Edisi menyatakan pemetaan afin $p_i$, menuliskan jumlah batas yang
berindeks lengkap, dan mengelompokkan muka bawah, atas, samping, serta muka
dalam dengan tanda yang benar. Baris 1188 membalik tanda $g_\#-f_\#$ menjadi
$f_*-g_*$; kesimpulan kesamaan tidak berubah, tetapi edisi menjaga tanda tetap
konsisten.
:::

::: {.corollary #o012-fom-u002-cor-contractible data-source-lines="1277-1289"}
**Akibat.** Jika $X$ kontraktil, maka $X\simeq\{*\}$ dan
[akibat ekuivalensi homotopi](#o012-fom-u002-cor-homotopy-equivalent) memberi

$$
H_n(X)\cong
\begin{cases}
\mathbb Z,&n=0,\\
0,&n\geq1.
\end{cases}
$$
:::

::: {.proof #o012-fom-u002-proof-contractible data-origin="edition-original"}
**Bukti edisi.** Pilih titik $x_0\in X$ dan kontraksi
$\operatorname{id}_X\simeq c_{x_0}$. Pemetaan tunggal
$f\colon X\to\{*\}$ dan pemetaan $g\colon\{*\}\to X$ dengan $g(*)=x_0$
memenuhi
$f\circ g=\operatorname{id}_{\{*\}}$ dan
$g\circ f=c_{x_0}\simeq\operatorname{id}_X$. Jadi $X\simeq\{*\}$.
Akibat tentang ekuivalensi homotopi kemudian mengidentifikasi $H_n(X)$ dengan
homologi satu titik yang telah dihitung di atas. $\square$
:::

# Lapisan penguasaan edisi {.unnumbered #o012-fom-u002-mastery data-origin="edition-original" data-course-route-unit-id="D60-R09"}

Bagian ini ditulis khusus untuk edisi bahasa Indonesia dan bukan bagian dari
catatan Fomberg. Keenam pemeriksaan berikut menutup kompetensi homologi
singular, augmentasi, pemetaan terinduksi, fungtorialitas, retrak, homotopi
rantai, dan operator prisma pada rute D60-R09.

::: {.exercise #o012-fom-u002-mcheck-001 data-origin="edition-original" data-course-route-unit-id="D60-R09"}
**Pemeriksaan Penguasaan F2.1 (kompleks singular satu titik).** Untuk
$X=\{*\}$:

1. tentukan $\partial_n\colon C_n(X)\to C_{n-1}(X)$ untuk
   $0\leq n\leq4$;
2. hitung $H_0(X),H_1(X),H_2(X),H_3(X)$; dan
3. hitung $\widetilde H_n(X)$ untuk semua $n\geq0$.
:::

::: {.hint #o012-fom-u002-hint-001 data-origin="edition-original"}
**Petunjuk.** Ada satu generator $\sigma^n$ pada setiap derajat.
Secara terpisah, $\partial_0=0$. Untuk $n\geq1$, jumlah
$\sum_{i=0}^{n}(-1)^i$ bernilai $1$ jika $n$ genap dan $0$ jika $n$ ganjil.
:::

::: {.solution #o012-fom-u002-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan F2.1.** Dengan $C_n(X)=\mathbb Z\sigma^n$,

$$
\partial_0=0,\qquad
\partial_1=0,\qquad
\partial_2=\operatorname{id},\qquad
\partial_3=0,\qquad
\partial_4=\operatorname{id}.
$$

Jadi

$$
H_0(X)=\mathbb Z/0\cong\mathbb Z,
$$

sedangkan

$$
H_1(X)=\mathbb Z/\mathbb Z=0,\qquad
H_2(X)=0/0=0,\qquad
H_3(X)=\mathbb Z/\mathbb Z=0.
$$

Pola ini berulang pada semua derajat positif. Dalam kompleks teraugmentasi,
$\varepsilon\colon C_0(X)\to\mathbb Z$ adalah identitas. Karena itu homologi
pada derajat nol juga lenyap dan $\widetilde H_n(X)=0$ untuk semua
$n\geq0$.
:::

::: {.exercise #o012-fom-u002-mcheck-002 data-origin="edition-original" data-course-route-unit-id="D60-R09"}
**Pemeriksaan Penguasaan F2.2 (komponen dan augmentasi).** Misalkan $X$
mempunyai tepat tiga komponen lintasan, dan pilih titik $x_1,x_2,x_3$, satu
pada setiap komponen.

1. Tentukan $H_0(X)$.
2. Tentukan $\widetilde H_0(X)$ dan berikan basis eksplisit.
3. Jelaskan mengapa jawabannya tidak bergantung pada banyaknya titik lain di
   setiap komponen.
:::

::: {.hint #o012-fom-u002-hint-002 data-origin="edition-original"}
**Petunjuk.** Modulo batas lintasan, semua titik dalam komponen yang sama
mewakili kelas yang sama. Pada basis $[x_1],[x_2],[x_3]$, augmentasi adalah
$(a,b,c)\mapsto a+b+c$.
:::

::: {.solution #o012-fom-u002-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan F2.2.** Dekomposisi menurut komponen lintasan dan lema
$H_0$ memberi

$$
H_0(X)\cong
\mathbb Z[x_1]\oplus\mathbb Z[x_2]\oplus\mathbb Z[x_3]
\cong\mathbb Z^3.
$$

Grup homologi tereduksi derajat nol adalah kernel augmentasi

$$
\widetilde H_0(X)
\cong\{(a,b,c)\in\mathbb Z^3:a+b+c=0\}.
$$

Sebuah basis ialah

$$
[x_2]-[x_1],\qquad [x_3]-[x_1],
$$

sehingga $\widetilde H_0(X)\cong\mathbb Z^2$. Untuk setiap titik lain dalam
komponen ke-$i$, selisihnya dengan $x_i$ merupakan batas suatu lintasan, maka
keduanya memberi kelas homologi yang sama. Itulah sebabnya hanya banyaknya
komponen lintasan yang berpengaruh.
:::

::: {.exercise #o012-fom-u002-mcheck-003 data-origin="edition-original" data-course-route-unit-id="D60-R09" data-repair-ids="FOM-PR-01 FOM-PR-02"}
**Pemeriksaan Penguasaan F2.3 (dari pemetaan kontinu ke homologi).** Misalkan
$f\colon X\to Y$ kontinu.

1. Buktikan langsung pada generator bahwa
   $\partial f_\#=f_\#\partial$.
2. Jika $z-z'=\partial c$, buktikan bahwa
   $[f_\#z]=[f_\#z']$.
3. Buktikan bahwa $f_*([z])=[f_\#z]$ aditif.
:::

::: {.hint #o012-fom-u002-hint-003 data-origin="edition-original"}
**Petunjuk.** Pascakomposisi oleh $f$ berkomutasi dengan pembatasan pada setiap
muka. Untuk bagian kedua, terapkan $f_\#$ pada persamaan
$z-z'=\partial c$.
:::

::: {.solution #o012-fom-u002-sol-003 data-origin="edition-original" data-repair-ids="FOM-PR-01 FOM-PR-02"}
**Solusi Pemeriksaan F2.3.** Untuk simpleks singular $\sigma$,

$$
\begin{aligned}
\partial f_\#(\sigma)
&=\sum_i(-1)^i(f\circ\sigma)\circ\delta_i\\
&=f_\#\!\left(\sum_i(-1)^i\sigma\circ\delta_i\right)
=f_\#(\partial\sigma).
\end{aligned}
$$

Linearitas memperluas identitas ini ke semua rantai. Jika
$z-z'=\partial c$, maka

$$
f_\#z-f_\#z'=f_\#(\partial c)=\partial f_\#c,
$$

sehingga selisih kedua citra merupakan batas dan keduanya mewakili kelas yang sama.
Terakhir,

$$
f_*([z]+[w])=[f_\#(z+w)]
=[f_\#z+f_\#w]=f_*([z])+f_*([w]).
$$

Jadi konstruksi terdefinisi dengan baik dan merupakan homomorfisma.
:::

::: {.exercise #o012-fom-u002-mcheck-004 data-origin="edition-original" data-course-route-unit-id="D60-R09"}
**Pemeriksaan Penguasaan F2.4 (retrak dan suku langsung).** Misalkan
$A\subseteq X$ suatu retrak dengan inklusi $i$ dan retraksi $r$.

1. Buktikan bahwa
   $H_n(X)=\operatorname{im}i_*\oplus\ker r_*$.
2. Gunakan $H_1(S^1)\cong\mathbb Z$ dan $H_1(D^2)=0$ untuk membuktikan bahwa
   lingkaran batas $S^1\subset D^2$ bukan retrak dari cakram.
:::

::: {.hint #o012-fom-u002-hint-004 data-origin="edition-original"}
**Petunjuk.** Untuk $x\in H_n(X)$, tulis
$x=i_*r_*(x)+(x-i_*r_*(x))$ dan periksa suku kedua berada di
$\ker r_*$. Gunakan $r_*i_*=\operatorname{id}$ untuk memeriksa irisannya nol.
:::

::: {.solution #o012-fom-u002-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan F2.4.** Untuk setiap $x\in H_n(X)$,

$$
x=i_*r_*(x)+\bigl(x-i_*r_*(x)\bigr).
$$

Suku pertama berada dalam $\operatorname{im}i_*$. Suku kedua berada dalam
$\ker r_*$ sebab

$$
r_*\bigl(x-i_*r_*(x)\bigr)
=r_*(x)-r_*i_*r_*(x)=0.
$$

Jika $i_*(a)\in\ker r_*$, maka
$a=r_*i_*(a)=0$, sehingga irisannya nol. Maka
$H_n(X)=\operatorname{im}i_*\oplus\ker r_*$.

Andaikan $S^1$ retrak dari $D^2$. Inklusi akan menginduksi pemetaan injektif

$$
i_*\colon H_1(S^1)\longrightarrow H_1(D^2),
$$

yakni monomorfisma $\mathbb Z\to0$, yang mustahil. Jadi tidak ada retraksi
$D^2\to S^1$.
:::

::: {.exercise #o012-fom-u002-mcheck-005 data-origin="edition-original" data-course-route-unit-id="D60-R09" data-repair-id="FOM-PR-03"}
**Pemeriksaan Penguasaan F2.5 (homotopi rantai dan invers homotopi).** Misalkan
$p,q\colon C_\bullet\to D_\bullet$ pemetaan rantai dan ada homomorfisma
$K_n\colon C_n\to D_{n+1}$ dengan

$$
q-p=\partial K+K\partial.
$$

1. Buktikan bahwa $p_*=q_*$ pada homologi.
2. Misalkan $f\colon X\to Y$ dan $g\colon Y\to X$ memenuhi
   $g\circ f\simeq\operatorname{id}_X$ dan
   $f\circ g\simeq\operatorname{id}_Y$. Buktikan bahwa $f_*$ isomorfisma
   dengan invers $g_*$.
:::

::: {.hint #o012-fom-u002-hint-005 data-origin="edition-original"}
**Petunjuk.** Evaluasi identitas homotopi rantai pada sebuah siklus. Untuk
bagian kedua, gabungkan invariansi homotopi dengan fungtorialitas.
:::

::: {.solution #o012-fom-u002-sol-005 data-origin="edition-original" data-repair-id="FOM-PR-03"}
**Solusi Pemeriksaan F2.5.** Jika $z$ siklus, maka

$$
q(z)-p(z)=\partial K(z)+K(\partial z)=\partial K(z).
$$

Jadi selisih $q(z)$ dan $p(z)$ merupakan batas, sehingga
$q_*([z])=p_*([z])$. Untuk pasangan $f,g$, invariansi homotopi dan
fungtorialitas memberi

$$
g_*f_*=(g\circ f)_*=(\operatorname{id}_X)_*
=\operatorname{id}_{H_n(X)}
$$

serta

$$
f_*g_*=(f\circ g)_*=(\operatorname{id}_Y)_*
=\operatorname{id}_{H_n(Y)}.
$$

Dengan demikian $f_*$ dan $g_*$ saling invers.
:::

::: {.exercise #o012-fom-u002-mcheck-006 data-origin="edition-original" data-course-route-unit-id="D60-R09"}
**Pemeriksaan Penguasaan F2.6 (operator prisma pada derajat rendah).** Ambil
homotopi $H\colon X\times I\to Y$ dari $f$ ke $g$.

1. Untuk simpleks-$0$ $\sigma$, tunjukkan bahwa
   $\partial P_0(\sigma)=g_\#(\sigma)-f_\#(\sigma)$.
2. Untuk simpleks-$1$ $\sigma$, triangulasikan perseginya oleh
   $[v_0,w_0,w_1]$ dan $[v_0,v_1,w_1]$, lalu periksa
   $\partial P_1(\sigma)+P_0(\partial\sigma)
   =g_\#(\sigma)-f_\#(\sigma)$.
3. Terapkan hasilnya pada kontraksi interval $I$ ke titik $0$.
:::

::: {.hint #o012-fom-u002-hint-006 data-origin="edition-original"}
**Petunjuk.** Pada derajat satu,
$P_1(\sigma)$ adalah citra bertanda
$[v_0,w_0,w_1]-[v_0,v_1,w_1]$ di bawah pemetaan prisma. Tulis batas kedua segitiga dan
hapus sisi diagonal yang muncul dengan tanda berlawanan.
:::

::: {.solution #o012-fom-u002-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan F2.6.** Untuk $n=0$, prisma adalah lintasan
$t\mapsto H(\sigma(*),t)$ dari $f(\sigma(*))$ ke $g(\sigma(*))$. Karena itu

$$
\partial P_0(\sigma)=g_\#(\sigma)-f_\#(\sigma).
$$

Untuk $n=1$, tulis

$$
Q=H\circ(\sigma\times\operatorname{id}_I),
$$

dan gunakan notasi singkat

$$
A=Q|_{[v_0,w_0,w_1]},\qquad
B=Q|_{[v_0,v_1,w_1]},\qquad
P_1(\sigma)=A-B.
$$

Dalam perhitungan berikut, simbol sisi juga berarti pembatasan $Q$ pada sisi
tersebut. Rumus batas memberi

$$
\begin{aligned}
\partial(A-B)
&=[w_0,w_1]-[v_0,w_1]+[v_0,w_0]\\
&\quad-[v_1,w_1]+[v_0,w_1]-[v_0,v_1]\\
&=[w_0,w_1]-[v_0,v_1]+[v_0,w_0]-[v_1,w_1].
\end{aligned}
$$

Sisi atas ialah $g_\#(\sigma)$, sisi bawah ialah $f_\#(\sigma)$, dan

$$
P_0(\partial\sigma)=[v_1,w_1]-[v_0,w_0].
$$

Maka

$$
\partial P_1(\sigma)+P_0(\partial\sigma)
=g_\#(\sigma)-f_\#(\sigma).
$$

Terakhir, kontraksi $H(x,t)=(1-t)x$ pada $I$ menunjukkan bahwa identitas
$I\to I$ homotopik dengan pemetaan konstan di $0$. Jadi $I\simeq\{0\}$ dan

$$
H_0(I)\cong\mathbb Z,\qquad H_n(I)=0\quad(n\geq1).
$$
:::

::: {.boundary #o012-fom-u002-boundary-001}
**Batas sumber komponen.** Unit ini menerjemahkan
`algebraic_topology.tex` baris 615–1290 secara kontigu, mencakup Bagian 1.3
tentang homologi singular dan Bagian 1.4 tentang invariansi homotopi. Kursor
komponen berikutnya adalah baris 1291, awal Bagian 1.5 tentang barisan eksak.
:::
