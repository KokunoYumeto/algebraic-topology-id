---
title: "Topologi Aljabar"
subtitle: "Unit 17: Ekuivalensi Ruang Penutup dan Grup Homotopi Lebih Tinggi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l17-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 3384--3481 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L3384-L3481)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang 98 baris itu dimulai dengan penanda Kuliah 17 dan berakhir sesudah
proposisi bahwa $\pi_n(X,x)$ abelian untuk $n\geq2$. Penanda Kuliah 18 pada
baris 3482 tidak termasuk. Materi sumber dan adaptasi Indonesia ini tersedia
di bawah [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/).

Perubahan edisi mencakup penerjemahan, pemformatan ulang agar mudah dibaca,
pemberian pengenal stabil, dan pemindahan ketiga catatan pinggir ke urutan
bacaan utama. Tampilan panjang yang mendefinisikan operasi grup dan kedua
konkatenasi koordinat ditata ulang dengan deskripsi linear, syarat jahitan,
dan inventaris empat kuadran. Tidak ada diagram gambar atau aset eksternal
pada rentang sumber ini.

Konvensi monodromi tetap sama dengan Unit 14--16. Pada serat titik basis
dalam model kelas lintasan, $G=\pi_1(X,x_0)$ bertindak dari **kanan** melalui

