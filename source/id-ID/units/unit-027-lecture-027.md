---
title: "Topologi Aljabar"
subtitle: "Unit 27: Kohomologi Tereduksi dan Barisan Mayer--Vietoris"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l27-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 5824--5923 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L5824-L5923)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang aktif itu terdiri atas 100 baris fisik. Dengan normalisasi LF dan
terminator LF penutup dipertahankan, ukurannya 7.012 byte dan SHA-256-nya
adalah
`65d2c393ddf29183f36d6e9ab65c65f8030110334f89c7f68ba88461fc30afa1`.
Baris 5924, yang memulai Kuliah 28, tidak termasuk. Materi sumber dan adaptasi
Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Rentang sumber memuat satu penanda kuliah, satu definisi, satu lema, satu
proposisi, satu teorema, satu latihan formal sumber, tiga contoh, satu
lingkungan bukti, satu catatan pinggir, satu diagram Xy-pic, empat label, dan
dua rujukan silang. Tidak ada gambar TikZ atau gambar eksternal, sitasi,
`input`, ataupun `include`.

Edisi menyelesaikan latihan sumber, membuktikan lema pembelahan, dan melengkapi
pembuktian perbandingan korantai kecil serta teorema Mayer--Vietoris. Ada satu
perbaikan struktural yang penting: korantai kecil harus didefinisikan pada
subkompleks rantai kecil, dan pemetaan pembanding yang sah adalah restriksi
dari seluruh korantai ke korantai kecil. Perluasan dengan nol yang ditulis sumber
tidak membentuk subkompleks pada umumnya. Edisi juga memperbaiki identitas
komposisi yang salah tipe, pernyataan derajat nol yang salah tulis, dan
hipotesis tak-kosong pada versi tereduksi yang dimulai dengan nol. Diagram dan
barisan lebar dialirkan ulang secara semantik agar tidak bergantung pada posisi
atau lebar halaman.

Latihan sumber beserta solusinya, lima pemeriksaan penguasaan tambahan, semua
petunjuk, penutupan bukti, audit, dan solusi lengkap merupakan materi edisi
yang tersedia di bawah CC BY 4.0. Edisi ini bersifat independen; edisi ini
tidak disponsori, didukung, disahkan, ataupun diberi status resmi oleh David
Michael Roberts atau institusinya. Produksi edisi ini dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini menambah transparansi
proses dan tidak mengurangi kredit penulis sumber ataupun kredit kontributor
manusia.

# Kuliah 27 {#o012-rbt-l27}

## Derajat nol tanpa memilih titik dasar {#o012-rbt-l27-s01}

Mari kita kembali sejenak ke kohomologi tereduksi. Pada unit sebelumnya,
konstruksi itu diperkenalkan melalui pasangan bertitik dasar dan karena itu
jelas fungtorial untuk pemetaan bertitik dasar. Ternyata derajat nol mempunyai
deskripsi kanonik yang menghilangkan kebutuhan untuk memilih titik dasar.

Untuk setiap ruang $X$ terdapat pemetaan tunggal

$$
!_X\colon X\longrightarrow \mathrm{pt}.
$$

Karena kohomologi bersifat kontravarian, pemetaan tersebut menginduksi

$$
\operatorname{const}:=!_X^*\colon
R=H^0(\mathrm{pt};R)\longrightarrow H^0(X;R).
$$

Jika $f\colon X\to Y$, maka $!_Y\circ f=!_X$. Karena itu, diagram

$$
\begin{array}{ccc}
R&\xrightarrow{\operatorname{const}_Y}&H^0(Y;R)\\
\big\Vert&&\downarrow\scriptstyle f^*\\
R&\xrightarrow{\operatorname{const}_X}&H^0(X;R)
\end{array}
$$

komutatif. Kita sekarang menentukan arti konkret pemetaan konstan tersebut.

