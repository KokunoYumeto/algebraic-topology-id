---
title: "Topologi Aljabar"
subtitle: "Unit 14: Menuju Klasifikasi Ruang Penutup"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l14-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 3047--3209 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L3047-L3209)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang itu dimulai dengan kata “Recall” dan penanda Kuliah 14 pada baris
3047, lalu berakhir sesudah catatan tentang komponen ruang penutup pada baris
3208 dan baris kosong 3209. Penanda Kuliah 15 pada baris 3210 tidak termasuk
dalam unit ini. Materi sumber dan adaptasi Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/).

Judul bagian sumber “Classifying covering spaces” berada pada baris 3045 dan
sudah dipertahankan sebagai judul penunjuk ke depan pada akhir Unit 13. Unit 14
langsung melanjutkan isi di bawah judul tersebut tanpa menggandakan judul
sumber. Sesuai istilah global edisi, *covering space* selanjutnya diterjemahkan
sebagai *ruang penutup*.

Perubahan edisi mencakup penerjemahan, pemformatan ulang agar mudah dibaca,
pemberian pengenal stabil, serta pemindahan kelima catatan pinggir ke urutan
bacaan utama. Ketiga diagram Xy-pic sumber ditulis ulang sebagai gambar
semantik yang juga mencantumkan daftar panah dan persamaan komutativitas;
maknanya tidak bergantung pada posisi visual.

Sejumlah cacat sumber diperbaiki secara independen. Dua aksi pada contoh
lingkaran dibatasi ke grup bertitik $\pi_1(S^1,1)$ dan kodomainnya ditulis
sebagai grup permutasi himpunan, bukan $\operatorname{Aut}$ yang dapat keliru
dibaca sebagai automorfisma grup siklik. Aksi monodromi langsung tetap berupa
aksi kanan, konsisten dengan urutan konkatenasi kronologis yang ditetapkan pada
Unit 7--10. Karena itu kategori himpunan-$G$ ditulis sebagai kategori aksi
kanan dan dekomposisi orbit memakai koset kanan
$\operatorname{Stab}(p)\backslash G$. Pemetaan yang salah ketik
$\pi_1(X_i,a_i)\to Z_{a_i}$ diganti oleh pemetaan aksi bertipe benar
$Z_{a_i}\times\pi_1(X_i,a_i)\to Z_{a_i}$. Notasi penampang dan himpunan titik
pilihan dipisahkan, dependensi pada pilihan dinyatakan, dan salah eja serta
kalimat tak gramatikal sumber dinormalkan.

Sumber menyerahkan dua bukti sebagai “Exercise” dan tidak memberikan bukti
bagi lema tentang $[\mathbf BG,\mathbf{Set}]$. Pendamping penguasaan yang jelas
ditandai sebagai materi asli edisi memberi enam pemeriksaan terbatas beserta
solusi lengkap: naturalitas monodromi; kedua latihan sumber; lema
$\mathbf BG$; audit tipe pada contoh lingkaran; serta reduksi melalui komponen,
orbit, dan hipotesis SLSC. Tidak satu pun solusi memakai konstruksi ruang
penutup universal atau hasil klasifikasi dari kuliah sesudahnya. Seluruh materi
pendamping tersedia di bawah CC BY 4.0 dan tidak meminjam solusi eksternal.
Edisi ini bersifat independen; edisi ini tidak disponsori, didukung, disahkan,
ataupun diberi status resmi oleh David Michael Roberts, MIT, Haynes Miller,
Sanath Devalapurkar, Yeheli Fomberg, Nir Lazarovich, atau institusi mereka.

# Kuliah 14 {#o012-rbt-l14}

