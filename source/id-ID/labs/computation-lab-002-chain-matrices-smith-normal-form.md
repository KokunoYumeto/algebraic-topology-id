---
title: "Laboratorium Komputasi 2 — Matriks Batas dan Bentuk Normal Smith"
lang: id-ID
course_id: "D60"
laboratory_id: "D60-LAB02"
license: "CC BY-SA 4.0"
edition_unit_id: "O012-ORIG-LAB02"
course_route_unit_ids: ["D60-R08"]
origin: "Materi asli edisi; bukan bagian dari sumber Roberts atau Fomberg."
model_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
---

# Laboratorium Komputasi 2 — Matriks Batas dan Bentuk Normal Smith {#o012-d60-lab02}

## Status dan keluaran laboratorium {#o012-d60-lab02-status}

Laboratorium ini adalah materi asli edisi. Kita mulai dari data simpleks
berhingga, membangun matriks batas integral tanpa jaringan, lalu menghitung
bentuk normal Smith beserta sertifikat perubahan basisnya. Contoh utama ialah
triangulasi enam simpul bidang projektif real
$\mathbb{RP}^2$. Contoh itu cukup kecil untuk diaudit dengan tangan, tetapi
cukup kaya untuk memperlihatkan kelas torsi
$H_1(\mathbb{RP}^2;\mathbb Z)\cong\mathbb Z/2\mathbb Z$.

Paket laboratorium memuat program Python yang hanya memakai pustaka standar, enam uji
deterministik, keluaran acuan, interpretasi matematis, petunjuk, dan solusi
lengkap. Program tidak sekadar mengumumkan grup homologi. Ia memeriksa
$\partial_1\partial_2=0$, menghasilkan matriks unimodular $U,V$, dan
memverifikasi identitas eksak

$$
UAV=D
$$

untuk setiap bentuk normal Smith $D$. Sebuah siklus torsi eksplisit dilengkapi
dua bukti yang berbeda: rantai yang mengisi dua kali siklus itu dan kosiklus
modulo $2$ yang membuktikan bahwa siklusnya sendiri bukan batas.

## Prasyarat yang dipakai {#o012-d60-lab02-prerequisites}