::: {.exercise #o012-rbt-l27-mcheck-001 data-origin="source-exercise"}
**Latihan sumber / Pemeriksaan Penguasaan 27.1 (kohomologi derajat nol).**
Buktikan bahwa

$$
H^0(X;R)\cong R^{[\mathrm{pt},X]},
$$

yakni modul fungsi bernilai $R$ yang konstan pada setiap komponen lintasan.
Untuk $f\colon X\to Y$, buktikan pula bahwa

$$
f^*\colon H^0(Y;R)\longrightarrow H^0(X;R)
$$

adalah prakomposisi dengan pemetaan komponen lintasan
$[\mathrm{pt},X]\to[\mathrm{pt},Y]$ yang diinduksi oleh $f$.
:::

::: {.hint #o012-rbt-l27-hint-001 data-origin="edition-original"}
**Petunjuk.** Simpleks singular berdimensi nol hanyalah titik $x\in X$.
Hitung $(\delta a)(\gamma)$ untuk lintasan
$\gamma\colon\Delta^1\to X$, lalu ingat bahwa tidak ada kobatas yang datang
dari derajat $-1$ dalam kompleks yang digunakan di sini.
:::

::: {.solution #o012-rbt-l27-sol-001 data-origin="edition-solution-to-source-exercise"}
**Solusi Pemeriksaan 27.1.** Korantai nol adalah fungsi

$$
a\colon\operatorname{Top}(\Delta^0,X)=X\longrightarrow R.
$$

Untuk simpleks singular satu
$\gamma\colon\Delta^1\to X$, rumus diferensial memberi

$$
(\delta a)(\gamma)=a(\gamma(1))-a(\gamma(0)).
$$

Jadi $\delta a=0$ tepat ketika $a$ mempunyai nilai yang sama pada kedua ujung
setiap lintasan. Ini ekuivalen dengan mengatakan bahwa $a$ konstan pada setiap
komponen lintasan. Sebaliknya, jika $a$ konstan pada komponen lintasan, kedua
ujung setiap $\gamma$ terletak dalam komponen yang sama, sehingga
$(\delta a)(\gamma)=0$.

Kompleks korantai dimulai pada derajat nol, sehingga
$\operatorname{im}(\delta\colon C^{-1}\to C^0)=0$. Akibatnya,

$$
H^0(X;R)=\ker(\delta\colon C^0\to C^1)
\cong\{\text{fungsi }\pi_0(X)\to R\}
=R^{[\mathrm{pt},X]}.
$$

Untuk $f\colon X\to Y$ dan kelas yang diwakili fungsi
$a\colon\pi_0(Y)\to R$, definisi tarik-balik memberi

$$
(f^*a)(x)=a(f(x)).
$$

Nilai ini hanya bergantung pada komponen lintasan $x$, dan tepat sama dengan
prakomposisi $a$ oleh
$\pi_0(f)\colon\pi_0(X)\to\pi_0(Y)$. Identifikasi tersebut dengan demikian
alami terhadap $f$.
:::

Di bawah identifikasi ini,
$\operatorname{const}(r)$ adalah fungsi yang bernilai $r$ pada setiap
komponen lintasan. Jika $X\ne\varnothing$ dan dipilih
$x\in X$, titik itu menentukan pemetaan $x\colon\mathrm{pt}\to X$. Pemetaan

$$
\operatorname{ev}_x:=x^*\colon H^0(X;R)\longrightarrow R
$$

mengevaluasi fungsi pada komponen $x$. Identitas topologis yang benar ialah

$$
!_X\circ x=\operatorname{id}_{\mathrm{pt}},
$$

sehingga, setelah arah dibalik oleh kohomologi,

$$
\operatorname{ev}_x\circ\operatorname{const}
=\operatorname{id}_R.
$$

Jadi $\operatorname{const}$ injektif.

::: {.source-audit #o012-rbt-l27-audit-001}
**Audit sumber 27.1.** Notes.tex baris 5831 menulis
$!_X\circ x=\operatorname{id}_X$. Kedua ruasnya bahkan tidak mempunyai tipe
yang sama: ruas kiri berpeta dari $\mathrm{pt}$ ke $\mathrm{pt}$. Edisi
memperbaikinya menjadi
$!_X\circ x=\operatorname{id}_{\mathrm{pt}}$, yang memang menghasilkan
$\operatorname{ev}_x\circ\operatorname{const}=\operatorname{id}_R$.
:::

::: {.definition #o012-rbt-l27-def-001}
**Definisi 27.1 (pembelahan kiri).** Untuk barisan eksak pendek modul-$R$

$$
0\longrightarrow A\xrightarrow{i}B\xrightarrow{\pi}C\longrightarrow0,
$$

sebuah **pembelahan kiri** adalah homomorfisma
$r\colon B\to A$ yang memenuhi

$$
r\circ i=\operatorname{id}_A.
$$
:::

::: {.lemma #o012-rbt-l27-lem-001}
**Lema 27.1 (dekomposisi dari pembelahan kiri).** Jika $r$ adalah pembelahan
kiri untuk barisan eksak pendek di atas, maka

$$
(r,\pi)\colon B\longrightarrow A\oplus C,
\qquad b\longmapsto(r(b),\pi(b))
$$

adalah isomorfisma. Selain itu, restriksi
$\pi|_{\ker r}\colon\ker r\to C$ adalah isomorfisma.
:::

::: {.proof #o012-rbt-l27-proof-001 data-origin="edition-proof-closure"}
**Bukti.** Jika $(r(b),\pi(b))=(0,0)$, maka eksaknya barisan memberi
$b=i(a)$ untuk suatu $a\in A$. Karena $r(b)=0$,

$$
0=r(i(a))=a,
$$

sehingga $b=0$. Jadi $(r,\pi)$ injektif.

Untuk membuktikan surjektivitas, ambil $(a,c)\in A\oplus C$. Karena $\pi$
surjektif, pilih $b_0\in B$ dengan $\pi(b_0)=c$, lalu tetapkan

$$
b=b_0+i\bigl(a-r(b_0)\bigr).
$$

Kita memperoleh

$$
r(b)=r(b_0)+a-r(b_0)=a,
\qquad
\pi(b)=\pi(b_0)=c.
$$

Maka $(r,\pi)$ surjektif dan karenanya isomorfisma.

Jika $b\in\ker r$ dan $\pi(b)=0$, argumen injektivitas tadi memberi $b=0$.
Untuk $c\in C$, pilih lagi $b_0$ dengan $\pi(b_0)=c$ dan bentuk

$$
b=b_0-i(r(b_0)).
$$

Sekarang $r(b)=0$ dan $\pi(b)=c$. Jadi
$\pi|_{\ker r}$ bijektif dan merupakan isomorfisma modul-$R$.
:::

Untuk ruang tak-kosong $X$ kita mempunyai barisan eksak pendek

$$
0\longrightarrow R
\xrightarrow{\operatorname{const}}H^0(X;R)
\longrightarrow\operatorname{coker}(\operatorname{const})
\longrightarrow0.
$$

Evaluasi $\operatorname{ev}_x$ adalah pembelahan kiri. Lema 27.1 memberi

$$
H^0(X;R)
\cong R\oplus\operatorname{coker}(\operatorname{const}),
\qquad
\operatorname{coker}(\operatorname{const})
\cong\ker(\operatorname{ev}_x).
$$

Barisan eksak panjang pasangan $(X,\{x\})$ mengidentifikasi kernel terakhir
dengan $H^0(X,x;R)$. Dengan demikian, setiap pilihan $x\in X$ memberi

$$
\operatorname{coker}(\operatorname{const})\cong H^0(X,x;R).
$$

::: {.source-margin #o012-rbt-l27-margin-001}
> **Catatan pinggir sumber (dialirkan ulang).** Submodul konkret
> $H^0(X,x;R)=\ker(\operatorname{ev}_x)$ di dalam $H^0(X;R)$ dapat berubah
> jika $x$ diganti dengan titik pada komponen lintasan lain. Namun, hasil bagi
> kanonik $\operatorname{coker}(\operatorname{const})$ tidak bergantung pada
> pilihan titik dasar.
:::

Kita karena itu dapat membuat definisi yang tidak memilih titik dasar:

::: {.definition #o012-rbt-l27-def-002}
**Definisi 27.2 (kohomologi tereduksi, bentuk kanonik).** Untuk setiap
$k\geq0$, tetapkan

$$
\widetilde H^k(X;R)
:=\operatorname{coker}\!\left(
H^k(\mathrm{pt};R)\xrightarrow{!_X^*}H^k(X;R)
\right).
$$
:::

Karena $H^k(\mathrm{pt};R)=0$ untuk $k>0$,

$$
\widetilde H^k(X;R)\cong H^k(X;R)
\quad(k>0),
$$

sedangkan untuk $X\ne\varnothing$,

$$
H^0(X;R)\cong R\oplus\widetilde H^0(X;R).
$$

Kealamian pemetaan $!_X$ yang dicatat di awal menunjukkan bahwa definisi ini
fungtorial bagi **semua** pemetaan ruang, bukan hanya pemetaan bertitik dasar.

::: {.example #o012-rbt-l27-exa-001}
**Contoh 27.1 (ruang terhubung lintasan).** Jika $X$ terhubung lintasan, setiap
fungsi yang konstan pada komponen lintasan adalah fungsi konstan. Jadi

$$
\widetilde H^0(X;R)=0.
$$

Jika $X$ kontraktil, invariansi homotopi juga memberi

$$
\widetilde H^k(X;R)=0
\qquad\text{untuk setiap }k\geq0.
$$
:::

::: {.source-audit #o012-rbt-l27-audit-002}
**Audit sumber 27.2.** Notes.tex baris 5847 menulis
$\widetilde H^0(X;R)=0$ “untuk semua $k$,” padahal ekspresi itu sudah berderajat
nol. Edisi memisahkan dua klaim yang benar: keterhubungan lintasan mematikan
derajat nol tereduksi, sedangkan kontraktilitas mematikan semua derajat
tereduksi.
:::

::: {.example #o012-rbt-l27-exa-002 data-source-label="eg:reduced_cohom_S0"}
**Contoh 27.2 (sfera nol).** Ruang $S^0$ terdiri atas dua titik. Karena
$H^0(S^0;R)\cong R\oplus R$ dan pemetaan konstan adalah diagonal
$r\mapsto(r,r)$,

$$
\widetilde H^0(S^0;R)
\cong (R\oplus R)/\Delta R
\cong R.
$$

Untuk $k>0$, $H^k(S^0;R)=0$, sehingga
$\widetilde H^k(S^0;R)=0$.
:::

## Korantai kecil untuk suatu sampul terbuka {#o012-rbt-l27-s02}

Sekarang kita kembali ke barisan eksak panjang. Misalkan
$\mathcal U=\{U,V\}$ adalah sampul terbuka ruang $X$. Pemetaan-pemetaan inklusi
memberi diagram pushout berikut.

::: {.figure #o012-rbt-l27-fig-001 data-source-format="xypic"}
**Diagram 27.1 (data panah pushout).** Diagram sumber yang posisional dialirkan
ulang menjadi

$$
\begin{array}{ccc}
U\cap V&\mathop{\longrightarrow}\limits^{i_V}&V\\
\downarrow^{i_U}&&\downarrow^{j_V}\\
U&\mathop{\longrightarrow}\limits_{j_U}&X,
\end{array}
$$

dengan persamaan komutativitas

$$
j_U\circ i_U=j_V\circ i_V.
$$

Sifat universalnya ialah: untuk pemetaan $a\colon U\to Z$ dan
$b\colon V\to Z$ yang memenuhi $a\circ i_U=b\circ i_V$, terdapat tepat satu
$h\colon X\to Z$ dengan $h\circ j_U=a$ dan $h\circ j_V=b$. Jadi informasi
diagram tidak bergantung pada warna, letak, atau lebar gambar.
:::

Pada derajat korantai, definisikan pemetaan selisih restriksi

::: {.equation #o012-rbt-l27-eq-001 data-source-label="eq:restr_to_intersection"}
$$
\begin{aligned}
d\colon C^\bullet(U;R)\oplus C^\bullet(V;R)
&\longrightarrow C^\bullet(U\cap V;R),\\
(f,g)&\longmapsto i_U^*f-i_V^*g.
\end{aligned}
$$
:::

Pemetaan $d$ adalah pemetaan kompleks korantai. Ia surjektif pada setiap
derajat: untuk

$$
h\colon\operatorname{Top}(\Delta^n,U\cap V)\longrightarrow R,
$$

perluas $h$ menjadi fungsi $f$ pada
$\operatorname{Top}(\Delta^n,U)$ dengan memberi nilai nol pada simpleks yang
tidak mendarat di $U\cap V$. Maka $d(f,0)=h$. Perluasan ini hanya dipakai
untuk membuktikan surjektivitas **pada satu derajat**; ia tidak diklaim
membentuk pemetaan kompleks.

Untuk mengidentifikasi kernel $d$ dengan benar, definisikan subkompleks rantai

$$
C_*^{\mathcal U}(X;R)
:=C_*(U;R)+C_*(V;R)\subseteq C_*(X;R).
$$

Subkompleks ini dibangkitkan oleh simpleks singular
$\sigma\colon\Delta^n\to X$ yang citranya termuat seluruhnya di $U$ atau
seluruhnya di $V$. Simpleks semacam itu disebut **kecil terhadap
$\mathcal U$**. Kompleks korantai kecil didefinisikan sebagai

$$
C_{\mathcal U}^\bullet(X;R)
:=\operatorname{Hom}_R(C_*^{\mathcal U}(X;R),R).
$$

Sebuah korantai pada $C_*^{\mathcal U}(X;R)$ sama dengan sepasang korantai
pada $U$ dan $V$ yang restriksinya ke $U\cap V$ sama. Karena itu terdapat
barisan eksak pendek kompleks korantai

$$
0\longrightarrow C_{\mathcal U}^\bullet(X;R)
\xrightarrow{\Phi}
C^\bullet(U;R)\oplus C^\bullet(V;R)
\xrightarrow{d}
C^\bullet(U\cap V;R)
\longrightarrow0.
$$

Di sini $\Phi$ mengambil dua restriksi sebuah fungsi pada jumlah rantai
$C_*(U;R)+C_*(V;R)$. Pemetaan itu injektif karena rantai kecil dibangkitkan
oleh kedua subkompleks tersebut, dan citranya tepat $\ker d$.

::: {.source-audit #o012-rbt-l27-audit-003}
**Audit sumber 27.3 (arah pembanding korantai kecil).** Notes.tex baris
5867--5880 menggambarkan $C_{\mathcal U}^\bullet(X;R)$ sebagai fungsi pada
semua simpleks yang bernilai nol pada simpleks tak-kecil, lalu menyebut
inklusi
$C_{\mathcal U}^\bullet(X;R)\to C^\bullet(X;R)$ sebagai kuasi-isomorfisma.
Pernyataan tingkat kompleks ini tidak benar pada umumnya. Sebuah simpleks
tak-kecil dapat mempunyai sisi-sisi kecil, sehingga diferensial korantai yang
diperluas dengan nol dapat bernilai tak-nol pada simpleks tak-kecil.

Konstruksi yang sah adalah
$C_{\mathcal U}^\bullet(X;R)=\operatorname{Hom}_R(C_*^{\mathcal U}(X;R),R)$,
dan pemetaan pembandingnya berjalan lewat restriksi

$$
\rho\colon C^\bullet(X;R)\longrightarrow
C_{\mathcal U}^\bullet(X;R).
$$

Perbaikan ini tidak mengubah teorema Mayer--Vietoris; justru inilah model
korantai kecil yang membuktikannya.
:::

::: {.proposition #o012-rbt-l27-prop-001}
**Proposisi 27.1 (teorema rantai kecil).** Untuk sampul terbuka
$\mathcal U=\{U,V\}$, inklusi rantai

$$
j\colon C_*^{\mathcal U}(X;R)\hookrightarrow C_*(X;R)
$$

adalah ekuivalensi homotopi rantai. Oleh dualitas, restriksi

$$
\rho=j^*\colon C^\bullet(X;R)\longrightarrow
C_{\mathcal U}^\bullet(X;R)
$$

adalah ekuivalensi homotopi korantai, dan khususnya kuasi-isomorfisma:

$$
H^k(X;R)\xrightarrow{\ \cong\ }
H^k(C_{\mathcal U}^\bullet(X;R)).
$$
:::

Sumber menunjuk Proposisi 2.21 dalam buku Hatcher sebagai argumen homologi
yang sejalan. Rujukan pembanding itu dipertahankan, tetapi bukti berikut
menuliskan konstruksi korantai yang diperlukan secara mandiri.

::: {.proof #o012-rbt-l27-proof-002 data-origin="edition-proof-closure"}
**Bukti.** Misalkan $S$ adalah operator subdivisi barisentris pada rantai
singular. Ada homotopi rantai prisma $T$ yang memenuhi

$$
S-\operatorname{id}=\partial T+T\partial.
$$

Dengan menjumlahkan homotopi yang sesuai, untuk setiap $m\geq0$ terdapat
$T_m$ dengan

$$
S^m-\operatorname{id}=\partial T_m+T_m\partial,
\qquad T_0=0.
$$

Jika sebuah simpleks sudah kecil, semua simpleks yang muncul dalam $S^m$ dan
$T_m$ atas simpleks itu tetap berada dalam anggota sampul yang sama.

Untuk simpleks singular
$\sigma\colon\Delta^n\to X$, himpunan
$\sigma^{-1}(U)$ dan $\sigma^{-1}(V)$ membentuk sampul terbuka dari simpleks
kompak $\Delta^n$. Lema bilangan Lebesgue menunjukkan bahwa setelah subdivisi
barisentris secukupnya, setiap subsimpleks dipetakan seluruhnya ke $U$ atau
ke $V$. Jadi, untuk setiap rantai hingga $c$, terdapat $m$ sehingga
$S^m c$ adalah rantai kecil.

Kita sekarang membangun pemetaan rantai
$r\colon C_*(X;R)\to C_*^{\mathcal U}(X;R)$ dan homotopi $K$ secara induktif.
Pada derajat nol, semua simpleks sudah kecil; tetapkan $r=\operatorname{id}$
dan $K=0$. Anggap $r$ dan $K$ telah dibangun pada derajat di bawah $n$ dan
memenuhi

$$
\operatorname{id}-jr=\partial K+K\partial.
$$

Untuk satu simpleks basis $\sigma$ berdimensi $n$, tetapkan

$$
z:=\sigma-K(\partial\sigma).
$$

Hipotesis induksi pada $\partial\sigma$ memberi

$$
\partial z=jr(\partial\sigma).
$$

Pilih $m$ cukup besar sehingga $S^m z$ kecil. Karena
$r(\partial\sigma)$ sudah kecil, $T_mr(\partial\sigma)$ juga kecil. Definisikan

$$
r(\sigma)
:=S^m z-T_mr(\partial\sigma),
\qquad
K(\sigma):=-T_mz.
$$

Dengan menggunakan
$S^m-\operatorname{id}=\partial T_m+T_m\partial$ dan
$\partial r(\partial\sigma)=0$, kita memperoleh

$$
\begin{aligned}
\partial r(\sigma)
&=S^m r(\partial\sigma)-\partial T_mr(\partial\sigma)\\
&=r(\partial\sigma),
\end{aligned}
$$

jadi $r$ adalah pemetaan rantai. Selain itu,

$$
\begin{aligned}
z-jr(\sigma)
&=z-S^m z+T_mr(\partial\sigma)\\
&=-\partial T_mz-T_m\partial z+T_mr(\partial\sigma)\\
&=-\partial T_mz
=\partial K(\sigma).
\end{aligned}
$$

Karena $z=\sigma-K(\partial\sigma)$, persamaan ini tepat mengatakan

$$
\sigma-jr(\sigma)
=\partial K(\sigma)+K(\partial\sigma).
$$

Jika $\sigma$ sudah kecil, kita memilih $m=0$; secara induktif diperoleh
$rj=\operatorname{id}$ dan $Kj=0$. Jadi $r$ adalah invers homotopi rantai
untuk $j$.

Terapkan $\operatorname{Hom}_R(-,R)$. Prakomposisi memberi

$$
j^*=\rho\colon C^\bullet(X;R)\to C_{\mathcal U}^\bullet(X;R),
\qquad
r^*\colon C_{\mathcal U}^\bullet(X;R)\to C^\bullet(X;R).
$$

Identitas $rj=\operatorname{id}$ dan homotopi
$jr\simeq\operatorname{id}$ berdualisasi menjadi
$j^*r^*=\operatorname{id}$ dan
$r^*j^*\simeq\operatorname{id}$. Maka $\rho$ adalah ekuivalensi homotopi
korantai dan menginduksi isomorfisma pada kohomologi.
:::

Gagasan geometrisnya sederhana: sebuah simpleks besar mungkin melintasi
$U$ dan $V$, tetapi subdivisi berulang memecahnya menjadi simpleks kecil yang
masing-masing berada di salah satu anggota sampul. Pembuktian di atas mencatat
homotopinya sehingga gagasan tersebut berlaku pada tingkat kompleks, bukan
hanya pada tingkat gambar. Analogi sumbernya adalah integrasi pada manifold:
pecah sebuah simpleks menjadi bagian-bagian yang masing-masing masuk ke satu
peta koordinat, kerjakan perhitungan pada setiap bagian, lalu jumlahkan
hasilnya.

## Barisan eksak panjang Mayer--Vietoris {#o012-rbt-l27-s03}

::: {.theorem #o012-rbt-l27-thm-001 data-source-label="thm:mayer-vietoris"}
**Teorema 27.1 (Mayer--Vietoris).** Jika
$\mathcal U=\{U,V\}$ adalah sampul terbuka $X$, terdapat barisan eksak
panjang modul-$R$

$$
\begin{aligned}
0\longrightarrow H^0(X;R)
&\longrightarrow H^0(U;R)\oplus H^0(V;R)\\
&\longrightarrow H^0(U\cap V;R)
\xrightarrow{\partial_{\mathrm{MV}}}H^1(X;R)\\
&\longrightarrow H^1(U;R)\oplus H^1(V;R)
\longrightarrow H^1(U\cap V;R)\\
&\xrightarrow{\partial_{\mathrm{MV}}}H^2(X;R)
\longrightarrow\cdots.
\end{aligned}
$$

Pemetaan dari $H^k(X;R)$ adalah pasangan restriksi, dan pemetaan menuju
$H^k(U\cap V;R)$ adalah selisih restriksi.

Jika $U\cap V\ne\varnothing$, versi tereduksi dalam konvensi derajat
tak-negatif unit ini juga eksak dan dimulai dengan

$$
\begin{aligned}
0\longrightarrow\widetilde H^0(X;R)
&\longrightarrow\widetilde H^0(U;R)
\oplus\widetilde H^0(V;R)\\
&\longrightarrow\widetilde H^0(U\cap V;R)
\xrightarrow{\partial_{\mathrm{MV}}}H^1(X;R)
\longrightarrow\cdots.
\end{aligned}
$$
:::

::: {.proof #o012-rbt-l27-proof-003 data-origin="edition-proof-closure"}
**Bukti.** Barisan eksak pendek kompleks korantai yang telah dibangun adalah

$$
0\to C_{\mathcal U}^\bullet(X;R)
\xrightarrow{\Phi}C^\bullet(U;R)\oplus C^\bullet(V;R)
\xrightarrow{d}C^\bullet(U\cap V;R)\to0.
$$

Setiap barisan eksak pendek kompleks korantai menghasilkan barisan eksak
panjang kohomologi. Untuk melihat pemetaan penghubungnya secara konkret, ambil
kosiklus $h\in C^k(U\cap V;R)$. Surjektivitas derajat demi derajat memberi
pasangan $(f,g)$ dengan $d(f,g)=h$. Karena $\delta h=0$,

$$
d\bigl(\delta f,\delta g\bigr)
=\delta d(f,g)=0.
$$

Maka ada tepat satu $a\in C_{\mathcal U}^{k+1}(X;R)$ dengan

$$
\Phi(a)=(\delta f,\delta g).
$$

Persamaan $\delta^2=0$ dan injektivitas $\Phi$ menunjukkan $\delta a=0$.
Definisikan

$$
\partial_{\mathrm{MV}}[h]:=[a]
\in H^{k+1}(C_{\mathcal U}^\bullet(X;R))
\cong H^{k+1}(X;R).
$$

Jika lift $(f,g)$ diganti, selisih kedua lift berada dalam
$\operatorname{im}\Phi$; akibatnya, kedua $a$ berbeda dengan sebuah kobatas.
Jika $h$ diganti dengan kosiklus sekohomolog, lift dapat disesuaikan dengan
sebuah diferensial dan kelas $[a]$ tetap sama. Jadi pemetaan penghubung
terdefinisi dengan baik.

Eksaknya dapat diperiksa pada ketiga jenis suku yang berulang. Pertama, jika
$b\in C^k(U;R)\oplus C^k(V;R)$ adalah kosiklus dan kelas $d(b)$ nol, tulis
$d(b)=\delta h$. Pilih $e$ dengan $d(e)=h$. Maka
$b-\delta e\in\ker d=\operatorname{im}\Phi$ dan tetap merupakan kosiklus,
sehingga $[b]$ berasal dari
$H^k(C_{\mathcal U}^\bullet(X;R))$.

Kedua, jika $h$ sebuah kosiklus dan
$\partial_{\mathrm{MV}}[h]=0$, pilih lift $b$ dari $h$. Dalam konstruksi di
atas, $\delta b=\Phi(a)$ dengan $a=\delta a_0$. Karena itu
$b-\Phi(a_0)$ adalah kosiklus yang masih dipetakan oleh $d$ ke $h$; jadi
$[h]$ berasal dari $H^k(U;R)\oplus H^k(V;R)$.

Ketiga, jika $a$ sebuah kosiklus dalam
$C_{\mathcal U}^{k+1}(X;R)$ dan $\Phi_*[a]=0$, tulis
$\Phi(a)=\delta b$. Unsur $h=d(b)$ adalah kosiklus, sebab
$\delta h=d(\delta b)=d(\Phi(a))=0$, dan konstruksi pemetaan penghubung
memberi $\partial_{\mathrm{MV}}[h]=[a]$. Komposisi dua pemetaan berturutan
jelas nol dari definisinya. Jadi pada setiap posisi citra sama dengan kernel,
yang membuktikan eksaknya barisan panjang.

Menurut Proposisi 27.1,
$H^*(C_{\mathcal U}^\bullet(X;R))\cong H^*(X;R)$. Mengganti suku korantai
kecil dengan kohomologi $X$ memberi barisan biasa yang dinyatakan dalam
teorema.

Untuk versi tereduksi, anggap $U\cap V\ne\varnothing$. Maka $U,V$, dan $X$
juga tak-kosong, dan suku fungsi konstan sendiri membentuk barisan eksak

$$
0\longrightarrow R
\xrightarrow{r\mapsto(r,r)}R\oplus R
\xrightarrow{(a,b)\mapsto a-b}R
\longrightarrow0.
$$

Mengambil hasil bagi barisan Mayer--Vietoris derajat nol oleh barisan konstan
ini menghasilkan tepat barisan tereduksi yang ditampilkan. Pada derajat
positif, kohomologi biasa dan tereduksi sudah sama.
:::

::: {.source-audit #o012-rbt-l27-audit-004}
**Audit sumber 27.4 (versi tereduksi).** Dengan definisi
$\widetilde H^0$ sebagai kokernel pemetaan konstan dan tanpa suku derajat
$-1$, barisan tereduksi yang dimulai dengan nol memerlukan
$U\cap V\ne\varnothing$. Untuk sampul dua komponen yang saling lepas,
pernyataan tanpa hipotesis itu gagal pada derajat nol. Versi sepenuhnya umum
dapat dipulihkan dengan kompleks teraugmentasi dan
$\widetilde H^{-1}(\varnothing;R)=R$. Sumber tidak menyatakan pembedaan ini;
edisi menyatakan hipotesis yang dipakai oleh contoh sfera berikutnya.
:::

## Kohomologi sfera {#o012-rbt-l27-s04}

::: {.example #o012-rbt-l27-exa-003}
**Contoh 27.3 (sampul hemisfer).** Untuk $n\geq1$, sampuli $S^n$ dengan dua
lingkungan hemisfer terbuka $D_+^n$ dan $D_-^n$. Masing-masing kontraktil
(dan homeomorfik dengan bola terbuka), sedangkan

$$
D_+^n\cap D_-^n\cong S^{n-1}\times J
\simeq S^{n-1},
$$

dengan $J$ sebuah interval terbuka kecil.

Barisan Mayer--Vietoris tereduksi dimulai sebagai

$$
\begin{aligned}
0\longrightarrow\widetilde H^0(S^n;R)
&\longrightarrow
\widetilde H^0(D_+^n;R)\oplus
\widetilde H^0(D_-^n;R)\\
&\longrightarrow
\widetilde H^0(S^{n-1}\times J;R)
\longrightarrow H^1(S^n;R)\\
&\longrightarrow
H^1(D_+^n;R)\oplus H^1(D_-^n;R)
\longrightarrow\cdots.
\end{aligned}
$$

Kedua hemisfer kontraktil, sehingga semua suku tereduksi dan semua suku
berderajat positif milik $D_+^n,D_-^n$ lenyap. Pertama,

$$
0\longrightarrow\widetilde H^0(S^n;R)\longrightarrow0
$$

memberi $\widetilde H^0(S^n;R)=0$, sesuai keterhubungan lintasan $S^n$.
Selanjutnya, untuk $k=1$ kita memperoleh

$$
0\longrightarrow\widetilde H^0(S^{n-1};R)
\longrightarrow H^1(S^n;R)\longrightarrow0,
$$

dan untuk $k>1$,

$$
0\longrightarrow H^{k-1}(S^{n-1};R)
\longrightarrow H^k(S^n;R)\longrightarrow0.
$$

Kedua kasus itu dapat ditulis seragam sebagai

::: {.equation #o012-rbt-l27-eq-002 data-source-label="eq:sphere_cohomol_reduction"}
$$
\widetilde H^{k-1}(S^{n-1};R)
\cong\widetilde H^k(S^n;R)
\qquad(k\geq1).
$$
:::

Ambil $k=n$ dan ulangi isomorfisma tersebut sampai mencapai $S^0$:

$$
\widetilde H^n(S^n;R)
\cong\widetilde H^{n-1}(S^{n-1};R)
\cong\cdots\cong\widetilde H^0(S^0;R)
\cong R.
$$

Karena $n>0$, kohomologi biasa dan tereduksi sama pada derajat $n$. Jadi

$$
H^n(S^n;R)\cong R
\qquad(n\geq1).
$$

Rekurensi yang sama juga menentukan semua derajat lain. Untuk $n\geq1$,

$$
H^k(S^n;R)\cong
\begin{cases}
R,&k=0\text{ atau }k=n,\\
0,&k>0\text{ dan }k\ne n.
\end{cases}
$$
:::

::: {.source-audit #o012-rbt-l27-audit-005}
**Audit sumber 27.5.** Sumber menyebut kedua anggota sampul terbuka di atas
“cakram.” Edisi menulisnya sebagai lingkungan hemisfer yang homeomorfik dengan
bola **terbuka**; sebuah himpunan terbuka di $S^n$ tidak dimaksudkan sebagai
cakram tertutup. Ruang irisan dan seluruh perhitungan homotopinya tetap sama.
:::

## Pemeriksaan penguasaan lanjutan {#o012-rbt-l27-mastery}

Lima pemeriksaan berikut melengkapi latihan sumber yang sudah diselesaikan
sebagai Pemeriksaan 27.1. Setiap pemeriksaan mempunyai petunjuk dan solusi
lengkap yang dapat dibaca secara terpisah.

::: {.exercise #o012-rbt-l27-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 27.2 (rumus invers pembelahan).** Misalkan

$$
0\to A\xrightarrow{i}B\xrightarrow{\pi}C\to0
$$

eksak dan $r\colon B\to A$ memenuhi $ri=\operatorname{id}_A$.

1. Untuk $c\in C$, pilih sembarang lift $b_c$ dengan $\pi(b_c)=c$ dan
   definisikan $s(c)=b_c-i(r(b_c))$. Buktikan bahwa $s(c)$ tidak bergantung
   pada pilihan lift dan merupakan homomorfisma $C\to B$.
2. Buktikan bahwa invers $(r,\pi)\colon B\to A\oplus C$ adalah
   $(a,c)\mapsto i(a)+s(c)$.
3. Tunjukkan $B=i(A)\oplus\ker r$.
:::

::: {.hint #o012-rbt-l27-hint-002 data-origin="edition-original"}
**Petunjuk.** Dua lift $c$ berbeda dengan unsur $i(A)$. Terapkan operasi
$b\mapsto b-i(r(b))$ pada selisih itu. Untuk jumlah langsung, periksa
keberadaan dekomposisi dan bahwa irisannya nol.
:::

::: {.solution #o012-rbt-l27-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 27.2.** Jika $b_c'$ adalah lift lain, maka
$b_c'-b_c=i(a)$ untuk suatu $a\in A$. Karena $ri=\operatorname{id}_A$,

$$
\begin{aligned}
b_c'-i(r(b_c'))
&=b_c+i(a)-i\bigl(r(b_c)+a\bigr)\\
&=b_c-i(r(b_c)).
\end{aligned}
$$

Jadi $s$ bebas pilihan. Untuk $c_1,c_2$, pilih lift $b_1,b_2$; maka
$b_1+b_2$ adalah lift $c_1+c_2$, dan rumus langsung memberi
$s(c_1+c_2)=s(c_1)+s(c_2)$. Hal yang sama berlaku untuk perkalian skalar, jadi
$s$ homomorfisma. Selain itu,

$$
r(s(c))=r(b_c)-r(i(r(b_c)))=0,
\qquad
\pi(s(c))=c.
$$

Sekarang

$$
(r,\pi)(i(a)+s(c))=(a,c).
$$

Sebaliknya, untuk $b\in B$, unsur
$b-i(r(b))$ berada dalam $\ker r$ dan mempunyai citra $\pi(b)$, sehingga
sama dengan $s(\pi(b))$. Maka

$$
b=i(r(b))+s(\pi(b)),
$$

yang membuktikan rumus invers. Setiap $b$ karena itu berada dalam
$i(A)+\ker r$. Jika $i(a)\in\ker r$, maka
$a=r(i(a))=0$, sehingga irisannya nol dan
$B=i(A)\oplus\ker r$.
:::

::: {.exercise #o012-rbt-l27-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 27.3 (banyak komponen lintasan).** Misalkan $X$
mempunyai tepat $m\geq1$ komponen lintasan dan pilih titik dasar pada komponen
ke-$j$.

1. Hitung $H^0(X;R)$ dan $\widetilde H^0(X;R)$.
2. Deskripsikan submodul $H^0(X,x;R)=\ker(\operatorname{ev}_x)$.
3. Berikan isomorfisma eksplisit
   $(R^m)/\Delta R\cong R^{m-1}$ yang tidak menggunakan pembagian dalam $R$.
:::

::: {.hint #o012-rbt-l27-hint-003 data-origin="edition-original"}
**Petunjuk.** Daftarkan nilai fungsi pada setiap komponen. Untuk hasil bagi
diagonal, kurangi koordinat ke-$j$ dari semua koordinat lainnya.
:::

::: {.solution #o012-rbt-l27-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 27.3.** Pemeriksaan 27.1 memberi

$$
H^0(X;R)\cong R^m.
$$

Pemetaan konstan adalah inklusi diagonal
$\Delta\colon R\to R^m$, $r\mapsto(r,\ldots,r)$, sehingga

$$
\widetilde H^0(X;R)\cong R^m/\Delta R.
$$

Evaluasi pada titik dasar di komponen ke-$j$ adalah proyeksi koordinat ke-$j$.
Jadi

$$
H^0(X,x;R)
=\{(a_1,\ldots,a_m)\in R^m:a_j=0\}\cong R^{m-1}.
$$

Definisikan

$$
q_j(a_1,\ldots,a_m)
=(a_1-a_j,\ldots,a_{j-1}-a_j,
a_{j+1}-a_j,\ldots,a_m-a_j).
$$

Kernel $q_j$ tepat $\Delta R$, dan $q_j$ surjektif karena setiap daftar
$m-1$ koordinat diperoleh dengan mengambil $a_j=0$. Teorema isomorfisma
pertama memberi

$$
R^m/\Delta R\xrightarrow{\ \cong\ }R^{m-1}.
$$

Tidak ada pembagian yang digunakan, sehingga argumen berlaku untuk setiap
gelanggang koefisien $R$.
:::

::: {.exercise #o012-rbt-l27-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 27.4 (mengapa perluasan dengan nol gagal).** Ambil
$X=[0,1]$ dengan sampul terbuka relatif

$$
U=[0,0.6),
\qquad
V=(0.4,1].
$$

Misalkan $a\in C^0(X;R)$ bernilai $0$ pada semua titik kecuali $a(1)=1_R$.
Ambil simpleks singular $\sigma(t)=t$.

1. Buktikan bahwa setiap simpleks nol kecil terhadap $\{U,V\}$, tetapi
   $\sigma$ tidak kecil.
2. Hitung $(\delta a)(\sigma)$.
3. Jelaskan mengapa submodul bertingkat “korantai yang nol pada simpleks
   tak-kecil” bukan subkompleks, lalu nyatakan pemetaan pembanding yang benar.
:::

::: {.hint #o012-rbt-l27-hint-004 data-origin="edition-original"}
**Petunjuk.** Setiap titik terletak di setidaknya satu anggota sampul, tetapi
citra $\sigma$ adalah seluruh interval. Gunakan
$(\delta a)(\sigma)=a(\sigma(1))-a(\sigma(0))$.
:::

::: {.solution #o012-rbt-l27-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 27.4.** Sebuah simpleks nol mempunyai citra satu titik.
Karena $U\cup V=X$, titik itu terletak seluruhnya di $U$ atau di $V$; jadi
setiap simpleks nol kecil. Namun,

$$
\operatorname{im}\sigma=[0,1]
$$

tidak termuat di $U$ dan tidak termuat di $V$, sehingga $\sigma$ tak-kecil.
Perhitungan diferensial memberi

$$
(\delta a)(\sigma)=a(1)-a(0)=1_R.
$$

Korantai $a$ memenuhi syarat “nol pada simpleks nol tak-kecil” secara vakum,
tetapi $\delta a$ tidak nol pada simpleks satu tak-kecil $\sigma$. Jadi syarat
tersebut tidak stabil di bawah $\delta$ dan tidak mendefinisikan subkompleks.

Pemetaan yang benar berasal dari inklusi subkompleks **rantai** kecil:

$$
C_*^{\mathcal U}(X;R)\hookrightarrow C_*(X;R).
$$

Setelah menerapkan $\operatorname{Hom}_R(-,R)$, arahnya berbalik menjadi
restriksi

$$
C^\bullet(X;R)\longrightarrow
\operatorname{Hom}_R(C_*^{\mathcal U}(X;R),R).
$$
:::

::: {.exercise #o012-rbt-l27-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 27.5 (generator $H^1(S^1;R)$).** Selimuti lingkaran
$S^1$ dengan dua busur terbuka kontraktil $U,V$ sedemikian sehingga
$U\cap V=W_0\sqcup W_1$ mempunyai dua komponen kontraktil.

1. Hitung $\widetilde H^0(U\cap V;R)$.
2. Gunakan Mayer--Vietoris untuk membuktikan bahwa pemetaan penghubung
   $\partial_{\mathrm{MV}}$ memberi isomorfisma
   $\widetilde H^0(U\cap V;R)\cong H^1(S^1;R)$.
3. Pilih fungsi $h$ yang bernilai $0$ pada $W_0$ dan $1_R$ pada $W_1$.
   Jelaskan bagaimana konstruksi penghubung mengubah $[h]$ menjadi generator
   $H^1(S^1;R)$.
:::

::: {.hint #o012-rbt-l27-hint-005 data-origin="edition-original"}
**Petunjuk.** Gunakan Contoh 27.2 untuk irisan yang mempunyai dua komponen.
Semua kohomologi tereduksi kedua busur lenyap. Untuk bagian terakhir,
perluas $h$ sebagai korantai pada salah satu busur dan ambil diferensialnya.
:::

::: {.solution #o012-rbt-l27-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 27.5.** Karena $U\cap V$ mempunyai dua komponen
kontraktil,

$$
H^0(U\cap V;R)\cong R\oplus R,
\qquad
\widetilde H^0(U\cap V;R)\cong(R\oplus R)/\Delta R\cong R.
$$

Kontraktilitas $U$ dan $V$ memberi

$$
\widetilde H^0(U;R)=\widetilde H^0(V;R)=0,
\qquad
H^1(U;R)=H^1(V;R)=0.
$$

Bagian yang relevan dari barisan eksak tereduksi karena itu adalah

$$
0\longrightarrow0\longrightarrow
\widetilde H^0(U\cap V;R)
\xrightarrow{\partial_{\mathrm{MV}}}H^1(S^1;R)
\longrightarrow0.
$$

Maka $\partial_{\mathrm{MV}}$ adalah isomorfisma dan
$H^1(S^1;R)\cong R$.

Fungsi $h$ dengan nilai $(0,1_R)$ pada $(W_0,W_1)$ mewakili generator hasil
bagi $(R\oplus R)/\Delta R$. Pilih korantai nol $f$ pada $U$ yang
restriksinya ke irisan sama dengan $h$—sebagai fungsi pada titik, kita dapat
memperluas nilai-nilainya secara sembarang—dan ambil pasangan $(f,0)$.
Selisih restriksinya ialah $h$. Karena $h$ sebuah kosiklus nol,
$(\delta f,0)$ terletak di kernel selisih restriksi dan karena itu menentukan
korantai kecil satu pada $S^1$. Kelasnya ialah
$\partial_{\mathrm{MV}}[h]$. Isomorfisma di atas menunjukkan bahwa kelas ini
adalah generator $H^1(S^1;R)$ yang bersesuaian dengan $1_R$.
:::

::: {.exercise #o012-rbt-l27-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 27.6 (seluruh kohomologi sfera).** Gunakan rekurensi

$$
\widetilde H^{k-1}(S^{n-1};R)
\cong\widetilde H^k(S^n;R)
$$

untuk membuktikan, bagi $n\geq1$, bahwa

$$
\widetilde H^k(S^n;R)\cong
\begin{cases}
R,&k=n,\\
0,&k\ne n,
\end{cases}
$$

untuk semua $k\geq0$. Deduksikan kohomologi biasa dan buktikan bahwa tidak
ada $S^n$ dengan $n\geq1$ yang kontraktil.
:::

::: {.hint #o012-rbt-l27-hint-006 data-origin="edition-original"}
**Petunjuk.** Untuk $k=n$, turunkan kedua indeks sampai $(0,0)$. Jika
$0<k<n$, proses berakhir pada derajat nol dari sfera berdimensi positif. Jika
$k>n$, proses berakhir pada derajat positif dari $S^0$. Bandingkan hasilnya
dengan kohomologi tereduksi sebuah titik.
:::

::: {.solution #o012-rbt-l27-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 27.6.** Untuk $k=n$, iterasi rekurensi memberi

$$
\widetilde H^n(S^n;R)
\cong\widetilde H^{n-1}(S^{n-1};R)
\cong\cdots\cong\widetilde H^0(S^0;R)
\cong R.
$$

Jika $0<k<n$, setelah $k$ langkah kita sampai pada

$$
\widetilde H^k(S^n;R)
\cong\widetilde H^0(S^{n-k};R).
$$

Karena $n-k\geq1$, sfera $S^{n-k}$ terhubung lintasan, sehingga ruas kanan
nol. Jika $k>n$, setelah $n$ langkah kita memperoleh

$$
\widetilde H^k(S^n;R)
\cong\widetilde H^{k-n}(S^0;R)=0,
$$

karena $k-n>0$. Akhirnya,
$\widetilde H^0(S^n;R)=0$ untuk $n\geq1$ oleh keterhubungan lintasan. Jadi
hanya derajat $n$ yang tak-nol dalam kohomologi tereduksi.

Pada derajat positif, kohomologi biasa sama dengan kohomologi tereduksi,
sedangkan keterhubungan lintasan memberi $H^0(S^n;R)\cong R$. Maka

$$
H^k(S^n;R)\cong
\begin{cases}
R,&k=0\text{ atau }k=n,\\
0,&k>0\text{ dan }k\ne n.
\end{cases}
$$

Jika $S^n$ kontraktil, invariansi homotopi akan memberi
$\widetilde H^k(S^n;R)=0$ untuk semua $k$. Namun
$\widetilde H^n(S^n;R)\cong R$, yang tak-nol untuk gelanggang koefisien
tak-nol. Ini kontradiksi. Jadi $S^n$ tidak kontraktil untuk setiap $n\geq1$.
:::

::: {.boundary #o012-rbt-l27-boundary-001}
**Batas ke Unit 28.** Unit 27 menerjemahkan Notes.tex baris 5824--5923 secara
kontigu dan menutup seluruh objek sumber pada rentang itu. Baris 5924 berbunyi
`From\lecturenum{28} the calculation of the connected components and the
fundamental group ...`, memulai Kuliah 28, dan tidak dimasukkan. Kursor sumber
berikutnya yang tepat adalah **Notes.tex baris 5924**.
:::
