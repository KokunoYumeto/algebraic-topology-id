---
title: "Topologi Aljabar"
subtitle: "Unit 23: Evaluasi, Gabungan Saling Lepas, dan Perekatan Korantai"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "23 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l23-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 4939--5112 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L4939-L5112)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang aktif itu terdiri atas 174 baris fisik. Setelah dinormalisasi dengan
LF dan mempertahankan baris kosong penutupnya, ukurannya 9.776 byte dan
SHA-256-nya adalah
`c7256a45621ad7a435277867298e4aeb8eb584dfce066cdae3b48c4ee0e0e3f4`.
Kuliah 24 dimulai pada Notes.tex baris 5113 di dalam contoh yang dibuka pada
baris 5076; karena itu unit ini menerjemahkan contoh tersebut hanya sampai
baris 5111 dan menandainya secara eksplisit sebagai berlanjut. Materi sumber
dan adaptasi Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Perubahan edisi mencakup penerjemahan, pemformatan ulang, pemberian pengenal
stabil, dan pemindahan enam catatan pinggir ke urutan bacaan utama. Dua
diagram Xy-pic ditulis ulang sebagai diagram semantik terpusat. Contoh batas
tetrahedron juga dilengkapi tabel simpleks dan deskripsi ketetanggaan yang
dapat dibaca tanpa mengandalkan letak visual, warna, atau ketebalan garis.

Rentang sumber memuat tepat satu catatan, satu lema, satu akibat, dua contoh
(contoh kedua berlanjut ke Kuliah 24), dua lingkungan `enumerate` dengan enam
butir seluruhnya, enam catatan pinggir, dua diagram Xy-pic, satu rujukan
silang, sembilan tampilan `\[...\]`, dan satu `align*`. Tidak ada definisi,
bukti formal, latihan sumber, konstruksi, label, sitasi, gambar eksternal,
`input`, atau `include` pada rentang ini.

Edisi memperbaiki kekeliruan tipe dan indeks pada pemetaan evaluasi,
menyatakan augmentasi hanya pada komponen derajat nol, dan menulis
fungtorialitas berarah kontravarian. Salah ketik $R^Q\oplus R^Q$ diperbaiki
menjadi $R^P\oplus R^Q$, sedangkan kompleks ditulis dengan gradasi
kohomologis. Untuk gabungan saling lepas tak hingga, produk dan hipotesis
teori himpunannya dinyatakan secara tepat. Uraian batas tetrahedron dibatasi
pada subhimpunan wajar takkosong dan derajat $0\leq n\leq2$. Klaim eksaknya
barisan perekatan dibuktikan lengkap, termasuk perekatan fungsi, surjektivitas,
dan kompatibilitas diferensial. Pada contoh hasil bagi, simbol $A$ digunakan
secara konsisten, kasus $A\ne\varnothing$ dibedakan dari $A=\varnothing$,
dan $q^*$ dibatasi secara tepat dari fungsi tereduksi menuju kernel restriksi.

Enam pemeriksaan penguasaan, enam petunjuk, dan enam solusi lengkap merupakan
materi asli edisi dan tersedia di bawah CC BY 4.0. Edisi ini bersifat
independen; edisi ini tidak disponsori, didukung, disahkan, ataupun diberi
status resmi oleh David Michael Roberts atau institusinya. Produksi edisi ini
dibantu oleh **OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini menambah
transparansi proses dan tidak mengurangi kredit penulis sumber ataupun kredit
kontributor manusia.

# Kuliah 23 {#o012-rbt-l23}

## Pemetaan nama dan evaluasi korantai {#o012-rbt-l23-s01}

