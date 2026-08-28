---
title: "Asesmen Kumulatif 2 — Homologi, Eksisi, dan Struktur Seluler"
lang: id-ID
course_id: D60
assessment_id: D60-CA02
edition_unit_id: O012-ORIG-CA02
course_route_unit_ids:
  - D60-R08
  - D60-R09
  - D60-R10
  - D60-R11
  - D60-R12
rights: "CC BY-SA 4.0"
origin: "Materi edisi asli; bukan bagian dari sumber Roberts atau Fomberg."
provenance: "OpenAI Codex gpt-5.6-sol, Ultra; disusun atas arahan pengguna; kredit dan hak komponen sumber tetap dipertahankan."
---

# Asesmen Kumulatif 2: homologi hingga struktur seluler {#o012-d60-ca02}

Asesmen ini menguji hubungan lintas-topik dari `D60-R08` sampai `D60-R12`:
homologi simpleksial dan singular, homotopi rantai, fungtorialitas, homologi
relatif, eksisi, Mayer–Vietoris, pemetaan pembandingan, kompleks CW,
homologi seluler, dan derajat. Setiap soal diikuti petunjuk dan solusi lengkap.
Untuk pemakaian sebagai ujian, kerjakan delapan soal terlebih dahulu tanpa
membuka kedua bagian tersebut.

Seluruh soal dan solusi pada berkas ini merupakan materi edisi asli
berlisensi CC BY-SA 4.0. Materi ini tidak berasal dari bank soal Fomberg yang
dikecualikan, tidak menyiratkan kepengarangan atau pengesahan dari penulis
sumber, dan tidak mengubah urutan maupun penomoran edisi Roberts dan Fomberg.

## Soal 1 — tabel muka berorientasi dan torsi {#o012-d60-ca02-s01}

