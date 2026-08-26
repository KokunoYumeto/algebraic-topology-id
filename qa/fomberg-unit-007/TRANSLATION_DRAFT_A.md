---
title: "Draf Terjemahan A — Homologi Seluler"
lang: id-ID
source_component: "Fomberg Algebraic Topology, Section 1.13"
source_lines: "3518-3849"
edition_unit_id: "O012-FOM-007"
course_route_unit_id: "D60-R12"
draft_status: "draf sumber kontigu; belum merupakan pembaca kanonik"
model_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
---

# Homologi Seluler {#o012-fom-u007 data-origin="source-derived" data-source-lines="3518-3849" data-course-route-unit-id="D60-R12"}

::: {.remark #o012-fom-u007-rem-good-pair data-origin="source-derived" data-source-lines="3520-3523"}
**Catatan.** Bagi setiap subkompleks $A\subseteq X$, pasangan $(X,A)$
merupakan pasangan baik.
:::

::: {.lemma #o012-fom-u007-lem-cellular-skeleta-homology data-origin="source-derived" data-source-lines="3525-3540" data-repair-id="FOM-PR-13"}
**Lema.** Misalkan $X$ suatu kompleks CW dengan
$X=\bigcup_n X^{(n)}$.

1. Kita mempunyai

   $$
   H_k\!\left(X^{(n)},X^{(n-1)}\right)
   \cong
   \begin{cases}
   \displaystyle\bigoplus_\alpha \mathbb Z[\phi_\alpha], & n=k,\\
   0, & n\neq k.
   \end{cases}
   $$

   Di sini $\phi_\alpha$ adalah pemetaan karakteristik sel-$n$.

2. Kita mempunyai $H_k(X^{(n)})\cong\{0\}$ untuk $k>n$.

3. Kita mempunyai $H_k(X^{(n)})\cong H_k(X)$ untuk $n>k$.
:::

::: {.proof #o012-fom-u007-proof-cellular-skeleta-homology data-origin="source-derived" data-source-lines="3541-3594" data-proof-status="source-incomplete-for-general-part-3" data-repair-id="FOM-PR-13"}
**Bukti.**

1. Pernyataan pertama mengikuti dari fakta bahwa
   $(X^{(n)},X^{(n-1)})$ merupakan pasangan baik dan
   $X^{(n)}/X^{(n-1)}$ adalah baji sfera-$n$. Karena itu homologi relatif
   hanya tak nol pada derajat $n$, dengan satu pembangkit
   $[\phi_\alpha]$ bagi setiap sel-$n$.

2. Perhatikan subbarisan berikut dari barisan eksak panjang pasangan
   $(X^{(n)},X^{(n-1)})$:

   :::: {.figure #o012-fom-u007-fig-les-vanishing data-origin="source-semantic-reflow" data-source-lines="3571-3576" data-draft-asset-status="redraw-required"}
   $$
   H_{k+1}\!\left(X^{(n)},X^{(n-1)}\right)
   \longrightarrow H_k\!\left(X^{(n-1)}\right)
   \longrightarrow H_k\!\left(X^{(n)}\right)
   \longrightarrow H_k\!\left(X^{(n)},X^{(n-1)}\right).
   $$

   **Semantik diagram.** Keempat simpul terletak pada satu baris dan ketiga
   panah mengarah dari kiri ke kanan. Ini adalah bagian barisan eksak
   panjang yang mengapit peta akibat inklusi
   $H_k(X^{(n-1)})\to H_k(X^{(n)})$.
   ::::

   Karena $k>n$, baik $k$ maupun $k+1$ berbeda dari $n$. Oleh bagian (1),

   $$
   H_{k+1}\!\left(X^{(n)},X^{(n-1)}\right)
   \cong
   H_k\!\left(X^{(n)},X^{(n-1)}\right)
   \cong \{0\}.
   $$

   Eksakitas kemudian memberi
   $H_k(X^{(n-1)})\cong H_k(X^{(n)})$. Jadi, untuk $k>n$,

   $$
   H_k(X^{(n)})
   \cong H_k(X^{(n-1)})
   \cong\cdots\cong H_k(X^{(0)})
   =\{0\},
   $$

   yang menyelesaikan bagian kedua lema.

3. Untuk $X$ berdimensi hingga, yakni $X=X^{(m)}$ bagi suatu $m$, klaim
   mengikuti dari barisan eksak panjang yang sama seperti pada bagian (2).
   Teks sumber berhenti pada kasus berdimensi hingga ini.
:::

::: {.prospective-ledger-event #o012-fom-u007-corr-skeleta-proof data-origin="edition-original" data-source-lines="3525-3594" data-candidate-ids="FOM-U007-SRC-001,FOM-PR-13"}
**Calon peristiwa ledger — koreksi dan celah bukti.** Pada diagram baris
3572, sumber mencetak grup relatif kiri dengan tanda kurung yang salah.
Pada baris 3582, sumber menyimpulkan
$H_k(X^{(n-1)})\cong H_k(X^{(k)})$; indeks yang dibenarkan oleh barisan
eksak adalah $H_k(X^{(n-1)})\cong H_k(X^{(n)})$. Kedua koreksi bertipe itu
telah diterapkan di atas sebagai `FOM-U007-SRC-001`.

Bagian (3) sumber hanya menangani $X$ berdimensi hingga. Edisi kanonik
masih harus memasukkan pembuktian lengkap untuk kompleks CW sembarang,
termasuk langkah melalui subkompleks hingga atau limit langsung, sebagai
`FOM-PR-13`. Baris komentar TeX nonaktif 3545–3568 dan 3592 tidak
dipromosikan menjadi prosa sumber aktif dalam draf ini.
:::

::: {.definition #o012-fom-u007-def-cellular-chains data-origin="source-derived" data-source-lines="3596-3610" data-repair-id="FOM-PR-14"}
**Definisi (rantai seluler).** Kita mendefinisikan

$$
C_n^{\mathrm{CW}}(X)
:=H_n\!\left(X^{(n)},X^{(n-1)}\right).
$$

Dengan demikian,

$$
C_n^{\mathrm{CW}}(X)
\cong\bigoplus_\alpha\mathbb Z[\phi_\alpha],
$$

dengan $\phi_\alpha$ pemetaan karakteristik sel-$n$. Grup-grup rantai
$C_n^{\mathrm{CW}}(X)$ membentuk kompleks rantai seluler kita:

:::: {.figure #o012-fom-u007-fig-cellular-chain-complex data-origin="source-semantic-reflow" data-source-lines="3603-3609" data-draft-asset-status="redraw-required"}
$$
\cdots\longrightarrow
H_{n+1}\!\left(X^{(n+1)},X^{(n)}\right)
\xrightarrow{d_{n+1}}
H_n\!\left(X^{(n)},X^{(n-1)}\right)
\xrightarrow{d_n}
H_{n-1}\!\left(X^{(n-1)},X^{(n-2)}\right)
\longrightarrow\cdots.
$$

**Semantik diagram.** Setiap panah menurunkan derajat satu; tiga grup yang
ditampilkan berturut-turut ialah
$C_{n+1}^{\mathrm{CW}}(X)$, $C_n^{\mathrm{CW}}(X)$, dan
$C_{n-1}^{\mathrm{CW}}(X)$.
::::
:::

::: {.prospective-ledger-event #o012-fom-u007-corr-cellular-chain-argument data-origin="edition-original" data-source-lines="3596-3602" data-candidate-id="FOM-U007-SRC-002"}
**Calon peristiwa ledger — argumen grup rantai.** Baris 3602 sumber tiba-tiba
menulis $C_n^{\mathrm{CW}}(W)$, padahal hanya $X$ yang diperkenalkan.
Draf memakai $C_n^{\mathrm{CW}}(X)$ secara konsisten.
:::

::: {.definition #o012-fom-u007-def-cellular-boundary data-origin="source-derived" data-source-lines="3612-3640" data-repair-id="FOM-PR-14"}
**Definisi (pemetaan batas seluler).** Kita membangun pemetaan batas $d_n$
dengan menggabungkan barisan-barisan eksak panjang dari pasangan kerangka
yang berurutan. Bagian diagram sumber yang menentukan kedua diferensial
dapat ditulis secara semantik sebagai

:::: {.figure #o012-fom-u007-fig-cellular-boundary-diagram data-origin="source-semantic-reflow" data-source-lines="3618-3635" data-draft-asset-status="redraw-required"}
$$
\begin{aligned}
H_{n+1}\!\left(X^{(n+1)},X^{(n)}\right)
&\xrightarrow{\partial_{n+1}} H_n(X^{(n)})
\xrightarrow{q_n} H_n\!\left(X^{(n)},X^{(n-1)}\right),\\
H_n\!\left(X^{(n)},X^{(n-1)}\right)
&\xrightarrow{\partial_n} H_{n-1}(X^{(n-1)})
\xrightarrow{q_{n-1}}
H_{n-1}\!\left(X^{(n-1)},X^{(n-2)}\right).
\end{aligned}
$$

Dengan kata lain,

$$
d_{n+1}=q_n\circ\partial_{n+1},
\qquad
d_n=q_{n-1}\circ\partial_n.
$$

**Semantik diagram.** Diagram asli juga menampilkan panah inklusi
$0\to H_n(X^{(n)})\to H_n(X^{(n+1)})$ dan panah di sekitar
$H_{n-1}(X^{(n-1)})\to
H_{n-1}(X^{(n-1)},X^{(n-2)})$; dua lintasan komposit yang ditulis di atas
adalah panah diagonal $d_{n+1}$ dan $d_n$ pada kompleks seluler.
::::

Kita mendefinisikan

$$
\partial_n^{\mathrm{CW}}:=d_n=q_{n-1}\circ\partial_n.
$$

Memang,

$$
d_{n-1}\circ d_n
=q_{n-2}\circ\partial_{n-1}\circ q_{n-1}\circ\partial_n
=0,
$$

karena eksakitas memberi
$\partial_{n-1}\circ q_{n-1}=0$.
:::

::: {.remark #o012-fom-u007-rem-cellular-incidence-formula data-origin="source-derived" data-source-lines="3642-3664" data-repair-id="FOM-PR-15"}
**Catatan (rumus praktis untuk batas seluler).** Misalkan

$$
\varphi_\alpha\colon\partial D^n_\alpha\longrightarrow X^{(n-1)}
$$

adalah peta pelekatan suatu sel-$n$. Untuk setiap sel-$(n-1)$ yang diberi
indeks $\beta$, perhatikan komposit

$$
\begin{aligned}
S^{n-1}_\alpha
&\cong\partial D^n_\alpha
\xrightarrow{\ \varphi_\alpha\ }
X^{(n-1)}
\xrightarrow{\ q\ }
X^{(n-1)}/X^{(n-2)}\\
&\cong\bigvee_\delta S^{n-1}_\delta
\xrightarrow{\ p_\beta\ }
\left(\bigvee_\delta S^{n-1}_\delta\right)
\Big/
\left(\bigvee_{\delta\neq\beta}S^{n-1}_\delta\right)
\cong S^{n-1}_\beta.
\end{aligned}
$$

Definisikan

$$
\varphi_{\alpha\beta}\colon
S^{n-1}_\alpha\longrightarrow S^{n-1}_\beta
$$

sebagai komposit tersebut. Maka

$$
\partial^{\mathrm{CW}}\!\left([\phi_\alpha]\right)
=\sum_\beta
\deg(\varphi_{\alpha\beta})[\phi_\beta].
$$
:::

::: {.prospective-ledger-event #o012-fom-u007-corr-incidence-formula data-origin="edition-original" data-source-lines="3642-3664" data-candidate-ids="FOM-U007-SRC-003,FOM-PR-15"}
**Calon peristiwa ledger — tipe komposit dan bukti rumus insidensi.** Pada
baris 3653–3654 sumber mengulang $S^{n-1}_\beta$ di semua suku penyebut,
padahal suku yang dikuosienkan harus
$S^{n-1}_\delta$ untuk $\delta\neq\beta$. Baris 3657 juga mengetikkan
$\varphi_{\alpha\beta}$ sebagai $S^n_\alpha\to S^n_\beta$, sedangkan semua
peta pada komposit berdimensi $n-1$. Draf menerapkan kedua koreksi
`FOM-U007-SRC-003` secara eksplisit.

Sumber baru menyatakan rumus koefisien derajat di dalam sebuah catatan.
Edisi kanonik masih harus menambahkan teorema dan bukti lengkap yang
menghubungkan komposit ini dengan pemetaan penghubung dan pilihan orientasi
pembangkit sel sebagai `FOM-PR-15`.
:::

::: {.remark #o012-fom-u007-rem-boundary-notation data-origin="source-derived" data-source-lines="3666-3670"}
**Catatan (notasi batas).** Sebelumnya kita memakai $d_n$ dan
$\partial_n^{\mathrm{CW}}$ secara bergantian untuk menyatakan pemetaan batas
kompleks rantai seluler. Mulai sekarang, demi singkatnya, kita hanya memakai
$d_n$.
:::

::: {.remark #o012-fom-u007-rem-computation-summary data-origin="source-derived" data-source-lines="3672-3682" data-repair-id="FOM-PR-15"}
**Catatan (ringkasan perhitungan).** Untuk menghitung homologi seluler suatu
ruang, fakta yang perlu diingat adalah

$$
C_n^{\mathrm{CW}}(X)
=\bigoplus_\alpha\mathbb Z[\phi_\alpha],
$$

dengan $\phi_\alpha$ pemetaan karakteristik sel-$n$, dan pemetaan batas
diberikan oleh

$$
d_n\!\left([\phi_\alpha]\right)
=\sum_\beta
\deg(\varphi_{\alpha\beta})[\phi_\beta].
$$
:::

::: {.prospective-ledger-event #o012-fom-u007-omission-cellular-homology-theorem data-origin="edition-original" data-source-lines="3596-3640,3684-3849" data-candidate-id="FOM-PR-14"}
**Calon peristiwa ledger — teorema homologi seluler yang hilang.** Sumber
mendefinisikan kompleks rantai seluler lalu langsung mulai menghitung contoh,
tetapi belum menyatakan atau membuktikan isomorfisma alami

$$
H_n\!\left(C_*^{\mathrm{CW}}(X),d_*\right)
\cong H_n(X).
$$

Edisi kanonik harus memasukkan teorema beserta bukti filtrasi, barisan eksak,
dan naturalitasnya sebagai `FOM-PR-14` sebelum notasi homologi singular
$H_n(X)$ dipakai untuk hasil perhitungan seluler.
:::

::: {.example #o012-fom-u007-ex-sphere-homology data-origin="source-derived" data-source-lines="3684-3710"}
**Contoh (homologi sfera).** Misalkan $X=S^n$ dengan $n\geq2$. Seperti yang
kita lihat pada contoh struktur CW sfera dengan satu sel-$n$, kita dapat
membangun kompleks CW untuk $X$ hanya dengan satu sel-$0$ dan satu sel-$n$.
Kompleks rantai selulernya berbentuk

:::: {.figure #o012-fom-u007-fig-sphere-chain-complex data-origin="source-semantic-reflow" data-source-lines="3690-3699" data-draft-asset-status="redraw-required"}
$$
\cdots\longrightarrow 0
\xrightarrow{d_{n+1}}\mathbb Z
\xrightarrow{d_n}0
\xrightarrow{d_{n-1}}\cdots
\xrightarrow{d_2}0
\xrightarrow{d_1}\mathbb Z
\xrightarrow{d_0}0.
$$

**Semantik diagram.** Satu salinan $\mathbb Z$ berada pada derajat $n$ dan
satu lagi pada derajat $0$; semua grup pada derajat lain adalah nol.
::::

Kita bahkan tidak perlu menghitung pemetaan batas, sebab semuanya merupakan
homomorfisma nol. Langsung diperoleh

$$
H_k^{\mathrm{CW}}(S^n)
\cong
\begin{cases}
\mathbb Z, & k=0\ \text{atau}\ k=n,\\
0, & \text{selain itu}.
\end{cases}
$$
:::

::: {.example #o012-fom-u007-ex-complex-projective-homology data-origin="source-derived" data-source-lines="3712-3738"}
**Contoh (homologi ruang projektif kompleks).** Misalkan

$$
X=\mathbb{CP}^n
=\left(\mathbb C^{n+1}\setminus\{0\}\right)
\Big/
\left(x\sim\lambda x\right),
\qquad 0\neq\lambda\in\mathbb C.
$$

Dari contoh struktur CW ruang projektif kompleks, kita mengetahui bahwa
$X$ mempunyai satu sel-$i$ untuk setiap $i=2k$ dengan $0\leq k\leq n$.
Kompleks rantai selulernya ialah

:::: {.figure #o012-fom-u007-fig-complex-projective-chain-complex data-origin="source-semantic-reflow" data-source-lines="3719-3729" data-draft-asset-status="redraw-required"}
$$
\cdots\longrightarrow0
\xrightarrow{d_{2n+1}}\mathbb Z
\xrightarrow{d_{2n}}0
\xrightarrow{d_{2n-1}}\cdots
\xrightarrow{d_3}\mathbb Z
\xrightarrow{d_2}0
\xrightarrow{d_1}\mathbb Z
\xrightarrow{d_0}0.
$$

**Semantik diagram.** Ada satu salinan $\mathbb Z$ tepat pada setiap derajat
genap $0,2,\ldots,2n$ dan grup nol pada setiap derajat ganjil.
::::

Karena itu homologinya adalah

$$
H_t^{\mathrm{CW}}(\mathbb{CP}^n)
=
\begin{cases}
\mathbb Z, & t\leq2n\ \text{dan }t\text{ genap},\\
\{0\}, & \text{selain itu}.
\end{cases}
$$
:::

::: {.example #o012-fom-u007-ex-torus-homology data-origin="source-derived" data-source-label="exmp:cw-for-torus-homology" data-source-lines="3740-3845"}
**Contoh (homologi torus).** Perhatikan struktur CW torus-$2$ yang telah kita
lihat sebelumnya.

:::: {.figure #o012-fom-u007-fig-torus-polygon data-origin="source-semantic-reflow" data-source-lines="3743-3761" data-draft-asset-status="redraw-required"}
**Draf gambar ulang dan semantik diagram.** Sebuah persegi fundamental
berisi satu sel-$2$ terbuka yang diberi label $\Delta$. Keempat sudutnya
menjadi satu sel-$0$. Kedua sisi tegak diberi label $a$ dan arah yang sama
dari bawah ke atas; kedua sisi mendatar diberi label $b$ dan arah yang sama
dari kiri ke kanan. Dengan batas persegi dibaca berlawanan arah jarum jam,
kata pelekatannya adalah

$$
aba^{-1}b^{-1}.
$$

Arsiran hijau pada sumber hanya membedakan bagian dalam sel-$2$; makna
diagram tidak bergantung pada warna.
::::

Kompleks rantai selulernya berbentuk

:::: {.figure #o012-fom-u007-fig-torus-chain-complex data-origin="source-semantic-reflow" data-source-lines="3763-3770" data-draft-asset-status="redraw-required"}
$$
\cdots\xrightarrow{d_4}0
\xrightarrow{d_3}\mathbb Z\Delta
\xrightarrow{d_2}\mathbb Za\oplus\mathbb Zb
\xrightarrow{d_1}\mathbb Zv
\xrightarrow{d_0}0.
$$

**Semantik diagram.** Pembangkit $\Delta$, $a,b$, dan $v$ masing-masing
berada pada derajat $2$, $1$, dan $0$.
::::

Dalam dimensi $0$ dan $1$, perhitungan batas struktur CW ini bersesuaian
dengan struktur kompleks-$\Delta$ berdimensi rendah yang realisasinya sama.
Khususnya,

$$
d_1(a)=v-v=0,
\qquad
d_1(b)=v-v=0.
$$

Jadi satu-satunya homomorfisma dalam kompleks ini yang mungkin bukan nol
adalah $d_2$. Rumus batas memberi

$$
d_2(\Delta)
=\deg(\varphi_{\Delta a})a
+\deg(\varphi_{\Delta b})b.
$$

Untuk menghitung kedua derajat itu, pertama perhatikan komposit

:::: {.figure #o012-fom-u007-fig-torus-attaching-projection data-origin="source-semantic-reflow" data-source-lines="3783-3803" data-draft-asset-status="redraw-required"}
$$
\varphi_{\Delta a}\colon
\partial D^2_\Delta
\xrightarrow{\ \varphi_\Delta\ }
X^{(1)}\cong S_a^1\vee S_b^1
\xrightarrow{\ p_a\ }S_a^1.
$$

**Semantik diagram.** Peta pelekatan membaca kata
$aba^{-1}b^{-1}$ pada baji dua lingkaran. Proyeksi $p_a$ meruntuhkan
lingkaran $b$ ke titik baji, sehingga lintasan hasilnya membaca
$aa^{-1}$ pada $S_a^1$.
::::

Ingat bahwa $\varphi_{\Delta a}$ adalah pemetaan antar-sfera,
$\varphi_{\Delta a}\colon S^1\to S^1$. Pemetaan itu mengirim batas
$D^2_\Delta$ ke sebuah gelung yang homotopik dengan gelung konstan:

:::: {.figure #o012-fom-u007-fig-torus-nullhomotopy data-origin="source-semantic-reflow" data-source-lines="3808-3829" data-draft-asset-status="redraw-required"}
$$
aba^{-1}b^{-1}
\xmapsto{\ p_a\ }
aa^{-1}
\simeq *.
$$

**Semantik diagram.** Satu penelusuran $a$ pada suatu arah segera diikuti
penelusuran $a$ pada arah berlawanan. Homotopi menciutkan pasangan lintasan
tersebut ke titik basis.
::::

Ini memang cara notasi yang agak janggal untuk mengatakan bahwa, ketika
batas persegi torus—yang merepresentasikan $S^1$—ditelusuri sekali dan
diproyeksikan ke $S_a^1$, lintasan bergerak sekali pada satu arah lalu sekali
pada arah berlawanan. Seperti diketahui, gelung itu homotopik dengan gelung
konstan. Jadi $\varphi_{\Delta a}$ homotopik-nol dan

$$
\deg(\varphi_{\Delta a})=0.
$$

Dengan alasan yang sama,
$\varphi_{\Delta b}$ homotopik-nol dan
$\deg(\varphi_{\Delta b})=0$. Semua pemetaan batas karena itu merupakan
homomorfisma nol, sehingga

$$
H_k(T^2)
=
\begin{cases}
\mathbb Z, & k=0\ \text{atau}\ k=2,\\
\mathbb Z^2, & k=1,\\
\{0\}, & \text{selain itu}.
\end{cases}
$$
:::

::: {.prospective-ledger-event #o012-fom-u007-corr-torus-nullhomotopy data-origin="edition-original" data-source-lines="3830-3836" data-candidate-id="FOM-U007-SRC-004"}
**Calon peristiwa ledger — peta ruang bukan “peta nol”.** Sumber menulis
$\varphi_{\Delta a}\equiv0$ dan $\varphi_{\Delta b}\equiv0$. Untuk peta
ruang bertitik, simpulan yang bertipe benar ialah bahwa keduanya homotopik
dengan peta konstan; akibat aljabarnya adalah kedua derajat dan kedua
koefisien batas sama dengan nol. Draf menerapkan penajaman
`FOM-U007-SRC-004` ini tanpa mengubah hasil homologi.
:::

::: {.example #o012-fom-u007-ex-genus-two-homology data-origin="source-derived" data-source-label="exmp:homology-of-genus-two" data-source-lines="3847-3849" data-fragment-status="continues-at-source-line-3850"}
**Contoh (permukaan genus dua; berlanjut).** Misalkan
$\Sigma_2=T\mathbin{\#}T$ adalah permukaan berorientasi kompak bergenus dua.
Bagian contoh berikutnya dimulai pada baris sumber 3850 dan berada di dalam
draf lanjutan, bukan dalam rentang Draf A ini.
:::

## Catatan integrasi draf {.unnumbered #o012-fom-u007-draft-a-integration-notes}

- Draf ini menerjemahkan tepat isi pembaca aktif baris 3518–3849. Ia tidak
  mempromosikan komentar TeX nonaktif menjadi teks sumber.
- Semua sembilan kelompok diagram yang bermula dan berakhir dalam rentang ini
  dipertahankan sebagai formula serta uraian semantik. Aset SVG/PNG akhir
  belum dibuat dalam draf ini.
- Empat koreksi sumber yang diterapkan diberi ID audit
  `FOM-U007-SRC-001` sampai `FOM-U007-SRC-004`; tidak ada perubahan ledger
  yang dilakukan oleh draf ini.
- `FOM-PR-13`, `FOM-PR-14`, dan `FOM-PR-15` tetap merupakan kewajiban
  perbaikan terpisah. Draf ini tidak menyamarkan ketiganya sebagai bukti yang
  sudah lengkap.
- Pada rumus $\mathbb{CP}^n$, kurung hanya dibuat eksplisit untuk menghapus
  ambiguitas tipografis pada operasi hasil bagi; syarat sumber
  $0\neq\lambda\in\mathbb C$ dipertahankan.