$$
[\gamma]\cdot g=[\gamma\#g],
$$

yakni $g$ ditempuh sesudah $\gamma$. Karena itu

$$
(z\cdot g)\cdot h=z\cdot(gh),
\qquad
\varphi(z\cdot g)=\varphi(z)\cdot g.
$$

Tidak ada aksi kiri baru dalam Unit 17. Aksi kanan ini tidak disamakan dengan
notasi kiri hasil konversi invers $g\star z=z\cdot g^{-1}$, dan juga tidak
disamakan dengan aksi kiri serat demi serat Unit 16
$h\triangleright[\gamma]=[h\#\gamma]$ yang dipakai untuk membentuk
$H\backslash\widetilde X$.

Edisi ini memperbaiki persamaan peta yang salah tipe pada lema keunikan,
melengkapi bukti kesetiaan komponen demi komponen, dan memberi bukti penuh
bagi kepenuhan fungtor monodromi, termasuk kontinuitas dalam trivialiasi
lokal. Rentang $n$ dinyatakan pada setiap hasil: $\pi_0$ mula-mula hanya
himpunan bertitik, sedangkan model kubus/cakram, adjungsi loop, dan struktur
grup di sini berlaku untuk $n\geq1$. Argumen Eckmann--Hilton dikoreksi:
hipotesis dua operasi berunit dan hukum pertukaran hanya menghasilkan
**monoid komutatif**; kesimpulan grup abelian baru sah bila invers telah
diperoleh secara terpisah. Kesalahan cabang kedua operasi $\#_2$ juga
diperbaiki dari $f_1$ menjadi $f_2$.

Keenam pemeriksaan penguasaan beserta solusi lengkap merupakan materi asli
edisi dan tersedia di bawah CC BY 4.0. Edisi ini bersifat independen; edisi
ini tidak disponsori, didukung, disahkan, ataupun diberi status resmi oleh
David Michael Roberts, MIT, Haynes Miller, Sanath Devalapurkar, Yeheli
Fomberg, Nir Lazarovich, atau institusi mereka.

# Kuliah 17 {#o012-rbt-l17}

Unit 16 membuktikan bahwa, untuk $X$ SLSC dalam konvensi mata kuliah, fungtor
monodromi

$$
\rho\colon\operatorname{Cov}_X
\longrightarrow[\Pi_1(X),\mathbf{Set}]
$$

surjektif secara esensial. Kini kita buktikan bahwa fungtor itu juga setia
dan penuh. Sesudah klasifikasi ruang penutup selesai, sumber memulai bagian
baru tentang grup homotopi lebih tinggi.

## Keunikan pemetaan ke ruang penutup {#o012-rbt-l17-s01}

::: {.lemma #o012-rbt-l17-lem-001}
**Lema 17.1 (keunikan pemetaan pengangkat).** Misalkan
$\pi\colon Z\to X$ ruang penutup, $Y$ terhubung lintasan, dan
$p\colon Y\to X$ suatu pemetaan. Jika $f,g\colon Y\to Z$ memenuhi

$$
\pi\circ f=p=\pi\circ g
$$

dan $f(y_0)=g(y_0)$ untuk suatu $y_0\in Y$, maka $f=g$.
:::

::: {.proof #o012-rbt-l17-proof-001}
**Bukti.** Ambil $y\in Y$ dan pilih lintasan
$\gamma\colon y_0\rightsquigarrow y$. Kedua lintasan
$f\circ\gamma$ dan $g\circ\gamma$ merupakan pengangkatan dari
$p\circ\gamma\colon I\to X$. Titik awalnya sama karena

$$
f(\gamma(0))=f(y_0)=g(y_0)=g(\gamma(0)).
$$

Keunikan pengangkatan lintasan memberi
$f\circ\gamma=g\circ\gamma$, sehingga pada titik akhir

$$
f(y)=f(\gamma(1))=g(\gamma(1))=g(y).
$$

Karena $y$ sebarang, $f=g$. Persamaan pada pernyataan memperbaiki urutan
komposisi yang salah tipe di sumber, dan $g(\gamma(0))$ memperbaiki argumen
$g(\gamma(y_0))$ yang tidak terdefinisi.
:::

Lema ini berlaku khususnya bila $Y$ sendiri merupakan ruang total suatu
ruang penutup dari $X$, asalkan diterapkan pada setiap komponen lintasannya.

::: {.corollary #o012-rbt-l17-cor-001}
**Akibat 17.1 (kesetiaan monodromi).** Fungtor monodromi

$$
\rho\colon\operatorname{Cov}_X
\longrightarrow[\Pi_1(X),\mathbf{Set}]
$$

bersifat setia.
:::

::: {.proof #o012-rbt-l17-proof-002}
**Bukti.** Mula-mula anggap $X$ terhubung dan pilih $x_0\in X$. Dalam
konvensi SLSC mata kuliah, $X$ terhubung lintasan. Ambil dua ruang penutup
$\pi_i\colon Z_i\to X$ dan dua pemetaan ruang penutup
$f,g\colon Z_1\to Z_2$. Andaikan transformasi natural yang diinduksi $f$
dan $g$ sama. Khususnya, pembatasan serat yang bertipe lengkap memenuhi

$$
f_{x_0}=g_{x_0}\colon
(Z_1)_{x_0}\longrightarrow(Z_2)_{x_0}.
$$

Kedua pembatasan ini adalah morfisma di $\mathbf{Set}_G$ untuk aksi
monodromi kanan; kesamaannya di sini adalah kesamaan fungsi serat yang
ekuivarian kanan.

Setiap komponen lintasan $C$ dari $Z_1$ memetakan surjektif ke $X$; ini
adalah hasil komponen ruang penutup yang dibuktikan pada Unit 15. Maka ada
$z_C\in C\cap(Z_1)_{x_0}$. Pembatasan $f|_C$ dan $g|_C$ adalah dua pemetaan
dari ruang terhubung lintasan $C$ ke $Z_2$ di atas $X$, dan keduanya sama
pada $z_C$. Lema 17.1 memberi $f|_C=g|_C$. Karena komponen-komponen itu
menutupi $Z_1$, diperoleh $f=g$.

Untuk $X$ yang tidak terhubung, komponen lintasannya terbuka menurut
konvensi SLSC. Terapkan argumen yang sama secara terpisah pada setiap
komponen ruang basis. Jadi kesamaan transformasi natural selalu memaksa
kesamaan pemetaan ruang penutup, yakni $\rho$ setia.
:::

## Kepenuhan dan teorema klasifikasi {#o012-rbt-l17-s02}

::: {.theorem #o012-rbt-l17-thm-001}
**Teorema 17.1 (klasifikasi ruang penutup).** Jika $X$ SLSC dalam konvensi
mata kuliah, fungtor monodromi

$$
\rho\colon\operatorname{Cov}_X
\longrightarrow[\Pi_1(X),\mathbf{Set}]
$$

merupakan ekuivalensi kategori.
:::

::: {.proof #o012-rbt-l17-proof-003}
**Bukti.** Unit 16 membuktikan surjektivitas esensial, dan Akibat 17.1
membuktikan kesetiaan. Tinggal dibuktikan bahwa $\rho$ penuh.

Ambil ruang penutup $\pi_i\colon Z_i\to X$, dengan representasi monodromi
$\rho_i$, dan transformasi natural

$$
\eta\colon\rho_1\Longrightarrow\rho_2.
$$

Untuk $z\in Z_1$ dengan $\pi_1(z)=x$, definisikan

$$
F(z):=\eta_x(z)\in(Z_2)_x.
$$

Definisi ini langsung memberi

$$
\pi_2\circ F=\pi_1,
\qquad
F|_{(Z_1)_x}=\eta_x
$$

untuk setiap $x\in X$. Jadi yang masih harus dibuktikan hanya kontinuitas.

Tetapkan $x\in X$. Pilih lingkungan terbuka terhubung lintasan $U\ni x$
yang diliputi secara merata oleh **kedua** ruang penutup; ini diperoleh
dengan memotong dua lingkungan yang diliputi secara merata lalu
memperhalusnya memakai basis SLSC. Tuliskan

$$
A_i:=(Z_i)_x.
$$

Penandaan lembaran oleh titiknya di atas $x$ memberi trivialiasi

$$
\tau_i\colon\pi_i^{-1}(U)\xrightarrow{\ \cong\ }U\times A_i.
$$

Bagi $u\in U$, $a\in A_1$, dan lintasan
$[\alpha\colon x\rightsquigarrow u]$ di $U$, titik pada lembaran berlabel
$a$ ialah $\alpha_*^{Z_1}(a)$. Naturalitas $\eta$ menyatakan

$$
\eta_u\bigl(\alpha_*^{Z_1}(a)\bigr)
=
\alpha_*^{Z_2}\bigl(\eta_x(a)\bigr).
$$

Karena $U$ diliputi secara merata, transpor di dalam $U$ tetap berada pada
satu lembaran dan tidak bergantung pada pilihan lintasan di $U$ setelah label
lembaran ditetapkan. Oleh karena itu, dalam kedua trivialiasi lokal, $F$
mempunyai rumus

$$
\tau_2\circ F\circ\tau_1^{-1}(u,a)
=
(u,\eta_x(a)).
$$

Rumus itu adalah identitas pada faktor $U$ dan satu pemetaan tetap di antara
himpunan diskret $A_1$ dan $A_2$; jadi ia kontinu. Lingkungan seperti $U$
menutupi $X$, maka $F$ kontinu secara global. Dengan demikian $F$ adalah
pemetaan ruang penutup yang menginduksi $\eta$. Keunikannya langsung dari
rumus $F(z)=\eta_{\pi_1(z)}(z)$, atau dari kesetiaan yang baru dibuktikan.
Jadi $\rho$ penuh. Fungtor yang penuh, setia, dan surjektif secara esensial
merupakan ekuivalensi kategori.

Untuk menghubungkan bukti ini dengan reduksi bertitik pada sumber, andaikan
$X$ terhubung, pilih $x_0$, dan letakkan $G=\pi_1(X,x_0)$. Komponen titik
basis dari transformasi natural adalah pemetaan himpunan-$G$ **kanan**

$$
\varphi\colon(Z_1)_{x_0}\longrightarrow(Z_2)_{x_0},
\qquad
\varphi(z\cdot g)=\varphi(z)\cdot g.
$$

Naturalitas terhadap semua lintasan memperluas $\varphi$ menjadi keluarga
$(\eta_x)_x$, dan konstruksi di atas menghasilkan $F$. Aksi kanan tersebut
adalah monodromi langsung; bukti ini tidak memakai aksi kiri serat demi
serat dari Unit 16.
:::

## Grup homotopi lebih tinggi {#o012-rbt-l17-s03}

Sejauh ini kita telah memakai invarian $\pi_0$, $[\mathrm{pt},-]$, dan
$\pi_1$. Catatan pinggir sumber mengingatkan bahwa pada dimensi rendah ada
dua invarian yang sama-sama mencoba menangkap “komponen” suatu ruang;
keadaan ganda ini merupakan kekhasan dimensi rendah.

Perhatikan bahwa

$$
\pi_1(X,x)=[(S^1,1),(X,x)]_*.
$$

Untuk ruang bertitik juga berlaku

$$
[\mathrm{pt},X]
\cong
[(S^0,1),(X,x)]_*,
$$

sebab $S^0=\{1,-1\}$ dan peta bertitik
$(S^0,1)\to(X,x)$ ditentukan sepenuhnya oleh citra $-1$. Pola ini memotivasi
pertanyaan retoris sumber: apa yang seharusnya menjadi $\pi_n$?

::: {.definition #o012-rbt-l17-def-001}
**Definisi 17.1 (himpunan dan grup homotopi ke-$n$).** Bagi ruang bertitik
$(X,x)$ dan bilangan bulat $n\geq0$, definisikan

$$
\pi_n(X,x):=[(S^n,1),(X,x)]_*.
$$

Untuk $n=0$, objek ini mula-mula hanya himpunan bertitik. Untuk $n\geq1$,
operasi yang dibangun di bawah menjadikannya grup, sehingga istilah
**grup homotopi ke-$n$** dipakai dalam rentang tersebut.
:::

Untuk setiap $n\geq0$, postkomposisi oleh peta bertitik membuat $\pi_n$
menjadi fungtor

$$
\pi_n\colon\mathbf{Top}_*\longrightarrow\mathbf{Set}.
$$

Kelas peta konstan memberi setiap nilai fungtor itu satu titik terpilih,
meskipun kita tetap menuliskan kodomain sumber sebagai $\mathbf{Set}$.

Pemetaan koordinat memberi bijeksi alami

$$
\pi_n(X\times Y,(x,y))
\cong
\pi_n(X,x)\times\pi_n(Y,y).
$$

## Model sfera, kubus, dan cakram {#o012-rbt-l17-s04}

Untuk pasangan ruang $(Y,A)$, hasil bagi $Y/A$ berarti ruang hasil bagi yang
mengidentifikasi semua titik $A$ menjadi satu titik dan tidak membuat
identifikasi lain. Catatan ini berasal dari catatan pinggir sumber.

Jika $n\geq1$, terdapat homeomorfisma bertitik

$$
S^n
\cong
I^n/\partial I^n
\cong
D^n/\partial D^n,
$$

dengan titik basis sebagai citra subruang batas yang diruntuhkan. Karena itu
peta bertitik dari $S^n$ ke $(X,x)$ sama datanya dengan peta pasangan

$$
f\colon(I^n,\partial I^n)\longrightarrow(X,\{x\}),
$$

dan juga dengan peta pasangan dari $(D^n,\partial D^n)$.

Homotopi relatif terhadap $A$ antara dua peta pasangan
$f_0,f_1\colon(Y,A)\to(X,\{x\})$ adalah homotopi
$H\colon I\times Y\to X$ yang memenuhi

$$
H(0,y)=f_0(y),
\qquad
H(1,y)=f_1(y),
\qquad
H(t,a)=x
$$

untuk semua $y\in Y$, $t\in I$, dan $a\in A$. Dengan relasi ini,

$$
[(S^n,1),(X,x)]_*
\cong
[(I^n,\partial I^n),(X,\{x\})]
\cong
[(D^n,\partial D^n),(X,\{x\})]
$$

untuk $n\geq1$.

Pengecualian $n=0$ penting: $I^0$ dan $D^0$ masing-masing satu titik dan
batasnya kosong, sehingga hasil bagi tersebut tetap satu titik, bukan
$S^0$. Jadi model hasil bagi kubus dan cakram di atas tidak dipakai untuk
$\pi_0$.

## Adjungsi loop dan struktur grup {#o012-rbt-l17-s05}

Ambil $n\geq1$ dan wakil
$f\colon(I^n,\partial I^n)\to(X,\{x\})$. Tuliskan titik kubus sebagai
$(u,t)\in I^{n-1}\times I$. Rumus

$$
\widehat f(u)(t):=f(u,t)
$$

memberi peta pasangan

$$
\widehat f\colon
(I^{n-1},\partial I^{n-1})
\longrightarrow
(\Omega_xX,c_x).
$$

Syarat batas pada $f$ memastikan bahwa $\widehat f(u)$ adalah loop di $x$
dan bahwa $u\in\partial I^{n-1}$ dikirim ke loop konstan. Proses yang
mengubah $f(u,t)$ menjadi $u\mapsto(t\mapsto f(u,t))$ dan proses kebalikannya
saling invers serta mempertahankan homotopi relatif. Maka

$$
\pi_n(X,x)
\cong
\pi_{n-1}(\Omega_xX,c_x)
$$

untuk setiap $n\geq1$; ketika $n=1$, ruas kanan ialah himpunan komponen
bertitik $\pi_0(\Omega_xX,c_x)$.

Konkatenasi loop kontinu
$\mu\colon\Omega_xX\times\Omega_xX\to\Omega_xX$ menginduksi operasi
biner melalui rantai pemetaan berikut:

$$
\begin{aligned}
\pi_n(X,x)\times\pi_n(X,x)
&\cong
\pi_{n-1}(\Omega_xX,c_x)
\times
\pi_{n-1}(\Omega_xX,c_x)\\
&\cong
\pi_{n-1}(\Omega_xX\times\Omega_xX,(c_x,c_x))\\
&\xrightarrow{\ \mu_*\ }
\pi_{n-1}(\Omega_xX,c_x)
\cong
\pi_n(X,x).
\end{aligned}
$$

Dalam model kubus, operasi ini adalah konkatenasi kronologis pada koordinat
terakhir. Jika $u\in I^{n-1}$ dan $t\in I$, definisikan

$$
(f\#_ng)(u,t)
=
\begin{cases}
f(u,2t),&0\leq t\leq\tfrac12,\\
g(u,2t-1),&\tfrac12\leq t\leq1.
\end{cases}
$$

Kedua cabang bertemu di $x$ pada $t=\tfrac12$ karena sisi
$t=1$ dari $f$ dan sisi $t=0$ dari $g$ berada di batas kubus. Operasi itu
turun ke kelas homotopi relatif. Kelas peta konstan menjadi identitas,
pembalikan koordinat terakhir

$$
f^{-1}(u,t):=f(u,1-t)
$$

memberi invers, dan reparametrisasi interval memberi asosiativitas pada
kelas homotopi. Postkomposisi oleh peta bertitik mempertahankan semua rumus.
Jadi, untuk setiap $n\geq1$, diperoleh fungtor

$$
\pi_n\colon\mathbf{Top}_*\longrightarrow\mathbf{Grp}.
$$

Sumber memperkenalkan hasil berikut sebagai abstraksi terkenal yang muncul
sesudah definisi awal grup homotopi lebih tinggi sekitar tahun 1932.

## Argumen Eckmann--Hilton yang bertipe tepat {#o012-rbt-l17-s06}

::: {.lemma #o012-rbt-l17-lem-002}
**Lema 17.2 (argumen Eckmann--Hilton).** Misalkan himpunan $M$ membawa dua
operasi biner berunit

$$
\circ,\#\colon M\times M\longrightarrow M
$$

dengan unit masing-masing $e_\circ$ dan $e_\#$, serta memenuhi hukum
pertukaran

$$
(a\circ b)\#(c\circ d)
=
(a\#c)\circ(b\#d)
$$

untuk semua $a,b,c,d\in M$. Maka kedua unit sama, kedua operasi sama, dan
operasi tunggal itu asosiatif serta komutatif. Jadi $M$ merupakan monoid
komutatif. Jika operasi tunggal itu diketahui mempunyai invers, maka $M$
merupakan grup abelian.
:::

::: {.proof #o012-rbt-l17-proof-004}
**Bukti.** Pertama, hukum pertukaran memberi

$$
\begin{aligned}
e_\#
&=e_\#\#e_\#\\
&=(e_\#\circ e_\circ)\#(e_\circ\circ e_\#)\\
&=(e_\#\#e_\circ)\circ(e_\circ\#e_\#)\\
&=e_\circ\circ e_\circ
=e_\circ.
\end{aligned}
$$

Tuliskan unit bersama ini sebagai $e$. Selanjutnya,

$$
\begin{aligned}
a\circ b
&=(a\#e)\circ(e\#b)\\
&=(a\circ e)\#(e\circ b)\\
&=a\#b.
\end{aligned}
$$

Jadi kedua operasi berimpit; tuliskan hasilnya sebagai $ab$. Untuk
komutativitas, gunakan pertukaran sekali lagi:

$$
ab
=(e\circ a)\#(b\circ e)
=(e\#b)\circ(a\#e)
=ba.
$$

Untuk asosiativitas,

$$
(ab)c
=(a\circ b)\#(e\circ c)
=(a\#e)\circ(b\#c)
=a(bc).
$$

Dengan demikian ada operasi berunit yang asosiatif dan komutatif, yakni
monoid komutatif. Tidak ada langkah yang menghasilkan invers. Sebagai
kontracontoh terhadap kesimpulan grup pada sumber, ambil
$M=\mathbb Z_{\geq0}$ dan pakai penjumlahan sebagai kedua operasi, dengan
unit $0$. Semua hipotesis terpenuhi, tetapi unsur positif tidak mempunyai
invers aditif. Bila invers diketahui dari struktur lain, monoid komutatif itu
barulah grup abelian.
:::

## Grup topologis dan loop teriterasi {#o012-rbt-l17-s07}

::: {.example #o012-rbt-l17-exa-001}
**Contoh 17.1 (grup fundamental suatu grup topologis).** Jika $G$ grup
topologis dengan unsur identitas $e$, maka $\pi_1(G,e)$ abelian. Pernyataan
ini tidak memerlukan $G$ menjadi grup Lie; perluasan tersebut merupakan isi
catatan pinggir sumber.

Pada kelas loop ada dua operasi. Yang pertama ialah konkatenasi kronologis
$[\alpha]\#[\beta]=[\alpha\#\beta]$. Yang kedua berasal dari perkalian
titik demi titik,

$$
(\alpha\cdot\beta)(t):=\alpha(t)\beta(t).
$$

Kontinuitas perkalian grup membuat rumus kedua berupa loop kontinu dan
membuatnya turun ke kelas homotopi: jika $H$ dan $K$ adalah homotopi loop,
maka $(s,t)\mapsto H(s,t)K(s,t)$ adalah homotopi bagi hasil kalinya. Kelas
loop konstan $c_e$ menjadi unit untuk kedua operasi. Pada wakil loop,
identitas potongan

$$
(\alpha\#\beta)\cdot(\gamma\#\delta)
=
(\alpha\cdot\gamma)\#(\beta\cdot\delta)
$$

berlaku, sebab kedua ruas bernilai
$\alpha(2t)\gamma(2t)$ pada paruh pertama dan
$\beta(2t-1)\delta(2t-1)$ pada paruh kedua. Jadi kelas-kelasnya memenuhi
hukum pertukaran. Lema 17.2 membuat kedua operasi sama dan komutatif;
struktur konkatenasi sudah mempunyai invers, sehingga hasilnya grup abelian.
:::

Sekarang iterasikan identifikasi loop. Bagi $n\geq2$,

$$
\pi_n(X,x)
\cong
\pi_{n-1}(\Omega_xX,c_x)
\cong
\pi_{n-2}(\Omega_x^2X,c_{c_x}),
$$

dengan

$$
\Omega_x^2X:=\Omega_{c_x}(\Omega_xX).
$$

Titik-titik $\Omega_x^2X$ dapat dipandang sebagai peta
$f\colon I^2\to X$ yang mengirim seluruh $\partial I^2$ ke $x$. Ada dua
operasi konkatenasi kontinu: $\#_1$ pada koordinat pertama dan $\#_2$ pada
koordinat kedua. Untuk $f_1,f_2\in\Omega_x^2X$, rumusnya ialah

$$
(f_1\#_1f_2)(s,t)
=
\begin{cases}
f_1(2s,t),&0\leq s\leq\tfrac12,\\
f_2(2s-1,t),&\tfrac12\leq s\leq1,
\end{cases}
$$

dan

$$
(f_1\#_2f_2)(s,t)
=
\begin{cases}
f_1(s,2t),&0\leq t\leq\tfrac12,\\
f_2(s,2t-1),&\tfrac12\leq t\leq1.
\end{cases}
$$

Pada jahitan $s=\tfrac12$, rumus pertama cocok karena
$f_1(1,t)=x=f_2(0,t)$. Pada jahitan $t=\tfrac12$, rumus kedua cocok karena
$f_1(s,1)=x=f_2(s,0)$. Ini juga menunjukkan kontinuitas melalui lema
penempelan. Pada setiap sisi luar, salah satu argumen koordinat bernilai
$0$ atau $1$, sehingga hasilnya tetap $x$. Cabang kedua $\#_2$ memakai
$f_2$, memperbaiki pengulangan $f_1$ pada sumber.

Kedua cara menggabungkan empat peta menghasilkan peta mentah yang sama:

$$
(f_1\#_1f_2)\#_2(f_3\#_1f_4)
=
(f_1\#_2f_3)\#_1(f_2\#_2f_4).
$$

Inventaris linearnya pada empat kuadran $I^2$ ialah:

1. $0\leq s,t\leq\tfrac12$: nilai
   $f_1(2s,2t)$;
2. $\tfrac12\leq s\leq1$ dan $0\leq t\leq\tfrac12$: nilai
   $f_2(2s-1,2t)$;
3. $0\leq s\leq\tfrac12$ dan $\tfrac12\leq t\leq1$: nilai
   $f_3(2s,2t-1)$;
4. $\tfrac12\leq s,t\leq1$: nilai
   $f_4(2s-1,2t-1)$.

Pada peta mentah, konkatenasi hanya berunit dan asosiatif hingga homotopi.
Karena itu Lema 17.2 diterapkan **sesudah** $\#_1$ dan $\#_2$ turun ke kelas
homotopi. Untuk setiap $n\geq2$, kedua operasi menginduksi operasi pada

$$
A_n:=\pi_{n-2}(\Omega_x^2X,c_{c_x}).
$$

Kelas peta konstan menjadi unit bersama, dan identitas empat kuadran memberi
hukum pertukaran. Lema 17.2 menyatakan bahwa kedua operasi berimpit dan
komutatif. Struktur grup pada $\pi_n$, yang sudah dibangun lewat pembalikan
koordinat, menyediakan invers yang tidak berasal dari lema tersebut. Dalam
pilihan koordinat Bagian 17.5, operasi $\#_2$ adalah konkatenasi pada
koordinat terakhir dan karenanya tepat hukum grup yang sudah dibangun.

::: {.proposition #o012-rbt-l17-prop-001}
**Proposisi 17.1 (komutativitas grup homotopi lebih tinggi).** Untuk setiap
ruang bertitik $(X,x)$ dan setiap $n\geq2$, grup $\pi_n(X,x)$ abelian.
:::

::: {.proof #o012-rbt-l17-proof-005}
**Bukti.** Identifikasi
$\pi_n(X,x)\cong A_n$ memindahkan kedua konkatenasi koordinat ke dua operasi
berunit pada himpunan yang sama. Identitas empat kuadran memberi hukum
pertukaran pada kelas homotopi, sehingga Lema 17.2 membuat kedua operasi
sama dan komutatif. Salah satu operasi adalah hukum grup $\pi_n$ dari
Bagian 17.5, lengkap dengan invers melalui pembalikan koordinat. Karena itu
hukum grup tersebut komutatif, yakni $\pi_n(X,x)$ grup abelian.
:::

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l17-mastery}

Enam pemeriksaan berikut merupakan materi asli edisi. Semuanya terbatas pada
isi Unit 17: keunikan dan kesetiaan, kepenuhan, model relatif, koreksi
Eckmann--Hilton, jahitan empat kuadran, serta dua penerapan komutativitas.
Tidak ada pemeriksaan yang memakai materi Kuliah 18.

::: {.exercise #o012-rbt-l17-mcheck-001 data-origin="edition-original"}
**Pemeriksaan penguasaan 17.1 (keunikan dan komponen ruang penutup).**
Buktikan Lema 17.1 dari keunikan pengangkatan lintasan. Lalu jelaskan secara
lengkap mengapa kesamaan dua pemetaan ruang penutup pada serat di atas satu
titik basis memaksa kesamaan keduanya, bahkan bila ruang total sumber tidak
terhubung.
:::

## Solusi Pemeriksaan 17.1 {#o012-rbt-l17-sol-001}

Misalkan $\pi\circ f=p=\pi\circ g$ dan $f(y_0)=g(y_0)$. Bagi $y\in Y$,
pilih lintasan $\gamma\colon y_0\rightsquigarrow y$. Kedua komposit
$f\circ\gamma$ dan $g\circ\gamma$ memproyeksi ke $p\circ\gamma$ dan mulai
di titik yang sama. Keunikan pengangkatan memberi
$f\circ\gamma=g\circ\gamma$, maka evaluasi di $1$ memberi $f(y)=g(y)$.
Karena $y$ sebarang, kedua peta sama.

Sekarang ambil $X$ terhubung dan SLSC, ruang penutup
$\pi_i\colon Z_i\to X$, serta pemetaan ruang penutup
$f,g\colon Z_1\to Z_2$ yang sama pada $(Z_1)_{x_0}$. Setiap komponen
lintasan $C\subseteq Z_1$ memetakan surjektif ke $X$: pilih titik dalam
$C$, angkat lintasan di $X$ dari citranya menuju $x_0$, dan titik akhir
pengangkatan tetap di $C$. Jadi ada $z_C\in C\cap(Z_1)_{x_0}$. Peta
$f|_C$ dan $g|_C$ sama di $z_C$ dan terletak di atas peta
$\pi_1|_C\colon C\to X$. Lema 17.1 memberi $f|_C=g|_C$. Mengambil semua
komponen memberi $f=g$. Jika $X$ tidak terhubung, ulangi argumen pada setiap
komponen lintasan terbuka ruang basis.

::: {.exercise #o012-rbt-l17-mcheck-002 data-origin="edition-original"}
**Pemeriksaan penguasaan 17.2 (konstruksi kepenuhan).** Diberikan
transformasi natural $\eta\colon\rho_1\Rightarrow\rho_2$ antara monodromi
dua ruang penutup, bangun pemetaan ruang penutup yang menginduksinya.
Buktikan bahwa peta itu kontinu. Untuk basis terhubung, tuliskan pula
persamaan ekuivariansi kanan pada serat titik basis dan jelaskan mengapa tidak
ada aksi kiri Unit 16 yang dipakai.
:::

## Solusi Pemeriksaan 17.2 {#o012-rbt-l17-sol-002}

Untuk $z\in Z_1$ dengan $\pi_1(z)=x$, satu-satunya definisi yang mungkin
ialah

$$
F(z)=\eta_x(z).
$$

Karena komponen $\eta_x$ memetakan $(Z_1)_x$ ke $(Z_2)_x$, berlaku
$\pi_2F=\pi_1$, dan pembatasan $F$ pada setiap serat tepat $\eta_x$.

Untuk kontinuitas, pilih lingkungan terbuka terhubung lintasan $U\ni x$
yang diliputi secara merata oleh kedua penutup. Beri label lembaran penutup
pertama dengan $A_1=(Z_1)_x$ dan lembaran penutup kedua dengan
$A_2=(Z_2)_x$. Dalam trivialiasi

$$
\pi_i^{-1}(U)\cong U\times A_i,
$$

sebuah titik $(u,a)$ diperoleh dengan mentranspor $a$ sepanjang lintasan di
$U$ dari $x$ ke $u$. Naturalitas terhadap lintasan itu memberi

$$
F(u,a)=(u,\eta_x(a)).
$$

Koordinat kedua adalah satu fungsi tetap di antara himpunan diskret, jadi
rumus lokal itu kontinu. Lingkungan-lingkungan tersebut menutupi $X$;
akibatnya $F$ kontinu secara global dan merupakan pemetaan ruang penutup.

Jika $X$ terhubung, $G=\pi_1(X,x_0)$, dan $g\in G$, naturalitas pada loop
memberi

$$
\eta_{x_0}(z\cdot g)=\eta_{x_0}(z)\cdot g.
$$

Ini ekuivariansi untuk monodromi **kanan** melalui postkonkatenasi. Aksi kiri
serat demi serat Unit 16 memakai prekonkatenasi dan tidak muncul dalam
konstruksi ini.

::: {.exercise #o012-rbt-l17-mcheck-003 data-origin="edition-original"}
**Pemeriksaan penguasaan 17.3 (model sfera, kubus, cakram, dan $n=0$).**
Bagi $n\geq1$, buktikan korespondensi antara kelas homotopi bertitik dari
$S^n$ dan kelas homotopi relatif dari kubus atau cakram. Nyatakan semua
syarat homotopi relatif. Lalu tunjukkan secara eksplisit mengapa model hasil
bagi itu tidak boleh dipakai untuk $n=0$.
:::

## Solusi Pemeriksaan 17.3 {#o012-rbt-l17-sol-003}

Untuk $n\geq1$, meruntuhkan $\partial I^n$ menjadi satu titik menghasilkan
ruang yang homeomorfik dengan $S^n$; demikian pula bagi
$D^n/\partial D^n$. Menurut sifat universal hasil bagi, peta kontinu

$$
\bar f\colon I^n/\partial I^n\longrightarrow X
$$

yang mengirim titik runtuhan ke $x$ tepat sama datanya dengan peta
$f\colon I^n\to X$ yang memenuhi $f(\partial I^n)=\{x\}$. Pernyataan yang
sama berlaku untuk $D^n$.

Dua peta pasangan $f_0,f_1\colon(Y,A)\to(X,\{x\})$ setara relatif terhadap
$A$ bila ada $H\colon I\times Y\to X$ dengan

$$
H(0,y)=f_0(y),
\quad
H(1,y)=f_1(y),
\quad
H(t,a)=x
$$

untuk semua $y,t,a$. Syarat terakhir tepat memastikan bahwa homotopi turun
ke homotopi bertitik pada $Y/A$. Mengangkat homotopi dari hasil bagi memberi
arah sebaliknya. Jadi diperoleh bijeksi ketiga himpunan kelas homotopi pada
Bagian 17.4.

Untuk $n=0$, $I^0=D^0=\{*\}$ dan batasnya kosong. Meruntuhkan himpunan kosong
tidak menambahkan titik atau identifikasi, sehingga
$I^0/\partial I^0$ dan $D^0/\partial D^0$ masing-masing satu titik. Akan
tetapi $S^0=\{1,-1\}$ mempunyai dua titik. Maka model hasil bagi tersebut
gagal tepat pada $n=0$, walaupun definisi
$\pi_0(X,x)=[(S^0,1),(X,x)]_*$ tetap sah sebagai himpunan bertitik.

::: {.exercise #o012-rbt-l17-mcheck-004 data-origin="edition-original"}
**Pemeriksaan penguasaan 17.4 (apa yang benar-benar dibuktikan
Eckmann--Hilton).** Buktikan bahwa dua operasi berunit yang memenuhi hukum
pertukaran berimpit dan membentuk monoid komutatif. Berikan kontracontoh
yang menunjukkan bahwa invers tidak mengikuti dari hipotesis itu. Nyatakan
hipotesis tambahan yang menghasilkan grup abelian.
:::

## Solusi Pemeriksaan 17.4 {#o012-rbt-l17-sol-004}

Misalkan unit kedua operasi ialah $e_\circ$ dan $e_\#$. Dengan hukum
pertukaran,

$$
\begin{aligned}
e_\#
&=e_\#\#e_\#\\
&=(e_\#\circ e_\circ)\#(e_\circ\circ e_\#)\\
&=(e_\#\#e_\circ)\circ(e_\circ\#e_\#)\\
&=e_\circ.
\end{aligned}
$$

Tuliskan unit bersama sebagai $e$. Lalu

$$
a\circ b
=(a\#e)\circ(e\#b)
=(a\circ e)\#(e\circ b)
=a\#b,
$$

sehingga ada satu operasi, ditulis $ab$. Hukum pertukaran memberi

$$
ab=(e\circ a)\#(b\circ e)
=(e\#b)\circ(a\#e)=ba
$$

dan

$$
(ab)c=(a\circ b)\#(e\circ c)
=(a\#e)\circ(b\#c)=a(bc).
$$

Jadi operasinya berunit, asosiatif, dan komutatif. Ambil
$M=\mathbb Z_{\geq0}$ dengan kedua operasi sama dengan penjumlahan dan unit
$0$. Hukum pertukaran berlaku karena penjumlahan komutatif, tetapi $1$ tidak
mempunyai invers aditif di $\mathbb Z_{\geq0}$. Maka kesimpulan umum hanya
monoid komutatif. Jika setiap unsur diketahui mempunyai invers untuk salah
satu operasi, kedua
operasi yang telah berimpit membentuk grup abelian.

::: {.exercise #o012-rbt-l17-mcheck-005 data-origin="edition-original"}
**Pemeriksaan penguasaan 17.5 (jahitan dan empat kuadran).** Tuliskan rumus
$\#_1$ dan $\#_2$ pada loop ganda. Buktikan bahwa cabang-cabangnya cocok,
bahwa hasilnya tetap mengirim batas $I^2$ ke $x$, dan bahwa kedua urutan
penggabungan empat peta memberi nilai yang sama pada setiap kuadran. Jelaskan
mengapa Eckmann--Hilton baru diterapkan pada kelas homotopi.
:::

## Solusi Pemeriksaan 17.5 {#o012-rbt-l17-sol-005}

Dengan konvensi kronologis, $f_1$ ditempuh pada paruh pertama dan $f_2$ pada
paruh kedua. Rumusnya

$$
(f_1\#_1f_2)(s,t)=
\begin{cases}
f_1(2s,t),&s\leq\tfrac12,\\
f_2(2s-1,t),&s\geq\tfrac12,
\end{cases}
$$

dan

$$
(f_1\#_2f_2)(s,t)=
\begin{cases}
f_1(s,2t),&t\leq\tfrac12,\\
f_2(s,2t-1),&t\geq\tfrac12.
\end{cases}
$$

Pada jahitan pertama, nilai kedua cabang ialah
$f_1(1,t)=x=f_2(0,t)$; pada jahitan kedua nilainya
$f_1(s,1)=x=f_2(s,0)$. Lema penempelan memberi kontinuitas. Jika $(s,t)$
berada pada batas persegi, argumen salah satu koordinat pada setiap cabang
berada di $0$ atau $1$, sehingga nilainya tetap $x$.

Baik
$(f_1\#_1f_2)\#_2(f_3\#_1f_4)$ maupun
$(f_1\#_2f_3)\#_1(f_2\#_2f_4)$ bernilai, berturut-turut pada kuadran kiri
bawah, kanan bawah, kiri atas, dan kanan atas,

$$
f_1(2s,2t),
\quad
f_2(2s-1,2t),
\quad
f_3(2s,2t-1),
\quad
f_4(2s-1,2t-1).
$$

Jadi hukum pertukaran berlaku bahkan pada wakil mentah. Namun peta konstan
bukan unit ketat bagi konkatenasi berkecepatan ganda, dan asosiativitas juga
memerlukan reparametrisasi. Keduanya menjadi persamaan setelah homotopi
relatif terhadap batas. Karena itu struktur berunit yang menjadi masukan
Lema 17.2 berada pada **kelas homotopi**, bukan pada ruang peta mentah.

::: {.exercise #o012-rbt-l17-mcheck-006 data-origin="edition-original"}
**Pemeriksaan penguasaan 17.6 (dua penerapan komutativitas).** Buktikan
bahwa $\pi_1(G,e)$ abelian untuk setiap grup topologis $G$. Lalu buktikan
bahwa $\pi_n(X,x)$ abelian untuk setiap $n\geq2$ dengan memakai ruang loop
teriterasi. Dalam kedua bagian, sebutkan dari mana invers berasal.
:::

## Solusi Pemeriksaan 17.6 {#o012-rbt-l17-sol-006}

Untuk loop pada grup topologis, gunakan konkatenasi $\#$ dan perkalian titik
demi titik $\cdot$. Kedua operasi turun ke $\pi_1(G,e)$ dan mempunyai kelas
loop konstan sebagai unit. Pada wakil,

$$
(\alpha\#\beta)\cdot(\gamma\#\delta)
=(\alpha\cdot\gamma)\#(\beta\cdot\delta),
$$

karena identitas itu dapat diperiksa pada kedua paruh interval. Maka
Eckmann--Hilton membuat operasi berimpit dan komutatif. Invers telah tersedia
dari struktur grup konkatenasi: kelas $[\alpha]^{-1}$ diwakili loop balik
$t\mapsto\alpha(1-t)$. Jadi $\pi_1(G,e)$ grup abelian. Tidak ada sifat Lie
yang digunakan.

Untuk $n\geq2$, gunakan

$$
\pi_n(X,x)
\cong
\pi_{n-2}(\Omega_x^2X,c_{c_x}).
$$

Konkatenasi koordinat pertama dan kedua pada loop ganda menginduksi dua
operasi pada ruas kanan. Kelas peta konstan menjadi unit bersama, dan
perhitungan empat kuadran memberi hukum pertukaran. Jadi kedua operasi sama
dan komutatif. Salah satunya adalah struktur grup $\pi_n$ yang dibangun dari
konkatenasi koordinat; inversnya diwakili oleh pembalikan koordinat tersebut.
Dengan invers yang sudah tersedia secara terpisah, monoid komutatif hasil
Eckmann--Hilton adalah grup abelian.
