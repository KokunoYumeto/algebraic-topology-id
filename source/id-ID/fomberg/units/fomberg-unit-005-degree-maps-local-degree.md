---
title: "Topologi Aljabar"
subtitle: "Komponen Fomberg 5: Derajat Pemetaan dan Derajat Lokal"
author:
  - "Yeheli Fomberg (catatan sumber; berdasarkan kuliah Nir Lazarovich)"
  - "Edisi Bahasa Indonesia dengan perbaikan bukti dan pendamping penguasaan"
date: "25 Agustus 2026"
lang: id-ID
rights: "Sumber dan adaptasi: CC BY-SA 4.0; lihat atribusi dan catatan perubahan di bawah."
source_component: "Fomberg Algebraic Topology, Section 1.11"
source_lines: "2847-3122"
edition_unit_id: "O012-FOM-005"
course_route_unit_id: "D60-R12"
route_status: "pembandingan derajat opsional; jembatan derajat lokal aditif"
status: "terjemahan kontigu dengan perbaikan bukti dan penguasaan lengkap"
---

# Tentang komponen ini {.unnumbered #o012-fom-u005-notice data-course-route-unit-id="D60-R12"}

Komponen ini merupakan terjemahan dan adaptasi bahasa Indonesia atas Bagian
1.11 *Algebraic Topology* karya Yeheli Fomberg, berdasarkan kuliah Nir
Lazarovich pada musim semi 2025. Otoritas sumber dibekukan pada commit
[563194fae879178b9a6871b249513bfc27968975](https://git.sr.ht/~yp/math-notes/tree/563194fae879178b9a6871b249513bfc27968975/item/algebraic_topology.tex).
Rentang yang diterjemahkan ialah `algebraic_topology.tex` baris 2847–3122:
276 baris fisik, 12.203 byte setelah normalisasi LF dan satu LF penutup,
dengan SHA-256
`9ac1d27872a09134b75bb077ad113716a9e828c2177ac296e7bf3331395da85a`.

Catatan sumber tersedia di bawah
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
Terjemahan, pemformatan semantik, koreksi terbatas, perbaikan bukti FOM-PR-12,
dan materi penguasaan asli di bawah ini diterbitkan dengan lisensi yang sama.
Semua perbaikan dibedakan dari teks sumber. Tidak ada prosa dari bank soal
Fomberg terpisah maupun materi MIT yang disalin ke dalam komponen ini.

Jalur wajib Roberts Unit 30 sudah memuat
[definisi derajat](#o012-rbt-l30-def-002),
[sifat-sifatnya](#o012-rbt-l30-prop-001),
[lema teknis](#o012-rbt-l30-lem-001),
[akibatnya](#o012-rbt-l30-cor-001),
[teorema sfera berbulu](#o012-rbt-l30-thm-003), dan
[buktinya](#o012-rbt-l30-proof-004).
Karena itu, bagian derajat Fomberg dipertahankan sebagai pembandingan opsional;
definisi derajat lokal, rumus lokal-ke-global, dan enam pemeriksaan penguasaan
memberi lapisan aditif. Rujukan teorema dasar aljabar diarahkan ke
[bukti mandiri Roberts](#o012-rbt-l30-proof-002).

Sumber mengulang satu TikZ-CD besar pada definisi dan bukti derajat lokal.
Edisi memecahnya menjadi satu diagram lokal yang dapat direflow dan satu
inventaris peta pusat yang bertipe jelas; tidak ada aset raster baru atau
informasi matematis yang dibuang.

Edisi ini independen dan tidak menyiratkan dukungan, pengesahan, atau
afiliasi dengan Yeheli Fomberg, Nir Lazarovich, ataupun institusi mereka.
Produksi terjemahan, struktur semantik, dan QA dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna.

# Derajat Pemetaan dan Derajat Lokal {#o012-fom-u005 data-source-lines="2847-3122" data-course-route-unit-id="D60-R12"}

## Derajat pemetaan {#o012-fom-u005-s11a data-origin="source-derived" data-source-lines="2847-2940"}

::: {.definition #o012-fom-u005-def-degree data-origin="source-derived" data-source-lines="2849-2854"}
**Definisi (derajat suatu pemetaan).** Misalkan
$f\colon S^n\to S^n$ kontinu dan $n\geq0$. Setelah memilih pembangkit orientasi
$u\in\widetilde H_n(S^n;\mathbb Z)\cong\mathbb Z$, homomorfisma terinduksi

$$
f_*\colon\widetilde H_n(S^n;\mathbb Z)
\longrightarrow\widetilde H_n(S^n;\mathbb Z)
$$

ditentukan oleh satu bilangan bulat $k$ melalui

$$
f_*(u)=ku.
$$

Bilangan

$$
\deg(f):=k
$$

disebut **derajat** $f$.
:::

::: {.source-audit #o012-fom-u005-audit-degree-reduced-homology data-origin="edition-original" data-source-lines="2849-2853,2882-2887" data-adverse-candidate-id="FOM-U005A-ADV-001"}
**Koreksi derajat nol.** Sumber memakai $H_n(S^n)\cong\mathbb Z$ tanpa
membatasi $n$. Pernyataan itu salah pada $n=0$, sebab
$H_0(S^0)\cong\mathbb Z^2$. Selain itu, bukti sifat ketiga memakai
$H_n(S^n\setminus\{y\})=0$, yang juga salah pada $n=0$ untuk homologi biasa.
Edisi memakai homologi tereduksi:

$$
\widetilde H_n(S^n)\cong\mathbb Z,
\qquad
\widetilde H_n(S^n\setminus\{y\})=0
$$

untuk setiap $n\geq0$. Pada $n\geq1$ definisi ini sama dengan definisi sumber.
Perbaikan tersebut juga membuat pernyataan berikut dan teorema sfera berbulu
berlaku seragam pada $S^0$.
:::

::: {.proposition #o012-fom-u005-prop-degree-properties data-origin="source-derived" data-source-lines="2856-2875"}
**Proposisi (sifat-sifat derajat).** Untuk pemetaan kontinu
$f,g\colon S^n\to S^n$, derajat mempunyai sifat-sifat berikut.

1. $\deg(\operatorname{id})=1$.
2. $\deg(f\circ g)=\deg(f)\deg(g)$.
3. Jika $f$ tidak surjektif, maka $\deg(f)=0$.
4. Jika $f$ suatu refleksi sfera yang diinduksi oleh refleksi linear terhadap
   hiperbidang melalui titik asal, maka $\deg(f)=-1$.
5. Untuk peta antipodal $a\colon S^n\to S^n$, $a(x)=-x$,

   $$
   \deg(a)=\deg(-\operatorname{id})=(-1)^{n+1}.
   $$

6. Jika $f$ suatu homeomorfisma, maka $\deg(f)=\pm1$.
7. Jika $f\simeq g$, maka $\deg(f)=\deg(g)$.
8. Jika $f$ tidak mempunyai titik tetap, maka

   $$
   \deg(f)=(-1)^{n+1}.
   $$

9. Misalkan $n$ genap dan sebuah grup $G$ beraksi bebas pada $S^n$, yakni

   $$
   g\cdot x=x\Longrightarrow g=1_G.
   $$

   Maka $G\cong1$ atau $G\cong\mathbb Z_2$.
:::

::: {.proof #o012-fom-u005-proof-degree-properties data-origin="source-derived" data-source-lines="2876-2932" data-proof-status="source-complete"}
**Bukti.**

1. Karena $(\operatorname{id})_*=\operatorname{id}_{\mathbb Z}$, derajat
   identitas adalah $1$.

2. Fungtorialitas memberi

   $$
   (f\circ g)_*=f_*\circ g_*.
   $$

   Jika $g_*(u)=du$ dan $f_*(u)=eu$, maka
   $(f\circ g)_*(u)=deu$. Jadi
   $\deg(f\circ g)=\deg(f)\deg(g)$.

3. Jika $f$ tidak surjektif, pilih $y\notin f(S^n)$. Pemetaan $f$ memfaktor
   sebagai

   $$
   S^n\xrightarrow{\ \bar f\ }S^n\setminus\{y\}
   \xrightarrow{\ i\ }S^n,
   $$

   dengan $i$ pemetaan inklusi. Karena
   $\widetilde H_n(S^n\setminus\{y\})=0$, pemetaan terinduksi $f_*$ nol.
   Maka $\deg(f)=0$.

4. Realisasikan $S^n$ sebagai dua simpleks berorientasi
   $\Delta_1^n$ dan $\Delta_2^n$ yang direkatkan sepanjang batasnya dengan
   orientasi muka yang sama. Pembangkit homologi puncaknya ialah

   $$
   [\Delta_1^n-\Delta_2^n]
   \in\widetilde H_n(S^n)\cong\mathbb Z.
   $$

   Refleksi menukar kedua simpleks. Karena itu

   $$
   f_*[\Delta_1^n-\Delta_2^n]
   =[\Delta_2^n-\Delta_1^n]
   =-[\Delta_1^n-\Delta_2^n],
   $$

   sehingga $\deg(f)=-1$.

5. Peta antipodal

   $$
   (x_1,x_2,\ldots,x_{n+1})
   \longmapsto
   (-x_1,-x_2,\ldots,-x_{n+1})
   $$

   adalah komposisi $n+1$ refleksi koordinat. Menurut butir 2 dan 4,

   $$
   \deg(-\operatorname{id})=(-1)^{n+1}.
   $$

6. Argumen yang sama berlaku lebih umum bagi ekuivalensi homotopi. Dengan
   memakai invariansi homotopi pada butir 7, jika $g$
   invers homotopi bagi $f$, maka $f\circ g\simeq\operatorname{id}$ dan

   $$
   1=\deg(\operatorname{id})
   =\deg(f\circ g)
   =\deg(f)\deg(g).
   $$

   Dua bilangan bulat yang hasil kalinya $1$ masing-masing bernilai $\pm1$.
   Khususnya, homeomorfisma mempunyai derajat $\pm1$.

7. Jika $f\simeq g$, invariansi homotopi homologi memberi $f_*=g_*$. Maka
   $\deg(f)=\deg(g)$.

8. Andaikan $f$ tidak mempunyai titik tetap. Pemetaan

   $$
   H(x,t)=
   \frac{t f(x)+(1-t)(-x)}
        {\lVert t f(x)+(1-t)(-x)\rVert}
   $$

   terdefinisi untuk $x\in S^n$ dan $t\in[0,1]$. Memang, ruas penyebut tidak
   pernah nol: secara geometris, jika $f(x)\ne x$, ruas garis yang
   menghubungkan $f(x)$ dan $-x$ tidak melalui titik asal. Nilai ujungnya
   adalah

   $$
   H(x,0)=-x,
   \qquad
   H(x,1)=f(x).
   $$

   Jadi $f$ homotop dengan peta antipodal. Butir 5 dan 7 memberi

   $$
   \deg(f)=(-1)^{n+1}.
   $$

9. Aksi $G$ pada $S^n$ merupakan homomorfisma dari $G$ ke grup
   homeomorfisma $S^n$. Tulis juga $g$ untuk homeomorfisma yang diberikan
   oleh suatu elemen grup. Menurut butir 6,

   $$
   \deg\colon G\longrightarrow\{+1,-1\},
   \qquad
   g\longmapsto\deg(g),
   $$

   terdefinisi, dan butir 2 menunjukkan bahwa ia homomorfisma. Karena aksinya
   bebas, setiap $g\ne1_G$ tidak mempunyai titik tetap. Untuk $n$ genap,
   butir 8 karena itu memberi $\deg(g)=(-1)^{n+1}=-1$. Dengan demikian

   $$
   \ker(\deg)=\{1_G\},
   $$

   sehingga $\deg$ injektif. Jadi $G$ isomorfik dengan suatu subgrup dari
   $\{+1,-1\}\cong\mathbb Z_2$, dan akibatnya
   $G\cong1$ atau $G\cong\mathbb Z_2$. $\square$
:::

::: {.source-audit #o012-fom-u005-audit-fixed-point-drawing-marker data-origin="edition-original" data-source-lines="2911-2920" data-adverse-candidate-id="FOM-U005A-ADV-006"}
**Penanda gambar sumber yang belum diwujudkan.** Komentar `%drawing` pada
baris 2911 tidak menunjuk berkas gambar atau kode gambar apa pun dalam sumber.
Edisi tidak mengarang aset pengganti: rumus homotopi, pemeriksaan bahwa
penyebutnya tidak nol, dan uraian geometris tentang ruas garis dipertahankan
secara lengkap sehingga argumennya dapat dibaca tanpa gambar.
:::

::: {.source-audit #o012-fom-u005-audit-two-simplex-gluing data-origin="edition-original" data-source-lines="2888-2893" data-adverse-candidate-id="FOM-U005A-ADV-002"}
**Koreksi konstruksi sfera.** Sumber menulis
$S^n=\Delta_1\sqcup\Delta_2$, seolah-olah sfera merupakan gabungan saling
lepas dua simpleks. Argumen pembangkit yang dipakai sebenarnya memerlukan
kedua batas simpleks direkatkan. Edisi menyatakan perekatan itu secara
eksplisit dan mempertahankan pembangkit
$[\Delta_1^n-\Delta_2^n]$ yang dimaksud.
:::

::: {.source-audit #o012-fom-u005-audit-action-subgroup-type data-origin="edition-original" data-source-lines="2921-2930" data-adverse-candidate-id="FOM-U005A-ADV-003"}
**Koreksi tipe kesimpulan aksi.** Sumber menyimpulkan $G\subset\mathbb Z_2$.
Tanpa suatu identifikasi literal yang telah dipilih, kesimpulan yang bertipe
benar ialah

$$
G\cong\operatorname{im}(\deg)
\leq\{+1,-1\}\cong\mathbb Z_2.
$$

Inilah kesimpulan yang digunakan di atas. Sumber juga berganti tanpa
penjelasan dari $S^n$ ke simbol $X$ pada baris 2923; edisi mempertahankan
sfera $S^n$ yang benar-benar sedang dikenai aksi.
:::

::: {.remark #o012-fom-u005-rem-fundamental-theorem-algebra data-origin="source-derived" data-source-lines="2933-2936" data-proof-status="external_source_problem_set_not_imported"}
**Catatan (teorema dasar aljabar).** Sifat 3 dapat dipakai untuk membuktikan
teorema dasar aljabar. Sumber merujuk pembuktiannya ke bank soal terpisah;
bank soal itu tidak termasuk komponen yang dipilih dan buktinya tidak disalin
ke dalam edisi ini. Pembaca dapat memakai
[bukti mandiri yang sudah tersedia dalam Roberts Unit 30](#o012-rbt-l30-proof-002);
tautan tersebut mengarah ke materi asli edisi yang sah, bukan ke bank soal
Fomberg.
:::

::: {.remark #o012-fom-u005-rem-hopf-theorem data-origin="source-derived" data-source-lines="2937-2940"}
**Catatan (teorema Hopf).** Untuk $n\geq1$, kebalikan sifat 7 juga benar:
dua pemetaan $f,g\colon S^n\to S^n$ homotop jika dan hanya jika
$\deg(f)=\deg(g)$. Hasil ini disebut teorema Hopf, tetapi sumber tidak
membuktikannya.
:::

::: {.source-audit #o012-fom-u005-audit-hopf-range data-origin="edition-original" data-source-lines="2937-2940" data-adverse-candidate-id="FOM-U005A-ADV-004"}
**Koreksi rentang teorema Hopf.** Sumber tidak menyatakan syarat $n\geq1$.
Pada $S^0$, dua pemetaan konstan menuju dua titik yang berbeda sama-sama
berderajat nol pada $\widetilde H_0(S^0)$, tetapi tidak homotop karena tidak
ada lintasan di $S^0$ yang menghubungkan kedua nilai tersebut. Edisi karena
itu menyatakan kebalikan sifat 7 hanya pada rentang yang sah.
:::

## Teorema sfera berbulu {#o012-fom-u005-s11b data-origin="source-derived" data-source-lines="2942-2982"}

::: {.theorem #o012-fom-u005-thm-hairy-sphere data-origin="source-derived" data-source-lines="2942-2948"}
**Teorema (teorema sfera berbulu).** Untuk setiap $n\geq0$, terdapat medan
vektor tangen kontinu yang tidak pernah nol pada $S^n$ jika dan hanya jika
$n$ ganjil. Secara ekuivalen, medan semacam itu tidak ada jika dan hanya jika
$n$ genap.
:::

::: {.proof #o012-fom-u005-proof-hairy-sphere data-origin="source-derived" data-source-lines="2949-2982" data-proof-status="source-complete"}
**Bukti.** Andaikan

$$
v\colon S^n\longrightarrow\mathbb R^{n+1}
$$

suatu medan vektor tangen kontinu yang tidak pernah nol; jadi $v(x)$ tangen
pada $S^n$ di $x$. Kita akan menunjukkan bahwa $n$ harus ganjil. Karena
$v(x)\ne0$ untuk setiap $x$, ganti $v(x)$ dengan
$v(x)/\lVert v(x)\rVert$ sehingga

$$
\lVert v(x)\rVert=1
$$

untuk setiap $x$. Vektor $x$ dan $v(x)$ ortogonal. Seperti
$\cos t+i\sin t$ yang terletak pada lingkaran satuan di bidang kompleks,
vektor

$$
(\cos t)x+(\sin t)v(x)
$$

terletak pada lingkaran satuan di bidang yang direntang oleh $x$ dan $v(x)$.
Secara eksplisit, tangensi memberi $x\mathbin{\cdot}v(x)=0$, sehingga

$$
\begin{aligned}
\lVert(\cos t)x+(\sin t)v(x)\rVert^2
&=\cos^2t\,\lVert x\rVert^2
  +\sin^2t\,\lVert v(x)\rVert^2
  +2\cos t\sin t\,x\mathbin{\cdot}v(x)\\
&=\cos^2t+\sin^2t=1.
\end{aligned}
$$

Karena itu,

$$
H\colon S^n\times[0,1]\longrightarrow S^n,
\qquad
H(x,t)=\cos(\pi t)x+\sin(\pi t)v(x),
$$

merupakan homotopi dari pemetaan identitas ke peta antipodal. Maka

$$
1=\deg(\operatorname{id})
=\deg(-\operatorname{id})
=(-1)^{n+1}.
$$

Jadi $n$ harus ganjil.

Sebaliknya, andaikan $n$ ganjil. Tuliskan $n=2k-1$ untuk suatu
$k\geq1$. Definisikan

$$
v(x_1,x_2,\ldots,x_{2k-1},x_{2k})
=(-x_2,x_1,\ldots,-x_{2k},x_{2k-1}).
$$

Rumus ini merupakan pembatasan pada $S^{2k-1}$ dari suatu transformasi linear
$\mathbb R^{2k}\to\mathbb R^{2k}$, sehingga $v$ kontinu. Untuk setiap
$x\in S^{2k-1}$,

$$
\begin{aligned}
x\mathbin{\cdot}v(x)
&=\sum_{j=1}^{k}
  \bigl(x_{2j-1}(-x_{2j})+x_{2j}x_{2j-1}\bigr)=0,\\
\lVert v(x)\rVert^2
&=\sum_{j=1}^{k}
  \bigl(x_{2j}^2+x_{2j-1}^2\bigr)
 =\lVert x\rVert^2=1.
\end{aligned}
$$

Persamaan pertama membuktikan tangensi, sedangkan persamaan kedua membuktikan
bahwa $v(x)$ tidak pernah nol. Jadi $v$ merupakan medan vektor tangen kontinu
yang tidak pernah nol. Ini menyelesaikan pembuktian. $\square$
:::

::: {.source-audit #o012-fom-u005-audit-source-typography data-origin="edition-original" data-source-lines="2889,2922-2923,2966,2980" data-adverse-candidate-id="FOM-U005A-ADV-005"}
**Normalisasi tipografi dan simbol sumber.** Edisi memperbaiki lima cacat deterministik
tanpa mengubah isi: *orientatoin* menjadi *orientation* pada baris 2889,
*homomoprhism* menjadi *homomorphism* pada baris 2922, simbol tak terikat $X$
menjadi sfera $S^n$ yang sedang dibahas pada baris 2923, frasa yang kehilangan
kata kerja pada baris 2966, dan susunan “is a evidently” pada baris 2980.
:::

## Derajat lokal {#o012-fom-u005-local-degree data-origin="source-derived" data-source-lines="2984-3121"}

**Derajat homologis** yang dinotasikan $\deg$ pada komponen Fomberg ini
menyatakan bilangan yang sama dengan **derajat kohomologis**
$\operatorname{Deg}$ pada Roberts Unit 30.
[Pemeriksaan F5.1](#o012-fom-u005-mcheck-001) di bawah membuktikan kesamaan
itu melalui kealamian pasangan Kronecker dan pembangkit orientasi yang
kompatibel.

::: {.definition #o012-fom-u005-def-local-degree data-origin="source-derived" data-source-label="def:local-degree" data-source-lines="2984-3019" data-repair-id="FOM-PR-12"}
**Definisi (derajat lokal).** Misalkan $n\geq1$,
$f\colon S^n\to S^n$ pemetaan kontinu, dan pilih $y\in S^n$ dengan
prabayangan hingga

$$
f^{-1}(y)=\{x_1,\ldots,x_m\}.
$$

Pilih lingkungan terbuka $V$ dari $y$ dan lingkungan terbuka saling lepas
$U_1,\ldots,U_m$ dari titik-titik $x_i$ sedemikian sehingga

$$
f(U_i)\subseteq V,
\qquad
f(U_i\setminus\{x_i\})\subseteq V\setminus\{y\}
$$

untuk setiap $1\leq i\leq m$. Pembatasan $f|_{U_i}$ merupakan peta pasangan

$$
(U_i,U_i\setminus\{x_i\})
\longrightarrow
(V,V\setminus\{y\}).
$$

Eksisi memberi isomorfisma vertikal dalam diagram komutatif berikut. Panah
bawah $\lambda_i$ adalah pemetaan homologi lokal yang diperoleh dengan
mengangkut $(f|_{U_i})_*$ melalui kedua isomorfisma itu:

:::: {.figure #o012-fom-u005-fig-local-degree data-source-lines="2992-3013" data-origin="source-derived" data-rendering="semantic-reflow"}
$$
\begin{aligned}
H_n(U_i,U_i\setminus\{x_i\})
&\xrightarrow{\ (f|_{U_i})_*\ }
H_n(V,V\setminus\{y\})\\
\mathord{\downarrow}\scriptstyle\cong
&\qquad\mathord{\downarrow}\scriptstyle\cong\\
H_n(S^n,S^n\setminus\{x_i\})
&\xrightarrow{\ \lambda_i\ }
H_n(S^n,S^n\setminus\{y\}).
\end{aligned}
$$

**Diagram semantik.** Grup kiri-atas adalah homologi lokal pada $x_i$ yang
dihitung di lingkungan $U_i$; grup kanan-atas adalah homologi lokal pada $y$
yang dihitung di $V$. Inklusi kedua lingkungan ke $S^n$ memberi kedua
isomorfisma eksisi. Panah mendatar atas diinduksi oleh $f|_{U_i}$; panah
mendatar bawah ialah pemetaan yang sama setelah identifikasi eksisi.
Komutativitas menyatakan bahwa hasilnya tidak bergantung pada apakah homologi
lokal dihitung di lingkungan kecil atau di seluruh sfera. Panah
$\lambda_i$ bukan peta pasangan global yang secara keliru membuang
prabayangan lain; ia didefinisikan dari pembatasan lokal di atas.
::::

Orientasi standar $S^n$ menentukan pembangkit lokal yang kompatibel, sehingga
keempat grup itu dapat diidentifikasi dengan $\mathbb Z$. Pemetaan
$\lambda_i$ kemudian berbentuk $1\mapsto d_i$ untuk suatu
$d_i\in\mathbb Z$.
**Derajat lokal $f$ di $x_i$**, relatif terhadap nilai $y$, adalah

$$
\deg_{x_i}(f):=d_i.
$$
:::

::: {.proof-supplement #o012-fom-u005-proof-local-degree-independence data-origin="edition-original" data-source-lines="2984-3018" data-repair-id="FOM-PR-12" data-proof-status="complete_original_repair"}
**Kebebasan dari pilihan lingkungan.** Ambil dua pilihan yang memenuhi syarat,
yakni $(V,U_i)$ dan $(V',U_i')$. Pilih lingkungan terbuka
$W\subseteq V\cap V'$ dari $y$. Untuk setiap $i$, kontinuitas $f$ dan fakta
bahwa $x_i$ adalah satu-satunya titik serat di lingkungan yang cukup kecil
memungkinkan kita memilih bola koordinat terbuka $W_i$ dengan

$$
x_i\in W_i\subseteq U_i\cap U_i'\cap f^{-1}(W).
$$

Pembatasan $f|_{W_i}$ adalah peta pasangan menuju
$(W,W\setminus\{y\})$. Inklusi $W_i\hookrightarrow U_i$ dan
$W\hookrightarrow V$ memberi persegi alami

$$
\begin{aligned}
H_n(W_i,W_i\setminus\{x_i\})
&\xrightarrow{\ (f|_{W_i})_*\ }
H_n(W,W\setminus\{y\})\\
\mathord{\downarrow}\scriptstyle\cong
&\qquad\mathord{\downarrow}\scriptstyle\cong\\
H_n(U_i,U_i\setminus\{x_i\})
&\xrightarrow{\ (f|_{U_i})_*\ }
H_n(V,V\setminus\{y\}),
\end{aligned}
$$

dan ada persegi yang sama untuk pilihan beraksen. Semua panah vertikal ialah
isomorfisma eksisi. Setelah keempat grup diangkut ke grup homologi lokal
global, kealamian kedua persegi menunjukkan bahwa kedua pilihan menghasilkan
homomorfisma $\lambda_i$ yang sama. Pembangkit orientasi pada lingkungan kecil
adalah pembatasan pembangkit orientasi sfera, sehingga bilangan bulat
$d_i=\deg_{x_i}(f)$ juga sama. Jadi derajat lokal terdefinisi dengan baik.
$\square$
:::

::: {.source-audit #o012-fom-u005-audit-local-degree-typing data-origin="edition-original" data-source-lines="2986-3018" data-repair-id="FOM-PR-12"}
**Koreksi notasi, indeks, dan tipe pemetaan.** Baris 2987 sumber menulis
`$f(y)^{-1}$`, padahal himpunan yang diperlukan adalah $f^{-1}(y)$. Baris
2991 memakai batas indeks $i\leq n$, yang tidak cocok dengan pencacahan
$x_1,\ldots,x_m$; edisi memakai $i\leq m$. Sumber juga menyebut $V$ sebagai
“citra semua lingkungan” tanpa terlebih dahulu memastikan bahwa $V$
merupakan lingkungan $y$, lalu menulis pembatasan bertipe tidak jelas
`$(f_i)|_U$`. Edisi memilih $V$ dan $U_i$ secara eksplisit sehingga
$f|_{U_i}$ benar-benar merupakan peta pasangan di atas. Terakhir, tanda
derajat lokal memerlukan pembangkit orientasi yang kompatibel; syarat ini
dibuat eksplisit. Struktur homologi dan nilai bilangan bulat yang dimaksud
sumber tidak diubah.
:::

::: {.source-audit #o012-fom-u005-audit-local-degree-range data-origin="edition-original" data-source-lines="2984-3018" data-repair-id="FOM-PR-12"}
**Koreksi rentang dimensi.** Sumber tidak memberi syarat pada $n$, padahal
untuk $n=0$ panah
$H_0(S^0)\to H_0(S^0,S^0\setminus\{x\})$ yang dipakai pada bagian bawah
diagram bukan isomorfisma. Edisi karena itu membatasi definisi lokal dan rumus
lokal-ke-global di bawah pada $n\geq1$. Definisi derajat global sebelumnya
tetap mencakup $n=0$ dengan homologi tereduksi; edisi tidak mengklaim varian
derajat lokal tereduksi pada dimensi nol.
:::

::: {.source-omission #o012-fom-u005-omission-pr12 data-origin="edition-original" data-source-lines="2984-3018" data-repair-id="FOM-PR-12"}
**Langkah formal yang tidak tersedia dalam sumber.** Agar tanda derajat lokal
dan rumus jumlah berikutnya terdefinisi, pemilihan lingkungan harus memberi
peta pasangan yang sah, isomorfisma eksisi harus diikat ke orientasi sfera,
kebebasan dari pilihan lingkungan harus dibuktikan, dan pembangkit global harus
diselaraskan dengan semua pembangkit lokal. Definisi di atas, suplemen
kebebasan pilihan, dan bukti di bawah menyediakan penutupan FOM-PR-12 secara
eksplisit.
:::

::: {.remark #o012-fom-u005-rem-local-homeomorphism data-origin="source-derived" data-source-lines="3021-3035"}
**Catatan.** Misalkan $f\colon S^n\to S^n$ homeomorfisma. Untuk setiap
$x\in S^n$, ambil $y=f(x)$. Karena $f^{-1}(y)=\{x\}$ dan semua pemetaan pada
diagram derajat lokal adalah isomorfisma,

$$
\deg_x(f)=\pm1.
$$

Lebih umum, jika setiap pembatasan
$f|_{U_i}\colon U_i\to V$ merupakan homeomorfisma, maka
$\deg_{x_i}(f)=\pm1$. Tanda positif berarti orientasi lokal dipertahankan,
sedangkan tanda negatif berarti orientasi lokal dibalik. Proposisi berikut
menjelaskan bagaimana bilangan-bilangan lokal ini menentukan derajat global.
:::

::: {.proposition #o012-fom-u005-prop-local-to-global data-origin="source-derived" data-source-label="prop:local-degree-for-global-degree" data-source-lines="3037-3041" data-repair-id="FOM-PR-12"}
**Proposisi (rumus derajat lokal-ke-global).** Misalkan $n\geq1$,
$f\colon S^n\to S^n$ kontinu, dan $y\in S^n$ mempunyai prabayangan hingga
$f^{-1}(y)=\{x_1,\ldots,x_m\}$. Maka

$$
\deg(f)=\sum_{i=1}^{m}\deg_{x_i}(f).
$$
:::

::: {.source-audit #o012-fom-u005-audit-local-global-formula data-origin="edition-original" data-source-lines="3037-3041"}
**Koreksi operator pada rumus.** Baris 3040 sumber menulis
$\sum_i\operatorname{del}(f|_{x_i})$—makro `\del` hanya membentuk tanda
kurung dan bukan operator derajat. Edisi menampilkan operator yang bertipe
benar, yaitu $\deg_{x_i}(f)$.
:::

::: {.proof #o012-fom-u005-proof-local-to-global data-origin="source-derived" data-source-lines="3042-3074" data-repair-id="FOM-PR-12" data-proof-status="complete_edition_repair_of_source_argument"}
**Bukti.** Selain grup-grup lokal pada definisi, pertimbangkan grup relatif

$$
H_n\bigl(S^n,S^n\setminus f^{-1}(y)\bigr).
$$

Eksisi pada lingkungan saling lepas $U_1,\ldots,U_m$ memberi dekomposisi

$$
H_n\bigl(S^n,S^n\setminus f^{-1}(y)\bigr)
\cong
\bigoplus_{i=1}^{m}H_n(U_i,U_i\setminus\{x_i\})
\cong\mathbb Z^m.
$$

Untuk mencatat seluruh jaringan pemetaan pada dua diagram sumber, tuliskan
$\iota_i$ untuk inklusi suku ke-$i$, $p_i$ untuk proyeksi ke suku ke-$i$,
dan

$$
M=H_n\bigl(S^n,S^n\setminus f^{-1}(y)\bigr),
\qquad
L_i=H_n(S^n,S^n\setminus\{x_i\}),
\qquad
L_y=H_n(S^n,S^n\setminus\{y\}).
$$

Pemetaan-pemetaan relatifnya adalah

$$
\iota_i\colon H_n(U_i,U_i\setminus\{x_i\})\longrightarrow M,
\qquad
p_i\colon M\longrightarrow L_i,
\qquad
F_*\colon M\longrightarrow L_y,
$$

dengan $F_*$ diinduksi oleh peta pasangan

$$
f\colon
\bigl(S^n,S^n\setminus f^{-1}(y)\bigr)
\longrightarrow
(S^n,S^n\setminus\{y\}).
$$

Isomorfisma eksisi mengidentifikasi domain $\iota_i$ dengan $L_i$ dan grup
lokal di $V$ dengan $L_y$; di bawah identifikasi itu,

$$
p_i\circ\iota_i=\operatorname{id},
\qquad
p_i\circ\iota_j=0\quad(j\ne i),
\qquad
F_*\circ\iota_i=\lambda_i.
$$

Pemetaan hasil bagi pada tingkat rantai menginduksi

$$
j\colon H_n(S^n)
\longrightarrow
H_n\bigl(S^n,S^n\setminus f^{-1}(y)\bigr).
$$

Tuliskan pula $q_i\colon H_n(S^n)\to L_i$ dan
$q_y\colon H_n(S^n)\to L_y$ untuk pemetaan hasil bagi. Karena $n\geq1$,
keduanya isomorfisma. Dua hubungan komutatif yang mengikat baris absolut dan
relatif pada diagram sumber adalah

$$
p_i\circ j=q_i,
\qquad
F_*\circ j=q_y\circ f_*.
$$

Jika $1\in H_n(S^n)\cong\mathbb Z$ adalah kelas fundamental yang berorientasi,
komutativitas dengan setiap proyeksi memberi

$$
(p_i\circ j)(1)=1.
$$

Karena itu, di bawah dekomposisi jumlah langsung,

$$
j(1)=(1,\ldots,1)=\sum_{i=1}^{m}\iota_i(1).
$$

Menurut definisi derajat lokal, pemetaan terinduksi $F_*$ mengirim
$\iota_i(1)$ ke
$\deg_{x_i}(f)$ kali pembangkit lokal di $y$. Jadi ia mengirim $j(1)$ ke

$$
\sum_{i=1}^{m}\deg_{x_i}(f).
$$

Di sisi lain, komutativitas dengan pemetaan
$H_n(S^n)\xrightarrow{f_*}H_n(S^n)$ menunjukkan bahwa citra yang sama adalah
$\deg(f)$ kali pembangkit tersebut. Maka

$$
\deg(f)=\sum_{i=1}^{m}\deg_{x_i}(f),
$$

seperti yang dikehendaki. $\square$
:::

::: {.source-audit #o012-fom-u005-audit-local-global-proof data-origin="edition-original" data-source-lines="3043-3073" data-repair-id="FOM-PR-12"}
**Koreksi notasi dalam bukti.** Diagram sumber memakai huruf $k_i$ sekaligus
untuk inklusi suku lokal dan untuk bilangan derajat lokal. Edisi memakai
$\iota_i$ untuk inklusi dan $d_i$ untuk bilangan, lalu menyatakan dekomposisi
lebih dahulu agar domain dan kodomain setiap pemetaan terbaca. Baris 3073
mengulang makro pembatas `\del` seolah-olah ia
operator derajat; edisi menggantinya dengan $\deg_{x_i}(f)$. Argumen
komutativitas sumber dipertahankan. Sumber menggambar ulang jaringan yang sama
pada baris 3044–3058; edisi menampilkan persegi lokal sekali lalu mencatat
secara eksplisit pemetaan pusat $M$, $\iota_i$, $p_i$, $j$, $q_i$, $q_y$,
dan $F_*$ beserta identitas komutatifnya dalam bukti. Dengan demikian, kedua kemunculan sumber
dipertahankan secara semantik tanpa menduplikasi permukaan visual yang identik.
:::

::: {.example #o012-fom-u005-ex-power-map data-origin="source-derived" data-source-lines="3076-3114"}
**Contoh (pemetaan pangkat pada lingkaran).** Untuk $k\in\mathbb Z$, definisikan

$$
f_k\colon S^1\longrightarrow S^1,
\qquad
f_k(z)=z^k.
$$

Siklus singular

$$
\gamma(t)=e^{2\pi i t},\qquad 0\leq t\leq1,
$$

mewakili pembangkit $H_1(S^1)$. Komposisi $f_k\circ\gamma$ melintasi lingkaran
sebanyak $k$ kali dengan tanda, sehingga perhitungan global sudah memberi
$\deg(f_k)=k$. Kita sekarang memperoleh hasil yang sama dari derajat lokal.

Jika $k=0$, maka
$f_0(z)=z^0=1$ adalah pemetaan konstan, sehingga
$\deg(f_0)=0$.

Sekarang andaikan $k>0$ dan pilih $y=1$. Prabayangannya ialah

$$
f_k^{-1}(1)=\{x_1,\ldots,x_k\},
\qquad
x_j=e^{2\pi i j/k},
\quad 1\leq j\leq k.
$$

Ambil busur terbuka kecil $V$ yang memuat $1$. Untuk setiap $j$, komponen
$U_j$ dari $f_k^{-1}(V)$ yang memuat $x_j$ dipetakan secara homeomorfik dan
mempertahankan orientasi ke $V$: dalam koordinat sudut, pemetaan itu
mengalikan perubahan sudut dengan $k>0$. Oleh karena itu

$$
\deg_{x_j}(f_k)=1
$$

untuk setiap $j$. Rumus lokal-ke-global memberi

$$
\deg(f_k)=\sum_{j=1}^{k}\deg_{x_j}(f_k)=k.
$$

Pemetaan $f_{-1}(z)=z^{-1}=\overline z$ adalah refleksi, sehingga
$\deg(f_{-1})=-1$. Jika $k<0$, maka $-k>0$ dan

$$
f_k=f_{-1}\circ f_{-k}.
$$

Multiplikativitas bersama kasus positif memberi

$$
\deg(f_k)=\deg(f_{-1})\deg(f_{-k})
=(-1)(-k)=k.
$$

Jadi $\deg(f_k)=k$ untuk setiap $k\in\mathbb Z$.
:::

::: {.source-audit #o012-fom-u005-audit-power-map data-origin="edition-original" data-source-lines="3076-3113"}
**Koreksi kasus nol, kasus negatif, dan lingkungan lokal.** Baris 3083
sumber menulis $z\mapsto0$, yang tidak bernilai di $S^1$; pemetaan pangkat
nol yang benar ialah $z\mapsto1$. Baris 3087 menyatakan
$f_k=f_{-1}\circ f_k$, yang tidak benar; untuk $k<0$ faktorisasi yang benar
ialah $f_k=f_{-1}\circ f_{-k}$. Baris 3093 memilih
$V=S^1\setminus\{1\}$, padahal nilai terpilih $y=1$ harus berada di dalam
$V$. Edisi memakai busur kecil di sekitar $1$ dan komponen-komponen
prabayangannya. Penalaran “peregangan homotop dengan identitas” sumber diganti
dengan koordinat sudut lokal, karena peregangan interval bukan pemetaan global
$S^1\to S^1$ yang derajatnya dapat langsung dikalikan. Baris 3079–3081
menyebut pemetaan identitas sebagai simpleks singular; edisi memakai siklus
singular $\gamma(t)=e^{2\pi it}$ yang benar-benar mewakili kelas fundamental.
:::

::: {.remark #o012-fom-u005-rem-piecewise-degree data-origin="source-derived" data-source-lines="3116-3121"}
**Catatan (kontribusi lokal bertanda).** Identifikasikan
$S^1=\mathbb R/\mathbb Z$. Ambil fungsi kontinu $F\colon[0,1]\to\mathbb R$
yang afin pada masing-masing selang
$[0,\tfrac13]$, $[\tfrac13,\tfrac23]$, dan $[\tfrac23,1]$, dengan kenaikan
berturut-turut $1$, $2$, dan $-4$. Nilai ujung setiap potongan sama dengan
nilai awal potongan berikutnya. Karena
$F(1)-F(0)=1+2-4=-1\in\mathbb Z$, proyeksi
$f([t])=[F(t)]$ memberi pemetaan kontinu $S^1\to S^1$.

Untuk nilai sasaran yang bukan citra titik-titik sambung domain, seratnya
hingga dan setiap prabayangan terletak pada bagian yang merupakan
homeomorfisma lokal. Potongan pertama memberi satu kontribusi positif,
potongan kedua memberi dua kontribusi positif, dan potongan ketiga memberi
empat kontribusi negatif. Jadi jumlah kontribusi derajat lokalnya adalah

$$
\deg(f)=1+2-4=-1.
$$

Contoh ini memperlihatkan bahwa derajat global menghitung prabayangan dengan
tanda orientasi, bukan sekadar banyaknya prabayangan.
:::

## Pemeriksaan penguasaan {#o012-fom-u005-mastery data-origin="edition-original" data-course-route-unit-id="D60-R12"}

Enam pemeriksaan berikut membentuk lapisan penguasaan asli edisi. Setiap soal
mempunyai petunjuk dan solusi lengkap; soal-soal ini tidak berasal dari bank
soal Fomberg yang tidak dipilih.

::: {.exercise #o012-fom-u005-mcheck-001 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F5.1 (menyamakan dua definisi derajat).** Pilih
pembangkit

$$
u\in\widetilde H_n(S^n;\mathbb Z)
$$

dan pembangkit dual

$$
\alpha\in\widetilde H^n(S^n;\mathbb Z)
$$

dengan pasangan Kronecker $\langle\alpha,u\rangle=1$. Jika

$$
f_*(u)=d_hu,
\qquad
f^*(\alpha)=d_c\alpha,
$$

kerjakan hal-hal berikut.

1. Gunakan kealamian pasangan Kronecker untuk membuktikan $d_h=d_c$.
2. Jelaskan mengapa mengganti pilihan orientasi $u$ dengan $-u$ tidak
   mengubah bilangan derajat.
3. Simpulkan bahwa definisi derajat melalui homologi pada bagian Fomberg ini
   sama dengan definisi melalui kohomologi tereduksi pada Roberts Unit 30.
:::

::: {.hint #o012-fom-u005-hint-001 data-origin="edition-original"}
**Petunjuk.** Hitung kedua ruas identitas

$$
\langle f^*\alpha,u\rangle
=\langle\alpha,f_*u\rangle.
$$

Jika orientasi dibalik, balikkan juga pembangkit dual agar nilai pasangannya
tetap $1$.
:::

::: {.solution #o012-fom-u005-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan F5.1.** Kealamian pasangan Kronecker memberi

$$
\begin{aligned}
\langle f^*\alpha,u\rangle
&=\langle d_c\alpha,u\rangle=d_c,\\
\langle\alpha,f_*u\rangle
&=\langle\alpha,d_hu\rangle=d_h.
\end{aligned}
$$

Kedua ruas sama, sehingga $d_c=d_h$. Jika $u'=-u$, maka

$$
f_*(u')=f_*(-u)=-d_hu=d_hu'.
$$

Jadi koefisien homologi tetap $d_h$. Pembangkit kohomologi dual yang
berpasangan dengan $u'$ ialah $\alpha'=-\alpha$, dan perhitungan yang sama menunjukkan
koefisien kohomologinya tetap $d_c$. Dengan demikian, kedua konstruksi
menghasilkan bilangan bulat yang sama dan tidak bergantung pada pembalikan
pilihan orientasi bersama. Definisi Fomberg dan Roberts karenanya kompatibel.
:::

::: {.exercise #o012-fom-u005-mcheck-002 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F5.2 (derajat sebagai kriteria titik tetap).**
Misalkan $f\colon S^n\to S^n$ kontinu.

1. Buktikan bahwa

   $$
   t f(x)+(1-t)(-x)=0
   $$

   untuk suatu $x\in S^n$ dan $t\in[0,1]$ jika dan hanya jika
   $t=\tfrac12$ dan $f(x)=x$.
2. Turunkan bahwa

   $$
   \deg(f)\ne(-1)^{n+1}
   \quad\Longrightarrow\quad
   f\text{ mempunyai titik tetap}.
   $$

3. Buktikan sebagai akibat bahwa setiap pemetaan-diri kontinu
   $S^n\to S^n$ yang tidak surjektif mempunyai titik tetap.
:::

::: {.hint #o012-fom-u005-hint-002 data-origin="edition-original"}
**Petunjuk.** Ambil norma pada persamaan di butir pertama. Untuk butir kedua,
gunakan kontraposisi sifat 8. Untuk butir ketiga, gabungkan sifat 3 dengan
fakta bahwa $0\ne(-1)^{n+1}$.
:::

::: {.solution #o012-fom-u005-sol-002 data-origin="edition-original"}
**Solusi Pemeriksaan F5.2.** Jika
$t f(x)+(1-t)(-x)=0$, maka

$$
t f(x)=(1-t)x.
$$

Karena $\lVert f(x)\rVert=\lVert x\rVert=1$, mengambil norma memberi
$t=1-t$, jadi $t=\tfrac12$. Substitusi kembali menghasilkan $f(x)=x$.
Sebaliknya, jika $t=\tfrac12$ dan $f(x)=x$, kedua suku jelas saling
menghapus.

Karena itu, bila $f$ tidak mempunyai titik tetap, penyebut pada homotopi

$$
H(x,t)=
\frac{t f(x)+(1-t)(-x)}
     {\lVert t f(x)+(1-t)(-x)\rVert}
$$

tidak pernah nol. Homotopi tersebut menghubungkan peta antipodal dengan $f$,
sehingga

$$
\deg(f)=\deg(-\operatorname{id})=(-1)^{n+1}.
$$

Kontraposisinya memberi kriteria titik tetap pada pernyataan. Jika $f$ tidak
surjektif, sifat 3 memberi $\deg(f)=0$. Karena
$0\ne(-1)^{n+1}$, kriteria tadi menjamin bahwa $f$ mempunyai titik tetap.
:::

::: {.exercise #o012-fom-u005-mcheck-003 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F5.3 (aksi bebas pada sfera genap).** Misalkan $n$
genap dan $G$ beraksi bebas pada $S^n$.

1. Tunjukkan bahwa elemen identitas berderajat $+1$, sedangkan setiap elemen
   nonidentitas berderajat $-1$.
2. Jika $a,b\in G$ adalah dua elemen nonidentitas yang berbeda, terapkan
   derajat pada $a^{-1}b$ untuk memperoleh kontradiksi.
3. Simpulkan bahwa $G$ trivial atau $G\cong\mathbb Z_2$.
4. Tunjukkan bahwa kesimpulan ini khusus bagi dimensi genap dengan memberi,
   untuk setiap $m\geq3$, aksi bebas grup siklik $C_m$ pada $S^1$.
:::

::: {.hint #o012-fom-u005-hint-003 data-origin="edition-original"}
**Petunjuk.** Aksi bebas membuat setiap elemen nonidentitas menjadi
homeomorfisma tanpa titik tetap. Untuk butir kedua, perhatikan bahwa
$a^{-1}b\ne1_G$ tetapi

$$
\deg(a^{-1}b)=\deg(a)^{-1}\deg(b).
$$

Pada $S^1\subset\mathbb C$, gunakan perkalian oleh akar kesatuan
$e^{2\pi i/m}$.
:::

::: {.solution #o012-fom-u005-sol-003 data-origin="edition-original"}
**Solusi Pemeriksaan F5.3.** Elemen identitas bertindak sebagai
$\operatorname{id}_{S^n}$ dan berderajat $+1$. Jika $g\ne1_G$, kebebasan aksi
menyatakan bahwa $g$ tidak mempunyai titik tetap. Karena $n$ genap, sifat 8
memberi

$$
\deg(g)=(-1)^{n+1}=-1.
$$

Andaikan ada dua elemen nonidentitas berbeda $a$ dan $b$. Elemen
$a^{-1}b$ nonidentitas, sehingga menurut kesimpulan tadi harus berderajat
$-1$. Namun,

$$
\deg(a^{-1}b)
=\deg(a^{-1})\deg(b)
=\deg(a)^{-1}\deg(b)
=(-1)^{-1}(-1)
=1,
$$

kontradiksi. Jadi $G$ mempunyai paling banyak satu elemen nonidentitas.
Akibatnya $G$ trivial atau mempunyai tepat dua elemen, sehingga
$G\cong\mathbb Z_2$.

Untuk melihat bahwa paritas penting, identifikasikan
$S^1=\{z\in\mathbb C:|z|=1\}$. Grup $C_m$ bertindak melalui

$$
[j]\cdot z=e^{2\pi i j/m}z.
$$

Jika $[j]\cdot z=z$, maka $e^{2\pi i j/m}=1$, sehingga $[j]=[0]$ dalam
$C_m$. Jadi aksi itu bebas. Untuk setiap $m\geq3$, grup ini bukan trivial dan
bukan $\mathbb Z_2$, sehingga kesimpulan sfera genap memang tidak meluas ke
$S^1$.
:::

::: {.exercise #o012-fom-u005-mcheck-004 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F5.4 (menghitung dengan tanda lokal).** Misalkan
$n\geq1$, $f\colon S^n\to S^n$, dan suatu $y\in S^n$ mempunyai lima prabayangan. Pada
tiga di antaranya $f$ merupakan homeomorfisma lokal yang mempertahankan
orientasi, sedangkan pada dua lainnya ia membalik orientasi.

1. Hitung $\deg(f)$.
2. Jelaskan mengapa $f$ harus surjektif.
3. Dapatkah $f$ menjadi homeomorfisma global?
:::

::: {.hint #o012-fom-u005-hint-004 data-origin="edition-original"}
**Petunjuk.** Homeomorfisma lokal yang mempertahankan orientasi menyumbang
$+1$ dan yang membalik orientasi menyumbang $-1$. Gunakan sifat bahwa
pemetaan yang tidak surjektif berderajat nol.
:::

::: {.solution #o012-fom-u005-sol-004 data-origin="edition-original"}
**Solusi Pemeriksaan F5.4.** Rumus lokal-ke-global memberi

$$
\deg(f)=3(+1)+2(-1)=1.
$$

Karena derajatnya tidak nol, $f$ tidak mungkin gagal surjektif; jadi $f$
surjektif. Namun $f$ bukan homeomorfisma global: titik $y$ mempunyai lima
prabayangan berbeda, sedangkan homeomorfisma harus injektif dan karena itu
mempunyai tepat satu prabayangan bagi setiap titik.
:::

::: {.exercise #o012-fom-u005-mcheck-005 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F5.5 (semua pangkat bilangan bulat).** Untuk
$f_k(z)=z^k$ pada $S^1$:

1. hitung derajat lokal pada setiap prabayangan $1$ ketika $k>0$;
2. tangani $k=0$ tanpa menulis nilai di luar $S^1$;
3. gunakan $f_{-1}(z)=\overline z$ untuk menurunkan jawaban ketika $k<0$.
:::

::: {.hint #o012-fom-u005-hint-005 data-origin="edition-original"}
**Petunjuk.** Untuk $k>0$, gunakan koordinat sudut pada busur kecil di sekitar
setiap akar ke-$k$ dari $1$. Untuk $k<0$, faktorkan melalui pangkat positif
$-k$.
:::

::: {.solution #o012-fom-u005-sol-005 data-origin="edition-original"}
**Solusi Pemeriksaan F5.5.** Jika $k>0$, terdapat $k$ prabayangan $1$.
Dalam koordinat sudut lokal, $\theta\mapsto k\theta$ mempertahankan orientasi,
sehingga setiap derajat lokal bernilai $+1$ dan
$\deg(f_k)=k$. Untuk $k=0$, $f_0(z)=1$ adalah pemetaan konstan, maka
$\deg(f_0)=0$. Jika $k<0$, tulis

$$
f_k=f_{-1}\circ f_{-k}.
$$

Konjugasi kompleks $f_{-1}$ membalik orientasi dan berderajat $-1$, sedangkan
$-k>0$. Jadi

$$
\deg(f_k)=(-1)(-k)=k.
$$

Ketiga kasus memberi satu rumus $\deg(f_k)=k$ untuk semua
$k\in\mathbb Z$.
:::

::: {.exercise #o012-fom-u005-mcheck-006 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F5.6 (derajat dari pengangkatan sudut).** Identifikasi
$S^1$ dengan $\mathbb R/\mathbb Z$. Misalkan $f\colon S^1\to S^1$ mempunyai
pengangkatan kontinu $F\colon\mathbb R\to\mathbb R$ yang memenuhi

$$
F(t+1)=F(t)+d
$$

untuk suatu $d\in\mathbb Z$.

1. Jelaskan mengapa bilangan bulat $d$ adalah derajat $f$.
2. Terapkan pada pemetaan potongan demi potongan yang kenaikan pengangkatannya pada tiga
   interval berturut-turut adalah $1$, $2$, dan $-4$.
:::

::: {.hint #o012-fom-u005-hint-006 data-origin="edition-original"}
**Petunjuk.** Kelas fundamental $H_1(S^1)\cong\mathbb Z$ direpresentasikan
oleh satu putaran parameter $t\in[0,1]$. Lihat perpindahan total
$F(1)-F(0)$.
:::

::: {.solution #o012-fom-u005-sol-006 data-origin="edition-original"}
**Solusi Pemeriksaan F5.6.** Ketika parameter domain bergerak sekali dari
$0$ ke $1$, pengangkat citranya bergerak dari $F(0)$ ke

$$
F(1)=F(0)+d.
$$

Setelah diproyeksikan ke $\mathbb R/\mathbb Z$, perpindahan ini berarti citra
melilit lingkaran sasaran bersih sebanyak $d$ kali. Karena pembangkit
$H_1(S^1)$ dikirim ke $d$ kali pembangkit, $\deg(f)=d$.

Pada contoh tiga interval yang afin pada setiap sepertiga domain, perpindahan
total pengangkatan adalah jumlah kenaikan bertandanya,

$$
d=1+2-4=-1.
$$

Karena itu $\deg(f)=-1$. Untuk nilai sasaran yang bukan citra titik-titik
sambung domain, setiap potongan afin bersifat monoton ketat dan memberi
berturut-turut satu, dua, dan empat prabayangan dengan tanda $+,+,-$.
Perhitungan pengangkatan ini karena itu sama dengan jumlah kontribusi derajat
lokal $1+2-4$.
:::

::: {.boundary #o012-fom-u005-boundary-001}
**Batas sumber komponen.** Unit ini menerjemahkan
`algebraic_topology.tex` baris 2847–3122 secara kontigu, mencakup Bagian 1.11
tentang derajat pemetaan, teorema sfera berbulu, derajat lokal, rumus
lokal-ke-global, dan pemetaan pangkat pada lingkaran. Unit ini menutup
FOM-PR-12 dan menyediakan enam soal penguasaan dengan petunjuk serta solusi
lengkap. Kursor komponen berikutnya adalah baris 3123,
`\subsection{Cellular complexes}`, awal Bagian 1.12.
:::
