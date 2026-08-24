# Tinjauan independen Fomberg Unit 002 — Bagian A

Tanggal: 2026-08-24  
Putusan akhir pascaperbaikan: **`PASS`**  
`FINAL_SEVERITY_COUNTS: {"P1":0,"P2":0,"P3":0}`  
Riwayat snapshot pra-perbaikan: **P1 = 1, P2 = 3, P3 = 3; seluruhnya
terselesaikan**

Tinjauan ini hanya membandingkan bagian pembaca yang memetakan
`algebraic_topology.tex` baris 615–953 dengan otoritas beku dan terminologi
yang telah diterima. Rebinding terakhir juga memeriksa permukaan kecil yang
beririsan dengan hasil Bagian A setelah snapshot maju: petunjuk penguasaan
F2.1, kalimat batas-lintasan F2.2, dan bukti kontraktilitas yang memakai
homologi satu titik. Tidak ada perubahan pada pembaca, glosarium, backend,
ledger, ataupun berkas QA lain oleh tinjauan ini.

## Identitas snapshot

- Otoritas: `algebraic_topology.tex`, commit
  `563194fae879178b9a6871b249513bfc27968975`.
- Berkas otoritas: 223.886 byte, SHA-256
  `d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483`.
- Rentang 615–953 setelah normalisasi LF dan satu LF penutup: 11.285 byte,
  SHA-256
  `e152211331e25f434fd79bd2f0ebb6a98c177a15080882bbe18a4ff3ebce764f`.
- Pembaca pra-perbaikan pada tinjauan pertama:
  `source/id-ID/fomberg/units/fomberg-unit-002-singular-homology-homotopy-invariance.md`,
  41.339 byte, 1.221 baris menurut pemisahan LF, SHA-256
  `16bf11d237577d85d6ae5bb08479b54a66a629ffedec77fd73901f6329a73305`.
- Snapshot PASS antara yang ditinjau ulang: berkas yang sama, 44.143 byte,
  1.338 baris LF, SHA-256
  `36083efc7b18c9bc76f8bf6ed9538e505e49913d860c5a5e229043026a739bc7`.
- Pembaca final yang menjadi dasar putusan sekarang: berkas yang sama,
  **44.407 byte, 1.342 baris LF, SHA-256
  `0851ab7d9f5ded1e836a0e73aa055fbd28b82998208d8136ec0cf4757747435c`**.

## Rebinding setelah audit penuh

Audit penuh menemukan tiga residu pada snapshot `36083efc…`; tidak satu pun
mengubah prosa terjemahan sumber Bagian A baris 615–953. Permukaan yang dapat
mempengaruhi penilaian Bagian A diperiksa ulang langsung pada snapshot
`0851ab7d…`:

- Petunjuk F2.1 kini menyatakan $\partial_0=0$ secara terpisah dan membatasi
  mnemonik $\sum_{i=0}^{n}(-1)^i$ pada $n\geq1$. Jadi petunjuk tidak lagi
  menerapkan rumus derajat positif pada derajat nol.
- Solusi F2.2 kini menyatakan bahwa selisih titik dengan wakil komponennya
  merupakan batas suatu lintasan. Kalimat ini bertipe benar dan alami dalam
  bahasa Indonesia.
- Bukti kontraktilitas memilih $x_0$, mendefinisikan
  $f\colon X\to\{*\}$ dan $g\colon\{*\}\to X$, lalu memeriksa
  $f\circ g=\operatorname{id}_{\{*\}}$ serta
  $g\circ f=c_{x_0}\simeq\operatorname{id}_X$. Bukti kini benar-benar
  menghasilkan pasangan ekuivalensi homotopi, bukan menyamakan kontraksi
  dengan ekuivalensi.

Ketiga perubahan tersebut menutup `O012-ADV-0454`–`O012-ADV-0456`. Tidak
ditemukan regresi pada hasil homologi satu titik, dekomposisi komponen,
augmentasi, formula, pengenal, locator, atau terminologi Bagian A.

