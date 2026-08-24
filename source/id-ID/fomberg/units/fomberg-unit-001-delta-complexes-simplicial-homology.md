---
title: "Topologi Aljabar"
subtitle: "Komponen Fomberg 1: Kompleks-Delta dan Homologi Simpleksial"
author:
  - "Yeheli Fomberg (catatan sumber; berdasarkan kuliah Nir Lazarovich)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Sumber dan adaptasi: CC BY-SA 4.0; lihat atribusi dan catatan perubahan di bawah."
source_component: "Fomberg Algebraic Topology, Sections 1.1-1.2"
edition_unit_id: "O012-FOM-001"
course_route_unit_id: "D60-R08"
---

# Tentang komponen ini {.unnumbered #o012-fom-u001-notice data-course-route-unit-id="D60-R08"}

Komponen ini merupakan terjemahan dan adaptasi bahasa Indonesia atas bagian
awal *Algebraic Topology* karya Yeheli Fomberg, berdasarkan kuliah Nir
Lazarovich pada musim semi 2025. Otoritas sumber dibekukan pada commit
[563194fae879178b9a6871b249513bfc27968975](https://git.sr.ht/~yp/math-notes/tree/563194fae879178b9a6871b249513bfc27968975/item/algebraic_topology.tex).
Rentang yang diterjemahkan ialah baris 31–614, Bagian 1.1–1.2: 584 baris fisik,
21.875 byte setelah normalisasi LF dan satu LF penutup, dengan SHA-256
68cb0dea7aa24a42e979877a95acf61b8152c87ed86d88ad7deac7cb5cea2fe3.

Catatan sumber tersedia di bawah
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
Terjemahan, pemformatan semantik, koreksi terbatas, dan materi penguasaan asli
di bawah ini diterbitkan dengan lisensi yang sama. Perubahan meliputi
penerjemahan, pemberian pengenal stabil, penggambaran ulang diagram secara
reflow dan dapat diakses, serta pembetulan salah ketik yang dicatat satu per
satu dalam audit. Blok yang seluruhnya dikomentari sebagai rencana “akan
ditambahkan” dalam TeX tidak diperlakukan sebagai isi pembaca.

Edisi ini independen dan tidak menyiratkan dukungan, pengesahan, atau afiliasi
dengan Yeheli Fomberg, Nir Lazarovich, ataupun institusi mereka. Produksi
terjemahan, struktur semantik, dan QA dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna. Tidak ada prosa dari
bank soal Fomberg yang dikecualikan ataupun materi MIT yang disalin ke unit ini.

# Homologi {#o012-fom-u001}

## Kompleks-$\Delta$ {#o012-fom-u001-s01 data-source-lines="31-345"}

Dalam topologi aljabar, kita mempelajari pemetaan yang membawa ruang topologis
ke data aljabar:

$$
\{\text{ruang topologis}\}\longrightarrow\{\text{data aljabar}\}.
$$

Salah satu contohnya ialah pemetaan $\pi_0(X)$ yang muncul dalam topologi
himpunan-titik:

$$
X\longmapsto
\pi_0(X)=\{\text{komponen terhubung lintasan}\}.
$$

Contoh lain ialah $\pi_1(X)$:

$$
(X,x_0)\longmapsto
\pi_1(X,x_0)
=\{\text{grup fundamental }X\text{ dengan titik dasar }x_0\}.
$$

::: {.remark #o012-fom-u001-rem-001 data-source-lines="48-50"}
**Catatan.** Untuk $n\geq1$ dan ruang bertitik $(X,x_0)$, unsur
$\pi_n(X,x_0)$ adalah kelas
homotopi bertitik dari pemetaan bertitik

$$
(S^n,s_0)\longrightarrow(X,x_0),
$$

bukan pemetaan mentah tanpa relasi homotopi.
:::

::: {.source-audit #o012-fom-u001-audit-pi-n}
**Audit sumber.** Baris 49 hanya mengatakan bahwa unsur $\pi_n$ “adalah
pemetaan dari $S^n$”. Edisi menambahkan titik dasar dan kelas homotopi yang
diperlukan oleh definisi grup homotopi.
:::

::: {.definition #o012-fom-u001-def-001 data-source-lines="52-56"}
**Definisi (vektor bebas afin).** Misalkan
$v_0,\ldots,v_n\in\mathbb R^m$ dengan $n\leq m$. Vektor-vektor ini disebut
**bebas afin** jika

$$
v_1-v_0,\ldots,v_n-v_0
$$

bebas linear.
:::

::: {.source-audit #o012-fom-u001-audit-affine-ambient}
**Audit sumber.** Baris 53 menempatkan $v_0,\ldots,v_n$ hanya di
$\mathbb R^n$, sedangkan definisi simpleks berikutnya memakai ruang ambien
$\mathbb R^m$. Edisi menyatakan bentuk umum yang konsisten:
$v_i\in\mathbb R^m$ dengan syarat dimensi perlu $n\leq m$.
:::

::: {.definition #o012-fom-u001-def-002 data-source-lines="58-61"}
**Definisi (simpleks-$n$).** Sebuah **simpleks-$n$** ialah selubung konveks
dari $n+1$ titik bebas afin di $\mathbb R^m$.
:::

::: {.example #o012-fom-u001-exa-001 data-source-lines="63-68"}
**Contoh.** Simpleks-$0$ adalah sebuah titik; simpleks-$1$ adalah sebuah ruas;
simpleks-$2$ adalah sebuah segitiga; dan simpleks-$3$ adalah sebuah
tetrahedron.
:::

::: {.definition #o012-fom-u001-def-003 data-source-lines="70-76"}
**Definisi (simpleks-$n$ standar).** Simpleks-$n$ standar ialah selubung
konveks dari $n+1$ vektor satuan di $\mathbb R^{n+1}$:

$$
\Delta^n:=[e_0,\ldots,e_n].
$$
:::

::: {.source-audit #o012-fom-u001-audit-001}
**Audit sumber.** Baris 74 memakai glif segitiga yang berbeda dan indeks akhir
$N$, sedangkan bagian selanjutnya memakai $\Delta^n$. Indeks akhir harus $n$,
sesuai frasa “$n+1$ vektor satuan”, dan simbol simpleks perlu konsisten. Edisi
menormalkan bentuknya menjadi
$\Delta^n=[e_0,\ldots,e_n]$.
:::

::: {.remark #o012-fom-u001-rem-002 data-source-lines="77-83"}
**Catatan.** Simpleks $\Delta^n$ memparametrisasi setiap simpleks-$n$ lain.
Untuk $[v_0,\ldots,v_n]$, pemetaannya ialah

$$
(t_0,t_1,\ldots,t_n)
\longmapsto
\sum_{i=0}^{n}t_iv_i.
$$
:::

::: {.definition #o012-fom-u001-def-004 data-source-lines="85-93"}
**Definisi (pemetaan barisentris).** Pemetaan

$$
b_{[v_0,\ldots,v_n]}\colon
\Delta^n\longrightarrow[v_0,\ldots,v_n]
$$

disebut **pemetaan barisentris**. Rumusnya

$$
b_{[v_0,\ldots,v_n]}(t_0,t_1,\ldots,t_n)
=\sum_{i=0}^{n}t_iv_i.
$$
:::

::: {.definition #o012-fom-u001-def-005 data-source-lines="95-102"}
**Definisi (muka).** Untuk setiap $0\leq i\leq n$, muka ke-$i$ dari
$[v_0,\ldots,v_n]$ ialah

$$
[v_0,\ldots,\widehat v_i,\ldots,v_n]
=[v_0,\ldots,v_{i-1},v_{i+1},\ldots,v_n].
$$
:::

::: {.source-audit #o012-fom-u001-audit-002}
**Audit sumber.** Baris 95–101 memulai daftar pada $v_1$ dan membatasi indeks
ke $1\leq i\leq n$, sedangkan semua penggunaan berikutnya memakai
$v_0,\ldots,v_n$ dan $0\leq i\leq n$. Edisi menyelaraskan definisi dengan
konvensi berikutnya.
:::

::: {.remark #o012-fom-u001-rem-003 data-source-lines="103-107"}
**Catatan.** Setiap muka dari $[v_0,\ldots,v_n]$ merupakan
simpleks-$(n-1)$.
Urutan simpul pada muka diwarisi dari urutan simpleks-$n$ semula.
:::

::: {.definition #o012-fom-u001-def-006 data-source-lines="109-116"}
**Definisi (batas simpleks).** Misalkan $\Delta^n$ sebuah simpleks. Batasnya
didefinisikan oleh

$$
\partial\Delta^n
=\bigcup\{\text{muka-muka }\Delta^n\}.
$$

Bagian dalam simpleks ialah

$$
\mathring{\Delta}^n=\Delta^n-\partial\Delta^n.
$$
:::

::: {.definition #o012-fom-u001-def-delta-complex
data-source-label="def:sigma-complex" data-source-lines="118-134"}
**Definisi (kompleks-$\Delta$).** Struktur kompleks-$\Delta$ pada ruang
topologis $X$ ialah suatu koleksi pemetaan kontinu

$$
\{\sigma_\alpha\colon\Delta^{n_\alpha}\to X\}_\alpha
$$

yang memenuhi:

1. pembatasan
   $\sigma_\alpha|_{\mathring{\Delta}^{n_\alpha}}$ injektif, dan setiap
   $x\in X$ berada dalam citra tepat satu pembatasan semacam itu;
2. pembatasan $\sigma_\alpha$ pada suatu muka $\Delta^{n_\alpha}$ sama dengan
   suatu $\sigma_\beta$ setelah identifikasi afin standar muka tersebut; dan
3. $U\subset X$ terbuka jika dan hanya jika
   $\sigma_\alpha^{-1}(U)\subset\Delta^{n_\alpha}$ terbuka untuk setiap
   $\alpha$.
:::

::: {.remark #o012-fom-u001-rem-004 data-source-lines="136-144"}
**Catatan tentang syarat 2.** Dalam
[definisi kompleks-$\Delta$](#o012-fom-u001-def-delta-complex), pernyataan itu
berarti

$$
\sigma_\beta
=\sigma_\alpha\circ
b_{[v_0,\ldots,\widehat v_i,\ldots,v_n]}
\colon\Delta^{n-1}\longrightarrow X,
$$

yang ekuivalen dengan pembatasan
$\sigma_\alpha$ pada muka ke-$i$.
:::

::: {.remark #o012-fom-u001-rem-005 data-source-lines="146-151"}
**Catatan notasi.** Kadang-kadang $\Delta_n$ menyatakan himpunan semua
simpleks berdimensi $n$. Jadi $\Delta_0$ adalah himpunan semua simpul,
$\Delta_1$ himpunan semua sisi, dan seterusnya.
:::

::: {.example #o012-fom-u001-exa-circle
data-source-lines="153-170"}
**Contoh (kompleks-$\Delta$ pada $S^1$).** Ambil $S^1$, lingkaran satuan dalam
$\mathbb R^2$. Strukturnya terdiri atas

$$
v\colon\Delta^0\to S^1,
\qquad
e\colon\Delta^1\to S^1.
$$

Pemetaan $v$ membawa satu-satunya titik $\Delta^0$ ke simpul $v$.
Pemetaan $e$ membawa bagian dalam interval
$\Delta^1=[v_0,v_1]$ satu-satu ke lingkaran tanpa $v$, sedangkan kedua titik
ujungnya dibawa ke $v$.
:::

::: {.figure #o012-fom-u001-fig-001 data-source-lines="156-162"}
**Gambar semantik (lingkaran satu simpul).** Sebuah loop terarah searah jarum
jam berlabel $e$ berawal dan berakhir pada satu simpul berlabel $v$. Ini
menggambar ulang panah melingkar dan satu titik yang terdapat dalam TikZ
sumber, sambil mempertahankan data pelekatan kedua ujung $e$ ke $v$.
:::

::: {.remark #o012-fom-u001-rem-006 data-source-lines="172-181"}
**Catatan (bukan contoh bagi topologi standar).** Jangan memberi satu
simpleks-$0$ yang berbeda kepada setiap titik $S^1$. Syarat 3 pada
[definisi kompleks-$\Delta$](#o012-fom-u001-def-delta-complex) akan membuat
setiap subhimpunan $S^1$ terbuka. Struktur patologis itu bukan
kompleks-$\Delta$ bagi lingkaran dengan topologi standarnya, tetapi sah bagi
himpunan titik yang sama dengan topologi diskret.
:::

::: {.example #o012-fom-u001-exa-torus data-source-lines="183-214"}
**Contoh (kompleks-$\Delta$ pada torus $T^2$).** Ambil
$T^2=S^1\times S^1$. Model persegi yang sisi-sisi berhadapannya
diidentifikasi dibelah oleh diagonal menjadi dua segitiga. Struktur
kompleks-$\Delta$ terdiri atas

$$
r\colon\Delta^0\to T^2,
\qquad
e,f,g\colon\Delta^1\to T^2,
\qquad
V,L\colon\Delta^2\to T^2.
$$

Keempat sudut persegi mewakili simpul $r$. Pasangan sisi tegak berlabel $e$,
pasangan sisi mendatar berlabel $f$, dan diagonal berlabel $g$. Segitiga atas
berlabel $V$ dan segitiga bawah berlabel $L$.
:::

::: {.figure #o012-fom-u001-fig-002 data-source-lines="185-210"}
**Gambar semantik (persegi fundamental torus).** Persegi dibelah oleh diagonal
dari sudut kiri bawah ke sudut kanan atas. Keempat sudut diidentifikasi menjadi
$r$; sisi-sisi tegak menjadi $e$ dan sisi-sisi mendatar menjadi $f$. Kedua
sisi mendatar berarah ke kanan, kedua sisi tegak berarah ke atas, dan diagonal
$g$ berarah dari sudut kiri bawah ke sudut kanan atas.
Daerah kiri-atas $V$ diberi orientasi searah jarum jam, sedangkan daerah
kanan-bawah $L$ diberi orientasi berlawanan arah jarum jam. Arsiran berbeda
pada kedua segitiga dalam sumber berfungsi membedakan $V$ dan $L$.
:::

::: {.source-audit #o012-fom-u001-audit-003}
**Audit sumber.** Judul contoh pada baris 183 mencetak $T^1$, tetapi baris 184
mendefinisikan $T=S^1\times S^1$, yaitu torus dua-dimensi $T^2$. Edisi
memakai $T^2$.
:::

::: {.example #o012-fom-u001-exa-rp2
data-source-label="exmp:delta-complex-rp2" data-source-lines="216-261"}
**Contoh (kompleks-$\Delta$ pada $\mathbb{RP}^2$).** Tulis

$$
\mathbb{RP}^2
:=D^2/\bigl(x\sim-x\text{ untuk setiap }x\in S^1\bigr).
$$

Model persegi yang ditriangulasi memberi koleksi

$$
r,w\colon\Delta^0\to\mathbb{RP}^2,
\qquad
e,f,g\colon\Delta^1\to\mathbb{RP}^2,
\qquad
V,L\colon\Delta^2\to\mathbb{RP}^2.
$$

Model cakram di sebelah kanan gambar sumber hanyalah ruang hasil bagi yang
mewakili bidang projektif real; model cakram itu sendiri bukan
kompleks-$\Delta$ yang sedang dinyatakan.
:::

::: {.figure #o012-fom-u001-fig-003 data-source-lines="219-254"}
**Gambar semantik (dua model $\mathbb{RP}^2$).**

1. Pada model kiri, sebuah persegi dibelah oleh diagonal kiri-bawah ke
   kanan-atas. Sudut kiri-bawah dan kanan-atas berlabel $r$; dua sudut lain
   berlabel $w$. Sisi tegak berlabel $e$, sisi mendatar berlabel $f$, diagonal
   berlabel $g$, dan kedua segitiga berlabel $V$ serta $L$. Sisi atas berarah
   ke kiri sedangkan sisi bawah berarah ke kanan; sisi kiri berarah ke atas
   sedangkan sisi kanan berarah ke bawah. Pasangan arah berlawanan inilah yang
   mencatat identifikasi sisi pada model persegi $\mathbb{RP}^2$.
2. Pada model kanan, sebuah cakram mempunyai pasangan titik antipodal pada
   lingkaran batas yang diidentifikasi. Busur batas berlabel $e$; panah yang
   ditandai pada sisi kiri lingkaran mengarah ke bawah, sedangkan panah pada
   sisi kanan mengarah ke atas. Model ini menjelaskan hasil bagi
   $D^2/(x\sim-x)$ tanpa memerlukan gambar sumber untuk memulihkan arah.
:::

::: {.remark #o012-fom-u001-rem-order data-source-label="rem:order"
data-source-lines="263-278"}
**Catatan (orientasi muka).** Dalam
[contoh $\mathbb{RP}^2$](#o012-fom-u001-exa-rp2), semua sisi pada muka $V$
dan $L$ harus muncul dalam urutan yang tepat. Jika

$$
V\colon[v_0,v_1,v_2]\longrightarrow\mathbb{RP}^2,
$$

maka syarat 2 pada
[definisi kompleks-$\Delta$](#o012-fom-u001-def-delta-complex) menuntut agar

$$
V|_{[v_0,v_1]},\qquad
V|_{[v_1,v_2]},\qquad
V|_{[v_0,v_2]}
$$

semuanya merupakan pemetaan dalam kompleks-$\Delta$. Panah melingkar pada
gambar mencatat apakah urutan $v_0,v_1,v_2$ searah atau berlawanan arah jarum
jam. Dalam kasus yang digambar, orientasi $V$ berlawanan arah jarum jam dan

$$
V|_{[v_0,v_1]}=g,\qquad
V|_{[v_1,v_2]}=f,\qquad
V|_{[v_0,v_2]}=e.
$$

Karena itu semua sisi yang diperlukan memang ada. Tanpa kecocokan ini,
struktur tersebut bukan kompleks-$\Delta$.
:::

::: {.remark #o012-fom-u001-rem-007 data-source-lines="280-284"}
**Catatan.** Ruang $X$ ditentukan oleh data kompleks-$\Delta$: kompleks CW
yang dihasilkan oleh data tersebut homeomorfik dengan $X$.
:::

::: {.definition #o012-fom-u001-def-simplicial-complex
data-source-label="def:simplicial-complex" data-source-lines="286-295"}
**Definisi (kompleks simpleksial).** Sebuah **kompleks simpleksial** ialah
kompleks-$\Delta$ sedemikian sehingga setiap simpleks
$\sigma_\alpha\colon\Delta^n\to X$ memenuhi:

1. $\sigma_\alpha$ injektif; cukup memeriksa keinjektifannya pada simpul; dan
2. $\sigma_\alpha$ ditentukan oleh simpul-simpulnya.
:::

::: {.example #o012-fom-u001-exa-004 data-source-lines="297-309"}
**Contoh.** Segitiga dengan tiga simpul $v_0,v_1,v_2$, tiga sisi berorientasi
$[v_0,v_1]$, $[v_1,v_2]$, $[v_0,v_2]$, dan satu muka
$[v_0,v_1,v_2]$ adalah salah satu contoh paling sederhana.
:::

::: {.figure #o012-fom-u001-fig-004 data-source-lines="299-308"}
**Gambar semantik (segitiga berorientasi).** Simpul $v_0$ berada di kiri
bawah, $v_1$ di kanan bawah, dan $v_2$ di kanan atas. Panah sisi berjalan
$v_0\to v_1$, $v_1\to v_2$, dan $v_0\to v_2$, tepat seperti pada TikZ sumber.
:::

::: {.example #o012-fom-u001-exa-005 data-source-lines="311-334"}
**Bukan contoh kompleks simpleksial.** Dua kompleks-$\Delta$ berikut bukan
kompleks simpleksial.

1. Satu loop $e$ dengan satu simpul $r$ gagal memenuhi syarat 1 karena
   $e\colon\Delta^1\to X$ tidak injektif.
2. Dua sisi berbeda $e$ dan $f$ yang menghubungkan pasangan simpul yang sama
   $v_0,v_1$ gagal memenuhi syarat 2 karena simpul-simpulnya tidak menentukan
   apakah simpleks itu $e$ atau $f$.
:::

::: {.figure #o012-fom-u001-fig-005 data-source-lines="314-328"}
**Gambar semantik (dua contoh yang bukan kompleks simpleksial).** Gambar kiri
ialah satu sisi melingkar $e$ yang kedua ujungnya melekat pada $r$. Gambar
kanan ialah dua busur sejajar $e$ dan $f$ dari $v_0$ ke $v_1$. Kedua gambar
mempertahankan titik, label, dan arah panah TikZ sumber.
:::

::: {.remark #o012-fom-u001-rem-008 data-source-lines="336-338"}
**Catatan.** Kompleks simpleksial menggeneralisasi graf sederhana.
:::

::: {.remark #o012-fom-u001-rem-009 data-source-lines="340-344"}
**Catatan.** Setiap ruang dapat ditutupi dengan memakai satu simpul bagi
setiap titik $X$, tetapi struktur yang dihasilkan adalah kompleks-$\Delta$
pada himpunan $X$ yang diberi topologi diskret.
:::

## Homologi simpleksial {#o012-fom-u001-s02 data-source-lines="346-614"}

::: {.definition #o012-fom-u001-def-007 data-source-lines="347-360"}
**Definisi (rantai).** Misalkan $X$ ruang topologis dengan struktur
kompleks-$\Delta$

$$
\{\sigma_\alpha^{n_\alpha}\colon
\Delta^{n_\alpha}\to X\}_\alpha.
$$

Untuk setiap $n\geq0$, grup $C_n^\Delta(X)$ dapat ditulis dengan salah satu
bentuk ekuivalen berikut:

$$
\begin{aligned}
C_n^\Delta(X)
&:=\text{grup abelian bebas dengan basis }
\{\sigma_\alpha^n\}_\alpha\\
&:=\bigoplus_\alpha\mathbb Z\sigma_\alpha^n\\
&:=\operatorname{span}_{\mathbb Z}\{\sigma_\alpha^n\}_\alpha\\
&:=\left\{
\sum_\alpha c_\alpha\sigma_\alpha^n
\ \middle|\
c_\alpha\in\mathbb Z,\ 
c_\alpha=0\text{ kecuali untuk berhingga banyak }\alpha
\right\}.
\end{aligned}
$$
:::

::: {.source-audit #o012-fom-u001-audit-005}
**Audit sumber.** Baris 350 menyatakan $n\geq1$, tetapi contoh berikutnya
memakai $C_0^\Delta(X)$. Definisi standar dan pemakaian sumber menuntut
$n\geq0$; edisi memakai rentang tersebut.
:::

::: {.remark #o012-fom-u001-rem-010 data-source-lines="362-364"}
**Catatan.** Unsur $C_n^\Delta(X)$ disebut **rantai-$n$**.
:::

::: {.example #o012-fom-u001-exa-006 data-source-lines="366-377"}
**Contoh (rantai pada $S^1$).** Untuk kompleks-$\Delta$ lingkaran satu simpul
dan satu sisi pada
[contoh sebelumnya](#o012-fom-u001-exa-circle),

$$
C_0^\Delta(S^1)=\mathbb Zv,
\qquad
C_1^\Delta(S^1)=\mathbb Ze,
$$

sedangkan $C_n^\Delta(S^1)=\{0\}$ untuk setiap $n\geq2$.
:::

::: {.figure #o012-fom-u001-fig-006 data-source-lines="368-374"}
**Gambar semantik (rantai lingkaran).** Sumber mengulang gambar loop $e$
searah jarum jam yang kedua ujungnya melekat pada simpul $v$; data rantai
derajat nol dan satu di atas adalah pembacaan aljabarnya.
:::

::: {.definition #o012-fom-u001-def-boundary data-source-lines="379-386"}
**Definisi (pemetaan batas).** Untuk $n\geq1$, pada unsur basis definisikan

$$
\partial_n\colon C_n^\Delta(X)\longrightarrow C_{n-1}^\Delta(X),
\qquad
\partial_n\sigma
=\sum_{i=0}^{n}(-1)^i
\sigma|_{[v_0,\ldots,\widehat v_i,\ldots,v_n]},
$$

lalu perluas secara linear. Tetapkan pula
$\partial_0\colon C_0^\Delta(X)\to0$ sebagai pemetaan nol; secara ekuivalen,
ambil $C_{-1}^\Delta(X)=0$.
:::

::: {.remark #o012-fom-u001-rem-011 data-source-lines="388-390"}
**Catatan.** Pemetaan batas adalah homomorfisma grup.
:::

::: {.example #o012-fom-u001-exa-007 data-source-lines="392-430"}
**Contoh (batas sisi dan segitiga).** Pandang objek berikut sebagai rantai
dalam suatu kompleks-$\Delta$.

Untuk sisi berorientasi $e=[v_0,v_1]$,

$$
\partial_1(e)
=e|_{[v_1]}-e|_{[v_0]}
=v_1-v_0.
$$

Untuk simpleks-$2$ berorientasi
$\sigma=[v_0,v_1,v_2]$, dengan label sisi $e_0,e_1,e_2$ seperti pada gambar,

$$
\begin{aligned}
\partial_2(\sigma)
&=\sigma|_{[v_1,v_2]}
-\sigma|_{[v_0,v_2]}
+\sigma|_{[v_0,v_1]}\\
&=e_0-e_1+e_2.
\end{aligned}
$$

Dalam praktik, rumus ini dapat dibaca dari orientasi: sebuah sisi mendapat
tanda minus jika orientasi yang diwarisinya berlawanan dengan orientasi sisi
yang dipilih.
:::

::: {.figure #o012-fom-u001-fig-007 data-source-lines="394-415"}
**Gambar semantik (sisi dan muka).** Gambar kiri ialah panah
$v_0\xrightarrow{e}v_1$. Gambar kanan ialah segitiga
$[v_0,v_1,v_2]$ berorientasi berlawanan arah jarum jam; sisi bawah
$v_0\to v_1$ berlabel $e_2$, sisi kanan $v_1\to v_2$ berlabel $e_0$, dan
diagonal $v_0\to v_2$ berlabel $e_1$. Karena diagonal dipakai dengan arah yang
berlawanan saat menelusuri batas, tandanya negatif.
:::

::: {.source-audit #o012-fom-u001-audit-006}
**Audit sumber.** Baris 418 memakai simbol $\sigma$ untuk pembatasan sisi
$e$, dan baris 422 mencetak $\sigma(\sigma)$ alih-alih
$\partial_2(\sigma)$. Bentuk sumber
$e_2+e_0-e_1$ identik secara aljabar dengan $e_0-e_1+e_2$; edisi hanya
mengurutkan kembali sukunya agar mengikuti urutan indeks muka, tanpa mengklaim
perubahan matematis pada tanda.
:::

::: {.example #o012-fom-u001-exa-008 data-source-lines="432-448"}
**Contoh (pemetaan batas pada $S^1$).** Untuk kompleks-$\Delta$ lingkaran,

$$
\partial_1\colon\mathbb Ze\longrightarrow\mathbb Zv.
$$

Jika $a\in\mathbb Z$, maka

$$
\partial_1(ae)
=a\,\partial_1(e)
=a(v-v)
=0.
$$

Jadi $\partial_1=0$.
:::

::: {.figure #o012-fom-u001-fig-008 data-source-lines="434-440"}
**Gambar semantik (batas loop).** Sumber kembali menggambar loop $e$ searah
jarum jam dengan satu simpul $v$. Kedua titik ujung simpleks standar mempunyai
citra yang sama, sehingga kedua suku batas saling meniadakan.
:::

::: {.source-audit #o012-fom-u001-audit-007}
**Audit sumber.** Baris 443 mencetak $a\in Z$, dan baris 445–447 memakai
$\sigma_1$ sebagai operator batas. Edisi menuliskan
$a\in\mathbb Z$ dan $\partial_1$.
:::

::: {.example #o012-fom-u001-exa-009 data-source-lines="450-496"}
**Contoh (pemetaan batas pada torus).** Untuk kompleks-$\Delta$ torus,
kompleks rantainya mempunyai bentuk

$$
\{0\}
\xrightarrow{\partial_3}
\mathbb ZV\oplus\mathbb ZL
\xrightarrow{\partial_2}
\mathbb Ze\oplus\mathbb Zf\oplus\mathbb Zg
\xrightarrow{\partial_1}
\mathbb Zr.
$$

Pada derajat satu,

$$
\partial_1(e)=r-r=0,\qquad
\partial_1(f)=r-r=0,\qquad
\partial_1(g)=r-r=0.
$$

Pada derajat dua,

$$
\partial_2(V)=e+f-g,
\qquad
\partial_2(L)=f+e-g.
$$
:::

::: {.figure #o012-fom-u001-fig-009 data-source-lines="452-484"}
**Gambar semantik (torus dan kompleks rantainya).** Sumber mengulang persegi
fundamental yang dibelah diagonal, dengan simpul $r$, sisi $e,f,g$, muka
$V,L$, pasangan panah sisi, arsiran, dan orientasi muka yang sama seperti
[gambar torus sebelumnya](#o012-fom-u001-fig-002). Di bawahnya, diagram
$0\to C_2\to C_1\to C_0$ menempatkan tepat grup-grup dan pemetaan batas yang
ditulis di atas.
:::

::: {.remark #o012-fom-u001-rem-012 data-source-lines="497-505"}
**Catatan.** Pemetaan karakteristik $V$ mempunyai domain simpleks-$2$
$[v_0,v_1,v_2]$; muka-mukanya ialah pembatasan $V$ pada ketiga
simpleks-$1$ $[v_0,v_1]$, $[v_1,v_2]$, dan $[v_0,v_2]$. Walaupun semua sudut
model torus dibawa ke titik $r$ yang sama, orientasi sisi telah menentukan
setiap pembatasan muka, sebagaimana dijelaskan dalam
[catatan orientasi](#o012-fom-u001-rem-order). Itulah yang menentukan tanda
sisi, misalnya kemunculan $-g$ pada batas $V$.
:::

::: {.source-audit #o012-fom-u001-audit-face-sign}
**Audit sumber.** Baris 504 menulis pembatasan muka sebagai
$V|_{[v_0,v_1]}=-g$. Tanda negatif tidak membentuk pemetaan karakteristik
simpleks baru: pembatasan mukanya tetap pemetaan simpleks $g$ (dengan
parametrisasi muka yang ditentukan), sedangkan $-g$ hanya berarti koefisien
rantai yang muncul setelah orientasi muka dibandingkan dengan orientasi basis
$g$. Edisi memisahkan kedua tingkat ini.
:::

::: {.lemma #o012-fom-u001-lem-boundary-square
data-source-label="lem:partial-partial-zero" data-source-lines="517-520"}
**Lema.** Untuk setiap $n\geq1$,

$$
\partial_{n-1}\circ\partial_n=0.
$$
:::

::: {.proof #o012-fom-u001-proof-001 data-source-lines="521-548"}
**Bukti.** Pernyataan dimaksudkan untuk $n\geq1$. Kasus $n=1$ langsung karena
$\partial_0=0$. Untuk $n\geq2$, cukup periksa unsur basis. Ambil
$\sigma=[v_0,\ldots,v_n]\in C_n^\Delta(X)$. Dari definisi,

$$
\partial_n\sigma
=\sum_{i=0}^{n}(-1)^i
\sigma|_{[v_0,\ldots,\widehat v_i,\ldots,v_n]}.
$$

Menerapkan $\partial_{n-1}$ sekali lagi memberi

$$
\begin{aligned}
(\partial_{n-1}\partial_n)(\sigma)
={}&
\sum_{i=0}^{n}\sum_{j<i}
(-1)^{i+j}\,
\sigma|_{[v_0,\ldots,\widehat v_j,\ldots,
\widehat v_i,\ldots,v_n]}\\
&+
\sum_{i=0}^{n}\sum_{j>i}
(-1)^{i+j-1}\,
\sigma|_{[v_0,\ldots,\widehat v_i,\ldots,
\widehat v_j,\ldots,v_n]}.
\end{aligned}
$$

Untuk setiap pasangan $p<q$, muka yang menghapus $v_p$ dan $v_q$ muncul dua
kali: sekali dengan koefisien $(-1)^{p+q}$ dan sekali dengan koefisien
$(-1)^{p+q-1}$. Kedua koefisien berjumlah nol. Semua suku berpasangan dengan
cara ini, sehingga

$$
(\partial_{n-1}\circ\partial_n)(\sigma)=0.
$$

Karena pemetaan batas linear, kesimpulan berlaku bagi setiap rantai. $\square$
:::

::: {.source-audit #o012-fom-u001-audit-008}
**Audit sumber.** Baris 523 menempatkan $\sigma$ dalam $C_{n+1}(X)$ tetapi
menuliskannya dengan $n+1$ simpul dan kemudian menerapkan $\partial_n$; bentuk
bertipe benar ialah $\sigma\in C_n(X)$. Baris 536–546 menghapus
$\widehat v_j$ dua kali dan tidak menuliskan dua indeks muka yang berbeda.
Edisi mempertahankan argumen pembatalan berpasangan sumber dan menuliskan
kedua indeksnya secara eksplisit.
:::

::: {.definition #o012-fom-u001-def-008 data-source-lines="550-553"}
**Definisi (siklus).** Definisikan

$$
Z_n^\Delta(X):=\ker\partial_n.
$$

Unsur $Z_n^\Delta(X)$ disebut **siklus** atau **siklus-$n$**.
:::

::: {.definition #o012-fom-u001-def-009 data-source-lines="555-558"}
**Definisi (batas).** Dengan konvensi standar yang bertipe benar, definisikan

$$
B_n^\Delta(X)
:=\operatorname{im}\!\left(
\partial_{n+1}\colon C_{n+1}^\Delta(X)\to C_n^\Delta(X)
\right).
$$

Unsur $B_n^\Delta(X)$ disebut **batas-$n$**.
:::

::: {.corollary #o012-fom-u001-cor-001 data-source-lines="560-564"}
**Akibat.** Dari
[lema $\partial^2=0$](#o012-fom-u001-lem-boundary-square),

$$
B_n^\Delta(X)\subseteq Z_n^\Delta(X).
$$
:::

::: {.definition #o012-fom-u001-def-010 data-source-lines="566-570"}
**Definisi (homologi).** Homologi ke-$n$ didefinisikan sebagai

$$
H_n^\Delta(X)
=Z_n^\Delta(X)\big/B_n^\Delta(X).
$$

Unsur $H_n^\Delta(X)$ disebut **kelas homologi**.
:::

::: {.figure #o012-fom-u001-fig-010 data-source-lines="571-577"}
**Diagram rantai sumber.** Tepat sesudah definisi homologi, sumber menampilkan
diagram tanpa keterangan tambahan:

$$
0\longrightarrow
\mathbb Z
\xrightarrow{\partial_2}
\mathbb Z^3
\xrightarrow{\partial_1}
\mathbb Z^3
\longrightarrow0.
$$

Urutan grup, label $\partial_2,\partial_1$, dan kedua suku nol dipertahankan
sebagaimana dicetak.
:::

::: {.definition #o012-fom-u001-def-011 data-source-lines="578-584"}
**Definisi (siklus homolog).** Misalkan
$z_1,z_2\in Z_n^\Delta(X)$. Kita menulis
$z_1\sim z_2$ dan mengatakan bahwa $z_1$ serta $z_2$ **homolog** jika

$$
[z_1]=[z_2]\in H_n^\Delta(X).
$$

Ini ekuivalen dengan

$$
z_1-z_2\in B_n^\Delta(X).
$$

Kelas-kelas ekuivalensi ini disebut kelas homologi.
:::

::: {.source-audit #o012-fom-u001-audit-009}
**Audit sumber.** Baris 582 mencetak syarat
$z_1-z_2\in B_n(X)$. Namun baris 555–582 sebelumnya mendefinisikan
$B_n=\operatorname{im}\partial_n$, kemudian memakai
$H_n=Z_n/B_{n+1}$, lalu kembali ke $B_n$ pada kalimat siklus homolog.
Ketiga pemakaian itu tidak konsisten satu sama lain dan
$\operatorname{im}\partial_n$ berada di $C_{n-1}$, bukan $C_n$. Edisi
menormalkan seluruh rangkaian menjadi konvensi standar
$B_n=\operatorname{im}\partial_{n+1}\subseteq C_n$,
$B_n\subseteq Z_n$, $H_n=Z_n/B_n$, dan
$z_1-z_2\in B_n$.
:::

::: {.remark #o012-fom-u001-rem-013 data-source-lines="610-613"}
**Catatan.** Untuk ruang terhubung lintasan $X$ dengan titik dasar $x_0$,
homologi singular memenuhi

$$
H_1^{\mathrm{sing}}(X;\mathbb Z)
\cong
\pi_1(X,x_0)^{\mathrm{ab}},
$$

yaitu homologi singular pertama adalah abelianisasi grup fundamental. Bagi
kompleks-$\Delta$, teorema pembandingan yang akan dibuktikan kemudian memberi
$H_1^\Delta(X;\mathbb Z)\cong H_1^{\mathrm{sing}}(X;\mathbb Z)$, sehingga
pernyataan yang sama berlaku untuk homologi simpleksial setelah jembatan itu
tersedia.
:::

::: {.source-audit #o012-fom-u001-audit-010}
**Audit sumber.** Baris 611 mencetak $H^1(X)$, tetapi abelianisasi
$\pi_1(X)$ secara kanonik adalah homologi singular pertama
$H_1^{\mathrm{sing}}(X;\mathbb Z)$, bukan kohomologi pertama. Edisi
membetulkan subskrip, menuliskan koefisien, menyatakan hipotesis
keterhubungan lintasan serta titik dasar, dan menandai teorema pembandingan
yang diperlukan sebelum simbol itu dapat diidentifikasi dengan
$H_1^\Delta$.
:::

# Lapisan penguasaan edisi {.unnumbered #o012-fom-u001-mastery data-origin="edition-original" data-course-route-unit-id="D60-R08"}

Bagian ini ditulis khusus untuk edisi bahasa Indonesia dan bukan bagian dari
catatan Fomberg. Keenam pemeriksaan berikut memetakan kompetensi
kompleks-$\Delta$, rantai, batas, siklus, dan homologi pada rute D60-R08.

::: {.exercise #o012-fom-u001-mcheck-001 data-origin="edition-original" data-course-route-unit-id="D60-R08"}
**Pemeriksaan Penguasaan F1.1 (koordinat barisentris).** Ambil

$$
v_0=(0,0),\qquad v_1=(2,0),\qquad v_2=(0,3).
$$

1. Periksa bahwa ketiga titik bebas afin.
2. Tulis $x=(1/2,3/4)$ dalam bentuk
   $x=t_0v_0+t_1v_1+t_2v_2$ dengan
   $t_i\geq0$ dan $t_0+t_1+t_2=1$.
3. Tentukan apakah $x$ berada pada batas atau bagian dalam segitiga.
:::

::: {.hint #o012-fom-u001-hint-001 data-origin="edition-original"}
**Petunjuk.** Periksa kebebasan linear $v_1-v_0,v_2-v_0$, lalu baca kedua
koordinat $x$ untuk menemukan $t_1,t_2$.
:::

::: {.solution #o012-fom-u001-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan F1.1.** Kita mempunyai

$$
v_1-v_0=(2,0),\qquad v_2-v_0=(0,3).
$$

Determinan matriks dengan kedua kolom itu adalah $6\neq0$, sehingga keduanya
bebas linear dan $v_0,v_1,v_2$ bebas afin. Persamaan koordinat memberi
$2t_1=1/2$ dan $3t_2=3/4$, jadi

$$
t_1=\frac14,\qquad t_2=\frac14,\qquad
t_0=1-t_1-t_2=\frac12.
$$

Semua koefisien positif. Karena titik batas mempunyai setidaknya satu
koefisien barisentris nol, $x$ berada di bagian dalam segitiga.
:::

::: {.exercise #o012-fom-u001-mcheck-002 data-origin="edition-original" data-course-route-unit-id="D60-R08"}
**Pemeriksaan Penguasaan F1.2 (lingkaran sebagai kompleks-$\Delta$).**
Jelaskan mengapa satu simpul $v$ dan satu sisi $e$ yang kedua ujungnya
dilekatkan ke $v$ membentuk kompleks-$\Delta$ pada $S^1$, tetapi bukan
kompleks simpleksial. Jelaskan pula mengapa satu simpleks-$0$ bagi setiap
titik lingkaran menghasilkan topologi diskret.
:::

::: {.hint #o012-fom-u001-hint-002 data-origin="edition-original"}
**Petunjuk.** Periksa tiga syarat kompleks-$\Delta$ secara berurutan. Untuk
kompleks simpleksial, tanyakan apakah $e\colon\Delta^1\to S^1$ injektif.
:::

::: {.solution #o012-fom-u001-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan F1.2.** Bagian dalam $\Delta^1$ dipetakan injektif ke
$S^1-\{v\}$, sedangkan bagian dalam $\Delta^0$ memetakan ke $v$; kedua citra
itu saling lepas dan menutupi $S^1$. Kedua muka $\Delta^1$, yakni kedua titik
ujung, membatasi menjadi pemetaan simpul $v$. Topologi akhir terhadap $v$ dan
$e$ adalah topologi lingkaran standar, sehingga ketiga syarat
kompleks-$\Delta$ terpenuhi.

Namun $e$ tidak injektif pada seluruh $\Delta^1$, sebab kedua titik ujung
mempunyai citra $v$ yang sama. Jadi syarat pertama kompleks simpleksial gagal.
Jika setiap titik dijadikan simpleks-$0$ tersendiri, prapeta setiap
$U\subseteq S^1$ pada setiap simpleks-$0$ selalu terbuka. Syarat topologi akhir
lalu menyatakan setiap $U$ terbuka; itulah topologi diskret.
:::

::: {.exercise #o012-fom-u001-mcheck-003 data-origin="edition-original" data-course-route-unit-id="D60-R08"}
**Pemeriksaan Penguasaan F1.3 (batas segitiga).** Untuk
$\sigma=[v_0,v_1,v_2]$, hitung $\partial_2\sigma$, lalu hitung
$\partial_1\partial_2\sigma$ secara eksplisit.
:::

::: {.hint #o012-fom-u001-hint-003 data-origin="edition-original"}
**Petunjuk.** Gunakan
$\partial[v_i,v_j]=[v_j]-[v_i]$ pada masing-masing dari tiga muka.
:::

::: {.solution #o012-fom-u001-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan F1.3.** Rumus tanda berselang-seling memberi

$$
\partial_2\sigma
=[v_1,v_2]-[v_0,v_2]+[v_0,v_1].
$$

Karena itu

$$
\begin{aligned}
\partial_1\partial_2\sigma
&=([v_2]-[v_1])
-([v_2]-[v_0])
+([v_1]-[v_0])\\
&=[v_2]-[v_1]-[v_2]+[v_0]+[v_1]-[v_0]\\
&=0.
\end{aligned}
$$

Setiap simpul muncul dua kali dengan tanda berlawanan.
:::

::: {.exercise #o012-fom-u001-mcheck-004 data-origin="edition-original" data-course-route-unit-id="D60-R08"}
**Pemeriksaan Penguasaan F1.4 (homologi lingkaran).** Gunakan
kompleks-$\Delta$ satu simpul dan satu sisi untuk menghitung semua
$H_n^\Delta(S^1)$ dengan koefisien $\mathbb Z$.
:::

::: {.hint #o012-fom-u001-hint-004 data-origin="edition-original"}
**Petunjuk.** Hanya $C_1=\mathbb Ze$ dan $C_0=\mathbb Zv$ yang taknol, dan
$\partial_1(e)=0$.
:::

::: {.solution #o012-fom-u001-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan F1.4.** Karena $\partial_1=0$,

$$
Z_1=\ker\partial_1=\mathbb Ze,
\qquad
B_1=\operatorname{im}\partial_2=0.
$$

Maka $H_1^\Delta(S^1)=Z_1/B_1\cong\mathbb Z$. Pada derajat nol,
$Z_0=C_0=\mathbb Zv$ dan $B_0=\operatorname{im}\partial_1=0$, sehingga
$H_0^\Delta(S^1)\cong\mathbb Z$. Untuk $n\geq2$, $C_n=0$, jadi
$H_n^\Delta(S^1)=0$.
:::

::: {.exercise #o012-fom-u001-mcheck-005 data-origin="edition-original" data-course-route-unit-id="D60-R08"}
**Pemeriksaan Penguasaan F1.5 (homologi torus dari matriks batas).** Untuk
kompleks torus sumber, gunakan

$$
\partial_2(V)=\partial_2(L)=e+f-g,
\qquad
\partial_1=0,
$$

untuk menentukan $H_2^\Delta(T^2)$, $H_1^\Delta(T^2)$, dan
$H_0^\Delta(T^2)$.
:::

::: {.hint #o012-fom-u001-hint-005 data-origin="edition-original"}
**Petunjuk.** Dalam basis $(V,L)$ dan $(e,f,g)$, kedua kolom matriks
$\partial_2$ sama dengan $(1,1,-1)^{\mathsf T}$. Vektor ini primitif dalam
$\mathbb Z^3$.
:::

::: {.solution #o012-fom-u001-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan F1.5.** Untuk $a,b\in\mathbb Z$,

$$
\partial_2(aV+bL)=(a+b)(e+f-g).
$$

Jadi

$$
\ker\partial_2
=\mathbb Z(V-L),
\qquad
\operatorname{im}\partial_2
=\mathbb Z(e+f-g).
$$

Karena $C_3=0$, diperoleh

$$
H_2^\Delta(T^2)
=\ker\partial_2/\operatorname{im}\partial_3
\cong\mathbb Z.
$$

Selanjutnya $\ker\partial_1=C_1\cong\mathbb Z^3$. Vektor
$(1,1,-1)$ primitif, sehingga dapat diperluas menjadi basis
$\mathbb Z^3$ dan

$$
H_1^\Delta(T^2)
=\mathbb Z^3/\mathbb Z(1,1,-1)
\cong\mathbb Z^2.
$$

Terakhir, $\partial_1=0$ memberi
$H_0^\Delta(T^2)=\mathbb Zr\cong\mathbb Z$.
:::

::: {.exercise #o012-fom-u001-mcheck-006 data-origin="edition-original" data-course-route-unit-id="D60-R08"}
**Pemeriksaan Penguasaan F1.6 (kelas homolog pada torus).** Dalam
$C_1^\Delta(T^2)$, ambil

$$
z_1=e,\qquad z_2=g-f.
$$

1. Periksa bahwa keduanya siklus.
2. Tentukan apakah keduanya homolog.
3. Tentukan apakah $e$ dan $f$ homolog.
:::

::: {.hint #o012-fom-u001-hint-006 data-origin="edition-original"}
**Petunjuk.** Semua rantai-$1$ adalah siklus karena $\partial_1=0$.
Dua siklus homolog tepat ketika selisihnya merupakan kelipatan
$e+f-g=\partial_2(V)$.
:::

::: {.solution #o012-fom-u001-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan F1.6.** Karena $\partial_1=0$,
$z_1,z_2,e,f$ semuanya siklus. Selisih pasangan pertama ialah

$$
z_1-z_2=e-(g-f)=e+f-g=\partial_2(V),
$$

sehingga $z_1\sim z_2$. Sebaliknya, jika $e$ dan $f$ homolog, harus ada
$k\in\mathbb Z$ dengan

$$
e-f=k(e+f-g).
$$

Membandingkan koefisien $g$ memberi $k=0$, tetapi kemudian koefisien $e$ di
ruas kiri adalah $1$ dan di ruas kanan $0$, kontradiksi. Jadi $e$ dan $f$
tidak homolog.
:::

::: {.boundary #o012-fom-u001-boundary-001}
**Batas sumber komponen.** Unit ini menerjemahkan
algebraic_topology.tex baris 31–614 secara kontigu, dari judul Bagian
“Homology” sampai catatan tentang abelianisasi $\pi_1$. Kursor komponen
berikutnya adalah baris 615, awal Bagian 1.3 tentang homologi singular.
:::