::: {.boundary #o012-rbt-l14-boundary-in}
**Sambungan bagian.** Unit 13 sudah memuat judul bagian sumber
“Mengklasifikasikan ruang pelapis” dari Notes.tex baris 3045. Kuliah ini
melanjutkan isi bagian tersebut mulai baris 3047. Jadi tidak ada isi matematis
yang hilang di batas unit, dan judul sumber tidak dihitung sebagai judul baru
yang kedua.
:::

Sepanjang unit ini, produk lintasan atau panah $[\gamma][\eta]$ dibaca
**kronologis**: $\gamma$ ditempuh dahulu, lalu $\eta$. Komposisi fungsi tetap
ditulis dalam urutan baku kanan-ke-kiri. Karena

$$
(\gamma\#\eta)_*=\eta_*\circ\gamma_*,
$$

transpor titik akhir langsung pada serat adalah aksi **kanan**.

## Pemetaan ruang penutup dan transformasi natural {#o012-rbt-l14-s01}

Ingat bahwa setiap ruang penutup $\pi\colon Z\to X$ memberi fungtor
monodromi

$$
\begin{aligned}
\rho_Z\colon\Pi_1(X)&\longrightarrow\mathbf{Set},\\
x&\longmapsto Z_x:=\pi^{-1}(x),\\
[\gamma\colon x\rightsquigarrow y]
&\longmapsto
\bigl(\gamma_*^Z\colon Z_x\xrightarrow{\cong}Z_y\bigr).
\end{aligned}
$$

Di sini $\gamma_*^Z(z)$ adalah titik akhir dari satu-satunya pengangkatan
$\gamma$ yang berawal di $z$.

Sekarang ambil dua ruang penutup $\pi_1\colon Z_1\to X$ dan
$\pi_2\colon Z_2\to X$, serta suatu morfisma $f\colon Z_1\to Z_2$ di
$\operatorname{Cov}_X$.

::: {.figure #o012-rbt-l14-fig-001}
**Diagram 14.1 (morfisma di atas ruang dasar).** Data panahnya adalah

$$
Z_1\xrightarrow{\ f\ }Z_2,
\qquad
Z_1\xrightarrow{\ \pi_1\ }X,
\qquad
Z_2\xrightarrow{\ \pi_2\ }X,
$$

dan syarat komutativitasnya ialah

$$
\pi_2\circ f=\pi_1.
$$

Jadi segitiga sumber menyatakan bahwa $f$ adalah pemetaan ruang penutup di
atas identitas $X$.
:::

Untuk setiap $x\in X$, komutativitas itu memberi pembatasan pada serat

$$
f_x:=f|_{(Z_1)_x}\colon (Z_1)_x\longrightarrow(Z_2)_x.
$$

Dengan kata lain, $f_x$ adalah fungsi
$\rho_{Z_1}(x)\to\rho_{Z_2}(x)$ pada setiap objek $x$ dari $\Pi_1(X)$.

Ambil lintasan $\gamma\colon x\rightsquigarrow y$ di $X$ dan
$z\in(Z_1)_x$. Terdapat tepat satu pengangkatan

$$
\widetilde{\gamma}^{\,1}_z\colon
z\rightsquigarrow\gamma_*^{Z_1}(z)
$$

di $Z_1$. Komposit $f\circ\widetilde{\gamma}^{\,1}_z$ adalah lintasan di
$Z_2$ dari $f_x(z)$ ke $f_y(\gamma_*^{Z_1}(z))$. Karena
$\pi_2\circ f=\pi_1$, komposit itu mengangkat $\gamma$. Keunikan pengangkatan
lintasan menunjukkan bahwa komposit tersebut adalah pengangkatan $\gamma$
yang berawal di $f_x(z)$; titik akhirnya ialah
$\gamma_*^{Z_2}(f_x(z))$. Maka

$$
f_y\bigl(\gamma_*^{Z_1}(z)\bigr)
=
\gamma_*^{Z_2}\bigl(f_x(z)\bigr).
$$

::: {.figure #o012-rbt-l14-fig-002}
**Diagram 14.2 (persegi naturalitas pada suatu lintasan).** Persegi

$$
\begin{array}{ccc}
(Z_1)_x&\longrightarrow&(Z_1)_y\\
\downarrow&&\downarrow\\
(Z_2)_x&\longrightarrow&(Z_2)_y
\end{array}
$$

komutatif. Panah atas adalah $\gamma_*^{Z_1}$, panah bawah adalah
$\gamma_*^{Z_2}$, dan panah tegak kiri serta kanan masing-masing adalah
$f_x$ dan $f_y$. Secara linear, kedua rute dari $(Z_1)_x$ ke $(Z_2)_y$ memenuhi

$$
f_y\circ\gamma_*^{Z_1}
=
\gamma_*^{Z_2}\circ f_x.
$$
:::

Jadi keluarga $(f_x)_{x\in X}$ merupakan transformasi natural
$\rho_{Z_1}\Rightarrow\rho_{Z_2}$. Ingat bahwa kategori fungtor
$[\mathcal C,\mathbf{Set}]$ mempunyai fungtor $\mathcal C\to\mathbf{Set}$
sebagai objek dan transformasi natural sebagai morfisma.

::: {.proposition #o012-rbt-l14-prop-001}
**Proposisi 14.1 (fungtor monodromi).** Penetapan

$$
(Z\xrightarrow{\pi}X)\longmapsto\rho_Z
$$

mendefinisikan fungtor

$$
\operatorname{Cov}_X
\longrightarrow
[\Pi_1(X),\mathbf{Set}].
$$
:::

::: {.proof #o012-rbt-l14-proof-001}
**Bukti.** Untuk pemetaan identitas $\operatorname{id}_Z$, pembatasan pada
setiap serat adalah $\operatorname{id}_{Z_x}$, sehingga transformasi natural
yang dihasilkan adalah identitas $\rho_Z\Rightarrow\rho_Z$.

Jika

$$
Z_1\xrightarrow{f}Z_2\xrightarrow{g}Z_3
$$

adalah dua morfisma ruang penutup di atas $X$, maka pada setiap $x\in X$

$$
(g\circ f)_x=g_x\circ f_x.
$$

Karena komposisi transformasi natural dihitung per komponen, transformasi
yang terkait dengan $g\circ f$ adalah komposit transformasi yang terkait
dengan $f$ dan $g$. Jadi identitas dan komposisi dipertahankan. $\square$
:::

## Dua ruang penutup lingkaran {#o012-rbt-l14-s02}

::: {.example #o012-rbt-l14-exa-001}
**Contoh 14.1 (reduksi modulo $n$ sebagai pemetaan monodromi).** Pandang
$S^1\subset\mathbb C$. Untuk $n>1$, definisikan

$$
p(t)=e^{2\pi it},
\qquad
F_n(t)=e^{2\pi it/n},
\qquad
q_n(z)=z^n.
$$

Pemetaan $p\colon\mathbb R\to S^1$ dan
$q_n\colon S^1\to S^1$ mendefinisikan ruang penutup, sedangkan
$F_n\colon\mathbb R\to S^1$ adalah morfisma di antara keduanya.

::: {.figure #o012-rbt-l14-fig-003}
**Diagram 14.3 (ruang penutup eksponensial menuju penutup pangkat-$n$).**
Daftar panahnya ialah

$$
\mathbb R\xrightarrow{\ F_n\ }S^1,
\qquad
\mathbb R\xrightarrow{\ p\ }S^1,
\qquad
S^1\xrightarrow{\ q_n\ }S^1.
$$

Segitiga komutatif karena

$$
(q_n\circ F_n)(t)
=
\bigl(e^{2\pi it/n}\bigr)^n
=
e^{2\pi it}
=p(t).
$$
:::

Setiap serat $p$ adalah torsor bagi translasi bilangan bulat, sehingga
isomorfik sebagai himpunan dengan $\mathbb Z$, meskipun tidak ada
identifikasi terpilih pada serat umum. Serat $p^{-1}(1)$ benar-benar sama
dengan $\mathbb Z$. Serat
$q_n^{-1}(1)$ adalah himpunan akar kesatuan

$$
\mu_n=\{e^{2\pi ik/n}:k\in\mathbb Z\}.
$$

Gunakan identifikasi terpilih

$$
\theta_n\colon\mathbb Z/n\xrightarrow{\cong}\mu_n,
\qquad
\overline{k}\longmapsto e^{2\pi ik/n}.
$$

Pada serat di atas $1$, pemetaan $F_n$ karena itu menginduksi

$$
\begin{aligned}
\mathbb Z&\longrightarrow\mathbb Z/n,\\
k&\longmapsto\overline{k}.
\end{aligned}
$$

Sebuah morfisma dari $1$ ke dirinya sendiri di $\Pi_1(S^1)$ adalah kelas
loop. Setelah memilih generator berarah positif, grup automorfisma objek itu
diidentifikasi dengan

$$
\pi_1(S^1,1)\cong\mathbb Z.
$$

Transpor titik akhir langsung memberi aksi kanan

$$
\begin{aligned}
\mathbb Z\times\mathbb Z&\longrightarrow\mathbb Z,
&k\cdot m&=k+m,\\
(\mathbb Z/n)\times\mathbb Z&\longrightarrow\mathbb Z/n,
&\overline{k}\cdot m&=\overline{k+m}.
\end{aligned}
$$

Jika $R_m^{\mathbb R}$ dan $R_m^n$ menyatakan operator titik akhir, tipe yang
tidak ambigu adalah

$$
\begin{aligned}
R^{\mathbb R}\colon\mathbb Z^{\mathrm{op}}
&\longrightarrow\operatorname{Sym}(\mathbb Z),
&m&\longmapsto(k\mapsto k+m),\\
R^n\colon\mathbb Z^{\mathrm{op}}
&\longrightarrow\operatorname{Sym}(\mathbb Z/n),
&m&\longmapsto(\overline{k}\mapsto\overline{k+m}).
\end{aligned}
$$

Di sini $\operatorname{Sym}(S)$ berarti grup semua bijeksi himpunan $S$.
Karena $\mathbb Z/n$ mempunyai $n$ unsur,
$\operatorname{Sym}(\mathbb Z/n)\cong S_n$ setelah pelabelan unsur dipilih.
Khusus untuk grup abelian $\mathbb Z$, grup lawan dapat diidentifikasi dengan
$\mathbb Z$ lagi; namun notasi aksi kanan tetap merekam asal rumus dari
pengangkatan lintasan.

Pemetaan reduksi modulo $n$ ekuivarian karena

$$
\overline{k\cdot m}
=
\overline{k+m}
=
\overline{k}\cdot m.
$$

Ini adalah kasus khusus naturalitas transformasi yang diinduksi oleh $F_n$.
:::

## Mereduksi pertanyaan klasifikasi {#o012-rbt-l14-s03}

::: {.question #o012-rbt-l14-q-001}
**Pertanyaan 14.1.** Fungtor atau representasi manakah

$$
\Pi_1(X)\longrightarrow\mathbf{Set}
$$

yang dapat muncul sebagai $\rho_Z$ untuk suatu ruang penutup $Z\to X$?
:::

Setiap himpunan jelas dapat direalisasikan sebagai himpunan komponen terhubung
suatu ruang. Unit 13 juga menjelaskan konstruksi pushout yang, untuk setiap
grup $G$, menghasilkan suatu ruang bertitik $(Y,*)$ dengan
$\pi_1(Y,*)\cong G$. Akan tetapi, kedua fakta realisasi tersebut belum
menunjukkan cara membangun ruang penutup dari sebuah fungtor yang diberikan

$$
\Pi_1(X)\longrightarrow\mathbf{Set}.
$$

Semua ruang penutup yang telah kita lihat sejauh ini merupakan contoh alami
yang sudah dikenal atau contoh kecil yang dipilih untuk menyoroti bagian
tertentu dari grupoid fundamental ruang sederhana. Strategi kita adalah
mereduksi kedua sisi masalah: sisi topologis $\operatorname{Cov}_X$ dan sisi
aljabar $[\Pi_1(X),\mathbf{Set}]$. Unit ini menyelesaikan reduksi aljabarnya;
realisasi semua objek dan klasifikasi penuh baru dibahas kemudian.

## Memilih satu titik pada setiap komponen {#o012-rbt-l14-s04}

Gunakan asumsi umum bahwa ruang-ruang kita terhubung lintasan semilokal
(SLPC). Tuliskan

$$
I:=[\mathrm{pt},X]
$$

untuk himpunan komponen lintasan $X$. Pilih suatu penampang pada tingkat
himpunan

$$
s\colon I\longrightarrow X,
\qquad
i\longmapsto a_i,
$$

dari pemetaan yang mengirim titik ke komponen lintasannya, lalu bedakan
penampang itu dari citranya dengan menulis

$$
A:=s(I)=\{a_i:i\in I\}\subseteq X.
$$

Dalam konvensi SLPC mata kuliah ini, setiap komponen lintasan terbuka. Jadi
pemetaan $X\to I$ kontinu jika $I$ diberi topologi diskret, dan penampang
$s$ juga kontinu karena domainnya diskret. Untuk argumen kategoris di bawah,
yang diperlukan hanyalah satu titik pilihan $a_i$ pada setiap komponen.

Inklusi subgrupoid penuh

$$
i\colon\Pi_1(X,A)\hookrightarrow\Pi_1(X)
$$

adalah ekuivalensi: setiap objek $x\in X$ terhubung oleh suatu kelas lintasan
dengan satu-satunya objek pilihan $a_i$ di komponennya. Pernyataan ini adalah
isi rujukan catatan pinggir sumber ke Assignment 2, soal 7; alasannya kini
diletakkan langsung dalam urutan bacaan.

::: {.lemma #o012-rbt-l14-lem-001}
**Lema 14.1 (restriksi sepanjang subkategori penuh yang ekuivalen).** Jika

$$
i\colon\mathcal C\hookrightarrow\mathcal D
$$

adalah inklusi subkategori penuh sekaligus ekuivalensi, maka fungtor restriksi

$$
\begin{aligned}
[\mathcal D,\mathbf{Set}]&\xrightarrow{\ i^*\ }
[\mathcal C,\mathbf{Set}],\\
F&\longmapsto F\circ i
\end{aligned}
$$

adalah ekuivalensi kategori.
:::

::: {.exercise #o012-rbt-l14-ex-001 data-origin="source"}
**Latihan Sumber 14.1.** Buktikan Lema 14.1. Sumber menuliskan seluruh
buktinya sebagai “Exercise”. Solusi mandiri tersedia pada
[Pemeriksaan Penguasaan 14.2](#o012-rbt-l14-mcheck-002).
:::

## Memisahkan komponen dan aksi grup {#o012-rbt-l14-s05}

Untuk setiap $i\in I$, misalkan $X_i$ adalah komponen lintasan yang memuat
$a_i$. Karena komponen-komponen itu terbuka, $X$ adalah koproduk topologis
$\coprod_{i\in I}X_i$. Tidak ada lintasan antara dua komponen yang berlainan,
sehingga

$$
\Pi_1(X,A)
=
\Pi_1\!\left(
\coprod_{i\in I}X_i,
\coprod_{i\in I}\{a_i\}
\right)
\cong
\coprod_{i\in I}\mathbf B\pi_1(X_i,a_i).
$$

::: {.lemma #o012-rbt-l14-lem-002}
**Lema 14.2 (fungtor dari koproduk kategori).** Untuk setiap keluarga
kategori $(\mathcal C_i)_{i\in I}$ terdapat isomorfisma kategori

$$
\left[\coprod_{i\in I}\mathcal C_i,\mathbf{Set}\right]
\xrightarrow{\ \cong\ }
\prod_{i\in I}[\mathcal C_i,\mathbf{Set}].
$$

Sebuah objek di ruas kanan adalah satu tupel fungtor, tepat satu dari setiap
kategori faktor; morfismanya adalah tupel transformasi natural dengan indeks
yang sama.
:::

::: {.exercise #o012-rbt-l14-ex-002 data-origin="source"}
**Latihan Sumber 14.2.** Buktikan Lema 14.2. Sumber menuliskan seluruh
buktinya sebagai “Exercise”. Solusi mandiri tersedia pada
[Pemeriksaan Penguasaan 14.3](#o012-rbt-l14-mcheck-003).
:::

Untuk suatu grup $G$, tuliskan $\mathbf{Set}_G$ bagi kategori himpunan dengan
aksi **kanan** $G$. Pilihan notasi ini mempertahankan konvensi monodromi
langsung Unit 7--10. Bentuk aksi kiri yang dipakai sumber dapat selalu
diperoleh dengan

$$
g\star p:=p\cdot g^{-1},
$$

tetapi bentuk itu tidak akan menggantikan aksi kanan langsung dalam unit ini.

::: {.definition #o012-rbt-l14-def-001}
**Definisi 14.1 (himpunan-$G$ kanan).** Objek $\mathbf{Set}_G$ adalah pasangan
$(S,\rho)$ dengan pemetaan

$$
\rho\colon S\times G\longrightarrow S,
\qquad
(p,g)\longmapsto p\cdot g,
$$

yang memenuhi

$$
p\cdot e=p,
\qquad
p\cdot(gh)=(p\cdot g)\cdot h.
$$

Morfisma $f\colon S\to T$ adalah fungsi ekuivarian, yakni

$$
f(p\cdot g)=f(p)\cdot g
$$

untuk semua $p\in S$ dan $g\in G$.
:::

Lebih umum, jika $\Gamma$ adalah grupoid dan
$\rho\colon\Gamma\to\mathbf{Set}$ suatu representasi, maka untuk setiap
objek $x\in\Gamma$ terdapat aksi oleh grup automorfisma $\Gamma(x,x)$ pada
$\rho(x)$. Dengan urutan produk kronologis, aksi langsung itu adalah aksi
kanan. Jika $\alpha\colon\rho\Rightarrow\rho'$ adalah transformasi natural,
komponennya

$$
\alpha_x\colon\rho(x)\longrightarrow\rho'(x)
$$

ekuivarian terhadap aksi $\Gamma(x,x)$. Evaluasi pada $x$ juga mempertahankan
identitas dan komposisi transformasi natural.

::: {.lemma #o012-rbt-l14-lem-003}
**Lema 14.3 (fungtor dari grupoid satu objek).** Dengan konvensi produk
kronologis, konstruksi sebelumnya memberi isomorfisma kategori

$$
[\mathbf BG,\mathbf{Set}]
\xrightarrow{\ \cong\ }
\mathbf{Set}_G.
$$
:::

Sumber tidak memberikan bukti lema ini. Bukti mandiri tersedia pada
[Pemeriksaan Penguasaan 14.4](#o012-rbt-l14-mcheck-004).

Gabungkan ketiga lema di atas. Kita memperoleh rantai ekuivalensi

$$
\begin{aligned}
[\Pi_1(X),\mathbf{Set}]
&\xrightarrow[\ \simeq\ ]{\ i^*\ }
[\Pi_1(X,A),\mathbf{Set}]\\
&\cong
\prod_{i\in I}
[\mathbf B\pi_1(X_i,a_i),\mathbf{Set}]\\
&\cong
\prod_{i\in I}\mathbf{Set}_{\pi_1(X_i,a_i)}.
\end{aligned}
$$

Ekuivalensi pertama bergantung pada pilihan titik $a_i$ dan, ketika invers
semu ditulis eksplisit, pada pilihan lintasan menuju titik-titik itu. Fungtor
monodromi asli $\rho_Z\colon\Pi_1(X)\to\mathbf{Set}$ tidak memerlukan pilihan
titik pangkal; hasil-hasil dari dua pilihan berbeda berhubungan melalui
ekuivalensi natural.

Komposisikan rantai tadi dengan Proposisi 14.1.

::: {.equation #o012-rbt-l14-eq-fibre-functor}
**Fungtor serat komponen.** Fungtor yang dihasilkan adalah

$$
\begin{aligned}
\operatorname{Cov}_X
&\longrightarrow
\prod_{i\in I}\mathbf{Set}_{\pi_1(X_i,a_i)},\\
(Z\to X)
&\longmapsto
\left(
\rho_i\colon
Z_{a_i}\times\pi_1(X_i,a_i)\longrightarrow Z_{a_i}
\right)_{i\in I},
\end{aligned}
$$

dengan

$$
\rho_i(z,[\gamma])
=
z\cdot[\gamma]
:=
\gamma_*^Z(z).
$$
:::

Kodomain ini lebih mudah ditangani. Setiap himpunan-$G$ kanan merupakan
gabungan saling lepas orbit-orbitnya. Pilih satu titik $p_j$ pada setiap orbit,
dengan $j\in S/G$, dan tuliskan

$$
H_j:=\operatorname{Stab}(p_j)
=
\{g\in G:p_j\cdot g=p_j\}.
$$

Maka terdapat isomorfisma himpunan-$G$ kanan

$$
\begin{aligned}
\coprod_{j\in S/G}H_j\backslash G
&\xrightarrow{\ \cong\ }S,\\
H_jg&\longmapsto p_j\cdot g.
\end{aligned}
$$

Ruang $H_j\backslash G$ terdiri atas koset kanan dan membawa aksi kanan melalui
perkalian di ruas kanan. Jika aksi diubah menjadi aksi kiri
$g\star p=p\cdot g^{-1}$, pernyataan ekuivalennya memakai
$G/H_j$; kedua sisi koset tidak boleh dicampurkan.

## Hipotesis untuk langkah berikutnya {#o012-rbt-l14-s06}

::: {.remark #o012-rbt-l14-rem-001}
**Catatan 14.1 (SLSC dan komponen ruang penutup).** Mulai titik ini, kita hanya
mempertimbangkan ruang yang terhubung sederhana semilokal (SLSC), karena
itulah hipotesis yang kelak dipakai pada teorema klasifikasi.

Dalam konvensi mata kuliah ini, SLSC sudah mencakup adanya basis lingkungan
yang terhubung lintasan. Jadi $X$ terhubung lintasan lokal. Jika
$\pi\colon Z\to X$ adalah ruang penutup dan $z\in Z$, pilih lingkungan
terhubung lintasan $U$ dari $\pi(z)$ yang tertutup rata. Lembaran
$V\subseteq\pi^{-1}(U)$ yang memuat $z$ homeomorfik dengan $U$. Lembaran
semacam itu membentuk basis lingkungan terhubung lintasan di $Z$. Karena itu
$Z$ terhubung lintasan lokal, sehingga komponen terhubung dan komponen
lintasannya bertepatan.
:::

::: {.boundary #o012-rbt-l14-boundary-out}
**Batas ke Unit 15.** Sampai di sini sisi aljabar telah dipisahkan menurut
komponen dasar dan orbit aksi. Unit 15 mulai pada Notes.tex baris 3210 dan
memberikan pemisahan topologis yang bersesuaian bagi kategori ruang penutup.
Unit 14 belum mengonstruksi ruang penutup dari sembarang aksi, belum memakai
ruang penutup universal, dan belum membuktikan teorema klasifikasi.
:::

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l14-mastery}

Bagian ini merupakan materi asli edisi, bukan bagian dari Notes.tex. Enam
pemeriksaan berikut hanya memakai hasil yang tersedia sampai akhir Unit 14.
Pemeriksaan 14.2 dan 14.3 menyelesaikan dua latihan sumber; Pemeriksaan 14.4
memberi bukti bagi lema yang tidak dibuktikan sumber. Seluruh solusi disusun
mandiri dan tersedia di bawah CC BY 4.0.

::: {.exercise #o012-rbt-l14-mcheck-001 data-origin="edition-original"}
**Pemeriksaan penguasaan 14.1 (naturalitas dan fungtorialitas).** Misalkan
$f\colon Z_1\to Z_2$ dan $g\colon Z_2\to Z_3$ adalah morfisma ruang penutup di
atas $X$.

1. Buktikan bahwa $f_y\circ\gamma_*^{Z_1}
   =\gamma_*^{Z_2}\circ f_x$ untuk setiap
   $[\gamma\colon x\rightsquigarrow y]$.
2. Buktikan bahwa keluarga $(g_x\circ f_x)_{x\in X}$ adalah transformasi
   natural yang terkait dengan $g\circ f$.
:::

## Solusi Pemeriksaan 14.1 {#o012-rbt-l14-sol-001}

Ambil $z\in(Z_1)_x$ dan angkat $\gamma$ ke lintasan
$\widetilde\gamma_z$ di $Z_1$. Karena $f$ berada di atas $X$,
$f\circ\widetilde\gamma_z$ juga mengangkat $\gamma$ dan berawal di $f_x(z)$.
Keunikan pengangkatan memberi

$$
f_y(\gamma_*^{Z_1}(z))
=
\gamma_*^{Z_2}(f_x(z)).
$$

Karena persamaan berlaku bagi setiap $z$, persegi naturalitas komutatif.

Pada setiap serat,

$$
(g\circ f)_x=g_x\circ f_x.
$$

Komposit dua persegi naturalitas memberi

$$
(g_y\circ f_y)\circ\gamma_*^{Z_1}
=
\gamma_*^{Z_3}\circ(g_x\circ f_x),
$$

sehingga keluarga tersebut natural. Perhitungan per komponen juga menunjukkan
bahwa fungtor monodromi mempertahankan komposisi.

::: {.exercise #o012-rbt-l14-mcheck-002 data-origin="edition-original"}
**Pemeriksaan penguasaan 14.2 (solusi Latihan Sumber 14.1).** Jika
$i\colon\mathcal C\hookrightarrow\mathcal D$ penuh dan merupakan
ekuivalensi, konstruksikan invers semu bagi

$$
i^*\colon[\mathcal D,\mathbf{Set}]\to[\mathcal C,\mathbf{Set}]
$$

dan jelaskan mengapa hasilnya hanya bergantung pada pilihan hingga isomorfisma
natural.
:::

## Solusi Pemeriksaan 14.2 {#o012-rbt-l14-sol-002}

Karena $i$ ekuivalensi, pilih fungtor invers semu
$r\colon\mathcal D\to\mathcal C$ beserta isomorfisma natural

$$
ri\cong\operatorname{id}_{\mathcal C},
\qquad
ir\cong\operatorname{id}_{\mathcal D}.
$$

Pra-komposisi dengan $r$ memberi

$$
r^*\colon[\mathcal C,\mathbf{Set}]\longrightarrow
[\mathcal D,\mathbf{Set}],
\qquad
F\longmapsto F\circ r.
$$

Pra-komposisi isomorfisma $ri\cong\operatorname{id}_{\mathcal C}$ dengan
setiap $F$ memberi

$$
i^*r^*(F)=F\circ r\circ i\cong F.
$$

Demikian pula, $ir\cong\operatorname{id}_{\mathcal D}$ memberi

$$
r^*i^*(H)=H\circ i\circ r\cong H
$$

untuk $H\colon\mathcal D\to\mathbf{Set}$. Kedua isomorfisma natural juga
berlaku pada transformasi natural, sehingga $i^*$ dan $r^*$ merupakan
ekuivalensi invers semu. Pilihan invers semu lain menghasilkan fungtor yang
terhubung oleh isomorfisma natural; karena itu reduksi ini bukan identifikasi
kanonik harfiah.

::: {.exercise #o012-rbt-l14-mcheck-003 data-origin="edition-original"}
**Pemeriksaan penguasaan 14.3 (solusi Latihan Sumber 14.2).** Bangun kedua
arah isomorfisma

$$
\left[\coprod_i\mathcal C_i,\mathbf{Set}\right]
\cong
\prod_i[\mathcal C_i,\mathbf{Set}]
$$

pada objek dan morfisma.
:::

## Solusi Pemeriksaan 14.3 {#o012-rbt-l14-sol-003}

Jika $F\colon\coprod_i\mathcal C_i\to\mathbf{Set}$, batasi $F$ pada setiap
komponen kategori untuk memperoleh tupel

$$
(F_i\colon\mathcal C_i\to\mathbf{Set})_{i\in I}.
$$

Transformasi natural $\alpha\colon F\Rightarrow G$ juga membatasi menjadi
tupel $(\alpha_i\colon F_i\Rightarrow G_i)_i$.

Sebaliknya, dari tupel $(F_i)_i$, definisikan $F$ pada objek atau morfisma yang
berasal dari $\mathcal C_i$ dengan memakai $F_i$. Definisi ini lengkap karena
koproduk kategori tidak memiliki morfisma di antara dua faktor berbeda.
Tupel transformasi natural dirakit dengan cara yang sama. Pembatasan sesudah
perakitan dan perakitan sesudah pembatasan sama dengan identitas, baik pada
objek maupun morfisma. Jadi yang diperoleh benar-benar isomorfisma kategori.

::: {.exercise #o012-rbt-l14-mcheck-004 data-origin="edition-original"}
**Pemeriksaan penguasaan 14.4 (lema grupoid satu objek).** Buktikan secara
langsung bahwa

$$
[\mathbf BG,\mathbf{Set}]\cong\mathbf{Set}_G
$$

untuk produk kronologis, termasuk pernyataan tentang transformasi natural.
:::

## Solusi Pemeriksaan 14.4 {#o012-rbt-l14-sol-004}

Grupoid $\mathbf BG$ mempunyai satu objek $*$ dan morfisma $g\in G$. Produk
$gh$ berarti menempuh $g$ dahulu, lalu $h$. Dari fungtor
$F\colon\mathbf BG\to\mathbf{Set}$, ambil $S=F(*)$ dan definisikan

$$
p\cdot g:=F(g)(p).
$$

Hukum fungtor untuk urutan kronologis adalah

$$
F(gh)=F(h)\circ F(g).
$$

Karena itu

$$
p\cdot(gh)
=F(gh)(p)
=F(h)(F(g)(p))
=(p\cdot g)\cdot h,
$$

dan identitas di $\mathbf BG$ memberi $p\cdot e=p$. Jadi $S$ adalah
himpunan-$G$ kanan.

Sebaliknya, dari aksi kanan pada $S$, tetapkan $F(*)=S$ dan
$F(g)(p)=p\cdot g$. Kedua hukum aksi tepat menjadi hukum identitas dan
komposisi fungtor. Sebuah transformasi natural antara dua fungtor hanya
mempunyai satu komponen $u\colon S\to T$, dan naturalitas pada $g$ menyatakan

$$
u(p\cdot g)=u(p)\cdot g.
$$

Jadi transformasi natural tepat sama dengan fungsi ekuivarian. Kedua
konstruksi saling invers pada objek dan morfisma.

::: {.exercise #o012-rbt-l14-mcheck-005 data-origin="edition-original"}
**Pemeriksaan penguasaan 14.5 (audit tipe contoh lingkaran).** Untuk contoh
$p$, $q_n$, dan $F_n$:

1. tuliskan domain dan kodomain operator monodromi bertitik secara tepat;
2. buktikan bahwa reduksi $\mathbb Z\to\mathbb Z/n$ ekuivarian;
3. jelaskan mengapa contoh abelian ini tidak dapat mendeteksi pembalikan urutan
   aksi.
:::

## Solusi Pemeriksaan 14.5 {#o012-rbt-l14-sol-005}

Setelah memilih titik $1\in S^1$, domainnya adalah
$\pi_1(S^1,1)\cong\mathbb Z$, bukan seluruh $\Pi_1(S^1)$. Operator langsung
bertipe

$$
\mathbb Z^{\mathrm{op}}\to\operatorname{Sym}(\mathbb Z),
\qquad
\mathbb Z^{\mathrm{op}}\to\operatorname{Sym}(\mathbb Z/n),
$$

atau, secara ekuivalen, berupa dua aksi kanan yang ditampilkan pada Contoh
14.1. Untuk $r(k)=\overline{k}$,

$$
r(k\cdot m)
=r(k+m)
=\overline{k+m}
=\overline{k}\cdot m
=r(k)\cdot m,
$$

jadi $r$ ekuivarian.

Secara umum operator aksi kanan memenuhi
$R_{gh}=R_h\circ R_g$, sedangkan homomorfisma aksi kiri biasa memenuhi urutan
operator yang berlawanan. Pada $\mathbb Z$, penjumlahan dan semua translasi
yang bersangkutan komutatif, sehingga

$$
R_{m+l}=R_l\circ R_m=R_m\circ R_l.
$$

Akibatnya contoh lingkaran saja menyembunyikan perbedaan sisi; konvensi harus
ditetapkan sebelum beralih ke grup fundamental nonabelian.

::: {.exercise #o012-rbt-l14-mcheck-006 data-origin="edition-original"}
**Pemeriksaan penguasaan 14.6 (komponen, orbit, dan SLSC).** Misalkan $X$
SLPC, pilih $a_i$ pada setiap komponen lintasan $X_i$, dan misalkan $S$ suatu
himpunan-$G$ kanan.

1. Jelaskan mengapa $\Pi_1(X,A)$ tidak mempunyai panah di antara dua
   $a_i$ yang berbeda dan mengapa inklusinya ke $\Pi_1(X)$ tetap esensial
   surjektif.
2. Untuk $p\in S$ dan $H=\operatorname{Stab}(p)$, buktikan bahwa orbit $pG$
   isomorfik dengan $H\backslash G$ sebagai himpunan-$G$ kanan.
3. Jika $X$ SLSC dan $Z\to X$ ruang penutup, buktikan bahwa komponen terhubung
   dan komponen lintasan $Z$ bertepatan.
:::

## Solusi Pemeriksaan 14.6 {#o012-rbt-l14-sol-006}

Lintasan dari $a_i$ ke $a_j$ akan menempatkan keduanya dalam komponen lintasan
yang sama. Karena dipilih tepat satu titik pada setiap komponen, tidak ada
panah demikian bila $i\ne j$. Sebaliknya, setiap $x\in X$ terletak dalam suatu
$X_i$, sehingga ada lintasan dari $x$ ke $a_i$. Jadi setiap objek
$\Pi_1(X)$ isomorfik dengan objek dalam subgrupoid penuh $\Pi_1(X,A)$; inklusi
itu esensial surjektif.

Definisikan

$$
\Phi\colon H\backslash G\longrightarrow pG,
\qquad
Hg\longmapsto p\cdot g.
$$

Jika $Hg=Hg'$, ambil $h\in H$ sedemikian sehingga $g'=hg$. Lalu

$$
p\cdot g'
=p\cdot(hg)
=(p\cdot h)\cdot g
=p\cdot g,
$$

sehingga $\Phi$ terdefinisi baik. Sebaliknya, jika $p\cdot g=p\cdot g'$,
terapkan aksi $g^{-1}$ di kanan pada kedua ruas untuk memperoleh

$$
p=p\cdot(g'g^{-1})
$$

dan karena itu $g'g^{-1}\in H$ serta $Hg'=Hg$. Dengan demikian $\Phi$
injektif, sedangkan
surjektivitas benar dari definisi orbit. Untuk $k\in G$,

$$
\Phi((Hg)\cdot k)
=\Phi(Hgk)
=p\cdot(gk)
=(p\cdot g)\cdot k,
$$

sehingga $\Phi$ ekuivarian.

Terakhir, SLSC dalam konvensi mata kuliah memberi basis lingkungan terhubung
lintasan pada $X$. Di atas lingkungan yang tertutup rata, setiap
lembaran ruang penutup homeomorfik dengan lingkungan tersebut. Lembaran-lembaran
ini memberi basis lingkungan terhubung lintasan pada $Z$, sehingga $Z$
terhubung lintasan lokal. Pada ruang terhubung lintasan lokal, setiap komponen
lintasan terbuka; suatu komponen terhubung tidak dapat menjadi gabungan saling
lepas dari lebih dari satu komponen lintasan terbuka. Maka komponen terhubung
dan komponen lintasan $Z$ bertepatan.
