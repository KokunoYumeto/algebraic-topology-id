---
title: "Topologi Aljabar"
subtitle: "Unit 28: Kohomologi Sfera, Eksisi, dan Baji Kerangka"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l28-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 5924--6052 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L5924-L6052)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang aktif terdiri atas 129 baris fisik. Dengan normalisasi LF dan satu
terminator LF penutup dipertahankan, ukurannya 8.257 byte dan SHA-256-nya
adalah
`f3e4a526fa2e504a449a606150c399520c255a98a91d60c934737f87497b4b51`.
Baris 6053, yang memulai Kuliah 29, tidak termasuk. Materi sumber dan adaptasi
Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Baris pertama unit ini melanjutkan contoh kohomologi sfera dari Unit 27.
Selanjutnya rentang sumber memuat satu definisi, tiga proposisi, dua teorema,
satu korolari, satu contoh baru, satu catatan, tiga lingkungan bukti, dan lima
catatan pinggir. Tidak ada latihan atau pertanyaan formal sumber, diagram,
gambar eksternal, ataupun berkas yang diimpor.

Edisi mempertahankan semua isi itu, memindahkan catatan pinggir ke urutan
bacaan, dan menerapkan empat perbaikan matematika penting. Gelanggang
koefisien taknol dinyatakan dalam bukti invariansi dimensi; arah kontravarian
peta hasil bagi pada kohomologi relatif dibetulkan; *join* yang salah diganti
dengan baji; dan teorema baji tak berhingga diberi hipotesis titik dasar baik
yang diperlukan. Pada akhir unit, peta pembanding dari korantai singular ke
korantai simpleksial ditulis sebagai restriksi dalam arah yang benar, bukan
sebagai inklusi ke arah sebaliknya. Bukti teorema hasil bagi yang hanya dirujuk
oleh sumber juga dilengkapi.

Enam pemeriksaan penguasaan, enam petunjuk, penutupan bukti edisi, dan enam
solusi lengkap merupakan materi asli edisi dan tersedia di bawah CC BY 4.0.
Edisi ini bersifat independen; edisi ini tidak disponsori, didukung,
disahkan, ataupun diberi status resmi oleh David Michael Roberts atau
institusinya. Produksi edisi ini dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini menambah transparansi
proses tanpa mengurangi kredit penulis sumber ataupun kredit kontributor
manusia.

# Kuliah 28 {#o012-rbt-l28}

## Menyelesaikan perhitungan kohomologi sfera {#o012-rbt-l28-s01}

Perhitungan komponen lintasan dan grup fundamental sudah menunjukkan bahwa
$S^0$ dan $S^1$ tidak kontraktil. Namun, $S^n$ terhubung sederhana untuk
$n\geq2$, sehingga $\Pi_1$ saja tidak dapat mendeteksi ketakkontraktilannya.
Perhitungan $H^n$ pada Unit 27 membuktikan bahwa **setiap** $S^n$ tidak
kontraktil.

Rumus kohomologi di bawah berlaku untuk setiap gelanggang koefisien $R$.
Setiap kali kohomologi dipakai untuk membedakan dua ruang, kita memilih
$R\neq0$, misalnya $R=\mathbb Z$.

