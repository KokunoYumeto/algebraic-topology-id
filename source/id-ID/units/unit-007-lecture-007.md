---
title: "Topologi Aljabar"
subtitle: "Unit 7: Konkatenasi Loop, Grup Fundamental, dan Funktorialitas"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l07-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic Topology* karya David Michael Roberts (2019), tepatnya [`Notes.tex` baris 1516--1770 pada commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L1516-L1770). Rentang itu dimulai dengan penanda Kuliah 7 dan pertanyaan tentang transpor sepanjang lintasan yang dikonkatenasi, lalu berakhir setelah funktorialitas grup fundamental. Baris 1771 memulai Kuliah 8 dan tidak termasuk dalam unit ini. Karya sumber tersedia di bawah [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah dibaca, pemberian pengenal stabil, serta pemindahan tugas dan gambar dari catatan pinggir ke urutan bacaan utama. Sepuluh grafik TikZ pinggir diganti dengan rumus eksplisit bagi keenam pemetaan parameter $\phi,\psi,\alpha,\beta,\mu,\nu$; dengan demikian semua informasi matematisnya tetap tersedia dalam bentuk yang dapat dibaca perangkat bantu. Koreksi substantif yang diterapkan adalah: notasi serat $Z_{\gamma(0)}$ diperbaiki; label dua grafik asosiativitas diselaraskan dengan rumusnya; homotopi afin yang keliru karena mengulang $\phi$ diperbaiki agar benar-benar menginterpolasi $\phi$ dan $\psi$; kata “terhubung” pada contoh $S^2$ diperkuat menjadi “terhubung lintasan,” sesuai hipotesis yang dipakai; dan arah aksi transpor dijelaskan secara eksplisit sebagai aksi kanan—atau, setelah membalik loop, sebagai representasi kiri—agar urutan komposisi tidak tersamarkan.

Rentang sumber tidak memberikan bukti bagi lema transpor-konkatenasi, proposisi funktor ruang loop, atau akibat funktorialitas $\pi_1$. Kekontinuan operasi konkatenasi diserahkan ke *Assignment 2*, dan identifikasi dengan kelas homotopi bertitik $S^1\to X$ diberikan sebagai latihan pinggir. Bagian pendamping penguasaan menutup semuanya dengan empat pemeriksaan beserta solusi lengkap dan mandiri. Seluruh materi pendamping tersedia di bawah CC BY 4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

# Kuliah 7 {#o012-rbt-l07}

## Konkatenasi dan transpor serat {#o012-rbt-l07-s01}

Apa yang terjadi pada isomorfisme

$$
\gamma_*\colon Z_x\longrightarrow Z_y
$$

jika lintasan $\gamma\colon I\to X$ dipecah menjadi dua sublintasan
$x\rightsquigarrow x'\rightsquigarrow y$, lalu isomorfisme-isomorfisme yang bersesuaian dikomposisikan?

Misalkan $\gamma,\eta\colon I\to X$ memenuhi
$\gamma(1)=\eta(0)$. *Konkatenasi* keduanya adalah lintasan
$\gamma\#\eta\colon I\to X$ yang didefinisikan oleh

$$
(\gamma\#\eta)(t)
=
\begin{cases}
\gamma(2t),&0\leq t\leq\frac12,\\
\eta(2t-1),&\frac12\leq t\leq1.
\end{cases}
$$

Kekontinuan mengikuti dari lema penempelan karena kedua rumus bernilai sama pada
$t=\frac12$.

::: {.lemma #o012-rbt-l07-lem-001}
**Lema 7.1 (transpor menghormati konkatenasi).** Jika
$\gamma,\eta\colon I\to X$ dan $\gamma(1)=\eta(0)$, maka

$$
(\gamma\#\eta)_*
=\eta_*\circ\gamma_*
\colon Z_{\gamma(0)}\longrightarrow Z_{\eta(1)}.
$$
:::

Secara khusus, jika $\gamma,\eta\in\Omega_xX$, maka
$\gamma\#\eta\in\Omega_xX$. Fungsi

$$
\Omega_xX\longrightarrow\operatorname{Aut}(Z_x),
\qquad
\gamma\longmapsto\gamma_*,
$$

kompatibel dengan konkatenasi dalam urutan yang dinyatakan Lema 7.1. Akan tetapi, konkatenasi tidak asosiatif sebagai kesamaan literal lintasan berparameter.

::: {.example #o012-rbt-l07-exa-001}
**Contoh 7.1 (kegagalan asosiativitas literal).** Ambil $X=S^1$ dan
$\gamma(t)=e^{2\pi it}$. Maka

$$
((\gamma\#\gamma)\#\gamma)(t)
=
\begin{cases}
e^{8\pi it},&0\leq t\leq\frac12,\\
e^{4\pi it},&\frac12\leq t\leq1,
\end{cases}
$$

sedangkan

$$
(\gamma\#(\gamma\#\gamma))(t)
=
\begin{cases}
e^{4\pi it},&0\leq t\leq\frac12,\\
e^{8\pi it},&\frac12\leq t\leq1.
\end{cases}
$$

Keduanya menempuh loop dasar tiga kali, tetapi dengan jadwal yang berbeda. Sebagai contoh, pada $t=\frac14$, lintasan pertama bernilai $1$, sedangkan lintasan kedua bernilai $-1$.
:::

## Hukum grup hingga homotopi {#o012-rbt-l07-s02}

Mari periksa kembali cara lintasan dikonkatenasi. Untuk
$\gamma(1)=\eta(0)$, terdapat fungsi kontinu alami

$$
\langle\gamma,\eta\rangle\colon[0,2]\longrightarrow X
$$

yang menempuh $\gamma$ pada $[0,1]$ dan $\eta$ pada $[1,2]$. Konkatenasi
$\gamma\#\eta$ diperoleh dengan melakukan prakomposisi terhadap
$t\mapsto2t\colon[0,1]\to[0,2]$.

Jika ditambahkan lintasan ketiga $\lambda$ dengan $\lambda(0)=\eta(1)$, definisikan

$$
\langle\gamma,\eta,\lambda\rangle\colon[0,3]\longrightarrow X
$$

dengan menempuh ketiga lintasan secara berurutan pada interval satuan berturut-turut. Dua cara memasang tanda kurung diperoleh melalui prakomposisi terhadap

$$
\phi(t)
=
\begin{cases}
4t,&0\leq t\leq\frac12,\\
2t+1,&\frac12\leq t\leq1,
\end{cases}
$$

dan

$$
\psi(t)
=
\begin{cases}
2t,&0\leq t\leq\frac12,\\
4t-1,&\frac12\leq t\leq1.
\end{cases}
$$

Lebih tepatnya,

$$
(\gamma\#\eta)\#\lambda
=\langle\gamma,\eta,\lambda\rangle\circ\phi,
\qquad
\gamma\#(\eta\#\lambda)
=\langle\gamma,\eta,\lambda\rangle\circ\psi.
$$

Kedua lintasan $\phi,\psi\colon I\to[0,3]$ mempunyai titik ujung yang sama. Homotopi afin

$$
h(s,t)=(1-s)\phi(t)+s\psi(t)
$$

mempertahankan titik ujung dan menghubungkan $\phi$ dengan $\psi$. Komposisi

$$
(s,t)\longmapsto
\langle\gamma,\eta,\lambda\rangle(h(s,t))
$$

memberikan homotopi berujung tetap dari
$(\gamma\#\eta)\#\lambda$ ke
$\gamma\#(\eta\#\lambda)$. Jadi konkatenasi lintasan *asosiatif hingga homotopi*.

Sekarang ambil sembarang lintasan $\gamma\colon I\to X$ dan definisikan lintasan balik

$$
\bar\gamma(t):=\gamma(1-t).
$$

Konkatenasi dengan lintasan balik difaktorkan melalui dua pemetaan parameter

$$
\gamma\#\bar\gamma=\gamma\circ\alpha,
\qquad
\alpha(t)=
\begin{cases}
2t,&0\leq t\leq\frac12,\\
2-2t,&\frac12\leq t\leq1,
\end{cases}
$$

dan

$$
\bar\gamma\#\gamma=\gamma\circ\beta,
\qquad
\beta(t)=
\begin{cases}
1-2t,&0\leq t\leq\frac12,\\
2t-1,&\frac12\leq t\leq1.
\end{cases}
$$

Grafik $\alpha$ bergerak dari $0$ ke $1$ lalu kembali ke $0$, sedangkan grafik
$\beta$ bergerak dari $1$ ke $0$ lalu kembali ke $1$. Homotopi-homotopi afin

$$
a(s,t)=(1-s)\alpha(t)
$$

dan

$$
b(s,t)=(1-s)\beta(t)+s
$$

masing-masing menghubungkan $\alpha$ ke fungsi konstan $0$ dan $\beta$ ke fungsi konstan $1$, sambil mempertahankan titik ujung. Setelah dikomposisikan dengan $\gamma$, kita memperoleh

$$
\gamma\#\bar\gamma\simeq c_{\gamma(0)},
\qquad
\bar\gamma\#\gamma\simeq c_{\gamma(1)}
$$

relatif terhadap titik ujung. Jadi lintasan balik merupakan invers hingga homotopi.

Untuk identitas hingga homotopi, gunakan lintasan konstan

$$
c_x\colon I\longrightarrow X,
\qquad
c_x(t)=x.
$$

Kita mempunyai faktorisasi

$$
\gamma\#c_{\gamma(1)}=\gamma\circ\mu,
\qquad
\mu(t)=
\begin{cases}
2t,&0\leq t\leq\frac12,\\
1,&\frac12\leq t\leq1,
\end{cases}
$$

dan

$$
c_{\gamma(0)}\#\gamma=\gamma\circ\nu,
\qquad
\nu(t)=
\begin{cases}
0,&0\leq t\leq\frac12,\\
2t-1,&\frac12\leq t\leq1.
\end{cases}
$$

Masing-masing $\mu$ dan $\nu$ homotopik relatif titik ujung dengan
$\operatorname{id}_I$, melalui

$$
m(s,t)=(1-s)\mu(t)+st,
\qquad
n(s,t)=(1-s)\nu(t)+st.
$$

Komposisi dengan $\gamma$ menghasilkan

$$
\gamma\#c_{\gamma(1)}\simeq\gamma,
\qquad
c_{\gamma(0)}\#\gamma\simeq\gamma
$$

relatif terhadap titik ujung.

Jika kelima homotopi—satu asosiativitas, dua invers, dan dua identitas—dipandang sebagai lintasan dalam $X^I$, maka untuk loop-loop pada $x$ semuanya merupakan lintasan dalam $\Omega_xX$. Jadi operasi biner

$$
\#\colon\Omega_xX\times\Omega_xX\longrightarrow\Omega_xX
$$

memenuhi hukum grup hingga keberadaan lintasan:

$$
\begin{aligned}
(\gamma\#\eta)\#\lambda
&\rightsquigarrow\gamma\#(\eta\#\lambda),\\
\gamma\#\bar\gamma
&\rightsquigarrow c_x,\\
\bar\gamma\#\gamma
&\rightsquigarrow c_x,\\
\gamma\#c_x
&\rightsquigarrow\gamma,\\
c_x\#\gamma
&\rightsquigarrow\gamma.
\end{aligned}
$$

Lebih banyak koherensi sebenarnya tersedia: homotopi-homotopi tersebut sendiri dapat dirangkai secara koheren untuk berbagai pilihan tanda kurung. Misalnya, catatan sumber menyebut keluarga bertipe

$$
I\times\Omega_xX\times\Omega_xX\times\Omega_xX
\longrightarrow\Omega_xX.
$$

Catatan sumber tidak membuktikan struktur tingkat lebih tinggi itu.

::: {.proposition #o012-rbt-l07-prop-001}
**Proposisi 7.1.** Misalkan $(X,x)$ ruang bertitik dan $X$ bersifat SLSC. Himpunan

$$
\pi_0(\Omega_xX)
$$

mempunyai struktur grup. Perkaliannya diinduksi oleh konkatenasi loop, unsur identitasnya diwakili oleh loop konstan $c_x$, dan invers kelas $[\gamma]$ diwakili oleh
$\bar\gamma$.

Jika hanya bekerja dengan ruang yang tidak diketahui SLSC, gunakan himpunan komponen lintasan
$[*,\Omega_xX]$ sebagai gantinya.
:::

::: {.proof #o012-rbt-l07-proof-001}
**Bukti.** Operasi konkatenasi

$$
\#\colon\Omega_xX\times\Omega_xX\longrightarrow\Omega_xX
$$

kontinu; inilah tugas yang dirujuk sumber sebagai *Assignment 2*, dan pembuktiannya diberikan dalam Pemeriksaan Penguasaan 7.2. Karena $X$ SLSC, Teorema 6.2 menyatakan bahwa $\Omega_xX$ SLPC. Maka komponen terhubung dan komponen lintasannya berimpit.

Menerapkan $\pi_0$ pada $\#$ memberi

$$
\pi_0(\Omega_xX\times\Omega_xX)
\longrightarrow\pi_0(\Omega_xX).
$$

Untuk ruang SLPC $M,N$, pemetaan kanonik

$$
\pi_0(M\times N)
\xrightarrow{\cong}
\pi_0(M)\times\pi_0(N)
$$

adalah bijeksi. Karena itu diperoleh perkalian

$$
\pi_0(\Omega_xX)\times\pi_0(\Omega_xX)
\longrightarrow\pi_0(\Omega_xX),
\qquad
([\gamma],[\eta])\longmapsto[\gamma\#\eta].
$$

Kelima lintasan dalam $\Omega_xX$ yang dibangun di atas menunjukkan bahwa perkalian kelas bersifat asosiatif, $[c_x]$ merupakan identitas dua sisi, dan
$[\bar\gamma]$ merupakan invers dua sisi $[\gamma]$. Jadi aksioma grup terpenuhi. $\square$
:::

::: {.definition #o012-rbt-l07-def-001}
**Definisi 7.1 (grup fundamental).** Untuk ruang bertitik $(X,x)$, *grup fundamental di $x$* adalah

$$
\pi_1(X,x):=[*,\Omega_xX],
$$

yakni himpunan komponen lintasan ruang loop, dengan perkalian yang diinduksi konkatenasi. Jika $X$ SLSC, Teorema 6.2 dan Proposisi 4.2 memberikan identifikasi

$$
\pi_1(X,x)\cong\pi_0(\Omega_xX).
$$

Ingat bahwa funktor $[*,{-}]$ turun menjadi funktor
$\mathbf{Ho}\to\mathbf{Set}$, sebagaimana dibuktikan dalam pendamping Unit 4.
:::

## Grup fundamental dan serat ruang penutup {#o012-rbt-l07-s03}

Penalaran sebelumnya memberi aksi transpor pada serat. Menurut Teorema 6.1, pemetaan

$$
\Omega_xX\times Z_x\longrightarrow Z_x,
\qquad
(\gamma,z)\longmapsto\gamma_*(z),
$$

kontinu. Homotopi loop berujung tetap adalah lintasan dalam $\Omega_xX$, sedangkan
$Z_x$ diskret. Karena itu transpor konstan sepanjang homotopi tersebut dan turun ke kelas dalam $\pi_1(X,x)$.

Dengan konvensi perkalian kronologis

$$
[\gamma]\,[\eta]:=[\gamma\#\eta]
$$

(menempuh $\gamma$ lebih dahulu, kemudian $\eta$), rumus Lema 7.1 berarti bahwa

$$
z\cdot[\gamma]:=\gamma_*(z)
$$

adalah **aksi kanan** $\pi_1(X,x)$ pada $Z_x$:

$$
(z\cdot[\gamma])\cdot[\eta]
=z\cdot([\gamma][\eta]).
$$

Jika representasi kiri lebih disukai, definisikan

$$
\rho\colon\pi_1(X,x)\longrightarrow\operatorname{Aut}(Z_x),
\qquad
\rho([\gamma])=(\bar\gamma)_*.
$$

Karena $\overline{\gamma\#\eta}=\bar\eta\#\bar\gamma$, Lema 7.1 memberikan

$$
\rho([\gamma][\eta])
=\rho([\gamma])\circ\rho([\eta]),
$$

sehingga $\rho$ benar-benar homomorfisme grup. Untuk ruang SLPC yang tidak SLSC, konstruksi yang sama tetap bekerja dengan kelas homotopi berujung tetap; asumsi SLSC hanya membuat pendekatan melalui komponen terhubung ruang fungsi lebih langsung.

Jika $Z$ terhubung lintasan dan $z\in Z_x$ dipilih, pemetaan orbit

$$
\pi_1(X,x)\longrightarrow Z_x,
\qquad
[\gamma]\longmapsto\gamma_*(z),
$$

surjektif. Jadi kardinalitas serat ruang penutup terhubung lintasan dibatasi dari atas oleh banyaknya kelas homotopi loop. Sebaliknya, serat sebuah ruang penutup terhubung lintasan memberi batas bawah bagi banyaknya kelas homotopi loop yang berbeda di $X$.

::: {.example #o012-rbt-l07-exa-002}
**Contoh 7.2.** Proyeksi

$$
S^2\longrightarrow\mathbb{R}\mathrm{P}^2
$$

adalah ruang penutup dengan serat dua titik, dan $S^2$ terhubung lintasan. Karena itu terdapat sedikitnya dua kelas homotopi loop di
$\mathbb{R}\mathrm{P}^2$ pada setiap titik dasar. Salah satunya adalah kelas loop konstan, sehingga ada loop di $\mathbb{R}\mathrm{P}^2$ yang tidak homotopik relatif titik ujung dengan loop konstan.
:::

::: {.example #o012-rbt-l07-exa-003 data-source-label="eg:piS^1_infinite"}
**Contoh 7.3.** Pemetaan penutup

$$
\exp(2\pi i{-})\colon\mathbb{R}\longrightarrow S^1,
\qquad
t\longmapsto e^{2\pi it},
$$

mempunyai serat $\mathbb{Z}$ di atas $1\in S^1$. Ruang atas
$\mathbb{R}$ terhubung lintasan, sehingga terdapat surjeksi
$\pi_1(S^1,1)\to\mathbb{Z}$. Akibatnya, $\pi_1(S^1,1)$ merupakan grup tak hingga.
:::

## Funktorialitas ruang loop dan grup fundamental {#o012-rbt-l07-s04}

::: {.proposition #o012-rbt-l07-prop-002}
**Proposisi 7.2.** Konstruksi ruang loop merupakan funktor

$$
\Omega\colon\mathbf{Top}_*\longrightarrow\mathbf{Top}_*.
$$

Pada objek, $\Omega(X,x)=(\Omega_xX,c_x)$. Pada pemetaan bertitik
$f\colon(X,x)\to(Y,y)$, funktor ini bertindak melalui pascakomposisi
$\Omega f(\gamma)=f\circ\gamma$.
:::

::: {.corollary #o012-rbt-l07-cor-001}
**Akibat 7.1.** Grup fundamental merupakan funktor

$$
\pi_1:=[*,{-}]\circ\Omega
\colon\mathbf{Top}_*\longrightarrow\mathbf{Grp}.
$$

Pada subkategori penuh ruang-ruang SLSC, funktor ini teridentifikasi secara natural dengan
$\pi_0\circ\Omega$ setelah setiap $\pi_0(\Omega_xX)$ diberi struktur grup Proposisi 7.1. Selain itu, terdapat isomorfisme natural

$$
\pi_1(X,x)
\cong
[(S^1,1),(X,x)]_*,
$$

yang pembuktiannya diberikan dalam Pemeriksaan Penguasaan 7.4.
:::

Bukti lengkap Proposisi 7.2 dan bagian funktorial Akibat 7.1 juga diberikan dalam Pemeriksaan Penguasaan 7.4.

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l07-mastery}

Bagian ini merupakan materi baru untuk edisi bahasa Indonesia dan tersedia di bawah CC BY 4.0. Empat pemeriksaan berikut menutup semua bukti dan tugas yang ditinggalkan sumber pada rentang Kuliah 7.

::: {.exercise #o012-rbt-l07-mcheck-001}
**Pemeriksaan penguasaan 7.1 (bukti Lema 7.1).** Buktikan bahwa transpor serat menghormati konkatenasi lintasan.
:::

## Solusi Pemeriksaan 7.1 {#o012-rbt-l07-sol-001}

Ambil $z\in Z_{\gamma(0)}$ dan tuliskan

$$
z':=\gamma_*(z)=\widetilde{\gamma}_z(1).
$$

Lintasan terangkat

$$
\widetilde{\gamma}_z\#\widetilde{\eta}_{z'}
$$

berawal di $z$. Proyeksinya adalah

$$
\pi\circ
(\widetilde{\gamma}_z\#\widetilde{\eta}_{z'})
=(\pi\circ\widetilde{\gamma}_z)
\#(\pi\circ\widetilde{\eta}_{z'})
=\gamma\#\eta.
$$

Jadi lintasan itu merupakan pengangkatan $\gamma\#\eta$ yang berawal di $z$. Keunikan pengangkatan memberikan

$$
\widetilde{(\gamma\#\eta)}_z
=\widetilde{\gamma}_z\#\widetilde{\eta}_{z'}.
$$

Evaluasi pada $t=1$ menghasilkan

$$
(\gamma\#\eta)_*(z)
=\eta_*(z')
=\eta_*(\gamma_*(z)).
$$

Karena berlaku untuk setiap $z$, diperoleh
$(\gamma\#\eta)_*=\eta_*\circ\gamma_*$.

::: {.exercise #o012-rbt-l07-mcheck-002}
**Pemeriksaan penguasaan 7.2 (kekontinuan konkatenasi).** Buktikan bahwa

$$
\#\colon\Omega_xX\times\Omega_xX\longrightarrow\Omega_xX
$$

kontinu untuk topologi kompak-terbuka.
:::

## Solusi Pemeriksaan 7.2 {#o012-rbt-l07-sol-002}

Definisikan pemetaan tiga variabel (sebelum mengambil adjoinnya)

$$
C\colon(\Omega_xX\times\Omega_xX)\times I\longrightarrow X
$$

dengan

$$
C(\gamma,\eta,t)
=
\begin{cases}
\gamma(2t),&0\leq t\leq\frac12,\\
\eta(2t-1),&\frac12\leq t\leq1.
\end{cases}
$$

Pada dua subruang tertutup
$(\Omega_xX\times\Omega_xX)\times[0,\frac12]$ dan
$(\Omega_xX\times\Omega_xX)\times[\frac12,1]$, masing-masing rumus kontinu karena merupakan komposisi evaluasi dengan pemetaan parameter kontinu. Pada irisan $t=\frac12$, kedua rumus bernilai $x$, sebab $\gamma(1)=x=\eta(0)$. Lema penempelan menunjukkan bahwa $C$ kontinu.

Karena $I$ kompak Hausdorff, hukum eksponensial topologi kompak-terbuka menyatakan bahwa pemetaan teradjung

$$
\widehat C\colon\Omega_xX\times\Omega_xX\longrightarrow X^I,
\qquad
\widehat C(\gamma,\eta)(t)=C(\gamma,\eta,t),
$$

kontinu. Citra $\widehat C$ berada dalam subruang $\Omega_xX$, dan pemetaan ke subruang itu tepat merupakan $\#$. Maka konkatenasi kontinu.

::: {.exercise #o012-rbt-l07-mcheck-003}
**Pemeriksaan penguasaan 7.3 (komponen dan aksi).** Lengkapi dua rincian dalam Proposisi 7.1: buktikan bahwa komponen suatu produk adalah produk komponen, dan jelaskan mengapa homotopi-homotopi pada bagian utama benar-benar memberikan aksioma grup pada kelas. Kemudian verifikasi konvensi aksi kanan pada serat.
:::

## Solusi Pemeriksaan 7.3 {#o012-rbt-l07-sol-003}

Misalkan $C_m$ dan $C_n$ adalah komponen terhubung yang memuat titik
$m\in M$ dan $n\in N$. Produk $C_m\times C_n$ terhubung dan memuat $(m,n)$. Sebaliknya, jika $A\subseteq M\times N$ terhubung dan memuat $(m,n)$, kedua proyeksinya terhubung, sehingga

$$
\operatorname{pr}_M(A)\subseteq C_m,
\qquad
\operatorname{pr}_N(A)\subseteq C_n.
$$

Jadi $A\subseteq C_m\times C_n$. Maka komponen terhubung yang memuat $(m,n)$ tepat
$C_m\times C_n$, dan diperoleh bijeksi

$$
\pi_0(M\times N)\cong\pi_0(M)\times\pi_0(N).
$$

Pada $\Omega_xX$, setiap homotopi berujung tetap adalah lintasan dalam ruang loop. Karena itu dua sisi setiap hukum pada bagian utama berada dalam komponen lintasan yang sama. Setelah mengambil kelas, tanda
$\rightsquigarrow$ berubah menjadi kesamaan. Maka

$$
([\gamma][\eta])[\lambda]
=[\gamma]([\eta][\lambda]),
$$

$$
[\gamma][\bar\gamma]
=[c_x]
=[\bar\gamma][\gamma],
$$

dan

$$
[\gamma][c_x]
=[\gamma]
=[c_x][\gamma].
$$

Terakhir, dengan $z\cdot[\gamma]=\gamma_*(z)$, Lema 7.1 memberikan

$$
(z\cdot[\gamma])\cdot[\eta]
=\eta_*(\gamma_*(z))
=(\gamma\#\eta)_*(z)
=z\cdot([\gamma][\eta]),
$$

dan loop konstan bertindak sebagai identitas. Jadi ini benar-benar aksi kanan.

::: {.exercise #o012-rbt-l07-mcheck-004}
**Pemeriksaan penguasaan 7.4 (funktorialitas dan model lingkaran).** Buktikan Proposisi 7.2 dan Akibat 7.1. Kemudian bangun secara eksplisit isomorfisme natural

$$
\pi_1(X,x)
\cong[(S^1,1),(X,x)]_*.
$$
:::

## Solusi Pemeriksaan 7.4 {#o012-rbt-l07-sol-004}

Pada objek, definisikan

$$
\Omega(X,x):=(\Omega_xX,c_x).
$$

Untuk pemetaan bertitik $f\colon(X,x)\to(Y,y)$, definisikan

$$
\Omega f\colon\Omega_xX\longrightarrow\Omega_yY,
\qquad
(\Omega f)(\gamma)=f\circ\gamma.
$$

Pemetaan ini kontinu menurut Lema 6.2, dan bertitik karena
$f\circ c_x=c_y$. Selain itu,

$$
\Omega(\operatorname{id})=\operatorname{id},
\qquad
\Omega(g\circ f)=\Omega g\circ\Omega f.
$$

Jadi $\Omega$ merupakan funktor $\mathbf{Top}_*\to\mathbf{Top}_*$.

Funktor $[*,{-}]$ mengirim ruang bertitik ke himpunan komponen lintasannya. Pada ruang loop, konkatenasi memberi struktur grup pada himpunan ini. Pemetaan $\Omega f$ mempertahankan konkatenasi secara literal:

$$
(\Omega f)(\gamma\#\eta)
=(f\circ\gamma)\#(f\circ\eta),
$$

serta mempertahankan loop konstan dan lintasan balik. Karena itu pemetaan terinduksi

$$
\pi_1(f)\colon\pi_1(X,x)\longrightarrow\pi_1(Y,y),
\qquad
[\gamma]\longmapsto[f\circ\gamma],
$$

adalah homomorfisme grup. Identitas dan komposisi dipertahankan karena sifat yang sama berlaku bagi $\Omega$, sehingga $\pi_1$ merupakan funktor ke
$\mathbf{Grp}$. Jika $X$ SLSC, Teorema 6.2 mengidentifikasi komponen lintasan dan komponen terhubung $\Omega_xX$ secara natural, yang memberi deskripsi
$\pi_1\cong\pi_0\circ\Omega$.

Sekarang ambil pemetaan hasil bagi

$$
q\colon I\longrightarrow I/\{0\sim1\}\cong S^1,
\qquad
q(t)=e^{2\pi it}.
$$

Setiap loop $\gamma\colon I\to X$ pada $x$ mempunyai
$\gamma(0)=\gamma(1)$, sehingga menurut sifat universal hasil bagi terdapat tepat satu pemetaan bertitik kontinu

$$
\gamma^\sharp\colon(S^1,1)\longrightarrow(X,x)
$$

dengan $\gamma^\sharp\circ q=\gamma$. Sebaliknya, setiap pemetaan bertitik
$u\colon(S^1,1)\to(X,x)$ menghasilkan loop $u\circ q$. Kedua konstruksi saling invers.

Jika $H\colon I\times I\to X$ merupakan homotopi loop yang mempertahankan titik ujung, maka $H(s,0)=H(s,1)=x$ untuk setiap $s$. Pemetaan

$$
\operatorname{id}_I\times q\colon I\times I\longrightarrow I\times S^1
$$

adalah pemetaan hasil bagi: ia merupakan surjeksi kontinu dari ruang kompak ke ruang Hausdorff. Karena $H$ konstan pada setiap seratnya, sifat universal hasil bagi memberi tepat satu homotopi bertitik $H^\sharp\colon I\times S^1\to X$. Sebaliknya, prakomposisi homotopi bertitik dengan $\operatorname{id}_I\times q$ menghasilkan homotopi loop berujung tetap. Jadi bijeksi di atas turun menjadi

$$
\pi_1(X,x)
\xrightarrow{\cong}
[(S^1,1),(X,x)]_*.
$$

Faktorisasi melalui $q$ dan pengambilan kembali dengan prakomposisi oleh $q$ bersifat natural. Untuk setiap pemetaan bertitik
$f\colon(X,x)\to(Y,y)$, pembentukan kelas memenuhi

$$
(f\circ\gamma)^\sharp=f\circ\gamma^\sharp.
$$

Dengan demikian isomorfisme tersebut natural. Untuk memeriksa perkalian, tuliskan $\iota_1,\iota_2\colon S^1\to S^1\vee S^1$ bagi kedua inklusi dan definisikan pemetaan jepit $p\colon S^1\to S^1\vee S^1$ melalui

$$
p(q(t))=
\begin{cases}
\iota_1(q(2t)),&0\leq t\leq\frac12,\\
\iota_2(q(2t-1)),&\frac12\leq t\leq1.
\end{cases}
$$

Kedua rumus bertemu di titik baji dan sama pada $t=0,1$, sehingga lema penempelan dan sifat hasil bagi $q$ memberi pemetaan bertitik kontinu $p$. Untuk pemetaan bertitik $u,v\colon S^1\to X$, pemetaan baji $u\vee v$ memenuhi

$$
\bigl((u\vee v)\circ p\bigr)\circ q
=(u\circ q)\#(v\circ q).
$$

Jadi perkalian yang diinduksi $p$ tepat bersesuaian dengan konkatenasi loop. Isomorfisme natural di atas merupakan isomorfisme grup.
