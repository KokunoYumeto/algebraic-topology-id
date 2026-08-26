---
title: "Asesmen Kumulatif 1 — Topologi Dasar, Ruang Penutup, dan Homotopi"
lang: id-ID
course_id: D60
assessment_id: D60-CA01
edition_unit_id: O012-ORIG-CA01
course_route_unit_ids:
  - D60-R01
  - D60-R02
  - D60-R03
  - D60-R04
  - D60-R05
  - D60-R06
  - D60-R07
rights: "CC BY-SA 4.0"
origin: "Materi edisi asli; bukan bagian dari sumber Roberts atau Fomberg."
provenance: "OpenAI Codex gpt-5.6-sol, Ultra; disusun atas arahan pengguna; kredit dan hak komponen sumber tetap dipertahankan."
---

# Asesmen Kumulatif 1: fondasi hingga barisan eksak homotopi {#o012-d60-ca01}

Asesmen ini menguji hubungan lintas-topik dari `D60-R01` sampai `D60-R07`.
Setiap soal diikuti petunjuk dan solusi lengkap. Untuk pemakaian sebagai ujian,
kerjakan delapan soal terlebih dahulu tanpa membuka kedua bagian tersebut.
Seluruh soal dan solusi pada berkas ini merupakan materi edisi asli berlisensi
CC BY-SA 4.0; materi ini tidak mengubah urutan atau penomoran edisi Roberts dan
Fomberg.

## Soal 1 — hasil bagi interval dan lingkaran {#o012-d60-ca01-s01}

