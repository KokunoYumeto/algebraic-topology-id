## Mayer–Vietoris {#o012-fom-u004-s08 data-source-lines="2441-2610"}

::: {.theorem #o012-fom-u004-thm-mayer-vietoris data-source-lines="2442-2499"}
**Teorema (Mayer–Vietoris).** Misalkan $A,B\subseteq X$ dan

$$
X=\mathring A\cup\mathring B.
$$

:::: {.figure #o012-fom-u004-fig-mayer-vietoris-cover data-source-lines="2445-2483" data-origin="edition-original-redraw"}
![Gambar ulang aksesibel penutup Mayer–Vietoris: A dan B menutupi X; rantai z dipotong menjadi tau di A dan eta di B dengan batas berlawanan pada irisan.](../assets/unit-004/mayer-vietoris-cover.png){.semantic-redraw width=88%}

**Diagram semantik (penutup dan pemotongan rantai).** Daerah $A$ dan $B$
menutupi $X$ dengan daerah tumpang tindih $A\cap B$. Sebuah rantai kecil pada
$X$ dapat dipisahkan menjadi rantai $\tau$ di $A$ dan rantai $\eta$ di $B$.
Jika $\sigma$ berada di $A\cap B$, dua salinannya masuk ke jumlah langsung
dengan tanda berlawanan, yaitu $(\sigma,-\sigma)$. Untuk siklus
$\sigma=\tau+\eta$ di $X$, persamaan $\partial\tau=-\partial\eta$
menempatkan batas bersama itu di $A\cap B$.
::::

Terdapat barisan eksak panjang

:::: {.figure #o012-fom-u004-fig-mayer-vietoris-sequence data-source-lines="2484-2498" data-origin="edition-original-redraw"}
$$
\cdots\longrightarrow H_n(A\cap B)
\xrightarrow{(i_*,-j_*)}H_n(A)\oplus H_n(B)
\xrightarrow{k_*+\ell_*}H_n(X)
\xrightarrow{\partial}H_{n-1}(A\cap B)
\longrightarrow\cdots,
$$

dengan $i\colon A\cap B\hookrightarrow A$,
$j\colon A\cap B\hookrightarrow B$, serta $k$ dan $\ell$ inklusi ke $X$.
Pada tingkat wakil,

$$
[\sigma]\longmapsto([\sigma],-[\sigma]),
\qquad
([\tau],[\eta])\longmapsto[\tau]+[\eta].
$$

Jika $[z]\in H_n(X)$ diwakili oleh pemisahan $z=\tau+\eta$, maka pemetaan
penghubung diberikan oleh

$$
\partial[z]=[\partial\tau]=-[\partial\eta]
\in H_{n-1}(A\cap B).
$$

**Diagram semantik.** Panah pertama memasukkan satu rantai perpotongan ke
dua bagian dengan tanda berlawanan; panah kedua menjumlahkan kedua bagian di
$X$; panah penghubung mengambil batas salah satu bagian, yang kini terletak
di perpotongan.
::::
:::

::: {.source-audit #o012-fom-u004-audit-mayer-vietoris-chain-labels data-origin="edition-original" data-source-lines="2447-2497"}
**Koreksi konsistensi label rantai.** Gambar sumber menempatkan $\eta$ pada
daerah biru $A$ dan $\tau$ pada daerah jingga $B$, tetapi diagram aljabarnya
menulis $([\tau],[\eta])\in H_n(A)\oplus H_n(B)$ dan
$\partial[z]=[\partial\tau]$. Edisi mempertahankan konvensi aljabar tersebut:
$\tau$ berada di $A$, $\eta$ berada di $B$, dan gambar ulang memakai label
yang sama. Pertukaran nama tidak mengubah kelas $[\tau]+[\eta]$.
:::

::: {.proof #o012-fom-u004-proof-mayer-vietoris data-source-lines="2500-2516"}
**Bukti.** Ambil penutup $\mathcal U=\{A,B\}$. Untuk setiap $n$, barisan

$$
0\longrightarrow C_n(A\cap B)
\xrightarrow{f}C_n(A)\oplus C_n(B)
\xrightarrow{g}C_n^{\mathcal U}(X)
\longrightarrow0,
$$

dengan

$$
f(\sigma)=(\sigma,-\sigma),
\qquad
g(\tau,\eta)=\tau+\eta,
$$

merupakan barisan eksak pendek kompleks rantai. Memang, $f$ injektif,
$g$ surjektif menurut definisi rantai kecil yang subordinat terhadap
$\mathcal U$, dan

$$
\ker g=\{(c,-c):c\in C_n(A\cap B)\}=\operatorname{im}f.
$$

Teorema rantai kecil dari bagian sebelumnya memberi
$H_n^{\mathcal U}(X)\cong H_n(X)$. Barisan eksak panjang dalam homologi yang
berasal dari barisan eksak pendek di atas karena itu tepat merupakan barisan
Mayer–Vietoris pada pernyataan. $\square$
:::

::: {.remark #o012-fom-u004-rem-reduced-mayer-vietoris data-source-lines="2517-2519"}
**Catatan.** Konstruksi yang sama menghasilkan barisan Mayer–Vietoris eksak
panjang untuk homologi tereduksi. Di sini kita memakai kompleks rantai
teraugmentasi; dengan konvensi itu suku derajat rendah tetap bermakna,
termasuk $\widetilde H_{-1}(\varnothing)\cong\mathbb Z$. Semua penerapan
berikut mempunyai $A\cap B\ne\varnothing$.
:::

::: {.example #o012-fom-u004-ex-sphere-mayer-vietoris data-source-lines="2521-2549"}
**Contoh (homologi sfera).** Kita ingin menghitung
$\widetilde H_k(S^n)$ untuk $n\geq1$. Tuliskan

$$
S^n=\mathring A\cup\mathring B,
\qquad
A=S^n\setminus\{N\},
\qquad
B=S^n\setminus\{S\},
$$

dengan $N$ dan $S$ berturut-turut kutub utara dan selatan. Kita mempunyai

$$
A\cong B\cong\mathbb R^n,
\qquad
A\cap B\simeq_{\mathrm{dr}}S^{n-1},
$$

karena perpotongan tersebut meretraksi deformasi ke ekuator (khatulistiwa
sfera). Bagian
barisan Mayer–Vietoris tereduksi adalah

:::: {.figure #o012-fom-u004-fig-sphere-mayer-vietoris data-source-lines="2532-2538" data-origin="edition-original-redraw"}
$$
\widetilde H_k(A)\oplus\widetilde H_k(B)
\longrightarrow\widetilde H_k(S^n)
\longrightarrow\widetilde H_{k-1}(A\cap B)
\longrightarrow
\widetilde H_{k-1}(A)\oplus\widetilde H_{k-1}(B).
$$

**Diagram semantik.** Empat suku berturutan menghubungkan homologi kedua
bagian, homologi sfera, homologi perpotongan satu derajat lebih rendah, lalu
homologi kedua bagian pada derajat yang lebih rendah itu.
::::

Karena $A$ dan $B$ kontraktibel, barisan ini menjadi

:::: {.figure #o012-fom-u004-fig-sphere-mayer-vietoris-zero data-source-lines="2539-2545" data-origin="edition-original-redraw"}
$$
0\oplus0
\longrightarrow\widetilde H_k(S^n)
\longrightarrow\widetilde H_{k-1}(S^{n-1})
\longrightarrow0\oplus0.
$$

**Diagram semantik.** Pemetaan di tengah berada di antara grup nol pada
kedua sisi dan karena itu merupakan isomorfisma.
::::

Eksakitas memberi

$$
\widetilde H_k(S^n)\cong\widetilde H_{k-1}(S^{n-1}).
$$

Dengan kasus dasar $S^0$, rumus ini menghitung homologi sfera secara induktif,
sebagaimana pada [akibat homologi sfera
sebelumnya](#o012-fom-u003-cor-sphere-homology).
:::

::: {.source-audit #o012-fom-u004-audit-sphere-tilde data-origin="edition-original" data-source-lines="2546-2548" data-adverse-candidate-id="FOM-U004B-ADV-001"}
**Kandidat koreksi sumber (tilde yang hilang).** Seluruh contoh memakai
homologi tereduksi, tetapi baris 2546 mencetak
$H_k(S^n)\cong H_{k-1}(S^{n-1})$. Rumus itu tidak benar pada derajat nol
dengan homologi biasa. Prosa Indonesia memakai bentuk yang konsisten,
$\widetilde H_k(S^n)\cong\widetilde H_{k-1}(S^{n-1})$, sambil mempertahankan
lokus sumber ini sebagai kandidat koreksi sumber.
:::

::: {.example #o012-fom-u004-ex-rp2-mayer-vietoris data-source-lines="2551-2609"}
**Contoh ($\mathbb{RP}^2$).** Pilih $A\cong\mathbb D^2$ dan
$B\cong M$, dengan $M$ pita Möbius, sehingga keduanya menutupi
$\mathbb{RP}^2$ dan $A\cap B$ merupakan anulus (daerah berbentuk gelang) yang meretraksi deformasi ke
$S^1$.

:::: {.figure #o012-fom-u004-fig-rp2-cover data-source-lines="2555-2573" data-origin="edition-original-redraw"}
![Gambar ulang aksesibel penutup bidang proyektif real: cakram A, lingkungan batas B yang menjadi pita Möbius, dan anulus irisan A dengan B.](../assets/unit-004/rp2-mayer-vietoris-cover.png){.semantic-redraw width=70%}

**Diagram semantik (penutup $\mathbb{RP}^2$).** Bagian tengah berbentuk
cakram menyatakan $A$. Daerah berbentuk anulus di sekelilingnya menyatakan
$B$; dua arah pada batas luar diidentifikasi berlawanan sehingga daerah itu
menjadi pita Möbius. Daerah tumpang tindih adalah anulus di sekitar batas
cakram dan mempunyai tipe homotopi $S^1$.
::::

Barisan Mayer–Vietoris tereduksi memuat bagian

:::: {.figure #o012-fom-u004-fig-rp2-long-sequence data-source-lines="2574-2580" data-origin="edition-original-redraw"}
$$
\begin{aligned}
\cdots&\longrightarrow
\widetilde H_2(A)\oplus\widetilde H_2(B)
\longrightarrow\widetilde H_2(\mathbb{RP}^2)
\longrightarrow\widetilde H_1(A\cap B)\\
&\longrightarrow
\widetilde H_1(A)\oplus\widetilde H_1(B)
\longrightarrow\widetilde H_1(\mathbb{RP}^2)
\longrightarrow\widetilde H_0(A\cap B)
\longrightarrow\cdots.
\end{aligned}
$$

**Diagram semantik.** Barisan turun dari derajat dua ke derajat satu melalui
pemetaan penghubung; suku perpotongan berada di antara homologi ruang total
dan jumlah langsung homologi kedua bagian.
::::

Ruang $A$ kontraktibel, sedangkan $B$ dan $A\cap B$ masing-masing meretraksi
deformasi ke $S^1$. Karena ketiga ruang itu terhubung lintasan, potongan yang
relevan menyederhana menjadi

:::: {.figure #o012-fom-u004-fig-rp2-short-sequence data-source-lines="2581-2598" data-origin="edition-original-redraw"}
$$
0\longrightarrow\widetilde H_2(\mathbb{RP}^2)
\longrightarrow\mathbb Z
\xrightarrow{\times2}\mathbb Z
\longrightarrow\widetilde H_1(\mathbb{RP}^2)
\longrightarrow0.
$$

**Diagram semantik.** Dua salinan $\mathbb Z$ berasal dari lingkaran
perpotongan dan inti pita Möbius. Pemetaan di antara keduanya mengalikan
generator dengan dua.
::::

Pemetaan $\mathbb Z\to\mathbb Z$ mempunyai derajat $\pm2$: lingkaran batas
pita Möbius mengelilingi lingkaran intinya dua kali. Setelah generator kedua
salinan $\mathbb Z$ dipilih secara serasi, pemetaan yang ditampilkan adalah
perkalian $+2$. Karena pemetaan ini injektif
dan kokernelnya $\mathbb Z/2\mathbb Z$, eksakitas memberi

$$
\widetilde H_2(\mathbb{RP}^2)=0,
\qquad
\widetilde H_1(\mathbb{RP}^2)=\mathbb Z/2\mathbb Z.
$$

Jadi barisan teridentifikasi sepenuhnya sebagai

:::: {.figure #o012-fom-u004-fig-rp2-completed-sequence data-source-lines="2601-2608" data-origin="edition-original-redraw"}
$$
0\longrightarrow0\longrightarrow\mathbb Z
\xrightarrow{\times2}\mathbb Z
\longrightarrow\mathbb Z/2\mathbb Z
\longrightarrow0.
$$

**Diagram semantik.** Kernel perkalian dua adalah nol dan kokernelnya adalah
$\mathbb Z/2\mathbb Z$.
::::
:::

::: {.source-audit #o012-fom-u004-audit-rp2-degree data-origin="edition-original" data-source-lines="2594-2600"}
**Pelengkapan penjelasan sumber.** Sumber menyatakan bahwa generator kiri
dipetakan ke dua kali generator kanan, lalu meninggalkan komentar TeX
“give intuition to $\mathbb Z/2\mathbb Z$” dan “explain??”. Edisi ini
menjelaskan lokus tersebut melalui pemetaan batas pita Möbius ke lingkaran
inti yang berderajat dua; komentar kerja sumber tidak diperlakukan sebagai
prosa pembaca.
:::

## Kealamian {#o012-fom-u004-s09 data-source-lines="2611-2683"}

::: {.remark #o012-fom-u004-rem-naturality-etymology data-source-lines="2612-2615"}
**Catatan.** Asal istilah “kealamian” akan menjadi lebih jelas setelah
interpretasinya secara kategoris dipahami.
:::

::: {.definition #o012-fom-u004-def-naturality-pair data-source-lines="2617-2640"}
**Definisi (kealamian).** Barisan eksak panjang suatu pasangan disebut
**alami** jika untuk setiap peta pasangan
$f\colon(X,A)\to(Y,B)$, diagram berikut komutatif:

:::: {.figure #o012-fom-u004-fig-naturality-pair data-source-lines="2620-2639" data-origin="edition-original-redraw"}
$$
\begin{array}{ccccccccc}
\cdots&\longrightarrow&H_n(A)&\xrightarrow{i_*}&H_n(X)
&\xrightarrow{q_*}&H_n(X,A)&\xrightarrow{\partial}&H_{n-1}(A)
\longrightarrow\cdots\\
&&\downarrow(f|_A)_*&&\downarrow f_*&&\downarrow f_*&&
\downarrow(f|_A)_*\\
\cdots&\longrightarrow&H_n(B)&\xrightarrow{i'_*}&H_n(Y)
&\xrightarrow{q'_*}&H_n(Y,B)&\xrightarrow{\partial'}&H_{n-1}(B)
\longrightarrow\cdots.
\end{array}
$$

**Diagram semantik.** Kedua baris adalah barisan eksak panjang pasangan.
Pemetaan vertikal diinduksi oleh $f$ dan pembatasannya pada subruang. Semua
persegi berkomutasi; khususnya,
$\partial'\circ f_*= (f|_A)_*\circ\partial$.
::::
:::

::: {.remark #o012-fom-u004-rem-naturality-chain-complexes data-source-lines="2642-2682"}
**Catatan (bentuk aljabar umum).** Secara lebih umum, barisan eksak panjang
homologi yang terkait dengan barisan eksak pendek kompleks rantai bersifat
alami. Jika terdapat morfisma komutatif antara dua barisan eksak pendek yang
komponen vertikalnya adalah $\alpha$, $\beta$, dan $\gamma$, maka diagram

:::: {.figure #o012-fom-u004-fig-naturality-chain-complexes data-source-lines="2647-2665" data-origin="edition-original-redraw"}
$$
\begin{array}{ccccccccc}
\cdots&\longrightarrow&H_n(\mathcal A)&\xrightarrow{i_*}&H_n(\mathcal B)
&\xrightarrow{q_*}&H_n(\mathcal C)&\xrightarrow{\partial}&
H_{n-1}(\mathcal A)\longrightarrow\cdots\\
&&\downarrow\alpha_*&&\downarrow\beta_*&&\downarrow\gamma_*&&
\downarrow\alpha_*\\
\cdots&\longrightarrow&H_n(\mathcal A')&\xrightarrow{i'_*}&
H_n(\mathcal B')&\xrightarrow{q'_*}&H_n(\mathcal C')
&\xrightarrow{\partial'}&H_{n-1}(\mathcal A')\longrightarrow\cdots
\end{array}
$$

komutatif.

**Diagram semantik.** Tiga pemetaan rantai vertikal menginduksi pemetaan
homologi pada setiap derajat. Persegi yang melibatkan pemetaan penghubung
menyatakan identitas $\partial'\gamma_*=\alpha_*\partial$.
::::
:::

::: {.source-omission #o012-fom-u004-omission-pr09 data-source-lines="2617-2665" data-repair-id="FOM-PR-09"}
**Argumen yang tidak diberikan dalam sumber.** Sumber mendefinisikan
kealamian barisan eksak panjang pasangan dan menyatakan bentuk aljabar
umumnya, tetapi tidak membuktikan komutativitas persegi yang memuat pemetaan
penghubung. Karena kealamian itu dipakai dalam bukti pembandingan pada Bagian
1.10, verifikasi tingkat rantai berikut disusun mandiri untuk edisi ini.
:::

::: {.proof-supplement #o012-fom-u004-proof-naturality-repair data-origin="edition-original" data-source-lines="2617-2665" data-repair-id="FOM-PR-09" data-proof-status="complete_original_repair"}
**Perbaikan bukti FOM-PR-09 (kealamian pemetaan penghubung).** Misalkan ada
diagram komutatif barisan eksak pendek kompleks rantai

$$
\begin{array}{ccccccccc}
0&\to&\mathcal A&\xrightarrow{i}&\mathcal B&\xrightarrow{q}&\mathcal C&\to&0\\
&&\downarrow\alpha&&\downarrow\beta&&\downarrow\gamma\\
0&\to&\mathcal A'&\xrightarrow{i'}&\mathcal B'&\xrightarrow{q'}&\mathcal C'&\to&0.
\end{array}
$$

Ambil kelas $[c]\in H_n(\mathcal C)$ dan wakili dengan siklus $c$. Pilih
$b\in\mathcal B_n$ dengan $q(b)=c$. Karena $q(\partial b)=\partial c=0$,
eksakitas memberi $a\in\mathcal A_{n-1}$ dengan $i(a)=\partial b$. Menurut
injektivitas $i$,
$i(\partial a)=\partial i(a)=\partial^2b=0$ juga memberi $\partial a=0$.
Menurut definisi, pemetaan penghubung baris atas mengirim $[c]$ ke $[a]$.

Pada baris bawah, $\beta(b)$ merupakan pengangkatan dari $\gamma(c)$ karena
$q'\beta(b)=\gamma q(b)=\gamma(c)$, dan

$$
\partial\beta(b)=\beta(\partial b)=\beta i(a)=i'\alpha(a).
$$

Karena itu pemetaan penghubung bawah mengirim $\gamma_*[c]$ ke
$\alpha_*[a]$, sehingga

$$
\partial'\gamma_*[c]=\alpha_*\partial[c].
$$

Persegi lain berkomutasi langsung dari $\beta i=i'\alpha$ dan
$q'\beta=\gamma q$. Jadi seluruh diagram barisan eksak panjang komutatif.
Untuk barisan pasangan, ambil diagram kompleks rantai yang diinduksi oleh
$f\colon(X,A)\to(Y,B)$; identitas yang sama memberi tepat kealamian pada
definisi. $\square$
:::

::: {.source-audit #o012-fom-u004-audit-spelling data-origin="edition-original" data-source-lines="2617-2619,2642-2646,2700-2704,2721-2722,2782-2785,2818-2821,2838-2843" data-adverse-candidate-id="FOM-U004B-ADV-002"}
**Kandidat koreksi tipografis.** Sumber mencetak “he long exact sequence”,
“that that”, “idependent”, “a long exact sequences”, “Suppse”, “two exact
sequence”, “interesected”, dan “surjevtive”. Terjemahan menormalkan semua
lokus tersebut tanpa mengubah isi matematis; semuanya dipertahankan di sini
sebagai satu kandidat koreksi sumber yang terdeduplikasi.
:::

## Homologi simpleksial versus homologi singular {#o012-fom-u004-s10 data-source-lines="2684-2845"}

::: {.remark #o012-fom-u004-rem-relative-simplicial data-source-lines="2686-2689"}
**Catatan.** Homologi simpleksial relatif dapat didefinisikan dengan cara
yang analog dengan homologi singular relatif.
:::

::: {.definition #o012-fom-u004-def-skeleton data-source-lines="2691-2696"}
**Definisi ($k$-kerangka suatu kompleks simpleksial).** Misalkan $X$ suatu
kompleks-$\Delta$. **$k$-kerangka** dari $X$ adalah gabungan citra semua
simpleks-$i$ untuk $0\leq i\leq k$. Kerangka ini dinotasikan dengan
$X^{(k)}$, atau cukup $X^k$.
:::

::: {.proposition #o012-fom-u004-prop-sing-simp data-source-label="prop:sing-simp" data-source-lines="2698-2705"}
**Proposisi (perbandingan simpleksial–singular).** Pemetaan alami

$$
f\colon C_n^{\Delta}(X)\longrightarrow C_n(X),
\qquad
f(\sigma_\alpha)=\sigma_\alpha,
$$

merupakan pemetaan rantai dan menginduksi isomorfisma

$$
f_*\colon H_n^{\Delta}(X)\xrightarrow{\cong}H_n(X)
$$

untuk setiap $n$. Secara khusus, homologi simpleksial suatu ruang topologis
$X$ tidak bergantung pada pilihan struktur kompleks-$\Delta$ pada $X$.
:::

::: {.source-audit #o012-fom-u004-audit-homology-not-homotopy data-origin="edition-original" data-source-lines="2700-2704" data-adverse-candidate-id="FOM-U004B-ADV-003"}
**Kandidat koreksi substantif.** Sumber mengatakan bahwa $f_*$ adalah
“an isomorphism in homotopy”, padahal $f_*$ pada baris yang sama ialah
pemetaan antara grup homologi. Terjemahan menyatakan sasaran yang bertipe
benar: $f_*$ merupakan isomorfisma dalam homologi.
:::

::: {.proof #o012-fom-u004-proof-sing-simp-finite data-source-lines="2706-2780"}
**Bukti, mula-mula untuk kompleks berdimensi hingga.** Andaikan
$X=X^{(N)}$ untuk suatu $N\geq0$. Kita membuktikan pernyataan dengan induksi
pada $k$-kerangka dari struktur kompleks-$\Delta$ yang diberikan.

Untuk $k=0$, kerangka $X^0$ merupakan gabungan lepas titik-titik, dan

$$
H_n^{\Delta}(X^0)\cong H_n(X^0)\cong
\begin{cases}
0,&n>0,\\
\displaystyle\bigoplus_{x\in X^0}\mathbb Z[x],&n=0.
\end{cases}
$$

Untuk langkah induksi, ambil $1\leq k\leq N$ dan andaikan
$H_n^{\Delta}(X^{k-1})\cong H_n(X^{k-1})$ untuk setiap $n$. Kita akan
membuktikan hasil yang sama untuk $X^k$. Pasangan
$(X^k,X^{k-1})$ merupakan pasangan baik. Kealamian menghubungkan barisan
eksak panjang simpleksial dan singular melalui pemetaan yang diinduksi oleh
$f$:

:::: {.figure #o012-fom-u004-fig-sing-simp-five-term data-source-lines="2721-2741" data-origin="edition-original-redraw"}
$$
\begin{array}{ccccccccc}
H_{n+1}^{\Delta}(X^k,X^{k-1})&\longrightarrow&
H_n^{\Delta}(X^{k-1})&\longrightarrow&H_n^{\Delta}(X^k)&\longrightarrow&
H_n^{\Delta}(X^k,X^{k-1})&\longrightarrow&H_{n-1}^{\Delta}(X^{k-1})\\
\downarrow f_*&&\downarrow f_*&&\downarrow f_*&&\downarrow f_*&&\downarrow f_*\\
H_{n+1}(X^k,X^{k-1})&\longrightarrow&
H_n(X^{k-1})&\longrightarrow&H_n(X^k)&\longrightarrow&
H_n(X^k,X^{k-1})&\longrightarrow&H_{n-1}(X^{k-1}).
\end{array}
$$

**Diagram semantik.** Kedua baris eksak mempunyai lima suku. Hipotesis
induksi mengendalikan panah vertikal kedua dan kelima; perhitungan relatif
berikut mengendalikan panah pertama dan keempat. Lemma lima lalu mengendalikan
panah vertikal tengah.
::::

Mulai sekarang, “panah pertama”, “panah kedua”, dan seterusnya berarti panah
vertikal dari kiri ke kanan. Hipotesis induksi menyatakan bahwa panah kedua
dan kelima adalah isomorfisma. Untuk panah pertama dan keempat, cukup
diperlihatkan bahwa

$$
H_n^{\Delta}(X^k,X^{k-1})\cong H_n(X^k,X^{k-1})
$$

melalui pemetaan yang diinduksi $f$, untuk semua $n$ dan $k$.

Kompleks rantai simpleksial relatif
$C_n^{\Delta}(X^k,X^{k-1})$ bernilai nol jika $n\ne k$, dan pada $n=k$
merupakan grup abelian bebas dengan basis semua simpleks-$k$ dari $X$.
Karena suku relatif pada derajat $k-1$ dan $k+1$ juga nol pada tempat yang
menentukan homologi ini,

$$
H_n^{\Delta}(X^k,X^{k-1})\cong
\begin{cases}
\displaystyle\bigoplus_{\alpha:\,n_\alpha=k}
\mathbb Z[\sigma_\alpha],&n=k,\\
0,&n\ne k.
\end{cases}
$$

Di sisi singular, $X^{k-1}$ merupakan retrak deformasi kuat dari suatu
lingkungannya di $X^k$. Teorema hasil bagi untuk pasangan baik dan
identifikasi ruang hasil bagi memberi

$$
\begin{aligned}
H_n(X^k,X^{k-1})
&\cong\widetilde H_n(X^k/X^{k-1})\\
&\cong\widetilde H_n\!\left(\bigvee_{s_k}S^k\right)\\
&\cong
\begin{cases}
\displaystyle\bigoplus_{\alpha:\,n_\alpha=k}
\mathbb Z[\sigma_\alpha],&n=k,\\
0,&n\ne k,
\end{cases}
\end{aligned}
$$

dengan $s_k$ banyaknya simpleks berdimensi $k$. Kompatibilitas pemetaan pada
tingkat generator dibuktikan dalam
[perbaikan FOM-PR-10](#o012-fom-u004-proof-relative-generator-repair) di
bawah: pemetaan relatif yang diinduksi $f$ adalah jumlah langsung unit pada
setiap komponen baji. Jadi pemetaan itu sendiri—bukan sekadar kedua grup
abstraknya—adalah isomorfisma. Panah pertama dan keempat pada diagram karena
itu isomorfisma.
Dengan [lemma lima](#o012-fom-u004-lem-five), panah ketiga juga isomorfisma.
Induksi pada $k$ menyelesaikan kasus berdimensi hingga. $\square$
:::

::: {.source-omission #o012-fom-u004-omission-pr10 data-source-lines="2747-2778" data-repair-id="FOM-PR-10"}
**Argumen yang tidak diberikan dalam sumber.** Sumber menghitung kedua grup
relatif secara abstrak, lalu langsung memakai lemma lima. Kesamaan tipe grup
tidak dengan sendirinya membuktikan bahwa **pemetaan pembandingan yang
sebenarnya** adalah isomorfisma. Verifikasi generator berikut menutup
ketergantungan tersebut.
:::

::: {.proof-supplement #o012-fom-u004-proof-relative-generator-repair data-origin="edition-original" data-source-lines="2747-2778" data-repair-id="FOM-PR-10" data-proof-status="complete_original_repair"}
**Perbaikan bukti FOM-PR-10 (kompatibilitas generator relatif).** Pada
derajat $k$, basis $C_k^\Delta(X^k,X^{k-1})$ terdiri atas simpleks berorientasi
$\sigma_\alpha\colon\Delta^k\to X^k$. Pemetaan pembandingan mengirim
$[\sigma_\alpha]$ ke **simpleks singular yang sama**, dipandang relatif
terhadap $X^{k-1}$.

Sesudah ruang bawah diruntuhkan, pemetaan karakteristik itu turun menjadi

$$
\Delta^k/\partial\Delta^k\cong S^k
\longrightarrow X^k/X^{k-1}\cong\bigvee_{\beta}S^k_\beta.
$$

Proyeksi ke komponen $S^k_\alpha$ mempunyai derajat $+1$ setelah orientasi
komponen dipilih sesuai orientasi $\sigma_\alpha$, sedangkan proyeksi ke
setiap komponen $S^k_\beta$ dengan $\beta\ne\alpha$ adalah konstan. Menurut
[proposisi generator simpleks](#o012-fom-u004-prop-simplex-generator) dan
[proposisi jumlah baji](#o012-fom-u004-prop-wedge-homology), pemetaan relatif
pada derajat $k$ karena itu adalah jumlah langsung pemetaan identitas

$$
\bigoplus_\alpha\mathbb Z[\sigma_\alpha]
\xrightarrow{\ \cong\ }
\bigoplus_\alpha\mathbb Z[S^k_\alpha].
$$

Pada setiap derajat $n\ne k$, kedua grup relatif bernilai nol, sehingga
pemetaan juga isomorfisma. Ini membuktikan kompatibilitas yang diperlukan
dalam langkah induksi, bukan hanya isomorfisma abstrak kedua ruas. $\square$
:::

::: {.source-audit #o012-fom-u004-audit-relative-case-indices data-origin="edition-original" data-source-lines="2751-2773" data-adverse-candidate-id="FOM-U004B-ADV-004"}
**Kandidat koreksi indeks pada rumus kasus.** Pada rumus simpleksial, sumber
mencetak syarat kedua $n_\alpha\ne0$; pada rumus singular, sumber mencetak
$n\ne0$. Kedua rumus sedang membandingkan derajat homologi $n$ dengan derajat
kerangka $k$, sehingga cabang nol yang bertipe dan sesuai dengan prosa adalah
$n\ne k$. Terjemahan juga menempatkan syarat $n_\alpha=k$ pada indeks jumlah
langsung, bukan sebagai syarat cabang yang menggantikan $n=k$.
:::

::: {.source-audit #o012-fom-u004-audit-finite-dimension-symbol data-origin="edition-original" data-source-lines="2707-2708" data-adverse-candidate-id="FOM-U004B-ADV-005"}
**Klarifikasi variabel.** Sumber memakai $n$ sekaligus untuk batas dimensi
dalam $X=X^{(n)}$ dan untuk derajat homologi. Terjemahan menamai batas dimensi
$N$ agar induksi kerangka dan derajat homologi tidak tercampur.
:::

::: {.lemma #o012-fom-u004-lem-five data-source-label="lem:five-lemma" data-source-lines="2782-2806"}
**Lemma (lemma lima).** Andaikan terdapat diagram komutatif grup abelian
dengan dua baris eksak,

:::: {.figure #o012-fom-u004-fig-five-lemma data-source-lines="2786-2803" data-origin="edition-original-redraw"}
$$
\begin{array}{ccccccccc}
A&\longrightarrow&B&\longrightarrow&C&\longrightarrow&D&\longrightarrow&E\\
\downarrow\alpha&&\downarrow\beta&&\downarrow\gamma&&
\downarrow\delta&&\downarrow\epsilon\\
A'&\longrightarrow&B'&\longrightarrow&C'&\longrightarrow&D'&\longrightarrow&E'.
\end{array}
$$

**Diagram semantik.** Dua baris berisi lima objek dan empat panah mendatar.
Lima panah vertikal $\alpha,\beta,\gamma,\delta,\epsilon$ membuat keempat
persegi komutatif.
::::

Jika $\alpha$, $\beta$, $\delta$, dan $\epsilon$ isomorfisma, maka
$\gamma$ isomorfisma.
:::

::: {.source-omission #o012-fom-u004-omission-pr07 data-source-lines="2807-2810" data-repair-id="FOM-PR-07"}
**Bagian yang dihilangkan dalam sumber.** Bukti sumber hanya berbunyi
“diagram chasing. to be added.” Tidak ada pembuktian injektivitas ataupun
surjektivitas panah tengah. Perbaikan lengkap berikut disusun mandiri untuk
edisi ini.
:::

::: {.proof #o012-fom-u004-proof-five-lemma-repair data-origin="edition-original" data-source-lines="2782-2810" data-repair-id="FOM-PR-07" data-proof-status="complete_original_repair"}
**Perbaikan bukti FOM-PR-07 (lemma lima).** Namai panah mendatar baris atas

$$
A\xrightarrow{p}B\xrightarrow{q}C\xrightarrow{r}D\xrightarrow{s}E
$$

dan panah baris bawah $p',q',r',s'$. Semua persegi komutatif.

Untuk membuktikan bahwa $\gamma$ injektif, ambil $c\in C$ dengan
$\gamma(c)=0$. Komutativitas memberi

$$
\delta(r(c))=r'(\gamma(c))=0.
$$

Karena $\delta$ injektif, $r(c)=0$. Eksakitas baris atas memberi
$b\in B$ dengan $q(b)=c$. Selanjutnya,

$$
q'(\beta(b))=\gamma(q(b))=\gamma(c)=0.
$$

Eksakitas baris bawah memberi $a'\in A'$ dengan
$p'(a')=\beta(b)$. Karena $\alpha$ surjektif, pilih $a\in A$ dengan
$\alpha(a)=a'$. Komutativitas lalu memberi

$$
\beta(p(a))=p'(\alpha(a))=p'(a')=\beta(b).
$$

Karena $\beta$ injektif, $p(a)=b$. Maka
$c=q(b)=q(p(a))=0$. Jadi $\gamma$ injektif.

Untuk membuktikan bahwa $\gamma$ surjektif, ambil $c'\in C'$ dan tuliskan
$d'=r'(c')$. Karena $\delta$ surjektif, pilih $d\in D$ dengan
$\delta(d)=d'$. Jika $e=s(d)$, maka

$$
\epsilon(e)=s'(\delta(d))=s'(d')=s'(r'(c'))=0.
$$

Karena $\epsilon$ injektif, $e=0$. Eksakitas baris atas memberi
$c\in C$ dengan $r(c)=d$. Sekarang

$$
r'(\gamma(c)-c')
=\delta(r(c))-r'(c')
=d'-d'=0.
$$

Eksakitas baris bawah memberi $b'\in B'$ dengan
$q'(b')=\gamma(c)-c'$. Karena $\beta$ surjektif, pilih $b\in B$ dengan
$\beta(b)=b'$. Letakkan $c_0=q(b)$. Komutativitas memberi

$$
\gamma(c_0)=q'(\beta(b))=q'(b')=\gamma(c)-c'.
$$

Dengan demikian $\gamma(c-c_0)=c'$, sehingga $\gamma$ surjektif. Jadi
$\gamma$ bijektif dan, sebagai homomorfisma grup abelian, merupakan
isomorfisma. $\square$
:::

::: {.lemma #o012-fom-u004-lem-compact-finite-simplices data-source-label="lem:sing-simp" data-source-lines="2812-2817"}
**Lemma.** Jika $C\subseteq X$ kompak, maka $C$ berpotongan dengan hanya
berhingga banyak simpleks $X$ pada interior masing-masing. Secara khusus,
$C\subseteq X^{(k)}$ untuk suatu $k$.
:::

::: {.proof #o012-fom-u004-proof-compact-finite-simplices-source data-source-lines="2818-2827" data-proof-status="source_incomplete"}
**Bukti sumber, sampai langkah yang belum dibuktikan.** Andaikan $C$
berpotongan dengan tak berhingga banyak simpleks terbuka. Pilih barisan tak
hingga titik $x_i\in C$, dengan setiap $x_i$ terletak pada simpleks terbuka
yang berbeda, dan definisikan

$$
U_i=X\setminus\bigcup_{j\ne i}\{x_j\}.
$$

Sumber kemudian menyatakan bahwa $\{U_i\}$ adalah penutup terbuka tanpa
subpenutup berhingga, tetapi tidak membuktikan bahwa setiap $U_i$ terbuka.
:::

::: {.source-omission #o012-fom-u004-omission-pr11 data-source-lines="2818-2827" data-repair-id="FOM-PR-11"}
**Argumen yang tidak diberikan dalam sumber.** Keterbukaan $U_i$ bergantung
pada topologi lemah dan sifat bahwa penutupan setiap simpleks hanya memuat
berhingga banyak muka; tanpa langkah
itu, kontradiksi kekompakan belum sah. Perbaikan berikut menyatakan dan
membuktikan langkah tersebut.
:::

::: {.proof-supplement #o012-fom-u004-proof-compact-finite-simplices-repair data-origin="edition-original" data-source-lines="2818-2827" data-repair-id="FOM-PR-11" data-proof-status="complete_original_repair"}
**Perbaikan bukti FOM-PR-11.** Andaikan $C$ berpotongan dengan tak berhingga
banyak simpleks terbuka. Pilih barisan tak hingga titik $x_i\in C$, dengan
setiap $x_i$ terletak pada simpleks terbuka yang berbeda. Definisikan

$$
U_i=X\setminus\bigcup_{j\ne i}\{x_j\}.
$$

Penutupan setiap simpleks hanya memuat berhingga banyak muka terbuka. Karena
dipilih paling banyak satu $x_j$ pada setiap simpleks terbuka, himpunan yang
dibuang berpotongan dengan setiap simpleks tertutup dalam himpunan berhingga,
dan karenanya tertutup. Menurut topologi lemah kompleks-$\Delta$, himpunan
yang dibuang itu tertutup di $X$. Karena itu setiap $U_i$ terbuka. Keluarga
$\{U_i\}$ menutupi $C$: titik yang bukan salah satu $x_j$ berada di setiap
$U_i$, sedangkan $x_i\in U_i$. Namun, gabungan berhingga
$U_{i_1}\cup\cdots\cup U_{i_m}$ tidak memuat
$x_j$ untuk $j\notin\{i_1,\ldots,i_m\}$. Jadi penutup tersebut tidak
mempunyai subpenutup berhingga, bertentangan dengan kekompakan $C$. Maka
$C$ hanya bertemu berhingga banyak simpleks terbuka. Maksimum dimensinya
memberi $k$ dengan $C\subseteq X^{(k)}$. $\square$
:::

::: {.remark #o012-fom-u004-rem-remove-finite-dimension data-source-lines="2829-2845"}
**Catatan (menghapus asumsi berdimensi hingga).** Lemma sebelumnya
memungkinkan kita membuktikan
[proposisi perbandingan](#o012-fom-u004-prop-sing-simp) tanpa asumsi
$X=X^{(N)}$.

Untuk surjektivitas, ambil kelas dalam $H_n(X)$ dan wakili dengan siklus
singular $z$. Dukungan $z$ adalah citra kontinu dari gabungan berhingga
simpleks kompak, sehingga kompak. Menurut
[lemma kekompakan](#o012-fom-u004-lem-compact-finite-simplices), dukungan itu
termuat dalam suatu $X^{(k)}$. Isomorfisma pada kerangka berdimensi hingga,

$$
H_n^{\Delta}(X^{(k)})\xrightarrow{\cong}H_n(X^{(k)}),
$$

memberi siklus simpleksial pada $X^{(k)}$ yang citra singularnya mewakili
$[z]$. Setelah dimasukkan ke $X$, siklus yang sama menunjukkan bahwa
$H_n^{\Delta}(X)\to H_n(X)$ surjektif.
:::

::: {.source-audit #o012-fom-u004-audit-surjectivity-class-type data-origin="edition-original" data-source-lines="2832-2841"}
**Koreksi tipe objek.** Sumber menyebut “an element in $X^{(k)}$” sebagai
prapeta suatu kelas homologi. Objek yang bertipe benar adalah kelas dalam
$H_n^\Delta(X^{(k)})$, diwakili oleh siklus simpleksial. Edisi menuliskan
kelas dan wakilnya secara eksplisit.
:::

::: {.source-omission #o012-fom-u004-omission-pr08 data-source-lines="2838-2844" data-repair-id="FOM-PR-08"}
**Bagian yang dihilangkan dalam sumber.** Sesudah argumen surjektivitas,
sumber hanya mengatakan bahwa injektivitas dapat diperlihatkan “secara
serupa”, lalu meninggalkan komentar “to be added”. Pernyataan itu belum
menangani rantai singular yang membatasi suatu siklus simpleksial. Perbaikan
lengkap berikut disusun mandiri untuk edisi ini.
:::

::: {.proof #o012-fom-u004-proof-injectivity-comparison-repair data-origin="edition-original" data-source-lines="2829-2845" data-repair-id="FOM-PR-08" data-proof-status="complete_original_repair"}
**Perbaikan bukti FOM-PR-08 (injektivitas untuk kompleks tak hingga).** Ambil
kelas $[z]\in H_n^{\Delta}(X)$ yang dipetakan ke nol dalam $H_n(X)$. Rantai
simpleksial $z$ adalah jumlah berhingga simpleks, sehingga terdapat $k$ dengan
$z\in C_n^{\Delta}(X^{(k)})$. Karena citra singularnya nol dalam homologi,
ada rantai singular berhingga $c\in C_{n+1}(X)$ dengan

$$
\partial c=f(z).
$$

Dukungan $c$ merupakan gabungan berhingga citra simpleks kompak, maka kompak.
Lemma sebelumnya memberi $m\geq k$ sehingga dukungan $c$ dan $z$ keduanya
termuat dalam $X^{(m)}$. Di dalam kerangka ini,

$$
f_*\colon H_n^{\Delta}(X^{(m)})
\xrightarrow{\cong}H_n(X^{(m)})
$$

adalah isomorfisma menurut kasus berdimensi hingga. Persamaan
$\partial c=f(z)$ menunjukkan bahwa $f_*[z]=0$ sudah di
$H_n(X^{(m)})$. Injektivitas isomorfisma tersebut memberi
$[z]=0$ di $H_n^{\Delta}(X^{(m)})$. Jadi terdapat rantai simpleksial
$w\in C_{n+1}^{\Delta}(X^{(m)})$ dengan

$$
\partial w=z.
$$

Inklusi $X^{(m)}\hookrightarrow X$ mempertahankan persamaan ini, sehingga
$[z]=0$ juga dalam $H_n^{\Delta}(X)$. Kernel pemetaan perbandingan trivial;
bersama surjektivitas di atas, pemetaan tersebut adalah isomorfisma untuk
setiap kompleks-$\Delta$, tanpa asumsi dimensi hingga. $\square$
:::

## Pemeriksaan penguasaan {#o012-fom-u004b-mastery data-origin="edition-original" data-course-route-unit-id="D60-R11"}

::: {.exercise #o012-fom-u004b-mcheck-001 data-origin="edition-original" data-course-route-unit-id="D60-R11"}
**Pemeriksaan Penguasaan F4B.1 (penutup kontraktibel dengan perpotongan tak
terhubung).** Misalkan $X=\mathring A\cup\mathring B$, dengan $A$ dan $B$
kontraktibel, sedangkan $A\cap B$ mempunyai tepat $r\geq1$ komponen lintasan
dan tidak mempunyai homologi tereduksi positif. Hitung
$\widetilde H_n(X)$ untuk semua $n\geq0$.
:::

::: {.hint #o012-fom-u004b-hint-001 data-origin="edition-original"}
**Petunjuk.** Gunakan barisan Mayer–Vietoris tereduksi. Ingat bahwa
$\widetilde H_0(A\cap B)\cong\mathbb Z^{r-1}$ dan bahwa $X$ terhubung
lintasan karena kedua bagian terhubung serta berpotongan.
:::

::: {.solution #o012-fom-u004b-sol-001 data-origin="edition-original"}
**Solusi Pemeriksaan F4B.1.** Karena $A$ dan $B$ kontraktibel,
$\widetilde H_n(A)=\widetilde H_n(B)=0$ untuk semua $n$. Untuk $n\geq1$,
potongan eksak memberi isomorfisma

$$
\widetilde H_n(X)\cong\widetilde H_{n-1}(A\cap B).
$$

Hipotesis pada perpotongan menunjukkan bahwa ruas kanan nol untuk $n\geq2$
dan bernilai $\mathbb Z^{r-1}$ untuk $n=1$. Karena $A$ dan $B$ terhubung
lintasan serta $A\cap B\ne\varnothing$, setiap titik $X$ dapat dihubungkan
ke titik perpotongan; jadi $X$ terhubung lintasan dan
$\widetilde H_0(X)=0$. Dengan demikian,

$$
\widetilde H_n(X)\cong
\begin{cases}
\mathbb Z^{r-1},&n=1,\\
0,&n\ne1.
\end{cases}
$$
:::

::: {.exercise #o012-fom-u004b-mcheck-002 data-origin="edition-original" data-course-route-unit-id="D60-R11" data-repair-id="FOM-PR-09"}
**Pemeriksaan Penguasaan F4B.2 (kealamian pemetaan penghubung).** Misalkan
$f\colon(X,A)\to(Y,B)$ peta pasangan. Jika kelas relatif
$[c]\in H_n(X,A)$ diwakili rantai $c\in C_n(X)$ dengan
$\partial c\in C_{n-1}(A)$, buktikan langsung dari wakil rantai bahwa

$$
\partial'\bigl(f_*[c]\bigr)
=(f|_A)_*\bigl(\partial[c]\bigr).
$$
:::

::: {.hint #o012-fom-u004b-hint-002 data-origin="edition-original"}
**Petunjuk.** Pemetaan penghubung mengirim $[c]$ ke kelas
$[\partial c]\in H_{n-1}(A)$. Gunakan identitas pemetaan rantai
$\partial f_\#=f_\#\partial$.
:::

::: {.solution #o012-fom-u004b-sol-002 data-origin="edition-original" data-repair-id="FOM-PR-09"}
**Solusi Pemeriksaan F4B.2.** Karena $f$ peta pasangan,
$f_\#(C_*(A))\subseteq C_*(B)$, sehingga
$f_*[c]=[f_\#c]\in H_n(Y,B)$ terdefinisi. Definisi pemetaan penghubung untuk
pasangan memberi

$$
\partial'\bigl(f_*[c]\bigr)
=[\partial f_\#c].
$$

Karena $f_\#$ pemetaan rantai,

$$
[\partial f_\#c]
=[f_\#(\partial c)]
=(f|_A)_*[\partial c].
$$

Di sisi lain, $\partial[c]=[\partial c]$ dalam $H_{n-1}(A)$. Maka

$$
\partial' f_*[c]=(f|_A)_*\partial[c],
$$

yang membuktikan komutativitas persegi pemetaan penghubung pada tingkat wakil.
:::

::: {.exercise #o012-fom-u004b-mcheck-003 data-origin="edition-original" data-course-route-unit-id="D60-R11" data-repair-id="FOM-PR-08"}
**Pemeriksaan Penguasaan F4B.3 (dukungan hingga dan injektivitas
perbandingan).** Misalkan $z$ suatu siklus simpleksial berhingga pada
kompleks-$\Delta$ $X$, dan andaikan citranya merupakan batas singular,
$f(z)=\partial c$. Susun argumen lengkap bahwa $z$ merupakan batas
simpleksial, tanpa mengasumsikan $X$ berdimensi hingga.
:::

::: {.hint #o012-fom-u004b-hint-003 data-origin="edition-original"}
**Petunjuk.** Tempatkan dukungan $z$ dan rantai singular berhingga $c$ dalam
satu kerangka berdimensi hingga $X^{(m)}$, lalu gunakan isomorfisma
pembandingan yang
sudah dibuktikan pada kerangka itu.
:::

::: {.solution #o012-fom-u004b-sol-003 data-origin="edition-original" data-repair-id="FOM-PR-08"}
**Solusi Pemeriksaan F4B.3.** Karena $z$ merupakan jumlah berhingga
simpleks, ia termuat dalam $X^{(k)}$ untuk suatu $k$. Dukungan rantai singular
$c$ adalah gabungan berhingga citra simpleks kompak, sehingga kompak. Lemma
kekompakan menempatkannya dalam $X^{(m)}$ untuk suatu $m\geq k$. Dengan
demikian, persamaan

$$
f(z)=\partial c
$$

sudah berlaku di kompleks singular $X^{(m)}$. Pemetaan

$$
f_*\colon H_n^{\Delta}(X^{(m)})\longrightarrow H_n(X^{(m)})
$$

adalah isomorfisma karena $X^{(m)}$ berdimensi hingga. Citra kelas $[z]$ di
ruas kanan nol, maka injektivitas $f_*$ memberi $[z]=0$ di ruas kiri. Jadi
ada $w\in C_{n+1}^{\Delta}(X^{(m)})$ dengan $\partial w=z$. Rantai $w$ juga
merupakan rantai simpleksial di $X$, sehingga $z$ batas simpleksial dalam
$X$. Ini membuktikan bahwa kernel pemetaan perbandingan global adalah nol.
:::

::: {.boundary #o012-fom-u004b-boundary-001}
**Batas sumber draf.** Draf ini menerjemahkan secara kontigu
`algebraic_topology.tex` baris 2441–2846, mencakup Bagian 1.8–1.10:
Mayer–Vietoris, kealamian, serta perbandingan homologi simpleksial dan
singular. Rentang sumber terdiri atas 406 baris fisik dan 17.079 byte setelah
normalisasi LF dengan satu LF penutup; SHA-256-nya adalah
`aafde945d05d1594b651da867ef080b1f17b4ab323783fb625324213a738d0dc`.
Kursor sumber berikutnya adalah baris 2847, awal Bagian 1.11 tentang derajat.
:::
