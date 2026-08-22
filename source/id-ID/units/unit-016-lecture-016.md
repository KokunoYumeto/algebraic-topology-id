---
title: "Topologi Aljabar"
subtitle: "Unit 16: Penutup Universal, Hasil Bagi Subgrup, dan Surjektivitas Esensial"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l16-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts, © 2019 David Michael Roberts, tepatnya
[Notes.tex baris 3287--3383 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L3287-L3383)
dari repositori
[DavidMichaelRoberts/AlgebraicTopology2019](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019).
Rentang itu dimulai dengan penanda Kuliah 16 pada baris 3287 dan berakhir
sesudah proposisi surjektivitas esensial pada baris 3381 serta dua baris
kosong. Penanda Kuliah 17 pada baris 3384 tidak termasuk dalam unit ini.
Materi sumber dan adaptasi Indonesia ini tersedia di bawah [Creative Commons
Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/).

Perubahan edisi mencakup penerjemahan, pemformatan ulang agar mudah dibaca,
pemberian pengenal stabil, dan pemindahan keempat catatan pinggir ke urutan
bacaan utama. Kedua segitiga Xy-pic ditulis ulang sebagai diagram semantik
dengan daftar panah dan persamaan komutativitas. Hubungan matematisnya tidak
bergantung pada posisi visual.

