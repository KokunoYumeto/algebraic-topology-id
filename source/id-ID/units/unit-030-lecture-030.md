---
title: "Topologi Aljabar"
subtitle: "Unit 30: Titik Tetap, Teorema Dasar Aljabar, dan Medan Vektor pada Sfera"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l30-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 6271--6368 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L6271-L6368)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang aktif terdiri atas 98 baris fisik. Dengan normalisasi LF dan satu
terminator LF penutup dipertahankan, ukurannya 8.290 byte dan SHA-256-nya
adalah
`c522b5ec0ba7d4c938be6588a070be648263d841e1db4f9905c9b388619b64b1`.
Baris 6368 adalah `\end{document}`; tidak ada baris sumber berikutnya. Materi
sumber dan adaptasi Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Rentang sumber memuat tiga teorema, satu definisi formal, satu definisi inline,
satu lema, satu korolari, satu catatan, tiga lingkungan bukti, satu daftar
empat butir, enam catatan pinggir, satu catatan sisi, dan satu gambar TikZ.
Tidak ada latihan atau pertanyaan formal sumber, diagram Xy-pic, gambar
eksternal, perintah sitasi, ataupun berkas yang diimpor.

Edisi memperbaiki beberapa masalah matematika yang dapat dibuktikan langsung.
Bukti Brouwer memakai kohomologi tereduksi dan arah peta kontravarian yang
benar; pendekatan dalam bukti teorema dasar aljabar diganti dengan batas
kuantitatif; sfera satuan serat singgung dibedakan dari sfera ambien; dan
rumus medan dimensi ganjil diperbaiki sehingga
$v(x)\mathbin{\cdot}x=0$, bukan $1$. Semua koreksi dijelaskan dalam blok audit
sumber dan audit pendamping.

Enam pemeriksaan penguasaan, enam petunjuk, satu bukti korolari, dan enam
solusi lengkap merupakan materi asli edisi dan tersedia di bawah CC BY 4.0.
Edisi ini bersifat independen; edisi ini tidak disponsori, didukung,
disahkan, ataupun diberi status resmi oleh David Michael Roberts atau
institusinya. Produksi edisi ini dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini menambah transparansi
proses tanpa mengurangi kredit penulis sumber ataupun kredit kontributor
manusia.

# Kuliah 30 {#o012-rbt-l30}

## Tiga penerapan klasik {#o012-rbt-l30-s01}

Pada sisa kuliah ini, kita menerapkan perangkat topologi yang telah dibangun
untuk tiga persoalan klasik:

1. keberadaan titik tetap bagi fungsi kontinu $D^n\to D^n$;
2. teorema dasar aljabar; dan
3. keberadaan medan vektor yang tidak pernah nol pada sfera.

## Teorema titik tetap Brouwer {#o012-rbt-l30-s02}

Teorema pemetaan kontraksi menyatakan bahwa jika fungsi
$f\colon D^n\to D^n$ memenuhi

$$
\|f(x)-f(y)\|\leq C\|x-y\|
\qquad\text{untuk suatu }C\in(0,1),
$$

maka terdapat titik tetap $x_0\in D^n$ dengan $f(x_0)=x_0$.

