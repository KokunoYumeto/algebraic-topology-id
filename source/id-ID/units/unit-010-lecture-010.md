---
title: "Topologi Aljabar"
subtitle: "Unit 10: Penutup Terhubung Sederhana, Lingkaran, dan Baji"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l10-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts (2019), tepatnya [Notes.tex baris
2094--2272 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L2094-L2272).
Rentang itu dimulai dengan penanda Kuliah 10 dan lanjutan bukti teorema ruang
koset dari Unit 9, lalu berakhir tepat setelah pratinjau bahwa grup fundamental
baji dua lingkaran adalah grup bebas pada dua pembangkit. Baris 2273 memulai
Kuliah 11 dan tidak termasuk dalam unit ini. Karya sumber tersedia di bawah
[Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah
dibaca, pemberian pengenal stabil, serta pemindahan keenam unsur pinggir ke
urutan bacaan utama: definisi himpunan-$G$, arti ekuivarian, konvensi
keterhubungan lintasan semilokal, sifat universal baji, diagram penutup tiga
lembaran, dan bentuk kata dalam grup bebas. Diagram penutup diganti dengan
daftar simpul dan sisi berarah yang mempertahankan semua data pelabelan,
proyeksi, dan pengangkatan lintasan.

Sejumlah cacat sumber diperbaiki secara independen. Huruf titik yang berubah
dari $p$ menjadi $s$ dalam pemetaan orbit--stabilisator diseragamkan; subgrup
stabilisator ditulis sebagai citra
$\pi_*\bigl(\pi_1(Z,z)\bigr)$, bukan disamakan secara harfiah dengan grup
asalnya; variabel $x,y$ pada himpunan morfisma grupoid terbatas disyaratkan
berada di $A$; dan dekomposisi grupoid dinyatakan hanya ketika
$X=X_1\sqcup X_2$ merupakan dekomposisi ke dalam komponen lintasan. Istilah
*join* yang salah diganti dengan *wedge* atau *baji*, urutan komposisi dalam
sifat universal baji diperbaiki agar bertipe benar, dan salah tulis
$S^\vee S^1$ dipulihkan menjadi $S^1\vee S^1$. Salah eja “goups”, simbol
`rho` yang kehilangan garis miring, serta bentuk jamak “homomorphism” juga
diperbaiki. Catatan bentuk normal produk bebas dilengkapi dengan syarat
eksponen tak nol, pergantian faktor, dan kata kosong agar tidak menyatakan
representasi tak tereduksi sebagai bentuk normal.

Konvensi aksi memerlukan perhatian khusus. Pengangkatan lintasan pada Unit
7--9 memberi aksi kanan langsung
$u\mathbin{\cdot}(gh)=(u\mathbin{\cdot}g)\mathbin{\cdot}h$, sehingga ruang
orbit--stabilisator alaminya adalah $H\backslash G$. Sumber memakai aksi kiri
dan $G/H$. Unit ini mempertahankan kedua bentuk dengan menyatakan operasi
inversi yang menghubungkannya. Demikian pula, operator titik akhir
$R_g(u)=u\mathbin{\cdot}g$ memenuhi
$R_{gh}=R_h\circ R_g$; representasi permutasi sebagai homomorfisma biasa
diperoleh dari $\lambda(g)=R_{g^{-1}}$. Pembedaan ini mencegah urutan
perkalian terbalik secara diam-diam pada contoh baji dua lingkaran.

Rentang sumber tidak memuat latihan. Bagian pendamping penguasaan menambahkan
lima pemeriksaan dengan solusi lengkap: aksi reguler dan kesetiaan; langkah
yang menuntaskan perhitungan $\pi_1(S^1)$; sifat universal baji; pemeriksaan
lokal dan monodromi penutup tiga lembaran; serta batas logis antara
nonkomutativitas yang sudah dibuktikan dan struktur grup bebas yang baru akan
dibuktikan. Seluruh materi pendamping yang ditambahkan tersedia di bawah CC
BY 4.0. Edisi ini bersifat independen dan tidak menyiratkan dukungan atau
pengesahan dari penulis sumber.

# Kuliah 10 {#o012-rbt-l10}

## Menuntaskan deskripsi serat sebagai ruang koset {#o012-rbt-l10-s01}

::: {.proof #o012-rbt-l10-proof-001}
**Bukti Teorema 9.2 (lanjutan).** Sebuah himpunan yang dilengkapi aksi grup
$G$ disebut *himpunan-$G$*. Mula-mula ambil sembarang himpunan-$G$ kanan
transitif $S$ dan suatu titik $p\in S$. Pemetaan

$$
G\longrightarrow S,
\qquad
g\longmapsto p\mathbin{\cdot}g
$$

turun menjadi bijeksi yang terdefinisi baik

$$
\operatorname{Stab}(p)\backslash G
\xrightarrow{\;\cong\;}
S,
\qquad
\operatorname{Stab}(p)g\longmapsto p\mathbin{\cdot}g,
$$

dengan

$$
\operatorname{Stab}(p)
:=
\{g\in G\mid p\mathbin{\cdot}g=p\}.
$$

Bijeksi ini *ekuivarian*: ia mempertahankan aksi kanan $G$. Jika aksi kiri
yang bersesuaian didefinisikan oleh

$$
g\star u:=u\mathbin{\cdot}g^{-1},
$$

bijeksi yang sama dapat ditulis

$$
G/\operatorname{Stab}(p)
\xrightarrow{\;\cong\;}
S,
\qquad
g\operatorname{Stab}(p)
\longmapsto
p\mathbin{\cdot}g^{-1}.
$$

Inilah bentuk aksi kiri yang digunakan dalam sumber.

Terapkan fakta tersebut pada aksi kanan transitif
$G=\pi_1(X,x)$ di serat $Z_x$. Aksi itu transitif karena $Z$ terhubung
lintasan. Kita memperoleh isomorfisma himpunan-$G$ kanan

$$
\operatorname{Stab}(z)\backslash\pi_1(X,x)
\xrightarrow{\;\cong\;}
Z_x.
$$

Tinggal mengidentifikasi stabilisatornya. Jika
$[\gamma]\in\pi_1(X,x)$ memenuhi

$$
z\mathbin{\cdot}[\gamma]
=
\gamma_*(z)
=z,
$$

maka pengangkatan $\widetilde\gamma_z$ yang berawal di $z$ juga berakhir di
$z$, sehingga merupakan loop di $Z$. Sebaliknya, proyeksi setiap loop pada
$z$ mempunyai pengangkatan berawal di $z$ yang berakhir di $z$. Karena
Teorema 9.1 menyatakan bahwa $\pi_*$ injektif, kita boleh mengidentifikasi
$\pi_1(Z,z)$ dengan citranya, tetapi sebagai subgrup dari
$\pi_1(X,x)$ pernyataan yang tepat adalah

$$
\operatorname{Stab}(z)
=
\pi_*\bigl(\pi_1(Z,z)\bigr).
$$

Jadi

$$
Z_x
\cong
\pi_*\bigl(\pi_1(Z,z)\bigr)\backslash\pi_1(X,x)
$$

sebagai himpunan-$\pi_1(X,x)$ kanan. Setelah aksi diubah melalui inversi,
hasil ini menjadi bentuk kiri

$$
Z_x
\cong
\pi_1(X,x)\big/\pi_*\bigl(\pi_1(Z,z)\bigr)
$$

yang ditampilkan dalam sumber. $\square$
:::

::: {.corollary #o012-rbt-l10-cor-001 data-source-label="cor:fibre_of_univ_cov_space"}
**Akibat 10.1 (serat penutup terhubung sederhana).** Jika

$$
\pi\colon(Z,z)\longrightarrow(X,x)
$$

suatu ruang penutup dengan $Z$ terhubung sederhana, maka pemetaan

$$
\begin{aligned}
\pi_1(X,x)&\longrightarrow Z_x,\\
g&\longmapsto z\mathbin{\cdot}g
\end{aligned}
$$

merupakan isomorfisma himpunan-$\pi_1(X,x)$ kanan, dengan grup pada ruas kiri
membawa aksi kanan reguler melalui perkalian.
:::

::: {.proof #o012-rbt-l10-proof-002}
**Bukti.** Karena $Z$ terhubung sederhana,
$\pi_1(Z,z)=1$. Stabilisator $z$ karena itu trivial, sehingga Teorema 9.2
memberi

$$
Z_x
\cong
\{1\}\backslash\pi_1(X,x)
\cong
\pi_1(X,x)
$$

secara ekuivarian untuk aksi kanan. $\square$
:::

::: {.example #o012-rbt-l10-exa-001}
**Contoh 10.1 (keterhitungan grup fundamental lingkaran).** Kini kita dapat
mengatakan bahwa $\pi_1(S^1,1)$ bukan hanya tak hingga, seperti yang sudah
dibuktikan pada Contoh 7.3, melainkan juga terhitung. Memang, ia berbijeksi
dengan serat $\mathbb Z$ dari ruang penutup terhubung sederhana

$$
\mathbb R\longrightarrow S^1,
\qquad
t\longmapsto e^{2\pi i t},
$$

di atas $1\in S^1$.
:::

Akibat 10.1 memberi lebih dari sekadar bijeksi. Untuk aksi kanan langsung,
tuliskan

$$
R_g\colon Z_x\longrightarrow Z_x,
\qquad
R_g(u)=u\mathbin{\cdot}g.
$$

Hukum aksi memberi

$$
R_{gh}=R_h\circ R_g.
$$

Jadi $g\mapsto R_g$ adalah aksi permutasi kanan, atau antihomomorfisma ke
grup permutasi bila komposisi fungsi dibaca dengan konvensi biasa. Dengan
membalik unsur grup, kita memperoleh representasi permutasi kiri

$$
\begin{aligned}
\lambda\colon\pi_1(X,x)&\longrightarrow\operatorname{Aut}(Z_x),\\
g&\longmapsto R_{g^{-1}},
\end{aligned}
$$

yang merupakan homomorfisma. Representasi ini *setia*. Jika $g\ne h$, maka
bijeksi Akibat 10.1 memberi suatu $u\in Z_x$---bahkan titik dasar $z$ sudah
cukup---dengan

$$
u\mathbin{\cdot}g^{-1}
\ne
u\mathbin{\cdot}h^{-1}.
$$

Dengan demikian $\lambda(g)\ne\lambda(h)$. Grup fundamental kini
direalisasikan sebagai grup permutasi, tempat perhitungan dapat dilakukan
secara lebih konkret.

::: {.corollary #o012-rbt-l10-cor-002}
**Akibat 10.2 (aksi bebas pada serat).** Untuk ruang penutup terhubung
sederhana bertitik $(Z,z)\to(X,x)$, aksi kanan
$\pi_1(X,x)$ pada $Z_x$ bersifat bebas.
:::

Sekarang kita dapat memberi contoh pertama grup fundamental nontrivial yang
dihitung secara lengkap.

::: {.theorem #o012-rbt-l10-thm-001}
**Teorema 10.1 (grup fundamental lingkaran).** Terdapat isomorfisma grup

$$
\pi_1(S^1,1)\cong\mathbb Z.
$$
:::

::: {.proof #o012-rbt-l10-proof-003}
**Bukti.** Gunakan ruang penutup terhubung sederhana

$$
q\colon\mathbb R\longrightarrow S^1,
\qquad
q(t)=e^{2\pi i t},
$$

yang turun menjadi homeomorfisma
$\mathbb R/\mathbb Z\cong S^1$ dan yang seratnya di atas $1\in S^1$ adalah
$\mathbb Z$. Inklusi

$$
[0,1]\longrightarrow\mathbb R,
\qquad
t\longmapsto t,
$$

merupakan pengangkatan loop $\gamma$ yang mengelilingi lingkaran satu kali
dalam arah positif. Semua pengangkatan loop itu adalah translasi inklusi
tersebut. Karena itu aksi kanan $[\gamma]$ pada serat $\mathbb Z$ adalah
translasi sebesar $1$:

$$
n\mathbin{\cdot}[\gamma]=n+1.
$$

Lebih umum,

$$
n\mathbin{\cdot}[\gamma]^k=n+k
\qquad(k,n\in\mathbb Z).
$$

Jadi subgrup yang dibangkitkan oleh $[\gamma]$ sudah bertindak transitif
pada $\mathbb Z$. Di sisi lain, Akibat 10.2 menyatakan bahwa aksi seluruh
$\pi_1(S^1,1)$ bebas. Untuk setiap $g\in\pi_1(S^1,1)$, pilih $k\in\mathbb Z$
dengan

$$
0\mathbin{\cdot}g=k
=
0\mathbin{\cdot}[\gamma]^k.
$$

Kebebasan aksi memaksa $g=[\gamma]^k$. Maka $[\gamma]$ membangkitkan seluruh
grup. Karena translasi sebesar $k$ hanya identitas ketika $k=0$, pembangkit
itu berordo tak hingga. Jadi grupnya siklik tak hingga dan isomorfik dengan
$\mathbb Z$. $\square$
:::

Akibatnya, untuk setiap $A\subseteq S^1$, grupoid fundamental terbatas
$\Pi_1(S^1,A)$ mempunyai himpunan objek $A$. Untuk setiap $x\in A$,

$$
\pi_1(S^1,x)\cong\mathbb Z.
$$

Untuk setiap $x,y\in A$, himpunan morfisma
$\Pi_1(S^1,A)(x,y)$ tidak kosong dan berbijeksi dengan $\mathbb Z$ sebagai
himpunan. Bijeksi terakhir tidak kanonik sebelum suatu kelas lintasan dari
$x$ menuju $y$ dipilih.

Bagaimana kita menghitung $\pi_1$ secara umum---atau, lebih baik,
$\Pi_1$? Jika sebuah ruang merupakan gabungan saling lepas dari dua komponen
lintasan,

$$
X=X_1\sqcup X_2,
$$

maka tidak ada morfisma grupoid fundamental di antara kedua komponen, dan
karena itu

$$
\Pi_1(X,A)
=
\Pi_1(X_1,A\cap X_1)
\sqcup
\Pi_1(X_2,A\cap X_2).
$$

Jika $A\cap X_i\ne\varnothing$ untuk $i=1,2$, maka setiap titik di $X$ dapat
dihubungkan oleh lintasan ke suatu titik di $A$. Dengan demikian grup
fundamental kedua komponen lintasan terwakili di dalam grupoid terbatas
tersebut.

::: {.example #o012-rbt-l10-exa-002}
**Contoh 10.2 (dua lingkaran yang saling lepas).** Grupoid

$$
\Pi_1(S^1\sqcup S^1,\{1\}\sqcup\{1\})
$$

mempunyai dua objek. Tidak terdapat morfisma di antara kedua objek itu, dan
grup automorfisma masing-masing objek isomorfik dengan $\mathbb Z$.
:::

## Baji ruang bertitik {#o012-rbt-l10-s02}

Kita akan memusatkan perhatian sejenak pada perhitungan grup fundamental,
atau grupoid fundamental, bagi ruang terhubung lintasan. Cara paling sederhana
membuat ruang terhubung baru dari dua ruang terhubung $X$ dan $Y$ ialah
memilih $x\in X$ serta $y\in Y$, lalu mengidentifikasi kedua titik itu. Sesuai
konvensi mata kuliah, ruang yang digunakan di sini bersifat terhubung lintasan
semilokal (SLPC); menurut Proposisi 4.2, dalam kelas ruang tersebut komponen
dan komponen lintasan berimpit.

::: {.definition #o012-rbt-l10-def-001}
**Definisi 10.1 (baji).** Untuk dua ruang bertitik $(X,x)$ dan $(Y,y)$,
*baji* $X\vee Y$ adalah ruang hasil bagi

$$
X\vee Y
:=
(X\sqcup Y)/(x\sim y).
$$

Titik dasarnya adalah

$$
*=[x]=[y].
$$

Pemetaan inklusi kanonik memberi diagram ruang bertitik

$$
(X,x)
\xrightarrow{\ \operatorname{in}_L\ }
(X\vee Y,*)
\xleftarrow{\ \operatorname{in}_R\ }
(Y,y).
$$
:::

Sifat utama baji adalah sifat universal berikut. Jika $(M,m)$ suatu ruang
bertitik dan

$$
f\colon(X,x)\longrightarrow(M,m),
\qquad
g\colon(Y,y)\longrightarrow(M,m)
$$

pemetaan bertitik, maka terdapat tepat satu pemetaan bertitik

$$
\langle f,g\rangle
\colon
(X\vee Y,*)\longrightarrow(M,m)
$$

yang memenuhi persamaan bertipe benar

$$
\langle f,g\rangle\circ\operatorname{in}_L=f,
\qquad
\langle f,g\rangle\circ\operatorname{in}_R=g.
$$

Karena semua pemetaan tersebut bertitik, fungtorialitas $\pi_1$ memberi dua
homomorfisma

$$
\pi_1(X,x)
\xrightarrow{\ \pi_1(\operatorname{in}_L)\ }
\pi_1(X\vee Y,*)
\xleftarrow{\ \pi_1(\operatorname{in}_R)\ }
\pi_1(Y,y).
$$

Jika grup fundamental $X$ dan $Y$ sudah diketahui, kita dapat mencoba
memanfaatkan keduanya untuk memahami grup fundamental bajinya. Sebagai
contoh, untuk $X=Y=S^1$ diperoleh

$$
\mathbb Z
\xrightarrow{\ \pi_1(\operatorname{in}_L)\ }
\pi_1(S^1\vee S^1,*)
\xleftarrow{\ \pi_1(\operatorname{in}_R)\ }
\mathbb Z.
$$

Definisikan

$$
a:=\pi_1(\operatorname{in}_L)(1),
\qquad
b:=\pi_1(\operatorname{in}_R)(1).
$$

Jadi $a$ dan $b$ adalah kelas loop yang masing-masing mengelilingi lingkaran
kiri dan kanan satu kali dalam arah positif.

## Penutup tiga lembaran yang mendeteksi nonkomutativitas {#o012-rbt-l10-s03}

Definisikan ruang penutup

$$
q_1\colon Z_1\longrightarrow S^1\vee S^1
$$

sebagai graf berarah berlabel berikut. Sumber menamai panah penutup ini
$\pi_1$; edisi menulisnya sebagai $q_1$ agar tidak bertabrakan dengan fungtor
grup fundamental $\pi_1$. Ruang dasar mempunyai satu simpul $*$ dan dua loop
berarah $a$ dan $b$. Ruang atas mempunyai tiga simpul $A,B,C$, semuanya
dipetakan ke $*$, dan enam sisi berarah:

::: {.figure #o012-rbt-l10-fig-001}
**Diagram linear penutup $q_1$.** Sisi-sisi yang dipetakan ke loop $a$ ialah

$$
A\xrightarrow{\ a_1\ }A,
\qquad
B\xrightarrow{\ a_2\ }C,
\qquad
C\xrightarrow{\ a_3\ }B,
$$

sedangkan sisi-sisi yang dipetakan ke loop $b$ ialah

$$
A\xrightarrow{\ b_1\ }B,
\qquad
B\xrightarrow{\ b_2\ }A,
\qquad
C\xrightarrow{\ b_3\ }C.
$$

Dengan kata lain,

$$
q_1(A)=q_1(B)=q_1(C)=*,
\qquad
q_1(a_i)=a,
\qquad
q_1(b_i)=b
\quad(i=1,2,3).
$$

Daftar tersebut merupakan pengganti aksesibel bagi gambar sumber: dari
setiap simpul terdapat tepat satu sisi keluar dan satu sisi masuk berlabel
$a$, serta tepat satu sisi keluar dan satu sisi masuk berlabel $b$.
:::

Pengangkatan loop memberi aksi kanan pada serat

$$
(Z_1)_*=\{A,B,C\}.
$$

Tuliskan $R_w(u)=u\mathbin{\cdot}w$ bagi operator titik akhir pengangkatan
kata loop $w$. Dari daftar sisi diperoleh

$$
R_a=(BC),
\qquad
R_b=(AB)
$$

sebagai permutasi $\{A,B,C\}$. Karena kata $ab$ berarti menelusuri $a$
terlebih dahulu lalu $b$, hukum aksi kanan memberi

$$
R_{ab}=R_b\circ R_a=(ABC).
$$

Serupa dengan itu,

$$
R_{ba}=R_a\circ R_b=(ACB).
$$

Kedua permutasi tersebut berbeda, sehingga $ab\ne ba$ di
$\pi_1(S^1\vee S^1,*)$. Dengan kata lain, grup fundamental baji dua
lingkaran **tidak abelian**.

Jika diinginkan representasi permutasi sebagai homomorfisma dengan komposisi
fungsi biasa, definisikan

$$
\rho_1(g):=R_{g^{-1}}.
$$

Maka

$$
\rho_1\colon
\pi_1(S^1\vee S^1,*)
\longrightarrow
\operatorname{Aut}\{A,B,C\}
\cong S_3
$$

merupakan homomorfisma. Karena $a$ dan $b$ dipetakan ke involusi, tetap
berlaku

$$
\rho_1(a)=(BC),
\qquad
\rho_1(b)=(AB),
$$

tetapi urutan siklus kompositnya berbalik terhadap operator kanan:

$$
\rho_1(ab)=(ACB),
\qquad
\rho_1(ba)=(ABC).
$$

Perbedaan itu hanyalah akibat konvensi aksi; kedua perhitungan membuktikan
kesimpulan nonkomutativitas yang sama.

Dengan memilih ruang penutup secara cermat, orang juga dapat membuktikan
bahwa kedua homomorfisma

$$
\mathbb Z\longrightarrow\pi_1(S^1\vee S^1,*)
$$

di atas injektif. Jadi $a$ dan $b$ masing-masing membangkitkan subgrup siklik
tak hingga. Kelak akan dibuktikan bahwa

$$
\pi_1(S^1\vee S^1,*)
\cong
\mathbb Z*\mathbb Z
=F_2,
$$

yakni grup bebas pada pembangkit $a,b$, dengan presentasi

$$
\langle a,b\mid\ \rangle.
$$

Setelah hasil itu tersedia, setiap unsur bukan identitas mempunyai bentuk
kata tereduksi yang berganti-ganti di antara pangkat tak nol dari $a$ dan
pangkat tak nol dari $b$. Kata dapat dimulai atau berakhir pada salah satu
faktor; identitas diwakili oleh kata kosong. Misalnya salah satu pola yang
mungkin ialah

$$
a^{n_1}b^{m_1}\cdots a^{n_k}b^{m_k},
$$

dengan setiap eksponen pada blok yang benar-benar tampil tidak nol; blok awal
atau akhir dapat dihilangkan agar kata dimulai atau berakhir pada salah satu
faktor. Pernyataan bentuk bebas ini masih merupakan pratinjau pada tahap
sekarang, bukan akibat dari satu penutup tiga lembaran saja.

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l10-mastery}

Bagian ini menambahkan lima pemeriksaan yang menutup langkah-langkah paling
mudah terlewat ketika unit dipelajari secara mandiri.

::: {.exercise #o012-rbt-l10-mcheck-001}
**Pemeriksaan penguasaan 10.1 (aksi reguler dari penutup terhubung
sederhana).** Dalam situasi Akibat 10.1:

1. buktikan langsung bahwa pemetaan
   $\Phi(g)=z\mathbin{\cdot}g$ terdefinisi dengan baik dan bijektif;
2. buktikan bahwa aksi pada $Z_x$ bebas dan transitif;
3. periksa bahwa $\lambda(g)=R_{g^{-1}}$ merupakan homomorfisma injektif ke
   $\operatorname{Aut}(Z_x)$;
4. untuk penutup terhubung lintasan yang tidak harus terhubung sederhana,
   buktikan bagaimana stabilisator berubah ketika titik pilihan dalam serat
   diganti, baik dalam konvensi aksi kanan maupun aksi kiri.
:::

## Solusi Pemeriksaan 10.1 {#o012-rbt-l10-sol-001}

Karena $Z$ terhubung lintasan, untuk setiap $u\in Z_x$ pilih lintasan
$\delta\colon z\rightsquigarrow u$ di $Z$. Loop $\pi\circ\delta$ pada $x$
memenuhi

$$
z\mathbin{\cdot}[\pi\circ\delta]=u,
$$

sehingga $\Phi$ surjektif. Jika $\Phi(g)=\Phi(h)$, maka

$$
z\mathbin{\cdot}(gh^{-1})=z.
$$

Stabilisator $z$ adalah
$\pi_*\pi_1(Z,z)=1$, sehingga $gh^{-1}=1$ dan $g=h$. Jadi $\Phi$ bijektif.

Surjektivitas $\Phi$ tepat menyatakan transitivitas. Jika
$u\mathbin{\cdot}g=u$, tulis $u=z\mathbin{\cdot}h$. Maka

$$
z\mathbin{\cdot}(hg)=z\mathbin{\cdot}h.
$$

Injektivitas $\Phi$ memberi $hg=h$, lalu $g=1$. Jadi aksi bebas.

Terakhir, dari $R_{gh}=R_h\circ R_g$ diperoleh

$$
\lambda(gh)
=R_{(gh)^{-1}}
=R_{h^{-1}g^{-1}}
=R_{g^{-1}}\circ R_{h^{-1}}
=\lambda(g)\circ\lambda(h).
$$

Jika $\lambda(g)=\lambda(h)$, evaluasi pada $z$ memberi
$z\mathbin{\cdot}g^{-1}=z\mathbin{\cdot}h^{-1}$. Kebebasan aksi memaksa
$g^{-1}=h^{-1}$, sehingga $g=h$. Jadi $\lambda$ homomorfisma injektif.

Untuk pernyataan perubahan titik, sekarang ambil penutup terhubung lintasan
umum dan tuliskan $H_z=\operatorname{Stab}(z)$. Jika
$z'=z\mathbin{\cdot}g$, maka

$$
\begin{aligned}
h\in H_{z'}
&\iff (z\mathbin{\cdot}g)\mathbin{\cdot}h
       =z\mathbin{\cdot}g\\
&\iff z\mathbin{\cdot}(ghg^{-1})=z\\
&\iff ghg^{-1}\in H_z.
\end{aligned}
$$

Karena itu

$$
H_{z'}=g^{-1}H_zg.
$$

Dalam konvensi kiri $g\star u=u\mathbin{\cdot}g^{-1}$, persamaan
$z'=g\star z$ berarti $z'=z\mathbin{\cdot}g^{-1}$, sehingga rumus yang sama
menjadi

$$
H_{z'}=gH_zg^{-1}.
$$

Jadi penutup bertitik menentukan subgrup tertentu, sedangkan penutup tanpa
pilihan titik dalam serat secara alami hanya menentukan kelas konjugasinya.

::: {.exercise #o012-rbt-l10-mcheck-002}
**Pemeriksaan penguasaan 10.2 (mengapa loop sekali putar membangkitkan).**
Untuk penutup $q(t)=e^{2\pi it}$:

1. tunjukkan bahwa pengangkatan $\gamma^k$ yang berawal di $n\in\mathbb Z$
   berakhir di $n+k$;
2. gunakan kebebasan dan transitivitas aksi untuk membuktikan bahwa setiap
   kelas loop sama dengan tepat satu $[\gamma]^k$;
3. untuk $x,y\in A\subseteq S^1$, jelaskan mengapa
   $\Pi_1(S^1,A)(x,y)$ hanya *berbijeksi*, bukan berisomorfisma grup secara
   alami, dengan $\mathbb Z$ ketika $x\ne y$.
:::

## Solusi Pemeriksaan 10.2 {#o012-rbt-l10-sol-002}

Pengangkatan $\gamma$ mulai dari $n$ adalah $t\mapsto n+t$ dan berakhir di
$n+1$. Konkatenasi kronologis serta keunikan pengangkatan menunjukkan secara
induktif bahwa pengangkatan $\gamma^k$ berakhir di $n+k$ untuk $k\geq0$.
Untuk $k<0$, ulangi loop balik $-k$ kali; satu loop balik yang berawal di
$n$ mengangkat menjadi $t\mapsto n-t$. Titik akhirnya kembali $n+k$.

Ambil $g\in\pi_1(S^1,1)$. Karena aksi transitif, titik
$0\mathbin{\cdot}g$ adalah suatu $k\in\mathbb Z$. Perhitungan sebelumnya
memberi

$$
0\mathbin{\cdot}[\gamma]^k=k.
$$

Karena aksi bebas, kesamaan kedua titik akhir memaksa
$g=[\gamma]^k$. Jika $[\gamma]^k=[\gamma]^\ell$, evaluasi pada $0$ memberi
$k=\ell$. Jadi pangkat itu ada dan unik.

Untuk $x,y\in A$, pilih satu kelas lintasan
$c\colon x\rightsquigarrow y$. Pascakomposisi dengan $c$ memberi bijeksi

$$
\pi_1(S^1,x)
\xrightarrow{\;\cong\;}
\Pi_1(S^1,A)(x,y)
$$

sebagai himpunan. Pilihan kelas $c$ lain mengubah bijeksi tersebut. Selain
itu, bila $x\ne y$, himpunan morfisma itu tidak memiliki operasi komposisi
internal karena dua morfisma $x\to y$ tidak dapat langsung dikomposisikan.
Jadi ia merupakan torsor bagi grup automorfisma terkait, bukan sebuah grup
kanonik.

::: {.exercise #o012-rbt-l10-mcheck-003}
**Pemeriksaan penguasaan 10.3 (sifat universal baji).** Misalkan
$f\colon(X,x)\to(M,m)$ dan $g\colon(Y,y)\to(M,m)$ pemetaan bertitik.

1. bangun $\langle f,g\rangle$ dari pemetaan pada gabungan saling lepas;
2. buktikan kekontinuannya dengan sifat hasil bagi;
3. buktikan keunikannya dan periksa urutan komposisi pada kedua persamaan
   pembatasan.
:::

## Solusi Pemeriksaan 10.3 {#o012-rbt-l10-sol-003}

Definisikan

$$
F\colon X\sqcup Y\longrightarrow M
$$

dengan $F|_X=f$ dan $F|_Y=g$. Pemetaan ini kontinu menurut sifat koproduk.
Karena $f(x)=m=g(y)$, pemetaan $F$ konstan pada kelas ekuivalensi yang
mengidentifikasi $x$ dengan $y$. Sifat universal hasil bagi karena itu
memberi satu-satunya pemetaan kontinu

$$
\langle f,g\rangle\colon X\vee Y\longrightarrow M
$$

dengan $\langle f,g\rangle\circ q=F$, tempat
$q\colon X\sqcup Y\to X\vee Y$ adalah pemetaan hasil bagi. Nilai titik
bajinya adalah $m$, jadi pemetaan tersebut bertitik.

Membatasi persamaan pada salinan $X$ dan $Y$ memberi

$$
\langle f,g\rangle\circ\operatorname{in}_L=f,
\qquad
\langle f,g\rangle\circ\operatorname{in}_R=g.
$$

Urutan sebaliknya tidak bertipe: $\operatorname{in}_L$ mempunyai kodomain
$X\vee Y$, bukan domain $M$. Jika $h\colon X\vee Y\to M$ mempunyai kedua
pembatasan yang sama, maka $h\circ q=F$ pada setiap komponen
$X\sqcup Y$. Surjektivitas $q$ memaksa
$h=\langle f,g\rangle$, yang membuktikan keunikan.

::: {.exercise #o012-rbt-l10-mcheck-004}
**Pemeriksaan penguasaan 10.4 (membaca penutup tiga lembaran).** Gunakan daftar
sisi pada Diagram 10.1 untuk:

1. memeriksa secara lokal bahwa $q_1$ adalah penutup graf tiga lembaran;
2. menghitung $R_a,R_b,R_{ab},R_{ba}$ titik demi titik;
3. menjelaskan mengapa perbedaan $R_{ab}$ dan $R_{ba}$ membuktikan
   $ab\ne ba$ tanpa mengharuskan $g\mapsto R_g$ menjadi homomorfisma biasa;
4. mengubah aksi kanan itu menjadi representasi kiri $\rho_1$.
:::

## Solusi Pemeriksaan 10.4 {#o012-rbt-l10-sol-004}

Ambil lingkungan kecil $U$ dari simpul $*$ yang terdiri atas ruas pendek pada
keempat ujung terarah kedua loop. Di atas setiap simpul $A,B,C$, daftar sisi
menyediakan tepat satu ruas yang memetakan homeomorfik ke setiap ruas keluar
dan masuk berlabel $a$ maupun $b$. Ketiga lingkungan bintang yang dihasilkan
saling lepas dan masing-masing dipetakan homeomorfik ke $U$. Pada bagian
dalam setiap sisi, sifat penutup jelas dari pemetaan interval ke interval.
Jadi $q_1$ merupakan penutup tiga lembaran.

Dari sisi berlabel $a$,

$$
A\mathbin{\cdot}a=A,
\qquad
B\mathbin{\cdot}a=C,
\qquad
C\mathbin{\cdot}a=B,
$$

sehingga $R_a=(BC)$. Dari sisi berlabel $b$,

$$
A\mathbin{\cdot}b=B,
\qquad
B\mathbin{\cdot}b=A,
\qquad
C\mathbin{\cdot}b=C,
$$

sehingga $R_b=(AB)$. Menelusuri $a$ lalu $b$ memberi

$$
\begin{array}{c|ccc}
u&A&B&C\\ \hline
u\mathbin{\cdot}(ab)&B&C&A,
\end{array}
$$

jadi $R_{ab}=(ABC)$. Menelusuri $b$ lalu $a$ memberi

$$
\begin{array}{c|ccc}
u&A&B&C\\ \hline
u\mathbin{\cdot}(ba)&C&A&B,
\end{array}
$$

jadi $R_{ba}=(ACB)$. Jika $ab=ba$ sebagai elemen grup fundamental, aksi apa
pun harus memberi operator titik akhir yang sama. Karena kedua operator di
atas berbeda, $ab\ne ba$. Argumen ini hanya memakai bahwa aksi menghormati
kesamaan unsur; tidak perlu menyebut pemetaan ke grup permutasi sebagai
homomorfisma biasa.

Untuk memperoleh homomorfisma biasa, tetapkan
$\rho_1(g)=R_{g^{-1}}$. Perhitungan pada Solusi 10.1 membuktikan

$$
\rho_1(gh)=\rho_1(g)\circ\rho_1(h).
$$

Karena $a^{-1}$ dan $b^{-1}$ bekerja melalui transposisi yang sama dengan
$a$ dan $b$, nilai pada pembangkit tetap $(BC)$ dan $(AB)$. Inversi kata
menjelaskan mengapa siklus bagi $ab$ dan $ba$ bertukar dibandingkan dengan
operator kanan langsung.

::: {.exercise #o012-rbt-l10-mcheck-005}
**Pemeriksaan penguasaan 10.5 (apa yang sudah dan belum dibuktikan).** Pisahkan
kesimpulan berikut menjadi yang sudah dibuktikan dalam unit ini, yang hanya
dinyatakan dapat dibuktikan dengan penutup lain, dan yang ditunda sampai
teorema berikutnya:

1. $a$ dan $b$ tidak komutatif;
2. masing-masing homomorfisma
   $\mathbb Z\to\pi_1(S^1\vee S^1,*)$ injektif;
3. $a$ dan $b$ membangkitkan seluruh grup fundamental;
4. tidak ada relasi taktrivial di antara $a$ dan $b$;
5. setiap unsur mempunyai bentuk kata tereduksi yang unik.
:::

## Solusi Pemeriksaan 10.5 {#o012-rbt-l10-sol-005}

Penutup tiga lembaran memberi $R_{ab}\ne R_{ba}$, jadi butir 1 sudah
dibuktikan. Sumber menyatakan bahwa penutup yang dipilih dengan cermat dapat
membuktikan injektivitas pada butir 2, tetapi penutup-penutup tambahan itu
belum dibangun dalam rentang ini. Karena itu butir 2 baru merupakan hasil yang
diumumkan, bukan hasil yang telah dibuktikan di sini.

Butir 3--5 akan mengikuti dari teorema

$$
\pi_1(S^1\vee S^1,*)\cong F_2,
$$

yang sumber janjikan untuk dibuktikan kemudian. Nonkomutativitas saja tidak
menunjukkan bahwa $a,b$ membangkitkan seluruh grup, dan juga tidak meniadakan
relasi lain. Setelah isomorfisma dengan $F_2$ terbukti, bentuk normal yang
tepat adalah kata tereduksi: huruf-huruf bukan identitas berasal
berganti-ganti dari dua faktor siklik; secara ekuivalen, kata memakai pangkat
tak nol dari $a$ dan $b$ secara berselang-seling. Identitas adalah kata kosong.
Keunikan bentuk tersebut merupakan bagian dari teori produk bebas, bukan
akibat langsung dari representasi ke $S_3$ yang tidak mungkin setia karena
$F_2$ tak hingga sedangkan $S_3$ berhingga.
