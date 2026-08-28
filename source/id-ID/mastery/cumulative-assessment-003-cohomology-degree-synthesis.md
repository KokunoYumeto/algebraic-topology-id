---
title: "Asesmen Kumulatif 3 — Kohomologi, Derajat, dan Sintesis Invarian"
lang: id-ID
course_id: D60
assessment_id: D60-CA03
edition_unit_id: O012-ORIG-CA03
course_route_unit_ids:
  - D60-R13
  - D60-R14
rights: "CC BY-SA 4.0"
origin: "Materi edisi asli; bukan bagian dari sumber Roberts atau Fomberg."
provenance: "OpenAI Codex gpt-5.6-sol, Ultra; disusun atas arahan pengguna; kredit dan hak komponen sumber tetap dipertahankan."
---

# Asesmen Kumulatif 3: kohomologi, derajat, dan sintesis invarian {#o012-d60-ca03}

Asesmen ini menutup delapan sasaran kumulatif pada `D60-R13` dan `D60-R14`.
Beberapa soal memakai kembali prasyarat yang sudah diterima dari route lebih
awal, tetapi setiap pemakaian itu dinyatakan dalam atribut dan tabel cakupan.
Kerjakan semua soal sebelum membuka petunjuk dan solusi jika berkas ini dipakai
sebagai ujian.

Seluruh soal, petunjuk, dan solusi di bawah merupakan materi edisi asli
berlisensi CC BY-SA 4.0. Tidak ada soal dari bank masalah Fomberg yang disalin
atau diadaptasi. Materi ini tidak mengubah urutan ataupun penomoran edisi
Roberts dan Fomberg, serta tidak menyiratkan dukungan atau pengesahan dari
penulis sumber maupun institusinya. Produksi materi ini dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra**; seluruh kredit sumber dan kontributor
manusia tetap dipertahankan.

## Soal 1 — kohomologi, torsi, dan perubahan koefisien {#o012-d60-ca03-s01}