::: {.aside #o012-rbt-l30-aside-001}
**Keunikan pada kasus kontraksi.** Teorema pemetaan kontraksi bahkan memberi
tepat satu titik tetap.
:::

Banyak fungsi-diri yang bukan kontraksi tetap mempunyai titik tetap. Rotasi
terhadap pusat $0$, misalnya, menetapkan $0$. Sebuah fungsi juga dapat sama
dengan identitas pada suatu daerah kecil—sehingga mempunyai banyak titik
tetap—namun meregangkan titik-titik di tempat lain.

::: {.definition #o012-rbt-l30-def-001 data-source-form="inline"}
**Definisi 30.1 (fungsi-diri bebas).** Fungsi-diri kontinu
$f\colon X\to X$ disebut **bebas** jika

$$
f(x)\neq x
\qquad\text{untuk setiap }x\in X.
$$

Dengan kata lain, fungsi-diri bebas tidak mempunyai titik tetap.
:::

::: {.theorem #o012-rbt-l30-thm-001}
**Teorema 30.1 (teorema titik tetap Brouwer).** Untuk setiap $n\geq0$, tidak
ada fungsi-diri kontinu bebas $f\colon D^n\to D^n$. Setiap fungsi-diri kontinu
$D^n$ mempunyai titik tetap.
:::

::: {.proof #o012-rbt-l30-proof-001}
**Bukti.** Untuk $n=0$, ruang $D^0$ hanya mempunyai satu titik, sehingga
pernyataannya langsung benar. Sekarang andaikan $n\geq1$ dan, untuk memperoleh
kontradiksi, andaikan $f\colon D^n\to D^n$ bebas.

Untuk $x\in D^n$, letakkan

$$
a=f(x),
\qquad
d=x-f(x)\neq0.
$$

Sinar yang bermula di $a$, melewati $x$, dan diteruskan ke arah $d$ memotong
batas $S^{n-1}=\partial D^n$ pada tepat satu titik sesudah $x$. Secara
eksplisit, letakkan

$$
\lambda(x)=
\frac{-\langle a,d\rangle+
\sqrt{\langle a,d\rangle^2+
\|d\|^2(1-\|a\|^2)}}{\|d\|^2}
$$

dan definisikan

$$
g_f(x)=a+\lambda(x)d.
$$

Rumus kuadrat menunjukkan
$\|g_f(x)\|=1$ dan $\lambda(x)\geq1$. Karena $d\neq0$, seluruh operasi dalam
rumus kontinu; jadi $g_f\colon D^n\to S^{n-1}$ kontinu. Jika
$x\in S^{n-1}$, akar keluar pada sinar tersebut adalah $\lambda(x)=1$, maka
$g_f(x)=x$.

::: {.figure #o012-rbt-l30-fig-001}
**Gambar semantik 30.1 (retraksi dari fungsi bebas).** Pada satu garis
berarah terdapat tiga titik dalam urutan

$$
f(x)\quad\longrightarrow\quad x\quad\longrightarrow\quad g_f(x).
$$

Titik $f(x)$ dan $x$ berada di $D^n$; titik $g_f(x)$ adalah perpotongan sinar
dengan batas $S^{n-1}$. Jika $x$ sudah berada pada batas, titik kedua dan
ketiga berimpit. Deskripsi ini mereflow gambar TikZ sumber tanpa menghilangkan
objek, arah, atau relasi geometrisnya.
:::

Tuliskan $i\colon S^{n-1}\hookrightarrow D^n$ untuk inklusi. Kesamaan pada
batas memberi

$$
g_f\circ i=\operatorname{id}_{S^{n-1}}.
$$

Terapkan fungtor kohomologi tereduksi dengan koefisien $\mathbb Z$. Karena
kohomologi kontravarian, urutan peta yang benar adalah

$$
\mathbb Z
\cong\widetilde H^{n-1}(S^{n-1};\mathbb Z)
\xrightarrow{\ g_f^*\ }
\widetilde H^{n-1}(D^n;\mathbb Z)=0
\xrightarrow{\ i^*\ }
\widetilde H^{n-1}(S^{n-1};\mathbb Z)
\cong\mathbb Z.
$$

Komposisinya harus

$$
i^*\circ g_f^*=(g_f\circ i)^*=\operatorname{id}_{\mathbb Z},
$$

tetapi setiap peta yang memfaktor melalui grup nol adalah nol. Kontradiksi ini
menunjukkan bahwa $f$ tidak mungkin bebas. $\square$
:::

::: {.source-audit #o012-rbt-l30-audit-001}
**Audit sumber 30.1.** Sumber menggambar $g_f$ tanpa terlebih dahulu
menyatakan pengandaian bahwa $f$ bebas, dan membiarkan kontinuitasnya sebagai
latihan. Edisi menyatakan pengandaian, memberi rumus kontinu, dan mereflow
gambar. Sumber juga menukar label $i^*$ dan $g_f^*$ serta memakai kohomologi
biasa, yang gagal memberi suku tengah nol ketika $n=1$. Edisi memakai arah
kontravarian dan kohomologi tereduksi. Contoh sumber “fungsi konstan pada suatu
daerah mempunyai banyak titik tetap” diperbaiki menjadi fungsi yang sama
dengan identitas pada daerah itu.
:::

::: {.remark #o012-rbt-l30-rem-001}
**Catatan 30.1 (keberadaan tanpa pilihan kontinu).** Teorema ini biasanya
dinyatakan sebagai “setiap fungsi-diri mempunyai titik tetap.” Bukti di atas
secara langsung menyingkirkan fungsi-diri tanpa titik tetap. Perbedaan itu
penting dalam logika nonklasik dan dalam komputasi numerik.

Lokasi titik tetap dapat meloncat secara tak kontinu ketika fungsi-diri
berubah dalam suatu keluarga kontinu. Jadi bukti Brouwer tidak menyediakan
satu metode kontinu untuk memilih titik tetap. Ini berbeda dari teorema
pemetaan kontraksi, yang membangun barisan Cauchy menuju titik tetap unik.
Himpunan titik tetap umum dapat berperilaku jauh lebih rumit.
:::

## Teorema dasar aljabar {#o012-rbt-l30-s03}

Penerapan kedua memerlukan masukan topologis melalui

$$
\pi_1(\mathbb C^\times)\cong\mathbb Z,
$$

tempat $\mathbb C^\times=\mathbb C\setminus\{0\}$. Kita mempertimbangkan
polinom berkoefisien kompleks. Polinom **monik** mempunyai koefisien utama
sama dengan $1$.

::: {.aside #o012-rbt-l30-aside-002}
**Catatan aljabar.** Formulasi yang lebih umum memakai medan tertutup-real
$k$: medan itu terurut, setiap elemen positif merupakan kuadrat, dan setiap
polinom berderajat ganjil mempunyai akar. Medan
$k[\sqrt{-1}]$ kemudian tertutup aljabar. Untuk $k=\mathbb R$, sifat nilai
antara merupakan salah satu masukan klasik yang menjamin perilaku akar real
yang diperlukan.
:::

::: {.theorem #o012-rbt-l30-thm-002}
**Teorema 30.2 (teorema dasar aljabar).** Fungsi polinom monik takkonstan

$$
p\colon\mathbb C\longrightarrow\mathbb C
$$

tidak dapat difaktorkan melalui inklusi
$\mathbb C^\times\hookrightarrow\mathbb C$. Dengan kata lain, $p$ mempunyai
sekurang-kurangnya satu akar kompleks.
:::

::: {.proof #o012-rbt-l30-proof-002}
**Bukti.** Tuliskan

$$
p(z)=z^n+a_{n-1}z^{n-1}+\cdots+a_1z+a_0,
\qquad n\geq1.
$$

Pilih $R>0$ cukup besar sehingga

$$
\sum_{j=0}^{n-1}|a_j|R^j<R^n.
$$

Pada lingkaran berjari-jari $R$, definisikan

$$
p_R(\theta)=p(Re^{i\theta}),
\qquad
q(\theta)=R^ne^{in\theta}.
$$

Homotopi garis lurus

$$
H(s,\theta)=q(\theta)+s\bigl(p_R(\theta)-q(\theta)\bigr),
\qquad 0\leq s\leq1,
$$

tidak pernah mengenai nol, sebab

$$
|H(s,\theta)|
\geq R^n-s\sum_{j=0}^{n-1}|a_j|R^j
>0.
$$

Jadi $p_R$ dan $q$ homotop sebagai fungsi $S^1\to\mathbb C^\times$. Fungsi
$q$ melilit titik asal sebanyak $n$ kali dan tidak homotop dengan fungsi
konstan. Hal ini dapat dilihat dengan mengangkat lintasan melalui penutup

$$
\exp\colon\mathbb C\longrightarrow\mathbb C^\times;
$$

angkatannya berubah sebesar $2\pi i n$ setelah satu putaran.

Andaikan sekarang $p$ memfaktor melalui $\mathbb C^\times$, yakni
$p(z)\neq0$ untuk setiap $z$. Maka

$$
K(t,\theta)=p\bigl((1-t)Re^{i\theta}\bigr)
$$

adalah homotopi di $\mathbb C^\times$ dari $p_R$ ke fungsi konstan bernilai
$p(0)$. Ini membuat $p_R$ nul-homotop, padahal $p_R$ homotop dengan $q$ yang
tidak nul-homotop. Kontradiksi. Jadi $p$ harus mempunyai akar. $\square$
:::

::: {.source-audit #o012-rbt-l30-audit-002}
**Audit sumber 30.2.** Tanda pendekatan informal sumber diganti dengan
pertaksamaan eksplisit yang menjamin seluruh homotopi berada di
$\mathbb C^\times$. Karakterisasi medan tertutup-real dilengkapi dengan syarat
bahwa setiap elemen positif merupakan kuadrat. Kata “contraction” pada akhir
bukti sumber adalah salah ketik kontekstual dan diperbaiki menjadi
“contradiction.”
:::

## Derajat dan teorema sfera berbulu {#o012-rbt-l30-s04}

Penerapan terakhir berada dalam topologi diferensial, pertemuan geometri
diferensial dan topologi. Pada $S^1\subset\mathbb R^2$ terdapat medan vektor
tangen satuan

$$
v(x,y)=(-y,x).
$$

Rumus ini merotasi vektor posisi sebesar $\pi/2$ dan tidak pernah nol. Kita
dapat bertanya apakah medan semacam itu ada pada sfera lain.

::: {.aside #o012-rbt-l30-aside-003}
Menentukan **berapa banyak** medan vektor yang bebas linear pada setiap titik
merupakan persoalan yang lebih sulit daripada sekadar menentukan keberadaan
satu medan yang tidak pernah nol.
:::

::: {.theorem #o012-rbt-l30-thm-003}
**Teorema 30.3 (teorema sfera berbulu).** Pada $S^n$ terdapat medan vektor
tangen yang tidak pernah nol jika dan hanya jika $n$ ganjil.
:::

Nama julukannya berasal dari $S^2$: medan vektor divisualisasikan sebagai
rambut-rambut kecil, dan syarat tangensi berarti setiap rambut disisir rata
sepanjang permukaan.

Andaikan tersedia medan tangen yang tidak pernah nol. Dengan membaginya oleh
panjangnya, kita boleh mengandaikan panjang medan itu selalu $1$. Pada setiap
$x\in S^n\subset\mathbb R^{n+1}$, vektor satuan $v(x)$ berada pada sfera
satuan ambien dan tegak lurus terhadap $x$. Jadi medan ternormalisasi memberi
fungsi

$$
v\colon S^n\longrightarrow S^n,
\qquad
v(x)\mathbin{\cdot}x=0.
$$

Sfera satuan di dalam serat $T_xS^n$ sendiri berdimensi $n-1$; kita tidak
mengidentifikasinya dengan satu salinan tetap $S^n$. Target $S^n$ pada rumus
di atas adalah sfera satuan ambien di $\mathbb R^{n+1}$.

::: {.definition #o012-rbt-l30-def-002}
**Definisi 30.2 (derajat).** Pilih generator orientasi standar

$$
u\in\widetilde H^n(S^n;\mathbb Z)\cong\mathbb Z.
$$

Untuk fungsi $f\colon S^n\to S^n$, **derajat** $f$ adalah bilangan bulat
$\operatorname{Deg}(f)$ yang ditentukan oleh

$$
f^*(u)=\operatorname{Deg}(f)u.
$$

Kohomologi tereduksi membuat definisi ini berlaku juga bagi $n=0$.
:::

::: {.proposition #o012-rbt-l30-prop-001}
**Proposisi 30.1 (sifat dasar derajat).** Derajat mempunyai sifat-sifat
berikut.

1. Jika $f$ tidak surjektif, maka $\operatorname{Deg}(f)=0$, sebab $f$
   memfaktor melalui $S^n\setminus\{y\}\cong\mathbb R^n$ untuk suatu titik
   $y$ yang tidak berada dalam citranya.
2. $\operatorname{Deg}(\operatorname{id}_{S^n})=1$.
3. $\operatorname{Deg}(g\circ f)=
   \operatorname{Deg}(g)\operatorname{Deg}(f)$.
4. Jika $f$ homotop dengan $g$, maka
   $\operatorname{Deg}(f)=\operatorname{Deg}(g)$.

Dengan demikian, derajat memberi homomorfisma monoid

$$
\operatorname{Deg}\colon[S^n,S^n]
\longrightarrow
\operatorname{End}(\mathbb Z)
\cong(\mathbb Z,\times).
$$
:::

::: {.lemma #o012-rbt-l30-lem-001}
**Lema 30.1 (derajat refleksi koordinat).** Definisikan

$$
r_i(x_1,\ldots,x_{n+1})
=(x_1,\ldots,-x_i,\ldots,x_{n+1}).
$$

Maka $\operatorname{Deg}(r_i)=-1$.
:::

Sebelum lema, sumber menyatakan bahwa masukan sulit ini mempunyai bukti dalam
Hatcher. Sesudah lema, sumber merangkum perhitungan eksplisit Hatcher:
$S^n$ ditriangulasi oleh dua salinan $\Delta[n]$ yang ditukar oleh $r_i$.

::: {.aside #o012-rbt-l30-aside-004}
Dalam kohomologi de Rham, tanda $-1$ dapat dilihat dari pembalikan orientasi
$S^n$ dan perubahan tanda bentuk volume global.
:::

::: {.corollary #o012-rbt-l30-cor-001}
**Korolari 30.1 (derajat peta antipodal).** Untuk peta antipodal
$-\operatorname{id}_{S^n}$,

$$
\operatorname{Deg}(-\operatorname{id}_{S^n})=(-1)^{n+1}.
$$
:::

::: {.proof #o012-rbt-l30-proof-003 data-origin="edition-original"}
**Bukti edisi.** Peta antipodal adalah komposisi seluruh $n+1$ refleksi
koordinat,

$$
-\operatorname{id}_{S^n}=r_1\circ r_2\circ\cdots\circ r_{n+1}.
$$

Gunakan multiplikativitas derajat dan Lema 30.1 untuk memperoleh hasil kali
$n+1$ salinan $-1$. $\square$
:::

::: {.proof #o012-rbt-l30-proof-004}
**Bukti Teorema 30.3.** Pertama andaikan terdapat medan tangen satuan
$v\colon S^n\to S^n$ dengan $v(x)\cdot x=0$. Definisikan

$$
\begin{aligned}
h\colon I\times S^n&\longrightarrow\mathbb R^{n+1},\\
(t,x)&\longmapsto
\cos(\pi t)x+\sin(\pi t)v(x).
\end{aligned}
$$

Ortogonalitas dan panjang satu memberi

$$
\|h(t,x)\|^2
=\cos^2(\pi t)\|x\|^2
+\sin^2(\pi t)\|v(x)\|^2
=1.
$$

Jadi $h$ sebenarnya bernilai di $S^n$. Karena

$$
h(0,x)=x,
\qquad
h(1,x)=-x,
$$

$h$ adalah homotopi dari identitas ke peta antipodal. Invariansi homotopi
derajat memberi

$$
1
=\operatorname{Deg}(\operatorname{id}_{S^n})
=\operatorname{Deg}(-\operatorname{id}_{S^n})
=(-1)^{n+1}.
$$

Jika $n$ genap, ruas terakhir adalah $-1$, suatu kontradiksi. Jadi keberadaan
medan memaksa $n$ ganjil.

Sebaliknya, andaikan $n=2k-1$ dengan $k\geq1$. Untuk
$x\in S^{2k-1}\subset\mathbb R^{2k}$, definisikan

$$
v(x_1,\ldots,x_{2k})
=(-x_2,x_1,-x_4,x_3,\ldots,-x_{2k},x_{2k-1}).
$$

Pada setiap pasangan koordinat,

$$
x_{2j-1}(-x_{2j})+x_{2j}x_{2j-1}=0,
$$

sehingga $v(x)\cdot x=0$. Selain itu,

$$
\|v(x)\|^2
=\sum_{j=1}^{k}(x_{2j}^2+x_{2j-1}^2)
=\|x\|^2=1.
$$

Maka $v$ adalah medan tangen satuan yang tidak pernah nol. Pada setiap
pasangan koordinat, rumusnya sama dengan medan rotasi pada $S^1$. $\square$
:::

::: {.source-audit #o012-rbt-l30-audit-003}
**Audit sumber 30.3.** Sumber menyamakan sfera satuan dalam $T_xS^n$ dengan
$S^n$, padahal serat itu mempunyai sfera satuan $S^{n-1}$. Edisi memakai
sfera satuan ambien dan syarat ortogonalitas. Definisi derajat dipindahkan ke
kohomologi tereduksi agar mencakup $n=0$. Pada konstruksi ganjil, indeks akhir
`x_{2k=1}` diperbaiki menjadi $x_{2k-1}$ dan klaim
$v(x)\cdot x=1$ diperbaiki menjadi $0$; panjangnya, bukan hasil kali
titiknya, yang bernilai $1$. Frasa translasi pada contoh $S^1$ dinyatakan
sebagai translasi grup, yang secara koordinat adalah rotasi sesuai rumus
sumber.
:::

## Pemeriksaan penguasaan {#o012-rbt-l30-mastery}

::: {.exercise #o012-rbt-l30-mcheck-001 data-origin="edition-original"}
**Pemeriksaan Penguasaan 30.1 (membangun retraksi Brouwer).** Andaikan
$f\colon D^n\to D^n$ bebas dan $n\geq1$. Dengan
$a=f(x)$ dan $d=x-f(x)$:

1. selesaikan persamaan $\|a+td\|^2=1$ untuk akar keluar $t=\lambda(x)$;
2. jelaskan mengapa $\lambda$ kontinu; dan
3. buktikan bahwa $g_f(x)=a+\lambda(x)d$ sama dengan $x$ pada $S^{n-1}$.
:::

::: {.hint #o012-rbt-l30-hint-001 data-origin="edition-original"}
**Petunjuk.** Persamaannya kuadrat dalam $t$. Pilih akar taknegatif yang
terletak sesudah $x$ pada sinar dari $a$ melalui $x$.
:::

::: {.solution #o012-rbt-l30-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 30.1.** Ekspansi memberi

$$
\|d\|^2t^2+2\langle a,d\rangle t+(\|a\|^2-1)=0.
$$

Karena $d\neq0$, akar keluarnya adalah

$$
\lambda(x)=
\frac{-\langle a,d\rangle+
\sqrt{\langle a,d\rangle^2+\|d\|^2(1-\|a\|^2)}}{\|d\|^2}.
$$

Semua suku bergantung kontinu pada $x$, penyebut tidak nol, dan akar yang
dipilih tetap akar keluar; jadi $\lambda$ kontinu. Jika $\|x\|=1$, titik
$a+d=x$ sudah merupakan perpotongan keluar sinar dengan batas. Keunikan akar
keluar memberi $\lambda(x)=1$, sehingga $g_f(x)=a+d=x$.
:::

::: {.exercise #o012-rbt-l30-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 30.2 (arah kohomologi pada bukti Brouwer).** Untuk
$n=1$:

1. hitung $H^0(D^1;\mathbb Z)$ dan
   $\widetilde H^0(D^1;\mathbb Z)$;
2. hitung $\widetilde H^0(S^0;\mathbb Z)$; dan
3. tuliskan arah $g_f^*$ dan $i^*$ serta jelaskan kontradiksinya.
:::

::: {.hint #o012-rbt-l30-hint-002 data-origin="edition-original"}
**Petunjuk.** $D^1$ terhubung, sedangkan $S^0$ mempunyai dua komponen.
Kohomologi membalik arah fungsi ruang.
:::

::: {.solution #o012-rbt-l30-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 30.2.** Karena $D^1$ terhubung,

$$
H^0(D^1;\mathbb Z)\cong\mathbb Z,
\qquad
\widetilde H^0(D^1;\mathbb Z)=0.
$$

Karena $S^0$ mempunyai dua komponen,
$\widetilde H^0(S^0;\mathbb Z)\cong\mathbb Z$. Peta ruang
$g_f:D^1\to S^0$ dan $i:S^0\to D^1$ menghasilkan

$$
\mathbb Z
\xrightarrow{g_f^*}0
\xrightarrow{i^*}\mathbb Z.
$$

Namun $g_f\circ i=\operatorname{id}_{S^0}$ menuntut
$i^*\circ g_f^*=\operatorname{id}_{\mathbb Z}$. Komposisi melalui nol tidak
mungkin identitas. Kohomologi biasa derajat nol tidak memberi suku tengah nol;
itulah alasan tilde diperlukan.
:::

::: {.exercise #o012-rbt-l30-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 30.3 (lingkaran besar suatu polinom).** Untuk
$p(z)=z^n+\sum_{j<n}a_jz^j$:

1. pilih syarat eksplisit pada $R$ yang membuat suku utama dominan;
2. buktikan homotopi garis lurus dari $p_R$ ke $R^ne^{in\theta}$ menghindari
   nol; dan
3. jelaskan mengapa hipotesis “$p$ tidak berakar” memberi kontradiksi.
:::

::: {.hint #o012-rbt-l30-hint-003 data-origin="edition-original"}
**Petunjuk.** Gunakan
$\sum_{j<n}|a_j|R^j<R^n$ dan kontraksikan lingkaran berjari-jari $R$ secara
radial di domain.
:::

::: {.solution #o012-rbt-l30-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 30.3.** Pilih $R$ dengan
$A_R:=\sum_{j<n}|a_j|R^j<R^n$. Untuk
$H(s,\theta)=R^ne^{in\theta}+s(p_R-R^ne^{in\theta})$,

$$
|H(s,\theta)|\geq R^n-sA_R>0.
$$

Jadi $p_R$ mempunyai kelas homotopi yang sama dengan lingkaran berbilangan
lilit $n$, dan kelas itu taknol. Jika $p$ tidak mempunyai akar, maka
$p((1-t)Re^{i\theta})$ selalu berada di $\mathbb C^\times$ dan menghomotopkan
$p_R$ ke konstanta $p(0)$. Kelas $p_R$ lalu sekaligus nol dan taknol, suatu
kontradiksi.
:::

::: {.exercise #o012-rbt-l30-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 30.4 (derajat peta antipodal).**

1. Turunkan multiplikativitas derajat dari kontravariansi kohomologi.
2. Nyatakan peta antipodal sebagai komposisi refleksi koordinat.
3. Hitung derajatnya.
:::

::: {.hint #o012-rbt-l30-hint-004 data-origin="edition-original"}
**Petunjuk.** $(g\circ f)^*=f^*\circ g^*$ dan setiap refleksi berderajat
$-1$.
:::

::: {.solution #o012-rbt-l30-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 30.4.** Jika $f^*(u)=du$ dan $g^*(u)=eu$, maka

$$
(g\circ f)^*(u)=f^*(g^*(u))=f^*(eu)=(ed)u.
$$

Jadi $\operatorname{Deg}(g\circ f)=ed$. Peta antipodal membalik seluruh
$n+1$ koordinat, sehingga

$$
-\operatorname{id}=r_1\circ\cdots\circ r_{n+1}.
$$

Karena setiap faktor berderajat $-1$, derajat komposisinya adalah
$(-1)^{n+1}$.
:::

::: {.exercise #o012-rbt-l30-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 30.5 (obstruksi pada dimensi genap).** Andaikan
$v$ medan tangen yang tidak pernah nol pada $S^n$.

1. Normalisasikan $v$.
2. Bangun homotopi antara identitas dan peta antipodal.
3. Tunjukkan mengapa $n$ tidak mungkin genap, termasuk $n=0$.
:::

::: {.hint #o012-rbt-l30-hint-005 data-origin="edition-original"}
**Petunjuk.** Gunakan
$h(t,x)=\cos(\pi t)x+\sin(\pi t)v(x)$ dan kohomologi tereduksi untuk
definisi derajat pada $S^0$.
:::

::: {.solution #o012-rbt-l30-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 30.5.** Ganti $v(x)$ dengan
$v(x)/\|v(x)\|$. Ortogonalitas terhadap $x$ membuat $h(t,x)$ selalu
berpanjang satu, sehingga $h$ bernilai di $S^n$. Nilai ujungnya adalah $x$ dan
$-x$. Karena derajat invarian terhadap homotopi,

$$
1=\operatorname{Deg}(\operatorname{id})
=\operatorname{Deg}(-\operatorname{id})=(-1)^{n+1}.
$$

Jika $n$ genap, ruas kanan $-1$, kontradiksi. Untuk $n=0$, definisi derajat
memakai $\widetilde H^0(S^0;\mathbb Z)\cong\mathbb Z$, sehingga argumen yang
sama berlaku; secara geometris, ruang singgung sfera berdimensi nol memang
hanya memuat vektor nol.
:::

::: {.exercise #o012-rbt-l30-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 30.6 (medan pada dimensi ganjil).** Untuk
$n=2k-1$, periksa bahwa

$$
v(x_1,\ldots,x_{2k})
=(-x_2,x_1,\ldots,-x_{2k},x_{2k-1})
$$

kontinu, tangen, berpanjang satu, dan tidak pernah nol pada $S^{2k-1}$.
:::

::: {.hint #o012-rbt-l30-hint-006 data-origin="edition-original"}
**Petunjuk.** Kelompokkan koordinat menjadi pasangan
$(x_{2j-1},x_{2j})$ dan hitung hasil kali titik serta norma pada setiap
pasangan.
:::

::: {.solution #o012-rbt-l30-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 30.6.** Rumus $v$ linear, jadi kontinu. Untuk setiap
pasangan,

$$
(x_{2j-1},x_{2j})\cdot(-x_{2j},x_{2j-1})=0.
$$

Menjumlahkan memberi $x\cdot v(x)=0$, sehingga $v(x)\in T_xS^{2k-1}$.
Selain itu,

$$
\|v(x)\|^2
=\sum_j(x_{2j}^2+x_{2j-1}^2)
=\|x\|^2=1.
$$

Jadi $v(x)$ tidak pernah nol. Rumus tersebut adalah rotasi seperempat putaran
pada setiap bidang koordinat $\mathbb R^2$.
:::

::: {.boundary #o012-rbt-l30-boundary-001}
**Batas akhir sumber Roberts.** Unit 30 menerjemahkan Notes.tex baris
6271--6368 secara kontigu, termasuk `\end{document}` sebagai penanda akhir
tanpa isi pembaca. Tidak ada Kuliah 31 dalam sumber beku. Kursor berikutnya
adalah **EOF setelah Notes.tex baris 6368** (posisi nominal baris 6369).
:::
