---
title: "Capstone D60 — Rekonstruksi Bukti dan Sintesis Lintas-Invarian"
subtitle: "Botol Klein, selubung berorientasi, dan batas inferensi"
author:
  - "Materi asli edisi Bahasa Indonesia"
date: "29 Agustus 2026"
lang: id-ID
course_id: D60
edition_unit_id: O012-ORIG-CAPSTONE
course_route_unit_id: D60-R14
rights: "CC BY-SA 4.0; materi asli edisi ini"
origin: "Lapisan sintesis asli; tidak disalin dari Roberts, Fomberg, atau bank soal Fomberg."
provenance: "OpenAI Codex gpt-5.6-sol, Ultra; disusun atas arahan pengguna; kredit penulis dan lisensi komponen sumber tetap dipertahankan."
status: "capstone rekonstruksi bukti, komputasi, dan batas inferensi"
---

# Capstone D60: botol Klein dan sintesis lintas-invarian {#o012-d60-capstone}

Capstone ini adalah lapisan asli edisi untuk `D60-R14`. Ia mengikat kembali
empat belas unit rute tanpa mengubah urutan atau pengenal unit edisi Roberts dan
Fomberg. Contoh utamanya ialah botol Klein $K$, dipandang sekaligus sebagai
ruang hasil bagi, pemetaan torus, kompleks CW, dan ruang dengan selubung ganda
berorientasi. Tujuan akhirnya bukan menghafal tabel invarian, melainkan mampu
menyatakan hipotesis, merekonstruksi bukti, menghitung, lalu menjelaskan apa
yang **tidak** dapat disimpulkan dari hitungan terbatas.