## Resolusi pascaperbaikan

| ID temuan | Lokator pembaca final | Bukti resolusi | Status |
|---|---|---|---|
| `FOM-U002-A-REV-P1-001` | 113–168 | Bukti kini menyatakan $\partial_0(\sigma^0)=0$ tersendiri dan membatasi rumus paritas ke $n\geq1$; kasus $0/0$ dan $\mathbb Z/\mathbb Z$ juga eksplisit. | `RESOLVED` |
| `FOM-U002-A-REV-P2-001` | 176–235 | Lema sumber atas komponen terhubung dipertahankan dan dibuktikan; dekomposisi atas komponen lintasan hadir sebagai penguatan edisi ber-ID dan `data-origin` tersendiri. Audit menjelaskan bahwa keduanya sah. | `RESOLVED` |
| `FOM-U002-A-REV-P2-002` | 50–83, 113–168, 186–209, 243–270, 284–350 | Definisi $C_n$, kedua hasil bagi paritas, hasil-bagi komponen, dua tampilan bukti pertama $H_0$, persamaan kernel augmentasi, dan rantai Teorema Isomorfisma Pertama kembali eksplisit pada posisi argumennya. | `RESOLVED` |
| `FOM-U002-A-REV-P2-003` | 470–509 | Formula siklus umum mendahului contoh derajat satu; gambar kembali berada sebelum pembahasan Kirchhoff/manifold; audit kini mencakup klaim nonsiklus, manifold berbatas, dan pseudomanifold pada baris sumber 942–951. | `RESOLVED` |
| `FOM-U002-A-REV-P3-001` | 171–174, 322–326, 447–453, 500–509 | Tambahan “kefungtoran” dihapus; kedua pemakaian basepoint menjadi `titik basis`; bentuk audit menjadi `insidensi nonmanifold`. | `RESOLVED` |
| `FOM-U002-A-REV-P3-002` | 41, 50–99, 171–174 | Locator definisi kini tepat `616-619`; uraian $\partial^2=0$ dipisahkan sebagai `edition-note` dengan `data-origin="edition-original"`; catatan homeomorfisma kembali hanya memuat isi sumber. | `RESOLVED` |
| `FOM-U002-A-REV-P3-003` | 482–487 | Deskripsi gambar kini secara eksplisit menyebut “simpul pusat tanpa label”; nama node internal TikZ tidak lagi disajikan sebagai label terlihat. | `RESOLVED` |

Pembacaan ulang penuh pada byte final tidak menemukan regresi baru. Riwayat
temuan berikut dipertahankan agar alasan setiap perbaikan dapat diaudit;
semua lokator bermasalah dalam riwayat itu merujuk pada SHA pra-perbaikan
`16bf11d2...`, bukan pada pembaca final.

## Riwayat temuan P1 pra-perbaikan

### `FOM-U002-A-REV-P1-001` — rumus batas titik salah mencakup derajat nol

**Lokator pembaca:** baris 99–115,
`#o012-fom-u002-proof-point`  
**Lokator sumber:** baris 652–668, terutama 658–659

Sumber secara eksplisit memisahkan
$\partial_0(\sigma^0)=0$ dari rumus berselang-seling yang hanya berlaku untuk
$n\geq1$. Pembaca menghapus pemisahan itu: setelah mengatakan bahwa terdapat
satu simpleks pada setiap derajat, pembaca langsung menulis

$$
\partial_n\sigma^n
=\sum_{i=0}^{n}(-1)^i
\underbrace{\sigma^n|_{\partial_i\Delta^n}}_{\sigma^{n-1}}
=
\begin{cases}
\sigma^{n-1},&n\text{ genap},\\
0,&n\text{ ganjil}.
\end{cases}
$$

Tanpa syarat $n\geq1$, rumus itu menyatakan
$\partial_0\sigma^0=\sigma^{-1}$, berlawanan dengan konvensi kompleks
singular dan dengan perhitungan pembaca sendiri pada baris 133. Gambar
semantik pada baris 126–130 memang mengatakan “derajat genap positif”, tetapi
tidak memperbaiki ruang lingkup rumus utama.

