---
title: "Topologi Aljabar"
subtitle: "Unit 22: Himpunan-Delta, Realisasi, dan Korantai Simpleksial"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "23 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l22-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 4501--4938 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L4501-L4938)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang aktif itu terdiri atas 438 baris fisik. Setelah dinormalisasi dengan
LF dan mempertahankan baris kosong penutupnya, ukurannya 20.585 byte dan
SHA-256-nya adalah
`86275c590cfcdf8519d3ce8d077fc48619bb94c3fdf039ca805ae4b7df995b7f`.
Kuliah 23 dimulai pada Notes.tex baris 4939, sehingga kursor berikutnya ialah
baris 4939. Materi sumber dan adaptasi Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Perubahan edisi mencakup penerjemahan, pemformatan ulang, pemberian pengenal
stabil, dan pemindahan lima catatan pinggir ke urutan bacaan utama. Dua gambar
TikZ dan tiga hubungan Xy-pic sumber ditulis ulang sebagai lima diagram
semantik terpusat. Setiap diagram menyatakan simpul, sisi, muka, arah, atau
komutativitasnya dengan teks dan rumus; tidak ada makna yang bergantung pada
posisi, warna, atau ketebalan garis.

Rentang sumber memuat tepat enam definisi, sebelas contoh, lima lema, tiga
bukti, tiga catatan, lima catatan pinggir, dua TikZ, tiga Xy-pic, dua label,
satu rujukan silang, delapan tampilan `\[...\]`, empat `align*`, satu `cases`,
dan satu lingkungan `center`. Tidak ada latihan sumber, konstruksi,
`enumerate`, `align` tanpa bintang, sitasi, gambar eksternal, `input`, atau
`include`.

Edisi memperbaiki beberapa persoalan sumber yang memengaruhi tipe atau
kebenaran: pemetaan nama sebuah simpleks tidak selalu merupakan inklusi;
relasi realisasi dan persamaan morfisma diberi tipe lengkap; dimensi tak
hingga dibedakan dari himpunan-$\Delta$ kosong; pemetaan kanonik
$|\Delta[n]|\to\Delta^n$ ditulis dengan indeks yang benar; dan diferensial
korantai memakai semua $n+2$ muka, bukan hanya $n+1$ muka. Klaim keterhinggaan
generator diberi hipotesis Noetherian, sedangkan klaim kisi untuk perubahan
koefisien $\mathbb Z\to\mathbb R$ dibatasi pada himpunan-$\Delta$ berhingga.
Bukti yang oleh sumber hanya disebut “latihan” diselesaikan secara lengkap.

Enam pemeriksaan penguasaan, enam petunjuk, dan enam solusi lengkap merupakan
materi asli edisi dan tersedia di bawah CC BY 4.0. Edisi ini bersifat
independen; edisi ini tidak disponsori, didukung, disahkan, ataupun diberi
status resmi oleh David Michael Roberts atau institusinya. Produksi edisi ini
dibantu oleh **OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini menambah
transparansi proses dan tidak mengurangi kredit penulis sumber ataupun kredit
kontributor manusia.

# Kuliah 22 {#o012-rbt-l22}

## Pemetaan permukaan kombinatorik {#o012-rbt-l22-s01}

Pada akhirnya kita menginginkan perilaku fungtorial. Karena itu kita mulai
dengan pemetaan yang mengirim simpul ke simpul, sisi ke sisi, dan segitiga ke
segitiga secara kompatibel.

