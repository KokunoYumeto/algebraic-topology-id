---
title: "Laboratorium Komputasi 3 — Batas Seluler dan Derajat"
lang: id-ID
course_id: "D60"
laboratory_id: "D60-LAB03"
license: "CC BY-SA 4.0"
edition_unit_id: "O012-ORIG-LAB03"
course_route_unit_ids: ["D60-R12", "D60-R14"]
origin: "Materi asli edisi; bukan bagian dari sumber Roberts atau Fomberg."
model_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
---

# Laboratorium Komputasi 3 — Batas Seluler dan Derajat {#o012-d60-lab03}

## Status dan keluaran laboratorium {#o012-d60-lab03-status}

Laboratorium ini adalah materi asli edisi. Kita menghubungkan tiga cara
membaca bilangan bulat bertanda yang sama: sebagai koefisien batas seluler,
sebagai koefisien pada kelas fundamental, dan sebagai jumlah derajat lokal
di atas suatu nilai sasaran. Contoh pertama ialah kompleks CW

$$
X_3=S^1_a\cup_{z\mapsto z^3}D^2,
$$

contoh kedua ialah struktur CW minimal pada torus, dan contoh ketiga ialah
keluarga pemetaan torus yang diberikan oleh matriks integral. Semua
perhitungan memakai aritmetika eksak pada bilangan bulat dan pecahan; tidak
ada pembulatan numerik dan tidak diperlukan akses jaringan.

Paket laboratorium memuat program Python berbasis pustaka standar, enam uji
deterministik, keluaran acuan, interpretasi, satu petunjuk bersama, dan solusi
lengkap. Program memeriksa konvensi kolom, jumlah eksponen bertanda, grup
homologi, prabayangan eksak, tanda lokal, urutan komposisi, serta kasus
singular yang sengaja dipilih untuk gagal secara informatif.

## Prasyarat yang dipakai {#o012-d60-lab03-prerequisites}