::: {.exercise #o012-d60-ca02-ex-001 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R08"}
Suatu kompleks-$\Delta$ hingga $K$ mempunyai satu simpul $v$, dua sisi
berorientasi $a,b$, dan dua simpleks-$2$ berorientasi $\alpha,\beta$.
Semua ujung sisi dipetakan ke $v$. Tabel muka berorientasinya adalah

$$
\begin{array}{c|ccc}
&F_0&F_1&F_2\\ \hline
\alpha&a&-a&b\\
\beta&-b&b&a
\end{array}
$$

dengan $F_i$ menyatakan restriksi ke muka ke-$i$, dan tanda minus berarti
restriksi itu membalik orientasi sisi yang telah dipilih.

1. Turunkan $\partial_2\alpha$ dan $\partial_2\beta$ langsung dari tabel.
2. Periksa $\partial_1\partial_2=0$ pada kedua generator.
3. Hitung seluruh homologi integral $H_n^\Delta(K;\mathbb Z)$, termasuk
   bagian torsinya.
:::

::: {.hint #o012-d60-ca02-hint-001 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R08"}
**Petunjuk.** Gunakan $\partial_2=F_0-F_1+F_2$. Terhadap basis
$(\alpha,\beta)$ dan $(a,b)$, bentuk matriks batas berukuran $2\times2$.
Determinan dan FPB semua entrinya menentukan bentuk normal Smith.
:::

::: {.solution #o012-d60-ca02-sol-001 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R08"}
**Solusi.** Tanda berselang-seling pada batas simpleks memberi

$$
\begin{aligned}
\partial_2\alpha
&=F_0\alpha-F_1\alpha+F_2\alpha
=a-(-a)+b=2a+b,\\
\partial_2\beta
&=F_0\beta-F_1\beta+F_2\beta
=(-b)-b+a=a-2b.
\end{aligned}
$$

Karena kedua ujung setiap sisi adalah $v$,

$$
\partial_1a=v-v=0,
\qquad
\partial_1b=v-v=0.
$$

Maka $\partial_1\partial_2\alpha=\partial_1(2a+b)=0$ dan
$\partial_1\partial_2\beta=\partial_1(a-2b)=0$. Jadi identitas
$\partial^2=0$ benar pada semua generator.

Kompleks rantainya adalah

$$
0\longrightarrow\mathbb Z^2
\xrightarrow{A}\mathbb Z^2
\xrightarrow{0}\mathbb Z
\longrightarrow0,
\qquad
A=
\begin{pmatrix}
2&1\\
1&-2
\end{pmatrix}.
$$

Determinan $A$ adalah $-5$, sehingga $A$ injektif dan
$H_2(K)=0$. FPB semua entri $A$ adalah $1$; karena $A$ berperingkat penuh,
bentuk normal Smith-nya ialah $\operatorname{diag}(1,5)$. Dengan demikian

$$
H_1(K)=\operatorname{coker}A\cong\mathbb Z/5\mathbb Z.
$$

Pada derajat nol, $\partial_1=0$ dan hanya ada satu simpul, jadi
$H_0(K)\cong\mathbb Z$. Tidak ada rantai pada derajat di atas dua. Ringkasnya,

$$
H_n^\Delta(K;\mathbb Z)\cong
\begin{cases}
\mathbb Z,&n=0,\\
\mathbb Z/5\mathbb Z,&n=1,\\
0,&n\geq2.
\end{cases}
$$
:::

## Soal 2 — deformasi dan homotopi rantai {#o012-d60-ca02-s02}

::: {.exercise #o012-d60-ca02-ex-002 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R09"}
Ambil silinder $C=S^1\times[0,1]$ dan lingkaran bawah
$A=S^1\times\{0\}$. Definisikan inklusi $i\colon A\hookrightarrow C$,
retraksi $r(z,s)=(z,0)$, dan

$$
H((z,s),t)=(z,(1-t)s).
$$

1. Buktikan bahwa $H$ adalah retraksi deformasi kuat $C$ ke $A$.
2. Misalkan $P$ adalah operator prisma pada rantai singular yang dibangun
   dari $H$. Tulis identitas homotopi rantainya dan buktikan langsung pada
   sebuah siklus bahwa $(i\circ r)_*=\operatorname{id}$ pada homologi.
3. Gunakan fungtorialitas bersama $r\circ i=\operatorname{id}_A$ untuk
   membuktikan bahwa $i_*$ dan $r_*$ saling invers, lalu hitung semua
   $H_n(C;\mathbb Z)$.
:::

::: {.hint #o012-d60-ca02-hint-002 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R09"}
**Petunjuk.** Periksa nilai $H$ pada $t=0$, $t=1$, dan pada titik-titik $A$.
Untuk homotopi dari identitas ke $i\circ r$, operator prisma memenuhi
$(i\circ r)_\#-\operatorname{id}_\#=\partial P+P\partial$.
:::

::: {.solution #o012-d60-ca02-sol-002 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R09"}
**Solusi.** Rumus $H$ kontinu dan bernilai di $C$. Pada kedua ujung parameter,

$$
H((z,s),0)=(z,s),
\qquad
H((z,s),1)=(z,0)=i(r(z,s)).
$$

Jika $(z,s)\in A$, maka $s=0$ dan $H((z,0),t)=(z,0)$ untuk setiap $t$.
Jadi $H$ adalah homotopi dari $\operatorname{id}_C$ ke $i\circ r$ yang
menetapkan $A$ titik demi titik: tepat suatu retraksi deformasi kuat.

Operator prisma memberi homotopi rantai

$$
(i\circ r)_\#-\operatorname{id}_\#=\partial P+P\partial.
$$

Jika $z$ sebuah siklus singular, maka $\partial z=0$ dan

$$
(i\circ r)_\#z-z
=\partial Pz+P(\partial z)
=\partial Pz.
$$

Selisih kedua rantai itu merupakan batas, sehingga
$(i\circ r)_*[z]=[z]$. Jadi $(i\circ r)_*=\operatorname{id}_{H_n(C)}$.
Di sisi lain, $r\circ i=\operatorname{id}_A$ secara literal. Fungtorialitas
memberi

$$
r_*i_*=(r\circ i)_*=\operatorname{id}_{H_n(A)},
\qquad
i_*r_*=(i\circ r)_*=\operatorname{id}_{H_n(C)}.
$$

Dengan demikian $i_*$ dan $r_*$ saling invers. Karena $A\cong S^1$,

$$
H_n(C;\mathbb Z)\cong H_n(S^1;\mathbb Z)
\cong
\begin{cases}
\mathbb Z,&n=0,1,\\
0,&n\geq2.
\end{cases}
$$
:::

## Soal 3 — ekuator dan barisan eksak pasangan {#o012-d60-ca02-s03}

::: {.exercise #o012-d60-ca02-ex-003 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R10"}
Misalkan $E\cong S^1$ adalah ekuator dalam $S^2$, dan tulis $D_+$ serta
$D_-$ untuk kedua hemisfer tertutup. Pilih orientasi sehingga kelas relatif
$u=[D_+]$ dan $v=[D_-]$ memenuhi

$$
\partial u=[E],\qquad \partial v=-[E].
$$

1. Gunakan ruang hasil bagi $S^2/E$ untuk menghitung
   $H_n(S^2,E;\mathbb Z)$ pada setiap $n$.
2. Tentukan pemetaan penghubung
   $\partial\colon H_2(S^2,E)\to H_1(E)$ pada koordinat $(u,v)$.
3. Tentukan citra kelas fundamental $[S^2]$ di $H_2(S^2,E)$ dan periksa
   eksakitas pada ketiga suku
   $H_2(S^2)\to H_2(S^2,E)\to H_1(E)$.
:::

::: {.hint #o012-d60-ca02-hint-003 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R10"}
**Petunjuk.** Setelah seluruh ekuator diruntuhkan, setiap hemisfer menjadi
satu sfera dan keduanya bertemu di titik hasil runtuhan. Pemetaan penghubung
mengambil batas wakil relatif; perhatikan tanda orientasi kedua hemisfer.
:::

::: {.solution #o012-d60-ca02-sol-003 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R10"}
**Solusi.** Pasangan $(S^2,E)$ adalah pasangan baik. Meruntuhkan $E$ membuat
masing-masing $D_+/E$ dan $D_-/E$ menjadi $S^2$, dengan kedua titik runtuhan
diidentifikasi. Jadi

$$
S^2/E\cong S^2\vee S^2.
$$

Teorema hasil bagi relatif memberi

$$
H_n(S^2,E;\mathbb Z)
\cong\widetilde H_n(S^2\vee S^2;\mathbb Z)
\cong
\begin{cases}
\mathbb Z^2,&n=2,\\
0,&n\ne2.
\end{cases}
$$

Basis pada derajat dua dapat dipilih sebagai $(u,v)$. Berdasarkan definisi
pemetaan penghubung dan orientasi yang ditetapkan,

$$
\partial(au+bv)=a[E]-b[E]=(a-b)[E].
$$

Jadi $\partial$ adalah matriks baris $(1,-1)$. Rantai fundamental
berorientasi pada $S^2$ adalah jumlah kedua hemisfer: batas ekuatornya saling
menghapus. Karena itu pemetaan
$j_*\colon H_2(S^2)\to H_2(S^2,E)$ memenuhi

$$
j_*[S^2]=u+v=(1,1).
$$

Pemetaan $j_*$ injektif, dan

$$
\operatorname{im}j_*=\mathbb Z(1,1)
=\ker(1,-1)=\ker\partial.
$$

Pemetaan $\partial$ surjektif karena $\partial u=[E]$. Jadi potongan

$$
0\longrightarrow\mathbb Z
\xrightarrow{\,1\mapsto(1,1)\,}
\mathbb Z^2
\xrightarrow{\,(a,b)\mapsto a-b\,}
\mathbb Z
\longrightarrow0
$$

eksak, sebagaimana diwajibkan barisan eksak panjang pasangan.
:::

## Soal 4 — penutup tiga-komponen graf theta {#o012-d60-ca02-s04}

::: {.exercise #o012-d60-ca02-ex-004 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R11"}
Misalkan $\Theta$ adalah graf theta: dua simpul $p,q$ dihubungkan oleh tiga
sisi $e_1,e_2,e_3$, semuanya diorientasikan dari $p$ ke $q$. Pilih penutup
terbuka $\Theta=U\cup V$ sehingga $U$ adalah lingkungan bintang $p$, $V$
adalah lingkungan bintang $q$, dan $U\cap V$ terdiri atas tepat tiga interval
terbuka $J_1,J_2,J_3$, satu di tengah setiap sisi.

1. Hitung homologi tereduksi $U$, $V$, dan $U\cap V$; berikan basis eksplisit
   bagi $\widetilde H_0(U\cap V)$.
2. Gunakan barisan Mayer–Vietoris tereduksi untuk menghitung semua
   $H_n(\Theta;\mathbb Z)$.
3. Hubungkan basis $\widetilde H_0(U\cap V)$ dengan dua siklus graf
   $e_1-e_3$ dan $e_2-e_3$ melalui pemetaan penghubung.
:::

::: {.hint #o012-d60-ca02-hint-004 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R11"}
**Petunjuk.** Kedua lingkungan bintang kontraktibel. Pilih titik
$x_i\in J_i$; dua selisih $[x_1]-[x_3]$ dan $[x_2]-[x_3]$ membentuk basis
homologi tereduksi derajat nol perpotongan. Pada barisan tereduksi, semua
suku yang mengapit $\widetilde H_1(\Theta)$ selain suku perpotongan bernilai
nol.
:::

::: {.solution #o012-d60-ca02-sol-004 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R11"}
**Solusi.** Ruang $U$ dan $V$ masing-masing berbentuk pohon bercabang tiga,
sehingga keduanya kontraktibel. Maka

$$
\widetilde H_n(U)=\widetilde H_n(V)=0
\qquad\text{untuk semua }n.
$$

Perpotongan merupakan gabungan saling lepas tiga interval kontraktibel.
Jadi $H_0(U\cap V)\cong\mathbb Z^3$, sedangkan

$$
\widetilde H_0(U\cap V)
\cong\{(c_1,c_2,c_3)\in\mathbb Z^3:c_1+c_2+c_3=0\}
\cong\mathbb Z^2.
$$

Jika $x_i\in J_i$, satu basisnya adalah

$$
[x_1]-[x_3],\qquad [x_2]-[x_3].
$$

Barisan Mayer–Vietoris tereduksi menyederhana menjadi

$$
0\longrightarrow\widetilde H_1(\Theta)
\xrightarrow{\partial}\widetilde H_0(U\cap V)
\longrightarrow0,
$$

sehingga $\partial$ isomorfisma dan
$H_1(\Theta)\cong\mathbb Z^2$. Graf $\Theta$ terhubung lintasan, maka
$H_0(\Theta)\cong\mathbb Z$; graf tidak mempunyai homologi di atas derajat
satu. Dengan demikian

$$
H_n(\Theta;\mathbb Z)\cong
\begin{cases}
\mathbb Z,&n=0,\\
\mathbb Z^2,&n=1,\\
0,&n\geq2.
\end{cases}
$$

Pecah rantai siklus $e_i-e_3$ menjadi bagian yang berada di $U$ dan bagian
yang berada di $V$. Batas bagian $U$ terletak di $J_i\cup J_3$ dan, setelah
orientasi pemisahan dipilih secara serasi, mewakili
$[x_i]-[x_3]$. Karena itu

$$
\partial[e_1-e_3]=[x_1]-[x_3],
\qquad
\partial[e_2-e_3]=[x_2]-[x_3].
$$

Kedua siklus graf tersebut karenanya membentuk basis $H_1(\Theta)$ yang
bersesuaian dengan basis homologi tereduksi perpotongan.
:::

## Soal 5 — hasil bagi pasangan kerangka torus {#o012-d60-ca02-s05}

::: {.exercise #o012-d60-ca02-ex-005 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R10" data-secondary-route-unit-ids="D60-R11"}
Berikan torus $T^2$ struktur CW dengan satu sel-$0$, dua sel-$1$ $a,b$, dan
satu sel-$2$ yang dilekatkan sepanjang $aba^{-1}b^{-1}$. Tulis
$T^1=S^1_a\vee S^1_b$ untuk kerangka-$1$.

1. Jelaskan mengapa $(T^2,T^1)$ pasangan baik dan identifikasi
   $T^2/T^1$.
2. Terapkan teorema hasil bagi relatif untuk menghitung
   $H_n(T^2,T^1;\mathbb Z)$ pada setiap $n$.
3. Hitung pemetaan penghubung
   $H_2(T^2,T^1)\to H_1(T^1)$ dari kata pelekatan, lalu gunakan barisan
   eksak panjang untuk menghitung $H_*(T^2;\mathbb Z)$.
:::

::: {.hint #o012-d60-ca02-hint-005 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R10" data-secondary-route-unit-ids="D60-R11"}
**Petunjuk.** Subkompleks CW memberi pasangan baik. Setelah seluruh
kerangka-$1$ diruntuhkan, cakram karakteristik sel-$2$ mempunyai seluruh
batas pada satu titik. Pemetaan penghubung membaca abelianisasi kata
pelekatan.
:::

::: {.solution #o012-d60-ca02-sol-005 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R10" data-secondary-route-unit-ids="D60-R11"}
**Solusi.** Setiap subkompleks dari kompleks CW membentuk pasangan baik
dengan ruang totalnya, sehingga teorema hasil bagi relatif berlaku. Ketika
$T^1$ diruntuhkan, sel-$2$ menjadi cakram yang seluruh batasnya diidentifikasi
ke satu titik. Maka

$$
T^2/T^1\cong D^2/\partial D^2\cong S^2.
$$

Teorema hasil bagi relatif memberi

$$
H_n(T^2,T^1;\mathbb Z)
\cong\widetilde H_n(S^2;\mathbb Z)
\cong
\begin{cases}
\mathbb Z,&n=2,\\
0,&n\ne2.
\end{cases}
$$

Pemetaan penghubung mengirim generator relatif sel-$2$ ke kelas homologi
kata pelekatannya. Dalam $H_1(T^1)\cong\mathbb Z[a]\oplus\mathbb Z[b]$,

$$
[aba^{-1}b^{-1}]=[a]+[b]-[a]-[b]=0.
$$

Jadi pemetaan penghubung bernilai nol. Potongan barisan eksak panjang ialah

$$
0\longrightarrow H_2(T^2)
\longrightarrow\mathbb Z
\xrightarrow{0}\mathbb Z^2
\longrightarrow H_1(T^2)
\longrightarrow0.
$$

Eksakitas memberi $H_2(T^2)\cong\mathbb Z$ dan
$H_1(T^2)\cong\mathbb Z^2$. Karena $T^1$ dan $T^2$ terhubung, bagian derajat
nol memberi $H_0(T^2)\cong\mathbb Z$; tidak ada homologi di atas derajat dua.
Dengan demikian

$$
H_n(T^2;\mathbb Z)\cong
\begin{cases}
\mathbb Z,&n=0,2,\\
\mathbb Z^2,&n=1,\\
0,&n>2.
\end{cases}
$$

Ini merupakan penerapan langsung teorema hasil bagi pasangan baik dan
barisan eksak, bukan penggantian bagi salah satu perbaikan bukti sumber.
:::

## Soal 6 — peta pelekatan dan topologi ruang Moore {#o012-d60-ca02-s06}

::: {.exercise #o012-d60-ca02-ex-006 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R12"}
Untuk $m\geq2$, bentuk ruang Moore

$$
M_m=S^1\cup_{\varphi_m}D^2,
\qquad
\varphi_m(z)=z^m.
$$

Gunakan struktur CW pada $S^1$ dengan satu sel-$0$ $v$ dan satu sel-$1$ $a$.

1. Daftarkan sel dan semua kerangka $M_m^{(k)}$. Bedakan secara bertipe peta
   pelekatan $\varphi_m$ dari pemetaan karakteristik
   $\Phi_m\colon D^2\to M_m$.
2. Buktikan bahwa $\Phi_m$ membatasi menjadi homeomorfisma dari
   $\operatorname{Int}D^2$ ke sel-$2$ terbuka, tetapi tidak injektif pada
   batas.
3. Periksa syarat hingga pada penutupan (*closure-finite*) dan nyatakan secara
   eksplisit uji topologi lemah melalui prabayangan semua pemetaan
   karakteristik.
4. Sebagai pemeriksaan, tulis kompleks rantai seluler dan hitung
   $H_*(M_m;\mathbb Z)$.
:::

::: {.hint #o012-d60-ca02-hint-006 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R12"}
**Petunjuk.** Peta pelekatan berdomain $\partial D^2$ dan berkodomain
kerangka-$1$; pemetaan karakteristik berdomain seluruh $D^2$ dan berkodomain
ruang hasil. Relasi hasil bagi hanya mengidentifikasi titik-titik batas.
Untuk topologi lemah, gunakan prabayangan pada cakram karakteristik setiap
sel tertutup.
:::

::: {.solution #o012-d60-ca02-sol-006 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R12"}
**Solusi.** Ruang $M_m$ mempunyai satu sel terbuka $e^k$ dalam setiap
dimensi $k=0,1,2$ dan tidak mempunyai sel lain. Kerangkanya ialah

$$
M_m^{(0)}=\{v\},
\qquad
M_m^{(1)}=S^1,
\qquad
M_m^{(2)}=M_m.
$$

Peta pelekatan dan pemetaan karakteristik berturut-turut bertipe

$$
\varphi_m\colon\partial D^2=S^1\longrightarrow M_m^{(1)}=S^1,
\qquad
\Phi_m\colon D^2\longrightarrow M_m.
$$

Jika $j\colon M_m^{(1)}\hookrightarrow M_m$ adalah inklusi, relasi hasil
bagi memberi

$$
\Phi_m|_{\partial D^2}=j\circ\varphi_m.
$$

Tidak ada titik bagian dalam cakram yang diidentifikasi dengan titik lain.
Karena itu

$$
\Phi_m|_{\operatorname{Int}D^2}\colon
\operatorname{Int}D^2\xrightarrow{\cong}e^2
$$

merupakan homeomorfisma. Pada batas, $\varphi_m(z)=z^m$ mempunyai $m$
prabayangan untuk setiap titik; karena $m\geq2$, $\Phi_m$ tidak injektif di
sana. Inilah perbedaan penting antara bagian dalam sel dan penutupannya.

Penutupan $e^0$ bertemu hanya $e^0$; penutupan $e^1=S^1$ bertemu
$e^0,e^1$; dan penutupan $e^2$ adalah seluruh $M_m$, yang bertemu tepat
$e^0,e^1,e^2$. Jadi setiap penutupan sel bertemu berhingga banyak sel:
syarat hingga pada penutupan (*closure-finite*) terpenuhi.

Ambil pemetaan karakteristik $\Phi_0\colon D^0\to M_m$,
$\Phi_1\colon D^1\to M_m^{(1)}$ yang mengidentifikasi kedua ujung interval
ke $v$, dan $\Phi_m\colon D^2\to M_m$. Topologi lemah menyatakan bahwa
$F\subseteq M_m$ tertutup tepat ketika

$$
\Phi_0^{-1}(F),\quad \Phi_1^{-1}(F),\quad \Phi_m^{-1}(F)
$$

tertutup pada cakram domain masing-masing. Secara ekuivalen, $U\subseteq M_m$
terbuka tepat ketika ketiga prabayangan tersebut terbuka. Pada kompleks
hingga ini, uji itu sama dengan topologi hasil bagi konstruksi pelekatan.

Koefisien batas sel-$2$ terhadap sel-$1$ adalah derajat $\varphi_m$, yaitu
$m$, sedangkan $d_1=0$. Jadi

$$
0\longrightarrow\mathbb Z
\xrightarrow{\times m}\mathbb Z
\xrightarrow{0}\mathbb Z
\longrightarrow0,
$$

dan

$$
H_n(M_m;\mathbb Z)\cong
\begin{cases}
\mathbb Z,&n=0,\\
\mathbb Z/m\mathbb Z,&n=1,\\
0,&n\geq2.
\end{cases}
$$
:::

## Soal 7 — dua relator dan bentuk normal Smith {#o012-d60-ca02-s07}

::: {.exercise #o012-d60-ca02-ex-007 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R12"}
Suatu kompleks CW $X$ mempunyai satu sel-$0$ $v$, dua sel-$1$ berorientasi
$a,b$, dan dua sel-$2$ $p,q$. Peta pelekatan sel-$2$ menelusuri kata

$$
w_p=a^2,
\qquad
w_q=ab^3.
$$

Tidak ada sel berdimensi lebih tinggi.

1. Turunkan matriks batas seluler $d_2$ terhadap basis $(p,q)$ pada domain
   dan $(a,b)$ pada kodomain, lalu hitung $d_1$.
2. Reduksi $d_2$ ke bentuk normal Smith dan hitung semua
   $H_n(X;\mathbb Z)$.
3. Periksa hasil $H_1$ dengan mengabelianisasi presentasi grup fundamental.
:::

::: {.hint #o012-d60-ca02-hint-007 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R12"}
**Petunjuk.** Koefisien insidensi adalah jumlah eksponen huruf yang
bersangkutan. Sesudah menukar kedua kolom, hilangkan entri $3$ di kiri bawah,
lalu hilangkan entri $2$ di kanan atas dengan operasi unimodular.
:::

::: {.solution #o012-d60-ca02-sol-007 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R12"}
**Solusi.** Jumlah eksponen pada $a^2$ adalah $(2,0)$ dan pada $ab^3$ adalah
$(1,3)$. Maka

$$
d_2(p)=2a,
\qquad
d_2(q)=a+3b,
\qquad
[d_2]_{(a,b)\leftarrow(p,q)}
=
\begin{pmatrix}
2&1\\
0&3
\end{pmatrix}.
$$

Kedua ujung setiap sel-$1$ melekat pada $v$, sehingga $d_1=0$. Operasi baris
dan kolom unimodular memberi

$$
\begin{pmatrix}2&1\\0&3\end{pmatrix}
\sim
\begin{pmatrix}1&2\\3&0\end{pmatrix}
\sim
\begin{pmatrix}1&2\\0&-6\end{pmatrix}
\sim
\begin{pmatrix}1&0\\0&6\end{pmatrix}.
$$

Determinan matriks semula adalah $6$, sehingga $d_2$ injektif dan
$H_2(X)=0$. Bentuk normal Smith memberi

$$
H_1(X)=\operatorname{coker}d_2\cong\mathbb Z/6\mathbb Z.
$$

Karena hanya ada satu simpul, $H_0(X)\cong\mathbb Z$, dan grup di atas
derajat dua nol. Jadi

$$
H_n(X;\mathbb Z)\cong
\begin{cases}
\mathbb Z,&n=0,\\
\mathbb Z/6\mathbb Z,&n=1,\\
0,&n\geq2.
\end{cases}
$$

Teorema Seifert–van Kampen memberi

$$
\pi_1(X,v)\cong\langle a,b\mid a^2=1,\ ab^3=1\rangle.
$$

Dalam abelianisasi, relasinya menjadi $2a=0$ dan $a+3b=0$. Mengganti
$a=-3b$ pada relasi pertama memberi $6b=0$. Transformasi Smith di atas
menunjukkan tidak ada relasi tambahan pada kelas $b$, sehingga
$\pi_1(X)_{\mathrm{ab}}\cong\mathbb Z/6\mathbb Z$, sesuai dengan
$H_1(X)$.
:::

## Soal 8 — pemetaan torus bermatriks determinan tiga {#o012-d60-ca02-s08}

::: {.exercise #o012-d60-ca02-ex-008 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R12" data-secondary-route-unit-ids="D60-R08,D60-R09,D60-R11"}
Tuliskan $T^2=\mathbb R^2/\mathbb Z^2$ dan definisikan

$$
F_A([x,y])=[2x+y,x+2y],
\qquad
A=
\begin{pmatrix}
2&1\\
1&2
\end{pmatrix}.
$$

1. Buktikan bahwa $F_A$ terdefinisi dengan baik dan merupakan penutup
   berlembar tiga. Tentukan serat di atas $[0,0]$.
2. Hitung $(F_A)_*$ pada $H_0(T^2)$, $H_1(T^2)$, dan $H_2(T^2)$, serta
   tentukan $\deg(F_A)$.
3. Jelaskan mengapa hitungan melalui model CW, suatu subdivisi
   kompleks-$\Delta$, dan rantai singular menghasilkan homomorfisma yang
   sama—bukan tiga pilihan yang tak berkaitan.
4. Tentukan kernel dan kokernel aksi pada $H_1$, lalu simpulkan apakah
   $F_A$ ekuivalensi homotopi.
:::

::: {.hint #o012-d60-ca02-hint-008 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R12" data-secondary-route-unit-ids="D60-R08,D60-R09,D60-R11"}
**Petunjuk.** Matriks integral melestarikan kisi $\mathbb Z^2$. Indeks
$A\mathbb Z^2$ adalah $|\det A|$; tiga unsur kernel dapat dipilih pada
diagonal torus. Untuk pembandingan model, gunakan aproksimasi seluler,
subdivisi yang kompatibel, kealamian, dan teorema pembandingan
simpleksial–singular.
:::

::: {.solution #o012-d60-ca02-sol-008 data-origin="edition-original" data-assessment-id="D60-CA02" data-course-route-unit-id="D60-R12" data-secondary-route-unit-ids="D60-R08,D60-R09,D60-R11"}
**Solusi.** Jika $(x,y)$ diganti dengan $(x,y)+(m,n)$ untuk
$(m,n)\in\mathbb Z^2$, citranya berubah sebesar

$$
A(m,n)=(2m+n,m+2n)\in\mathbb Z^2.
$$

Jadi $F_A$ terdefinisi dengan baik pada hasil bagi. Matriks $A$ invertibel
di atas $\mathbb R$ dan turun menjadi homeomorfisma lokal torus. Banyaknya
lembar adalah indeks $A\mathbb Z^2$ dalam $\mathbb Z^2$, yaitu

$$
|\det A|=|4-1|=3.
$$

Serat di atas titik nol adalah kernel homomorfisma torus, dengan wakil

$$
[0,0],
\qquad
[1/3,1/3],
\qquad
[2/3,2/3].
$$

Ketiganya memang dipetakan ke pasangan bilangan bulat, dan cacah lembar
menunjukkan bahwa tidak ada unsur kernel lain.

Pada $H_0(T^2)\cong\mathbb Z$, ruang dan sasaran terhubung sehingga
$(F_A)_*$ adalah identitas. Jika $a,b$ adalah kelas kedua lingkaran
koordinat, maka

$$
(F_A)_*[a]=2[a]+[b],
\qquad
(F_A)_*[b]=[a]+2[b].
$$

Jadi aksi pada $H_1(T^2)\cong\mathbb Z^2$ tepat matriks $A$. Karena
$\det A=3>0$, ketiga lembar lokal mempertahankan orientasi. Rumus
lokal-ke-global memberi

$$
\deg(F_A)=3,
$$

dan karena $H_2(T^2)\cong\mathbb Z$ dibangkitkan kelas fundamental,
$(F_A)_*$ pada $H_2$ adalah perkalian tiga.

Untuk model CW standar torus, aproksimasi seluler terhadap $F_A$ menghasilkan
pemetaan homotopik yang menelusuri kata dengan jumlah eksponen berupa kolom
$A$ pada kerangka-$1$ dan bertindak dengan koefisien $3$ pada sel-$2$.
Pada model kompleks-$\Delta$, pilih subdivisi domain dan sasaran yang membuat
pemetaan linear torus itu simpleksial. Pemetaan pembandingan mengirim setiap
simpleks berorientasi ke simpleks singular yang sama. Kealamiannya memberi
persegi komutatif

$$
\begin{array}{ccc}
H_n^\Delta(T^2)&\xrightarrow{(F_A)_*}&H_n^\Delta(T^2)\\
\downarrow\cong&&\downarrow\cong\\
H_n(T^2)&\xrightarrow{(F_A)_*}&H_n(T^2).
\end{array}
$$

Invariansi homotopi mengidentifikasi hasil aproksimasi seluler dengan
pemetaan semula. Jadi ketiga model memberi aksi intrinsik yang sama pada
homologi.

Matriks $A$ mempunyai determinan taknol, maka kernelnya pada $\mathbb Z^2$
adalah nol. FPB semua entrinya $1$ dan $|\det A|=3$, sehingga bentuk normal
Smith-nya $\operatorname{diag}(1,3)$ dan

$$
\ker\!\left((F_A)_*|_{H_1}\right)=0,
\qquad
\operatorname{coker}\!\left((F_A)_*|_{H_1}\right)
\cong\mathbb Z/3\mathbb Z.
$$

Karena aksi pada $H_1$ bukan isomorfisma, $F_A$ bukan ekuivalensi homotopi.
:::

## Peta cakupan asesmen {#o012-d60-ca02-coverage}

| Soal | Route utama | Route sekunder | Kompetensi yang diperiksa |
|---:|:---:|:---:|---|
| 1 | D60-R08 | — | tabel muka berorientasi, batas, $\partial^2=0$, bentuk normal Smith, dan torsi |
| 2 | D60-R09 | — | retraksi deformasi kuat, operator prisma, homotopi rantai, dan fungtorialitas |
| 3 | D60-R10 | — | homologi relatif, ruang hasil bagi, pemetaan penghubung, dan eksakitas |
| 4 | D60-R11 | — | penutup graf theta, tiga komponen perpotongan, $\widetilde H_0$, dan Mayer–Vietoris |
| 5 | D60-R10 | D60-R11 | pasangan baik $(T^2,T^1)$, teorema hasil bagi, dan barisan eksak panjang |
| 6 | D60-R12 | — | peta pelekatan, pemetaan karakteristik, closure-finite, topologi lemah, dan ruang Moore |
| 7 | D60-R12 | — | bilangan insidensi, matriks batas seluler, dan bentuk normal Smith $\operatorname{diag}(1,6)$ |
| 8 | D60-R12 | D60-R08, D60-R09, D60-R11 | pemetaan torus, derajat tiga, dan kealamian pembandingan model |

Asesmen selesai pada tepat delapan soal, delapan petunjuk, dan delapan solusi
penuh. Tidak ada ungkapan soal dari bank masalah Fomberg yang disalin atau
diadaptasi di sini.
