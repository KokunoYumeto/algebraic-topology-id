---
title: "Petunjuk Penguasaan Rute 1–6"
lang: id-ID
course_id: D60
edition_unit_id: O012-ORIG-HINTS-R01-R06
course_route_unit_ids:
  - D60-R01
  - D60-R02
  - D60-R03
  - D60-R04
  - D60-R05
  - D60-R06
rights: "CC BY-SA 4.0"
origin: "Materi edisi asli; bukan bagian dari sumber Roberts atau Fomberg."
provenance: "OpenAI Codex gpt-5.6-sol, Ultra; disusun atas arahan pengguna; kredit dan hak komponen sumber tetap dipertahankan."
---

# Petunjuk penguasaan untuk Rute 1–6 {#o012-d60-hints-r01-r06}

Berkas ini menambahkan petunjuk bagi 36 soal yang sudah mempunyai solusi
lengkap dalam edisi. Soal dan solusi tersebut tidak disalin atau diubah di
sini. Setiap blok menunjuk tepat ke satu soal, satu solusi yang sudah ada,
komponen sumber, dan jalur berkas kanoniknya. Seluruh petunjuk merupakan materi
edisi asli berlisensi CC BY-SA 4.0.

## D60-R01 — topologi dasar dan konstruksi universal {#o012-d60-hints-r01}

