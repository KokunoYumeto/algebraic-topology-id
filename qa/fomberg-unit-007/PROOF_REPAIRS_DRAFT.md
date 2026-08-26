# Draf perbaikan bukti Unit 007: homologi seluler

Dokumen kerja ini memuat tiga perbaikan yang ditulis mandiri untuk edisi
Bahasa Indonesia. Ketiganya menutup lokus yang dibekukan dalam audit sumber
Unit 007; tidak satu pun dinyatakan sebagai prosa sumber. Koefisien homologi
selalu dalam $\mathbb Z$.

::: {.proof-repair-module #o012-fom-u007-repair-pr13 data-origin="edition-original" data-source-lines="3525-3594" data-repair-id="FOM-PR-13" data-proof-status="complete_original_repair"}
## FOM-PR-13 — stabilisasi homologi kerangka untuk kompleks CW sebarang

::: {.theorem #o012-fom-u007-thm-skeleton-stabilization data-origin="edition-original" data-source-lines="3525-3594" data-repair-id="FOM-PR-13"}
**Teorema (stabilisasi kerangka).** Misalkan $X$ suatu kompleks CW, tanpa
asumsi berdimensi hingga atau mempunyai berhingga banyak sel, dan tuliskan
$X^{(r)}$ untuk $r$-kerangkanya. Untuk $k\geq 0$ dan $n>k$, inklusi

$$
\iota_n\colon X^{(n)}\hookrightarrow X
$$

menginduksi isomorfisma kanonik

$$
(\iota_n)_*\colon H_k(X^{(n)})\xrightarrow{\cong}H_k(X).
$$
:::

::: {.proof #o012-fom-u007-proof-pr13 data-origin="edition-original" data-source-lines="3525-3594" data-repair-id="FOM-PR-13" data-proof-status="complete_original_repair"}
**Bukti.** Kita pisahkan argumen hingga dari langkah yang menghapus asumsi
dimensi hingga.

**1. Perubahan dari satu kerangka ke kerangka berikutnya.** Untuk setiap
$r$, hasil bagi $X^{(r)}/X^{(r-1)}$ adalah baji satu sfera $S^r$ bagi setiap
sel-$r$. Teorema hasil bagi relatif dan aditivitas homologi tereduksi memberi

$$
H_j(X^{(r)},X^{(r-1)})\cong
\begin{cases}
\displaystyle\bigoplus_{\alpha\in I_r}\mathbb Z[\Phi_\alpha],&j=r,\\[4pt]
0,&j\ne r,
\end{cases}
$$

dengan $I_r$ himpunan sel-$r$ dan $\Phi_\alpha$ pemetaan
karakteristiknya. Jika $r\geq n+1$ dan $n>k$, maka $r>k+1$. Karena itu kedua
suku relatif yang mengapit panah inklusi dalam barisan eksak panjang pasangan,

$$
H_{k+1}(X^{(r)},X^{(r-1)})\longrightarrow
H_k(X^{(r-1)})\longrightarrow H_k(X^{(r)})\longrightarrow
H_k(X^{(r)},X^{(r-1)}),
$$

bernilai nol. Jadi

$$
H_k(X^{(r-1)})\xrightarrow{\cong}H_k(X^{(r)})
\qquad(r\geq n+1).
\tag{13.1}
$$

Secara khusus, jika $K$ adalah subkompleks berdimensi hingga, penyusunan
isomorfisma (13.1) memberi

$$
H_k(K^{(n)})\xrightarrow{\cong}H_k(K).
\tag{13.2}
$$

**2. Lemma dukungan kompak bagi kompleks CW.** Setiap himpunan kompak
$A\subseteq X$ termuat dalam suatu subkompleks hingga. Untuk melihatnya,
andaikan $A$ bertemu tak berhingga banyak sel terbuka yang berbeda dan pilih
$x_i\in A$ pada sel terbuka ke-$i$. Bagi setiap $i$, tetapkan

$$
U_i=X\setminus\{x_j:j\ne i\}.
$$

Penutupan setiap sel CW bertemu hanya berhingga banyak sel, sehingga
$\{x_j:j\ne i\}$ beririsan dengan setiap sel tertutup dalam himpunan hingga.
Irisan itu tertutup. Menurut topologi lemah CW, himpunan yang dibuang
tertutup di $X$, maka $U_i$ terbuka. Keluarga $\{U_i\}$ menutupi $A$, tetapi
gabungan berhingga anggotanya kehilangan suatu $x_j$ yang indeksnya tidak
terpilih. Ini bertentangan dengan kekompakan $A$. Jadi $A$ hanya bertemu
berhingga banyak sel terbuka. Gabungan penutupan sel-sel tersebut, beserta
berhingga banyak sel pada penutupannya, adalah subkompleks hingga yang memuat
$A$.

Setiap rantai singular adalah jumlah berhingga simpleks singular. Dukungan
rantai itu merupakan gabungan berhingga citra simpleks standar yang kompak;
langkah sebelumnya menempatkannya dalam suatu subkompleks hingga.

**3. Surjektivitas.** Ambil $[z]\in H_k(X)$ dan pilih wakil siklus singular
$z$. Ada subkompleks hingga $K\subseteq X$ yang memuat dukungan $z$.
Isomorfisma (13.2) memberi kelas $[z_n]\in H_k(K^{(n)})$ yang citranya di
$H_k(K)$ adalah $[z]$. Karena $K^{(n)}\subseteq X^{(n)}$, kelas yang sama
memberi prapeta $[z]$ di $H_k(X^{(n)})$.

**4. Injektivitas.** Ambil siklus $c$ dalam $X^{(n)}$ dan andaikan
$c=\partial b$ untuk suatu rantai singular $b$ dalam $X$. Pilih subkompleks
hingga $K$ yang memuat dukungan $c$ dan $b$. Karena $c$ terletak dalam
$X^{(n)}$, ia terletak dalam

$$
K\cap X^{(n)}=K^{(n)}.
$$

Kelasnya bernilai nol di $H_k(K)$. Injektivitas isomorfisma (13.2) memaksa
kelasnya bernilai nol di $H_k(K^{(n)})$, sehingga $c$ sudah membatasi dalam
$K^{(n)}\subseteq X^{(n)}$. Jadi $(\iota_n)_*$ injektif. Bersama langkah
sebelumnya, ini membuktikan teorema untuk kompleks CW sebarang. $\square$
:::

::: {.proof-check #o012-fom-u007-check-pr13 data-origin="edition-original" data-repair-id="FOM-PR-13"}
**Pemeriksaan internal FOM-PR-13.** (i) Pada (13.1), syarat $r>k+1$
mematikan tepat suku relatif berderajat $k+1$ dan $k$; (ii) dukungan siklus
dan rantai pembatas sama-sama dimasukkan ke subkompleks hingga, sehingga
argumen injektivitas tidak hanya memeriksa wakil; (iii) tidak digunakan
kesimpulan teorema homologi seluler, jadi perbaikan ini tidak melingkar;
(iv) isomorfisma adalah pemetaan yang diinduksi inklusi, bukan sekadar
isomorfisma abstrak.
:::
:::

::: {.proof-repair-module #o012-fom-u007-repair-pr14 data-origin="edition-original" data-source-lines="3596-3640,3684-4184" data-repair-id="FOM-PR-14" data-proof-status="complete_original_repair"}
## FOM-PR-14 — teorema homologi seluler dan kealamiannya

::: {.theorem #o012-fom-u007-thm-cellular-homology data-origin="edition-original" data-source-lines="3596-3640,3684-4184" data-repair-id="FOM-PR-14"}
**Teorema (homologi seluler).** Misalkan $X$ suatu kompleks CW sebarang,
$X^{(-1)}=\varnothing$, dan

$$
C_n^{\mathrm{CW}}(X)=H_n(X^{(n)},X^{(n-1)}).
$$

Tuliskan

$$
\delta_n\colon H_n(X^{(n)},X^{(n-1)})\longrightarrow
H_{n-1}(X^{(n-1)})
$$

untuk pemetaan penghubung dan

$$
\rho_{n-1}\colon H_{n-1}(X^{(n-1)})\longrightarrow
H_{n-1}(X^{(n-1)},X^{(n-2)})
$$

untuk pemetaan pasangan. Tetapkan

$$
d_n=\rho_{n-1}\circ\delta_n
\quad(n\geq1),
\qquad d_0=0.
\tag{14.1}
$$

Maka $d_{n-1}d_n=0$, dan ada isomorfisma natural

$$
\Theta_{X,n}\colon
H_n(C_*^{\mathrm{CW}}(X),d)\xrightarrow{\cong}H_n(X).
\tag{14.2}
$$

Kealamian (14.2) berlaku secara langsung untuk pemetaan seluler. Untuk
pemetaan kontinu sebarang antarkompleks CW, ambil pendekatan seluler; pemetaan
yang dihasilkan pada homologi seluler tidak bergantung pada pilihan setelah
diidentifikasi melalui $\Theta$, dan sama dengan pemetaan homologi singular.
:::

::: {.proof #o012-fom-u007-proof-pr14 data-origin="edition-original" data-source-lines="3596-3640,3684-4184" data-repair-id="FOM-PR-14" data-proof-status="complete_original_repair"}
**Bukti.**

**1. Grup relatif dan pembentukan kompleks rantai.** Pasangan
$(X^{(p)},X^{(p-1)})$ adalah pasangan baik. Dengan meruntuhkan kerangka
sebelumnya dan memakai orientasi yang dipilih pada setiap sel-$p$, kita
memperoleh

$$
\begin{aligned}
H_m(X^{(p)},X^{(p-1)})
&\cong \widetilde H_m(X^{(p)}/X^{(p-1)})\\
&\cong \widetilde H_m\!\left(\bigvee_{\alpha\in I_p}S^p_\alpha\right)\\
&\cong
\begin{cases}
\displaystyle\bigoplus_{\alpha\in I_p}\mathbb Z[\Phi_\alpha],&m=p,\\[4pt]
0,&m\ne p.
\end{cases}
\end{aligned}
\tag{14.3}
$$

Untuk $p=0$, pernyataan yang sama dibaca sebagai
$H_0(X^{(0)})\cong\bigoplus_{\alpha\in I_0}\mathbb Z[\Phi_\alpha]$.
Untuk $n\geq2$, eksakitas barisan pasangan
$(X^{(n-1)},X^{(n-2)})$ memberi

$$
\delta_{n-1}\circ\rho_{n-1}=0.
$$

Karena itu

$$
d_{n-1}d_n
=\rho_{n-2}\delta_{n-1}\rho_{n-1}\delta_n=0,
$$

dan (14.1) benar-benar mendefinisikan kompleks rantai. Untuk $n=1$,
persamaan yang diperlukan adalah $d_0d_1=0$, yang langsung mengikuti
$d_0=0$.

**2. Kopel eksak filtrasi kerangka.** Barisan eksak panjang semua pasangan
kerangka dapat ditempatkan dalam kopel eksak (*exact couple*)

$$
D^1_{p,q}=H_{p+q}(X^{(p)}),
\qquad
E^1_{p,q}=H_{p+q}(X^{(p)},X^{(p-1)}).
$$

Tiga panahnya adalah inklusi kerangka, pemetaan menuju homologi relatif, dan
pemetaan penghubung. Diferensial turunannya ialah

$$
d^1=j\circ k\colon E^1_{p,q}\longrightarrow E^1_{p-1,q}.
$$

Menurut (14.3), $E^1_{p,q}=0$ untuk $q\ne0$, sedangkan pada baris $q=0$
kita mempunyai

$$
E^1_{p,0}=C_p^{\mathrm{CW}}(X),
\qquad d^1=d_p.
$$

Jadi

$$
E^2_{p,0}=H_p(C_*^{\mathrm{CW}}(X)),
$$

dan tidak ada diferensial lebih tinggi yang dapat masuk atau keluar dari
baris ini. Dengan demikian kopel eksak sudah runtuh pada halaman kedua.
Filtrasi ini menyapu habis rantai singular: citra setiap simpleks singular
kompak dan karenanya termuat dalam suatu subkompleks hingga. Jadi tidak ada
kelas homologi “di luar” semua kerangka. Perbaikan FOM-PR-13 memberi
stabilisasi pada setiap derajat dan memastikan konvergensi ini juga untuk
kompleks CW tak berdimensi hingga.

Langkah berikut memberi identifikasi tepi secara eksplisit; karena itu bukti
tidak hanya mengandalkan istilah “runtuh” pada kopel eksak.

**3. Siklus seluler sebagai kelas pada $X^{(n)}$.** Tuliskan

$$
\rho_n\colon H_n(X^{(n)})\longrightarrow
H_n(X^{(n)},X^{(n-1)})=C_n^{\mathrm{CW}}(X).
$$

Untuk $n\geq1$, karena $H_n(X^{(n-1)})=0$, pemetaan $\rho_n$ injektif.
Selanjutnya, $H_{n-1}(X^{(n-2)})=0$, sehingga $\rho_{n-1}$ juga injektif. Eksakitas
barisan pasangan $(X^{(n)},X^{(n-1)})$ kini memberi

$$
\ker d_n
=\ker(\rho_{n-1}\delta_n)
=\ker\delta_n
=\operatorname{im}\rho_n.
\tag{14.4}
$$

Untuk $n=0$, rumus yang sama berlaku dengan $d_0=0$ dan $\rho_0$ sebagai
identitas $H_0(X^{(0)})\to C_0^{\mathrm{CW}}(X)$.

Jadi setiap siklus seluler $c\in C_n^{\mathrm{CW}}(X)$ mempunyai tepat satu
kelas $a\in H_n(X^{(n)})$ dengan $\rho_n(a)=c$.

**4. Batas seluler dan sel-$n+1$.** Bagian relevan dari barisan eksak
panjang pasangan $(X^{(n+1)},X^{(n)})$ adalah

$$
C_{n+1}^{\mathrm{CW}}(X)
\xrightarrow{\delta_{n+1}}H_n(X^{(n)})
\longrightarrow H_n(X^{(n+1)})
\longrightarrow H_n(X^{(n+1)},X^{(n)}).
$$

Suku terakhir nol menurut (14.3). Karena
$d_{n+1}=\rho_n\delta_{n+1}$, (14.4) mengidentifikasi batas seluler dengan
$\rho_n(\operatorname{im}\delta_{n+1})$. Oleh karena itu

$$
\begin{aligned}
H_n(C_*^{\mathrm{CW}}(X))
&=\frac{\ker d_n}{\operatorname{im}d_{n+1}}\\
&\cong
\frac{H_n(X^{(n)})}{\operatorname{im}\delta_{n+1}}\\
&\cong H_n(X^{(n+1)}).
\end{aligned}
\tag{14.5}
$$

Karena $n+1>n$, FOM-PR-13 mengidentifikasi suku terakhir secara kanonik
dengan $H_n(X)$. Inilah isomorfisma $\Theta_{X,n}$.

Secara konkret, jika $[c]$ adalah kelas homologi seluler dan
$c=\rho_n(a)$ menurut (14.4), maka

$$
\Theta_{X,n}([c])=(X^{(n)}\hookrightarrow X)_*(a).
\tag{14.6}
$$

Jika $c$ diganti dengan $c+d_{n+1}(e)$, kelas $a$ berubah sebesar
$\delta_{n+1}(e)$, yang mati setelah dimasukkan ke $X^{(n+1)}$ dan kemudian
ke $X$. Sebaliknya, eksakitas pada (14.5) menunjukkan bahwa hanya perubahan
semacam itu yang mati. Maka (14.6) terdefinisi dengan baik dan bijektif.

**5. Kealamian.** Misalkan $f\colon X\to Y$ seluler, jadi
$f(X^{(p)})\subseteq Y^{(p)}$ untuk semua $p$. Pemetaan-pemetaan pasangan
menghasilkan

$$
f^{\mathrm{CW}}_p\colon
H_p(X^{(p)},X^{(p-1)})\longrightarrow
H_p(Y^{(p)},Y^{(p-1)}).
$$

Kealamian pemetaan penghubung dan pemetaan pasangan memberi persegi
komutatif

$$
\begin{array}{ccc}
C_p^{\mathrm{CW}}(X)&\xrightarrow{d_p^X}&C_{p-1}^{\mathrm{CW}}(X)\\
\downarrow f_p^{\mathrm{CW}}&&\downarrow f_{p-1}^{\mathrm{CW}}\\
C_p^{\mathrm{CW}}(Y)&\xrightarrow{d_p^Y}&C_{p-1}^{\mathrm{CW}}(Y).
\end{array}
\tag{14.7}
$$

Jadi $f^{\mathrm{CW}}_*$ adalah pemetaan rantai. Jika
$c=\rho_n^X(a)$, kealamian $\rho_n$ memberi
$f_n^{\mathrm{CW}}(c)=\rho_n^Y(f_*a)$. Memasukkan kedua kelas ke ruang penuh
menunjukkan

$$
\begin{array}{ccc}
H_n(C_*^{\mathrm{CW}}(X))&\xrightarrow{\Theta_{X,n}}&H_n(X)\\
\downarrow H_n(f^{\mathrm{CW}})&&\downarrow H_n(f)\\
H_n(C_*^{\mathrm{CW}}(Y))&\xrightarrow{\Theta_{Y,n}}&H_n(Y)
\end{array}
$$

komutatif. Jika $f$ hanya kontinu, teorema pendekatan seluler memberi
$f_{\mathrm{sel}}\simeq f$. Dua pendekatan seluler memberi pemetaan yang sama
pada homologi setelah diagram ini, sebab keduanya sama dengan $H_n(f)$ pada
homologi singular. Ini membuktikan pernyataan kealamian yang diklaim.
$\square$
:::

::: {.proof-check #o012-fom-u007-check-pr14 data-origin="edition-original" data-repair-id="FOM-PR-14"}
**Pemeriksaan internal FOM-PR-14.** (i) Semua domain dan kodomain pada
$d_n=\rho_{n-1}\delta_n$ cocok; (ii) $d^2=0$ berasal dari dua panah berurutan
dalam barisan eksak, bukan dari manipulasi simbolik tanpa tipe; (iii) baris
tunggal kopel eksak menghasilkan kompleks seluler dan halaman keduanya;
(iv) rumus kernel–citra (14.4)–(14.5) membuktikan konvergensi tanpa
menyembunyikan asumsi hingga; (v) kasus derajat nol ditangani secara
eksplisit; (vi) diagram (14.7) dan (14.6) membuktikan kealamian pemetaan,
bukan hanya keisomorfisan grup.
:::
:::

::: {.proof-repair-module #o012-fom-u007-repair-pr15 data-origin="edition-original" data-source-lines="3642-3664" data-repair-id="FOM-PR-15" data-proof-status="complete_original_repair"}
## FOM-PR-15 — rumus bilangan insidensi seluler

::: {.theorem #o012-fom-u007-thm-cellular-incidence data-origin="edition-original" data-source-lines="3642-3664" data-repair-id="FOM-PR-15"}
**Teorema (rumus bilangan insidensi).** Pilih orientasi pada setiap sel CW.
Untuk $n\geq1$ dan sel-$n$ $e^n_\alpha$, tuliskan

$$
\Phi_\alpha\colon(D^n_\alpha,S^{n-1}_\alpha)\longrightarrow
(X^{(n)},X^{(n-1)})
$$

untuk pemetaan karakteristik dan
$\varphi_\alpha=\Phi_\alpha|_{S^{n-1}_\alpha}$ untuk peta pelekatan sel
tersebut.
Untuk setiap sel-$(n-1)$ $e^{n-1}_\beta$, bentuk komposisi

$$
\varphi_{\alpha\beta}\colon
S^{n-1}_\alpha
\xrightarrow{\ \varphi_\alpha\ }
X^{(n-1)}
\xrightarrow{\ Q\ }
X^{(n-1)}/X^{(n-2)}
\cong\bigvee_{\delta\in I_{n-1}}S^{n-1}_\delta
\xrightarrow{\ P_\beta\ }S^{n-1}_\beta,
\tag{15.1}
$$

dengan $P_\beta$ meruntuhkan semua suku baji berindeks
$\delta\ne\beta$. Untuk $n=1$, hasil bagi pada (15.1) dibaca sebagai
$X^{(0)}$ dengan satu titik pangkal terpisah; homologi tereduksinya sama
dengan $H_0(X^{(0)})$, dan derajat peta $S^0\to S^0$ dibaca pada
$\widetilde H_0$.

Jika $[\Phi_\alpha]$ dan $[\Phi_\beta]$ adalah pembangkit seluler yang
ditentukan orientasi, maka

$$
d_n[\Phi_\alpha]
=\sum_{\beta\in I_{n-1}}
\deg(\varphi_{\alpha\beta})[\Phi_\beta].
\tag{15.2}
$$

Hanya berhingga banyak suku pada (15.2) yang taknol.
:::

::: {.proof #o012-fom-u007-proof-pr15 data-origin="edition-original" data-source-lines="3642-3664" data-repair-id="FOM-PR-15" data-proof-status="complete_original_repair"}
**Bukti.** Orientasikan $S^{n-1}_\alpha=\partial D^n_\alpha$ dengan konvensi
normal-ke-luar-lebih-dahulu. Pembangkit yang bersesuaian adalah

$$
[\Phi_\alpha]
=(\Phi_\alpha)_*[D^n_\alpha,S^{n-1}_\alpha]
\in H_n(X^{(n)},X^{(n-1)}).
$$

Kealamian pemetaan penghubung bagi pemetaan pasangan $\Phi_\alpha$ memberi

$$
\delta_n[\Phi_\alpha]
=(\varphi_\alpha)_*[S^{n-1}_\alpha]
\in H_{n-1}(X^{(n-1)}).
\tag{15.3}
$$

Tidak ada tanda tambahan pada (15.3), karena orientasi batas sudah ditentukan
oleh konvensi normal-ke-luar-lebih-dahulu.

Sekarang terapkan

$$
\rho_{n-1}\colon H_{n-1}(X^{(n-1)})\longrightarrow
H_{n-1}(X^{(n-1)},X^{(n-2)}).
$$

Di bawah isomorfisma hasil bagi dan pemisahan menurut suku baji,

$$
\kappa\colon
H_{n-1}(X^{(n-1)},X^{(n-2)})
\xrightarrow{\cong}
\bigoplus_{\beta\in I_{n-1}}
\widetilde H_{n-1}(S^{n-1}_\beta),
\tag{15.4}
$$

pemetaan $\rho_{n-1}$ menjadi pemetaan yang diinduksi $Q$. Orientasi
sel-$(n-1)$ ke-$\beta$ dipilih sehingga

$$
\kappa([\Phi_\beta])=[S^{n-1}_\beta]
$$

pada komponen ke-$\beta$. Proyeksikan (15.3) ke komponen itu. Dengan
kealamian (15.4), kita memperoleh

$$
\begin{aligned}
\operatorname{pr}_\beta\!\left(
\kappa\rho_{n-1}\delta_n[\Phi_\alpha]
\right)
&=(P_\beta Q\varphi_\alpha)_*[S^{n-1}_\alpha]\\
&=(\varphi_{\alpha\beta})_*[S^{n-1}_\alpha]\\
&=\deg(\varphi_{\alpha\beta})[S^{n-1}_\beta].
\end{aligned}
\tag{15.5}
$$

Namun $d_n=\rho_{n-1}\delta_n$ menurut definisi. Karena (15.5) menghitung
setiap koordinat dalam penjumlahan langsung (15.4), penggabungan semua
koordinat memberi tepat (15.2).

Untuk $n=1$, kelas fundamental tereduksi dari $S^0=\partial D^1$ adalah
selisih titik ujung positif dan negatif. Meruntuhkan semua simpul selain
$\beta$ ke titik pangkal mengirim selisih itu ke
$\deg(\varphi_{\alpha\beta})$ kali pembangkit
$\widetilde H_0(S^0)$. Jadi argumen yang sama menghasilkan koefisien
insidensi bertanda pada batas sel-$1$.

Akhirnya, citra kompak $\varphi_\alpha(S^{n-1}_\alpha)$ termuat dalam suatu
subkompleks hingga dari $X^{(n-1)}$. Untuk setiap $\beta$ di luar
subkompleks itu, $P_\beta Q\varphi_\alpha$ konstan dan berderajat nol. Maka
jumlah (15.2) mempunyai dukungan hingga. $\square$
:::

::: {.proof-check #o012-fom-u007-check-pr15 data-origin="edition-original" data-repair-id="FOM-PR-15"}
**Pemeriksaan internal FOM-PR-15.** (i) Domain dan kodomain komposisi
(15.1) sama-sama sfera berdimensi $n-1$, bukan $n$; (ii) penyebut hasil bagi
meruntuhkan suku berindeks $\delta\ne\beta$, bukan mengulang suku
$\beta$; (iii) koefisien diturunkan dari pemetaan penghubung dan proyeksi
hasil bagi sebelum disebut “derajat”; (iv) pilihan orientasi dan tanda batas
ditetapkan; membalik orientasi sel sumber atau sasaran mengubah basis dan
derajat dengan tanda yang sama, sehingga (15.2) tetap benar; (v) kasus
$n=1$ dan keterhinggaan jumlah diperiksa terpisah.
:::
:::

::: {.boundary #o012-fom-u007-proof-repairs-draft-boundary data-origin="edition-original"}
**Batas draf.** Dokumen ini hanya memuat FOM-PR-13, FOM-PR-14, dan
FOM-PR-15. Ia tidak mengubah terjemahan kanonik Unit 007, backend, ledger,
kontrol rilis, atau artefak publik. Ketiga modul siap diintegrasikan setelah
peninjauan independen terhadap notasi di pembaca Unit 007.
:::