::: {.exercise #o012-d60-ca03-ex-001 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
Pertimbangkan kompleks korantai

$$
0\longrightarrow C^0=\mathbb Z
\xrightarrow{\delta^0}C^1=\mathbb Z^2
\xrightarrow{\delta^1}C^2=\mathbb Z
\longrightarrow0,
$$

dengan

$$
\delta^0(t)=(0,0),
\qquad
\delta^1(a,b)=2a.
$$

1. Periksa bahwa rumus itu benar-benar mendefinisikan kompleks, lalu hitung
   $H^k(C^\bullet)$ untuk setiap $k$.
2. Reduksi matriks diferensial modulo $2$ dan hitung kohomologi kompleks yang
   dihasilkan dengan koefisien $\mathbb F_2$.
3. Setelah memperluas skalar ke $\mathbb Q$, periksa kesamaan karakteristik
   Euler antara modul korantai dan modul kohomologi. Jelaskan informasi mana
   yang hilang dari hitungan dimensi rasional.
:::

::: {.hint #o012-d60-ca03-hint-001 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
**Petunjuk.** Tentukan kernel $\delta^1$ dan citranya secara terpisah.
Bandingkan persamaan $2a=0$ di $\mathbb Z$ dengan persamaan yang sama di
$\mathbb F_2$. Untuk bagian terakhir, hitung rank diferensial di atas
$\mathbb Q$; jangan mengganti faktor torsi dengan dimensi yang tidak
dimilikinya.
:::

::: {.solution #o012-d60-ca03-sol-001 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
**Solusi.** Komposisi $\delta^1\delta^0$ bernilai nol karena $\delta^0$
sendiri nol. Jadi ini memang kompleks korantai. Tidak ada diferensial yang
masuk ke $C^0$, sehingga

$$
H^0(C^\bullet)=\ker\delta^0\cong\mathbb Z.
$$

Di $\mathbb Z$, persamaan $2a=0$ memaksa $a=0$. Maka

$$
\ker\delta^1=\{(0,b):b\in\mathbb Z\}\cong\mathbb Z,
\qquad
\operatorname{im}\delta^0=0,
$$

dan karena itu $H^1(C^\bullet)\cong\mathbb Z$. Pada derajat dua semua unsur
merupakan kosiklus, sedangkan citra $\delta^1$ adalah $2\mathbb Z$. Jadi

$$
H^2(C^\bullet)=\mathbb Z/2\mathbb Z,
$$

dan semua $H^k$ di luar derajat $0,1,2$ nol.

Sesudah reduksi modulo $2$, rumus $\delta^1(a,b)=2a$ menjadi pemetaan nol.
Kedua diferensial kini nol, sehingga

$$
H^0(C^\bullet;\mathbb F_2)\cong\mathbb F_2,
\qquad
H^1(C^\bullet;\mathbb F_2)\cong\mathbb F_2^2,
\qquad
H^2(C^\bullet;\mathbb F_2)\cong\mathbb F_2.
$$

Di atas $\mathbb Q$, diferensial $\delta^1$ ber-rank satu. Karena itu

$$
\dim C^0-\dim C^1+\dim C^2=1-2+1=0,
$$

sedangkan kohomologinya berdimensi $1,1,0$, sehingga

$$
\dim H^0-\dim H^1+\dim H^2=1-1+0=0.
$$

Kedua karakteristik Euler sama. Namun dimensi rasional tidak melihat faktor
torsi $\mathbb Z/2\mathbb Z$ pada $H^2$. Perhitungan modulo $2$ juga
menunjukkan bahwa perubahan koefisien dapat memperbesar kernel diferensial;
ia bukan sekadar operasi mengganti simbol $\mathbb Z$ pada daftar jawaban
integral.
:::

## Soal 2 — koproduk tak hingga dan hasil kali kohomologi {#o012-d60-ca03-s02}

::: {.exercise #o012-d60-ca03-ex-002 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
Untuk $j\in\mathbb N_0$, ambil satu salinan $S_j^1$ dari lingkaran dan
tetapkan

$$
X=\bigsqcup_{j\in\mathbb N_0}S_j^1.
$$

1. Buktikan bahwa kompleks korantai singular $X$ adalah hasil kali kompleks
   korantai komponen-komponennya, lalu hitung $H^k(X;R)$ pada semua derajat.
2. Jelaskan mengapa jawabannya memakai hasil kali $\prod_jR$, bukan jumlah
   langsung $\bigoplus_jR$.
3. Definisikan $F\colon X\to X$ dengan mengirim $S_j^1$ ke $S_{j+1}^1$
   melalui pemetaan sudut identitas. Tentukan $F^*$ pada $H^0$ dan $H^1$
   di bawah identifikasi dengan barisan dalam $\prod_{j\ge0}R$.
:::

::: {.hint #o012-d60-ca03-hint-002 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
**Petunjuk.** Simpleks standar terhubung, sehingga satu simpleks singular
tidak dapat mengenai dua komponen koproduk. Fungsi pada gabungan saling lepas
adalah keluarga semua pembatasannya, tanpa syarat dukungan hingga. Untuk
$F^*$, lihat komponen domain ke-$j$ dan tentukan komponen kodomain mana yang
dibacanya.
:::

::: {.solution #o012-d60-ca03-sol-002 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
**Solusi.** Karena $\Delta^n$ terhubung dan setiap $S_j^1$ terbuka sekaligus
tertutup dalam $X$, citra setiap simpleks singular $\Delta^n\to X$ berada
seluruhnya dalam tepat satu komponen. Jadi himpunan simpleks singular adalah
gabungan saling lepas himpunan simpleks tiap komponen. Pembatasan fungsi
memberi isomorfisma kompleks

$$
C^\bullet(X;R)
\cong\prod_{j\ge0}C^\bullet(S_j^1;R),
$$

dan diferensial bertindak per koordinat. Dalam ZFC, kernel dan citra
diferensial produk dihitung per koordinat; untuk citra, praimaj dapat dipilih
serentak pada semua koordinat. Maka

$$
H^k(X;R)\cong\prod_{j\ge0}H^k(S_j^1;R)
\cong
\begin{cases}
\displaystyle\prod_{j\ge0}R,&k=0\text{ atau }k=1,\\
0,&k>1.
\end{cases}
$$

Unsur $\prod_jR$ boleh mempunyai koordinat taknol pada tak hingga banyak
$j$. Jumlah langsung hanya memuat keluarga berdukungan hingga. Misalnya,
$(1_R,1_R,\ldots)$ berada dalam hasil kali bila $1_R\ne0$, tetapi tidak dalam
jumlah langsung.

Pada komponen domain $S_j^1$, pemetaan $F$ mendarat di komponen
$S_{j+1}^1$. Karena kohomologi kontravarian, koordinat ke-$j$ dari tarik-balik
membaca koordinat ke-$(j+1)$ dari kelas semula. Jadi, baik pada $H^0$ maupun
$H^1$,

$$
F^*(a_0,a_1,a_2,\ldots)=(a_1,a_2,a_3,\ldots).
$$

Pergeseran ke kiri ini memperlihatkan arah kontravarian secara konkret.
:::

## Soal 3 — penghubung Lema Ular yang taktrivial {#o012-d60-ca03-s03}

::: {.exercise #o012-d60-ca03-ex-003 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
Pertimbangkan diagram komutatif dengan baris eksak pendek

$$
\begin{array}{ccccccccc}
0&\to&\mathbb Z&\xrightarrow{\times4}&\mathbb Z
&\xrightarrow{\pi_4}&\mathbb Z/4&\to&0\\
&&\downarrow{\scriptstyle\alpha=\times2}
&&\downarrow{\scriptstyle\beta=\operatorname{id}}
&&\downarrow{\scriptstyle\gamma=\pi_2}&&\\
0&\to&\mathbb Z&\xrightarrow{\times2}&\mathbb Z
&\xrightarrow{\pi_2}&\mathbb Z/2&\to&0,
\end{array}
$$

tempat $\gamma([x]_4)=[x]_2$.

1. Hitung keenam kernel dan kokernel dalam barisan Lema Ular.
2. Bangun pemetaan penghubung
   $\delta\colon\ker\gamma\to\operatorname{coker}\alpha$ dari pilihan
   pengangkatan dan tentukan nilainya pada generator.
3. Periksa secara eksplisit eksaknya barisan Ular pada keempat suku internal.
:::

::: {.hint #o012-d60-ca03-hint-003 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
**Petunjuk.** Generator $\ker\gamma$ adalah $[2]_4$. Angkat unsur itu ke
$2\in\mathbb Z$ pada baris atas, terapkan $\beta$, lalu angkat balik melalui
pemetaan $\times2$ pada baris bawah. Setelah itu barisan Ular menyederhana
menjadi satu peta di antara dua salinan $\mathbb Z/2$.
:::

::: {.solution #o012-d60-ca03-sol-003 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
**Solusi.** Pemetaan $\alpha=\times2$ dan $\beta=\operatorname{id}$
injektif, sedangkan $\gamma$ surjektif dengan kernel
$\{[0]_4,[2]_4\}\cong\mathbb Z/2$. Jadi

$$
\ker\alpha=0,
\quad\ker\beta=0,
\quad\ker\gamma\cong\mathbb Z/2,
$$

dan

$$
\operatorname{coker}\alpha\cong\mathbb Z/2,
\quad\operatorname{coker}\beta=0,
\quad\operatorname{coker}\gamma=0.
$$

Ambil $c=[2]_4\in\ker\gamma$. Pilih $b=2\in\mathbb Z$ dengan
$\pi_4(b)=c$. Karena $\beta$ identitas, $\beta(b)=2$. Pada baris bawah,
$2$ adalah citra $a'=1$ melalui pemetaan $\times2$. Definisi penghubung
memberi

$$
\delta([2]_4)=[1]
\in\mathbb Z/\alpha(\mathbb Z)
=\mathbb Z/2.
$$

Jika pengangkatan $b$ diganti dengan $2+4r$, unsur pada baris bawah yang
dipilih menjadi $a'=1+2r$. Kelasnya modulo
$\alpha(\mathbb Z)=2\mathbb Z$ tetap $[1]$. Jadi hasil itu tidak bergantung
pada pilihan pengangkatan.

Jadi $\delta$ mengirim generator ke generator dan merupakan isomorfisma.
Barisan Ular dalam contoh ini adalah

$$
0\longrightarrow0\longrightarrow\mathbb Z/2
\xrightarrow{\ \delta\ }\mathbb Z/2
\longrightarrow0\longrightarrow0.
$$

Eksak pada $\ker\beta=0$ bersifat langsung. Pada $\ker\gamma$, citra peta
sebelumnya nol dan sama dengan $\ker\delta$ karena $\delta$ injektif. Pada
$\operatorname{coker}\alpha$, citra $\delta$ adalah seluruh grup dan sama
dengan kernel peta menuju $\operatorname{coker}\beta=0$. Terakhir, pada
$\operatorname{coker}\beta=0$, citra peta masuk dan kernel peta keluar
sama-sama nol. Keempat posisi internal dengan demikian eksak.
:::

## Soal 4 — pasangan cakram–sfera dan kasus batas dua titik {#o012-d60-ca03-s04}

::: {.exercise #o012-d60-ca03-ex-004 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
Untuk setiap $n\ge1$, hitung $H^k(D^n,S^{n-1};\mathbb Z)$ pada semua derajat
dengan dua cara yang saling memeriksa:

1. gunakan pemetaan hasil bagi $q\colon D^n\to D^n/S^{n-1}\cong S^n$; dan
2. gunakan barisan eksak panjang pasangan.

Pada $n=1$, tuliskan secara eksplisit pemetaan
$H^0(D^1)\to H^0(S^0)$ dan identifikasi kokernelnya. Nyatakan arah tepat
pemetaan kohomologi yang diinduksi oleh $q$.
:::

::: {.hint #o012-d60-ca03-hint-004 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
**Petunjuk.** Teorema hasil bagi memakai kohomologi tereduksi sfera. Untuk
$n=1$, pembatasan fungsi konstan dari interval ke kedua titik batas adalah
pemetaan diagonal $\mathbb Z\to\mathbb Z^2$.
:::

::: {.solution #o012-d60-ca03-sol-004 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
**Solusi.** Pasangan $(D^n,S^{n-1})$ adalah pasangan CW yang baik, dan
pemetaan hasil bagi menginduksi, secara kontravarian,

$$
q^*\colon
\widetilde H^k(S^n;\mathbb Z)
\xrightarrow{\ \cong\ }
H^k(D^n,S^{n-1};\mathbb Z).
$$

Karena kohomologi tereduksi $S^n$ adalah $\mathbb Z$ tepat pada derajat $n$,

$$
H^k(D^n,S^{n-1};\mathbb Z)
\cong
\begin{cases}
\mathbb Z,&k=n,\\
0,&k\ne n.
\end{cases}
$$

Untuk $n\ge2$, $D^n$ dan $S^{n-1}$ terhubung, sehingga pemetaan pada $H^0$
adalah isomorfisma. Semua kohomologi positif cakram nol. Di sekitar derajat
$n-1$, barisan pasangan menjadi

$$
0\longrightarrow H^{n-1}(S^{n-1};\mathbb Z)\cong\mathbb Z
\xrightarrow{\partial}H^n(D^n,S^{n-1};\mathbb Z)
\longrightarrow0,
$$

jadi penghubung adalah isomorfisma dan hasilnya sama.

Jika $n=1$, batasnya $S^0=\{-1,1\}$ dan awal barisan ialah

$$
0\to H^0(D^1,S^0)\to\mathbb Z
\xrightarrow{\Delta}\mathbb Z^2
\xrightarrow{\partial}H^1(D^1,S^0)\to0,
$$

dengan $\Delta(a)=(a,a)$. Pemetaan diagonal injektif, sehingga grup relatif
derajat nol adalah nol. Pemetaan

$$
(u,v)\longmapsto v-u
$$

surjektif dan berkernel $\Delta(\mathbb Z)$; maka
$\operatorname{coker}\Delta\cong\mathbb Z$ dan
$H^1(D^1,S^0)\cong\mathbb Z$. Ini menutup kasus $n=1$ tanpa menyamakan
$H^0$ biasa dengan kohomologi tereduksi.
:::

## Soal 5 — kohomologi semua sfera dari Mayer–Vietoris {#o012-d60-ca03-s05}

::: {.exercise #o012-d60-ca03-ex-005 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
Untuk $n\ge1$, selimuti $S^n$ dengan dua lingkungan hemisfer terbuka
$U,V$. Keduanya kontraktil, sedangkan $U\cap V\simeq S^{n-1}$.

1. Turunkan isomorfisma reduksi
   $\widetilde H^{k-1}(S^{n-1};R)\cong\widetilde H^k(S^n;R)$.
2. Mulai dari $\widetilde H^0(S^0;R)\cong R$, hitung seluruh kohomologi
   tereduksi dan biasa $S^n$.
3. Periksa secara eksplisit mengapa argumen tetap benar untuk $n=1$, ketika
   irisan mempunyai dua komponen lintasan.
:::

::: {.hint #o012-d60-ca03-hint-005 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
**Petunjuk.** Dalam barisan Mayer–Vietoris tereduksi, semua suku milik $U$
dan $V$ lenyap. Pada $n=1$, jangan mengganti
$\widetilde H^0(S^0;R)$ dengan kohomologi biasa derajat nol.
:::

::: {.solution #o012-d60-ca03-sol-005 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R13"}
**Solusi.** Karena $U,V$ kontraktil dan irisannya takkosong, bagian tereduksi
barisan Mayer–Vietoris memberi, untuk $k\ge1$,

$$
0\longrightarrow\widetilde H^{k-1}(U\cap V;R)
\xrightarrow{\partial_{\mathrm{MV}}}\widetilde H^k(S^n;R)
\longrightarrow0.
$$

Invariansi homotopi $U\cap V\simeq S^{n-1}$ menghasilkan

$$
\widetilde H^{k-1}(S^{n-1};R)
\xrightarrow{\ \cong\ }\widetilde H^k(S^n;R).
$$

Untuk $k=n$, iterasi mencapai
$\widetilde H^0(S^0;R)\cong R$. Jika $k=0$, grup tereduksi nol karena
$S^n$ terhubung lintasan. Jika $0<k<n$, iterasi berakhir pada derajat nol
sfera berdimensi positif, yang juga nol karena keterhubungan lintasan. Jika
$k>n$, iterasi berakhir pada derajat positif $S^0$, yang nol. Jadi

$$
\widetilde H^k(S^n;R)
\cong
\begin{cases}
R,&k=n,\\
0,&k\ne n.
\end{cases}
$$

Karena $S^n$ terhubung lintasan untuk $n\ge1$,

$$
H^k(S^n;R)
\cong
\begin{cases}
R,&k=0\text{ atau }k=n,\\
0,&\text{selain itu}.
\end{cases}
$$

Pada $n=1$, irisan dua busur mempunyai tipe homotopi $S^0$. Walaupun
$H^0(S^0;R)\cong R^2$, hasil bagi oleh fungsi konstan adalah
$\widetilde H^0(S^0;R)\cong R$. Pemetaan penghubung mengidentifikasi modul
ini dengan $H^1(S^1;R)\cong R$. Jadi kasus dasar satu-dimensi justru
memerlukan versi tereduksi dan tercakup tanpa pengecualian tersembunyi.
:::

## Soal 6 — pembandingan korantai dan induksi Lema Lima {#o012-d60-ca03-s06}

::: {.exercise #o012-d60-ca03-ex-006 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R14" data-secondary-route-unit-ids="D60-R13"}
Untuk himpunan-$\Delta$ berdimensi hingga $X_\bullet$, pemetaan karakteristik
$\chi_x\colon\Delta^n\to|X_\bullet|$ menentukan restriksi

$$
\rho_X\colon C^\bullet_{\mathrm{sing}}(|X_\bullet|;R)
\longrightarrow C^\bullet_\Delta(X_\bullet;R).
$$

1. Tuliskan rumus $\rho_X$ dan buktikan bahwa ia pemetaan korantai.
2. Buktikan kealamiannya terhadap pemetaan himpunan-$\Delta$.
3. Dengan pasangan kerangka
   $(X_\bullet,\operatorname{sk}_{n-1}X_\bullet)$, perbandingan relatif,
   dan Lema Lima, buktikan bahwa $\rho_X$ menginduksi isomorfisma pada setiap
   kohomologi.
:::

::: {.hint #o012-d60-ca03-hint-006 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R14" data-secondary-route-unit-ids="D60-R13"}
**Petunjuk.** Evaluasikan korantai singular pada simpleks karakteristik dan
gunakan $\chi_x\circ\partial_i=\chi_{d_ix}$. Untuk induksi dimensi, ambil
lima suku barisan pasangan: kerangka, relatif, absolut, kerangka, relatif.
Empat peta selain peta absolut sudah diketahui merupakan isomorfisma.
:::

::: {.solution #o012-d60-ca03-sol-006 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R14" data-secondary-route-unit-ids="D60-R13"}
**Solusi.** Pada derajat $n$, definisikan

$$
(\rho_X\varphi)(x)=\varphi(\chi_x)
\qquad(x\in X_n).
$$

Karena muka simpleks karakteristik adalah simpleks karakteristik muka,

$$
\begin{aligned}
(\rho_X\delta_{\mathrm{sing}}\varphi)(x)
&=\sum_i(-1)^i\varphi(\chi_x\circ\partial_i)\\
&=\sum_i(-1)^i\varphi(\chi_{d_ix})
=(\delta_\Delta\rho_X\varphi)(x).
\end{aligned}
$$

Jadi $\rho_X$ pemetaan korantai. Jika
$f\colon X_\bullet\to Y_\bullet$, maka
$|f|\circ\chi_x=\chi_{f(x)}$. Untuk
$\varphi\in C^n_{\mathrm{sing}}(|Y|;R)$,

$$
(\rho_X|f|^*\varphi)(x)
=\varphi(|f|\chi_x)
=\varphi(\chi_{f(x)})
=(f^*\rho_Y\varphi)(x).
$$

Inilah kealamian $\rho_X|f|^*=f^*\rho_Y$.

Sekarang lakukan induksi pada dimensi $n$. Pada $n=0$, realisasi adalah ruang
diskret; kedua teori memberi $R^{X_0}$ pada derajat nol dan nol di atasnya,
serta $\rho^*$ identitas koordinat. Untuk langkah induksi, bandingkan barisan
eksak panjang pasangan kerangka pada teori singular dan simpleksial. Lima
suku yang mengapit peta absolut derajat $k$ adalah

$$
H^{k-1}(\operatorname{sk}_{n-1}X)
\to H^k(X,\operatorname{sk}_{n-1}X)
\to H^k(X)
\to H^k(\operatorname{sk}_{n-1}X)
\to H^{k+1}(X,\operatorname{sk}_{n-1}X).
$$

Dua peta vertikal pada suku kerangka adalah isomorfisma menurut hipotesis
induksi. Dua peta vertikal pada suku relatif adalah isomorfisma karena hasil
bagi kerangka merupakan baji sfera-$n$ dan pada setiap faktor pemetaan
pembanding mengirim kelas kanonik ke kelas kanonik. Kealamian membuat seluruh
diagram komutatif, termasuk pemetaan penghubung. Lema Lima karena itu memaksa
peta vertikal tengah

$$
\rho_X^*\colon H^k_{\mathrm{sing}}(|X|;R)
\longrightarrow H^k_\Delta(X;R)
$$

menjadi isomorfisma. Ini berlaku pada semua $k$, sehingga induksi selesai.
:::

## Soal 7 — paritas dan teorema sfera berbulu {#o012-d60-ca03-s07}

::: {.exercise #o012-d60-ca03-ex-007 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R14"}
Rekonstruksi kedua arah teorema sfera berbulu.

1. Andaikan $S^n$ mempunyai medan vektor tangen kontinu yang tidak pernah
   nol. Normalisasikan medan itu dan bangun homotopi dari identitas
   $S^n\to S^n$ ke peta antipodal.
2. Gunakan derajat untuk membuktikan bahwa $n$ harus ganjil.
3. Untuk $n=2k-1$, bangun secara eksplisit medan tangen satuan yang tidak
   pernah nol, lalu periksa tangensi dan normanya.
4. Jelaskan secara terpisah apa yang dikatakan argumen pada $S^0$.
:::

::: {.hint #o012-d60-ca03-hint-007 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R14"}
**Petunjuk.** Setelah normalisasi, $x$ dan $v(x)$ adalah dua vektor satuan
ortogonal. Putar yang pertama menuju negatifnya di bidang yang mereka
rentang. Untuk arah sebaliknya, kelompokkan koordinat $\mathbb R^{2k}$ dalam
pasangan dan lakukan rotasi seperempat putaran pada setiap pasangan.
:::

::: {.solution #o012-d60-ca03-sol-007 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R14"}
**Solusi.** Bagi medan yang tidak pernah nol dengan panjangnya. Kita boleh
mengandaikan

$$
\lVert v(x)\rVert=1,
\qquad x\cdot v(x)=0.
$$

Definisikan

$$
H(t,x)=\cos(\pi t)x+\sin(\pi t)v(x).
$$

Ortogonalitas memberi

$$
\lVert H(t,x)\rVert^2
=\cos^2(\pi t)+\sin^2(\pi t)=1,
$$

jadi $H$ bernilai di $S^n$. Nilai ujungnya adalah
$H(0,x)=x$ dan $H(1,x)=-x$. Maka identitas homotop dengan peta antipodal.
Derajat bersifat invarian terhadap homotopi, sedangkan

$$
\operatorname{Deg}(\operatorname{id}_{S^n})=1,
\qquad
\operatorname{Deg}(-\operatorname{id}_{S^n})=(-1)^{n+1}.
$$

Karena kedua derajat harus sama, $(-1)^{n+1}=1$, sehingga $n$ ganjil.

Sebaliknya, jika $n=2k-1$, untuk
$x\in S^{2k-1}\subset\mathbb R^{2k}$ tetapkan

$$
v(x_1,x_2,\ldots,x_{2k-1},x_{2k})
=(-x_2,x_1,\ldots,-x_{2k},x_{2k-1}).
$$

Rumus itu linear dan karenanya kontinu. Pada setiap pasangan koordinat,

$$
(x_{2j-1},x_{2j})\cdot(-x_{2j},x_{2j-1})=0,
$$

sehingga $x\cdot v(x)=0$ dan $v(x)$ tangen. Selain itu,

$$
\lVert v(x)\rVert^2
=\sum_{j=1}^k(x_{2j-1}^2+x_{2j}^2)
=\lVert x\rVert^2=1.
$$

Jadi medan itu tidak pernah nol. Pada $S^0$, setiap ruang singgung
berdimensi nol dan hanya mempunyai vektor nol. Sisi derajat juga memberi
kontradiksi, karena kohomologi tereduksi membuat
$\operatorname{Deg}(-\operatorname{id}_{S^0})=-1$, sedangkan identitas
berderajat $1$.
:::

## Soal 8 — ketika invarian aditif belum cukup {#o012-d60-ca03-s08}

::: {.exercise #o012-d60-ca03-ex-008 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R14" data-secondary-route-unit-ids="D60-R13,D60-R05,D60-R12"}
Bandingkan

$$
X=T^2
\qquad\text{dan}\qquad
Y=S^1\vee S^1\vee S^2.
$$

Gunakan struktur CW dengan satu sel-$0$, dua sel-$1$, dan satu sel-$2$ pada
masing-masing ruang.

1. Hitung $\pi_1(X)$ dan $\pi_1(Y)$ dengan Seifert–van Kampen.
2. Hitung seluruh homologi integral kedua ruang dari pemetaan batas seluler.
3. Hitung seluruh kohomologi integral aditif dan karakteristik Eulernya.
4. Putuskan apakah $X$ dan $Y$ dapat ekuivalen homotopi, lalu jelaskan secara
   tepat mengapa sebagian invarian di atas gagal membedakannya.
:::

::: {.hint #o012-d60-ca03-hint-008 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R14" data-secondary-route-unit-ids="D60-R13,D60-R05,D60-R12"}
**Petunjuk.** Sel-$2$ torus dilekatkan sepanjang komutator
$aba^{-1}b^{-1}$, sedangkan sel-$2$ pada $Y$ dilekatkan secara konstan.
Jumlah eksponen $a$ dan $b$ dalam komutator sama-sama nol, jadi kedua matriks
batas seluler dapat berimpit walaupun relasi grup fundamentalnya berbeda.
:::

::: {.solution #o012-d60-ca03-sol-008 data-origin="edition-original" data-assessment-id="D60-CA03" data-edition-unit-id="O012-ORIG-CA03" data-course-route-unit-id="D60-R14" data-secondary-route-unit-ids="D60-R13,D60-R05,D60-R12"}
**Solusi.** Kerangka-$1$ kedua ruang adalah $S^1\vee S^1$, sehingga sebelum
sel-$2$ dilekatkan grup fundamentalnya adalah grup bebas $F(a,b)$. Pada torus,
peta pelekatan memberi relasi komutator:

$$
\pi_1(X)
\cong\langle a,b\mid aba^{-1}b^{-1}=1\rangle
\cong\mathbb Z^2.
$$

Pada $Y$, sel-$2$ membentuk faktor baji $S^2$ dan peta pelekatannya konstan,
sehingga tidak menambahkan relasi. Maka

$$
\pi_1(Y)\cong F(a,b).
$$

Kompleks rantai seluler masing-masing mempunyai bentuk

$$
0\longrightarrow\mathbb Z
\xrightarrow{d_2}\mathbb Z^2
\xrightarrow{d_1}\mathbb Z\longrightarrow0.
$$

Karena kedua ujung setiap sel-$1$ melekat pada satu sel-$0$, $d_1=0$.
Untuk torus, koefisien $d_2$ adalah jumlah eksponen generator pada kata
pelekatan. Dalam $aba^{-1}b^{-1}$, jumlah eksponen $a$ dan $b$ keduanya nol,
jadi $d_2=0$. Pada $Y$, peta pelekatan konstan juga memberi $d_2=0$. Oleh
karena itu kedua ruang mempunyai homologi yang sama:

$$
H_k(X;\mathbb Z)\cong H_k(Y;\mathbb Z)
\cong
\begin{cases}
\mathbb Z,&k=0,2,\\
\mathbb Z^2,&k=1,\\
0,&\text{selain itu}.
\end{cases}
$$

Mendualkan kompleks seluler menghasilkan diferensial korantai nol yang sama.
Karena semua grup bebas, tidak muncul suku torsi tambahan. Jadi secara aditif

$$
H^k(X;\mathbb Z)\cong H^k(Y;\mathbb Z)
\cong
\begin{cases}
\mathbb Z,&k=0,2,\\
\mathbb Z^2,&k=1,\\
0,&\text{selain itu}.
\end{cases}
$$

Kedua struktur CW juga memberi

$$
\chi=1-2+1=0,
$$

sesuai jumlah berganti tanda rank homologi atau kohomologi.

Namun $\pi_1(X)=\mathbb Z^2$ abelian, sedangkan $\pi_1(Y)=F(a,b)$
nonabelian. Ekuivalensi homotopi harus menginduksi isomorfisma grup
fundamental, sehingga $X$ dan $Y$ tidak ekuivalen homotopi. Contoh ini
menunjukkan batas invarian **aditif**: grup homologi, grup kohomologi sebagai
grup bergradasi, dan karakteristik Euler semuanya sama, tetapi data perkalian
atau nonkomutativitas yang masih terlihat oleh $\pi_1$ telah hilang setelah
abelianisasi dan pengambilan rank.
:::

## Peta cakupan asesmen {#o012-d60-ca03-coverage}

| Soal | Route utama | Route prasyarat | Kompetensi yang diperiksa |
|---:|:---:|:---:|---|
| 1 | D60-R13 | — | kompleks korantai, kernel/citra, torsi, perubahan koefisien, dan Euler |
| 2 | D60-R13 | — | koproduk tak hingga, hasil kali kohomologi, dan tarik-balik kontravarian |
| 3 | D60-R13 | — | konstruksi penghubung Lema Ular dan eksak pada empat suku internal |
| 4 | D60-R13 | — | kohomologi relatif/tereduksi pasangan cakram–sfera, termasuk $n=1$ |
| 5 | D60-R13 | — | kohomologi sfera melalui Mayer–Vietoris, termasuk irisan $S^0$ |
| 6 | D60-R14 | D60-R13 | pembandingan korantai, kealamian, pasangan kerangka, dan Lema Lima |
| 7 | D60-R14 | — | derajat, peta antipodal, paritas, dan teorema sfera berbulu |
| 8 | D60-R14 | D60-R13, D60-R05, D60-R12 | perbandingan $\pi_1$, homologi, kohomologi, dan Euler pada dua ruang |

Asesmen selesai tepat pada delapan soal, delapan petunjuk, dan delapan solusi
lengkap. Setiap objek `exercise`, `hint`, dan `solution` memiliki pengenal
stabil `o012-d60-ca03-ex/hint/sol-001` sampai `008`, serta setiap bagian dan
tabel cakupan memiliki pengenal stabil tersendiri.
