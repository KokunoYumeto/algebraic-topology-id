---
title: "Topologi Aljabar"
subtitle: "Unit 4: Invarian Homotopi, Transformasi Natural, dan Ruang Penutup"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l04-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic Topology* karya David Michael Roberts (2019), tepatnya `Notes.tex` baris 878-1131 pada commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`. Rentang itu dimulai dengan proposisi yang memuat penanda Kuliah 4 dan berakhir tepat setelah pernyataan tentang serat ruang penutup di sepanjang lintasan. Bukti pernyataan terakhir tidak terdapat dalam rentang unit ini. Karya sumber tersedia di bawah [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah dibaca, pemberian pengenal stabil, pemindahan diagram dan tugas dari catatan pinggir ke badan teks, serta koreksi atau klarifikasi terbatas yang dicatat satu per satu dalam ledger edisi. Di antaranya: arah pemetaan pada pelestarian koproduk; rumus $\sin(1/x)$ pada kurva sinus topolog; objek kanan bawah diagram naturalitas; kodomain transformasi $U\Rightarrow\pi_0$; karakterisasi SLPC yang benar beserta bukti global Proposisi 4.2; notasi prapeta $\chi^{-1}$; makna basis lingkungan dalam definisi SLPC; definisi pemetaan dan homotopi bertitik; kekontinuan fungsi yang turun melalui pemetaan kuadrat; serta penggunaan homeomorfisme pada definisi ruang penutup dan istilah baji untuk $S^1\vee S^1$. Materi pendamping penguasaan menjawab seluruh empat latihan dan satu pertanyaan sumber, serta melengkapi bukti Lema 4.1 yang tidak dituliskan dalam sumber. Materi baru ini juga tersedia di bawah CC BY 4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

# Kuliah 4 {#o012-rbt-l04}

## Funktor pada kategori homotopi {#o012-rbt-l04-s01}

::: {.proposition #o012-rbt-l04-prop-001}
**Proposisi 4.1.** Funktor $\pi_0$ turun menjadi sebuah funktor

$$
\pi_0\colon\mathbf{Ho}\longrightarrow\mathbf{Set}.
$$
:::

::: {.proof #o012-rbt-l04-proof-001}
**Bukti.** Kita buktikan bahwa aturan pada morfisme terdefinisi dengan baik pada setiap himpunan morfisme; sifat-sifat lainnya rutin. Misalkan
$f,g\colon X\to Y$ homotopik melalui $H\colon I\times X\to Y$. Kita harus menunjukkan bahwa untuk setiap $\alpha\in\pi_0(X)$,

$$
\pi_0(f)(\alpha)=\pi_0(g)(\alpha).
$$

Ambil $x$ dalam komponen terhubung $X_\alpha$. Komposisi

$$
I\longrightarrow I\times X\xrightarrow{H}Y,
\qquad
t\longmapsto(t,x),
$$

adalah lintasan $f(x)\rightsquigarrow g(x)$. Karena $X_\alpha$ terhubung, masing-masing citra $f(X_\alpha)$ dan $g(X_\alpha)$ termuat dalam satu komponen terhubung $Y$. Lintasan di atas menunjukkan bahwa kedua komponen tersebut sama. Jadi
$\pi_0(f)(\alpha)=\pi_0(g)(\alpha)$. $\square$
:::

Akibatnya, jika $\pi_0(X)\not\cong\pi_0(Y)$, maka $X$ dan $Y$ tidak mungkin ekuivalen secara homotopi, apalagi homeomorfik.

::: {.exercise #o012-rbt-l04-ex-001}
**Latihan 4.1.** Tunjukkan bahwa funktor
$[*,{-}]\colon\mathbf{Top}\to\mathbf{Set}$ turun menjadi funktor
$[*,{-}]\colon\mathbf{Ho}\to\mathbf{Set}$.
:::

Berikut sebuah fakta yang berguna tentang ruang.

::: {.lemma #o012-rbt-l04-lem-001}
**Lema 4.1 (pelestarian koproduk).** Untuk setiap keluarga ruang
$\{X_\beta\}_{\beta\in J}$, terdapat isomorfisme

$$
\bigsqcup_{\beta\in J}\pi_0(X_\beta)
\xrightarrow{\cong}
\pi_0\!\left(\bigsqcup_{\beta\in J}X_\beta\right)
$$

dan

$$
\bigsqcup_{\beta\in J}[*,X_\beta]
\xrightarrow{\cong}
\left[*,\bigsqcup_{\beta\in J}X_\beta\right].
$$

Pemetaan maju diinduksi oleh keluarga inklusi
$\operatorname{in}_\beta\colon X_\beta\to\bigsqcup_{\gamma\in J}X_\gamma$, sedangkan pemetaan balik mengirim setiap komponen ke suku koproduk tunggal yang memuatnya. Dengan kata lain, $\pi_0$ dan $[*,{-}]$ *melestarikan koproduk*.
:::

Kita telah memperoleh funktor $\pi_0\colon\mathbf{Top}\to\mathbf{Set}$ dan, dengan sedikit penyalahgunaan notasi, funktor
$\pi_0\colon\mathbf{Ho}\to\mathbf{Set}$. Keduanya membentuk segitiga komutatif

$$
\begin{array}{ccc}
\mathbf{Top}&\xrightarrow{\ \pi_0\ }&\mathbf{Set}\\
\downarrow Q&\nearrow_{\pi_0}&\\
\mathbf{Ho}&&
\end{array}
$$

dengan $Q$ mengirim pemetaan kontinu ke kelas homotopinya.

::: {.example #o012-rbt-l04-exa-001}
**Contoh 4.1.** Jika $X$ dan $Y$ adalah ruang dengan
$|\pi_0(X)|<|\pi_0(Y)|$, tidak ada pemetaan kontinu surjektif
$X\to Y$. Memang, pemetaan kontinu surjektif akan menginduksi fungsi surjektif
$\pi_0(X)\to\pi_0(Y)$, yang bertentangan dengan pertidaksamaan kardinalitas tersebut.
:::

Berikut contoh yang instruktif.

::: {.example #o012-rbt-l04-exa-002}
**Contoh 4.2 (kurva sinus topolog).** *Kurva sinus topolog* adalah citra $C$ dari pemetaan

$$
[-1,1]\sqcup(0,1]\longrightarrow\mathbb{R}^2
$$

yang didefinisikan oleh

$$
\begin{cases}
y\longmapsto(0,y),&y\in[-1,1],\\
x\longmapsto\bigl(x,\sin(1/x)\bigr),&x\in(0,1],
\end{cases}
$$

dan diberi **topologi subruang**. Ruang ini merupakan ruang metrik kompak dengan metrik Euklides yang diwariskan.

Faktanya, setiap fungsi kontinu $f\colon C\to\{0,1\}$ bersifat konstan. Pada cabang berosilasi, nilai $f$ konstan karena $(0,1]$ terhubung. Tuliskan nilai itu sebagai $a$. Pada ruas vertikal, nilai $f$ juga konstan; tuliskan sebagai $b$. Karena

$$
\left(\frac{1}{n\pi},0\right)\longrightarrow(0,0)
$$

di $C$, kekontinuan memberikan

$$
b=f(0,0)
=\lim_{n\to\infty}f\!\left(\frac{1}{n\pi},0\right)
=a.
$$

Jadi $C$ terhubung. Akan tetapi, tidak ada lintasan kontinu
$\gamma\colon[0,1]\to C$ dengan
$\gamma(0)=(0,0)$ dan
$\gamma(1)=(1,\sin 1)$. Karena interval terhubung lintasan, $C$ mempunyai tepat dua komponen lintasan, tetapi hanya satu komponen terhubung:

$$
[*,C]\cong\{0,1\},
\qquad
\pi_0(C)=*.
$$
:::

::: {.exercise #o012-rbt-l04-ex-002}
**Latihan 4.2.** Buktikan klaim pada Contoh 4.2 bahwa tidak ada lintasan dari $(0,0)$ ke $(1,\sin 1)$ di dalam $C$. Petunjuk sumber menyarankan agar Anda memeriksa perilaku limit suatu lintasan saat koordinat pertamanya mendekati nol.
:::

Jadi kita mempunyai dua invarian berbeda. Untuk setiap ruang $X$, terdapat pemetaan surjektif kanonik

$$
[*,X]\longrightarrow\pi_0(X)
$$

yang mengirim setiap komponen lintasan ke komponen terhubung yang memuatnya. Selain itu, untuk setiap pemetaan $f\colon X\to Y$, diagram berikut selalu komutatif:

$$
\begin{array}{ccc}
[*,X]&\xrightarrow{[*,f]}&[*,Y]\\
\downarrow&&\downarrow\\
\pi_0(X)&\xrightarrow{\pi_0(f)}&\pi_0(Y).
\end{array}
$$

Inilah sebuah contoh *transformasi natural*.

::: {.definition #o012-rbt-l04-def-001}
**Definisi 4.1 (transformasi natural).** Misalkan
$F,G\colon\mathcal{C}\to\mathcal{D}$ adalah funktor. Sebuah *transformasi natural*
$\alpha\colon F\Rightarrow G$ terdiri atas data berikut: untuk setiap objek $X$ dalam $\mathcal{C}$, dipilih sebuah morfisme

$$
\alpha_X\colon F(X)\longrightarrow G(X),
$$

yang disebut *komponen* $\alpha$ pada $X$. Data ini harus memenuhi syarat bahwa untuk setiap morfisme $f\colon X\to Y$ dalam $\mathcal{C}$, diagram berikut komutatif:

$$
\begin{array}{ccc}
F(X)&\xrightarrow{F(f)}&F(Y)\\
\alpha_X\downarrow&&\downarrow\alpha_Y\\
G(X)&\xrightarrow{G(f)}&G(Y).
\end{array}
$$

Dengan kata lain,

$$
G(f)\circ\alpha_X=\alpha_Y\circ F(f).
$$

Transformasi natural disebut *isomorfisme natural* jika semua komponennya merupakan isomorfisme.
:::

Sebagai contoh, terdapat transformasi natural

$$
\operatorname{disc}\circ U\Rightarrow\operatorname{id}_{\mathbf{Top}}
\colon\mathbf{Top}\longrightarrow\mathbf{Top},
$$

yang komponennya pada $X$ adalah pemetaan identitas kontinu
$\operatorname{disc}(U(X))\to X$, dan transformasi natural

$$
U\Rightarrow\pi_0
\colon\mathbf{Top}\longrightarrow\mathbf{Set},
$$

yang komponennya adalah pemetaan kanonik $U(X)\to\pi_0(X)$.

## Ruang terhubung lintasan semilokal {#o012-rbt-l04-s02}

Kita mencari syarat yang menentukan suatu subkategori penuh dari
$\mathbf{Top}$ sedemikian sehingga komponen

$$
[*,X]\longrightarrow\pi_0(X)
$$

dari transformasi natural $[*,{-}]\Rightarrow\pi_0$ menjadi isomorfisme untuk setiap ruang $X$ dalam subkategori tersebut.

::: {.definition #o012-rbt-l04-def-002}
**Definisi 4.2 (terhubung lintasan semilokal).** Sebuah ruang $X$ disebut *terhubung lintasan semilokal*, disingkat **SLPC**, jika $X$ mempunyai basis lingkungan yang terdiri atas himpunan-himpunan $N$ dengan sifat berikut: untuk setiap $x,y\in N$, terdapat suatu lintasan di $X$ dari $x$ ke $y$.

Lintasan dalam definisi ini tidak disyaratkan tetap berada di dalam $N$.
:::

Sebuah ruang bersifat SLPC jika dan hanya jika setiap komponen lintasannya terbuka. Pernyataan yang tampak mirip dengan “setiap komponen terhubungnya SLPC” tidak memadai: pada $\mathbb{Q}$ dengan topologi subruang, setiap komponen terhubung adalah ruang satu titik dan karenanya SLPC, tetapi $\mathbb{Q}$ sendiri tidak SLPC. Sifat SLPC dipertahankan oleh homeomorfisme: jika $X\cong Y$ dan salah satunya SLPC, maka yang lain juga SLPC.

::: {.proposition #o012-rbt-l04-prop-002}
**Proposisi 4.2.** Jika $X$ merupakan ruang SLPC, maka pemetaan kanonik

$$
[*,X]\longrightarrow\pi_0(X)
$$

adalah isomorfisme.
:::

::: {.proof #o012-rbt-l04-proof-002}
**Bukti.** Kasus $X=\varnothing$ langsung. Untuk setiap $x\in X$, definisikan
$\chi_x\colon X\to\{0,1\}$ dengan

$$
\chi_x(y)=
\begin{cases}
1,&\text{jika terdapat lintasan }y\rightsquigarrow x,\\
0,&\text{jika tidak.}
\end{cases}
$$

Tuliskan

$$
C_x:=\chi_x^{-1}(1),
$$

yakni komponen lintasan yang memuat $x$. Kita akan menunjukkan bahwa $C_x$ terbuka dan tertutup.

Ambil $y\in C_x$ dan pilih lingkungan $V\ni y$ dari basis dalam Definisi 4.2. Untuk setiap $z\in V$, terdapat lintasan $z\rightsquigarrow y$ di $X$. Menggabungkannya dengan lintasan $y\rightsquigarrow x$ menunjukkan bahwa $z\in C_x$. Jadi $V\subseteq C_x$, dan $C_x$ terbuka.

Sebaliknya, ambil $y\in\overline{C_x}$ dan lingkungan basis $V\ni y$. Karena $V\cap C_x\ne\varnothing$, pilih $z\in V\cap C_x$. Sifat $V$ memberikan lintasan $y\rightsquigarrow z$ di $X$, sedangkan $z\in C_x$ memberikan lintasan $z\rightsquigarrow x$. Penggabungan keduanya menghasilkan lintasan $y\rightsquigarrow x$, sehingga $y\in C_x$. Maka
$\overline{C_x}\subseteq C_x$, jadi $C_x$ tertutup.

Sekarang biarkan $K$ menjadi komponen terhubung dari $X$. Ruang $K$ merupakan gabungan komponen-komponen lintasan yang termuat di dalamnya. Setiap komponen lintasan $C\subseteq K$ terbuka di $K$, dan komplemennya di $K$ merupakan gabungan komponen lintasan lain yang juga terbuka. Jadi $C$ terbuka sekaligus tertutup di $K$. Karena $K$ terhubung dan tak kosong, hanya satu komponen lintasan yang termuat di dalam $K$. Dengan demikian komponen lintasan dan komponen terhubung $X$ berimpit, sehingga pemetaan kanonik $[*,X]\to\pi_0(X)$ bijektif. $\square$
:::

Untuk sisa bagian mata kuliah ini, kita akan mempertimbangkan ruang-ruang SLPC. Ruang-ruang tersebut membentuk subkategori penuh

$$
\mathbf{Top}_{\mathrm{slpc}}\hookrightarrow\mathbf{Top}.
$$

Ruang diskret bersifat SLPC, sehingga terdapat pula subkategori
$\mathbf{Set}\hookrightarrow\mathbf{Top}_{\mathrm{slpc}}$ melalui funktor topologi diskret.

::: {.example #o012-rbt-l04-exa-003}
**Contoh 4.3.** Setiap ruang terhubung lintasan $X$ bersifat SLPC. Memang, untuk lingkungan apa pun $N$ dan setiap $x,y\in N$, sudah tersedia lintasan di $X$ yang menghubungkan $x$ dan $y$.
:::

::: {.exercise #o012-rbt-l04-ex-003}
**Latihan 4.3.** Tunjukkan bahwa produk dua ruang SLPC bersifat SLPC, dan bahwa setiap ruang vektor topologis yang konveks lokal bersifat SLPC.
:::

::: {.example #o012-rbt-l04-exa-004}
**Contoh 4.4.** Setiap manifold bersifat SLPC, sebab setiap titik berada dalam suatu peta koordinat yang homeomorfik dengan sebuah subruang terbuka dari $\mathbb{R}^n$, dan bola-bola Euklides yang cukup kecil terhubung lintasan.
:::

Peringatan: subruang dari ruang SLPC belum tentu SLPC. Sebagai contoh, kurva sinus topolog merupakan subruang dari ruang kontraktil $\mathbb{R}^2$, tetapi kurva itu sendiri tidak SLPC.

::: {.question #o012-rbt-l04-q-001}
**Pertanyaan 4.1.** Jika $X$ bersifat SLPC dan
$q\colon X\to Y$ adalah pemetaan hasil bagi, sehingga $Y$ diberi topologi final terhadap $q$, apakah $Y$ juga bersifat SLPC?
:::

## Ruang dan homotopi bertitik {#o012-rbt-l04-s03}

Masih ada satu pokok teknis terakhir.

::: {.definition #o012-rbt-l04-def-003}
**Definisi 4.3 (ruang bertitik).** Sebuah *ruang bertitik* adalah pasangan $(X,x)$, dengan $X$ ruang topologis dan $x\in X$. Pemetaan bertitik

$$
f\colon(X,x)\longrightarrow(Y,y)
$$

adalah pemetaan kontinu $f\colon X\to Y$ yang memenuhi $f(x)=y$. Ruang bertitik dan pemetaan bertitik membentuk kategori $\mathbf{Top}_*$.

Sebuah *homotopi bertitik* antara pemetaan bertitik
$f,g\colon(X,x_0)\to(Y,y_0)$ adalah homotopi
$H\colon I\times X\to Y$ dari $f$ ke $g$ yang juga memenuhi

$$
H(t,x_0)=y_0
\qquad\text{untuk setiap }t\in I.
$$

Kelas homotopi bertitik dari pemetaan bertitik dinotasikan dengan

$$
[(X,x_0),(Y,y_0)]_*.
$$

Kategori $\mathbf{Ho}_*$ didefinisikan secara analog dengan $\mathbf{Ho}$. Kita memperoleh funktor

$$
\pi_0\colon\mathbf{Ho}_*\longrightarrow\mathbf{Set}_*,
$$

dengan titik terpilih pada $\pi_0(X)$ adalah komponen yang memuat $x_0$.
:::

## Ruang penutup {#o012-rbt-l04-s04}

Kadang-kadang, ketika mempelajari suatu ruang tertentu $X$, kita perlu membangun ruang-ruang lain yang berkaitan dengan $X$ untuk menelaah objek yang menarik.

::: {.example #o012-rbt-l04-exa-005}
**Contoh 4.5 (akar kuadrat pada bidang kompleks berlubang).** Ambil

$$
X=\mathbb{C}^{\times}:=\mathbb{C}\setminus\{0\}.
$$

Tidak ada pilihan akar kuadrat yang kontinu pada seluruh $X$; suatu cabang kontinu dapat dipilih setelah sebuah potongan cabang dibuang dari domain. Bahkan, untuk fungsi kontinu
$f\colon\mathbb{C}^{\times}\to\mathbb{C}$, ekspresi
$x\mapsto f(\sqrt{x})$ bergantung pada pilihan akar dan tidak serta-merta memberikan fungsi kontinu global pada $X$.

Namun, kita memperoleh fungsi kontinu jika domainnya diubah. Pemetaan

$$
Z:=\mathbb{C}^{\times}\longrightarrow\mathbb{C}^{\times},
\qquad
z\longmapsto z^2=x,
$$

tidak injektif dan karena itu tidak mempunyai invers global. Jika kita bersedia memakai $Z$ sebagai domain dan memasukkan argumen $z$ yang memenuhi $z^2=x$ ke dalam $f$, kita kembali berurusan dengan fungsi kontinu. Jika
$f(z)=f(-z)$ untuk setiap $z\in Z$, definisikan $g(x)=f(z)$ untuk sembarang $z$ dengan $z^2=x$. Fungsi $g$ terdefinisi dengan baik dan kontinu: pemetaan $p(z)=z^2$ adalah pemetaan terbuka dan surjektif, jadi merupakan pemetaan hasil bagi, dan persamaan $f=g\circ p$ memaksa kekontinuan $g$.
:::

Sifat pemetaan $z\mapsto z^2$ di luar nol, serta pemetaan lain seperti
$z\mapsto z^n$, eksponensial kompleks, dan fungsi rasional di luar kutub serta titik kritisnya, mengarah pada gagasan ruang penutup bagi domain tertentu di $\mathbb{C}$. Kita memakai definisi umum untuk ruang sembarang.

::: {.definition #o012-rbt-l04-def-004}
**Definisi 4.4 (ruang penutup).** Sebuah *ruang penutup* dari $X$ adalah ruang $Z$ yang dilengkapi pemetaan

$$
\pi\colon Z\longrightarrow X
$$

dengan sifat berikut: untuk setiap $x\in X$, terdapat lingkungan terbuka
$V_x\ni x$ dan homeomorfisme

$$
\varphi_x\colon\pi^{-1}(V_x)
\xrightarrow{\cong}
V_x\times\pi^{-1}(x)
$$

di atas $V_x$. Artinya, diagram

$$
\begin{array}{ccc}
\pi^{-1}(V_x)&\xrightarrow{\ \varphi_x\ }&V_x\times\pi^{-1}(x)\\
\pi\downarrow&&\downarrow\operatorname{pr}_1\\
V_x&=&V_x
\end{array}
$$

komutatif, dengan $\pi^{-1}(x)$ diberi topologi diskret. Perhatikan bahwa

$$
V_x\times\pi^{-1}(x)
\cong
\bigsqcup_{z\in\pi^{-1}(x)}V_x.
$$

Pemetaan $\pi$ sendiri juga disebut *pemetaan penutup*.
:::

Untuk ruang penutup $Z\xrightarrow{\pi}X$ dan $x\in X$, tuliskan

$$
Z_x:=\pi^{-1}(x)
$$

untuk *serat* di atas $x$. Ruang $X$ disebut *ruang dasar*.

Contoh ruang penutup mencakup

$$
\exp\colon\mathbb{C}\longrightarrow\mathbb{C}^{\times},
\qquad
S^2\longrightarrow\mathbb{R}\mathrm{P}^2,
\qquad
U(1)\xrightarrow{(-)^n}U(1)\quad(n\geq 1),
$$

serta berbagai penutup ruang berbentuk angka delapan
$S^1\vee S^1$.

::: {.exercise #o012-rbt-l04-ex-004}
**Latihan 4.4.** Misalkan $Z\xrightarrow{\pi}Y$ dan
$Y\xrightarrow{\rho}X$ adalah pemetaan penutup. Andaikan $\rho$ mempunyai serat hingga, yakni $Y_x$ hingga untuk setiap $x\in X$. Tunjukkan bahwa komposisi

$$
Z\xrightarrow{\rho\circ\pi}X
$$

juga merupakan pemetaan penutup.
:::

::: {.proposition #o012-rbt-l04-prop-003}
**Proposisi 4.3.** Untuk ruang penutup $Z\xrightarrow{\pi}X$, jika terdapat lintasan
$x_0\rightsquigarrow x_1$ di $X$, maka terdapat bijeksi—ekuivalen dengan homeomorfisme untuk serat-serat diskret—

$$
Z_{x_0}\cong Z_{x_1}.
$$

Bijeksi tersebut pada umumnya bergantung pada pilihan lintasan. Buktinya dimulai dalam Kuliah 5 dan karena itu berada dalam unit berikutnya.
:::

# Pendamping penguasaan: solusi lengkap {.unnumbered #o012-rbt-l04-mastery}

Bagian ini merupakan materi baru untuk edisi bahasa Indonesia. Seluruh tugas dan pertanyaan dalam Kuliah 4 dijawab lengkap. Bukti Lema 4.1, yang tidak dituliskan dalam sumber, juga diberikan. Proposisi 4.3 sengaja tidak dibuktikan di sini karena pernyataannya berada tepat di batas akhir rentang sumber dan pembahasannya dilanjutkan pada unit berikutnya.

## Solusi Latihan 4.1 {#o012-rbt-l04-sol-001}

Pada objek, tetapkan $X\mapsto[*,X]$. Untuk kelas homotopi
$[f]\in\mathbf{Ho}(X,Y)$, definisikan

$$
[*,[f]]\colon[*,X]\longrightarrow[*,Y],
\qquad
[u]\longmapsto[f\circ u].
$$

Pertama, aturan ini tidak bergantung pada wakil $u$. Jika $u_0\simeq u_1$, maka komposisi suatu homotopi $H\colon I\times *\to X$ dengan $f$ memberi
$f\circ u_0\simeq f\circ u_1$.

Aturan ini juga tidak bergantung pada wakil $f$. Jika $f_0\simeq f_1$ melalui
$K\colon I\times X\to Y$, maka untuk setiap $u\colon *\to X$, pemetaan

$$
(t,*)\longmapsto K(t,u(*))
$$

adalah homotopi $f_0\circ u\simeq f_1\circ u$. Jadi aturan tersebut terdefinisi pada morfisme $[f]$ dalam $\mathbf{Ho}$. Pelestarian identitas dan komposisi mengikuti dari

$$
[\operatorname{id}_X\circ u]=[u],
\qquad
[(g\circ f)\circ u]=[g\circ(f\circ u)].
$$

Maka $[*,{-}]$ turun menjadi funktor $\mathbf{Ho}\to\mathbf{Set}$.

## Bukti Lema 4.1 {#o012-rbt-l04-check-001}

Dalam koproduk topologis

$$
X=\bigsqcup_{\beta\in J}X_\beta,
$$

setiap suku koproduk $X_\beta$ terbuka sekaligus tertutup. Setiap subset terhubung tak kosong dari $X$ harus termuat dalam satu suku koproduk: jika ia bertemu dua suku, fungsi kontinu ke himpunan diskret $J$ yang mencatat indeks suku tidak akan konstan. Sebaliknya, setiap subset terhubung dalam sebuah $X_\beta$ tetap terhubung setelah dimasukkan ke $X$. Karena itu, komponen-komponen terhubung $X$ tepat merupakan komponen-komponen dari semua $X_\beta$, dan diperoleh bijeksi pertama.

Untuk komponen lintasan, ambil lintasan $\gamma\colon I\to X$. Karena $I$ terhubung, citranya harus termuat dalam satu suku koproduk. Jadi dua titik dalam suku berbeda tidak mungkin terhubung oleh lintasan, sedangkan lintasan di suatu $X_\beta$ tetap merupakan lintasan di $X$. Komponen lintasan $X$ pun tepat merupakan komponen lintasan semua suku, yang memberikan bijeksi kedua. Kedua bijeksi diinduksi oleh inklusi suku koproduk dan natural terhadap keluarga pemetaan.

## Solusi Latihan 4.2 {#o012-rbt-l04-sol-002}

Andaikan terdapat lintasan
$\gamma\colon[0,1]\to C$ dari $(0,0)$ ke $(1,\sin 1)$. Tuliskan

$$
\gamma(t)=(a(t),b(t)),
$$

dengan $a,b$ kontinu. Karena $a(0)=0$ dan $a(1)=1$, himpunan
$a^{-1}(0)$ merupakan subset tertutup tak kosong dari $[0,1]$ yang tidak memuat $1$. Maka ia mempunyai unsur terbesar

$$
t_0=\max a^{-1}(0)<1.
$$

Untuk setiap $t>t_0$, kita mempunyai $a(t)>0$, sehingga

$$
b(t)=\sin\!\left(\frac{1}{a(t)}\right).
$$

Pilih dua barisan bilangan positif yang menuju nol,

$$
r_n=\frac{1}{\frac{\pi}{2}+2\pi n},
\qquad
s_n=\frac{1}{\frac{3\pi}{2}+2\pi n}.
$$

Untuk setiap $k$ cukup besar, tetapkan $m_k=a(t_0+1/k)>0$. Pilih indeks $n_k$ sedemikian sehingga $r_{n_k}<m_k$ dan $s_{n_k}<m_k$. Karena $a(t_0)=0$, teorema nilai antara memberikan titik
$u_k,v_k\in(t_0,t_0+1/k)$ dengan

$$
a(u_k)=r_{n_k},
\qquad
a(v_k)=s_{n_k}.
$$

Jadi $u_k\to t_0$ dan $v_k\to t_0$.

Akibatnya,

$$
b(u_k)=1,
\qquad
b(v_k)=-1.
$$

Namun, kekontinuan $b$ di $t_0$ menuntut kedua barisan nilai itu menuju nilai yang sama, yaitu $b(t_0)$. Kontradiksi. Jadi lintasan tersebut tidak ada.

Cabang berosilasi adalah citra kontinu dari $(0,1]$ dan terhubung lintasan, sedangkan ruas vertikal juga terhubung lintasan. Argumen di atas, diterapkan setelah reparametrisasi ujung bila perlu, menunjukkan bahwa tidak ada lintasan yang menghubungkan kedua bagian itu. Dengan demikian keduanya tepat merupakan dua komponen lintasan $C$.

## Solusi Latihan 4.3 {#o012-rbt-l04-sol-003}

Misalkan $X$ dan $Y$ bersifat SLPC. Untuk $(x,y)\in X\times Y$, ambil lingkungan dasar $U\times V$ dengan $U$ dan $V$ berasal dari basis SLPC masing-masing. Jika
$(x_0,y_0),(x_1,y_1)\in U\times V$, pilih lintasan

$$
\alpha\colon I\to X,
\quad
\alpha(0)=x_0,
\quad
\alpha(1)=x_1,
$$

dan

$$
\beta\colon I\to Y,
\quad
\beta(0)=y_0,
\quad
\beta(1)=y_1.
$$

Lintasan $t\mapsto(\alpha(t),\beta(t))$ berada di $X\times Y$ dan menghubungkan kedua titik tersebut. Jadi himpunan-himpunan $U\times V$ membentuk basis SLPC bagi produk.

Sekarang misalkan $E$ ruang vektor topologis yang konveks lokal. Setiap titik mempunyai basis lingkungan berupa translasi himpunan-himpunan konveks. Jika $u$ dan $v$ berada dalam satu lingkungan konveks $N$, lintasan garis

$$
\gamma(t)=(1-t)u+tv
$$

bahkan tetap berada dalam $N$. Karena itu setiap lingkungan basis tersebut memenuhi syarat Definisi 4.2, sehingga $E$ bersifat SLPC.

## Jawaban Pertanyaan 4.1 {#o012-rbt-l04-ans-001}

Ya. Menurut Definisi 4.2, suatu ruang bersifat SLPC jika dan hanya jika setiap komponen lintasannya terbuka.

Untuk arah maju, jika $P$ adalah komponen lintasan dan $y\in P$, pilih lingkungan basis $N\ni y$. Semua titik $N$ dapat dihubungkan ke $y$ oleh lintasan di ruang, sehingga $N\subseteq P$. Jadi $P$ terbuka. Untuk arah balik, jika semua komponen lintasan terbuka, maka himpunan $P_x\cap U$, dengan $P_x$ komponen lintasan $x$ dan $U$ lingkungan terbuka dari $x$, membentuk basis lingkungan. Dua titik di $P_x\cap U$ dapat dihubungkan oleh lintasan di $X$, sebagaimana diperbolehkan oleh Definisi 4.2.

Sekarang biarkan $P$ menjadi sebuah komponen lintasan $Y$. Jika dua titik $x_0,x_1\in X$ berada dalam komponen lintasan yang sama di $X$, citra suatu lintasan di antara keduanya adalah lintasan dari $q(x_0)$ ke $q(x_1)$ di $Y$. Jadi $q^{-1}(P)$ merupakan gabungan komponen-komponen lintasan $X$. Karena $X$ SLPC, setiap komponen itu terbuka, sehingga $q^{-1}(P)$ terbuka. Definisi topologi hasil bagi menyatakan bahwa $P$ terbuka di $Y$ karena $q^{-1}(P)$ terbuka di $X$. Dengan demikian semua komponen lintasan $Y$ terbuka, dan $Y$ bersifat SLPC.

## Solusi Latihan 4.4 {#o012-rbt-l04-sol-004}

Tetapkan $x\in X$. Karena $\rho$ adalah pemetaan penutup, terdapat lingkungan terbuka $U\ni x$ yang tertutup secara merata:

$$
\rho^{-1}(U)=\bigsqcup_{i\in I}U_i,
$$

dengan setiap pembatasan
$\rho_i:=\rho|_{U_i}\colon U_i\to U$ suatu homeomorfisme. Himpunan indeks $I$ berkorespondensi dengan serat $Y_x$, sehingga $I$ hingga.

Untuk setiap $i\in I$, tuliskan
$y_i=\rho_i^{-1}(x)$. Karena $\pi$ adalah pemetaan penutup, pilih lingkungan terbuka
$W_i\subseteq U_i$ dari $y_i$ yang tertutup secara merata oleh $\pi$. Himpunan
$\rho_i(W_i)$ adalah lingkungan terbuka dari $x$ di $U$. Karena $I$ hingga, irisan

$$
V=\bigcap_{i\in I}\rho_i(W_i),
$$

masih merupakan lingkungan terbuka dari $x$; jika $I=\varnothing$, irisan kosong ini dipahami sebagai $U$. Gantikan $U$ dengan $V$ dan setiap $U_i$ dengan
$V_i:=\rho_i^{-1}(V)\subseteq W_i$. Setiap $V_i$ tetap tertutup secara merata oleh $\pi$ dan dipetakan homeomorfik ke $V$ oleh $\rho$.

Untuk setiap $i$, tuliskan dekomposisi penutup

$$
\pi^{-1}(V_i)=\bigsqcup_{j\in J_i}W_{ij},
$$

dengan $\pi|_{W_{ij}}\colon W_{ij}\to V_i$ sebuah homeomorfisme. Maka

$$
(\rho\circ\pi)^{-1}(V)
=\bigsqcup_{i\in I}\bigsqcup_{j\in J_i}W_{ij},
$$

dan pada setiap $W_{ij}$, komposisi

$$
W_{ij}\xrightarrow{\ \pi\ }V_i
\xrightarrow{\ \rho\ }V
$$

merupakan homeomorfisme. Jadi $V$ tertutup secara merata oleh
$\rho\circ\pi$. Karena $x$ dipilih sembarang, komposisi itu merupakan pemetaan penutup.