::: {.definition #o012-rbt-l22-def-001}
**Definisi 22.1 (pemetaan permukaan kombinatorik).** Untuk permukaan
kombinatorik $X_\bullet$ dan $Y_\bullet$, sebuah pemetaan
$f\colon X_\bullet\to Y_\bullet$ adalah tiga fungsi

$$
f_n\colon X_n\longrightarrow Y_n
\qquad(n=0,1,2)
$$

yang memenuhi

$$
d_{i,Y}^{n}\circ f_n
=f_{n-1}\circ d_{i,X}^{n}
\qquad
(1\leq n\leq2,\ 0\leq i\leq n).
$$

Dengan kata lain, mengambil muka lalu memetakan memberi hasil yang sama
dengan memetakan lalu mengambil muka yang bersesuaian.
:::

Pemetaan seperti ini sangat kaku. Banyak fungsi kontinu yang tampak wajar
antara realisasi tidak berasal dari pemetaan antara triangulasi yang telah
dipilih. Definisi itu juga mencakup pemetaan graf berarah bila himpunan
segitiga domain dan kodomain kosong, serta pemetaan dari graf berarah ke
permukaan kombinatorik yang mempunyai segitiga.

::: {.example #o012-rbt-l22-exa-001}
**Contoh 22.1 (inklusi 1-kerangka).** Untuk setiap permukaan kombinatorik
$X_\bullet$ terdapat pemetaan

$$
\operatorname{sk}_1X_\bullet\longrightarrow X_\bullet
$$

yang merupakan identitas pada $X_0$ dan $X_1$, sedangkan komponen derajat
duanya adalah satu-satunya fungsi

$$
(\operatorname{sk}_1X_\bullet)_2=\varnothing\longrightarrow X_2.
$$
:::

::: {.example #o012-rbt-l22-exa-002}
**Contoh 22.2 (menamai sebuah segitiga).** Setelah memilih
$x\in X_2$, ada pemetaan kanonik

$$
\ulcorner x\urcorner\colon\Delta[2]\longrightarrow X_\bullet
$$

yang mengirim muka puncak tunggal ke $x$ dan setiap muka bawah ke muka
bersesuaian dari $x$. Untuk sebuah muka segitiga pada
$\partial\Delta[3]$, pemetaan ini memang merupakan inklusi
$\Delta[2]\hookrightarrow\partial\Delta[3]$. Pada permukaan kombinatorik
umum, beberapa muka $x$ dapat teridentifikasi, sehingga pemetaan nama itu
tidak harus injektif.
:::

::: {.source-audit #o012-rbt-l22-audit-001}
**Audit sumber 22.1.** Notes.tex baris 4522--4523 mengatakan tanpa syarat
bahwa sebuah segitiga dapat “diinklusikan” ke $X_\bullet$. Yang tersedia
secara kanonik ialah pemetaan nama setelah memilih $x\in X_2$; ia hanya
merupakan inklusi bila muka-muka $x$ tidak teridentifikasi. Edisi menyatakan
pilihan dan perbedaan itu secara eksplisit.
:::

::: {.example #o012-rbt-l22-exa-003}
**Contoh 22.3 (poligon dan garis menuju satu gelang).** Misalkan
$L_\bullet$ adalah graf berarah dengan satu simpul $v$ dan satu sisi gelang
$e$. Jika $P_\bullet$ adalah graf poligonal berarah, terdapat pemetaan

$$
P_\bullet\longrightarrow L_\bullet
$$

yang mengirim semua simpul ke $v$ dan semua sisi ke $e$.

::: {.source-margin #o012-rbt-l22-margin-001}
> **Catatan pinggir sumber.** Graf poligonal berarah adalah graf berarah
> berhingga dengan banyak simpul sama dengan banyak sisi. Simpul-simpulnya
> diurutkan secara siklik, dan setiap dua simpul bersebelahan dihubungkan oleh
> satu sisi dengan salah satu dari dua orientasi.
:::

Ada pula graf tak hingga $R_\bullet$ dengan simpul $v_k$, $k\in\mathbb Z$,
dan sisi $r_k\colon v_k\to v_{k+1}$. Realisasinya homeomorfik dengan
$\mathbb R$, dan pemetaan $R_\bullet\to L_\bullet$ sekali lagi mengirim
semua simpul ke $v$ dan semua sisi ke $e$.
:::

::: {.example #o012-rbt-l22-exa-004 data-source-label="eg:infinite_cylinder"}
**Contoh 22.4 (silinder kombinatorik tak hingga).** Definisikan
$C_\bullet$ dengan

$$
C_0=\{v_i\mid i\in\mathbb Z\},\qquad
C_1=\{e_{1i},e_{2i},e_{3i}\mid i\in\mathbb Z\},
$$

dan

$$
C_2=\{f_{1i},f_{2i}\mid i\in\mathbb Z\}.
$$

Data titik ujungnya ialah

$$
\begin{array}{c|cc}
 &d_1^1&d_0^1\\ \hline
e_{1i}&v_i&v_i\\
e_{2i}&v_i&v_{i+1}\\
e_{3i}&v_{i+1}&v_i
\end{array}
$$

dan data muka dua dimensinya ialah

$$
\begin{array}{c|ccc}
 &d_0^2&d_1^2&d_2^2\\ \hline
f_{1i}&e_{3i}&e_{1i}&e_{2i}\\
f_{2i}&e_{2i}&e_{1,i+1}&e_{3i}.
\end{array}
$$

::: {.figure #o012-rbt-l22-fig-001 data-source-format="tikz"}
**Diagram 22.1 (deskripsi semantik silinder tak hingga).** Untuk setiap
$i$, satu persegi antara $v_i$ dan $v_{i+1}$ mempunyai sisi vertikal gelang
$e_{1i}$ di kiri dan $e_{1,i+1}$ di kanan, sisi horizontal $e_{2i}$ dari
$v_i$ ke $v_{i+1}$ pada kedua batas lingkarannya, dan diagonal $e_{3i}$ dari
$v_{i+1}$ kembali ke $v_i$. Diagonal itu membagi persegi menjadi
$f_{1i}$ dan $f_{2i}$. Persegi-persegi berlanjut untuk semua
$i\in\mathbb Z$; garis bertitik pada gambar sumber hanya menandakan kelanjutan
tak hingga. Tabel di atas, bukan letak atau arah visual panah, adalah data
yang menentukan objek.
:::

Ada pemetaan ke torus kombinatorik $T_\bullet$ dari Unit 20,

$$
q\colon C_\bullet\longrightarrow T_\bullet,
\qquad
v_i\longmapsto v,\qquad
e_{ai}\longmapsto e_a,\qquad
f_{bi}\longmapsto f_b,
$$

dengan $a=1,2,3$ dan $b=1,2$.
:::

::: {.source-audit #o012-rbt-l22-audit-002}
**Audit sumber 22.2.** Gambar pada Notes.tex baris 4543--4594 direflow menjadi
Diagram 22.1 dengan seluruh arah dan indeks tertulis. Baris 4598 mengatakan
bahwa *face map* silinder dapat direkonstruksi hanya dari definisi pemetaan
$q$. Sebenarnya $q$ sendiri tidak menentukan pilihan lift berindeks; tabel
di atas merekam lift periodik yang ditentukan oleh diagram dan yang membuat
$q$ sebuah pemetaan permukaan kombinatorik.
:::

::: {.lemma #o012-rbt-l22-lem-001}
**Lema 22.1 (realisasi bersifat fungtorial dalam dimensi dua).** Sebuah
pemetaan $f\colon X_\bullet\to Y_\bullet$ antara permukaan kombinatorik
menginduksi pemetaan kontinu

$$
|f|\colon|X_\bullet|\longrightarrow|Y_\bullet|,
$$

dan konstruksi ini melestarikan identitas serta komposisi.
:::

::: {.proof #o012-rbt-l22-proof-001}
**Bukti.** Pada ruang sebelum hasil bagi, definisikan

$$
\widetilde{|f|}:=
\bigsqcup_{n=0}^{2}
(f_n\times\operatorname{id}_{\Delta^n})
\colon
\bigsqcup_{n=0}^{2}\operatorname{disc}(X_n)\times\Delta^n
\longrightarrow
\bigsqcup_{n=0}^{2}\operatorname{disc}(Y_n)\times\Delta^n.
$$

Ambil $x\in X_n$, $\mathbf v\in\Delta^{n-1}$, $1\leq n\leq2$, dan
$0\leq i\leq n$. Relasi pada realisasi domain dan kodomain memberi

$$
\begin{aligned}
\widetilde{|f|}(x,\partial_i\mathbf v)
&=(f_n(x),\partial_i\mathbf v)\\
&\sim(d_{i,Y}^nf_n(x),\mathbf v)\\
&=(f_{n-1}d_{i,X}^n(x),\mathbf v)\\
&=\widetilde{|f|}(d_{i,X}^n(x),\mathbf v).
\end{aligned}
$$

Jadi $\widetilde{|f|}$ konstan pada kelas-kelas relasi pembangkit dan, oleh
sifat universal hasil bagi, turun secara unik menjadi $|f|$.

::: {.figure #o012-rbt-l22-fig-002 data-source-format="xypic"}
**Diagram 22.2 (kuadrat hasil bagi yang komutatif).** Jika $Q_X$ dan $Q_Y$
menyatakan dua koproduk sebelum hasil bagi, hubungan empat pemetaan adalah

$$
\begin{array}{ccc}
Q_X&\xrightarrow{\ \widetilde{|f|}\ }&Q_Y\\
\big\downarrow&&\big\downarrow\\
|X_\bullet|&\xrightarrow{\ |f|\ }&|Y_\bullet|.
\end{array}
$$

Kedua lintasan dari $Q_X$ ke $|Y_\bullet|$ sama. Panah vertikal adalah
pemetaan hasil bagi; posisi panah tidak menambahkan asumsi apa pun.
:::

Untuk pemetaan identitas, pemetaan pada setiap komponen sebelum hasil bagi
adalah identitas, sehingga keunikan memberi
$|\operatorname{id}|=\operatorname{id}$. Untuk pasangan yang dapat
dikomposisikan
$X_\bullet\xrightarrow{f}Y_\bullet\xrightarrow{g}Z_\bullet$, kedua pemetaan
$|g\circ f|$ dan $|g|\circ|f|$ mempunyai lift komponen-demi-komponen yang sama,
maka keunikan memberi

$$
|g\circ f|=|g|\circ|f|.
$$

Dengan demikian konstruksi itu fungtorial. $\square$
:::

::: {.source-audit #o012-rbt-l22-audit-003}
**Audit sumber 22.3.** Notes.tex baris 4608--4632 mengetik ulang pemetaan
prahasil-bagi secara ambigu sebagai `: =` dan menyimpulkan fungtorialitas
hanya dari komposisi. Edisi menulis domain, indeks, dan relasi secara lengkap,
lalu memeriksa identitas dan komposisi. Kuadrat Xy-pic sumber diganti oleh
Diagram 22.2 yang menyatakan komutativitasnya secara linear.
:::

Untuk Contoh 22.4, sumber menyatakan identifikasi geometrik standar

$$
|C_\bullet|\cong\mathbb R\times S^1,
\qquad
|T_\bullet|\cong S^1\times S^1.
$$

Di bawah identifikasi itu, $|q|$ adalah

$$
\exp\times\operatorname{id}
\colon\mathbb R\times S^1\longrightarrow S^1\times S^1,
\qquad
\exp(t)=e^{2\pi i t}.
$$

Sumber tidak membuktikan homeomorfisma silinder tersebut di rentang ini;
edisi mempertahankannya sebagai fakta geometrik standar dan menguji data
kombinatoriknya dalam Pemeriksaan Penguasaan 22.1.

Jika ruang topologis $\Sigma$ ditriangulasi oleh
$\Sigma\cong|X_\bullet|$, kita mungkin mencoba mendefinisikan
$H^n(\Sigma;R):=H^n(X_\bullet;R)$. Ini definisi yang buruk untuk ruang tanpa
triangulasi terpilih: belum ada jaminan bahwa pilihan triangulasi berbeda
memberi modul yang sama, dan hanya pemetaan kontinu yang direalisasikan oleh
pemetaan kombinatorik yang menghasilkan pemetaan kohomologi dengan cara ini.

::: {.source-margin #o012-rbt-l22-margin-002}
> **Catatan pinggir sumber.** Fungtorialitas modul kohomologi terhadap
> pemetaan permukaan kombinatorik akan tercakup oleh definisi yang diberikan
> kemudian. Catatan ini bukan klaim bahwa semua pemetaan kontinu sudah
> ditangani oleh model dua dimensi tersebut.
:::

Kita juga tidak ingin membatasi topologi pada permukaan. Definisi berikut
memperluas data kombinatorik ke semua dimensi.

## Himpunan-Delta dan kerangka {#o012-rbt-l22-s02}

::: {.definition #o012-rbt-l22-def-002}
**Definisi 22.2 (himpunan-$\Delta$).** Sebuah *himpunan-$\Delta$* adalah
barisan himpunan

$$
X_0,X_1,X_2,\ldots
$$

yang elemennya disebut simpleks-$n$, bersama *face map*

$$
d_i^n\colon X_n\longrightarrow X_{n-1}
\qquad(n>0,\ 0\leq i\leq n),
$$

yang memenuhi identitas muka

$$
d_i^{n-1}\circ d_j^n
=d_{j-1}^{n-1}\circ d_i^n
\qquad(0\leq i<j\leq n).
$$

Superskrip boleh dihilangkan bila dimensinya dapat dibaca dari domain dan
kodomain.
:::

::: {.example #o012-rbt-l22-exa-005}
**Contoh 22.5 (simpleks kombinatorik $\Delta[n]$).** Tuliskan

$$
\mathbf{n+1}:=\{0,1,\ldots,n\}.
$$

Simpleks kombinatorik $\Delta[n]$ mempunyai

$$
\Delta[n]_k=
\begin{cases}
\displaystyle\binom{\mathbf{n+1}}{k+1},&0\leq k\leq n,\\[4pt]
\varnothing,&k>n,
\end{cases}
$$

di mana $\binom{\mathbf{n+1}}{k+1}$ adalah himpunan semua subhimpunan
beranggota $k+1$. Khususnya,

$$
\Delta[n]_0=\mathbf{n+1},
\qquad
\Delta[n]_n=\{\mathbf{n+1}\}.
$$

Setiap subhimpunan diberi urutan warisan dari
$0<1<\cdots<n$. Pemetaan

$$
d_i^k\colon
\binom{\mathbf{n+1}}{k+1}
\longrightarrow
\binom{\mathbf{n+1}}{k}
$$

menghapus elemen ke-$i$, dengan indeks dimulai dari $0$.
:::

::: {.example #o012-rbt-l22-exa-006}
**Contoh 22.6 (batas simpleks kombinatorik).** Batas
$\partial\Delta[n]$ didefinisikan oleh

$$
\partial\Delta[n]_k=
\begin{cases}
\Delta[n]_k,&k<n,\\
\varnothing,&k\geq n.
\end{cases}
$$

Jadi $\partial\Delta[3]$ mempunyai simpul, sisi, dan segitiga, tetapi tidak
mempunyai simpleks tiga dimensi yang mengisi batas itu.
:::

Untuk setiap himpunan-$\Delta$ $X_\bullet$ dan $m\geq0$, *$m$-kerangka*
$\operatorname{sk}_mX_\bullet$ diberikan oleh

$$
(\operatorname{sk}_mX_\bullet)_k=
\begin{cases}
X_k,&k\leq m,\\
\varnothing,&k>m.
\end{cases}
$$

Jika $X_n\ne\varnothing$, maka penerapan *face map* menunjukkan
$X_m\ne\varnothing$ untuk setiap $0\leq m<n$. Himpunan-$\Delta$ takkosong
disebut berdimensi $n$ bila $n$ adalah bilangan bulat terbesar dengan
$X_n\ne\varnothing$, dan disebut berdimensi tak hingga bila
$X_n\ne\varnothing$ untuk bilangan $n$ yang tak berbatas. Himpunan-$\Delta$
kosong tidak dimasukkan ke salah satu dari dua kasus itu; jika diperlukan,
dimensinya dapat dikonvensikan sebagai $-1$.

Jika $X_\bullet$ berdimensi $n$ dan $0\leq m<n$, atau bila ia berdimensi tak
hingga, maka $\operatorname{sk}_mX_\bullet$ berdimensi $m$. Jadi
$\Delta[n]$ berdimensi $n$ dan

$$
\partial\Delta[n]=\operatorname{sk}_{n-1}\Delta[n]
$$

berdimensi $n-1$. Permukaan kombinatorik dari Unit 20 adalah
himpunan-$\Delta$ berdimensi paling tinggi dua.

::: {.source-audit #o012-rbt-l22-audit-004}
**Audit sumber 22.4.** Notes.tex baris 4693--4695 menyebut objek berdimensi
tak hingga bila tidak ada dimensi terbesar. Secara literal itu juga mencakup
objek kosong, yang tidak mempunyai simpleks pada dimensi mana pun. Edisi
membedakan kasus kosong dari kasus dimensi yang tak berbatas. Salah eja
`defintitions` pada baris 4700 juga dinormalisasi dalam terjemahan.
:::

## Realisasi dan triangulasi dalam semua dimensi {#o012-rbt-l22-s03}

::: {.definition #o012-rbt-l22-def-003}
**Definisi 22.3 (realisasi geometrik umum).** Realisasi geometrik sebuah
himpunan-$\Delta$ $X_\bullet$ adalah ruang hasil bagi

$$
|X_\bullet|:=
\left(
\bigsqcup_{n=0}^{\infty}
\operatorname{disc}(X_n)\times\Delta^n
\right)\Big/\!\sim,
$$

dengan relasi yang dibangkitkan oleh

$$
(d_i^n(x),\mathbf v)\sim(x,\partial_i\mathbf v),
$$

untuk

$$
x\in X_n,
\qquad
\mathbf v\in\Delta^{n-1},
\qquad
n\geq1,
\qquad
0\leq i\leq n.
$$
:::

::: {.definition #o012-rbt-l22-def-004}
**Definisi 22.4 (pemetaan himpunan-$\Delta$).** Sebuah pemetaan
$f\colon X_\bullet\to Y_\bullet$ adalah barisan fungsi

$$
f_n\colon X_n\longrightarrow Y_n
\qquad(n=0,1,2,\ldots)
$$

yang memenuhi

$$
d_{i,Y}^n\circ f_n
=f_{n-1}\circ d_{i,X}^n
\qquad(n>0,\ 0\leq i\leq n).
$$

Himpunan-$\Delta$ dan pemetaannya membentuk kategori
$\Delta\mathbf{Set}$.
:::

::: {.source-audit #o012-rbt-l22-audit-005}
**Audit sumber 22.5.** Notes.tex baris 4708 dan 4714 tidak menyatakan tipe
variabel pada relasi realisasi dan memakai simbol $d_i^n$ yang sama untuk
domain serta kodomain persamaan morfisma. Edisi memberi semua rentang indeks
dan subskrip $X,Y$, sehingga kedua persamaan dapat diperiksa tipenya.
:::

::: {.example #o012-rbt-l22-exa-007}
**Contoh 22.7 (inklusi kerangka dan kealamian).** Selalu ada inklusi

$$
\operatorname{sk}_mX_\bullet\hookrightarrow X_\bullet,
$$

dan untuk $0\leq m\leq\ell$ ada inklusi
$\operatorname{sk}_mX_\bullet\hookrightarrow\operatorname{sk}_\ell X_\bullet$.

::: {.source-margin #o012-rbt-l22-margin-003}
> **Catatan pinggir sumber.** Sumber menaruh segitiga Xy-pic berikut di margin
> untuk menyatakan bahwa inklusi langsung sama dengan komposit dua inklusi.
> Hubungan itu dipusatkan di bawah agar urutan komposisinya terbaca.
:::

::: {.figure #o012-rbt-l22-fig-003 data-source-format="xypic"}
**Diagram 22.3 (segitiga inklusi kerangka).** Untuk $m\leq\ell$, diagram

$$
\begin{array}{ccc}
\operatorname{sk}_mX_\bullet
&\lhook\joinrel\longrightarrow&
\operatorname{sk}_\ell X_\bullet\\
&\searrow&\big\downarrow\\
&&X_\bullet
\end{array}
$$

komutatif: panah diagonal adalah inklusi langsung dan sama dengan komposit
panah mendatar lalu vertikal.
:::

Inklusi kerangka juga alami. Untuk
$f\colon X_\bullet\to Y_\bullet$, kuadrat berikut komutatif.

::: {.figure #o012-rbt-l22-fig-004 data-source-format="xypic"}
**Diagram 22.4 (kealamian kerangka).** Hubungannya ialah

$$
\begin{array}{ccc}
\operatorname{sk}_mX_\bullet
&\xrightarrow{\ \operatorname{sk}_m f\ }&
\operatorname{sk}_mY_\bullet\\
\big\downarrow&&\big\downarrow\\
X_\bullet&\xrightarrow{\ f\ }&Y_\bullet.
\end{array}
$$

Kedua komposit pada setiap simpleks berdimensi paling tinggi $m$ sama dengan
$f$, dan pada derajat lebih tinggi domain kerangka kosong.
:::
:::

::: {.example #o012-rbt-l22-exa-008 data-source-label="eg:name_of_simplex"}
**Contoh 22.8 (pemetaan nama simpleks).** Untuk setiap
$x\in X_n$ terdapat pemetaan tunggal

$$
\ulcorner x\urcorner\colon\Delta[n]\longrightarrow X_\bullet
$$

yang mengirim muka puncak unik $\mathbf{n+1}$ ke $x$. Semua nilai pada muka
yang lebih rendah dipaksa oleh identitas *face map*. Seperti pada Contoh 22.2,
pemetaan nama ini tidak harus injektif.
:::

Lebih umum, misalkan $Y_n\subseteq X_n$ untuk semua $n$ dan semua *face map*
$X_\bullet$ membatasi ke fungsi
$d_i^n\colon Y_n\to Y_{n-1}$. Maka $Y_\bullet$ adalah sub-himpunan-$\Delta$
dan terdapat inklusi $Y_\bullet\hookrightarrow X_\bullet$. Jika
$X_\bullet$ berdimensi $k$, setiap pilihan $Y_k\subseteq X_k$ menghasilkan
sub-himpunan-$\Delta$ terkecil yang memuatnya: ambil semua citra muka di
derajat $k-1$, lalu semua muka dari citra itu, dan teruskan hingga derajat
nol; pada derajat di atas $k$ ambil himpunan kosong.

::: {.lemma #o012-rbt-l22-lem-002 data-proof-status="source-refers-to-lemma-22.1"}
**Lema 22.2 (fungtor realisasi geometrik).** Realisasi geometrik mendefinisikan
fungtor

$$
|-|\colon\Delta\mathbf{Set}\longrightarrow\mathbf{Top}.
$$
:::

**Justifikasi.** Sumber tidak memberi bukti baru setelah pernyataan ini.
Konstruksi dan bukti Lema 22.1 berlaku tanpa perubahan pada koproduk
$n=0,1,2,\ldots$: gunakan
$\bigsqcup_{n\geq0}(f_n\times\operatorname{id}_{\Delta^n})$, periksa relasi
pada setiap $n$, lalu gunakan keunikan pemetaan hasil bagi untuk identitas dan
komposisi. Dengan demikian lema ini tidak dibiarkan sebagai kotak hitam,
walaupun tidak ditambah lingkungan bukti sumber baru.

::: {.definition #o012-rbt-l22-def-005}
**Definisi 22.5 (triangulasi ruang topologis).** Triangulasi ruang topologis
$Z$ adalah himpunan-$\Delta$ $X_\bullet$ yang dilengkapi homeomorfisma

$$
\tau\colon Z\xrightarrow{\ \cong\ }|X_\bullet|.
$$
:::

Realisasi $|X_\bullet|$ selalu ditriangulasi oleh $X_\bullet$ bersama
homeomorfisma identitas. Jika subruang $Y\subseteq Z$ sudah ditriangulasi oleh
$Y_\bullet$, dalam situasi yang baik triangulasi itu dapat diperluas dengan
mencari $X_\bullet$ yang memuat $Y_\bullet$ sebagai sub-himpunan-$\Delta$.

::: {.example #o012-rbt-l22-exa-009}
**Contoh 22.9 (simpleks topologis standar).** Simpleks topologis
$\Delta^n$ ditriangulasi oleh $\Delta[n]$. Untuk muka

$$
S=\{j_0<j_1<\cdots<j_k\}\in\Delta[n]_k,
$$

definisikan

$$
\lambda_S\colon\Delta^k\longrightarrow\Delta^n,
\qquad
(u_0,\ldots,u_k)\longmapsto(w_0,\ldots,w_n),
$$

dengan $w_{j_r}=u_r$ dan $w_j=0$ bila $j\notin S$. Pemetaan-pemetaan ini
kompatibel dengan semua relasi muka dan menginduksi homeomorfisma kanonik

$$
\Lambda_n\colon|\Delta[n]|\xrightarrow{\ \cong\ }\Delta^n.
$$

Komponen yang diindeks muka puncak $S=\mathbf{n+1}$ adalah identitas pada
$\Delta^n$; semua komponen lain dilekatkan tepat ke muka batas yang sama.
:::

::: {.source-audit #o012-rbt-l22-audit-006}
**Audit sumber 22.6.** Notes.tex baris 4765--4766 menulis sumber pemetaan
kanonik dengan $\operatorname{disc}(\Delta[k])$, padahal komponen derajat $k$
harus diindeks oleh $\Delta[n]_k$. Edisi menggantinya dengan pemetaan bertipe
$\lambda_S$ dan menyebut hasilnya homeomorfisma, bukan isomorfisma himpunan
yang tidak bertipe.
:::

## Triangulasi prisma {#o012-rbt-l22-s04}

Pertimbangkan $I\times\Delta^2$. Kedua ujung
$\{0\}\times\Delta^2$ dan $\{1\}\times\Delta^2$ ditriangulasi oleh
$\Delta[2]$. Namai simpul pada ujung pertama $0,1,2$ dan simpul pada ujung
kedua $\overline0,\overline1,\overline2$.

Ada himpunan-$\Delta$ $P_\bullet$ dengan tiga simpleks tiga dimensi berurutan

$$
\begin{aligned}
T_2&=[0,1,2,\overline2],\\
T_1&=[0,1,\overline1,\overline2],\\
T_0&=[0,\overline0,\overline1,\overline2].
\end{aligned}
$$

Simpleks dua dan satu dimensinya adalah semua subdaftar berurutan yang muncul
dari ketiga daftar itu, dan simpleks nolnya adalah keenam simpul.

::: {.source-margin #o012-rbt-l22-margin-004}
> **Catatan pinggir sumber.** Gambar TikZ sumber ditempatkan dua sentimeter
> lebih tinggi di margin dan memakai proyeksi perspektif. Diagram berikut
> menggantinya dengan data insidensi yang tidak bergantung pada proyeksi.
:::

::: {.figure #o012-rbt-l22-fig-005 data-source-format="tikz"}
**Diagram 22.5 (deskripsi semantik triangulasi prisma).** Prisma segitiga
mempunyai simpul bawah $0,1,2$ dan simpul atas
$\overline0,\overline1,\overline2$. Ia dibagi menjadi tetrahedron
$T_2,T_1,T_0$ di atas. Irisan $T_2\cap T_1$ adalah muka
$[0,1,\overline2]$, irisan $T_1\cap T_0$ adalah muka
$[0,\overline1,\overline2]$, dan irisan ketiganya adalah sisi
$[0,\overline2]$. Muka bawah $[0,1,2]$ dan muka atas
$[\overline0,\overline1,\overline2]$ tetap utuh. Garis yang tampak saling
menyilang pada gambar perspektif sumber bukan simpul tambahan.
:::

Secara umum, $I\times\Delta^n$ mempunyai triangulasi dengan $n+1$ simpleks
berdimensi $n+1$. Untuk $0\leq r\leq n$, muka puncaknya berlabel

$$
P_r=[0,1,\ldots,r,\overline r,
\overline{r+1},\ldots,\overline n].
$$

Sumber menuliskan daftar itu dari $r=n$ turun ke $r=0$. Urutan $n+2$ simpul
pada setiap $P_r$ adalah urutan yang tampil, sedangkan semua simpleks dimensi
lebih rendah diperoleh dengan menghapus satu atau beberapa elemen daftar
melalui *face map*.

## Kompleks korantai dan perubahan koefisien {#o012-rbt-l22-s05}

Untuk himpunan-$\Delta$ $X_\bullet$ dan gelanggang komutatif berunsur satu
$R$, tuliskan $R^{X_n}$ untuk modul **semua** fungsi $X_n\to R$. Jika
$X_n$ tak hingga, ini adalah produk salinan $R$, bukan jumlah langsung
berpenyangga hingga. Definisikan diferensial berderajat naik

$$
\cdots\longrightarrow R^{X_n}
\xrightarrow{\delta_n}R^{X_{n+1}}
\longrightarrow\cdots
$$

dengan, untuk $g\colon X_n\to R$,

$$
\delta_n(g)
=\sum_{i=0}^{n+1}(-1)^i g\circ d_i^{n+1}
\colon X_{n+1}\longrightarrow R.
$$

::: {.source-audit #o012-rbt-l22-audit-007}
**Audit sumber 22.7.** Notes.tex baris 4836 menjumlahkan hanya dari
$i=0$ sampai $n$. Simpleks berdimensi $n+1$ mempunyai $n+2$ muka, sehingga
batas atas yang benar ialah $n+1$. Dengan batas sumber, bahkan
$\delta_0g$ hanya memakai satu dari dua titik ujung sebuah sisi dan
$\delta_1\delta_0$ tidak nol pada umumnya. Edisi memperbaiki batas dan
menyelesaikan bukti yang ditinggalkan sebagai “Exercise!”.
:::

::: {.lemma #o012-rbt-l22-lem-003}
**Lema 22.3.** Barisan di atas adalah kompleks:

$$
\delta_{n+1}\circ\delta_n=0
\qquad(n\geq0).
$$
:::

::: {.proof #o012-rbt-l22-proof-002 data-source-proof="exercise-completed-in-edition"}
**Bukti.** Ambil $g\in R^{X_n}$ dan $x\in X_{n+2}$. Dengan rumus yang telah
dikoreksi,

$$
\begin{aligned}
(\delta_{n+1}\delta_ng)(x)
&=\sum_{j=0}^{n+2}\sum_{i=0}^{n+1}
(-1)^{i+j}
g\bigl(d_i^{n+1}d_j^{n+2}x\bigr)\\
&=\sum_{0\leq i<j\leq n+2}
\Bigl[
(-1)^{i+j}g(d_i d_jx)
+(-1)^{i+j-1}g(d_{j-1}d_ix)
\Bigr].
\end{aligned}
$$

Pada baris kedua, setiap pasangan penghapusan muka dikumpulkan dalam dua
urutan yang mungkin. Identitas himpunan-$\Delta$
$d_i d_j=d_{j-1}d_i$ untuk $i<j$ membuat dua suku dalam setiap kurung sama
besar dan berlawanan tanda. Semua suku berpasangan, sehingga jumlahnya nol.
$\square$
:::

Kompleks ini dinotasikan

$$
C^\bullet(X_\bullet;R)
$$

dan disebut **kompleks korantai simpleksial** dari $X_\bullet$.

Untuk fungsi himpunan $\alpha\colon A\to B$, prakomposisi memberi pemetaan
$R$-linear

$$
\alpha^*\colon R^B\longrightarrow R^A,
\qquad
g\longmapsto g\circ\alpha.
$$

Jika $\beta\colon B\to C$, maka

$$
\alpha^*\circ\beta^*=(\beta\circ\alpha)^*
\colon R^C\longrightarrow R^A.
$$

Jadi arah dan urutan komposisi berbalik. Secara kategoris, ini adalah fungtor

$$
R^{(-)}\colon\mathbf{Set}^{\mathrm{op}}
\longrightarrow\mathbf{Mod}_R,
$$

dengan $\mathrm{op}$ menandakan kategori lawan.

::: {.lemma #o012-rbt-l22-lem-004}
**Lema 22.4 (fungtor korantai).** Terdapat fungtor kontravarian

$$
C^\bullet(-;R)\colon
\Delta\mathbf{Set}^{\mathrm{op}}
\longrightarrow\mathbf{Cplx}_R.
$$
:::

::: {.proof #o012-rbt-l22-proof-003}
**Bukti.** Untuk $f\colon X_\bullet\to Y_\bullet$, prakomposisi memberi
$f_n^*\colon R^{Y_n}\to R^{X_n}$. Jika $g\in R^{Y_n}$ dan
$x\in X_{n+1}$, maka

$$
\begin{aligned}
(\delta_{n,X}f_n^*g)(x)
&=\sum_{i=0}^{n+1}(-1)^i
g\bigl(f_n(d_{i,X}^{n+1}x)\bigr)\\
&=\sum_{i=0}^{n+1}(-1)^i
g\bigl(d_{i,Y}^{n+1}(f_{n+1}x)\bigr)\\
&=(f_{n+1}^*\delta_{n,Y}g)(x).
\end{aligned}
$$

Jadi $f^*$ adalah morfisma kompleks. Identitas dan komposisi mengikuti dari
$\operatorname{id}^*=\operatorname{id}$ dan
$(g\circ f)^*=f^*\circ g^*$, sehingga arah fungtor memang berlawanan.
$\square$
:::

::: {.definition #o012-rbt-l22-def-006}
**Definisi 22.6 (kohomologi himpunan-$\Delta$).** Modul kohomologi ke-$n$
dengan koefisien dalam $R$ adalah

$$
H^n(X_\bullet;R)
:=H^n(C^\bullet(X_\bullet;R))
=\frac{\ker\delta_n}{\operatorname{im}\delta_{n-1}},
$$

dengan $\operatorname{im}\delta_{-1}=0$. Untuk setiap $n$, konstruksi ini
memberi fungtor

$$
H^n(-;R)\colon
\Delta\mathbf{Set}^{\mathrm{op}}
\longrightarrow\mathbf{Mod}_R.
$$
:::

Karena $R^\varnothing=0$, bila $X_\bullet$ berdimensi $n$ maka

$$
H^k(X_\bullet;R)=0
\qquad(k>n).
$$

Himpunan-$\Delta$ berdimensi tak hingga dapat mempunyai atau tidak mempunyai
kohomologi taknol dalam tak hingga banyak derajat.

Jika $R$ Noetherian dan $X_n$ berhingga, maka $R^{X_n}$ adalah modul bebas
berhingga dan $\ker\delta_n$ terbangkit hingga; akibatnya $H^n$ terbangkit
hingga. Khususnya, himpunan-$\Delta$ berhingga mempunyai kohomologi
terbangkit hingga untuk $R=\mathbb Z$, $\mathbb R$, atau $\mathbb Z/2$.

::: {.source-margin #o012-rbt-l22-margin-005}
> **Catatan pinggir sumber.** Sumber menyatakan versi lebih umum: cukup ada
> berhingga banyak simpleks pada dimensi $n$. Pernyataan itu benar untuk
> gelanggang Noetherian yang digunakan dalam kuliah. Tanpa hipotesis
> Noetherian, kernel submodul dari modul bebas berhingga tidak harus
> terbangkit hingga.
:::

::: {.remark #o012-rbt-l22-rem-001}
**Catatan 22.1 (gelanggang yang dipakai).** Dalam praktik, sumber hanya akan
memakai $R=\mathbb Z$, $\mathbb R$, dan $\mathbb Z/2$.
:::

::: {.remark #o012-rbt-l22-rem-002}
**Catatan 22.2 (perhitungan hingga dan tak hingga).** Jika sebuah
himpunan-$\Delta$ berhingga dan semua *face map* diberikan secara eksplisit,
menghitung kohomologinya adalah persoalan kombinatorika dan aljabar linear,
meskipun pekerjaannya dapat besar. Untuk objek tak berhingga—baik berdimensi
tak hingga maupun mempunyai tak hingga banyak simpleks pada suatu dimensi—
aljabar linear berhingga tidak lagi cukup. Hal ini akan penting ketika
kohomologi ruang topologis umum didefinisikan tanpa memilih
himpunan-$\Delta$.
:::

Misalkan $\alpha\colon R\to S$ adalah homomorfisma gelanggang. Untuk setiap
himpunan $A$, komposisi pasca memberi pemetaan $R$-linear

$$
R^A\longrightarrow S^A,
\qquad
g\longmapsto\alpha\circ g,
$$

di mana $S^A$ dipandang sebagai modul-$R$ melalui $\alpha$. Penerapan pada
setiap derajat kompleks **korantai simpleksial** menghasilkan lema berikut.

::: {.lemma #o012-rbt-l22-lem-005 data-proof-status="verified-in-prose"}
**Lema 22.5 (perubahan koefisien).** Homomorfisma gelanggang
$\alpha\colon R\to S$ menginduksi morfisma kompleks

$$
C^\bullet(X_\bullet;R)
\longrightarrow
C^\bullet(X_\bullet;S),
$$

dan, untuk $X_\bullet$ tetap, konstruksi ini fungtorial dalam $\alpha$.
:::

**Verifikasi.** Karena $\alpha$ aditif,

$$
\alpha\circ\delta_n(g)
=\sum_{i=0}^{n+1}(-1)^i
(\alpha\circ g)\circ d_i^{n+1}
=\delta_n(\alpha\circ g).
$$

Identitas dan komposisi homomorfisma gelanggang jelas dilestarikan. Dengan
demikian diperoleh pemetaan perubahan koefisien

$$
H^n(X_\bullet;R)
\longrightarrow
H^n(X_\bullet;S),
$$

yang $R$-linear bila kodomain dipandang sebagai modul-$R$ melalui $\alpha$.

::: {.source-audit #o012-rbt-l22-audit-008}
**Audit sumber 22.8.** Notes.tex baris 4879--4880 menghilangkan hipotesis
Noetherian dari klaim keterbangkitan hingga. Baris 4899 keliru menyebut
$C^\bullet(X_\bullet;R)$ sebagai kompleks korantai *singular*; kompleks yang
baru didefinisikan adalah kompleks korantai simpleksial. Edisi memperbaiki
keduanya dan mempertahankan semantik $R^A$ sebagai semua fungsi, yakni produk
bila $A$ tak hingga.
:::

::: {.example #o012-rbt-l22-exa-010}
**Contoh 22.10 (dari bilangan bulat ke bilangan real).** Inklusi
$\mathbb Z\hookrightarrow\mathbb R$ memberi pemetaan

$$
H^n(X_\bullet;\mathbb Z)
\longrightarrow
H^n(X_\bullet;\mathbb R).
$$

Jika $X_\bullet$ berhingga, domain adalah grup abelian terbangkit hingga,
kernel pemetaan ini tepat subgrup torsinya, dan citra bagian bebasnya adalah
kisi penuh di ruang vektor real $H^n(X_\bullet;\mathbb R)$. Tanpa hipotesis
keterhinggaan, pemetaan perubahan koefisien tetap ada, tetapi pernyataan kisi
dan identifikasi kernel itu tidak dinyatakan di sini.
:::

::: {.source-audit #o012-rbt-l22-audit-009}
**Audit sumber 22.9.** Notes.tex baris 4911--4916 menyatakan klaim kernel dan
kisi untuk setiap himpunan-$\Delta$. Argumen standar memakai kompleks
korantai bebas berhingga dan struktur grup abelian terbangkit hingga. Edisi
membatasi kesimpulan itu pada $X_\bullet$ berhingga; pada kasus umum hanya
pemetaan alaminya yang dipertahankan tanpa klaim kisi.
:::

::: {.example #o012-rbt-l22-exa-011}
**Contoh 22.11 (reduksi modulo prima).** Untuk prima $p$, proyeksi
$\mathbb Z\to\mathbb Z/p=\mathbb F_p$ memberi

$$
H^n(X_\bullet;\mathbb Z)
\longrightarrow
H^n(X_\bullet;\mathbb F_p).
$$

Kodomain adalah ruang vektor atas $\mathbb F_p$. Setiap kelas torsi yang
ordenya relatif prima terhadap $p$ dipetakan ke nol. Pernyataan ini tidak
mengatakan bahwa semua torsi-$p$ pasti terdeteksi; kohomologi modulo $p$ juga
dapat mempunyai kelas tambahan.
:::

::: {.remark #o012-rbt-l22-rem-003}
**Catatan 22.3 (bilangan Betti dan koefisien torsi).** Sumber mencatat bahwa
pada masa awal topologi aljabar, perhatian banyak diberikan pada kompleks
hingga. Dimensi ruang vektor $H^n(X_\bullet;\mathbb R)$ disebut **bilangan
Betti**, sedangkan orde faktor siklik dalam
$H^n(X_\bullet;\mathbb Z)_{\mathrm{tors}}$ disebut **koefisien torsi**.
Angka-angka itu mengemas informasi numerik—bilangan Betti khususnya memasuki
karakteristik Euler—tetapi tidak membawa pemetaan yang diinduksi secara
fungtorial. Sumber mengaitkan pergeseran penekanan menuju invarian yang
sendiri merupakan objek aljabar dengan Emmy Noether dan matematikawan lain
pada dasawarsa 1920-an.
:::

::: {.source-audit #o012-rbt-l22-audit-010}
**Audit sumber 22.10.** Edisi menormalkan salah eja atau tata bahasa
deterministik pada Notes.tex baris 4512, 4529, 4532, 4598, 4700, 4747, 4765,
4815, 4887, dan 4890 (`map`, `cyclicly`, `singe`, `defintion`,
`defintitions`, `relisation`, `combinatrial`, `visualised`, `calulate`, dan
`an` sebelum $\Delta$-*set*) tanpa mengubah urutan sumber.
:::

# Pendamping penguasaan: pemeriksaan, petunjuk, dan solusi lengkap {.unnumbered #o012-rbt-l22-mastery}

Enam paket berikut adalah materi asli edisi. Semuanya dibatasi pada sasaran
Unit 22: pemetaan dan realisasi, data silinder tak hingga, simpleks serta
kerangka, triangulasi prisma, diferensial korantai, kontravariansi, dan
perubahan koefisien.

::: {.exercise #o012-rbt-l22-mcheck-001 data-origin="edition-original"}
**Pemeriksaan Penguasaan 22.1 (silinder menuju torus).** Untuk tabel *face
map* Contoh 22.4, periksa ketiga identitas muka pada $f_{1i}$ dan $f_{2i}$.
Kemudian buktikan bahwa $q(v_i)=v$, $q(e_{ai})=e_a$, dan
$q(f_{bi})=f_b$ mendefinisikan pemetaan ke torus kombinatorik Unit 20.
:::

::: {.hint #o012-rbt-l22-hint-001 data-origin="edition-original"}
**Petunjuk.** Gunakan tiga identitas permukaan dari Unit 20. Untuk $f_{2i}$,
ingat bahwa muka tengahnya adalah $e_{1,i+1}$. Setelah itu bandingkan setiap
baris tabel muka dengan baris $f_1,f_2$ pada torus.
:::

::: {.solution #o012-rbt-l22-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 22.1.** Untuk $f_{1i}$, tiga identitas memberi

$$
\begin{aligned}
d_0d_2(f_{1i})&=d_0(e_{2i})=v_{i+1}
=d_1(e_{3i})=d_1d_0(f_{1i}),\\
d_0d_1(f_{1i})&=d_0(e_{1i})=v_i
=d_0(e_{3i})=d_0d_0(f_{1i}),\\
d_1d_2(f_{1i})&=d_1(e_{2i})=v_i
=d_1(e_{1i})=d_1d_1(f_{1i}).
\end{aligned}
$$

Untuk $f_{2i}$,

$$
\begin{aligned}
d_0d_2(f_{2i})&=d_0(e_{3i})=v_i
=d_1(e_{2i})=d_1d_0(f_{2i}),\\
d_0d_1(f_{2i})&=d_0(e_{1,i+1})=v_{i+1}
=d_0(e_{2i})=d_0d_0(f_{2i}),\\
d_1d_2(f_{2i})&=d_1(e_{3i})=v_{i+1}
=d_1(e_{1,i+1})=d_1d_1(f_{2i}).
\end{aligned}
$$

Jadi $C_\bullet$ adalah permukaan kombinatorik. Pada derajat satu, kedua
titik ujung setiap $e_{ai}$ dipetakan ke $v$, sama dengan kedua titik ujung
$e_a$. Pada derajat dua, tabel muka menjadi

$$
f_1\mapsto(e_3,e_1,e_2),
\qquad
f_2\mapsto(e_2,e_1,e_3),
$$

tepat seperti tabel torus. Maka $q$ komutatif dengan semua *face map* dan
merupakan pemetaan permukaan kombinatorik. Lema 22.1 menghasilkan pemetaan
kontinu $|q|$; di bawah model geometrik standar, koordinat strip
$\mathbb R$ direduksi modulo $\mathbb Z$, sehingga
$|q|=\exp\times\operatorname{id}$.
:::

::: {.exercise #o012-rbt-l22-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 22.2 (simpleks, batas, dan pemetaan nama).** Hitung
banyak simpleks pada setiap derajat $\Delta[3]$ dan
$\partial\Delta[3]$. Untuk $x\in X_3$, bangun
$\ulcorner x\urcorner\colon\Delta[3]\to X_\bullet$ dan jelaskan kapan
pemetaan itu gagal menjadi injektif.
:::

::: {.hint #o012-rbt-l22-hint-002 data-origin="edition-original"}
**Petunjuk.** Gunakan $\binom4{k+1}$. Nilai pemetaan nama pada subhimpunan
$\{j_0<\cdots<j_k\}$ diperoleh dengan menghapus dari $x$ semua indeks yang
tidak muncul, dalam urutan yang konsisten dengan identitas muka.
:::

::: {.solution #o012-rbt-l22-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 22.2.** Karena
$|\Delta[3]_k|=\binom4{k+1}$ untuk $0\leq k\leq3$, jumlahnya adalah

$$
\begin{array}{c|ccccc}
k&0&1&2&3&k>3\\ \hline
|\Delta[3]_k|&4&6&4&1&0,\\
|\partial\Delta[3]_k|&4&6&4&0&0.
\end{array}
$$

Tetapkan muka puncak ke $x$. Untuk setiap muka kodimensi satu, syarat
komutativitas memaksa nilainya menjadi $d_i(x)$; pada kodimensi dua nilainya
menjadi komposit dua *face map*, dan seterusnya. Identitas muka menjamin bahwa
dua urutan penghapusan yang menghasilkan subhimpunan sama memberi hasil yang
sama. Karena itu pemetaan nama ada dan tunggal.

Namun dua muka berbeda dari $x$ dapat sama, misalnya
$d_i(x)=d_j(x)$ untuk $i\ne j$, atau identifikasi dapat terjadi pada derajat
lebih rendah. Dalam keadaan itu dua simpleks berbeda pada $\Delta[3]$
memiliki citra sama, sehingga $\ulcorner x\urcorner$ tidak injektif. Jadi kata
“nama” lebih tepat daripada “inklusi” tanpa hipotesis tambahan.
:::

::: {.exercise #o012-rbt-l22-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 22.3 (mengapa tiga tetrahedron mengisi prisma).**
Petakan simpul $j$ ke $(0,e_j)$ dan $\overline j$ ke $(1,e_j)$ dalam
$I\times\Delta^2$. Buktikan bahwa citra afin $T_2,T_1,T_0$ menutupi prisma,
dan tentukan irisan berpasangannya.
:::

::: {.hint #o012-rbt-l22-hint-003 data-origin="edition-original"}
**Petunjuk.** Untuk $(t;x_0,x_1,x_2)$ dengan $x_0+x_1+x_2=1$, bandingkan
$t$ berturut-turut dengan $x_2$ dan $x_1+x_2$. Citra $T_r$ dicirikan oleh
$\sum_{j>r}x_j\leq t\leq\sum_{j\geq r}x_j$.
:::

::: {.solution #o012-rbt-l22-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 22.3.** Pada $T_r$, tulis koefisien barisentris simpul
bawah sebagai $a_j$ untuk $j\leq r$ dan simpul atas sebagai $b_j$ untuk
$j\geq r$. Pemetaan afin memberi

$$
t=\sum_{j\geq r}b_j,
\qquad
x_j=
\begin{cases}
a_j,&j<r,\\
a_r+b_r,&j=r,\\
b_j,&j>r.
\end{cases}
$$

Koefisien taknegatif seperti itu ada tepat bila

$$
\sum_{j>r}x_j\leq t\leq\sum_{j\geq r}x_j.
$$

Untuk $n=2$, ketiga selang itu adalah

$$
0\leq t\leq x_2,
\qquad
x_2\leq t\leq x_1+x_2,
\qquad
x_1+x_2\leq t\leq1.
$$

Selang-selang tersebut menutupi $[0,1]$ untuk setiap titik
$(x_0,x_1,x_2)\in\Delta^2$, maka ketiga tetrahedron menutupi prisma. Kesamaan
$t=x_2$ memberi muka bersama
$T_2\cap T_1=[0,1,\overline2]$, sedangkan
$t=x_1+x_2$ memberi
$T_1\cap T_0=[0,\overline1,\overline2]$. Irisan
$T_2\cap T_0=[0,\overline2]$ adalah sisi yang juga menjadi irisan ketiganya.
Jadi pelekatan terjadi sepanjang muka penuh dan benar-benar merupakan
triangulasi.
:::

::: {.exercise #o012-rbt-l22-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 22.4 (diferensial pada satu segitiga).** Untuk
$\Delta[2]$, tulis $\delta_0\colon R^{X_0}\to R^{X_1}$ dan
$\delta_1\colon R^{X_1}\to R^{X_2}$ secara eksplisit, lalu verifikasi
$\delta_1\delta_0=0$. Jelaskan mengapa batas atas $n+1$ pada rumus umum
tidak dapat diganti oleh $n$.
:::

::: {.hint #o012-rbt-l22-hint-004 data-origin="edition-original"}
**Petunjuk.** Orientasikan sisi $[a,b]$ dengan $a<b$. Muka segitiga
$[0,1,2]$ adalah $[1,2]$, $[0,2]$, dan $[0,1]$ dengan tanda berganti.
:::

::: {.solution #o012-rbt-l22-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 22.4.** Untuk $g\in R^{X_0}$,

$$
(\delta_0g)([a,b])=g(b)-g(a),
$$

karena $d_0[a,b]=[b]$ dan $d_1[a,b]=[a]$. Untuk
$h\in R^{X_1}$,

$$
(\delta_1h)([0,1,2])
=h([1,2])-h([0,2])+h([0,1]).
$$

Karena itu

$$
\begin{aligned}
(\delta_1\delta_0g)([0,1,2])
&=(g(2)-g(1))-(g(2)-g(0))+(g(1)-g(0))\\
&=0.
\end{aligned}
$$

Pada derajat nol, simpleks satu dimensi mempunyai dua *face map* $d_0,d_1$.
Jumlah sampai $n=0$ hanya akan memberi $g\circ d_0$, bukan selisih titik
ujung. Jadi ia bukan diferensial graf yang telah dipakai dan komposisi
berikutnya tidak akan mengalami pembatalan berpasangan.
:::

::: {.exercise #o012-rbt-l22-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 22.5 (kontravariansi pada poligon).** Misalkan
$P_m$ adalah poligon dengan $m\geq2$ sisi yang semuanya berorientasi siklik,
dan $c\colon P_m\to L_\bullet$ mengirim semua simpul ke satu simpul serta
semua sisi ke satu gelang. Hitung pemetaan

$$
c^*\colon H^0(L_\bullet;R)\to H^0(P_m;R),
\qquad
c^*\colon H^1(L_\bullet;R)\to H^1(P_m;R).
$$
:::

::: {.hint #o012-rbt-l22-hint-005 data-origin="edition-original"}
**Petunjuk.** Pada korantai derajat nol dan satu, prakomposisi mengirim satu
nilai ke fungsi konstan pada $m$ simpul atau $m$ sisi. Identifikasikan
$H^1(P_m;R)$ melalui jumlah nilai pada seluruh sisi berorientasi.
:::

::: {.solution #o012-rbt-l22-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 22.5.** Untuk $L_\bullet$, kompleksnya adalah

$$
0\longrightarrow R\xrightarrow{0}R\longrightarrow0,
$$

sehingga $H^0(L;R)\cong R\cong H^1(L;R)$. Untuk $P_m$, kernel diferensial
insidensi pada derajat nol terdiri atas fungsi konstan, jadi
$H^0(P_m;R)\cong R$. Prakomposisi oleh $c_0$ mengirim $a\in R$ ke fungsi
konstan bernilai $a$, sehingga pemetaan pada $H^0$ adalah identitas di bawah
identifikasi tersebut.

Pada derajat satu, $c_1^*$ mengirim $b\in R$ ke vektor konstan
$(b,\ldots,b)\in R^m$. Fungsi

$$
\sigma\colon R^m\longrightarrow R,
\qquad
(y_0,\ldots,y_{m-1})\longmapsto\sum_{j=0}^{m-1}y_j
$$

lenyap pada citra diferensial insidensi karena jumlahnya berteleskop, dan
menginduksi isomorfisma $H^1(P_m;R)\cong R$. Maka

$$
\sigma(c_1^*b)=mb.
$$

Jadi pemetaan pada $H^1$ adalah perkalian dengan $m$. Arah pemetaan
kohomologi berlawanan dengan $c$, sesuai fungtor
$H^1(-;R)$ yang kontravarian.
:::

::: {.exercise #o012-rbt-l22-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 22.6 (perubahan koefisien dan hipotesis hingga).**
Misalkan $X_\bullet$ berhingga dan

$$
H^n(X_\bullet;\mathbb Z)\cong\mathbb Z^b\oplus T
$$

dengan $T$ berhingga. Tentukan kernel dan citra pemetaan ke koefisien real.
Kemudian buktikan bahwa reduksi modulo prima $p$ membunuh bagian torsi yang
ordenya relatif prima terhadap $p$, dan jelaskan mengapa kesimpulan “kisi”
memerlukan hipotesis keterhinggaan.
:::

::: {.hint #o012-rbt-l22-hint-006 data-origin="edition-original"}
**Petunjuk.** Untuk kompleks korantai bebas berhingga, perluasan skalar ke
$\mathbb R$ bersifat datar. Untuk torsi-$q$ dengan $q$ relatif prima terhadap
$p$, gunakan identitas Bézout pada grup aditif ruang vektor
$\mathbb F_p$, yang dibunuh oleh $p$.
:::

::: {.solution #o012-rbt-l22-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 22.6.** Karena setiap grup korantai integral berderajat
hingga bebas dengan rank berhingga dan $\mathbb R$ datar atas $\mathbb Z$,

$$
H^n(X;\mathbb R)
\cong H^n(X;\mathbb Z)\otimes_{\mathbb Z}\mathbb R
\cong\mathbb R^b.
$$

Pemetaan perubahan koefisien adalah $x\mapsto x\otimes1$. Ia membunuh tepat
$T$ dan mengirim $\mathbb Z^b$ ke kisi standar
$\mathbb Z^b\subset\mathbb R^b$. Jadi kernelnya $T$ dan citranya kisi penuh.

Sekarang ambil kelas $x$ berorde $q^r$ dengan $\gcd(q,p)=1$, dan tulis
$\overline x$ untuk citranya di grup aditif
$H^n(X;\mathbb F_p)$. Kita mempunyai

$$
q^r\overline x=0,
\qquad
p\overline x=0.
$$

Ada $a,b\in\mathbb Z$ dengan $aq^r+bp=1$, sehingga

$$
\overline x=(aq^r+bp)\overline x=0.
$$

Argumen ini tidak menyatakan apa yang terjadi pada torsi-$p$, dan tidak
menghitung kelas modulo $p$ yang mungkin datang dari derajat berikutnya.
Terakhir, bila $X_\bullet$ tak hingga, grup kohomologi integral dapat tidak
terbangkit hingga dan citra di ruang vektor real tidak perlu merupakan kisi
diskret ber-rank hingga. Karena itu kesimpulan kisi pada Contoh 22.10 memang
memerlukan hipotesis keterhinggaan.
:::

::: {.boundary #o012-rbt-l22-boundary-001}
**Batas ke Unit 23.** Notes.tex baris 4939 memulai Kuliah 23 dengan kembali
ke fungtorialitas terhadap pemetaan himpunan-$\Delta$ dan pemetaan nama
$\ulcorner x\urcorner$. Tidak ada lingkungan sumber yang terbelah pada batas
ini. Kursor sumber berikutnya yang aman adalah baris 4939.
:::
