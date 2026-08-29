---
title: "Laboratorium Komputasi 4 — Sintesis Lintas-Invarian"
lang: id-ID
course_id: "D60"
laboratory_id: "D60-LAB04"
license: "CC BY-SA 4.0"
edition_unit_id: "O012-ORIG-LAB04"
course_route_unit_ids: ["D60-R04", "D60-R05", "D60-R12", "D60-R13", "D60-R14"]
origin: "Materi asli edisi; bukan bagian dari sumber Roberts atau Fomberg."
model_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
---

# Laboratorium Komputasi 4 — Sintesis Lintas-Invarian {#o012-d60-lab04}

## Status dan keluaran laboratorium {#o012-d60-lab04-status}

Laboratorium terakhir ini membandingkan grup fundamental, homologi integral,
kohomologi aditif, dan produk cup pada empat kompleks CW yang dibekukan. Dua
pasang ruang sengaja mempunyai beberapa invarian yang sama. Tujuannya bukan
menghasilkan satu “sidik jari lengkap,” melainkan menentukan dengan tepat
informasi apa yang hilang ketika kita beralih dari peta pelekatan ke
diferensial seluler, dari grup fundamental ke abelianisasinya, atau dari
gelanggang kohomologi ke grup-grup aditifnya.

Paket memuat program Python berbasis pustaka standar, enam uji deterministik,
keluaran acuan, interpretasi, petunjuk, dan solusi lengkap. Semua koefisien
adalah bilangan bulat. Program hanya memverifikasi empat model yang dijelaskan
di bawah; ia tidak mengaku menyelesaikan masalah isomorfisma grup, gelanggang,
atau tipe homotopi secara umum.

## Prasyarat yang dipakai {#o012-d60-lab04-prerequisites}