::: {.hint #o012-d60-r01-hint-001 data-origin="edition-original" data-course-route-unit-id="D60-R01" data-component-id="o012-rbt-l01" data-target-exercise-id="unit:o012-rbt-l01-ex-001" data-existing-solution-id="unit:o012-rbt-l01-sol-001" data-source-path="source/id-ID/reader-unit-001.md"}
**Rujukan:** [soal](#o012-rbt-l01-ex-001) · [solusi lengkap](#o012-rbt-l01-sol-001).

**Petunjuk.** Ambil himpunan terbuka $U\subseteq Y$ dan satu titik
$x\in f^{-1}(U)$. Hubungkan ketiga informasi berikut secara berurutan:
$f(x)\in U$, definisi keterbukaan melalui basis lingkungan di $Y$, dan
kontinuitas berbasis lingkungan dari $f$. Sasaran lokalnya ialah menemukan
lingkungan dasar dari $x$ yang seluruhnya berada di dalam $f^{-1}(U)$.
:::

::: {.hint #o012-d60-r01-hint-002 data-origin="edition-original" data-course-route-unit-id="D60-R01" data-component-id="o012-rbt-l01" data-target-exercise-id="unit:o012-rbt-l01-ex-002" data-existing-solution-id="unit:o012-rbt-l01-sol-002" data-source-path="source/id-ID/reader-unit-001.md"}
**Rujukan:** [soal](#o012-rbt-l01-ex-002) · [solusi lengkap](#o012-rbt-l01-sol-002).

**Petunjuk.** Periksa satu per satu ketiga aksioma basis lingkungan. Untuk
irisan dua anggota, gabungkan semua prabayangan dalam satu irisan berhingga;
jika indeks yang sama muncul dua kali, gunakan aksioma irisan pada ruang
targetnya. Untuk aksioma penyempurnaan lokal, sempurnakan dahulu setiap
lingkungan $N_i$ di $Y_{\alpha_i}$, baru tarik semuanya kembali ke $X$.
:::

::: {.hint #o012-d60-r01-hint-003 data-origin="edition-original" data-course-route-unit-id="D60-R01" data-component-id="o012-rbt-l02" data-target-exercise-id="unit:o012-rbt-l02-ex-001" data-existing-solution-id="unit:o012-rbt-l02-sol-001" data-source-path="source/id-ID/units/unit-002-lecture-002.md"}
**Rujukan:** [soal](#o012-rbt-l02-ex-001) · [solusi lengkap](#o012-rbt-l02-sol-001).

**Petunjuk.** Deskripsikan lingkungan dasar suatu titik $x$ dalam topologi
awal sebagai $f^{-1}(N)$ untuk lingkungan $N$ dari $f(x)$. Karena
$f(x_1)=f(x_2)$, lingkungan yang sama di $Y$ dapat dipakai pada kedua titik.
Setelah memperoleh satu arah implikasi, tukarkan peran $x_1$ dan $x_2$.
:::

::: {.hint #o012-d60-r01-hint-004 data-origin="edition-original" data-course-route-unit-id="D60-R01" data-component-id="o012-rbt-l02" data-target-exercise-id="unit:o012-rbt-l02-ex-002" data-existing-solution-id="unit:o012-rbt-l02-sol-002" data-source-path="source/id-ID/units/unit-002-lecture-002.md"}
**Rujukan:** [soal](#o012-rbt-l02-ex-002) · [solusi lengkap](#o012-rbt-l02-sol-002).

**Petunjuk.** Tulis dahulu invers himpunan dari $\Phi$ dengan mempertahankan
label komponen $\beta$. Untuk kontinuitas $\Phi$, uji setiap pembatasannya ke
$X\times Z_\beta$ dan gunakan sifat universal jumlah. Untuk inversnya,
perhatikan bahwa himpunan $X\times\operatorname{in}_\beta(Z_\beta)$ membentuk
sampul terbuka, sehingga kontinuitas dapat diperiksa per komponen lalu
direkatkan.
:::

::: {.hint #o012-d60-r01-hint-005 data-origin="edition-original" data-course-route-unit-id="D60-R01" data-component-id="o012-rbt-l02" data-target-exercise-id="unit:o012-rbt-l02-ex-003" data-existing-solution-id="unit:o012-rbt-l02-sol-003" data-source-path="source/id-ID/units/unit-002-lecture-002.md"}
**Rujukan:** [soal](#o012-rbt-l02-ex-003) · [solusi lengkap](#o012-rbt-l02-sol-003).

**Petunjuk.** Setiap titik pada gabungan saling lepas mengingat tepat satu label
$\beta$, jadi nilai calon $h$ sudah dipaksa oleh $h_\beta$. Setelah fungsi
himpunannya didefinisikan per komponen, jangan periksa kontinuitas dari awal:
gunakan langsung karakterisasi topologi akhir melalui semua inklusi
$\operatorname{in}_\beta$.
:::

::: {.hint #o012-d60-r01-hint-006 data-origin="edition-original" data-course-route-unit-id="D60-R01" data-component-id="o012-rbt-l02" data-target-exercise-id="unit:o012-rbt-l02-ex-004" data-existing-solution-id="unit:o012-rbt-l02-sol-004" data-source-path="source/id-ID/units/unit-002-lecture-002.md"}
**Rujukan:** [soal](#o012-rbt-l02-ex-004) · [solusi lengkap](#o012-rbt-l02-sol-004).

**Petunjuk.** Untuk membuktikan arah yang tidak langsung, misalkan
$A\cap U_\alpha$ terbuka dalam $U_\alpha$ untuk setiap $\alpha$. Gunakan
fakta bahwa setiap $U_\alpha$ sendiri terbuka dalam $X$, lalu tulis $A$ sebagai
gabungan semua $A\cap U_\alpha$. Arah sebaliknya cukup memakai sifat topologi
subruang.
:::

## D60-R02 — keterhubungan, homotopi, dan kategori homotopi {#o012-d60-hints-r02}

::: {.hint #o012-d60-r02-hint-001 data-origin="edition-original" data-course-route-unit-id="D60-R02" data-component-id="o012-rbt-l03" data-target-exercise-id="unit:o012-rbt-l03-ex-001" data-existing-solution-id="unit:o012-rbt-l03-sol-001" data-source-path="source/id-ID/units/unit-003-lecture-003.md"}
**Rujukan:** [soal](#o012-rbt-l03-ex-001) · [solusi lengkap](#o012-rbt-l03-sol-001).

**Petunjuk.** Dari $u\colon X\to S$, angkut fungsi itu ke $Z$ dengan
memakai $h^{-1}$; keunikan diperoleh dengan mengomposisikan kembali dengan
$h$. Kemudian bandingkan citra kedua fungsi. Karakterisasi keterhubungan
melalui semua pemetaan kontinu ke ruang diskret membuat kesimpulan simetris
dalam $X$ dan $Z$.
:::

::: {.hint #o012-d60-r02-hint-002 data-origin="edition-original" data-course-route-unit-id="D60-R02" data-component-id="o012-rbt-l03" data-target-exercise-id="unit:o012-rbt-l03-ex-002" data-existing-solution-id="unit:o012-rbt-l03-sol-002" data-source-path="source/id-ID/units/unit-003-lecture-003.md"}
**Rujukan:** [soal](#o012-rbt-l03-ex-002) · [solusi lengkap](#o012-rbt-l03-sol-002).

**Petunjuk.** Untuk $C\cup D$, batasi satu pemetaan ke ruang diskret pada
$C$ dan $D$; sebuah titik dalam $C\cap D$ memaksa kedua nilai konstan itu
sama. Gunakan hasil ini untuk transitivitas $\sim$. Untuk mengenali kelas
$[x]$, pandanglah ia sebagai gabungan semua himpunan terhubung yang memuat
$x$, lalu buktikan keterhubungan dan kemaksimalannya secara terpisah.
:::

::: {.hint #o012-d60-r02-hint-003 data-origin="edition-original" data-course-route-unit-id="D60-R02" data-component-id="o012-rbt-l03" data-target-exercise-id="unit:o012-rbt-l03-ex-003" data-existing-solution-id="unit:o012-rbt-l03-sol-003" data-source-path="source/id-ID/units/unit-003-lecture-003.md"}
**Rujukan:** [soal](#o012-rbt-l03-ex-003) · [solusi lengkap](#o012-rbt-l03-sol-003).

**Petunjuk.** Jika $Y$ terhubung lintasan, pilih untuk setiap $s\in S$ satu
lintasan dari nilai pemetaan pertama ke nilai pemetaan kedua. Diskretnya $S$
memungkinkan lintasan-lintasan itu dirakit menjadi pemetaan kontinu pada
$I\times S$. Untuk arah balik, pilih ruang diskret sekecil mungkin yang masih
merekam dua titik sebarang di $Y$.
:::

::: {.hint #o012-d60-r02-hint-004 data-origin="edition-original" data-course-route-unit-id="D60-R02" data-component-id="o012-rbt-l03" data-target-exercise-id="unit:o012-rbt-l03-ex-004" data-existing-solution-id="unit:o012-rbt-l03-sol-004" data-source-path="source/id-ID/units/unit-003-lecture-003.md"}
**Rujukan:** [soal](#o012-rbt-l03-ex-004) · [solusi lengkap](#o012-rbt-l03-sol-004).

**Petunjuk.** Pada morfisma $h\colon Y\to Z$, calon pemetaan
$[A,Y]\to[A,Z]$ harus berupa pascakomposisi. Periksa lebih dahulu bahwa
homotopi antara dua wakil tetap menjadi homotopi setelah dipascakomposisikan
dengan $h$. Sesudah itu, hukum identitas dan komposisi mengikuti dari hukum
komposisi fungsi biasa.
:::

::: {.hint #o012-d60-r02-hint-005 data-origin="edition-original" data-course-route-unit-id="D60-R02" data-component-id="o012-rbt-l03" data-target-exercise-id="unit:o012-rbt-l03-ex-005" data-existing-solution-id="unit:o012-rbt-l03-sol-005" data-source-path="source/id-ID/units/unit-003-lecture-003.md"}
**Rujukan:** [soal](#o012-rbt-l03-ex-005) · [solusi lengkap](#o012-rbt-l03-sol-005).

**Petunjuk.** Untuk kemandirian wakil dari $[g\circ f]$, ubah dahulu wakil
$f$ sambil menahan $g$, lalu ubah wakil $g$ sambil menahan hasil perubahan
$f$; gabungkan kedua homotopi. Setelah kategori terbentuk, terjemahkan
persamaan invers di $\mathbf{Ho}$ kembali menjadi dua homotopi terhadap
pemetaan identitas.
:::

::: {.hint #o012-d60-r02-hint-006 data-origin="edition-original" data-course-route-unit-id="D60-R02" data-component-id="o012-rbt-l04" data-target-exercise-id="unit:o012-rbt-l04-ex-001" data-existing-solution-id="unit:o012-rbt-l04-sol-001" data-source-path="source/id-ID/units/unit-004-lecture-004.md"}
**Rujukan:** [soal](#o012-rbt-l04-ex-001) · [solusi lengkap](#o012-rbt-l04-sol-001).

**Petunjuk.** Untuk morfisma $[f]\colon X\to Y$ di $\mathbf{Ho}$, kandidat
aksi pada $[*,X]$ adalah $[u]\mapsto[f\circ u]$. Ada dua kemandirian wakil
yang harus diperiksa secara terpisah: wakil $u$ dan wakil $f$. Baru setelah
keduanya selesai, verifikasi identitas dan komposisi.
:::

## D60-R03 — ruang penutup, tarik balik, dan transpor {#o012-d60-hints-r03}

::: {.hint #o012-d60-r03-hint-001 data-origin="edition-original" data-course-route-unit-id="D60-R03" data-component-id="o012-rbt-l05" data-target-exercise-id="unit:o012-rbt-l05-mcheck-001" data-existing-solution-id="unit:o012-rbt-l05-sol-001" data-source-path="source/id-ID/units/unit-005-lecture-005.md"}
**Rujukan:** [soal](#o012-rbt-l05-mcheck-001) · [solusi lengkap](#o012-rbt-l05-sol-001).

**Petunjuk.** Pisahkan “ada suatu bijeksi di antara dua serat” dari “lintasan
tertentu menentukan suatu bijeksi”. Pada pernyataan kedua, ikuti satu titik
serat melalui pengangkatan tunggal dan evaluasi titik akhirnya. Lalu tanyakan
apa yang berubah jika lintasan antara dua titik dasar diganti dengan lintasan
lain.
:::

::: {.hint #o012-d60-r03-hint-002 data-origin="edition-original" data-course-route-unit-id="D60-R03" data-component-id="o012-rbt-l05" data-target-exercise-id="unit:o012-rbt-l05-mcheck-002" data-existing-solution-id="unit:o012-rbt-l05-sol-002" data-source-path="source/id-ID/units/unit-005-lecture-005.md"}
**Rujukan:** [soal](#o012-rbt-l05-mcheck-002) · [solusi lengkap](#o012-rbt-l05-sol-002).

**Petunjuk.** Untuk trivialitas lokal, tarik kembali suatu trivialisasi di
atas $V\subseteq X$ ke $f^{-1}(V)\subseteq Y$. Pada morfisma, pertahankan
koordinat $y$ dan terapkan morfisma pada koordinat serat. Untuk komposisi dua
tarik balik, tulis kedua himpunan hasil kali serat secara eksplisit; untuk
isomorfisma serat, gunakan proyeksi $(y,z)\mapsto z$.
:::

::: {.hint #o012-d60-r03-hint-003 data-origin="edition-original" data-course-route-unit-id="D60-R03" data-component-id="o012-rbt-l05" data-target-exercise-id="unit:o012-rbt-l05-mcheck-003" data-existing-solution-id="unit:o012-rbt-l05-sol-003" data-source-path="source/id-ID/units/unit-005-lecture-005.md"}
**Rujukan:** [soal](#o012-rbt-l05-mcheck-003) · [solusi lengkap](#o012-rbt-l05-sol-003).

**Petunjuk.** Tulis titik pada $S^1$ melalui koordinat sudut modulo $1$.
Carilah fungsi sudut $a(t)$ yang memenuhi $na(t)\equiv t\pmod 1$ dan
$a(0)=k/n$. Setelah memverifikasi proyeksinya, transpor diperoleh hanya dengan
mengevaluasi pengangkatan itu pada $t=1$.
:::

::: {.hint #o012-d60-r03-hint-004 data-origin="edition-original" data-course-route-unit-id="D60-R03" data-component-id="o012-rbt-l05" data-target-exercise-id="unit:o012-rbt-l05-mcheck-004" data-existing-solution-id="unit:o012-rbt-l05-sol-004" data-source-path="source/id-ID/units/unit-005-lecture-005.md"}
**Rujukan:** [soal](#o012-rbt-l05-mcheck-004) · [solusi lengkap](#o012-rbt-l05-sol-004).

**Petunjuk.** Ambil pengangkatan $\widetilde\gamma_z$ di $Z_1$ lalu
komposisikan dengan $h$. Persamaan bahwa $h$ berada di atas $X$ menunjukkan
bahwa komposisi ini masih mengangkat $\gamma$ dan mempunyai titik awal
$h(z)$. Gunakan ketunggalan pengangkatan sebelum mengevaluasi kedua ruas pada
titik akhir.
:::

::: {.hint #o012-d60-r03-hint-005 data-origin="edition-original" data-course-route-unit-id="D60-R03" data-component-id="o012-rbt-l06" data-target-exercise-id="unit:o012-rbt-l06-mcheck-001" data-existing-solution-id="unit:o012-rbt-l06-sol-001" data-source-path="source/id-ID/units/unit-006-lecture-006.md"}
**Rujukan:** [soal](#o012-rbt-l06-mcheck-001) · [solusi lengkap](#o012-rbt-l06-sol-001).

**Petunjuk.** Mulailah di titik serat $2\pi k$ dan cari pengangkatan afin dari
$\gamma_n$; kemiringannya ditentukan oleh bilangan putaran $n$. Untuk
konkatenasi, jangan memulai pengangkatan bagian kedua lagi di $2\pi k$:
mulailah di titik akhir bagian pertama dan lacak perubahan total indeks
bilangan bulat.
:::

::: {.hint #o012-d60-r03-hint-006 data-origin="edition-original" data-course-route-unit-id="D60-R03" data-component-id="o012-rbt-l06" data-target-exercise-id="unit:o012-rbt-l06-mcheck-002" data-existing-solution-id="unit:o012-rbt-l06-sol-002" data-source-path="source/id-ID/units/unit-006-lecture-006.md"}
**Rujukan:** [soal](#o012-rbt-l06-mcheck-002) · [solusi lengkap](#o012-rbt-l06-sol-002).

**Petunjuk.** Pecah bukti menjadi empat tahap. (1) Bandingkan irisan berhingga
subbasis $[K,O]$ dengan lingkungan yang berasal dari partisi interval; untuk
arah sulit gunakan kekompakan dan bilangan Lebesgue. (2) Uji evaluasi dan
pascakomposisi pada subbasis. (3) Untuk kasus metrik, buktikan dua inklusi
topologi dengan jarak positif dari citra kompak ke komplemen dan kekontinuan
seragam. (4) Untuk hukum eksponensial, gunakan kekompakan $K$ saat membuktikan
kekontinuan pemetaan teradjung, dan evaluasi untuk arah sebaliknya.
:::

## D60-R04 — grup fundamental, grupoid, dan aksi monodromi {#o012-d60-hints-r04}

::: {.hint #o012-d60-r04-hint-001 data-origin="edition-original" data-course-route-unit-id="D60-R04" data-component-id="o012-rbt-l07" data-target-exercise-id="unit:o012-rbt-l07-mcheck-001" data-existing-solution-id="unit:o012-rbt-l07-sol-001" data-source-path="source/id-ID/units/unit-007-lecture-007.md"}
**Rujukan:** [soal](#o012-rbt-l07-mcheck-001) · [solusi lengkap](#o012-rbt-l07-sol-001).

**Petunjuk.** Angkat $\gamma$ dari $z$, lalu angkat $\eta$ dari titik akhir
pengangkatan pertama. Konkatenasi kedua lintasan terangkat memproyeksikan ke
$\gamma\#\eta$. Bandingkan lintasan ini dengan pengangkatan tunggal
$\gamma\#\eta$ yang berawal di $z$, kemudian evaluasi di $t=1$ dan perhatikan
urutan komposisinya.
:::

::: {.hint #o012-d60-r04-hint-002 data-origin="edition-original" data-course-route-unit-id="D60-R04" data-component-id="o012-rbt-l07" data-target-exercise-id="unit:o012-rbt-l07-mcheck-002" data-existing-solution-id="unit:o012-rbt-l07-sol-002" data-source-path="source/id-ID/units/unit-007-lecture-007.md"}
**Rujukan:** [soal](#o012-rbt-l07-mcheck-002) · [solusi lengkap](#o012-rbt-l07-sol-002).

**Petunjuk.** Bentuk dahulu pemetaan evaluasi tiga variabel yang memakai
$\gamma(2t)$ pada separuh interval pertama dan $\eta(2t-1)$ pada separuh
kedua. Buktikan kontinuitasnya dengan lema penempelan pada dua subruang
tertutup. Hukum eksponensial untuk topologi kompak-terbuka kemudian mengubah
pemetaan itu menjadi konkatenasi bernilai di subruang $\Omega_xX$.
:::

::: {.hint #o012-d60-r04-hint-003 data-origin="edition-original" data-course-route-unit-id="D60-R04" data-component-id="o012-rbt-l07" data-target-exercise-id="unit:o012-rbt-l07-mcheck-003" data-existing-solution-id="unit:o012-rbt-l07-sol-003" data-source-path="source/id-ID/units/unit-007-lecture-007.md"}
**Rujukan:** [soal](#o012-rbt-l07-mcheck-003) · [solusi lengkap](#o012-rbt-l07-sol-003).

**Petunjuk.** Untuk komponen produk, gunakan keterhubungan produk dua
komponen dan proyeksi setiap himpunan terhubung di dalam produk. Aksioma grup
pada kelas diperoleh dengan menunjukkan bahwa kedua sisi tiap hukum
dihubungkan oleh lintasan di ruang loop. Terakhir, cocokkan
$(z\cdot[\gamma])\cdot[\eta]$ dengan rumus transpor untuk
$\gamma\#\eta$; ini menentukan sisi aksinya.
:::

::: {.hint #o012-d60-r04-hint-004 data-origin="edition-original" data-course-route-unit-id="D60-R04" data-component-id="o012-rbt-l07" data-target-exercise-id="unit:o012-rbt-l07-mcheck-004" data-existing-solution-id="unit:o012-rbt-l07-sol-004" data-source-path="source/id-ID/units/unit-007-lecture-007.md"}
**Rujukan:** [soal](#o012-rbt-l07-mcheck-004) · [solusi lengkap](#o012-rbt-l07-sol-004).

**Petunjuk.** Bangun fungtor ruang loop dengan pascakomposisi, lalu ambil
komponen lintasan untuk memperoleh $\pi_1$. Untuk model lingkaran, gunakan
pemetaan hasil bagi $q\colon I\to I/\{0\sim1\}\cong S^1$: loop memfaktor secara
unik melalui $q$, dan homotopi berujung tetap memfaktor melalui
$\operatorname{id}_I\times q$. Periksa naturalitas dengan pascakomposisi;
pemetaan jepit pada $S^1$ menangani perkalian.
:::

::: {.hint #o012-d60-r04-hint-005 data-origin="edition-original" data-course-route-unit-id="D60-R04" data-component-id="o012-rbt-l08" data-target-exercise-id="unit:o012-rbt-l08-ex-001" data-existing-solution-id="unit:o012-rbt-l08-sol-001" data-source-path="source/id-ID/units/unit-008-lecture-008.md"}
**Rujukan:** [soal](#o012-rbt-l08-ex-001) · [solusi lengkap](#o012-rbt-l08-sol-001).

**Petunjuk.** Gunakan pusat bintang $v_0$ untuk menggerakkan setiap titik
sepanjang ruas garis menuju $v_0$. Periksa bahwa definisi daerah berbentuk
bintang menjaga seluruh homotopi tetap di $K$. Dari homotopi ini, peroleh
lintasan menuju pusat dan bandingkan setiap dua lintasan dengan titik ujung
yang sama melalui lintasan kanonik yang melewati pusat.
:::

::: {.hint #o012-d60-r04-hint-006 data-origin="edition-original" data-course-route-unit-id="D60-R04" data-component-id="o012-rbt-l08" data-target-exercise-id="unit:o012-rbt-l08-mcheck-002" data-existing-solution-id="unit:o012-rbt-l08-sol-002" data-source-path="source/id-ID/units/unit-008-lecture-008.md"}
**Rujukan:** [soal](#o012-rbt-l08-mcheck-002) · [solusi lengkap](#o012-rbt-l08-sol-002).

**Petunjuk.** Tipekan setiap komposisi panah sebelum menghitung: suatu panah
$a\colon x\to y$ mengangkut automorfisma di $x$ ke automorfisma di $y$ lewat
konjugasi, sedangkan himpunan panah $x\to y$ menjadi torsor di bawah
automorfisma di $x$. Pada $Y/\!/G$, komponen grupoid adalah orbit dan
automorfisma suatu objek adalah stabilisatornya. Terjemahkan “tepat satu
morfisma” untuk menentukan syarat diskret dan kodiskret, termasuk kasus
$Y=\varnothing$.
:::

## D60-R05 — pushout dan Seifert–van Kampen {#o012-d60-hints-r05}

::: {.hint #o012-d60-r05-hint-001 data-origin="edition-original" data-course-route-unit-id="D60-R05" data-component-id="o012-rbt-l11" data-target-exercise-id="unit:o012-rbt-l11-mcheck-001" data-existing-solution-id="unit:o012-rbt-l11-sol-001" data-source-path="source/id-ID/units/unit-011-lecture-011.md"}
**Rujukan:** [soal](#o012-rbt-l11-mcheck-001) · [solusi lengkap](#o012-rbt-l11-sol-001).

**Petunjuk.** Pada $F_n$, tentukan nilai homomorfisma pada kata tereduksi
dengan mengganti setiap $x_i^{\pm1}$ oleh $k_i^{\pm1}$; periksa bahwa
penyisipan pasangan invers tidak mengubah nilai. Untuk $G*H$, lakukan hal yang
sama pada kata bergantian dan gunakan tidak adanya relasi silang. Pada bagian
terakhir, tulis domain dan kodomain setiap panah sebelum memilih urutan
komposisi.
:::

::: {.hint #o012-d60-r05-hint-002 data-origin="edition-original" data-course-route-unit-id="D60-R05" data-component-id="o012-rbt-l11" data-target-exercise-id="unit:o012-rbt-l11-mcheck-002" data-existing-solution-id="unit:o012-rbt-l11-sol-002" data-source-path="source/id-ID/units/unit-011-lecture-011.md"}
**Rujukan:** [soal](#o012-rbt-l11-mcheck-002) · [solusi lengkap](#o012-rbt-l11-sol-002).

**Petunjuk.** Untuk pushout topologis, definisikan peta pada $U\cup V$ secara
sepotong-sepotong dan gunakan kesepakatan di $U\cap V$ bersama lema
perekatan. Untuk pushout ruang vektor, mulai dari peta linear
$T(v_1,v_2)=A(v_1)+B(v_2)$ pada $V_1\oplus V_2$. Syarat kompatibilitas harus
menunjukkan bahwa $J(W)\subseteq\ker T$, sehingga $T$ turun ke hasil bagi.
:::

::: {.hint #o012-d60-r05-hint-003 data-origin="edition-original" data-course-route-unit-id="D60-R05" data-component-id="o012-rbt-l11" data-target-exercise-id="unit:o012-rbt-l11-mcheck-003" data-existing-solution-id="unit:o012-rbt-l11-sol-003" data-source-path="source/id-ID/units/unit-011-lecture-011.md"}
**Rujukan:** [soal](#o012-rbt-l11-mcheck-003) · [solusi lengkap](#o012-rbt-l11-sol-003).

**Petunjuk.** Saat satu ruas partisi dibelah, tunjukkan bahwa satu faktor lama
diganti oleh produk dua faktor yang sama nilainya; dua partisi dapat
dibandingkan melalui perhalusan bersama. Untuk $P(s,u)$, periksa dahulu
penempelan rumus pada $s=1/2$, lalu keempat sisi persegi. Akhirnya, tunjukkan
secara eksplisit langkah yang masih hilang ketika citra homotopi tidak berada
seluruhnya dalam satu anggota sampul.
:::

::: {.hint #o012-d60-r05-hint-004 data-origin="edition-original" data-course-route-unit-id="D60-R05" data-component-id="o012-rbt-l12" data-target-exercise-id="unit:o012-rbt-l12-mcheck-001" data-existing-solution-id="unit:o012-rbt-l12-sol-001" data-source-path="source/id-ID/units/unit-012-lecture-012.md"}
**Rujukan:** [soal](#o012-rbt-l12-mcheck-001) · [solusi lengkap](#o012-rbt-l12-sol-001).

**Petunjuk.** Pertukaran rute pada satu sel berlangsung seluruhnya di $U$ atau
$V$, jadi kesamaannya berasal dari fungtor lokal $F$ atau $G$, bukan dari
fungtor global yang sedang dibangun. Untuk hukum komposisi, gabungkan dua
partisi subordinat menjadi satu partisi bagi lintasan gabungan. Untuk
keunikan, faktorkan setiap morfisma menjadi ruas-ruas lokal yang nilainya
sudah dipaksa.
:::

::: {.hint #o012-d60-r05-hint-005 data-origin="edition-original" data-course-route-unit-id="D60-R05" data-component-id="o012-rbt-l12" data-target-exercise-id="unit:o012-rbt-l12-mcheck-002" data-existing-solution-id="unit:o012-rbt-l12-sol-002" data-source-path="source/id-ID/units/unit-012-lecture-012.md"}
**Rujukan:** [soal](#o012-rbt-l12-mcheck-002) · [solusi lengkap](#o012-rbt-l12-sol-002).

**Petunjuk.** Mulai dari satu kocone kompatibel pada persegi retrak $S$.
Prakomposisikan kedua kakinya dengan komponen retraksi untuk memperoleh
kocone pada pushout $T$, lalu gunakan sifat universal $T$. Bawa peta universal
yang dihasilkan kembali ke $S$ melalui komponen inklusi. Untuk keunikan,
angkat setiap pesaing dari $S$ ke $T$ dan gunakan persamaan
$r\circ i=\operatorname{id}_S$.
:::

::: {.hint #o012-d60-r05-hint-006 data-origin="edition-original" data-course-route-unit-id="D60-R05" data-component-id="o012-rbt-l12" data-target-exercise-id="unit:o012-rbt-l12-mcheck-003" data-existing-solution-id="unit:o012-rbt-l12-sol-003" data-source-path="source/id-ID/units/unit-012-lecture-012.md"}
**Rujukan:** [soal](#o012-rbt-l12-mcheck-003) · [solusi lengkap](#o012-rbt-l12-sol-003).

**Petunjuk.** Kirim setiap objek $x$ ke titik pilihan $a_x$, dan pada suatu
kelas lintasan tempelkan kebalikan lintasan pilihan di ujung awal serta
lintasan pilihan di ujung akhir. Periksa identitas dan komposisi dengan
membatalkan pasangan lintasan yang saling berbalik. Dalam kubus Teorema 12.1,
pilihan pada irisan harus dipakai serentak oleh semua pembatasan agar
komutativitasnya ketat, bukan hanya hingga isomorfisma.
:::

## D60-R06 — klasifikasi ruang penutup {#o012-d60-hints-r06}

::: {.hint #o012-d60-r06-hint-001 data-origin="edition-original" data-course-route-unit-id="D60-R06" data-component-id="o012-rbt-l14" data-target-exercise-id="unit:o012-rbt-l14-ex-001" data-existing-solution-id="unit:o012-rbt-l14-sol-002" data-source-path="source/id-ID/units/unit-014-lecture-014.md"}
**Rujukan:** [soal](#o012-rbt-l14-ex-001) · [solusi lengkap](#o012-rbt-l14-sol-002).

**Petunjuk.** Karena $i\colon\mathcal C\hookrightarrow\mathcal D$ adalah
ekuivalensi, pilih invers semu $r$ beserta isomorfisma natural
$ri\cong\operatorname{id}_{\mathcal C}$ dan
$ir\cong\operatorname{id}_{\mathcal D}$. Prakomposisi dengan $r$ adalah calon
invers semu bagi $i^*$. Prakomposisikan fungtor sebarang dengan $ri$ atau $ir$
untuk memperoleh isomorfisma natural yang diperlukan.
:::

::: {.hint #o012-d60-r06-hint-002 data-origin="edition-original" data-course-route-unit-id="D60-R06" data-component-id="o012-rbt-l14" data-target-exercise-id="unit:o012-rbt-l14-ex-002" data-existing-solution-id="unit:o012-rbt-l14-sol-003" data-source-path="source/id-ID/units/unit-014-lecture-014.md"}
**Rujukan:** [soal](#o012-rbt-l14-ex-002) · [solusi lengkap](#o012-rbt-l14-sol-003).

**Petunjuk.** Satu arah diperoleh dengan membatasi suatu fungtor pada setiap
$\mathcal C_i$; lakukan hal yang sama pada transformasi natural. Untuk arah
balik, rakit tupel fungtor komponen demi komponen. Ketiadaan morfisma di antara
dua faktor berbeda menjamin bahwa perakitan itu lengkap dan bahwa kedua
konstruksi benar-benar saling invers.
:::

::: {.hint #o012-d60-r06-hint-003 data-origin="edition-original" data-course-route-unit-id="D60-R06" data-component-id="o012-rbt-l14" data-target-exercise-id="unit:o012-rbt-l14-mcheck-001" data-existing-solution-id="unit:o012-rbt-l14-sol-001" data-source-path="source/id-ID/units/unit-014-lecture-014.md"}
**Rujukan:** [soal](#o012-rbt-l14-mcheck-001) · [solusi lengkap](#o012-rbt-l14-sol-001).

**Petunjuk.** Untuk bagian pertama, komposisikan pengangkatan $\gamma$ di
$Z_1$ dengan $f$ dan gunakan ketunggalan pengangkatan di $Z_2$. Untuk bagian
kedua, tulis $(g\circ f)_x$ sebagai komposisi pemetaan serat, lalu tumpuk dua
persegi naturalitas. Perhitungan yang sama sekaligus menunjukkan pelestarian
komposisi oleh fungtor monodromi.
:::

::: {.hint #o012-d60-r06-hint-004 data-origin="edition-original" data-course-route-unit-id="D60-R06" data-component-id="o012-rbt-l14" data-target-exercise-id="unit:o012-rbt-l14-mcheck-004" data-existing-solution-id="unit:o012-rbt-l14-sol-004" data-source-path="source/id-ID/units/unit-014-lecture-014.md"}
**Rujukan:** [soal](#o012-rbt-l14-mcheck-004) · [solusi lengkap](#o012-rbt-l14-sol-004).

**Petunjuk.** Sebuah fungtor $F\colon\mathbf BG\to\mathbf{Set}$ hanya
mempunyai satu himpunan objek $S=F(*)$. Definisikan aksi melalui nilai
$F(g)$, lalu gunakan konvensi produk kronologis untuk menentukan apakah
aksinya kiri atau kanan. Sebaliknya, bangun fungtor dari aksi tersebut.
Syarat naturalitas pada setiap $g\in G$ harus berubah tepat menjadi syarat
ekuivarians bagi satu fungsi $S\to T$.
:::

::: {.hint #o012-d60-r06-hint-005 data-origin="edition-original" data-course-route-unit-id="D60-R06" data-component-id="o012-rbt-l14" data-target-exercise-id="unit:o012-rbt-l14-mcheck-005" data-existing-solution-id="unit:o012-rbt-l14-sol-005" data-source-path="source/id-ID/units/unit-014-lecture-014.md"}
**Rujukan:** [soal](#o012-rbt-l14-mcheck-005) · [solusi lengkap](#o012-rbt-l14-sol-005).

**Petunjuk.** Setelah memilih titik dasar $1\in S^1$, tulis operator
monodromi sebagai operator dari $\pi_1(S^1,1)$—bukan dari seluruh grupoid—ke
permutasi serat. Uji ekuivarians reduksi modulo $n$ langsung pada aksi
translasi. Untuk butir terakhir, bandingkan urutan operator pada aksi kanan
dengan aksi kiri dan perhatikan apa yang disembunyikan oleh komutativitas
$\mathbb Z$.
:::

::: {.hint #o012-d60-r06-hint-006 data-origin="edition-original" data-course-route-unit-id="D60-R06" data-component-id="o012-rbt-l14" data-target-exercise-id="unit:o012-rbt-l14-mcheck-006" data-existing-solution-id="unit:o012-rbt-l14-sol-006" data-source-path="source/id-ID/units/unit-014-lecture-014.md"}
**Rujukan:** [soal](#o012-rbt-l14-mcheck-006) · [solusi lengkap](#o012-rbt-l14-sol-006).

**Petunjuk.** Panah di $\Pi_1(X,A)$ adalah kelas lintasan, sehingga dua titik
pilihan dari komponen berbeda tidak dapat dihubungkan; esensial surjektif
dibuktikan dengan menghubungkan setiap titik $X$ ke wakil komponennya. Untuk
orbit $pG$, coba peta $Hg\mapsto p\cdot g$ dengan
$H=\operatorname{Stab}(p)$ dan periksa keterdefinisian serta ekuivariansnya.
Terakhir, angkat basis lingkungan terhubung lintasan pada ruang dasar ke setiap
lembaran ruang penutup dan gunakan keterhubungan lintasan lokal ruang total.
:::
