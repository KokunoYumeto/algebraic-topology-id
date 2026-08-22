---
title: "Topologi Aljabar"
subtitle: "Unit 12: Menuntaskan Seifert–van Kampen, Retrak, dan Versi Grup"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi di bawah."
---

# Tentang unit ini {.unnumbered #o012-rbt-l12-notice}

Unit ini merupakan terjemahan dan adaptasi bahasa Indonesia atas *Algebraic
Topology* karya David Michael Roberts (2019), tepatnya [Notes.tex baris
2495--2726 pada commit
b947ad2e9f9e301bfe24590a9db653bc54fa1a53](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/blob/b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex#L2495-L2726).
Rentang itu dimulai dengan penanda Kuliah 12 dan kelanjutan bukti teorema
Seifert--van Kampen dari Unit 11. Rentang berakhir setelah penjelasan mengapa
sampul dua kutub tidak memenuhi hipotesis versi grup ketika $n=1$. Baris 2727
memulai Kuliah 13 dan tidak termasuk dalam unit ini. Karya sumber tersedia di
bawah [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/).

Perubahan pada unit ini meliputi penerjemahan, pemformatan ulang agar mudah
dibaca, dan pemberian pengenal stabil. Keenam unsur pinggir dipindahkan ke
urutan bacaan utama. Ketujuh gambar sumber---satu gambar TikZ dan enam diagram
Xy-pic---ditulis ulang sebagai diagram semantik, daftar panah, dan persamaan
komutativitas yang tetap bermakna tanpa bergantung pada posisi visual.

Beberapa rincian matematis diperbaiki atau dilengkapi secara independen.
Argumen kisi pada bukti Seifert--van Kampen dibuat tak melingkar dengan
pertukaran satu sel, lalu penurunan fungsi sementara
$\widetilde K_1$ ke $K_1$, hukum identitas dan komposisi, pembatasan ke $F$
serta $G$, dan keunikan funktor universal $K$ diperiksa secara eksplisit.
Dalam bukti versi relatif, pilihan jalur dibuat sebagai satu keluarga koheren
dengan mendahulukan $U\cap V$; pilihan terpisah di $U$ dan $V$ tidak dengan
sendirinya bersepakat pada irisan. Rumus funktor retraksi ditulis dengan jalur
balik yang diperlukan. Klaim sumber bahwa empat retraksi simpul saja sudah
cukup diperketat: keempat retraksi harus merupakan komponen dari satu morfisme
balik di $\mathcal C^\square$. Dalam lemma subkategori penuh, peran kategori
ambient dan subkategori yang tertukar dalam sumber dikembalikan ke arah yang
bertipe benar. Funktor $\mathbf B$ dinyatakan sepenuhnya setia ke citra esensial
grupoid satu objek, alih-alih diperlakukan sebagai inklusi harfiah tanpa
identifikasi itu. Salah eja “homopic” dan “one-obect” juga dinormalkan.

Sumber menyerahkan satu bukti sebagai latihan. Pendamping penguasaan yang
dibatasi pada empat pemeriksaan memberikan solusi lengkap bagi latihan itu
serta keterampilan inti unit: pertukaran sel dan keunikan funktor universal,
retraksi persegi pushout, retraksi grupoid fundamental dan koherensi kubus,
serta peralihan dari grupoid ke grup pada contoh sfera. Seluruh materi
pendamping yang ditambahkan tersedia di bawah CC BY 4.0. Edisi ini bersifat
independen dan tidak menyiratkan dukungan atau pengesahan dari penulis sumber.

# Kuliah 12 {#o012-rbt-l12}

## Menuntaskan bukti Seifert--van Kampen {#o012-rbt-l12-s01}

::: {.proof #o012-rbt-l12-proof-001}
**Bukti Teorema 11.1 (lanjutan dan penutup).** Ingat data dari Unit 11:
$H\colon I^2\to X$ adalah homotopi yang mempertahankan titik ujung dari
lintasan $\gamma$ ke lintasan $\eta$. Dengan koordinat $(s,t)$ pada $I^2$,

$$
H(s,0)=\gamma(s),
\qquad
H(s,1)=\eta(s),
$$

dan terdapat $x,y\in X$ sedemikian sehingga

$$
H(0,t)=x,
\qquad
H(1,t)=y
$$

untuk semua $t\in I$; dua persamaan sebelumnya berlaku untuk semua
$s\in I$. Semua homotopi yang digunakan di bawah ini
mempertahankan kedua titik ujung tersebut.

Terapkan lema bilangan Lebesgue pada ruang metrik kompak

$$
(I^2,d_\infty),
\qquad
d_\infty\bigl((s,t),(s',t')\bigr)
=
\max\{|s-s'|,|t-t'|\},
$$

dan sampul terbuka

$$
\{H^{-1}(U^\circ),H^{-1}(V^\circ)\}.
$$

Kita memperoleh $\delta>0$ sehingga setiap persegi kecil dengan panjang sisi
kurang dari $\delta$ termuat dalam salah satu dari
$H^{-1}(U^\circ)$ atau $H^{-1}(V^\circ)$. Pilih $N\geq1$ dengan
$1/N<\delta$, lalu gunakan garis-garis kisi $s=i/N$ dan $t=j/N$. Untuk setiap
sel $Q$ pada kisi itu, pembatasan

$$
H|_Q
$$

berfaktor melalui $U$ atau melalui $V$. Titik-titik kisi pada sisi bawah dan
atas sekaligus memberi partisi $I$ yang subordinat bagi $\gamma$ dan $\eta$,
sehingga nilai sementara $\widetilde K_1(\gamma)$ dan
$\widetilde K_1(\eta)$ dapat dibaca dari ruas-ruas kisi.

::: {.figure #o012-rbt-l12-fig-001}
**Diagram 12.1 (kisi Lebesgue dan pertukaran satu sel).** Persegi parameter
mempunyai sisi bawah $\gamma$, sisi atas $\eta$, dan kedua sisi tegak yang
dipetakan secara konstan ke $x$ dan $y$. Persegi itu dibagi menjadi sel-sel
yang masing-masing mempunyai panjang sisi kurang dari $\delta$ dan dipetakan
seluruhnya ke $U$ atau seluruhnya ke $V$.

Gambar sumber memakai skala $[0,3]^2$ dengan kisi $6\times6$. Rute tangga
merah utuh melewati simpul, dalam urutan tempuh,

$$
\begin{aligned}
&(0,0),(1,0),(1,\tfrac32),(\tfrac32,\tfrac32),
(\tfrac32,2),\\
&(\tfrac52,2),(\tfrac52,\tfrac52),(3,\tfrac52),(3,3).
\end{aligned}
$$

Pada satu sel, ruas

$$
(1,\tfrac32)\longrightarrow
(\tfrac32,\tfrac32)\longrightarrow
(\tfrac32,2)
$$

dapat diganti dengan rute bertitik

$$
(1,\tfrac32)\longrightarrow
(1,2)\longrightarrow
(\tfrac32,2).
$$

Membagi semua koordinat dengan $3$ menempatkan gambar itu di $I^2$. Kedua
rute kecil adalah rute “bawah lalu kanan” dan “kiri lalu atas” pada sel yang
sama; inilah satu langkah pertukaran sel.
:::

Pertimbangkan semua lintasan tangga monoton pada kisi dari sudut kiri bawah
ke sudut kanan atas. Dua lintasan yang hanya berbeda pada satu sel mempunyai
bentuk yang sama di luar sel itu. Di dalam sel, satu lintasan menempuh sisi
bawah lalu sisi kanan, sedangkan yang lain menempuh sisi kiri lalu sisi atas.
Karena citra sel berada seluruhnya dalam $U$ atau seluruhnya dalam $V$, hasil
pemanasan pada akhir Unit 11 memberi kesamaan nilai $\widetilde K_1$ bagi dua
ruas kecil tersebut. Mengalikan kesamaan itu di sebelah kiri dan kanan dengan
nilai ruas-ruas yang sama di luar sel menunjukkan bahwa pertukaran satu sel
tidak mengubah nilai seluruh lintasan tangga.

Dengan sejumlah berhingga pertukaran satu sel, rute yang menyusuri sisi bawah
lalu sisi kanan dapat diubah menjadi rute yang menyusuri sisi kiri lalu sisi
atas. Setelah diterapkan $H$, sisi kanan adalah lintasan konstan di $y$ dan
sisi kiri adalah lintasan konstan di $x$. Hukum identitas lokal dan
kemandirian terhadap subdivisi karena itu memberi

$$
\begin{aligned}
\widetilde K_1(\gamma)
&=
\widetilde K_1(\gamma)\,1_{K_0(y)}\\
&=
1_{K_0(x)}\,\widetilde K_1(\eta)\\
&=
\widetilde K_1(\eta).
\end{aligned}
$$

Argumen ini berlaku bagi setiap homotopi berujung tetap $H$. Jadi
$\widetilde K_1$ invarian terhadap homotopi berujung tetap pada seluruh $X$,
bukan hanya pada lintasan yang berada dalam satu anggota sampul.

### Penurunan ke kelas homotopi {#o012-rbt-l12-proof-descent}

Sekarang definisikan

$$
K_1([\alpha]_X)
:=
\widetilde K_1(\alpha).
$$

Invariansi yang baru dibuktikan memastikan bahwa ruas kanan tidak bergantung
pada wakil $\alpha$. Pemeriksaan sumber dan sasaran dari Unit 11 memberi

$$
K_1([\alpha])\colon K_0(\alpha(0))\longrightarrow K_0(\alpha(1)).
$$

Untuk lintasan konstan $c_x$, definisi lokal memberi

$$
K_1([c_x])=1_{K_0(x)}.
$$

Jika $\alpha\colon x\rightsquigarrow y$ dan
$\beta\colon y\rightsquigarrow z$, gabungkan partisi subordinat bagi
$\alpha$ dan $\beta$ menjadi partisi subordinat bagi konkatenasi
$\alpha\#\beta$. Kemandirian dari partisi kemudian memberi

$$
K_1([\alpha][\beta])
=
K_1([\alpha])K_1([\beta]).
$$

Pada persamaan ini penjajaran aljabar dibaca dari kiri ke kanan: $\alpha$
ditempuh lebih dahulu, kemudian $\beta$. Dengan notasi komposisi kategoris
standar yang dibaca dari kanan ke kiri, persamaan yang sama adalah

$$
K_1([\beta]\circ[\alpha])
=
K_1([\beta])\circ K_1([\alpha]).
$$

Maka pasangan $K=(K_0,K_1)$ adalah funktor

$$
K\colon\Pi_1(X)\longrightarrow\Gamma.
$$

### Pembatasan dan keunikan {#o012-rbt-l12-proof-universal}

Tuliskan $j_U\colon\Pi_1(U)\to\Pi_1(X)$ dan
$j_V\colon\Pi_1(V)\to\Pi_1(X)$ bagi funktor inklusi. Pada objek di $U$,
definisi $K_0$ sama dengan $F_0$, dan pada lintasan yang seluruhnya berada di
$U$, definisi lokal $\widetilde K_1$ sama dengan $F_1$. Jadi

$$
K\circ j_U=F.
$$

Argumen yang sama memberi

$$
K\circ j_V=G.
$$

Tersisa keunikan yang tersirat, tetapi tidak dituliskan, dalam sumber.
Misalkan

$$
L\colon\Pi_1(X)\longrightarrow\Gamma
$$

funktor lain dengan $L\circ j_U=F$ dan $L\circ j_V=G$. Setiap $x\in X$
berada di $U$ atau di $V$, sehingga kedua persamaan pembatasan memaksa
$L_0(x)=K_0(x)$. Untuk morfisme $[\alpha]$, pilih subdivisi subordinat

$$
\alpha\simeq
\alpha_0\#\alpha_1\#\cdots\#\alpha_n
$$

yang setiap ruasnya berada di $U$ atau di $V$. Funktorialitas dan kedua
pembatasan memaksa

$$
\begin{aligned}
L_1([\alpha])
&=
L_1([\alpha_0])\cdots L_1([\alpha_n])\\
&=
\widetilde K_1(\alpha_0)\cdots\widetilde K_1(\alpha_n)\\
&=
K_1([\alpha]).
\end{aligned}
$$

Jadi $L=K$. Keberadaan dan keunikan ini membuktikan sifat universal pushout,
dan dengan demikian menuntaskan bukti Teorema 11.1.
:::

Teorema tersebut sangat kuat, tetapi dalam bentuk itu tidak selalu paling
nyaman untuk perhitungan. Kita menginginkan versi bagi
$\Pi_1(X,A)$ dengan $A\subseteq X$ yang lebih kecil, atau bahkan bagi
$\pi_1(X,x)$. Untuk mendapatkannya, kita memerlukan sebuah lemma kategoris
umum.

## Persegi komutatif dan retrak {#o012-rbt-l12-s02}

Untuk kategori sebarang $\mathcal C$, definisikan kategori
$\mathcal C^\square$. Objeknya adalah persegi komutatif di $\mathcal C$, dan
morfismenya adalah kubus komutatif: kubus yang setiap sisinya merupakan
persegi komutatif.

::: {.figure #o012-rbt-l12-fig-002}
**Diagram 12.2 (morfisme antardua persegi komutatif).** Persegi belakang dan
depan masing-masing adalah

$$
\begin{array}{ccc}
A_1&\xrightarrow{f_1}&B_1\\
{\scriptstyle g_1}\downarrow&&\downarrow{\scriptstyle h_1}\\
C_1&\xrightarrow{k_1}&D_1
\end{array}
\qquad
\begin{array}{ccc}
A_2&\xrightarrow{f_2}&B_2\\
{\scriptstyle g_2}\downarrow&&\downarrow{\scriptstyle h_2}\\
C_2&\xrightarrow{k_2}&D_2.
\end{array}
$$

Selain empat panah pada setiap persegi, morfisme di
$\mathcal C^\square$ mempunyai empat panah penghubung

$$
u_A\colon A_1\to A_2,
\quad
u_B\colon B_1\to B_2,
\quad
u_C\colon C_1\to C_2,
\quad
u_D\colon D_1\to D_2.
$$

Dua sisi ujung memenuhi $h_i\circ f_i=k_i\circ g_i$ untuk $i=1,2$.
Keempat sisi penghubung memenuhi

$$
\begin{aligned}
u_B\circ f_1&=f_2\circ u_A,&
u_C\circ g_1&=g_2\circ u_A,\\
u_D\circ h_1&=h_2\circ u_B,&
u_D\circ k_1&=k_2\circ u_C.
\end{aligned}
$$

Keenam persamaan itu adalah pembacaan linear lengkap dari kubus pada catatan
pinggir sumber.
:::

::: {.definition #o012-rbt-l12-def-001}
**Definisi 12.1 (retrak).** Dalam kategori $\mathcal C$, objek $V$ adalah
sebuah *retrak* dari objek $W$ jika terdapat morfisme

$$
i\colon V\longrightarrow W,
\qquad
r\colon W\longrightarrow V
$$

sedemikian sehingga

$$
r\circ i=\operatorname{id}_V.
$$

Morfisme $r$ disebut sebuah *retraksi*.
:::

Sebagai contoh, di $\mathbf{Vect}$ setiap subruang vektor
$V\subseteq\mathbb R^n$ adalah retrak: ambil $i$ sebagai inklusi dan $r$
sebagai proyeksi ortogonal ke $V$. Di $\mathbf{Set}$, misalkan
$T\subseteq S$ dan pilih $t_0\in T$. Inklusi $i\colon T\to S$ bersama fungsi

$$
r\colon S\longrightarrow T,
\qquad
r(s)=
\begin{cases}
s,&s\in T,\\
t_0,&s\in S\setminus T,
\end{cases}
$$

memberi retrak karena $r|_T=\operatorname{id}_T$.

Contoh yang lebih penting adalah sebagai berikut.

::: {.example #o012-rbt-l12-exa-001 data-source-label="eg:retracts_of_Pi1"}
**Contoh 12.1 (retraksi grupoid fundamental terbatas).** Misalkan $X$ suatu
ruang dan $A'\subseteq A\subseteq X$. Andaikan setiap titik di $A$ dapat
dihubungkan oleh lintasan di $X$ ke suatu titik di $A'$. Maka

$$
\Pi_1(X,A')
$$

adalah retrak dari $\Pi_1(X,A)$. Pernyataan ini memperumum kasus dari Tugas 2
dengan $A'=\{x\}$. Konstruksi retraksinya diperiksa lengkap dalam
Pemeriksaan Penguasaan 12.3.
:::

Kita juga dapat menanyakan kapan sebuah persegi komutatif di $\mathcal C$
merupakan retrak dari persegi komutatif lain: artinya tepat retrak sebagai
objek di $\mathcal C^\square$. Ingat bahwa persegi pushout adalah jenis khusus
persegi komutatif. Secara tepat, kita memerlukan morfisme
$i\colon S\to T$ dan $r\colon T\to S$ yang keduanya sudah merupakan kubus
komutatif. Setelah kompatibilitas kubus itu tersedia, persamaan
$r\circ i=\operatorname{id}_S$ boleh diperiksa pada masing-masing dari empat
simpul. Empat retraksi simpul yang dipilih secara terpisah belum tentu
merakit diri menjadi satu morfisme $r$ di $\mathcal C^\square$.

::: {.lemma #o012-rbt-l12-lem-001 data-source-label="lemma:retracts_of_pushouts"}
**Lemma 12.1 (retrak dari persegi pushout).** Setiap retrak dari persegi
pushout adalah persegi pushout.
:::

::: {.proof #o012-rbt-l12-proof-002}
**Bukti.** Sumber menyerahkan pernyataan ini sebagai **latihan**. Inilah
Latihan Sumber 12.1; solusi lengkap diberikan pada Pemeriksaan Penguasaan
12.2.
:::

Kita akan menerapkan Lemma 12.1 pada persegi pushout di $\mathbf{Gpd}$ dari
teorema Seifert--van Kampen. Persegi itu adalah objek
$\mathbf{Gpd}^\square$ dan melibatkan grupoid fundamental penuh
$\Pi_1(X)$, $\Pi_1(U)$, $\Pi_1(V)$, serta $\Pi_1(U\cap V)$. Retraksi seperti
pada Contoh 12.1 akan dirakit menjadi sebuah retraksi di
$\mathbf{Gpd}^\square$ yang simpul-simpulnya merupakan grupoid lebih kecil.

::: {.theorem #o012-rbt-l12-thm-001}
**Teorema 12.1 (Seifert--van Kampen relatif).** Misalkan $X$ suatu ruang,
$\{U,V\}$ sampul $X$ oleh lingkungan, dan $A\subseteq X$ suatu subruang.
Andaikan dalam masing-masing dari empat pasangan

$$
(X,A),
\quad
(U,A\cap U),
\quad
(V,A\cap V),
\quad
(U\cap V,A\cap U\cap V),
$$

setiap titik di ruang yang lebih besar dapat dihubungkan oleh lintasan di
dalam ruang itu ke suatu titik di ruang yang lebih kecil. Sebagai contoh,
setiap titik di $U$ harus terhubung oleh lintasan di $U$ ke suatu titik di
$A\cap U$. Maka persegi

$$
\begin{array}{ccc}
\Pi_1(U\cap V,A\cap U\cap V)&\longrightarrow&\Pi_1(V,A\cap V)\\
\downarrow&&\downarrow\\
\Pi_1(U,A\cap U)&\longrightarrow&\Pi_1(X,A)
\end{array}
$$

merupakan persegi pushout di $\mathbf{Gpd}$.
:::

::: {.figure #o012-rbt-l12-fig-003}
**Diagram 12.3 (fungsi persegi relatif).** Keempat panah adalah funktor yang
diinduksi oleh inklusi ruang. Panah atas memasukkan data lintasan dari
$U\cap V$ ke $V$; panah kiri memasukkannya ke $U$. Panah kanan memasukkan
lintasan di $V$ ke $X$, dan panah bawah melakukan hal yang sama bagi $U$.
Pada simpul mana pun, hanya titik-titik objek yang berada dalam irisan dengan
$A$ yang dipertahankan. Kedua komposit dari simpul kiri atas adalah funktor
inklusi yang sama ke $\Pi_1(X,A)$.
:::

::: {.proof #o012-rbt-l12-proof-003}
**Bukti.** Bagian yang melibatkan homotopi telah diselesaikan oleh Teorema
11.1. Kita hanya perlu menunjukkan bahwa persegi pada pernyataan merupakan
retrak di $\mathbf{Gpd}^\square$ dari persegi pushout pada teorema tersebut.

Funktor inklusi

$$
\begin{aligned}
\Pi_1(U\cap V,A\cap U\cap V)&\longrightarrow\Pi_1(U\cap V),\\
\Pi_1(U,A\cap U)&\longrightarrow\Pi_1(U),\\
\Pi_1(V,A\cap V)&\longrightarrow\Pi_1(V),\\
\Pi_1(X,A)&\longrightarrow\Pi_1(X)
\end{aligned}
$$

memberi satu morfisme di $\mathbf{Gpd}^\square$. Kita akan membangun morfisme
ke arah sebaliknya sebagai satu keluarga pilihan yang koheren.

Untuk setiap $x\in X$, pilih titik $a_x\in A$ dan kelas lintasan

$$
\eta_x\colon x\rightsquigarrow a_x.
$$

Pilihan dibuat menurut urutan berikut.

1. Jika $x\in A$, ambil $a_x=x$ dan $\eta_x$ lintasan konstan.
2. Jika $x\in(U\cap V)\setminus A$, gunakan hipotesis pasangan
   $(U\cap V,A\cap U\cap V)$ untuk memilih $a_x\in A\cap U\cap V$ dan
   $\eta_x$ seluruhnya di $U\cap V$.
3. Jika $x\in U\setminus V$, pilih $a_x\in A\cap U$ dan $\eta_x$ di $U$.
4. Jika $x\in V\setminus U$, pilih $a_x\in A\cap V$ dan $\eta_x$ di $V$.

Karena $U\cup V=X$, daftar itu mencakup semua titik. Mendahulukan irisan
memastikan bahwa pilihan yang dipakai pada $U$ dan $V$ benar-benar sama pada
$U\cap V$.

Definisikan funktor

$$
R_X\colon\Pi_1(X)\longrightarrow\Pi_1(X,A)
$$

pada objek dengan $R_X(x)=a_x$. Untuk morfisme yang diwakili lintasan
$\gamma\colon x\rightsquigarrow y$, tetapkan

$$
R_X([\gamma])
=
[\overline{\eta_x}\#\gamma\#\eta_y]
\colon a_x\rightsquigarrow a_y,
$$

di mana $\overline{\eta_x}$ adalah lintasan $\eta_x$ yang ditempuh balik.
Rumus ini tidak bergantung pada wakil $\gamma$, sebab mengonkatenasikan
homotopi berujung tetap dengan dua lintasan tetap tetap menghasilkan homotopi
berujung tetap. Lintasan
$\overline{\eta_x}\#\eta_x$ dan
$\eta_x\#\overline{\eta_x}$ dapat dibatalkan melalui homotopi berujung
tetap. Karena itu rumus mempertahankan identitas dan komposisi, sehingga
$R_X$ memang funktor.

Jika $x\in A$, pilihan $\eta_x$ konstan. Jadi, untuk funktor inklusi
$I_X\colon\Pi_1(X,A)\to\Pi_1(X)$, berlaku

$$
R_X\circ I_X=\operatorname{id}_{\Pi_1(X,A)}.
$$

Pilihan koheren di atas juga memastikan bahwa pembatasan $R_X$ memberi
funktor

$$
\begin{aligned}
\Pi_1(U\cap V)&\longrightarrow\Pi_1(U\cap V,A\cap U\cap V),\\
\Pi_1(U)&\longrightarrow\Pi_1(U,A\cap U),\\
\Pi_1(V)&\longrightarrow\Pi_1(V,A\cap V),\\
\Pi_1(X)&\longrightarrow\Pi_1(X,A).
\end{aligned}
$$

Keempat rumus adalah pembatasan dari rumus yang sama, sehingga setiap sisi
penghubung pada kubus komutatif benar-benar komutatif. Pada setiap simpul,
komposit retraksi setelah inklusi adalah identitas. Maka persegi relatif
adalah retrak di $\mathbf{Gpd}^\square$ dari persegi pushout Teorema 11.1.
Lemma 12.1 sekarang menunjukkan bahwa persegi relatif juga merupakan
pushout.
:::

## Dari pushout grupoid ke pushout grup {#o012-rbt-l12-s03}

Kita ingin memakai pushout grup karena dalam beberapa kasus objek itu lebih
mudah dihitung. Akan tetapi, Teorema 12.1 menyatakan pushout grupoid. Bahkan
jika kita memakai grupoid satu objek yang berasal dari grup, masih harus
diperiksa bahwa sifat universal di $\mathbf{Gpd}$ menyiratkan sifat universal
di $\mathbf{Grp}$. Hal itu mengikuti dari lemma kategoris berikut.

::: {.lemma #o012-rbt-l12-lem-002}
**Lemma 12.2 (pushout dalam subkategori penuh).** Misalkan $\mathcal C$ suatu
kategori dan $\mathcal D\hookrightarrow\mathcal C$ suatu subkategori penuh.
Misalkan persegi komutatif di $\mathcal D$

$$
\begin{array}{ccc}
A&\xrightarrow{f}&B\\
{\scriptstyle g}\downarrow&&\downarrow{\scriptstyle b}\\
C&\xrightarrow{c}&P
\end{array}
$$

merupakan persegi pushout ketika dipandang di $\mathcal C$. Maka persegi itu
juga merupakan persegi pushout di $\mathcal D$.
:::

::: {.figure #o012-rbt-l12-fig-004}
**Diagram 12.4 (data pushout pada lemma subkategori).** Keempat objek
$A,B,C,P$ berada di $\mathcal D$. Daftar panahnya adalah

$$
f\colon A\to B,
\quad
g\colon A\to C,
\quad
b\colon B\to P,
\quad
c\colon C\to P,
$$

dan komutativitas berarti $b\circ f=c\circ g$. Hipotesis mengatakan bahwa
untuk setiap objek target di $\mathcal C$, persegi ini mempunyai sifat
universal pushout; kesimpulan hanya membatasi objek target dan morfisme ke
$\mathcal D$.
:::

::: {.proof #o012-rbt-l12-proof-004}
**Bukti.** Kita memeriksa sifat universal di $\mathcal D$. Ambil persegi
komutatif sebarang di $\mathcal D$

$$
\begin{array}{ccc}
A&\xrightarrow{f}&B\\
{\scriptstyle g}\downarrow&&\downarrow{\scriptstyle u}\\
C&\xrightarrow{v}&Q,
\end{array}
$$

jadi $u\circ f=v\circ g$. Huruf $Q$ dipakai untuk objek kanan bawah agar
tidak tertukar dengan nama kategori $\mathcal D$.

::: {.figure #o012-rbt-l12-fig-005}
**Diagram 12.5 (kocone uji dalam subkategori penuh).** Data linear diagram
adalah $f\colon A\to B$, $g\colon A\to C$,
$u\colon B\to Q$, dan $v\colon C\to Q$, semuanya di $\mathcal D$, dengan
persamaan kompatibilitas $u\circ f=v\circ g$. Sifat universal harus
menghasilkan tepat satu $k\colon P\to Q$ dengan
$k\circ b=u$ dan $k\circ c=v$.
:::

Pandang data itu di kategori ambient $\mathcal C$. Karena persegi dengan
sudut $P$ adalah pushout di $\mathcal C$, terdapat tepat satu morfisme

$$
k\colon P\longrightarrow Q
$$

di $\mathcal C$ dengan $k\circ b=u$ dan $k\circ c=v$. Kedua objek $P,Q$
berada di $\mathcal D$, dan $\mathcal D$ penuh di $\mathcal C$. Karena itu
$k$ adalah morfisme di $\mathcal D$; persamaan kedua segitiga tetap berlaku
di sana. Jika $\ell\colon P\to Q$ adalah morfisme lain di $\mathcal D$ yang
memenuhi kedua persamaan, maka $\ell$ juga morfisme di $\mathcal C$.
Keunikan ambient memberi $\ell=k$. Jadi sifat universal berlaku di
$\mathcal D$.
:::

Funktor

$$
\mathbf B\colon\mathbf{Grp}\longrightarrow\mathbf{Gpd}
$$

mengirim sebuah grup ke grupoid satu objeknya. Funktor ini sepenuhnya setia.
Dengan mengidentifikasi $\mathbf{Grp}$ dengan citra esensialnya, yaitu
subkategori penuh grupoid satu objek, kita dapat menerapkan Lemma 12.2.
Secara khusus, untuk ruang bertitik $(Y,x)$ terdapat identifikasi alami

$$
\Pi_1(Y,\{x\})\cong\mathbf B\pi_1(Y,x).
$$

::: {.corollary #o012-rbt-l12-cor-001}
**Akibat 12.1 (Seifert--van Kampen untuk grup fundamental).** Misalkan $X$
terhubung lintasan, $\{U,V\}$ sampul $X$ oleh lingkungan yang masing-masing
terhubung lintasan, dan $U\cap V$ terhubung lintasan. Untuk
$x\in U\cap V$, persegi

$$
\begin{array}{ccc}
\pi_1(U\cap V,x)&\longrightarrow&\pi_1(V,x)\\
\downarrow&&\downarrow\\
\pi_1(U,x)&\longrightarrow&\pi_1(X,x)
\end{array}
$$

merupakan persegi pushout di $\mathbf{Grp}$.
:::

::: {.figure #o012-rbt-l12-fig-006}
**Diagram 12.6 (fungsi persegi grup fundamental).** Keempat homomorfisme
diinduksi oleh inklusi ruang bertitik. Dua panah keluar dari
$\pi_1(U\cap V,x)$ memandang loop yang sama masing-masing di $U$ dan $V$.
Dua panah berikutnya memandang loop-loop itu di $X$. Komutativitas menyatakan
bahwa kedua cara memasukkan loop irisan ke $X$ menghasilkan kelas loop yang
sama.
:::

::: {.proof #o012-rbt-l12-proof-005}
**Bukti.** Ambil $A=\{x\}$ dalam Teorema 12.1. Keterhubungan lintasan
$X,U,V$, dan $U\cap V$ memastikan semua syarat pasangan relatif terpenuhi.
Kita memperoleh persegi pushout dari grupoid satu objek. Lemma 12.2, setelah
identifikasi melalui $\mathbf B$, menjadikannya persegi pushout grup.
:::

Jadi sekarang kita perlu mengetahui seperti apa pushout grup itu.

## Contoh: grup fundamental sfera {#o012-rbt-l12-s04}

::: {.example #o012-rbt-l12-exa-002}
**Contoh 12.2 (sfera berdimensi lebih dari satu).** Ambil $n>1$. Sampuli
$S^n$ dengan

$$
U=S^n\setminus\{N\},
\qquad
V=S^n\setminus\{S\},
$$

di mana $N$ dan $S$ adalah dua titik antipodal, yaitu kutub Utara dan kutub
Selatan. Kedua subruang itu terbuka dan $U\cup V=S^n$, jadi keduanya memang
membentuk sampul oleh lingkungan. Kita mempunyai ekuivalensi homotopi

$$
U\cap V\simeq S^{n-1}\times(-1,1).
$$

Karena $n>1$, sfera $S^{n-1}$ terhubung lintasan; demikian pula
$U\cap V$. Ruang $U$ dan $V$ juga terhubung lintasan, sebagaimana terlihat
dari proyeksi stereografik di bawah. Jadi Akibat 12.1 dapat diterapkan. Pilih
titik basis

$$
x\in S^{n-1}\subset U\cap V.
$$

Proyeksi stereografik memberi

$$
U\simeq\mathbb R^n\simeq V.
$$

Kedua ruang $U$ dan $V$ kontraktibel, maka grup fundamentalnya trivial:

$$
\pi_1(U,x)=1=\pi_1(V,x).
$$

Teorema Seifert--van Kampen karena itu memberi persegi pushout

$$
\begin{array}{ccc}
\pi_1(S^{n-1}\times(-1,1),x)&\longrightarrow&1\\
\downarrow&&\downarrow\\
1&\longrightarrow&\pi_1(S^n,x).
\end{array}
$$

::: {.figure #o012-rbt-l12-fig-007}
**Diagram 12.7 (pembacaan semantik pushout sfera).** Kedua panah keluar dari
$\pi_1(S^{n-1}\times(-1,1),x)$ adalah homomorfisme unik ke grup trivial.
Kedua panah dari grup trivial masuk ke $\pi_1(S^n,x)$. Untuk menguji
pushout, pilih grup sebarang $K$ dan pasangan homomorfisme

$$
1\longrightarrow K\longleftarrow1.
$$

Pasangan itu unik dan otomatis kompatibel pada grup kiri atas. Karena itu
sifat universal memaksa adanya tepat satu homomorfisme
$\pi_1(S^n,x)\to K$.
:::

Satu-satunya grup yang mempunyai tepat satu homomorfisme ke setiap grup lain
adalah grup trivial. Memang, jika sebuah grup $P$ mempunyai sifat itu, kedua
homomorfisme $P\to P$ berupa identitas dan homomorfisme trivial harus sama;
jadi setiap unsur $P$ adalah identitas. Dengan demikian

$$
\pi_1(S^n,x)=1
$$

untuk setiap $n>1$.
:::

Argumen ini gagal untuk $n=1$. Sampul yang sama menghasilkan

$$
U\cap V\simeq S^0\times(-1,1),
$$

yakni gabungan saling lepas dua interval. Irisan itu tidak terhubung lintasan,
sehingga hipotesis Akibat 12.1 tidak terpenuhi. Kegagalan ini hanya mengenai
versi grup satu objek; Teorema 11.1 dalam bentuk grupoid tetap berlaku bagi
sampul oleh lingkungan tersebut.

::: {.boundary #o012-rbt-l12-boundary}
**Batas sumber.** Kalimat sebelumnya adalah isi terakhir Notes.tex baris
2726. Baris 2727 memulai Kuliah 13. Unit ini tidak menerjemahkan, merangkum,
atau memakai materi setelah batas tersebut.
:::

# Pendamping penguasaan: pemeriksaan dan solusi lengkap {.unnumbered #o012-rbt-l12-mastery}

Bagian ini menutup satu latihan eksplisit dan tiga kelompok keterampilan yang
dipakai oleh sumber. Semua solusi hanya mengembangkan data dan argumen unit
ini.

::: {.exercise #o012-rbt-l12-mcheck-001}
**Pemeriksaan penguasaan 12.1 (dari pertukaran sel ke funktor universal).**

1. Jelaskan mengapa mengganti satu rute “kanan lalu atas” dengan “atas lalu
   kanan” pada sebuah sel tidak mengandaikan invariansi homotopi global yang
   sedang dibuktikan.
2. Buktikan hukum komposisi $K_1$ memakai partisi subordinat.
3. Misalkan $L\colon\Pi_1(X)\to\Gamma$ mempunyai pembatasan $F$ dan $G$.
   Buktikan langsung bahwa $L=K$.
:::

## Solusi Pemeriksaan 12.1 {#o012-rbt-l12-sol-001}

Setiap sel dipetakan seluruhnya ke satu subruang, katakan $U$. Kedua rute
batas sel karena itu mewakili morfisme yang sama di $\Pi_1(U)$ melalui
homotopi persegi lokal dari Unit 11. Menerapkan funktor yang sudah diberikan,
$F$, menghasilkan nilai yang sama. Jika citra sel berada di $V$, gunakan
$G$. Jadi langkah lokal hanya memakai funktorialitas $F$ atau $G$ yang sudah
tersedia; ia belum memakai funktor global $K$ ataupun invariansi global
$\widetilde K_1$.

Untuk $\alpha\colon x\rightsquigarrow y$ dan
$\beta\colon y\rightsquigarrow z$, pilih partisi subordinat

$$
\alpha\simeq\alpha_0\#\cdots\#\alpha_m,
\qquad
\beta\simeq\beta_0\#\cdots\#\beta_n.
$$

Setelah skala parameter kedua partisi disesuaikan, daftar ruas gabungan

$$
\alpha_0,\ldots,\alpha_m,\beta_0,\ldots,\beta_n
$$

adalah partisi subordinat bagi $\alpha\#\beta$. Maka definisi dan
kemandirian partisi memberi

$$
\begin{aligned}
K_1([\alpha][\beta])
&=
\prod_{i=0}^{m}\widetilde K_1(\alpha_i)
\prod_{j=0}^{n}\widetilde K_1(\beta_j)\\
&=
K_1([\alpha])K_1([\beta]).
\end{aligned}
$$

Terakhir, pembatasan memaksa $L_0=K_0$ karena $U\cup V=X$. Untuk setiap
$[\alpha]$, subdivisi di atas menulis morfisme itu sebagai komposit morfisme
yang masing-masing berasal dari $\Pi_1(U)$ atau $\Pi_1(V)$. Pada setiap
faktor, $L$ dipaksa sama dengan $F$ atau $G$, dan nilai itu persis faktor yang
mendefinisikan $K$. Funktorialitas memaksa kesamaan pada seluruh komposit.
Jadi $L_1=K_1$ dan $L=K$.

::: {.exercise #o012-rbt-l12-mcheck-002}
**Pemeriksaan penguasaan 12.2 (Latihan Sumber 12.1: retrak pushout).**
Misalkan persegi $S$ merupakan retrak dari persegi pushout $T$ di
$\mathcal C^\square$. Tuliskan morfisme inklusi $i\colon S\to T$ dan
retraksi $r\colon T\to S$, dengan $r\circ i=\operatorname{id}_S$ pada setiap
simpul. Buktikan bahwa $S$ memenuhi sifat universal pushout.
:::

## Solusi Pemeriksaan 12.2 {#o012-rbt-l12-sol-002}

Tuliskan persegi retrak $S$ sebagai

$$
\begin{array}{ccc}
A&\xrightarrow{f}&B\\
{\scriptstyle g}\downarrow&&\downarrow{\scriptstyle b}\\
C&\xrightarrow{c}&P,
\end{array}
$$

dan beri tanda prima pada keempat objek serta panah persegi pushout $T$.
Komponen morfisme kubus ditulis $i_A,i_B,i_C,i_P$ dan
$r_A,r_B,r_C,r_P$.

Ambil kocone kompatibel $u\colon B\to Z$ dan $v\colon C\to Z$, jadi
$u\circ f=v\circ g$. Pascakomposisi komponen retraksi menghasilkan kocone
pada $T$,

$$
u\circ r_B\colon B'\to Z,
\qquad
v\circ r_C\colon C'\to Z.
$$

Komutativitas kubus dan kompatibilitas kocone awal memberi

$$
u\circ r_B\circ f'
=u\circ f\circ r_A
=v\circ g\circ r_A
=v\circ r_C\circ g'.
$$

Karena $T$ pushout, terdapat tepat satu $q'\colon P'\to Z$ yang memperluas
kocone ini. Definisikan

$$
q:=q'\circ i_P\colon P\to Z.
$$

Komutativitas kubus dan $r_B\circ i_B=\operatorname{id}_B$ memberi

$$
q\circ b
=q'\circ b'\circ i_B
=u\circ r_B\circ i_B
=u,
$$

dan cara yang sama memberi $q\circ c=v$.

Untuk keunikan, andaikan $w\colon P\to Z$ juga memperluas $u,v$. Maka
$w\circ r_P\colon P'\to Z$ memperluas
$u\circ r_B$ dan $v\circ r_C$. Keunikan pushout $T$ memberi
$w\circ r_P=q'$. Akibatnya

$$
w
=w\circ r_P\circ i_P
=q'\circ i_P
=q.
$$

Jadi $S$ adalah persegi pushout.

::: {.exercise #o012-rbt-l12-mcheck-003}
**Pemeriksaan penguasaan 12.3 (retraksi grupoid dan koherensi kubus).**

1. Dalam Contoh 12.1, pilih $a_x\in A'$ dan
   $\eta_x\colon x\rightsquigarrow a_x$ untuk setiap $x\in A$, dengan
   pilihan konstan pada $A'$. Bangun retraksi
   $R\colon\Pi_1(X,A)\to\Pi_1(X,A')$.
2. Periksa identitas, komposisi, dan persamaan retraksi.
3. Jelaskan mengapa pilihan berprioritas pada irisan dalam bukti Teorema 12.1
   membuat keempat retraksi menjadi satu morfisme di
   $\mathbf{Gpd}^\square$.
:::

## Solusi Pemeriksaan 12.3 {#o012-rbt-l12-sol-003}

Definisikan $R(x)=a_x$ dan

$$
R([\gamma\colon x\rightsquigarrow y])
=
[\overline{\eta_x}\#\gamma\#\eta_y].
$$

Jika $\gamma$ diganti oleh lintasan yang homotopik berujung tetap, rumus itu
memberi kelas yang sama setelah jalur tetap ditempelkan di kedua ujung. Untuk
identitas di $x$, lintasan
$\overline{\eta_x}\#c_x\#\eta_x$ homotopik dengan lintasan konstan di
$a_x$. Untuk lintasan berurutan
$\gamma\colon x\rightsquigarrow y$ dan
$\lambda\colon y\rightsquigarrow z$, komposit citranya mempunyai bagian
tengah

$$
\eta_y\#\overline{\eta_y},
$$

yang homotopik berujung tetap dengan lintasan konstan di $y$. Setelah bagian
itu dibatalkan, tersisa

$$
[\overline{\eta_x}\#\gamma\#\lambda\#\eta_z]
=R([\gamma][\lambda]).
$$

Maka $R$ funktor. Jika $x\in A'$, $a_x=x$ dan $\eta_x$ konstan. Pada objek
dan morfisme yang seluruh titik ujungnya berada di $A'$, komposit

$$
\Pi_1(X,A')\longrightarrow\Pi_1(X,A)
\xrightarrow{R}\Pi_1(X,A')
$$

adalah identitas. Jadi ini benar-benar retraksi.

Dalam Teorema 12.1, satu pilihan pada $x\in U\cap V$ dipakai sekaligus untuk
pembatasan ke $U$, $V$, dan $U\cap V$. Karena rumus objek serta morfismenya
sama sebelum dan sesudah pembatasan, empat persegi samping kubus komutatif
secara ketat. Pilihan terpisah tanpa prioritas irisan hanya akan menghasilkan
retraksi individual dan tidak menjamin komutativitas kubus.

::: {.exercise #o012-rbt-l12-mcheck-004}
**Pemeriksaan penguasaan 12.4 (subkategori penuh dan sfera).**

1. Dalam Lemma 12.2, tunjukkan tepat di mana kepenuhan
   $\mathcal D\subseteq\mathcal C$ dipakai untuk keberadaan, dan tepat di
   mana sifat pushout ambient dipakai untuk keunikan.
2. Buktikan langsung bahwa pushout dari diagram grup
   $1\leftarrow H\to1$ adalah grup trivial, untuk grup sebarang $H$.
3. Jelaskan mengapa jawaban bagian 2 menghitung $\pi_1(S^n,x)$ untuk $n>1$
   tetapi argumen sampul yang sama tidak boleh dipakai untuk $S^1$.
:::

## Solusi Pemeriksaan 12.4 {#o012-rbt-l12-sol-004}

Pushout ambient mula-mula menghasilkan morfisme universal
$k\colon P\to Q$ di $\mathcal C$. Kepenuhan dipakai karena $P,Q$ adalah
objek $\mathcal D$: setiap morfisme ambient di antara keduanya, termasuk
$k$, juga merupakan morfisme $\mathcal D$. Untuk keunikan, calon lain di
$\mathcal D$ dipandang sebagai morfisme di $\mathcal C$, lalu keunikan
pushout ambient memaksanya sama dengan $k$.

Sekarang ambil diagram $1\leftarrow H\to1$. Untuk setiap grup $K$, hanya ada
satu homomorfisme dari $1$ ke $K$, sehingga hanya ada satu kocone

$$
1\longrightarrow K\longleftarrow1,
$$

dan kompatibilitas pada $H$ otomatis. Grup trivial $1$ mempunyai tepat satu
homomorfisme ke $K$, jadi ia mewakili sifat universal pushout. Keunikan
pushout hingga isomorfisme memberi bahwa pushout diagram tersebut adalah
grup trivial.

Untuk $n>1$, $U$, $V$, dan $U\cap V\simeq S^{n-1}\times(-1,1)$ semuanya
terhubung lintasan. Akibat 12.1 mengubah sampul sfera menjadi tepat diagram
grup pada bagian 2, sehingga $\pi_1(S^n,x)=1$. Untuk $n=1$, irisan setara
dengan dua interval yang saling lepas. Hipotesis keterhubungan lintasan pada
irisan gagal, maka Akibat 12.1 tidak menghasilkan diagram satu-objek itu;
menerapkan hasil bagian 2 pada diagram yang tidak disediakan oleh teorema
akan menjadi langkah yang tidak sah.