::: {.note #o012-d60-capstone-status data-origin="edition-original"}
**Status dan batas.** Semua soal, petunjuk, solusi, peta bukti, dan rubrik
oral di sini merupakan materi asli berlisensi CC BY-SA 4.0. Capstone ini
terpisah dari sensus 108 soal bersolusi; ia adalah satu asesmen penutup yang
memakai keempat laboratorium dan seluruh rute sebagai prasyarat. Tidak ada
pernyataan soal atau solusi dari bank masalah Fomberg yang dipakai.
:::

## Prasyarat dan kontrak notasi {#o012-d60-capstone-prerequisites}

Kita bekerja dengan ruang terhubung, kompleks CW hingga, dan koefisien
$\mathbb Z$ kecuali disebut lain. Titik pangkal untuk grup fundamental harus
dipilih dan dipertahankan pada semua peta. Untuk pasangan $(X,A)$, barisan
eksak panjang, peta penghubung, dan identifikasi hasil bagi dipakai hanya
setelah pasangan itu terbukti baik. Ketika orientasi atau kelas fundamental
diperlukan, kita menyatakannya secara eksplisit; botol Klein sendiri tidak
memiliki kelas fundamental integral dalam dimensi dua.

Kita gunakan konvensi generator berikut. Huruf $a$ adalah gelung basis pemetaan
torus yang membalik orientasi serat, sedangkan $b$ adalah gelung serat. Dengan
demikian relasi sel-2 adalah

$$
w=aba^{-1}b,
\qquad\text{yakni }aba^{-1}=b^{-1}.
$$

Konvensi ini sengaja membuat jumlah eksponen $w$ terhadap $(a,b)$ menjadi
$(0,2)$. Mengganti generator atau mengambil inversnya sah, tetapi semua
perubahan harus dicatat sebelum menghitung matriks.

## Sasaran yang harus dapat direkonstruksi {#o012-d60-capstone-objectives}

Setelah menyelesaikan capstone, pembaca harus dapat:

1. membangun $K$ sebagai torus pemetaan refleksi dan menjelaskan monodrominya;
2. menghitung $\pi_1(K)$ dengan Seifert--van Kampen (SvK) serta barisan eksak
   panjang fibrasi, lalu menemukan subgrup torus indeks dua;
3. menurunkan kata pelekatan, diferensial seluler, dan homologi dari jumlah
   eksponen bertanda;
4. menyambung bukti hasil bagi--stabilisasi kerangka--homologi seluler--rumus
   insidensi dengan empat pengenal perbaikan bukti yang tepat;
5. memakai teorema koefisien universal (UCT) untuk memperoleh kohomologi dan membedakan isu orientasi,
   koefisien, serta derajat;
6. menyimpulkan dengan beberapa invarian tanpa mengubah kesamaan daftar
   invarian menjadi klaim ekuivalensi homotopi.

## Data kasus: refleksi dan selubung berorientasi {#o012-d60-capstone-data}

Ambil $r:S^1\to S^1$, $r(z)=\overline z$. Definisikan

$$
K=T_r=(S^1\times[0,1]) / ((z,1)\sim(r(z),0)).
$$

Memotong pada $t=0$ menghasilkan silinder; menempelkan kembali kedua
lingkaran dengan refleksi adalah tepat peta monodromi $r$. Jika kita
menjalankan basis dua kali, $r^2=\operatorname{id}$, sehingga tarik balik pada
selubung basis ganda ialah

$$
\widetilde K=(S^1\times[0,2])/
((z,2)\sim(z,0))\cong S^1\times S^1=T^2.
$$

Transformasi dek $\tau$ menukar dua pengangkatan satu putaran basis dan membalik
orientasi torus; secara koordinat ia dapat direpresentasikan (setelah memilih
koordinat yang sesuai) oleh peta afin dengan determinan $-1$. Maka
$p:T^2\to K$ ialah selubung berlembar dua yang terhubung dan merupakan
selubung orientasi.

Ada model CW lain yang dipakai pada Roberts Unit 20: satu sel-$0$, tiga
sel-$1$, dan dua sel-$2$. Model itu bukan ruang baru, melainkan subdivisi
seluler dari $K$. Matriks diferensial yang sudah dikoreksi di unit tersebut
ialah (baris berindeks pada tiga sel-$1$ dan kolom pada dua sel-$2$)

$$
d_1=0,\qquad
d_2=\begin{pmatrix}1&1\\[2pt]-1&1\\[2pt]1&-1\end{pmatrix}.
$$

Kedua kolomnya bebas linear, sedangkan fpb minor-$2\times2$-nya adalah $2$;
bentuk normal Smith-nya ialah $\operatorname{diag}(1,2)$. (Matriks $2\times3$
yang tampak pada catatan Roberts adalah transpos, yakni peta kokit $\delta^1$,
bukan diferensial seluler $d_2$.) Karenanya model ini memberi
$H_1\cong\mathbb Z\oplus\mathbb Z/2$ dan $H_2=0$, sama dengan model
satu-relator di bawah. Kesalahan lama yang
mengulang $d_2^2(f_2)=e_2$ telah diperbaiki pada sumber; capstone memakai
model relator $(0,2)$ untuk memperlihatkan rumus insidensi secara langsung,
serta model Roberts ini sebagai pemeriksaan silang independen.

::: {.figure #o012-d60-capstone-cover data-origin="edition-original" data-rendering="semantic-reflow"}
**Diagram semantik selubung.** Lingkaran serat dengan generator $b$ diangkat
menjadi dua lingkaran; gelung basis $a$ menukar pengangkatan dan menerapkan $b\mapsto
b^{-1}$. Dua putaran basis kembali ke pengangkatan semula, sehingga subgrup yang
ditetapkan ialah $\langle a^2,b\rangle$.
:::

## Soal capstone 1 — hipotesis, monodromi, dan tarik balik {#o012-d60-capstone-task-001}

::: {.exercise #o012-d60-capstone-ex-001 data-origin="edition-original" data-capstone="true"}
Nyatakan semua hipotesis topologis yang diperlukan untuk konstruksi di atas.
Tunjukkan bahwa tarik balik terhadap selubung basis $S^1\xrightarrow{z\mapsto
z^2}S^1$ adalah $T^2$, dan tentukan aksi monodromi pada $H_1(S^1;\mathbb Z)$.
Jelaskan mengapa $p$ adalah selubung orientasi, bukan peta berderajat integral
dari $T^2$ ke $K$.
:::

::: {.hint #o012-d60-capstone-hint-001 data-origin="edition-original" data-capstone="true"}
Periksa keterhubungan, aksi $r_*$ pada generator serat, dan apakah ruang sasaran
memiliki kelas fundamental integral berdimensi dua.
:::

::: {.solution #o012-d60-capstone-sol-001 data-origin="edition-original" data-capstone="true"}
**Solusi.** Ruang serat dan basis harus terhubung, $r$ harus homeomorfisme,
dan identifikasi di ujung harus dilakukan dengan peta yang sama pada seluruh
serat. Tarik balik oleh peta basis dua-lembar mengulang monodromi dua kali;
karena $r^2=1$, identifikasi totalnya adalah produk $S^1\times S^1$.
Pada $H_1(S^1;\mathbb Z)=\mathbb Z[b]$, refleksi memberi $r_*[b]=-[b]$.
Dengan demikian monodromi nontrivial pada putaran pertama, tetapi trivial
setelah dua putaran, tepat seperti konstruksi $T^2$ di atas. Peta $p$ ialah
selubung orientasi karena dek involusinya membalik orientasi dan ruang hasil
tidak dapat diorientasikan. Derajat integral biasanya didefinisikan untuk
peta antara manifold tertutup berorientasi dengan kelas fundamental integral;
$K$ tidak mempunyai kelas tersebut, sehingga simbol $\deg(p:T^2\to K)$ tidak
bermakna sebagai derajat integral.
:::

## Soal capstone 2 — grup fundamental dan subgrup indeks dua {#o012-d60-capstone-task-002}

::: {.exercise #o012-d60-capstone-ex-002 data-origin="edition-original" data-capstone="true"}
Dengan membuka $K$ menjadi dua pita yang irisannya mempunyai dua komponen,
gunakan teorema van Kampen versi grupoid (atau tambahkan jalur penghubung
sehingga bentuk berbasis satu titik pangkal berlaku) untuk memperoleh presentasi

$$
\pi_1(K)=\langle a,b\mid aba^{-1}b\rangle.
$$

Konfirmasi hasil itu dari barisan eksak panjang fibrasi $S^1\to K\to S^1$. Tunjukkan bahwa
homomorfisme $\epsilon:\pi_1(K)\to\mathbb Z/2$ dengan
$\epsilon(a)=1,\epsilon(b)=0$ terdefinisi, dan bahwa kernel-nya ialah
$\langle a^2,b\rangle\cong\mathbb Z^2$.
:::

::: {.hint #o012-d60-capstone-hint-002 data-origin="edition-original" data-capstone="true"}
Relasi berasal dari pita yang orientasinya dibalik: konjugasi oleh $a$
mengirim $b$ ke $b^{-1}$. Untuk kernel, tulis setiap kata sebagai $a^m$ kali
kata serat dan gunakan relasi untuk memindahkan $b$ melewati $a$.
:::

::: {.solution #o012-d60-capstone-sol-002 data-origin="edition-original" data-capstone="true"}
**Solusi.** Pilih satu pita sebagai $U$ dan pita kedua sebagai $V$ setelah
memotong pada dua titik basis. Karena $U\cap V$ memiliki dua komponen,
terapkan van Kampen untuk grupoid dengan kedua titik pangkal itu (setara
dengan menambahkan jalur penghubung sebelum memakai versi biasa). Generator
irisan memberi gelung serat $b$; gelung yang melintasi pita memberi $a$. Jalur yang
melewati kedua komponen irisan menghasilkan $aba^{-1}=b^{-1}$, atau relator
$aba^{-1}b$. Teorema van Kampen kemudian memberi presentasi yang dinyatakan.
Urutan eksak homotopi dari fibrasi $S^1\to K\to S^1$ hanya memberi ekstensi

$$
0\longrightarrow\pi_1(S^1)_{\mathrm{serat}}\xrightarrow{\,i_*\,}\pi_1(K)
\xrightarrow{\,p_*\,}\pi_1(S^1)_{\mathrm{basis}}\longrightarrow 0,
$$

dengan aksi konjugasi generator basis pada serat diberikan oleh $r_*=-1$.
Jadi ekstensi tersebut adalah $\mathbb Z\rtimes_{-1}\mathbb Z$ dan memberi
relasi yang sama. Faktor $1-r_*=2$ muncul pada barisan Wang untuk homologi
pemetaan-torus (bukan pada barisan eksak panjang homotopi):

$$
H_1(S^1)\xrightarrow{\,1-r_*\,}H_1(S^1)\longrightarrow H_1(K)
\longrightarrow H_0(S^1)\xrightarrow{\,1-r_*\,}H_0(S^1).
$$

Relasi memiliki jumlah paritas nol pada kedua sisi, jadi $\epsilon$ terdefinisi.
Setiap kelas dapat ditulis $a^m b^n$ (dengan relasi produk semilangsung), dan paritas
$m$ adalah nilai $\epsilon$. Kernel terdiri dari kata dengan $m$ genap,
sehingga dihasilkan oleh $a^2$ dan $b$. Keduanya komutatif karena
$a^2ba^{-2}=b$, tidak ada relasi tambahan, dan karenanya kernel isomorfik
dengan $\mathbb Z^2$. Inilah grup fundamental selubung $T^2$ dan indeksnya dua.
:::

## Soal capstone 3 — kompleks seluler dan homologi {#o012-d60-capstone-task-003}

::: {.exercise #o012-d60-capstone-ex-003 data-origin="edition-original" data-capstone="true"}
Gunakan CW dengan satu sel-$0$, sel-$1$ bernama $a,b$, dan satu sel-$2$ yang
melekat melalui $w=aba^{-1}b$. Hitung $d_1$, $d_2$, semua grup homologi, serta
karakteristik Euler. Hubungkan koordinat $d_2$ dengan jumlah eksponen bertanda.
:::

::: {.hint #o012-d60-capstone-hint-003 data-origin="edition-original" data-capstone="true"}
Karena hanya ada satu titik sudut, $d_1=0$. Jumlah eksponen $a$ pada $w$
adalah $1-1$, sedangkan jumlah eksponen $b$ adalah $1+1$.
:::

::: {.solution #o012-d60-capstone-sol-003 data-origin="edition-original" data-capstone="true"}
**Solusi.** Kompleks rantai seluler ialah

$$
0\longrightarrow C_2=\mathbb Z
\xrightarrow{d_2=(0,2)} C_1=\mathbb Z a\oplus\mathbb Z b
\xrightarrow{d_1=0} C_0=\mathbb Z\longrightarrow0.
$$

Peta $d_1$ nol karena kedua sel-$1$ kembali ke satu-satunya sel-$0$ dengan
orientasi awal dan akhir yang sama. Rumus insidensi memberi koefisien sel-$1$
sebagai jumlah eksponen bertanda dalam kata pelekatan: untuk $a$ ialah
$1+(-1)=0$, dan untuk $b$ ialah $1+1=2$. Karena $(0,2)$ injektif,
$H_2(K;\mathbb Z)=0$. Selanjutnya

$$
H_1(K;\mathbb Z)=\mathbb Z^2/\langle(0,2)\rangle
\cong\mathbb Z\oplus\mathbb Z/2\mathbb Z,
\qquad H_0(K;\mathbb Z)\cong\mathbb Z.
$$

Karena ada satu sel pada dimensi $0$ dan $2$ serta dua pada dimensi $1$,
$\chi(K)=1-2+1=0$, sama dengan $1-1+0$ dari grup homologi bebas.
:::

## Soal capstone 4 — UCT, koefisien, dan derajat {#o012-d60-capstone-task-004}

::: {.exercise #o012-d60-capstone-ex-004 data-origin="edition-original" data-capstone="true"}
Hitung $H^0,H^1,H^2$ dengan UCT untuk kohomologi integral. Lalu hitung
homologi dengan koefisien $\mathbb F_2$ dari kompleks seluler yang sama.
Terangkan mengapa involusi dek $\tau:T^2\to T^2$ mempunyai derajat $-1$,
sedangkan $p:T^2\to K$ tidak boleh diberi derajat integral.
:::

::: {.hint #o012-d60-capstone-hint-004 data-origin="edition-original" data-capstone="true"}
Gunakan $\operatorname{Hom}(\mathbb Z/2,\mathbb Z)=0$ dan
$\operatorname{Ext}(\mathbb Z/2,\mathbb Z)=\mathbb Z/2$. Modulo $2$, panah
$(0,2)$ menjadi nol.
:::

::: {.solution #o012-d60-capstone-sol-004 data-origin="edition-original" data-capstone="true"}
**Solusi.** UCT memberi barisan pendek

$$
0\to\operatorname{Ext}(H_{k-1}(K),\mathbb Z)
\to H^k(K;\mathbb Z)\to\operatorname{Hom}(H_k(K),\mathbb Z)\to0.
$$

Maka $H^0\cong\mathbb Z$, $H^1\cong\operatorname{Hom}(\mathbb Z\oplus
\mathbb Z/2,\mathbb Z)\cong\mathbb Z$, dan
$H^2\cong\operatorname{Ext}(\mathbb Z\oplus\mathbb Z/2,\mathbb Z)
\cong\mathbb Z/2$. Secara korantai, $\delta^0=0$ dan
$\delta^1(x,y)=2y$, yang menghasilkan jawaban sama.

Dengan koefisien $\mathbb F_2$, $d_2=(0,0)$ dan $d_1=0$, sehingga
$H_0\cong\mathbb F_2$, $H_1\cong\mathbb F_2^2$, dan
$H_2\cong\mathbb F_2$. Involusi dek membalik satu arah torus, jadi matriks
turunannya memiliki determinan $-1$ dan $\deg(\tau)=-1$. Sebaliknya, ruang sasaran
$K$ tidak berorientasi dan $H_2(K;\mathbb Z)=0$; tidak ada kelas fundamental
integral yang dapat menjadi sasaran persamaan derajat. Pernyataan “derajat
$p$” harus diganti dengan pernyataan selubung, transfer, atau koefisien
modulo $2$, bukan dipaksakan sebagai bilangan bulat.
:::

## Soal capstone 5 — peta rekonstruksi empat perbaikan bukti {#o012-d60-capstone-task-005}

::: {.exercise #o012-d60-capstone-ex-005 data-origin="edition-original" data-capstone="true"}
Tuliskan rantai dependensi bukti yang mengubah data CW menjadi perhitungan di
Soal 3. Setiap panah harus menyebut hipotesis dan pengenal perbaikan bukti yang
menutup lokasi sumber yang semula ringkas.
:::

::: {.hint #o012-d60-capstone-hint-005 data-origin="edition-original" data-capstone="true"}
Mulai dari pasangan $(X^{(n)},X^{(n-1)})$, bukan langsung dari matriks.
Bedakan hasil bagi, stabilisasi kerangka, teorema homologi seluler, dan rumus
insidensi.
:::

::: {.solution #o012-d60-capstone-sol-005 data-origin="edition-original" data-capstone="true"}
**Solusi.** Untuk setiap kerangka, pasangan $(X^{(n)},X^{(n-1)})$ adalah
pasangan baik. Pertama, identifikasi homologi relatif dengan homologi hasil
bagi melalui penanda maju **FOM-U003-QUOTIENT-LES** dan bukti relatif yang
lengkap. Kedua, gunakan stabilisasi kerangka **FOM-PR-13** untuk menunjukkan
bahwa pada derajat tetap hanya kerangka yang relevan yang memengaruhi
homologi. Ketiga, **FOM-PR-14** memberi isomorfisme antara homologi kompleks
rantai seluler dan homologi singular. Keempat, **FOM-PR-15** menghitung setiap
koefisien diferensial sebagai jumlah derajat lokal (jumlah eksponen bertanda)
sepanjang peta pelekatan.

Untuk $K$, langkah keempat mengubah $w=aba^{-1}b$ menjadi $(0,2)$; langkah
ketiga mengizinkan kita membaca kernel dan kokernel sebagai $H_2$ dan $H_1$.
Tidak ada langkah yang mengasumsikan orientabilitas $K$ atau mengganti
homologi singular dengan tabel. Peta ini juga menjelaskan mengapa setiap
lokus sumber yang tercatat tidak lengkap tidak boleh dianggap sebagai bukti hanya
karena formula akhirnya tampak benar.
:::

## Soal capstone 6 — sintesis dan batas inferensi {#o012-d60-capstone-task-006}

::: {.exercise #o012-d60-capstone-ex-006 data-origin="edition-original" data-capstone="true"}
Susun kesimpulan satu halaman yang menggabungkan $\pi_1$, abelianisasi,
homologi, kohomologi, selubung, dan derajat. Sertakan satu pernyataan yang
terbukti, satu yang disangkal oleh contoh $K$, dan satu yang tetap tidak dapat
diputuskan oleh daftar invarian terbatas. Jelaskan mengapa H$_1$ saja tidak
memulihkan grup fundamental.
:::

::: {.hint #o012-d60-capstone-hint-006 data-origin="edition-original" data-capstone="true"}
Urutkan bukti dari informasi paling kaya ke paling tereduksi: presentasi grup,
abelianisasi, kompleks seluler, lalu UCT. Kesesuaian bukan ekuivalensi.
:::

::: {.solution #o012-d60-capstone-sol-006 data-origin="edition-original" data-capstone="true"}
**Solusi.** Presentasi memberi $\pi_1(K)=\mathbb Z\rtimes_{-1}\mathbb Z$,
sedangkan abelianisasi memberi $H_1(K)=\mathbb Z\oplus\mathbb Z/2$. Jadi
komutator dan aksi monodromi tidak terlihat seluruhnya pada $H_1$; ruang
dengan $\pi_1$ nonisomorfik dapat mempunyai $H_1$ yang sama. Kompleks seluler
menunjukkan $H_2(K;\mathbb Z)=0$, $H_0=\mathbb Z$, dan UCT menambahkan
$H^1=\mathbb Z$, $H^2=\mathbb Z/2$. Selubung orientasi $T^2$ memulihkan
subgrup indeks dua dan menyediakan kelas fundamental untuk menghitung derajat
endomorfisme torus, tetapi tidak mengubah $K$ menjadi manifold berorientabel.

Pernyataan yang terbukti: relasi presentasi dan hasil homologi di atas saling
konsisten melalui rumus insidensi. Pernyataan yang disangkal: “isomorfisme
$H_1$ memaksa isomorfisme $\pi_1$” salah karena abelianisasi menghapus
komutator. Pernyataan yang tidak dapat diputuskan: kesamaan semua data hingga
yang dihitung di sini tidak membuktikan ekuivalensi homotopi atau homeomorfisme
dua ruang umum; diperlukan invarian tambahan atau bukti peta eksplisit.
:::

## Peta bukti dan pemeriksaan mandiri {#o012-d60-capstone-proof-map}

Tabel berikut adalah peta eksplisit dari sasaran ke saksi. Pengenal tidak boleh
diganti dengan nama bebas ketika backend dibaca mesin.

| Langkah | Saksi/pengenal | Apa yang diperiksa |
|---|---|---|
| hasil bagi dari pasangan baik | `FOM-U003-QUOTIENT-LES` | barisan eksak panjang, peta penghubung, dan identifikasi hasil bagi |
| stabilisasi kerangka | `FOM-PR-13` | kerangka cukup tinggi tidak mengubah derajat homologi |
| homologi seluler | `FOM-PR-14` | kompleks seluler menghitung homologi singular |
| rumus insidensi | `FOM-PR-15` | derajat lokal/jumlah eksponen bertanda |
| pemeriksaan matematika | `qa/fomberg-unit-007/INDEPENDENT_MATH_REVIEW_FINAL.json` | P1=P2=P3=0 pada empat perbaikan |

Daftar periksa mandiri: (i) nyatakan titik pangkal dan orientasi sebelum memakai
SvK; (ii) bedakan aksi kiri/kanan monodromi; (iii) abelianisasi hanya memberi
hasil bagi abelian; (iv) cek $d_1d_2=0$; (v) jangan memberi derajat integral pada
$T^2\to K$; (vi) kesesuaian pada daftar invarian terbatas berarti “belum
terbedakan”, bukan “ekuivalen”.

## Rubrik rekonstruksi oral {#o012-d60-capstone-oral-rubric}

Ujian lisan meminta pembaca menggambar kembali diagram selubung, menuliskan
relator, dan merekonstruksi empat panah bukti tanpa membaca solusi. Setiap
kriteria diberi 0, 1, atau 2 poin (maksimum 12).

| Kriteria | 2 poin | 1 poin | 0 poin |
|---|---|---|---|
| hipotesis, titik pangkal, orientasi | semua dinyatakan dan konsisten | satu detail kurang tetapi dapat diperbaiki | memakai hipotesis salah |
| monodromi dan subgrup | $b\mapsto b^{-1}$ dan indeks dua dijustifikasi | hasil benar tanpa justifikasi lengkap | arah monodromi atau subgrup salah |
| SvK dan presentasi | relator $aba^{-1}b$ diturunkan | relator benar tetapi asalnya kabur | presentasi tidak konsisten |
| kompleks seluler | $(0,2)$, kernel, kokernel dihitung | satu aritmetika kecil salah | mengabaikan $d_1d_2$ atau tanda |
| UCT dan derajat | $H^*$ serta batas orientasi dijelaskan | tabel benar, alasan kurang | memberi derajat $T^2\to K$ |
| peta bukti dan batas inferensi | empat pengenal dan ketidak-ekuivalenan disebut | tiga pengenal atau batas disebut | penalaran melingkar/invarian hingga dianggap menyiratkan ekuivalensi |

Skor $\ge 9$ menunjukkan rekonstruksi mandiri. Skor 7--8 memerlukan
pengulangan hanya pada kriteria bernilai 0 atau 1. Skor $\le 6$ berarti
ulangi seluruh rantai. **Gagal otomatis**, berapa pun jumlah lainnya, terjadi bila
pembaca menyatakan ruang sasaran $K$ berorientasi integral, menukar peta
$T^2\to K$ dengan endomorfisme torus saat menghitung derajat, atau memakai
kesamaan invarian terbatas sebagai bukti ekuivalensi.

## Interpretasi lintas-invarian dan batas {#o012-d60-capstone-interpretation}

Kasus $K$ memperlihatkan alur informasi yang terarah: monodromi menentukan
presentasi; presentasi diubah menjadi matriks insidensi; matriks memberi
homologi; UCT mengubahnya menjadi kohomologi aditif; selubung mengembalikan
informasi orientasi yang hilang pada ruang sasaran. Tidak satu pun tahap membenarkan
inferensi terbalik tanpa data tambahan. Secara khusus, $H_1$ ialah abelianisasi
$\pi_1$, bukan pengganti grup fundamental, dan $H^2(K;\mathbb Z)=\mathbb Z/2$
tidak menyediakan kelas fundamental bebas.

Kesimpulan yang sah dari audit ini bersifat kondisional dan eksplisit. Jika
dua ruang berbeda mempunyai saksi invarian yang tidak sama, keduanya pasti
bukan ekuivalen homotopi. Jika semua saksi yang dipilih sama, hasilnya hanya
“belum dibedakan oleh audit ini”. Klasifikasi ruang, masalah kata grup, dan
informasi operasi kohomologi berada di luar daftar hingga ini.

## Hak, atribusi, dan provenans {#o012-d60-capstone-rights}

::: {.rights data-origin="edition-original" data-license="CC-BY-SA-4.0"}
Capstone, termasuk kasus botol Klein, soal, petunjuk, solusi, tabel, rubrik,
dan peta bukti, adalah materi asli edisi di bawah **CC BY-SA 4.0**. Ia
bergantung secara konseptual pada hasil Roberts CC BY 4.0 dan Fomberg CC
BY-SA 4.0 yang tetap diatribusikan pada komponen masing-masing; tidak ada
teks sumber atau bank masalah yang disalin. Catatan perubahan dan
pemberitahuan non-pengesahan komponen sumber tetap berlaku. Produksi dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra** atas arahan pengguna. Edisi ini tidak
menyiratkan dukungan, pengesahan, atau afiliasi penulis maupun institusi
sumber.
:::
