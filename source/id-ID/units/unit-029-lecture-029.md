---
title: "Topologi Aljabar"
subtitle: "Unit 29: Perbandingan Kohomologi dan Aksioma Eilenberg–Steenrod"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l29-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 6053--6270 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L6053-L6270)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang aktif terdiri atas 218 baris fisik. Dengan normalisasi LF dan satu
terminator LF penutup dipertahankan, ukurannya 11.447 byte dan SHA-256-nya
adalah
`33c6b7bfe3216d271c6b1f9d0cb952e6ef02a5e27a57f686936e764bfc4a9233`.
Baris 6271, yang memuat penanda Kuliah 30, tidak termasuk. Materi sumber dan
adaptasi Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Rentang sumber memuat dua definisi, satu lema, satu fakta, dua teorema, satu
korolari, tiga contoh, dua catatan, dua lingkungan bukti, empat catatan
pinggir, empat diagram Xy-pic, dan satu gambar TikZ. Tidak ada latihan atau
pertanyaan formal sumber, gambar eksternal, sitasi, ataupun berkas yang
diimpor.

Perbaikan utama unit ini mengikuti Audit 28.5: semua peta pembanding ditulis
dalam arah kanonik dari korantai singular ke korantai simpleksial. Diagram
barisan eksak, fakta relatif, teorema perbandingan, dan korolarinya disusun
ulang secara seragam. Induksi Lema Lima dilengkapi; definisi kompleks CW
dimulai dengan pelekatan sel-1 pada indeks nol; gambar pelekatan disajikan
ulang sebagai data semantik; dan aksioma eksisi dibatasi pada objek yang
benar-benar berada dalam domain fungtornya. Contoh manifold juga dirumuskan
tanpa menyamakan tipe homotopi CW dengan triangulabilitas literal.

Enam pemeriksaan penguasaan, enam petunjuk, penutupan bukti edisi, dan enam
solusi lengkap merupakan materi asli edisi dan tersedia di bawah CC BY 4.0.
Edisi ini bersifat independen; edisi ini tidak disponsori, didukung,
disahkan, ataupun diberi status resmi oleh David Michael Roberts atau
institusinya. Produksi edisi ini dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini menambah transparansi
proses tanpa mengurangi kredit penulis sumber ataupun kredit kontributor
manusia.

# Kuliah 29 {#o012-rbt-l29}

## Kealamian peta pembanding {#o012-rbt-l29-s01}

Unit 28 membangun peta restriksi kanonik

$$
\rho_X\colon
C^\bullet_{\mathrm{sing}}(|X_\bullet|;R)
\longrightarrow
C^\bullet_\Delta(X_\bullet;R).
$$

Peta ini natural terhadap pemetaan himpunan-$\Delta$.