- rantai simpleksial sebagai grup abelian bebas:
  [definisi rantai](#o012-fom-u001-def-007);
- rumus muka berselang-seling:
  [definisi pemetaan batas](#o012-fom-u001-def-boundary) dan
  [contoh sisi serta segitiga](#o012-fom-u001-exa-007);
- syarat kompleks rantai:
  [lema $\partial^2=0$](#o012-fom-u001-lem-boundary-square);
- siklus, batas, dan hasil bagi:
  [siklus](#o012-fom-u001-def-008),
  [batas](#o012-fom-u001-def-009), dan
  [homologi](#o012-fom-u001-def-010);
- contoh reduksi Smith yang lebih kecil tersedia pada
  [Pemeriksaan Penguasaan F7.1](#o012-fom-u007-mcheck-001), tetapi
  laboratorium ini memakai matriks batas simpleksial, bukan matriks batas
  seluler.

## Tujuan {#o012-d60-lab02-objectives}

Sesudah menyelesaikan laboratorium ini, pembaca dapat:

1. mengubah daftar simpleks berorientasi menjadi matriks batas integral;
2. mendeteksi kesalahan tanda dengan menguji
   $\partial_{n-1}\partial_n=0$;
3. memeriksa bahwa data simpleks memang membentuk triangulasi permukaan tertutup;
4. membaca rank bebas dan faktor torsi dari bentuk normal Smith;
5. memeriksa sertifikat Smith, bukan hanya mempercayai diagonal keluaran;
6. membuktikan secara eksplisit bahwa suatu kelas mempunyai orde tepat $2$;
7. menjelaskan mengapa perubahan urutan atau orientasi basis tidak mengubah
   homologi;
8. memakai kontrol tanpa torsi untuk membedakan kesimpulan matematis dari
   artefak program.

## Data simpleks dan konvensi basis {#o012-d60-lab02-data}

Ambil simpul

$$
v_0,v_1,v_2,v_3,v_4,v_5.
$$

Semua sisi $e_{ij}=[v_i,v_j]$ diarahkan dari $i$ ke $j$ untuk $i<j$ dan
diurutkan leksikografis:

$$
\begin{aligned}
(&e_{01},e_{02},e_{03},e_{04},e_{05},
e_{12},e_{13},e_{14},e_{15},\\
&e_{23},e_{24},e_{25},e_{34},e_{35},e_{45}).
\end{aligned}
$$

Sepuluh simpleks-$2$ juga memakai urutan simpul menaik dan basis terurut

$$
\begin{aligned}
(&f_{012},f_{013},f_{024},f_{035},f_{045},\\
&f_{125},f_{134},f_{145},f_{234},f_{235}).
\end{aligned}
$$

Masing-masing dari $\binom62=15$ sisi muncul tepat dua kali dalam kumpulan ini.
Tautan setiap simpul adalah suatu siklus lima sisi. Karena itu realisasi
geometrisnya merupakan permukaan tertutup terhubung. Karakteristik Eulernya
ialah

$$
\chi=6-15+10=1.
$$

Pemeriksaan orientasi menghasilkan kontradiksi di sepanjang siklus pada graf
dual

$$
f_{012},f_{013},f_{035},f_{235},f_{125},f_{012}.
$$

Jadi permukaan itu tidak terorientasi. Klasifikasi permukaan tertutup kemudian
mengenalinya sebagai bidang projektif real.

## Dari muka ke matriks {#o012-d60-lab02-matrices}

Untuk $i<j$,

$$
\partial_1 e_{ij}=v_j-v_i.
$$

Untuk $i<j<k$,

$$
\partial_2 f_{ijk}=e_{jk}-e_{ik}+e_{ij}.
$$

Dengan basis di atas, sepuluh kolom matriks $[\partial_2]$ ditentukan oleh

$$
\begin{array}{rcl@{\qquad}rcl}
\partial f_{012}&=&e_{12}-e_{02}+e_{01},&
\partial f_{013}&=&e_{13}-e_{03}+e_{01},\\
\partial f_{024}&=&e_{24}-e_{04}+e_{02},&
\partial f_{035}&=&e_{35}-e_{05}+e_{03},\\
\partial f_{045}&=&e_{45}-e_{05}+e_{04},&
\partial f_{125}&=&e_{25}-e_{15}+e_{12},\\
\partial f_{134}&=&e_{34}-e_{14}+e_{13},&
\partial f_{145}&=&e_{45}-e_{15}+e_{14},\\
\partial f_{234}&=&e_{34}-e_{24}+e_{23},&
\partial f_{235}&=&e_{35}-e_{25}+e_{23}.
\end{array}
$$

Program membangun kedua matriks langsung dari daftar simpleks dan rumus muka,
bukan dari salinan matriks yang diketik terpisah. Matriks $\partial_1$
berukuran $6\times15$ dan matriks $\partial_2$ berukuran $15\times10$.

::: {.exercise #o012-d60-lab02-task-001}
**Tugas 1 — jalankan bukti komputasional.** Dari akar repositori, jalankan

```text
python -B source/id-ID/labs/test_o012_d60_lab02_smith_normal_form.py
python -B source/id-ID/labs/o012_d60_lab02_smith_normal_form.py
```

Pastikan keenam uji lulus, aliran galat kosong, dan keluaran program sama byte
demi byte dengan `expected-output-lab02.txt`.
:::

::: {.exercise #o012-d60-lab02-task-002}
**Tugas 2 — audit kompleks permukaan.** Hitung banyaknya kemunculan setiap
sisi dalam daftar muka. Tuliskan tautan keenam simpul sebagai siklus. Periksa
$\chi=1$ dan ikuti kendala orientasi di sepanjang siklus dual yang ditampilkan
di atas untuk menunjukkan bahwa permukaan tidak terorientasi.
:::

::: {.exercise #o012-d60-lab02-task-003}
**Tugas 3 — bangun matriks batas.** Bentuk kolom $\partial_1(e_{ij})$ dan
$\partial_2(f_{ijk})$ dalam basis terurut. Kalikan matriksnya dan periksa
$[\partial_1][\partial_2]=0$. Kemudian ubah sengaja satu koefisien kolom
$f_{012}$ dan jelaskan mengapa uji yang sama harus gagal.
:::

::: {.exercise #o012-d60-lab02-task-004}
**Tugas 4 — bentuk normal Smith dan homologi.** Verifikasi keluaran

$$
\operatorname{SNF}(\partial_1)
=\operatorname{diag}(1,1,1,1,1,0),
$$

dan bahwa bagian taknol bentuk normal Smith $\partial_2$ ialah

$$
(1,1,1,1,1,1,1,1,1,2).
$$

Gunakan rank kedua pemetaan dan faktor invarian terakhir untuk menghitung
$H_0,H_1,H_2$ dengan koefisien integral. Periksa pula identitas $UAV=D$,
$|\det U|=|\det V|=1$, bahwa entri diagonal tidak negatif, dan syarat
keterbagian.
:::

::: {.exercise #o012-d60-lab02-task-005}
**Tugas 5 — saksikan torsi, jangan hanya membacanya.** Tetapkan

$$
z=e_{01}-e_{04}+e_{14}.
$$

Periksa $\partial_1z=0$. Temukan rantai-$2$ $c$ dengan
$\partial_2c=2z$. Lalu definisikan korantai modulo $2$ yang bernilai $1$
pada

$$
e_{01},e_{02},e_{13},e_{24},e_{34}
$$

dan bernilai $0$ pada sisi lain. Buktikan bahwa korantai itu mematikan setiap
batas tetapi bernilai $1$ pada $z$. Simpulkan bahwa $[z]$ berorde tepat $2$.
:::

::: {.exercise #o012-d60-lab02-task-006}
**Tugas 6 — perubahan basis dan kontrol.** Susun ulang sisi dan muka lalu
balikkan beberapa orientasi. Bentuk matriks batas baru dengan matriks
permutasi bertanda dan periksa bahwa bentuk normal Smith tidak berubah.
Sebagai kontrol, jalankan perhitungan pada batas tetrahedron. Jelaskan mengapa
kontrol itu memberi $H_0\cong\mathbb Z$, $H_1=0$, dan
$H_2\cong\mathbb Z$ tanpa faktor torsi.
:::

::: {.hint #o012-d60-lab02-hint}
**Petunjuk.** Setiap kolom $\partial_2$ mempunyai pola tanda $+,-,+$.
Pembatalan $\partial_1\partial_2=0$ terjadi per kolom, jadi satu salah tanda
sudah dapat dideteksi. Untuk homologi, gunakan

$$
\operatorname{rank}_{\mathbb Z}H_n^{\mathrm{bebas}}
=\operatorname{rank}C_n
-\operatorname{rank}\partial_n
-\operatorname{rank}\partial_{n+1}.
$$

Torsi $H_n$ dibaca dari faktor invarian lebih besar daripada $1$ pada
$\partial_{n+1}$. Alasannya,
$C_n/\ker\partial_n\cong\operatorname{im}\partial_n$ bebas, sehingga
$\ker\partial_n$ merupakan suku langsung dari $C_n$ dan torsi
$\operatorname{coker}\partial_{n+1}$ tepat sama dengan torsi $H_n$. Untuk
saksi torsi, coba jumlah bertanda kesepuluh muka. Jika $z$ adalah batas
integral, reduksi modulo $2$ juga merupakan batas; pasangan dengan suatu
kosiklus modulo $2$ harus nol.
:::

## Program lengkap {#o012-d60-lab02-program}

Berkas kanonis:
[`o012_d60_lab02_smith_normal_form.py`](o012_d60_lab02_smith_normal_form.py).
Proses pembuatan pembaca mengganti penanda berikut dengan byte sumber tersebut
agar HTML dan PDF tetap mandiri dan agar salinan tampilan tidak dapat
menyimpang dari berkas yang diuji.

O012_LAB02_INCLUDE_PROGRAM

## Uji deterministik lengkap {#o012-d60-lab02-tests}

Berkas kanonis:
[`test_o012_d60_lab02_smith_normal_form.py`](test_o012_d60_lab02_smith_normal_form.py).

O012_LAB02_INCLUDE_TESTS

## Keluaran acuan {#o012-d60-lab02-expected-output}

Berkas kanonis:
[`expected-output-lab02.txt`](expected-output-lab02.txt).

O012_LAB02_INCLUDE_EXPECTED

## Membaca bentuk normal Smith {#o012-d60-lab02-interpretation}

Operasi baris integral unimodular mengganti basis kodomain, sedangkan operasi
kolom integral unimodular mengganti basis domain. Karena keduanya mempunyai
invers integral, perubahan basis tersebut menghasilkan homomorfisma yang sama
hingga isomorfisma. Diagonal Smith

$$
D=\operatorname{diag}(d_1,\ldots,d_r,0,\ldots,0),
\qquad
0<d_1\mid d_2\mid\cdots\mid d_r,
$$

memberi

$$
\operatorname{coker}A
\cong
\mathbb Z^{m-r}
\oplus
\bigoplus_{d_i>1}\mathbb Z/d_i\mathbb Z
$$

untuk $A\colon\mathbb Z^n\to\mathbb Z^m$. Dalam kompleks rantai, kita juga
harus memperhitungkan kernel pemetaan batas keluar. Karena
$C_n/\ker\partial_n\cong\operatorname{im}\partial_n$ bebas,
$\ker\partial_n$ merupakan suku langsung dari $C_n$; akibatnya torsi
$\operatorname{coker}\partial_{n+1}$ tepat sama dengan torsi $H_n$. Jadi rank
bebas $H_n$ memakai kedua rank batas, sedangkan torsi berasal dari faktor
invarian takunit $\partial_{n+1}$.

# Solusi lengkap {#o012-d60-lab02-solution}

## Audit triangulasi {#o012-d60-lab02-sol-surface}

Menghitung kemunculan sisi pada sepuluh muka memberi nilai $2$ untuk semua
15 sisi. Tautan simpul, ditulis sebagai siklus dan mengulang simpul awal pada
akhir, ialah

$$
\begin{array}{c|l}
v_0&(1,2,4,5,3,1)\\
v_1&(0,2,5,4,3,0)\\
v_2&(0,1,5,3,4,0)\\
v_3&(0,1,4,2,5,0)\\
v_4&(0,2,3,1,5,0)\\
v_5&(0,3,2,1,4,0).
\end{array}
$$

Jadi setiap titik mempunyai lingkungan cakram dan tidak ada sisi batas.
Kompleks juga terhubung karena graf kerangka satunya adalah graf lengkap.

Untuk orientasi global, pilih tanda pada $f_{012}$. Melintasi sisi bersama
memaksa tanda muka tetangga agar koefisien sisi saling meniadakan. Pada siklus
dual

$$
f_{012}\xleftrightarrow{e_{01}}f_{013}
\xleftrightarrow{e_{03}}f_{035}
\xleftrightarrow{e_{35}}f_{235}
\xleftrightarrow{e_{25}}f_{125}
\xleftrightarrow{e_{12}}f_{012},
$$

hasil kali lima kendala tanda adalah $-1$. Tanda awal dipaksa menjadi
negatifnya sendiri, sehingga tidak ada orientasi global. Dengan
$\chi=1$, ini adalah permukaan tidak terorientasi genus satu, yaitu
$\mathbb{RP}^2$.

## Matriks batas dan syarat rantai {#o012-d60-lab02-sol-boundaries}

Kolom $e_{ij}$ pada $\partial_1$ mempunyai tepat dua entri taknol: $-1$ pada
baris $v_i$ dan $+1$ pada baris $v_j$. Kolom $f_{ijk}$ pada $\partial_2$
mempunyai koefisien $+1,-1,+1$ pada baris
$e_{jk},e_{ik},e_{ij}$.

Sebagai contoh,

$$
\begin{aligned}
\partial_1\partial_2f_{012}
&=\partial_1(e_{12}-e_{02}+e_{01})\\
&=(v_2-v_1)-(v_2-v_0)+(v_1-v_0)=0.
\end{aligned}
$$

Argumen identik berlaku untuk setiap kolom. Program melakukan perkalian
matriks integral dan memperoleh matriks nol $6\times10$. Uji negatif menambah
$1$ pada koefisien $e_{01}$ di kolom pertama. Kolom komposisi lalu bertambah
$v_1-v_0\ne0$, sehingga pemeriksaan gagal sebagaimana seharusnya.

## Sertifikat Smith dan grup homologi {#o012-d60-lab02-sol-smith}

Reduksi eksak memberi

$$
\operatorname{rank}\partial_1=5,
\qquad
\operatorname{SNF}(\partial_1)_{\ne0}=(1,1,1,1,1),
$$

dan

$$
\operatorname{rank}\partial_2=10,
\qquad
\operatorname{SNF}(\partial_2)
=(1,1,1,1,1,1,1,1,1,2).
$$

Program menyimpan semua operasi sebagai matriks $U,V$. Ia memeriksa
$UAV=D$, determinan $U,V$ sama dengan $\pm1$, semua entri di luar diagonal
nol, diagonal tidak negatif, dan setiap faktor taknol membagi faktor
berikutnya. Karena

$$
\operatorname{rank}C_0=6,
\quad
\operatorname{rank}C_1=15,
\quad
\operatorname{rank}C_2=10,
$$

kita memperoleh rank bebas

$$
6-5=1,
\qquad
15-5-10=0,
\qquad
10-10=0.
$$

Tidak ada faktor torsi pada $\partial_1$, sedangkan faktor terakhir
$\partial_2$ adalah $2$. Maka

$$
H_n(\mathbb{RP}^2;\mathbb Z)
\cong
\begin{cases}
\mathbb Z,&n=0,\\
\mathbb Z/2\mathbb Z,&n=1,\\
0,&n\geq2.
\end{cases}
$$

## Saksi torsi eksplisit {#o012-d60-lab02-sol-torsion}

Untuk

$$
z=e_{01}-e_{04}+e_{14},
$$

kita mempunyai

$$
\partial_1z
=(v_1-v_0)-(v_4-v_0)+(v_4-v_1)=0.
$$

Ambil

$$
\begin{aligned}
c={}&f_{012}+f_{013}+f_{024}+f_{035}-f_{045}\\
&-f_{125}-f_{134}+f_{145}+f_{234}-f_{235}.
\end{aligned}
$$

Menjumlahkan sepuluh kolom batas dengan koefisien tersebut memberi

$$
\partial_2c=2e_{01}-2e_{04}+2e_{14}=2z.
$$

Jadi orde $[z]$ membagi $2$. Untuk membuktikan bahwa ordonya bukan $1$,
definisikan korantai $\alpha\in C^1(-;\mathbb F_2)$ yang bernilai $1$ pada

$$
e_{01},e_{02},e_{13},e_{24},e_{34}
$$

dan nol pada sepuluh sisi lain. Pemeriksaan terhadap kesepuluh kolom
$\partial_2$ memberi $\alpha(\partial_2f)=0$ untuk setiap muka $f$; jadi
$\alpha$ adalah kosiklus modulo $2$ dan mematikan setiap batas integral
setelah reduksi modulo $2$. Namun

$$
\alpha(z)=1\pmod2.
$$

Jika $z=\partial_2b$ untuk suatu rantai integral $b$, maka
$\alpha(z)=\alpha(\partial_2b)=0$, suatu kontradiksi. Karena itu $z$ bukan
batas, sedangkan $2z$ adalah batas. Kelas $[z]$ berorde tepat $2$.

## Perubahan basis dan kontrol sfera {#o012-d60-lab02-sol-control}

Susunan ulang basis dan pembalikan orientasi dinyatakan oleh matriks
permutasi bertanda $P,Q$. Matriks itu unimodular dan inversnya integral.
Jika

$$
\partial_2'=P\partial_2Q,
\qquad
\partial_1'=\partial_1P^{-1},
$$

maka

$$
\partial_1'\partial_2'
=\partial_1P^{-1}P\partial_2Q
=\partial_1\partial_2Q=0.
$$

Uji memakai satu permutasi bertanda tetap pada 15 sisi dan satu lagi pada
10 muka. Bentuk normal Smith keduanya tetap sama; faktor $2$ tidak dapat
dihapus oleh perubahan basis integral.

Kontrol memakai empat muka batas tetrahedron. Ia mempunyai empat simpul,
enam sisi, dan empat muka. Hasilnya

$$
\operatorname{SNF}(\partial_1)_{\ne0}=(1,1,1),
\qquad
\operatorname{SNF}(\partial_2)_{\ne0}=(1,1,1),
$$

sehingga

$$
H_0(S^2;\mathbb Z)\cong\mathbb Z,
\qquad
H_1(S^2;\mathbb Z)=0,
\qquad
H_2(S^2;\mathbb Z)\cong\mathbb Z.
$$

Tidak muncul faktor invarian lebih besar daripada $1$. Kontrol ini menguji
jalur kode yang sama pada permukaan terorientasi tanpa torsi.

## Pemeriksaan reproduktibilitas {#o012-d60-lab02-reproducibility}

Uji otomatis memeriksa:

1. sepuluh muka membentuk permukaan tertutup dengan tautan simpul berupa
   siklus dan tidak menerima data simpleks duplikat;
2. ukuran serta tanda contoh pada kedua matriks batas dan penolakan satu
   kolom yang sengaja dirusak;
3. sertifikat $UAV=D$, unimodularitas, entri diagonal tidak negatif,
   keterbagian, rank, serta satu matriks ber-rank satu tambahan;
4. grup homologi $\mathbb{RP}^2$, rantai pengisi $2z$, dan detektor
   non-batas modulo $2$;
5. invariansi di bawah perubahan urutan/orientasi basis dan kontrol
   $S^2$ tanpa torsi;
6. aliran galat kosong dan keluaran CLI yang sama byte demi byte dengan
   keluaran acuan UTF-8 berakhiran LF.

Dengan demikian keluaran bukan hasil yang diketik ulang. Matriks, diagonal,
sertifikat, saksi torsi, dan kontrol semuanya dihitung dari data simpleks yang
sama dengan data yang disajikan dalam pembaca.

## Hak, atribusi, dan provenans {#o012-d60-lab02-rights}

Laboratorium, program, uji, keluaran acuan, interpretasi, dan solusi ini adalah
materi asli edisi dan didistribusikan di bawah CC BY-SA 4.0. Materi ini memakai
konsep matematika yang sudah dikembangkan dalam edisi Roberts–Fomberg, tetapi
tidak menyalin ekspresi dari bank masalah yang dikecualikan. Produksi dilakukan
dengan **OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna. Kredit,
lisensi, dan hubungan sumber David Michael Roberts serta Yeheli Fomberg tetap
dibedakan; laboratorium ini tidak menyiratkan dukungan atau pengesahan dari
penulis sumber.
