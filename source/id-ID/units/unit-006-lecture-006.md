---
title: "Topologi Aljabar"
subtitle: "Unit 6: Ruang Lintasan, Pengangkatan Kontinu, dan Keterhubungan Sederhana Semilokal"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l06-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic Topology* karya David Michael Roberts (2019), tepatnya [`Notes.tex` baris 1305--1515 pada commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex). Rentang itu dimulai dengan penanda Kuliah 6 dan aksi lintasan pada serat ruang penutup, lalu berakhir setelah teorema Wada--Roberts tentang keterhubungan lintasan semilokal ruang pemetaan. Baris 1516 memulai Kuliah 7 dan tidak termasuk dalam unit ini. Karya sumber tersedia di bawah [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah dibaca, pemberian pengenal stabil, dan pemindahan semua keterangan pinggir ke urutan bacaan utama. Koreksi atau klarifikasi substantif yang diterapkan adalah sebagai berikut: contoh penutup eksponensial dibuat konsisten sebagai $p\colon\mathbb{R}\to S^1$, $p(t)=e^{it}$, sehingga serat dan titik akhir pengangkatan benar; hipotesis bagi pemilihan satu titik serat pada setiap komponen lintasan ruang atas dinyatakan; dua salah ketik pada pembahasan faktorisasi dan homotopi diperbaiki; bukti kekontinuan operator pengangkatan diperbaiki dengan kendali eksplisit pada irisan lembaran, menggantikan himpunan yang salah tipe, lingkungan yang tidak didefinisikan, dan klaim kesamaan yang tidak terbukti dalam sumber; contoh manifold memakai bola koordinat yang benar-benar konveks; serta indeks anting-anting Hawaii dibatasi pada $n\geq1$. Semua perbaikan merupakan bagian dari adaptasi independen ini, bukan salinan ungkapan dari sumber lain.

Rentang sumber tidak memuat lingkungan latihan. Bagian pendamping penguasaan menambahkan empat pemeriksaan beserta solusi lengkap: aksi loop pada penutup lingkaran, basis topologi kompak-terbuka, kekontinuan dan kesurjektifan transpor, serta contoh-contoh SLSC. Bukti utama Wada--Roberts tidak diberikan dalam sumber, melainkan dirujuk ke *Handout 1*. Agar unit dapat dipelajari mandiri, pendamping menutup celah itu dengan pembuktian khusus kasus $n=1$ yang diturunkan langsung dari definisi SLSC dan diberi label tegas sebagai materi edisi, bukan sebagai teks Roberts atau reproduksi handout. Seluruh materi pendamping tersedia di bawah CC BY 4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

# Kuliah 6 {#o012-rbt-l06}

## Loop dan aksi pada serat {#o012-rbt-l06-s01}

Hasil Unit 5 dapat dirumuskan lebih kuat sebagai sebuah fungsi

$$
\{\text{lintasan }x_0\rightsquigarrow x_1\text{ di }X\}
\times Z_{x_0}
\longrightarrow Z_{x_1},
\qquad
(\gamma,z)\longmapsto\gamma_*(z).
$$

Jika $x_0=x_1=x$, fungsi itu menjadi

$$
\{\text{loop }x\rightsquigarrow x\text{ di }X\}
\times Z_x
\longrightarrow Z_x.
$$

Setiap loop memberikan bijeksi $Z_x\to Z_x$, sehingga informasi yang sama dapat dipandang sebagai fungsi

$$
\{\text{loop }x\rightsquigarrow x\text{ di }X\}
\longrightarrow\operatorname{Aut}(Z_x),
\qquad
\gamma\longmapsto\gamma_*.
$$

Jika diinginkan, himpunan lintasan atau loop pada rumus-rumus ini dapat terlebih dahulu dibagi menurut reparameterisasi berujung tetap, karena Unit 5 menunjukkan bahwa reparameterisasi tidak mengubah $\gamma_*$.

Untuk ruang penutup bertitik

$$
(Z,z)\xrightarrow{\pi}(X,x),
$$

kita juga memperoleh fungsi kanonik

$$
\{\text{loop }x\rightsquigarrow x\text{ di }X\}
\longrightarrow Z_x,
\qquad
\gamma\longmapsto\gamma_*(z).
\tag{6.1}
$$

::: {.example #o012-rbt-l06-exa-001}
**Contoh 6.1 (penutup trivial dan penutup eksponensial).** Untuk penutup trivial
$Z=S\times X\to X$, transpor setiap lintasan bertindak sebagai identitas pada koordinat $S$:

$$
\gamma_*\colon S\longrightarrow S,
\qquad
\gamma_*=\operatorname{id}_S.
$$

Karena itu, setelah suatu titik $(s,x)$ dipilih, citra fungsi (6.1) hanya terdiri atas satu titik. Setiap ruang penutup dari $I$ bersifat trivial menurut Proposisi 5.2, sehingga fenomena yang sama berlaku di sana.

Sebaliknya, pertimbangkan pemetaan penutup

$$
p\colon\mathbb{R}\longrightarrow S^1,
\qquad
p(t)=e^{it},
$$

dengan titik dasar $x=1\in S^1$ dan $z=0\in\mathbb{R}$. Seratnya adalah

$$
p^{-1}(1)=2\pi\mathbb{Z}.
$$

Fungsi

$$
\{\gamma\colon I\to S^1\mid\gamma(0)=\gamma(1)=1\}
\longrightarrow2\pi\mathbb{Z},
\qquad
\gamma\longmapsto\gamma_*(0),
$$

surjektif. Untuk setiap $n\in\mathbb{Z}$, lintasan

$$
\widetilde{\gamma}_n(t)=2\pi nt
$$

mengangkat loop

$$
\gamma_n(t)=e^{2\pi int},
$$

dan memenuhi

$$
\widetilde{\gamma}_n(0)=0,
\qquad
\widetilde{\gamma}_n(1)=2\pi n.
$$

Perbedaan dengan penutup trivial berserat lebih dari satu titik adalah bahwa
$\mathbb{R}$ terhubung lintasan, sedangkan $X\times S$ tidak terhubung lintasan jika $|S|>1$.
:::

Secara umum, andaikan $(Z,z)\xrightarrow{\pi}(X,x)$ merupakan ruang penutup bertitik dan $Z$ terhubung lintasan. Untuk setiap $z'\in Z_x$, terdapat lintasan

$$
\widetilde{\gamma}\colon I\longrightarrow Z,
\qquad
\widetilde{\gamma}(0)=z,
\quad
\widetilde{\gamma}(1)=z'.
$$

Proyeksinya $\gamma=\pi\circ\widetilde{\gamma}$ adalah loop pada $x$, dan keunikan pengangkatan memberi
$\widetilde{\gamma}=\widetilde{\gamma}_z$. Jadi fungsi (6.1) surjektif. Dengan demikian, lintasan membatasi ukuran serat ruang penutup terhubung, dan ukuran serat juga membatasi kemungkinan lintasan. Himpunan loop pada $X$ sendiri tidak bergantung pada ruang penutup yang dipilih.

Lebih umum lagi, andaikan setiap komponen lintasan $Z_\alpha$ dari $Z$ bertemu serat $Z_x$; kondisi ini berlaku, misalnya, jika $X$ terhubung lintasan. Pilih satu titik
$z_\alpha\in Z_\alpha\cap Z_x$ untuk setiap $\alpha$. Pilihan itu adalah sebuah penampang dari pemetaan kanonik $Z\to[*,Z]$ pada tingkat himpunan. Maka fungsi

$$
\{\text{loop pada }x\}\times[*,Z]
\cong
\{\text{loop pada }x\}\times\{z_\alpha\}
\longrightarrow Z_x,
\qquad
(\gamma,\alpha)\longmapsto\gamma_*(z_\alpha),
\tag{6.2}
$$

selalu surjektif. Memang, setiap $z'\in Z_x$ berada dalam satu komponen $Z_\alpha$, lalu suatu lintasan dalam komponen itu dari $z_\alpha$ ke $z'$ memproyeksikan ke loop yang diperlukan.

Jumlah lintasan biasanya sangat besar. Mengambil hasil bagi terhadap reparameterisasi memang mengurangi redundansi, tetapi kita dapat berbuat lebih banyak: kita dapat memberi topologi pada himpunan lintasan.

## Topologi kompak-terbuka pada ruang lintasan {#o012-rbt-l06-s02}

Serat $Z_x$ dari ruang penutup bersifat diskret, sedangkan himpunan
$\operatorname{Top}(I,X)$ dari semua lintasan $I\to X$ dapat diberi topologi. Jika $X$ metrik, kita dapat memakai metrik supremum

$$
d_\infty(\gamma,\eta)
=\sup_{t\in I}d(\gamma(t),\eta(t)).
$$

Tujuan kita adalah mendefinisikan topologi yang juga berlaku ketika $X$ bukan ruang metrik.

::: {.lemma #o012-rbt-l06-lem-001}
**Lema 6.1 (basis lingkungan kompak-terbuka).** Misalkan $X$ ruang topologis dan
$\gamma\in\operatorname{Top}(I,X)$. Pilih partisi

$$
0=t_0<t_1<\cdots<t_n<t_{n+1}=1
$$

serta himpunan-himpunan terbuka $U_0,\ldots,U_n\subseteq X$ sedemikian sehingga

$$
\gamma([t_i,t_{i+1}])\subseteq U_i
\qquad(0\leq i\leq n),
$$

Definisikan

$$
\begin{aligned}
N_\gamma(&t_1<\cdots<t_n;U_0,\ldots,U_n)\\
:={}&\{\eta\colon I\to X\mid
\eta([t_i,t_{i+1}])\subseteq U_i
\text{ untuk setiap }i\}.
\end{aligned}
$$

Ketika partisi dan himpunan terbuka tersebut bervariasi, himpunan-himpunan
$N_\gamma$ membentuk basis lingkungan pada
$\operatorname{Top}(I,X)$.

Catatan sumber merumuskan hal yang sama dengan lingkungan $U_i$ dan interior $U_i^\circ$, yang didefinisikan di catatan pinggir sebagai gabungan semua himpunan terbuka yang termuat dalam $U_i$. Edisi ini memilih $U_i$ terbuka sejak awal, sehingga $U_i^\circ=U_i$ dan rumusnya ekuivalen.
:::

::: {.definition #o012-rbt-l06-def-001}
**Definisi 6.1 (ruang lintasan).** *Ruang lintasan* $X^I$ adalah himpunan
$\operatorname{Top}(I,X)$ yang dilengkapi topologi dari Lema 6.1. Topologi itu disebut *topologi kompak-terbuka*.
:::

Jika $X$ metrik, topologi kompak-terbuka sama dengan topologi yang dihasilkan oleh metrik supremum. Sifat penting lainnya adalah hukum eksponensial: karena $I$ kompak Hausdorff, untuk setiap ruang $Y$, pemetaan kontinu

$$
H\colon Y\times I\longrightarrow X
$$

berkorespondensi dengan pemetaan kontinu

$$
h\colon Y\longrightarrow X^I,
\qquad
h(y)(t)=H(y,t),
$$

dan sebaliknya. Secara khusus, homotopi $H\colon I\times I\to X$ dapat dipandang sebagai lintasan $h\colon I\to X^I$, dengan

$$
h_s(t)=H(s,t).
$$

::: {.lemma #o012-rbt-l06-lem-002}
**Lema 6.2.** Berlaku dua sifat berikut.

1. Pemetaan evaluasi
   $$
   \operatorname{ev}\colon X^I\times I\longrightarrow X,
   \qquad
   \operatorname{ev}(\gamma,t)=\gamma(t),
   $$
   kontinu.
2. Untuk setiap pemetaan kontinu $f\colon X\to Y$, pemetaan pascakomposisi
   $$
   f_*\colon X^I\longrightarrow Y^I,
   \qquad
   f_*(\gamma)=f\circ\gamma,
   $$
   kontinu.
:::

Untuk $t\in I$, evaluasi pada waktu tetap

$$
\operatorname{ev}_t\colon X^I\longrightarrow X,
\qquad
\operatorname{ev}_t(\gamma)=\gamma(t),
$$

kontinu sebagai komposisi

$$
X^I\cong X^I\times\{t\}
\hookrightarrow X^I\times I
\xrightarrow{\operatorname{ev}}X.
$$

Kasus yang paling sering dipakai adalah $t=0$ dan $t=1$. Untuk $x,y\in X$, definisikan subruang-subruang

$$
\begin{aligned}
P_xX
&:=\{\gamma\in X^I\mid\gamma(0)=x\}
=\operatorname{ev}_0^{-1}(x),\\
P_x^yX
&:=\{\gamma\in X^I\mid\gamma(0)=x,
\ \gamma(1)=y\}\\
&=\operatorname{ev}_0^{-1}(x)\cap\operatorname{ev}_1^{-1}(y),\\
\Omega_xX
&:=P_x^xX
=\{\gamma\in X^I\mid\gamma(0)=x=\gamma(1)\}.
\end{aligned}
$$

Dua ruang terakhir sudah muncul sebelumnya, tetapi tanpa topologinya. Lintasan di dalam $P_x^yX$ berkorespondensi dengan homotopi antarlintasan yang mempertahankan kedua titik ujung. Karena itu, komponen lintasan ruang-ruang pemetaan ini berkaitan langsung dengan kelas homotopi lintasan relatif terhadap titik ujung.

## Kekontinuan operator pengangkatan {#o012-rbt-l06-s03}

Transformasi natural

$$
\operatorname{id}\Rightarrow\operatorname{disc}\pi_0
\colon\mathbf{Top}_{\mathrm{slpc}}
\longrightarrow\mathbf{Top}_{\mathrm{slpc}}
$$

mempunyai sifat universal berikut. Jika $S$ diskret, $X$ SLPC, dan
$f\colon X\to S$ kontinu, terdapat tepat satu fungsi
$\bar f\colon\pi_0(X)\to U(S)$ yang membuat diagram

$$
\begin{array}{ccc}
X&\xrightarrow{\ f\ }&S\\
q\downarrow&\nearrow_{\operatorname{disc}(\bar f)}&\\
\operatorname{disc}(\pi_0(X))&&
\end{array}
$$

komutatif. Di sini $q$ mengirim setiap titik ke komponen terhubungnya.

Sekarang ambil ruang penutup $Z\to X$. Fungsi transpor Unit 5 memberikan

$$
A\colon P_x^yX\times Z_x\longrightarrow Z_y,
\qquad
A(\gamma,z)=\gamma_*(z).
\tag{6.3}
$$

Jika $A$ kontinu, karena $Z_y$ diskret fungsi itu konstan pada komponen terhubung dan memfaktor sebagai

$$
P_x^yX\times Z_x
\longrightarrow
\pi_0(P_x^yX\times Z_x)
\cong
\pi_0(P_x^yX)\times Z_x
\longrightarrow Z_y.
$$

Isomorfisma tengah ada karena $Z_x$ diskret. Jika $Z$ terhubung lintasan dan suatu
$z\in Z_x$ ditetapkan, kita memperoleh fungsi surjektif

$$
\pi_0(P_x^yX)\longrightarrow Z_y.
$$

Hal ini semakin membatasi topologi ruang lintasan dan serat yang mungkin dimiliki ruang penutup. Namun, masih ada dua persoalan:

1. kita belum mengetahui bahwa fungsi pengangkatan lintasan kontinu;
2. kita belum mengetahui bahwa $P_x^yX$ bersifat SLPC, sehingga belum dapat menyamakan komponen lintasan dengan komponen terhubungnya.

Untuk menangani persoalan pertama, kita tingkatkan sifat pengangkatan lintasan tunggal menjadi sebuah fungsi kontinu. Definisikan hasil kali serat

$$
X^I\times_X Z
:=\{(\gamma,z)\in X^I\times Z\mid\gamma(0)=\pi(z)\}
$$

dan operator

$$
\operatorname{Lift}\colon X^I\times_X Z\longrightarrow Z^I,
\qquad
\operatorname{Lift}(\gamma,z)=\widetilde{\gamma}_z.
$$

Fungsi ini sudah terdefinisi oleh Teorema 5.1; yang harus dibuktikan sekarang adalah kekontinuannya. Setelah itu, fungsi (6.3) dapat ditulis sebagai komposisi

$$
P_x^yX\times Z_x
\hookrightarrow X^I\times_X Z
\xrightarrow{\operatorname{Lift}}Z^I
\xrightarrow{\operatorname{ev}_1}Z,
$$

yang citranya termuat dalam $Z_y$.

::: {.theorem #o012-rbt-l06-thm-001}
**Teorema 6.1.** Fungsi

$$
\operatorname{Lift}\colon X^I\times_X Z\longrightarrow Z^I
$$

kontinu.
:::

::: {.proof #o012-rbt-l06-proof-001}
**Bukti.** Tetapkan $(\gamma,z)\in X^I\times_X Z$, dan tuliskan

$$
\widetilde{\gamma}
=\operatorname{Lift}(\gamma,z).
$$

Ambil lingkungan dasar

$$
N_{\widetilde{\gamma}}
=N_{\widetilde{\gamma}}(t_1<\cdots<t_n;U_0,\ldots,U_n)
$$

dari $\widetilde{\gamma}$ dalam $Z^I$. Kita akan membangun lingkungan
$M(\gamma,z)$ yang dipetakan oleh $\operatorname{Lift}$ ke dalam
$N_{\widetilde{\gamma}}$.

Karena $\pi$ merupakan homeomorfisma lokal dan $I$ kompak, kita dapat memperhalus partisi menjadi

$$
0=s_0<s_1<\cdots<s_m=1
$$

yang memuat semua titik $t_j$, serta memilih lembaran-lembaran terbuka
$W_1,\ldots,W_m\subseteq Z$ sedemikian sehingga, untuk setiap $k$,

$$
\widetilde{\gamma}([s_{k-1},s_k])\subseteq W_k
\subseteq U_{j(k)},
$$

subinterval $[s_{k-1},s_k]$ termuat dalam
$[t_{j(k)},t_{j(k)+1}]$, dan pembatasan

$$
\pi|_{W_k}\colon W_k\xrightarrow{\cong}V_k:=\pi(W_k)
$$

merupakan homeomorfisma ke himpunan terbuka $V_k\subseteq X$.

Pada setiap titik sambung $s_k$, kedua lembaran $W_k$ dan $W_{k+1}$ memuat
$\widetilde{\gamma}(s_k)$. Pilih lingkungan terbuka

$$
Q_k\ni\widetilde{\gamma}(s_k),
\qquad
Q_k\subseteq W_k\cap W_{k+1},
$$

yang dipetakan homeomorfik oleh $\pi$ ke lingkungan terbuka
$R_k:=\pi(Q_k)$ dari $\gamma(s_k)$.

Definisikan lingkungan terbuka $B$ dari $\gamma$ dalam $X^I$ dengan

$$
B
:=
N_\gamma(s_1<\cdots<s_{m-1};V_1,\ldots,V_m)
\cap
\bigcap_{k=1}^{m-1}\operatorname{ev}_{s_k}^{-1}(R_k).
$$

Lalu tetapkan

$$
M(\gamma,z)
:=(B\times W_1)\cap(X^I\times_X Z).
$$

Ini merupakan lingkungan terbuka $(\gamma,z)$ dalam hasil kali serat.

Ambil $(\eta,w)\in M(\gamma,z)$ dan tuliskan
$\widetilde{\eta}=\operatorname{Lift}(\eta,w)$. Pada subinterval pertama, lintasan

$$
t\longmapsto(\pi|_{W_1})^{-1}(\eta(t))
$$

adalah pengangkatan $\eta|_{[s_0,s_1]}$ yang berawal di $w$. Oleh keunikan pengangkatan,
$\widetilde{\eta}([s_0,s_1])\subseteq W_1$. Karena
$\eta(s_1)\in R_1$ dan prapeta $R_1$ pada lembaran $W_1$ termuat dalam
$Q_1\subseteq W_2$, titik $\widetilde{\eta}(s_1)$ juga berada dalam $W_2$.

Argumen yang sama dapat diulang secara induktif. Kita memperoleh

$$
\widetilde{\eta}([s_{k-1},s_k])\subseteq W_k
\subseteq U_{j(k)}
$$

untuk setiap $k$. Karena partisi $s_k$ memperhalus partisi $t_j$, hal ini menunjukkan

$$
\widetilde{\eta}\in N_{\widetilde{\gamma}}.
$$

Jadi

$$
M(\gamma,z)
\subseteq
\operatorname{Lift}^{-1}(N_{\widetilde{\gamma}}).
$$

Setiap lingkungan dasar dari $\widetilde{\gamma}$ mempunyai prapeta yang merupakan lingkungan $(\gamma,z)$. Maka $\operatorname{Lift}$ kontinu. $\square$
:::

::: {.remark #o012-rbt-l06-rem-001}
**Catatan 6.1.** Keunikan pengangkatan menunjukkan bahwa
$\operatorname{Lift}$ sebenarnya bijektif, bahkan homeomorfisma. Inversnya adalah

$$
(\pi_*,\operatorname{ev}_0)
\colon Z^I\longrightarrow X^I\times_X Z,
\qquad
\lambda\longmapsto(\pi\circ\lambda,\lambda(0)).
$$

Pemetaan invers itu kontinu menurut Lema 6.2. Komposisi pada kedua arah adalah identitas karena setiap lintasan $\lambda$ merupakan pengangkatan tunggal dari
$\pi\circ\lambda$ dengan nilai awal $\lambda(0)$.
:::

Dengan demikian fungsi transpor

$$
P_x^yX\times Z_x\longrightarrow Z_y
$$

kontinu dan menghasilkan fungsi

$$
\pi_0(P_x^yX)\times Z_x\longrightarrow Z_y.
$$

Kita masih ingin mengetahui bahwa dua titik $\gamma,\eta\in P_x^yX$ dalam komponen terhubung yang sama dapat dihubungkan oleh lintasan dalam $P_x^yX$. Lintasan seperti itu setara dengan homotopi

$$
H\colon I\times I\longrightarrow X
$$

dari $\gamma$ ke $\eta$ yang *mempertahankan titik ujung*, yaitu

$$
H(0,t)=\gamma(t),
\qquad
H(1,t)=\eta(t)
\qquad
\text{untuk setiap }t\in I,
$$

dan

$$
H(s,0)=x,
\qquad
H(s,1)=y
\qquad
\text{untuk setiap }s\in I.
$$

## Ruang terhubung sederhana semilokal {#o012-rbt-l06-s04}

::: {.definition #o012-rbt-l06-def-002}
**Definisi 6.2 (terhubung sederhana semilokal).** Dalam konvensi mata kuliah ini, sebuah ruang $X$ disebut *terhubung sederhana semilokal*, disingkat **SLSC**, jika setiap titik mempunyai basis lingkungan terbuka $N$ dengan kedua sifat berikut:

1. $N$ terhubung lintasan;
2. untuk setiap $x,y\in N$ dan setiap dua lintasan
   $\gamma,\eta\in P_x^yN$, terdapat homotopi di $X$ dari $\gamma$ ke $\eta$ yang mempertahankan titik ujung.

Lintasan-lintasan awal berada di dalam $N$, sedangkan homotopinya diperbolehkan bergerak di seluruh $X$. Ini adalah syarat teknis terakhir pada ruang yang diperlukan dalam bagian mata kuliah ini.

Peringatan istilah: konvensi ini menggabungkan dua syarat yang sering dipisahkan dalam pustaka, yakni *terhubung lintasan lokal* dan *terhubung sederhana semilokal* dalam arti standar. Dengan keterhubungan lintasan lokal, Definisi 6.2 setara dengan adanya basis lingkungan terhubung lintasan $N$ sehingga homomorfisma yang diinduksi inklusi $\pi_1(N,u)\to\pi_1(X,u)$ trivial untuk setiap $u\in N$. Istilah SLSC tanpa syarat tambahan dalam arti standar tidak dengan sendirinya menyiratkan SLPC.
:::

Setiap ruang SLSC bersifat SLPC, sebab basis lingkungan dalam Definisi 6.2 khususnya terdiri atas himpunan-himpunan terhubung lintasan.

::: {.example #o012-rbt-l06-exa-002}
**Contoh 6.2.** Setiap manifold bersifat SLSC. Untuk manifold tanpa batas, di dalam suatu peta koordinat kita dapat memilih lingkungan yang citranya merupakan bola Euklides kecil. Untuk manifold dengan batas, gunakan setengah bola yang konveks dalam peta koordinat batas. Dalam kedua kasus citra itu konveks, sehingga dua lintasan di dalamnya yang mempunyai titik ujung sama dapat dihubungkan oleh homotopi garis lurus yang mempertahankan titik ujung.
:::

::: {.example #o012-rbt-l06-exa-003}
**Contoh 6.3 (anting-anting Hawaii).** *Anting-anting Hawaii* adalah subruang

$$
\mathbb{H}
:=
\bigcup_{n\geq1}
\left\{(u,v)\in\mathbb{R}^2
\mathrel{\Big|}
\left\|(u,v)-\left(\frac1n,0\right)\right\|
=\frac1n
\right\}.
$$

Ruang ini tidak SLSC. Setiap lingkungan titik $(0,0)$ memuat seluruh lingkaran penyusun untuk semua $n$ yang cukup besar. Loop yang mengitari salah satu lingkaran itu tidak dapat dikontraksikan bahkan di dalam seluruh $\mathbb{H}$.
:::

::: {.theorem #o012-rbt-l06-thm-002}
**Teorema 6.2 (Wada 1955; diperkuat oleh Roberts 2010).** Jika $X$ terhubung sederhana semilokal, maka ruang-ruang

$$
X^I,
\qquad
P_xX,
\qquad
P_x^yX,
\qquad
\text{dan karenanya }\Omega_xX,
$$

bersifat terhubung lintasan semilokal.

Atribusi yang dicantumkan dalam sumber: H. Wada, “Local connectivity of mapping spaces,” *Duke Mathematical Journal* **22**(3), 1955, hlm. 419--425; dan D. M. Roberts, [“Fundamental bigroupoids and 2-covering spaces,” Teorema 5.12](https://ncatlab.org/davidroberts/files/DMRthesis_final.pdf) (2010). Teorema 6.2 adalah kasus $n=1$ dari hasil Roberts tersebut.
:::

::: {.proof #o012-rbt-l06-proof-002}
**Bukti (tidak diujikan dalam catatan sumber).** Sumber merujuk pembaca ke *Handout 1*. Argumen lengkap tidak terdapat dalam rentang sumber unit ini dan tidak direkonstruksi sebagai seolah-olah merupakan teks Roberts. Sebagai pengganti untuk keperluan belajar mandiri, bagian pendamping di bawah memberikan pembuktian kasus $n=1$ yang diturunkan secara independen dari definisi-definisi unit ini dan dilabeli sebagai materi edisi. $\square$
:::

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l06-mastery}

Bagian ini merupakan materi baru untuk edisi bahasa Indonesia dan tersedia di bawah CC BY 4.0. Keempat pemeriksaan berikut dapat dikerjakan tanpa sumber tambahan dan semuanya disertai solusi lengkap. Bagian terakhir memberikan bukti mandiri khusus kasus Teorema 6.2 yang digunakan dalam mata kuliah ini; bukti tersebut merupakan kontribusi edisi dan bukan reproduksi *Handout 1*.

::: {.exercise #o012-rbt-l06-mcheck-001}
**Pemeriksaan penguasaan 6.1 (aksi loop pada penutup lingkaran).** Untuk
$p(t)=e^{it}\colon\mathbb{R}\to S^1$, tentukan transpor pada serat
$2\pi\mathbb{Z}$ yang dihasilkan oleh loop
$\gamma_n(t)=e^{2\pi int}$. Tunjukkan pula bahwa penggabungan loop dengan bilangan putaran $m$ dan $n$ menghasilkan transpor dengan bilangan putaran $m+n$.
:::

## Solusi Pemeriksaan 6.1 {#o012-rbt-l06-sol-001}

Jika titik awal pada serat ditulis $2\pi k$, pengangkatan tunggal adalah

$$
\widetilde{\gamma}_{n,k}(t)=2\pi k+2\pi nt,
$$

sebab

$$
p(\widetilde{\gamma}_{n,k}(t))
=e^{i(2\pi k+2\pi nt)}
=e^{2\pi int}
=\gamma_n(t).
$$

Karena titik akhirnya $2\pi(k+n)$, transpor bertindak sebagai translasi

$$
(\gamma_n)_*\colon2\pi k\longmapsto2\pi(k+n).
$$

Jika loop berputaran $m$ diikuti loop berputaran $n$, pengangkatan bagian kedua dimulai di
$2\pi(k+m)$ dan berakhir di $2\pi(k+m+n)$. Jadi transpor gabungan adalah translasi sebesar
$2\pi(m+n)$, sama dengan komposisi kedua transpor.

::: {.exercise #o012-rbt-l06-mcheck-002}
**Pemeriksaan penguasaan 6.2 (basis dan pemetaan dasar ruang lintasan).** Mulai dari definisi standar topologi kompak-terbuka dengan subbasis

$$
[K,O]:=\{\eta\colon I\to X\mid\eta(K)\subseteq O\},
$$

dengan $K\subseteq I$ kompak dan $O\subseteq X$ terbuka. Buktikan Lema 6.1 dan kedua bagian Lema 6.2. Jika $X$ metrik, buktikan pula bahwa topologi ini sama dengan topologi metrik supremum. Terakhir, buktikan hukum eksponensial

$$
\operatorname{Top}(Y\times I,X)
\cong
\operatorname{Top}(Y,X^I)
$$

untuk setiap ruang $Y$.
:::

## Solusi Pemeriksaan 6.2 {#o012-rbt-l06-sol-002}

Setiap lingkungan pada Lema 6.1 adalah irisan berhingga

$$
N_\gamma(t_1<\cdots<t_n;U_0,\ldots,U_n)
=\bigcap_{i=0}^{n}
\bigl[[t_i,t_{i+1}],U_i\bigr],
$$

sehingga terbuka dalam topologi kompak-terbuka.

Sebaliknya, ambil lingkungan dasar

$$
\mathcal{W}=\bigcap_{j=1}^{r}[K_j,O_j]
$$

yang memuat $\gamma$. Semua $K_j$ kompak, dan karena $I$ Hausdorff, semuanya tertutup. Untuk setiap $t\in I$, pilih interval terbuka relatif $A_t\ni t$ dengan sifat berikut: jika $t\in K_j$, maka
$A_t\subseteq\gamma^{-1}(O_j)$; jika $t\notin K_j$, maka
$A_t\cap K_j=\varnothing$. Pilihan serentak ini mungkin karena hanya ada berhingga banyak $j$.

Sampul $\{A_t\}_{t\in I}$ mempunyai bilangan Lebesgue. Pilih partisi cukup halus sehingga setiap $[t_i,t_{i+1}]$ termuat dalam suatu $A_{a_i}$. Definisikan

$$
J_i:=\{j\mid[t_i,t_{i+1}]\cap K_j\ne\varnothing\},
\qquad
U_i:=\bigcap_{j\in J_i}O_j,
$$

dengan irisan kosong dipahami sebagai $X$. Dari sifat $A_{a_i}$ diperoleh
$\gamma([t_i,t_{i+1}])\subseteq U_i$. Jika
$\eta\in N_\gamma(t_1<\cdots<t_n;U_0,\ldots,U_n)$ dan $s\in K_j$, setiap subinterval partisi yang memuat $s$ mempunyai $j\in J_i$, sehingga
$\eta(s)\in O_j$. Jadi $N_\gamma\subseteq\mathcal{W}$, dan keluarga pada Lema 6.1 memang merupakan basis lingkungan.

Untuk kekontinuan evaluasi, tetapkan $(\gamma,t)$ dan lingkungan terbuka
$O\ni\gamma(t)$. Prapeta $\gamma^{-1}(O)$ terbuka di $I$, sehingga terdapat lingkungan relatif terbuka $J$ dari $t$ yang penutupannya $K=\overline J$ kompak dan termuat dalam $\gamma^{-1}(O)$. Maka

$$
[K,O]\times J
$$

adalah lingkungan $(\gamma,t)$ yang dipetakan evaluasi ke $O$.

Untuk pascakomposisi, cukup diperiksa pada subbasis. Bagi $K\subseteq I$ kompak dan
$O\subseteq Y$ terbuka,

$$
(f_*)^{-1}([K,O])
=[K,f^{-1}(O)],
$$

yang terbuka dalam $X^I$. Jadi $f_*$ kontinu.

Sekarang andaikan $X$ metrik. Pertama, ambil lingkungan subdasar $[K,O]$ dari $\gamma$. Himpunan kompak $\gamma(K)$ termuat dalam himpunan terbuka $O$, sehingga terdapat $\varepsilon>0$ dengan

$$
\{x\in X\mid d(x,\gamma(K))<\varepsilon\}\subseteq O.
$$

Karena itu bola metrik supremum $B_\infty(\gamma,\varepsilon)$ termuat dalam $[K,O]$. Sebaliknya, untuk $\varepsilon>0$, kekontinuan seragam $\gamma$ pada interval kompak memberi partisi cukup halus sehingga citra setiap subinterval termuat dalam bola berjari-jari $\varepsilon/3$ terhadap suatu nilai $\gamma(a_i)$. Pilih

$$
U_i=B\!\left(\gamma(a_i),\frac{2\varepsilon}{3}\right).
$$

Lingkungan $N_\gamma(t_1<\cdots<t_n;U_0,\ldots,U_n)$ lalu termuat dalam $B_\infty(\gamma,\varepsilon)$ menurut pertidaksamaan segitiga. Kedua topologi jadi sama.

Terakhir, misalkan $H\colon Y\times I\to X$ kontinu dan definisikan $h(y)(t)=H(y,t)$. Untuk menunjukkan $h$ kontinu, ambil $y_0\in h^{-1}([K,O])$. Bagi setiap $t\in K$, kekontinuan $H$ memberi lingkungan $W_t\ni y_0$ dan $V_t\ni t$ dengan

$$
H(W_t\times V_t)\subseteq O.
$$

Kekompakan $K$ memberi subkeluarga berhingga $V_{t_1},\ldots,V_{t_r}$ yang menutupi $K$. Irisan $W=\bigcap_jW_{t_j}$ adalah lingkungan $y_0$ dan memenuhi $H(W\times K)\subseteq O$, jadi $W\subseteq h^{-1}([K,O])$. Maka $h$ kontinu. Sebaliknya, jika $h\colon Y\to X^I$ kontinu, maka

$$
H=\operatorname{ev}\circ(h\times\operatorname{id}_I)
$$

kontinu menurut Lema 6.2. Kedua pengubahan ini saling invers, sehingga hukum eksponensial terbukti.

::: {.exercise #o012-rbt-l06-mcheck-003}
**Pemeriksaan penguasaan 6.3 (transpor kontinu dan surjektif).** Gunakan Teorema 6.1 dan Lema 6.2 untuk membuktikan bahwa
$A\colon P_x^yX\times Z_x\to Z_y$ kontinu. Jika $Z$ terhubung lintasan dan
$z\in Z_x$, buktikan bahwa fungsi terinduksi
$\pi_0(P_x^yX)\to Z_y$ surjektif.
:::

## Solusi Pemeriksaan 6.3 {#o012-rbt-l06-sol-003}

Inklusi

$$
P_x^yX\times Z_x\hookrightarrow X^I\times_X Z
$$

kontinu. Menurut Teorema 6.1, $\operatorname{Lift}$ kontinu, dan menurut Lema 6.2,
$\operatorname{ev}_1\colon Z^I\to Z$ kontinu. Maka komposisi

$$
(\gamma,w)
\longmapsto
\operatorname{ev}_1(\operatorname{Lift}(\gamma,w))
=\gamma_*(w)
$$

kontinu. Citranya berada di subruang diskret $Z_y$, sehingga inilah kekontinuan $A$.

Sekarang tetapkan $z\in Z_x$ dan ambil sembarang $w\in Z_y$. Karena $Z$ terhubung lintasan, pilih lintasan
$\lambda\colon I\to Z$ dari $z$ ke $w$. Proyeksi
$\gamma=\pi\circ\lambda$ berada dalam $P_x^yX$. Lintasan $\lambda$ adalah pengangkatan $\gamma$ yang berawal di $z$, sehingga keunikan pengangkatan memberi

$$
A(\gamma,z)=\gamma_*(z)=w.
$$

Jadi $A(-,z)$ surjektif. Karena $Z_y$ diskret dan $A(-,z)$ kontinu, ia konstan pada setiap komponen terhubung $P_x^yX$ dan turun menjadi fungsi surjektif
$\pi_0(P_x^yX)\to Z_y$.

::: {.exercise #o012-rbt-l06-mcheck-004}
**Pemeriksaan penguasaan 6.4 (SLSC dan dua contoh).** Buktikan langsung bahwa setiap ruang SLSC bersifat SLPC. Jelaskan secara rinci mengapa manifold memenuhi Definisi 6.2 dan mengapa anting-anting Hawaii tidak memenuhinya.
:::

## Solusi Pemeriksaan 6.4 {#o012-rbt-l06-sol-004}

Basis pada Definisi 6.2 terdiri atas lingkungan-lingkungan $N$ yang terhubung lintasan. Jadi, untuk setiap dua titik $u,v\in N$, terdapat lintasan di $N$, dan khususnya di $X$, dari $u$ ke $v$. Ini persis memenuhi syarat basis dalam definisi SLPC Unit 4.

Untuk manifold tanpa batas, pilih peta koordinat $\varphi\colon N\to C$ yang citranya $C$ merupakan bola Euklides terbuka; pada titik batas manifold dengan batas, pilih sebagai $C$ sebuah setengah bola yang konveks. Karena $C$ konveks, ia terhubung lintasan. Jika
$\gamma,\eta\colon I\to N$ mempunyai titik ujung sama, tuliskan $\bar\gamma=\varphi\circ\gamma$ dan $\bar\eta=\varphi\circ\eta$, lalu definisikan dalam koordinat

$$
\bar H(s,t)=(1-s)\bar\gamma(t)+s\bar\eta(t),
\qquad
H=\varphi^{-1}\circ\bar H.
$$

Kekonveksan $C$ menjamin $\bar H(s,t)\in C$, sedangkan kesamaan titik ujung menjamin
$H(s,0)$ dan $H(s,1)$ tetap. Jadi $H$ membuktikan syarat SLSC.

Untuk anting-anting Hawaii $\mathbb H$, setiap lingkungan relatif dari $(0,0)$ memuat lingkaran penuh
$C_n$ untuk semua $n$ yang cukup besar. Untuk satu $n$ tetap, terdapat retraksi kontinu

$$
r_n\colon\mathbb H\longrightarrow C_n
$$

yang merupakan identitas pada $C_n$ dan meruntuhkan setiap $C_m$ dengan $m\ne n$ ke titik $(0,0)$. Jika loop yang mengitari $C_n$ dapat dikontraksikan dalam $\mathbb H$, komposisi kontraksi itu dengan $r_n$ akan mengontraksikan loop pembangkit di lingkaran $C_n$, yang mustahil. Jadi setiap lingkungan $(0,0)$ memuat loop yang tetap tidak dapat dikontraksikan di seluruh ruang. Tidak mungkin ada basis lingkungan di $(0,0)$ yang memenuhi Definisi 6.2; maka $\mathbb H$ tidak SLSC.

## Bukti mandiri Teorema 6.2 untuk kasus yang digunakan {.unnumbered #o012-rbt-l06-check-001}

**Materi edisi.** Kita membuktikan langsung bahwa jika $X$ SLSC menurut Definisi 6.2, maka $X^I$, $P_xX$, dan $P_x^yX$ memenuhi definisi SLPC Unit 4. Kasus $\Omega_xX=P_x^xX$ lalu langsung mengikuti. Ingat bahwa definisi SLPC hanya meminta dua titik dalam satu lingkungan basis dapat dihubungkan oleh lintasan di ruang keseluruhan; lintasan penghubung tidak harus tetap berada dalam lingkungan basis itu.

Tetapkan $\gamma\in X^I$ dan suatu lingkungan dasar kompak-terbuka

$$
\mathcal U
=N_\gamma(t_1<\cdots<t_n;U_0,\ldots,U_n).
$$

Karena $X$ SLSC, kekompakan $I$, dan Lema 6.1, kita dapat memperhalus partisi menjadi

$$
0=s_0<s_1<\cdots<s_m=1
$$

yang memuat semua $t_j$, lalu memilih lingkungan basis SLSC terbuka
$V_1,\ldots,V_m$ sehingga

$$
\gamma([s_{k-1},s_k])\subseteq V_k
\subseteq U_{j(k)}
$$

dan $[s_{k-1},s_k]\subseteq[t_{j(k)},t_{j(k)+1}]$. Kedua himpunan
$V_k$ dan $V_{k+1}$ memuat $\gamma(s_k)$. Pilih lingkungan basis SLSC terbuka

$$
L_k\ni\gamma(s_k),
\qquad
L_k\subseteq V_k\cap V_{k+1}
\quad(1\leq k<m).
$$

Pilih pula $L_0\subseteq V_1$ dan $L_m\subseteq V_m$ dari basis yang sama pada kedua titik ujung. Definisikan

$$
\mathcal V
:=
N_\gamma(s_1<\cdots<s_{m-1};V_1,\ldots,V_m)
\cap
\bigcap_{k=0}^{m}\operatorname{ev}_{s_k}^{-1}(L_k).
$$

Himpunan $\mathcal V$ adalah lingkungan terbuka $\gamma$ dan termuat dalam
$\mathcal U$.

Ambil sembarang $\eta,\zeta\in\mathcal V$. Karena setiap $L_k$ terhubung lintasan, pilih lintasan

$$
\delta_k\colon I\longrightarrow L_k
$$

dari $\eta(s_k)$ ke $\zeta(s_k)$. Untuk subinterval ke-$k$, tuliskan
$\eta_k$ dan $\zeta_k$ bagi reparameterisasi pembatasan $\eta$ dan $\zeta$ ke
$[s_{k-1},s_k]$. Kedua lintasan komposit

$$
\eta_k*\delta_k
\qquad\text{dan}\qquad
\delta_{k-1}*\zeta_k
$$

berada dalam $V_k$ dan mempunyai titik awal serta titik akhir yang sama. Sifat SLSC bagi $V_k$ memberikan homotopi di $X$ di antara kedua lintasan itu yang mempertahankan titik ujung. Secara ekuivalen, loop batas yang dibentuk oleh
$\eta_k$, $\delta_k$, lintasan balik $\zeta_k$, dan lintasan balik
$\delta_{k-1}$ mempunyai pengisian disk di $X$. Setelah disk diidentifikasi dengan persegi, kita memperoleh homotopi persegi yang sisi bawahnya $\eta_k$, sisi atasnya $\zeta_k$, dan kedua sisi tegaknya $\delta_{k-1}$ serta $\delta_k$.

Homotopi-homotopi persegi untuk $k=1,\ldots,m$ memiliki sisi tegak yang sama pada setiap batas bersama. Lema penempelan karena itu menghasilkan homotopi kontinu

$$
H\colon I\times I\longrightarrow X
$$

dari $\eta$ ke $\zeta$. Menurut hukum eksponensial, $H$ adalah lintasan di $X^I$ dari $\eta$ ke $\zeta$. Jadi setiap dua titik dalam $\mathcal V$ dapat dihubungkan oleh lintasan dalam $X^I$. Karena lingkungan awal $\mathcal U$ sembarang, lingkungan-lingkungan seperti $\mathcal V$ membentuk basis SLPC bagi $X^I$.

Untuk $P_xX$, lakukan konstruksi yang sama di dalam subruang dan pilih
$\delta_0$ sebagai lintasan konstan di $x$. Homotopi hasil penempelan lalu memenuhi

$$
H(s,0)=x
$$

untuk semua $s$, sehingga seluruh lintasan di ruang pemetaan tetap berada dalam $P_xX$. Untuk $P_x^yX$, pilih juga $\delta_m$ sebagai lintasan konstan di $y$; dengan demikian

$$
H(s,0)=x,
\qquad
H(s,1)=y
$$

untuk semua $s$. Irisan lingkungan-lingkungan $\mathcal V$ dengan subruang masing-masing membentuk basis relatif yang memenuhi syarat SLPC. Maka
$P_xX$ dan $P_x^yX$ bersifat SLPC, dan mengambil $y=x$ memberi hasil untuk
$\Omega_xX$. $\square$