**Perbaikan yang diperlukan:** sebelum rumus, nyatakan
$\partial_0(\sigma^0)=0$; awali rumus berselang-seling dengan “untuk
$n\geq1$”.

## Riwayat temuan P2 pra-perbaikan

### `FOM-U002-A-REV-P2-001` — hasil sah tentang komponen terhubung diganti, bukan dipertahankan

**Lokator pembaca:** baris 147–182,
`#o012-fom-u002-lem-components` dan audit sesudahnya  
**Lokator sumber:** baris 714–739

Sumber menyatakan lema untuk **komponen terhubung** $X_\alpha$, lalu satu
kalimat buktinya menyebut komponen lintasan. Pembaca mengganti seluruh lema
dengan dekomposisi atas **komponen lintasan** dan menyebut perubahan itu
sebagai koreksi. Dekomposisi atas komponen lintasan memang benar dan cocok
dengan akibat $H_0$, tetapi pernyataan tercetak atas komponen terhubung juga
benar: citra setiap simpleks singular terhubung lintasan, sehingga khususnya
termuat dalam satu komponen terhubung; kompleks rantai lalu terdekomposisi
menurut komponen terhubung. Jadi hasil sumber yang sah telah hilang, bukan
sekadar salah ketik yang telah dibetulkan. Ledger terminologi juga sengaja
membedakan `connected component` = `komponen terhubung` dari
`path component` = `komponen lintasan`.

**Perbaikan yang diperlukan:** pertahankan lema sumber untuk komponen
terhubung dan nyatakan dekomposisi komponen lintasan sebagai penguatan/akibat,
atau tulis kedua dekomposisi secara eksplisit. Koreksi ruas kiri baris sumber
736 dari $H_n(X_\alpha)$ menjadi $H_n(X)$ tetap benar.

### `FOM-U002-A-REV-P2-002` — beberapa objek rumus sumber dikondensasikan atau hilang

**Lokator pembaca utama:** baris 50–77, 99–138, 157–174, 190–197,
211–263  
**Lokator sumber:** baris 621–639, 652–705, 719–739, 746–762,
776–830

Urutan teorema dan kesimpulan matematis utama dipertahankan, tetapi kontrak
“setiap formula” belum terpenuhi. Contoh yang konkret:

1. definisi display
   $C_n(X):=\{\text{grup abelian bebas ...}\}$ pada baris 625–628 telah
   menjadi prosa, sehingga relasi definisional `:=` tidak lagi hadir sebagai
   objek rumus (meskipun koreksi tipe terhadap kurung himpunan memang tepat);
2. dua perhitungan hasil bagi pada baris 692–705,
   $\mathbb Z/\mathbb Z$ dan $\{0\}/\{0\}$, hilang dari bukti utama. Untuk
   $n$ genap, pembaca bahkan hanya menyebut kernelnya dan tidak menyatakan
   $\operatorname{im}\partial_{n+1}=0$ sebelum menyimpulkan $H_n=0$;
3. identitas hasil-bagi penutup pada baris 735–737, dua tampilan dalam bukti
   pertama $H_0$ pada baris 748–759, rantai isomorfisma pada baris 797–801,
   dan persamaan kernel pada baris 811–813 semuanya dikondensasikan menjadi
   prosa atau tidak diulang di posisi sumbernya.

Sebagian isi muncul kembali dalam latihan edisi, tetapi itu memindahkan rumus
sumber ke lapisan `edition-original` dan tidak mempertahankan urutan sumber.

**Perbaikan yang diperlukan:** pulihkan formula-formula tersebut pada posisi
argumennya. Rumus berulang boleh digabung ke blok `aligned`, tetapi setiap
kesamaan dan kedua kasus hasil bagi harus tetap eksplisit.

### `FOM-U002-A-REV-P2-003` — urutan dan closure bagian geometris belum setia