- definisi dan sifat derajat pada
  [bagian derajat Roberts](../units/unit-030-lecture-030.md#o012-rbt-l30-s04)
  dan [jembatan derajat Fomberg](../fomberg/units/fomberg-unit-005-degree-maps-local-degree.md#o012-fom-u005-s11a);
- rumus penjumlahan derajat lokal pada
  [bagian derajat lokal](../fomberg/units/fomberg-unit-005-degree-maps-local-degree.md#o012-fom-u005-local-degree);
- kompleks CW, pemetaan batas seluler, dan rumus koefisien insidensi pada
  [Homologi Seluler](../fomberg/units/fomberg-unit-007-cellular-homology.md#o012-fom-u007);
- kelas fundamental, orientasi, produk cup, dan funktorialitas homologi serta
  kohomologi;
- matriks integral, determinan, dan aritmetika dalam
  $\mathbb R^2/\mathbb Z^2$.

## Tujuan {#o012-d60-lab03-objectives}

Sesudah menyelesaikan laboratorium ini, pembaca dapat:

1. menghitung koefisien batas seluler dari derajat pemetaan pelekatan;
2. membedakan jumlah eksponen bertanda dari banyaknya kemunculan huruf;
3. memperoleh homologi $X_3$ dan torus dari kompleks rantai selulernya;
4. menjelaskan pengaruh pembalikan orientasi sel terhadap matriks, tetapi
   bukan terhadap grup homologi;
5. menentukan kapan matriks real mendefinisikan pemetaan pada torus;
6. menghitung pemetaan terinduksi pada $H_1(T^2)$ dengan konvensi kolom;
7. membuktikan bahwa derajat pemetaan torus integral sama dengan
   determinannya, bukan menyimpulkannya hanya dari naturalitas batas nol;
8. menemukan prabayangan eksak dan menjumlahkan tanda lokalnya;
9. membedakan urutan matriks pada komposisi pemetaan;
10. mengaudit kasus determinan nol tanpa menyatakan secara keliru bahwa
    setiap serat harus kosong.

## Data, orientasi, dan konvensi kolom {#o012-d60-lab03-data}

Kita tulis $S^1=\mathbb R/\mathbb Z$ dengan koordinat $[t]$ dan
$T^2=\mathbb R^2/\mathbb Z^2$ dengan koordinat kolom $[x]$. Basis berorientasi
$H_1(T^2;\mathbb Z)$ ialah $([a],[b])$, masing-masing berasal dari arah
koordinat pertama dan kedua. Untuk matriks integral $A$, definisikan

$$
f_A([x])=[Ax].
$$

Entri integral bukan sekadar kemudahan komputasional. Jika $x$ diganti oleh
$x+n$ untuk $n\in\mathbb Z^2$, nilai $Ax$ berubah sebesar $An$; pemetaan
turun ke hasil bagi tepat ketika $A\mathbb Z^2\subseteq\mathbb Z^2$, yakni
ketika kolom-kolom $A$ integral.

Empat data uji kanonis ialah sebagai berikut.

1. $X_3$ mempunyai satu sel-$0$ $v$, satu sel-$1$ berorientasi $a$, dan
   satu sel-$2$ $e^2$ yang dilekatkan oleh $q_3([t])=[3t]$.
2. Torus minimal mempunyai satu sel-$0$ $v$, dua sel-$1$ $a,b$, dan satu
   sel-$2$ $\tau$ dengan kata pelekatan
   $aba^{-1}b^{-1}$.
3. Tiga matriks yang diuji ialah

   $$
   M=\begin{pmatrix}2&1\\-1&2\end{pmatrix},\qquad
   N=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
   C=\begin{pmatrix}1&1\\2&2\end{pmatrix}.
   $$

   Dengan konvensi kolom,
   $f_{M*}[a]=2[a]-[b]$ dan $f_{M*}[b]=[a]+2[b]$.
4. Nilai sasaran untuk $M$, $N$, dan komposisi ialah
   $y=(1/7,2/7)$, sedangkan kasus singular memakai
   $y_0=(0,1/3)$.

Kesamaan pada torus selalu berarti kesamaan modulo $\mathbb Z^2$. Karena itu,
$f_A([x])=[y]$ setara dengan adanya $k\in\mathbb Z^2$ sehingga
$Ax=y+k$.

## Batas seluler dan perluasan derajat ke permukaan {#o012-d60-lab03-cellular-boundaries}

Untuk sel-$n$ $e^n_\alpha$ dan sel-$(n-1)$ $e^{n-1}_\beta$, koefisien
$e^{n-1}_\beta$ dalam $d_n(e^n_\alpha)$ adalah derajat komposisi: peta
pelekatan menuju kerangka $(n-1)$, kemudian semua sel selain
$e^{n-1}_\beta$ diruntuhkan. Tanda koefisien bergantung pada orientasi basis.

Pada $X_3$, peta pelekatan mengitari $a$ tiga kali secara positif, sehingga

$$
C_2\xrightarrow{\ d_2=[3]\ }C_1
\xrightarrow{\ d_1=[0]\ }C_0,
\qquad C_2=C_1=C_0=\mathbb Z.
$$

Jika orientasi $e^2$ dibalik sementara orientasi $a$ dipertahankan, kolom
$d_2$ menjadi $[-3]$. Ini adalah perubahan basis unimodular pada $C_2$;
kernel dan hasil bagi yang menentukan homologi tetap isomorfik.

Pada torus minimal, koefisien $a$ dan $b$ dalam batas $\tau$ adalah jumlah
eksponen **bertanda** pada kata $aba^{-1}b^{-1}$:

$$
(+1)+(-1)=0\quad\text{untuk }a,
\qquad
(+1)+(-1)=0\quad\text{untuk }b.
$$

Jadi $d_2(\tau)=0a+0b$ dan $d_1=0$. Menghitung kemunculan tanpa tanda akan
memberi $(2,2)^{\mathsf T}$ dan merupakan kesalahan, bukan konvensi lain.

**Proposisi asli edisi (derajat pada permukaan dan determinan torus).** Jika
$F\colon\Sigma\to\Sigma'$ adalah pemetaan kontinu antara permukaan tertutup,
terhubung, dan berorientasi, definisikan $\deg(F)$ melalui

$$
F_*[\Sigma]=\deg(F)[\Sigma']
\quad\text{dalam }H_2(\Sigma';\mathbb Z).
$$

Definisi ini bebas dari perwakilan siklus setelah orientasi kedua kelas
fundamental ditetapkan. Khusus untuk matriks integral
$A=\bigl(\begin{smallmatrix}p&q\\r&s\end{smallmatrix}\bigr)$, pemetaan
$f_A\colon T^2\to T^2$ mempunyai derajat $\det A$.

**Bukti.** Ambil basis kohomologi dual $\alpha,\beta\in H^1(T^2;\mathbb Z)$
dengan
$\langle\alpha\smile\beta,[T^2]\rangle=1$. Konvensi kolom memberi

$$
f_A^*\alpha=p\alpha+q\beta,
\qquad
f_A^*\beta=r\alpha+s\beta.
$$

Antikomutativitas bergradasi dan
$\alpha\smile\alpha=\beta\smile\beta=0$ menghasilkan

$$
f_A^*(\alpha\smile\beta)
=(ps-qr)(\alpha\smile\beta).
$$

Dengan naturalitas pasangan evaluasi,

$$
\begin{aligned}
\deg(f_A)
&=\langle\alpha\smile\beta,f_{A*}[T^2]\rangle\\
&=\langle f_A^*(\alpha\smile\beta),[T^2]\rangle\\
&=ps-qr=\det A.
\end{aligned}
$$

Ini juga menjelaskan langkah yang tidak boleh dilewati. Aproksimasi seluler
memungkinkan kita mewakili $f_A$ oleh pemetaan rantai seluler dan membaca
$A$ pada $C_1$ serta $H_1$. Namun, karena kedua pemetaan batas torus adalah
nol, persamaan naturalitas batas $dF_*=F_*d$ menerima **setiap** koefisien
bulat pada $C_2$. Persamaan itu sendiri tidak membuktikan bahwa koefisien
teratas adalah $\det A$; argumen kelas fundamental dan produk cup di ataslah
yang memaksanya.

::: {.exercise #o012-d60-lab03-task-001}
**Tugas 1 — jalankan bukti komputasional.** Dari akar repositori, jalankan

```text
python -B source/id-ID/labs/test_o012_d60_lab03_cellular_degree.py
python -B source/id-ID/labs/o012_d60_lab03_cellular_degree.py
```

Pastikan laporan `unittest` berakhir dengan enam uji lulus dan `OK`. Program
pada perintah kedua harus mempunyai aliran galat kosong dan keluaran yang sama
byte demi byte dengan `expected-output-lab03.txt`.
:::

::: {.exercise #o012-d60-lab03-task-002}
**Tugas 2 — turunkan kompleks rantai $X_3$.** Hitung $d_2$ dari derajat
$q_3$, hitung $H_0,H_1,H_2$, lalu balik orientasi sel-$2$ dan jelaskan apa
yang berubah. Untuk nilai $[1/7]\in S^1$, temukan semua prabayangan eksak
di bawah $q_3$ dan jumlahkan derajat lokalnya.
:::

::: {.exercise #o012-d60-lab03-task-003}
**Tugas 3 — audit torus minimal dengan tanda.** Gunakan kata
$aba^{-1}b^{-1}$ untuk menghitung kedua koefisien $d_2(\tau)$. Tunjukkan
secara eksplisit mengapa hitungan tanpa tanda salah. Hitung homologi torus
dan bandingkan mekanismenya dengan homologi $X_3$.
:::

::: {.exercise #o012-d60-lab03-task-004}
**Tugas 4 — pisahkan $H_1$ dari derajat teratas.** Periksa bahwa konvensi
kolom untuk $M$ memberi
$f_{M*}[a]=2[a]-[b]$ dan $f_{M*}[b]=[a]+2[b]$. Jelaskan mengapa
aproksimasi seluler diperlukan untuk pernyataan pada rantai seluler. Lalu
buktikan, tanpa memakai naturalitas batas nol sebagai jalan pintas, bahwa
pemetaan pada $H_2(T^2)$ adalah perkalian dengan $5$.
:::

::: {.exercise #o012-d60-lab03-task-005}
**Tugas 5 — prabayangan, tanda lokal, dan komposisi.** Untuk sasaran
$y=(1/7,2/7)$, tentukan semua prabayangan eksak di bawah $f_M$, prabayangan
di bawah $f_N$, serta semua prabayangan di bawah $f_N\circ f_M$. Tentukan
tanda lokal tiap titik dan cocokkan jumlah bertandanya dengan derajat global.
Hitung pula $NM$ dan $MN$ dan jelaskan mengapa urutannya tidak boleh ditukar.
:::

::: {.exercise #o012-d60-lab03-task-006}
**Tugas 6 — audit kasus negatif.** Tunjukkan bahwa matriks tak integral pada
umumnya tidak mendefinisikan pemetaan torus. Temukan kesalahan dalam argumen
“batas nol memaksa koefisien teratas”, “derajat sama dengan banyaknya
prabayangan”, dan “$\det C=0$ membuat setiap serat kosong”. Terakhir, gunakan
vektor null kiri $(-2,1)$ untuk membuktikan bahwa $y_0=(0,1/3)$ tidak berada
dalam citra $f_C$, tetapi berikan pula satu serat $f_C$ yang tidak kosong.
:::

::: {.hint #o012-d60-lab03-hint}
**Petunjuk.** Pada kata pelekatan, invers menyumbang $-1$, bukan $+1$.
Untuk prabayangan torus, selesaikan $Ax=y+k$ dengan $k\in\mathbb Z^2$ dan
pilih wakil dalam $[0,1)^2$. Jika $\det A\ne0$, setiap titik prabayangan
mempunyai tanda lokal $\operatorname{sgn}(\det A)$ dan banyaknya titik pada
serat ialah $|\det A|$. Untuk komposisi, tulis fungsi pada sebuah kolom:
$f_N(f_M([x]))=[NMx]$. Pada kasus singular, kalikan persamaan
$Cx=y_0+k$ dari kiri dengan $(-2,1)$.
:::

## Program lengkap {#o012-d60-lab03-program}

Berkas kanonis:
[`o012_d60_lab03_cellular_degree.py`](o012_d60_lab03_cellular_degree.py).
Proses pembuatan pembaca mengganti penanda berikut dengan byte sumber tersebut
agar HTML dan PDF tetap mandiri dan agar salinan tampilan tidak dapat
menyimpang dari berkas yang diuji.

O012_LAB03_INCLUDE_PROGRAM

## Uji deterministik lengkap {#o012-d60-lab03-tests}

Berkas kanonis:
[`test_o012_d60_lab03_cellular_degree.py`](test_o012_d60_lab03_cellular_degree.py).

O012_LAB03_INCLUDE_TESTS

## Keluaran acuan {#o012-d60-lab03-expected-output}

Berkas kanonis:
[`expected-output-lab03.txt`](expected-output-lab03.txt).

O012_LAB03_INCLUDE_EXPECTED

## Interpretasi matematis {#o012-d60-lab03-interpretation}

Matriks batas dan matriks pemetaan terinduksi menjawab pertanyaan yang
berbeda. Untuk $X_3$, bilangan $3$ adalah koefisien insidensi dari sel-$2$
ke sel-$1$ dan menghasilkan torsi $\mathbb Z/3\mathbb Z$ pada $H_1$. Untuk
torus minimal, jumlah eksponen bertanda membuat semua batas nol, tetapi ini
tidak berarti bahwa setiap pemetaan torus berderajat nol. Pemetaan $f_A$
membawa informasi tambahan: aksinya pada dua arah lingkaran adalah $A$, dan
aksinya pada orientasi dua-dimensi adalah $\det A$.

Jika $A$ tak singular, $f_A$ adalah penutup berhingga dengan
$|\det A|$ lembar. Determinan positif membuat semua lembar mempertahankan
orientasi; determinan negatif membuat semuanya membalik orientasi. Karena
itu banyaknya prabayangan memberi nilai mutlak derajat, sedangkan jumlah
**bertanda** memberi derajat itu sendiri. Untuk matriks singular, serat dapat
kosong atau berdimensi positif, bergantung pada apakah sasaran berada dalam
citra. Determinan nol hanya menyatakan derajat global nol.

# Solusi lengkap {#o012-d60-lab03-solution}

## Eksekusi dan kontrak keluaran {#o012-d60-lab03-sol-execution}

Perintah pertama memakai konvensi `unittest`: laporan enam uji dan `OK` muncul
pada aliran galat, sedangkan aliran keluarannya kosong. Perintah kedua harus
berhasil dengan aliran galat kosong dan menghasilkan tepat byte UTF-8 dalam
`expected-output-lab03.txt`, termasuk urutan titik, tanda, spasi, dan LF
terakhir. Enam kelompok yang diperiksa ialah $X_3$, torus minimal, pemetaan
$M$, pemetaan $N$, komposisi $NM$, dan kegagalan terkontrol untuk data yang
tidak sah atau singular. Pemeriksaan byte mencegah daftar prabayangan yang
secara matematis setara tetapi tidak kanonis menyamarkan perubahan keluaran.

## Kompleks $X_3$ dan tiga prabayangan {#o012-d60-lab03-sol-x3}

Karena $q_3([t])=[3t]$ berderajat $3$, basis $(e^2,a,v)$ memberi

$$
0\longrightarrow\mathbb Z
\xrightarrow{[3]}\mathbb Z
\xrightarrow{[0]}\mathbb Z
\longrightarrow0.
$$

Maka

$$
H_0(X_3;\mathbb Z)\cong\mathbb Z,
\qquad
H_1(X_3;\mathbb Z)\cong\mathbb Z/3\mathbb Z,
\qquad
H_2(X_3;\mathbb Z)=0.
$$

Membalik orientasi $e^2$ mengganti $[3]$ dengan $[-3]$. Kernel tetap nol
dan citranya tetap $3\mathbb Z$, sehingga homologi tidak berubah.

Untuk $q_3([t])=[1/7]$, persamaan $3t=1/7+m$ dengan $m=0,1,2$ memberi,
dalam urutan menaik,

$$
q_3^{-1}([1/7])=\left\{[1/21],[8/21],[15/21]\right\}.
$$

Di sekitar setiap titik, pengangkatan realnya mempunyai kemiringan positif
$3$, sehingga setiap derajat lokal adalah $+1$. Jumlahnya $3$, sama dengan
derajat global peta pelekatan.

## Kata pelekatan dan homologi torus {#o012-d60-lab03-sol-torus}

Dalam kata $aba^{-1}b^{-1}$, jumlah eksponen $a$ ialah $1-1=0$ dan jumlah
eksponen $b$ juga $1-1=0$. Jadi

$$
d_2=\begin{pmatrix}0\\0\end{pmatrix},
\qquad
d_1=\begin{pmatrix}0&0\end{pmatrix}.
$$

Menghitung empat kemunculan tanpa orientasi akan memberi dua untuk setiap
huruf. Itu mengabaikan bahwa proyeksi peta pelekatan menuju lingkaran $a$
atau $b$ berjalan sekali maju dan sekali mundur; kedua kontribusi derajat
saling meniadakan.

Kompleks rantainya ialah

$$
0\longrightarrow\mathbb Z
\xrightarrow{0}\mathbb Z^2
\xrightarrow{0}\mathbb Z
\longrightarrow0,
$$

sehingga

$$
H_0(T^2;\mathbb Z)\cong\mathbb Z,
\qquad
H_1(T^2;\mathbb Z)\cong\mathbb Z^2,
\qquad
H_2(T^2;\mathbb Z)\cong\mathbb Z.
$$

Berbeda dari $X_3$, torus tidak memperoleh torsi karena citra batas seluler
atasnya nol, bukan subgrup indeks tiga.

## Pemetaan $M,N$, komposisi, dan tanda lokal {#o012-d60-lab03-sol-degree}

Sebuah aproksimasi seluler dari $f_M$ menginduksi pemetaan rantai pada
$C_1$ dengan kolom $M$:

$$
M\binom10=\binom2{-1},
\qquad
M\binom01=\binom12.
$$

Jadi pernyataan pada $H_1$ tepat seperti yang diminta. Determinan
$\det M=2\cdot2-1\cdot(-1)=5$. Bukti produk cup pada bagian sebelumnya,
bukan persamaan naturalitas dengan batas nol, memberi
$f_{M*}[T^2]=5[T^2]$.

Lima prabayangan $y=(1/7,2/7)$ di bawah $f_M$, dalam urutan leksikografis,
beserta vektor bulat $Mx-y$, ialah

$$
\begin{array}{c|c|c}
x&Mx-y&\deg_x(f_M)\\ \hline
(0,1/7)&(0,0)&+1\\
(1/5,26/35)&(1,1)&+1\\
(2/5,12/35)&(1,0)&+1\\
(3/5,33/35)&(2,1)&+1\\
(4/5,19/35)&(2,0)&+1.
\end{array}
$$

Setiap tanda lokal positif karena $\det M>0$, dan jumlahnya $5$.

Matriks $N$ menukar dua koordinat, jadi satu-satunya prabayangan ialah

$$
f_N^{-1}(y)=\{(2/7,1/7)\}.
$$

Karena $\det N=-1$, tanda lokal dan derajat globalnya sama dengan $-1$.

Urutan fungsi memberi

$$
f_N\circ f_M=f_{NM},
\qquad
NM=\begin{pmatrix}-1&2\\2&1\end{pmatrix},
$$

bukan $MN$. Lima prabayangan eksak $y$ di bawah $f_{NM}$ ialah

$$
\begin{array}{c|c|c}
x&(NM)x-y&\deg_x(f_{NM})\\ \hline
(3/35,4/35)&(0,0)&-1\\
(2/7,5/7)&(1,1)&-1\\
(17/35,11/35)&(0,1)&-1\\
(24/35,32/35)&(1,2)&-1\\
(31/35,18/35)&(0,2)&-1.
\end{array}
$$

Jadi jumlah lokalnya $-5$, sesuai
$\det(NM)=\det N\det M=-5$. Dalam urutan sebaliknya,

$$
MN=\begin{pmatrix}1&2\\2&-1\end{pmatrix}.
$$

Kedua komposisi mempunyai derajat $-5$, tetapi matriks dan pemetaannya tidak
sama. Kesamaan determinan tidak mengizinkan pertukaran urutan komposisi.

## Kasus gagal dan serat singular {#o012-d60-lab03-sol-negative}

Jika sebuah kolom $A$ tidak integral, titik $[x]=[x+e_i]$ dapat dikirim ke
dua kelas berbeda karena $Ae_i\notin\mathbb Z^2$. Jadi rumus
$[x]\mapsto[Ax]$ tidak terdefinisi baik pada torus. Berikutnya, naturalitas
batas torus hanya membaca $0=0$ pada derajat dua; ia tidak menentukan
bilangan yang mengalikan generator $C_2$. Bilangan itu diperoleh dari kelas
fundamental. Demikian pula, banyaknya prabayangan tanpa tanda hanya memberi
$|\deg|$ untuk penutup linear tak singular; $N$ mempunyai satu prabayangan,
tetapi derajatnya $-1$.

Untuk

$$
C=\begin{pmatrix}1&1\\2&2\end{pmatrix},
\qquad y_0=(0,1/3),
$$

vektor baris $\lambda=(-2,1)$ memenuhi $\lambda C=(0,0)$. Jika
$Cx=y_0+k$ untuk $k\in\mathbb Z^2$, maka

$$
0=\lambda Cx=\lambda y_0+\lambda k
=\frac13+\text{suatu bilangan bulat},
$$

yang mustahil. Jadi serat di atas $y_0$ kosong. Akan tetapi, serat di atas
$0$ tidak kosong, bahkan memuat seluruh lingkaran

$$
\{[(t,-t)]:t\in\mathbb R\},
$$

karena $C(t,-t)^{\mathsf T}=0$. Dengan demikian $\det C=0$ berarti derajat
global nol; ia tidak membuat setiap serat kosong.

## Pemeriksaan reproduktibilitas {#o012-d60-lab03-reproducibility}

Uji otomatis harus memeriksa:

1. matriks batas $X_3$, homologinya, pembalikan orientasi, tiga prabayangan
   $[1/21],[8/21],[15/21]$, dan jumlah tanda lokal $3$;
2. jumlah eksponen bertanda kata torus, penolakan hitungan tanpa tanda, dan
   homologi $(\mathbb Z,\mathbb Z^2,\mathbb Z)$;
3. syarat entri integral agar $f_A$ terdefinisi baik serta konvensi kolom
   untuk aksi $M$ pada $H_1$;
4. kelima prabayangan $M$, satu prabayangan $N$, tanda lokal, determinan,
   dan aksi yang diwajibkan pada $H_2$;
5. urutan $NM\ne MN$, kelima prabayangan komposisi, jumlah tanda $-5$,
   serta sertifikat null kiri untuk serat kosong $C$;
6. kasus serat singular yang tidak kosong, aliran galat kosong, urutan
   keluaran kanonis, dan kesamaan byte keluaran CLI dengan keluaran acuan
   UTF-8 berakhiran LF.

Semua pecahan dibandingkan sebagai pasangan bilangan bulat tereduksi. Tidak
ada toleransi titik-mengambang yang dapat membuat titik salah tampak benar.
Program juga harus menghitung matriks komposisi dan vektor pemeriksaan
$Ax-y$ dari data, bukan menerima daftar jawaban sebagai satu-satunya bukti.

## Hak, atribusi, dan provenans {#o012-d60-lab03-rights}

Laboratorium, program, uji, keluaran acuan, pembuktian perluasan derajat ke
permukaan, interpretasi, dan solusi ini adalah materi asli edisi dan
didistribusikan di bawah CC BY-SA 4.0. Jangkar konseptual yang dipertahankan
ialah Fomberg `algebraic_topology.tex:2849–2875` untuk definisi/sifat derajat,
`:3037–3114` untuk derajat lokal dan contoh peta pangkat,
`:3612–3664` untuk pemetaan batas seluler, dan `:3740–3845` untuk struktur CW
minimal torus; pembanding Roberts ialah `Notes.tex:6327–6348`. Uraian
penghubung, bukti permukaan, data matriks, tugas, dan solusi di sini ditulis
secara independen dan tidak menyalin ekspresi sumber atau bank masalah yang
dikecualikan.

Produksi dilakukan dengan **OpenAI Codex gpt-5.6-sol, Ultra** atas arahan
pengguna. Kredit, lisensi, dan hubungan sumber David Michael Roberts serta
Yeheli Fomberg tetap dibedakan. Laboratorium ini tidak menyiratkan dukungan
atau pengesahan dari penulis sumber maupun institusi mana pun.