Edisi ini memperbaiki beberapa cacat matematis sumber. Monodromi langsung
tetap merupakan aksi **kanan**, sehingga serat penutup yang merealisasikan
subgrup $H\leq G$ ialah ruang koset kanan $H\backslash G$, bukan $G/H$.
Aksi kiri serat demi serat, untuk $h=[\omega]$,
$h\mathbin{\cdot}[\gamma]=[\omega\#\gamma]$, pada penutup universal
dibedakan dari aksi kanan monodromi
$[\gamma]\mathbin{\cdot}g=[\gamma\#\eta]$ untuk $g=[\eta]$; kedua aksi itu
saling komutatif. Pernyataan keliru
$\pi_1(X^{(1)},*)=H$ diganti oleh pernyataan bertipe benar

$$
(p_H)_*\pi_1(H\backslash\widetilde X,H[c_{x_0}])=H
\leq\pi_1(X,x_0).
$$

Sumber menyebut ruang kelas lintasan sebagai ruang hasil bagi dan kemudian
menunda bukti topologinya ke halaman 64--65 buku Hatcher. Di sini himpunan
kelas lintasan diberi **topologi basis penutup** secara langsung. Edisi ini
tidak menyatakan tanpa bukti bahwa topologi tersebut sama dengan topologi
hasil bagi dari topologi kompak-terbuka, dan tidak memakai pemilihan lintasan
yang berubah kontinu terhadap titik ujung. Aksi kiri, aksi kanan, aksioma
basis, partisi lembaran, keterhubungan lintasan, keterhubungan sederhana,
realisasi subgrup, dan kesurjektifan esensial semuanya dibuktikan. Prosa
pembanding tidak disalin. Notasi sumber $X^{(1)}$ untuk penutup universal
dinormalkan menjadi $\widetilde X$, sedangkan penutup yang merealisasikan
$H$ selalu ditulis terpisah sebagai $H\backslash\widetilde X$.

Keenam pemeriksaan penguasaan beserta solusi lengkap merupakan materi asli
edisi, tersedia di bawah CC BY 4.0. Materi itu tidak memperkenalkan
klasifikasi transformasi dek ataupun kepenuhan dan kesetiaan fungtor, yang
merupakan perkara kuliah kemudian. Edisi ini bersifat independen; edisi ini
tidak disponsori, didukung, disahkan, ataupun diberi status resmi oleh David
Michael Roberts, Allen Hatcher, Cornell University, MIT, Haynes Miller,
Sanath Devalapurkar, Yeheli Fomberg, Nir Lazarovich, atau institusi mereka.

# Kuliah 16 {#o012-rbt-l16}

Sepanjang unit ini, konkatenasi $\alpha\#\beta$ ditempuh secara
**kronologis**: mula-mula $\alpha$, kemudian $\beta$. Jika
$p\colon Z\to X$ ruang penutup, transpor titik akhir langsung ditulis sebagai
aksi kanan

$$
z\cdot[\eta]:=\eta_*^Z(z).
$$

Karena itu, bila $X$ terhubung lintasan dan
$G:=\pi_1(X,x_0)$, serat di atas $x_0$ dari suatu penutup terhubung sederhana
merupakan torsor **kanan** $G$. Tujuan yang tersisa dari Unit 15 ialah
membangun penutup tersebut dan, bagi $H\leq G$, memperoleh serat
$H\backslash G$. Mengambil hasil bagi tiap serat secara terpisah tidak
mendefinisikan topologi ruang total; hasil bagi harus dilakukan sekaligus.

## Aksi serat demi serat dan hasil bagi ruang penutup {#o012-rbt-l16-s01}

::: {.definition #o012-rbt-l16-def-001}
**Definisi 16.1 (aksi serat demi serat).** Misalkan $p\colon Y\to X$ suatu
pemetaan dan $K$ grup diskret yang bertindak kontinu dari kiri pada $Y$.
Aksi itu disebut **serat demi serat** jika

$$
p(k\cdot y)=p(y)
$$

untuk setiap $y\in Y$ dan $k\in K$. Setiap $k$ dengan demikian bertindak
sebagai homeomorfisma di atas $X$.
:::

Definisi itu memberi satu-satunya pemetaan
$\bar p\colon K\backslash Y\to X$ yang memenuhi
$\bar p(Ky)=p(y)$. Seratnya di atas $x$ ialah
$K\backslash p^{-1}(x)$.

::: {.diagram #o012-rbt-l16-dia-001}
**Diagram 16.1 (segitiga hasil bagi).** Data panahnya adalah

$$
Y\xrightarrow{\ q\ }K\backslash Y,
\qquad
Y\xrightarrow{\ p\ }X,
\qquad
K\backslash Y\xrightarrow{\ \bar p\ }X,
$$

dengan $q(y)=Ky$. Persamaan komutativitasnya ialah

$$
\bar p\circ q=p.
$$
:::

::: {.proposition #o012-rbt-l16-prop-001}
**Proposisi 16.1 (hasil bagi suatu ruang penutup).** Misalkan
$p\colon Z\to X$ ruang penutup dan $X$ SLSC dalam konvensi mata kuliah. Jika
grup diskret $K$ bertindak dari kiri pada $Z$ secara serat demi serat, maka

$$
\bar p\colon K\backslash Z\longrightarrow X
$$

merupakan ruang penutup dan peta hasil bagi
$q\colon Z\to K\backslash Z$ merupakan pemetaan ruang penutup di atas $X$.
:::

::: {.proof #o012-rbt-l16-proof-001}
**Bukti.** Ambil $x\in X$. Pilih lingkungan terbuka terhubung lintasan
$U\ni x$ yang diliputi secara merata oleh $p$; pilihan seperti ini tersedia
dalam konvensi SLSC mata kuliah dengan memperkecil suatu lingkungan yang
diliputi secara merata. Tuliskan $F:=p^{-1}(x)$. Dengan menandai setiap
lembaran oleh satu-satunya titiknya di atas $x$, diperoleh homeomorfisma di
atas $U$

$$
p^{-1}(U)\cong U\times F.
$$

Setiap $k\in K$ mengirim satu lembaran terhubung lintasan ke suatu himpunan
terhubung di atas $U$, jadi ke satu lembaran. Karena $k^{-1}$ juga demikian,
$k$ benar-benar mempermutasikan lembaran-lembaran utuh. Pada satu lembaran,
persamaan $p(k\cdot z)=p(z)$ memaksa peta itu menjadi identitas pada
koordinat $U$. Maka trivialiasi di atas ekuivarian untuk rumus

$$
k\cdot(u,f)=(u,k\cdot f).
$$

Peta hasil bagi $q$ terbuka, sebab bagi himpunan terbuka $O\subseteq Z$,

$$
q^{-1}(q(O))=\bigcup_{k\in K}k\cdot O
$$

terbuka. Himpunan $p^{-1}(U)$ jenuh terhadap aksi, sehingga pembatasan
hasil bagi mempunyai topologi yang tepat dan memberi homeomorfisma

$$
\bar p^{-1}(U)
\cong
K\backslash p^{-1}(U)
\cong
U\times(K\backslash F)
$$

di atas $U$. Karena $F$ diskret, $K\backslash F$ juga diskret. Jadi $U$
diliputi secara merata oleh $\bar p$. Hal ini berlaku di sekitar setiap
$x$, maka $\bar p$ adalah ruang penutup. Persamaan
$\bar p\circ q=p$ menunjukkan bahwa $q$ merupakan pemetaan ruang penutup.
Ini juga membuktikan identifikasi pembatasan dan hasil bagi yang oleh sumber
diserahkan kepada Tugas 4.
:::

## Aksi kiri hasil bagi dan monodromi kanan {#o012-rbt-l16-s02}

Andaikan untuk sementara bahwa penutup terhubung sederhana bertitik
$p\colon(Z^{(1)},z_0)\to(X,x_0)$ telah tersedia. Serat
$Z^{(1)}_{x_0}$ merupakan torsor kanan untuk
$G=\pi_1(X,x_0)$. Jika $G$, yang dipandang diskret, juga bertindak dari
**kiri** secara serat demi serat sehingga identifikasi serat dengan $G$
mengubah aksi itu menjadi perkalian kiri, pembatasan aksi ke $H\leq G$ dan
Proposisi 16.1 memberi

$$
p_H\colon H\backslash Z^{(1)}\longrightarrow X,
\qquad
(p_H)^{-1}(x_0)\cong H\backslash G.
$$

Rumus ini memperbaiki sisi koset pada sumber: $H\backslash G$ membawa aksi
kanan $(Hg)\cdot k=H(gk)$, sedangkan $G/H$ tidak membawa rumus itu untuk
subgrup umum.

::: {.lemma #o012-rbt-l16-lem-001}
**Lema 16.1 (ekuivariansi peta hasil bagi).** Dalam situasi di atas, untuk
setiap $x\in X$ peta serat

$$
q_x\colon Z^{(1)}_x\longrightarrow
(H\backslash Z^{(1)})_x
$$

ekuivarian terhadap aksi kanan $\pi_1(X,x)$ melalui monodromi. Lebih umum,
untuk kelas lintasan $[\eta\colon x\rightsquigarrow y]$,

$$
q_y\bigl(z\cdot[\eta]\bigr)
=q_x(z)\cdot[\eta].
$$
:::

::: {.proof #o012-rbt-l16-proof-002}
**Bukti.** Angkat $\eta$ ke lintasan $\widetilde\eta_z$ di $Z^{(1)}$ yang
mulai di $z$. Karena $q$ merupakan pemetaan ruang penutup di atas $X$,
$q\circ\widetilde\eta_z$ adalah pengangkatan $\eta$ ke
$H\backslash Z^{(1)}$ yang mulai di $q_x(z)$. Keunikan pengangkatan memberi

$$
q_y\bigl(\widetilde\eta_z(1)\bigr)
=\widetilde\eta_{q_x(z)}(1),
$$

yang tepat merupakan persamaan yang dinyatakan. Untuk $x=y$ persamaan itu
adalah ekuivariansi terhadap aksi kanan $\pi_1(X,x)$. Ini menyelesaikan bukti
yang pada sumber hanya ditandai “Exercise”, sekaligus memperbaiki salah eja
*equvariant* dan *path lifing*.
:::

Masih ada dua masalah yang harus dipecahkan:

1. bagaimana membangun, atau membuktikan keberadaan, ruang penutup terhubung
   sederhana dari $X$;
2. setelah ruang itu tersedia, bagaimana membangun aksi serat demi serat
   untuk setiap subgrup $H<\pi_1(X,x_0)$.

Masalah kedua cukup direduksi ke aksi serat demi serat seluruh grup
$G=\pi_1(X,x_0)$, sebab aksi setiap subgrup diperoleh dengan pembatasan.
Ternyata konstruksi yang menyelesaikan masalah pertama sekaligus membawa
aksi kiri $G$ yang diperlukan.

## Konstruksi himpunan kelas lintasan dan topologi basis {#o012-rbt-l16-s03}

::: {.construction #o012-rbt-l16-con-001}
**Konstruksi 16.1 (calon penutup universal).** Ambil ruang bertitik
$(X,x_0)$. Definisikan $\widetilde X$ sebagai himpunan kelas homotopi dengan
titik ujung tetap dari lintasan
$\gamma\colon x_0\rightsquigarrow x$, dengan $x$ boleh berubah. Tuliskan
$[\gamma]$ untuk kelasnya dan

$$
p([\gamma])=\gamma(1).
$$

Kelas lintasan konstan di $x_0$ ditulis $[c_{x_0}]$; sesuai singkatan
sumber, bila tidak menimbulkan kerancuan kelas itu juga ditulis
$c_{x_0}$.

Sebut lingkungan terbuka terhubung lintasan $U\ni x$ **dapat dipakai** bila
pemetaan yang diinduksi inklusi

$$
\pi_1(U,x)\longrightarrow\pi_1(X,x)
$$

trivial. Untuk $[\gamma]\in p^{-1}(x)$ dan lingkungan dapat dipakai $U$,
definisikan

$$
U_{[\gamma]}
:=
\bigl\{
[\gamma\#\eta]\mid
\eta\text{ lintasan di }U,
\ \eta(0)=x
\bigr\}.
$$

Berikan kepada $\widetilde X$ topologi yang basisnya terdiri atas semua
$U_{[\gamma]}$. Ini adalah definisi topologinya; tidak diasumsikan bahwa
topologi tersebut merupakan topologi hasil bagi dari ruang lintasan dengan
topologi kompak-terbuka.
:::

::: {.diagram #o012-rbt-l16-dia-002}
**Diagram 16.2 (kelas lintasan dan titik ujung).** Pada tingkat himpunan
bertitik, data panahnya adalah

$$
(P_{x_0}X,c_{x_0})
\xrightarrow{\ r\ }
(\widetilde X,[c_{x_0}]),
\qquad
(P_{x_0}X,c_{x_0})
\xrightarrow{\ e_1\ }
(X,x_0),
\qquad
(\widetilde X,[c_{x_0}])
\xrightarrow{\ p\ }
(X,x_0),
$$

dengan $r(\gamma)=[\gamma]$ dan $e_1(\gamma)=\gamma(1)$. Persamaan
komutativitasnya ialah

$$
p\circ r=e_1.
$$

Diagram ini belum mengklaim bahwa $r$ kontinu untuk topologi
kompak-terbuka. Kontinuitas $p$ akan mengikuti langsung dari lembaran-lembaran
basis.
:::

Sebagai himpunan, konstruksi itu dapat dibaca sebagai gabungan semua
morfisma grupoid fundamental yang berawal di $x_0$:

$$
\widetilde X
=
\bigsqcup_{x\in X}\Pi_1(X)(x_0,x),
\qquad
p^{-1}(x)=\Pi_1(X)(x_0,x).
$$

Topologi basis di atas mengubah himpunan tersebut menjadi ruang topologis.

::: {.proposition #o012-rbt-l16-prop-002}
**Proposisi 16.2 (penutup universal berbasis kelas lintasan).** Jika $X$
terhubung lintasan dan SLSC dalam konvensi mata kuliah, maka

$$
p\colon(\widetilde X,[c_{x_0}])\longrightarrow(X,x_0)
$$

merupakan ruang penutup terhubung sederhana. Grup
$G=\pi_1(X,x_0)$, yang dipandang sebagai grup diskret, bertindak kontinu,
bebas, dan serat demi serat dari kiri pada $\widetilde X$ melalui prefiks
loop.
:::

::: {.proof #o012-rbt-l16-proof-003}
**Bukti.** Kita membuktikan semua bagian secara berurutan.

**Aksioma basis.** Setiap $[\alpha]\in\widetilde X$ berada dalam
$U_{[\alpha]}$ untuk lingkungan dapat dipakai $U$ dari titik ujungnya,
karena lintasan konstan boleh dipilih sebagai $\eta$. Jika

$$
[\alpha]\in U_{[\gamma]}\cap V_{[\delta]},
$$

pilih lingkungan dapat dipakai $W$ dari $p([\alpha])$ dengan
$W\subseteq U\cap V$; basis lingkungan seperti itu merupakan bagian dari
konvensi SLSC mata kuliah. Menambahkan lintasan di $W$ pada $\alpha$ juga
menambahkan lintasan di $U$ pada wakil yang berasal dari $U_{[\gamma]}$,
dan demikian pula untuk $V$. Jadi

$$
W_{[\alpha]}
\subseteq
U_{[\gamma]}\cap V_{[\delta]}.
$$

Kedua aksioma basis terpenuhi.

**Lembaran lokal.** Tetapkan lingkungan dapat dipakai $U\ni x$. Untuk setiap
$a=[\gamma]\in p^{-1}(x)$, pembatasan

$$
p|_{U_a}\colon U_a\longrightarrow U
$$

surjektif karena $U$ terhubung lintasan. Ia injektif: jika
$p([\gamma\#\eta_1])=p([\gamma\#\eta_2])$, kedua lintasan $\eta_1$ dan
$\eta_2$ berakhir di titik yang sama. Loop
$\eta_1\#\overline{\eta_2}$ berada di $U$ dan kelasnya trivial di $X$.
Maka $[\eta_1]=[\eta_2]$ dalam grupoid fundamental, sehingga
$[\gamma\#\eta_1]=[\gamma\#\eta_2]$.

Pemetaan itu juga homeomorfisma. Memang, jika $O\subseteq U_a$ terbuka dan
$[\alpha]\in O$, aksioma basis memberi lingkungan basis yang memuat
$[\alpha]$ dan termuat dalam $O$. Dengan memperhalusnya sekaligus di dalam
$U$, diperoleh lingkungan dapat dipakai $V$ dari titik ujung $\alpha$
sedemikian sehingga $V_{[\alpha]}\subseteq O$ dan

$$
p(V_{[\alpha]})=V.
$$

Jadi pembatasan bijektif tersebut terbuka. Argumen yang sama menunjukkan
bahwa $p$ kontinu, karena setiap titik di $p^{-1}(O)$, untuk $O$ terbuka,
mempunyai lingkungan basis yang dipetakan ke dalam $O$.

Lembaran-lembaran itu mempartisi seluruh prabayangan:

$$
p^{-1}(U)
=
\bigsqcup_{a\in p^{-1}(x)}U_a.
$$

Untuk keberadaan, jika $[\beta]$ berakhir di $y\in U$, pilih lintasan
$\eta\colon x\rightsquigarrow y$ di $U$; maka
$[\beta]\in U_{[\beta\#\overline\eta]}$. Jika dua lembaran berpotongan,
perbandingan kedua lintasan di $U$ menghasilkan loop yang trivial di $X$,
sehingga kedua pusatnya di atas $x$ sama. Dengan demikian $U$ diliputi
secara merata. Jika $a(b)$ menandai satu-satunya pusat lembaran yang memuat
$b\in p^{-1}(U)$, trivialiasi lokal yang bertipe lengkap ialah

$$
\begin{aligned}
\Theta_U\colon p^{-1}(U)&\xrightarrow{\ \cong\ }U\times p^{-1}(x),\\
b&\longmapsto\bigl(p(b),a(b)\bigr).
\end{aligned}
$$

Inversnya mengirim $(y,a)$ ke satu-satunya titik lembaran $U_a$ di atas $y$.
Konstruksi ini memakai lembaran basis, bukan pemilih lintasan kontinu
$x'\mapsto\eta_{x'}$. Secara khusus,
$U_a\cap p^{-1}(x)=\{a\}$, sehingga setiap serat $p^{-1}(x)$ diskret.

Pada tempat ini sumber mengarahkan pembaca ke [halaman 64--65 buku
Hatcher](https://pi.math.cornell.edu/~hatcher/AT/AT%2B.pdf) dan mencatat
bahwa perincian akan ditambahkan kemudian serta tidak termasuk materi ujian
kuliah asal. Argumen di atas memberikan perincian itu secara mandiri dan
tidak mengidentifikasi topologi basis ini dengan topologi hasil bagi
kompak-terbuka.

**Keterhubungan lintasan.** Bagi lintasan
$\gamma\colon x_0\rightsquigarrow x$, definisikan

$$
\Gamma_\gamma(s)=[\gamma_s],
\qquad
\gamma_s(t)=\gamma(st).
$$

Ini memindahkan rumus yang diletakkan sumber di pinggir ke urutan bacaan
utama. Peta $\Gamma_\gamma$ kontinu. Untuk melihatnya di $s_0$, mulai dari
sebarang lingkungan basis yang memuat $[\gamma_{s_0}]$ dan perhalus menjadi
$U_{[\gamma_{s_0}]}$ yang masih termuat di dalamnya. Kontinuitas $\gamma$
memberi interval $J$ dari $s_0$ sehingga $\gamma(J)\subseteq U$. Bagi
$s\in J$, segmen

$$
\eta_s(t)=\gamma((1-t)s_0+ts)
$$

berada di $U$, dan setelah menghapus atau menambahkan penelusuran balik,
$[\gamma_s]=[\gamma_{s_0}\#\eta_s]$. Maka
$\Gamma_\gamma(J)\subseteq U_{[\gamma_{s_0}]}$. Karena
$\Gamma_\gamma(0)=[c_{x_0}]$ dan
$\Gamma_\gamma(1)=[\gamma]$, setiap titik dapat dihubungkan dengan titik
basis; jadi $\widetilde X$ terhubung lintasan.

**Aksi kiri.** Jika $h=[\omega]\in G$, definisikan

$$
h\cdot[\gamma]:=[\omega\#\gamma].
$$

Rumus ini terdefinisi baik dan serat demi serat. Untuk setiap himpunan
basis,

$$
h\cdot U_{[\gamma]}=U_{[\omega\#\gamma]},
$$

sehingga setiap translasi kiri adalah homeomorfisma, dengan invers
translasi oleh $h^{-1}$. Karena $G$ diskret, aksi gabungan
$G\times\widetilde X\to\widetilde X$ kontinu. Asosiativitas mengikuti dari
asosiativitas komposisi dalam $\Pi_1(X)$. Jika
$h\cdot[\gamma]=[\gamma]$, menggabungkan $[\overline\gamma]$ di kanan
memberi $h=1$; jadi aksi kiri itu bebas.

Aksi ini berbeda dari monodromi kanan. Untuk
$[\eta\colon x\rightsquigarrow y]$, pengangkatan dari $[\gamma]$ berakhir
di

$$
[\gamma]\cdot[\eta]=[\gamma\#\eta].
$$

Kedua aksi saling komutatif karena

$$
h\cdot\bigl([\gamma]\cdot[\eta]\bigr)
=[\omega\#\gamma\#\eta]
=\bigl(h\cdot[\gamma]\bigr)\cdot[\eta].
$$

**Keterhubungan sederhana.** Untuk lintasan
$\alpha\colon[0,1]\to X$ yang mulai di $x_0$, rumus

$$
\widetilde\alpha(t)=[\alpha_t],
\qquad
\alpha_t(s)=\alpha(ts),
$$

memberi pengangkatannya yang mulai di $[c_{x_0}]$; kontinuitasnya adalah
argumen lembaran basis yang sama seperti untuk $\Gamma_\gamma$. Sekarang ambil
loop $\lambda$ di $(\widetilde X,[c_{x_0}])$ dan letakkan
$\alpha=p\circ\lambda$. Karena $\lambda$ dan $\widetilde\alpha$ merupakan
dua pengangkatan $\alpha$ dengan titik awal yang sama, keunikan pengangkatan
memberi $\lambda=\widetilde\alpha$. Loop $\lambda$ tertutup, maka

$$
[\alpha]=\widetilde\alpha(1)=[c_{x_0}].
$$

Dengan kata lain, kriteria pengangkatan tertutup menyatakan bahwa hanya kelas
loop trivial pada $X$ yang mempunyai pengangkatan tertutup dari
$[c_{x_0}]$. Jadi citra

$$
p_*\colon
\pi_1(\widetilde X,[c_{x_0}])
\longrightarrow
\pi_1(X,x_0)
$$

trivial. Pemetaan $p_*$ injektif untuk suatu ruang penutup, menurut teorema
pengangkatan yang telah dibuktikan sebelumnya. Karena itu
$\pi_1(\widetilde X,[c_{x_0}])$ trivial. Bersama keterhubungan lintasan di
atas, $\widetilde X$ terhubung sederhana. Bukti ini tidak menyamakan aksi
kiri bebas dengan penstabil monodromi kanan.
:::

## Realisasi subgrup dan semua representasi {#o012-rbt-l16-s04}

Ambil kembali $G=\pi_1(X,x_0)$ dan subgrup $H\leq G$. Batasi aksi kiri pada
Proposisi 16.2 ke $H$. Proposisi 16.1 menghasilkan ruang penutup bertitik

$$
p_H\colon
(H\backslash\widetilde X,H[c_{x_0}])
\longrightarrow
(X,x_0).
$$

Ruang totalnya terhubung lintasan karena merupakan citra kontinu ruang
terhubung lintasan $\widetilde X$ di bawah peta hasil bagi.

::: {.corollary #o012-rbt-l16-cor-001}
**Akibat 16.1 (realisasi subgrup).** Untuk penutup bertitik di atas,

$$
(p_H)_*\pi_1
(H\backslash\widetilde X,H[c_{x_0}])
=H
\leq G.
$$
:::

::: {.proof #o012-rbt-l16-proof-004}
**Bukti.** Bagi $g=[\omega]\in G$, pengangkatan loop $\omega$ melalui
$p_H$ yang mulai di $H[c_{x_0}]$ ialah

$$
t\longmapsto H[\omega_t],
\qquad
\omega_t(s)=\omega(ts).
$$

Titik akhirnya $H[\omega]$. Menurut kriteria pengangkatan tertutup,
$g$ berada dalam citra $(p_H)_*$ tepat ketika

$$
H[\omega]=H[c_{x_0}],
$$

dan persamaan koset ini berlaku tepat ketika $g\in H$. Jadi citra itu
persis $H$. Ruang $\widetilde X$ sendiri tetap mempunyai grup fundamental
trivial; inilah koreksi terhadap persamaan salah pada baris 3374 sumber.
:::

Konstruksi tersebut juga menyelesaikan masalah objek umum. Misalkan mula-mula
$X$ terhubung lintasan dan $S$ suatu himpunan dengan aksi kanan $G$. Uraikan
$S$ menjadi orbit dan pilih satu wakil dalam setiap orbit:

$$
S=\bigsqcup_{i\in I}S_i,
\qquad
s_i\in S_i,
\qquad
H_i:=\operatorname{Stab}_G(s_i).
$$

Bangun ruang penutup

$$
Z_S:=\bigsqcup_{i\in I}H_i\backslash\widetilde X
\longrightarrow X.
$$

Jika $S=\varnothing$, maka $I=\varnothing$ dan $Z_S=\varnothing$; ini
tetap ruang penutup menurut konvensi sumber, yang mengizinkan serat kosong.

Seratnya di atas $x_0$ ialah
$\bigsqcup_iH_i\backslash G$, dan pemetaan

$$
\begin{aligned}
\Phi\colon\bigsqcup_{i\in I}H_i\backslash G
&\longrightarrow S,\\
H_i g&\longmapsto s_i\cdot g
\end{aligned}
$$

terdefinisi baik, bijektif pada setiap orbit, dan ekuivarian kanan. Memang,
$H_i g'=H_i g$ berarti $g'=hg$ untuk suatu $h\in H_i$, sehingga
$s_i\cdot g'=s_i\cdot g$. Sebaliknya, kesamaan kedua nilai menunjukkan
$g'g^{-1}\in H_i$, dan sifat ekuivariannya mengikuti dari
$\Phi(H_i gk)=s_i\cdot(gk)$.

Jika $F\colon\Pi_1(X)\to\mathbf{Set}$ representasi yang diberikan, ambil
$S=F(x_0)$ dengan aksi kanan $s\cdot g:=F(g)(s)$ dalam konvensi komposisi
kronologis unit ini. Tuliskan $M$ untuk monodromi $Z_S$. Isomorfisma $\Phi$
pada titik basis meluas melalui transpor lintasan: untuk pilihan
$\alpha\colon x_0\rightsquigarrow x$, definisikan

$$
\Phi_x
:=
F(\alpha)\circ\Phi\circ M(\overline\alpha)
\colon (Z_S)_x\longrightarrow F(x).
$$

Rumus ini tidak bergantung pada $\alpha$. Memang, jika
$\beta\colon x_0\rightsquigarrow x$ pilihan lain dan
$g=[\beta\#\overline\alpha]\in G$, maka

$$
M(\overline\alpha)=M(g)\circ M(\overline\beta),
\qquad
F(\alpha)=F(\beta)\circ F(g)^{-1}.
$$

Ekuivariansi $\Phi\circ M(g)=F(g)\circ\Phi$ membuat kedua rumus untuk
$\Phi_x$ sama. Jika $[\eta\colon x\rightsquigarrow y]$ diberikan, gunakan
$\alpha\#\eta$ sebagai pilihan lintasan menuju $y$; langsung diperoleh
$\Phi_y\circ M(\eta)=F(\eta)\circ\Phi_x$. Jadi $(\Phi_x)_x$ adalah
isomorfisma natural antara monodromi $Z_S$ dan $F$.

Bila $X$ tidak terhubung, konvensi SLSC menjamin bahwa setiap komponen
lintasannya $X_j$ terbuka. Untuk setiap $j$, pilih titik basis
$x_j\in X_j$, uraikan **secara independen** himpunan
$F(x_j)$ menjadi orbit di bawah $\pi_1(X_j,x_j)$, dan lakukan konstruksi di
atas pada $X_j$. Gabungan saling lepas semua ruang penutup komponen adalah
ruang penutup dari $X$, dan isomorfisma natural komponen demi komponen
bergabung menjadi isomorfisma representasi seluruh grupoid fundamental.

::: {.proposition #o012-rbt-l16-prop-003}
**Proposisi 16.3 (surjektivitas esensial monodromi).** Jika $X$ SLSC dalam
konvensi mata kuliah, fungtor monodromi

$$
\operatorname{Cov}_X
\longrightarrow
[\Pi_1(X),\mathbf{Set}]
$$

surjektif secara esensial: setiap representasi
$\Pi_1(X)\to\mathbf{Set}$ isomorfik dengan representasi yang berasal dari
suatu ruang penutup.
:::

::: {.note #o012-rbt-l16-note-001 data-origin="edition-original"}
**Batas hasil.** Proposisi 16.3 hanya menyelesaikan keberadaan **objek**
hingga isomorfisma. Belum dibuktikan bahwa setiap pemetaan ekuivarian serat
berasal dari suatu pemetaan ruang penutup, ataupun bahwa pemetaan tersebut
unik. Dengan demikian, kepenuhan, kesetiaan, dan ekuivalensi kategori tidak
diklaim pada batas Unit 16.
:::

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l16-mastery}

Enam pemeriksaan berikut merupakan materi asli edisi. Pemeriksaan itu
menutup tepat enam kewajiban pembuktian unit ini: hasil bagi lokal, dua aksi
yang saling komutatif, topologi basis, pengangkatan dan keterhubungan
sederhana, realisasi subgrup, serta realisasi orbit demi orbit dan komponen
demi komponen. Tidak ada pemeriksaan yang memakai hasil klasifikasi
transformasi dek atau kepenuhan-setiaan dari kuliah sesudahnya.

::: {.exercise #o012-rbt-l16-mcheck-001 data-origin="edition-original"}
**Pemeriksaan penguasaan 16.1 (hasil bagi suatu penutup).** Misalkan grup
diskret $K$ bertindak kontinu dari kiri dan serat demi serat pada ruang
penutup $p\colon Z\to X$, dengan $X$ SLSC dalam konvensi mata kuliah.
Buktikan langsung bahwa
$K\backslash Z\to X$ merupakan ruang penutup. Dalam bukti Anda, jelaskan
mengapa elemen $K$ mempermutasikan lembaran utuh dan mengapa topologi hasil
bagi membatasi dengan benar di atas lingkungan yang diliputi secara merata.
:::

## Solusi Pemeriksaan 16.1 {#o012-rbt-l16-sol-001}

Pilih $x\in X$ dan lingkungan terbuka terhubung lintasan $U\ni x$ yang
diliputi secara merata. Jika $V$ satu lembaran di atas $U$, maka $kV$
terhubung lintasan, termuat dalam $p^{-1}(U)$, dan karena
$p(kz)=p(z)$, peta $kV\to U$ masih surjektif. Himpunan terhubung itu termuat
dalam satu lembaran $V'$. Menerapkan $k^{-1}$ menunjukkan $kV=V'$. Jadi setiap
$k$ mempermutasikan lembaran-lembaran utuh.

Dengan $F=p^{-1}(x)$, trivialiasi menurut lembaran memberi

$$
p^{-1}(U)\cong U\times F,
\qquad
k(u,f)=(u,kf).
$$

Peta hasil bagi $q\colon Z\to K\backslash Z$ terbuka karena

$$
q^{-1}(q(O))=\bigcup_{k\in K}kO
$$

terbuka untuk setiap $O$ terbuka. Selain itu, $p^{-1}(U)$ jenuh: sebuah orbit
yang bertemu $p^{-1}(U)$ seluruhnya berada di atas titik-titik $U$. Maka
pembatasan $q|_{p^{-1}(U)}$ adalah peta hasil bagi ke prabayangan $U$ dalam
$K\backslash Z$. Dengan demikian

$$
(K\backslash Z)_U
\cong K\backslash(U\times F)
\cong U\times(K\backslash F).
$$

Himpunan $K\backslash F$ diskret, sehingga ruas kanan merupakan gabungan
saling lepas salinan $U$. Jadi setiap $x$ mempunyai lingkungan yang diliputi
secara merata dan $K\backslash Z\to X$ adalah ruang penutup.

::: {.exercise #o012-rbt-l16-mcheck-002 data-origin="edition-original"}
**Pemeriksaan penguasaan 16.2 (hasil bagi kiri dan monodromi kanan).** Pada
$\widetilde X$, tuliskan aksi kiri $G=\pi_1(X,x_0)$ dan transpor kanan
sepanjang $[\eta\colon x\rightsquigarrow y]$. Buktikan bahwa keduanya
komutatif. Lalu buktikan bahwa, bagi $H\leq G$, peta serat

$$
q_x\colon\widetilde X_x\to(H\backslash\widetilde X)_x
$$

komutatif dengan transpor kanan.
:::

## Solusi Pemeriksaan 16.2 {#o012-rbt-l16-sol-002}

Jika $h=[\omega]$ diwakili loop pada $x_0$ dan
$[\gamma]\in\widetilde X_x$, rumus aksi kirinya

$$
h\cdot[\gamma]=[\omega\#\gamma].
$$

Transpor kanan sepanjang $\eta$ ialah

$$
[\gamma]\cdot[\eta]=[\gamma\#\eta].
$$

Asosiativitas dalam grupoid fundamental memberi

$$
h\cdot([\gamma]\cdot[\eta])
=[\omega\#\gamma\#\eta]
=(h\cdot[\gamma])\cdot[\eta].
$$

Jadi aksi prefiks kiri tidak boleh disamakan dengan monodromi sufiks kanan,
namun kedua operator itu komutatif.

Peta hasil bagi adalah $q_x([\gamma])=H[\gamma]$. Karena rumus di atas,

$$
\begin{aligned}
q_y([\gamma]\cdot[\eta])
&=H[\gamma\#\eta]\\
&=(H[\gamma])\cdot[\eta]\\
&=q_x([\gamma])\cdot[\eta].
\end{aligned}
$$

Rumus itu juga menunjukkan bahwa pada serat titik basis aksi yang turun
adalah $(Hg)\cdot k=H(gk)$ pada $H\backslash G$.

::: {.exercise #o012-rbt-l16-mcheck-003 data-origin="edition-original"}
**Pemeriksaan penguasaan 16.3 (basis dan lembaran tanpa pemilih lintasan).**
Untuk himpunan kelas lintasan $\widetilde X$, buktikan bahwa semua
$U_{[\gamma]}$ membentuk basis. Buktikan pula bahwa, untuk lingkungan dapat
dipakai $U\ni x$,

$$
p^{-1}(U)=\bigsqcup_{a\in p^{-1}(x)}U_a
$$

dan setiap $p|_{U_a}$ merupakan homeomorfisma ke $U$. Jangan memilih
keluarga lintasan $x'\mapsto\eta_{x'}$ yang diasumsikan kontinu.
:::

## Solusi Pemeriksaan 16.3 {#o012-rbt-l16-sol-003}

Kelas $[\alpha]$ berada dalam $U_{[\alpha]}$ melalui lintasan konstan di
titik ujungnya. Jika $[\alpha]$ berada dalam dua himpunan basis calon,
pilih lingkungan dapat dipakai $W$ dari titik ujung $\alpha$ yang termuat
dalam irisan kedua lingkungan dasar. Setiap ekstensi $\alpha$ oleh lintasan
di $W$ juga merupakan ekstensi melalui masing-masing lingkungan lama, jadi
$W_{[\alpha]}$ termuat dalam irisan. Ini membuktikan kedua aksioma basis.

Tetapkan $a=[\gamma]\in p^{-1}(x)$. Karena $U$ terhubung lintasan, setiap
$y\in U$ dapat dicapai oleh lintasan $\eta$ di $U$, dan
$[\gamma\#\eta]\in U_a$ terletak di atas $y$. Jadi pembatasan $p|_{U_a}$
surjektif. Jika dua unsur $[\gamma\#\eta_1]$ dan
$[\gamma\#\eta_2]$ dipetakan ke titik $y$ yang sama, loop
$\eta_1\#\overline{\eta_2}$ berada di $U$ dan karenanya trivial di $X$.
Jadi $[\eta_1]=[\eta_2]$ dan kedua unsur tadi sama. Maka pembatasan tersebut
bijektif.

Jika $O\subseteq U_a$ terbuka dan $[\alpha]\in O$, perhalus suatu
lingkungan basis di dalam $O$ menjadi $V_{[\alpha]}\subseteq O$ dengan
$V\subseteq U$ dapat dipakai. Himpunan itu dipetakan bijektif ke $V$. Maka
$p(O)$ terbuka sebagai gabungan lingkungan-lingkungan $V$, sehingga
$p|_{U_a}$ terbuka dan merupakan homeomorfisma.

Untuk menunjukkan bahwa lembaran-lembaran menutupi $p^{-1}(U)$, ambil
$[\beta]$ di atas $y\in U$ dan lintasan $\eta\colon x\rightsquigarrow y$
dalam $U$. Lalu $[\beta]$ berada pada lembaran yang pusatnya
$[\beta\#\overline\eta]$ di atas $x$. Jika dua lembaran bertemu, lintasan
dalam $U$ dari kedua pusat ke titik temu berbeda hanya dengan loop di $U$;
loop itu trivial di $X$, sehingga pusatnya sama. Jadi gabungan itu saling
lepas. Seluruh argumen hanya menggunakan lintasan satu per satu dan tidak
mendalilkan pemilih lintasan kontinu.

::: {.exercise #o012-rbt-l16-mcheck-004 data-origin="edition-original"}
**Pemeriksaan penguasaan 16.4 (pengangkatan dan keterhubungan sederhana).**
Bagi lintasan $\alpha\colon x\rightsquigarrow y$ dan
$a=[\gamma]\in\widetilde X_x$, berikan rumus pengangkatan yang mulai di
$a$ dan buktikan kontinuitasnya dari basis. Gunakan rumus itu untuk
membuktikan bahwa $\widetilde X$ terhubung lintasan dan terhubung sederhana.
:::

## Solusi Pemeriksaan 16.4 {#o012-rbt-l16-sol-004}

Tuliskan $\alpha_t(s)=\alpha(ts)$. Pengangkatan yang dicari ialah

$$
\widetilde\alpha_a(t)
=[\gamma\#\alpha_t].
$$

Jelas $p(\widetilde\alpha_a(t))=\alpha(t)$ dan nilai awalnya $a$. Untuk
kontinuitas di $t_0$, ambil sebarang lingkungan basis dari
$[\gamma\#\alpha_{t_0}]$ dan perhalus menjadi
$U_{[\gamma\#\alpha_{t_0}]}$ di dalamnya. Pada interval kecil $J$ sekitar
$t_0$, citra $\alpha(J)$ termuat di $U$. Segmen $\alpha$ dari $t_0$ ke $t$
berada dalam $U$, dan setelah reparametrisasi serta menghapus penelusuran balik,
$[\gamma\#\alpha_t]$ diperoleh dengan menambahkan segmen itu pada
$[\gamma\#\alpha_{t_0}]$. Maka citra $J$ berada dalam satu lingkungan basis.

Untuk keterhubungan lintasan, ambil $[\gamma]\in\widetilde X$ dan gunakan
$t\mapsto[\gamma_t]$. Peta ini kontinu menurut argumen yang baru diberikan,
mulai di $[c_{x_0}]$, dan berakhir di $[\gamma]$.

Untuk keterhubungan sederhana, ambil loop $\lambda$ di
$[c_{x_0}]$ dan proyeksikan menjadi $\alpha=p\circ\lambda$. Keunikan
pengangkatan menjadikan $\lambda(t)=[\alpha_t]$. Karena $\lambda(1)$ kembali
ke $[c_{x_0}]$, kelas $[\alpha]$ trivial. Jadi
$p_*[\lambda]=1$ bagi setiap $[\lambda]$. Pemetaan $p_*$ injektif untuk
ruang penutup, sehingga $[\lambda]=1$. Bersama keterhubungan lintasan,
kesimpulannya $\widetilde X$ terhubung sederhana.

::: {.exercise #o012-rbt-l16-mcheck-005 data-origin="edition-original"}
**Pemeriksaan penguasaan 16.5 (realisasi subgrup).** Untuk $H\leq G$, buktikan
bahwa $H\backslash\widetilde X\to X$ terhubung dan bahwa citra grup
fundamentalnya di $G$ tepat $H$. Jelaskan mengapa kesimpulan itu bukan
$\pi_1(\widetilde X)=H$.
:::

## Solusi Pemeriksaan 16.5 {#o012-rbt-l16-sol-005}

Peta hasil bagi kontinu dan surjektif, sedangkan $\widetilde X$ terhubung
lintasan. Citra lintasan yang menghubungkan dua wakil menghubungkan kelas
orbitnya, sehingga $H\backslash\widetilde X$ terhubung lintasan.

Ambil $g=[\omega]\in G$. Pengangkatan loop $\omega$ ke penutup hasil bagi
dari titik $H[c_{x_0}]$ ialah $t\mapsto H[\omega_t]$, dengan titik akhir
$H[\omega]$. Pengangkatan itu tertutup tepat ketika

$$
H[\omega]=H[c_{x_0}],
$$

yakni tepat ketika $g\in H$. Kriteria pengangkatan tertutup menyatakan bahwa
loop basis berada dalam citra $(p_H)_*$ tepat ketika pengangkatannya dari
titik basis tertutup. Oleh karena itu

$$
(p_H)_*\pi_1(H\backslash\widetilde X,H[c_{x_0}])=H.
$$

Di pihak lain, $\widetilde X$ adalah penutup universal yang baru dibuktikan
terhubung sederhana, sehingga $\pi_1(\widetilde X,[c_{x_0}])=1$. Grup $H$
muncul sebagai citra grup fundamental **ruang hasil bagi**, bukan sebagai
grup fundamental penutup universal itu sendiri.

::: {.exercise #o012-rbt-l16-mcheck-006 data-origin="edition-original"}
**Pemeriksaan penguasaan 16.6 (realisasi orbit dan komponen).** Misalkan
$F\colon\Pi_1(X)\to\mathbf{Set}$ dan $X$ SLSC dalam konvensi mata kuliah.
Bangun ruang penutup yang monodrominya isomorfik dengan $F$: pertama untuk
satu komponen lintasan, lalu untuk semua komponen. Buktikan secara langsung
bahwa pemetaan serat pada titik basis terdefinisi baik, bijektif, dan
ekuivarian.
:::

## Solusi Pemeriksaan 16.6 {#o012-rbt-l16-sol-006}

Mula-mula andaikan $X$ terhubung lintasan dan pilih $x_0$. Letakkan
$G=\pi_1(X,x_0)$ dan $S=F(x_0)$. Uraikan $S$ menjadi orbit kanan,

$$
S=\bigsqcup_{i\in I}S_i,
$$

pilih $s_i\in S_i$, dan letakkan
$H_i=\operatorname{Stab}_G(s_i)$. Bentuk

$$
Z=\bigsqcup_{i\in I}H_i\backslash\widetilde X
\longrightarrow X.
$$

Untuk $S=\varnothing$, koproduk ini kosong dan tetap merupakan ruang penutup
menurut konvensi serat kosong edisi.

Pada serat di $x_0$, definisikan

$$
\Phi(H_i g)=s_i\cdot g.
$$

Jika $H_i g'=H_i g$, maka $g'=hg$ untuk $h\in H_i$, sehingga
$s_i\cdot g'=(s_i\cdot h)\cdot g=s_i\cdot g$; jadi $\Phi$ terdefinisi baik.
Setiap unsur orbit $S_i$ berbentuk $s_i\cdot g$, sehingga peta surjektif.
Jika $s_i\cdot g'=s_i\cdot g$, maka $g'g^{-1}\in H_i$, sehingga
$H_i g'=H_i g$; orbit yang berbeda juga saling lepas. Jadi peta injektif.
Terakhir,

$$
\Phi((H_i g)\cdot k)
=\Phi(H_i gk)
=s_i\cdot(gk)
=(s_i\cdot g)\cdot k,
$$

maka $\Phi$ ekuivarian kanan. Transpor dari $x_0$ ke setiap $x$ memperluas
$\Phi$ menjadi isomorfisma natural monodromi $Z$ dengan $F$; independensi
pilihan lintasan tepat merupakan ekuivariansi yang baru dibuktikan.

Untuk $X$ umum, tuliskan
$X=\bigsqcup_{j\in J}X_j$ sebagai gabungan komponen lintasan terbuka. Pilih
$x_j\in X_j$, terapkan konstruksi tadi secara terpisah pada
$F|_{\Pi_1(X_j)}$, dan peroleh $Z_j\to X_j$. Maka

$$
\bigsqcup_{j\in J}Z_j
\longrightarrow
\bigsqcup_{j\in J}X_j=X
$$

adalah ruang penutup. Isomorfisma natural pada setiap komponen bergabung
karena tidak ada morfisma grupoid fundamental di antara dua komponen
lintasan yang berbeda. Monodromi ruang penutup ini isomorfik dengan $F$.
Argumen membuktikan surjektivitas esensial saja; tidak ada klaim tentang
morfisma antarpenutup.
