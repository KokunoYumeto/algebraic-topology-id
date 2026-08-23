---
title: "Topologi Aljabar"
subtitle: "Unit 19: Bundel Homogen, Ekuivalensi Homotopi Lemah, dan Kompleks"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l19-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 3678--3947 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L3678-L3947)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang 270 baris itu dimulai dengan penanda Kuliah 19 dan berakhir pada
baris kosong tepat sebelum penanda Kuliah 20 pada baris 3948. Materi sumber
dan adaptasi Indonesia ini tersedia di bawah [Creative Commons Attribution
4.0 International](https://creativecommons.org/licenses/by/4.0/).

Perubahan edisi mencakup penerjemahan, pemformatan ulang agar mudah dibaca,
pemberian pengenal stabil, dan pemindahan ketiga belas catatan pinggir ke
urutan bacaan utama. Keempat diagram Xy-pic dan kedua gambar TikZ sumber
ditulis ulang sebagai diagram, tabel, dan deskripsi semantik terpusat yang
menyebutkan setiap objek, arah, serta label panah. Edisi juga menerapkan
koreksi audit pada aksi kanan dan serat hasil bagi, rentang $n\geq3$, tanda
peta penghubung, hipotesis keterhinggaan karakteristik Euler, arti produk
$R^S$, dimensi ruang bagi operator vektor, komutativitas morfisma kompleks,
augmentasi kompleks de Rham, perbedaan jenis invarian, serta konvensi graf
berarah. Salah eja dan salah tata bahasa sumber diperbaiki tanpa mengubah
urutan matematisnya.

Rentang sumber aktif memuat tepat enam definisi, dua belas contoh, dua lema,
satu catatan, satu lingkungan bukti yang ditandai sebagai latihan, lima belas
tampilan `\[...\]`, satu tampilan `align*`, dua label sumber, empat diagram
Xy-pic, dan dua gambar TikZ. Tidak ada sitasi, rujukan silang, gambar
eksternal, `input`, atau `include`. Teorema bundel hasil bagi subgrup
tertutup, fakta penutup ganda grup matriks berdimensi rendah, fakta umum
$\pi_2$ bagi grup Lie, sifat Lingkaran Warsawa, dan bentuk global Lema
Poincaré ditandai secara jujur sebagai hasil eksternal atau kotak hitam bila
dipakai. Latihan sumber tentang fungtorialitas $\operatorname{slpc}$
diselesaikan lengkap di tempatnya.

Keenam pemeriksaan penguasaan, keenam petunjuk, dan keenam solusi lengkap
merupakan materi asli edisi dan tersedia di bawah CC BY 4.0. Edisi ini
bersifat independen; edisi ini tidak disponsori, didukung, disahkan, ataupun
diberi status resmi oleh David Michael Roberts atau institusinya. Produksi
edisi ini dibantu oleh **OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini
menambah transparansi proses dan tidak mengurangi kredit penulis sumber
ataupun kredit kontributor manusia.

# Kuliah 19 {#o012-rbt-l19}

## Bundel hasil bagi grup Lie {#o012-rbt-l19-s01}

Sumber besar bundel serat yang dapat dikenai barisan eksak panjang berasal
dari grup Lie. Misalkan $G$ grup Lie dan $H\leq G$ subgrup tertutup. Bentuk
$G/H$ sebagai ruang orbit bagi **aksi kanan**

$$
G\times H\longrightarrow G,
\qquad
(g,h)\longmapsto g\cdot h=gh.
$$

Pemetaan hasil bagi

$$
q\colon G\longrightarrow G/H,
\qquad
q(g)=gH,
$$

merupakan bundel serat. Ini adalah **teorema hasil bagi subgrup tertutup**,
suatu hasil eksternal yang dipakai di sini sebagai kotak hitam. Serat di
atas $gH$ ialah orbit $gH$ itu sendiri. Perkalian kanan membuat serat ini
sebuah torsor-$H$: aksinya bebas dan transitif. Setelah memilih $g$ di dalam
serat, pemetaan $h\mapsto gh$ memberi homeomorfisma $H\cong gH$, tetapi
tanpa pilihan tersebut serat tidak teridentifikasi secara kanonik dengan
$H$.

::: {.source-margin #o012-rbt-l19-margin-001}
> **Catatan pinggir sumber.** Contoh grup Lie matriks ialah
> $GL(n,\mathbb R)$, $O(n)$, $SO(n)$, $U(n)$, dan $SU(n)$: berturut-turut
> grup matriks invertibel real, ortogonal, ortogonal khusus, uniter, dan
> uniter khusus. “Khusus” berarti determinannya $1$. Dalam setiap keluarga
> terdapat pemasukan blok tertutup $K(n)\hookrightarrow K(n+1)$ melalui
> $A\mapsto\operatorname{diag}(A,1)$; selain itu
> $SO(n)\subseteq O(n)$ dan $SU(n)\subseteq U(n)$. Daftar ini bukan satu
> rantai inklusi tunggal—misalnya grup ortogonal real dan grup uniter
> kompleks tidak boleh dicampur menjadi satu rantai hanya karena ditulis
> berurutan.
:::

::: {.source-audit #o012-rbt-l19-audit-001}
**Audit sumber 19.1.** Notes.tex baris 3678 mempunyai ketaksesuaian
subjek--verba. Baris 3680 juga tidak menyebutkan sisi aksi dan menyebut serat
“isomorfik dengan $H$” tanpa mencatat pilihannya. Edisi memakai aksi kanan
$g\cdot h=gh$, menyatakan serat sebagai torsor-$H$, dan membedakan
homeomorfisma setelah memilih titik dari identifikasi kanonik yang memang
tidak tersedia.
:::

::: {.example #o012-rbt-l19-ex-001}
**Contoh 19.1 (sfera sebagai ruang homogen).** Aksi standar pada vektor
satuan memberikan bundel serat

$$
SO(n)\longrightarrow SO(n+1)
\longrightarrow SO(n+1)/SO(n)\cong S^n
$$

dan

$$
SU(n)\longrightarrow SU(n+1)
\longrightarrow SU(n+1)/SU(n)\cong S^{2n+1}.
$$

Identifikasi ruang homogen tersebut dipakai oleh sumber tanpa bukti;
Pemeriksaan Penguasaan 19.1 memverifikasi aksi, stabilisator, dan seratnya.
:::

::: {.example #o012-rbt-l19-ex-002}
**Contoh 19.2 (bundel Hopf sebagai hasil bagi).** Bundel Hopf kompleks juga
berbentuk demikian:

$$
U(1)\longrightarrow SU(2)
\longrightarrow SU(2)/U(1)\cong S^2,
$$

dengan pemasukan

$$
U(1)\hookrightarrow SU(2),
\qquad
z\longmapsto
\begin{pmatrix}
z&0\\
0&\overline z
\end{pmatrix}.
$$

Identifikasi $SU(2)/U(1)\cong S^2$ adalah fakta standar eksternal yang
dipakai sumber tanpa bukti dalam unit ini.
:::

Karena $SU(1)$, yakni grup matriks uniter $1\times1$ berdeterminan $1$,
trivial, kita memperoleh

$$
SU(2)=SU(2)/SU(1)\cong S^3.
$$

Ada homomorfisma surjektif

$$
SU(2)\longrightarrow SO(3)
$$

dengan kernel pusat $\{\pm I\}$. Jadi

$$
SO(3)\cong SU(2)/\{\pm I\},
$$

dan $SU(2)\to SO(3)$ adalah bundel serat, bahkan ruang penutup ganda.

::: {.source-margin #o012-rbt-l19-margin-002}
> **Catatan pinggir sumber.** Sebagai grup Lie, $SU(2)$ isomorfik dengan
> grup kuaternion satuan. Konjugasi oleh kuaternion satuan mempertahankan
> subruang kuaternion imajiner murni, yang dapat diidentifikasi dengan
> $\mathbb R^3$, dan bertindak padanya sebagai rotasi. Konstruksi ini
> menghasilkan homomorfisma $SU(2)\to SO(3)$ di atas.
:::

Isomorfisma kuaternion, surjektivitas, dan perhitungan kernel tersebut adalah
fakta standar eksternal dalam unit ini. Karena $SU(2)\cong S^3$ terhubung
sederhana dan $\{\pm I\}$ bertindak bebas dengan hasil bagi $SO(3)$,
teori ruang penutup memberi

$$
\pi_1(SO(3),I)\cong\{\pm I\}\cong\mathbb Z/2\mathbb Z.
$$

Sekarang terapkan barisan eksak panjang pada bundel
$SO(n)\to SO(n+1)\to S^n$. Bagi $n\geq3$, bagian ekornya adalah

$$
\cdots\longrightarrow
\pi_2(S^n,*)=0\longrightarrow
\pi_1(SO(n),I)\longrightarrow
\pi_1(SO(n+1),I)\longrightarrow
\pi_1(S^n,*)=0\longrightarrow\cdots.
$$

Keeksakan menunjukkan bahwa

$$
\pi_1(SO(n),I)\longrightarrow\pi_1(SO(n+1),I)
$$

isomorfisma bagi $n\geq3$. Dimulai dari $SO(3)$, induksi memberi

$$
\pi_1(SO(n),I)\cong\mathbb Z/2\mathbb Z
\qquad(n\geq3).
$$

Untuk $n=2$, bagian barisan eksaknya adalah

$$
\cdots\longrightarrow
\pi_2(SO(3),I)\longrightarrow
\pi_2(S^2,*)=\mathbb Z\xrightarrow{\delta}
\pi_1(SO(2),I)\longrightarrow
\pi_1(SO(3),I)\longrightarrow
\pi_1(S^2,*)=0\longrightarrow\cdots.
$$

Grup $SO(2)$ homeomorfik dengan $S^1$, sehingga
$\pi_1(SO(2),I)\cong\mathbb Z$. Setelah memasukkan grup-grup yang sudah
diketahui, kita memperoleh

$$
\cdots\longrightarrow
\pi_2(SO(3),I)\xrightarrow{\pi_*}\mathbb Z
\xrightarrow{\delta}\mathbb Z
\xrightarrow{i_*}\mathbb Z/2\mathbb Z
\longrightarrow0.
$$

Pemetaan $i_*$ surjektif, maka kernelnya $2\mathbb Z$. Keeksakan memberi

$$
\operatorname{im}(\delta)=2\mathbb Z.
$$

Jadi, setelah generator bagi kedua salinan $\mathbb Z$ dipilih,
$\delta$ adalah perkalian dengan $+2$ atau $-2$. Tanda $+2$ hanya diperoleh
setelah pilihan generator dan orientasi dibuat serasi; tanpa pilihan itu,
kesimpulan kanoniknya hanyalah perkalian dengan $\pm2$. Karena peta ini
injektif, $\ker\delta=0$, sehingga keeksakan juga memberi $\pi_*=0$.

Perhitungan ini memberi informasi bukan hanya tentang grup-grup homotopi,
tetapi juga tentang pemetaan yang diinduksi di antaranya; informasi tentang
pemetaan itu sama pentingnya.

Satu langkah lebih tinggi dapat ditulis

$$
\cdots\longrightarrow
\pi_2(SO(2),I)\xrightarrow{i_*}
\pi_2(SO(3),I)\xrightarrow{0}\mathbb Z
\xrightarrow{\times(\pm2)}\mathbb Z
\xrightarrow{\bmod 2}\mathbb Z/2\mathbb Z
\longrightarrow0.
$$

Karena
$\pi_2(SO(2),I)\cong\pi_2(S^1,*)=0$, citra $i_*$ trivial. Akan tetapi,
keeksakan pada $\pi_2(SO(3),I)$ mengatakan bahwa citra ini adalah kernel
pemetaan nol ke $\mathbb Z$, yakni seluruh $\pi_2(SO(3),I)$. Maka

$$
\pi_2(SO(3),I)=0.
$$

Hasil yang sama juga mengikuti dari penutup
$SU(2)\to SO(3)$ dan $SU(2)\cong S^3$, jika fakta
$\pi_2(S^3)=0$ sudah tersedia.

::: {.source-audit #o012-rbt-l19-audit-002}
**Audit sumber 19.2.** Notes.tex baris 3692 menghilangkan variabel dari
syarat “$\geq3$”. Baris 3704 menggandakan sebuah verba dan menetapkan tanda
$+2$ tanpa menyebut pilihan generator. Rentang yang benar ialah $n\geq3$,
sedangkan keeksakan sendiri hanya menentukan
$\operatorname{im}\delta=2\mathbb Z$ dan dengan demikian faktor
$\pm2$.
:::

::: {.remark #o012-rbt-l19-rem-001}
**Catatan 19.1 (fakta keras tentang grup Lie; kotak hitam).** Untuk setiap
grup Lie berdimensi hingga $G$ dengan unsur identitas $e$, berlaku

$$
\pi_2(G,e)=0.
$$

Ini adalah hasil eksternal yang sulit dan tidak dibuktikan oleh sumber
ataupun edisi ini.
:::

## Ekuivalensi homotopi lemah {#o012-rbt-l19-s02}

Pada awal mata kuliah kita mengatakan bahwa topologi aljabar mencari
invarian ruang terhadap deformasi kontinu, yakni terhadap ekuivalensi
homotopi. Namun, itu belum seluruh ceritanya. Jika suatu pemetaan
$f\colon X\to Y$ menginduksi isomorfisma pada seluruh grup homotopi, maka
kumpulan invarian tersebut tidak dapat membedakan $X$ dari $Y$. Gagasan ini
menuntun ke definisi berikut.

::: {.source-audit #o012-rbt-l19-audit-003}
**Audit sumber 19.3.** Edisi memperbaiki frasa salah “whose story” pada
Notes.tex baris 3714 menjadi “whole story”, yang diterjemahkan sebagai
“seluruh ceritanya”.
:::

::: {.definition #o012-rbt-l19-def-001}
**Definisi 19.1 (ekuivalensi homotopi lemah).** Sebuah pemetaan ruang
$f\colon X\to Y$ disebut *ekuivalensi homotopi lemah* jika fungtor yang
diinduksinya

$$
\Pi_1(X)\longrightarrow\Pi_1(Y)
$$

merupakan ekuivalensi grupoid dan, untuk setiap $x\in X$ dan setiap
$n>1$, homomorfisma

$$
f_*\colon\pi_n(X,x)\longrightarrow\pi_n(Y,f(x))
$$

merupakan isomorfisma.

::: {.source-margin #o012-rbt-l19-margin-003}
> **Catatan pinggir sumber.** Syarat pada grupoid fundamental ekuivalen
> dengan meminta bijeksi pada **komponen lintasan**
> $[\mathrm{pt},X]\xrightarrow{\sim}[\mathrm{pt},Y]$ dan isomorfisma
> $\pi_1(X,x)\xrightarrow{\sim}\pi_1(Y,f(x))$ untuk setiap $x\in X$.
> Notasi $[\mathrm{pt},X]$ di sini tidak diganti dengan $\pi_0(X)$, sebab
> mata kuliah membedakan komponen lintasan dari komponen terhubung.
:::
:::

::: {.example #o012-rbt-l19-ex-003}
**Contoh 19.3.** Setiap ekuivalensi homotopi
$f\colon X\to Y$ merupakan ekuivalensi homotopi lemah.
:::

Kebalikannya tidak selalu benar.

::: {.example #o012-rbt-l19-ex-004}
**Contoh 19.4 (kurva sinus topolog).** Tuliskan

$$
C=
\left\{
\left(x,\sin\frac1x\right):0<x\leq\frac1\pi
\right\}
\cup
\bigl(\{0\}\times[-1,1]\bigr).
$$

Ruang $C$ mempunyai dua komponen lintasan: kurva berosilasi dan ruas
vertikal limit. Pilih satu titik pada masing-masing komponen dan beri
$\{a,b\}$ topologi diskret. Pemetaan perwakilan

$$
j\colon\{a,b\}\longrightarrow C
$$

merupakan ekuivalensi homotopi lemah. Kedua komponen lintasan $C$
kontraktil, sehingga semua grup homotopi bertitiknya trivial, persis seperti
pada ruang dua titik diskret, dan $j$ bijektif pada komponen lintasan.
Namun, $C$ terhubung, sehingga setiap pemetaan kontinu
$C\to\{a,b\}$ konstan dan tidak dapat menjadi invers homotopi bagi $j$.
Pemeriksaan Penguasaan 19.3 memberikan verifikasi lengkap kedua klaim.
:::

::: {.example #o012-rbt-l19-ex-005}
**Contoh 19.5 (Lingkaran Warsawa).** Lingkaran Warsawa $W$ dibentuk dari
kurva sinus topolog dengan menambahkan sebuah busur dari “titik ujung bebas”
komponen berosilasi ke komponen vertikal pada sumbu $y$.

::: {.source-margin #o012-rbt-l19-margin-004}
> **Catatan pinggir sumber.** Secara lebih formal, ambil hasil bagi
> $C\sqcup[0,1]\to W$ dengan mengidentifikasi $0$ dan $1$ dengan kedua
> titik yang sesuai pada $C$. Gambar TikZ yang semula berada di catatan
> pinggir dipindahkan ke Diagram 19.1 agar geometri pentingnya berada dalam
> urutan bacaan utama.
:::

::: {.figure #o012-rbt-l19-fig-001 data-source-format="tikz"}
**Diagram 19.1 (deskripsi semantik Lingkaran Warsawa).** Tetapkan

$$
\Gamma=
\left\{\left(x,\sin\frac1x\right):0<x\leq\frac1\pi\right\},
\qquad
L=\{0\}\times[-1,1],
\qquad
C=\Gamma\cup L.
$$

Kurva $\Gamma$ berosilasi semakin rapat ketika $x\to0^+$ dan mempunyai
ruas vertikal limit $L$. Tambahkan busur penutup $\alpha$ yang berujung pada
$(1/\pi,0)\in\Gamma$ dan $(0,0)\in L$, serta yang selain pada kedua titik
ujung itu tidak berpotongan dengan $C$. Dengan demikian data gambar sumber
dapat ditulis tanpa bergantung pada posisi atau warna sebagai

$$
W=C\cup\alpha,
\qquad
\alpha\colon(1/\pi,0)\rightsquigarrow(0,0).
$$
:::

Ruang $W$ terhubung lintasan tetapi semua grup homotopinya trivial. Karena
itu pemetaan $W\to\mathrm{pt}$ adalah ekuivalensi homotopi lemah. Meskipun
demikian, $W$ tidak kontraktil: kontraksi akan memaksa perilaku lintasan yang
tidak mungkin melintasi dua komponen lintasan kurva sinus topolog asal.
Trivialitas semua grup homotopi dan ketidakkontraktilan ini adalah fakta
eksternal dalam unit; kalimat singkat sumber bukan bukti lengkap, sehingga
edisi tidak mengklaim telah membuktikannya.
:::

## Penggantian SLPC {#o012-rbt-l19-s03}

Kelas contoh berikut menjelaskan mengapa pembatasan umum pada ruang-ruang
SLPC tidak banyak merugikan dari sudut pandang homotopi lemah. Di sini
**SLPC** tetap berarti *terhubung lintasan semilokal* menurut Definisi 4.2
mata kuliah: ekuivalen dengan syarat bahwa setiap komponen lintasan terbuka.
Istilah ini tidak berarti SLSC dan tidak diganti dengan pengertian standar
lain tentang keterhubungan lintasan lokal.

::: {.definition #o012-rbt-l19-def-002}
**Definisi 19.2 (ruang $\operatorname{slpc}(X)$).** Untuk ruang $X$, beri
himpunan komponen lintasan $[\mathrm{pt},X]$ topologi hasil bagi dari
pemetaan

$$
q_X\colon X\longrightarrow[\mathrm{pt},X].
$$

Tuliskan

$$
D_X=\operatorname{disc}[\mathrm{pt},X]
$$

untuk himpunan yang sama dengan topologi diskret, dan biarkan
$i_X\colon D_X\to[\mathrm{pt},X]$ menjadi fungsi bijektif identitas pada
himpunan yang mendasarinya. Definisikan

$$
\operatorname{slpc}(X)
=D_X\times_{[\mathrm{pt},X]}X
$$

sebagai pullback pada Diagram 19.2.

::: {.figure #o012-rbt-l19-fig-002 data-source-format="xymatrix"}
**Diagram 19.2 (pullback yang mendefinisikan
$\operatorname{slpc}(X)$).** Keempat objek dan semua panahnya adalah

$$
\begin{array}{ccc}
D_X\times_{[\mathrm{pt},X]}X&
\xrightarrow{\ p_2\ }&X\\
{\scriptstyle p_1}\downarrow&&
\downarrow{\scriptstyle q_X}\\
D_X&\xrightarrow{\ i_X\ }&[\mathrm{pt},X].
\end{array}
$$

Panah atas $p_2$ menuju $X$, panah kiri $p_1$ menuju ruang diskret $D_X$,
panah kanan adalah pemetaan komponen $q_X$, dan panah bawah $i_X$ melupakan
topologi diskret. Pernyataan bahwa persegi ini pullback berarti titik sudut
kiri atas tepat pasangan $([x],x)$ dengan $[x]=q_X(x)$.
:::
:::

Secara himpunan, setiap $x\in X$ muncul tepat sekali sebagai $([x],x)$.
Topologi baru itu membuat $X$ menjadi gabungan saling lepas topologis dari
komponen-komponen lintasannya, sambil mempertahankan topologi subruang pada
setiap komponen.

::: {.lemma #o012-rbt-l19-lem-001}
**Lema 19.1 (fungtorialitas penggantian SLPC).** Penetapan
$X\mapsto\operatorname{slpc}(X)$ adalah komponen objek suatu fungtor

$$
\operatorname{slpc}\colon\mathbf{Top}\longrightarrow\mathbf{Top}
$$

yang nilainya terletak dalam subkategori penuh ruang-ruang SLPC.
:::

::: {.proof #o012-rbt-l19-proof-001 data-source-exercise="true"}
**Bukti (latihan sumber, diselesaikan edisi).** Diberikan pemetaan kontinu
$f\colon X\to Y$, citra suatu lintasan di $X$ adalah lintasan di $Y$.
Karena itu terdapat fungsi pada komponen lintasan

$$
[\mathrm{pt},f]\colon[\mathrm{pt},X]\longrightarrow[\mathrm{pt},Y],
\qquad
[x]\longmapsto[f(x)].
$$

Fungsi yang sama di antara ruang diskret $D_X\to D_Y$ otomatis kontinu.
Pasangan pemetaan

$$
D_X\longrightarrow D_Y,
\qquad
X\xrightarrow{f}Y
$$

kompatibel dengan kedua pemetaan ke himpunan komponen, sebab

$$
q_Y\circ f=[\mathrm{pt},f]\circ q_X.
$$

Sifat universal pullback kemudian memberi pemetaan kontinu unik

$$
\operatorname{slpc}(f)\colon
\operatorname{slpc}(X)\longrightarrow\operatorname{slpc}(Y),
\qquad
([x],x)\longmapsto([f(x)],f(x)).
$$

Rumus ini segera memberi

$$
\operatorname{slpc}(\operatorname{id}_X)
=\operatorname{id}_{\operatorname{slpc}(X)}
$$

dan, bagi $X\xrightarrow{f}Y\xrightarrow{g}Z$,

$$
\operatorname{slpc}(g\circ f)
=\operatorname{slpc}(g)\circ\operatorname{slpc}(f).
$$

Jadi penetapan tersebut fungtorial. Terakhir, serat proyeksi
$p_1\colon\operatorname{slpc}(X)\to D_X$ adalah salinan satu komponen
lintasan $X$. Serat itu terbuka karena $D_X$ diskret, dan ia memang
terhubung lintasan karena topologinya sama dengan topologi subruang komponen
asal. Maka setiap komponen lintasan $\operatorname{slpc}(X)$ terbuka. Dengan
karakterisasi SLPC mata kuliah, $\operatorname{slpc}(X)$ bersifat SLPC.
$\square$
:::

Menurut konstruksi, proyeksi kedua memberi pemetaan kontinu bijektif

$$
\varepsilon_X\colon\operatorname{slpc}(X)\longrightarrow X,
\qquad
([x],x)\longmapsto x,
$$

yang merupakan identitas pada himpunan yang mendasarinya.

::: {.lemma #o012-rbt-l19-lem-002}
**Lema 19.2 (perbandingan dengan ruang asal).** Pemetaan

$$
\varepsilon_X\colon\operatorname{slpc}(X)\longrightarrow X
$$

merupakan ekuivalensi homotopi lemah. Jika $X$ tidak bersifat SLPC, pemetaan
ini bukan ekuivalensi homotopi.
:::

Bukti lengkap kedua pernyataan Lema 19.2 diberikan bersama penguatan
“hanya jika” pada Solusi Pemeriksaan 19.4. Jadi klaim ini tidak dibiarkan
sebagai kotak hitam. Akibatnya, jika ruang yang ekuivalen secara homotopi
lemah tidak hendak dibedakan, bekerja hanya dengan ruang SLPC relatif tidak
merugikan.

## Kompleks dan motivasi karakteristik Euler {#o012-rbt-l19-s04}

Ingat karakteristik Euler sebuah poliedron **berhingga** $P$. Dalam dimensi
dua,

$$
\chi(P)
=\underbrace{\#(\text{simpul})}_{\text{dimensi }0}
-\underbrace{\#(\text{sisi})}_{\text{dimensi }1}
+\underbrace{\#(\text{muka})}_{\text{dimensi }2}.
$$

Poliedron itu tidak harus konveks, terhubung sederhana, atau bahkan
terhubung. Bagi poliedron berhingga berdimensi berhingga, rumusnya meluas
menjadi

$$
\chi(P)
=\sum_{d=0}^{\dim P}(-1)^d
\#(\text{muka berdimensi }d).
$$

Karakteristik Euler tidak bersifat fungtorial secara langsung, sehingga
sukar membandingkan karakteristik Euler poliedron berbeda hanya dari daftar
jumlah mukanya. Gagasan kuncinya ialah mengganti jumlah simpul, sisi, dan
seterusnya dengan dimensi ruang vektor yang sesuai. Untuk data berhingga,
jumlah tersebut dapat dipulihkan sebagai dimensi.

Untuk poliedron tak berhingga, jumlah kardinal berselang-seling tidak dengan
sendirinya mendefinisikan karakteristik Euler; diperlukan hipotesis
keterhinggaan atau teori konvergensi yang sesuai. Demikian pula, bagi
himpunan tak berhingga $S$, ruang fungsi $R^S$ yang muncul di bawah adalah
produk, bukan modul bebas berdukungan hingga, dan dimensinya sebagai ruang
vektor tidak harus $|S|$.

::: {.source-margin #o012-rbt-l19-margin-005}
> **Catatan pinggir sumber.** Salah satu sumber data tak berhingga ialah
> triangulasi sebuah permukaan bergenus tak berhingga. Contoh ini memotivasi
> ruang vektor tak berdimensi hingga, tetapi tidak membenarkan penjumlahan
> kardinal berselang-seling tanpa syarat tambahan.
:::

::: {.source-audit #o012-rbt-l19-audit-004}
**Audit sumber 19.4.** Notes.tex baris 3789--3793 tidak membatasi formula
elementer karakteristik Euler dan rekonstruksi dimensi pada data berhingga,
serta salah mengeja “vertex”. Edisi menyatakan hipotesis keterhinggaan dan
memisahkan produk fungsi $R^S$ dari modul bebas berdukungan hingga.
:::

::: {.definition #o012-rbt-l19-def-003}
**Definisi 19.3 (kompleks bergradasi naik).** Sebuah *kompleks*
$A_\bullet$ dari ruang vektor, grup abelian, atau modul atas $R$ adalah barisan

$$
\cdots\longrightarrow
A_{n-1}\xrightarrow{d_{n-1}}A_n
\xrightarrow{d_n}A_{n+1}\longrightarrow\cdots
$$

sedemikian sehingga

$$
d_n\circ d_{n-1}=0
\qquad\text{untuk setiap }n.
$$

Gradasi sumber bersifat **kohomologis**: diferensial
$d_n\colon A_n\to A_{n+1}$ menaikkan derajat.

::: {.source-margin #o012-rbt-l19-margin-006}
> **Catatan pinggir sumber.** Persamaan
> $d_n\circ d_{n-1}=0$ ekuivalen dengan
> $\operatorname{im}(d_{n-1})\subseteq\ker(d_n)$.
:::
:::

::: {.example #o012-rbt-l19-ex-006}
**Contoh 19.6.** Setiap barisan eksak, misalnya barisan grup abelian,
merupakan kompleks karena pada setiap suku citra diferensial sebelumnya
sama dengan kernel diferensial berikutnya, dan khususnya termuat di
dalamnya.
:::

Seperti pada barisan eksak, sebuah kompleks dapat mempunyai hanya satu ruas
berhingga yang tidak trivial, sedangkan semua suku lain nol. Dalam keadaan
itu kita cukup menuliskan ruas yang tidak trivial.

::: {.example #o012-rbt-l19-ex-007}
**Contoh 19.7 (kompleks yang tidak eksak).** Tempatkan tiga suku tak nol
pada derajat $0,1,2$. Barisan

$$
0\longrightarrow\mathbb Z
\xrightarrow{\times4}\mathbb Z
\xrightarrow{\bmod2}\mathbb Z/2\mathbb Z
\longrightarrow0
$$

adalah kompleks karena reduksi modulo $2$ membunuh $4\mathbb Z$. Pemetaan
kiri injektif dan pemetaan kanan surjektif, tetapi

$$
4\mathbb Z\subsetneq2\mathbb Z;
$$

jadi citra pada suku tengah tidak sama dengan kernelnya.
:::

::: {.example #o012-rbt-l19-ex-008}
**Contoh 19.8 (kompleks matriks).** Misalkan $A$ dan $B$ matriks real
$n\times n$ dengan $BA=0$. Maka

$$
0\longrightarrow\mathbb R^n
\xrightarrow{A}\mathbb R^n
\xrightarrow{B}\mathbb R^n
\longrightarrow0
$$

adalah kompleks. Kompleks ini tidak mungkin eksak. Jika eksak, $A$ harus
injektif dan $B$ harus surjektif. Karena keduanya endomorfisma ruang vektor
berdimensi hingga yang sama, keduanya lalu invertibel, bertentangan dengan
$BA=0$.
:::

Sekarang ambil $U\subset\mathbb R^3$ **terbuka**. Tuliskan $C^\infty(U)$
untuk ruang vektor fungsi mulus $U\to\mathbb R$ dan
$C^\infty(U,\mathbb R^3)$ untuk ruang vektor medan vektor mulus pada $U$.

::: {.example #o012-rbt-l19-ex-009}
**Contoh 19.9 (kompleks kalkulus vektor).** Operator turunan gradien
$\nabla$, rotor (*curl*) $\nabla\times-$, dan divergensi
$\nabla\mathbin{\cdot}-$ membentuk kompleks yang dinotasikan
$\Omega^\bullet(U)$:

$$
C^\infty(U)\xrightarrow{\nabla}
C^\infty(U,\mathbb R^3)\xrightarrow{\nabla\times-}
C^\infty(U,\mathbb R^3)\xrightarrow{\nabla\mathbin{\cdot}-}
C^\infty(U)\longrightarrow0.
$$

Memang, rotor suatu gradien nol dan divergensi suatu rotor nol.
:::

::: {.source-audit #o012-rbt-l19-audit-005}
**Audit sumber 19.5.** Notes.tex baris 3830 menulis
$U\subset\mathbb R^n$, padahal medan vektor yang ditampilkan bernilai
$\mathbb R^3$ dan operator rotor serta divergensinya adalah operator tiga
dimensi. Edisi mensyaratkan $U\subset\mathbb R^3$ terbuka. Salah gabung
“acomplex” pada baris 3833 juga diperbaiki.
:::

## Morfisma kompleks {#o012-rbt-l19-s05}

::: {.definition #o012-rbt-l19-def-004}
**Definisi 19.4 (morfisma kompleks).** Sebuah *morfisma kompleks*
$f\colon A_\bullet\to B_\bullet$ terdiri atas pemetaan yang mempertahankan
derajat

$$
f_n\colon A_n\longrightarrow B_n
$$

untuk setiap $n$, sedemikian sehingga **setiap** persegi pada Diagram 19.3
komutatif.

::: {.figure #o012-rbt-l19-fig-003 data-source-format="xymatrix"}
**Diagram 19.3 (persegi morfisma kompleks).** Objek dan panah lengkapnya
adalah

$$
\begin{array}{ccc}
A_{n-1}&\xrightarrow{\ d^A_{n-1}\ }&A_n\\
{\scriptstyle f_{n-1}}\downarrow&&
\downarrow{\scriptstyle f_n}\\
B_{n-1}&\xrightarrow{\ d^B_{n-1}\ }&B_n.
\end{array}
$$

Panah mendatar atas berjalan dari $A_{n-1}$ ke $A_n$, panah mendatar bawah
dari $B_{n-1}$ ke $B_n$, dan kedua panah vertikal masing-masing ialah
$f_{n-1}$ serta $f_n$. Komutativitas berarti

$$
f_n\circ d^A_{n-1}=d^B_{n-1}\circ f_{n-1}.
$$
:::

Kategori kompleks modul atas $R$ dan morfisma kompleks dinotasikan
$\mathbf{Cplx}_R$.

::: {.source-margin #o012-rbt-l19-margin-007}
> **Catatan pinggir sumber.** Sumber mengatakan bahwa pemetaan ini kadang
> disebut *chain map*. Karena diferensial yang ditampilkan menaikkan derajat,
> $d_n\colon A_n\to A_{n+1}$, edisi memakai istilah netral **morfisma
> kompleks**; dalam konvensi yang membedakan gradasi, istilah
> *cochain map* juga lazim. Arah panah tidak dibalik.
:::
:::

::: {.source-audit #o012-rbt-l19-audit-006}
**Audit sumber 19.6.** Definisi pada Notes.tex baris 3840--3851 berhenti
secara sintaksis setelah kata “all the squares” tanpa mengatakan apa yang
harus dipenuhi. Edisi melengkapinya dengan syarat bahwa setiap persegi
komutatif dan menuliskan persamaan komutativitasnya.
:::

::: {.example #o012-rbt-l19-ex-010}
**Contoh 19.10 (morfisma dari kompleks matriks).** Untuk matriks $A,B$ pada
Contoh 19.8, syarat $BA=0$ membuat pemetaan

$$
\overline B\colon\mathbb R^n/\operatorname{im}(A)
\longrightarrow\mathbb R^n,
\qquad
\overline B([x])=Bx
$$

terdefinisi baik. Data berikut membentuk morfisma kompleks.

::: {.figure #o012-rbt-l19-fig-004 data-source-format="xymatrix"}
**Diagram 19.4 (padanan semantik diagram matriks enam kolom).** Kompleks
atas, dari kiri ke kanan, adalah

$$
0\longrightarrow0\longrightarrow\mathbb R^n
\xrightarrow{A}\mathbb R^n
\xrightarrow{B}\mathbb R^n\longrightarrow0,
$$

sedangkan kompleks bawah, dengan posisi kolom yang sama, adalah

$$
0\longrightarrow\ker(A)\longrightarrow0
\longrightarrow\mathbb R^n/\operatorname{im}(A)
\xrightarrow{\overline B}\mathbb R^n\longrightarrow0.
$$

Peta vertikal yang mempertahankan setiap posisi adalah sebagai berikut.

| Posisi | Objek atas | Peta vertikal | Objek bawah |
|---:|:---:|:---:|:---:|
| 1 | $0$ | $\operatorname{id}_0$ | $0$ |
| 2 | $0$ | peta nol $0\to\ker(A)$ | $\ker(A)$ |
| 3 | $\mathbb R^n$ | peta nol $\mathbb R^n\to0$ | $0$ |
| 4 | $\mathbb R^n$ | peta hasil bagi $q$ | $\mathbb R^n/\operatorname{im}(A)$ |
| 5 | $\mathbb R^n$ | $\operatorname{id}_{\mathbb R^n}$ | $\mathbb R^n$ |
| 6 | $0$ | $\operatorname{id}_0$ | $0$ |

Dengan demikian hubungan vertikal tidak dikodekan hanya oleh posisi. Semua
panah mendatar yang tidak berlabel adalah peta nol yang ditentukan oleh
sumber atau targetnya, kecuali peta bawah $\overline B$ yang telah diberi
label.
:::

Persegi pada $A$ komutatif karena $qA=0$. Persegi pada $B$ komutatif karena

$$
\overline B\,q=B.
$$

Semua persegi lain mempunyai kedua komposit nol atau identitas pada objek
nol. Jadi setiap persegi benar-benar komutatif.
:::

::: {.source-audit #o012-rbt-l19-audit-007}
**Audit sumber 19.7.** Notes.tex baris 3853 kehilangan artikel dalam “There
is map”, dan diagramnya tidak memberi label pada peta-peta vertikal ataupun
peta terinduksi di baris bawah. Diagram 19.4 menyebutkan peta nol, hasil
bagi, identitas, serta $\overline B$ dan memeriksa semua perseginya.
:::

::: {.example #o012-rbt-l19-ex-011}
**Contoh 19.11 (pembatasan operator diferensial).** Untuk setiap himpunan
terbuka $U\subset\mathbb R^3$, pembatasan fungsi dan medan vektor memberi
morfisma kompleks

$$
\Omega^\bullet(\mathbb R^3)\longrightarrow\Omega^\bullet(U).
$$

::: {.figure #o012-rbt-l19-fig-005 data-source-format="xymatrix"}
**Diagram 19.5 (padanan semantik diagram pembatasan).** Kompleks sumbernya
adalah

$$
C^\infty(\mathbb R^3)\xrightarrow{\nabla}
C^\infty(\mathbb R^3,\mathbb R^3)
\xrightarrow{\nabla\times-}
C^\infty(\mathbb R^3,\mathbb R^3)
\xrightarrow{\nabla\mathbin{\cdot}-}
C^\infty(\mathbb R^3)\longrightarrow0,
$$

dan kompleks targetnya adalah

$$
C^\infty(U)\xrightarrow{\nabla}
C^\infty(U,\mathbb R^3)
\xrightarrow{\nabla\times-}
C^\infty(U,\mathbb R^3)
\xrightarrow{\nabla\mathbin{\cdot}-}
C^\infty(U)\longrightarrow0.
$$

Hubungan vertikal pada lima posisi, dari sumber ke target, ialah

| Posisi | Peta vertikal dari baris $\mathbb R^3$ ke baris $U$ |
|---:|:---|
| 1 | pembatasan fungsi $\rho_0(f)=f|_U$ |
| 2 | pembatasan medan vektor $\rho_1(\mathbf v)=\mathbf v|_U$ |
| 3 | pembatasan medan vektor $\rho_2(\mathbf v)=\mathbf v|_U$ |
| 4 | pembatasan fungsi $\rho_3(f)=f|_U$ |
| 5 | satu-satunya peta $0\to0$, yakni $\operatorname{id}_0$ |

Setiap peta mendatar menuju ke kanan. Setiap peta vertikal menuju dari data
global pada $\mathbb R^3$ ke pembatasannya pada $U$.
:::

Operator diferensial bersifat lokal, sehingga pembatasan berkomutasi dengan
gradien, rotor, dan divergensi. Dengan demikian keempat persegi pada Diagram
19.5 komutatif.
:::

## Keeksakan kalkulus vektor dan informasi topologis {#o012-rbt-l19-s06}

Kompleks **tak teraugmentasi** $\Omega^\bullet(\mathbb R^3)$ pada Contoh
19.9 tidak eksak pada suku pertama $C^\infty(\mathbb R^3)$, sebab kernel
gradien adalah fungsi-fungsi konstan. Ia eksak pada derajat positif. Secara
ekuivalen, kompleks yang diaugmentasi

$$
0\longrightarrow\mathbb R
\xrightarrow{\ c\ }C^\infty(\mathbb R^3)
\xrightarrow{\nabla}C^\infty(\mathbb R^3,\mathbb R^3)
\xrightarrow{\nabla\times-}C^\infty(\mathbb R^3,\mathbb R^3)
\xrightarrow{\nabla\mathbin{\cdot}-}C^\infty(\mathbb R^3)
\longrightarrow0,
$$

dengan $c(r)$ fungsi konstan bernilai $r$, adalah eksak.

::: {.source-margin #o012-rbt-l19-margin-008}
> **Catatan pinggir sumber.** Keeksakan ini mengikuti Lema Poincaré, atau
> secara lebih elementer dari hasil standar kalkulus multivariabel.
:::

Lema Poincaré global pada $\mathbb R^3$ dipakai di sini sebagai hasil
analitik eksternal: medan vektor berotor nol adalah gradien, medan vektor
berdivergensi nol adalah rotor, dan setiap fungsi mulus adalah divergensi
suatu medan vektor mulus. Kontraktilitas $\mathbb R^3$ menjelaskan mengapa
tidak ada obstruksi topologis pada derajat positif.

Untuk

$$
U=\mathbb R^3\setminus\{0\},
$$

keadaan berbeda. Sebagai contoh konkret,

$$
\mathbf v(x)=\frac{x}{\lVert x\rVert^3}
$$

berdivergensi nol pada $U$, tetapi bukan rotor medan vektor global pada
$U$: fluksnya melalui sfera satuan adalah $4\pi$, sedangkan fluks rotor
melalui permukaan tertutup harus nol. Ruang $U$ ekuivalen secara homotopi
dengan $S^2$. Kohomologi de Rham
$H^2_{\mathrm{dR}}(U;\mathbb R)\cong\mathbb R$ mengukur kegagalan

$$
\ker(\nabla\mathbin{\cdot}-)
=\operatorname{im}(\nabla\times-).
$$

Grup $\pi_2(S^2)\cong\mathbb Z$ juga mendeteksi topologi sfera, tetapi
kedua objek itu **bukan invarian yang sama**: yang pertama adalah ruang
vektor kohomologi real, sedangkan yang kedua adalah grup homotopi integral.
Perbandingannya hanya kualitatif.

Demikian pula, ambil

$$
U=\mathbb R^3\setminus\ell,
$$

dengan $\ell\subset\mathbb R^3$ subruang berdimensi satu.

::: {.source-margin #o012-rbt-l19-margin-009}
> **Catatan pinggir sumber.** Contoh pilihan $\ell$ ialah sumbu $z$.
:::

Ruang ini ekuivalen secara homotopi dengan $S^1$. Untuk sumbu $z$, medan
vektor

$$
\mathbf w(x,y,z)
=\left(
-\frac{y}{x^2+y^2},
\frac{x}{x^2+y^2},
0
\right)
$$

mempunyai rotor nol pada $U$, tetapi bukan gradien fungsi global: integral
garisnya mengelilingi lingkaran satuan adalah $2\pi$, sedangkan integral
garis gradien pada loop tertutup selalu nol. Jadi

$$
\ker(\nabla\times-)
\neq\operatorname{im}(\nabla).
$$

Pada akhirnya, bukan ukuran ruang vektornya yang membawa informasi penting.
Ruang-ruang fungsi dalam $\Omega^\bullet(\mathbb R^3)$ sangat besar dan
berdimensi tak hingga, sedangkan $\mathbb R^3$ sendiri tidak menarik secara
homotopis. Kompleks de Rham analog pada $\mathbb R^n$ juga mempunyai
fenomena yang sama, dengan bentuk diferensial pada semua derajat sebagai
pengganti notasi gradien--rotor--divergensi khusus dimensi tiga.

::: {.source-margin #o012-rbt-l19-margin-010}
> **Catatan pinggir sumber.** Kernel gradien terdiri tepat atas fungsi
> konstan dan karenanya isomorfik dengan $\mathbb R$. Ruang vektor satu
> dimensi itu sejalan dengan fakta bahwa himpunan komponen lintasan
> $[\mathrm{pt},\mathbb R^3]=*$; pernyataan ini tidak menyamakan kedua
> jenis invarian.
:::

::: {.source-audit #o012-rbt-l19-audit-008}
**Audit sumber 19.8.** Notes.tex baris 3874 menyebut kompleks tak
teraugmentasi eksak, padahal fungsi konstan membentuk kernel gradien.
Edisi menyatakan keeksakan positif dan menampilkan augmentasi
$\mathbb R\hookrightarrow C^\infty(\mathbb R^3)$. Baris 3880--3886 kini
membedakan kohomologi de Rham real dari $\pi_2(S^2)$, dan frasa salah “the
image gradient” pada baris 3892 diperbaiki menjadi citra gradien.
:::

## Graf berarah dan kompleksnya {#o012-rbt-l19-s07}

Kita beralih ke contoh yang jauh lebih kecil untuk menghangatkan aljabar
yang akan muncul.

::: {.definition #o012-rbt-l19-def-005 data-source-label="def:directed_grph"}
**Definisi 19.5 (graf berarah sederhana).** Sebuah *graf berarah sederhana*
terdiri atas himpunan simpul $V$, himpunan sisi $E$, dan dua fungsi

$$
d_0,d_1\colon E\longrightarrow V
$$

sedemikian sehingga

$$
(d_0,d_1)\colon E\longrightarrow V\times V
$$

injektif dan

$$
\operatorname{im}(d_0,d_1)\cap\Delta(V)=\varnothing.
$$

::: {.source-margin #o012-rbt-l19-margin-011}
> **Catatan pinggir sumber.** Di sini
> $\Delta(V)=\{(v,v):v\in V\}\subseteq V^2$ adalah diagonal.
:::
:::

Konvensi arah sumber adalah sebagai berikut: sebuah sisi $e$ menunjuk dari
**sumber** $d_1(e)$ ke **target** $d_0(e)$. Syarat diagonal melarang loop
dari sebuah simpul ke dirinya sendiri. Injektivitas $(d_0,d_1)$ mengizinkan
paling banyak satu sisi bagi setiap **pasangan terurut** target--sumber.
Namun, ia masih mengizinkan dua sisi dengan arah berlawanan di antara dua
simpul yang sama, sebab pasangan terurutnya berbeda.

::: {.source-audit #o012-rbt-l19-audit-009}
**Audit sumber 19.9.** Notes.tex baris 3910 mengatakan secara terlalu luas
bahwa tidak ada lebih dari satu sisi “di antara” dua simpul. Definisi hanya
melarang pengulangan pasangan terurut $(d_0,d_1)$; dua sisi berlawanan arah
tetap diizinkan. Edisi juga mengulang konvensi $d_1(e)\to d_0(e)$ dalam
kata-kata agar orientasi tidak bergantung pada kepala panah.
:::

::: {.example #o012-rbt-l19-ex-012 data-source-label="eg:triangle_graph"}
**Contoh 19.12 (segitiga berarah).** Ambil

$$
V=\{A,B,C\},
\qquad
E=\{a,b,c\}.
$$

::: {.source-margin #o012-rbt-l19-margin-012}
> **Catatan pinggir sumber.** Sumber menempatkan gambar TikZ segitiga di
> margin. Diagram itu dipindahkan ke Diagram 19.6 dan diuraikan sebagai
> tabel sumber--target sehingga arah tidak disampaikan hanya secara visual.
:::

::: {.figure #o012-rbt-l19-fig-006 data-source-format="tikz"}
**Diagram 19.6 (deskripsi semantik segitiga berarah).** Ketiga sisi dan
arahnya ialah

| Sisi | Sumber $d_1$ | Target $d_0$ | Panah berlabel |
|:---:|:---:|:---:|:---:|
| $a$ | $A$ | $B$ | $a\colon A\to B$ |
| $b$ | $B$ | $C$ | $b\colon B\to C$ |
| $c$ | $A$ | $C$ | $c\colon A\to C$ |

Jadi $a$ berjalan dari $A$ ke $B$, $b$ dari $B$ ke $C$, dan $c$ langsung
dari $A$ ke $C$. Daftar ini memuat seluruh simpul, sisi, label, dan arah
gambar sumber tanpa memakai warna atau posisi sebagai kode.
:::

Dengan sengaja menuliskan pasangan dalam urutan sumber--target, datanya
adalah

$$
(d_1,d_0)\colon
\begin{cases}
a\longmapsto(A,B),\\
b\longmapsto(B,C),\\
c\longmapsto(A,C).
\end{cases}
$$

Graf ini dinotasikan $\partial\Delta[2]$, untuk alasan yang akan menjadi
lebih jelas kemudian. Perhatikan bahwa definisi kesederhanaan menguji
injektivitas $(d_0,d_1)$, sedangkan tampilan contoh memilih urutan
$(d_1,d_0)$ agar terbaca sebagai sumber lalu target.
:::

Untuk membentuk kompleks dari graf berarah sederhana, bagi himpunan $S$ dan
gelanggang $R$ tuliskan

$$
R^S=\{f:S\to R\},
$$

modul semua fungsi dengan operasi titik demi titik.

::: {.source-margin #o012-rbt-l19-margin-013}
> **Catatan pinggir sumber.** Untuk $R=\mathbb Z$, modul $R^S$ adalah
> produk $\prod_{s\in S}\mathbb Z$; untuk $R$ medan, ia adalah ruang semua
> fungsi $S\to R$. Bila $S$ berhingga, produk ini sama dengan jumlah
> langsung dan dimensinya $|S|$. Bila $S$ tak berhingga, ia bukan modul
> bebas berdukungan hingga $R^{(S)}$, dan dimensi ruang vektornya tidak
> harus $|S|$.
:::

Definisi berikut memakai $R=\mathbb Z$, tetapi rumus yang sama berlaku bagi
gelanggang umum.

::: {.definition #o012-rbt-l19-def-006}
**Definisi 19.6 (kompleks graf).** Untuk graf berarah sederhana
$d_0,d_1\colon E\rightrightarrows V$, definisikan kompleks

$$
\begin{aligned}
0\quad\longrightarrow\quad
\mathbb Z^V&\xrightarrow{\ \delta\ }\mathbb Z^E
\quad\longrightarrow\quad0,\\
f&\longmapsto f\circ d_0-f\circ d_1.
\end{aligned}
$$

Jadi bagi sisi $e$ yang berarah dari $d_1(e)$ ke $d_0(e)$,

$$
\delta(f)(e)=f(d_0(e))-f(d_1(e)),
$$

yakni nilai pada target dikurangi nilai pada sumber. Kompleks ini ditempatkan
pada derajat $0$ dan $1$, sesuai gradasi kohomologis yang menaikkan derajat.
:::

# Pendamping penguasaan: pemeriksaan, petunjuk, dan solusi lengkap {.unnumbered #o012-rbt-l19-mastery}

Enam pemeriksaan berikut, keenam petunjuknya, dan keenam solusi lengkapnya
merupakan materi asli edisi. Semuanya terbatas pada sasaran beku Unit 19:
ruang homogen dan seratnya, perhitungan barisan eksak grup ortogonal,
ekuivalensi lemah kurva sinus topolog, penggantian SLPC, kohomologi kompleks
dan morfisma matriks, serta kobatas segitiga berarah. Tidak ada pemeriksaan
yang memakai materi Kuliah 20.

::: {.exercise #o012-rbt-l19-mcheck-001 data-origin="edition-original"}
**Pemeriksaan penguasaan 19.1 (bundel ruang homogen).** Untuk $n\geq1$:

1. Tunjukkan bahwa aksi standar $SO(n+1)$ pada $S^n\subset\mathbb R^{n+1}$
   transitif dan bahwa stabilisator $e_{n+1}$ adalah salinan blok $SO(n)$.
2. Tunjukkan bahwa aksi standar $SU(n+1)$ pada
   $S^{2n+1}\subset\mathbb C^{n+1}$ transitif dan bahwa stabilisator
   $e_{n+1}$ adalah salinan blok $SU(n)$.
3. Turunkan identifikasi
   $SO(n+1)/SO(n)\cong S^n$ dan
   $SU(n+1)/SU(n)\cong S^{2n+1}$, lalu jelaskan serat setiap pemetaan hasil
   bagi menurut konvensi aksi kanan.
:::

::: {.hint #o012-rbt-l19-hint-001 data-origin="edition-original"}
**Petunjuk.** Lengkapi sebuah vektor satuan menjadi basis ortonormal atau
uniter. Dalam kasus uniter, sesuaikan determinan pada salah satu vektor basis
yang bukan $e_{n+1}$. Untuk serat, bandingkan dua unsur $g,g'$ yang mempunyai
citra sama pada vektor terakhir.
:::

::: {.solution #o012-rbt-l19-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 19.1.** Pertama, $SO(n+1)$ bertindak pada $S^n$ melalui

$$
g\cdot v=gv.
$$

Untuk $v\in S^n$, lengkapi $v$ menjadi basis ortonormal terorientasi

$$
(v_1,\ldots,v_n,v)
$$

dari $\mathbb R^{n+1}$. Matriks yang kolom-kolomnya basis ini berada dalam
$SO(n+1)$ dan mengirim $e_{n+1}$ ke $v$. Jadi aksinya transitif.

Jika $g\in SO(n+1)$ menetapkan $e_{n+1}$, maka komplemen ortogonal
$e_{n+1}^{\perp}$ dipertahankan. Pembatasan $g$ pada komplemen itu adalah
matriks $A\in O(n)$, dan

$$
1=\det(g)=\det(A),
$$

sehingga $A\in SO(n)$. Sebaliknya, setiap
$A\in SO(n)$ memberi
$\operatorname{diag}(A,1)\in SO(n+1)$ yang menetapkan $e_{n+1}$. Maka
stabilisatornya tepat salinan blok $SO(n)$.

Untuk kasus kompleks, $SU(n+1)$ bertindak pada sfera satuan
$S^{2n+1}\subset\mathbb C^{n+1}$. Ambil $v$ pada sfera itu dan pilih
$T\in U(n+1)$ dengan $Te_{n+1}=v$. Karena $n\geq1$, ada koordinat basis
yang berbeda dari koordinat terakhir. Kalikan $T$ di kanan dengan matriks
diagonal $D$ yang menetapkan $e_{n+1}$ dan mempunyai

$$
\det(D)=\det(T)^{-1}.
$$

Maka $TD\in SU(n+1)$ dan tetap mengirim $e_{n+1}$ ke $v$. Jadi aksi
$SU(n+1)$ transitif. Unsur $g\in SU(n+1)$ yang menetapkan $e_{n+1}$
mempunyai bentuk blok $\operatorname{diag}(A,1)$ dengan $A\in U(n)$; syarat
$\det g=1$ memberi $\det A=1$, jadi $A\in SU(n)$. Kebalikannya langsung,
maka stabilisatornya $SU(n)$.

Untuk kedua kasus, tuliskan $G$ bagi grup besar, $H$ bagi stabilisator, dan
$v_0=e_{n+1}$. Pemetaan orbit

$$
\Phi\colon G/H\longrightarrow G\cdot v_0,
\qquad
gH\longmapsto gv_0
$$

terdefinisi baik: jika $g'=gh$ dengan $h\in H$, maka
$g'v_0=ghv_0=gv_0$. Jika $gv_0=g'v_0$, maka
$g^{-1}g'$ menetapkan $v_0$, jadi $g^{-1}g'\in H$ dan $gH=g'H$.
Transitivitas memberi surjektivitas. Pemetaan orbit
$o\colon G\to G\mathbin{\cdot}v_0$, $o(g)=gv_0$, kontinu dan konstan pada
setiap orbit kanan $H$, sehingga sifat universal topologi hasil bagi memberi
kontinuitas $\Phi$. Dalam kedua kasus, $G=SO(n+1)$ atau $SU(n+1)$ kompak,
maka hasil baginya $G/H$ kompak; sfera sasaran bersifat Hausdorff. Karena itu
bijeksi kontinu $\Phi$ adalah homeomorfisma. Jadi

$$
SO(n+1)/SO(n)\cong S^n,
\qquad
SU(n+1)/SU(n)\cong S^{2n+1}.
$$

Serat pemetaan $G\to G/H$ di atas $gH$ adalah orbit $gH$, yaitu koset kiri
$gH$. Aksi kanan

$$
gH\times H\longrightarrow gH,
\qquad
(gh_1,h_2)\longmapsto gh_1h_2
$$

bebas dan transitif, jadi serat sebuah torsor-$H$. Pilihan $g$ menghasilkan
homeomorfisma $H\to gH$, $h\mapsto gh$, tetapi pilihan $gh_0$ akan mengubah
koordinat itu. Dengan demikian serat hanya nonkanonik homeomorfik dengan
$H$.
:::

::: {.exercise #o012-rbt-l19-mcheck-002 data-origin="edition-original"}
**Pemeriksaan penguasaan 19.2 (perhitungan barisan eksak ortogonal).** Pakai
bundel

$$
SO(n)\longrightarrow SO(n+1)\longrightarrow S^n
$$

dan fakta $\pi_1(SO(3))\cong\mathbb Z/2\mathbb Z$ untuk:

1. menurunkan $\pi_1(SO(n))\cong\mathbb Z/2\mathbb Z$ bagi semua
   $n\geq3$;
2. membuktikan $\pi_2(SO(3))=0$ dari kasus $n=2$;
3. menjelaskan mengapa peta penghubung $\mathbb Z\to\mathbb Z$ hanya
   merupakan perkalian dengan $\pm2$ sebelum generator dan orientasi dipilih
   secara serasi.
:::

::: {.hint #o012-rbt-l19-hint-002 data-origin="edition-original"}
**Petunjuk.** Untuk $n\geq3$, apit pemetaan pada $\pi_1$ di antara
$\pi_2(S^n)=0$ dan $\pi_1(S^n)=0$. Untuk $n=2$, kernel surjeksi
$\mathbb Z\to\mathbb Z/2$ adalah $2\mathbb Z$. Lalu gunakan satu suku lebih
ke kiri dan fakta $\pi_2(SO(2))=0$.
:::

::: {.solution #o012-rbt-l19-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 19.2.** Bagi $n\geq3$, barisan eksak panjang memuat

$$
0=\pi_2(S^n)\longrightarrow\pi_1(SO(n))
\xrightarrow{i_*}\pi_1(SO(n+1))
\longrightarrow\pi_1(S^n)=0.
$$

Keeksakan membuat $i_*$ injektif dari nol di kiri dan surjektif dari nol di
kanan, jadi $i_*$ isomorfisma. Mulai dengan

$$
\pi_1(SO(3))\cong\mathbb Z/2\mathbb Z
$$

dan terapkan isomorfisma tersebut berturut-turut untuk
$n=3,4,\ldots$. Diperoleh

$$
\pi_1(SO(n))\cong\mathbb Z/2\mathbb Z
\qquad(n\geq3).
$$

Untuk $n=2$, gunakan $SO(2)\cong S^1$ dan bagian eksak

$$
\pi_2(SO(3))\xrightarrow{\pi_*}\mathbb Z
\xrightarrow{\delta}\mathbb Z
\xrightarrow{i_*}\mathbb Z/2\mathbb Z\longrightarrow0.
$$

Pemetaan $i_*$ surjektif. Setiap surjeksi dari grup siklik tak hingga ke
grup siklik orde dua mempunyai kernel $2\mathbb Z$, sehingga

$$
\operatorname{im}\delta=\ker i_*=2\mathbb Z.
$$

Homomorfisma $\delta\colon\mathbb Z\to\mathbb Z$ ditentukan oleh citra satu
generator. Agar citranya tepat $2\mathbb Z$, generator itu harus dikirim ke
$2$ atau $-2$ kali generator target. Karena itu

$$
\delta=\times(\pm2).
$$

Mengganti generator pada salah satu salinan $\mathbb Z$ membalik tanda;
pilihan orientasi pada sfera dan lingkaran juga menentukan generator. Hanya
setelah pilihan tersebut dibuat serasi kita boleh menulis $+2$.

Pemetaan $\delta$ injektif, jadi $\ker\delta=0$. Keeksakan pada salinan
$\mathbb Z=\pi_2(S^2)$ memberi $\operatorname{im}\pi_*=0$, sehingga
$\pi_*$ adalah peta nol. Sekarang sertakan suku sebelumnya:

$$
\pi_2(SO(2))\xrightarrow{i_*}\pi_2(SO(3))
\xrightarrow{0}\mathbb Z.
$$

Karena $SO(2)\cong S^1$,
$\pi_2(SO(2))=0$, maka $\operatorname{im}i_*=0$. Di sisi lain, keeksakan
pada $\pi_2(SO(3))$ memberi

$$
\operatorname{im}i_*
=\ker(0)
=\pi_2(SO(3)).
$$

Jadi $\pi_2(SO(3))=0$.
:::

::: {.exercise #o012-rbt-l19-mcheck-003 data-origin="edition-original"}
**Pemeriksaan penguasaan 19.3 (lemah tidak berarti ekuivalen homotopi).**
Untuk kurva sinus topolog

$$
C=
\left\{\left(x,\sin\frac1x\right):0<x\leq\frac1\pi\right\}
\cup(\{0\}\times[-1,1]),
$$

pilih satu titik pada masing-masing komponen lintasan dan definisikan
$j\colon\{a,b\}_{\mathrm{disc}}\to C$. Verifikasi langsung dari Definisi
19.1 bahwa $j$ ekuivalensi homotopi lemah. Kemudian buktikan bahwa $j$ tidak
mungkin merupakan ekuivalensi homotopi.
:::

::: {.hint #o012-rbt-l19-hint-003 data-origin="edition-original"}
**Petunjuk.** Proyeksi pada koordinat $x$ mengidentifikasi komponen
berosilasi dengan $(0,1/\pi]$, sedangkan komponen limit adalah sebuah
interval. Untuk penolakan ekuivalensi homotopi, gunakan bahwa $C$ terhubung
tetapi ruang dua titik diskret tidak, lalu amati bentuk homotopi di ruang
diskret.
:::

::: {.solution #o012-rbt-l19-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 19.3.** Tuliskan

$$
\Gamma=
\left\{\left(x,\sin\frac1x\right):0<x\leq\frac1\pi\right\},
\qquad
L=\{0\}\times[-1,1].
$$

Kedua himpunan ini adalah komponen lintasan $C$. Proyeksi
$(x,\sin(1/x))\mapsto x$ adalah homeomorfisma
$\Gamma\cong(0,1/\pi]$, dan $L\cong[-1,1]$. Keduanya kontraktil, sehingga
grup fundamental dan semua grup homotopi lebih tingginya trivial.

Pemetaan $j$ memilih satu objek pada masing-masing dari dua komponen. Ia
bijektif pada himpunan komponen lintasan. Grupoid fundamental $C$ tidak
mempunyai morfisma di antara kedua komponen; di dalam masing-masing
komponen, hanya ada satu kelas homotopi lintasan di antara setiap dua titik
karena komponen itu kontraktil. Karena itu fungtor

$$
\Pi_1(\{a,b\})\longrightarrow\Pi_1(C)
$$

sepenuhnya setia dan surjektif esensial, jadi suatu ekuivalensi grupoid.
Untuk setiap titik basis yang dipilih dan $n>1$, pemetaan terinduksi adalah
isomorfisma dari grup trivial ke grup trivial. Maka $j$ ekuivalensi homotopi
lemah.

Sekarang $\Gamma$ terhubung dan $C=\overline\Gamma$, sehingga $C$
terhubung. Andaikan $j$ mempunyai invers homotopi
$r\colon C\to\{a,b\}$. Citra ruang terhubung oleh peta kontinu terhubung,
sedangkan satu-satunya subruang terhubung dari ruang dua titik diskret adalah
satu titik. Jadi $r$ konstan dan $rj$ juga konstan.

Setiap homotopi

$$
H\colon\{a,b\}\times I\longrightarrow\{a,b\}
$$

menetapkan citra setiap titik sepanjang suatu lintasan dalam ruang diskret;
lintasan itu harus konstan. Karena itu dua pemetaan ruang dua titik diskret
homotopik hanya jika keduanya sama. Pemetaan konstan $rj$ tidak sama dengan
$\operatorname{id}_{\{a,b\}}$, sehingga tidak dapat homotopik dengannya.
Ini bertentangan dengan syarat invers homotopi. Jadi $j$ bukan ekuivalensi
homotopi.
:::

::: {.exercise #o012-rbt-l19-mcheck-004 data-origin="edition-original"}
**Pemeriksaan penguasaan 19.4 (penggantian SLPC).** Diberikan pemetaan
$f\colon X\to Y$:

1. bangun $\operatorname{slpc}(f)$ dan buktikan hukum identitas serta
   komposisi;
2. buktikan bahwa $\operatorname{slpc}(X)$ bersifat SLPC;
3. buktikan bahwa
   $\varepsilon_X\colon\operatorname{slpc}(X)\to X$ merupakan ekuivalensi
   homotopi lemah;
4. buktikan bahwa jika $\varepsilon_X$ merupakan ekuivalensi homotopi, maka
   setiap komponen lintasan $X$ terbuka. Tunjukkan pula bahwa bila semua
   komponen lintasan terbuka, $\varepsilon_X$ sebenarnya homeomorfisma.
:::

::: {.hint #o012-rbt-l19-hint-004 data-origin="edition-original"}
**Petunjuk.** Gunakan fungsi
$[x]\mapsto[f(x)]$ di antara diskretisasi himpunan komponen. Semua lintasan,
sfera bertitik, dan homotopi berparameter terletak di dalam satu komponen
lintasan. Untuk syarat perlu, komposisikan calon invers homotopi dengan
proyeksi $\operatorname{slpc}(X)\to\operatorname{disc}[\mathrm{pt},X]$.
:::

::: {.solution #o012-rbt-l19-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 19.4.** Tuliskan

$$
D_X=\operatorname{disc}[\mathrm{pt},X],
\qquad
D_Y=\operatorname{disc}[\mathrm{pt},Y].
$$

Pemetaan kontinu $f$ membawa lintasan ke lintasan, maka menentukan fungsi

$$
D(f)\colon D_X\longrightarrow D_Y,
\qquad
[x]\longmapsto[f(x)].
$$

Fungsi ini kontinu karena domain dan target diskret. Fungsi pada ruang
komponen dengan topologi hasil bagi juga kontinu: persamaan

$$
q_Yf=[\mathrm{pt},f]q_X
$$

dan sifat hasil bagi $q_X$ membuktikannya. Pasangan $D(f)$ dan $f$ kompatibel
dengan pemetaan ke $[\mathrm{pt},Y]$, sehingga sifat universal pullback
memberi

$$
\operatorname{slpc}(f)([x],x)
=([f(x)],f(x)).
$$

Untuk identitas,

$$
\operatorname{slpc}(\operatorname{id}_X)([x],x)
=([x],x).
$$

Untuk $X\xrightarrow{f}Y\xrightarrow{g}Z$, kedua ruas persamaan fungtor
mengirim $([x],x)$ ke $([g(f(x))],g(f(x)))$. Karena itu

$$
\operatorname{slpc}(g\circ f)
=\operatorname{slpc}(g)\circ\operatorname{slpc}(f).
$$

Selanjutnya, proyeksi

$$
p_1\colon\operatorname{slpc}(X)\longrightarrow D_X
$$

mempunyai serat

$$
p_1^{-1}([x])
=\{([x],y):y\in[x]\}.
$$

Serat ini homeomorfik dengan komponen lintasan $[x]\subseteq X$, sebab
pembatasan $p_2$ adalah homeomorfisma ke subruang tersebut. Jadi seratnya
terhubung lintasan. Karena $D_X$ diskret, setiap serat juga terbuka.
Serat-serat ini tepat komponen lintasan $\operatorname{slpc}(X)$, maka semua
komponen lintasannya terbuka dan ruang itu SLPC menurut konvensi mata kuliah.

Pemetaan $\varepsilon_X=p_2$ adalah identitas pada himpunan yang
mendasarinya dan membatasi pada homeomorfisma di setiap komponen lintasan.
Setiap lintasan di $X$ tinggal di satu komponen, sehingga dapat dipandang
secara unik sebagai lintasan di $\operatorname{slpc}(X)$; hal yang sama
berlaku bagi homotopi lintasan. Dengan demikian

$$
\Pi_1(\operatorname{slpc}(X))
\longrightarrow\Pi_1(X)
$$

bahkan merupakan isomorfisma grupoid setelah objek-objek diidentifikasi.
Untuk $n>1$, citra setiap pemetaan bertitik $S^n\to X$ berada di komponen
lintasan titik basis karena $S^n$ terhubung lintasan. Citra setiap homotopi
$S^n\times I\to X$ juga berada di komponen itu. Homeomorfisma per komponen
kemudian memberi isomorfisma

$$
\pi_n(\operatorname{slpc}(X),x)
\xrightarrow{\ \cong\ }\pi_n(X,x)
$$

untuk semua $n>1$. Jadi $\varepsilon_X$ ekuivalensi homotopi lemah.

Terakhir, andaikan $\varepsilon_X$ ekuivalensi homotopi dan pilih invers
homotopi

$$
r\colon X\longrightarrow\operatorname{slpc}(X).
$$

Cukup gunakan salah satu homotopinya,
$H\colon\varepsilon_Xr\simeq\operatorname{id}_X$. Komposit

$$
p_1r\colon X\longrightarrow D_X
$$

kontinu. Bagi setiap $x\in X$, lintasan $t\mapsto H(x,t)$ menghubungkan
$\varepsilon_Xr(x)$ dengan $x$. Jadi keduanya berada pada komponen lintasan
yang sama dan

$$
p_1r(x)=[x].
$$

Dengan demikian $p_1r$ adalah fungsi komponen
$X\to D_X$. Karena fungsi ini kontinu dan $D_X$ diskret, setiap seratnya

$$
(p_1r)^{-1}(\{[x]\})=[x]
$$

terbuka. Jadi setiap komponen lintasan $X$ terbuka, yakni $X$ SLPC.

Sebaliknya, jika semua komponen lintasan $X$ terbuka, fungsi
$X\to D_X$, $x\mapsto[x]$, kontinu. Maka

$$
s\colon X\longrightarrow\operatorname{slpc}(X),
\qquad
x\longmapsto([x],x)
$$

kontinu dan merupakan invers dua sisi $\varepsilon_X$. Jadi
$\varepsilon_X$ homeomorfisma. Secara ringkas,

$$
\varepsilon_X\text{ ekuivalensi homotopi}
\quad\Longrightarrow\quad
X\text{ SLPC}
\quad\Longrightarrow\quad
\varepsilon_X\text{ homeomorfisma}.
$$
:::

::: {.exercise #o012-rbt-l19-mcheck-005 data-origin="edition-original"}
**Pemeriksaan penguasaan 19.5 (kohomologi dan morfisma kompleks).** Tempatkan
kompleks

$$
0\longrightarrow\mathbb Z
\xrightarrow{\times4}\mathbb Z
\xrightarrow{\bmod2}\mathbb Z/2\mathbb Z
\longrightarrow0
$$

pada derajat $0,1,2$. Dengan

$$
H^k(A_\bullet)
=\ker(d_k)/\operatorname{im}(d_{k-1}),
$$

hitung $H^k$ untuk setiap $k$. Kemudian, untuk $A,B\in M_n(\mathbb R)$
dengan $BA=0$, sebutkan semua peta yang tidak diberi label dalam diagram
morfisma matriks sumber, bangun $\overline B$, dan verifikasi setiap
persegi komutatif.
:::

::: {.hint #o012-rbt-l19-hint-005 data-origin="edition-original"}
**Petunjuk.** Kernel reduksi modulo $2$ adalah $2\mathbb Z$, sedangkan citra
perkalian dengan $4$ adalah $4\mathbb Z$. Dalam diagram matriks, gunakan
peta nol, proyeksi hasil bagi $q$, identitas, dan persamaan
$\overline Bq=B$.
:::

::: {.solution #o012-rbt-l19-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 19.5.** Tuliskan diferensialnya sebagai

$$
d_0=\times4,
\qquad
d_1=\bmod2,
\qquad
d_2=0,
$$

dengan semua suku di luar derajat $0,1,2$ nol. Karena perkalian dengan $4$
pada $\mathbb Z$ injektif,

$$
H^0
=\ker(d_0)/\operatorname{im}(d_{-1})
=0/0
=0.
$$

Pada derajat $1$,

$$
\ker(d_1)=2\mathbb Z,
\qquad
\operatorname{im}(d_0)=4\mathbb Z,
$$

sehingga

$$
H^1
=2\mathbb Z/4\mathbb Z
\cong\mathbb Z/2\mathbb Z.
$$

Pemetaan $d_1$ surjektif, maka

$$
H^2
=\ker(d_2)/\operatorname{im}(d_1)
=(\mathbb Z/2\mathbb Z)/(\mathbb Z/2\mathbb Z)
=0.
$$

Semua $H^k$ lain nol karena suku kompleksnya nol. Jadi satu-satunya
kohomologi tak trivial ialah

$$
H^1\cong\mathbb Z/2\mathbb Z.
$$

Sekarang pandang diagram matriks. Dari kiri ke kanan, enam peta vertikalnya
adalah

$$
\operatorname{id}_0,
\quad
0\colon0\to\ker(A),
\quad
0\colon\mathbb R^n\to0,
\quad
q\colon\mathbb R^n\to\mathbb R^n/\operatorname{im}(A),
\quad
\operatorname{id}_{\mathbb R^n},
\quad
\operatorname{id}_0.
$$

Peta mendatar bawah yang substantif adalah

$$
\overline B\colon\mathbb R^n/\operatorname{im}(A)\longrightarrow\mathbb R^n,
\qquad
\overline B([x])=Bx.
$$

Jika $[x]=[x']$, maka $x'-x=Ay$ untuk suatu $y$, sehingga

$$
Bx'-Bx=BAy=0.
$$

Jadi $\overline B$ terdefinisi baik dan memenuhi
$\overline Bq=B$. Sekarang periksa persegi-perseginya berurutan:

1. di antara dua kolom pertama, kedua komposit adalah peta nol
   $0\to\ker(A)$;
2. di antara kolom kedua dan ketiga, kedua komposit adalah peta nol
   $0\to0$;
3. pada panah $A$, rute atas lalu turun adalah $qA=0$ karena
   $\operatorname{im}(A)$ dibunuh oleh $q$, sama dengan rute turun lalu
   mendatar melalui objek nol;
4. pada panah $B$, rute atas lalu identitas adalah $B$, sedangkan rute turun
   lalu mendatar adalah $\overline Bq=B$;
5. pada panah terakhir ke nol, kedua komposit adalah peta nol
   $\mathbb R^n\to0$.

Maka setiap persegi komutatif, dan keluarga peta vertikal itu benar-benar
morfisma kompleks.
:::

::: {.exercise #o012-rbt-l19-mcheck-006 data-origin="edition-original"}
**Pemeriksaan penguasaan 19.6 (kobatas segitiga berarah).** Untuk segitiga
Contoh 19.12, gunakan basis terurut $(A,B,C)$ bagi $\mathbb Z^V$ dan
$(a,b,c)$ bagi $\mathbb Z^E$.

1. Tuliskan matriks
   $\delta\colon\mathbb Z^V\to\mathbb Z^E$.
2. Jelaskan tanda setiap baris memakai konvensi
   $d_1(e)\to d_0(e)$ dan
   $\delta f(e)=f(d_0(e))-f(d_1(e))$.
3. Hitung $\ker\delta$ dan $\operatorname{coker}\delta$.
:::

::: {.hint #o012-rbt-l19-hint-006 data-origin="edition-original"}
**Petunjuk.** Evaluasi $\delta f$ pada $a,b,c$ secara berurutan. Untuk
kokernel, gambarkan citra sebagai semua $(x,y,z)\in\mathbb Z^3$ yang
memenuhi satu relasi primitif dan gunakan homomorfisma ke $\mathbb Z$ yang
mengukur kegagalan relasi itu.
:::

::: {.solution #o012-rbt-l19-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 19.6.** Tuliskan nilai fungsi simpul sebagai vektor

$$
(f_A,f_B,f_C)^T.
$$

Karena $a$ berarah dari $A=d_1(a)$ ke $B=d_0(a)$,

$$
\delta f(a)=f_B-f_A.
$$

Serupa, $b$ berarah dari $B$ ke $C$ dan $c$ dari $A$ ke $C$, sehingga

$$
\delta f(b)=f_C-f_B,
\qquad
\delta f(c)=f_C-f_A.
$$

Dalam basis yang diminta,

$$
[\delta]_{(a,b,c)\leftarrow(A,B,C)}
=
\begin{pmatrix}
-1&1&0\\
0&-1&1\\
-1&0&1
\end{pmatrix}.
$$

Tanda $-1$ selalu berada pada simpul sumber $d_1(e)$ dan tanda $+1$ pada
simpul target $d_0(e)$. Jadi matriks ini menerapkan “target dikurangi
sumber”, bukan kebalikannya.

Jika $\delta f=0$, dua baris pertama memberi

$$
f_B=f_A,
\qquad
f_C=f_B.
$$

Baris ketiga lalu otomatis nol. Jadi

$$
\ker\delta
=\{(t,t,t):t\in\mathbb Z\}
=\mathbb Z(1,1,1)
\cong\mathbb Z.
$$

Untuk citra, jika

$$
\delta f=(x,y,z),
$$

maka

$$
z=f_C-f_A
=(f_B-f_A)+(f_C-f_B)
=x+y.
$$

Sebaliknya, bagi setiap $(x,y,x+y)$, pilih

$$
(f_A,f_B,f_C)=(0,x,x+y);
$$

maka $\delta f=(x,y,x+y)$. Jadi

$$
\operatorname{im}\delta
=\{(x,y,z)\in\mathbb Z^3:z=x+y\}.
$$

Definisikan homomorfisma surjektif

$$
\Phi\colon\mathbb Z^3\longrightarrow\mathbb Z,
\qquad
\Phi(x,y,z)=z-x-y.
$$

Ia surjektif karena $\Phi(0,0,1)=1$, dan perhitungan di atas memberi
$\ker\Phi=\operatorname{im}\delta$. Teorema isomorfisma pertama menghasilkan

$$
\operatorname{coker}\delta
=\mathbb Z^3/\operatorname{im}\delta
\cong\mathbb Z.
$$

Dengan penempatan derajat $0$ dan $1$, hasil yang sama dapat ditulis
$H^0\cong\mathbb Z$ dan $H^1\cong\mathbb Z$ bagi kompleks graf segitiga.
:::
