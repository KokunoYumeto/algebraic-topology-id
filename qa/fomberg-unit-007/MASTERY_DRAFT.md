---
unit_id: O012-FOM-007
course_route_unit_id: D60-R12
language: id-ID
data-origin: edition-original
status: mastery-draft
---

## Pemeriksaan penguasaan {#o012-fom-u007-mastery data-origin="edition-original" data-course-route-unit-id="D60-R12"}

Enam pemeriksaan berikut merupakan materi asli edisi ini. Masing-masing
memuat petunjuk dan solusi lengkap agar dapat dipakai untuk belajar mandiri.
Tidak ada soal yang disalin dari bank soal Fomberg terpisah.

::: {.exercise #o012-fom-u007-mcheck-001 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F7.1 (membangun kompleks rantai seluler).**
Mulailah dengan baji dua lingkaran

$$
X^{(1)}=S^1_a\vee S^1_b
$$

yang mempunyai satu sel-$0$ $v$ dan dua sel-$1$ berorientasi $a,b$.
Lekatkan dua sel-$2$ $p,q$ dengan kata pelekatan

$$
w_p=a^2b^{-1},
\qquad
w_q=ab^2.
$$

Tidak ada sel berdimensi lebih tinggi.

1. Tuliskan $C_n^{\mathrm{CW}}(X)$ beserta basisnya untuk setiap $n$.
2. Hitung matriks $d_2$ terhadap basis terurut $(p,q)$ pada domain dan
   $(a,b)$ pada kodomain. Jelaskan hubungan koefisien matriks dengan derajat
   peta insidensi.
3. Hitung $d_1$ dan periksa $d_1d_2=0$.
4. Tentukan semua kelompok homologi integral $H_n(X;\mathbb Z)$ dengan
   mereduksi matriks $d_2$ ke bentuk normal Smith.
:::

::: {.hint #o012-fom-u007-hint-001 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Petunjuk.** Setelah semua lingkaran selain $a$ diruntuhkan, derajat peta
$S^1\to S^1_a$ sama dengan jumlah eksponen $a$ dalam kata pelekatan;
demikian pula untuk $b$. Untuk bentuk normal Smith, tukarkan kedua kolom,
lalu gunakan operasi baris dan kolom unimodular.
:::

::: {.solution #o012-fom-u007-sol-001 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Solusi Pemeriksaan F7.1.** Satu sel-$0$, dua sel-$1$, dan dua sel-$2$
memberi

$$
C_2^{\mathrm{CW}}(X)=\mathbb Z\langle p,q\rangle,
\qquad
C_1^{\mathrm{CW}}(X)=\mathbb Z\langle a,b\rangle,
\qquad
C_0^{\mathrm{CW}}(X)=\mathbb Z\langle v\rangle,
$$

sedangkan $C_n^{\mathrm{CW}}(X)=0$ untuk $n\notin\{0,1,2\}$.
Koefisien insidensi sebuah sel-$2$ terhadap sebuah sel-$1$ adalah derajat
komposisi

$$
S^1\xrightarrow{\ \varphi\ }X^{(1)}
\longrightarrow X^{(1)}/(X^{(1)}\setminus e^1)
\cong S^1.
$$

Untuk kata pada baji lingkaran, derajat ini adalah jumlah eksponen huruf
yang bersangkutan. Karena

$$
\begin{array}{c|cc}
 & a&b\\ \hline
w_p=a^2b^{-1}&2&-1\\
w_q=ab^2&1&2
\end{array},
$$

kita memperoleh

$$
d_2(p)=2a-b,
\qquad
d_2(q)=a+2b,
\qquad
[d_2]_{(a,b)\leftarrow(p,q)}=
\begin{pmatrix}2&1\\-1&2\end{pmatrix}.
$$

Kedua ujung setiap sel-$1$ melekat pada simpul yang sama, sehingga
$d_1(a)=d_1(b)=v-v=0$. Jadi $d_1d_2=0$.

Untuk menghitung hasil bagi, lakukan operasi unimodular

$$
\begin{pmatrix}2&1\\-1&2\end{pmatrix}
\sim
\begin{pmatrix}1&2\\2&-1\end{pmatrix}
\sim
\begin{pmatrix}1&2\\0&-5\end{pmatrix}
\sim
\begin{pmatrix}1&0\\0&5\end{pmatrix}.
$$

Determinan matriks semula adalah $5$, sehingga $d_2$ injektif dan
$\ker d_2=0$. Bentuk normal Smith menunjukkan

$$
\operatorname{coker}d_2
\cong \mathbb Z/1\mathbb Z\oplus\mathbb Z/5\mathbb Z
\cong\mathbb Z/5\mathbb Z.
$$

Akibatnya

$$
H_n(X;\mathbb Z)\cong
\begin{cases}
\mathbb Z,&n=0,\\
\mathbb Z/5\mathbb Z,&n=1,\\
0,&n\geq2.
\end{cases}
$$
:::

::: {.exercise #o012-fom-u007-mcheck-002 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F7.2 (lemma kerangka).** Misalkan $X$ adalah
kompleks CW berdimensi hingga dan $X^{(m)}$ adalah $m$-kerangkanya. Gunakan

$$
H_j\bigl(X^{(m)},X^{(m-1)}\bigr)\cong
\begin{cases}
\displaystyle\bigoplus_{e^m_\alpha}\mathbb Z[e^m_\alpha],&j=m,\\
0,&j\ne m,
\end{cases}
$$

bersama barisan eksak panjang pasangan untuk membuktikan:

1. $H_k(X^{(n)})=0$ untuk $k>n$;
2. inklusi $X^{(n)}\hookrightarrow X$ menginduksi isomorfisma pada $H_k$
   untuk $k<n$ dan epimorfisma pada $H_n$;
3. klaim epimorfisma pada derajat $n$ tidak dapat, secara umum, diperkuat
   menjadi isomorfisma. Berikan satu contoh CW yang eksplisit.

Terakhir, jelaskan secara singkat bagaimana argumen meluas ke kompleks CW
berdimensi tak hingga.
:::

::: {.hint #o012-fom-u007-hint-002 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Petunjuk.** Untuk pasangan $(X^{(m)},X^{(m-1)})$, lihat tiga suku
berturutan pada derajat $k+1,k,k-1$. Ketika sel-$m$ dilekatkan, homologi
derajat $k<m-1$ tidak berubah dan homologi derajat $m-1$ hanya dapat
berkurang. Untuk contoh terakhir, lekatkan satu sel-$(n+1)$ pada $S^n$
melalui peta identitas.
:::

::: {.solution #o012-fom-u007-sol-002 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Solusi Pemeriksaan F7.2.** Barisan eksak panjang pasangan memuat

$$
H_{k+1}(X^{(m)},X^{(m-1)})\longrightarrow
H_k(X^{(m-1)})\longrightarrow H_k(X^{(m)})\longrightarrow
H_k(X^{(m)},X^{(m-1)}).
$$

Jika $k>m$, kedua kelompok relatif di ujung bernilai nol. Maka
$H_k(X^{(m-1)})\to H_k(X^{(m)})$ adalah isomorfisma. Mengulang proses
sampai $X^{(0)}$ memberi

$$
H_k(X^{(m)})\cong H_k(X^{(0)})=0
\qquad(k>m),
$$

karena $X^{(0)}$ diskret dan tidak mempunyai homologi positif.

Sekarang tetapkan $n$ dan lekatkan sel-sel dalam urutan kerangka. Pada
langkah pertama,

$$
X^{(n)}\hookrightarrow X^{(n+1)},
$$

kelompok relatif hanya mungkin tak nol pada derajat $n+1$. Karena itu
inklusi tersebut merupakan isomorfisma pada $H_k$ untuk $k<n$ dan
epimorfisma pada $H_n$. Pada setiap langkah berikutnya $m>n+1$, kedua
kelompok relatif yang mengapit $H_k$ lenyap untuk $k\le n$, sehingga
inklusinya merupakan isomorfisma pada derajat-derajat itu. Komposisi
memberi

$$
H_k(X^{(n)})\xrightarrow{\ \cong\ }H_k(X)quad(k<n),
\qquad
H_n(X^{(n)})\twoheadrightarrow H_n(X).
$$

Epimorfisma terakhir dapat mempunyai kernel. Ambil $X^{(n)}=S^n$ dan
lekatkan satu sel-$(n+1)$ melalui peta identitas
$S^n\to S^n$. Ruang hasilnya adalah $D^{n+1}$, sehingga

$$
H_n(X^{(n)})\cong\mathbb Z,
\qquad
H_n(X)=0.
$$

Jadi sel-$(n+1)$ dapat membunuh kelas homologi berdimensi $n$.

Untuk kompleks CW berdimensi tak hingga, setiap rantai singular hanya
memakai berhingga banyak simpleks dan citranya kompak. Sifat
closure-finite dan topologi lemah CW menempatkan dukungan tersebut di
subkompleks hingga. Dengan mengambil limit terarah atas subkompleks hingga,
argumen yang sama memberi kesimpulan pada setiap derajat tetap.
:::

::: {.exercise #o012-fom-u007-mcheck-003 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F7.3 (rumus insidensi dan perubahan orientasi).**
Sebuah kompleks CW $Y$ mempunyai satu sel-$0$, tiga sel-$1$ berorientasi
$e_1,e_2,e_3$, serta dua sel-$2$ berorientasi $x_1,x_2$. Kata pelekatannya
adalah

$$
w_{x_1}=e_1e_3^{-1},
\qquad
w_{x_2}=e_1^{-2}e_2^3e_3.
$$

1. Gunakan rumus derajat insidensi untuk menghitung matriks $d_2$ terhadap
   basis $(x_1,x_2)$ dan $(e_1,e_2,e_3)$.
2. Balik orientasi $x_1$ dan $e_2$, tanpa mengubah orientasi sel lain.
   Hitung matriks baru dan nyatakan sebagai perkalian matriks tanda di kiri
   dan kanan matriks lama.
3. Buktikan secara konseptual bahwa perubahan orientasi sel mana pun tidak
   mengubah homologi seluler.
4. Sebagai pemeriksaan, hitung $H_2(Y)$ dan $H_1(Y)$ sebelum maupun sesudah
   perubahan orientasi.
:::

::: {.hint #o012-fom-u007-hint-003 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Petunjuk.** Meruntuhkan semua sel-$1$ kecuali $e_i$ mengubah kata
pelekatan menjadi peta $S^1\to S^1_{e_i}$; derajatnya adalah jumlah
eksponen $e_i$. Membalik orientasi sel domain mengalikan satu kolom dengan
$-1$, sedangkan membalik orientasi sel kodomain mengalikan satu baris
dengan $-1$.
:::

::: {.solution #o012-fom-u007-sol-003 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Solusi Pemeriksaan F7.3.** Jumlah eksponen pada kedua kata ialah

$$
x_1:(1,0,-1),
\qquad
x_2:(-2,3,1).
$$

Dengan baris berurutan $(e_1,e_2,e_3)$ dan kolom berurutan $(x_1,x_2)$,

$$
A=[d_2]=
\begin{pmatrix}
1&-2\\
0&3\\
-1&1
\end{pmatrix}.
$$

Ini tepat merupakan rumus

$$
d_2(x_j)=\sum_i\deg(\varphi_{x_je_i})e_i,
$$

dengan $\varphi_{x_je_i}$ diperoleh dengan meruntuhkan semua sel-$1$
selain $e_i$.

Tuliskan basis baru $x'_1=-x_1$, $x'_2=x_2$ dan
$e'_1=e_1$, $e'_2=-e_2$, $e'_3=e_3$. Perubahan koordinat memberi

$$
A'=
\underbrace{\begin{pmatrix}1&0&0\\0&-1&0\\0&0&1\end{pmatrix}}_{P}
A
\underbrace{\begin{pmatrix}-1&0\\0&1\end{pmatrix}}_{Q}
=
\begin{pmatrix}
-1&-2\\
0&-3\\
1&1
\end{pmatrix}.
$$

Matriks $P$ dan $Q$ unimodular dan inversnya sama dengan dirinya. Secara
abstrak, perubahan orientasi hanya mengganti basis bebas kelompok rantai.
Isomorfisma rantai yang diberikan oleh perubahan basis membawa kernel ke
kernel dan citra ke citra; karena itu hasil bagi
$\ker d_n/\operatorname{im}d_{n+1}$ tidak berubah.

Karena terdapat satu simpul, $d_1=0$. Kedua kolom $A$ bebas linear
(misalnya minor dua baris pertama bernilai $3$), sehingga
$H_2(Y)=\ker A=0$. Pembagi elementer pertama adalah FPB semua entri, yakni
$1$. FPB semua minor berukuran $2$ adalah

$$
\gcd(3,-1,3)=1,
$$

sehingga bentuk normal Smith $A$ mempunyai dua entri diagonal $1,1$.
Dengan demikian

$$
H_1(Y)=\mathbb Z^3/\operatorname{im}A\cong\mathbb Z.
$$

Matriks $A'=PAQ$ mempunyai bentuk normal Smith yang sama, jadi perhitungan
setelah pembalikan orientasi memberi kelompok yang sama.
:::

::: {.exercise #o012-fom-u007-mcheck-004 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F7.4 (torus dan permukaan genus-$g$).** Untuk
$g\geq1$, berikan $\Sigma_g$ struktur CW dengan satu sel-$0$ $v$, sel-$1$

$$
a_1,b_1,\ldots,a_g,b_g,
$$

dan satu sel-$2$ $\Delta$ yang dilekatkan melalui kata

$$
w_g=\prod_{i=1}^{g}[a_i,b_i],
\qquad
[a_i,b_i]=a_ib_ia_i^{-1}b_i^{-1}.
$$

1. Tuliskan seluruh kompleks rantai selulernya dan kedua matriks batas
   yang mungkin tak sepele.
2. Hitung $H_n(\Sigma_g;\mathbb Z)$ untuk semua $n$.
3. Khususkan jawaban pada $g=1$ untuk memperoleh homologi torus.
4. Periksa jawaban dengan karakteristik Euler dan jelaskan bagaimana
   $H_1$ membedakan genus permukaan-permukaan ini.
:::

::: {.hint #o012-fom-u007-hint-004 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Petunjuk.** Setiap huruf $a_i$ maupun $b_i$ muncul satu kali dengan
eksponen $+1$ dan satu kali dengan eksponen $-1$. Karena semua sel-$1$
berawal dan berakhir di $v$, $d_1$ juga nol.
:::

::: {.solution #o012-fom-u007-sol-004 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Solusi Pemeriksaan F7.4.** Kelompok rantainya adalah

$$
0\longrightarrow
C_2=\mathbb Z\langle\Delta\rangle
\xrightarrow{d_2}
C_1=\bigoplus_{i=1}^{g}
\bigl(\mathbb Z\langle a_i\rangle\oplus
\mathbb Z\langle b_i\rangle\bigr)
\xrightarrow{d_1}
C_0=\mathbb Z\langle v\rangle
\longrightarrow0.
$$

Karena setiap gelung mempunyai kedua ujung pada $v$, matriks $d_1$ adalah
matriks nol berukuran $1\times2g$. Koefisien insidensi $d_2$ adalah jumlah
eksponen pada $w_g$. Semua jumlah tersebut nol, sehingga

$$
[d_2]_{(a_1,b_1,\ldots,a_g,b_g)\leftarrow(\Delta)}
=
\begin{pmatrix}0\\0\\\vdots\\0\end{pmatrix}_{2g\times1}.
$$

Jadi

$$
H_n(\Sigma_g;\mathbb Z)\cong
\begin{cases}
\mathbb Z,&n=0,2,\\
\mathbb Z^{2g},&n=1,\\
0,&\text{selain itu}.
\end{cases}
$$

Untuk $g=1$, kata pelekatannya
$aba^{-1}b^{-1}$ dan diperoleh

$$
H_0(T^2)=\mathbb Z,
\qquad H_1(T^2)=\mathbb Z^2,
\qquad H_2(T^2)=\mathbb Z.
$$

Hitungan sel memberi

$$
\chi(\Sigma_g)=1-2g+1=2-2g,
$$

sedangkan jumlah berselang-seling peringkat homologi memberi nilai yang
sama: $1-2g+1$. Terakhir,
$\operatorname{rank}H_1(\Sigma_g)=2g$, sehingga genus dapat dipulihkan
sebagai setengah peringkat $H_1$.
:::

::: {.exercise #o012-fom-u007-mcheck-005 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F7.5 (botol Klein dan kata pelekatan yang
dibaca dari polygon sumber).** Pertahankan struktur CW polygon pada sumber:
botol Klein $K$ mempunyai satu sel-$0$ $v$, dua sel-$1$ berorientasi $a,b$,
dan satu sel-$2$ $\Delta$. Jika batas persegi ditelusuri dengan mengikuti
panah yang benar-benar digambar pada sumber, kata pelekatannya siklik
ekuivalen dengan

$$
w_{\mathrm{sumber}}=b^2a^2
$$

(atau inversnya jika orientasi $\Delta$ dibalik).

1. Hitung kolom matriks $d_2$ dari jumlah eksponen $a$ dan $b$, serta
   jelaskan pengaruh pembalikan orientasi $\Delta$.
2. Hitung $H_2(K;\mathbb Z)$, $H_1(K;\mathbb Z)$, dan
   $H_0(K;\mathbb Z)$, dengan menampilkan kernel dan citra yang digunakan.
3. Lakukan perubahan basis unimodular

   $$u=a,\qquad v=a+b,$$

   lalu tuliskan $d_2$ dan $H_1$ dalam basis $(u,v)$.
4. Bandingkan dengan dekomposisi persegi berhadapan yang lebih lazim,
   dengan pembangkit $x,y$ dan kata $xyx^{-1}y$. Bangun isomorfisma
   eksplisit antara kedua kompleks rantai seluler. Sebagai pemeriksaan yang
   lebih kuat, berikan perubahan pembangkit yang menghubungkan kedua
   presentasi kelompok.
:::

::: {.hint #o012-fom-u007-hint-005 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Petunjuk.** Pada $b^2a^2$, jumlah eksponen kedua huruf adalah $2$.
Karena $b=v-u$, vektor $2a+2b$ menjadi $2v$. Untuk dekomposisi standar,
$d_2$ mengirim pembangkit sel-$2$ ke $2y$. Pada tingkat grup, cobalah
$x=a$ dan $y=a^{-1}b^{-1}$; invers relator yang dihasilkan merupakan
pergeseran siklik dari $a^2b^2$.
:::

::: {.solution #o012-fom-u007-sol-005 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Solusi Pemeriksaan F7.5.** Kompleks rantainya ialah

$$
0\longrightarrow\mathbb Z\langle\Delta\rangle
\xrightarrow{d_2}
\mathbb Z\langle a\rangle\oplus\mathbb Z\langle b\rangle
\xrightarrow{d_1}
\mathbb Z\langle v\rangle\longrightarrow0.
$$

Karena $a$ dan $b$ adalah gelung pada $v$, $d_1=0$. Dari kata yang dibaca
langsung pada polygon sumber,

$$
\operatorname{exp}_a(b^2a^2)=2,
\qquad
\operatorname{exp}_b(b^2a^2)=2,
$$

diperoleh

$$
d_2(\Delta)=2a+2b=2(a+b),
\qquad
[d_2]_{(a,b)\leftarrow(\Delta)}=
\begin{pmatrix}2\\2\end{pmatrix}.
$$

Jika orientasi $\Delta$ dibalik, seluruh kolom dikalikan dengan $-1$;
kernel dan citranya tidak berubah.

Dengan demikian

$$
\ker d_2=0,
\qquad
\operatorname{im}d_2=\mathbb Z(2,2),
\qquad
\ker d_1=\mathbb Z^2.
$$

Maka

$$
H_2(K)=0,
\qquad
H_1(K)=\frac{\mathbb Z a\oplus\mathbb Z b}{\langle2(a+b)\rangle},
\qquad
H_0(K)=\mathbb Z.
$$

Perubahan basis yang diminta mempunyai matriks

$$
U=
\begin{pmatrix}1&1\\0&1\end{pmatrix},
\qquad
\det U=1,
$$

dengan kolom-kolom berupa koordinat $u=a$ dan $v=a+b$ terhadap basis lama.
Karena $b=v-u$,

$$
d_2(\Delta)=2u+2(v-u)=2v.
$$

Oleh sebab itu

$$
H_1(K)
\cong
\frac{\mathbb Zu\oplus\mathbb Zv}{\langle2v\rangle}
\cong\mathbb Z\langle u\rangle\oplus
\mathbb Z/2\mathbb Z\langle v\rangle.
$$

Sekarang ambil dekomposisi persegi berhadapan yang lazim dengan kata
$xyx^{-1}y$. Jumlah eksponennya adalah $(0,2)$, jadi kompleks rantainya
mempunyai $d_2^{\mathrm{std}}(\Delta_{\mathrm{std}})=2y$. Isomorfisma
rantai yang paling langsung diberikan oleh

$$
F_0(v_{\mathrm{std}})=v,
\qquad
F_1(x)=u,
\qquad
F_1(y)=v,
\qquad
F_2(\Delta_{\mathrm{std}})=\Delta.
$$

Memang,

$$
F_1d_2^{\mathrm{std}}(\Delta_{\mathrm{std}})
=F_1(2y)=2v
=d_2F_2(\Delta_{\mathrm{std}}),
$$

dan semua pemetaan batas lain nol. Jadi $F_*$ merupakan isomorfisma
kompleks rantai dan menginduksi isomorfisma homologi yang ditampilkan di
atas.

Hubungan pada tingkat presentasi kelompok juga dapat dibuat eksplisit.
Dalam grup bebas, tetapkan

$$
x=a,
\qquad
y=a^{-1}b^{-1};
$$

perubahan ini invertibel karena $a=x$ dan $b=y^{-1}x^{-1}$. Relator
standar berubah menjadi

$$
xyx^{-1}y
=b^{-1}a^{-2}b^{-1}.
$$

Inversnya, $ba^2b$, adalah pergeseran siklik dari $a^2b^2$, yang sendiri
merupakan pergeseran siklik dari $b^2a^2$. Jadi keduanya menentukan kelas
konjugasi relator yang sama setelah perubahan pembangkit. Pada
abelianisasi, perubahan ini mengirim $x$ ke $u$ dan $y$ ke $-v$; tanda
tersebut diserap dengan membalik orientasi sel-$2$.
:::

::: {.exercise #o012-fom-u007-mcheck-006 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Pemeriksaan Penguasaan F7.6 (alternasi batas dan homologi
$\mathbb{RP}^n$).** Berikan $\mathbb{RP}^n$ struktur CW standar dengan
satu sel $e^k$ dalam setiap dimensi $0\leq k\leq n$.

1. Tunjukkan bahwa, terhadap orientasi yang serasi, pemetaan batas seluler
   $d_k\colon C_k\to C_{k-1}$ adalah perkalian dengan

   $$1+(-1)^k,$$

   yaitu $d_k=0$ untuk $k$ ganjil dan $d_k=2$ untuk $k$ genap.
2. Hitung $H_j(\mathbb{RP}^n;\mathbb Z)$ untuk semua $j$ dan pisahkan kasus
   $n$ ganjil dari kasus $n$ genap.
3. Tuliskan kompleks rantai dan kelompok homologi secara eksplisit untuk
   $\mathbb{RP}^4$ dan $\mathbb{RP}^5$ sebagai pemeriksaan alternasi.
:::

::: {.hint #o012-fom-u007-hint-006 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Petunjuk.** Setelah $\mathbb{RP}^{k-2}$ diruntuhkan, dua belahan sfera
batas sel-$k$ memetakan ke $S^{k-1}$. Kontribusi derajatnya adalah $1$ dan
derajat peta antipodal pada $S^{k-1}$, yaitu $(-1)^k$. Pada derajat
$0<j<n$, hitung $\ker d_j/\operatorname{im}d_{j+1}$; pada derajat teratas
tidak ada citra dari atas.
:::

::: {.solution #o012-fom-u007-sol-006 data-origin="edition-original" data-course-route-unit-id="D60-R12"}
**Solusi Pemeriksaan F7.6.** Peta pelekatan sel-$k$ adalah penutup ganda

$$
S^{k-1}\longrightarrow\mathbb{RP}^{k-1}.
$$

Setelah $\mathbb{RP}^{k-2}$ diruntuhkan, peta insidensi
$S^{k-1}\to S^{k-1}$ mempunyai dua lembar lokal. Pilih orientasi agar
lembar pertama berderajat $1$. Lembar kedua berbeda melalui peta antipodal
pada $S^{k-1}$, yang berderajat

$$
(-1)^{(k-1)+1}=(-1)^k.
$$

Karena derajat global adalah jumlah derajat lokal,

$$
d_k=1+(-1)^k=
\begin{cases}
0,&k\text{ ganjil},\\
2,&k\text{ genap}.
\end{cases}
$$

Jadi kompleks rantainya berupa satu salinan $\mathbb Z$ pada setiap
derajat $0,\ldots,n$, dengan panah yang berselang-seling

$$
\cdots\xrightarrow{0}\mathbb Z
\xrightarrow{2}\mathbb Z
\xrightarrow{0}\mathbb Z
\xrightarrow{2}\mathbb Z
\xrightarrow{0}\mathbb Z.
$$

Untuk $0<j<n$, jika $j$ ganjil maka $\ker d_j=\mathbb Z$ dan
$\operatorname{im}d_{j+1}=2\mathbb Z$, sehingga
$H_j\cong\mathbb Z/2\mathbb Z$. Jika $j$ genap, $d_j$ adalah perkalian
dengan $2$ dan kernelnya nol. Pada dimensi teratas,
$H_n=\ker d_n$ bernilai $\mathbb Z$ bila $n$ ganjil dan nol bila $n$
genap. Dengan demikian, untuk $n\geq1$,

$$
H_j(\mathbb{RP}^n;\mathbb Z)\cong
\begin{cases}
\mathbb Z,&j=0,\\
\mathbb Z/2\mathbb Z,&0<j<n\text{ dan }j\text{ ganjil},\\
\mathbb Z,&j=n\text{ dan }n\text{ ganjil},\\
0,&\text{selain itu}.
\end{cases}
$$

Untuk $\mathbb{RP}^4$,

$$
0\longrightarrow\mathbb Z
\xrightarrow{2}\mathbb Z
\xrightarrow{0}\mathbb Z
\xrightarrow{2}\mathbb Z
\xrightarrow{0}\mathbb Z\longrightarrow0,
$$

sehingga

$$
H_0=\mathbb Z,
\quad H_1=\mathbb Z/2,
\quad H_2=0,
\quad H_3=\mathbb Z/2,
\quad H_4=0.
$$

Untuk $\mathbb{RP}^5$,

$$
0\longrightarrow\mathbb Z
\xrightarrow{0}\mathbb Z
\xrightarrow{2}\mathbb Z
\xrightarrow{0}\mathbb Z
\xrightarrow{2}\mathbb Z
\xrightarrow{0}\mathbb Z\longrightarrow0,
$$

sehingga

$$
H_0=\mathbb Z,
\quad H_1=\mathbb Z/2,
\quad H_2=0,
\quad H_3=\mathbb Z/2,
\quad H_4=0,
\quad H_5=\mathbb Z.
$$
:::