**Lokator pembaca:** baris 383–413,
`#o012-fom-u002-rem-geometric`, `#o012-fom-u002-fig-flow-balance`, dan
audit sesudahnya  
**Lokator sumber:** baris 914–952

Ada tiga masalah terkait pada satu bagian sumber:

1. sumber lebih dahulu memberi formula umum
   $c=\sum n_\sigma\sigma\in Z_n(X)$, baru memberi contoh
   $c=\sum n_e e\in Z_1(X)$. Pembaca hanya mempertahankan contoh
   derajat satu;
2. gambar sumber pada baris 921–937 berada sebelum pembahasan Kirchhoff dan
   manifold pada baris 938–951. Pembaca menempatkan seluruh pembahasan itu
   sebelum gambar, jadi fungsi diagram telah direlokasi melawan urutan sumber;
3. klaim baris 947–948 bahwa rantai yang bukan siklus menghasilkan manifold
   berbatas dihapus, tetapi audit hanya mencatat cacat pada baris 942–946.
   Penghapusan itu secara matematis beralasan—rantai singular umum tidak
   otomatis merealisasikan manifold berbatas—namun koreksi tersebut belum
   dicatat. Pelemahan baris 950–951 menjadi “siklus atau pseudomanifold
   berbobot” juga tidak dijelaskan dalam audit.

Koreksi hukum arus Kirchhoff dan penolakan implikasi “siklus = manifold”
sendiri benar.

**Perbaikan yang diperlukan:** pulihkan formula siklus umum, letakkan gambar
di antara uraian keseimbangan dan pembahasan sesudahnya, lalu perluas audit
agar mencakup baris 947–951 dan alasan matematis untuk setiap pelemahan.

## Riwayat temuan P3 pra-perbaikan

### `FOM-U002-A-REV-P3-001` — dua istilah tidak mengikuti ledger hidup

**Lokator pembaca:** baris 143–144, 249–250, dan 364–366

- Ledger menerima `functoriality` sebagai **fungtorialitas**, tetapi pembaca
  memakai “kefungtoran”.
- Ledger menerima `basepoint` sebagai **titik basis**, tetapi pembaca dua kali
  memakai “titik dasar”.

Gunakan istilah yang diterima atau ubah ledger lebih dahulu melalui keputusan
terminologi tersendiri; jangan membiarkan dua keluarga istilah berjalan tanpa
catatan. Frasa audit “insidensi takmanifold” pada baris 411–412 juga kurang
alami; “insidensi nonmanifold” atau “insidensi yang bukan manifold” lebih
jelas.

### `FOM-U002-A-REV-P3-002` — locator sumber mengklaim prosa edisi sebagai prosa sumber

**Lokator pembaca:** baris 41, 50–77, dan 141–144

- Definisi simpleks singular diberi `data-source-lines="615-619"`, padahal
  baris 615 adalah judul subbagian dan definisinya sendiri berada pada
  616–619.
- Paragraf baris pembaca 75–77 tentang $\partial^2=0$, pembatalan muka ganda,
  dan rujukan ke Unit 001 tidak terdapat pada baris sumber 621–639, tetapi
  berada dalam blok yang seluruhnya mengklaim locator itu.
- Kalimat bahwa invariansi homeomorfisma “akan menjadi akibat langsung dari
  kefungtoran” tidak terdapat pada baris sumber 709–712.

Tambahan-tambahan itu benar dan berguna, tetapi perlu dipisahkan sebagai
catatan edisi dengan `data-origin` yang tepat atau dicakup oleh audit
perubahan. Ubah locator definisi menjadi `616-619`.

### `FOM-U002-A-REV-P3-003` — deskripsi diagram mengubah nama node internal menjadi label terlihat

**Lokator pembaca:** baris 398–403,
`#o012-fom-u002-fig-flow-balance`  
**Lokator sumber:** baris 921–937, terutama 929