- [grup fundamental baji](../units/unit-013-lecture-013.md#o012-rbt-l13-s04)
  dan [kompleks presentasi](../units/unit-013-lecture-013.md#o012-rbt-l13-s05);
- identifikasi
  [$H_1(X;\mathbb Z)\cong\pi_1(X)^{\mathrm{ab}}$](../fomberg/units/fomberg-unit-001-delta-complexes-simplicial-homology.md#o012-fom-u001-rem-013);
- [kompleks korantai dan kohomologi singular](../units/unit-026-lecture-026.md#o012-rbt-l26-s02);
- struktur CW pada ruang projektif kompleks dalam
  [pemeriksaan $\mathbb{CP}^n$](../fomberg/units/fomberg-unit-006-cellular-complexes.md#o012-fom-u006-mcheck-001);
- hubungan batas seluler, kelas fundamental, dan produk cup pada
  [Laboratorium 3](computation-lab-003-cellular-boundaries-degree.md#o012-d60-lab03-cellular-boundaries).

## Tujuan {#o012-d60-lab04-objectives}

Sesudah menyelesaikan laboratorium ini, pembaca dapat:

1. menghitung diferensial seluler dari jumlah eksponen bertanda;
2. menjelaskan mengapa $H_1$ hanya melihat abelianisasi $\pi_1$;
3. membedakan homologi dari informasi penuh peta pelekatan;
4. membedakan kohomologi sebagai grup bergradasi dari gelanggang kohomologi;
5. memakai produk cup sebagai obstruksi terhadap ekuivalensi homotopi;
6. memeriksa hukum unit, asosiativitas, dan komutativitas bergradasi pada
   tabel produk cup jarang;
7. mengaudit kesimpulan negatif tanpa mengubah “invarian ini tidak
   membedakan” menjadi klaim ekuivalensi.

## Empat model beku dan konvensi {#o012-d60-lab04-data}

Kita memakai dua pasangan berikut, selalu dengan koefisien $\mathbb Z$.

**Pasangan A.** Ambil

$$
X=T^2=(S^1_a\vee S^1_b)\cup_{aba^{-1}b^{-1}}e^2
$$

dan

$$
Y=S^1_a\vee S^1_b\vee S^2,
$$

yang dapat dipandang sebagai pelekatan sel-$2$ konstan pada baji dua
lingkaran. Keduanya mempunyai satu sel-$0$, dua sel-$1$, satu sel-$2$, dan
diferensial seluler nol. Namun,

$$
\pi_1(X)=\langle a,b\mid aba^{-1}b^{-1}\rangle\cong\mathbb Z^2,
\qquad
\pi_1(Y)=\langle a,b\mid\ \rangle\cong F_2.
$$

**Pasangan B.** Gunakan struktur CW

$$
P=\mathbb{CP}^2\cong S^2\cup_\eta e^4,
\qquad
Q=S^2\vee S^4\cong S^2\cup_{\mathrm{konstan}}e^4,
$$

di mana $\eta\colon S^3\to S^2$ adalah peta Hopf. Kedua ruang terhubung
sederhana dan mempunyai satu sel pada dimensi $0,2,4$. Semua diferensial
selulernya nol, tetapi peta pelekatan sel-$4$ tidak sama.

Orientasi dipilih sehingga generator teratas $\omega\in H^2(T^2)$ dan
$u\in H^4(\mathbb{CP}^2)$ mempunyai tanda positif dalam rumus di bawah.
Mengganti orientasi mengganti nama generator bertanda, bukan fakta bahwa
produknya nol atau tak nol.

## Prinsip perbandingan yang dihitung {#o012-d60-lab04-comparison-principles}

Untuk Pasangan A, kata komutator sudah tereduksi dalam grup bebas:

$$
aba^{-1}b^{-1}\ne 1\quad\text{di }F_2.
$$

Vektor jumlah eksponennya ialah $(0,0)$. Karena abelianisasi melupakan urutan
huruf, relator komutator tidak memberi relasi baru setelah abelianisasi. Maka

$$
H_1(X;\mathbb Z)\cong H_1(Y;\mathbb Z)\cong\mathbb Z^2,
$$

walaupun grup fundamentalnya tidak isomorfik: yang pertama abelian dan yang
kedua tidak. Kompleks rantai seluler keduanya ialah

$$
0\longrightarrow\mathbb Z\xrightarrow{0}\mathbb Z^2
\xrightarrow{0}\mathbb Z\longrightarrow0.
$$

Jadi homologi keduanya sama. Kohomologi aditifnya juga sama, tetapi
perkaliannya berbeda. Dengan basis dual $\alpha,\beta$ dan kelas orientasi
$\omega$,

$$
\alpha\smile\beta=\omega,
\qquad
\beta\smile\alpha=-\omega
\quad\text{pada }T^2,
$$

sedangkan semua produk dua kelas berderajat positif pada
$S^1\vee S^1\vee S^2$ adalah nol. Pada baji, kedua kelas derajat satu
didukung oleh suku lingkaran, sedangkan kelas derajat dua berasal dari suku
sfera; retraksi baji ke setiap suku memperlihatkan bahwa tidak ada produk
yang dapat menghasilkan generator sfera itu.

Untuk Pasangan B, grup fundamental, homologi, dan kohomologi aditif semuanya
sama. Keduanya mempunyai $\mathbb Z$ hanya pada derajat $0,2,4$. Informasi
yang tersisa berada dalam peta pelekatan. Jika

$$
Z_f=S^2\cup_f e^4,
$$

pilih $x\in H^2(Z_f;\mathbb Z)$ dan $u\in H^4(Z_f;\mathbb Z)$ sesuai
orientasi sel. Koefisien dalam

$$
x\smile x=H(f)u
$$

adalah invarian Hopf $H(f)$. Peta Hopf $\eta$ mempunyai $H(\eta)=1$,
sedangkan peta konstan mempunyai invarian Hopf nol. Karena itu

$$
H^*(\mathbb{CP}^2;\mathbb Z)\cong\mathbb Z[x]/(x^3),\quad |x|=2,
$$

dalam rentang dimensi ini dengan $x^2=u$, sementara pada $S^2\vee S^4$
berlaku $x^2=0$. Produk cup dipertahankan oleh ekuivalensi homotopi; jadi
kedua ruang pada setiap pasangan bukan ekuivalen homotopi.

::: {.exercise #o012-d60-lab04-task-001}
**Tugas 1 — jalankan verifikator beku.** Jalankan program uji dan program
utama. Pastikan enam uji lulus, aliran galat program utama kosong, dan
keluarannya sama byte demi byte dengan `expected-output-lab04.txt`.
:::

::: {.exercise #o012-d60-lab04-task-002}
**Tugas 2 — hitung kompleks seluler Pasangan A.** Hitung jumlah eksponen
relator torus, turunkan kedua diferensial, lalu hitung $H_0,H_1,H_2$ untuk
$X$ dan $Y$. Periksa juga karakteristik Euler.
:::

::: {.exercise #o012-d60-lab04-task-003}
**Tugas 3 — temukan informasi yang hilang pada $H_1$.** Reduksi bebas kata
$aba^{-1}b^{-1}$, bandingkan perilakunya pada $F_2$ dan $\mathbb Z^2$, dan
jelaskan mengapa abelianisasi kedua grup tetap $\mathbb Z^2$.
:::

::: {.exercise #o012-d60-lab04-task-004}
**Tugas 4 — bandingkan gelanggang Pasangan A.** Tulis basis kohomologi
bergradasi, hitung tabel produk cup tak nol, periksa tanda
$\beta\smile\alpha=-\alpha\smile\beta$, dan tentukan invarian pertama pada
urutan audit yang membedakan ruang.
:::

::: {.exercise #o012-d60-lab04-task-005}
**Tugas 5 — isolasi peta pelekatan Pasangan B.** Hitung invarian aditif
kedua ruang, kemudian gunakan rumus invarian Hopf untuk memperoleh
$x^2=u$ pada $\mathbb{CP}^2$ dan $x^2=0$ pada $S^2\vee S^4$.
:::

::: {.exercise #o012-d60-lab04-task-006}
**Tugas 6 — audit empat implikasi palsu.** Tolak dengan saksi eksplisit:
“$H_1$ sama berarti $\pi_1$ sama,” “homologi sama berarti ekuivalen
homotopi,” “diferensial seluler nol berarti peta pelekatan trivial,” dan
“kohomologi aditif sama berarti gelanggang kohomologi sama.” Jelaskan pula
mengapa kesamaan semua invarian yang kebetulan dihitung program tidak akan
menjadi algoritme umum untuk membuktikan ekuivalensi homotopi.
:::

::: {.hint #o012-d60-lab04-hint}
**Petunjuk.** Pisahkan tiga operasi: reduksi bebas mempertahankan urutan
huruf, abelianisasi hanya menyimpan jumlah eksponen, dan diferensial seluler
hanya membaca derajat komponen ke sel satu dimensi lebih rendah. Untuk
Pasangan B, tidak ada grup rantai pada dimensi $1$ atau $3$, sehingga semua
diferensial nol tanpa memaksa $\eta$ menjadi null-homotopik. Produk cup
membaca koefisien yang tidak tampak pada kompleks rantai aditif itu.
:::

## Program lengkap {#o012-d60-lab04-program}

Berkas kanonis:
[`o012_d60_lab04_cross_invariants.py`](o012_d60_lab04_cross_invariants.py).
Pembangun pembaca mengganti penanda berikut dengan byte sumber yang diuji.

O012_LAB04_INCLUDE_PROGRAM

## Uji deterministik lengkap {#o012-d60-lab04-tests}

Berkas kanonis:
[`test_o012_d60_lab04_cross_invariants.py`](test_o012_d60_lab04_cross_invariants.py).

O012_LAB04_INCLUDE_TESTS

## Keluaran acuan {#o012-d60-lab04-expected-output}

Berkas kanonis:
[`expected-output-lab04.txt`](expected-output-lab04.txt).

O012_LAB04_INCLUDE_EXPECTED

## Interpretasi matematis {#o012-d60-lab04-interpretation}

Pasangan A menunjukkan dua kehilangan informasi berurutan. Pemetaan
$\pi_1\to H_1$ mengabeliankan grup, sehingga komutator tidak terlihat.
Pemetaan dari gelanggang kohomologi ke grup kohomologi bergradasi melupakan
perkalian, sehingga kelas orientasi torus tidak lagi dikenali sebagai produk
dua kelas derajat satu. Pasangan B lebih tajam: bahkan $\pi_1$, homologi, dan
kohomologi aditif serentak tidak membedakan ruang, tetapi kuadrat cup
membedakannya.

Keluaran “pemisah pertama” bergantung pada urutan audit yang dinyatakan:
$\pi_1$, lalu homologi, lalu kohomologi aditif, lalu produk cup. Ini bukan
urutan kekuatan total bagi semua invarian. Sebuah perbedaan pada invarian
mana pun membuktikan tidak adanya ekuivalensi homotopi; kesamaan daftar
terbatas hanya berarti daftar itu belum menemukan perbedaan.

# Solusi lengkap {#o012-d60-lab04-solution}

## Eksekusi dan kontrak keluaran {#o012-d60-lab04-sol-execution}

Jalankan dari akar repositori:

```text
python -B source/id-ID/labs/test_o012_d60_lab04_cross_invariants.py
python -B source/id-ID/labs/o012_d60_lab04_cross_invariants.py
```

Perintah pertama menulis laporan `unittest` pada aliran galat dan harus
berakhir dengan `Ran 6 tests` serta `OK`; aliran keluarnya kosong. Perintah
kedua menulis UTF-8 dengan LF ke aliran keluar, tanpa aliran galat. Uji keenam
membandingkan byte itu dengan keluaran acuan. Program memvalidasi basis,
derajat produk, unit, asosiativitas, komutativitas bergradasi, sensus sel,
kesesuaian $H_1$ dengan abelianisasi, dan urutan laporan.

## Kompleks seluler dan homologi Pasangan A {#o012-d60-lab04-sol-cellular-pair-a}

Jumlah eksponen $a$ dalam $aba^{-1}b^{-1}$ ialah $1-1=0$, dan jumlah
eksponen $b$ juga nol. Jadi sel-$2$ torus mempunyai kolom batas $(0,0)^T$.
Pada $Y$, peta pelekatan sel-$2$ konstan, sehingga kolomnya juga nol.
Kedua sel-$1$ berawal dan berakhir pada simpul yang sama, maka $d_1=0$.
Dengan demikian kedua kompleks rantai sama:

$$
0\to\mathbb Z\xrightarrow{0}\mathbb Z^2
\xrightarrow{0}\mathbb Z\to0.
$$

Akibatnya

$$
H_0\cong\mathbb Z,\qquad H_1\cong\mathbb Z^2,
\qquad H_2\cong\mathbb Z,
$$

dan $\chi=1-2+1=0$. Kesamaan ini tidak menyatakan bahwa peta pelekatan
torus konstan: diferensial hanya menyimpan dua jumlah eksponen.

## Grup fundamental dan produk cup Pasangan A {#o012-d60-lab04-sol-pi1-cup-pair-a}

Tidak ada dua huruf bertetangga yang saling invers dalam
$aba^{-1}b^{-1}$, sehingga reduksi bebas tidak menghapus apa pun. Kata itu
bukan unsur identitas $F_2$. Dalam grup torus, kata yang sama justru relator
dan karenanya identitas. Lebih struktural, $\mathbb Z^2$ abelian sedangkan
$F_2$ tidak, jadi keduanya tidak isomorfik.

Setelah abelianisasi, urutan huruf boleh dipertukarkan dan kata komutator
menjadi $a+b-a-b=0$. Karena itu kedua abelianisasi ialah $\mathbb Z^2$,
sesuai $H_1$. Pada torus, orientasi memberi
$\alpha\smile\beta=\omega$; komutativitas bergradasi memberi

$$
\beta\smile\alpha=(-1)^{1\cdot1}\alpha\smile\beta=-\omega.
$$

Kuadrat kedua generator derajat satu nol. Pada baji, semua produk
kelas-kelas berderajat positif adalah nol. Dalam urutan audit program,
$\pi_1$ adalah pemisah pertama;
produk cup memberikan pemisah kedua yang independen.

## Peta Hopf dan kuadrat cup Pasangan B {#o012-d60-lab04-sol-pair-b}

Kedua ruang tidak mempunyai sel-$1$, sehingga terhubung sederhana. Kompleks
rantainya mempunyai $\mathbb Z$ pada dimensi $0,2,4$ dan nol di dimensi
lain; semua diferensial terpaksa nol. Maka homologi dan kohomologi aditifnya
masing-masing $\mathbb Z$ pada derajat $0,2,4$.

Perbedaan terletak pada pelekatan sel-$4$. Untuk kompleks dua-sel
$S^2\cup_f e^4$, definisi kohomologis invarian Hopf menyatakan bahwa
koefisien kuadrat generator derajat dua terhadap generator sel teratas ialah
$H(f)$. Peta Hopf memiliki invarian $1$ setelah orientasi dipilih, sedangkan
peta konstan berinvarian nol. Jadi

$$
x^2=u\ne0\quad\text{pada }\mathbb{CP}^2,
\qquad
x^2=0\quad\text{pada }S^2\vee S^4.
$$

Karena pemetaan yang menginduksi isomorfisma gelanggang kohomologi harus
mempertahankan kuadrat, tidak mungkin ada ekuivalensi homotopi antara kedua
ruang itu.

## Audit kesimpulan negatif {#o012-d60-lab04-sol-negative}

Pasangan A menolak implikasi pertama: $H_1$ keduanya $\mathbb Z^2$, tetapi
$\pi_1$ masing-masing $\mathbb Z^2$ dan $F_2$. Kedua pasangan menolak
implikasi kedua karena homologi sama sedangkan produk cup atau grup
fundamental membedakan tipe homotopinya. Pasangan B menolak implikasi ketiga:
$d_4=0$ baik untuk peta Hopf maupun peta konstan, sebab $C_3=0$, tetapi peta
Hopf tidak trivial. Kedua pasangan menolak implikasi keempat karena grup
kohomologi bergradasi sama dan tabel perkaliannya berbeda.

Program hanya membandingkan deskriptor yang telah dibuktikan bagi empat
model. Jika semua deskriptor dua ruang lain kebetulan sama, hasil yang sah
hanyalah “belum terbedakan oleh pemeriksaan ini.” Masalah kata grup yang
dipresentasikan hingga dan klasifikasi tipe homotopi tidak diganti oleh tabel
kasus beku ini.

## Pemeriksaan reproduktibilitas {#o012-d60-lab04-reproducibility}

Enam uji harus memeriksa:

1. validitas empat model dan penolakan tabel produk yang salah derajat atau
   mempunyai basis ganda;
2. sensus sel, homologi, vektor jumlah eksponen, dan karakteristik Euler
   Pasangan A;
3. saksi komutator bebas, grup fundamental berbeda, dan abelianisasi sama;
4. hukum gelanggang serta tabel produk cup Pasangan A;
5. kesamaan invarian aditif dan perbedaan kuadrat cup Pasangan B;
6. keluaran CLI yang deterministik dan sama persis dengan keluaran acuan.

Program tidak mengakses jaringan, tidak memakai keacakan atau aritmetika
titik-mengambang, dan tidak menerima jawaban dari keluaran acuan sebagai
masukan. Semua iterasi yang tampil di keluaran mempunyai urutan kanonis.

## Hak, atribusi, dan provenans {#o012-d60-lab04-rights}

Laboratorium, program, uji, keluaran acuan, susunan perbandingan, petunjuk,
interpretasi, dan solusi ini adalah materi asli edisi di bawah CC BY-SA 4.0.
Jangkar konseptual yang dipakai ialah Roberts `Notes.tex:2826–3046` untuk
baji dan kompleks presentasi, `Notes.tex:5370–5728` untuk korantai dan
kohomologi, Fomberg `algebraic_topology.tex:610–613` untuk abelianisasi,
`algebraic_topology.tex:3448–3516` untuk struktur CW pada ruang projektif kompleks,
serta Laboratorium 3 untuk konvensi produk cup dan kelas fundamental.
Pernyataan tentang invarian Hopf dan kedua tabel produk disusun mandiri untuk
menutup kebutuhan sintesis; tidak ada ekspresi bank masalah Fomberg yang
dikecualikan atau sumber tak berlisensi yang disalin.

Produksi dilakukan dengan **OpenAI Codex gpt-5.6-sol, Ultra** atas arahan
pengguna. Kredit, lisensi, dan hubungan sumber David Michael Roberts serta
Yeheli Fomberg tetap dibedakan. Edisi independen ini tidak menyiratkan
dukungan atau pengesahan penulis sumber maupun institusi mana pun.
