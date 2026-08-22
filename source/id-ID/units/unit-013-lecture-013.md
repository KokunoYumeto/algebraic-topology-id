---
title: "Topologi Aljabar"
subtitle: "Unit 13: Amalgamasi, Pushout Grupoid, Baji, dan Kompleks Presentasi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l13-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 2727--3046 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L2727-L3046)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang itu dimulai dengan penanda Kuliah 13 dan berakhir dengan judul bagian
“Mengklasifikasikan ruang pelapis” serta baris kosong sesudahnya. Kuliah 14
dimulai di tengah berkas sumber pada baris 3047 dan tidak termasuk dalam unit
ini. Materi sumber dan adaptasi Indonesia ini tersedia di bawah [Creative
Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/).

Perubahan edisi mencakup penerjemahan, pemformatan ulang agar mudah dibaca,
pemberian pengenal stabil, dan pemindahan kesebelas catatan pinggir ke urutan
bacaan utama. Kesebelas diagram Xy-pic dan kedua gambar TikZ sumber ditulis
ulang sebagai diagram semantik dan daftar panah lengkap. Pada gambar yang
semula membedakan faktor hanya melalui warna dan posisi, setiap panah kini
diberi tag faktor $\Gamma$ atau $H$, sumber, dan sasaran; maknanya tidak lagi
bergantung pada warna atau tata letak.

Sejumlah cacat matematis sumber diperbaiki secara independen. Matriks kedua
pada contoh grup modular bertindak melalui $z\mapsto(z-1)/z$, bukan
$z\mapsto(1-z)/z$; hasil bagi bidang setengah atas juga bukan ruang pelapis
biasa karena aksi memiliki penstabil eliptik. Pada konstruksi pushout grupoid,
peran $F\colon\Lambda\to H$ dan $G\colon\Lambda\to\Gamma$ yang tertukar
dikembalikan ke tipe yang benar. Contoh relasi dan beberapa kata sumber yang
tidak dapat dikomposisikan diganti oleh kata sejajar yang dapat
dikomposisikan, dan hasil bagi dibentuk oleh kongruensi grupoid terkecil,
bukan sekadar relasi ekuivalensi terpisah yang belum dijamin kompatibel dengan
komposisi. Pada contoh lingkaran, arah $\gamma$ dan $\eta$ dipulihkan sehingga
generator kronologisnya adalah $\gamma\eta$.

Istilah “join” pada sumber dikoreksi menjadi *baji*, sesuai simbol
$\vee$ dan konstruksi yang benar-benar dipakai. Penerapan Seifert--van Kampen
untuk baji diberi hipotesis keterhubungan lintasan yang diperlukan. Peta
pelekatan kompleks presentasi dinyatakan oleh kelas loop
$[f_i]=R_i$, bukan persamaan tak bertipe $f_i(1)=R_i$; penggunaan lingkungan
berkerah dan topologi CW/lemah (*weak topology*) juga dibuat eksplisit. Salah tik
$F_n\langle\cdots\rangle$, $\Pi_(\cdots)$, “Seiert”, “coutable”, dan
“preceeding” dinormalkan. Placeholder gambar oktagon sumber diganti dengan
deskripsi sisi berarah yang lengkap.

Sumber memuat dua latihan tanpa solusi. Pendamping penguasaan yang jelas
ditandai sebagai materi asli edisi memberi solusi lengkap untuk keduanya dan
untuk keterampilan yang belum diuji: presentasi amalgamasi, reduksi kata
grupoid, sifat universal, perhitungan lingkaran, hipotesis baji, relasi yang
dibunuh oleh sel-$2$, dan kata permukaan genus-$g$. Materi pendamping itu juga
tersedia di bawah CC BY 4.0 dan tidak meminjam solusi eksternal. Edisi ini
bersifat independen; edisi ini tidak disponsori, didukung, disahkan, ataupun
diberi status resmi oleh David Michael Roberts, MIT, Haynes Miller, Sanath
Devalapurkar, Yeheli Fomberg, Nir Lazarovich, atau institusi mereka.

# Kuliah 13 {#o012-rbt-l13}

Sepanjang unit ini, produk panah $\alpha\beta$ dibaca **kronologis**:
$\alpha$ ditempuh dahulu, lalu $\beta$. Sebaliknya, tanda komposisi fungsi
tetap memakai konvensi baku kanan-ke-kiri: $g\circ f$ berarti menerapkan $f$
dahulu, lalu $g$.

## Produk bebas dengan amalgamasi {#o012-rbt-l13-s01}