TikZ sumber menulis `\node ... (v) at (0,0) {};`. Teks `(v)` adalah nama node
internal untuk TikZ; node tersebut tidak mempunyai label yang dirender.
Pembaca mengatakan “simpul $v$” dan kembali merujuk “di $v$”, sehingga
menciptakan label terlihat yang tidak ada dalam gambar sumber. Fungsi diagram
lain—tiga sisi $e'_i$ masuk dan tiga sisi $e_i$ keluar—sudah benar.

**Perbaikan yang diperlukan:** tulis “sebuah simpul pusat” tanpa label, atau
tandai $v$ secara eksplisit sebagai nama yang ditambahkan oleh edisi.

## Pemeriksaan yang lulus

- Seluruh tiga definisi, tiga lema, empat blok bukti, satu akibat, sepuluh
  catatan, dan enam fungsi diagram dari baris 615–952 mempunyai padanan dalam
  pembaca; tidak ada blok lingkungan sumber yang hilang seluruhnya.
- Label sumber tunggal `lem:path-connected-then-hzero-z` dipertahankan pada
  lema yang tepat.
- Bagian A final mempunyai 35 ID berawalan `o012-fom-u002`; semuanya unik.
  Empat tautan fragmen internal mempunyai target. Jumlah pembuka dan penutup
  fenced-div sama-sama 33; Pandoc mem-parsing seluruh pembaca dengan kode
  keluar nol.
- Semua locator numerik Bagian A berada di dalam rentang otoritas 615–953 dan
  mempunyai awal yang tidak melampaui akhirnya. Definisi pembuka kini tepat
  memetakan 616–619; label sumber dan urutan blok sumber tetap utuh meskipun
  dua blok edisi ber-ID disisipkan secara transparan.
- Semua formula aktif sumber hadir dalam urutan matematisnya. Ini mencakup
  definisi grup rantai, rumus batas, kompleks satu titik beserta dua kasus
  hasil bagi, kedua dekomposisi komponen, dua bukti $H_0$, augmentasi,
  kompleks rantai umum, kedua diagram kompleks teraugmentasi, hubungan
  homologi biasa–tereduksi, dan formula siklus umum.
- Keenam fungsi diagram dipertahankan pada posisi sumber: kompleks satu titik,
  ujung derajat nol, kompleks rantai umum, dua kemunculan kompleks
  teraugmentasi, dan keseimbangan enam sisi pada satu simpul. Arah, label sisi,
  paritas pemetaan, dan ketiadaan label terlihat pada simpul terakhir kini
  benar.
- Koreksi kurung himpunan pada definisi $C_n$, batas indeks penjumlahan,
  ruas kiri salah pada baris sumber 736, hipotesis tak kosong untuk lema
  $H_0$, ejaan augmentasi, pemisahan $H_0$, hukum arus Kirchhoff, serta
  penolakan klaim manifold tanpa hipotesis tambahan semuanya matematis dan
  beralasan.
- Terminologi inti `simpleks singular`, `homologi singular`, `kompleks rantai
  singular`, `pemetaan batas`, `siklus`, `batas`, `komponen lintasan`,
  `komponen terhubung`, `augmentasi`, `kompleks rantai teraugmentasi`,
  `homologi tereduksi`, `jumlah langsung`, `homomorfisma`, dan
  `homeomorfik` sesuai ledger.
- Tidak tersisa `kefungtoran`, `titik dasar`, atau `takmanifold` pada Bagian A.
  Bahasa Indonesia final terbaca alami dan konsisten dengan gaya Unit 001.

## Kesimpulan

Pada pembaca final SHA-256
`0851ab7d9f5ded1e836a0e73aa055fbd28b82998208d8136ec0cf4757747435c`,
ketujuh temuan pra-perbaikan benar-benar terselesaikan. Pembacaan ulang penuh
terhadap otoritas baris 615–953 tidak menemukan cacat baru pada matematika,
closure formula, urutan dan fungsi diagram, bahasa, terminologi, pengenal, atau
locator. Putusan akhir Bagian A ialah **`PASS`**, dengan
`FINAL_SEVERITY_COUNTS: {"P1":0,"P2":0,"P3":0}`.
