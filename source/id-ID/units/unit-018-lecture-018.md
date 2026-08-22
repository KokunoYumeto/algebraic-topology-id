---
title: "Topologi Aljabar"
subtitle: "Unit 18: Transpor Grup Homotopi, Bundel Serat, dan Barisan Eksak Panjang"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l18-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 3482--3677 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L3482-L3677)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang 196 baris itu dimulai dengan penanda Kuliah 18 dan berakhir pada
baris kosong tepat sebelum penanda Kuliah 19 pada baris 3678. Materi sumber
dan adaptasi Indonesia ini tersedia di bawah [Creative Commons Attribution
4.0 International](https://creativecommons.org/licenses/by/4.0/).

Perubahan edisi mencakup penerjemahan, pemformatan ulang agar mudah dibaca,
pemberian pengenal stabil, dan pemindahan kelima catatan pinggir ke urutan
bacaan utama. Edisi memperbaiki domain yang salah tipe pada peta terinduksi,
membatasi target $\mathbf{Ab}$ pada $n\geq2$, mendefinisikan norma pada
konstruksi transpor, dan melengkapi bukti transpor, hasil kali, perubahan
titik basis, serta invariansi homotopi. Definisi bundel memakai
homeomorfisma di atas lingkungan; contoh Hopf kini menampilkan dua
trivialisasi lokal lengkap. Ekor bertitik barisan eksak panjang diberi tipe
yang benar dan konvensi kosetnya diselaraskan dengan aksi monodromi kanan
kronologis. Teorema barisan eksak panjang tetap dinyatakan secara jujur
sebagai hasil eksternal yang dipakai sebagai kotak hitam; edisi hanya
menjelaskan peta penghubungnya.

Contoh pada Notes.tex baris 3499--3501 sepenuhnya dikomentari dalam sumber,
sehingga tidak dimasukkan sebagai teks pembaca. Contoh itu telah diaudit:
ia mengomposisikan representasi bernilai himpunan dengan fungtor ruang
vektor bebas, tetapi menyingkat $\Pi_1(X)$ menjadi $\Pi_1$ pada kemunculan
kedua. Tidak ada lingkungan latihan, gambar eksternal, atau aset terpisah
dalam rentang sumber aktif ini.

Keenam pemeriksaan penguasaan, keenam petunjuk, dan keenam solusi lengkap
merupakan materi asli edisi dan tersedia di bawah CC BY 4.0. Edisi ini
bersifat independen; edisi ini tidak disponsori, didukung, disahkan, ataupun
diberi status resmi oleh David Michael Roberts atau institusinya. Produksi
edisi ini dibantu oleh **OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini
menambah transparansi proses dan tidak mengurangi kredit penulis sumber
ataupun kredit kontributor manusia.

# Kuliah 18 {#o012-rbt-l18}

## Fungtorialitas dan contoh awal {#o012-rbt-l18-s01}

Untuk $n\geq1$, penetapan

$$
\begin{aligned}
(X,x)&\longmapsto\pi_n(X,x),\\
\bigl(f\colon(X,x)\to(Y,y)\bigr)
&\longmapsto
\bigl(f_*\colon\pi_n(X,x)\to\pi_n(Y,y)\bigr)
\end{aligned}
$$

merupakan fungtor

$$
\mathbf{Top}_*\longrightarrow\mathbf{Grp}.
$$

Karena Unit 17 membuktikan bahwa $\pi_n(X,x)$ abelian untuk $n\geq2$,
bagi setiap $n\geq2$ fungtor ini memperhalus menjadi

$$
\pi_n\colon\mathbf{Top}_*\longrightarrow\mathbf{Ab}.
$$

::: {.source-audit #o012-rbt-l18-audit-001}
**Audit sumber 18.1.** Notes.tex baris 3485 mencetak
$f_*\colon\pi_1(X,x)\to\pi_n(Y,y)$; domain bertipe benar adalah
$\pi_n(X,x)$. Baris 3487 juga menyatakan target $\mathbf{Ab}$ tanpa
membatasi $n$. Untuk $n=1$, grup fundamental tidak harus abelian, sehingga
target $\mathbf{Ab}$ hanya benar bagi $n\geq2$.
:::

::: {.example #o012-rbt-l18-ex-001}
**Contoh 18.1 (ruang diskret).** Jika $T$ ruang diskret, maka

$$
\pi_n(T,*)=1,
$$

sebab setiap pemetaan $S^n\to T$ konstan: sfera $S^n$ terhubung.
:::

::: {.example #o012-rbt-l18-ex-002}
**Contoh 18.2 (ruang kontraktil).** Jika $X$ kontraktil, misalnya daerah
berbentuk bintang di dalam suatu ruang vektor topologis, maka

$$
\pi_n(X,x)=1.
$$
:::

Ingat kembali bahwa ruang penutup $Z\to X$ menentukan representasi

$$
\Pi_1(X)\longrightarrow\mathbf{Set}.
$$

Namun, tidak ada sesuatu yang istimewa tentang kategori $\mathbf{Set}$ di
sini. Kita dapat memakai kategori lain, misalnya kategori $\mathbf{Fin}$
dari himpunan berhingga, kategori $\mathbf{Vect}$ dari ruang vektor,
kategori $\mathbf{Ab}$ dari grup abelian, atau, secara lebih umum, kategori
$R\mathbf{Mod}$ dari modul atas $R$, dengan $R$ suatu gelanggang yang
ditetapkan.

## Transpor grup homotopi sepanjang lintasan {#o012-rbt-l18-s02}

::: {.proposition #o012-rbt-l18-prop-001}
**Proposisi 18.1 (representasi transpor).** Tetapkan ruang $X$ dan
$n\geq1$. Penetapan

$$
x\longmapsto\pi_n(X,x)
$$

merupakan komponen objek dari representasi

$$
\Pi_1(X)\longrightarrow\mathbf{Grp}.
$$

Untuk $n\geq2$, representasi ini mengambil nilai dalam $\mathbf{Ab}$.
:::

::: {.proof #o012-rbt-l18-proof-001}
**Bukti.** Diberikan lintasan

$$
\gamma\colon[0,1]\to X,\qquad x\rightsquigarrow y,
$$

dan pemetaan

$$
\alpha\colon(I^n,\partial I^n)\to(X,x)
$$

yang mewakili suatu kelas dalam $\pi_n(X,x)$, kita membangun kelas dalam
$\pi_n(X,y)$. Untuk konstruksi ini, tuliskan

$$
I=\left[-\frac12,\frac12\right]
$$

dan gunakan norma maksimum

$$
\lVert\mathbf u\rVert_\infty
=\max_{1\leq k\leq n}|u_k|.
$$

Tetapkan homeomorfisma yang mempertahankan orientasi, diterapkan pada setiap
koordinat,

$$
i\colon
\left[-\frac14,\frac14\right]^n
\xrightarrow{\simeq}I^n,
$$

serta homeomorfisma yang mempertahankan orientasi

$$
j\colon
\left[\frac14,\frac12\right]\xrightarrow{\simeq}[0,1].
$$

Definisikan $\alpha^\gamma\colon I^n\to X$ oleh

$$
\alpha^\gamma(\mathbf u)=
\begin{cases}
\alpha(i(\mathbf u)),
&
\lVert\mathbf u\rVert_\infty\leq\frac14,\\[3pt]
\gamma\!\left(j(\lVert\mathbf u\rVert_\infty)\right),
&
\frac14\leq\lVert\mathbf u\rVert_\infty\leq\frac12.
\end{cases}
$$

Pada jahitan $\lVert\mathbf u\rVert_\infty=\frac14$, kedua rumus bernilai
$x$ karena $\alpha(\partial I^n)=\{x\}$ dan $\gamma(0)=x$. Lema penempelan
memberi kontinuitas. Pada batas luar
$\lVert\mathbf u\rVert_\infty=\frac12$, nilainya $\gamma(1)=y$, sehingga

$$
\alpha^\gamma\colon(I^n,\partial I^n)\to(X,y).
$$

Homotopi relatif terhadap batas antara dua wakil $\alpha$, serta homotopi
yang mempertahankan titik ujung antara dua wakil $\gamma$, dapat dimasukkan
ke rumus sepotong-sepotong yang sama dengan satu parameter tambahan. Karena
semua rumus bertemu pada nilai $x$ atau $y$, lema penempelan parametrik
menunjukkan bahwa $[\alpha^\gamma]$ hanya bergantung pada $[\alpha]$ dan
$[\gamma]$. Jadi kita memperoleh fungsi

$$
T_\gamma\colon\pi_n(X,x)\longrightarrow\pi_n(X,y),
\qquad
T_\gamma[\alpha]=[\alpha^\gamma].
$$

Sekarang periksa struktur grup. Wakil produk
$[\alpha][\beta]$ dapat dibuat dengan menempatkan wakil $\alpha$ dan
$\beta$ dalam dua kotak yang saling lepas pada kubus pusat dan mengirim
sisa kubus pusat ke $x$. Pada $(\alpha\#\beta)^\gamma$, kedua kotak itu
dikelilingi oleh satu kerah radial yang menelusuri $\gamma$. Pada
$\alpha^\gamma\#\beta^\gamma$, masing-masing mula-mula mempunyai kerah
sendiri. Susutkan kedua kotak secara linear di dalam kubus pusat, geser
kedua kerah dalam hingga berimpit, lalu perluas kerah luar. Pada setiap
tahap, batas kotak dalam bernilai $x$, batas kubus luar bernilai $y$, dan
seluruh perubahan merupakan reparameterisasi sepotong-sepotong yang
menetapkan batas. Lema penempelan memberi homotopi relatif terhadap
$\partial I^n$, sehingga

$$
T_\gamma([\alpha][\beta])
=T_\gamma[\alpha]\,T_\gamma[\beta].
$$

Dengan demikian $T_\gamma$ homomorfisma. Reparameterisasi kerah memberi

$$
T_{\gamma\#\eta}=T_\eta\circ T_\gamma,
\qquad
T_{c_x}=\operatorname{id}.
$$

Lintasan balik $\bar\gamma$ memberi
$T_{\bar\gamma}\circ T_\gamma=T_{c_x}$ dan
$T_\gamma\circ T_{\bar\gamma}=T_{c_y}$, jadi $T_\gamma$ isomorfisma.
Identitas dan komposisi dipertahankan, sehingga kita benar-benar memperoleh
representasi $\Pi_1(X)\to\mathbf{Grp}$. Untuk $n\geq2$, semua grup nilainya
abelian. $\square$

::: {.source-margin #o012-rbt-l18-margin-001}
> **Catatan pinggir sumber.** Sumber menunjuk Hatcher, §4.1, halaman 341,
> untuk bukti bahwa transpor ini homomorfisma. Edisi telah menutup langkah
> tersebut di atas agar unit dapat dibaca mandiri.
:::
:::

::: {.source-audit #o012-rbt-l18-audit-002}
**Audit sumber 18.2.** Notes.tex baris 3513 memakai
$|\mathbf x|$ tanpa mendefinisikannya. Norma maksimum diperlukan agar
$j(|\mathbf x|)$ tetap berada dalam domain
$[\frac14,\frac12]$ pada seluruh kulit kubus; norma Euklides gagal di
sudut-sudut kubus.
:::

Untuk $n=1$, kita telah melihat versi konstruksi ini. Diberikan lintasan
$\gamma\colon x\rightsquigarrow y$, terdapat isomorfisma

$$
\pi_1(X,x)\xrightarrow{\simeq}\pi_1(X,y).
$$

Jika $x=y$, maka $\gamma$ sebuah loop dan automorfisma yang dihasilkan pada
$\pi_1(X,x)$ adalah konjugasi dengan arah yang ditentukan kerah:

$$
T_\gamma([\alpha])
=[\bar\gamma\#\alpha\#\gamma].
$$

Jadi, dengan perkalian kronologis edisi, unsur $[\alpha]$ dikirim ke
$[\gamma]^{-1}[\alpha][\gamma]$.

::: {.remark #o012-rbt-l18-rem-001}
**Catatan 18.1 (titik basis pada ruang terhubung sederhana).** Jika $X$
terhubung sederhana, terdapat isomorfisma kanonik

$$
\pi_n(X,x)\simeq\pi_n(X,y)
$$

untuk setiap $x,y\in X$: dua lintasan dari $x$ ke $y$ homotopik dengan titik
ujung tetap, sehingga menginduksi transpor yang sama. Karena alasan ini,
banyak penulis menghilangkan titik basis ketika titik itu tidak penting.

::: {.source-margin #o012-rbt-l18-margin-002}
> **Catatan pinggir sumber.** Pernyataan yang sama berlaku di dalam satu
> komponen lintasan $X$ yang terhubung sederhana, bagi titik-titik di
> komponen tersebut.
:::
:::

::: {.remark #o012-rbt-l18-rem-002}
**Catatan 18.2 (keluarga grup yang kontinu).** Untuk setiap $n\geq2$,
koleksi $\pi_n(X,x)$ memberikan representasi

$$
\Pi_1(X)\longrightarrow\mathbf{Ab}\longrightarrow\mathbf{Set},
$$

dengan panah kedua fungtor pelupa. Bila $X$ memenuhi hipotesis klasifikasi
ruang penutup dari Unit 17—yakni SLSC menurut konvensi mata kuliah—representasi
bernilai himpunan ini menentukan ruang penutup dari $X$ yang seratnya di atas
$x$ adalah $\pi_n(X,x)$. Untuk ruang yang tidak terhubung, konstruksi ini
berlaku komponen demi komponen. Ruang penutup itu mengingat bahwa serat-serat
tersebut merupakan grup: ia adalah keluarga grup yang bervariasi secara
kontinu, bukan sekadar keluarga himpunan.
:::

## Hasil kali dan invariansi homotopi {#o012-rbt-l18-s03}

::: {.lemma #o012-rbt-l18-lem-001}
**Lema 18.1 (grup homotopi hasil kali).** Tetapkan $n\geq1$. Diberikan ruang
bertitik $(X,x)$ dan $(Y,y)$, terdapat isomorfisma natural

$$
\pi_n(X\times Y,(x,y))
\xrightarrow{\simeq}
\pi_n(X,x)\times\pi_n(Y,y).
$$

::: {.source-margin #o012-rbt-l18-margin-003}
> **Catatan pinggir sumber.** Kata “natural” muncul sebagai catatan pinggir;
> edisi memasukkannya ke pernyataan karena sifat itu benar dan penting.
:::
:::

::: {.proof #o012-rbt-l18-proof-002}
**Bukti.** Proyeksi $\operatorname{pr}_X$ dan $\operatorname{pr}_Y$
memberikan

$$
\Phi([\alpha])
=
\bigl([\operatorname{pr}_X\circ\alpha],
[\operatorname{pr}_Y\circ\alpha]\bigr).
$$

Sebaliknya, dari wakil bertitik
$a\colon S^n\to X$ dan $b\colon S^n\to Y$, bentuk

$$
\Psi([a],[b])=[(a,b)].
$$

Homotopi ke atau dari ruang hasil kali tepat sama datanya dengan sepasang
homotopi koordinat, sehingga kedua rumus terdefinisi baik dan saling invers.
Operasi grup pada model kubus dilakukan dengan konkatenasi koordinat yang
sama; proyeksi mengubahnya menjadi operasi pada masing-masing faktor. Maka
$\Phi$ homomorfisma. Untuk pemetaan bertitik
$f\colon X\to X'$ dan $g\colon Y\to Y'$, kedua cara mengelilingi persegi
naturalitas mengirim $[\alpha]$ ke

$$
\bigl([f\operatorname{pr}_X\alpha],
[g\operatorname{pr}_Y\alpha]\bigr),
$$

sehingga isomorfisma ini natural. $\square$
:::

Sebagaimana pemetaan homotopik semestinya dianggap sama dari sudut pandang
grup fundamental dan ruang penutup, hal yang sama berlaku bagi grup homotopi
lebih tinggi.

::: {.lemma #o012-rbt-l18-lem-002}
**Lema 18.2 (pemetaan homotopik dan perubahan titik basis).** Tetapkan
$n\geq1$. Misalkan $f,g\colon X\to Y$ homotopik melalui

$$
H\colon I\times X\to Y.
$$

Tuliskan $h(t)=H(t,x)$, lintasan dari $f(x)$ ke $g(x)$. Ketiga panah

$$
\pi_n(X,x)\xrightarrow{f_*}\pi_n(Y,f(x)),
\qquad
\pi_n(Y,f(x))\xrightarrow[\simeq]{T_h}\pi_n(Y,g(x)),
\qquad
\pi_n(X,x)\xrightarrow{g_*}\pi_n(Y,g(x))
$$

membentuk segitiga komutatif; secara ekuivalen,

$$
T_h\circ f_*=g_*.
$$
:::

::: {.proof #o012-rbt-l18-proof-003}
**Bukti.** Ambil wakil bertitik
$\alpha\colon(S^n,*)\to(X,x)$. Rumus

$$
K(t,s)=H(t,\alpha(s))
$$

memberi homotopi bebas dari $f\circ\alpha$ ke $g\circ\alpha$; lintasan yang
ditempuh titik basis selama homotopi itu tepat $h(t)=H(t,x)$. Sisipkan
kerah kecil di sekitar titik basis $S^n$. Pada waktu $t$, kirim kerah
tersebut sepanjang potongan $h|_{[0,t]}$ dan gunakan
$H(t,-)\circ\alpha$ di luar kerah. Rumus-rumus bertemu karena nilai pada
batas kerah adalah $H(t,x)$. Lema penempelan parametrik memberi homotopi
bertitik dari wakil transpor $(f\circ\alpha)^h$ ke $g\circ\alpha$.
Karenanya

$$
T_h(f_*[\alpha])=g_*[\alpha].
$$

Ini berlaku bagi setiap $[\alpha]$, sehingga segitiga komutatif. $\square$
:::

::: {.proposition #o012-rbt-l18-prop-002}
**Proposisi 18.2 (invariansi homotopi).** Tetapkan $n\geq1$. Jika
$f\colon X\to Y$ merupakan ekuivalensi homotopi, maka

$$
f_*\colon\pi_n(X,x)\xrightarrow{\simeq}\pi_n(Y,f(x))
$$

merupakan isomorfisma.
:::

::: {.proof #o012-rbt-l18-proof-004}
**Bukti.** Untuk membedakan titik basis, tuliskan

$$
f_*^{\,u}\colon\pi_n(X,u)\longrightarrow\pi_n(Y,f(u)).
$$

Pilih invers homotopi $g\colon Y\to X$, homotopi
$H\colon g f\simeq\operatorname{id}_X$, dan
$K\colon f g\simeq\operatorname{id}_Y$. Lintasan

$$
h(t)=H(t,x)
$$

berjalan dari $g f(x)$ ke $x$. Menurut Lema 18.2,

$$
T_h\circ g_*^{\,f(x)}\circ f_*^{\,x}
=\operatorname{id}_{\pi_n(X,x)}.
$$

Jadi $f_*^{\,x}$ injektif.

Untuk kesurjektifan, gunakan pula naturalitas transpor. Untuk lintasan
$\lambda\colon u\rightsquigarrow v$ di $X$, penerapan $f$ pada rumus kerah
memberi

$$
f_*^{\,v}\circ T_\lambda
=T_{f\circ\lambda}\circ f_*^{\,u}.
$$

Lintasan

$$
k(t)=K(t,f(x))
$$

berjalan dari $f g f(x)$ ke $f(x)$ dan memberi

$$
T_k\circ f_*^{\,g f(x)}\circ g_*^{\,f(x)}
=\operatorname{id}_{\pi_n(Y,f(x))}.
$$

Maka

$$
\begin{aligned}
f_*^{\,x}\circ T_h\circ g_*^{\,f(x)}
&=
T_{f\circ h}\circ f_*^{\,g f(x)}\circ g_*^{\,f(x)}\\
&=
T_{f\circ h}\circ T_k^{-1}.
\end{aligned}
$$

Ruas kanan isomorfisma karena kedua faktor transpor isomorfisma. Ruas kiri
memfaktorkan melalui $f_*^{\,x}$ dan surjektif; karena itu $f_*^{\,x}$
surjektif. Jadi $f_*^{\,x}$ bijektif dan, karena merupakan homomorfisma, ia
isomorfisma. $\square$
:::

Menghitung grup homotopi sangatlah sulit. Bahkan untuk ruang yang relatif
sederhana seperti sfera, kita memerlukan beragam siasat dan kadang-kadang
hasil dari topologi diferensial.

::: {.source-margin #o012-rbt-l18-margin-004}
> **Catatan pinggir sumber.** Salah satu contohnya ialah teorema Sard.
:::

Kenyataannya, kita tidak mengetahui seluruh grup homotopi dari sfera mana
pun $S^n$ dengan $n>1$. Namun, setelah beberapa grup homotopi ruang standar
diketahui, objek berikut dapat menghasilkan relasi antara grup homotopi
ruang-ruang yang berbeda, bahkan dalam dimensi yang berbeda.

## Bundel serat dan bundel Hopf kompleks {#o012-rbt-l18-s04}

::: {.definition #o012-rbt-l18-def-001}
**Definisi 18.1 (bundel serat).** Sebuah *bundel serat* (*fibre bundle*) di
atas ruang $X$ adalah ruang $P$ bersama pemetaan kontinu
$\pi\colon P\to X$ sedemikian sehingga, untuk setiap $x\in X$, terdapat
lingkungan terbuka $U\ni x$, suatu ruang $F$, dan homeomorfisma

$$
\Phi_U\colon\pi^{-1}(U)\xrightarrow{\cong}U\times F
$$

di atas $U$, yakni

$$
\operatorname{pr}_1\circ\Phi_U
=\pi|_{\pi^{-1}(U)}.
$$

Ruang $X$ disebut *ruang dasar*, $P$ disebut *ruang total*, dan $F$ disebut
*serat tipikal* pada trivialisasi tersebut.

::: {.source-margin #o012-rbt-l18-margin-005}
> **Catatan pinggir sumber.** Frasa “di atas $U$” berarti terdapat panah
> $\Phi_U\colon\pi^{-1}(U)\to U\times F$, panah
> $\pi|_{\pi^{-1}(U)}\colon\pi^{-1}(U)\to U$, dan proyeksi
> $\operatorname{pr}_1\colon U\times F\to U$, dengan
> $\operatorname{pr}_1\circ\Phi_U=\pi|_{\pi^{-1}(U)}$.
:::
:::

Jika $X$ terhubung lintasan, serat-serat $\pi^{-1}(x)$ otomatis
homeomorfik secara nonkanonik. Memang, tarik bundel kembali sepanjang suatu
lintasan di antara dua titik. Bundel di atas interval dapat ditrivialkan,
dan pembatasan trivialisasi pada kedua titik ujung memberi homeomorfisma di
antara kedua serat. Pilihan lintasan dan trivialisasi menjelaskan mengapa
homeomorfisma itu tidak kanonik.

Bundel serat merupakan perumuman besar ruang penutup karena seratnya tidak
lagi harus diskret.

::: {.example #o012-rbt-l18-ex-003}
**Contoh 18.3.** Setiap ruang penutup merupakan bundel serat: pada
lingkungan yang tertutup rata, tiap lembaran dipetakan secara homeomorfik ke
lingkungan tersebut, sehingga seluruh prabayangan homeomorfik dengan hasil
kali lingkungan dan serat diskret.
:::

::: {.example #o012-rbt-l18-ex-004}
**Contoh 18.4 (bundel Hopf kompleks).** Misalkan

$$
S^3=\{(z,w)\in\mathbb C^2:|z|^2+|w|^2=1\}.
$$

Ruang $\mathbb{CP}^1$ adalah garis projektif kompleks; titik-titiknya ditulis
dalam koordinat homogen $[z:w]$. Pemetaan

$$
q\colon S^3\longrightarrow\mathbb{CP}^1,
\qquad
q(z,w)=[z:w],
$$

terdefinisi baik karena $z$ dan $w$ tidak nol secara bersamaan. Serat suatu
titik merupakan satu orbit perkalian skalar oleh

$$
U(1)=\{\lambda\in\mathbb C:|\lambda|=1\},
$$

dan karenanya homeomorfik dengan $S^1$.

Kita periksa trivialisasi lokalnya. Pada

$$
U_z=\{[z:w]:z\neq0\},
\qquad
u=w/z,
$$

definisikan

$$
\Phi_z\colon q^{-1}(U_z)\longrightarrow U_z\times U(1),
\qquad
\Phi_z(z,w)=\left([z:w],\frac z{|z|}\right).
$$

Inversnya, dalam koordinat $[1:u]$, ialah

$$
\Phi_z^{-1}([1:u],\lambda)
=
\left(
\frac{\lambda}{\sqrt{1+|u|^2}},
\frac{\lambda u}{\sqrt{1+|u|^2}}
\right).
$$

Pada

$$
U_w=\{[z:w]:w\neq0\},
\qquad
v=z/w,
$$

definisikan

$$
\Phi_w(z,w)
=
\left([z:w],\frac w{|w|}\right),
$$

dengan invers

$$
\Phi_w^{-1}([v:1],\lambda)
=
\left(
\frac{\lambda v}{\sqrt{1+|v|^2}},
\frac{\lambda}{\sqrt{1+|v|^2}}
\right).
$$

Kedua pasangan rumus saling invers, kontinu, dan mempertahankan proyeksi ke
$\mathbb{CP}^1$. Karena $U_z\cup U_w=\mathbb{CP}^1$, pemetaan $q$ benar-benar
bundel serat dengan serat $U(1)\cong S^1$. Inilah *bundel Hopf kompleks*

$$
S^1\longrightarrow S^3\longrightarrow\mathbb{CP}^1\cong S^2.
$$

Hanya ada sangat sedikit bundel serat yang ruang dasar, ruang total, dan
seratnya semuanya berupa sfera. Jadi bundel Hopf kompleks agak tidak tipikal,
tetapi sangat konkret dan merupakan contoh uji yang baik bagi gagasan baru.
:::

## Barisan eksak {#o012-rbt-l18-s05}

::: {.definition #o012-rbt-l18-def-002}
**Definisi 18.2 (keeksakan).** Suatu barisan grup dan homomorfisma

$$
\cdots\to
A_{n-1}\xrightarrow{f_{n-1}}
A_n\xrightarrow{f_n}
A_{n+1}\to\cdots
$$

disebut *eksak pada $A_n$* jika

$$
\ker(f_n)=\operatorname{im}(f_{n-1}).
$$

Barisan itu disebut *eksak* jika eksak pada setiap suku. Definisi ini
berlaku bagi grup, termasuk grup abelian bila semua objeknya abelian.
:::

::: {.example #o012-rbt-l18-ex-005}
**Contoh 18.5 (barisan eksak pendek).** Barisan

$$
0\to A\xrightarrow{\alpha}B\xrightarrow{\beta}C\to0
$$

disebut *barisan eksak pendek*. Keeksakannya setara dengan ketiga syarat

$$
\alpha\ \text{injektif},
\qquad
\beta\ \text{surjektif},
\qquad
\ker(\beta)=\operatorname{im}(\alpha).
$$
:::

Berikut contoh yang tampak bahkan lebih trivial, tetapi tetap muncul dalam
praktik.

::: {.example #o012-rbt-l18-ex-006}
**Contoh 18.6.** Barisan

$$
0\to A\xrightarrow{\phi}B\to0
$$

eksak jika dan hanya jika $\phi$ isomorfisma.
:::

::: {.remark #o012-rbt-l18-rem-003}
**Catatan 18.3 (keeksakan himpunan bertitik).** Definisi keeksakan masih
bermakna bagi himpunan bertitik dan pemetaan bertitik. Diberikan

$$
(A,a)\xrightarrow{f}(B,b)\xrightarrow{g}(C,c),
$$

barisan ini eksak pada $(B,b)$ jika

$$
\operatorname{im}(f)=g^{-1}(c).
$$

Hal ini penting karena, untuk ruang bertitik $(X,x)$,

$$
[\mathrm{pt},X]\simeq[S^0,(X,x)]_*
$$

merupakan himpunan bertitik, dengan titik basis komponen yang memuat $x$.
:::

Diberikan bundel serat $q\colon P\to X$, kita menyebutnya *bertitik* bila
dipilih $x\in X$ dan

$$
p\in F=q^{-1}(x).
$$

::: {.source-audit #o012-rbt-l18-audit-003}
**Audit sumber 18.3.** Notes.tex baris 3606 mencetak
$p\in F=\pi^{-1}(F)$, yang salah tipe. Rumus bertipe benar adalah
$p\in F=q^{-1}(x)$.
:::

## Barisan eksak panjang bundel serat {#o012-rbt-l18-s06}

::: {.theorem #o012-rbt-l18-thm-001}
**Teorema 18.1 (barisan eksak panjang; hasil eksternal).** Untuk bundel
serat bertitik

$$
q\colon(P,p)\to(X,x),
\qquad
F=q^{-1}(x),
$$

terdapat barisan eksak

$$
\begin{aligned}
\cdots
&\to\pi_n(F,p)
\xrightarrow{i_*}\pi_n(P,p)
\xrightarrow{q_*}\pi_n(X,x)
\xrightarrow{\delta}\pi_{n-1}(F,p)
\xrightarrow{i_*}\cdots\\
&\to\pi_1(F,p)
\xrightarrow{i_*}\pi_1(P,p)
\xrightarrow{q_*}\pi_1(X,x)
\xrightarrow{\delta}[\mathrm{pt},F]
\xrightarrow{i_*}[\mathrm{pt},P]
\xrightarrow{q_*}[\mathrm{pt},X],
\end{aligned}
$$

dengan $i\colon F\hookrightarrow P$ inklusi.
:::

Teorema ini dipakai sebagai kotak hitam. Sumber merujuk Hatcher, Teorema
4.41, untuk pembuktiannya. Nama *barisan eksak panjang* membedakannya dari
barisan eksak pendek.

Peta penghubung dapat dipahami sebagai berikut. Wakili unsur
$\pi_n(X,x)$ oleh

$$
a\colon(D^n,S^{n-1},s_0)\to(X,x,x).
$$

Bundel serat mempunyai sifat pengangkatan homotopi. Pilih kontraksi

$$
C\colon D^n\times I\longrightarrow D^n,
\qquad
C(u,0)=s_0,
\quad
C(u,1)=u,
\quad
C(s_0,t)=s_0.
$$

Homotopi $a\circ C$ dimulai pada pemetaan konstan bernilai $x$. Gunakan sifat
pengangkatan homotopi relatif terhadap $\{s_0\}$, mulai dari pemetaan konstan
bernilai $p$ dan tetapkan lintasan di atas $s_0$ tetap bernilai $p$. Irisan
pada $t=1$ memberi pengangkatan $\widetilde a\colon D^n\to P$ dengan
$\widetilde a(s_0)=p$. Karena $a(S^{n-1})=\{x\}$, pembatasan
$\widetilde a|_{S^{n-1}}$ mengambil nilai di $F$ dan menentukan kelas

$$
\delta[a]=[\widetilde a|_{S^{n-1}}]\in\pi_{n-1}(F,p)
$$

untuk $n\geq2$; bagi $n=1$, kelas itu berada dalam himpunan bertitik
$[\mathrm{pt},F]$. Keberadaan pengangkatan, ketakbergantungan pilihan,
keeksakan, dan kesesuaian tanda merupakan isi teorema eksternal, bukan bukti
baru yang diklaim edisi ini.

::: {.remark #o012-rbt-l18-rem-004}
**Catatan 18.4 (ekor bertitik dan koset kanan).** Beberapa penjelasan
diperlukan pada $\pi_1(X,x)$ dan suku-suku selanjutnya yang hanya berupa
himpunan bertitik. Andaikan $P$ terhubung lintasan, tuliskan

$$
G=\pi_1(X,x),
\qquad
H=q_*\pi_1(P,p)\leq G.
$$

Dengan konvensi kronologis edisi, pengangkatan loop memberi aksi **kanan**
pada komponen serat: $[u]\cdot g$ adalah komponen titik akhir pengangkatan
loop $g$ yang dimulai di $u$. Stabilisator $[p]$ adalah $H$, sehingga
pemetaan

$$
H\backslash G\longrightarrow[\mathrm{pt},F],
\qquad
Hg\longmapsto[p]\cdot g
$$

merupakan bijeksi himpunan bertitik. Di sini $H\backslash G$ berarti koset
kanan $Hg$; tidak diperlukan normalitas $H$.

Jika $P$ tidak terhubung lintasan, orbit titik basis hanya merupakan
prabayangan komponen $[p]\in[\mathrm{pt},P]$:

$$
H\backslash G
\simeq
i_*^{-1}([p])
\subseteq[\mathrm{pt},F].
$$

Meskipun $\delta\colon G\to[\mathrm{pt},F]$ bukan homomorfisma,

$$
H=\delta^{-1}([p]).
$$
:::

::: {.source-audit #o012-rbt-l18-audit-004}
**Audit sumber 18.4.** Notes.tex baris 3619 menulis
$i_*^{-1}(p)$, padahal kodomain $i_*$ adalah $[\mathrm{pt},P]$; objek
bertipe benar ialah $[p]$. Notasi hasil bagi sumber juga tidak menentukan
sisi koset. Konvensi aksi kanan kronologis menghasilkan $H\backslash G$,
yakni koset $Hg$.
:::

## Penerapan pada ruang penutup {#o012-rbt-l18-s07}

::: {.example #o012-rbt-l18-ex-007}
**Contoh 18.7 (grup homotopi ruang penutup).** Untuk ruang penutup bertitik

$$
(Z,z)\to(X,x),
$$

serat $Z_x$ diskret. Karena itu, bagi $n>1$, barisan eksak panjang memuat

$$
\cdots\to
0=\pi_n(Z_x,z)
\to\pi_n(Z,z)
\to\pi_n(X,x)
\to\pi_{n-1}(Z_x,z)=0
\to\cdots,
$$

sehingga

$$
\pi_n(Z,z)\simeq\pi_n(X,x)
\qquad(n>1).
$$

Ujung barisan eksaknya ialah

$$
\cdots\to
0=\pi_1(Z_x,z)
\to\pi_1(Z,z)
\to\pi_1(X,x)
\to[\mathrm{pt},Z_x]=Z_x
\to[\mathrm{pt},Z]
\to[\mathrm{pt},X].
$$

Jadi $\pi_1(Z,z)\to\pi_1(X,x)$ injektif, sebagaimana telah diperoleh
sebelumnya. Jika $[\mathrm{pt},Z]=*$, yakni $Z$ terhubung lintasan, maka
pemetaan bertitik

$$
\pi_1(X,x)\longrightarrow Z_x
$$

surjektif.
:::

Contoh ini menunjukkan bahwa barisan eksak panjang grup homotopi merupakan
perumuman besar dari hubungan antara grup fundamental ruang dasar dan grup
fundamental ruang-ruang penutupnya. Meskipun demikian, ruang penutup masih
memberikan hasil baru.

::: {.example #o012-rbt-l18-ex-008}
**Contoh 18.8 (penutup universal kontraktil).** Jika $X$ **terhubung** dan
SLSC serta mempunyai ruang penutup universal kontraktil $\widetilde X$,
maka

$$
\pi_n(X)=0
\qquad(n>1).
$$

Memang,
$\pi_n(X)\cong\pi_n(\widetilde X)=0$. Hal ini berlaku bagi setiap torus
$\mathbb T^m$, dan khususnya bagi lingkaran $S^1$.
:::

::: {.source-audit #o012-rbt-l18-audit-005}
**Audit sumber 18.5.** Sumber tidak menyatakan keterhubungan $X$ pada klaim
tentang “ruang penutup universal”. Edisi menambahkannya agar istilah dan
kesimpulannya mempunyai cakupan yang tepat.
:::

## Penerapan pada bundel Hopf kompleks {#o012-rbt-l18-s08}

Sekarang terapkan barisan eksak panjang pada bundel Hopf kompleks
$S^1\to S^3\to S^2$.

::: {.example #o012-rbt-l18-ex-009}
**Contoh 18.9 (grup homotopi melalui bundel Hopf kompleks).** Sfera-sfera
terhubung, dan

$$
\pi_1(S^n)=0
\qquad(n>1).
$$

Karena $\pi_k(S^1)=0$ bagi $k>1$, diperoleh

$$
\cdots\to
0=\pi_n(S^1)
\to\pi_n(S^3)
\to\pi_n(S^2)
\to\pi_{n-1}(S^1)=0
\to\cdots,
\qquad n>2,
$$

serta

$$
\cdots\to
0=\pi_2(S^1)
\to\pi_2(S^3)
\to\pi_2(S^2)
\to\pi_1(S^1)=\mathbb Z
\to0
\to\cdots.
$$

Jadi, untuk $n>2$,

$$
\pi_n(S^3)\simeq\pi_n(S^2),
$$

dan terdapat barisan eksak pendek

$$
0\to\pi_2(S^3)\to\pi_2(S^2)\to\mathbb Z\to0.
$$

Akibatnya, $\pi_2(S^2)$ grup abelian tak hingga dan

$$
\pi_2(S^2)\Big/
\operatorname{im}\!\bigl(\pi_2(S^3)\to\pi_2(S^2)\bigr)
\simeq\mathbb Z.
$$

Jika kita menerima hasil kotak hitam

$$
\pi_2(S^3)=0,
\qquad
\pi_3(S^3)\simeq\mathbb Z,
$$

maka

$$
\pi_2(S^2)\simeq\mathbb Z,
\qquad
\pi_3(S^2)\simeq\mathbb Z.
$$
:::

::: {.remark #o012-rbt-l18-rem-005}
**Catatan 18.5.** Kenyataannya,

$$
\pi_k(S^n)=0
$$

untuk setiap $0<k<n$. Ini hasil standar, tetapi pembuktiannya melampaui
teknik yang telah dikembangkan sejauh ini dalam mata kuliah.
:::

Berikut contoh bonus yang disajikan tanpa konstruksi.

::: {.example #o012-rbt-l18-ex-010}
**Contoh 18.10 (bundel Hopf kuaternionik).** Terdapat bundel serat

$$
S^3\longrightarrow S^7\longrightarrow S^4.
$$

Barisan eksak panjang memuat

$$
\cdots\to
0=\pi_4(S^7)
\to\pi_4(S^4)
\to\pi_3(S^3)
\to\pi_3(S^7)=0
\to\cdots.
$$

Karena $\pi_3(S^3)\simeq\mathbb Z$, diperoleh

$$
\pi_4(S^4)\simeq\mathbb Z.
$$
:::

::: {.remark #o012-rbt-l18-rem-006}
**Catatan 18.6.** Hasil klasik yang lebih umum menyatakan

$$
\pi_n(S^n)\simeq\mathbb Z
$$

untuk setiap $n$. Sekali lagi, pembuktiannya melampaui cakupan mata kuliah
sejauh ini.
:::

Mengetahui grup homotopi sfera saja sudah sulit. Inilah salah satu alasan
Serre dianugerahi Medali Fields: ia mengembangkan perangkat yang, antara
lain, dapat dipakai untuk menunjukkan bahwa seluruh grup homotopi sfera
berhingga kecuali

$$
\pi_n(S^n)\simeq\mathbb Z
$$

dan

$$
\pi_{4n-1}(S^{2n})\simeq\mathbb Z\oplus A,
$$

dengan $A$ grup abelian berhingga. Fenomena yang ganjil dan tidak terduga
memang terjadi. Sebagai contoh yang dipilih secara acak,

$$
\pi_{25}(S^6)
\simeq
\mathbb Z/(1056\mathbb Z)\oplus\mathbb Z/(8\mathbb Z).
$$

::: {.source-audit #o012-rbt-l18-audit-006}
**Audit sumber 18.6.** Edisi memperbaiki salah tata bahasa “These is” pada
baris 3660 dan salah eja “calulate” pada baris 3676 tanpa mengubah isi
matematis.
:::

# Pendamping penguasaan: pemeriksaan, petunjuk, dan solusi lengkap {.unnumbered #o012-rbt-l18-mastery}

Enam pemeriksaan berikut merupakan materi asli edisi. Semuanya terbatas pada
isi Unit 18: transpor sepanjang lintasan, hasil kali, perubahan titik basis,
invariansi homotopi, trivialisasi bundel Hopf kompleks, keeksakan lima suku,
serta perhitungan melalui ruang penutup dan bundel-bundel Hopf. Tidak ada
pemeriksaan yang memakai materi Kuliah 19.

::: {.exercise #o012-rbt-l18-mcheck-001 data-origin="edition-original"}
**Pemeriksaan penguasaan 18.1 (transpor sepanjang lintasan).** Tetapkan
$n\geq1$. Misalkan $\gamma\colon x\rightsquigarrow y$ dan
$\eta\colon y\rightsquigarrow z$ lintasan di $X$.

1. Jelaskan mengapa rumus kerah dengan norma maksimum mendefinisikan
   $T_\gamma\colon\pi_n(X,x)\to\pi_n(X,y)$.
2. Buktikan
   $T_{\gamma\#\eta}=T_\eta T_\gamma$ dan
   $T_{c_x}=\operatorname{id}$.
3. Buktikan bahwa $T_\gamma$ homomorfisma dan isomorfisma.
4. Jika $x$ dan $y$ terletak dalam satu komponen lintasan yang terhubung
   sederhana, buktikan bahwa isomorfisma transpor tidak bergantung pada
   lintasan yang dipilih dari $x$ ke $y$.
:::

::: {.hint #o012-rbt-l18-hint-001 data-origin="edition-original"}
**Petunjuk.** Periksa nilai pada dua batas kulit kubus. Untuk perkalian,
bandingkan dua kotak pusat yang masing-masing berkerah dengan dua kotak di
dalam satu kerah bersama. Untuk invers, gunakan lintasan balik. Untuk
ketakbergantungan kanonik, bandingkan dua lintasan dengan titik ujung tetap.
:::

::: {.solution #o012-rbt-l18-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 18.1.** Pada
$\lVert\mathbf u\rVert_\infty=\frac14$, cabang dalam bernilai $x$ karena
$i(\mathbf u)\in\partial I^n$, sedangkan cabang luar bernilai
$\gamma(0)=x$. Jadi lema penempelan memberi pemetaan kontinu. Pada
$\partial I^n$, norma maksimum bernilai $\frac12$, sehingga nilainya
$\gamma(1)=y$. Dengan demikian rumus kerah menghasilkan peta pasangan

$$
(I^n,\partial I^n)\longrightarrow(X,y).
$$

Homotopi relatif antara wakil $\alpha$ dan homotopi yang mempertahankan titik
ujung antara wakil $\gamma$ dapat dimasukkan sebagai parameter tambahan ke
rumus yang sama. Jadi $T_\gamma$ terdefinisi pada kelas homotopi.

Konstruksi bagi $\gamma\#\eta$ mempunyai kerah yang mula-mula menelusuri
$\gamma$ lalu $\eta$. Konstruksi $T_\eta T_\gamma$ mempunyai dua kerah
bersarang. Homeomorfisma radial sepotong-sepotong yang melebur dua kerah
menjadi satu memberi homotopi relatif terhadap batas, maka

$$
T_{\gamma\#\eta}=T_\eta\circ T_\gamma.
$$

Kerah berlabel lintasan konstan dapat disusutkan ke batas kubus pusat, jadi
$T_{c_x}=\operatorname{id}$.

Untuk dua wakil $\alpha,\beta$, tampilkan produk dengan dua kotak dukungan
yang saling lepas. Pada $T_\gamma([\alpha][\beta])$, keduanya berada dalam
satu kerah $\gamma$. Pada
$T_\gamma[\alpha]\,T_\gamma[\beta]$, masing-masing mempunyai salinan kerah.
Geser kedua kerah dalam hingga berimpit dan perluas kerah luarnya. Semua
jahitan tetap bernilai $x$ atau $y$, sehingga reparameterisasi ini memberi
homotopi relatif terhadap batas. Oleh karena itu

$$
T_\gamma([\alpha][\beta])
=T_\gamma[\alpha]\,T_\gamma[\beta].
$$

Akhirnya,

$$
T_{\bar\gamma}T_\gamma
=T_{\gamma\#\bar\gamma}
=T_{c_x}
=\operatorname{id},
$$

dan serupa
$T_\gamma T_{\bar\gamma}=\operatorname{id}$. Maka
$T_{\bar\gamma}=T_\gamma^{-1}$ dan $T_\gamma$ isomorfisma grup.

Terakhir, andaikan $\gamma_0$ dan $\gamma_1$ menghubungkan $x$ ke $y$ di
dalam komponen lintasan yang terhubung sederhana. Loop
$\gamma_0\#\bar\gamma_1$ nulhomotopik. Dengan menempelkan nulhomotopi itu
pada salah satu sisi, diperoleh homotopi yang mempertahankan titik ujung
dari $\gamma_0$ ke $\gamma_1$. Ketakbergantungan wakil lintasan yang telah
dibuktikan di atas memberi

$$
T_{\gamma_0}=T_{\gamma_1}.
$$

Jadi isomorfisma transpor pada komponen tersebut kanonik.
:::

::: {.exercise #o012-rbt-l18-mcheck-002 data-origin="edition-original"}
**Pemeriksaan penguasaan 18.2 (hasil kali).** Tetapkan $n\geq1$. Bangun
langsung isomorfisma

$$
\pi_n(X\times Y,(x,y))
\cong
\pi_n(X,x)\times\pi_n(Y,y).
$$

Buktikan bahwa ia terdefinisi baik, mempertahankan operasi grup, mempunyai
invers, dan natural terhadap pasangan pemetaan bertitik.
:::

::: {.hint #o012-rbt-l18-hint-002 data-origin="edition-original"}
**Petunjuk.** Pemetaan atau homotopi ke hasil kali ditentukan tepat oleh dua
komponen proyeksinya. Tulis kedua arah isomorfisma sebelum memeriksa
naturalitas.
:::

::: {.solution #o012-rbt-l18-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 18.2.** Definisikan

$$
\Phi[\alpha]
=
\bigl[
\operatorname{pr}_X\alpha
\bigr]
\times
\bigl[
\operatorname{pr}_Y\alpha
\bigr]
:=
\bigl(
[\operatorname{pr}_X\alpha],
[\operatorname{pr}_Y\alpha]
\bigr).
$$

Jika $\alpha\simeq\alpha'$ secara bertitik, komposisi homotopi itu dengan
kedua proyeksi memberi homotopi komponen, sehingga $\Phi$ terdefinisi baik.
Sebaliknya, tetapkan

$$
\Psi([a],[b])=[(a,b)].
$$

Jika $a\simeq a'$ dan $b\simeq b'$, pasangan kedua homotopi adalah homotopi
bertitik $(a,b)\simeq(a',b')$, jadi $\Psi$ juga terdefinisi baik. Persamaan

$$
\Phi\Psi([a],[b])=([a],[b]),
\qquad
\Psi\Phi[\alpha]=[\alpha]
$$

mengikuti dari identitas
$(\operatorname{pr}_X\alpha,\operatorname{pr}_Y\alpha)=\alpha$.

Konkatenasi pada kubus dilakukan pada satu koordinat domain. Proyeksi
mempertahankan rumus sepotong-sepotong itu, sehingga

$$
\Phi([\alpha][\beta])
=
\Phi[\alpha]\,\Phi[\beta]
$$

dengan perkalian komponen demi komponen pada ruas kanan. Jadi $\Phi$
isomorfisma grup.

Untuk pemetaan bertitik $f\colon X\to X'$ dan $g\colon Y\to Y'$, kedua
komposit dalam persegi naturalitas mengirim $[\alpha]$ ke

$$
\bigl(
[f\operatorname{pr}_X\alpha],
[g\operatorname{pr}_Y\alpha]
\bigr).
$$

Karena kedua hasilnya sama pada setiap kelas, isomorfisma tersebut natural.
:::

::: {.exercise #o012-rbt-l18-mcheck-003 data-origin="edition-original"}
**Pemeriksaan penguasaan 18.3 (titik basis yang bergerak dan ekuivalensi
homotopi).** Tetapkan $n\geq1$. Misalkan $H\colon f\simeq g$ dan
$h(t)=H(t,x)$. Buktikan

$$
T_h\circ f_*=g_*.
$$

Kemudian gunakan pernyataan ini untuk membuktikan bahwa ekuivalensi homotopi
$f\colon X\to Y$ menginduksi isomorfisma pada $\pi_n$, tanpa menganggap
bahwa invers homotopinya mempertahankan titik basis.
:::

::: {.hint #o012-rbt-l18-hint-003 data-origin="edition-original"}
**Petunjuk.** Homotopi $H(t,\alpha(s))$ menggerakkan nilai titik basis
sepanjang $h$. Untuk ekuivalensi homotopi, satu homotopi memberikan invers
kiri bagi $f_*$ setelah transpor; homotopi lainnya menunjukkan bahwa suatu
komposit yang memfaktorkan melalui $f_*$ surjektif.
:::

::: {.solution #o012-rbt-l18-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 18.3.** Ambil wakil bertitik
$\alpha\colon(S^n,*)\to(X,x)$. Homotopi

$$
L(t,s)=H(t,\alpha(s))
$$

berjalan dari $f\alpha$ ke $g\alpha$, sedangkan nilai titik basisnya
$L(t,*)=h(t)$. Sisipkan kerah di sekitar $*$ dan gunakan potongan
$h|_{[0,t]}$ pada kerah itu. Di luar kerah gunakan $L(t,-)$. Kedua rumus
bertemu pada $h(t)$, sehingga lema penempelan memberi homotopi bertitik
antara $(f\alpha)^h$ dan $g\alpha$. Maka

$$
T_h(f_*[\alpha])=g_*[\alpha],
$$

dan karena $[\alpha]$ sebarang, $T_hf_*=g_*$.

Sekarang tuliskan
$f_*^{\,u}\colon\pi_n(X,u)\to\pi_n(Y,f(u))$ agar titik basis terlihat.
Pilih invers homotopi $r\colon Y\to X$ bagi $f$, dengan
$H\colon rf\simeq\operatorname{id}_X$ dan
$K\colon fr\simeq\operatorname{id}_Y$. Lintasan
$h(t)=H(t,x)$ memberikan

$$
T_h r_*^{\,f(x)}f_*^{\,x}
=\operatorname{id}_{\pi_n(X,x)}.
$$

Jadi $f_*^{\,x}$ mempunyai invers kiri dan injektif. Lintasan
$k(t)=K(t,f(x))$ memberikan

$$
T_k f_*^{\,r f(x)}r_*^{\,f(x)}
=\operatorname{id}_{\pi_n(Y,f(x))}.
$$

Naturalisasi transpor terhadap $f$ memberi

$$
f_*^{\,x}T_h
=T_{f\circ h}f_*^{\,r f(x)}.
$$

Oleh karena itu

$$
\begin{aligned}
f_*^{\,x}T_h r_*^{\,f(x)}
&=T_{f\circ h}f_*^{\,r f(x)}r_*^{\,f(x)}\\
&=T_{f\circ h}T_k^{-1}.
\end{aligned}
$$

Ruas kanan isomorfisma, jadi ruas kiri surjektif. Karena ruas kiri
memfaktorkan melalui $f_*^{\,x}$, pemetaan $f_*^{\,x}$ surjektif.
Homomorfisma yang sekaligus injektif dan surjektif adalah isomorfisma.
Tidak pernah diasumsikan bahwa $r(f(x))=x$; transpor titik basis menutup
tepat celah tersebut.
:::

::: {.exercise #o012-rbt-l18-mcheck-004 data-origin="edition-original"}
**Pemeriksaan penguasaan 18.4 (trivialisasi lokal bundel Hopf kompleks).** Untuk

$$
q(z,w)=[z:w]\colon S^3\to\mathbb{CP}^1,
$$

periksa secara lengkap trivialisasi pada peta koordinat $U_z$ dan $U_w$ yang diberikan
dalam Contoh 18.4. Tunjukkan bahwa rumus invers mengambil nilai di $S^3$,
saling invers dengan $\Phi_z,\Phi_w$, kontinu, dan berada di atas daerah peta koordinat
yang benar. Tentukan fungsi transisi pada $U_z\cap U_w$.
:::

::: {.hint #o012-rbt-l18-hint-004 data-origin="edition-original"}
**Petunjuk.** Pada $U_z$, tulis $[z:w]=[1:u]$ dengan $u=w/z$ dan pisahkan
fase $z/|z|$. Pada irisan, jika $v=1/u$, bandingkan parameter fase yang
diberikan oleh $z$ dan oleh $w$.
:::

::: {.solution #o012-rbt-l18-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 18.4.** Untuk $([1:u],\lambda)\in U_z\times U(1)$,
tetapkan

$$
(z,w)
=
\left(
\frac{\lambda}{\sqrt{1+|u|^2}},
\frac{\lambda u}{\sqrt{1+|u|^2}}
\right).
$$

Karena $|\lambda|=1$,

$$
|z|^2+|w|^2
=
\frac{1+|u|^2}{1+|u|^2}
=1,
$$

jadi $(z,w)\in S^3$. Selain itu $z\neq0$,
$[z:w]=[1:u]$, dan $z/|z|=\lambda$. Jadi
$\Phi_z\Phi_z^{-1}$ identitas. Sebaliknya, bila $(z,w)\in q^{-1}(U_z)$,
ambil $u=w/z$ dan $\lambda=z/|z|$. Dari
$1=|z|^2(1+|u|^2)$ diperoleh
$|z|=1/\sqrt{1+|u|^2}$, sehingga rumus invers mengembalikan $(z,w)$.

Argumen yang sama pada $U_w$, dengan $v=z/w$, memberikan

$$
(z,w)
=
\left(
\frac{\lambda v}{\sqrt{1+|v|^2}},
\frac{\lambda}{\sqrt{1+|v|^2}}
\right),
\qquad
\lambda=\frac w{|w|}.
$$

Semua operasi dalam rumus tersebut kontinu pada peta koordinat masing-masing.
Koordinat projektif pertama tidak berubah, jadi kedua homeomorfisma berada
di atas $\mathbb{CP}^1$.

Pada irisan, $u\neq0$ dan $v=1/u$. Jika $\lambda_z=z/|z|$ dan
$\lambda_w=w/|w|$, maka $w=uz$ memberi

$$
\lambda_w
=
\frac{u}{|u|}\lambda_z.
$$

Jadi fungsi transisinya, dalam arah dari trivialisasi $z$ ke trivialisasi
$w$, adalah

$$
([1:u],\lambda_z)
\longmapsto
\left([1:u],\frac{u}{|u|}\lambda_z\right).
$$

Faktor $u/|u|\in U(1)$ juga kontinu pada $u\neq0$. Dengan demikian kedua
peta koordinat membuktikan trivialisasi lokal bundel Hopf kompleks.
:::

::: {.exercise #o012-rbt-l18-mcheck-005 data-origin="edition-original"}
**Pemeriksaan penguasaan 18.5 (inferensi dari lima suku bundel).** Untuk
$k\geq2$, pandang lima suku berturutan dari barisan eksak panjang:

$$
\pi_k(F)\xrightarrow{i_*}\pi_k(P)
\xrightarrow{q_*}\pi_k(X)
\xrightarrow{\delta}\pi_{k-1}(F)
\xrightarrow{i_*}\pi_{k-1}(P).
$$

Buktikan:

1. jika $\pi_k(F)=0$, maka $q_*$ injektif;
2. jika $\pi_{k-1}(F)=0$, maka $q_*$ surjektif;
3. jika kedua grup serat itu nol, maka $q_*$ isomorfisma;
4. jika $P$ kontraktil, maka
   $\delta\colon\pi_k(X)\to\pi_{k-1}(F)$ isomorfisma.
:::

::: {.hint #o012-rbt-l18-hint-005 data-origin="edition-original"}
**Petunjuk.** Gunakan
$\ker(q_*)=\operatorname{im}(i_*)$ dan
$\operatorname{im}(q_*)=\ker(\delta)$. Untuk bagian terakhir, masukkan
$\pi_k(P)=0=\pi_{k-1}(P)$ pada kedua sisi $\delta$.
:::

::: {.solution #o012-rbt-l18-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 18.5.** Jika $\pi_k(F)=0$, citra pemetaan
$i_*\colon\pi_k(F)\to\pi_k(P)$ adalah subgrup nol. Keeksakan pada
$\pi_k(P)$ memberi

$$
\ker(q_*)
=\operatorname{im}(i_*)
=0.
$$

Jadi $q_*$ injektif.

Jika $\pi_{k-1}(F)=0$, peta penghubung $\delta$ mempunyai target grup nol,
sehingga kernelnya seluruh $\pi_k(X)$. Keeksakan pada $\pi_k(X)$ memberi

$$
\operatorname{im}(q_*)
=\ker(\delta)
=\pi_k(X).
$$

Jadi $q_*$ surjektif. Bila kedua grup serat tersebut nol, $q_*$ sekaligus
injektif dan surjektif, maka isomorfisma.

Terakhir, bila $P$ kontraktil, fragmen di sekitar $\delta$ menjadi

$$
0=\pi_k(P)
\longrightarrow\pi_k(X)
\xrightarrow{\delta}\pi_{k-1}(F)
\longrightarrow\pi_{k-1}(P)=0.
$$

Keeksakan pada $\pi_k(X)$ membuat kernel $\delta$ nol, jadi $\delta$
injektif. Keeksakan pada $\pi_{k-1}(F)$ membuat citra $\delta$ seluruh
$\pi_{k-1}(F)$, jadi $\delta$ surjektif. Karena $k\geq2$, suku-suku ini
grup dan $\delta$ homomorfisma; akibatnya $\delta$ isomorfisma.
:::

::: {.exercise #o012-rbt-l18-mcheck-006 data-origin="edition-original"}
**Pemeriksaan penguasaan 18.6 (ruang projektif dan bundel-bundel Hopf).**

1. Untuk penutup antipodal
   $S^m\to\mathbb{RP}^m$ dengan $m\geq2$, tentukan hubungan antara
   $\pi_n(S^m)$ dan $\pi_n(\mathbb{RP}^m)$ bagi $n>1$. Dengan hasil standar
   $\pi_k(S^m)=0$ untuk $0<k<m$ dan
   $\pi_m(S^m)\cong\mathbb Z$, simpulkan nilai
   $\pi_n(\mathbb{RP}^m)$ untuk $1<n<m$ serta
   $\pi_m(\mathbb{RP}^m)$. Gunakan pula ekor bertitik untuk menghitung
   $\pi_1(\mathbb{RP}^m)$.
2. Gunakan bundel Hopf kompleks dan hasil
   $\pi_2(S^3)=0$, $\pi_3(S^3)\cong\mathbb Z$ untuk menghitung
   $\pi_2(S^2)$ dan $\pi_3(S^2)$. Nyatakan pula hubungan bagi semua $n>2$.
3. Gunakan bundel Hopf kuaternionik
   $S^3\to S^7\to S^4$ untuk menghitung $\pi_4(S^4)$ dari
   $\pi_4(S^7)=0$, $\pi_3(S^7)=0$, dan
   $\pi_3(S^3)\cong\mathbb Z$.
:::

::: {.hint #o012-rbt-l18-hint-006 data-origin="edition-original"}
**Petunjuk.** Serat penutup antipodal mempunyai dua titik. Grup homotopi
lebih tinggi ruang total dan dasar isomorfik. Untuk grup fundamental, gunakan
deskripsi orbit pada Catatan 18.4 dengan
$H=q_*\pi_1(S^m)=1$, bukan argumen kernel bagi pemetaan yang bukan
homomorfisma. Untuk bundel Hopf kompleks maupun kuaternionik, tulis fragmen
eksak yang mengapit grup dasar yang hendak dihitung dan nolkan grup sfera
dalam dimensi di bawah dimensinya.
:::

::: {.solution #o012-rbt-l18-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 18.6.** Karena
$S^m\to\mathbb{RP}^m$ ruang penutup, Contoh 18.7 memberi

$$
\pi_n(S^m)\xrightarrow{\simeq}\pi_n(\mathbb{RP}^m)
\qquad(n>1).
$$

Maka, untuk $1<n<m$,

$$
\pi_n(\mathbb{RP}^m)=0,
$$

sedangkan

$$
\pi_m(\mathbb{RP}^m)\cong\mathbb Z.
$$

Khususnya,
$\pi_2(\mathbb{RP}^2)\cong\mathbb Z$.

Untuk menghitung grup fundamental, serat penutup antipodal ialah
$\{+,-\}$ dan $S^m$ terhubung sederhana bagi $m\geq2$. Bagian bertitik
barisan eksak adalah

$$
0=\pi_1(S^m)
\longrightarrow\pi_1(\mathbb{RP}^m)
\xrightarrow{\delta}\{+,-\}
\longrightarrow[\mathrm{pt},S^m]=*.
$$

Pemetaan $\delta$ bukan homomorfisma, jadi prabayangan titik basis saja tidak
membuktikan bahwa ia injektif. Gunakan deskripsi orbit Catatan 18.4. Dengan

$$
G=\pi_1(\mathbb{RP}^m),
\qquad
H=q_*\pi_1(S^m)=1,
$$

terdapat bijeksi himpunan bertitik

$$
H\backslash G\xrightarrow{\simeq}\{+,-\}.
$$

Karena $H=1$, himpunan $H\backslash G$ dapat diidentifikasi dengan himpunan
yang mendasari $G$. Jadi $G$ mempunyai tepat dua unsur. Satu-satunya grup
berorde dua adalah grup siklik:

$$
\pi_1(\mathbb{RP}^m)\cong\mathbb Z/2\mathbb Z.
$$

Dengan demikian nilai $\pi_2(\mathbb{RP}^2)\cong\mathbb Z$ tidak
bertentangan dengan grup fundamentalnya; isomorfisma grup homotopi melalui
ruang penutup berlaku dalam derajat $n>1$.

Untuk bundel Hopf kompleks, bagian relevan barisan eksak adalah

$$
0=\pi_2(S^1)
\longrightarrow\pi_2(S^3)
\longrightarrow\pi_2(S^2)
\longrightarrow\pi_1(S^1)\cong\mathbb Z
\longrightarrow\pi_1(S^3)=0.
$$

Dengan $\pi_2(S^3)=0$, peta
$\pi_2(S^2)\to\mathbb Z$ sekaligus injektif dan surjektif, sehingga

$$
\pi_2(S^2)\cong\mathbb Z.
$$

Bagi $n>2$, kedua grup serat di kiri dan kanan lenyap:

$$
\pi_n(S^1)=0=\pi_{n-1}(S^1).
$$

Karena itu

$$
\pi_n(S^3)\xrightarrow{\simeq}\pi_n(S^2)
\qquad(n>2).
$$

Dengan $n=3$ dan $\pi_3(S^3)\cong\mathbb Z$, diperoleh

$$
\pi_3(S^2)\cong\mathbb Z.
$$

Untuk bundel Hopf kuaternionik
$S^3\to S^7\to S^4$, fragmen yang relevan adalah

$$
0=\pi_4(S^7)
\longrightarrow\pi_4(S^4)
\xrightarrow{\delta}\pi_3(S^3)\cong\mathbb Z
\longrightarrow\pi_3(S^7)=0.
$$

Keeksakan membuat $\delta$ injektif karena suku di kirinya nol, dan
surjektif karena suku di kanannya nol. Jadi

$$
\pi_4(S^4)\cong\mathbb Z.
$$
:::