::: {.definition #o012-rbt-l13-def-001}
**Definisi 13.1 (produk bebas dengan amalgamasi).** Misalkan diberikan
sepasang homomorfisma

$$
G\xleftarrow{\ \phi\ }L\xrightarrow{\ \psi\ }H.
$$

*Produk bebas dengan amalgamasi* adalah grup

$$
G*_L H
:=
(G*H)\big/
\left\langle\!\left\langle
\phi(x)\psi(x)^{-1}:x\in L
\right\rangle\!\right\rangle,
$$

di mana kurung ganda menyatakan subgrup normal terkecil dari $G*H$ yang
memuat semua unsur $\phi(x)\psi(x)^{-1}$. Homomorfisma kanonik

$$
G\longrightarrow G*_L H\longleftarrow H
$$

membuat $G*_L H$ memenuhi sifat universal pushout di $\mathbf{Grp}$.
Dengan kata lain, untuk setiap homomorfisma $u\colon G\to K$ dan
$v\colon H\to K$ dengan

$$
u\circ\phi=v\circ\psi,
$$

terdapat tepat satu $k\colon G*_L H\to K$ yang membatasi menjadi $u$ pada
$G$ dan $v$ pada $H$.
:::

Misalkan

$$
G=\langle g_1,\ldots,g_m\mid R_1,\ldots,R_n\rangle,
\qquad
H=\langle h_1,\ldots,h_k\mid Q_1,\ldots,Q_l\rangle.
$$

Maka

$$
G*_L H
\cong
\left\langle
g_1,\ldots,g_m,h_1,\ldots,h_k
\ \middle|\
R_1,\ldots,R_n,Q_1,\ldots,Q_l,
\phi(x)\psi(x)^{-1}=e\ (x\in L)
\right\rangle.
$$

Tambahkan satu relasi untuk setiap $x\in L$, atau cukup untuk setiap $x$
dalam suatu himpunan pembangkit $L$. Relasi itu ekuivalen dengan
$\phi(x)=\psi(x)$, sehingga persegi kanonik memang komutatif. Keterangan
pinggir sumber menekankan bahwa uraian melalui presentasi ini tetap berlaku
untuk grup yang tidak mempunyai presentasi berhingga: daftar pembangkit dan
relasinya boleh tak berhingga.

::: {.example #o012-rbt-l13-exa-001 data-source-label="eg:one-relator_group"}
**Contoh 13.1 (grup satu-relator).** Pertimbangkan grup satu-relator yang
dibangkitkan secara berhingga

$$
G=\langle g_1,\ldots,g_m\mid R=e\rangle,
$$

di mana $R$ adalah unsur grup bebas $F_m$ pada
$g_1,\ldots,g_m$. Grup itu merupakan pushout pada Diagram 13.1. Keterangan
pinggir sumber mencatat bahwa grup satu-relator penting dalam teori grup
geometrik dan banyak hasil telah diketahui tentangnya.
:::

::: {.figure #o012-rbt-l13-fig-001}
**Diagram 13.1 (pushout untuk satu relator).** Diagram semantiknya adalah

$$
\begin{array}{ccc}
\mathbb Z&\xrightarrow{\ !\ }&1\\
{\scriptstyle r}\downarrow&&\downarrow\\
F_m&\longrightarrow&G,
\end{array}
$$

dengan $r\colon\mathbb Z\to F_m$ ditentukan oleh $r(1)=R$ dan $!$ satu-
satunya homomorfisma ke grup trivial. Pushout memaksa citra $R$ menjadi
identitas, jadi sudut kanan bawah adalah
$F_m/\langle\!\langle R\rangle\!\rangle\cong G$.
:::

Sebagai contoh yang lebih khusus, grup permukaan berorientasi tertutup genus
$g$ mempunyai presentasi

$$
\left\langle
a_1,\ldots,a_g,b_1,\ldots,b_g
\ \middle|\
\prod_{i=1}^{g}[a_i,b_i]=e
\right\rangle.
$$

Di sini $[a,b]=aba^{-1}b^{-1}$.

Secara lebih umum lagi, setiap grup yang dipresentasikan secara berhingga
merupakan pushout pada diagram berikut.

::: {.figure #o012-rbt-l13-fig-002}
**Diagram 13.2 (pushout untuk presentasi berhingga).** Ambil

$$
F_n=\langle a_1,\ldots,a_n\mid\ \rangle,
$$

dan homomorfisma $r\colon F_n\to F_m$ yang ditentukan oleh kata relator
$r(a_1),\ldots,r(a_n)$. Maka

$$
\begin{array}{ccc}
F_n&\xrightarrow{\ !\ }&1\\
{\scriptstyle r}\downarrow&&\downarrow\\
F_m&\longrightarrow&
\langle g_1,\ldots,g_m\mid
r(a_1)=e,\ldots,r(a_n)=e\rangle
\end{array}
$$

adalah persegi pushout. Panah atas membunuh semua pembangkit $a_i$, sehingga
pushout membagi $F_m$ dengan penutupan normal semua $r(a_i)$.
:::

::: {.remark #o012-rbt-l13-rem-001}
**Catatan 13.1 (grup modular dan koreksi ruang pelapis).** Contoh terkenal
produk bebas adalah

$$
\mathbb Z/2*\mathbb Z/3\cong\operatorname{PSL}_2(\mathbb Z),
$$

dengan

$$
\operatorname{PSL}_2(\mathbb Z)
=
\operatorname{SL}_2(\mathbb Z)/\{\pm I\},
\qquad
\operatorname{SL}_2(\mathbb Z)
=
\{A\in M_2(\mathbb Z):\det A=1\}.
$$

Satu presentasi memakai kelas kedua matriks

$$
S=
\begin{pmatrix}0&-1\\1&0\end{pmatrix},
\qquad
B=
\begin{pmatrix}1&-1\\1&0\end{pmatrix};
$$

matriks kedua ditulis $ST$ dalam sumber. Di
$\operatorname{PSL}_2(\mathbb Z)$ keduanya memenuhi

$$
S^2=I,
\qquad
B^3=I.
$$

Bahwa relasi-relasi ini memberi seluruh presentasi tidak langsung jelas.
Catatan pinggir sumber merujuk Roger C. Alperin,
“$PSL_2(\mathbf Z)=\mathbf Z_2*\mathbf Z_3$,” *The American Mathematical
Monthly* 100, no. 4 (April 1993), 385--386,
[doi:10.2307/2324963](https://doi.org/10.2307/2324963).

Grup modular bertindak kontinu pada bidang setengah atas

$$
\mathcal H=\{z\in\mathbb C:\operatorname{Im}z>0\}
$$

melalui transformasi linear pecahan. Untuk dua matriks di atas,

$$
S(z)=-\frac1z,
\qquad
B(z)=\frac{z-1}{z}.
$$

Di sini sumber mencetak $(1-z)/z$, yang bukan transformasi matriks $B$.
Selain itu, orbit-orbit diskret saja tidak cukup untuk membuat
$\mathcal H\to\mathcal H/\operatorname{PSL}_2(\mathbb Z)$ suatu ruang
pelapis. Sebagai contoh, kelas $S$ bukan identitas tetapi menetapkan
$i\in\mathcal H$. Jadi aksi tidak bebas dan peta hasil bagi bukan peta
pelapis biasa pada titik eliptik; interpretasi yang tepat adalah hasil bagi
orbifold (dan peta pelapis biasa baru diperoleh setelah titik bercabang
ditangani atau grup bebas-torsi yang sesuai dipakai).
:::

## Pushout grupoid sebagai kata panah {#o012-rbt-l13-s02}

Setelah memperoleh perlakuan konkret bagi pushout grup sebagai produk bebas
dengan amalgamasi, wajar mengharapkan perlakuan serupa bagi grupoid. Hal itu
memang dapat dilakukan: morfisma pushout grupoid diwakili oleh kata-kata
dalam morfisma grupoid yang diberikan. Namun, tidak seperti kata dalam unsur
grup, rangkaian panah hanya bermakna bila sasaran setiap panah sama dengan
sumber panah berikutnya.

Kita tidak akan membangun pushout grupoid dalam keumuman penuh. Kita akan
menguraikan kasus khusus yang muncul dari teorema Seifert--van Kampen.

::: {.example #o012-rbt-l13-exa-002}
**Contoh 13.2 (bentuk yang berasal dari Seifert--van Kampen).** Misalkan
$X$ suatu ruang, $\{U,V\}$ sampul $X$ oleh lingkungan, dan
$A\subseteq U\cap V$ sedemikian sehingga setiap komponen lintasan dari
$U$, $V$, dan $U\cap V$ memuat sedikitnya satu titik $A$. Karena setiap
titik $X=U\cup V$ berada di salah satu dari $U,V$, syarat itu juga memastikan
bahwa setiap komponen lintasan $X$ bertemu $A$. Teorema Seifert--van Kampen
relatif dari Unit 12 memberi persegi pushout pada Diagram 13.3.
:::

::: {.figure #o012-rbt-l13-fig-003}
**Diagram 13.3 (pushout grupoid fundamental dengan objek tetap).** Semua
panah diinduksi oleh inklusi ruang:

$$
\begin{array}{ccc}
\Pi_1(U\cap V,A)&\xrightarrow{\ i_V\ }&\Pi_1(V,A)\\
{\scriptstyle i_U}\downarrow&&\downarrow\\
\Pi_1(U,A)&\longrightarrow&\Pi_1(X,A).
\end{array}
$$

Keempat grupoid mempunyai himpunan objek yang sama, yaitu $A$, dan setiap
fungtor pada diagram adalah identitas pada objek; misalnya $i_U(a)=a$.
Komutativitas berarti bahwa kelas lintasan di $U\cap V$ mempunyai citra yang
sama setelah dipandang di $X$ melalui salah satu dari dua rute.
:::

Dalam bukti Seifert--van Kampen, sebuah lintasan di $X$ dinyatakan sebagai
komposit ruas-ruas yang bergantian berada di $U$ dan $V$. Secara aljabar,
itulah situasi yang hendak dihitung. Untuk menyederhanakan notasi, sumber
membatasi perhatian pada $A$ berhingga, sebagaimana lazim terjadi dalam
perhitungan contoh yang cukup teratur.

Sekarang misalkan diberikan diagram grupoid berikut.

::: {.figure #o012-rbt-l13-fig-004}
**Diagram 13.4 (span grupoid yang akan didorong keluar).** Data panahnya
adalah

$$
\Lambda\xrightarrow{\ F\ }H,
\qquad
\Lambda\xrightarrow{\ G\ }\Gamma.
$$

Secara visual, sumber menaruh $H$ di kanan dan $\Gamma$ di bawah:

$$
\begin{array}{ccc}
\Lambda&\xrightarrow{\ F\ }&H\\
{\scriptstyle G}\downarrow&&\\
\Gamma&&
\end{array}
$$

Huruf $H$ di sini adalah huruf Latin kapital, bukan huruf Yunani eta
$\eta$; itulah keterangan pinggir sumber pada diagram ini.
:::

Andaikan ketiga grupoid mempunyai himpunan objek berhingga yang sama,

$$
A=\{a_1,\ldots,a_N\},
$$

dan komponen objek $F$ serta $G$ adalah fungsi identitas. Kita hendak
membangun grupoid $\Gamma*_\Lambda H$ yang melengkapi span tersebut menjadi
persegi pushout. Himpunan objeknya kembali $A$, sedangkan fungtor kanonik

$$
\Gamma\longrightarrow\Gamma*_\Lambda H\longleftarrow H
$$

adalah identitas pada objek.

Setiap grupoid---bahkan setiap kategori---mempunyai graf dasar berarah yang
objek-objeknya menjadi simpul dan setiap morfismanya menjadi sisi. Loop dan
beberapa sisi dengan pasangan titik ujung sama diperbolehkan. Untuk skema kata
di sini, hapus sisi identitas dan pandang graf itu sebagai graf berarah dengan
involusi: dari setiap pasangan $\{\alpha,\alpha^{-1}\}$ cukup satu orientasi
yang digambar, sedangkan penelusuran balik mewakili inversnya. Jadi sisi yang
**digambar** tidak diklaim sama secara harfiah dengan seluruh morfisma
nonidentitas. Dari $\Gamma$ dan $H$, bentuk $\mathcal G$ memakai gabungan
saling lepas sisi terpilih kedua faktor pada simpul $A$. Alih-alih mengandalkan
warna sumber, kita beri setiap sisi tag $[\Gamma]$ atau $[H]$; huruf pada kata
tetap merupakan morfisma sebenarnya dalam faktor terkait.

::: {.figure #o012-rbt-l13-fig-005}
**Diagram 13.5 (daftar semantik seluruh sisi pada graf sumber).** Gambar
sumber mempunyai enam simpul $a_1,\ldots,a_6$ dan sisi-sisi berikut:

$$
\begin{array}{lll}
[\Gamma]&\gamma_1\colon a_1\to a_2,
&[H]\ \eta_2\colon a_2\to a_1,\\
[\Gamma]&\gamma_3\colon a_2\to a_4,
&[H]\ \eta_1\colon a_2\to a_4,\\
[\Gamma]&\gamma_2\colon a_4\to a_5,
&[H]\ \eta_3\colon a_5\to a_5,\\
[\Gamma]&\gamma_4\colon a_5\to a_2,
&[H]\ \eta_4\colon a_3\to a_6,\\
[\Gamma]&\gamma_5\colon a_3\to a_3,
&[\Gamma]\ \gamma_6\colon a_6\to a_6.
\end{array}
$$

Setiap sisi dapat ditempuh balik untuk memperoleh panah invers. Tidak ada
sisi lain pada ilustrasi, walaupun grupoid tentu juga mempunyai identitas dan
komposit. Catatan pinggir sumber bermaksud memberi contoh komposit yang
tidak digambar; kata tercetak $\gamma_3\gamma_1\gamma_2$ tidak bertipe.
Dengan konvensi kronologis, contoh yang dapat dikomposisikan adalah

$$
\gamma_1\gamma_3\gamma_2\colon a_1\longrightarrow a_5.
$$
:::

Mulailah dengan grupoid
$\Gamma*_{\Lambda_0}H$, di mana
$\Lambda_0=\operatorname{Disc}(A)$ adalah grupoid diskret pada himpunan
objek yang sama. Morfismanya dapat diwakili oleh kata berhingga

$$
\alpha_1\alpha_2\cdots\alpha_r
$$

yang dapat dikomposisikan dan bergantian antara panah nonidentitas
$\Gamma$ dan panah nonidentitas $H$. Kata kosong di objek $a$ mewakili
$1_a$. Jika dua panah bersebelahan berasal dari faktor yang sama, komposisikan
keduanya di faktor itu; jika hasilnya identitas, hapus hasil tersebut. Dengan
reduksi ini, contoh kata dari Diagram 13.5 adalah

$$
\gamma_3^{-1}\eta_1\gamma_2\eta_3^5\gamma_4
\colon a_4\longrightarrow a_2
$$

dan

$$
\eta_4\gamma_6^{-3}\eta_4^{-1}
\colon a_3\longrightarrow a_3.
$$

Jika $\Lambda$ memang sudah diskret, konstruksi ini selesai; sebagaimana
dicatat di pinggir sumber, keadaan itu adalah analog produk bebas grup. Untuk
$\Lambda$ umum, masih harus ditambahkan relasi. Bagi setiap
$\lambda\colon a\to b$ dalam $\Lambda$, identifikasikan panah sejajar

$$
G(\lambda)\in\Gamma(a,b)
\qquad\text{dan}\qquad
F(\lambda)\in H(a,b).
$$

Karena $F$ mendarat di $H$ dan $G$ mendarat di $\Gamma$, urutan ini
memperbaiki penandaan faktor yang tertukar dalam sumber. Bentuk hasil bagi
dengan **kongruensi grupoid terkecil** yang memuat semua identifikasi itu:
relasi ekuivalensi pada setiap hom-set harus tetap berlaku setelah
prakomposisi, pascakomposisi, dan pengambilan invers. Hasilnya adalah
$\Gamma*_\Lambda H$.

Sebagai contoh yang bertipe benar pada Diagram 13.5, andaikan
$\lambda\colon a_2\to a_4$ memenuhi

$$
G(\lambda)=\gamma_3,
\qquad
F(\lambda)=\eta_1.
$$

Relasi $\gamma_3=\eta_1$ lalu memberi

$$
\gamma_3^{-1}\eta_1\gamma_2\eta_3^5\gamma_4
=
\gamma_2\eta_3^5\gamma_4.
$$

Formula sumber memakai $F(\lambda)=\gamma_1$ dan
$G(\lambda)=\eta_1$, padahal kedua ruas bukan saja berada di faktor yang
salah, melainkan mempunyai pasangan sumber--sasaran yang berbeda; formula
turunannya juga tidak dapat dikomposisikan. Kesamaan di atas mempertahankan
maksud contoh sambil memperbaiki kedua cacat. Komposisi dalam
$\Gamma*_\Lambda H$ dilakukan dengan mengonkatenasikan kata, mereduksi
panah-panah bersebelahan dari faktor yang sama, lalu menerapkan kongruensi.

::: {.exercise #o012-rbt-l13-ex-001}
**Latihan Sumber 13.1.** Buktikan bahwa konstruksi di atas membuat
$\Gamma*_\Lambda H$ menjadi grupoid.
:::

Jika yang hendak dihitung hanya grup morfisma dari satu objek $a_i$ ke
dirinya sendiri---seperti ketika menghitung grup fundamental melalui
Seifert--van Kampen grupoid---cukup perhatikan kata yang berawal dan berakhir
di $a_i$.

## Contoh lingkaran {#o012-rbt-l13-s03}

::: {.example #o012-rbt-l13-exa-003}
**Contoh 13.3 (menghitung grup fundamental lingkaran).** Pandang
$S^1\subset\mathbb C$ dan ambil

$$
U=S^1\setminus\{-i\},
\qquad
V=S^1\setminus\{i\},
\qquad
A=\{+1,-1\}\subset U\cap V.
$$

Ruang $S^1$, $U$, dan $V$ terhubung lintasan. Irisan $U\cap V$ mempunyai
dua komponen lintasan, dan masing-masing memuat tepat satu titik $A$. Jadi
data ini memenuhi hipotesis Teorema Seifert--van Kampen relatif.
:::

::: {.figure #o012-rbt-l13-fig-006}
**Diagram 13.6 (pushout Seifert--van Kampen bagi lingkaran).** Persegi
pushoutnya adalah

$$
\begin{array}{ccc}
\Pi_1(U\cap V,\{\pm1\})&\longrightarrow&
\Pi_1(V,\{\pm1\})\\
\downarrow&&\downarrow\\
\Pi_1(U,\{\pm1\})&\longrightarrow&
\Pi_1(S^1,\{\pm1\}).
\end{array}
$$

Keempat panah diinduksi oleh inklusi; semua fungtor mempertahankan kedua
objek $+1$ dan $-1$. Subskrip $1$ pada $\Pi_1$ kanan bawah memulihkan salah
tik $\Pi_(S^1,\{\pm1\})$ dalam sumber; subskrip yang sama juga hilang pada
penyebutan $\Pi_1(U\cap V,\{\pm1\})$ sesudah diagram sumber.
:::

Baik $U$ maupun $V$ homeomorfik dengan interval terbuka, dengan kedua titik
$A$ tetap terbedakan. Karena itu grupoid fundamental terbatasnya masing-
masing isomorfik dengan grupoid kodiskret dua objek $\mathbf 2$. Setelah
panah identitas dihilangkan dari notasi, pilih satu-satunya kelas panah

$$
\gamma\colon +1\longrightarrow-1
\quad\text{di }\Pi_1(U,A),
$$

yang diwakili lintasan berlawanan arah jarum jam di $S^1$, dan satu-satunya
kelas panah

$$
\eta\colon -1\longrightarrow+1
\quad\text{di }\Pi_1(V,A),
$$

yang juga diwakili lintasan berlawanan arah jarum jam. Jadi

$$
\Pi_1(U,A)
\cong
\bigl(+1\mathrel{\mathop{\rightleftarrows}^{\gamma}_{\gamma^{-1}}}-1\bigr),
\qquad
\Pi_1(V,A)
\cong
\bigl(-1\mathrel{\mathop{\rightleftarrows}^{\eta}_{\eta^{-1}}}+1\bigr),
$$

dengan tipe panah ditentukan oleh dua tampilan sebelumnya, bukan oleh posisi
label di atas atau di bawah simbol panah.

Selanjutnya,

$$
\Pi_1(U\cap V,A)
=
\operatorname{Disc}(\{+1,-1\}),
$$

karena setiap komponen irisan kontraktibel dan memuat hanya satu objek
pilihan. Jadi $\Lambda$ diskret dan tidak diperlukan hasil bagi tambahan.

::: {.figure #o012-rbt-l13-fig-007}
**Diagram 13.7 (pushout yang telah disederhanakan).** Tuliskan
$D=\operatorname{Disc}(\{+1,-1\})$. Diagram lengkapnya adalah

$$
\begin{array}{ccc}
D&\longrightarrow&
\bigl(-1\mathrel{\mathop{\rightleftarrows}^{\eta}_{\eta^{-1}}}+1\bigr)\\
\downarrow&&\downarrow\\
\bigl(+1\mathrel{\mathop{\rightleftarrows}^{\gamma}_{\gamma^{-1}}}-1\bigr)
&\longrightarrow&\Pi_1(S^1,\{\pm1\}).
\end{array}
$$

Panah dari $D$ adalah identitas pada objek dan hanya membawa panah
identitas. Panah bawah serta kanan memasukkan masing-masing kelas $\gamma$
dan $\eta$ ke grupoid fundamental lingkaran.
:::

::: {.figure #o012-rbt-l13-fig-008}
**Diagram 13.8 (graf pembangkit lingkaran tanpa sandi warna).** Graf sumber
yang diperlukan mempunyai tepat dua simpul dan dua sisi berarah:

$$
[\Gamma=\Pi_1(U,A)]\quad
+1\xrightarrow{\ \gamma\ }-1,
\qquad
[H=\Pi_1(V,A)]\quad
-1\xrightarrow{\ \eta\ }+1.
$$

Panah balik mewakili $\gamma^{-1}$ dan $\eta^{-1}$. Gambar sumber menukar
label serta faktor kedua panah; daftar ini mengikuti definisi tekstual
$\gamma$ dan $\eta$ serta membuat semua kata berikut bertipe benar.
:::

Loop tereduksi dari $+1$ ke dirinya sendiri adalah kata kosong, suatu pangkat
positif

$$
(\gamma\eta)^n,
$$

atau pangkat negatif yang ditulis

$$
(\eta^{-1}\gamma^{-1})^n
=(\gamma\eta)^{-n},
\qquad n\geq1.
$$

Memang, dari $+1$ satu-satunya huruf pertama yang tereduksi adalah
$\gamma$ atau $\eta^{-1}$; sesudah itu huruf-huruf dipaksa bergantian jika
tidak terjadi pembatalan. Maka pemetaan

$$
\mathbb Z\longrightarrow\pi_1(S^1,+1),
\qquad
n\longmapsto(\gamma\eta)^n
$$

adalah isomorfisma. Jadi

$$
\pi_1(S^1,+1)\cong\mathbb Z.
$$

Urutan $\eta\gamma$ yang tercetak dalam sumber tidak dapat dimulai di $+1$
dengan konvensi produk kronologis unit-unit sebelumnya; koreksi di atas
memulihkan tipe sumber dan sasaran.

::: {.exercise #o012-rbt-l13-ex-002}
**Latihan Sumber 13.2.** Buktikan bahwa konstruksi
$\Gamma*_\Lambda H$ di atas benar-benar merupakan pushout di
$\mathbf{Gpd}$.
:::

## Grup fundamental baji {#o012-rbt-l13-s04}

Kita pertimbangkan satu variasi lagi dari Seifert--van Kampen secara ringkas,
karena rinciannya serupa dengan versi-versi sebelumnya. Konstruksi yang
dipakai sumber adalah **baji** $X\vee Y$, bukan join. Produk bebas grup
fundamental tidak boleh langsung dinyatakan tanpa sampul dan hipotesis yang
memungkinkan penerapan teorema.

Misalkan $(X,x)$ dan $(Y,y)$ ruang bertitik yang **terhubung lintasan**.
Andaikan terdapat lingkungan

$$
x\in U\subseteq X,
\qquad
y\in V\subseteq Y
$$

yang masing-masing dapat dikontraksikan ke $x$ dan $y$ melalui kontraksi
yang menetapkan titik basis. Maka

$$
\{X\vee V,\ U\vee Y\}
$$

adalah sampul $X\vee Y$ oleh lingkungan. Irisannya adalah $U\vee V$.
Catatan pinggir sumber menunjukkan bahwa kontraksi bertitik kedua faktor
merakit menjadi kontraksi $U\vee V$ ke

$$
*= [x]=[y].
$$

Ada retraksi bertitik

$$
X\vee V\longrightarrow X,
\qquad
U\vee Y\longrightarrow Y,
$$

dan kontraksi yang diberikan menunjukkan bahwa keduanya merupakan
ekuivalensi homotopi. Jadi

$$
\pi_1(X\vee V,*)\cong\pi_1(X,x),
\qquad
\pi_1(U\vee Y,*)\cong\pi_1(Y,y),
$$

sedangkan $\pi_1(U\vee V,*)$ trivial. Hipotesis keterhubungan lintasan pada
$X,Y$ memastikan keempat ruang dalam persegi juga terhubung lintasan, seperti
yang disyaratkan versi grup Seifert--van Kampen.

::: {.figure #o012-rbt-l13-fig-009}
**Diagram 13.9 (sampul baji).** Semua panah adalah inklusi ruang bertitik:

$$
\begin{array}{ccc}
(U\vee V,*)&\longrightarrow&(U\vee Y,*)\\
\downarrow&&\downarrow\\
(X\vee V,*)&\longrightarrow&(X\vee Y,*).
\end{array}
$$

Panah atas mempertahankan faktor $U$ dan memasukkan $V$ ke $Y$; panah kiri
memasukkan $U$ ke $X$ dan mempertahankan $V$. Kedua komposit mengirim setiap
titik irisan ke kelas yang sama di baji penuh.
:::

Seifert--van Kampen mengubah persegi itu menjadi pushout grup berikut.

::: {.figure #o012-rbt-l13-fig-010}
**Diagram 13.10 (pushout grup fundamental baji).** Setelah memakai
ekuivalensi homotopi di atas, persegi menjadi

$$
\begin{array}{ccc}
1&\longrightarrow&\pi_1(Y,y)\\
\downarrow&&\downarrow\\
\pi_1(X,x)&\longrightarrow&\pi_1(X\vee Y,*).
\end{array}
$$

Kedua panah keluar dari $1$ adalah homomorfisma unik. Karena pushout diagram
$\pi_1(X,x)\leftarrow1\to\pi_1(Y,y)$ adalah produk bebas, panah kanan bawah
mengidentifikasi sudut tersebut secara kanonik dengan produk bebas.
:::

Dengan demikian

$$
\pi_1(X\vee Y,*)
\cong
\pi_1(X,x)*\pi_1(Y,y).
$$

Ini memperumum perhitungan

$$
\pi_1(S^1\vee S^1,*)
\cong F_2
\cong\mathbb Z*\mathbb Z.
$$

Tanpa keterhubungan lintasan $X$ dan $Y$, sampul yang sama tetap dapat
dianalisis dengan versi grupoid, tetapi persegi grup satu-objek di atas tidak
langsung mengikuti dari Akibat Seifert--van Kampen Unit 12.

## Kompleks presentasi {#o012-rbt-l13-s05}

::: {.fact #o012-rbt-l13-fact-001}
**Fakta 13.1 (setiap grup adalah grup fundamental suatu kompleks
presentasi).** Diberikan presentasi berhingga

$$
G=
\langle g_1,\ldots,g_m\mid
R_1=e,\ldots,R_n=e\rangle,
$$

terdapat ruang $X$ yang diperoleh sebagai pushout pada Diagram 13.11 dan
memenuhi $\pi_1(X,*)\cong G$.
:::

::: {.figure #o012-rbt-l13-fig-011}
**Diagram 13.11 (memasang sel-$2$ bagi presentasi berhingga).** Tuliskan

$$
W_m:=\bigvee_{j=1}^{m}S^1
=
\underbrace{S^1\vee\cdots\vee S^1}_{m\text{ buah}},
$$

sebagaimana dijabarkan oleh catatan pinggir sumber. Pilih peta bertitik

$$
f_i\colon(S^1,1)\longrightarrow(W_m,*)
$$

yang kelas loopnya, di bawah isomorfisma
$\pi_1(W_m,*)\cong F_m$, adalah kata $R_i$. Gabungkan peta-peta itu menjadi
$\bigsqcup_i f_i$. Persegi pushoutnya ialah

$$
\begin{array}{ccc}
\displaystyle\bigsqcup_{i=1}^{n}S^1
&\longrightarrow&
\displaystyle\bigsqcup_{i=1}^{n}D^2\\
{\scriptstyle\bigsqcup_i f_i}\downarrow&&\downarrow\\
\displaystyle\bigvee_{j=1}^{m}S^1&\longrightarrow&X.
\end{array}
$$

Panah atas adalah gabungan inklusi batas $S^1=\partial D^2\hookrightarrow
D^2$. Pushout menempelkan satu sel-$2$ sepanjang setiap $f_i$.
:::

Persamaan sumber $f_i(1)=R_i$ tidak bertipe: ruas kiri adalah titik ruang,
sedangkan ruas kanan adalah unsur grup. Pernyataan bertipe benar adalah

$$
[f_i]=R_i\in\pi_1(W_m,*)\cong F_m.
$$

Untuk membenarkan perhitungan dengan Seifert--van Kampen, tebalkan
$W_m$ dan bagian dalam sel-sel yang terpasang hingga menjadi sampul oleh
lingkungan berkerah. Setiap cakram kontraktibel; loop pada komponen kerah
batas dipetakan ke $[f_i]$. Teorema Seifert--van Kampen, atau penerapannya
berturut-turut untuk tiap sel, menyatakan bahwa memasang sel-$2$ membagi
$\pi_1(W_m,*)$ dengan penutupan normal kelas-kelas $[f_i]$. Karena itu

$$
\pi_1(X,*)
\cong
F_m/\langle\!\langle R_1,\ldots,R_n\rangle\!\rangle
\cong G.
$$

Ruang $X$ adalah kompleks CW berdimensi $2$: ruang itu diperoleh dengan
merekatkan cakram-cakram berdimensi dua pada graf satu-dimensi. Kadang-kadang
$X$ merupakan manifold, tetapi pada umumnya tidak.

Fakta tersebut berlaku lebih luas untuk **setiap** grup $G$ dan setiap
presentasi

$$
G=\langle g_\alpha\ (\alpha\in I)
\mid R_\beta=e\ (\beta\in J)\rangle,
$$

termasuk himpunan pembangkit atau relasi tak berhingga.

::: {.figure #o012-rbt-l13-fig-012}
**Diagram 13.12 (kompleks presentasi umum).** Beri baji
$W_I=\bigvee_{\alpha\in I}S^1$ topologi CW atau topologi lemah
(*weak topology*), dan untuk
setiap $\beta\in J$ pilih peta bertitik

$$
f_\beta\colon S^1\longrightarrow W_I,
\qquad
[f_\beta]=R_\beta.
$$

Kemudian bentuk pushout

$$
\begin{array}{ccc}
\displaystyle\bigsqcup_{\beta\in J}S^1
&\longrightarrow&
\displaystyle\bigsqcup_{\beta\in J}D^2\\
{\scriptstyle\bigsqcup_\beta f_\beta}\downarrow&&\downarrow\\
\displaystyle\bigvee_{\alpha\in I}S^1&\longrightarrow&X.
\end{array}
$$

Panah atas kembali merupakan gabungan inklusi batas; panah kiri adalah
gabungan peta pelekatan. Sudut kanan bawah diberi topologi pushout CW.
:::

Dengan topologi ini,

$$
\pi_1\!\left(\bigvee_{\alpha\in I}S^1,*\right)
\cong F_I,
$$

grup bebas pada himpunan $I$, dan argumen sel-$2$ yang sama memberi
$\pi_1(X,*)\cong G$. Setiap kata relator berhingga, sehingga setiap
$f_\beta$ hanya perlu melintasi berhingga banyak lingkaran.

Sumber menyebut konstruksi ini “baji tak berhingga”, walaupun salah ketik
“join” muncul pada naskah. Topologinya perlu diperhatikan. Catatan pinggir
sumber membandingkan baji terhitung

$$
\bigvee_{n\in\mathbb N}S^1
$$

dengan anting Hawaii. Baji CW tidak kompak dan semilokal terhubung
sederhana, sedangkan anting Hawaii kompak dan tidak semilokal terhubung
sederhana. Jadi keduanya tidak homeomorfik.

::: {.example #o012-rbt-l13-exa-004}
**Contoh 13.4 (permukaan Riemann kompak).** Permukaan Riemann kompak
berorientasi $\Sigma_g$ dengan genus $g\geq1$ merupakan contoh ruang yang
diperoleh melalui Fakta 13.1. Bahkan hanya satu salinan $D^2$ yang
diperlukan.
:::

::: {.figure #o012-rbt-l13-fig-013}
**Diagram 13.13 (satu sel-$2$ untuk permukaan genus $g$).** Persegi
pushoutnya adalah

$$
\begin{array}{ccc}
S^1&\longrightarrow&D^2\\
{\scriptstyle f}\downarrow&&\downarrow\\
\displaystyle\bigvee_{i=1}^{2g}S^1&\longrightarrow&\Sigma_g.
\end{array}
$$

Panah atas memasukkan batas cakram. Beri lingkaran-lingkaran baji berturut-
turut pembangkit $a_1,b_1,\ldots,a_g,b_g$. Peta kiri adalah peta bertitik
yang memenuhi

$$
[f]
=
\prod_{i=1}^{g}[a_i,b_i]
\in
\pi_1\!\left(\bigvee_{i=1}^{2g}S^1,*\right).
$$
:::

Konstruksi yang setara dimulai dari poligon bersisi $4g$, lalu
mengidentifikasi sisi-sisinya secara berpasangan. Pola urutan batasnya adalah

$$
a_1b_1a_1^{-1}b_1^{-1}\cdots
a_gb_ga_g^{-1}b_g^{-1}
=
\prod_{i=1}^{g}[a_i,b_i].
$$

Setiap pasangan sisi dengan label sama diidentifikasi dengan orientasi yang
ditunjukkan oleh eksponen; semua titik sudut menjadi titik basis. Setelah
identifikasi, kerangka sisi menjadi baji $2g$ lingkaran dan bagian dalam
poligon menjadi satu sel-$2$. Catatan pinggir sumber meninggalkan placeholder
“sisipkan gambar oktagon untuk $g=2$”. Deskripsi semantik lengkap untuk
oktagon itu adalah urutan delapan sisi berarah

$$
a_1,\ b_1,\ a_1^{-1},\ b_1^{-1},\
a_2,\ b_2,\ a_2^{-1},\ b_2^{-1},
$$

dengan setiap dua sisi berlabel sama dipasangkan. Inilah relator satu pada
[Contoh 13.1](#o012-rbt-l13-exa-001) dan menjelaskan presentasi

$$
\pi_1(\Sigma_g,*)
\cong
\left\langle a_1,b_1,\ldots,a_g,b_g
\ \middle|\
\prod_{i=1}^{g}[a_i,b_i]=e
\right\rangle.
$$

## Mengklasifikasikan ruang pelapis {#o012-rbt-l13-s06}

::: {.boundary #o012-rbt-l13-boundary}
**Batas sumber.** Judul bagian tepat di atas adalah isi Notes.tex baris 3045;
baris 3046 kosong. Baris 3047 memulai Kuliah 14 di tengah sumber. Unit ini
tidak menerjemahkan, merangkum, atau memakai materi pada baris 3047 maupun
sesudahnya. Karena itu judul tersebut sengaja menjadi penunjuk ke depan tanpa
isi sumber di bawahnya pada unit ini.
:::

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l13-mastery}

Bagian ini merupakan materi asli edisi, bukan bagian dari Notes.tex. Enam
pemeriksaan berikut dibatasi pada konsep dan data Unit 13. Pemeriksaan 13.2
dan 13.3 menyelesaikan dua latihan sumber; pemeriksaan lain menutup langkah
yang dipakai sumber tetapi belum dijadikan latihan. Seluruh solusi disusun
mandiri dan tersedia di bawah CC BY 4.0.

::: {.exercise #o012-rbt-l13-mcheck-001 data-origin="edition-original"}
**Pemeriksaan penguasaan 13.1 (presentasi amalgamasi).** Misalkan

$$
G=\langle g_i\ (i\in I)\mid R_\alpha\ (\alpha\in A)\rangle,
\qquad
H=\langle h_j\ (j\in J)\mid Q_\beta\ (\beta\in B)\rangle,
$$

dan $L$ dibangkitkan oleh $S$. Buktikan bahwa $G*_L H$ mempunyai presentasi
yang menggabungkan pembangkit dan relasi kedua faktor serta menambahkan
$\phi(s)=\psi(s)$ untuk $s\in S$. Terapkan hasilnya pada
$F_m*_{\mathbb Z}1$ ketika $1\in\mathbb Z$ dikirim ke $R\in F_m$.
:::

## Solusi Pemeriksaan 13.1 {#o012-rbt-l13-sol-001}

Produk bebas mempunyai presentasi

$$
G*H
\cong
\langle g_i,h_j\mid R_\alpha,Q_\beta\rangle.
$$

Membentuk $G*_L H$ berarti membagi grup ini dengan penutupan normal semua

$$
\phi(x)\psi(x)^{-1},
\qquad x\in L.
$$

Jika relasi $\phi(s)=\psi(s)$ berlaku untuk setiap $s\in S$, relasi itu juga
berlaku untuk invers dan produk pembangkit: homomorfisma dari $L$ yang
diberikan oleh dua komposit ke hasil bagi bersepakat pada $S$, maka
bersepakat pada seluruh $L$. Jadi cukup menambahkan relasi bagi $s\in S$,
dan diperoleh

$$
G*_L H
\cong
\left\langle g_i,h_j\ \middle|\
R_\alpha,Q_\beta,
\phi(s)\psi(s)^{-1}=e\ (s\in S)
\right\rangle.
$$

Presentasi ini juga mempunyai sifat universal yang diinginkan. Homomorfisma
ke grup $K$ sama dengan pasangan homomorfisma $u\colon G\to K$ dan
$v\colon H\to K$ yang menghormati relasi tambahan; syarat terakhir tepat
$u\circ\phi=v\circ\psi$ pada $S$, dan karenanya pada $L$.

Untuk $L=\mathbb Z$, $H=1$, dan $\phi(1)=R$, relasi tambahan adalah
$R=e$. Karena faktor trivial tidak menambah pembangkit,

$$
F_m*_{\mathbb Z}1
\cong
F_m/\langle\!\langle R\rangle\!\rangle
\cong
\langle g_1,\ldots,g_m\mid R=e\rangle.
$$

::: {.exercise #o012-rbt-l13-mcheck-002 data-origin="edition-original"}
**Pemeriksaan penguasaan 13.2 (solusi Latihan Sumber 13.1).** Buktikan
bahwa kata panah tereduksi, setelah dibagi dengan kongruensi yang dihasilkan
oleh $G(\lambda)=F(\lambda)$, membentuk grupoid.
:::

## Solusi Pemeriksaan 13.2 {#o012-rbt-l13-sol-002}

Mula-mula bekerja sebelum relasi $\Lambda$ dikenakan. Objeknya adalah
$A$. Suatu panah $a\to b$ diwakili oleh kata kosong jika $a=b$, atau kata

$$
w=\alpha_1\cdots\alpha_r
$$

yang panah-panahnya dapat dikomposisikan dari $a$ ke $b$. Dua langkah
reduksi elementer diperbolehkan:

1. hapus suatu identitas;
2. ganti dua panah bersebelahan dari faktor yang sama oleh kompositnya di
   faktor tersebut.

Kata tereduksi yang tidak kosong karena itu bergantian antara faktor
$\Gamma$ dan $H$. Untuk $[u]\colon a\to b$ dan
$[v]\colon b\to c$, definisikan produk kronologis $[u][v]$ dengan
mengonkatenasikan $u$ dan $v$, lalu mereduksi sambungan jika kedua huruf di
sana berasal dari faktor yang sama. Definisi tidak bergantung pada wakil:
setiap reduksi di dalam $u$ atau $v$ tetap menjadi reduksi sah setelah kata
lain ditempelkan.

Asosiativitas mengikuti asosiativitas konkatenasi dan komposisi di setiap
faktor. Lebih eksplisit, $(uv)w$ dan $u(vw)$ berasal dari daftar huruf yang
sama; semua pengelompokan berturutan di satu faktor memberi panah yang sama
karena komposisi faktor asosiatif. Kata kosong di $a$ menjadi identitas
$1_a$.

Definisikan

$$
(\alpha_1\cdots\alpha_r)^{-1}
:=
\alpha_r^{-1}\cdots\alpha_1^{-1}.
$$

Kata ini berjalan dari $b$ ke $a$. Dalam produk
$ww^{-1}$, pasangan tengah $\alpha_r\alpha_r^{-1}$ tereduksi menjadi
identitas; pembatalan berulang memberi kata kosong di $a$. Serupa dengan
itu, $w^{-1}w$ tereduksi menjadi kata kosong di $b$. Jadi
$\Gamma*_{\Lambda_0}H$ adalah grupoid.

Sekarang bagi setiap hom-set dengan kongruensi grupoid terkecil yang memuat
$G(\lambda)\sim F(\lambda)$. Karena kongruensi menurut definisi stabil
terhadap komposisi di kedua sisi dan invers, komposisi serta operasi invers
turun secara terdefinisi baik ke kelas ekuivalensi. Identitas, asosiativitas,
dan persamaan invers tetap benar setelah mengambil kelas. Maka
$\Gamma*_\Lambda H$ juga grupoid.

::: {.exercise #o012-rbt-l13-mcheck-003 data-origin="edition-original"}
**Pemeriksaan penguasaan 13.3 (solusi Latihan Sumber 13.2).** Untuk grupoid
$\mathcal K$, misalkan diberikan fungtor

$$
P\colon\Gamma\to\mathcal K,
\qquad
Q\colon H\to\mathcal K
$$

dengan $P\circ G=Q\circ F$. Bangun satu-satunya fungtor
$T\colon\Gamma*_\Lambda H\to\mathcal K$ yang memperluas $P$ dan $Q$.
:::

## Solusi Pemeriksaan 13.3 {#o012-rbt-l13-sol-003}

Karena $F$ dan $G$ adalah identitas pada objek, kesamaan
$P\circ G=Q\circ F$ pada objek memberi

$$
P(a)=Q(a)
$$

untuk setiap $a\in A$. Definisikan $T(a)$ sebagai objek bersama ini. Untuk
kata yang dapat dikomposisikan
$w=\alpha_1\cdots\alpha_r$, tetapkan

$$
T(w)=T(\alpha_1)\cdots T(\alpha_r),
$$

dengan $T(\alpha_i)=P(\alpha_i)$ bila huruf itu berasal dari $\Gamma$ dan
$T(\alpha_i)=Q(\alpha_i)$ bila berasal dari $H$. Produk pada ruas kanan
dibaca kronologis. Kata kosong dikirim ke identitas.

Fungtorialitas $P$ dan $Q$ memastikan bahwa menghapus identitas atau
mengomposisikan dua huruf dari faktor yang sama tidak mengubah nilai. Bagi
$\lambda\in\Lambda$, kompatibilitas memberi

$$
T(G(\lambda))
=P(G(\lambda))
=Q(F(\lambda))
=T(F(\lambda)).
$$

Karena kesamaan di $\mathcal K$ stabil terhadap komposisi dan invers,
$T$ tetap konstan pada seluruh kongruensi yang dihasilkan relasi tersebut.
Jadi rumus turun ke fungtor

$$
T\colon\Gamma*_\Lambda H\longrightarrow\mathcal K.
$$

Konstruksinya jelas membatasi menjadi $P$ dan $Q$. Untuk keunikan, setiap
fungtor perluasan harus mempunyai nilai $P(\alpha)$ atau $Q(\alpha)$ pada
setiap kata satu huruf. Fungtorialitas kemudian memaksanya mempunyai nilai
produk di atas pada setiap kata, dan karenanya pada setiap kelas kongruensi.
Jadi $T$ unik. Inilah tepat sifat universal pushout di $\mathbf{Gpd}$.

::: {.exercise #o012-rbt-l13-mcheck-004 data-origin="edition-original"}
**Pemeriksaan penguasaan 13.4 (bentuk normal pada lingkaran).** Tentukan
semua empat hom-set dari grupoid pada Diagram 13.8. Gunakan jawaban itu untuk
membuktikan lagi bahwa grup automorfisma di $+1$ isomorfik dengan
$\mathbb Z$.
:::

## Solusi Pemeriksaan 13.4 {#o012-rbt-l13-sol-004}

Setiap kata tereduksi harus bergantian dan arah panah menentukan huruf
berikutnya. Dengan $n\in\mathbb Z$, semua hom-set dapat ditulis

$$
\begin{aligned}
\operatorname{Hom}(+1,+1)
&=\{(\gamma\eta)^n:n\in\mathbb Z\},\\
\operatorname{Hom}(-1,-1)
&=\{(\eta\gamma)^n:n\in\mathbb Z\},\\
\operatorname{Hom}(+1,-1)
&=\{(\gamma\eta)^n\gamma:n\in\mathbb Z\},\\
\operatorname{Hom}(-1,+1)
&=\{(\eta\gamma)^n\eta:n\in\mathbb Z\}.
\end{aligned}
$$

Rumus itu juga mencakup kata yang tampak diawali invers. Sebagai contoh,

$$
(\gamma\eta)^{-1}\gamma
=
\eta^{-1}\gamma^{-1}\gamma
=
\eta^{-1}.
$$

Keunikan bentuk tereduksi menunjukkan bahwa pangkat berbeda dari
$\gamma\eta$ memberi loop berbeda. Komposisi kronologis menjumlahkan
pangkat:

$$
(\gamma\eta)^m(\gamma\eta)^n
=(\gamma\eta)^{m+n}.
$$

Karena itu $n\mapsto(\gamma\eta)^n$ adalah homomorfisma bijektif dari
$\mathbb Z$ ke $\operatorname{Aut}(+1)=\pi_1(S^1,+1)$.

::: {.exercise #o012-rbt-l13-mcheck-005 data-origin="edition-original"}
**Pemeriksaan penguasaan 13.5 (hipotesis baji).**

1. Tunjukkan bahwa $X\vee V$ meretrak deformasi ke $X$, $U\vee Y$
   meretrak deformasi ke $Y$, dan $U\vee V$ kontraktibel ke titik basis.
2. Jelaskan tepat di mana keterhubungan lintasan $X$ dan $Y$ dipakai.
3. Turunkan isomorfisma produk bebas dari sifat universal pushout.
:::

## Solusi Pemeriksaan 13.5 {#o012-rbt-l13-sol-005}

Biarkan $h_V\colon V\times I\to V$ merupakan kontraksi ke $y$ yang
menetapkan $y$. Pada $X\vee V$, definisikan homotopi sebagai identitas pada
faktor $X$ dan $h_V$ pada faktor $V$. Kedua rumus bersepakat di titik baji
sepanjang waktu karena $h_V(y,t)=y$, sehingga turun melalui hasil bagi baji.
Pada waktu akhir, citranya $X$ dan homotopi menetapkan $X$; jadi ini retraksi
deformasi. Argumen dengan kontraksi $U$ memberi retraksi deformasi
$U\vee Y\to Y$. Menggabungkan kedua kontraksi bertitik pada $U\vee V$
memberi kontraksi ke $*$.

Keterhubungan lintasan $X,Y$ bersama keterhubungan $U,V$ memastikan
$X\vee V$, $U\vee Y$, dan $X\vee Y$ terhubung lintasan; $U\vee V$ bahkan
kontraktibel. Karena itu Akibat Seifert--van Kampen untuk **grup** dari Unit
12 berlaku pada titik basis tunggal. Tanpa syarat itu, Teorema grupoid masih
tersedia, tetapi kita belum memperoleh persegi satu-objek pada Diagram 13.10.

Setelah identifikasi melalui retraksi deformasi, diagram grup adalah

$$
\pi_1(X,x)\longleftarrow1\longrightarrow\pi_1(Y,y).
$$

Untuk grup $K$, sebuah kocone dari diagram ini tepat pasangan homomorfisma

$$
\pi_1(X,x)\to K\longleftarrow\pi_1(Y,y),
$$

karena kompatibilitas pada $1$ otomatis. Sifat universal produk bebas
menunjukkan bahwa pushoutnya adalah
$\pi_1(X,x)*\pi_1(Y,y)$. Keunikan pushout memberi isomorfisma kanonik dengan
$\pi_1(X\vee Y,*)$.

::: {.exercise #o012-rbt-l13-mcheck-006 data-origin="edition-original"}
**Pemeriksaan penguasaan 13.6 (sel-$2$ dan kata permukaan).**

1. Jelaskan mengapa memasang satu sel-$2$ sepanjang loop yang mewakili
   $R\in\pi_1(W,*)$ membagi $\pi_1(W,*)$ dengan
   $\langle\!\langle R\rangle\!\rangle$, bukan hanya subgrup siklik
   $\langle R\rangle$.
2. Untuk $g=2$, baca kata pelekatan dari oktagon dan tuliskan presentasi
   grup fundamentalnya.
3. Jelaskan mengapa peta pelekatan harus dinyatakan oleh $[f]=R$, bukan
   $f(1)=R$.
:::

## Solusi Pemeriksaan 13.6 {#o012-rbt-l13-sol-006}

Gunakan sampul berkerah $\mathcal U\cup\mathcal V$: bagian $\mathcal U$
meretrak deformasi ke $W$, bagian $\mathcal V$ meretrak deformasi ke cakram
$D^2$ dan karenanya mempunyai grup fundamental trivial, sedangkan
$\mathcal U\cap\mathcal V$ meretrak deformasi ke lingkaran batas. Kedua
homomorfisma dari grup fundamental irisan mengirim generator batas masing-
masing ke $R$ di $\pi_1(W,*)$ dan ke identitas di $\pi_1(D^2,*)$. Pushout
grup karena itu menambahkan relasi $R=e$.

Kernel suatu homomorfisma grup selalu subgrup normal. Setelah $R$ menjadi
identitas, setiap konjugat $wRw^{-1}$ juga harus menjadi identitas; demikian
pula semua produk konjugat dan inversnya. Jadi sedikitnya seluruh penutupan
normal $\langle\!\langle R\rangle\!\rangle$ dibunuh. Sebaliknya, hasil bagi
oleh penutupan normal itu mempunyai sifat universal yang tepat bagi semua
homomorfisma yang membunuh $R$. Maka grup hasilnya persis

$$
\pi_1(W,*)/\langle\!\langle R\rangle\!\rangle.
$$

Untuk $g=2$, urutan sisi oktagon adalah

$$
a_1b_1a_1^{-1}b_1^{-1}a_2b_2a_2^{-1}b_2^{-1}
=[a_1,b_1][a_2,b_2].
$$

Dengan memasang bagian dalam oktagon sebagai satu sel-$2$, diperoleh

$$
\pi_1(\Sigma_2,*)
\cong
\langle a_1,b_1,a_2,b_2
\mid [a_1,b_1][a_2,b_2]=e\rangle.
$$

Terakhir, $f(1)$ adalah titik $W$; karena $f$ bertitik, nilainya justru titik
basis $*$. Relator $R$ adalah unsur grup fundamental, yakni kelas homotopi
berujung tetap dari keseluruhan loop. Jadi persamaan yang bertipe benar
adalah

$$
[f]=R\in\pi_1(W,*).
$$
