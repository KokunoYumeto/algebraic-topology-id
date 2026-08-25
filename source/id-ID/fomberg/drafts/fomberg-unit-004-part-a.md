---
title: "Topologi Aljabar"
subtitle: "Komponen Fomberg 4, Bagian A: Eksisi"
author:
  - "Yeheli Fomberg (catatan sumber; berdasarkan kuliah Nir Lazarovich)"
  - "Edisi Bahasa Indonesia dengan perbaikan bukti dan pendamping penguasaan"
date: "25 Agustus 2026"
lang: id-ID
rights: "Sumber dan adaptasi: CC BY-SA 4.0; lihat atribusi dan catatan perubahan di bawah."
source_component: "Fomberg Algebraic Topology, Section 1.7"
source_lines: "1923-2440"
edition_unit_id: "O012-FOM-004"
course_route_unit_id: "D60-R11"
status: "draf terjemahan kontigu; belum merupakan unit final"
---

# Tentang bagian draf ini {.unnumbered #o012-fom-u004-part-a-notice data-course-route-unit-id="D60-R11"}

Bagian ini menerjemahkan secara kontigu Bagian 1.7 *Algebraic Topology* karya
Yeheli Fomberg, berdasarkan kuliah Nir Lazarovich pada musim semi 2025.
Otoritas sumber dibekukan pada commit
`563194fae879178b9a6871b249513bfc27968975`. Rentang yang diterjemahkan ialah
`algebraic_topology.tex` baris 1923–2440: 518 baris fisik, 21.424 byte setelah
normalisasi LF dan satu LF penutup, dengan SHA-256
`cfd82ea5a32ad032258e085a7520c6cd6a2517bf397c28866fb208ad1e58bc7b`.
Baris sumber berikutnya, 2441, adalah `\subsection{Mayer--Vietoris}`.

Catatan sumber tersedia di bawah
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
Terjemahan, pemformatan semantik, audit sumber, perbaikan bukti mandiri, dan
materi penguasaan asli di bawah ini diterbitkan dengan lisensi yang sama.
Perbaikan FOM-PR-05 dan FOM-PR-06 dibedakan secara eksplisit dari teks sumber.
Edisi ini independen dan tidak menyiratkan dukungan, pengesahan, atau afiliasi
dengan penulis, pengajar, ataupun institusi mereka. Produksi terjemahan,
struktur semantik, dan QA dibantu oleh **OpenAI Codex gpt-5.6-sol, Ultra** atas
arahan pengguna.

# Eksisi {#o012-fom-u004-s07 data-source-lines="1923-2440"}