Kita kembali ke fungtorialitas terhadap pemetaan himpunan-$\Delta$. Untuk
$x\in X_n$, dengan $X_\bullet$ sebuah himpunan-$\Delta$,
[Contoh 22.8](#o012-rbt-l22-exa-008) memberi
pemetaan nama

$$
\ulcorner x\urcorner\colon\Delta[n]\longrightarrow X_\bullet.
$$

Karena kompleks korantai simpleksial bersifat kontravarian, pemetaan itu
menginduksi bagian diagram kompleks di sekitar derajat $n$ berikut.

::: {.figure #o012-rbt-l23-fig-001 data-source-format="xypic"}
**Diagram 23.1 (evaluasi yang berasal dari pemetaan nama).** Kuadrat
komutatifnya adalah

$$
\begin{array}{ccccc}
\cdots&\longrightarrow&R^{X_n}&\overset{\delta_X^n}{\longrightarrow}&R^{X_{n+1}}\longrightarrow\cdots\\
&&\downarrow&&\downarrow\\
\cdots&\longrightarrow&R^{\Delta[n]_n}&\overset{\delta_{\Delta[n]}^n}{\longrightarrow}&R^{\Delta[n]_{n+1}}\longrightarrow\cdots.
\end{array}
$$

Panah vertikal kiri adalah
$\ulcorner x\urcorner_n^*\colon R^{X_n}\to R^{\Delta[n]_n}$, sedangkan
panah vertikal kanan adalah

$$
\ulcorner x\urcorner_{n+1}^*\colon
R^{X_{n+1}}\longrightarrow R^{\Delta[n]_{n+1}}.
$$

Kedua lintasan dari $R^{X_n}$ ke
$R^{\Delta[n]_{n+1}}$ sama. Karena $\Delta[n]_n$ adalah himpunan satu
anggota dan $\Delta[n]_{n+1}=\varnothing$, baris bawah di dua derajat itu
ialah $R\to0$. Posisi panah pada gambar tidak membawa informasi tambahan.
:::

Dengan identifikasi

$$
R^{\Delta[n]_n}\cong R^{\{\mathbf{n+1}\}}\cong R,
\qquad
R^{\Delta[n]_{n+1}}=R^\varnothing=0,
$$

komponen derajat-$n$ dari pemetaan korantai ialah pemetaan $R$-linear

$$
C^n(X_\bullet;R)=R^{X_n}\longrightarrow R,
\qquad
g\longmapsto g(x).
$$

Jadi pemetaan itu tepat evaluasi pada simpleks $x\in X_n$.

::: {.source-audit #o012-rbt-l23-audit-001}
**Audit sumber 23.1.** Notes.tex baris 4950 menulis
$C^n(X_\bullet;R)=R^{X_{n+1}}$, padahal definisi dan diagramnya memberi
$C^n(X_\bullet;R)=R^{X_n}$. Edisi memperbaiki indeks tersebut dan mengetik
kedua pemetaan vertikal sebagai komponen prakomposisi dari pemetaan nama.
:::

Kasus penting diperoleh dengan memilih titik basis $x\in X_0$.

::: {.source-margin #o012-rbt-l23-margin-001}
> **Catatan pinggir sumber.** Dalam penafsiran geometrik yang dimaksud,
> simpleks nol terpilih ini memang merupakan sebuah titik.
:::

Pemetaan bertitik $\Delta[0]\to X_\bullet$ menginduksi morfisma kompleks

$$
C^\bullet(X_\bullet;R)\longrightarrow C^\bullet(\Delta[0];R).
$$

Kodomainnya adalah kompleks

$$
0\longrightarrow R\longrightarrow0\longrightarrow0\longrightarrow\cdots,
$$

dan komponen derajat nolnya adalah evaluasi
$R^{X_0}\to R$, $g\mapsto g(x)$; komponen pada setiap derajat positif menuju
modul nol. Setelah mengambil kohomologi, kita memperoleh pemetaan $R$-linear

$$
\varepsilon_x\colon H^0(X_\bullet;R)\longrightarrow R.
$$

Pemetaan seperti ini disebut **augmentasi** modul-$R$, dan pasangan
$(H^0(X_\bullet;R),\varepsilon_x)$ disebut modul-$R$ teraugmentasi.

Arahnya harus diperhatikan. Jika

$$
f\colon(X_\bullet,x)\longrightarrow(Y_\bullet,y)
$$

adalah pemetaan himpunan-$\Delta$ yang mempertahankan titik basis,
$f_0(x)=y$, maka kontravariansi memberi

$$
f^*\colon H^0(Y_\bullet;R)\longrightarrow H^0(X_\bullet;R),
\qquad
\varepsilon_x\circ f^*=\varepsilon_y.
$$

Dengan demikian

$$
(X_\bullet,x)\longmapsto
(H^0(X_\bullet;R),\varepsilon_x)
$$

adalah fungtor kontravarian dari himpunan-$\Delta$ bertitik ke
modul-$R$ teraugmentasi. Struktur geometrik tambahan berupa pilihan titik
basis tercermin pada augmentasi itu.

::: {.source-audit #o012-rbt-l23-audit-002}
**Audit sumber 23.2.** Notes.tex baris 4954 menyamakan seluruh kompleks
$C^\bullet(X_\bullet;R)$ dengan $R^{X_0}$, yang hanya merupakan komponen
derajat nolnya. Baris 4958 tidak menyatakan arah fungtorialitas. Edisi
mengetik komponen derajat nol dan positif secara terpisah serta menulis
persamaan augmentasi yang menunjukkan arah kontravarian.
:::

::: {.remark #o012-rbt-l23-rem-001}
**Catatan 23.1 (peran sementara himpunan-$\Delta$).** Pada tahap ini,
himpunan-$\Delta$ dan kohomologinya belum dipakai untuk mendefinisikan atau
menghitung kohomologi ruang topologis umum. Alat yang sedang dikembangkan
akan berguna ketika kita sampai pada tujuan itu. Untuk sementara, kita tetap
berfokus pada himpunan-$\Delta$ dan kompleks yang terkait dengannya.
:::

## Gabungan saling lepas dan produk {#o012-rbt-l23-s02}

Hasil umum apa yang membantu menghitung kohomologi himpunan-$\Delta$? Seperti
untuk ruang topologis, kita mulai dari cara paling sederhana membangun objek
baru dari objek lama: gabungan saling lepas. Kita memerlukan empat pengamatan.

1. Untuk himpunan $P,Q$ dan gelanggang $R$, pembatasan memberi isomorfisma
   alami modul-$R$

   $$
   R^{P\sqcup Q}\xrightarrow{\ \cong\ }R^P\oplus R^Q,
   \qquad
   g\longmapsto(g|_P,g|_Q).
   $$

   ::: {.source-margin #o012-rbt-l23-margin-002}
   > **Catatan pinggir sumber, diperjelas.** Untuk sebuah keluarga terindeks
   > himpunan $(P_\alpha)_{\alpha\in I}$, bentuk umumnya adalah
   >
   > $$
   > R^{\bigsqcup_{\alpha\in I}P_\alpha}
   > \cong\prod_{\alpha\in I}R^{P_\alpha},
   > $$
   >
   > yaitu produk, bukan jumlah langsung, bila $I$ tak hingga.
   :::

2. Dari himpunan-$\Delta$ $X_\bullet$ dan $Y_\bullet$ kita membentuk
   $X_\bullet\sqcup Y_\bullet$ secara derajat demi derajat:

   $$
   (X_\bullet\sqcup Y_\bullet)_n=X_n\sqcup Y_n.
   $$

3. Dari kompleks **korantai** modul-$R$ $(A^\bullet,\delta_A)$ dan
   $(B^\bullet,\delta_B)$ kita membentuk jumlah langsung

   $$
   \cdots\longrightarrow A^n\oplus B^n
   \xrightarrow{\ \delta_A^n\oplus\delta_B^n\ }
   A^{n+1}\oplus B^{n+1}\longrightarrow\cdots.
   $$

   Notasi superskrip menegaskan bahwa diferensial menaikkan derajat.

4. Untuk jumlah langsung kompleks tersebut terdapat isomorfisma alami

   $$
   H^n(A^\bullet\oplus B^\bullet)
   \xrightarrow{\ \cong\ }
   H^n(A^\bullet)\oplus H^n(B^\bullet).
   $$

Penggabungan keempat bahan ini memberi hasil berikut.

::: {.lemma #o012-rbt-l23-lem-001 data-proof-status="verified-by-restriction"}
**Lema 23.1 (korantai gabungan saling lepas).** Terdapat isomorfisma alami
kompleks modul-$R$

$$
C^\bullet(X_\bullet\sqcup Y_\bullet;R)
\xrightarrow{\ \cong\ }
C^\bullet(X_\bullet;R)\oplus C^\bullet(Y_\bullet;R).
$$

Pada derajat $n$, isomorfisma itu membatasi sebuah fungsi pada dua komponen.
Ia komutatif dengan diferensial karena setiap *face map* pada gabungan saling
lepas melestarikan komponennya.
:::

::: {.proof #o012-rbt-l23-proof-001 data-origin="edition-proof-closure"}
**Bukti.** Pada derajat $n$, definisikan

$$
\rho_n\colon R^{X_n\sqcup Y_n}\longrightarrow R^{X_n}\oplus R^{Y_n},
\qquad
g\longmapsto(g|_{X_n},g|_{Y_n}).
$$

Pemetaan baliknya merekatkan $(f,h)$ menjadi fungsi yang bernilai $f$ pada
$X_n$ dan $h$ pada $Y_n$; kedua komponen saling lepas, sehingga fungsi ini
terdefinisi secara unik. Setiap *face map* mempertahankan komponen $X$ atau
$Y$. Karena itu pembatasan sebelum atau sesudah menerapkan jumlah bertanda
*face map* memberi hasil yang sama:

$$
\rho_{n+1}\delta_{X\sqcup Y}^n
=(\delta_X^n\oplus\delta_Y^n)\rho_n.
$$

Jadi $(\rho_n)_n$ adalah isomorfisma kompleks. Rumus pembatasan juga
komutatif dengan pemetaan pada $X$ dan $Y$, sehingga isomorfisma ini natural.
:::

::: {.corollary #o012-rbt-l23-cor-001 data-proof-status="follows-from-lemma-23.1"}
**Akibat 23.1 (kohomologi gabungan saling lepas).** Untuk
$n=0,1,2,\ldots$ terdapat isomorfisma alami modul-$R$

$$
H^n(X_\bullet\sqcup Y_\bullet;R)
\xrightarrow{\ \cong\ }
H^n(X_\bullet;R)\oplus H^n(Y_\bullet;R).
$$
:::

::: {.proof #o012-rbt-l23-proof-002 data-origin="edition-proof-closure"}
**Bukti.** Untuk diferensial komponen
$\delta_A\oplus\delta_B$, kernel dan citra dihitung per komponen:

$$
Z^n(A^\bullet\oplus B^\bullet)
=Z^n(A^\bullet)\oplus Z^n(B^\bullet),
\qquad
B^n(A^\bullet\oplus B^\bullet)
=B^n(A^\bullet)\oplus B^n(B^\bullet).
$$

Mengambil hasil bagi kosiklus oleh kobatas lalu memberi

$$
\frac{Z^n(A)\oplus Z^n(B)}{B^n(A)\oplus B^n(B)}
\cong H^n(A)\oplus H^n(B).
$$

Terapkan ini pada isomorfisma kompleks dalam Lema 23.1. Kealamian diwarisi
dari pembatasan komponen pada bukti lema tersebut.
:::

::: {.source-margin #o012-rbt-l23-margin-003}
> **Catatan pinggir sumber, dengan syarat yang dinyatakan.** Untuk keluarga
> himpunan-$\Delta$ $(X_\bullet^\alpha)_{\alpha\in I}$ yang diindeks oleh
> sebuah himpunan, korantai gabungan saling lepas adalah produk kompleks:
>
> $$
> C^\bullet\!\left(\bigsqcup_{\alpha\in I}X_\bullet^\alpha;R\right)
> \cong\prod_{\alpha\in I}C^\bullet(X_\bullet^\alpha;R).
> $$
>
> Dalam teori himpunan ZFC biasa, produk terindeks himpunan di kategori
> $R$-Mod adalah eksak: pilihan praimaj untuk keluarga pemetaan surjektif
> memakai aksioma pilihan. Karena itu
>
> $$
> H^n\!\left(\prod_\alpha C_\alpha^\bullet\right)
> \cong \prod_\alpha H^n(C_\alpha^\bullet).
> $$
>
> Tanpa prinsip pilihan yang memadai,
> langkah surjektivitas produk tidak boleh dianggap otomatis.
:::

::: {.source-audit #o012-rbt-l23-audit-003}
**Audit sumber 23.3.** Notes.tex baris 4975 salah menulis
$R^{P\sqcup Q}\cong R^Q\oplus R^Q$; faktor pertama seharusnya $R^P$.
Baris 4980--4985 memakai notasi subskrip untuk kompleks yang diferensialnya
menaikkan derajat; edisi menggunakan gradasi kohomologis. Baris 5004 salah
menulis `H^(`, yang diperbaiki menjadi $H^n$. Klaim produk tak hingga pada
catatan pinggir baris 5002 dibatasi pada keluarga terindeks himpunan di
$R$-Mod dan dinyatakan dalam ZFC, tempat produk bersifat eksak.
:::

Untuk grupoid fundamental kita sebelumnya mempunyai

$$
\Pi_1(X\sqcup Y)\simeq\Pi_1(X)\sqcup\Pi_1(Y).
$$

Demikian pula, perhitungan kohomologi di atas dapat direduksi ke
himpunan-$\Delta$ yang bukan gabungan saling lepas objek-objek yang lebih
kecil. Perlu dicatat bahwa Lema 23.1 sungguh lebih kuat daripada Akibat 23.1:
dua kompleks dapat mempunyai modul kohomologi yang isomorfik tanpa kompleks
itu sendiri isomorfik.

## Perekatan dua sub-himpunan-$\Delta$ {#o012-rbt-l23-s03}

Sesudah menghitung grupoid fundamental gabungan saling lepas, langkah
berikutnya dahulu ialah menghitung grupoid fundamental sebuah perekatan ruang
$X=U\cup V$ dari lingkungan $U,V\subseteq X$. Secara lebih tepat, kita
mengambil informasi tentang $\Pi_1(X)$ dari $\Pi_1(U)$, $\Pi_1(V)$, dan
$\Pi_1(U\cap V)$. Untuk kohomologi keadaan tidak sesederhana itu, bahkan
sebelum memperhitungkan bahwa kita bekerja dengan himpunan-$\Delta$. Dua
contoh berikut memotivasi alat utama yang akan dikembangkan.

::: {.example #o012-rbt-l23-exa-001}
**Contoh 23.1 (menutupi batas tetrahedron dengan dua cakram).** Pertimbangkan
permukaan kombinatorik $X_\bullet=\partial\Delta[3]$ dengan simpul
$0,1,2,3$. Simpleksnya adalah **subhimpunan wajar takkosong** dari
$\{0,1,2,3\}$: simpleks-$n$ adalah subhimpunan beranggota $n+1$ hanya untuk
$0\leq n\leq2$. Tidak ada simpleks-$3$, karena tetrahedron bagian dalam
tidak termasuk batas.

Definisikan dua sub-himpunan-$\Delta$ $U_\bullet$ dan $V_\bullet$ sebagai
berikut.

1. $U_\bullet$ mempunyai keempat simpul, dua simpleks-$2$
   $\{0,1,2\}$ dan $\{0,1,3\}$, serta semua sisi $X_\bullet$ kecuali
   $\{2,3\}$.

2. $V_\bullet$ juga mempunyai keempat simpul, dua simpleks-$2$
   $\{1,2,3\}$ dan $\{0,2,3\}$, serta semua sisi kecuali $\{0,1\}$.

::: {.source-margin #o012-rbt-l23-margin-004}
> **Catatan pinggir sumber.** Irisan $U_\bullet\cap V_\bullet$ didefinisikan
> derajat demi derajat oleh
> $(U_\bullet\cap V_\bullet)_n=U_n\cap V_n\subseteq X_n$.
:::

Tabel berikut mencatat seluruh simpleks dan sekaligus menggantikan kebutuhan
akan gambar tetrahedron yang bergantung pada posisi visual.

| Derajat | $X=\partial\Delta[3]$ | $U$ | $V$ | $W=U\cap V$ |
|---:|---|---|---|---|
| 0 | $0,1,2,3$ | $0,1,2,3$ | $0,1,2,3$ | $0,1,2,3$ |
| 1 | $01,02,03,12,13,23$ | $01,02,03,12,13$ | $02,03,12,13,23$ | $02,03,12,13$ |
| 2 | $012,013,023,123$ | $012,013$ | $023,123$ | $\varnothing$ |

Setiap sisi diarahkan dari label yang lebih kecil ke label yang lebih besar.
Kedua segitiga $U$ bertemu pada sisi $01$; kedua segitiga $V$ bertemu pada
sisi $23$. Irisan $W$ adalah graf dengan siklus tak berarah

$$
0-2-1-3-0,
$$

yang menggunakan sisi $02,12,13,03$. Dengan demikian jumlah simpleks per
derajat adalah

$$
X:(4,6,4),\qquad
U:(4,5,2),\qquad
V:(4,5,2),\qquad
W:(4,4,0).
$$

::: {.source-margin #o012-rbt-l23-margin-005}
> **Catatan pinggir sumber.** Realisasi geometrik graf irisan $W_\bullet$
> homeomorfik dengan sebuah lingkaran.
:::

Kita mengetahui, atau setidaknya menduga dari model standar, kohomologi
$U_\bullet$, $V_\bullet$, dan $W_\bullet$: dua objek pertama
mentriangulasi cakram $I^2$, sedangkan yang terakhir mentriangulasi lingkaran.
Kita ingin menghitung kohomologi $\partial\Delta[3]$ hanya dari informasi itu.

Fungtorialitas $C^\bullet(-;R)$ memberi pemetaan restriksi pada setiap
derajat.

::: {.figure #o012-rbt-l23-fig-002 data-source-format="xypic"}
**Diagram 23.2 (kuadrat restriksi yang komutatif).** Dengan
$W_\bullet=U_\bullet\cap V_\bullet$, kuadrat

$$
\begin{array}{ccc}
R^{X_n}&\overset{\operatorname{res}_U}{\longrightarrow}&R^{U_n}\\
\downarrow&&\downarrow\\
R^{V_n}&\overset{\operatorname{res}_W}{\longrightarrow}&R^{W_n}
\end{array}
$$

Panah vertikal kiri adalah
$\operatorname{res}_V\colon R^{X_n}\to R^{V_n}$ dan panah vertikal kanan
adalah $\operatorname{res}_W\colon R^{U_n}\to R^{W_n}$. Panah mendatar
bawah adalah $\operatorname{res}_W\colon R^{V_n}\to R^{W_n}$. Kuadrat itu
komutatif: kedua lintasan memetakan $g\in R^{X_n}$ ke $g|_{W_n}$. Dua label
$\operatorname{res}_W$ mempunyai domain berbeda, tetapi keduanya berarti
pembatasan ke himpunan yang sama $W_n$.
:::

Untuk memperoleh bentuk linear berurutan, definisikan

$$
\alpha_n\colon R^{X_n}\longrightarrow R^{U_n}\oplus R^{V_n},
\qquad
\alpha_n(g)=(g|_{U_n},g|_{V_n}),
$$

dan

$$
\beta_n\colon R^{U_n}\oplus R^{V_n}\longrightarrow R^{W_n},
\qquad
\beta_n(f,h)=f|_{W_n}-h|_{W_n}.
$$

Maka diperoleh barisan

$$
0\longrightarrow R^{X_n}
\xrightarrow{\ \alpha_n\ }
R^{U_n}\oplus R^{V_n}
\xrightarrow{\ \beta_n\ }
R^{W_n}\longrightarrow0.
$$

::: {.proof #o012-rbt-l23-proof-003 data-origin="edition-proof-closure"}
**Bukti eksaknya barisan perekatan.**
Barisan ini eksak. Pemetaan $\alpha_n$ injektif karena
$X_n=U_n\cup V_n$: sebuah fungsi pada $X_n$ ditentukan oleh dua
pembatasannya. Jelas $\beta_n\alpha_n=0$. Jika $\beta_n(f,h)=0$, maka $f$
dan $h$ setuju pada $W_n$. Karena itu rumus

$$
g(z)=
\begin{cases}
f(z),&z\in U_n,\\
h(z),&z\in V_n
\end{cases}
$$

terdefinisi dengan baik dan menghasilkan satu-satunya $g\in R^{X_n}$ dengan
$\alpha_n(g)=(f,h)$. Jadi $\ker\beta_n=\operatorname{im}\alpha_n$.
Terakhir, untuk $k\in R^{W_n}$, perluas $k$ menjadi
$f\in R^{U_n}$ dengan menetapkan $f=0$ pada $U_n\setminus W_n$, dan ambil
$h=0$. Maka $\beta_n(f,h)=k$, sehingga $\beta_n$ surjektif.

Pemetaan-pemetaan ini juga komutatif dengan diferensial. Untuk
$g\in R^{X_n}$,

$$
\alpha_{n+1}(\delta_X^n g)
=\bigl(\delta_U^n(g|_{U_n}),\delta_V^n(g|_{V_n})\bigr)
=(\delta_U^n\oplus\delta_V^n)\alpha_n(g),
$$

karena semua *face map* pada sub-himpunan-$\Delta$ merupakan pembatasan
*face map* pada $X_\bullet$. Demikian pula,

$$
\begin{aligned}
\beta_{n+1}(\delta_U^n f,\delta_V^n h)
&=(\delta_U^n f)|_{W_{n+1}}-(\delta_V^n h)|_{W_{n+1}}\\
&=\delta_W^n(f|_{W_n}-h|_{W_n})\\
&=\delta_W^n\beta_n(f,h).
\end{aligned}
$$

Jadi, untuk **setiap** $n\geq0$ dengan
$X_n=U_n\cup V_n$, barisan derajat-$n$ di atas menyatu menjadi barisan
eksak pendek kompleks korantai

$$
0\longrightarrow C^\bullet(X_\bullet;R)
\xrightarrow{\ \alpha\ }
C^\bullet(U_\bullet;R)\oplus C^\bullet(V_\bullet;R)
\xrightarrow{\ \beta\ }
C^\bullet(W_\bullet;R)\longrightarrow0.
$$
:::

Kita ingin mengetahui kohomologi kompleks taknol paling kiri, sedangkan
yang telah kita hitung—setidaknya secara prinsip—hanyalah kohomologi dua
kompleks lain dalam barisan tersebut.
:::

Argumen itu berlaku tanpa perubahan untuk sembarang himpunan-$\Delta$
$X_\bullet$ dan sub-himpunan-$\Delta$ $U_\bullet,V_\bullet$ yang memenuhi

$$
X_n=U_n\cup V_n
\qquad\text{untuk setiap }n\geq0.
$$

Dengan $W_\bullet=U_\bullet\cap V_\bullet$, kita kembali memperoleh barisan
eksak pendek kompleks modul-$R$ yang ditampilkan di atas.

::: {.source-audit #o012-rbt-l23-audit-004}
**Audit sumber 23.4.** Notes.tex baris 5023--5024 menggambarkan simpleks
$\partial\Delta[3]$ sebagai semua subhimpunan beranggota $n+1$ tanpa
membatasi $n$; untuk batas tetrahedron, yang benar ialah subhimpunan wajar
takkosong, sehingga $0\leq n\leq2$. Baris 5057 hanya menyebut eksak sebagai
latihan singkat. Edisi memberi sensus simpleks dan bukti lengkap injektivitas,
perekatan pada kernel, surjektivitas melalui perluasan dengan nol, serta
komutativitas kedua pemetaan dengan diferensial. Baris 5067 juga diperjelas
dengan kuantor `untuk setiap n` pada syarat penutup derajat demi derajat.
:::

## Fungsi tereduksi pada sebuah hasil bagi {#o012-rbt-l23-s04}

Untuk contoh kedua, kita menyelidiki bagaimana kohomologi hasil bagi mungkin
dihitung dari kohomologi himpunan-$\Delta$ semula dan sub-himpunan-$\Delta$
yang diruntuhkan.

::: {.example #o012-rbt-l23-exa-002 data-source-status="continues-in-lecture-024"}
**Contoh 23.2 (pasangan dan fungsi pada hasil bagi; bagian pertama).** Ambil
himpunan-$\Delta$ $X_\bullet$ beserta sub-himpunan-$\Delta$
$A_\bullet\subset X_\bullet$.

::: {.source-margin #o012-rbt-l23-margin-006}
> **Catatan pinggir sumber.** Data ini disebut sebuah **pasangan**
> $(X_\bullet,A_\bullet)$.
:::

Secara geometrik, $X_\bullet$ dapat mentriangulasi sebuah ruang dan
$A_\bullet$ mentriangulasi subruangnya. Kita dapat membentuk ruang hasil bagi
$|X_\bullet|/|A_\bullet|$, tetapi belum jelas bahwa terdapat hasil bagi
himpunan-$\Delta$ yang wajar, dengan simpleks derajat-$n$ berupa
$X_n/A_n$, dan yang realisasinya mentriangulasi hasil bagi topologis itu.
Untuk sementara, andaikan terdapat himpunan-$\Delta$
$X_\bullet/A_\bullet$ beserta pemetaan hasil bagi

$$
X_\bullet\longrightarrow X_\bullet/A_\bullet.
$$

Pertanyaannya ialah apakah
$H^n(X_\bullet/A_\bullet;R)$ dapat dihitung dari
$H^n(X_\bullet;R)$ dan $H^n(A_\bullet;R)$.

Mulailah pada tingkat himpunan. Misalkan $i\colon A\hookrightarrow X$.
Jika $A\ne\varnothing$, definisikan

$$
X/A:=X/(a_1\sim a_2\text{ untuk semua }a_1,a_2\in A).
$$

Pemetaan hasil bagi $q\colon X\to X/A$ meruntuhkan seluruh $A$ ke titik
basis kanonik $*=[a]$. Prakomposisi memberi pemetaan $R$-linear

$$
R^{X/A}\xrightarrow{\ q^*\ }R^X
\xrightarrow{\ i^*\ }R^A.
$$

Pemetaan $q^*$ injektif karena $q$ surjektif, sedangkan $i^*$ surjektif
karena setiap fungsi $A\to R$ dapat diperluas dengan memberikan nilai nol
pada $X\setminus A$. Bila $R$ bukan gelanggang nol, ini pada umumnya bukan
kompleks: citra $q^*$ terdiri atas
fungsi $X\to R$ yang konstan pada $A$, sementara kernel $i^*$ terdiri atas
fungsi yang bernilai nol pada $A$. Jadi
$\operatorname{im}q^*$ tidak termuat dalam $\ker i^*$.

Titik basis hasil bagi memberi evaluasi

$$
\operatorname{ev}_*\colon R^{X/A}\longrightarrow R,
$$

dan kita definisikan modul fungsi **tereduksi**

$$
\widetilde R^{X/A}:=\ker(\operatorname{ev}_*)
=\{\varphi\colon X/A\to R\mid\varphi(*)=0\}.
$$

Pembatasan pemetaan yang sama, bukan seluruh $q^*$, menghasilkan isomorfisma

$$
q^*\big|_{\widetilde R^{X/A}}\colon
\widetilde R^{X/A}\xrightarrow{\ \cong\ }\ker(i^*)\subseteq R^X.
$$

::: {.proof #o012-rbt-l23-proof-004 data-origin="edition-proof-closure"}
**Bukti isomorfisma fungsi tereduksi.**
Memang, jika $\varphi(*)=0$, maka $\varphi\circ q$ bernilai nol pada $A$.
Sebaliknya, setiap $g\colon X\to R$ yang nol pada $A$ turun secara unik ke
$\varphi\colon X/A\to R$ dengan $\varphi(*)=0$. Oleh karena itu kita
memperoleh barisan eksak pendek

$$
0\longrightarrow\widetilde R^{X/A}
\xrightarrow{\ q^*\ }R^X
\xrightarrow{\ i^*\ }R^A\longrightarrow0.
$$

Jika $A=\varnothing$, tidak ada unsur $a$ yang menghasilkan titik basis
kanonik. Dengan konvensi $X/\varnothing=X$, kita mempunyai
$R^A=R^\varnothing=0$, $i^*$ adalah pemetaan nol, dan
$\ker i^*=R^X$. Barisan yang relevan hanyalah

$$
0\longrightarrow R^X\xrightarrow{\ \operatorname{id}\ }R^X
\longrightarrow0,
$$

bukan barisan yang memakai kernel evaluasi pada titik basis yang tidak ada.
Pemisahan kedua kasus ini juga menunjukkan mengapa hasil bagi
himpunan-$\Delta$ derajat demi derajat memerlukan kehati-hatian: sekalipun
$A_\bullet$ takkosong, beberapa $A_n$ dapat kosong.
:::

Dengan cara ini kita bahkan tidak perlu membentuk himpunan hasil bagi untuk
mendapatkan modul yang berperilaku seperti fungsi tereduksi padanya:
$\ker i^*$ sudah tersedia langsung. Hal itu juga membantu mengatasi
ketidakjelasan apakah $X_\bullet/A_\bullet$ sendiri merupakan konstruksi
himpunan-$\Delta$ yang baik.

**Kelanjutan sumber.** Lingkungan `example` sumber yang dibuka pada
Notes.tex baris 5076 **belum berakhir** pada batas unit ini. Baris 5112 kosong;
Kuliah 24 dimulai di baris 5113 dan contoh baru ditutup pada baris 5121.
Penutupan blok Markdown edisi ini hanya menjaga struktur berkas, bukan
menyatakan bahwa lingkungan sumber telah selesai. Baris 5113--5121 tidak
diimpor ke Unit 23 dan harus diterjemahkan sebagai awal Unit 24.
:::

::: {.source-audit #o012-rbt-l23-audit-005}
**Audit sumber 23.5.** Notes.tex baris 5078--5111 berganti-ganti antara
$A$ dan $Y$ untuk subobjek yang sama. Edisi memakai $A$ secara konsisten.
Pernyataan titik basis kanonik pada baris 5090 hanya benar bila
$A\ne\varnothing$; kasus kosong dipisahkan. Baris 5102--5105 diperketat:
yang dipetakan isomorfik oleh $q^*$ ke $\ker i^*$ bukan seluruh
$R^{X/A}$, melainkan pembatasan
$q^*|_{\ker(\operatorname{ev}_*)}$. Edisi membuktikan kedua arah
isomorfisma dan tidak menutup lingkungan contoh sumber yang melintasi batas
Kuliah 24.
:::

::: {.source-audit #o012-rbt-l23-audit-006}
**Audit aksesibilitas 23.6.** Dua diagram Xy-pic pada Notes.tex baris
4944--4947 dan 5045--5048 diganti dengan diagram semantik terpusat yang
menamai setiap domain, kodomain, dan pemetaan. Keenam catatan pinggir
ditempatkan kembali dalam urutan baca. Sensus tetrahedron, daftar sisi,
komutativitas, dan fungsi setiap panah juga dinyatakan dalam prosa, sehingga
tidak ada argumen yang bergantung pada posisi, warna, atau isi gambar saja.
:::

::: {.source-audit #o012-rbt-l23-audit-007}
**Audit prosa 23.7.** Kekeliruan ejaan, tanda baca, artikel, dan frasa ganda
yang deterministik pada Notes.tex baris 4941, 4952--4953, 4987, 5002, 5013,
5050, dan 5057 dinormalisasi dalam bahasa Indonesia alami tanpa mengubah
urutan maupun isi matematis sumber.
:::

::: {.source-audit #o012-rbt-l23-audit-008}
**Audit batas 23.8.** Lingkungan `example` sumber melintasi penanda Kuliah 24.
Edisi menutup blok Markdown Unit 23 hanya secara sintaktis, mempertahankan
pengenal kelanjutan, dan tidak memindahkan satu pun baris 5113--5121 ke unit
ini. Unit 24 harus membuka kembali contoh yang sama sebelum menerjemahkan
penutupnya.
:::

# Pendamping penguasaan: pemeriksaan, petunjuk, dan solusi lengkap {.unnumbered #o012-rbt-l23-mastery}

Enam paket berikut adalah materi asli edisi. Semuanya dibatasi pada sasaran
Unit 23: evaluasi pada simpleks, augmentasi bertitik, gabungan saling lepas,
eksaknya perekatan, sensus tetrahedron, dan fungsi tereduksi pada hasil bagi.

::: {.exercise #o012-rbt-l23-mcheck-001 data-origin="edition-original"}
**Pemeriksaan Penguasaan 23.1 (evaluasi dalam derajat $n$).** Untuk
$x\in X_n$, tentukan pemetaan korantai yang diinduksi oleh
$\ulcorner x\urcorner\colon\Delta[n]\to X_\bullet$ pada derajat $n$ dan
$n+1$. Buktikan langsung bahwa komponen derajat-$n$ adalah evaluasi pada $x$
dan jelaskan mengapa rumus $C^n(X_\bullet;R)=R^{X_{n+1}}$ tidak mungkin benar.
:::

::: {.hint #o012-rbt-l23-hint-001 data-origin="edition-original"}
**Petunjuk.** Gunakan
$\Delta[n]_n=\{\{0,\ldots,n\}\}$ dan
$\Delta[n]_{n+1}=\varnothing$. Ingat bahwa prakomposisi oleh komponen
pemetaan nama membalik arah.
:::

::: {.solution #o012-rbt-l23-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 23.1.** Pada derajat $n$, komponen pemetaan nama ialah

$$
\ulcorner x\urcorner_n\colon\Delta[n]_n\longrightarrow X_n,
\qquad
\{0,\ldots,n\}\longmapsto x.
$$

Prakomposisi memberi

$$
\ulcorner x\urcorner_n^*\colon R^{X_n}\longrightarrow
R^{\Delta[n]_n}\cong R,
\qquad
g\longmapsto g(x).
$$

Jadi komponen itu tepat evaluasi. Pada derajat $n+1$, kodomain pemetaan
prakomposisi adalah
$R^{\Delta[n]_{n+1}}=R^\varnothing=0$, sehingga komponen
$R^{X_{n+1}}\to0$ adalah pemetaan nol yang unik. Diagram kompleks komutatif
karena pemetaan nama komutatif dengan semua *face map*.

Menurut definisi, korantai derajat $k$ adalah fungsi pada simpleks-$k$:
$C^k(X_\bullet;R)=R^{X_k}$. Maka menulis
$C^n=R^{X_{n+1}}$ menggeser derajat dan bertentangan sekaligus dengan
definisi, domain evaluasi $g(x)$, dan diagram yang menempatkan
$R^{X_n}$ pada derajat $n$.
:::

::: {.exercise #o012-rbt-l23-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 23.2 (kealamian dan pemisahan augmentasi).** Untuk
pemetaan bertitik
$f\colon(X_\bullet,x)\to(Y_\bullet,y)$, buktikan
$\varepsilon_x f^*=\varepsilon_y$ pada $H^0$. Lalu tunjukkan bahwa pemetaan

$$
s\colon R\longrightarrow H^0(X_\bullet;R),
\qquad
r\longmapsto[\text{fungsi konstan bernilai }r]
$$

memenuhi $\varepsilon_xs=\operatorname{id}_R$ bila $X_\bullet$ bertitik,
dan simpulkan dekomposisi modul yang dihasilkan.
:::

::: {.hint #o012-rbt-l23-hint-002 data-origin="edition-original"}
**Petunjuk.** Wakili kelas $H^0$ oleh fungsi $g\colon Y_0\to R$ dengan
$\delta^0g=0$. Evaluasi $g\circ f_0$ pada $x$. Untuk pemisahan, fungsi
konstan selalu merupakan kosiklus nol.
:::

::: {.solution #o012-rbt-l23-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 23.2.** Ambil $[g]\in H^0(Y_\bullet;R)$. Karena
$f_0(x)=y$,

$$
(\varepsilon_x\circ f^*)([g])
=\varepsilon_x([g\circ f_0])
=(g\circ f_0)(x)
=g(y)
=\varepsilon_y([g]).
$$

Jadi kuadrat augmentasi komutatif dan arah $f^*$ memang berlawanan dengan
$f$. Untuk $r\in R$, fungsi konstan $c_r$ memenuhi
$\delta^0c_r=0$, sebab pada setiap sisi kedua nilai titik ujungnya sama.
Tidak ada korantai berderajat negatif, sehingga $[c_r]$ terdefinisi di
$H^0$. Evaluasi memberi

$$
(\varepsilon_x\circ s)(r)=c_r(x)=r.
$$

Maka $s$ adalah invers kanan bagi augmentasi. Setiap $m\in H^0(X;R)$ mempunyai
uraian unik

$$
m=\bigl(m-s\varepsilon_x(m)\bigr)+s\varepsilon_x(m),
$$

dengan suku pertama di $\ker\varepsilon_x$ dan suku kedua di $s(R)$.
Akibatnya

$$
H^0(X_\bullet;R)\cong\ker\varepsilon_x\oplus R.
$$
:::

::: {.exercise #o012-rbt-l23-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 23.3 (jumlah hingga versus produk tak hingga).**
Untuk keluarga himpunan-$\Delta$ $(X_\bullet^\alpha)_{\alpha\in I}$,
buktikan isomorfisma kompleks

$$
C^\bullet\!\left(\bigsqcup_{\alpha\in I}X_\bullet^\alpha;R\right)
\cong\prod_{\alpha\in I}C^\bullet(X_\bullet^\alpha;R).
$$

Jelaskan mengapa ruas kanan bukan jumlah langsung bila $I$ tak hingga, dan
buktikan dalam ZFC bahwa kohomologi produk kompleks modul-$R$ adalah produk
kohomologi.
:::

::: {.hint #o012-rbt-l23-hint-003 data-origin="edition-original"}
**Petunjuk.** Sebuah fungsi pada gabungan saling lepas setara dengan keluarga
semua pembatasannya, tanpa syarat dukungan hingga. Kernel dihitung per
koordinat. Untuk citra, pilih praimaj pada setiap koordinat; langkah terakhir
inilah yang memakai aksioma pilihan.
:::

::: {.solution #o012-rbt-l23-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 23.3.** Pada setiap derajat $n$, pemetaan pembatasan

$$
R^{\bigsqcup_\alpha X_n^\alpha}\longrightarrow
\prod_\alpha R^{X_n^\alpha},
\qquad
g\longmapsto(g|_{X_n^\alpha})_\alpha
$$

bijektif: keluarga fungsi di ruas kanan melekat secara unik menjadi sebuah
fungsi pada gabungan saling lepas. Karena setiap *face map* melestarikan
komponen $\alpha$, bijeksi ini komutatif dengan diferensial dan memberi
isomorfisma kompleks.

Jika $I$ tak hingga, sebuah unsur produk boleh mempunyai komponen taknol pada
tak hingga banyak indeks. Jumlah langsung hanya memuat keluarga dengan
dukungan hingga. Misalnya, bila semua $X_0^\alpha$ adalah himpunan satu
anggota dan
$1_R\ne0$, keluarga konstan $(1_R)_\alpha$ berada di produk tetapi tidak di
jumlah langsung.

Tuliskan $C^\bullet=\prod_\alpha C_\alpha^\bullet$. Karena diferensial
bertindak per koordinat,

$$
Z^n(C)=\ker\!\left(\prod_\alpha\delta_\alpha^n\right)
=\prod_\alpha Z^n(C_\alpha).
$$

Juga

$$
B^n(C)=\operatorname{im}\!\left(\prod_\alpha\delta_\alpha^{n-1}\right)
=\prod_\alpha B^n(C_\alpha).
$$

Inklusi dari kiri ke kanan jelas. Untuk arah sebaliknya, bagi setiap
$b_\alpha\in B^n(C_\alpha)$ pilih
$a_\alpha$ dengan $\delta_\alpha^{n-1}a_\alpha=b_\alpha$; pilihan serentak
ini tersedia dalam ZFC. Akhirnya pemetaan

$$
\prod_\alpha Z^n(C_\alpha)\longrightarrow
\prod_\alpha H^n(C_\alpha),
\qquad
(z_\alpha)\longmapsto([z_\alpha])
$$

surjektif dalam ZFC dan berkernel $\prod_\alpha B^n(C_\alpha)$. Teorema
isomorfisma memberi

$$
H^n\!\left(\prod_\alpha C_\alpha^\bullet\right)
\cong\prod_\alpha H^n(C_\alpha^\bullet).
$$
:::

::: {.exercise #o012-rbt-l23-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 23.4 (eksak melalui perekatan fungsi).** Misalkan
$U_\bullet,V_\bullet\subseteq X_\bullet$ dan
$X_n=U_n\cup V_n$ untuk setiap $n$. Dengan
$W_\bullet=U_\bullet\cap V_\bullet$, buktikan dari definisi bahwa

$$
0\to C^\bullet(X;R)\xrightarrow{\alpha}
C^\bullet(U;R)\oplus C^\bullet(V;R)
\xrightarrow{\beta}C^\bullet(W;R)\to0
$$

adalah barisan eksak pendek kompleks, untuk
$\alpha(g)=(g|_U,g|_V)$ dan $\beta(f,h)=f|_W-h|_W$.
:::

::: {.hint #o012-rbt-l23-hint-004 data-origin="edition-original"}
**Petunjuk.** Kerjakan setiap derajat terlebih dahulu. Pasangan dalam kernel
$\beta$ melekat karena setuju pada irisan. Untuk surjektivitas, perluas
fungsi pada $W_n$ dengan nol ke $U_n$. Sesudah itu gunakan bahwa restriksi
komutatif dengan diferensial korantai.
:::

::: {.solution #o012-rbt-l23-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 23.4.** Untuk setiap $n$, $\alpha_n$ injektif karena
fungsi pada $X_n=U_n\cup V_n$ ditentukan oleh pembatasannya. Selain itu
$\beta_n\alpha_n(g)=g|_{W_n}-g|_{W_n}=0$.

Jika $(f,h)\in\ker\beta_n$, maka $f|_{W_n}=h|_{W_n}$. Definisikan
$g\colon X_n\to R$ dengan $g=f$ pada $U_n$ dan $g=h$ pada $V_n$.
Kesamaan pada irisan membuat definisi ini konsisten, dan
$\alpha_n(g)=(f,h)$. Jadi
$\ker\beta_n=\operatorname{im}\alpha_n$.

Untuk $k\in R^{W_n}$, definisikan $f\in R^{U_n}$ dengan $f=k$ pada $W_n$
dan $f=0$ pada $U_n\setminus W_n$, lalu ambil $h=0$. Maka
$\beta_n(f,h)=k$, sehingga $\beta_n$ surjektif.

Terakhir, karena $U,V,W$ adalah sub-himpunan-$\Delta$, pembatasan komutatif
dengan setiap jumlah bertanda *face map*. Oleh sebab itu

$$
\alpha_{n+1}\delta_X^n
=(\delta_U^n\oplus\delta_V^n)\alpha_n,
\qquad
\beta_{n+1}(\delta_U^n\oplus\delta_V^n)
=\delta_W^n\beta_n.
$$

Jadi $\alpha$ dan $\beta$ adalah morfisma kompleks, dan eksak pada setiap
derajat berarti barisan tersebut eksak pendek sebagai barisan kompleks.
:::

::: {.exercise #o012-rbt-l23-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 23.5 (sensus dan irisan tetrahedron).** Dari
definisi $U_\bullet,V_\bullet\subseteq\partial\Delta[3]$ pada Contoh 23.1,
turunkan—bukan sekadar baca dari gambar—jumlah simpleks

$$
X:(4,6,4),\quad U:(4,5,2),\quad V:(4,5,2),\quad W:(4,4,0).
$$

Tunjukkan bahwa realisasi $W$ adalah lingkaran dan bahwa
$X_n=U_n\cup V_n$ untuk setiap $n$.
:::

::: {.hint #o012-rbt-l23-hint-005 data-origin="edition-original"}
**Petunjuk.** Daftar semua subhimpunan wajar takkosong dari
$\{0,1,2,3\}$. Irisan membuang sisi $01$ dan $23$ sekaligus serta tidak
mempunyai segitiga. Susun empat sisi sisanya menjadi satu siklus.
:::

::: {.solution #o012-rbt-l23-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 23.5.** Batas tetrahedron mempunyai
$\binom41=4$ simpul, $\binom42=6$ sisi, dan $\binom43=4$ segitiga; subhimpunan
beranggota empat dikeluarkan. Jadi $X$ mempunyai sensus $(4,6,4)$.

$U$ mempertahankan semua simpul, membuang tepat sisi $23$, dan mempertahankan
tepat segitiga $012,013$, sehingga sensusnya $(4,5,2)$. Demikian pula $V$
membuang tepat sisi $01$ dan mempertahankan $023,123$, sehingga sensusnya
$(4,5,2)$. Irisan $W$ mempertahankan semua simpul dan hanya sisi yang muncul
di kedua daftar,

$$
02,03,12,13,
$$

serta tidak mempunyai segitiga. Jadi sensusnya $(4,4,0)$. Graf itu terhubung
dan setiap simpul berderajat dua; urutan
$0-2-1-3-0$ melintasi setiap sisi tepat sekali. Realisasinya adalah satu
siklus, maka homeomorfik dengan $S^1$.

Pada derajat nol kedua subobjek memuat semua simpul. Pada derajat satu, sisi
yang hilang dari $U$ adalah $23$ tetapi sisi itu berada di $V$, sedangkan
sisi yang hilang dari $V$ adalah $01$ tetapi berada di $U$. Pada derajat dua,
dua pasangan segitiga mereka saling melengkapi seluruh empat segitiga $X$.
Pada derajat $n\geq3$ ketiga himpunan kosong. Jadi
$X_n=U_n\cup V_n$ untuk setiap $n$.
:::

::: {.exercise #o012-rbt-l23-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 23.6 (fungsi tereduksi dan kasus kosong).** Untuk
inklusi himpunan $i\colon A\hookrightarrow X$, buktikan bahwa bila
$A\ne\varnothing$,

$$
q^*|_{\ker(\operatorname{ev}_*)}\colon
\ker(\operatorname{ev}_*)\xrightarrow{\ \cong\ }\ker(i^*)
$$

adalah isomorfisma, lalu turunkan barisan eksak pendek yang bersesuaian.
Jelaskan tepat apa yang berubah bila $A=\varnothing$.
:::

::: {.hint #o012-rbt-l23-hint-006 data-origin="edition-original"}
**Petunjuk.** Fungsi pada $X/A$ berada di kernel evaluasi tepat bila nilainya
pada kelas yang diruntuhkan adalah nol. Untuk arah balik, turunkan fungsi
$g\colon X\to R$ yang nol pada $A$ ke kelas-kelas ekuivalensi. Pada kasus
kosong tidak ada kelas runtuhan yang menyediakan titik basis.
:::

::: {.solution #o012-rbt-l23-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 23.6.** Andaikan $A\ne\varnothing$ dan tuliskan
$*=[A]\in X/A$. Jika
$\varphi\in\ker(\operatorname{ev}_*)$, maka untuk setiap $a\in A$,

$$
(q^*\varphi)(a)=\varphi(q(a))=\varphi(*)=0.
$$

Jadi $q^*\varphi\in\ker i^*$. Pembatasan $q^*$ tetap injektif karena $q$
surjektif. Sebaliknya, jika $g\in\ker i^*$, definisikan

$$
\varphi([x])=g(x).
$$

Rumus ini terdefinisi dengan baik: kelas bukan-$*$ berisi satu unsur,
sedangkan semua wakil kelas $*$ berada di $A$ dan bernilai nol. Maka
$\varphi(*)=0$ dan $q^*\varphi=g$. Jadi pembatasan itu surjektif serta
merupakan isomorfisma. Karena $i^*$ surjektif melalui perluasan dengan nol,
diperoleh

$$
0\longrightarrow\ker(\operatorname{ev}_*)
\xrightarrow{\ q^*\ }R^X
\xrightarrow{\ i^*\ }R^A\longrightarrow0.
$$

Jika $A=\varnothing$, tidak ada $*=[A]$ kanonik dan karena itu tidak ada
evaluasi kanonik yang kernel-nya dapat dipakai. Dengan
$X/\varnothing=X$, pemetaan $q$ adalah identitas,
$R^\varnothing=0$, dan $\ker i^*=R^X$. Barisannya merosot menjadi

$$
0\longrightarrow R^X\xrightarrow{\operatorname{id}}R^X
\longrightarrow0.
$$

Jadi kasus kosong bukan alasan untuk memilih titik basis sebarang; ia
memerlukan pernyataan terpisah.
:::

::: {.boundary #o012-rbt-l23-boundary-001}
**Batas ke Unit 24.** Rentang Unit 23 berhenti pada Notes.tex baris 5112,
tepat sebelum penanda `\lecturenum{24}` pada baris 5113. Lingkungan contoh
sumber yang dibuka pada baris 5076 tetap terbuka dan baru ditutup pada baris
5121. Unit 24 harus mulai pada baris 5113, menerjemahkan kelanjutan itu, dan
baru kemudian menutup objek sumbernya. Tidak satu pun isi baris 5113--5121
dimasukkan ke unit ini. Kursor sumber berikutnya yang tepat adalah baris 5113.
:::
