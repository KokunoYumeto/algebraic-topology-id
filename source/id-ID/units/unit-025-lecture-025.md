---
title: "Topologi Aljabar"
subtitle: "Unit 25: Kohomologi Relatif, Lema Lima, dan Karakteristik Euler"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l25-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 5370--5611 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L5370-L5611)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang aktif itu terdiri atas 242 baris fisik. Dengan normalisasi LF dan
terminator LF penutup dipertahankan, ukurannya 12.732 byte dan SHA-256-nya
adalah
`d05781ae58b1b6fd6174d030e52ca9ee6a08048be96f7c103e5be8de473b60b0`.
Baris 5612, yang memulai Kuliah 26, tidak termasuk. Materi sumber dan adaptasi
Indonesia ini tersedia di bawah
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Rentang sumber memuat satu penanda kuliah, tiga definisi, dua lema, dua
proposisi, enam contoh, dua lingkungan bukti, satu enumerasi dua butir, delapan
catatan pinggir, dua diagram Xy-pic, satu label, dan satu rujukan silang. Tidak
ada latihan formal sumber, pertanyaan formal, gambar eksternal, sitasi,
`input`, atau `include`.

Edisi memindahkan kedelapan catatan pinggir ke urutan bacaan utama dan
menggambar ulang kedua diagram posisional sebagai data barisan dan morfisma
yang semantik serta dapat mengalir ulang. Edisi juga melengkapi bukti lema
kerangka, membangun dan memeriksa barisan eksak panjang kohomologi relatif,
menyelesaikan separuh injektivitas Lema Lima yang ditinggalkan sebagai
latihan, serta memperbaiki pembuktian karakteristik Euler dengan argumen
rank--nulitas yang bertipe benar. Kekeliruan deterministik dalam proyeksi,
tipe unsur, indeks, citra diferensial, dan rumus penutup diperbaiki serta
dicatat tepat di tempatnya.

Enam pemeriksaan penguasaan, enam petunjuk, semua penutupan bukti edisi, dan
enam solusi lengkap merupakan materi asli edisi dan tersedia di bawah CC BY
4.0. Edisi ini bersifat independen; edisi ini tidak disponsori, didukung,
disahkan, ataupun diberi status resmi oleh David Michael Roberts atau
institusinya. Produksi edisi ini dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra**. Pernyataan ini menambah transparansi proses dan tidak mengurangi
kredit penulis sumber ataupun kredit kontributor manusia.

# Kuliah 25 {#o012-rbt-l25}

## Kohomologi relatif dan kerangka atas {#o012-rbt-l25-s01}

Kohomologi kompleks korantai simpleksial relatif ternyata sangat penting. Ia
juga memberi keluwesan tambahan dalam mendefinisikan kohomologi sebuah
himpunan-$\Delta$. Kompleks biasa $C^\bullet(X_\bullet;R)$ diperoleh kembali
dengan mengambil $A_\bullet=\varnothing$; dengan kata lain, kompleks itu
adalah $C^\bullet(X_\bullet,\varnothing;R)$.