::: {.exercise #o012-d60-ca01-ex-001 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R01"}
Pada $I=[0,1]$, ambil relasi ekuivalensi yang hanya mengidentifikasi $0$ dengan
$1$, dan tulis $q:I\to I/{\sim}$ untuk peta hasil bagi. Buktikan bahwa

$$
\bar f:I/{\sim}\longrightarrow S^1,
\qquad
\bar f([t])=(\cos 2\pi t,\sin 2\pi t),
$$

adalah homeomorfisma. Dalam bukti Anda, jelaskan secara terpisah mengapa
$\bar f$ terdefinisi dengan baik, kontinu, dan mempunyai invers kontinu.
:::

::: {.hint #o012-d60-ca01-hint-001 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R01"}
**Petunjuk.** Mulailah dari $f(t)=(\cos 2\pi t,\sin 2\pi t)$. Gunakan sifat
universal topologi hasil bagi. Setelah memperoleh bijeksi kontinu, gunakan
kekompakan $I/{\sim}$ dan sifat Hausdorff $S^1$.
:::

::: {.solution #o012-d60-ca01-sol-001 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R01"}
**Solusi.** Fungsi $f:I\to S^1$ memenuhi $f(0)=f(1)$, sehingga nilainya konstan
pada setiap kelas ekuivalensi. Karena itu rumus $\bar f([t])=f(t)$ terdefinisi
dengan baik dan memenuhi $f=\bar f\circ q$. Berdasarkan sifat universal peta
hasil bagi, kontinuitas $f$ mengimplikasikan kontinuitas $\bar f$.

Setiap titik $S^1$ mempunyai representasi $(\cos 2\pi t,\sin 2\pi t)$ untuk
suatu $t\in[0,1]$, jadi $\bar f$ surjektif. Jika $f(s)=f(t)$, maka
$s-t\in\mathbb Z$. Untuk $s,t\in[0,1]$, hal ini berarti $s=t$ atau
$\{s,t\}=\{0,1\}$; kedua kemungkinan memberi $[s]=[t]$. Jadi $\bar f$
injektif.

Ruang $I/{\sim}$ kompak karena merupakan citra kontinu ruang kompak $I$, dan
$S^1$ Hausdorff. Setiap bijeksi kontinu dari ruang kompak ke ruang Hausdorff
adalah homeomorfisma. Maka invers $\bar f^{-1}$ kontinu, sehingga $\bar f$
adalah homeomorfisma.
:::

## Soal 2 — retraksi deformasi kuat {#o012-d60-ca01-s02}

::: {.exercise #o012-d60-ca01-ex-002 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R02"}
Untuk $X=\mathbb R^2\setminus\{0\}$, definisikan

$$
H(x,t)=\left((1-t)+\frac{t}{\lVert x\rVert}\right)x.
$$

Buktikan bahwa $H$ adalah retraksi deformasi kuat $X$ ke $S^1$. Simpulkan
bahwa inklusi $i:S^1\hookrightarrow X$ menginduksi isomorfisma pada grup
fundamental.
:::

::: {.hint #o012-d60-ca01-hint-002 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R02"}
**Petunjuk.** Periksa empat hal: kontinuitas, fakta bahwa $H(x,t)\ne0$ untuk
semua $(x,t)$, nilai pada $t=0$ dan $t=1$, serta apa yang terjadi bila
$\lVert x\rVert=1$.
:::

::: {.solution #o012-d60-ca01-sol-002 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R02"}
**Solusi.** Fungsi norma tidak nol pada $X$, sehingga $H$ kontinu. Koefisien

$$
(1-t)+\frac{t}{\lVert x\rVert}
$$

selalu positif untuk $0\le t\le1$; akibatnya $H(x,t)\ne0$ dan seluruh homotopi
berada di $X$. Selain itu,

$$
H(x,0)=x,
\qquad
H(x,1)=\frac{x}{\lVert x\rVert}\in S^1.
$$

Jika $x\in S^1$, koefisien tersebut sama dengan $1$ untuk semua $t$, jadi
$H(x,t)=x$. Dengan demikian $r(x)=x/\lVert x\rVert$ adalah retraksi dan $H$
adalah homotopi dari $\operatorname{id}_X$ ke $i\circ r$ yang tetap pada
$S^1$: tepatnya suatu retraksi deformasi kuat.

Karena $r\circ i=\operatorname{id}_{S^1}$ dan
$i\circ r\simeq\operatorname{id}_X$, peta $i$ dan $r$ adalah ekuivalensi
homotopi. Funktorialitas grup fundamental kemudian memberi isomorfisma
$i_*:\pi_1(S^1)\xrightarrow{\cong}\pi_1(X)$.
:::

## Soal 3 — pengangkatan lintasan dan bilangan lilit {#o012-d60-ca01-s03}

::: {.exercise #o012-d60-ca01-ex-003 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R03"}
Ambil peta penutup $p:\mathbb R\to S^1$, $p(u)=e^{2\pi i u}$, dan loop

$$
\gamma(s)=e^{2\pi i(3s+1/4)},\qquad 0\le s\le1.
$$

Tentukan pengangkatan tunggal $\widetilde\gamma$ yang memenuhi
$\widetilde\gamma(0)=1/4$. Hitung titik akhirnya dan jelaskan bagaimana hasil
itu merekam kelas $[\gamma]$ di $\pi_1(S^1,i)$.
:::

::: {.hint #o012-d60-ca01-hint-003 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R03"}
**Petunjuk.** Coba $\widetilde\gamma(s)=3s+1/4$, lalu gunakan ketunggalan
pengangkatan dengan titik awal tetap. Selisih titik akhir dan titik awal adalah
bilangan bulat.
:::

::: {.solution #o012-d60-ca01-sol-003 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R03"}
**Solusi.** Rumus

$$
\widetilde\gamma(s)=3s+\frac14
$$

memenuhi $\widetilde\gamma(0)=1/4$ dan
$p(\widetilde\gamma(s))=\gamma(s)$. Teorema pengangkatan lintasan menjamin
bahwa inilah satu-satunya pengangkatan dengan titik awal tersebut. Titik
akhirnya ialah

$$
\widetilde\gamma(1)=\frac{13}{4}
=\frac14+3.
$$

Untuk penutup universal $\mathbb R\to S^1$, selisih bilangan bulat antara
titik akhir dan titik awal pengangkatan loop adalah bilangan lilitnya. Jadi
$[\gamma]$ bersesuaian dengan $3\in\mathbb Z\cong\pi_1(S^1,i)$. Pengangkatan
tidak tertutup karena kelas ini bukan nol.
:::

## Soal 4 — monodromi penutup berhingga {#o012-d60-ca01-s04}

::: {.exercise #o012-d60-ca01-ex-004 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R04"}
Untuk $n\ge2$, ambil $p_n:S^1\to S^1$, $p_n(z)=z^n$. Beri label serat di
atas $1$ dengan $\zeta_j=e^{2\pi i j/n}$, $j\in\mathbb Z/n\mathbb Z$.
Hitung aksi monodromi generator $\lambda(t)=e^{2\pi i t}$ pada serat itu.
Gunakan hasilnya untuk menentukan keterhubungan ruang total, stabilisator
$\zeta_0$, dan grup transformasi dek.
:::

::: {.hint #o012-d60-ca01-hint-004 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R04"}
**Petunjuk.** Angkat $\lambda$ dari $\zeta_j$ dengan lintasan
$t\mapsto e^{2\pi i(t+j)/n}$. Ingat bahwa orbit monodromi adalah komponen
ruang total.
:::

::: {.solution #o012-d60-ca01-sol-004 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R04"}
**Solusi.** Pengangkatan yang berawal di $\zeta_j$ ialah

$$
\widetilde\lambda_j(t)=e^{2\pi i(t+j)/n},
$$

sebab $p_n(\widetilde\lambda_j(t))=e^{2\pi i(t+j)}=\lambda(t)$. Titik akhirnya
adalah $\zeta_{j+1}$. Jadi generator $1\in\pi_1(S^1)\cong\mathbb Z$ bertindak
dengan siklus

$$
j\longmapsto j+1\pmod n.
$$

Aksi ini transitif, sehingga ruang total penutup terhubung. Suatu unsur
$m\in\mathbb Z$ menstabilkan $\zeta_0$ tepat bila $m\equiv0\pmod n$; jadi
stabilisatornya $n\mathbb Z$. Transformasi dek adalah rotasi
$z\mapsto\zeta_jz$. Rotasi-rotasi ini membentuk grup siklik berorde $n$, maka
$\operatorname{Deck}(p_n)\cong\mathbb Z/n\mathbb Z$.
:::

## Soal 5 — van Kampen dan grup fundamental torus {#o012-d60-ca01-s05}

::: {.exercise #o012-d60-ca01-ex-005 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R05"}
Gunakan model CW torus $T^2$ yang mempunyai satu sel-$0$, dua sel-$1$ berlabel
$a,b$, dan satu sel-$2$ yang dilekatkan sepanjang kata
$aba^{-1}b^{-1}$. Terapkan teorema Seifert–van Kampen untuk menghitung
$\pi_1(T^2)$.
:::

::: {.hint #o012-d60-ca01-hint-005 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R05"}
**Petunjuk.** Kerangka-$1$ adalah $S^1\vee S^1$ dengan grup bebas pada
$a,b$. Pelekatan sel-$2$ menambahkan satu relasi: kata pelekat menjadi unsur
identitas.
:::

::: {.solution #o012-d60-ca01-sol-005 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R05"}
**Solusi.** Kerangka-$1$ torus mempunyai grup fundamental
$F(a,b)$, grup bebas pada dua generator. Menurut van Kampen, pelekatan sel-$2$
di sepanjang loop yang mewakili $aba^{-1}b^{-1}$ menghasilkan hasil bagi grup
bebas oleh penutupan normal kata tersebut. Jadi

$$
\pi_1(T^2)
\cong
\langle a,b\mid aba^{-1}b^{-1}=1\rangle
=\langle a,b\mid ab=ba\rangle.
$$

Presentasi terakhir adalah grup abelian bebas pada $a$ dan $b$. Pemetaan
$a\mapsto(1,0)$ dan $b\mapsto(0,1)$ memberi isomorfisma
$\pi_1(T^2)\cong\mathbb Z^2$.
:::

## Soal 6 — klasifikasi penutup lingkaran {#o012-d60-ca01-s06}

::: {.exercise #o012-d60-ca01-ex-006 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R06"}
Klasifikasikan, hingga isomorfisma penutup, semua penutup terhubung berlembar
empat dari $S^1$. Berikan model eksplisit, subgrup $\pi_1(S^1)$ yang
bersesuaian, serta grup transformasi deknya. Jelaskan pula mengapa tidak ada
model terhubung lain yang tidak isomorfik dengannya.
:::

::: {.hint #o012-d60-ca01-hint-006 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R06"}
**Petunjuk.** Subgrup berindeks empat dari $\mathbb Z$ hanya satu. Karena
$\mathbb Z$ abelian, klasifikasi ruang penutup bertitik maupun tak bertitik
tidak menimbulkan kelas konjugasi tambahan.
:::

::: {.solution #o012-d60-ca01-sol-006 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R06"}
**Solusi.** Kita mempunyai $\pi_1(S^1)\cong\mathbb Z$. Subgrup berindeks empat
harus berbentuk $4\mathbb Z$, dan memang indeksnya empat. Teorema klasifikasi
ruang penutup memberi satu kelas penutup terhubung bertitik untuk subgrup ini.
Model eksplisitnya adalah

$$
p_4:S^1\longrightarrow S^1,
\qquad p_4(z)=z^4.
$$

Karena $\mathbb Z$ abelian, semua subgrupnya normal dan konjugasi tidak
mengubah $4\mathbb Z$. Maka klasifikasi tak bertitik juga hanya mempunyai satu
kelas isomorfisma terhubung berlembar empat. Grup transformasi dek adalah

$$
N_{\mathbb Z}(4\mathbb Z)/(4\mathbb Z)
=\mathbb Z/4\mathbb Z,
$$

yang pada model eksplisit bekerja melalui rotasi oleh akar-akar keempat dari
$1$.
:::

## Soal 7 — barisan eksak homotopi fibrasi Hopf {#o012-d60-ca01-s07}

::: {.exercise #o012-d60-ca01-ex-007 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R07"}
Untuk fibrasi Hopf

$$
S^1\longrightarrow S^3\longrightarrow S^2,
$$

gunakan barisan eksak panjang homotopi dan fakta standar
$\pi_1(S^3)=\pi_2(S^3)=0$ untuk membuktikan
$\pi_2(S^2)\cong\mathbb Z$. Buktikan juga bahwa
$\pi_k(S^3)\to\pi_k(S^2)$ adalah isomorfisma untuk setiap $k\ge3$.
:::

::: {.hint #o012-d60-ca01-hint-007 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R07"}
**Petunjuk.** Tulis bagian barisan yang mengapit $\pi_2(S^2)$. Untuk
$k\ge3$, gunakan $\pi_j(S^1)=0$ bagi semua $j\ge2$.
:::

::: {.solution #o012-d60-ca01-sol-007 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R07"}
**Solusi.** Bagian relevan barisan eksak panjang ialah

$$
\pi_2(S^3)\longrightarrow\pi_2(S^2)
\xrightarrow{\partial}\pi_1(S^1)
\longrightarrow\pi_1(S^3).
$$

Kedua grup di ujung bernilai nol. Eksakitas karena itu membuat
$\partial$ injektif sekaligus surjektif. Maka

$$
\pi_2(S^2)\cong\pi_1(S^1)\cong\mathbb Z.
$$

Untuk $k\ge3$, barisan yang sama memuat

$$
\pi_k(S^1)\longrightarrow\pi_k(S^3)
\longrightarrow\pi_k(S^2)
\longrightarrow\pi_{k-1}(S^1).
$$

Karena $k\ge3$, kedua grup yang melibatkan $S^1$ bernilai nol. Eksakitas
memaksa peta tengah $\pi_k(S^3)\to\pi_k(S^2)$ menjadi isomorfisma.
:::

## Soal 8 — kriteria pengangkatan peta torus {#o012-d60-ca01-s08}

::: {.exercise #o012-d60-ca01-ex-008 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R06" data-secondary-route-unit-ids="D60-R04,D60-R05"}
Untuk bilangan bulat $m,n$ dan $k\ge2$, definisikan

$$
f_{m,n}:T^2=S^1\times S^1\longrightarrow S^1,
\qquad f_{m,n}(z,w)=z^m w^n,
$$

dan $p_k:S^1\to S^1$, $p_k(u)=u^k$. Tentukan syarat perlu dan cukup agar
ada $g:T^2\to S^1$ dengan $p_k\circ g=f_{m,n}$. Jika syarat itu terpenuhi,
berikan semua pengangkatan tersebut.
:::

::: {.hint #o012-d60-ca01-hint-008 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R06" data-secondary-route-unit-ids="D60-R04,D60-R05"}
**Petunjuk.** Di bawah identifikasi
$\pi_1(T^2)\cong\mathbb Z^2$ dan $\pi_1(S^1)\cong\mathbb Z$, hitung
$(f_{m,n})_*(a,b)$. Citra $(p_k)_*$ adalah $k\mathbb Z$.
:::

::: {.solution #o012-d60-ca01-sol-008 data-origin="edition-original" data-assessment-id="D60-CA01" data-course-route-unit-id="D60-R06" data-secondary-route-unit-ids="D60-R04,D60-R05"}
**Solusi.** Pada grup fundamental,

$$
(f_{m,n})_*:\mathbb Z^2\longrightarrow\mathbb Z,
\qquad (a,b)\longmapsto ma+nb.
$$

Kriteria pengangkatan untuk $p_k$ menyatakan bahwa pengangkatan ada tepat bila

$$
(f_{m,n})_*(\mathbb Z^2)\subseteq(p_k)_*(\mathbb Z)=k\mathbb Z.
$$

Dengan memasukkan $(1,0)$ dan $(0,1)$, inklusi ini setara dengan
$k\mid m$ dan $k\mid n$. Jadi syarat tersebut perlu dan cukup.

Jika $m=km'$ dan $n=kn'$, satu pengangkatan ialah

$$
g_0(z,w)=z^{m'}w^{n'},
$$

karena $g_0(z,w)^k=f_{m,n}(z,w)$. Semua pengangkatan lain diperoleh dengan
mengalikan $g_0$ oleh transformasi dek konstan: untuk
$\zeta\in\mu_k=\{u\in S^1:u^k=1\}$,

$$
g_\zeta(z,w)=\zeta z^{m'}w^{n'}.
$$

Ruang $T^2$ terhubung, sehingga dua pengangkatan yang berimpit di satu titik
harus sama. Serat $p_k$ di setiap titik mempunyai tepat $k$ anggota. Dengan
demikian, $g_\zeta$ untuk $\zeta\in\mu_k$ adalah seluruh pengangkatan
$f_{m,n}$ melalui $p_k$, dan jumlahnya tepat $k$.
:::

## Peta cakupan asesmen {#o012-d60-ca01-coverage}

| Soal | Route utama | Kompetensi yang diperiksa |
|---:|:---:|---|
| 1 | D60-R01 | topologi hasil bagi, kekompakan, dan sifat Hausdorff |
| 2 | D60-R02 | retraksi deformasi kuat dan invariansi homotopi |
| 3 | D60-R03 | pengangkatan lintasan dan bilangan lilit |
| 4 | D60-R04 | monodromi, orbit, stabilisator, dan transformasi dek |
| 5 | D60-R05 | van Kampen dan presentasi grup |
| 6 | D60-R06 | klasifikasi ruang penutup |
| 7 | D60-R07 | fibrasi dan barisan eksak panjang homotopi |
| 8 | D60-R06; sintesis R04–R05 | kriteria pengangkatan melalui grup fundamental |

Asesmen selesai pada delapan soal, delapan petunjuk, dan delapan solusi penuh.
Tidak ada soal dari bank masalah Fomberg yang disalin atau diadaptasi di sini.