::: {.aside #o012-rbt-l28-aside-001}
**Pembanding homotopi lebih tinggi.** Kita telah melihat pernyataan
$\pi_n(S^n)\cong\mathbb Z$, tetapi belum menghitungnya sendiri. Kohomologi
memberi deteksi ketakkontraktilan yang dapat diselesaikan dengan perangkat
yang sudah dibangun dalam kuliah ini.
:::

Ingat isomorfisma reduksi Mayer--Vietoris dari Unit 27:

$$
\widetilde H^{k-1}(S^{n-1};R)
\cong
\widetilde H^k(S^n;R).
$$

Ada dua rentang derajat yang masih perlu diperiksa.

1. Ambil $k=n+\ell$ dengan $\ell\geq1$ dan iterasikan reduksi. Diperoleh

   $$
   \widetilde H^{n+\ell}(S^n;R)
   \cong
   \widetilde H^\ell(S^0;R)=0.
   $$

   Jadi $H^m(S^n;R)=0$ untuk semua $m>n$.

   ::: {.aside #o012-rbt-l28-aside-002}
   Dalam dunia kombinatorial himpunan-$\Delta$, sfera
   $S^n\cong|\partial\Delta[n+1]|$ tidak mempunyai simpleks berdimensi
   $m>n$, sehingga lenyapnya derajat tinggi tampak langsung. Untuk
   kohomologi singular, himpunan $\operatorname{Top}(\Delta^m,S^n)$ justru
   tak terhitung; lenyapnya kohomologi merupakan hasil teorema, bukan
   ketiadaan simpleks singular.
   :::

   Secara khusus, dengan $R\neq0$, hasil ini menunjukkan bahwa $S^n$ tidak
   ekuivalen homotopi dengan $S^m$ jika $m>n$.

2. Andaikan $n>1$ dan $0\leq k\leq n-2$. Dengan mengiterasikan reduksi ke
   bawah,

   $$
   \widetilde H^{k+1}(S^n;R)
   \cong
   \widetilde H^1(S^{n-k};R).
   $$

   Karena $n-k>1$, cukup hitung $\widetilde H^1(S^q;R)$ untuk $q>1$.
   Bagian awal barisan eksak panjang Mayer--Vietoris memberi

   $$
   0=\widetilde H^0(S^{q-1};R)
   \longrightarrow \widetilde H^1(S^q;R)
   \longrightarrow
   \widetilde H^1(D^q_+;R)\oplus
   \widetilde H^1(D^q_-;R)=0.
   $$

   Maka $\widetilde H^1(S^q;R)=0$.

::: {.proposition #o012-rbt-l28-prop-001}
**Proposisi 28.1 (kohomologi tereduksi sfera).** Untuk setiap $n\geq0$,

$$
\widetilde H^k(S^n;R)
=
\begin{cases}
R,&k=n,\\
0,&k\neq n.
\end{cases}
$$
:::

## Invariansi dimensi ruang Euklides {#o012-rbt-l28-s02}

Isomorfisma linear antara ruang vektor real berdimensi hingga otomatis
merupakan isomorfisma ruang vektor topologis: pemetaan dan inversnya sama-sama
linear dan kontinu. Karena dua ruang vektor berdimensi hingga isomorfik tepat
ketika dimensinya sama, terdapat homeomorfisma **linear**
$\mathbb R^n\cong\mathbb R^m$ tepat ketika $n=m$.

Untuk $n,m>0$, kedua himpunan mempunyai kardinalitas yang sama,

$$
|\mathbb R^n|=|\mathbb R^m|=2^{\aleph_0},
$$

sehingga kardinalitas tidak menyingkirkan kemungkinan adanya homeomorfisma
**taklinear** ketika $n\neq m$.

::: {.aside #o012-rbt-l28-aside-003}
Pemetaan kontinu $\mathbb R^n\to\mathbb R^m$ dapat sangat liar; kurva pengisi
ruang adalah salah satu contoh. Karena itu, persoalan ini sungguh topologis,
bukan sekadar linear.
:::

::: {.proposition #o012-rbt-l28-prop-002}
**Proposisi 28.2 (invariansi dimensi).** Untuk $n,m\geq0$,
$\mathbb R^n$ homeomorfik dengan $\mathbb R^m$ jika dan hanya jika $n=m$.
:::

::: {.proof #o012-rbt-l28-proof-001}
**Bukti.** Arah balik jelas. Untuk arah maju, kasus $n=0$ atau $m=0$
ditangani oleh fakta bahwa $\mathbb R^0$ mempunyai satu titik sedangkan
$\mathbb R^r$ mempunyai lebih dari satu titik jika $r>0$. Jadi andaikan
$n,m>0$.

Pilih gelanggang koefisien taknol $R$, misalnya $R=\mathbb Z$. Jika
$\phi\colon\mathbb R^n\to\mathbb R^m$ sebuah homeomorfisma, komposisikan
dengan translasi sebesar $-\phi(0)$ agar $\phi(0)=0$. Restriksi kemudian
memberi homeomorfisma

$$
\mathbb R^n\setminus\{0\}
\cong
\mathbb R^m\setminus\{0\}.
$$

Kedua ruang itu masing-masing berekuivalensi homotopi dengan
$S^{n-1}$ dan $S^{m-1}$. Oleh invariansi homotopi dan kontravariansi,

$$
R
\cong
\widetilde H^{n-1}(S^{n-1};R)
\cong
\widetilde H^{n-1}(S^{m-1};R).
$$

Menurut Proposisi 28.1, ruas terakhir taknol tepat ketika
$n-1=m-1$. Jadi $n=m$. $\square$
:::

::: {.source-audit #o012-rbt-l28-audit-001}
**Audit sumber 28.1.** Bukti sumber memakai $R$ untuk mendeteksi satu grup
taknol, tetapi tidak mengecualikan gelanggang nol. Edisi memilih koefisien
taknol dan menutup kasus dimensi nol yang tidak dicakup argumen ruang
tertusuk.
:::

## Eksisi dan kohomologi hasil bagi {#o012-rbt-l28-s03}

Sifat berikut sulit dibuktikan langsung dan memerlukan masukan topologis yang
tidak sepele.

::: {.theorem #o012-rbt-l28-thm-001}
**Teorema 28.1 (eksisi).** Misalkan $(X,A)$ pasangan ruang dan
$Z\subseteq A$ subruang dengan

$$
\overline Z\subseteq\operatorname{int}(A).
$$

Inklusi pasangan

$$
j\colon(X\setminus Z,A\setminus Z)\hookrightarrow(X,A)
$$

menginduksi isomorfisma

$$
j^*\colon
H^k(X,A;R)
\xrightarrow{\ \cong\ }
H^k(X\setminus Z,A\setminus Z;R)
$$

untuk setiap $k$.
:::

Hipotesis penutupan dan interior menjamin bahwa $Z$ berada cukup jauh di
dalam $A$ untuk dapat dibuang tanpa mengubah kohomologi relatif. Hipotesis
tersebut otomatis terpenuhi jika $A$ terbuka dan $Z$ tertutup dalam $X$.

Jika kohomologi relatif $(X,A)$ dipikirkan sebagai kohomologi ruang hasil bagi
$X/A$, teorema ini mencerminkan identifikasi hasil bagi

$$
(X\setminus Z)/(A\setminus Z)\cong X/A
$$

di bawah hipotesis yang sesuai. Untuk pasangan bertitik, kita memakai
konvensi $X/\varnothing=X_+:=X\sqcup\{*\}$.

::: {.theorem #o012-rbt-l28-thm-002}
**Teorema 28.2 (kohomologi relatif sebagai kohomologi hasil bagi).**
Misalkan $A\subseteq X$ takkosong dan tertutup. Andaikan terdapat lingkungan
terbuka $U\supseteq A$ sedemikian sehingga $A$ merupakan retrak deformasi
dari $U$. Pemetaan hasil bagi pasangan

$$
q\colon(X,A)\longrightarrow(X/A,*)
$$

menginduksi isomorfisma dalam arah kontravarian

$$
q^*\colon
H^k(X/A,*;R)
\xrightarrow{\ \cong\ }
H^k(X,A;R).
$$

Dengan $H^k(X/A,*;R)=\widetilde H^k(X/A;R)$, inversnya dapat ditulis

$$
H^k(X,A;R)
\xrightarrow{\ \cong\ }
\widetilde H^k(X/A;R).
$$
:::

::: {.proof #o012-rbt-l28-proof-002 data-origin="edition-original"}
**Bukti edisi.** Karena $A\hookrightarrow U$ merupakan ekuivalensi homotopi,
$H^k(U,A;R)=0$ untuk setiap $k$. Barisan eksak panjang bagi rangkaian
$A\subseteq U\subseteq X$ lalu memberi isomorfisma

$$
H^k(X,U;R)\xrightarrow{\ \cong\ }H^k(X,A;R).
$$

Di ruang hasil bagi, $q(U)=U/A$ adalah lingkungan terbuka titik $*$ dan
kontraktil: retraksi deformasi $U\to A$ turun menjadi kontraksi
$U/A\to *$. Terapkan eksisi pada pasangan $(X,U)$ dengan membuang $A$, dan
pada pasangan $(X/A,U/A)$ dengan membuang $*$. Pemetaan $q$ membatasi menjadi
homeomorfisma pasangan

$$
(X\setminus A,U\setminus A)
\cong
((X/A)\setminus\{*\},(U/A)\setminus\{*\}).
$$

Karena itu,

$$
H^k(X,U;R)
\cong
H^k(X/A,U/A;R).
$$

Terakhir, $U/A$ takkosong dan kontraktil. Barisan eksak panjang tereduksi
bagi pasangan $(X/A,U/A)$ memberi

$$
H^k(X/A,U/A;R)
\cong
\widetilde H^k(X/A;R).
$$

Komposisi ketiga isomorfisma ini adalah invers dari $q^*$; naturalitas
menetapkan arah peta terinduksi seperti pada pernyataan. $\square$
:::

::: {.source-audit #o012-rbt-l28-audit-002}
**Audit sumber 28.2.** Sumber menuliskan panah hasil bagi yang “diinduksi” dari
$H^k(X,A;R)$ ke $H^k(X/A,*;R)$. Karena kohomologi kontravarian, arah
terinduksi yang benar ialah arah $q^*$ di atas. Panah sumber tetap sah hanya
setelah dipahami sebagai invers isomorfisma. Rujukan tunggal ke Hatcher juga
diganti dengan bukti lengkap agar unit dapat dipelajari mandiri. Catatan
pinggir sumber menulis $X\setminus\varnothing:=X\sqcup\{*\}$; konteksnya
memerlukan hasil bagi, sehingga edisi memperbaikinya menjadi
$X/\varnothing=X_+$.
:::

::: {.corollary #o012-rbt-l28-cor-001}
**Korolari 28.1.** Untuk pasangan $(X,A)$ seperti pada Teorema 28.2, terdapat
barisan eksak panjang

$$
0\longrightarrow\widetilde H^0(X/A;R)
\longrightarrow H^0(X;R)
\longrightarrow H^0(A;R)
\longrightarrow H^1(X/A;R)
\longrightarrow\cdots.
$$
:::

::: {.proof #o012-rbt-l28-proof-003}
**Bukti.** Substitusikan isomorfisma Teorema 28.2 ke barisan eksak panjang
pasangan $(X,A)$. $\square$
:::

Pasangan himpunan-$\Delta$ $(X_\bullet,A_\bullet)$ memberi pasangan ruang
$(|X_\bullet|,|A_\bullet|)$. Realisasi geometriknya merupakan pasangan CW,
sehingga tersedia lingkungan yang diretrak-deformasikan ke
$|A_\bullet|$. Sumber menunjuk Proposition A.4 dalam buku Hatcher untuk
langkah lingkungan ini. Jadi Teorema 28.2 berlaku pada situasi tersebut.

## Hasil bagi kerangka dan baji sfera {#o012-rbt-l28-s04}

Misalkan $X_\bullet$ sebuah himpunan-$\Delta$ berdimensi $n$. Inklusi
$\operatorname{sk}_{n-1}X_\bullet\subseteq X_\bullet$ menghasilkan
homeomorfisma berurutan

$$
\begin{aligned}
|X_\bullet|/|\operatorname{sk}_{n-1}X_\bullet|
&\cong
\left(\bigsqcup_{x\in X_n}\Delta^n\right)
\Big/
\left(\bigsqcup_{x\in X_n}\partial\Delta^n\right)\\
&\cong
\left(\bigsqcup_{x\in X_n}
  (\Delta^n/\partial\Delta^n)\right)
\Big/
\left(\bigsqcup_{x\in X_n}*\right)\\
&\cong
\left(\bigsqcup_{x\in X_n}S^n\right)
\Big/\operatorname{disc}(X_n)\\
&=: \bigvee_{x\in X_n}S^n.
\end{aligned}
$$

Objek terakhir adalah **baji**, bukan *join*, dari satu salinan $S^n$ untuk
setiap simpleks-$n$ dalam $X_n$.

::: {.definition #o012-rbt-l28-def-001}
**Definisi 28.1 (baji keluarga ruang bertitik).** Untuk himpunan indeks
takkosong $J$ dan keluarga ruang bertitik
$\{(X_\alpha,x_\alpha)\}_{\alpha\in J}$, **baji**

$$
\bigvee_{\alpha\in J}X_\alpha
$$

adalah ruang hasil bagi

$$
\left(\bigsqcup_{\alpha\in J}X_\alpha\right)
\Big/\operatorname{disc}(J),
$$

tempat pemetaan
$J\to\bigsqcup_{\alpha\in J}X_\alpha$ mengirim
$\alpha\mapsto x_\alpha$, dan seluruh citranya diidentifikasi menjadi satu
titik. Citra bersama itu adalah titik dasar kanonik baji.
:::

::: {.source-audit #o012-rbt-l28-audit-003}
**Audit sumber 28.3.** Notes.tex baris 6004 dan 6013 menyebut konstruksi
$\bigvee$ sebagai *join*. Simbol dan definisinya menyatakan baji (*wedge
sum*); *join* adalah konstruksi topologis lain. Edisi menerapkan koreksi yang
sama seperti pada Unit 10 dan Unit 13.
:::

Barisan eksak panjang pasangan kerangka mengandung bagian

$$
\cdots\longrightarrow
H^{k-1}(|\operatorname{sk}_{n-1}X_\bullet|;R)
\longrightarrow
H^k(|X_\bullet|,|\operatorname{sk}_{n-1}X_\bullet|;R)
\longrightarrow
H^k(|X_\bullet|;R)
\longrightarrow
H^k(|\operatorname{sk}_{n-1}X_\bullet|;R)
\longrightarrow\cdots.
$$

Teorema 28.2 memberi

$$
H^k(|X_\bullet|,|\operatorname{sk}_{n-1}X_\bullet|;R)
\cong
\widetilde H^k\!\left(\bigvee_{x\in X_n}S^n;R\right).
$$

Jadi kohomologi realisasi dibangun dari kohomologi kerangka berdimensi lebih
kecil dan sebuah suku baji yang dapat dihitung.

::: {.proposition #o012-rbt-l28-prop-003}
**Proposisi 28.3 (kohomologi baji).** Misalkan $J$ takkosong,
$\{(X_\alpha,x_\alpha)\}_{\alpha\in J}$ keluarga ruang bertitik, dan setiap
$\{x_\alpha\}$ tertutup dalam $X_\alpha$ serta merupakan retrak deformasi
suatu lingkungan terbuka dalam $X_\alpha$. Inklusi faktor menginduksi
isomorfisma

$$
\widetilde H^k\!\left(\bigvee_{\alpha\in J}X_\alpha;R\right)
\xrightarrow{\ \cong\ }
\prod_{\alpha\in J}\widetilde H^k(X_\alpha;R)
$$

untuk setiap $k$.
:::

::: {.proof #o012-rbt-l28-proof-004 data-origin="edition-original"}
**Penjelasan bukti edisi.** Letakkan
$Y=\bigsqcup_\alpha X_\alpha$ dan
$A=\bigsqcup_\alpha\{x_\alpha\}$. Hipotesis menjamin bahwa $A$ tertutup dalam
$Y$ dan merupakan retrak deformasi dari lingkungan terbuka
$\bigsqcup_\alpha U_\alpha$. Karena $Y/A=\bigvee_\alpha X_\alpha$, Teorema
28.2 memberi

$$
\widetilde H^k\!\left(\bigvee_\alpha X_\alpha;R\right)
\cong H^k(Y,A;R).
$$

Kompleks rantai relatif pada gabungan saling lepas terurai sebagai jumlah
langsung kompleks rantai relatif tiap faktor. Setelah menerapkan
$\operatorname{Hom}(-,R)$, kompleks korantainya berupa hasil kali:

$$
C^k\!\left(\bigsqcup_{\alpha}X_\alpha,
            \bigsqcup_{\alpha}\{x_\alpha\};R\right)
\cong
\prod_{\alpha}C^k(X_\alpha,\{x_\alpha\};R).
$$

Siklus dan kobatas dihitung per koordinat, sehingga mengambil kohomologi
memberi hasil kali kohomologi relatif. Identifikasi
$H^k(X_\alpha,\{x_\alpha\};R)=\widetilde H^k(X_\alpha;R)$ menyelesaikan
argumen. $\square$
:::

::: {.source-audit #o012-rbt-l28-audit-004}
**Audit sumber 28.4.** Pernyataan sumber memakai keluarga ruang bertitik
sembarang. Edisi mensyaratkan himpunan indeks takkosong serta titik dasar yang
tertutup dan diretrak-deformasikan dari lingkungan terbuka; inilah hipotesis
yang diperlukan oleh penerapan Teorema 28.2 dalam bukti di atas. Hipotesis
tersebut otomatis berlaku pada aplikasi sekarang: setiap $S^n$ adalah kompleks
CW dan titik dasarnya dapat dipilih sebagai sel-$0$.
:::

::: {.example #o012-rbt-l28-exa-001}
**Contoh 28.1 (baji sfera).** Untuk himpunan takkosong $J$,

$$
\widetilde H^k\!\left(\bigvee_{\alpha\in J}S^n;R\right)
=
\begin{cases}
\displaystyle\prod_{\alpha\in J}R\cong R^J,&k=n,\\[4pt]
0,&k\neq n.
\end{cases}
$$
:::

## Peta pembanding singular–simpleksial {#o012-rbt-l28-s05}

Untuk setiap himpunan-$\Delta$ $X_\bullet$, realisasi $|X_\bullet|$
mempunyai pemetaan istimewa

$$
\chi_x\colon\Delta^n\longrightarrow|X_\bullet|
\qquad(x\in X_n).
$$

Dengan kata lain, ada inklusi himpunan

$$
\iota_n\colon
X_n\hookrightarrow\operatorname{Top}(\Delta^n,|X_\bullet|),
\qquad x\longmapsto\chi_x.
$$

Karena korantai adalah fungsi pada himpunan simpleks dan karena konstruksi
$R^{(-)}$ kontravarian, inklusi ini menghasilkan **restriksi**

$$
\rho_n:=\iota_n^*\colon
C^n_{\mathrm{sing}}(|X_\bullet|;R)
\longrightarrow
C^n_\Delta(X_\bullet;R),
\qquad
(\rho_n\varphi)(x)=\varphi(\chi_x).
$$

Pemetaan-pemetaan $\rho_n$ membentuk pemetaan kompleks korantai. Memang,
karena sisi pemetaan karakteristik adalah pemetaan karakteristik sisi,
$\chi_x\circ\partial_i=\chi_{d_i x}$, maka

$$
\begin{aligned}
(\rho_{n+1}\delta_{\mathrm{sing}}\varphi)(x)
&=(\delta_{\mathrm{sing}}\varphi)(\chi_x)\\
&=\sum_{i=0}^{n+1}(-1)^i
  \varphi(\chi_x\circ\partial_i)\\
&=\sum_{i=0}^{n+1}(-1)^i
  \varphi(\chi_{d_i x})\\
&=(\delta_\Delta\rho_n\varphi)(x).
\end{aligned}
$$

Jadi terdapat peta kanonik

$$
\rho\colon
C^\bullet_{\mathrm{sing}}(|X_\bullet|;R)
\longrightarrow
C^\bullet_\Delta(X_\bullet;R).
$$

Unit 29 akan membuktikan bahwa peta ini menginduksi isomorfisma kohomologi.

::: {.source-audit #o012-rbt-l28-audit-005}
**Audit sumber 28.5.** Sumber membalik arah peta ini. Inklusi simpleks
istimewa ke semua simpleks singular menghasilkan prakomposisi dari fungsi
pada **semua** simpleks ke fungsi pada simpleks istimewa. Tidak ada inklusi
kanonik korantai simpleksial ke korantai singular. Seluruh diagram pembanding
berikutnya harus memakai arah restriksi $\rho$ di atas.
:::

## Pemeriksaan penguasaan {#o012-rbt-l28-mastery}

::: {.exercise #o012-rbt-l28-mcheck-001 data-origin="edition-original"}
**Pemeriksaan Penguasaan 28.1 (seluruh kohomologi sfera).** Ambil
$R\neq0$.

1. Hitung $H^k(S^n;R)$ untuk semua $k$ dan $n\geq1$.
2. Jelaskan perbedaan derajat nol antara kohomologi biasa dan tereduksi.
3. Buktikan bahwa $S^n$ dan $S^m$ tidak ekuivalen homotopi jika $n\neq m$.
:::

::: {.hint #o012-rbt-l28-hint-001 data-origin="edition-original"}
**Petunjuk.** Gunakan Proposisi 28.1 dan fakta bahwa $S^n$ terhubung lintasan
untuk $n\geq1$. Ekuivalensi homotopi harus melestarikan setiap derajat
kohomologi.
:::

::: {.solution #o012-rbt-l28-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 28.1.** Untuk $n\geq1$, sfera terhubung lintasan, sehingga
$H^0(S^n;R)\cong R$ dan $\widetilde H^0(S^n;R)=0$. Proposisi 28.1 memberi

$$
H^k(S^n;R)=
\begin{cases}
R,&k=0\text{ atau }k=n,\\
0,&\text{selain itu}.
\end{cases}
$$

Kohomologi tereduksi membuang salinan konstanta $R$ pada derajat nol, tetapi
bersepakat dengan kohomologi biasa pada derajat positif. Jika, misalnya,
$m>n$, maka

$$
H^m(S^m;R)\cong R\neq0,
\qquad
H^m(S^n;R)=0.
$$

Kedua fungtor kohomologi tidak mungkin diisomorfiskan oleh ekuivalensi
homotopi. Jadi $S^n\not\simeq S^m$ untuk $n\neq m$.
:::

::: {.exercise #o012-rbt-l28-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 28.2 (mengapa koefisien harus taknol).**

1. Ulangi bukti Proposisi 28.2 dengan $R=\mathbb Z$.
2. Tunjukkan tepat di mana bukti gagal jika $R$ adalah gelanggang nol.
3. Mengapa kasus $n=0<m$ tidak memerlukan kohomologi?
:::

::: {.hint #o012-rbt-l28-hint-002 data-origin="edition-original"}
**Petunjuk.** Bandingkan kohomologi tereduksi derajat $n-1$ dari dua sfera.
Ruang $\mathbb R^0$ adalah singleton.
:::

::: {.solution #o012-rbt-l28-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 28.2.** Jika $n,m>0$ dan ruang Euklides homeomorfik,
ruang tertusuknya homeomorfik dan karenanya

$$
\widetilde H^{n-1}(S^{n-1};\mathbb Z)
\cong
\widetilde H^{n-1}(S^{m-1};\mathbb Z).
$$

Ruas kiri adalah $\mathbb Z$. Ruas kanan adalah $\mathbb Z$ jika
$m-1=n-1$ dan nol jika tidak. Maka $m=n$. Dengan gelanggang nol, kedua ruas
selalu nol dan tidak membedakan dimensi apa pun; langkah “ruas kanan taknol”
gagal. Jika $n=0<m$, $\mathbb R^0$ mempunyai satu titik sedangkan
$\mathbb R^m$ mempunyai tak berhingga banyak titik, sehingga bahkan tidak ada
bijeksi, apalagi homeomorfisma.
:::

::: {.exercise #o012-rbt-l28-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 28.3 (arah eksisi).** Misalkan
$Z\subseteq A\subseteq X$ memenuhi hipotesis eksisi dan
$j:(X\setminus Z,A\setminus Z)\hookrightarrow(X,A)$.

1. Tentukan arah $j^*$ pada kohomologi relatif.
2. Jelaskan mengapa arah yang sama tidak boleh ditebak dari arah panah pada
   homologi.
3. Jika $Z=\varnothing$, identifikasi $j^*$.
:::

::: {.hint #o012-rbt-l28-hint-003 data-origin="edition-original"}
**Petunjuk.** Kohomologi membalik arah pemetaan ruang. Untuk $Z=\varnothing$,
$j$ adalah identitas pasangan.
:::

::: {.solution #o012-rbt-l28-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 28.3.** Kontravariansi memberi

$$
j^*\colon H^k(X,A;R)
\longrightarrow H^k(X\setminus Z,A\setminus Z;R).
$$

Teorema eksisi menyatakan bahwa panah ini isomorfisma. Homologi bersifat
kovarian, sehingga inklusi yang sama menghasilkan panah relatif dalam arah
yang sama dengan $j$; menyalin arah itu ke kohomologi akan salah. Jika
$Z=\varnothing$, domain pasangan sumber sama dengan $(X,A)$ dan $j$ adalah
identitas. Maka $j^*$ juga identitas.
:::

::: {.exercise #o012-rbt-l28-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 28.4 (merekonstruksi teorema hasil bagi).** Dalam
hipotesis Teorema 28.2, susun empat langkah berikut dalam urutan logis dan
jelaskan isomorfisma pada setiap langkah:

- kontraktilitas $U/A$;
- barisan eksak rangkaian $A\subseteq U\subseteq X$;
- eksisi $A$ dan $*$;
- barisan eksak tereduksi pasangan $(X/A,U/A)$.
:::

::: {.hint #o012-rbt-l28-hint-004 data-origin="edition-original"}
**Petunjuk.** Mulailah dengan $H^k(X,A;R)$, pindah ke pasangan $(X,U)$,
bandingkan komplemen melalui $q$, lalu akhiri pada kohomologi tereduksi.
:::

::: {.solution #o012-rbt-l28-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 28.4.** Karena $H^*(U,A;R)=0$, barisan eksak rangkaian
memberi

$$
H^k(X,A;R)\cong H^k(X,U;R).
$$

Eksisi membuang $A$ dari $(X,U)$ dan $*$ dari $(X/A,U/A)$. Pemetaan hasil
bagi mengidentifikasi kedua pasangan komplemen, sehingga

$$
H^k(X,U;R)\cong H^k(X/A,U/A;R).
$$

Retraksi deformasi $U\to A$ turun menjadi kontraksi $U/A\to *$. Karena itu,
barisan eksak tereduksi pasangan terakhir memberi

$$
H^k(X/A,U/A;R)\cong\widetilde H^k(X/A;R).
$$

Komposisinya adalah isomorfisma yang dinyatakan Teorema 28.2; peta kanonik
yang diinduksi oleh $q$ berjalan dalam arah sebaliknya dan merupakan
inversnya.
:::

::: {.exercise #o012-rbt-l28-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 28.5 (sel baru dan baji sfera).** Misalkan
$X_\bullet$ berdimensi $n$ dan mempunyai tepat $r<\infty$ simpleks-$n$.

1. Identifikasi
   $|X_\bullet|/|\operatorname{sk}_{n-1}X_\bullet|$.
2. Hitung kohomologi tereduksinya.
3. Tentukan satu-satunya derajat tempat suku relatif
   $H^k(|X_\bullet|,|\operatorname{sk}_{n-1}X_\bullet|;R)$ dapat taknol.
:::

::: {.hint #o012-rbt-l28-hint-005 data-origin="edition-original"}
**Petunjuk.** Setiap simpleks-$n$ menjadi satu sfera setelah seluruh batasnya
diruntuhkan. Gunakan Proposisi 28.3.
:::

::: {.solution #o012-rbt-l28-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 28.5.** Meruntuhkan kerangka mengidentifikasi batas setiap
simpleks-$n$ menjadi titik dasar bersama. Jadi

$$
|X_\bullet|/|\operatorname{sk}_{n-1}X_\bullet|
\cong
\bigvee_{j=1}^{r}S^n.
$$

Karena baji berhingga, hasil kali $r$ salinan $R$ sama dengan jumlah langsung
berhingga, sehingga

$$
\widetilde H^k\!\left(\bigvee_{j=1}^{r}S^n;R\right)
=
\begin{cases}
R^r,&k=n,\\
0,&k\neq n.
\end{cases}
$$

Teorema 28.2 mengidentifikasi ini dengan kohomologi relatif pasangan
kerangka. Jadi suku relatif hanya mungkin taknol pada derajat $n$.
:::

::: {.exercise #o012-rbt-l28-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 28.6 (arah peta pembanding).** Untuk
$x\in X_n$ dan $\varphi\in C^n_{\mathrm{sing}}(|X_\bullet|;R)$:

1. Tuliskan $(\rho_n\varphi)(x)$.
2. Buktikan $\rho_{n+1}\delta_{\mathrm{sing}}
   =\delta_\Delta\rho_n$.
3. Jelaskan mengapa inklusi himpunan simpleks tidak menghasilkan peta
   korantai kanonik dalam arah simpleksial-ke-singular.
:::

::: {.hint #o012-rbt-l28-hint-006 data-origin="edition-original"}
**Petunjuk.** Prakomposisikan fungsi dengan
$\iota_n:X_n\hookrightarrow\operatorname{Top}(\Delta^n,|X_\bullet|)$ dan
gunakan $\chi_x\circ\partial_i=\chi_{d_i x}$.
:::

::: {.solution #o012-rbt-l28-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 28.6.** Definisi memberi

$$
(\rho_n\varphi)(x)=\varphi(\chi_x).
$$

Karena sisi simpleks karakteristik sesuai dengan pemetaan muka,

$$
\begin{aligned}
(\rho_{n+1}\delta_{\mathrm{sing}}\varphi)(x)
&=\sum_i(-1)^i\varphi(\chi_x\circ\partial_i)\\
&=\sum_i(-1)^i\varphi(\chi_{d_i x})\\
&=(\delta_\Delta\rho_n\varphi)(x).
\end{aligned}
$$

Jadi $\rho$ adalah pemetaan kompleks korantai. Secara set-teoretis,
$\iota_n$ memasukkan simpleks istimewa ke himpunan semua simpleks singular.
Fungsi bernilai $R$ berubah secara kontravarian: fungsi pada himpunan besar
dapat direstriksi ke himpunan kecil. Sebaliknya, tidak ada cara kanonik untuk
memperluas fungsi pada simpleks istimewa ke semua simpleks singular; ekstensi
sembarang juga tidak otomatis berkomutasi dengan diferensial. Karena itu arah
kanonik hanyalah singular-ke-simpleksial.
:::

::: {.boundary #o012-rbt-l28-boundary-001}
**Batas ke Unit 29.** Unit 28 menerjemahkan Notes.tex baris 5924--6052 secara
kontigu dan menutup seluruh objek sumber pada rentang itu. Baris 6053 adalah
`\lecturenum{29}` dan tidak dimasukkan. Kursor sumber berikutnya yang tepat
adalah **Notes.tex baris 6053**. Unit 29 harus mempertahankan arah restriksi
$C^\bullet_{\mathrm{sing}}(|X_\bullet|;R)\to
C^\bullet_\Delta(X_\bullet;R)$ pada semua diagram naturalitas dan perbandingan.
:::