::: {.theorem #o012-fom-u004-thm-excision-closed data-source-lines="1925-1929"}
**Teorema (eksisi).** Misalkan $Z\subseteq A\subseteq X$ dan
$\overline Z\subseteq\mathring A$. Inklusi pasangan

$$
i\colon(X\setminus Z,A\setminus Z)\hookrightarrow(X,A)
$$

menginduksi isomorfisma

$$
i_*\colon H_n(X\setminus Z,A\setminus Z)
\xrightarrow{\ \cong\ }H_n(X,A)
$$

untuk setiap $n$. Dengan kata lain,
$H_n(X,A)\cong H_n(X\setminus Z,A\setminus Z)$.
:::

::: {.source-audit #o012-fom-u004-audit-excision-direction data-origin="edition-original" data-source-lines="1925-1929"}
**Klarifikasi arah pemetaan.** Sumber menuliskan isomorfisma abstrak dengan
$H_n(X,A)$ di sebelah kiri. Karena pemetaan yang disebutkan berasal dari
inklusi $(X\setminus Z,A\setminus Z)\hookrightarrow(X,A)$, arah pemetaan
terinduksi yang kanonis adalah arah yang ditampilkan di atas. Tidak ada isi
matematis yang diubah.
:::

::: {.corollary #o012-fom-u004-cor-good-pair-quotient data-source-label="cor:cor" data-source-lines="1930-1934"}
**Akibat.** Jika $(X,A)$ pasangan baik dalam arti standar—$A$ tak kosong,
tertutup, dan merupakan retrak deformasi dari suatu lingkungannya—maka

$$
H_n(X,A)\cong\widetilde H_n(X/A).
$$

Akibat ini akan diperoleh lagi secara eksplisit dari
[teorema hasil bagi](#o012-fom-u004-thm-relative-quotient) di bawah.
:::

::: {.remark #o012-fom-u004-rem-excision-cover-form data-source-lines="1935-1989"}
**Catatan (bentuk penutup).** Rumusan ekuivalen teorema eksisi adalah sebagai
berikut. Jika $X_1,X_2\subseteq X$ dan

$$
\mathring X_1\cup\mathring X_2=X,
$$

maka inklusi

$$
i\colon(X_1,X_1\cap X_2)\hookrightarrow(X,X_2)
$$

menginduksi isomorfisma

$$
i_*\colon H_n(X_1,X_1\cap X_2)
\xrightarrow{\ \cong\ }H_n(X,X_2)
$$

untuk setiap $n$.

:::: {.figure #o012-fom-u004-fig-excision-equivalence data-source-lines="1942-1987" data-origin="edition-original-redraw"}
![Gambar ulang aksesibel dua rumusan eksisi: daerah Z di dalam A di dalam X, dan penutup X satu–X dua dengan daerah irisan.](../assets/unit-004/excision-equivalence.png){.semantic-redraw width=92%}

**Diagram semantik hasil gambar ulang.** Pada rumusan pertama terdapat tiga
daerah bersarang

$$
Z\subseteq A\subseteq X,
\qquad \overline Z\subseteq\mathring A.
$$

Pada rumusan kedua, $X$ ditutup oleh bagian dalam dua daerah $X_1$ dan $X_2$;
daerah tumpang-tindihnya ialah $X_1\cap X_2$. Korespondensi antarrumusan
adalah

$$
\begin{array}{rcl}
A&=&X_2,\\
Z&=&X\setminus X_1=X_2\setminus X_1,\\
X\setminus Z&=&X_1,\\
A\setminus Z&=&X_1\cap X_2.
\end{array}
$$

Deskripsi aksesibel: menghapus daerah $Z$ yang terletak sepenuhnya di bagian
dalam $A$ menyisakan pasangan yang sama dengan mengambil daerah kiri $X_1$
beserta irisannya dengan daerah kanan $X_2$. Diagram ini disusun ulang secara
mandiri dari relasi himpunan; tidak ada ekspresi TikZ sumber yang disalin.
::::

Untuk memperoleh bentuk kedua dari bentuk pertama, ambil $A=X_2$ dan
$Z=X\setminus X_1$. Karena
$\mathring X_1\cup\mathring X_2=X$, kita mempunyai
$\overline{X\setminus X_1}\subseteq\mathring X_2$. Substitusi pada empat
identitas di atas memberi tepat inklusi pasangan dalam bentuk penutup.
Sebaliknya, untuk $Z\subseteq A\subseteq X$ dengan
$\overline Z\subseteq\mathring A$, ambil $X_1=X\setminus Z$ dan $X_2=A$.
Karena

$$
\operatorname{int}(X\setminus Z)=X\setminus\overline Z,
$$

kedua bagian dalam itu menutup $X$; keempat identitas di atas menghasilkan
pernyataan semula.
:::

::: {.definition #o012-fom-u004-def-u-chains data-source-lines="1990-1998"}
**Definisi (rantai-$\mathcal U$).** Misalkan
$\mathcal U=\{U_j\}$ suatu koleksi subhimpunan $X$ yang bagian-bagian dalamnya
membentuk penutup terbuka bagi $X$, yaitu

$$
X=\bigcup_{U\in\mathcal U}\mathring U.
$$

Kita definisikan

$$
C_n^{\mathcal U}(X)
=\operatorname{span}_{\mathbb Z}
\left\{
\sigma\colon\Delta^n\to X
\;\middle|\;
\exists U\in\mathcal U\text{ sehingga }
\sigma(\Delta^n)\subseteq U
\right\}.
$$

Generator seperti itu disebut **simpleks singular $\mathcal U$-kecil**, dan
unsur grup di atas disebut **rantai-$\mathcal U$**.
:::

::: {.remark #o012-fom-u004-rem-u-chain-complex data-source-lines="1999-2003"}
**Catatan.** Setiap sisi simpleks $\mathcal U$-kecil masih mempunyai citra di
anggota $\mathcal U$ yang sama. Karena itu

$$
\partial\bigl(C_n^{\mathcal U}(X)\bigr)
\subseteq C_{n-1}^{\mathcal U}(X),
$$

sehingga grup-grup $C_n^{\mathcal U}(X)$ membentuk kompleks rantai. Homologi
kompleks ini dinotasikan $H_n^{\mathcal U}(X)$.
:::

::: {.proposition #o012-fom-u004-prop-small-chains data-source-lines="2005-2012" data-repair-id="FOM-PR-05" data-proof-status="statement_with_complete_original_repair"}
**Proposisi (teorema rantai kecil).** Inklusi

$$
\iota\colon C_*^{\mathcal U}(X)\hookrightarrow C_*(X)
$$

merupakan ekuivalensi homotopi kompleks rantai. Jadi terdapat pemetaan rantai

$$
\rho\colon C_*(X)\longrightarrow C_*^{\mathcal U}(X)
$$

sedemikian sehingga $\iota\rho$ dan $\rho\iota$ homotopik-rantai dengan
pemetaan identitas masing-masing. Khususnya,

$$
\iota_*\colon H_n^{\mathcal U}(X)
\xrightarrow{\ \cong\ }H_n(X)
$$

untuk setiap $n$.
:::

::: {.proof #o012-fom-u004-proof-small-chains-source data-source-lines="2013-2152" data-repair-id="FOM-PR-05" data-proof-status="source_incomplete"}
**Bukti sumber, sampai bagian yang dihilangkan.** Sumber mengumumkan bukti
dalam empat langkah, tetapi hanya memulai langkah pertama.

1. **Subdivisi barisentris simpleks.** Simpleks
   $[v_0,v_1,\ldots,v_n]$ terdiri atas semua titik
   $\sum_i t_iv_i$ dengan $t_i\geq0$ dan $\sum_i t_i=1$. **Barisentrum**
   simpleks itu adalah titik berkoordinat barisentris sama besar,

   $$
   b=\sum_{i=0}^{n}\frac1{n+1}v_i.
   $$

   (Awalan *bary-* berarti massa.) Subdivisi barisentris didefinisikan secara
   induktif. Pada dimensi nol,

   $$
   BS([v_0])=\{[v_0]\}.
   $$

   Pada dimensi satu, dengan $b=(v_0+v_1)/2$,

   $$
   BS([v_0,v_1])=\{[b,v_0],[b,v_1]\}.
   $$

   Secara induktif, jika $F_i$ adalah sisi ke-$i$ dari
   $[v_0,\ldots,v_n]$, definisikan

   $$
   BS([v_0,\ldots,v_n])
   =\bigcup_{i=0}^{n}
     \bigl\{[b,s]\mid s\in BS(F_i)\bigr\}.
   $$

   Subdivisi itu terdiri atas $(n+1)!$ simpleks berdimensi $n$ yang menutup
   simpleks semula:

   $$
   \bigl|BS([v_0,\ldots,v_n])\bigr|=(n+1)!.
   $$

   Selain itu, $BS(\Delta^n)$ memberi struktur kompleks simpleks pada
   $\Delta^n$. Sumber kemudian hendak membuktikan bahwa setiap
   $[w_0,\ldots,w_n]\in BS(\Delta^n)$ memenuhi

   $$
   \operatorname{diam}[w_0,\ldots,w_n]
   \leq\frac n{n+1}\operatorname{diam}[v_0,\ldots,v_n].
   $$

   Untuk itu sumber terlebih dahulu mengamati

   $$
   \operatorname{diam}[w_0,\ldots,w_n]
   =\max_{i,j}\lVert w_i-w_j\rVert.
   $$

   Memang, untuk sebuah titik sudut $v$ dan titik
   $\sum_{i=0}^nt_iv_i$ di selubung konveks,

   $$
   \begin{aligned}
   \left\lVert v-\sum_{i=0}^{n}t_iv_i\right\rVert
   &=\left\lVert\sum_{i=0}^{n}t_i(v-v_i)\right\rVert\\
   &\leq\sum_{i=0}^{n}t_i\lVert v-v_i\rVert\\
   &\leq\sum_{i=0}^{n}t_i\max_j\lVert v-v_j\rVert\\
   &=\max_j\lVert v-v_j\rVert.
   \end{aligned}
   $$

:::: {.source-omission #o012-fom-u004-omission-pr05a data-source-lines="2050-2070" data-repair-id="FOM-PR-05" data-proof-part="diameter-and-iteration"}
**Bagian FOM-PR-05a yang dihilangkan dalam sumber.** Sesudah menuliskan batas
diameter yang diinginkan dan estimasi selubung konveks di atas, sumber hanya
menyatakan bahwa sisa argumennya bersifat geometris. Sumber lalu menyebut
konsekuensinya—setiap simpleks dapat dibagi menjadi simpleks-simpleks
berdiameter sekecil yang diinginkan—tanpa membuktikan batas diameter ataupun
iterasinya. [Perbaikan FOM-PR-05a](#o012-fom-u004-proof-pr05a) mengisi kedua
langkah tersebut.
::::

:::: {.source-omission #o012-fom-u004-omission-pr05b data-source-lines="2071-2152" data-repair-id="FOM-PR-05" data-proof-part="small-chain-and-homotopy-equivalence"}
**Bagian FOM-PR-05b yang dihilangkan dalam sumber.** Langkah kedua pada sumber
berbunyi bahwa “sisa bukti mungkin akan ditambahkan kelak”; langkah ketiga dan
keempat tidak hadir. Baris 2073–2150 hanya merupakan komentar TeX nonaktif,
bukan teks bukti yang diterbitkan. Komentar itu mencoba memperkenalkan rantai
linear $LC_n(Y)$ untuk $Y\subseteq\mathbb R^n$ konveks, operator kerucut

$$
b([w_0,\ldots,w_n])=[b,w_0,\ldots,w_n],
\qquad \partial b+b\partial=\operatorname{id},
$$

operator subdivisi $S$ melalui skema
$S(\lambda)=b_\lambda(S\partial\lambda)$, dan suatu operator $T$ yang
dimaksudkan memenuhi

$$
\partial T+T\partial=\operatorname{id}-S.
$$

Rumus rekursif $T$ dalam komentar adalah awal konstruksi standar dan suku
$S\sigma$ dapat muncul ketika identitas operator kerucut diterapkan. Namun
perhitungannya berhenti sebelum keterdefinisian, kealamian terhadap simpleks
singular, argumen bilangan Lebesgue, surjektivitas dan injektivitas homologi,
ataupun pemetaan $\rho$ dibuktikan. Karena komentar tersebut belum merupakan
bukti yang sah, edisi ini tidak mengangkatnya menjadi prosa sumber.
[Perbaikan FOM-PR-05b](#o012-fom-u004-proof-pr05b) memberi konstruksi lengkap
yang diperlukan.
::::
:::

::: {.source-audit #o012-fom-u004-audit-barycentric-face-notation data-origin="edition-original" data-source-lines="2028-2044"}
**Koreksi notasi.** Sumber memakai $\Delta^i$ untuk “sisi ke-$i$” ketika
menuliskan rekursi subdivisi. Superskrip biasanya menyatakan dimensi, bukan
nomor sisi. Edisi memakai $F_i$ untuk sisi ke-$i$ dan mempertahankan rumus
rekursif yang dimaksud.
:::

::: {.proof #o012-fom-u004-proof-pr05a data-origin="edition-original" data-source-lines="2050-2070" data-repair-id="FOM-PR-05" data-proof-status="complete_original_repair" data-repair-part="diameter-and-iteration"}
**Perbaikan bukti FOM-PR-05a (penyusutan diameter).** Setiap simpleks
berdimensi $n$ dalam subdivisi barisentris berkorespondensi dengan rantai sisi
tak kosong

$$
F_0\subsetneq F_1\subsetneq\cdots\subsetneq F_n=\Delta^n,
$$

dan titik-titik sudutnya adalah barisentrum $b_{F_0},\ldots,b_{F_n}$.
Kita lengkapi dahulu fakta diameter yang dipakai sumber. Jika
$x=\sum_i a_iw_i$ dan $y=\sum_j b_jw_j$ adalah dua titik selubung konveks
titik-titik sudut $w_0,\ldots,w_r$, maka

$$
\begin{aligned}
\lVert x-y\rVert
&=\left\lVert\sum_{i,j}a_ib_j(w_i-w_j)\right\rVert\\
&\leq\sum_{i,j}a_ib_j\lVert w_i-w_j\rVert\\
&\leq\max_{i,j}\lVert w_i-w_j\rVert.
\end{aligned}
$$

Karena titik-titik sudut sendiri termasuk dalam selubung konveks, diameter
selubung itu tepat jarak maksimum antara dua titik sudut.

Ambil dua sisi dalam rantai itu, $F\subseteq G$. Misalkan $F$ mempunyai $p$
titik sudut dan $G$ mempunyai $q$ titik sudut. Maka

$$
b_G=\frac pqb_F+\frac1q\sum_{v\in G\setminus F}v
$$

dan karena $b_F$ terletak di selubung konveks titik-titik sudut $F$,

$$
\begin{aligned}
\lVert b_G-b_F\rVert
&=\left\lVert\frac1q\sum_{v\in G\setminus F}(v-b_F)\right\rVert\\
&\leq\frac{q-p}{q}\operatorname{diam}(\Delta^n)\\
&\leq\frac n{n+1}\operatorname{diam}(\Delta^n).
\end{aligned}
$$

Kesamaan diameter selubung konveks dengan jarak maksimum antartitik sudut,
yang telah diperiksa dalam bagian sumber, sekarang memberi

$$
\operatorname{diam}(\tau)
\leq\frac n{n+1}\operatorname{diam}(\Delta^n)
$$

untuk setiap simpleks $\tau$ dalam $BS(\Delta^n)$. Sesudah $r$ iterasi,

$$
\operatorname{diam}(\tau_r)
\leq\left(\frac n{n+1}\right)^r
\operatorname{diam}(\Delta^n).
$$

Faktor $n/(n+1)$ kurang dari satu untuk $n>0$, sehingga ruas kanan menuju
nol. Untuk $n=0$ diameter sejak awal nol. Jadi subdivisi berulang menghasilkan
simpleks-simpleks berdiameter sekecil yang diinginkan. $\square$
:::

::: {.proof #o012-fom-u004-proof-pr05b data-origin="edition-original" data-source-lines="2071-2152" data-repair-id="FOM-PR-05" data-proof-status="complete_original_repair" data-repair-part="small-chain-and-homotopy-equivalence"}
**Perbaikan bukti FOM-PR-05b (operator subdivisi, rantai kecil, dan ekuivalensi
homotopi).** Beri setiap simpleks dalam subdivisi barisentris orientasi yang
diinduksi oleh orientasi $\Delta^n$. Untuk simpleks singular
$\sigma\colon\Delta^n\to X$, definisikan

$$
Sd(\sigma)=\sum_{\tau\in BS(\Delta^n)}
\varepsilon_\tau\,\sigma\circ a_\tau,
$$

di mana $a_\tau\colon\Delta^n\to\tau$ adalah isomorfisma afin berorientasi dan
$\varepsilon_\tau\in\{1,-1\}$ mencatat orientasinya. Perluas secara linear.
Pada batas subdivisi, setiap sisi internal muncul dua kali dengan orientasi
berlawanan, sedangkan sisi luar memberi subdivisi dari batas. Karena itu

$$
\partial Sd=Sd\,\partial;
$$

jadi $Sd$ adalah pemetaan rantai.

Selanjutnya kita bangun homotopi rantai $T\colon C_n(X)\to C_{n+1}(X)$ secara
induktif. Pada simpleks standar, andaikan $T$ telah didefinisikan pada semua
dimensi lebih rendah dan letakkan

$$
z_n=\operatorname{id}_{\Delta^n}
-Sd(\operatorname{id}_{\Delta^n})
-T(\partial\operatorname{id}_{\Delta^n}).
$$

Hipotesis induksi dan fakta bahwa $Sd$ pemetaan rantai memberi

$$
\begin{aligned}
\partial z_n
&=\partial\operatorname{id}_{\Delta^n}
-Sd(\partial\operatorname{id}_{\Delta^n})
-\partial T(\partial\operatorname{id}_{\Delta^n})\\
&=0.
\end{aligned}
$$

Karena $\Delta^n$ kontraktibel, siklus $z_n$ membatasi suatu rantai
$b(z_n)$; secara konkret $b$ dapat dipilih sebagai operator kerucut menuju
barisentrum. Definisikan

$$
T(\operatorname{id}_{\Delta^n})=b(z_n),
\qquad
T(\sigma)=\sigma_\#T(\operatorname{id}_{\Delta^n}).
$$

Konstruksi ini alami terhadap $\sigma$ dan menghasilkan identitas

$$
\partial T+T\partial=\operatorname{id}-Sd.
$$

Yang penting, semua simpleks yang muncul dalam $Sd(\sigma)$ dan $T(\sigma)$
mempunyai citra di dalam $\sigma(\Delta^n)$. Maka kedua operator mempertahankan
subkompleks $C_*^{\mathcal U}(X)$.

Sekarang, bagi suatu simpleks singular $\sigma$, himpunan-himpunan

$$
\left\{\sigma^{-1}(\mathring U)\mid U\in\mathcal U\right\}
$$

membentuk penutup terbuka bagi $\Delta^n$. Lemma bilangan Lebesgue memberi
$\lambda_\sigma>0$ sehingga setiap subhimpunan $\Delta^n$ berdiameter kurang
dari $\lambda_\sigma$ terkandung dalam salah satu prapeta tersebut. Menurut
FOM-PR-05a, ada $N_\sigma$ sehingga semua simpleks dalam
$Sd^{N_\sigma}(\operatorname{id}_{\Delta^n})$ berdiameter kurang dari
$\lambda_\sigma$. Jadi $Sd^{N_\sigma}(\sigma)$ merupakan rantai-$\mathcal U$.
Untuk rantai berhingga $c$, ambil maksimum eksponen bagi simpleks-simpleks yang
muncul di dalamnya; dengan demikian terdapat $N$ sehingga

$$
Sd^N(c)\in C_*^{\mathcal U}(X).
$$

Tuliskan

$$
K_N=\sum_{r=0}^{N-1}Sd^rT.
$$

Penjumlahan teleskopik memberi

$$
\partial K_N+K_N\partial=\operatorname{id}-Sd^N.
$$

Jika $z$ siklus di $C_*(X)$, pilih $N$ sehingga $Sd^Nz$ kecil. Maka
$z-Sd^Nz=\partial K_Nz$, jadi setiap kelas homologi mempunyai wakil kecil;
$\iota_*$ surjektif. Jika siklus kecil $z$ membatasi $c$ dalam $C_*(X)$,
pilih $N$ sehingga $Sd^Nc$ kecil. Karena $T$ dan $Sd$ mempertahankan rantai
kecil, $K_Nz$ juga kecil, dan

$$
z=Sd^Nz+\partial K_Nz
=\partial\bigl(Sd^Nc+K_Nz\bigr)
$$

di dalam $C_*^{\mathcal U}(X)$. Jadi $\iota_*$ injektif. Dengan demikian
$\iota$ adalah kuasi-isomorfisma.

Tersisa membangun invers homotopi rantai yang dinyatakan sumber. Singkatkan
$B_*=C_*^{\mathcal U}(X)$, $C_*=C_*(X)$, dan $Q_*=C_*/B_*$. Karena $B_n$
dibangkitkan oleh suatu subhimpunan basis simpleks singular $C_n$, setiap
$Q_n$ bebas dan barisan

$$
0\longrightarrow B_n\xrightarrow{\iota}C_n
\longrightarrow Q_n\longrightarrow0
$$

terbelah sebagai grup. Barisan eksak panjang dan fakta bahwa $\iota_*$
isomorfisma menunjukkan bahwa $Q_*$ asiklik. Setiap subgrup grup abelian bebas
kembali bebas; jadi barisan

$$
0\longrightarrow Z_n(Q)=B_n(Q)
\longrightarrow Q_n\xrightarrow{\partial_Q}B_{n-1}(Q)
\longrightarrow0
$$

terbelah pada setiap derajat. Pilihan pembelahan memberi homotopi kontraksi
$h\colon Q_n\to Q_{n+1}$ dengan

$$
\partial_Qh+h\partial_Q=\operatorname{id}_Q.
$$

Pilih pula pembelahan berderajat $C_n\cong B_n\oplus Q_n$. Dalam koordinat
ini, pemetaan batas berbentuk

$$
\partial_C(b,q)=\bigl(\partial_Bb+\tau q,\partial_Qq\bigr)
$$

untuk suatu $\tau\colon Q_n\to B_{n-1}$. Identitas $\partial_C^2=0$ memberi

$$
\partial_B\tau+\tau\partial_Q=0.
$$

Sekarang definisikan

$$
\rho(b,q)=b-\tau h(q),
\qquad
H(b,q)=(0,hq).
$$

Relasi terakhir dan identitas kontraksi menunjukkan langsung bahwa $\rho$
pemetaan rantai. Selain itu,

$$
\rho\iota=\operatorname{id}_{B_*},
\qquad
\partial_CH+H\partial_C
=\operatorname{id}_{C_*}-\iota\rho.
$$

Jadi $\rho$ benar-benar invers homotopi rantai bagi $\iota$: komposisi pada
$B_*$ adalah identitas secara ketat dan komposisi pada $C_*$ homotopik-rantai
dengan identitas. Ini menutup pernyataan penuh, bukan hanya isomorfisma
homologi. $\square$
:::

::: {.theorem #o012-fom-u004-thm-excision-cover data-source-lines="2154-2159" data-repair-id="FOM-PR-06" data-proof-status="statement_with_complete_original_repair"}
**Teorema (eksisi, bentuk penutup).** Misalkan $A,B\subseteq X$ dan

$$
\mathring A\cup\mathring B=X.
$$

Inklusi pasangan

$$
i\colon(B,A\cap B)\hookrightarrow(X,A)
$$

menginduksi isomorfisma

$$
i_*\colon H_n(B,A\cap B)
\xrightarrow{\ \cong\ }H_n(X,A)
$$

untuk setiap $n$.
:::

::: {.proof #o012-fom-u004-proof-excision-source data-source-lines="2160-2178" data-repair-id="FOM-PR-06" data-proof-status="source_omitted"}
**Bukti sumber.** Teks aktif sumber hanya mengatakan bahwa bukti bergantung
pada bukti eksisi dan akan ditambahkan kelak.

:::: {.source-omission #o012-fom-u004-omission-pr06 data-source-lines="2160-2178" data-repair-id="FOM-PR-06"}
**Bagian FOM-PR-06 yang dihilangkan dalam sumber.** Komentar TeX nonaktif
mengusulkan $\mathcal U=\{A,B\}$, lalu membandingkan

$$
C_n(X)/C_n(A)
\quad\text{dengan}\quad
C_n^{\mathcal U}(X)/C_n(A)
\cong C_n(B)/C_n(A\cap B),
$$

tetapi tidak membuktikan bahwa perbandingan hasil bagi menginduksi
isomorfisma dalam homologi. Bukti lengkap dan pengecekan aljabarnya diberikan
berikutnya.
::::
:::

::: {.proof #o012-fom-u004-proof-pr06 data-origin="edition-original" data-source-lines="2160-2178" data-repair-id="FOM-PR-06" data-proof-status="complete_original_repair"}
**Perbaikan bukti FOM-PR-06.** Ambil $\mathcal U=\{A,B\}$. Hipotesis
$\mathring A\cup\mathring B=X$ memastikan bahwa koleksi ini memenuhi syarat
teorema rantai kecil. Karena setiap simpleks $\mathcal U$-kecil mempunyai citra
di $A$ atau di $B$,

$$
C_*^{\mathcal U}(X)=C_*(A)+C_*(B).
$$

Pertimbangkan diagram barisan eksak pendek kompleks rantai

$$
\begin{array}{ccccccccc}
0&\longrightarrow&C_*(A)&\longrightarrow&C_*^{\mathcal U}(X)
&\longrightarrow&C_*^{\mathcal U}(X)/C_*(A)&\longrightarrow&0\\
&&\Vert&&\downarrow\iota&&\downarrow\bar\iota\\
0&\longrightarrow&C_*(A)&\longrightarrow&C_*(X)
&\longrightarrow&C_*(X)/C_*(A)&\longrightarrow&0.
\end{array}
$$

Baris atas dan bawah eksak, dan diagram komutatif. Pemetaan vertikal kiri
adalah identitas, sedangkan pemetaan vertikal tengah menginduksi isomorfisma
homologi menurut FOM-PR-05. Dengan menerapkan barisan eksak panjang homologi
pada kedua baris dan lemma lima, $\bar\iota$ juga menginduksi isomorfisma
homologi.

Selanjutnya, karena grup rantai singular bebas pada simpleks singular,

$$
C_*(A)\cap C_*(B)=C_*(A\cap B).
$$

Teorema isomorfisma kedua memberi isomorfisma kompleks rantai yang eksplisit,

$$
\begin{aligned}
C_*^{\mathcal U}(X)/C_*(A)
&=\bigl(C_*(A)+C_*(B)\bigr)/C_*(A)\\
&\cong C_*(B)/\bigl(C_*(A)\cap C_*(B)\bigr)\\
&=C_*(B)/C_*(A\cap B)\\
&=C_*(B,A\cap B).
\end{aligned}
$$

Di sisi lain, $C_*(X)/C_*(A)=C_*(X,A)$. Setelah mengambil homologi, pemetaan
yang dihasilkan tepat pemetaan yang diinduksi oleh inklusi pasangan
$(B,A\cap B)\hookrightarrow(X,A)$. Maka

$$
H_n(B,A\cap B)\xrightarrow{\ \cong\ }H_n(X,A)
$$

untuk setiap $n$. Melalui ekuivalensi pada
[catatan bentuk penutup](#o012-fom-u004-rem-excision-cover-form), bukti ini juga
membuktikan bentuk eksisi dengan $Z\subseteq A$. $\square$
:::

::: {.theorem #o012-fom-u004-thm-relative-quotient data-source-label="thm:reduced-and-relative-homologies" data-source-lines="2182-2188"}
**Teorema (homologi relatif sebagai homologi hasil bagi).** Misalkan $(X,A)$
pasangan baik dalam arti standar: $A$ tak kosong dan tertutup, serta $A$
merupakan retrak deformasi dari suatu lingkungan terbukanya. Pemetaan hasil
bagi

$$
q\colon(X,A)\longrightarrow(X/A,A/A)
$$

menginduksi isomorfisma

$$
q_*\colon H_n(X,A)
\xrightarrow{\ \cong\ }H_n(X/A,A/A)
\cong\widetilde H_n(X/A)
$$

untuk setiap $n$.
:::

::: {.proof #o012-fom-u004-proof-relative-quotient data-source-lines="2189-2233"}
**Bukti.** Homologi suatu ruang relatif terhadap satu titik secara alami
isomorfik dengan homologi tereduksi ruang itu. Jadi cukup dibuktikan bahwa

$$
q_*\colon H_n(X,A)\longrightarrow H_n(X/A,A/A)
$$

merupakan isomorfisma. Karena $(X,A)$ pasangan baik, terdapat lingkungan
terbuka $U$ dari $A$ di $X$ yang beretraksi deformasi ke $A$. Karena $A$
tertutup, $\overline A=A\subseteq\mathring U=U$, sehingga eksisi terhadap $A$
di dalam pasangan $(X,U)$ berlaku. Pertimbangkan
diagram komutatif berikut.

:::: {.figure #o012-fom-u004-fig-relative-quotient-square data-source-lines="2195-2206" data-origin="edition-original-redraw"}
$$
\begin{array}{ccccc}
H_n(X,A)&\longrightarrow&H_n(X,U)&\longleftarrow&H_n(X\setminus A,U\setminus A)\\
\downarrow q_*&&\downarrow q_*&&\downarrow q_*\\
H_n(X/A,A/A)&\longrightarrow&H_n(X/A,U/A)&\longleftarrow&
H_n\bigl((X/A)\setminus\{A/A\},(U/A)\setminus\{A/A\}\bigr).
\end{array}
$$

**Deskripsi aksesibel.** Kedua baris adalah zig-zag tiga grup homologi relatif.
Ketiga panah vertikal diinduksi oleh pemetaan hasil bagi. Panah mendatar kiri
memperbesar subruang relatif dari $A$ ke $U$; panah mendatar kanan adalah
inklusi pasangan komplemen. Kedua persegi berkomutasi. Diagram ini ditulis
ulang secara mandiri dan tidak menyalin ekspresi TikZ-CD sumber.
::::

Barisan eksak panjang tripel $(X,U,A)$ memuat bagian

:::: {.figure #o012-fom-u004-fig-triple-xua data-source-lines="2207-2215" data-origin="edition-original-redraw"}
$$
\cdots\longrightarrow H_n(U,A)
\longrightarrow H_n(X,A)
\longrightarrow H_n(X,U)
\longrightarrow H_{n-1}(U,A)
\longrightarrow\cdots.
$$

**Deskripsi aksesibel.** Empat suku berturutan adalah homologi pasangan
$(U,A)$, $(X,A)$, $(X,U)$, lalu pasangan $(U,A)$ satu derajat lebih rendah.
Eksakitas akan memaksa panah tengah menjadi isomorfisma ketika kedua suku
ujung nol.
::::

Retraksi deformasi $U$ ke $A$ memberi ekuivalensi homotopi pasangan
$(U,A)\simeq(A,A)$, sehingga

$$
H_k(U,A)\cong H_k(A,A)=0
$$

untuk setiap $k$. Eksakitas barisan di atas dengan demikian menunjukkan bahwa
panah mendatar kiri atas $H_n(X,A)\to H_n(X,U)$ adalah isomorfisma. Retraksi
deformasi tersebut turun menjadi retraksi deformasi $U/A$ ke $A/A$; argumen
yang sama menunjukkan bahwa panah mendatar kiri bawah juga isomorfisma.

Dua panah mendatar kanan adalah isomorfisma oleh teorema eksisi. Pemetaan
hasil bagi $q$ membatasi diri menjadi homeomorfisma pasangan

$$
(X\setminus A,U\setminus A)
\xrightarrow{\ \cong\ }
\bigl((X/A)\setminus\{A/A\},(U/A)\setminus\{A/A\}\bigr),
$$

sehingga panah vertikal kanan juga isomorfisma. Komutativitas persegi kanan
memberi bahwa panah vertikal tengah adalah isomorfisma; komutativitas persegi
kiri kemudian memberi bahwa panah vertikal kiri adalah isomorfisma. Inilah
$q_*$ pada pernyataan teorema. $\square$
:::

::: {.source-audit #o012-fom-u004-audit-relative-quotient data-origin="edition-original" data-source-lines="2197-2230"}
**Koreksi hipotesis, notasi, dan pengulangan.** Definisi “pasangan baik” sumber
pada baris 1369–1374 hanya meminta retraksi deformasi dari suatu lingkungan,
sedangkan bukti sekarang memakai $\overline A\subseteq\mathring U$, fakta
bahwa $X\setminus A$ terbuka, serta titik hasil bagi $A/A$. Konvensi standar
menambahkan bahwa $A$ tak kosong dan tertutup; edisi menyatakan syarat yang
diperlukan itu secara eksplisit. Baris 2219 sumber menulis
$H_n(U,A)\cong H_n(U,A)\cong\{0\}$; suku tengah yang dimaksud adalah
$H_n(A,A)$. Ekspresi komplemen pada baris 2198 dan 2203 juga tidak memasang
tanda kurung pada ruang hasil bagi. Edisi menuliskan
$(X/A)\setminus\{A/A\}$ dan $(U/A)\setminus\{A/A\}$ agar pasangan serta
homeomorfisma pembatasan $q$ tidak ambigu.
:::

::: {.theorem #o012-fom-u004-thm-invariance-dimension data-source-label="thm:invariance-of-dimension" data-source-lines="2237-2241"}
**Teorema (invariansi dimensi).** Misalkan $U\subseteq\mathbb R^n$ dan
$V\subseteq\mathbb R^m$ merupakan **himpunan terbuka tak kosong**. Jika $U$
dan $V$ homeomorfik, maka $m=n$.
:::

::: {.source-audit #o012-fom-u004-audit-invariance-nonempty data-origin="edition-original" data-source-lines="2237-2241"}
**Perbaikan hipotesis.** Sumber tidak menyatakan bahwa $U$ dan $V$ tak kosong.
Tanpa syarat itu, pernyataannya salah karena himpunan kosong terbuka di setiap
$\mathbb R^d$ dan semua himpunan kosong homeomorfik. Syarat tak kosong
ditambahkan agar teorema benar dan agar pemilihan $x\in U$ pada bukti sah.
:::

::: {.proof #o012-fom-u004-proof-invariance-dimension data-source-lines="2242-2287"}
**Bukti.** Pilih $x\in U$. Untuk $n\geq1$, eksisi pada suatu bola terbuka kecil
di sekitar $x$ memberi

$$
H_k(U,U\setminus\{x\})
\cong H_k(\mathbb R^n,\mathbb R^n\setminus\{x\}).
$$

Barisan eksak panjang pasangan
$(\mathbb R^n,\mathbb R^n\setminus\{x\})$ memuat

:::: {.figure #o012-fom-u004-fig-local-homology-les data-source-lines="2252-2258" data-origin="edition-original-redraw"}
$$
\widetilde H_k(\mathbb R^n)
\longrightarrow H_k(\mathbb R^n,\mathbb R^n\setminus\{x\})
\longrightarrow\widetilde H_{k-1}(\mathbb R^n\setminus\{x\})
\longrightarrow\widetilde H_{k-1}(\mathbb R^n).
$$

**Deskripsi aksesibel.** Grup relatif lokal berada di antara dua grup homologi
tereduksi ruang Euklides dan grup homologi tereduksi komplemennya. Kedua grup
ruang Euklides nol karena ruang itu kontraktibel. Diagram ditulis ulang tanpa
menyalin ekspresi TikZ-CD sumber.
::::

Karena $\mathbb R^n$ kontraktibel dan
$\mathbb R^n\setminus\{x\}\simeq S^{n-1}$, eksakitas memberi, untuk $k\geq1$,

$$
\begin{aligned}
H_k(U,U\setminus\{x\})
&\cong H_k(\mathbb R^n,\mathbb R^n\setminus\{x\})\\
&\cong\widetilde H_{k-1}(S^{n-1})\\
&\cong
\begin{cases}
\mathbb Z,&k=n,\\
0,&k\ne n.
\end{cases}
\end{aligned}
$$

Pada $k=0$, grup relatif juga nol: komplemen tak kosong dan pemetaan
$H_0(\mathbb R^n\setminus\{x\})\to H_0(\mathbb R^n)$ surjektif. Jadi rumus
per kasus di atas memang berlaku untuk semua $k\geq0$ ketika $n\geq1$.

Untuk $n=0$, satu-satunya himpunan terbuka tak kosong dalam $\mathbb R^0$
adalah satu titik; perhitungan langsung memberi
$H_k(\{x\},\varnothing)\cong\mathbb Z$ tepat pada $k=0$. Jadi rumus “satu
grup $\mathbb Z$ tepat pada derajat $n$” berlaku juga pada dimensi nol.

Misalkan $\varphi\colon U\to V$ homeomorfisma. Ia memberi homeomorfisma
pasangan

$$
(U,U\setminus\{x\})
\xrightarrow{\ \cong\ }
(V,V\setminus\{\varphi(x)\}),
$$

dan karenanya isomorfisma grup bergradasi

$$
H_k(U,U\setminus\{x\})
\cong H_k(V,V\setminus\{\varphi(x)\}).
$$

Perhitungan yang sama di $V\subseteq\mathbb R^m$ menunjukkan bahwa ruas kanan
isomorfik dengan $\mathbb Z$ tepat pada derajat $k=m$. Ruas kiri isomorfik
dengan $\mathbb Z$ tepat pada derajat $k=n$. Karena isomorfisma berlaku pada
setiap derajat, $n=m$. $\square$
:::

::: {.source-audit #o012-fom-u004-audit-local-relative-notation data-origin="edition-original" data-source-lines="2243-2280"}
**Koreksi notasi.** Baris 2245 sumber menulis $H_k(X,X\setminus\{x\})$ setelah
memilih $x\in U$; $X$ tidak didefinisikan di sana. Baris 2249–2280 memakai
tilde pada grup homologi relatif dan menjatuhkannya pada satu tempat. Konvensi
standar memakai homologi biasa untuk pasangan dan homologi tereduksi untuk
ruang komplemen. Edisi menerapkan konvensi itu secara konsisten dan menutup
kasus dimensi nol secara terpisah.
:::

::: {.remark #o012-fom-u004-rem-invariance-name data-source-lines="2288-2291"}
**Catatan.** Hasil
[teorema sebelumnya](#o012-fom-u004-thm-invariance-dimension) lazim disebut
**invariansi dimensi**.
:::

::: {.remark #o012-fom-u004-rem-local-homology data-source-lines="2292-2306"}
**Catatan (homologi lokal).** Dalam bukti invariansi dimensi muncul grup

$$
H_n(X,X\setminus\{x\}),
$$

yang disebut **homologi lokal $X$ di $x$**. Jika singleton $\{x\}$ tertutup dan
$U$ merupakan lingkungan terbuka $x$, eksisi memberi

$$
H_n(X,X\setminus\{x\})
\cong H_n(U,U\setminus\{x\}).
$$

Jadi struktur grup tersebut hanya bergantung pada topologi $X$ di sekitar
$x$. Setiap homeomorfisma $f\colon X\to Y$ menginduksi isomorfisma

$$
H_n(X,X\setminus\{x\})
\cong H_n(Y,Y\setminus\{f(x)\})
$$

untuk setiap $x$ dan $n$. Karena itu homologi lokal dapat membuktikan bahwa
dua ruang tidak homeomorfik secara lokal pada titik-titik tertentu, seperti
dalam [teorema invariansi dimensi](#o012-fom-u004-thm-invariance-dimension).
:::

::: {.remark #o012-fom-u004-rem-relative-disk-generator data-source-lines="2308-2322"}
**Catatan.** Kita telah memperoleh

$$
H_k(D^n,\partial D^n)
\cong\widetilde H_k(S^n)
\cong
\begin{cases}
\mathbb Z,&k=n,\\
0,&k\ne n.
\end{cases}
$$

Dengan mengidentifikasi
$H_n(D^n,\partial D^n)\cong H_n(\Delta^n,\partial\Delta^n)$, proposisi
berikut menentukan siklus eksplisit yang menghasilkan grup itu dan, kemudian,
$\widetilde H_n(S^n)$.
:::

::: {.proposition #o012-fom-u004-prop-simplex-generator data-source-lines="2324-2328"}
**Proposisi.** Pemetaan identitas

$$
\sigma_n\colon\Delta^n\longrightarrow\Delta^n,
\qquad \sigma_n=\operatorname{id}_{\Delta^n},
$$

dipandang sebagai simpleks singular berdimensi $n$, menghasilkan

$$
H_n(\Delta^n,\partial\Delta^n)\cong\mathbb Z.
$$
:::

::: {.proof #o012-fom-u004-proof-simplex-generator data-source-lines="2329-2413"}
**Bukti.** Karena
$\partial\sigma_n\in C_{n-1}(\partial\Delta^n)$, batas itu nol dalam kompleks
hasil bagi:

$$
\partial\sigma_n=0
\quad\text{di}\quad
C_{n-1}(\Delta^n)/C_{n-1}(\partial\Delta^n).
$$

Jadi $\sigma_n$ adalah siklus relatif dan
$[\sigma_n]\in H_n(\Delta^n,\partial\Delta^n)$. Kita berinduksi pada $n$.
Untuk $n=0$, $\partial\Delta^0=\varnothing$ dan $\sigma_0$ jelas menghasilkan

$$
H_0(\Delta^0,\partial\Delta^0)
=H_0(\{*\},\varnothing)
=H_0(\{*\})\cong\mathbb Z.
$$

Sekarang misalkan $n>0$. Pilih satu sisi $F_i\cong\Delta^{n-1}$ dari
$\Delta^n$ dan letakkan

$$
\Lambda=\partial\Delta^n\setminus\mathring F_i.
$$

(Mohon hargai kehebatan notasi ini.) Kita akan memakai dua isomorfisma

:::: {.figure #o012-fom-u004-fig-simplex-generator-isomorphisms data-source-lines="2343-2348" data-origin="edition-original-redraw"}
$$
H_n(\Delta^n,\partial\Delta^n)
\xrightarrow{\ \cong\ }
H_{n-1}(\partial\Delta^n,\Lambda)
\xleftarrow{\ \cong\ }
H_{n-1}(\Delta^{n-1},\partial\Delta^{n-1}).
$$

**Deskripsi aksesibel.** Grup relatif simpleks berdimensi $n$ dipetakan oleh
pemetaan penghubung ke grup relatif batasnya pada derajat $n-1$. Inklusi sisi
yang tidak terkandung dalam $\Lambda$ mengidentifikasi grup terakhir dengan
grup relatif simpleks berdimensi $n-1$. Diagram disusun ulang sebagai zig-zag
linear, bukan menyalin TikZ-CD sumber.
::::

Untuk isomorfisma pertama, gunakan barisan eksak panjang tripel
$(\Delta^n,\partial\Delta^n,\Lambda)$:

:::: {.figure #o012-fom-u004-fig-simplex-triple-les data-source-lines="2349-2358" data-origin="edition-original-redraw"}
$$
\cdots\longrightarrow H_n(\partial\Delta^n,\Lambda)
\longrightarrow H_n(\Delta^n,\Lambda)
\longrightarrow H_n(\Delta^n,\partial\Delta^n)
\xrightarrow{\delta}H_{n-1}(\partial\Delta^n,\Lambda)
\longrightarrow\cdots.
$$

**Deskripsi aksesibel.** Pemetaan penghubung $\delta$ keluar dari homologi
relatif $(\Delta^n,\partial\Delta^n)$ menuju homologi relatif
$(\partial\Delta^n,\Lambda)$ satu derajat lebih rendah. Suku relatif
$(\Delta^n,\Lambda)$ pada kedua sisi yang relevan akan bernilai nol.
::::

Simpleks $\Delta^n$ beretraksi deformasi ke $\Lambda$: secara simpleks,
$\Delta^n$ dapat dikolaps sepanjang sisi $F_i$ yang hilang, dengan
mempertahankan gabungan semua sisi lainnya. Maka
$(\Delta^n,\Lambda)\simeq(\Lambda,\Lambda)$ dan
$H_j(\Delta^n,\Lambda)=0$ untuk setiap $j$. Eksakitas menjadikan $\delta$
isomorfisma pertama.

Isomorfisma kedua diinduksi oleh inklusi sisi yang tidak terkandung dalam
$\Lambda$,

$$
i\colon(\Delta^{n-1},\partial\Delta^{n-1})
\hookrightarrow(\partial\Delta^n,\Lambda).
$$

Untuk $n=1$, pernyataan itu merupakan identifikasi langsung pada $H_0$.
Untuk $n>1$, kedua pasangan merupakan pasangan baik, dan $i$ menginduksi
homeomorfisma hasil bagi

$$
\Delta^{n-1}/\partial\Delta^{n-1}
\xrightarrow{\ \cong\ }
\partial\Delta^n/\Lambda.
$$

Teorema hasil bagi relatif memberi isomorfisma kedua.

Di bawah pemetaan penghubung pertama,

$$
[\sigma_n]\longmapsto[\partial\sigma_n]
=\pm[\sigma_{n-1}],
$$

karena semua sisi batas selain $F_i$ terletak di $\Lambda$ dan menjadi nol.
Menurut hipotesis induksi, $[\sigma_{n-1}]$ menghasilkan
$H_{n-1}(\Delta^{n-1},\partial\Delta^{n-1})$. Jadi
$[\partial\sigma_n]$ menghasilkan
$H_{n-1}(\partial\Delta^n,\Lambda)$, dan $[\sigma_n]$ menghasilkan
$H_n(\Delta^n,\partial\Delta^n)$.

Untuk memperoleh generator $\widetilde H_n(S^n)$, bentuk $S^n$ dari dua
salinan $\Delta_1^n$ dan $\Delta_2^n$ dengan mengidentifikasi batasnya menurut
urutan titik sudut. (Konstruksi ini sangat mirip dengan salah satu soal
pekerjaan rumah dalam kuliah sumber.) Misalkan $\sigma_1$ dan $\sigma_2$
simpleks singular yang merepresentasikan kedua salinan. Orientasi identifikasi memberi
$\partial\sigma_1=\partial\sigma_2$, sehingga

$$
\partial(\sigma_1-\sigma_2)=0.
$$

Kita klaim bahwa $[\sigma_1-\sigma_2]$ menghasilkan
$\widetilde H_n(S^n)$. Gunakan isomorfisma

:::: {.figure #o012-fom-u004-fig-sphere-generator-isomorphisms data-source-lines="2400-2405" data-origin="edition-original-redraw"}
$$
\widetilde H_n(S^n)
\xrightarrow{\ \cong\ }
H_n(S^n,\Delta_2^n)
\xleftarrow{\ \cong\ }
H_n(\Delta_1^n,\partial\Delta_1^n).
$$

**Deskripsi aksesibel.** Panah kiri berasal dari barisan eksak panjang pasangan
$(S^n,\Delta_2^n)$; panah kanan memasukkan belahan simpleks pertama dan
mengidentifikasi batasnya dengan belahan kedua. Diagram ditulis ulang secara
mandiri sebagai zig-zag.
::::

Isomorfisma pertama berasal dari barisan eksak panjang pasangan
$(S^n,\Delta_2^n)$ karena $\Delta_2^n$ kontraktibel. Untuk $n>0$,
isomorfisma kedua dapat diperoleh dengan melewati hasil bagi seperti di atas;
kasus $n=0$ diperiksa langsung. Dalam grup relatif tengah, suku $\sigma_2$
menjadi nol, sehingga $[\sigma_1-\sigma_2]$ bersesuaian dengan
$[\sigma_1]$ pada grup ketiga. Kelas terakhir adalah generator menurut bagian
pertama bukti. Jadi $[\sigma_1-\sigma_2]$ menghasilkan
$\widetilde H_n(S^n)$. $\square$
:::

::: {.source-audit #o012-fom-u004-audit-simplex-generator-degree data-origin="edition-original" data-source-lines="2379-2387"}
**Koreksi derajat.** Baris 2385 sumber menyebut
$H_n(\partial\Delta^n,\Lambda)$. Pemetaan penghubung pada diagram dan kedua
baris di sekitarnya menunjukkan bahwa grup yang dimaksud adalah
$H_{n-1}(\partial\Delta^n,\Lambda)$. Edisi memakai derajat yang benar.
:::

::: {.source-audit #o012-fom-u004-audit-simplex-sphere-notation data-origin="edition-original" data-source-lines="2308-2412"}
**Koreksi homologi dan nama siklus.** Baris 2319 sumber menulis $H_n(S^n)$
ketika grup siklik yang sedang diidentifikasi adalah
$\widetilde H_n(S^n)$; pembedaan ini menentukan pada $n=0$. Baris 2338
beralih ke $H_0(\Delta^0/\partial\Delta^0)$ di tengah argumen pasangan relatif,
sehingga edisi mempertahankan $H_0(\Delta^0,\partial\Delta^0)$. Diagram pada
baris 2402 memakai tilde pada grup homologi relatif; edisi memakai tilde hanya
pada homologi tereduksi absolut dan $H_n$ biasa pada pasangan. Terakhir, baris
2412 menyebut $\Delta_1^n-\Delta_2^n$ sebagai siklus, padahal simpleks singular
yang dapat dikurangkan di kompleks rantai adalah $\sigma_1-\sigma_2$. Semua
empat normalisasi dinyatakan eksplisit di sini; generator dan orientasinya
tidak diubah.
:::

::: {.proposition #o012-fom-u004-prop-wedge-homology data-source-lines="2415-2425"}
**Proposisi (homologi tereduksi jumlah baji).** Misalkan
$\{(X_\alpha,x_\alpha)\}_\alpha$ suatu koleksi pasangan baik dalam konvensi
standar; khususnya setiap singleton $\{x_\alpha\}$ tertutup. Inklusi

$$
i_\alpha\colon X_\alpha\hookrightarrow\bigvee_\alpha X_\alpha
$$

menginduksi isomorfisma

$$
\bigoplus_\alpha(i_\alpha)_*\colon
\bigoplus_\alpha\widetilde H_k(X_\alpha)
\xrightarrow{\ \cong\ }
\widetilde H_k\!\left(\bigvee_\alpha X_\alpha\right).
$$
:::

::: {.source-audit #o012-fom-u004-audit-wedge-arrow data-origin="edition-original" data-source-lines="2417-2424"}
**Koreksi arah pemetaan.** Sumber menampilkan
$\bigoplus_\alpha(i_\alpha)_*$ sebagai pemetaan dari homologi baji menuju
jumlah langsung. Akan tetapi setiap $(i_\alpha)_*$ berarah dari
$\widetilde H_k(X_\alpha)$ ke homologi baji; karena itu jumlah langsungnya
harus berarah seperti pada pernyataan edisi. Rumus sumber tidak bertipe dengan
arah semula.
:::

::: {.proof #o012-fom-u004-proof-wedge-homology data-source-lines="2426-2439"}
**Bukti.** Pasangan

$$
\left(\bigsqcup_\alpha X_\alpha,
\{x_\alpha\mid\alpha\}\right)
$$

merupakan pasangan baik: ambil gabungan lepas lingkungan baik pada setiap
komponen dan gabungkan retraksi deformasinya komponen demi komponen. Hasil
bagi yang meruntuhkan semua titik dasar menjadi satu titik adalah jumlah baji,

$$
\left(\bigsqcup_\alpha X_\alpha\right)
\big/\{x_\alpha\mid\alpha\}
\cong\bigvee_\alpha X_\alpha.
$$

[Teorema hasil bagi relatif](#o012-fom-u004-thm-relative-quotient) dan
dekomposisi rantai singular menurut komponen memberi

$$
\begin{aligned}
\widetilde H_k\!\left(
  \left(\bigsqcup_\alpha X_\alpha\right)
  \big/\{x_\alpha\mid\alpha\}
\right)
&\cong H_k\!\left(\bigsqcup_\alpha X_\alpha,
                   \{x_\alpha\mid\alpha\}\right)\\
&\cong\bigoplus_\alpha H_k(X_\alpha,\{x_\alpha\})\\
&\cong\bigoplus_\alpha\widetilde H_k(X_\alpha).
\end{aligned}
$$

Jika $j_\alpha\colon X_\alpha\to\bigsqcup_\beta X_\beta$ adalah inklusi
komponen dan $q$ pemetaan hasil bagi menuju baji, maka
$q\circ j_\alpha=i_\alpha$. Karena semua isomorfisma di atas bersifat alami,
invers dari isomorfisma yang ditampilkan dalam perhitungan tepat
$\bigoplus_\alpha(i_\alpha)_*$. Jadi pemetaan pada pernyataan merupakan
isomorfisma. $\square$
:::

::: {.source-audit #o012-fom-u004-audit-wedge-set-notation data-origin="edition-original" data-source-lines="2427-2437"}
**Koreksi notasi himpunan.** Baris 2435 sumber menulis
$\{x_\alpha\}_\alpha$ di dalam pasangan, sedangkan baris 2427 dan 2431 memakai
himpunan $\{x_\alpha\mid\alpha\}$. Edisi memakai bentuk terakhir secara
konsisten dan menambahkan argumen kealamian yang mengidentifikasi
isomorfisma abstrak dengan jumlah langsung pemetaan inklusi.
:::

## Pemeriksaan penguasaan bagian A {#o012-fom-u004-part-a-mastery data-origin="edition-original" data-course-route-unit-id="D60-R11"}

::: {.exercise #o012-fom-u004-part-a-mcheck-001 data-origin="edition-original" data-course-route-unit-id="D60-R11" data-repair-id="FOM-PR-05"}
**Pemeriksaan Penguasaan F4A.1 (subdivisi dan rantai kecil).** Misalkan
$\sigma\colon\Delta^2\to X$ simpleks singular dan
$\mathcal U=\{U_j\}$ memenuhi syarat definisi rantai-$\mathcal U$.

1. Berapa banyak segitiga yang muncul setelah $r$ subdivisi barisentris?
2. Berikan batas atas diameter setiap segitiga sesudah $r$ subdivisi.
3. Gunakan lemma bilangan Lebesgue pada penutup
   $\{\sigma^{-1}(\mathring U_j)\}_j$ untuk membuktikan bahwa
   $Sd^r(\sigma)$ merupakan rantai-$\mathcal U$ untuk $r$ cukup besar.
4. Jelaskan mengapa argumen yang sama berlaku serentak untuk setiap rantai
   singular berhingga.
:::

::: {.hint #o012-fom-u004-part-a-hint-001 data-origin="edition-original"}
**Petunjuk.** Setiap subdivisi segitiga menghasilkan $3!=6$ segitiga, dan
faktor penyusutan diameter untuk $n=2$ adalah $2/3$. Pilih $r$ sehingga
$(2/3)^r\operatorname{diam}(\Delta^2)$ lebih kecil daripada bilangan Lebesgue.
Untuk rantai berhingga, ambil maksimum dari sejumlah berhingga eksponen.
:::

::: {.solution #o012-fom-u004-part-a-sol-001 data-origin="edition-original" data-repair-id="FOM-PR-05"}
**Solusi Pemeriksaan F4A.1.** Satu subdivisi memberi enam segitiga; menerapkan
aturan itu pada setiap segitiga secara berulang memberi $6^r$ segitiga.
Menurut estimasi FOM-PR-05a, diameter masing-masing paling besar

$$
\left(\frac23\right)^r\operatorname{diam}(\Delta^2).
$$

Prapeta bagian-bagian dalam $U_j$ membentuk penutup terbuka bagi ruang kompak
$\Delta^2$, sehingga mempunyai bilangan Lebesgue $\lambda>0$. Pilih $r$ dengan

$$
\left(\frac23\right)^r\operatorname{diam}(\Delta^2)<\lambda.
$$

Setiap segitiga hasil subdivisi lalu terkandung dalam suatu
$\sigma^{-1}(\mathring U_j)$; citranya di bawah $\sigma$ terkandung dalam
$U_j$. Maka semua generator yang muncul dalam $Sd^r(\sigma)$ bersifat
$\mathcal U$-kecil. Jika
$c=\sum_{\ell=1}^N a_\ell\sigma_\ell$, lakukan konstruksi ini pada setiap
$\sigma_\ell$ dan ambil maksimum $r_1,\ldots,r_N$. Subdivisi tambahan tidak
merusak kekecilan, sehingga satu eksponen bersama membuat $Sd^r(c)$ kecil.
:::

::: {.exercise #o012-fom-u004-part-a-mcheck-002 data-origin="edition-original" data-course-route-unit-id="D60-R11" data-repair-id="FOM-PR-06"}
**Pemeriksaan Penguasaan F4A.2 (inti aljabar eksisi).** Misalkan
$\mathring A\cup\mathring B=X$ dan $\mathcal U=\{A,B\}$.

1. Buktikan bahwa
   $C_*^{\mathcal U}(X)=C_*(A)+C_*(B)$ dan
   $C_*(A)\cap C_*(B)=C_*(A\cap B)$.
2. Bangun isomorfisma kompleks rantai

   $$
   C_*^{\mathcal U}(X)/C_*(A)
   \cong C_*(B)/C_*(A\cap B).
   $$

3. Jelaskan, dengan barisan eksak pendek dan lemma lima, mengapa inklusi ke
   $C_*(X)/C_*(A)$ menginduksi isomorfisma homologi.
:::

::: {.hint #o012-fom-u004-part-a-hint-002 data-origin="edition-original"}
**Petunjuk.** Basis grup rantai singular terdiri atas semua simpleks singular.
Bandingkan dua barisan eksak pendek dengan suku kiri $C_*(A)$ dan suku tengah
berturut-turut $C_*^{\mathcal U}(X)$ dan $C_*(X)$. Gunakan FOM-PR-05 pada
pemetaan tengah.
:::

::: {.solution #o012-fom-u004-part-a-sol-002 data-origin="edition-original" data-repair-id="FOM-PR-06"}
**Solusi Pemeriksaan F4A.2.** Sebuah generator $\mathcal U$-kecil mempunyai
citra seluruhnya di $A$ atau seluruhnya di $B$, sehingga grup yang dibangkitkan
semua generator itu tepat $C_*(A)+C_*(B)$. Sebuah simpleks singular menjadi
generator baik bagi $C_*(A)$ maupun $C_*(B)$ tepat ketika citranya terkandung
dalam $A\cap B$. Karena grup rantai bebas pada basis simpleks singular,

$$
C_*(A)\cap C_*(B)=C_*(A\cap B).
$$

Pemetaan yang mengirim kelas $b+C_*(A\cap B)$ ke $b+C_*(A)$ terdefinisi baik
dan memberi

$$
C_*(B)/C_*(A\cap B)
\xrightarrow{\ \cong\ }
\bigl(C_*(A)+C_*(B)\bigr)/C_*(A).
$$

Untuk langkah terakhir, pakai diagram

$$
\begin{array}{ccccccccc}
0&\to&C_*(A)&\to&C_*^{\mathcal U}(X)&\to&C_*^{\mathcal U}(X)/C_*(A)&\to&0\\
&&\Vert&&\downarrow&&\downarrow\\
0&\to&C_*(A)&\to&C_*(X)&\to&C_*(X)/C_*(A)&\to&0.
\end{array}
$$

Diagram barisan eksak panjang dalam homologi yang diinduksi kedua barisan
eksak pendek itu komutatif. Pemetaan kiri adalah
identitas dan pemetaan tengah menginduksi isomorfisma menurut FOM-PR-05; lemma
lima memberi isomorfisma pada suku hasil bagi. Setelah identifikasi di atas,
inilah isomorfisma eksisi
$H_*(B,A\cap B)\cong H_*(X,A)$.
:::

::: {.exercise #o012-fom-u004-part-a-mcheck-003 data-origin="edition-original" data-course-route-unit-id="D60-R11"}
**Pemeriksaan Penguasaan F4A.3 (homologi lokal dan dimensi).** Untuk
$x\in\mathbb R^n$, hitung

$$
H_k(\mathbb R^n,\mathbb R^n\setminus\{x\})
$$

pada setiap $k\geq0$, termasuk $n=0$. Lalu tunjukkan bahwa tidak ada
homeomorfisma antara dua himpunan terbuka tak kosong di $\mathbb R^n$ dan
$\mathbb R^m$ bila $n\ne m$. Terakhir, jelaskan mengapa syarat “tak kosong”
tidak boleh dihapus.
:::

::: {.hint #o012-fom-u004-part-a-hint-003 data-origin="edition-original"}
**Petunjuk.** Untuk $n\geq1$, gunakan kontraktibilitas $\mathbb R^n$ dan
$\mathbb R^n\setminus\{x\}\simeq S^{n-1}$ dalam barisan eksak panjang
pasangan. Untuk $n=0$, hitung pasangan $(\{x\},\varnothing)$ langsung. Ingat
bahwa himpunan kosong terbuka di setiap ruang Euklides.
:::

::: {.solution #o012-fom-u004-part-a-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan F4A.3.** Untuk $n\geq1$, barisan eksak panjang dan
kontraktibilitas ruang Euklides memberi, untuk $k\geq1$,

$$
H_k(\mathbb R^n,\mathbb R^n\setminus\{x\})
\cong\widetilde H_{k-1}(S^{n-1})
\cong
\begin{cases}
\mathbb Z,&k=n,\\
0,&k\ne n.
\end{cases}
$$

Pada $k=0$, pemetaan
$H_0(\mathbb R^n\setminus\{x\})\to H_0(\mathbb R^n)$ surjektif karena
komplemen tak kosong dan ruang Euklides terhubung lintasan. Eksakitas memberi
$H_0(\mathbb R^n,\mathbb R^n\setminus\{x\})=0$, sesuai dengan rumus per kasus.

Pada $n=0$, $\mathbb R^0=\{x\}$ dan komplemennya kosong, jadi
$H_0(\{x\},\varnothing)\cong\mathbb Z$ serta grup derajat lain nol; rumus yang
sama tetap berlaku. Jika $U\subseteq\mathbb R^n$ dan
$V\subseteq\mathbb R^m$ terbuka tak kosong serta $f\colon U\to V$
homeomorfisma, pilih $x\in U$. Eksisi dan $f$ memberi

$$
H_k(\mathbb R^n,\mathbb R^n\setminus\{x\})
\cong H_k(U,U\setminus\{x\})
\cong H_k(V,V\setminus\{f(x)\})
\cong H_k(\mathbb R^m,\mathbb R^m\setminus\{f(x)\}).
$$

Derajat tunggal tempat grup ini $\mathbb Z$ harus sama, sehingga $n=m$.
Tanpa syarat tak kosong, $U=V=\varnothing$ memberi homeomorfisma untuk setiap
pasangan $n,m$ dan membantah kesimpulan.
:::

::: {.exercise #o012-fom-u004-part-a-mcheck-004 data-origin="edition-original" data-course-route-unit-id="D60-R11"}
**Pemeriksaan Penguasaan F4A.4 (generator sfera dan jumlah baji).** Bentuk
$S^n$ dari dua simpleks $\Delta_1^n$ dan $\Delta_2^n$ dengan batas yang
diidentifikasi menurut urutan titik sudut.

1. Buktikan bahwa $\sigma_1-\sigma_2$ merupakan siklus singular.
2. Gunakan pasangan $(S^n,\Delta_2^n)$ untuk membuktikan bahwa kelasnya
   menghasilkan $\widetilde H_n(S^n)$.
3. Untuk koleksi pasangan baik $(X_\alpha,x_\alpha)$, tentukan arah yang benar
   bagi $\bigoplus_\alpha(i_\alpha)_*$ dan jelaskan mengapa pemetaan itu
   isomorfisma.
:::

::: {.hint #o012-fom-u004-part-a-hint-004 data-origin="edition-original"}
**Petunjuk.** Dua batas berorientasi sama setelah identifikasi, sehingga saling
menghapus dalam selisih. Dalam homologi relatif terhadap $\Delta_2^n$, suku
$\sigma_2$ menjadi nol. Untuk jumlah baji, mulai dari gabungan lepas dan
runtuhkan semua titik dasar menjadi satu titik.
:::

::: {.solution #o012-fom-u004-part-a-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan F4A.4.** Identifikasi batas yang mempertahankan urutan
titik sudut memberi $\partial\sigma_1=\partial\sigma_2$, maka

$$
\partial(\sigma_1-\sigma_2)=0.
$$

Karena $\Delta_2^n$ kontraktibel, barisan eksak panjang pasangan memberi

$$
\widetilde H_n(S^n)\cong H_n(S^n,\Delta_2^n).
$$

Eksisi atau teorema hasil bagi kemudian memberi

$$
H_n(S^n,\Delta_2^n)
\cong H_n(\Delta_1^n,\partial\Delta_1^n).
$$

Di bawah kedua isomorfisma, $[\sigma_1-\sigma_2]$ dipetakan ke
$[\sigma_1]$, yang menghasilkan grup terakhir. Jadi kelas semula menghasilkan
$\widetilde H_n(S^n)$.

Setiap inklusi $i_\alpha$ berarah dari $X_\alpha$ menuju baji; karena itu
pemetaan yang bertipe benar adalah

$$
\bigoplus_\alpha(i_\alpha)_*\colon
\bigoplus_\alpha\widetilde H_k(X_\alpha)
\longrightarrow\widetilde H_k\!\left(\bigvee_\alpha X_\alpha\right).
$$

Pasangan gabungan lepas dan himpunan semua titik dasar merupakan pasangan
baik. Meruntuhkan titik-titik dasar menghasilkan baji, sedangkan kompleks
rantai gabungan lepas terurai sebagai jumlah langsung kompleks rantai
komponennya. Jika
$j_\alpha\colon X_\alpha\to\bigsqcup_\beta X_\beta$ adalah inklusi komponen
dan $q$ pemetaan hasil bagi menuju baji, maka
$q\circ j_\alpha=i_\alpha$. Karena isomorfisma hasil bagi relatif dan
dekomposisi menurut komponen bersifat alami, invers dari isomorfisma

$$
\widetilde H_k\!\left(\bigvee_\alpha X_\alpha\right)
\cong\bigoplus_\alpha\widetilde H_k(X_\alpha)
$$

tepat $\bigoplus_\alpha(i_\alpha)_*$. Jadi pemetaan yang ditampilkan pada
pernyataan memang isomorfisma.
:::

::: {.boundary #o012-fom-u004-part-a-boundary-001}
**Batas sumber bagian.** Draf ini menerjemahkan
`algebraic_topology.tex` baris 1923–2440 secara kontigu, mencakup Bagian 1.7
tentang eksisi, teorema rantai kecil, homologi lokal, generator relatif
simpleks dan sfera, serta homologi jumlah baji. Ia menutup kedua lokus
FOM-PR-05 dan lokus FOM-PR-06 dengan bukti mandiri lengkap. Kursor sumber
berikutnya adalah baris 2441, awal Bagian 1.8 tentang Mayer–Vietoris.
:::