::: {.lemma #o012-rbt-l29-lem-001}
**Lema 29.1 (kealamian pembanding).** Jika
$f\colon X_\bullet\to Y_\bullet$ pemetaan himpunan-$\Delta$, persegi

$$
\begin{array}{ccc}
C^\bullet_{\mathrm{sing}}(|Y_\bullet|;R)
&\xrightarrow{|f|^*}&
C^\bullet_{\mathrm{sing}}(|X_\bullet|;R)\\[3pt]
\downarrow\rho_Y&&\downarrow\rho_X\\[3pt]
C^\bullet_\Delta(Y_\bullet;R)
&\xrightarrow{f^*}&
C^\bullet_\Delta(X_\bullet;R)
\end{array}
$$

komutatif.
:::

::: {.proof #o012-rbt-l29-proof-001 data-origin="edition-original"}
**Bukti edisi.** Untuk
$\varphi\in C^n_{\mathrm{sing}}(|Y_\bullet|;R)$ dan $x\in X_n$,

$$
\begin{aligned}
(\rho_X|f|^*\varphi)(x)
&=(|f|^*\varphi)(\chi_x)\\
&=\varphi(|f|\circ\chi_x)\\
&=\varphi(\chi_{f(x)})\\
&=(f^*\rho_Y\varphi)(x).
\end{aligned}
$$

Kesamaan ketiga berasal dari definisi realisasi geometrik suatu pemetaan
himpunan-$\Delta$. Jadi kedua komposisi sama pada setiap derajat. $\square$
:::

::: {.source-audit #o012-rbt-l29-audit-001}
**Audit sumber 29.1.** Diagram sumber menempatkan peta horizontal
simpleksial-ke-singular. Inklusi simpleks istimewa justru menghasilkan
restriksi singular-ke-simpleksial. Edisi membalik seluruh keluarga diagram,
bukan hanya panah pertama, agar kealamian dan sifat kontravarian tetap seragam.
:::

## Perbandingan relatif pada kerangka {#o012-rbt-l29-s02}

Ambil inklusi
$i\colon\operatorname{sk}_{n-1}X_\bullet\hookrightarrow X_\bullet$.
Restriksi $\rho$ menghasilkan peta dari barisan eksak pendek singular ke
barisan eksak pendek simpleksial:

$$
\begin{array}{ccccccccc}
0&\to&C^\bullet_{\mathrm{sing}}
(|X_\bullet|,|\operatorname{sk}_{n-1}X_\bullet|;R)
&\to&C^\bullet_{\mathrm{sing}}(|X_\bullet|;R)
&\to&C^\bullet_{\mathrm{sing}}
(|\operatorname{sk}_{n-1}X_\bullet|;R)&\to&0\\
&&\downarrow\rho_{\mathrm{rel}}&&\downarrow\rho_X
&&\downarrow\rho_{\mathrm{sk}}&&\\
0&\to&C^\bullet_\Delta
(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)
&\to&C^\bullet_\Delta(X_\bullet;R)
&\to&C^\bullet_\Delta
(\operatorname{sk}_{n-1}X_\bullet;R)&\to&0.
\end{array}
$$

Karena semua persegi komutatif, diperoleh peta barisan eksak panjang. Agar
diagram lima suku sumber tetap dapat mengalir pada layar sempit, baris
singularnya ditulis sebagai

$$
\begin{aligned}
H^{k-1}_{\mathrm{sing}}(|\operatorname{sk}_{n-1}X_\bullet|;R)
&\longrightarrow H^k_{\mathrm{sing}}
(|X_\bullet|,|\operatorname{sk}_{n-1}X_\bullet|;R)
\longrightarrow H^k_{\mathrm{sing}}(|X_\bullet|;R)\\
&\longrightarrow H^k_{\mathrm{sing}}
(|\operatorname{sk}_{n-1}X_\bullet|;R)
\longrightarrow H^{k+1}_{\mathrm{sing}}
(|X_\bullet|,|\operatorname{sk}_{n-1}X_\bullet|;R).
\end{aligned}
$$

Baris simpleksialnya adalah

$$
\begin{aligned}
H^{k-1}_\Delta(\operatorname{sk}_{n-1}X_\bullet;R)
&\longrightarrow H^k_\Delta
(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)
\longrightarrow H^k_\Delta(X_\bullet;R)\\
&\longrightarrow H^k_\Delta(\operatorname{sk}_{n-1}X_\bullet;R)
\longrightarrow H^{k+1}_\Delta
(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R).
\end{aligned}
$$

Restriksi $\rho$ memberi peta vertikal dari setiap suku baris singular ke
suku simpleksial tepat di bawahnya. Peta vertikal pada kedua suku relatif
(suku kedua dan kelima) adalah peta yang diberi tanda $(*)$ dalam sumber.

::: {.fact #o012-rbt-l29-fact-001}
**Fakta 29.1 (pembanding relatif adalah isomorfisma).** Jika
$X_\bullet$ berdimensi $n$, peta pembanding

$$
H^k_{\mathrm{sing}}
(|X_\bullet|,|\operatorname{sk}_{n-1}X_\bullet|;R)
\longrightarrow
H^k_\Delta
(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)
$$

adalah isomorfisma untuk setiap $k$.
:::

::: {.proof #o012-rbt-l29-proof-002 data-origin="edition-original"}
**Penjelasan bukti edisi.** Teorema hasil bagi Unit 28 mengidentifikasi ruas
kiri dengan

$$
\widetilde H^k\!\left(\bigvee_{x\in X_n}S^n;R\right).
$$

Jika $k\neq n$, kedua ruas nol. Jika $k=n$, kedua ruas adalah hasil kali
salinan $R$ berindeks $X_n$:

$$
\widetilde H^n\!\left(\bigvee_{x\in X_n}S^n;R\right)
\cong
\prod_{x\in X_n}R
\cong
H^n_\Delta
(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R).
$$

Pada faktor $x$, ambil peta hasil bagi pasangan
$q_x\colon(\Delta^n,\partial\Delta^n)\to(S^n,*)$. Kontravariansi memberi peta
faktor

$$
\widetilde H^n(S^n;R)
\longrightarrow
H^n(\Delta^n,\partial\Delta^n;R)
$$

mengirim kelas kanonik ke kelas kanonik, sehingga isomorfisma. Mengambil hasil kali
atas semua $x\in X_n$ membuktikan fakta. $\square$
:::

::: {.source-audit #o012-rbt-l29-audit-002}
**Audit sumber 29.2.** Fakta sumber mempunyai arah relatif terbalik dan pada
salah satu faktor menulis $\widetilde H^k(S^n;R)$ di tengah perhitungan kasus
$k=n$. Edisi menuliskan peta kanonik singular-ke-simpleksial dan memakai
derajat $n$ secara konsisten.
:::

## Teorema perbandingan {#o012-rbt-l29-s03}

::: {.theorem #o012-rbt-l29-thm-001}
**Teorema 29.1 (perbandingan berdimensi hingga).** Jika $X_\bullet$ sebuah
himpunan-$\Delta$ berdimensi hingga, restriksi simpleks istimewa menginduksi
isomorfisma natural

$$
\rho_X^*\colon
H^k_{\mathrm{sing}}(|X_\bullet|;R)
\xrightarrow{\ \cong\ }
H^k_\Delta(X_\bullet;R)
$$

untuk setiap $k$.
:::

::: {.proof #o012-rbt-l29-proof-003}
**Bukti.** Gunakan induksi pada dimensi $n$ dari $X_\bullet$. Jika $n=0$,
realisasi adalah ruang diskret $\operatorname{disc}(X_0)$. Kedua teori
menghasilkan $R^{X_0}$ pada derajat nol dan nol pada derajat positif, dan
$\rho^*$ adalah identitas koordinat.

Andaikan teorema benar bagi himpunan-$\Delta$ berdimensi paling tinggi
$n-1$, dan ambil $X_\bullet$ berdimensi $n$. Bandingkan barisan eksak panjang
pasangan kerangka seperti di atas. Untuk lima suku berurutan yang mengapit
$H^k_{\mathrm{sing}}(|X_\bullet|;R)\to H^k_\Delta(X_\bullet;R)$:

- kedua peta pada suku relatif adalah isomorfisma menurut Fakta 29.1; dan
- kedua peta pada suku kerangka adalah isomorfisma menurut hipotesis induksi.

Lema Lima menyatakan bahwa peta tengah juga isomorfisma. Argumen berlaku pada
setiap $k$, sehingga induksi selesai. $\square$
:::

Argumen serupa berlaku bagi kohomologi relatif. Dengan mengambil pasangan
terhadap titik dasar baik, ia juga memberi perbandingan bagi kohomologi
tereduksi.

::: {.corollary #o012-rbt-l29-cor-001 data-source-label="eq:comparison_iso_simplicial_singular"}
**Korolari 29.1 (semua himpunan-$\Delta$).** Untuk setiap himpunan-$\Delta$
$X_\bullet$ dan setiap $k$,

$$
\rho_X^*\colon
H^k_{\mathrm{sing}}(|X_\bullet|;R)
\xrightarrow{\ \cong\ }
H^k_\Delta(X_\bullet;R).
$$
:::

::: {.proof #o012-rbt-l29-proof-004 data-origin="edition-original"}
**Penjelasan bukti edisi.** Tetapkan $k$. Pada sisi kombinatorial,
$H^k$ hanya melibatkan

$$
C^{k-1}\longrightarrow C^k\longrightarrow C^{k+1},
$$

sehingga inklusi $\operatorname{sk}_{k+1}X_\bullet\hookrightarrow X_\bullet$
menginduksi isomorfisma pada $H^k_\Delta$.

Pada sisi topologis, realisasi kerangka adalah kerangka CW. Sel-sel yang
ditambahkan setelah dimensi $k+1$ mempunyai dimensi sekurang-kurangnya
$k+2$. Barisan eksak relatif dan perhitungan baji sfera menunjukkan bahwa
setiap peta pembatas dari satu kerangka lebih tinggi ke kerangka sebelumnya
adalah isomorfisma pada $H^k_{\mathrm{sing}}$ dan $H^{k-1}_{\mathrm{sing}}$
setelah tahap tersebut. Jadi sistem invers pada derajat $k$ stabil setelah
kerangka $k+1$, dan sistem pada derajat $k-1$ juga stabil. Karena itu
suku $\lim\nolimits_{\leftarrow}^{1}H^{k-1}$ dalam barisan eksak Milnor
lenyap dan limitnya
benar-benar menghasilkan

$$
H^k_{\mathrm{sing}}(|X_\bullet|;R)
\cong
H^k_{\mathrm{sing}}(|\operatorname{sk}_{k+1}X_\bullet|;R).
$$

Sekarang $\operatorname{sk}_{k+1}X_\bullet$ berdimensi hingga, walaupun dapat
mempunyai tak berhingga banyak simpleks. Terapkan Teorema 29.1 dan gunakan
kealamian untuk mendapatkan korolari.
$\square$
:::

::: {.source-audit #o012-rbt-l29-audit-003}
**Audit sumber 29.3.** Sumber menyebut kolimit terfilter tetapi tidak menutup
argumen. Edisi mengekspresikan stabilisasi pada kerangka $k+1$. Fakta bahwa
setiap simpleks singular kompak mendarat di suatu subkompleks hingga tidak
berarti ada satu subkompleks hingga yang seragam bagi semua simpleks; bukti
tidak memakai klaim seragam tersebut.
:::

Beberapa konsekuensi praktis perlu dibedakan.

1. $H^k_\Delta$ fungtorial terhadap pemetaan himpunan-$\Delta$, sedangkan
   $H^k_{\mathrm{sing}}$ fungtorial terhadap semua pemetaan kontinu. Jadi
   isomorfisma di atas natural pada domain pemetaan himpunan-$\Delta$ yang
   direalisasikan, bukan identifikasi dua fungtor yang sejak awal mempunyai
   domain sama.
2. Untuk menghitung kohomologi satu ruang yang diberi triangulasi, kompleks
   simpleksial biasanya jauh lebih kecil daripada kompleks singular.
3. Jika $|X_\bullet|$ dan $|Y_\bullet|$ homeomorfik, mungkin tidak ada pemetaan
   himpunan-$\Delta$ di antara $X_\bullet$ dan $Y_\bullet$. Meskipun begitu,

   $$
   H^k_\Delta(X_\bullet;R)
   \cong H^k_{\mathrm{sing}}(|X_\bullet|;R)
   \cong H^k_{\mathrm{sing}}(|Y_\bullet|;R)
   \cong H^k_\Delta(Y_\bullet;R).
   $$

4. Pernyataan yang sama berlaku jika kedua realisasi hanya ekuivalen homotopi.

## Kompleks CW {#o012-rbt-l29-s04}

Realisasi himpunan-$\Delta$ dibangun dari simpleks yang ditempelkan dengan
aturan muka yang kaku. Di sini $\Delta^{n+1}$ homeomorfik dengan
$D^{n+1}$ dan $\partial\Delta^{n+1}$ homeomorfik dengan $S^n$. Kompleks CW
memperlonggar bentuk sel dan peta pelekatannya.

::: {.definition #o012-rbt-l29-def-001}
**Definisi 29.1 (struktur kompleks CW).** Struktur **kompleks CW** pada ruang
$X$ terdiri atas filtrasi

$$
X^0\hookrightarrow X^1\hookrightarrow X^2\hookrightarrow\cdots,
\qquad
X=\bigcup_{n\geq0}X^n,
$$

dengan topologi lemah terhadap filtrasi tersebut, sehingga:

1. $X^0$ diskret; dan
2. untuk setiap $n\geq0$ terdapat himpunan $J_{n+1}$ dan peta pelekatan

   $$
   a_{n+1}\colon
   \operatorname{disc}(J_{n+1})\times S^n
   \longrightarrow X^n
   $$

   yang membuat persegi

   $$
   \begin{array}{ccc}
   \operatorname{disc}(J_{n+1})\times S^n
   &\xrightarrow{a_{n+1}}&X^n\\[3pt]
   \downarrow{\operatorname{id}\times\iota_n}&&\downarrow\\[3pt]
   \operatorname{disc}(J_{n+1})\times D^{n+1}
   &\longrightarrow&X^{n+1}
   \end{array}
   $$

   menjadi pushout, dengan
   $\iota_n\colon S^n\hookrightarrow D^{n+1}$ inklusi batas.

Secara ekuivalen,

$$
X^{n+1}
=
\left(
\operatorname{disc}(J_{n+1})\times D^{n+1}\sqcup X^n
\right)\big/\sim,
$$

tempat $(\alpha,s)\sim a_{n+1}(\alpha,s)$ pada batas.

Gabungan $\bigcup_n X^n$ di atas adalah kolimit topologis filtrasi: sebagai
himpunan bertopologi, ia diperoleh dari $\bigsqcup_n X^n$ dengan
mengidentifikasi setiap $x\in X^n$ dengan citranya di $X^{n+1}$. Inilah isi
topologi lemah yang dipakai dalam definisi.
:::

::: {.source-audit #o012-rbt-l29-audit-004}
**Audit sumber 29.4.** Definisi sumber memulai langkah ini pada $n\geq1$,
yang menghilangkan pelekatan sel-1. Edisi memulai pada $n=0$ dan mengindeks
$J_{n+1}$ dengan dimensi sel yang dilekatkan.
:::

::: {.figure #o012-rbt-l29-fig-001}
**Gambar semantik 29.1 (melekatkan sel).** Untuk setiap
$\alpha\in J_{n+1}$:

- objek sumber batas: $S^n_\alpha$;
- peta pelekatan: $a_{n+1,\alpha}\colon S^n_\alpha\to X^n$;
- objek pengisi: $D^{n+1}_\alpha$ dengan
  $\partial D^{n+1}_\alpha=S^n_\alpha$;
- hasil: $X^{n+1}$, diperoleh dengan menempelkan seluruh
  $D^{n+1}_\alpha$ ke $X^n$ menurut peta batasnya.

Daftar ini menggambar ulang TikZ sumber sebagai objek dan morfisma yang tetap
terbaca saat halaman mengalir ulang dan oleh teknologi bantu.
:::

Untuk setiap $\alpha\in J_{n+1}$, restriksi $a_{n+1}$ memberi peta

$$
a_{n+1,\alpha}\colon S^n=\partial D^{n+1}\longrightarrow X^n,
$$

yang disebut **peta pelekatan** sel tersebut. Kategori $\mathbf{CW}$ mempunyai
kompleks CW sebagai objek dan semua pemetaan kontinu sebagai morfisma.

::: {.example #o012-rbt-l29-exa-001}
**Contoh 29.1 (realisasi sebagai CW).** Setiap realisasi
$|X_\bullet|$ mempunyai struktur CW: setiap simpleks berdimensi $n$
menjadi sel-$n$, dan peta mukanya menentukan peta pelekatan. Jadi realisasi
geometrik dapat dipandang sebagai fungtor

$$
|-|\colon\Delta\mathbf{Set}\longrightarrow\mathbf{CW}.
$$
:::

::: {.example #o012-rbt-l29-exa-002}
**Contoh 29.2 (manifold).** Setiap manifold mulus kompak mempunyai struktur CW
hingga. Lebih umum, setiap manifold topologis kompak mempunyai tipe homotopi
suatu kompleks CW hingga. Pernyataan homeomorfisma literal dalam kategori
topologis memerlukan hipotesis dimensi atau struktur tambahan; ia tidak boleh
disamakan begitu saja dengan triangulabilitas semua manifold.
:::

## Pasangan CW dan kategori homotopi {#o012-rbt-l29-s05}

::: {.definition #o012-rbt-l29-def-002}
**Definisi 29.2 (pasangan CW).** Sebuah **pasangan CW** $(X,A)$ terdiri atas
kompleks CW $X$ dan subkompleks $A\subseteq X$. Pada setiap dimensi, sel-sel
$A$ dipilih sebagai subhimpunan sel-sel $X$, dan peta pelekatannya mendarat di
kerangka $A$ yang sesuai.
:::

Subkompleks $A$ tertutup dalam $X$. Untuk pasangan himpunan-$\Delta$
$(X_\bullet,A_\bullet)$, realisasi
$(|X_\bullet|,|A_\bullet|)$ merupakan pasangan CW.

::: {.example #o012-rbt-l29-exa-003}
**Contoh 29.3.** Untuk $n\geq1$, pasangan $(D^n,S^{n-1})$ adalah pasangan
CW. Jika $n=1$, batas $S^0$ terdiri atas dua sel-0; jika $n\geq2$, gunakan
struktur CW sfera dengan satu sel-0 dan satu sel-$(n-1)$. Dalam kedua kasus,
tambahkan satu sel-$n$ bagian dalam melalui peta pelekatan identitas pada
batas. Hasil baginya adalah

$$
D^n/S^{n-1}\cong S^n.
$$
:::

Tuliskan $\mathbf{CW}^{(2)}$ untuk kategori pasangan CW dan pemetaan pasangan.
Sebuah morfisma

$$
f\colon(X,A)\longrightarrow(Y,B)
$$

adalah pemetaan kontinu $f\colon X\to Y$ dengan $f(A)\subseteq B$. Penyertaan
$\mathbf{CW}\to\mathbf{CW}^{(2)}$ mengirim
$X\mapsto(X,\varnothing)$.

Setiap pasangan CW mempunyai lingkungan $U\supseteq A$ yang dapat diretrak
secara deformasi ke $A$. Teorema 28.2 karena itu memberi

$$
\widetilde H^k(X/A;R)
\xrightarrow{\ \cong\ }
H^k(X,A;R),
$$

dengan arah yang ditampilkan sebagai peta kontravarian hasil bagi.

Homotopi pemetaan pasangan adalah homotopi yang pada setiap waktu tetap
mengirim $A$ ke $B$. Kategori $h\mathbf{CW}^{(2)}$ mempunyai pasangan CW
sebagai objek dan **kelas homotopi pemetaan pasangan** sebagai morfisma.
Demikian pula didefinisikan $h\mathbf{CW}$.

::: {.source-audit #o012-rbt-l29-audit-005}
**Audit sumber 29.5.** Frasa sumber “homotopy equivalence classes of maps”
dapat dibaca sebagai hanya mengizinkan pemetaan yang merupakan ekuivalensi
homotopi. Yang dimaksud adalah kelas ekuivalensi pemetaan di bawah relasi
homotopi. Edisi menuliskannya secara eksplisit.
:::

## Karakterisasi Eilenberg–Steenrod {#o012-rbt-l29-s06}

::: {.theorem #o012-rbt-l29-thm-002}
**Teorema 29.2 (Eilenberg–Steenrod, 1945).** Misalkan, untuk setiap
$k\in\mathbb Z$, diberikan fungtor

$$
h^k\colon
\left(h\mathbf{CW}^{(2)}\right)^{\mathrm{op}}
\longrightarrow\operatorname{Mod}_R,
$$

dan tuliskan $h^k(X):=h^k(X,\varnothing)$. Andaikan sifat-sifat berikut
berlaku. Penulisan domain berlawanan ini berarti bahwa $h^k$ bersifat
kontravarian pada $h\mathbf{CW}^{(2)}$.

1. **Aditivitas.** Untuk setiap keluarga kompleks CW
   $\{X_\alpha\}_{\alpha\in J}$, inklusi faktor menginduksi isomorfisma

   $$
   h^k\!\left(\bigsqcup_{\alpha\in J}X_\alpha\right)
   \xrightarrow{\ \cong\ }
   \prod_{\alpha\in J}h^k(X_\alpha).
   $$

2. **Eksak dan natural.** Terdapat homomorfisma penghubung natural
   $h^k(A)\to h^{k+1}(X,A)$ dan barisan eksak panjang

   $$
   \cdots\longrightarrow h^k(X,A)
   \longrightarrow h^k(X)
   \longrightarrow h^k(A)
   \longrightarrow h^{k+1}(X,A)
   \longrightarrow\cdots
   $$

   bagi setiap pasangan CW $(X,A)$.

3. **Eksisi bertipe CW.** Jika $Z\subseteq A\subseteq X$ memenuhi
   $\overline Z\subseteq\operatorname{int}_X(A)$ dan baik
   $(X,A)$ maupun $(X\setminus Z,A\setminus Z)$ merupakan pasangan CW, maka
   inklusi pasangan menginduksi isomorfisma

   $$
   h^k(X,A)
   \xrightarrow{\ \cong\ }
   h^k(X\setminus Z,A\setminus Z).
   $$

   Bentuk eksisi kuat yang dipakai dalam pembuktian seluler menyatakan bahwa,
   untuk setiap pasangan CW, peta hasil bagi
   $q\colon(X,A)\to(X/A,*)$ menginduksi isomorfisma yang selalu bertipe benar,

   $$
   h^k(X/A,*)\xrightarrow{\ \cong\ }h^k(X,A).
   $$

4. **Dimensi.** $h^0(*)\cong R$ dan $h^k(*)=0$ untuk $k\neq0$.

Maka terdapat isomorfisma natural

$$
h^k(X,A)\cong H^k(X,A;R)
$$

untuk semua pasangan CW dan semua $k$.
:::

::: {.source-audit #o012-rbt-l29-audit-006}
**Audit sumber 29.6.** Sumber mendefinisikan $h^k$ hanya pada pasangan CW,
tetapi aksioma eksisinya langsung mengevaluasi pasangan komplemen yang tidak
otomatis merupakan pasangan CW. Edisi menyatakan syarat domain dan bentuk
eksisi kuat melalui hasil bagi seluler yang dipakai dalam teorema keunikan.
Karena domain sudah kategori homotopi, invariansi homotopi tidak perlu
ditambahkan lagi sebagai aksioma terpisah.
:::

Ada versi tereduksi $\widetilde h^k$, dan teorema memberi
$\widetilde h^k\cong\widetilde H^k$. Semua barisan eksak dan sifat
perhitungan kohomologi biasa dapat diturunkan dari aksioma-aksioma tersebut.
Dari sudut pandang ini, pembangunan korantai singular membuktikan **eksistensi**
satu teori yang memenuhi aksioma; teorema Eilenberg–Steenrod membuktikan
**keunikan** teori biasa setelah normalisasi dimensinya ditetapkan.

## Pemeriksaan penguasaan {#o012-rbt-l29-mastery}

::: {.exercise #o012-rbt-l29-mcheck-001 data-origin="edition-original"}
**Pemeriksaan Penguasaan 29.1 (kealamian pada satu simpleks).** Misalkan
$f\colon X_\bullet\to Y_\bullet$ dan
$\varphi\in C^n_{\mathrm{sing}}(|Y_\bullet|;R)$.

1. Hitung $(\rho_X|f|^*\varphi)(x)$ bagi $x\in X_n$.
2. Hitung $(f^*\rho_Y\varphi)(x)$.
3. Identifikasi persamaan geometris yang membuat kedua jawaban sama.
:::

::: {.hint #o012-rbt-l29-hint-001 data-origin="edition-original"}
**Petunjuk.** Pemetaan karakteristik simpleks $f(x)$ adalah komposisi
$|f|$ dengan pemetaan karakteristik $x$.
:::

::: {.solution #o012-rbt-l29-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 29.1.** Dengan $\chi_x$ pemetaan karakteristik,

$$
(\rho_X|f|^*\varphi)(x)
=\varphi(|f|\circ\chi_x).
$$

Di sisi lain,

$$
(f^*\rho_Y\varphi)(x)
=(\rho_Y\varphi)(f(x))
=\varphi(\chi_{f(x)}).
$$

Realisasi geometrik memenuhi
$|f|\circ\chi_x=\chi_{f(x)}$. Jadi kedua nilai sama pada setiap $x$, yang
membuktikan komutativitas persegi Lema 29.1.
:::

::: {.exercise #o012-rbt-l29-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 29.2 (empat isomorfisma mengapit peta tengah).**
Dalam bukti Teorema 29.1, tuliskan lima suku berurutan barisan eksak panjang
yang mengapit $H^k_{\mathrm{sing}}(|X|;R)\to H^k_\Delta(X;R)$. Tandai dua peta yang merupakan
isomorfisma menurut hipotesis induksi dan dua menurut Fakta 29.1.
:::

::: {.hint #o012-rbt-l29-hint-002 data-origin="edition-original"}
**Petunjuk.** Gunakan urutan: kerangka derajat $k-1$, relatif derajat $k$,
absolut derajat $k$, kerangka derajat $k$, relatif derajat $k+1$.
:::

::: {.solution #o012-rbt-l29-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 29.2.** Lima sukunya adalah

$$
H^{k-1}(\operatorname{sk}_{n-1}X)
\to H^k(X,\operatorname{sk}_{n-1}X)
\to H^k(X)
\to H^k(\operatorname{sk}_{n-1}X)
\to H^{k+1}(X,\operatorname{sk}_{n-1}X),
$$

baik pada sisi singular maupun simpleksial. Peta vertikal pertama dan keempat
adalah isomorfisma menurut hipotesis induksi pada kerangka berdimensi
$n-1$. Peta kedua dan kelima adalah isomorfisma menurut Fakta 29.1. Kedua
baris eksak dan diagram komutatif; Lema Lima memaksa peta vertikal ketiga
menjadi isomorfisma.
:::

::: {.exercise #o012-rbt-l29-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 29.3 (mengapa kerangka $k+1$ cukup).**

1. Tunjukkan bahwa $H^k_\Delta(X;R)$ hanya bergantung pada simpleks sampai
   dimensi $k+1$.
2. Jelaskan mengapa melekatkan sel berdimensi sekurang-kurangnya $k+2$ tidak
   mengubah $H^k_{\mathrm{sing}}$.
3. Simpulkan Korolari 29.1 dari Teorema 29.1.
:::

::: {.hint #o012-rbt-l29-hint-003 data-origin="edition-original"}
**Petunjuk.** Kohomologi derajat $k$ adalah kernel satu diferensial dibagi
citra diferensial sebelumnya. Untuk sisi topologis, gunakan kohomologi relatif
pasangan kerangka.
:::

::: {.solution #o012-rbt-l29-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 29.3.** Rumus

$$
H^k=\ker(C^k\to C^{k+1})/\operatorname{im}(C^{k-1}\to C^k)
$$

hanya memakai derajat $k-1,k,k+1$. Jadi kerangka $k+1$ memuat semua data
simpleksial yang diperlukan. Jika suatu sel berdimensi $r\geq k+2$
dilekatkan, kohomologi relatif pasangan tahap baru terhadap tahap lama hanya
dapat taknol pada derajat $r$. Barisan eksak pasangan karena itu memberi
isomorfisma pada derajat $k$. Mengulangi untuk semua sel lebih tinggi
menunjukkan stabilisasi topologis. Terapkan Teorema 29.1 pada
$\operatorname{sk}_{k+1}X$, lalu identifikasi kedua sisi stabil tersebut.
:::

::: {.exercise #o012-rbt-l29-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 29.4 (indeks pelekatan sel).**

1. Bangun $S^1$ dari satu sel-0 dan satu sel-1.
2. Bangun $S^2$ dari satu sel-0 dan satu sel-2.
3. Jelaskan mengapa syarat “untuk $n\geq1$” pada peta
   $S^n\to X^n$ tidak dapat menghasilkan contoh pertama.
:::

::: {.hint #o012-rbt-l29-hint-004 data-origin="edition-original"}
**Petunjuk.** Sel-1 mempunyai batas $S^0$ dan sel-2 mempunyai batas $S^1$.
Peta konstan pada batas memberi hasil bagi cakram menjadi sfera.
:::

::: {.solution #o012-rbt-l29-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 29.4.** Untuk $S^1$, ambil $X^0=\{*\}$ dan lekatkan
$D^1$ dengan kedua titik $S^0=\partial D^1$ dipetakan ke $*$. Hasilnya
$D^1/S^0\cong S^1$. Langkah ini adalah $n=0$ dalam definisi, sebab sel yang
dilekatkan berdimensi $n+1=1$.

Untuk $S^2$, ambil $X^0=X^1=\{*\}$ dan lekatkan satu $D^2$ melalui peta
konstan $S^1\to *$. Hasilnya $D^2/S^1\cong S^2$. Jika langkah pelekatan baru
dimulai pada $n=1$, tidak pernah ada mekanisme menambahkan sel-1; maka bahkan
graf dasar seperti $S^1$ tidak dapat dibangun.
:::

::: {.exercise #o012-rbt-l29-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 29.5 (pasangan cakram–sfera).** Untuk pasangan CW
$(D^n,S^{n-1})$:

1. hitung $H^k(D^n,S^{n-1};R)$;
2. tentukan arah peta hasil bagi yang diinduksi pada kohomologi; dan
3. bandingkan hasilnya dengan kohomologi tereduksi $S^n$.
:::

::: {.hint #o012-rbt-l29-hint-005 data-origin="edition-original"}
**Petunjuk.** Gunakan $D^n/S^{n-1}\cong S^n$ dan Teorema 28.2.
:::

::: {.solution #o012-rbt-l29-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 29.5.** Pemetaan hasil bagi pasangan

$$
q\colon(D^n,S^{n-1})\to(S^n,*)
$$

menginduksi, secara kontravarian,

$$
q^*\colon H^k(S^n,*;R)
\xrightarrow{\ \cong\ }
H^k(D^n,S^{n-1};R).
$$

Karena $H^k(S^n,*;R)=\widetilde H^k(S^n;R)$,

$$
H^k(D^n,S^{n-1};R)=
\begin{cases}
R,&k=n,\\
0,&k\neq n.
\end{cases}
$$

Jadi kohomologi relatif mengukur tepat sel-$n$ yang ditambahkan.
:::

::: {.exercise #o012-rbt-l29-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 29.6 (mengenali aksioma).** Sebuah teori
$h^*$ pada pasangan CW memenuhi eksak, eksisi, dan aditivitas, serta
$h^0(*)\cong R$ dan $h^k(*)=0$ untuk $k\neq0$.

1. Aksioma mana yang menghitung teori pada gabungan saling lepas tak
   berhingga?
2. Aksioma mana yang menghasilkan homomorfisma penghubung?
3. Gunakan hasil bagi $(D^n,S^{n-1})$ dan normalisasi titik untuk menjelaskan
   mengapa $h^k(D^n,S^{n-1})$ hanya taknol pada $k=n$.
:::

::: {.hint #o012-rbt-l29-hint-006 data-origin="edition-original"}
**Petunjuk.** Aditivitas memberi hasil kali; eksak memberi penghubung.
Suspensi atau induksi sel menggeser satu-satunya salinan $R$ dari derajat nol.
:::

::: {.solution #o012-rbt-l29-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 29.6.** Aditivitas memberi

$$
h^k\!\left(\bigsqcup_\alpha X_\alpha\right)
\cong\prod_\alpha h^k(X_\alpha).
$$

Barisan eksak panjang menyediakan peta penghubung
$h^k(A)\to h^{k+1}(X,A)$. Untuk pasangan cakram–batas, eksisi atau bentuk
hasil bagi memberi

$$
h^k(D^n,S^{n-1})\cong\widetilde h^k(S^n).
$$

Barisan eksak pasangan kerucut menghasilkan isomorfisma suspensi
$\widetilde h^k(S^n)\cong\widetilde h^{k-1}(S^{n-1})$. Mengiterasikan sampai
$S^0$ dan memakai aksioma dimensi memberi satu salinan $R$ tepat pada
$k=n$, serta nol pada derajat lain. Ini adalah langkah lokal yang membuat
induksi sel dalam teorema keunikan bekerja.
:::

::: {.boundary #o012-rbt-l29-boundary-001}
**Batas ke Unit 30.** Unit 29 menerjemahkan Notes.tex baris 6053--6270 secara
kontigu dan menutup seluruh objek sumber pada rentang itu. Baris 6271 memuat
`\lecturenum{30}` di tengah kalimat dan tidak dimasukkan. Kursor sumber
berikutnya yang tepat adalah **Notes.tex baris 6271**.
:::