::: {.definition #o012-rbt-l25-def-001}
**Definisi 25.1 (kohomologi relatif).** Untuk pasangan himpunan-$\Delta$
$(X_\bullet,A_\bullet)$, **kohomologi relatif** pasangan itu ialah

$$
H^k(X_\bullet,A_\bullet;R)
:=H^k\!\left(C^\bullet(X_\bullet,A_\bullet;R)\right).
$$
:::

::: {.example #o012-rbt-l25-exa-001 data-source-label="eg:dim_minus_one_skeleton_rel_cochains"}
**Contoh 25.1 (relatif terhadap kerangka satu dimensi lebih rendah).**
Misalkan $X_\bullet$ merupakan himpunan-$\Delta$ berdimensi hingga $n$.
Pasangan

$$
(X_\bullet,\operatorname{sk}_{n-1}X_\bullet)
$$

memiliki kompleks korantai relatif

$$
0\longrightarrow
C^0(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)
\longrightarrow\cdots\longrightarrow
C^{n-1}(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)
\longrightarrow
C^n(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)
\longrightarrow0.
$$

Untuk $k<n$ berlaku
$\operatorname{sk}_{n-1}X_k=X_k$. Karena itu,

$$
C^k(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)
=\ker\!\left(\operatorname{id}_{R^{X_k}}\right)=0.
$$

Sebaliknya,
$\operatorname{sk}_{n-1}X_n=\varnothing$, sehingga

$$
\begin{aligned}
C^n(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)
&=\ker\!\left(R^{X_n}\longrightarrow R^\varnothing=0\right)\\
&=R^{X_n}.
\end{aligned}
$$

Jadi semua modul kompleks itu nol kecuali modul pada posisi $n$, yang
merupakan modul fungsi $X_n\to R$. Akibatnya,

$$
H^k(X_\bullet,\operatorname{sk}_{n-1}X_\bullet;R)
=
\begin{cases}
0,&k\ne n,\\
R^{X_n},&k=n.
\end{cases}
$$
:::

::: {.aside #o012-rbt-l25-aside-001}
**Notasi aljabar homologis.** Kompleks yang hanya memuat $R^{X_n}$ pada
derajat $n$ sering ditulis $R^{X_n}[n]$.
:::

::: {.source-audit #o012-rbt-l25-audit-001}
**Audit sumber 25.1.** Tampilan pada Notes.tex baris 5383--5385 mulai dari
$C^1$, padahal argumennya mencakup derajat $0$. Edisi menampilkan rentang
penuh $C^0$ sampai $C^n$. Perbaikan ini tidak mengubah hasil: semua suku
berderajat kurang dari $n$, termasuk suku derajat $0$, memang nol.
:::

::: {.lemma #o012-rbt-l25-lem-001}
**Lema 25.1 (kohomologi tidak melihat simpleks di atas derajat yang
diperlukan).** Jika $k<n$, maka

$$
H^k(\operatorname{sk}_nX_\bullet;R)
\cong H^k(X_\bullet;R).
$$
:::

::: {.proof #o012-rbt-l25-proof-001 data-origin="edition-proof-closure"}
**Bukti.** Kohomologi pada derajat $k$ ditentukan oleh bagian tiga-suku

$$
C^{k-1}\xrightarrow{\delta_{k-1}}C^k
\xrightarrow{\delta_k}C^{k+1}.
$$

Karena $k<n$, kita mempunyai $k+1\le n$. Himpunan-$\Delta$
$\operatorname{sk}_nX_\bullet$ sama dengan $X_\bullet$ pada setiap derajat
$j\le n$, dan semua *face map* di antara derajat-derajat tersebut juga sama.
Maka ketiga modul korantai di atas dan kedua diferensial yang menghubungkannya
sama untuk $\operatorname{sk}_nX_\bullet$ dan $X_\bullet$. Kernel, citra, dan
hasil bagi yang mendefinisikan $H^k$ pun sama. Untuk $k=0$, suku derajat
$-1$ dipahami sebagai nol, sehingga argumen yang sama tetap berlaku. Isomorfisma
yang diperoleh adalah isomorfisma alami yang diinduksi oleh inklusi kerangka.
:::

Dengan demikian, setiap modul kohomologi suatu himpunan-$\Delta$ dapat
dihitung sebagai modul kohomologi himpunan-$\Delta$ berdimensi hingga, meski
dimensi kerangka yang dibutuhkan bertambah bersama derajat kohomologinya.

::: {.aside #o012-rbt-l25-aside-002}
**Aproksimasi yang lebih halus.** Ada hasil lebih canggih yang, dalam arti
yang presisi, mengaproksimasi modul-modul kohomologi dengan kohomologi
himpunan-$\Delta$ yang benar-benar **hingga**, bukan hanya berdimensi hingga.
Hasil itu berada di luar cakupan kuliah ini.
:::

## Barisan eksak panjang kohomologi relatif {#o012-rbt-l25-s02}

::: {.proposition #o012-rbt-l25-prop-001}
**Proposisi 25.1 (barisan eksak panjang pasangan).** Untuk pasangan
himpunan-$\Delta$ $(X_\bullet,A_\bullet)$ terdapat barisan eksak panjang
modul-$R$

$$
0\longrightarrow H^0(X_\bullet,A_\bullet;R)
\longrightarrow H^0(X_\bullet;R)
\longrightarrow H^0(A_\bullet;R)
\xrightarrow{\partial^0}H^1(X_\bullet,A_\bullet;R)
\longrightarrow\cdots,
$$

dan, pada setiap derajat $k$,

$$
\cdots\longrightarrow H^{k-1}(A_\bullet;R)
\xrightarrow{\partial^{k-1}}H^k(X_\bullet,A_\bullet;R)
\longrightarrow H^k(X_\bullet;R)
\longrightarrow H^k(A_\bullet;R)
\xrightarrow{\partial^k}\cdots.
$$
:::

::: {.figure #o012-rbt-l25-fig-001}
**Data semantik Diagram 25.1.** Urutan objek adalah
`kohomologi relatif -> kohomologi X -> kohomologi A -> kohomologi relatif
pada derajat berikutnya`. Dua panah pertama diinduksi, berturut-turut, oleh
inklusi kompleks relatif dan restriksi $A_\bullet\hookrightarrow X_\bullet$;
panah ketiga adalah morfisma penghubung $\partial^k$. Pola ini diulang untuk
setiap $k$. Uraian ini, bersama dua fragmen barisan di atas, merupakan
penggambaran ulang diagram Xy-pic sumber tanpa ketergantungan pada posisi,
warna, atau arah baca zig-zag.
:::

::: {.proof #o012-rbt-l25-proof-002 data-origin="edition-proof-closure"}
**Bukti.** Unit 24 membangun barisan eksak pendek kompleks korantai

$$
0\longrightarrow C^\bullet(X_\bullet,A_\bullet;R)
\xrightarrow{j}C^\bullet(X_\bullet;R)
\xrightarrow{i^*}C^\bullet(A_\bullet;R)
\longrightarrow0,
$$

dengan $j$ inklusi kernel dan $i^*$ restriksi. Barisan eksak panjang dari
barisan eksak pendek itu memberi barisan yang dinyatakan. Agar konstruksinya
eksplisit, ambil kelas $[a]\in H^k(A_\bullet;R)$ dan wakili dengan kosiklus
$a\in C^k(A_\bullet;R)$. Pilih pengangkatan
$x\in C^k(X_\bullet;R)$ dengan $i^*x=a$. Karena

$$
i^*(\delta x)=\delta(i^*x)=\delta a=0,
$$

unsur $\delta x$ berada dalam kompleks relatif. Definisikan

$$
\partial^k[a]:=[\delta x]
\in H^{k+1}(X_\bullet,A_\bullet;R).
$$

Jika $x$ diganti oleh pengangkatan lain, selisihnya berada dalam kompleks
relatif dan mengubah $\delta x$ hanya dengan suatu kobatas relatif. Jika
$a$ diganti oleh wakil sekohomologi $a+\delta b$, angkat $b$ dan ubah $x$
dengan kobatas pengangkatan itu; kelas $[\delta x]$ tetap sama. Jadi
$\partial^k$ terdefinisi baik dan linear.

Eksaknya dapat diperiksa pada tiga jenis suku yang berulang. Pertama, kelas
relatif yang menjadi nol dalam $H^k(X)$ diwakili oleh
$r=\delta x$; restriksi $i^*x$ adalah kosiklus pada $A$ dan
$\partial^{k-1}[i^*x]=[r]$. Kedua, jika kelas $[x]\in H^k(X)$ membatasi
menjadi nol pada $A$, tulis $i^*x=\delta b$, angkat $b$ ke $\widetilde b$,
dan perhatikan bahwa $x-\delta\widetilde b$ adalah kosiklus relatif yang
mewakili $[x]$. Ketiga, $[a]\in H^k(A)$ memiliki
$\partial^k[a]=0$ tepat ketika, setelah mengubah pengangkatan $x$ dengan
suatu korantai relatif, diperoleh kosiklus pada $X$ yang membatasi menjadi
$a$. Ini sama dengan mengatakan bahwa $[a]$ berada dalam citra
$H^k(X)\to H^k(A)$. Pemeriksaan pada suku awal derajat $0$ serupa dengan
kompleks yang nol pada derajat negatif. Kealamian mengikuti dengan memetakan
pilihan pengangkatan melalui morfisma pasangan; ketakbergantungan dari pilihan
membuat bujur sangkar penghubung komutatif.
:::

::: {.source-audit #o012-rbt-l25-audit-002}
**Audit sumber 25.2.** Notes.tex baris 5408--5419 menyatakan proposisi tanpa
bukti dan menyajikan barisannya sebagai diagram zig-zag posisional. Edisi
menyediakan konstruksi penghubung, ketakbergantungan pilihan, tiga pemeriksaan
eksak yang berulang, kealamian, dan representasi semantik yang dapat mengalir
ulang.
:::

::: {.example #o012-rbt-l25-exa-002}
**Contoh 25.2 (simpleks relatif terhadap batasnya).** Pertimbangkan pasangan

$$
(\Delta[n],\partial\Delta[n]).
$$

Ini merupakan kasus khusus [Contoh 25.1](#o012-rbt-l25-exa-001), sebab
$\partial\Delta[n]=\operatorname{sk}_{n-1}\Delta[n]$. Karena $\Delta[n]$
memiliki tepat satu simpleks berdimensi $n$,

$$
H^k(\Delta[n],\partial\Delta[n];R)
=
\begin{cases}
0,&k\ne n,\\
R,&k=n.
\end{cases}
$$

Untuk $k<n-1$, barisan eksak panjang terpecah menjadi potongan

$$
0\longrightarrow H^k(\Delta[n];R)
\xrightarrow{\ \cong\ }H^k(\partial\Delta[n];R)
\longrightarrow0,
$$

sesuai dengan hasil umum tentang kerangka di atas. Di sekitar derajat atas,
potongannya ialah

$$
0\longrightarrow H^{n-1}(\Delta[n];R)
\longrightarrow H^{n-1}(\partial\Delta[n];R)
\longrightarrow R
\longrightarrow H^n(\Delta[n];R)
\longrightarrow0.
$$

Khususnya, $H^n(\Delta[n];R)$ merupakan hasil bagi modul berperingkat satu
$R$, sehingga modul itu tidak dapat lebih besar daripada $R$ dalam pengertian
ini.
:::

::: {.aside #o012-rbt-l25-aside-003}
**Dua catatan tentang contoh.** Identitas
$\partial\Delta[n]=\operatorname{sk}_{n-1}\Delta[n]$ menjadikan contoh ini
kasus khusus langsung dari Contoh 25.1. Sebenarnya
$H^n(\Delta[n];R)=0$, tetapi pada titik sumber ini fakta tersebut belum
dibuktikan, sehingga edisi tidak memakainya untuk memperpendek barisan.
:::

Kohomologi relatif dapat dibayangkan sebagai kohomologi suatu “hasil bagi
virtual” oleh sub-himpunan-$\Delta$. Jika pasangannya
$(X_\bullet,\{x\})$ dengan $x\in X_0$, kita dapat mengambil hasil bagi yang
meruntuhkan $\{x\}$ menjadi satu titik tanpa mengubah himpunan yang
mendasarinya. Namun kohomologi relatif benar-benar berbeda dari kohomologi
biasa: kompleks relatif tetap mengingat bahwa titik itu telah dipilih. Karena
itu, gambaran hasil bagi naif tersebut memerlukan penafsiran yang lebih halus.

::: {.example #o012-rbt-l25-exa-003}
**Contoh 25.3 (dua titik dan satu titik dasar).** Ambil himpunan-$\Delta$
sangat sederhana $\partial\Delta[1]$, yang memiliki dua simpleks-$0$,
$x_0$ dan $x_1$, dan tidak memiliki simpleks pada derajat lain. Untuk pasangan
$(\partial\Delta[1],\{x_0\})$, satu-satunya modul relatif yang taknol ialah

$$
\begin{aligned}
C^0(\partial\Delta[1],\{x_0\};R)
&=\ker\!\left(
R^{\{x_0,x_1\}}=R^2
\xrightarrow{\ \rho_{x_0}\ }
R^{\{x_0\}}=R\right)\\
&=\{(0,a_1):a_1\in R\}\cong R,
\end{aligned}
$$

dengan $\rho_{x_0}(a_0,a_1)=a_0$. Maka

$$
H^0(\partial\Delta[1],\{x_0\};R)=R,
$$

sedangkan semua $H^k$ lainnya nol. Sebagai perbandingan,
$H^0(\partial\Delta[1];R)=R^2$.
:::

::: {.source-audit #o012-rbt-l25-audit-003}
**Audit sumber 25.3.** Notes.tex baris 5449 menamai restriksi ke
$\{x_0\}$ sebagai $\operatorname{pr}_2$. Nama itu bergantung pada urutan
koordinat dan, untuk urutan tertulis $(x_0,x_1)$, biasanya berarti proyeksi
yang salah. Edisi memakai pemetaan takambigu
$\rho_{x_0}(a_0,a_1)=a_0$ dan menuliskan kernelnya secara eksplisit.
:::

Secara lebih umum, jika himpunan-$\Delta$ berdimensi nol memiliki $n+1$
simpleks-$0$ dan satu titik dasar yang dipilih, kohomologi relatifnya adalah
modul-$R$ bebas berperingkat $n$. Jadi kohomologi itu menghitung banyaknya
titik **selain** titik dasar yang ditentukan. Kasus ini cukup sering muncul
untuk diberi nama tersendiri: himpunan-$\Delta$ dengan satu simpleks-$0$ yang
ditentukan disebut himpunan-$\Delta$ **bertitik dasar**.

::: {.definition #o012-rbt-l25-def-002}
**Definisi 25.2 (kohomologi tereduksi).** Untuk himpunan-$\Delta$ bertitik
dasar $(X_\bullet,x)$, **kohomologi tereduksi** ialah kohomologi relatif

$$
H^k(X_\bullet,x;R).
$$
:::

::: {.example #o012-rbt-l25-exa-004}
**Contoh 25.4 (titik tebal).** Definisikan himpunan-$\Delta$
$Pt_\bullet$ dengan $Pt_n=\{\ast\}$ untuk semua $n\ge0$, dan semua *face
map* adalah fungsi identitas. Maka
$C^n(Pt_\bullet;R)=R$ untuk setiap $n$.

Anggap unsur $g\in R$ sebagai fungsi $\{\ast\}\to R$. Prapengomposisian
dengan $d_i=\operatorname{id}_{\{\ast\}}$ adalah identitas pada $R$, sehingga

$$
g\stackrel{\delta_n}{\longmapsto}
\sum_{i=0}^{n+1}(-1)^i g
=
\begin{cases}
0,&n\text{ genap},\\
g,&n\text{ ganjil}.
\end{cases}
$$

Kompleksnya ialah

$$
0\longrightarrow R\xrightarrow{0}R\xrightarrow{\operatorname{id}}R
\xrightarrow{0}R\xrightarrow{\operatorname{id}}R\longrightarrow\cdots.
$$

Jadi $H^0(Pt_\bullet;R)=R$, sedangkan
$H^k(Pt_\bullet;R)=0$ untuk semua $k>0$. Himpunan-$\Delta$ ini memiliki titik
dasar kanonik, dan kompleks relatif terhadap titik itu memiliki kohomologi
nol pada setiap derajat:

$$
H^k(Pt_\bullet,\ast;R)=0\qquad\text{untuk semua }k.
$$

Memang, kompleks relatifnya nol pada derajat $0$ dan sama dengan $R$ pada
setiap derajat positif; diferensial positif tetap bergantian antara identitas
dan nol. Karena itu setiap kosiklus relatif merupakan kobatas relatif.
:::

::: {.aside #o012-rbt-l25-aside-004}
**Mengapa disebut tebal?** $Pt_\bullet$ berdimensi takhingga: ia mempunyai
satu simpleks-$n$ untuk setiap $n\in\mathbb N$. Ia dapat dipandang sebagai
sejenis titik tebal berdimensi takhingga, atau analog kombinatorial dari
“ruang” kontraktibel, meski kita belum mempunyai gagasan deformasi kontinu
untuk himpunan-$\Delta$. Bahkan, analoginya lebih tepat disebut aljabar:
himpunan-$\Delta$ menyediakan kompleks sebagai model aljabar ruang yang lebih
sederhana.
:::

Kita dapat mendefinisikan analog bagi sebuah pemetaan kompleks yang merupakan
ekuivalensi homotopi lemah.

::: {.definition #o012-rbt-l25-def-003}
**Definisi 25.3 (kuasi-isomorfisma).** Morfisma kompleks
$f\colon A_\bullet\to B_\bullet$ disebut **kuasi-isomorfisma** jika

$$
H^k(f)\colon H^k(A_\bullet)\longrightarrow H^k(B_\bullet)
$$

merupakan isomorfisma untuk setiap $k$.
:::

::: {.example #o012-rbt-l25-exa-005}
**Contoh 25.5.** Inklusi
$\operatorname{sk}_0Pt_\bullet\hookrightarrow Pt_\bullet$ menginduksi
morfisma korantai kontravarian

$$
C^\bullet(Pt_\bullet;R)
\longrightarrow C^\bullet(\operatorname{sk}_0Pt_\bullet;R).
$$

Morfisma ini merupakan kuasi-isomorfisma. Kompleks sumbernya taknol pada
setiap posisi taknegatif, sedangkan kompleks sasarannya terkonsentrasi pada
satu posisi; tetapi keduanya mempunyai $H^0\cong R$ dan kohomologi nol pada
semua derajat positif, dan pemetaan terinduksi pada $H^0$ adalah identitas.
:::

## Lema Lima {#o012-rbt-l25-s03}

Kita hanya memerlukan satu lema lagi dari aljabar homologis yang sangat
berguna dalam praktik.

::: {.aside #o012-rbt-l25-aside-005}
**Tentang nama.** Kali ini, tidak seperti Lema Ular, lema tersebut tidak
dinamai menurut seekor hewan.
:::

::: {.lemma #o012-rbt-l25-lem-002}
**Lema 25.2 (Lema Lima).** Misalkan dua baris berikut eksak:

$$
A\xrightarrow{f}B\xrightarrow{g}C\xrightarrow{h}D\xrightarrow{k}E,
$$

$$
A'\xrightarrow{f'}B'\xrightarrow{g'}C'\xrightarrow{h'}D'
\xrightarrow{k'}E'.
$$

Misalkan pula terdapat morfisma vertikal

$$
\alpha\colon A\to A',\quad
\beta\colon B\to B',\quad
\gamma\colon C\to C',\quad
\delta\colon D\to D',\quad
\varepsilon\colon E\to E'
$$

yang membuat semua bujur sangkar komutatif. Jika $\alpha$ surjektif,
$\beta$ dan $\delta$ merupakan isomorfisma, serta $\varepsilon$ injektif,
maka $\gamma$ merupakan isomorfisma.
:::

::: {.figure #o012-rbt-l25-fig-002}
**Data semantik Diagram 25.2.** Diagram sumber terdiri atas dua baris eksak
yang ditulis dalam pernyataan lema, dengan lima morfisma vertikal berurutan
$\alpha,\beta,\gamma,\delta,\varepsilon$. Komutativitas berarti

$$
\beta f=f'\alpha,\qquad
\gamma g=g'\beta,\qquad
\delta h=h'\gamma,\qquad
\varepsilon k=k'\delta.
$$

Daftar objek, panah, dan persamaan ini menggambar ulang diagram Xy-pic secara
semantik. Ia tetap lengkap ketika baris matematika mengalir ulang atau dibaca
secara linear oleh teknologi bantu.
:::

::: {.proof #o012-rbt-l25-proof-003 data-origin="source-proof-completed-by-edition"}
**Bukti.** Kita membagi pengejaran diagram menjadi surjektivitas dan
injektivitas. Masing-masing memakai separuh hipotesis.

1. Andaikan $\varepsilon$ injektif dan $\beta,\delta$ surjektif. Ambil
   $c'\in C'$. Karena $\delta$ surjektif, pilih $d\in D$ sedemikian sehingga
   $\delta(d)=h'(c')$. Komutativitas dan eksaknya baris bawah memberi

   $$
   \varepsilon(k(d))=k'(\delta(d))=k'(h'(c'))=0.
   $$

   Karena $\varepsilon$ injektif, $k(d)=0$. Eksaknya baris atas memberi
   $d=h(c)$ untuk suatu $c\in C$. Sekarang

   $$
   \begin{aligned}
   h'(c'-\gamma(c))
   &=h'(c')-h'(\gamma(c))\\
   &=\delta(d)-\delta(h(c))=0.
   \end{aligned}
   $$

   Oleh eksaknya baris bawah, ada $b'\in B'$ dengan
   $c'-\gamma(c)=g'(b')$. Karena $\beta$ surjektif, tulis
   $b'=\beta(b)$ untuk suatu $b\in B$. Maka

   $$
   c'-\gamma(c)=g'(\beta(b))=\gamma(g(b)),
   $$

   sehingga $c'=\gamma(c+g(b))$. Jadi $\gamma$ surjektif.

2. Andaikan $\alpha$ surjektif dan $\beta,\delta$ injektif. Ambil
   $c\in C$ dengan $\gamma(c)=0$. Dari komutativitas,

   $$
   \delta(h(c))=h'(\gamma(c))=0.
   $$

   Injektivitas $\delta$ memberi $h(c)=0$. Karena baris atas eksak, ada
   $b\in B$ dengan $c=g(b)$. Selanjutnya

   $$
   0=\gamma(c)=\gamma(g(b))=g'(\beta(b)).
   $$

   Eksaknya baris bawah memberi $a'\in A'$ dengan
   $\beta(b)=f'(a')$. Surjektivitas $\alpha$ memungkinkan kita memilih
   $a\in A$ dengan $\alpha(a)=a'$. Komutativitas bujur sangkar kiri memberi

   $$
   \beta(f(a))=f'(\alpha(a))=f'(a')=\beta(b).
   $$

   Karena $\beta$ injektif, $f(a)=b$. Akhirnya, eksaknya baris atas memberi

   $$
   c=g(b)=g(f(a))=0.
   $$

   Jadi $\ker\gamma=0$, sehingga $\gamma$ injektif.

Karena $\gamma$ sekaligus surjektif dan injektif, ia merupakan isomorfisma.
:::

::: {.source-audit #o012-rbt-l25-audit-004}
**Audit sumber 25.4.** Pada langkah surjektivitas, Notes.tex baris 5526--5527
menempatkan unsur $b'$ di $B$, padahal tipenya harus $b'\in B'$ agar dapat
diangkat melalui $\beta\colon B\to B'$. Edisi memperbaiki tipe itu. Sumber
menyebut langkah injektivitas sebagai latihan untuk mendualkan langkah
sebelumnya; edisi memberikan seluruh pengejaran unsur, termasuk tempat tepat
digunakannya surjektivitas $\alpha$ serta injektivitas $\beta$ dan $\delta$.
:::

## Karakteristik Euler dari modul kohomologi {#o012-rbt-l25-s04}

Ingat kembali karakteristik Euler sebuah himpunan-$\Delta$ hingga:

$$
\chi(X_\bullet)=\sum_{d=0}^{\infty}(-1)^d|X_d|.
$$

::: {.aside #o012-rbt-l25-aside-006}
**Mengapa jumlahnya berhingga?** Untuk himpunan-$\Delta$ hingga,
$|X_d|=0$ bagi semua $d$ yang cukup besar. Jadi hanya berhingga banyak suku
dalam jumlah tersebut yang taknol.
:::

Salah satu gagasan utama bagian ini ialah mengganti invarian numerik—misalnya
kardinalitas himpunan hingga—dengan ruang vektor atau, secara lebih umum,
modul, lalu mengganti kardinalitas dengan dimensi. Jika kita mengambil
$R=\mathbb R$, dimensi modul kohomologi memberi invarian numerik lain.
Definisikan **karakteristik Euler kohomologis** dengan

$$
\chi^{\mathrm{coh}}(X_\bullet)
:=\sum_{d=0}^{\infty}(-1)^d
\dim_{\mathbb R}H^d(X_\bullet;\mathbb R),
$$

asalkan semua dimensi yang muncul hingga dan hanya berhingga banyak suku yang
taknol. Syarat ini mengharuskan
$H^d(X_\bullet;\mathbb R)=0$ untuk $d$ yang cukup besar, tetapi tidak
mengharuskan $X_\bullet$ hingga atau bahkan berdimensi hingga. Misalnya,
$Pt_\bullet$ memberi $\chi^{\mathrm{coh}}(Pt_\bullet)=1$.

::: {.aside #o012-rbt-l25-aside-007}
**Koefisien.** Setiap medan berkarakteristik nol dapat menggantikan
$\mathbb R$ dalam pembahasan dimensi ini.
:::

Kita juga dapat menangani himpunan-$\Delta$ berdimensi hingga tetapi takhingga,
misalnya triangulasi garis real oleh simpleks-$1$.

::: {.example #o012-rbt-l25-exa-006}
**Contoh 25.6 (garis bilangan bulat).** Misalkan $L_\bullet$ adalah graf
berarah dengan

$$
L_0=\mathbb Z,\qquad L_1=\mathbb Z,
$$

dan $d_0(n)=n+1$, $d_1(n)=n$. Jadi untuk setiap $n$ ada sisi dari $n$ ke
$n+1$. Bagi $g\in\mathbb R^{L_0}=\mathbb R^{\mathbb Z}$,

$$
\delta_0(g)(n)=g(n+1)-g(n).
$$

Persamaan $\delta_0(g)=0$ berlaku tepat ketika $g$ konstan. Maka

$$
\ker\delta_0=H^0(L_\bullet;\mathbb R)=\mathbb R.
$$

Sebaliknya, ambil sembarang
$h\in\mathbb R^{L_1}=\mathbb R^{\mathbb Z}$. Tetapkan $g(0)=0$. Untuk
$n\ge0$, definisikan maju

$$
g(n+1)=h(n)+g(n),
$$

dan untuk $n<0$, definisikan mundur

$$
g(n)=g(n+1)-h(n).
$$

Kedua rekursi menentukan fungsi $g\colon\mathbb Z\to\mathbb R$ dengan
$\delta_0(g)=h$. Jadi $\delta_0$ surjektif dan

$$
\operatorname{coker}\delta_0
=H^1(L_\bullet;\mathbb R)=0.
$$

Semua ruang kohomologi berkoefisien real pada derajat lain juga nol, sehingga

$$
\chi^{\mathrm{coh}}(L_\bullet)=1.
$$
:::

Untuk himpunan-$\Delta$ hingga, kita sekarang mempunyai dua invarian numerik,
$\chi$ dan $\chi^{\mathrm{coh}}$. Hubungan keduanya tidak langsung tampak,
tetapi ternyata keduanya berimpit.

::: {.proposition #o012-rbt-l25-prop-002}
**Proposisi 25.2 (kesamaan karakteristik Euler).** Untuk himpunan-$\Delta$
hingga $X_\bullet$,

$$
\chi(X_\bullet)=\chi^{\mathrm{coh}}(X_\bullet).
$$
:::

::: {.proof #o012-rbt-l25-proof-004 data-origin="source-proof-repaired-by-edition"}
**Bukti.** Tuliskan

$$
C^d:=\mathbb R^{X_d},\qquad
Z^d:=\ker\delta_d,\qquad
B^d:=\operatorname{im}\delta_{d-1},
$$

dan tetapkan

$$
r_d:=\dim\operatorname{im}\delta_d,
\qquad r_{-1}:=0,
\qquad h_d:=\dim H^d(X_\bullet;\mathbb R).
$$

Karena $X_\bullet$ hingga, semua ruang ini berdimensi hingga dan semuanya
nol pada derajat yang cukup besar. Rank--nulitas untuk
$\delta_d\colon C^d\to C^{d+1}$ memberi

$$
\dim C^d=\dim Z^d+r_d.
$$

Karena $H^d=Z^d/B^d$ dan
$\dim B^d=r_{d-1}$, kita juga mempunyai

$$
\dim Z^d=h_d+r_{d-1}.
$$

Dengan menggabungkan kedua persamaan,

$$
|X_d|=\dim C^d=h_d+r_{d-1}+r_d.
$$

Karena semua jumlah berikut sebenarnya berhingga,

$$
\begin{aligned}
\chi(X_\bullet)
&=\sum_{d=0}^{\infty}(-1)^d|X_d|\\
&=\sum_{d=0}^{\infty}(-1)^d h_d
 +\sum_{d=0}^{\infty}(-1)^d r_{d-1}
 +\sum_{d=0}^{\infty}(-1)^d r_d.
\end{aligned}
$$

Pada jumlah tengah, penggantian indeks $j=d-1$ dan syarat $r_{-1}=0$
memberi

$$
\sum_{d=0}^{\infty}(-1)^d r_{d-1}
=-\sum_{j=0}^{\infty}(-1)^j r_j.
$$

Dua jumlah yang memuat peringkat diferensial saling meniadakan. Karena itu,

$$
\chi(X_\bullet)
=\sum_{d=0}^{\infty}(-1)^d h_d
=\chi^{\mathrm{coh}}(X_\bullet),
$$

sebagaimana dikehendaki.
:::

::: {.source-audit #o012-rbt-l25-audit-005}
**Audit sumber 25.5.** Notes.tex baris 5574--5585 menulis
$\mathbb R^{X_d}=\ker\delta_d\oplus\operatorname{im}\delta_d$, tetapi
$\operatorname{im}\delta_d$ berada di $\mathbb R^{X_{d+1}}$, bukan di
$\mathbb R^{X_d}$. Baris yang sama kemudian menulis
$\dim\delta_d$ alih-alih $\dim\operatorname{im}\delta_d$, dan baris 5588
menulis $|X_\bullet|$ alih-alih $|X_d|$. Edisi mengganti pemisahan yang
bertipe salah dengan dua persamaan dimensi yang sah dan memperlihatkan
pembatalan jumlah peringkat melalui pergeseran indeks. Hasil proposisi tetap
sama.
:::

Kita kini dapat menghilangkan superskrip pada
$\chi^{\mathrm{coh}}$ dan cukup berbicara tentang **karakteristik Euler**
sebuah himpunan-$\Delta$.

::: {.remark #o012-rbt-l25-rem-001}
**Catatan 25.1 (kompleks berhingga umum).** Bukti yang sama berlaku hampir
kata demi kata bagi kompleks korantai $V_\bullet$ ruang vektor berdimensi
hingga dan panjang hingga,

$$
0\longrightarrow V_m\longrightarrow V_{m+1}\longrightarrow\cdots
\longrightarrow V_{m+N}\longrightarrow0.
$$

Dengan indeks kohomologis yang sama pada kedua sisi,

$$
\sum_{d=m}^{m+N}(-1)^d\dim V_d
=\sum_{d=m}^{m+N}(-1)^d\dim H^d(V_\bullet).
$$
:::

::: {.source-audit #o012-rbt-l25-audit-006}
**Audit sumber 25.6.** Rumus penutup pada Notes.tex baris 5608 menghilangkan
eksponen $d$ dari tanda di ruas kiri dan menghilangkan $\dim$ beserta
eksponen $d$ di ruas kanan. Rumus pada Catatan 25.1 memulihkan kedua faktor
yang diperlukan; argumennya adalah pembatalan rank--nulitas yang sama seperti
pada Proposisi 25.2.
:::

## Pemeriksaan penguasaan {#o012-rbt-l25-mastery}

Soal-soal berikut merupakan materi asli edisi. Masing-masing dilengkapi
petunjuk dan solusi lengkap sehingga dapat dipakai untuk belajar mandiri.

::: {.exercise #o012-rbt-l25-mcheck-001 data-origin="edition-original"}
**Pemeriksaan Penguasaan 25.1 (satu modul pada derajat atas).** Misalkan
$X_\bullet$ berdimensi $n$ dan
$A_\bullet=\operatorname{sk}_{n-1}X_\bullet$. Buktikan langsung dari definisi
restriksi bahwa

$$
C^\bullet(X_\bullet,A_\bullet;R)\cong R^{X_n}[n],
$$

lalu tentukan semua modul kohomologi relatif. Jelaskan juga apa yang terjadi
jika $X_n=\varnothing$.
:::

::: {.hint #o012-rbt-l25-hint-001 data-origin="edition-original"}
**Petunjuk.** Bandingkan $A_k$ dengan $X_k$ untuk $k<n$ dan $k=n$.
Korantai relatif adalah kernel pemetaan restriksi $R^{X_k}\to R^{A_k}$.
:::

::: {.solution #o012-rbt-l25-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan 25.1.** Untuk $k<n$, definisi kerangka memberi
$A_k=X_k$, sehingga restriksi adalah identitas dan kernelnya nol. Karena
$X_\bullet$ berdimensi $n$, $A_n=\varnothing$ dan

$$
\ker(R^{X_n}\to R^\varnothing)=R^{X_n}.
$$

Di atas derajat $n$, kedua himpunan simpleks kosong, jadi modul korantainya
juga nol. Satu-satunya diferensial yang mungkin masuk atau keluar dari
$R^{X_n}$ memiliki sumber atau sasaran nol. Jadi kompleks relatif tepat
$R^{X_n}[n]$, dan

$$
H^k(X_\bullet,A_\bullet;R)=
\begin{cases}
R^{X_n},&k=n,\\
0,&k\ne n.
\end{cases}
$$

Jika $X_n=\varnothing$, maka $R^{X_n}=R^\varnothing=0$ dan seluruh kompleks
serta seluruh kohomologi relatifnya nol. Dalam hal itu, “berdimensi $n$”
sebenarnya hanyalah batas atas dimensi, bukan dimensi tepat.
:::

::: {.exercise #o012-rbt-l25-mcheck-002 data-origin="edition-original"}
**Pemeriksaan Penguasaan 25.2 (batas simpleks).** Ambil $n\ge2$. Selain hasil
relatif pada Contoh 25.2, andaikan telah diketahui bahwa

$$
H^0(\Delta[n];R)=R,
\qquad H^k(\Delta[n];R)=0\quad(k>0).
$$

Gunakan barisan eksak panjang pasangan untuk menentukan
$H^k(\partial\Delta[n];R)$ pada setiap $k$ dan identifikasi pemetaan
penghubung yang taktrivial.
:::

::: {.hint #o012-rbt-l25-hint-002 data-origin="edition-original"}
**Petunjuk.** Kohomologi relatif hanya $R$ pada derajat $n$. Untuk derajat
di bawah $n-1$, dua suku relatif yang mengapit pemetaan biasa adalah nol.
Periksa secara terpisah derajat $0$ dan potongan di sekitar $n-1,n$.
:::

::: {.solution #o012-rbt-l25-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan 25.2.** Karena kelompok relatif pada derajat $0$ dan
$1$ nol untuk $n\ge2$, awal barisan memberi isomorfisma

$$
H^0(\Delta[n];R)\xrightarrow{\cong}
H^0(\partial\Delta[n];R),
$$

sehingga $H^0(\partial\Delta[n];R)=R$. Untuk
$0<k<n-1$, kedua suku relatif yang mengapit pemetaan
$H^k(\Delta[n])\to H^k(\partial\Delta[n])$ nol, dan suku pertama juga nol
menurut asumsi. Jadi $H^k(\partial\Delta[n];R)=0$.

Di derajat atas, barisan menyederhana menjadi

$$
0\longrightarrow H^{n-1}(\partial\Delta[n];R)
\xrightarrow{\ \partial^{n-1}\ }R
\longrightarrow0,
$$

karena $H^{n-1}(\Delta[n];R)=H^n(\Delta[n];R)=0$. Maka
$\partial^{n-1}$ adalah isomorfisma dan

$$
H^{n-1}(\partial\Delta[n];R)\cong R.
$$

Semua derajat di atasnya nol. Jadi kohomologi batas simpleks hanya $R$ pada
derajat $0$ dan $n-1$, dan pemetaan penghubung
$\partial^{n-1}$ adalah pemetaan taktrivial yang mengidentifikasi suku atas
dengan $H^n(\Delta[n],\partial\Delta[n];R)=R$.
:::

::: {.exercise #o012-rbt-l25-mcheck-003 data-origin="edition-original"}
**Pemeriksaan Penguasaan 25.3 (kohomologi tereduksi himpunan diskret).**
Misalkan $D_\bullet$ berdimensi nol, dengan
$D_0=\{x_0,x_1,\ldots,x_n\}$ dan titik dasar $x_0$. Hitung kompleks relatif
$C^\bullet(D_\bullet,x_0;R)$ dan kohomologi tereduksinya. Berikan basis
eksplisit jika $R$ sebuah medan.
:::

::: {.hint #o012-rbt-l25-hint-003 data-origin="edition-original"}
**Petunjuk.** Pemetaan restriksi pada derajat $0$ mengevaluasi fungsi di
$x_0$. Tidak ada modul pada derajat positif.
:::

::: {.solution #o012-rbt-l25-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan 25.3.** Pada derajat $0$,

$$
C^0(D_\bullet,x_0;R)
=\ker\!\left(R^{n+1}\xrightarrow{\rho_{x_0}}R\right)
=\{(0,a_1,\ldots,a_n):a_i\in R\}\cong R^n.
$$

Semua modul pada derajat positif nol, sehingga semua diferensial nol dan

$$
H^k(D_\bullet,x_0;R)=
\begin{cases}
R^n,&k=0,\\
0,&k>0.
\end{cases}
$$

Jika $R$ medan, sebuah basis ialah fungsi indikator
$e_i$ untuk $1\le i\le n$, dengan $e_i(x_i)=1$ dan bernilai nol pada semua
titik lain. Tidak ada indikator $e_0$ karena setiap korantai relatif harus
lenyap pada titik dasar.
:::

::: {.exercise #o012-rbt-l25-mcheck-004 data-origin="edition-original"}
**Pemeriksaan Penguasaan 25.4 (kuasi-isomorfisma titik tebal).** Tuliskan
kompleks $C^\bullet(Pt_\bullet;R)$ dan
$C^\bullet(\operatorname{sk}_0Pt_\bullet;R)$ derajat demi derajat. Buktikan
bahwa restriksi yang diinduksi inklusi kerangka adalah kuasi-isomorfisma,
tetapi bukan isomorfisma kompleks.
:::

::: {.hint #o012-rbt-l25-hint-004 data-origin="edition-original"}
**Petunjuk.** Diferensial pada kompleks pertama bergantian antara nol dan
identitas. Kompleks kedua hanya mempunyai $R$ pada derajat $0$. Bandingkan
lebih dahulu modulnya, lalu kohomologinya.
:::

::: {.solution #o012-rbt-l25-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan 25.4.** Kompleks pertama ialah

$$
0\to R\xrightarrow0R\xrightarrow{\operatorname{id}}R
\xrightarrow0R\xrightarrow{\operatorname{id}}\cdots,
$$

sedangkan kompleks kerangka ialah

$$
0\to R\to0\to0\to\cdots.
$$

Restriksi adalah identitas pada derajat $0$ dan pemetaan nol $R\to0$ pada
setiap derajat positif. Ia komutatif dengan diferensial: pada derajat $0$
kedua komposisi menuju nol, dan pada derajat positif sasaran seluruhnya nol.
Kompleks pertama mempunyai $H^0=R$ dan $H^k=0$ untuk $k>0$, sebab pemetaan
bergantian nol dan identitas. Kompleks kedua mempunyai kohomologi yang sama.
Pemetaan terinduksi adalah identitas pada $H^0$ dan isomorfisma unik
$0\to0$ pada derajat positif. Jadi restriksi merupakan kuasi-isomorfisma.
Namun ia bukan isomorfisma kompleks, sebab pada setiap derajat positif
komponennya adalah pemetaan $R\to0$, yang tidak bijektif jika $R\ne0$.
:::

::: {.exercise #o012-rbt-l25-mcheck-005 data-origin="edition-original"}
**Pemeriksaan Penguasaan 25.5 (separuh injektif Lema Lima).** Dalam Diagram
25.2, andaikan $\alpha$ surjektif, $\beta$ dan $\delta$ injektif, dan kedua
baris eksak. Mulai dari $c\in\ker\gamma$ dan buktikan $c=0$. Pada setiap
langkah, nyatakan hipotesis mana yang digunakan.
:::

::: {.hint #o012-rbt-l25-hint-005 data-origin="edition-original"}
**Petunjuk.** Dorong $c$ ke $D$, gunakan injektivitas $\delta$, angkat $c$
dari citra $g$, dorong pengangkatnya ke $B'$, lalu gunakan eksaknya baris
bawah, surjektivitas $\alpha$, dan terakhir injektivitas $\beta$.
:::

::: {.solution #o012-rbt-l25-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan 25.5.** Ambil $c$ dengan $\gamma(c)=0$.
Komutativitas memberi

$$
\delta(h(c))=h'(\gamma(c))=0.
$$

Injektivitas $\delta$ memberi $h(c)=0$. Eksaknya baris atas di $C$ memberi
$b\in B$ dengan $c=g(b)$. Maka

$$
g'(\beta(b))=\gamma(g(b))=\gamma(c)=0.
$$

Eksaknya baris bawah di $B'$ memberi $a'\in A'$ dengan
$\beta(b)=f'(a')$. Surjektivitas $\alpha$ memberi $a\in A$ dengan
$\alpha(a)=a'$. Dari komutativitas,

$$
\beta(f(a))=f'(\alpha(a))=f'(a')=\beta(b).
$$

Injektivitas $\beta$ memberi $f(a)=b$. Eksaknya baris atas di $B$—atau
langsung sifat kompleks $gf=0$—akhirnya memberi

$$
c=g(b)=g(f(a))=0.
$$

Jadi $\gamma$ injektif. Hipotesis tentang $\varepsilon$ dan surjektivitas
$\beta,\delta$ tidak dipakai dalam separuh ini; hipotesis itu tepat untuk
separuh surjektif.
:::

::: {.exercise #o012-rbt-l25-mcheck-006 data-origin="edition-original"}
**Pemeriksaan Penguasaan 25.6 (garis takhingga dan pembatalan Euler).** Untuk
$L_\bullet$ pada Contoh 25.6:

1. bangun secara eksplisit $g\colon\mathbb Z\to\mathbb R$ dengan
   $g(n+1)-g(n)=h(n)$ bagi sembarang $h\colon\mathbb Z\to\mathbb R$;
2. hitung seluruh kohomologi dan $\chi^{\mathrm{coh}}(L_\bullet)$;
3. jelaskan mengapa jumlah simpleks biasa tidak mendefinisikan
   $\chi(L_\bullet)$; dan
4. untuk kompleks berdimensi hingga, jelaskan secara aljabar mengapa suku
   $\dim\operatorname{im}\delta_d$ selalu muncul dua kali dengan tanda
   berlawanan dalam jumlah Euler.
:::

::: {.hint #o012-rbt-l25-hint-006 data-origin="edition-original"}
**Petunjuk.** Tetapkan $g(0)=0$, jumlahkan $h$ ke kanan, dan kurangkan $h$
ketika bergerak ke kiri. Untuk bagian terakhir, gunakan
$\dim C^d=\dim H^d+r_{d-1}+r_d$.
:::

::: {.solution #o012-rbt-l25-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan 25.6.** Untuk sembarang $h$, definisikan

$$
g(n)=
\begin{cases}
\displaystyle\sum_{j=0}^{n-1}h(j),&n>0,\\[6pt]
0,&n=0,\\[6pt]
\displaystyle-\sum_{j=n}^{-1}h(j),&n<0.
\end{cases}
$$

Pada ketiga kemungkinan posisi $n$, pengurangan langsung memberi
$g(n+1)-g(n)=h(n)$. Jadi $\delta_0$ surjektif. Kernelnya terdiri tepat atas
fungsi konstan, sehingga

$$
H^0(L_\bullet;\mathbb R)=\mathbb R,
\qquad H^1(L_\bullet;\mathbb R)=0,
$$

dan semua kohomologi di atas derajat $1$ nol karena tidak ada simpleks pada
derajat itu. Maka $\chi^{\mathrm{coh}}(L_\bullet)=1$.

Namun $L_0$ dan $L_1$ keduanya takhingga. Ekspresi
$|L_0|-|L_1|$ bukan jumlah bilangan berdimensi hingga yang dimaksud dalam
definisi karakteristik Euler biasa, sehingga argumen “takhingga dikurangi
takhingga” tidak mendefinisikan $\chi(L_\bullet)$.

Untuk kompleks hingga, tetapkan
$r_d=\dim\operatorname{im}\delta_d$. Rank--nulitas dan definisi kohomologi
memberi

$$
\dim C^d=\dim H^d+r_{d-1}+r_d.
$$

Dalam jumlah berganti tanda, $r_d$ muncul dari suku derajat $d$ dengan tanda
$(-1)^d$ dan dari $r_{(d+1)-1}$ pada suku derajat $d+1$ dengan tanda
$(-1)^{d+1}$. Kedua koefisien berjumlah nol. Inilah mekanisme aljabar yang
meninggalkan hanya jumlah berganti tanda dimensi kohomologi.
:::

::: {.boundary #o012-rbt-l25-boundary-001}
**Batas ke Unit 26.** Unit 25 menerjemahkan Notes.tex baris 5370--5611 secara
kontigu dan menutup seluruh objek sumber pada rentang itu. Baris 5612 berbunyi
`Recall\lecturenum{26} the geometric realisation ...`, memulai Kuliah 26, dan
tidak dimasukkan. Kursor sumber berikutnya yang tepat adalah **Notes.tex baris
5612**.
:::
