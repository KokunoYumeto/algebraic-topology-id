---
title: "Draf terjemahan Fomberg Unit 007 — fragmen B"
lang: id-ID
edition_unit_id: "O012-FOM-007"
course_route_unit_id: "D60-R12"
source_component: "Fomberg Algebraic Topology, Section 1.13"
source_lines: "3850-4185"
source_commit: "563194fae879178b9a6871b249513bfc27968975"
status: "draf terjemahan terbatas; belum menjadi pembaca kanonis"
model_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
---

# Homologi seluler: contoh-contoh komputasi, fragmen B

::: {.translation-note #o012-fom-u007-draft-b-boundary data-origin="edition-original" data-source-lines="3850-4185"}
**Batas draf.** Draf ini menerjemahkan tepat baris sumber 3850–4185.
Baris 3850 meneruskan Contoh `exmp:homology-of-genus-two`, yang dimulai pada
baris 3847; kalimat pembuka dan definisi
$\Sigma _2=T\mathbin{\#}T$ pada baris 3847–3849 harus datang dari fragmen A
ketika kedua draf digabungkan. Kode TikZ sumber dipertahankan di otoritas;
di sini setiap diagram diberi spesifikasi semantik lengkap untuk tahap gambar
ulang aksesibel.
:::

::: {.example #o012-fom-u007-ex-genus-two-homology data-origin="source-derived" data-source-label="exmp:homology-of-genus-two" data-source-lines="3847-3971" data-translation-slice="3850-3971"}
Saya menyarankan pembaca mencari gambar daring permukaan itu. Berikut ialah
diagramnya sebagai ruang hasil bagi.

:::: {.figure #o012-fom-u007-fig-genus-two-polygon data-origin="source-derived-diagram-specification" data-source-lines="3852-3906"}
**Spesifikasi gambar ulang aksesibel (poligon genus dua).** Sebuah segi delapan
berarsir mempunyai satu sel-$2$ di bagian dalam, berlabel $\Delta$. Delapan
sisinya, dibaca mengelilingi batas, berlabel

$$
a, b, a, c, d, c, d, b,
$$

dengan tanda panah pasangan sisi yang menunjukkan identifikasi. Untuk setiap
label $a,b,c,d$, kedua kemunculannya mempunyai orientasi yang saling berlawanan
relatif terhadap lintasan batas. Semua delapan simpul diidentifikasi menjadi
satu simpul $v$. Warna pada gambar sumber hanya membedakan pasangan sisi dan
tidak memuat data matematika tambahan.
::::

Semua simpul diidentifikasi satu sama lain dan simpul hasil identifikasi itu
dilambangkan dengan $v$. Kompleks rantai selulernya ialah

$$
\cdots \longrightarrow 0
\xrightarrow{d_3} \mathbb Z\Delta
\xrightarrow{d_2}
\mathbb Za\oplus\mathbb Zb\oplus\mathbb Zc\oplus\mathbb Zd
\xrightarrow{d_1}\mathbb Zv
\xrightarrow{d_0}0.
$$

Jelas bahwa semua homomorfisma dalam kompleks ini, kecuali mungkin $d_2$,
adalah homomorfisma nol. Seperti pada
Contoh `exmp:cw-for-torus-homology`, kita memperoleh

$$
\varphi_{\Delta a}\bigl(\partial D^2_\Delta\bigr)
=
\bigl(a\cdot a^{-1}\bigr)
\simeq \bullet.
$$

:::: {.figure #o012-fom-u007-fig-genus-two-nullhomotopy data-origin="source-derived-diagram-specification" data-source-lines="3920-3959"}
**Spesifikasi diagram semantik (proyeksi ke lingkaran $a$).** Mulailah dengan
lintasan batas segi delapan. Proyeksi ke faktor $S^1_a$ meruntuhkan semua sisi
selain kedua sisi berlabel $a$ ke titik pangkal. Dua sisi $a$ dilalui dengan
orientasi berlawanan, sehingga lintasan hasil proyeksi ialah $a a^{-1}$ dan
homotopik-nol. Diagram sumber menggambarkan kedua putaran berlawanan pada satu
lingkaran yang kemudian dikontraksikan ke sebuah titik. Konstruksi yang sama
berlaku untuk $b$, $c$, dan $d$.
::::

Jadi $\varphi_{\Delta a}$, $\varphi_{\Delta b}$,
$\varphi_{\Delta c}$, dan $\varphi_{\Delta d}$ semuanya homotopik-nol. Dengan
demikian semua koefisien derajatnya nol, sehingga $d_2=0$. Akibatnya,

$$
H_n(\Sigma _2)=
\begin{cases}
\mathbb Z, & n=0\ \text{atau}\ n=2,\\
\mathbb Z^4, & n=1,\\
\{0\}, & \text{selain itu}.
\end{cases}
$$
:::

::: {.source-audit #o012-fom-u007-audit-genus-two-nullhomotopy data-origin="edition-original" data-source-lines="3960-3962" data-source-correction-id="FOM-U007-SRC-004"}
**Koreksi jenis objek.** Sumber menyebut keempat peta ruang di atas sebagai
“peta nol”. Dalam kategori ruang bertitik, kesimpulan yang dibuktikan oleh
diagram ialah bahwa peta-peta itu **homotopik-nol**. Yang benar-benar nol
secara aljabar ialah derajat setiap peta dan, karenanya, koefisien-koefisien
pemetaan batas seluler $d_2$.
:::

::: {.remark #o012-fom-u007-rem-genus-g-homology data-origin="source-derived" data-source-lines="3973-3988"}
**Catatan.** Argumen pada Contoh `exmp:homology-of-genus-two` sebenarnya tidak
bergantung pada asumsi bahwa genus permukaannya sama dengan $2$. Jadi, untuk
permukaan terorientasi kompak bergenus $g$,

$$
\Sigma_g=\mathbin{\#}^{g}T^2,
$$

kita memperoleh

$$
H_n(\Sigma_g)=
\begin{cases}
\mathbb Z, & n=0\ \text{atau}\ n=2,\\
\mathbb Z^{2g}, & n=1,\\
\{0\}, & \text{selain itu}.
\end{cases}
$$
:::

::: {.example #o012-fom-u007-ex-klein-bottle-homology data-origin="source-derived" data-source-lines="3990-4097"}
**Contoh (homologi botol Klein).** Tinjau botol Klein $K$ dengan struktur CW
berikut.

:::: {.figure #o012-fom-u007-fig-klein-bottle-polygon data-origin="source-derived-diagram-specification" data-source-lines="3992-4010"}
**Spesifikasi gambar ulang aksesibel (poligon botol Klein).** Sebuah persegi
berarsir mempunyai satu sel-$2$ di bagian dalam, berlabel $\Delta$. Sisi bawah
dan kiri berlabel $a$; sisi atas dan kanan berlabel $b$. Tanda panah sumber
menunjukkan bahwa, ketika batas sel-$2$ ditelusuri menurut orientasinya,
masing-masing label $a$ dan $b$ muncul dua kali dengan tanda yang sama. Keempat
simpul diidentifikasi menjadi satu simpul $v$. Dengan pemilihan titik awal dan
arah penelusuran yang sesuai, kata pelekatan dapat ditulis sebagai
$b^2a^2$; perubahan titik awal hanya mengubahnya melalui konjugasi siklik.
::::

Ini bukan representasi baku botol Klein, tetapi kita dapat memperoleh
representasi yang lebih lazim dengan memotong sepanjang antidiagonal lalu
merekatkan kembali sepanjang sisi $a$. Dari representasi di atas kita
memperoleh kompleks rantai seluler

$$
\cdots\longrightarrow 0
\xrightarrow{d_3}\mathbb Z\Delta
\xrightarrow{d_2}\mathbb Za\oplus\mathbb Zb
\xrightarrow{d_1}\mathbb Zv
\xrightarrow{d_0}0.
$$

Seperti pada semua contoh sebelumnya, homomorfisma yang perlu dihitung ialah
$d_2$. Kali ini hasilnya sedikit berbeda. Kita mempunyai

$$
\varphi_{\Delta a}\colon
\partial D^2_\Delta
\xrightarrow{\ \varphi_\Delta\ }
X^{(1)}\cong S^1_a\vee S^1_b
\xrightarrow{\ p_a\ }S^1_a,
$$

:::: {.figure #o012-fom-u007-fig-klein-bottle-attaching-projection data-origin="source-derived-diagram-specification" data-source-lines="4026-4046"}
**Spesifikasi diagram semantik (proyeksi pelekatan ke faktor $a$).** Lingkaran
$\partial D^2_\Delta$ dipetakan oleh $\varphi_\Delta$ ke baji dua lingkaran,
$S^1_a\vee S^1_b$. Proyeksi $p_a$ mempertahankan lingkaran $a$ dan meruntuhkan
seluruh lingkaran $b$ ke titik pangkal. Label, titik pangkal, dan arah lintasan
dipertahankan; warna sumber hanya membedakan kedua faktor.
::::

dan pada lintasan batas,

$$
\varphi_{\Delta a}\bigl(\partial D^2_\Delta\bigr)
=a^2\simeq\bigl(z\longmapsto z^2\bigr).
$$

:::: {.figure #o012-fom-u007-fig-klein-bottle-degree-two data-origin="source-derived-diagram-specification" data-source-lines="4048-4069"}
**Spesifikasi diagram semantik (derajat dua pada faktor $a$).** Sesudah faktor
$b$ diruntuhkan, dua ruas batas berlabel $a$ memiliki orientasi yang sama.
Akibatnya, lingkaran batas mengelilingi $S^1_a$ dua kali. Diagram sumber
menampilkan dua putaran searah dan membandingkan peta itu dengan pemetaan
pangkat $z\mapsto z^2$; derajatnya adalah $2$.
::::

Jadi $\varphi_{\Delta a}$ membawa satu putaran mengelilingi
$\partial D^2_\Delta\cong S^1$ menjadi dua putaran mengelilingi $S^1_a$,
seperti pemetaan $z\mapsto z^2$. Karena itu

$$
\deg(\varphi_{\Delta a})=2.
$$

Dengan perhitungan yang sama pada proyeksi $p_b$,

$$
\deg(\varphi_{\Delta b})=2.
$$

Maka

$$
d_2(\Delta)=2a+2b=2(a+b).
$$

Satu-satunya kelompok homologi taktrivial yang masih perlu dihitung ialah

$$
\begin{aligned}
H_1(K)
&=\frac{\ker d_1}{\operatorname{im}d_2}
=\frac{\mathbb Za\oplus\mathbb Zb}{\mathbb Z\bigl(2(a+b)\bigr)}\\
&=\langle a,a+b\mid 2(a+b)\rangle\\
&=\langle a\rangle\oplus\langle a+b\mid2(a+b)\rangle
\cong\mathbb Z\oplus\mathbb Z/2\mathbb Z.
\end{aligned}
$$

Dengan demikian,

$$
H_n(K)=
\begin{cases}
\mathbb Z, & n=0,\\
\mathbb Z\oplus\mathbb Z/2\mathbb Z, & n=1,\\
\{0\}, & \text{selain itu}.
\end{cases}
$$
:::

::: {.source-audit #o012-fom-u007-audit-klein-incidence data-origin="edition-original" data-source-lines="4070-4086" data-source-correction-ids="FOM-U007-SRC-005,FOM-U007-SRC-006"}
**Koreksi koefisien dan notasi.** Baris 4074 sumber mengulang
$\deg(\varphi_{\Delta a})=2$ ketika koefisien kedua seharusnya merujuk kepada
$\varphi_{\Delta b}$. Orientasi pada gambar memberi kata batas dengan jumlah
eksponen $2$ untuk $a$ dan $2$ untuk $b$, sehingga
$d_2(\Delta)=2(a+b)$ memang konsisten dengan gambar. Baris 4086 juga
dinormalkan dari $Z$ menjadi $\mathbb Z$.
:::

::: {.source-audit #o012-fom-u007-audit-klein-boundary-wording data-origin="edition-original" data-source-lines="4070-4072" data-prospective-ledger-id="FOM-U007-PROSPECTIVE-B-001"}
**Usulan kejadian ledger (batas ruang versus batas sel).** Sumber menyebut
domain peta sebagai “the boundary of the Klein bottle”. Botol Klein adalah
permukaan tertutup dan tidak mempunyai batas. Domain yang dimaksud ialah batas
sel-$2$ fundamental, $\partial D^2_\Delta$. Terjemahan memakai tipe yang benar
dan mencatat perubahannya di sini agar koreksi tidak tersembunyi.
:::

::: {.example #o012-fom-u007-ex-real-projective-space-homology data-origin="source-derived" data-source-label="exmp:homology-of-rpn" data-source-lines="4099-4184"}
**Contoh (homologi ruang projektif real).** Ambil
$X=\mathbb{RP}^{n}$. Kita mengetahui bahwa $X$ mempunyai struktur CW dengan
satu sel-$i$ pada setiap dimensi $0\leq i\leq n$. Karena itu kompleks rantai
selulernya berbentuk

$$
\cdots\xrightarrow{d_{n+2}}0
\xrightarrow{d_{n+1}}\mathbb Z
\xrightarrow{d_n}\cdots
\xrightarrow{d_2}\mathbb Z
\xrightarrow{d_1}\mathbb Z
\xrightarrow{d_0}0.
$$

Pemetaan-pemetaan batasnya sekarang tidak langsung terlihat. Ingatlah bahwa,
untuk sel-$n$ $\Delta_\alpha$ dan sel-$(n-1)$ $\Delta_\beta$, komponen peta
pelekatan yang menentukan koefisien insidensi ialah

$$
\begin{aligned}
S^{n-1}_\alpha
&\cong\partial D^n_\alpha
\xrightarrow{\ \varphi_\alpha\ }X^{(n-1)}
\xrightarrow{\ q\ }
X^{(n-1)}/X^{(n-2)}\\
&\cong\bigvee_\delta S^{n-1}_\delta
\xrightarrow{\ p_\beta\ }
\left(\bigvee_\delta S^{n-1}_\delta\right)
\Big/
\left(\bigvee_{\delta\ne\beta}S^{n-1}_\delta\right)
\cong S^{n-1}_\beta.
\end{aligned}
$$

Dalam kasus kita, $X^{(n)}=\mathbb{RP}^{n}$ dan hanya ada satu sel pada setiap
dimensi. Jadi komposit tersebut menjadi

$$
\varphi_{\Delta_n\Delta_{n-1}}\colon
S^{n-1}\cong\partial D^n
\xrightarrow{\ \varphi_{\Delta_n}\ }
\mathbb{RP}^{n-1}
\xrightarrow{\ q\ }
\mathbb{RP}^{n-1}/\mathbb{RP}^{n-2}
\cong S^{n-1}.
$$

Maka

$$
\begin{aligned}
d_n\bigl([\phi_{\Delta_n}]\bigr)
&=\sum_\beta
\deg\bigl(\varphi_{\Delta_n\Delta_{n-1}}\bigr)
\,[\phi_{\Delta_{n-1}}]\\
&=\deg\bigl(\varphi_{\Delta_n\Delta_{n-1}}\bigr)
\,[\phi_{\Delta_{n-1}}],
\end{aligned}
$$

karena $\Delta_n$ melambangkan satu-satunya sel-$n$ dalam kompleks itu.

Peta pelekatan

$$
\varphi_{\Delta_n}\colon
S^{n-1}\longrightarrow
S^{n-1}/(x\sim -x)\cong\mathbb{RP}^{n-1}
$$

ialah pemetaan penutup ganda kanonis atas $\mathbb{RP}^{n-1}$. Sekarang kita
gunakan Proposisi `prop:local-degree-for-global-degree`. Pilih
$y\in S^{n-1}$ yang tidak berada pada khatulistiwa. Maka

$$
\varphi_{\Delta_n\Delta_{n-1}}^{-1}(y)=\{x,-x\}
$$

untuk suatu $x\in S^{n-1}$. Oleh karena itu,

$$
\deg\bigl(\varphi_{\Delta_n\Delta_{n-1}}\bigr)
=
\deg_x\bigl(\varphi_{\Delta_n\Delta_{n-1}}\bigr)
+
\deg_{-x}\bigl(\varphi_{\Delta_n\Delta_{n-1}}\bigr).
$$

Dari sifat multiplikatif derajat, kontribusi lokal pada $-x$ ialah kontribusi
lokal pada $x$ dikalikan derajat peta antipodal $\alpha$. Dengan orientasi
lokal yang kompatibel,

$$
\deg_{-x}\bigl(\varphi_{\Delta_n\Delta_{n-1}}\bigr)
=
\deg_x\bigl(\varphi_{\Delta_n\Delta_{n-1}}\bigr)
\deg(\alpha)
=(-1)^n,
$$

sedangkan kontribusi di $x$ sama dengan $1$. Jadi

$$
\deg\bigl(\varphi_{\Delta_n\Delta_{n-1}}\bigr)
=1+(-1)^n
=
\begin{cases}
2, & n\ \text{genap},\\
0, & n\ \text{ganjil}.
\end{cases}
$$

Dengan kata lain, $d_n$ adalah perkalian dengan $2$ ketika $n$ genap dan
homomorfisma nol ketika $n$ ganjil. Akibatnya, jika $n$ ganjil,

$$
H_k(\mathbb{RP}^{n})=
\begin{cases}
\mathbb Z, & k=0\ \text{atau}\ k=n,\\
\mathbb Z/2\mathbb Z,
  & 0<k<n\ \text{dan}\ k\ \text{ganjil},\\
\{0\}, & \text{selain itu},
\end{cases}
$$

sedangkan jika $n$ genap,

$$
H_k(\mathbb{RP}^{n})=
\begin{cases}
\mathbb Z, & k=0,\\
\mathbb Z/2\mathbb Z,
  & 0<k<n\ \text{dan}\ k\ \text{ganjil},\\
\{0\}, & \text{selain itu}.
\end{cases}
$$
:::

::: {.source-audit #o012-fom-u007-audit-projective-incidence-quotient data-origin="edition-original" data-source-lines="4117-4124" data-source-correction-id="FOM-U007-SRC-003"}
**Koreksi indeks pada proyeksi ke satu faktor baji.** Penyebut hasil bagi
sumber mengulang $S^{n-1}_\beta$ untuk setiap $\delta\ne\beta$. Penyebut yang
menyisakan faktor ke-$\beta$ haruslah

$$
\bigvee_{\delta\ne\beta}S^{n-1}_\delta.
$$

Koreksi ini adalah kemunculan ulang pola salah indeks yang sudah dicatat bagi
rumus umum pada baris 3647–3658.
:::

::: {.source-audit #o012-fom-u007-audit-projective-dimensions data-origin="edition-original" data-source-lines="4143-4165" data-source-correction-ids="FOM-U007-SRC-007,FOM-U007-SRC-008"}
**Koreksi dimensi dan tipe aljabar.** Baris 4149 menempatkan
$x$ di $S^1$, padahal peta aktif berdomain $S^{n-1}$; edisi memakai
$x\in S^{n-1}$. Setelah derajat peta sfera dihitung, sumber menulis
$\deg(d_n)$, tetapi $d_n$ adalah homomorfisma grup rantai dan tidak mempunyai
derajat topologis. Edisi menyatakan bahwa peta sfera mempunyai derajat
$1+(-1)^n$, sehingga $d_n$ adalah perkalian dengan $2$ untuk $n$ genap dan
homomorfisma nol untuk $n$ ganjil.
:::

::: {.translation-note #o012-fom-u007-draft-b-ledger-candidates data-origin="edition-original" data-source-lines="3850-4185"}
**Kandidat terminologi untuk ledger (belum diadmisikan oleh draf ini).** Draf
memakai pasangan berikut secara konsisten: *cellular chain complex* →
**kompleks rantai seluler**; *compact orientable surface* → **permukaan
terorientasi kompak**; *double cover* → **penutup ganda**; *incidence
coefficient* → **koefisien insidensi**; *zero homomorphism* → **homomorfisma
nol**. Pasangan tersebut harus dibandingkan dengan fragmen A dan baru boleh
ditambahkan ke `00_control/TERMINOLOGY.csv` oleh pemilik integrasi.
:::

::: {.translation-note #o012-fom-u007-draft-b-ambiguities data-origin="edition-original" data-source-lines="3992-4077,4146-4163"}
**Ambiguitas substantif yang harus diperiksa saat integrasi.** Pertama, gambar
botol Klein sumber memang memberikan jumlah eksponen $2$ bagi kedua pembangkit
dalam basis yang digambar, jadi $d_2(\Delta)=2(a+b)$; ini berbeda dari basis
representasi baku yang biasanya memberi satu koefisien nol dan satu koefisien
$\pm2$, tetapi kedua presentasi menghasilkan
$H_1(K)\cong\mathbb Z\oplus\mathbb Z/2\mathbb Z$. Kedua, baris 4160–4163
menjelaskan cabang lokal melalui “homotopy equivalent to the identity”. Draf
menyatakan isi yang diperlukan dalam bahasa derajat lokal dengan orientasi
kompatibel; pemeriksa independen harus memastikan bahwa konvensi orientasi
yang dipakai oleh perbaikan `FOM-PR-15` menghasilkan tanda yang sama.
:::
