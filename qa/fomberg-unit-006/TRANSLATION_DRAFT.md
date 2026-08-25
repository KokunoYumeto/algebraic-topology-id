---
title: "DRAF NONKANONIK — Topologi Aljabar"
subtitle: "Komponen Fomberg 6: Kompleks Seluler"
author:
  - "Yeheli Fomberg (catatan sumber; berdasarkan kuliah Nir Lazarovich)"
  - "Draf edisi Bahasa Indonesia"
date: "25 Agustus 2026"
lang: id-ID
rights: "Sumber dan adaptasi: CC BY-SA 4.0; draf nonkanonik untuk QA internal."
source_component: "Fomberg Algebraic Topology, Section 1.12"
source_lines: "3123-3517"
edition_unit_id: "O012-FOM-006"
course_route_unit_id: "D60-R12"
status: "draf terjemahan kontigu; belum memuat materi penguasaan"
---

# Tentang draf ini {.unnumbered #o012-fom-u006-draft-notice data-course-route-unit-id="D60-R12"}

Draf nonkanonik ini menerjemahkan secara kontigu Bagian 1.12
*Algebraic Topology* karya Yeheli Fomberg, berdasarkan kuliah Nir Lazarovich
pada musim semi 2025. Otoritas sumber dibekukan pada commit
[563194fae879178b9a6871b249513bfc27968975](https://git.sr.ht/~yp/math-notes/tree/563194fae879178b9a6871b249513bfc27968975/item/algebraic_topology.tex).
Rentang sumber tepatnya ialah `algebraic_topology.tex` baris 3123–3517:
395 baris fisik, 15.540 byte setelah normalisasi LF dan satu LF penutup,
dengan SHA-256
`c16d595b8f8c4c67ea5f0f58c1ad7de83ac94efae509d3a8d3bef28da2522f19`.

Catatan sumber tersedia di bawah
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
Draf terjemahan dan pemformatan semantik ini memakai lisensi yang sama.
Tidak ada materi penguasaan baru yang ditambahkan pada tahap draf ini.
Kode TikZ sumber dipertahankan di dalam blok gambar agar fungsi setiap
diagram dapat direkonstruksi secara tepat pada tahap produksi pembaca.

Edisi ini independen dan tidak menyiratkan dukungan, pengesahan, atau
afiliasi dengan Yeheli Fomberg, Nir Lazarovich, ataupun institusi mereka.
Produksi terjemahan dan struktur semantik dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna.

# Kompleks Seluler {#o012-fom-u006 data-source-lines="3123-3517" data-course-route-unit-id="D60-R12"}

::: {.remark #o012-fom-u006-rem-intro data-origin="source-derived" data-source-lines="3125-3132"}
**Catatan.** Dalam topologi kita dapat membangun ruang-ruang yang benar-benar
buruk. Ketika kita memperkenalkan struktur sederhana seperti
kompleks-$\Delta$, struktur itu memungkinkan kita menghitung homologi suatu
keluarga ruang tertentu. Sekarang kita (kembali) memperkenalkan kompleks sel
(CW), yang memperumum kompleks-$\Delta$ dan memungkinkan kita menghitung
homologi lebih banyak ruang dengan lebih mudah.
:::

::: {.definition #o012-fom-u006-def-cw data-origin="source-derived" data-source-lines="3134-3248"}
**Definisi (kompleks CW).** Kompleks **CW** (atau **seluler**) adalah ruang
$X$ yang dibangun secara induktif sebagai berikut. Pertama, kita mendefinisikan
$0$-kerangka, yang merepresentasikan struktur berdimensi $0$ dari kompleks
tersebut:

$$
X^{(0)}=\text{suatu himpunan simpul diskret}.
$$

:::: {.figure #o012-fom-u006-fig-zero-skeleton data-origin="source-derived" data-source-lines="3138-3148" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Lima titik yang saling terpisah merepresentasikan suatu
himpunan simpul diskret, yaitu $0$-kerangka $X^{(0)}$.

```tex
\tikz[eqpic]{
  \node[circle,fill,inner sep=1.5pt] (p1) at (0,0) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (1,1) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (1.5,-1) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (2.5,0.3) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (3.5,0) {};
}
```
::::

Kemudian $1$-kerangka didefinisikan dengan menetapkan pasangan-pasangan yang
terdiri atas cakram-$1$ dan peta pelekatan
$\{\D^1_{\alpha},\varphi_{\alpha}\}$, dengan peta pelekatan

$$
\varphi_{\alpha}\colon \partial\D^1_{\alpha}\longrightarrow X^{(0)},
$$

sehingga

$$
X^{(1)}=
\del{X^{(0)}\sqcup\bigsqcup_{\alpha}\D^1_{\alpha}}
\big/\set{x\sim\varphi_{\alpha}(x)}.
$$

Sebagai contoh, dengan memakai $0$-kerangka di atas, kita dapat memperoleh
$1$-kerangka berikut.

:::: {.figure #o012-fom-u006-fig-one-skeleton data-origin="source-derived" data-source-lines="3159-3177" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Lima simpul yang sama dihubungkan oleh enam sel-$1$:
tiga sisi membentuk sebuah segitiga pada tiga simpul teratas, satu busur
menghubungkan simpul paling kiri dengan simpul bawah, satu lintasan bergelombang
menghubungkan simpul bawah dengan simpul paling kanan, dan satu loop melekat
pada simpul paling kanan.

```tex
\tikz[eqpic,every path/.style={thick}]{
  \draw (0,0) -- (1,1);
  \draw (0,0) -- (2.5,0.3);
  \draw (2.5,0.3) -- (1,1);
  \draw (0,0) to [bend right=35] (1.5,-1);
  \draw plot [smooth cycle] coordinates
    {(3.5,0) (3.5,-0.7) (3.9,-0.5)};
  \node[circle,fill,inner sep=1.5pt] (p1) at (0,0) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (1,1) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (1.5,-1) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (2.5,0.3) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (3.5,0) {};
  \draw[smooth,tension=1] plot coordinates
    {(1.5,-1) (2,-0.75+0.2) (2.5,-0.5-0.2) (3,-0.25+0.2) (3.5,0)};
}
```
::::

Kita juga mempunyai pemetaan karakteristik

$$
\phi_{\alpha}\colon\D^1_{\alpha}\longrightarrow X^{(1)}.
$$

Pemetaan ini membawa setiap cakram dari “kehampaan” ke cakram tersebut dalam
konteks kompleks CW. Diagram berikut membandingkan
$\varphi_{\alpha}$ dan $\phi_{\alpha}$.

:::: {.figure #o012-fom-u006-fig-characteristic-map data-origin="source-derived" data-source-lines="3178-3207" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Pemetaan karakteristik $\phi_{\alpha}$ membawa seluruh
interval merah $\D^1_{\alpha}$, termasuk kedua titik ujungnya, ke sel-$1$
merah beserta kedua simpul tempat sel itu melekat di dalam $X^{(1)}$.

```tex
\tikz[eqpic,every path/.style={thick}]{
  \draw[-->] (-3,0) -- (1,0);
  \draw[-->] (-1,-1.5) -- (-1,1.5);
  \draw[red,very thick] (-2,0) -- (0,0);
  \node[red,circle,fill,inner sep=1.5pt] (p1) at (0,0) {};
  \node[red,circle,fill,inner sep=1.5pt] (p2) at (-2,0) {};
} \quad
\taking{\quad \phi_{\alpha} \quad} \quad
\tikz[eqpic,every path/.style={thick}]{
  \draw (0,0) -- (1,1);
  \draw (0,0) -- (2.5,0.3);
  \draw (2.5,0.3) -- (1,1);
  \draw (0,0) to [bend right=35] (1.5,-1);
  \draw plot [smooth cycle] coordinates
    {(3.5,0) (3.5,-0.7) (3.9,-0.5)};
  \node[circle,fill,inner sep=1.5pt] (p1) at (0,0) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (1,1) {};
  \node[red,circle,fill,inner sep=1.5pt] (p1) at (1.5,-1) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (2.5,0.3) {};
  \node[red,circle,fill,inner sep=1.5pt] (p1) at (3.5,0) {};
  \draw[red,smooth,tension=1] plot coordinates
    {(1.5,-1) (2,-0.75+0.2) (2.5,-0.5-0.2) (3,-0.25+0.2) (3.5,0)};
}
```
::::

:::: {.figure #o012-fom-u006-fig-attaching-map data-origin="source-derived" data-source-lines="3208-3232" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Peta pelekatan $\varphi_{\alpha}$ hanya membawa batas
$\partial\D^1_{\alpha}$—dua titik ujung berwarna merah—ke dua simpul merah
di $X^{(0)}$. Bagian dalam interval tidak termasuk dalam domain peta pelekatan.

```tex
\tikz[eqpic,every path/.style={thick}]{
  \draw[-->] (-3,0) -- (1,0);
  \draw[-->] (-1,-1.5) -- (-1,1.5);
  \draw[red,very thick] (-2,0) -- (0,0);
  \node[red,circle,fill,inner sep=1.5pt] (p1) at (0,0) {};
  \node[red,circle,fill,inner sep=1.5pt] (p2) at (-2,0) {};
} \quad
\taking{\quad \varphi_{\alpha} \quad} \quad
\tikz[eqpic,every path/.style={thick}]{
  \draw (0,0) -- (1,1);
  \draw (0,0) -- (2.5,0.3);
  \draw (2.5,0.3) -- (1,1);
  \draw (0,0) to [bend right=35] (1.5,-1);
  \draw plot [smooth cycle] coordinates
    {(3.5,0) (3.5,-0.7) (3.9,-0.5)};
  \node[circle,fill,inner sep=1.5pt] (p1) at (0,0) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (1,1) {};
  \node[circle,fill,inner sep=1.5pt] (p1) at (2.5,0.3) {};
  \draw[smooth,tension=1] plot coordinates
    {(1.5,-1) (2,-0.75+0.2) (2.5,-0.5-0.2) (3,-0.25+0.2) (3.5,0)};
  \node[red,circle,fill,inner sep=1.5pt] (p1) at (1.5,-1) {};
  \node[red,circle,fill,inner sep=1.5pt] (p1) at (3.5,0) {};
}
```
::::

Kadang-kadang kita menyebut keluarga

$$
\set{\Int(\phi_{\alpha}(\D^1_{\alpha}))}_{\alpha}
$$

sebagai **sel-sel-$1$** dari $X$.

Sekarang kita dapat mendefinisikan secara induktif suatu kompleks CW
berdimensi hingga $X=X^{(n)}$ sebagai berikut. Andaikan kita mempunyai
$X^{(n-1)}$-kerangka dan pasangan cakram-$n$ serta peta pelekatan

$$
\set{(\D^n_{\alpha},\varphi_{\alpha})}_{\alpha}.
$$

Maka

$$
X^{(n)}=
\del{X^{(n-1)}\sqcup\bigsqcup_{\alpha}\D^1_{\alpha}}
\big/\set{x\sim\varphi_{\alpha}(x)}.
$$
:::

::: {.remark #o012-fom-u006-rem-one-dimensional-equivalence data-origin="source-derived" data-source-lines="3250-3253"}
**Catatan.** Dalam dimensi $0$ dan $1$, setiap kompleks CW ekuivalen dengan
sebuah kompleks-$\Delta$, dan sebaliknya.
:::

::: {.remark #o012-fom-u006-rem-delta-characteristic data-origin="source-derived" data-source-lines="3255-3259"}
**Catatan.** Dalam suatu struktur kompleks-$\Delta$, pemetaan

$$
\sigma_{\alpha}\colon\Delta^{n_{\alpha}}\longrightarrow X
$$

merupakan pemetaan karakteristik.
:::

::: {.remark #o012-fom-u006-rem-infinite-cw data-origin="source-derived" data-source-lines="3261-3266"}
**Catatan.** Bila $n\to\infty$ untuk suatu barisan $X^{(n)}$, kita
mendefinisikan

$$
X:=\lim_{n\to\infty}X^{(n)}=\bigcup X^{(n)},
$$

dan menyatakan bahwa $U\subseteq X$ terbuka jika dan hanya jika
$U\cap X^{(n)}$ terbuka untuk setiap $n$.
:::

::: {.example #o012-fom-u006-ex-hawaiian-earring data-origin="source-derived" data-source-lines="3268-3295"}
**Contoh (noncontoh baku).** Sebelum memberikan contoh, berikut ini sebuah
noncontoh baku. Pandang $\mathbb R^2$ sebagai ruang latar, lalu tambahkan semua
lingkaran berjari-jari $1/n$ dengan pusat $(0,1/n)$. Kita memperoleh suatu
kompleks CW yang tampak seperti berikut.

:::: {.figure #o012-fom-u006-fig-hawaiian-earring data-origin="source-derived" data-source-lines="3270-3287" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Sumbu mendatar dan barisan lingkaran yang semuanya
menyinggung titik asal dari atas. Lingkaran ke-$n$ berpusat di $(0,1/n)$ dan
berjari-jari $1/n$, sehingga ukuran lingkaran menyusut menuju titik asal.
Titik-titik merah menandai $(0,2)$, $(0,1)$, $(0,1/2)$, $(0,1/4)$, dan
$(0,1/8)$.

```tex
\begin{tikzpicture}[every path/.style={thick}]
  \draw (-4,0) -- (4,0);
  \draw (0,1) circle (1);
  \draw (0,0.5) circle (0.5);
  \draw (0,0.25) circle (0.25);
  \draw (0,0.125) circle (0.125);
  \draw (0,0.125/2) circle (0.125/2);
  \node[circle, fill, inner sep=1.5,red] (p4) at (0,2) {};
  \node[circle, fill, inner sep=1.5,red] (p1) at (0,1) {};
  \node[circle, fill, inner sep=1.5,red] (p2) at (0,0.5) {};
  \node[circle, fill, inner sep=1.5,red] (p3) at (0,0.25) {};
  \node[circle, fill, inner sep=1.5,red] (p5) at (0,0.125) {};
\end{tikzpicture}
```
::::

Ruang ini dikenal sebagai **anting-anting Hawaii**. Ruang ini bukan kompleks
CW karena kita mensyaratkan simpul-simpul kita, yakni unsur-unsur
$X^{(0)}$, bersifat diskret, sedangkan jelas bahwa titik-titik $(0,1/n)$
konvergen ke $(0,0)$. Secara kontraintuitif, jika kita memilih $(0,n)$ sebagai
pusat lingkaran berjari-jari $n$, kita akan memperoleh kompleks CW yang
terdefinisi dengan baik.
:::

::: {.example #o012-fom-u006-ex-topological-graph data-origin="source-derived" data-source-lines="3297-3333"}
**Contoh (graf topologis).** Suatu graf topologis adalah kompleks CW. Sebagai
contoh:

:::: {.figure #o012-fom-u006-fig-petersen-graph data-origin="source-derived" data-source-lines="3299-3324" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Graf Petersen dengan lima simpul pada sebuah pentagon
luar, lima simpul pada sebuah pentagram dalam, lima sisi radial yang
memasangkan simpul-simpul luar dan dalam, lima sisi pentagon luar, dan lima
sisi pentagram dalam.

```tex
\begin{tikzpicture}[every path/.style=thick]
  \node[circle,fill,inner sep=1.5pt] at (90:2.2) {};
  \node[circle,fill,inner sep=1.5pt] at (162:2.2) {};
  \node[circle,fill,inner sep=1.5pt] at (234:2.2) {};
  \node[circle,fill,inner sep=1.5pt] at (306:2.2) {};
  \node[circle,fill,inner sep=1.5pt] at (18:2.2) {};

  \node[circle,fill,inner sep=1.5pt] at (90:1.2) {};
  \node[circle,fill,inner sep=1.5pt] at (162:1.2) {};
  \node[circle,fill,inner sep=1.5pt] at (234:1.2) {};
  \node[circle,fill,inner sep=1.5pt] at (306:1.2) {};
  \node[circle,fill,inner sep=1.5pt] at (18:1.2) {};

  \draw (90:2.2) -- (162:2.2) -- (234:2.2) -- (306:2.2) -- (18:2.2) -- (90:2.2);
  \draw (90:1.2) -- (306:1.2) -- (162:1.2) -- (18:1.2) -- (234:1.2) -- (90:1.2);
  \draw (90:2.2) -- (90:1.2);
  \draw (162:2.2) -- (162:1.2);
  \draw (234:2.2) -- (234:1.2);
  \draw (306:2.2) -- (306:1.2);
  \draw (18:2.2) -- (18:1.2);
\end{tikzpicture}
```
::::

Graf ini dikenal sebagai **graf Petersen**. Namun, kita harus berhati-hati.
Ingat bahwa graf Petersen bukan graf planar. Ini berarti bahwa di bidang real,
sel-sel-$1$ harus berpotongan, yang berarti bahwa ini bukan kompleks CW.
Akan tetapi, kita dapat membenamkan graf ini (dan juga setiap graf hingga
lainnya) ke dalam $\mathbb R^3$ tanpa perpotongan antar-sel-$1$, sehingga graf
ini mempunyai representasi kompleks CW.
:::

::: {.example #o012-fom-u006-ex-sphere-two data-origin="source-derived" data-source-lines="3335-3365"}
**Contoh (suatu struktur seluler pada $S^2$).** Kita dapat mendefinisikan
kompleks seluler bagi $S^2$ dengan menetapkan
$X^{(0)}=\set{v}$ dan mengambil

$$
X^{(1)}=X^{(0)}\sqcup\D^1/\varphi_1,
$$

dengan

$$
\varphi_1\colon\partial\D^1\longrightarrow\set{v}
$$

sebagai pemetaan konstan. Kemudian kita merekatkan dua cakram-$2$ lagi dengan
peta pelekatan yang mengirim batas masing-masing ke $\phi_1(\D^1)$. Kita
memperoleh gambaran seperti berikut.

:::: {.figure #o012-fom-u006-fig-sphere-two-construction data-origin="source-derived" data-source-lines="3343-3363" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Konstruksi berlangsung dalam tiga tahap: satu simpul
$v$; kemudian satu sel-$1$ yang kedua titik ujungnya dilekatkan pada $v$ dan
karena itu membentuk sebuah lingkaran; kemudian dua sel-$2$ yang dilekatkan
sepanjang lingkaran tersebut dan bersama-sama membentuk $S^2$.

```tex
\tikz[eqpic]{
  \node[circle, fill, inner sep=1.5pt] (v) at (0,0) {};
} \quad\taking{\qquad}\quad
\tikz[eqpic,scale=0.7]{
  \node[circle, fill, inner sep=1.5pt] (v) at (2,0) {};
  \draw (-2,0) arc
    [start angle=180, end angle=360, x radius=2cm, y radius=0.35cm];
  \draw (2,0) arc
    [start angle=0, end angle=180, x radius=2cm, y radius=0.35cm];
} \quad\taking{\qquad}\quad
\tikz[eqpic,scale=0.7]{
  \node[circle, fill, inner sep=1.5pt] (v) at (2,0) {};
  \draw (-2,0) arc
    [start angle=180, end angle=360, x radius=2cm, y radius=0.35cm];
  \draw[dashed] (2,0) arc
    [start angle=0, end angle=180, x radius=2cm, y radius=0.35cm];
  \draw (0,0) circle (2cm);
}
```
::::

Perhatikan bahwa struktur ini bukan kompleks-$\Delta$.
:::

::: {.example #o012-fom-u006-ex-sphere-n data-origin="source-derived" data-source-label="exmp:cw-for-sn-one-n-cell" data-source-lines="3367-3389"}
**Contoh (satu sel-$0$ dan satu sel-$n$ pada $S^n$).** Kita juga dapat
membangun kompleks seluler bagi $S^n$ dengan menetapkan

$$
X^{(0)}=\set{x_0}
$$

dan $X^{(i)}=X^{(0)}$ untuk $1\leq i<k$, lalu menambahkan satu sel-$n$
melalui $(\D^n,\varphi)$ sedemikian rupa sehingga

$$
\varphi\colon\partial\D^n\longrightarrow X
$$

adalah pemetaan konstan $\varphi(x)=x_0$. Perhatikan bahwa struktur ini bukan
kompleks-$\Delta$. Konstruksi umumnya tampak seperti berikut.

:::: {.figure #o012-fom-u006-fig-sphere-n-construction data-origin="source-derived" data-source-lines="3376-3388" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Pada setiap kerangka dari dimensi $0$ sampai $n-1$
hanya terdapat titik $x_0$. Pada tahap terakhir dilekatkan satu sel-$n$ dengan
seluruh batasnya dikirim ke $x_0$, sehingga hasilnya adalah sfera-$n$ dengan
satu titik yang ditandai.

```tex
\tikz[eqpic]{
  \node[circle, fill, inner sep=1.5pt] (v) at (0,0) {};
} \quad\taking{\qquad}\quad
\tikz[eqpic]{
  \node[circle, fill, inner sep=1.5pt] (v) at (0,0) {};
} \quad\taking{\qquad}\quad \cdots \quad\taking{\qquad}\quad
\tikz[eqpic]{
  \node[circle, fill, inner sep=1.5pt] (v) at (0,0) {};
} \quad\taking{\qquad}\quad
\text{$n$-sphere with a point}
```
::::
:::

::: {.remark #o012-fom-u006-rem-many-sphere-cells data-origin="source-derived" data-source-lines="3391-3397"}
**Catatan.** Kita juga dapat membangun kompleks CW bagi $S^2$ dengan sangat
banyak sel, sehingga bentuknya menyerupai bola basket atau bola sepak. Kita
juga dapat sekadar mentriangulasi $S^2$ sebagaimana yang kita lakukan untuk
kompleks-$\Delta$. Namun, cara-cara ini tidak akan terbukti sangat efisien
ketika kita mencoba menghitung homologi kompleks tersebut.
:::

::: {.example #o012-fom-u006-ex-torus data-origin="source-derived" data-source-label="exmp:cw-for-torus" data-source-lines="3399-3441"}
**Contoh (torus).** Kita dapat membangun kompleks CW bagi torus $T^2$ dengan
memperhatikan bahwa

:::: {.figure #o012-fom-u006-fig-torus-cw data-origin="source-derived" data-source-lines="3401-3434" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Persegi fundamental torus mempunyai pasangan sisi
mendatar berlabel $b$ dengan orientasi yang sama dan pasangan sisi tegak
berlabel $a$ dengan orientasi yang sama. Setelah keempat titik sudut
diidentifikasi, batas persegi menjadi buket dua loop berarah $a$ dan $b$ yang
bertemu pada satu simpul; bagian dalam persegi menjadi satu sel-$2$.

```tex
T^2 \,\,\cong\,\,
\tikz[eqpic,scale=0.7]{
  \draw[pattern=north west lines,opacity=0.7,pattern color=green]
    (-2,-2) -- (-2,2) -- (2,2) -- (2,-2) -- cycle;
  \draw[->-=4/0.7,red] (-2,2) -- (2,2);
  \draw[-<-=4/0.7,blue] (2,2) -- (2,-2);
  \draw[-<-=4/0.7,red] (2,-2) -- (-2,-2);
  \draw[->-=4/0.7,blue] (-2,-2) -- (-2,2);
  \node[fill, circle, inner sep=1.5pt] (r1) at (-2,-2) {};
  \node[fill, circle, inner sep=1.5pt] (r2) at (2,2) {};
  \node[fill, circle, inner sep=1.5pt] (r3) at (2,-2) {};
  \node[fill, circle, inner sep=1.5pt] (r4) at (-2,2) {};
  \node[label=left:$a$] (a1) at (-2,0) {};
  \node[label=right:$a$] (a2) at (2,0) {};
  \node[label=above:$b$] (b1) at (0,2) {};
  \node[label=below:$b$] (b2) at (0,-2) {};
}
\,\, \cong\,\,
\tikz[eqpic,scale=1.2]{
  \draw[pattern=north west lines,opacity=0.7,pattern color=green]
    (1,0) circle (1cm) {};
  \draw[pattern=north west lines,opacity=0.7,pattern color=green]
    (-1,0) circle (1cm) {};
  \begin{scope}[xscale=-1]
  \draw[blue,<--] (0:2) arc[start angle=0, end angle=-360, radius=1];
  \end{scope}
  \draw[red,-->] (0:2) arc[start angle=0, end angle=360, radius=1];
  \node[fill, circle, inner sep=1.5pt] (r1) at (0,0) {};
  \node[label=left:$a$] (a) at (-2,0) {};
  \node[label=right:$b$] (b) at (2,0) {};
}
```
::::

Jadi kita hanya memerlukan satu sel-$0$ yang dilambangkan $e^0$, dua sel-$1$
yang dilambangkan $e^1_a$ dan $e^1_b$ dengan batas yang dilekatkan pada
$e^0$, serta satu sel-$2$ yang dilambangkan $e^2$. Peta pelekatan merekatkan
batas sel-$2$ itu sepanjang kata

$$
aba^{-1}b^{-1},
$$

dengan loop $a$ dan $b$ masing-masing merepresentasikan sel-$1$ $e^1_a$ dan
$e^1_b$.
:::

::: {.example #o012-fom-u006-ex-real-projective-space data-origin="source-derived" data-source-lines="3443-3501"}
**Contoh (ruang projektif real).** Ruang $\mathbb{RP}^n$ adalah ruang garis
di $\mathbb R^{n+1}$ yang melalui titik asal:

$$
\mathbb R^{n+1}-\set{0}\big/x\sim\lambda x.
$$

Secara khusus, kita memperoleh bahwa $\mathbb{RP}^0$ hanyalah satu titik,
$\D^0=\set{*}$. Kita juga mengetahui bahwa $\mathbb{RP}^n$ homeomorfik dengan
$S^n/x\sim -x$. Karena itu, untuk $\mathbb{RP}^1$ kita memperoleh

:::: {.figure #o012-fom-u006-fig-rp-one data-origin="source-derived" data-source-lines="3447-3466" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Sfera-$1$ dengan pasangan titik antipodal yang
diidentifikasi dapat digambar sebagai dua busur berarah di antara satu pasangan
titik yang menjadi simpul $v$. Setelah kedua ujung diidentifikasi, kedua busur
menyusun satu lingkaran berarah. Jadi $\mathbb{RP}^1\cong S^1$.

```tex
\RP^1 =
\tikz[eqpic]{
  \draw[<--] (90:1) arc[start angle=90, end angle=-90, radius=1];
  \draw[<--] (-90:1) arc[start angle=-90, end angle=-270, radius=1];
  \node[fill, circle, inner sep=1.5pt, label=left:$v$] (v1) at (-1,0) {};
  \node[fill, circle, inner sep=1.5pt, label=right:$v$] (v2) at (1,0) {};
} =
\tikz[eqpic]{
  \draw[-->] (90:0) arc[start angle=90, end angle=270+360, radius=1];
  \draw[-->] (0:0) arc[start angle=-90, end angle=90+360, radius=1];
  \node[fill, circle, inner sep=1.5pt, label=above:$v$] (v) at (0,0) {};
} =
\tikz[eqpic]{
  \draw[-->] (0:0) arc[start angle=90, end angle=90+360, radius=1];
  \node[fill, circle, inner sep=1.5pt, label=above:$v$] (v) at (0,-2) {};
} = S^1
```
::::

Jadi $S^1\cong\mathbb{RP}^1$ (tetapi ini merupakan suatu anomali). Hal ini
menunjukkan bahwa kita dapat membangun kompleks CW bagi $\mathbb{RP}^1$
dengan melekatkan satu sel-$1$ pada satu sel-$0$ melalui cara yang jelas.
Secara ekuivalen, kita melekatkan satu sel-$1$ pada $\mathbb{RP}^0$.

Ketika meninjau $\mathbb{RP}^2$, kita memperoleh sfera-$2$ dengan titik-titik
antipodal yang diidentifikasi. Ruang ini sama dengan belahan atas sfera-$2$,
dengan titik-titik antipodal pada khatulistiwa direkatkan seperti pada satu
salinan $\mathbb{RP}^1$. Kita akan sedikit menyalahgunakan notasi dan
melambangkan khatulistiwa $\mathbb{RP}^2$ dengan $\mathbb{RP}^1$.

:::: {.figure #o012-fom-u006-fig-rp-two data-origin="source-derived" data-source-lines="3472-3495" data-rendering="source-tikz-preserved"}
**Gambar semantik.** Kuosien sfera-$2$ oleh identifikasi antipodal dapat
direpresentasikan oleh satu belahan sfera. Pada lingkaran khatulistiwanya,
setiap titik masih diidentifikasi dengan titik antipodalnya; kuosien
khatulistiwa itu adalah $\mathbb{RP}^1$.

```tex
\RP^2 =
\tikz[eqpic,scale=0.7]{
  \draw (-2,0) arc
    [start angle=180, end angle=360, x radius=2cm, y radius=0.35cm];
  \draw[dashed] (2,0) arc
    [start angle=0, end angle=180, x radius=2cm, y radius=0.35cm];
  \draw (0,0) circle (2cm);
} \,/\, \forall x(x \sim -x) =
\tikz[eqpic,scale=0.7]{
  \draw (-2,0) arc
    [start angle=180, end angle=360, x radius=2cm, y radius=0.35cm];
  \draw[dashed] (2,0) arc
    [start angle=0, end angle=180, x radius=2cm, y radius=0.35cm];
  \draw[] (2,0) arc
    [start angle=0, end angle=180, radius=2cm];
} \,/\,\forall x \in \RP^1(x \sim -x)
```
::::

Hal ini menunjukkan bahwa kita dapat membangun kompleks CW bagi
$\mathbb{RP}^2$ dengan melekatkan satu sel-$2$ pada $\mathbb{RP}^1$.
Pola ini berlanjut. Dengan cara ini, untuk setiap $n$ kita dapat membangun
kompleks CW bagi $\mathbb{RP}^n$ yang mempunyai satu sel-$i$ untuk setiap
$0\leq i\leq n$.
:::

::: {.remark #o012-fom-u006-rem-rp-inductive data-origin="source-derived" data-source-lines="3503-3509"}
**Catatan.** Secara formal, pola konstruksi induktif ruang projektif real
adalah

$$
\mathbb{RP}^n\cong
\mathbb{RP}^{n-1}\sqcup\bigsqcup\D^n
\big/\set{x\sim\varphi(x)},
$$

dengan

$$
\varphi_{\alpha}\colon
\partial\D^n_{\alpha}\longrightarrow\mathbb{RP}^{n-1}
$$

yang didefinisikan melalui cara alamiah.
:::

::: {.exercise #o012-fom-u006-ex-cp data-origin="source-derived" data-source-label="ex:cw-for-cp" data-source-lines="3511-3516"}
**Latihan.** Pikirkan suatu kompleks CW bagi $\mathbb{CP}^n$ (dengan satu sel
pada setiap dimensi genap). Secara khusus, hal ini menyiratkan bahwa

$$
\mathbb{CP}^1\cong S^2.
$$
:::

::: {.boundary #o012-fom-u006-boundary-draft}
**Batas sumber draf.** Draf ini menerjemahkan
`algebraic_topology.tex` baris 3123–3517 secara kontigu, yaitu seluruh Bagian
1.12 tentang kompleks seluler. Baris sumber berikutnya adalah 3518,
`\subsection{Cellular homology}`, awal Bagian 1.13. Tidak ada materi penguasaan
atau perbaikan sumber yang dimasukkan ke dalam draf ini.
:::

# Catatan audit untuk editor {.unnumbered #o012-fom-u006-draft-editorial-flags}

Bagian ini bukan bagian dari terjemahan sumber dan harus diputuskan pada tahap
admisibilitas kanonik.

1. **Baris 3245:** rumus konstruksi $X^{(n)}$ memakai
   $\D^1_{\alpha}$, sedangkan kalimat sebelumnya memperkenalkan
   $\D^n_{\alpha}$. Draf mempertahankan $\D^1_{\alpha}$ tepat seperti sumber;
   secara matematis ini tampaknya salah ketik untuk $\D^n_{\alpha}$.
2. **Baris 3272 dan 3288–3291:** sumber mula-mula menyebut anting-anting Hawaii
   sebagai “a CW complex”, lalu langsung menyatakan bahwa ruang itu bukan
   kompleks CW. Kontradiksi ini dipertahankan agar tidak ada koreksi diam-diam.
3. **Baris 3297–3332:** sumber mengaitkan status graf Petersen sebagai kompleks
   CW dengan ada-tidaknya pembenaman planar. Graf abstrak hingga sendiri dapat
   direalisasikan sebagai kompleks CW berdimensi satu; yang gagal di bidang
   adalah gambar dengan sisi yang saling berpotongan sebagai suatu pembenaman.
   Prosa sumber membutuhkan penajaman sebelum admisi kanonik.
4. **Baris 3250–3253:** kata “equivalent” pada klaim tentang kompleks CW dan
   kompleks-$\Delta$ tidak menyebut jenis ekuivalensi (homeomorfisma,
   ekuivalensi homotopi, atau ekuivalensi struktur). Draf menerjemahkannya
   secara netral sebagai “ekuivalen”.
5. **Baris 3371:** konstruksi $S^n$ memakai syarat $1\leq i<k$, tetapi tidak
   mendefinisikan $k$ dan kemudian langsung melekatkan sel-$n$. Draf
   mempertahankan $k$; tampaknya yang dimaksud ialah $1\leq i<n$.
6. **Baris 3444–3445:** relasi $x\sim\lambda x$ tidak menyatakan syarat
   $\lambda\in\mathbb R^{\times}$. Tanpa syarat $\lambda\neq0$, rumus kuosien
   tidak lengkap.
7. **Baris 3506–3508:** rumus konstruksi $\mathbb{RP}^n$ menampilkan
   $\bigsqcup\D^n$ tanpa indeks, tetapi baris berikutnya memakai
   $\varphi_{\alpha}$ dan $\D^n_{\alpha}$. Maksud jumlah koproduk/keluarga sel
   tidak dinyatakan secara konsisten; untuk dekomposisi yang baru saja
   dijelaskan, hanya satu sel-$n$ diperlukan.
8. **Definisi keseluruhan, baris 3134–3266:** konstruksi skeleta dan topologi
   lemah untuk dimensi tak hingga diberikan, tetapi syarat “closure-finite”
   yang lazim dijelaskan oleh huruf C dalam CW tidak disebutkan. Perlu diputuskan
   apakah edisi kanonik akan menambah klarifikasi terpisah tanpa menisbahkannya
   kepada sumber.
9. **Baris 3511–3516:** satu-satunya latihan sumber dalam bagian ini tidak
   mempunyai petunjuk atau solusi. Itu bukan kehilangan pada terjemahan, tetapi
   merupakan celah self-study yang harus ditutup oleh lapisan penguasaan pada
   tahap berikutnya.
