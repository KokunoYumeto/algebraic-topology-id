---
title: "Topologi Aljabar"
subtitle: "Unit 24: Korantai Relatif, Lema Ular, dan Barisan Eksak Panjang"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l24-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 5113--5369 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L5113-L5369)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang aktif itu terdiri atas 257 baris fisik. Dengan normalisasi LF dan
terminator baris kosong penutup dipertahankan, ukurannya 12.837 byte dan
SHA-256-nya adalah
`b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea`.
Baris 5113--5121 melanjutkan dan menutup contoh yang dimulai pada baris 5076
dan diterjemahkan pertama kali dalam
[Contoh 23.2](#o012-rbt-l23-exa-002). Baris 5370, yang memulai Kuliah 25,
tidak termasuk. Materi sumber dan adaptasi Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Rentang sumber memuat satu penanda kuliah, satu penutup `example` tanpa
pembuka baru, satu definisi, satu teorema, tiga lema, satu catatan, tiga
lingkungan bukti, satu enumerasi enam butir, tujuh catatan pinggir, dua
diagram Xy-pic, satu gambar TikZ, empat label, empat rujukan silang, dan
delapan tampilan matematika. Tidak ada latihan formal sumber, sitasi, gambar
eksternal, `input`, atau `include`.

Edisi memindahkan ketujuh catatan pinggir ke urutan bacaan utama dan mengganti
dua diagram Xy-pic serta gambar TikZ dengan data panah semantik terpusat.
Edisi juga melengkapi bukti bahwa kernel dan kompleks korantai relatif
benar-benar membentuk kompleks, seluruh enam kewajiban pembuktian Lema Ular,
eksaknya diagram persiapan, identifikasi kernel dan kokernel dengan
kohomologi, penyambungan barisan enam-suku, dan kealamian barisan eksak
panjang. Kekeliruan deterministik yang diperbaiki dicatat tepat di tempatnya;
tidak ada bahan matematis luar yang dimasukkan sebagai materi sumber.

Enam pemeriksaan penguasaan, enam petunjuk, semua bukti penutup edisi, dan
enam solusi lengkap merupakan materi asli edisi dan tersedia di bawah CC BY
4.0. Edisi ini bersifat independen; edisi ini tidak disponsori, didukung, disahkan,
ataupun diberi status resmi oleh David Michael Roberts atau institusinya.
Produksi edisi ini dibantu oleh **OpenAI Codex gpt-5.6-sol, Ultra**.
Pernyataan ini menambah transparansi proses dan tidak mengurangi
kredit penulis sumber ataupun kredit kontributor manusia.

# Kuliah 24 {#o012-rbt-l24}

## Kelanjutan contoh pasangan dan hasil bagi {#o012-rbt-l24-s01}

::: {.example #o012-rbt-l24-exa-001 data-source-status="resumes-and-closes-lecture-023-example" data-continuation-of="o012-rbt-l23-exa-002"}
**Kelanjutan Contoh 23.2 (hubungan timbal balik).** Bagian ini melanjutkan
objek sumber yang diterjemahkan sebagai
[Contoh 23.2](#o012-rbt-l23-exa-002); objek itu menunjuk ke baris 5113 sebagai
kursor berikutnya, sedangkan objek ini mencatat induknya melalui atribut
`data-continuation-of` dan menutup lingkungan sumber pada baris 5121.

Jadi, untuk pasangan $(X_\bullet,A_\bullet)$ dengan fungsi inklusi
$i\colon A_\bullet\hookrightarrow X_\bullet$, kita dapat mengambil pemetaan
restriksi yang surjektif

$$
C^\bullet(X_\bullet;R)
\xrightarrow{\ i^*\ }
C^\bullet(A_\bullet;R)
\longrightarrow0.
$$

Kernel $\ker(i^*)$ berperan sebagai modul fungsi virtual pada
$X_\bullet/A_\bullet$ tanpa mengharuskan kita mendefinisikan hasil bagi itu
sebagai himpunan-$\Delta$. Selain itu, sebagaimana dalam contoh sebelumnya,
kita memperoleh barisan eksak pendek kompleks modul-$R$.
:::

::: {.proof #o012-rbt-l24-proof-001 data-origin="edition-proof-closure"}
**Penutupan bukti: restriksi, kernel, dan eksaknya barisan.** Pada derajat
$n$, komponen restriksi adalah

$$
i_n^*\colon R^{X_n}\longrightarrow R^{A_n},
\qquad
i_n^*(g)=g|_{A_n}.
$$

Karena $A_\bullet$ merupakan sub-himpunan-$\Delta$, setiap *face map* pada
$A_\bullet$ adalah pembatasan *face map* pada $X_\bullet$. Oleh sebab itu

$$
\delta_A^n i_n^*=i_{n+1}^*\delta_X^n,
$$

sehingga $(i_n^*)_n$ adalah pemetaan korantai. Pemetaan $i_n^*$ surjektif:
untuk $h\colon A_n\to R$, definisikan $\widehat h\colon X_n\to R$ dengan
$\widehat h=h$ pada $A_n$ dan $\widehat h=0$ pada $X_n\setminus A_n$.
Maka $i_n^*(\widehat h)=h$.

Jika $g\in\ker i_n^*$, persamaan pemetaan korantai memberi

$$
i_{n+1}^*(\delta_X^n g)=\delta_A^n(i_n^*g)=0.
$$

Jadi diferensial $\delta_X^n$ membatasi diri ke pemetaan
$\ker i_n^*\to\ker i_{n+1}^*$, dan diferensial terbatas itu tetap berkuadrat
nol. Dengan inklusi kernel pada ruas kiri, diperoleh barisan eksak pendek
kompleks

$$
0\longrightarrow\ker(i^*)
\longrightarrow C^\bullet(X_\bullet;R)
\xrightarrow{\ i^*\ }C^\bullet(A_\bullet;R)
\longrightarrow0.
$$

Perluasan dengan nol di atas hanya membuktikan surjektivitas **pada setiap
derajat**; pada umumnya ia bukan pemetaan korantai dan bukan pemisahan
kompleks. Misalnya, ambil $X_\bullet=\Delta[1]$, ambil
$A_\bullet$ yang hanya memuat simpul $0$, dan andaikan $1_R\ne0$. Fungsi
$1$ pada $A_0$ meluas dengan nol menjadi fungsi bernilai $1$ di simpul $0$
dan $0$ di simpul $1$. Kobatasnya pada sisi $01$ adalah $\pm1_R$, sedangkan
perluasan dengan nol dari kobatas pada $A_\bullet$ adalah nol karena
$A_1=\varnothing$. Jadi pemisahan derajat demi derajat itu tidak komutatif
dengan diferensial.
:::

::: {.source-audit #o012-rbt-l24-audit-001}
**Audit sumber 24.1.** Notes.tex baris 5113--5120 menyatakan surjektivitas
dan eksaknya barisan melalui analogi. Edisi memeriksa pemetaan korantai,
surjektivitas derajat demi derajat, kestabilan kernel, dan eksaknya barisan;
ia juga membedakan perluasan dengan nol dari pemisahan pemetaan korantai.
:::

## Kernel morfisma kompleks dan korantai relatif {#o012-rbt-l24-s02}

Sebelum melanjutkan, perlu dicatat bahwa konstruksi kernel terakhir memang
terdefinisi dengan baik.

::: {.lemma #o012-rbt-l24-lem-001}
**Lema 24.1 (kernel derajat demi derajat adalah sebuah kompleks).** Diberikan
morfisma kompleks

$$
\varphi\colon A_\bullet\longrightarrow B_\bullet,
$$

kernel derajat demi derajat $\ker(\varphi_n)\subseteq A_n$ menyusun sebuah
kompleks $\ker(\varphi)$. Diferensialnya adalah pembatasan diferensial
$A_n\to A_{n+1}$ ke kernel yang sesuai.
:::

::: {.proof #o012-rbt-l24-proof-002 data-origin="edition-proof-closure"}
**Bukti.** Tuliskan diferensial kedua kompleks sebagai
$d_A^n\colon A_n\to A_{n+1}$ dan $d_B^n\colon B_n\to B_{n+1}$. Untuk
$a\in\ker\varphi_n$, sifat morfisma kompleks memberi

$$
\varphi_{n+1}(d_A^n a)=d_B^n(\varphi_n a)=d_B^n(0)=0.
$$

Karena itu $d_A^n a\in\ker\varphi_{n+1}$, sehingga pemetaan terbatas

$$
d_{\ker\varphi}^n
:=d_A^n|_{\ker\varphi_n}\colon
\ker\varphi_n\longrightarrow\ker\varphi_{n+1}
$$

terdefinisi. Komposisinya berkuadrat nol karena

$$
d_{\ker\varphi}^{n+1}d_{\ker\varphi}^n
=\left.d_A^{n+1}d_A^n\right|_{\ker\varphi_n}=0.
$$

Jadi modul-modul kernel itu, bersama diferensial terbatas, benar-benar
membentuk kompleks.
:::

::: {.source-audit #o012-rbt-l24-audit-002}
**Audit sumber 24.2.** Lema pada Notes.tex baris 5125--5129 tidak memiliki
bukti formal. Edisi mengetik diferensial terbatas, membuktikan bahwa ia
mendarat di kernel berikutnya, dan memeriksa bahwa kuadratnya nol.
:::

Dengan lema ini kita dapat mendefinisikan kompleks yang terkait dengan suatu
pasangan.

::: {.definition #o012-rbt-l24-def-001}
**Definisi 24.1 (kompleks korantai simpleksial relatif).** Untuk pasangan
$(X_\bullet,A_\bullet)$, kompleks

$$
C^\bullet(X_\bullet,A_\bullet;R):=\ker(i^*)
$$

disebut **kompleks korantai simpleksial relatif** pasangan itu.
:::

## Prinsip aljabar homologis {#o012-rbt-l24-s03}

Kedua contoh motivasi tersebut merupakan kasus khusus dari satu prinsip
umum. Misalkan diberikan barisan eksak pendek kompleks modul-$R$

$$
0\longrightarrow A_\bullet\longrightarrow B_\bullet
\longrightarrow C_\bullet\longrightarrow0.
$$

Kita mungkin hendak menghitung $H^n(A_\bullet)$ sementara hanya mengetahui
$H^n(B_\bullet)$ dan $H^n(C_\bullet)$; atau mengetahui kohomologi $A_\bullet$
dan $C_\bullet$ tetapi hendak menghitung kohomologi $B_\bullet$. Dalam situasi
berhingga ini mungkin hanya persoalan efisiensi komputasi. Dalam keadaan
umum, bagaimanapun, kita berhadapan dengan modul-$R$ yang dibangkitkan secara
tak hingga, sehingga teknik aljabar linear sederhana mulai gagal. Kita akan
membuktikan hasil umum dari **aljabar homologis** yang menghubungkan semua
grup kohomologi tersebut.

::: {.source-margin #o012-rbt-l24-margin-001}
> **Catatan pinggir sumber.** Aljabar homologis adalah cabang aljabar yang
> mempelajari interaksi antara barisan, pemetaan barisan, diagram komutatif
> objek aljabar yang mempunyai sifat eksak tertentu, serta cara menghitung
> berbagai objek, termasuk grup (ko)homologi.
:::

::: {.remark #o012-rbt-l24-rem-001}
**Catatan 24.1 (alat komputasi utama).** Jika hanya satu hasil dari bagian
kuliah ini yang diingat, hasil berikut mungkin yang paling berguna, sebab ia
dapat diterapkan dalam banyak konteks untuk menghasilkan barisan eksak
panjang. Sebaliknya, sebuah barisan eksak panjang standar yang sudah dikenal
di suatu bidang sering kali muncul dari teorema ini; memahami bukti
abstraknya karena itu penting. Bersama barisan eksak panjang grup homotopi
dari berkas serat, hasil ini merupakan salah satu alat komputasi utama sampai
teori barisan spektral digunakan. Barisan spektral sangat kuat, tetapi jauh
kurang intuitif.

::: {.source-margin #o012-rbt-l24-margin-002}
> **Catatan pinggir sumber.** Dalam teori-$K$, barisan eksak panjang yang
> dimaksud dapat melipat kembali ke dirinya sendiri.
:::
:::

::: {.theorem #o012-rbt-l24-thm-001 data-source-label="thm:alg_Mayer-Vietoris"}
**Teorema 24.1 (Mayer--Vietoris aljabar; alias sumber
`thm:alg_Mayer-Vietoris`).** Diberikan barisan eksak pendek kompleks
modul-$R$

$$
0\longrightarrow A_\bullet
\xrightarrow{\ i\ }B_\bullet
\xrightarrow{\ \pi\ }C_\bullet
\longrightarrow0,
$$

terdapat barisan eksak panjang modul-$R$

$$
\cdots\xrightarrow{\ \delta^{k-1}\ }H^k(A_\bullet)
\xrightarrow{\ H^k(i)\ }H^k(B_\bullet)
\xrightarrow{\ H^k(\pi)\ }H^k(C_\bullet)
\xrightarrow{\ \delta^k\ }H^{k+1}(A_\bullet)
\xrightarrow{\ H^{k+1}(i)\ }H^{k+1}(B_\bullet)
\longrightarrow\cdots.
$$

::: {.source-margin #o012-rbt-l24-margin-003}
> **Catatan pinggir sumber.** Sumber menyebut hasil ini teorema
> Mayer--Vietoris aljabar; nama lain yang lazim ialah **lema zig-zag**.
:::
:::

::: {.source-audit #o012-rbt-l24-audit-003}
**Audit sumber 24.3.** Pada Notes.tex baris 5173, suku setelah
$H^{k+1}(i)$ hanya tertulis `$(B_\bullet)$`. Edisi memulihkan suku bertipe
$H^{k+1}(B_\bullet)$ dan mempertahankan semua arah pemetaan dalam barisan.
:::

Bukti teorema ini menggunakan sebuah lema terkenal dalam aljabar homologis,
yaitu **Lema Ular**.

::: {.source-margin #o012-rbt-l24-margin-004}
> **Catatan pinggir sumber (ancillary).** Ada sebuah "kebun binatang" kecil
> berisi lema yang dinamai menurut hewan; contoh lain ialah Lema Salamander
> dan Lema Siput. Nama-nama ini tidak membawa muatan matematis.
:::

## Lema Ular {#o012-rbt-l24-s04}

::: {.lemma #o012-rbt-l24-lem-002 data-source-label="snakeLemma"}
**Lema 24.2 (Lema Ular; alias sumber `snakeLemma`).** Diberikan diagram
komutatif modul-$R$ berikut, dengan kedua baris eksak,

::: {.figure #o012-rbt-l24-fig-001 data-source-format="xypic"}
**Diagram 24.1 (data panah untuk diagram Lema Ular).** Baris atas dan bawah
serta pemetaan vertikalnya adalah

$$
\begin{array}{ccccccccc}
&&A&\xrightarrow{\ i\ }&B&\xrightarrow{\ \pi\ }&C&\longrightarrow&0\\
&&\downarrow\,{\scriptstyle\alpha}&&\downarrow\,{\scriptstyle\beta}&&
\downarrow\,{\scriptstyle\gamma}&&\\
0&\longrightarrow&A'&\xrightarrow{\ i'\ }&B'&
\xrightarrow{\ \pi'\ }&C'&&
\end{array}
$$

dengan persamaan komutativitas

$$
\beta\circ i=i'\circ\alpha,
\qquad
\gamma\circ\pi=\pi'\circ\beta.
$$

Baris atas eksak pada $B,C$ dan $\pi$ surjektif; baris bawah eksak pada
$A',B'$ dan $i'$ injektif. Modul kanan bawah adalah $C'$, bukan $C$.
Tidak ada informasi yang bergantung pada letak panah.
:::

terdapat barisan eksak

$$
\ker\alpha\longrightarrow\ker\beta\longrightarrow\ker\gamma
\xrightarrow{\ \delta\ }\operatorname{coker}\alpha
\longrightarrow\operatorname{coker}\beta
\longrightarrow\operatorname{coker}\gamma.
$$

Eksak di sini dinyatakan pada empat suku internal yang mempunyai pemetaan
masuk dan keluar. Tanpa hipotesis tambahan, tidak diklaim adanya nol tersirat
di kiri $\ker\alpha$ atau di kanan $\operatorname{coker}\gamma$.
[Diagram 24.2](#o012-rbt-l24-fig-002) mencatat seluruh jalur Ular tanpa
bergantung pada warna atau posisi.
:::

::: {.source-audit #o012-rbt-l24-audit-004}
**Audit sumber 24.4.** Diagram Xy-pic pada Notes.tex baris 5186--5189 menulis
modul kanan bawah sebagai $C$. Komutativitas menuntut $C'$. Edisi memperbaiki
tipe itu dan mengganti diagram posisional dengan data panah serta kedua
persamaan komutativitas.
:::

Lema ini merupakan alat utama. Bukti lengkapnya panjang dan mempunyai banyak
rincian, tetapi pada setiap tahap biasanya hanya ada satu atau dua langkah
yang mungkin.

::: {.figure #o012-rbt-l24-fig-002 data-source-format="tikz" data-source-label="fig:snake_lemma"}
**Diagram 24.2 (jalur semantik Lema Ular; alias sumber
`fig:snake_lemma`).** Gambar TikZ sumber menggabungkan Diagram 24.1 dengan
kernel di atas, kokernel di bawah, serta satu jalur penghubung berwarna. Data
yang dibawanya adalah:

- inklusi vertikal $\ker\alpha\to A$, $\ker\beta\to B$, dan
  $\ker\gamma\to C$;
- proyeksi vertikal $A'\to\operatorname{coker}\alpha$,
  $B'\to\operatorname{coker}\beta$, dan
  $C'\to\operatorname{coker}\gamma$;
- panah horizontal yang diinduksi oleh $i,\pi,i',\pi'$; dan
- jalur ular, yang mulai dari $c\in\ker\gamma$, mengangkat $c$ melalui
  $\pi$ ke $b\in B$, menurunkan $b$ melalui $\beta$ ke $B'$, mengangkat
  balik melalui $i'$ ke $a'\in A'$, lalu mengambil kelas
  $[a']\in\operatorname{coker}\alpha$.

Jalur terakhir mendefinisikan $\delta$. Warna merah dan geometri jalur pada
gambar sumber tidak memuat informasi tambahan; semua pilihan dan
ketakbergantungannya dibuktikan di bawah.
:::

::: {.proof #o012-rbt-l24-proof-003 data-origin="source-proof-expanded"}
**Bukti lengkap Lema Ular.** Sumber memecah bukti menjadi enam kewajiban:

1. membangun fungsi
   $\delta\colon\ker\gamma\to\operatorname{coker}\alpha$;
2. membuktikan bahwa $\delta$ adalah homomorfisma modul-$R$;
3. membuktikan

   $$
   \operatorname{im}(\ker\alpha\to\ker\beta)
   =\ker(\ker\beta\to\ker\gamma);
   $$

4. membuktikan
   $\operatorname{im}(\ker\beta\to\ker\gamma)=\ker\delta$;
5. membuktikan

   $$
   \operatorname{im}\delta
   =\ker(\operatorname{coker}\alpha\to\operatorname{coker}\beta);
   $$

6. membuktikan

   $$
   \operatorname{im}(\operatorname{coker}\alpha
   \to\operatorname{coker}\beta)
   =\ker(\operatorname{coker}\beta
   \to\operatorname{coker}\gamma).
   $$

Pemetaan selain $\delta$ adalah pemetaan yang diinduksi oleh diagram:

$$
i_K(a)=i(a),\qquad \pi_K(b)=\pi(b),\qquad
\overline i([a'])=[i'(a')],\qquad
\overline\pi([b'])=[\pi'(b')].
$$

Keempatnya $R$-linear karena masing-masing merupakan pembatasan atau pemetaan
hasil bagi dari homomorfisma modul-$R$ pada diagram semula.

Pemetaan kernel memang mendarat di kernel karena kuadrat-kuadratnya
komutatif. Pemetaan kokernel terdefinisi dengan baik: misalnya,
$i'(a'+\alpha(a))-i'(a')=i'\alpha(a)=\beta i(a)$ berada di
$\operatorname{im}\beta$; argumen untuk $\overline\pi$ sama.

**1. Konstruksi penghubung.** Ambil $c\in\ker\gamma\subseteq C$. Karena
$\pi$ surjektif, pilih $b\in B$ dengan $\pi(b)=c$. Komutativitas memberi

$$
\pi'(\beta(b))=\gamma(\pi(b))=\gamma(c)=0.
$$

Eksaknya baris bawah pada $B'$ menghasilkan $a'_b\in A'$ dengan
$i'(a'_b)=\beta(b)$. Unsur ini unik karena $i'$ injektif. Definisikan

$$
\delta(c):=[a'_b]
\in A'/\operatorname{im}\alpha
=\operatorname{coker}\alpha.
$$

Untuk memeriksa bahwa kelas ini tidak bergantung pada pengangkatan, ambil
$\widetilde b\in B$ lain dengan $\pi(\widetilde b)=c$. Maka
$\pi(b-\widetilde b)=0$. Eksaknya baris atas pada $B$ memberi
$a\in A$ dengan $i(a)=b-\widetilde b$. Oleh komutativitas,

$$
\begin{aligned}
i'(a'_b-a'_{\widetilde b})
&=\beta(b)-\beta(\widetilde b)\\
&=\beta(i(a))\\
&=i'(\alpha(a)).
\end{aligned}
$$

Injektivitas $i'$ memberi
$a'_b-a'_{\widetilde b}=\alpha(a)$, sehingga
$[a'_b]=[a'_{\widetilde b}]$. Jadi $\delta$ terdefinisi dengan baik.

**2. Linearitas $R$.** Untuk $c_1,c_2\in\ker\gamma$ dan $r,s\in R$,
pilih $b_1,b_2$ dengan $\pi(b_j)=c_j$, serta $a'_j$ dengan
$i'(a'_j)=\beta(b_j)$. Unsur $rb_1+sb_2$ mengangkat $rc_1+sc_2$, dan

$$
i'(ra'_1+sa'_2)
=r\beta(b_1)+s\beta(b_2)
=\beta(rb_1+sb_2).
$$

Oleh definisi penghubung dan ketakbergantungannya dari pilihan,

$$
\delta(rc_1+sc_2)=r\delta(c_1)+s\delta(c_2).
$$

Jadi $\delta$ adalah homomorfisma modul-$R$.

Teknik yang dipakai selanjutnya disebut **pengejaran diagram**: kita mulai
dengan unsur dalam satu modul, menggunakan pemetaan atau eksaknya barisan
untuk menghasilkan unsur pada modul berdekatan, lalu mengulangi proses sampai
mencapai modul yang diperlukan.

**3. Eksak pada $\ker\beta$.** Jika $a\in\ker\alpha$, maka
$\beta(i(a))=i'(\alpha(a))=0$, dan tentu $\pi(i(a))=0$; jadi
$\operatorname{im}i_K\subseteq\ker\pi_K$. Sebaliknya, bila
$b\in\ker\beta$ dan $\pi(b)=0$, eksaknya baris atas memberi $a\in A$
dengan $i(a)=b$. Kemudian

$$
0=\beta(b)=\beta(i(a))=i'(\alpha(a)).
$$

Karena $i'$ injektif, $\alpha(a)=0$. Jadi $a\in\ker\alpha$ dan
$b=i_K(a)$, sehingga $\operatorname{im}i_K=\ker\pi_K$.

**4. Eksak pada $\ker\gamma$.** Andaikan $c\in\ker\gamma$ dan
$\delta(c)=0$. Pilih $b$ dan $a'_b$ seperti pada konstruksi. Persamaan
$[a'_b]=0$ berarti terdapat $a\in A$ dengan $a'_b=\alpha(a)$. Maka

$$
\beta(b-i(a))
=\beta(b)-i'(\alpha(a))
=i'(a'_b)-i'(a'_b)=0,
$$

sedangkan $\pi(b-i(a))=c$. Jadi $c$ berada dalam citra
$\ker\beta\to\ker\gamma$. Sebaliknya, jika $c=\pi(b)$ untuk
$b\in\ker\beta$, maka $i'(a'_b)=\beta(b)=0$. Injektivitas $i'$ memberi
$a'_b=0$, sehingga $\delta(c)=0$. Dengan demikian

$$
\operatorname{im}(\ker\beta\to\ker\gamma)=\ker\delta.
$$

**5. Eksak pada $\operatorname{coker}\alpha$.** Untuk
$c\in\ker\gamma$, konstruksi memberi
$\delta(c)=[a'_b]$. Citranya dalam $\operatorname{coker}\beta$ ialah

$$
\overline i([a'_b])=[i'(a'_b)]=[\beta(b)]=0.
$$

Jadi $\operatorname{im}\delta\subseteq\ker\overline i$. Sebaliknya,
ambil $[a']\in\operatorname{coker}\alpha$ dengan
$\overline i([a'])=0$. Artinya $i'(a')=\beta(b)$ untuk suatu $b\in B$.
Letakkan $c:=\pi(b)$. Maka

$$
\gamma(c)=\gamma(\pi(b))=\pi'(\beta(b))=\pi'(i'(a'))=0,
$$

dan pengangkatan $b$ dalam definisi memberi $\delta(c)=[a']$. Jadi
$\operatorname{im}\delta=\ker\overline i$.

**6. Eksak pada $\operatorname{coker}\beta$.** Komposisi
$\overline\pi\,\overline i$ nol karena $\pi'i'=0$. Sekarang ambil
$[b']\in\operatorname{coker}\beta$ dengan
$\overline\pi([b'])=0$. Ini berarti $\pi'(b')\in\operatorname{im}\gamma$,
jadi terdapat $c\in C$ dengan $\gamma(c)=\pi'(b')$. Pilih $b\in B$ dengan
$\pi(b)=c$. Kemudian

$$
\pi'(b'-\beta(b))
=\pi'(b')-\gamma(\pi(b))=0.
$$

Eksaknya baris bawah pada $B'$ memberi $a'\in A'$ dengan
$b'-\beta(b)=i'(a')$. Sesudah mengambil kelas modulo
$\operatorname{im}\beta$ kita memperoleh
$[b']=[i'(a')]=\overline i([a'])$. Maka
$\ker\overline\pi\subseteq\operatorname{im}\overline i$, dan inklusi
sebaliknya sudah dibuktikan. Keempat posisi internal itu eksak, sehingga
barisan dalam pernyataan lema eksak.
:::

::: {.source-audit #o012-rbt-l24-audit-005}
**Audit sumber 24.5.** Bukti sumber hanya mengerjakan konstruksi penghubung
serta eksaknya posisi keempat dan kelima; linearitas dan posisi ketiga serta
keenam diserahkan kepada pembaca. Edisi menyelesaikan seluruh enam kewajiban,
mengetik keempat pemetaan terinduksi, dan memperbaiki selip notasi
$a_b/a'_b$ tanpa mengubah strategi pengejaran diagram sumber.
:::

## Diagram persiapan {#o012-rbt-l24-s05}

Untuk menerapkan Lema Ular pada bukti
[Teorema 24.1](#o012-rbt-l24-thm-001), kita perlu membangun diagram yang
mempunyai sifat yang sesuai. Menerapkan Lema Ular langsung pada dua derajat
dari barisan eksak pendek kompleks bukan langkah yang benar, sebab kernel dan
kokernel yang dihasilkan dengan cara itu bukan grup kohomologi dalam teorema.

::: {.lemma #o012-rbt-l24-lem-003 data-source-label="lemma:setup_for_algMV"}
**Lema 24.3 (diagram persiapan; alias sumber
`lemma:setup_for_algMV`).** Diagram komutatif berikut memenuhi hipotesis Lema
Ular; khususnya, kedua barisnya eksak pada semua posisi yang mempunyai panah
masuk dan keluar.

::: {.figure #o012-rbt-l24-fig-003 data-source-format="xypic"}
**Diagram 24.3 (data panah diagram persiapan).** Untuk
$K=A,B,C$, tuliskan

$$
Q_K^k:=K_k/\delta_{k-1}^K(K_{k-1}),
\qquad
Z_K^{k+1}:=\ker(\delta_{k+1}^K).
$$

Diagramnya adalah

$$
\begin{array}{ccccccccc}
&&Q_A^k&\longrightarrow&Q_B^k&\longrightarrow&Q_C^k&\longrightarrow&0\\
&&\downarrow\,{\scriptstyle\overline\delta_A^k}&&
\downarrow\,{\scriptstyle\overline\delta_B^k}&&
\downarrow\,{\scriptstyle\overline\delta_C^k}&&\\
0&\longrightarrow&Z_A^{k+1}&\longrightarrow&Z_B^{k+1}&
\longrightarrow&Z_C^{k+1}&&
\end{array}
$$

dengan

$$
\overline\delta_K^k([x])=\delta_k^K(x).
$$

Panah horizontal diinduksi oleh $i$ dan $\pi$. Tidak ada sifat yang
bergantung pada posisi visual diagram.
:::
:::

::: {.proof #o012-rbt-l24-proof-004 data-origin="source-proof-completed"}
**Bukti.** Pertama, setiap pemetaan vertikal terdefinisi dengan baik. Jika
$x$ diganti oleh $x+\delta_{k-1}^K(u)$, maka

$$
\delta_k^K(x+\delta_{k-1}^K(u))
=\delta_k^K(x)+\delta_k^K\delta_{k-1}^K(u)
=\delta_k^K(x).
$$

Selain itu,
$\delta_{k+1}^K\delta_k^K(x)=0$, sehingga citranya memang berada di
$Z_K^{k+1}$. Karena $i$ dan $\pi$ adalah morfisma kompleks, kedua kuadrat
komutatif.

Untuk baris atas, pemetaan $Q_B^k\to Q_C^k$ surjektif: kelas $[c]$ dapat
diangkat dengan memilih $b\in B_k$ sedemikian sehingga $\pi(b)=c$. Jika
$[b]\in Q_B^k$ dipetakan ke nol, maka
$\pi(b)=\delta_{k-1}^C(c_-)$ untuk suatu $c_-\in C_{k-1}$. Pilih
$b_-\in B_{k-1}$ dengan $\pi(b_-)=c_-$. Dengan komutativitas diferensial,

$$
\pi\bigl(b-\delta_{k-1}^B(b_-)\bigr)=0.
$$

Eksaknya barisan kompleks pada derajat $k$ menghasilkan $a\in A_k$ dengan
$i(a)=b-\delta_{k-1}^B(b_-)$. Oleh karena itu $[b]$ adalah citra $[a]$.
Sebaliknya, setiap citra dari $Q_A^k$ dipetakan ke nol sebab $\pi i=0$.
Jadi baris atas eksak pada $Q_B^k,Q_C^k$.

Untuk baris bawah, pemetaan $Z_A^{k+1}\to Z_B^{k+1}$ injektif karena $i$
injektif pada setiap derajat. Jika $b\in Z_B^{k+1}$ dan $\pi(b)=0$, maka
$b=i(a)$ untuk suatu $a\in A_{k+1}$. Selanjutnya

$$
i(\delta_{k+1}^A(a))
=\delta_{k+1}^B(i(a))
=\delta_{k+1}^B(b)=0.
$$

Injektivitas $i$ memberi $\delta_{k+1}^A(a)=0$, jadi
$a\in Z_A^{k+1}$. Inklusi sebaliknya mengikuti dari $\pi i=0$. Maka baris
bawah eksak pada $Z_A^{k+1},Z_B^{k+1}$. Inilah tepat hipotesis sisi kanan
atas dan sisi kiri bawah yang diperlukan dalam Lema Ular.
:::

::: {.source-audit #o012-rbt-l24-audit-006}
**Audit sumber 24.6.** Lingkungan bukti pada Notes.tex baris 5332--5334 hanya
berisi `Exercise, for now.` Edisi membuktikan keterdefinisian ketiga pemetaan
vertikal, komutativitas diagram, eksaknya baris hasil bagi, dan eksaknya baris
kernel.
:::

## Bukti teorema dan penyambungan {#o012-rbt-l24-s06}

::: {.proof #o012-rbt-l24-proof-005 data-origin="source-proof-expanded"}
**Bukti Teorema 24.1.** Untuk $K=A,B,C$, gunakan notasi dari Diagram 24.3.
Kernel pemetaan vertikal ialah

$$
\begin{aligned}
\ker\overline\delta_K^k
&=\{[x]\in K_k/\delta_{k-1}^K(K_{k-1})
      \mid \delta_k^K(x)=0\}\\
&=\ker(\delta_k^K)/\delta_{k-1}^K(K_{k-1})\\
&=H^k(K_\bullet).
\end{aligned}
$$

Kesetaraan kedua sah karena
$\delta_{k-1}^K(K_{k-1})\subseteq\ker\delta_k^K$. Dengan demikian ini bukan
hanya kesamaan ukuran: pemetaan $[x]\mapsto[x]$ memberi isomorfisma kanonik.

::: {.source-margin #o012-rbt-l24-margin-005}
> **Catatan pinggir sumber.** Sumber menandai identifikasi kernel ini sebagai
> "latihan". Bukti eksplisitnya diberikan tepat di atas.
:::

Citra pemetaan vertikal adalah

$$
\operatorname{im}\overline\delta_K^k
=\delta_k^K(K_k)
\subseteq\ker(\delta_{k+1}^K).
$$

Karena itu kokernelnya adalah

$$
\operatorname{coker}\overline\delta_K^k
=\frac{\ker(\delta_{k+1}^K)}{\delta_k^K(K_k)}
=H^{k+1}(K_\bullet).
$$

Rumus ini juga memperbaiki kurung penutup yang hilang dalam rumus citra pada
sumber. Semua isomorfisma tersebut natural terhadap morfisma kompleks.

Dengan menerapkan [Lema 24.2](#o012-rbt-l24-lem-002) pada diagram yang
dijamin oleh [Lema 24.3](#o012-rbt-l24-lem-003), lalu memakai identifikasi
kernel dan kokernel tadi, kita memperoleh barisan eksak enam-suku

$$
H^k(A_\bullet)\longrightarrow H^k(B_\bullet)
\longrightarrow H^k(C_\bullet)
\xrightarrow{\ \delta^k\ }H^{k+1}(A_\bullet)
\longrightarrow H^{k+1}(B_\bullet)
\longrightarrow H^{k+1}(C_\bullet)
$$

untuk setiap $k$. Pemetaan-pemetaan selain $\delta^k$ tepat pemetaan
kohomologi yang diinduksi oleh $i$ dan $\pi$: konstruksi hasil bagi, kernel,
dan semua isomorfisma di atas memakai pemetaan yang sama.

::: {.source-margin #o012-rbt-l24-margin-006}
> **Catatan pinggir sumber, dibuktikan.** Jika untuk setiap $k$ tersedia
> barisan eksak
> $L_{k-1}\to M_{k-1}\to N_{k-1}\to L_k\to M_k\to N_k$
> dan pemetaan yang berulang pada suku bersama benar-benar sama, maka
> barisan-barisannya menyambung menjadi
> $\cdots\to N_{k-2}\to L_{k-1}\to M_{k-1}\to N_{k-1}\to L_k\to M_k\to N_k\to L_{k+1}\to\cdots$.
:::

Dalam kasus kita, barisan untuk indeks $k+1$ dimulai dengan tiga suku dan
pemetaan terakhir dari barisan indeks $k$. Karena identifikasi kernel dan
kokernel bersifat kanonik, bukan sekadar isomorfisma yang dipilih secara
terpisah, kedua salinan setiap suku $H^{k+1}$ beserta pemetaannya identik.
Maka barisan enam-suku itu dapat disambung tanpa celah menjadi

$$
\cdots\longrightarrow H^k(A_\bullet)
\xrightarrow{\ H^k(i)\ }H^k(B_\bullet)
\xrightarrow{\ H^k(\pi)\ }H^k(C_\bullet)
\xrightarrow{\ \delta^k\ }H^{k+1}(A_\bullet)
\longrightarrow\cdots,
$$

dan eksaknya pada setiap suku diwarisi dari salah satu barisan enam-suku yang
memuat suku tersebut. Inilah barisan eksak panjang yang dinyatakan dalam
teorema.
:::

::: {.source-audit #o012-rbt-l24-audit-007}
**Audit sumber 24.7.** Notes.tex baris 5338--5354 menandai identifikasi
kernel sebagai latihan, meninggalkan identifikasi kokernel tanpa bukti,
kehilangan satu kurung pada rumus citra, dan menyatakan penyambungan hanya
sebagai latihan pinggir. Edisi membuktikan kedua identifikasi, memulihkan
kurung, dan menunjukkan bahwa suku serta pemetaan bersama benar-benar sama
ketika $k$ berubah.
:::

## Kealamian {#o012-rbt-l24-s07}

Ada satu konsekuensi yang berguna. Diberikan dua diagram seperti yang masuk
ke Lema Ular dan homomorfisma antara setiap modul yang membuat semua kubus
yang mungkin menjadi komutatif, kita memperoleh pemetaan terinduksi antara
kernel dan kokernel. Dengan demikian, untuk dua barisan eksak pendek kompleks
dan sebuah morfisma di antaranya, terdapat morfisma antara **barisan eksak
panjang** yang dihasilkan.

::: {.source-margin #o012-rbt-l24-margin-007}
> **Catatan pinggir sumber.** Sifat ini diringkas dengan mengatakan bahwa
> Lema Ular bersifat **natural**.
:::

Situasi ini muncul, misalnya, ketika gelanggang koefisien kohomologi
himpunan-$\Delta$ diganti dalam salah satu contoh motivasi. Ia juga muncul
untuk pemetaan pasangan

$$
(X_\bullet,A_\bullet)\longrightarrow(Y_\bullet,B_\bullet),
$$

karena setiap pasangan menghasilkan barisan eksak pendek kompleks dan
pemetaan pasangan menginduksi morfisma antara kedua barisan tersebut.

::: {.proof #o012-rbt-l24-proof-006 data-origin="edition-proof-closure"}
**Verifikasi kealamian pemetaan penghubung.** Misalkan homomorfisma vertikal
tambahan mengirim diagram Lema Ular pertama ke diagram kedua dan membuat
semua kubus komutatif. Untuk $c\in\ker\gamma$, pilih pengangkatan
$b\in B$ dan unsur $a'\in A'$ dengan $\pi(b)=c$ serta $i'(a')=\beta(b)$.
Sesudah ketiga unsur itu dipetakan ke diagram kedua, komutativitas kubus
menunjukkan bahwa citra $b$ mengangkat citra $c$ dan citra $a'$ memenuhi
persamaan yang mendefinisikan penghubung kedua. Karena penghubung tidak
bergantung pada pilihan pengangkatan,

$$
\delta_2(f_C(c))
=\overline f_{A'}(\delta_1(c)).
$$

Jadi bujur sangkar yang melibatkan pemetaan penghubung komutatif. Bujur
sangkar lain komutatif langsung dari fungtorialitas kernel, kokernel, dan
kohomologi. Akibatnya yang dihasilkan bukan sekadar pemetaan antara kompleks
yang tidak ditentukan, melainkan morfisma antara kedua barisan eksak panjang.
:::

::: {.source-audit #o012-rbt-l24-audit-008}
**Audit sumber 24.8.** Notes.tex baris 5357--5367 mula-mula menyebut
"pemetaan antara kompleks" sebelum memperjelas konsekuensinya. Edisi
menyatakan sasaran yang tepat—morfisma antara barisan eksak panjang—dan
memeriksa komutativitas pemetaan penghubung melalui pengangkatan yang sama.
:::

# Pendamping penguasaan: pemeriksaan, petunjuk, dan solusi lengkap {.unnumbered #o012-rbt-l24-mastery}

Enam paket berikut adalah materi asli edisi. Semuanya dibatasi pada sasaran
Unit 24: korantai relatif, kernel morfisma kompleks, konstruksi dan eksaknya
Lema Ular, diagram persiapan, penyambungan, dan kealamian.

::: {.exercise #o012-rbt-l24-mcheck-001 data-origin="edition-original"}
**Pemeriksaan Penguasaan 24.1 (korantai relatif dan perluasan nol).** Untuk
inklusi sub-himpunan-$\Delta$
$i\colon A_\bullet\hookrightarrow X_\bullet$, buktikan langsung bahwa

$$
0\longrightarrow C^\bullet(X_\bullet,A_\bullet;R)
\longrightarrow C^\bullet(X_\bullet;R)
\xrightarrow{\ i^*\ }C^\bullet(A_\bullet;R)
\longrightarrow0
$$

adalah barisan eksak pendek kompleks. Lalu, untuk
$A_\bullet=\{0\}\subseteq\Delta[1]$ dan $1_R\ne0$, tunjukkan bahwa
perluasan dengan nol yang memisahkan $i^*$ pada setiap derajat bukan
pemetaan korantai.
:::

::: {.hint #o012-rbt-l24-hint-001 data-origin="edition-original"}
**Petunjuk.** Restriksi dan diferensial sama-sama dibentuk dengan
prakomposisi oleh *face map*. Untuk contoh tandingan, perluas fungsi bernilai
$1$ pada simpul $0$ menjadi fungsi yang bernilai nol pada simpul $1$, lalu
hitung kobatasnya pada sisi $01$.
:::

::: {.solution #o012-rbt-l24-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 24.1.** Pada derajat $n$,
$i_n^*(g)=g|_{A_n}$. Karena *face map* $A_\bullet$ adalah pembatasan *face
map* $X_\bullet$, untuk setiap $g\in R^{X_n}$ berlaku

$$
\delta_A^n(i_n^*g)=i_{n+1}^*(\delta_X^n g).
$$

Jadi $i^*$ adalah pemetaan korantai. Ia surjektif pada setiap derajat: untuk
$h\in R^{A_n}$, tetapkan $\widehat h=h$ pada $A_n$ dan nol di luar $A_n$.
Kernel restriksi stabil terhadap diferensial oleh persamaan komutativitas
tadi, dan menurut Definisi 24.1 kernel itu ialah
$C^\bullet(X_\bullet,A_\bullet;R)$. Inklusi kernel injektif, citranya tepat
kernel $i^*$, dan $i^*$ surjektif. Maka barisan tersebut eksak pendek sebagai
barisan kompleks.

Sekarang ambil $X_\bullet=\Delta[1]$ dan $A_\bullet$ yang hanya memuat simpul
$0$. Jika $h(0)=1_R$, perluasan nol $e^0h$ mempunyai nilai $1_R$ pada simpul
$0$ dan $0$ pada simpul $1$. Dengan salah satu konvensi tanda yang konsisten,

$$
(\delta_X^0e^0h)(01)=0-1_R=-1_R\ne0
$$

(dengan konvensi urutan muka berlawanan nilainya $1_R$, tetap taknol).
Sebaliknya $A_1=\varnothing$, sehingga $\delta_A^0h=0$ dan perluasan nolnya
pada derajat satu juga nol. Jadi
$\delta_X^0e^0\ne e^1\delta_A^0$: pemisahan modul derajat demi derajat
bukan pemisahan kompleks.
:::

::: {.exercise #o012-rbt-l24-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 24.2 (kernel morfisma kompleks).** Misalkan
$\varphi\colon A_\bullet\to B_\bullet$ adalah morfisma kompleks. Bangun
diferensial pada $K_n:=\ker\varphi_n$, buktikan bahwa diferensial itu bertipe
$K_n\to K_{n+1}$ dan berkuadrat nol, lalu buktikan bahwa konstruksi kernel
ini natural terhadap sebuah bujur sangkar komutatif morfisma kompleks.
:::

::: {.hint #o012-rbt-l24-hint-002 data-origin="edition-original"}
**Petunjuk.** Terapkan persamaan
$\varphi_{n+1}d_A^n=d_B^n\varphi_n$ pada unsur $K_n$. Untuk kealamian,
batasi pemetaan vertikal pada kedua kernel dan gunakan komutativitas bujur
sangkar derajat demi derajat.
:::

::: {.solution #o012-rbt-l24-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 24.2.** Jika $a\in K_n$, maka

$$
\varphi_{n+1}(d_A^n a)=d_B^n(\varphi_n a)=0,
$$

jadi $d_A^n a\in K_{n+1}$. Definisikan

$$
d_K^n:=d_A^n|_{K_n}\colon K_n\longrightarrow K_{n+1}.
$$

Karena diferensial ini merupakan pembatasan,

$$
d_K^{n+1}d_K^n
=\left.d_A^{n+1}d_A^n\right|_{K_n}=0.
$$

Maka $K_\bullet$ adalah kompleks. Untuk kealamian, ambil bujur sangkar
komutatif morfisma kompleks

$$
\begin{array}{ccc}
A_\bullet&\xrightarrow{\ \varphi\ }&B_\bullet\\
\downarrow{\scriptstyle f}&&\downarrow{\scriptstyle g}\\
A'_\bullet&\xrightarrow{\ \varphi'\ }&B'_\bullet.
\end{array}
$$

Jika $a\in\ker\varphi_n$, maka
$\varphi'_n(f_n(a))=g_n(\varphi_n(a))=0$, sehingga $f_n$ membatasi diri ke
$\ker\varphi_n\to\ker\varphi'_n$. Karena $f$ adalah morfisma kompleks,
pembatasan tersebut komutatif dengan $d_K$. Identitas dan komposisi tetap
identitas dan komposisi sesudah pembatasan; jadi kernel kompleks bersifat
natural.
:::

::: {.exercise #o012-rbt-l24-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 24.3 (membangun penghubung Ular).** Dalam diagram
Lema Ular, mulai dari $c\in\ker\gamma$. Bangun
$\delta(c)\in\operatorname{coker}\alpha$ dengan dua pengangkatan yang tepat,
lalu buktikan bahwa kelas yang dihasilkan tidak bergantung pada pilihan
$b\in B$ dengan $\pi(b)=c$. Jelaskan persis tempat digunakannya eksak baris
atas, eksak baris bawah, surjektivitas $\pi$, dan injektivitas $i'$.
:::

::: {.hint #o012-rbt-l24-hint-003 data-origin="edition-original"}
**Petunjuk.** Pilih $b$ dengan $\pi b=c$. Tunjukkan bahwa
$\beta b\in\ker\pi'=\operatorname{im}i'$, lalu tulis
$\beta b=i'a'_b$. Untuk dua pilihan $b,\widetilde b$, tulis
$b-\widetilde b=i(a)$ dan bandingkan $a'_b$ dengan
$a'_{\widetilde b}$.
:::

::: {.solution #o012-rbt-l24-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 24.3.** Surjektivitas $\pi$ memberi $b\in B$ dengan
$\pi(b)=c$. Karena $c\in\ker\gamma$ dan diagram komutatif,

$$
\pi'(\beta(b))=\gamma(\pi(b))=\gamma(c)=0.
$$

Eksaknya baris bawah pada $B'$ memberi
$\beta(b)=i'(a'_b)$ untuk suatu $a'_b\in A'$, dan injektivitas $i'$ membuat
$a'_b$ unik. Definisikan $\delta(c)=[a'_b]$ modulo
$\operatorname{im}\alpha$.

Jika $\widetilde b$ adalah pengangkatan lain, maka
$b-\widetilde b\in\ker\pi=\operatorname{im}i$ oleh eksaknya baris atas pada
$B$. Jadi $b-\widetilde b=i(a)$ untuk suatu $a\in A$. Dengan
$i'(a'_{\widetilde b})=\beta(\widetilde b)$ dan komutativitas,

$$
i'(a'_b-a'_{\widetilde b})
=\beta(b-\widetilde b)
=\beta(i(a))
=i'(\alpha(a)).
$$

Injektivitas $i'$ memberi
$a'_b-a'_{\widetilde b}=\alpha(a)$. Karena selisihnya berada di
$\operatorname{im}\alpha$, kedua unsur menentukan kelas kokernel yang sama.
Jadi $\delta$ terdefinisi dengan baik. Hipotesis digunakan tepat sebagai
berikut: $\pi$ surjektif untuk memilih $b$; komutativitas dan eksak bawah
untuk memperoleh $a'_b$; $i'$ injektif untuk keunikan dan pembatalan; eksak
atas untuk membandingkan dua pengangkatan.
:::

::: {.exercise #o012-rbt-l24-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 24.4 (linearitas dan eksaknya Lema Ular).** Dengan
penghubung dari Pemeriksaan 24.3, buktikan linearitas $\delta$. Kemudian
buktikan eksaknya barisan Ular pada keempat suku internal
$\ker\beta$, $\ker\gamma$, $\operatorname{coker}\alpha$, dan
$\operatorname{coker}\beta$. Jangan menggunakan geometri atau warna Diagram
24.2 sebagai alasan.
:::

::: {.hint #o012-rbt-l24-hint-004 data-origin="edition-original"}
**Petunjuk.** Untuk linearitas gunakan $rb_1+sb_2$ sebagai pengangkatan.
Pada posisi kernel gunakan eksaknya baris atas serta injektivitas $i'$. Pada
posisi kokernel, terjemahkan "kelas nol" menjadi "berbeda dari nol oleh
citra pemetaan vertikal", lalu gunakan eksaknya baris bawah dan
surjektivitas $\pi$.
:::

::: {.solution #o012-rbt-l24-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 24.4.** Bila $b_j$ mengangkat $c_j$ dan
$i'(a'_j)=\beta(b_j)$, maka $rb_1+sb_2$ mengangkat $rc_1+sc_2$ serta

$$
i'(ra'_1+sa'_2)=\beta(rb_1+sb_2).
$$

Karena kelas penghubung tidak bergantung pada pilihan,
$\delta(rc_1+sc_2)=r\delta(c_1)+s\delta(c_2)$.

Pada $\ker\beta$, citra $\ker\alpha$ berada dalam kernel pemetaan ke
$\ker\gamma$. Jika $b\in\ker\beta$ dan $\pi(b)=0$, tulis $b=i(a)$.
Persamaan $0=\beta(b)=i'(\alpha(a))$ dan injektivitas $i'$ memberi
$a\in\ker\alpha$. Jadi kedua himpunan itu sama.

Pada $\ker\gamma$, bila $\delta(c)=0$, pilih $b$ dengan $\pi(b)=c$ dan
$i'(a'_b)=\beta(b)$. Tulis $a'_b=\alpha(a)$; maka
$b-i(a)\in\ker\beta$ dan tetap dipetakan ke $c$. Arah sebaliknya mengikuti
karena untuk $b\in\ker\beta$ kita mendapat $a'_b=0$. Jadi
$\operatorname{im}(\ker\beta\to\ker\gamma)=\ker\delta$.

Pada $\operatorname{coker}\alpha$, kelas $\delta(c)=[a'_b]$ dipetakan ke
$[i'(a'_b)]=[\beta(b)]=0$. Jika sebaliknya $[i'(a')]=0$, tulis
$i'(a')=\beta(b)$ dan tetapkan $c=\pi(b)$. Komutativitas memberi
$c\in\ker\gamma$, dan $\delta(c)=[a']$.

Terakhir, pada $\operatorname{coker}\beta$, citra kelas dari
$\operatorname{coker}\alpha$ jelas mati di
$\operatorname{coker}\gamma$. Jika $[b']$ mati di sana, pilih $c\in C$
dengan $\gamma(c)=\pi'(b')$, lalu pilih $b\in B$ dengan $\pi(b)=c$.
Maka $\pi'(b'-\beta b)=0$, sehingga $b'-\beta b=i'(a')$. Modulo
$\operatorname{im}\beta$ kita memperoleh $[b']=[i'(a')]$. Ini membuktikan
eksaknya keempat posisi tanpa memakai informasi posisional gambar.
:::

::: {.exercise #o012-rbt-l24-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 24.5 (eksaknya diagram persiapan).** Mulai dari
barisan eksak pendek kompleks
$0\to A_\bullet\xrightarrow{i}B_\bullet\xrightarrow{\pi}C_\bullet\to0$.
Buktikan bahwa semua pemetaan vertikal pada Diagram 24.3 terdefinisi dengan
baik dan membentuk bujur sangkar komutatif. Lalu buktikan eksaknya baris
hasil bagi dan baris kernel pada posisi yang diperlukan Lema Ular.
:::

::: {.hint #o012-rbt-l24-hint-005 data-origin="edition-original"}
**Petunjuk.** Gunakan $\delta_k\delta_{k-1}=0$ untuk pemetaan vertikal. Jika
$[b]$ mati dalam hasil bagi $C$, angkat dahulu batas yang mewakili
$\pi(b)$ ke derajat $k-1$ di $B$, kurangi batasnya dari $b$, lalu gunakan
$\ker\pi=\operatorname{im}i$. Untuk baris bawah, gunakan injektivitas $i$.
:::

::: {.solution #o012-rbt-l24-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 24.5.** Rumus
$\overline\delta_K^k([x])=\delta_k^K(x)$ tidak berubah jika $x$ diganti
dengan $x+\delta_{k-1}^K(u)$, karena
$\delta_k^K\delta_{k-1}^K=0$. Nilainya berada di
$\ker\delta_{k+1}^K$ karena $\delta_{k+1}^K\delta_k^K=0$. Sifat morfisma
kompleks untuk $i$ dan $\pi$ membuktikan komutativitas kedua bujur sangkar.

Pemetaan $Q_B^k\to Q_C^k$ surjektif karena $B_k\to C_k$ surjektif. Jika
$[b]$ masuk ke nol, tulis $\pi(b)=\delta_{k-1}^C(c_-)$ dan angkat $c_-$ ke
$b_-\in B_{k-1}$. Maka

$$
\pi(b-\delta_{k-1}^B b_-)=0,
$$

jadi $b-\delta_{k-1}^B b_-=i(a)$ untuk suatu $a\in A_k$. Karena batas yang
dikurangkan hilang dalam hasil bagi, $[b]$ adalah citra $[a]$. Komposisi dari
$Q_A^k$ ke $Q_C^k$ nol, sehingga baris atas eksak.

Pada baris bawah, $Z_A^{k+1}\to Z_B^{k+1}$ injektif. Jika
$b\in Z_B^{k+1}$ dan $\pi(b)=0$, tulis $b=i(a)$. Lalu
$0=\delta_B b=i(\delta_A a)$; injektivitas $i$ memberi
$\delta_A a=0$. Jadi $a\in Z_A^{k+1}$ dan baris bawah eksak. Semua hipotesis
Lema Ular sekarang terverifikasi.
:::

::: {.exercise #o012-rbt-l24-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 24.6 (penyambungan dan kealamian).** Untuk setiap
$k$, Lema Ular pada Diagram 24.3 memberi barisan enam-suku. Buktikan
identifikasi

$$
\ker\overline\delta_K^k\cong H^k(K_\bullet),
\qquad
\operatorname{coker}\overline\delta_K^k\cong H^{k+1}(K_\bullet),
$$

jelaskan mengapa barisan untuk semua $k$ menyambung menjadi satu barisan
eksak panjang, dan buktikan bahwa sebuah morfisma antara dua barisan eksak
pendek kompleks menghasilkan morfisma antara barisan eksak panjangnya.
:::

::: {.hint #o012-rbt-l24-hint-006 data-origin="edition-original"}
**Petunjuk.** Kernel pemetaan $[x]\mapsto\delta_kx$ adalah kosiklus modulo
kobatas; kokernelnya adalah kosiklus derajat $k+1$ modulo citra
$\delta_k$. Untuk kealamian, petakan satu pilihan pengangkatan dalam
konstruksi Ular ke diagram kedua dan gunakan ketakbergantungan penghubung
dari pilihan.
:::

::: {.solution #o012-rbt-l24-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 24.6.** Dengan
$Q_K^k=K_k/\operatorname{im}\delta_{k-1}^K$ dan
$Z_K^{k+1}=\ker\delta_{k+1}^K$, pemetaan vertikal ialah
$\overline\delta_K^k([x])=\delta_k^Kx$. Maka

$$
\ker\overline\delta_K^k
=\frac{\ker\delta_k^K}{\operatorname{im}\delta_{k-1}^K}
=H^k(K_\bullet),
$$

sedangkan

$$
\operatorname{coker}\overline\delta_K^k
=\frac{Z_K^{k+1}}{\operatorname{im}\delta_k^K}
=H^{k+1}(K_\bullet).
$$

Karena identifikasi ini kanonik dan pemetaan horizontalnya diinduksi oleh
$i,\pi$, Lema Ular memberi

$$
H^k(A)\to H^k(B)\to H^k(C)\xrightarrow{\delta^k}
H^{k+1}(A)\to H^{k+1}(B)\to H^{k+1}(C).
$$

Barisan untuk $k+1$ memakai tiga suku terakhir yang sama sebagai tiga suku
pertamanya—dengan pemetaan yang sama, bukan salinan yang dipilih secara
sembarang. Karena setiap suku internal dan kedua pemetaan yang mengapitnya
terdapat dalam salah satu barisan enam-suku, penyambungan mempertahankan
eksaknya dan menghasilkan barisan eksak panjang.

Sekarang ambil morfisma antara dua barisan eksak pendek kompleks. Ia
menginduksi morfisma antara semua $Q_K^k$ dan $Z_K^{k+1}$ serta membuat
diagram persiapan komutatif. Jika $c$ diangkat ke $b$ lalu menghasilkan
$a'$, citra ketiga unsur itu merupakan pilihan yang sah dalam diagram kedua.
Karena kelas penghubung tidak bergantung pada pilihan,

$$
f_{A,*}^{k+1}\delta_1^k([c])
=\delta_2^k f_{C,*}^k([c]).
$$

Semua bujur sangkar lain komutatif oleh fungtorialitas kohomologi. Jadi
pemetaan-pemetaan derajat demi derajat menyambung menjadi morfisma antara
barisan eksak panjang, yang membuktikan kealamian.
:::

::: {.boundary #o012-rbt-l24-boundary-001}
**Batas ke Unit 25.** Unit 24 menerjemahkan Notes.tex baris 5113--5369 secara
kontigu. Baris 5113--5121 melanjutkan dan menutup contoh Unit 23; hubungan
timbal baliknya direkam sebagai
`data-continuation-of="o012-rbt-l23-exa-002"`. Penanda
`\lecturenum{25}` berada pada baris 5370 dan tidak dimasukkan. Kursor sumber
berikutnya yang tepat adalah Notes.tex baris 5370.
:::
