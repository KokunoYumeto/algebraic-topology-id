# Tinjauan independen Fomberg Unit 001

Tanggal: 2026-08-24  
Putusan akhir pascaperbaikan: **`PASS`**  
`FINAL_SEVERITY_COUNTS: {"P1":0,"P2":0,"P3":0}`  
Riwayat pra-perbaikan: **P1 = 1, P2 = 3, P3 = 2; seluruhnya terselesaikan**

Tinjauan ini hanya membandingkan pembaca Unit 001 dengan otoritas beku dan
audit sumber. Tidak ada perubahan pada pembaca, glosarium, backend, atau
ledger bersama.

## Identitas yang diperiksa

- Otoritas: `algebraic_topology.tex` pada commit
  `563194fae879178b9a6871b249513bfc27968975`, tree
  `fb678966d1533d529bdd72f49d8496a3bdc14a9b`.
- Berkas otoritas: 223.886 byte, 6.069 baris LF, SHA-256
  `d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483`.
- Rentang yang dihitung ulang langsung dari byte otoritas: baris 31–614,
  offset 671–22.545 inklusif, 21.875 byte, SHA-256
  `68cb0dea7aa24a42e979877a95acf61b8152c87ed86d88ad7deac7cb5cea2fe3`.
- Audit pembanding saat tinjauan pertama:
  `qa/FOMBERG_UNIT_001_SOURCE_AUDIT.md`, 16.360 byte, SHA-256
  `774571f51d5cc594fc3f6736db8e0751adaf414d9faf70e27636c76e1db145c9`.
- Audit pembanding pascaperbaikan:
  `qa/FOMBERG_UNIT_001_SOURCE_AUDIT.md`, 16.794 byte, SHA-256
  `4157bfcfc12502d5fd56fb55cd162f3b45dae40eee2c5319cc7a8f245bb88e3a`,
  beserta JSON valid 4.513 byte, SHA-256
  `f8706a32f0bf7cdb0695d9d70e808dd0b03dfa2af6a6c40bd3817b9c4a7956b0`.
  Audit kini mencatat kesalahan tipe muka sumber sebagai
  `FOM-U001-SRC-015`, jadi perbaikannya bukan koreksi tak terlacak.
- Pembaca: `source/id-ID/fomberg/units/fomberg-unit-001-delta-complexes-simplicial-homology.md`.
  Identitas pra-perbaikan pada awal tinjauan ialah 33.943 byte, 1.060 baris LF,
  SHA-256
  `20cb76761248ad0650fa726cbfad578da2c15b09dae128014798c0b97c4782ee`.
  Laporan pra-perbaikan yang merekam enam temuan mempunyai SHA-256
  `cc46d76d237bfa5d05b8c6c0ee2c4fe8e808a294a42eef7c189d655cc5271091`.
- Kandidat perbaikan pertama, 34.621 byte / 1.071 baris LF / SHA-256
  `deab0769355fde0210252da0771f196a2140554af98d7400f3092a6d16526d75`,
  **tidak** diloloskan: frasa arah yang bergantung pada sumber masih tersisa
  pada model cakram $\mathbb{RP}^2$.
- Pembaca final yang ditinjau ulang: **34.773 byte, 1.073 baris LF, tanpa CR,
  SHA-256
  `d9b64140f9340c75bc34c12bc02ee843d87de3566e331c50c2374075718aa2c6`**.

## Resolusi pascaperbaikan

| ID temuan | Lokator pembaca final | Bukti resolusi | Status |
|---|---|---|---|
| `FOM-U001-REV-P1-001` | 640–646 | $V$ kini dinyatakan sebagai pemetaan karakteristik berdomain simpleks-$2$; ketiga mukanya dinyatakan sebagai pembatasan pada simpleks-$1$. | `RESOLVED` |
| `FOM-U001-REV-P2-001` | 259–262, 493–495, 586–588 | Ketiga penggambaran loop secara konsisten menyatakan arah searah jarum jam, sesuai lintasan TikZ $90^\circ\to-270^\circ$; kata “positif” dihapus. | `RESOLVED` |
| `FOM-U001-REV-P2-002` | 293–301, 334–348, 629–634 | Arah empat sisi/diagonal torus, empat sisi persegi $\mathbb{RP}^2$, serta panah kiri-turun/kanan-naik pada cakram kini eksplisit dan tidak memerlukan gambar sumber. Pengulangan torus merujuk ke deskripsi lengkap yang teresolusi. | `RESOLVED` |
| `FOM-U001-REV-P2-003` | 809–833 | Klaim kini secara eksplisit memakai $H_1^{\mathrm{sing}}$, lalu menyatakan jembatan pembandingan ke $H_1^\Delta$; keterhubungan lintasan, titik dasar, dan koefisien $\mathbb Z$ tetap ada. | `RESOLVED` |
| `FOM-U001-REV-P3-001` | 778–790 | Definisi siklus homolog memakai $Z_n^\Delta$, $H_n^\Delta$, dan $B_n^\Delta$ secara konsisten. | `RESOLVED` |
| `FOM-U001-REV-P3-002` | 177–179, 420–424 | “muka dari” telah bertipe dan berbahasa alami; judul kini “dua contoh yang bukan kompleks simpleksial”. | `RESOLVED` |

Tidak ditemukan temuan baru pada pembacaan ulang byte final. Bagian berikut
mempertahankan teks keenam temuan pra-perbaikan sebagai riwayat audit; semua
lokator dan bentuk bermasalah di bagian itu merujuk pada SHA pra-perbaikan
`20cb7676...`, bukan pada pembaca final.

## Riwayat temuan pra-perbaikan (dipertahankan)

### P1 — kesalahan tipe muka/simpleks pada catatan torus

**ID:** `FOM-U001-REV-P1-001`  
**Lokator pembaca:** baris 634–637, `#o012-fom-u001-rem-012`  
**Lokator sumber:** baris 497–505, terutama 499–500

Pembaca mengatakan bahwa “suatu muka kompleks-$\Delta$ adalah citra
simpleks-$2$ $[v_0,v_1,v_2]$”. Ini salah tipe: $V$ adalah simpleks-$2$ dengan
domain $[v_0,v_1,v_2]$, sedangkan muka-mukanya adalah pembatasan $V$ pada
simpleks-$1$ seperti $[v_0,v_1]$, $[v_1,v_2]$, dan $[v_0,v_2]$. Sumber memang
memuat frasa rancu yang sama, tetapi terjemahan tidak boleh mempertahankan
kesalahan itu karena pembedaan antara pemetaan karakteristik berdimensi dua,
pembatasan muka, dan koefisien rantai adalah inti catatan tersebut. Ganti
kalimat pembuka dengan pernyataan bertipe benar; pertahankan penjelasan yang
sudah benar bahwa tanda $-g$ ialah koefisien rantai, bukan pemetaan topologis.

### P2 — arah loop sumber dilabeli “positif” secara keliru

**ID:** `FOM-U001-REV-P2-001`  
**Lokator pembaca:** baris 257–261, `#o012-fom-u001-fig-001`  
**Lokator sumber:** baris 156–162, khususnya 158

TikZ sumber menelusuri busur dari sudut $90^\circ$ ke $-270^\circ$, yakni satu
putaran **searah jarum jam**. Pembaca menyebutnya “loop berorientasi positif”,
yang secara konvensional berarti berlawanan arah jarum jam dan tidak pernah
dinyatakan oleh sumber. Arah ini tidak mengubah perhitungan $\partial e=0$,
tetapi merupakan kehilangan fidelitas diagram. Tulis “loop terarah berlabel
$e$” jika konvensi positif tidak dibutuhkan, atau nyatakan arah searah jarum
jam secara eksplisit dan gunakan arah yang sama pada dua pengulangan loop.

### P2 — dua deskripsi diagram masih bergantung pada gambar sumber

**ID:** `FOM-U001-REV-P2-002`  
**Lokator pembaca:** baris 292–300 dan 332–344,
`#o012-fom-u001-fig-002` serta `#o012-fom-u001-fig-003`  
**Lokator sumber:** baris 185–209 dan 219–253

Semua empat belas node diagram memang tercakup dalam sepuluh kelompok
semantik, tetapi kedua kelompok ini memakai frasa “panah ... mengikuti
identifikasi sumber” dan “sesuai panah sumber”. Pembaca mandiri atau pembaca
layar tidak dapat memulihkan arah dari frasa itu. Untuk persegi torus, arah
pasangan harus dieja (kedua sisi mendatar ke kanan, kedua sisi tegak ke atas,
dan diagonal dari kiri-bawah ke kanan-atas), di samping orientasi $V$ dan $L$
yang sudah tercatat. Untuk persegi $\mathbb{RP}^2$, nyatakan bahwa sisi atas
dan bawah berarah berlawanan, demikian pula sisi kiri dan kanan, beserta arah
masing-masing pada model yang dipilih. Ini perbaikan aksesibilitas/fungsi
diagram, bukan permintaan menambah gambar dekoratif.

### P2 — ruang lingkup klaim abelianisasi belum dibedakan dari homologi
simpleksial unit

**ID:** `FOM-U001-REV-P2-003`  
**Lokator pembaca:** baris 802–814, `#o012-fom-u001-rem-013`  
**Lokator sumber:** baris 610–613

Perbaikan utama sudah benar: pembaca memakai subskrip $H_1$, koefisien
$\mathbb Z$, hipotesis $X$ terhubung lintasan, dan titik dasar $x_0$. Namun
unit ini baru mendefinisikan $H_n^\Delta$, sedangkan catatan menulis
$H_1(X;\mathbb Z)$ tanpa menjelaskan apakah simbol itu berarti homologi
singular atau homologi simpleksial melalui teorema pembandingan. Nyatakan
salah satu dari dua jalur secara eksplisit: (a) klaim umum untuk homologi
singular, dengan catatan bahwa jembatan ke $H_1^\Delta$ datang pada bagian
pembandingan; atau (b) klaim $H_1^\Delta(X;\mathbb Z)$ untuk kompleks-$\Delta$
terhubung lintasan, lagi-lagi dengan penanda bahwa isomorfisma pembanding akan
dibuktikan kemudian. Hipotesis abelianisasi sendiri **lulus**; temuannya ialah
ruang lingkup notasi dan jembatan yang belum dinyatakan.

### P3 — superskrip komponen hilang pada definisi siklus homolog

**ID:** `FOM-U001-REV-P3-001`  
**Lokator pembaca:** baris 772–785, `#o012-fom-u001-def-011`  
**Lokator sumber:** baris 578–584

Definisi ini memakai $Z_n(X)$, $H_n(X)$, dan $B_n(X)$ tanpa pernah menyatakan
bahwa superskrip $\Delta$ sedang disingkat, padahal seluruh objek yang baru
didefinisikan adalah $Z_n^\Delta(X)$, $H_n^\Delta(X)$, dan $B_n^\Delta(X)$.
Konvensi indeks batasnya sendiri sudah benar: $z_1-z_2\in B_n$. Tambahkan
superskrip $\Delta$ secara konsisten atau deklarasikan singkatannya agar unit
tidak mencampur objek ini dengan homologi singular yang mulai pada baris 615.

### P3 — dua frasa id-ID perlu dinaturalkan

**ID:** `FOM-U001-REV-P3-002`  
**Lokator pembaca:** baris 176–178 dan 417–419

“Setiap muka $[v_0,\ldots,v_n]$” kehilangan kata **dari** dan terbaca seolah
$[v_0,\ldots,v_n]$ sendiri adalah muka; bentuk alami dan tepat ialah “Setiap
muka **dari** $[v_0,\ldots,v_n]$ ...”. Judul “dua bukan-contoh” juga tidak
alami; gunakan “dua noncontoh” atau “dua contoh yang bukan kompleks
simpleksial”. Keduanya mudah diperbaiki tanpa mengubah isi matematika.

## Pemeriksaan yang lulus

- **Bukti $\partial^2=0$:** lulus. Pembaca mulai dengan
  $\sigma\in C_n^\Delta(X)$, memisahkan penghapusan kedua menurut $j<i$ dan
  $j>i$, lalu memasangkan setiap $p<q$ dengan koefisien
  $(-1)^{p+q}$ dan $(-1)^{p+q-1}$. Indeks, domain, dan pembatalannya benar.
- **Konvensi batas:** lulus. Pembaca memakai
  $B_n^\Delta=\operatorname{im}\partial_{n+1}$,
  $B_n^\Delta\subseteq Z_n^\Delta$, dan
  $H_n^\Delta=Z_n^\Delta/B_n^\Delta$ secara bertipe benar. Definisi siklus
  homolog sekarang juga mempertahankan superskrip $\Delta$ pada ketiga grup.
- **Ekspresi batas segitiga:** lulus. Bentuk pembaca
  $e_0-e_1+e_2$ sama persis dalam grup abelian dengan bentuk sumber
  $e_2+e_0-e_1$; catatan audit tidak salah menganggap pengurutan ulang ini
  sebagai perubahan tanda.
- **Abelianisasi:** perbaikan $H^1\to H_1$, koefisien $\mathbb Z$,
  keterhubungan lintasan, dan titik dasar semuanya lulus. Pembaca final
  membedakan $H_1^{\mathrm{sing}}$ dari $H_1^\Delta$ dan menyatakan teorema
  pembandingan yang kelak menghubungkannya.
- **Diagram:** sepuluh kelompok semantik memuat 14 node sumber dengan pola
  `1+1+2+1+2+1+2+1+2+1=14`. Label, simpul, sisi, muka, arsiran yang berfungsi
  membedakan muka, dan diagram rantai tak berkonteks dipertahankan. Tidak ada
  aset eksternal. Semua arah yang bermakna kini dinyatakan langsung; tiga loop
  berarah konsisten, dan tidak tersisa frasa yang menyuruh pembaca memulihkan
  arah dari gambar sumber.
- **Alias sumber:** tepat lima nilai dipertahankan sebagai
  `data-source-label`: `def:sigma-complex`, `exmp:delta-complex-rp2`,
  `rem:order`, `def:simplicial-complex`, dan
  `lem:partial-partial-zero`.
- **Pengenal stabil:** Pandoc 3.9.0.2 merender 87 ID berawalan
  `o012-fom-u001`; semuanya unik. Delapan tautan fragmen internal teresolusi.
  `edition_unit_id=O012-FOM-001` tetap terpisah dari 30 unit Roberts dan
  `course_route_unit_id=D60-R08` benar.
- **Lapisan penguasaan:** tepat enam latihan, enam petunjuk, dan enam solusi
  dengan korespondensi ID satu-ke-satu. Semua solusi lengkap dan benar:
  koordinat barisentris, aksioma kompleks-$\Delta$, pembatalan batas segitiga,
  homologi lingkaran, homologi torus, dan kelas homolog torus telah dihitung
  tanpa kesalahan yang ditemukan.
- **Penutupan sumber:** semua 14 definisi, 14 catatan, 10 contoh, satu lema
  dengan bukti, satu akibat, 24 fungsi blok display, lima label, dan isi aktif
  baris 31–613 hadir. Baris 614 kosong; blok komentar 507–515 dan 586–608
  secara benar tidak dipromosikan menjadi isi pembaca.
- **Hak dan asal:** CC BY-SA 4.0, atribusi Yeheli Fomberg/Nir Lazarovich,
  pemberitahuan perubahan, non-endorsement, asal materi penguasaan, dan
  identifikasi model `OpenAI Codex gpt-5.6-sol, Ultra` semuanya dinyatakan.
  Tidak ditemukan materi problem bank, MIT, atau aset pihak ketiga yang
  masuk diam-diam.
- **Terminologi:** `bebas afin`, `pemetaan barisentris`, `simpleks`, `muka`,
  `simpul`, `kompleks-Delta`, `kompleks simpleksial`, `homologi simpleksial`,
  `rantai`, `pemetaan batas`, `batas`, `siklus`, `homolog`, `kelas homologi`,
  `homologi singular`, `citra`, dan `kernel` konsisten dengan ledger hidup yang
  diperiksa.

## Kesimpulan

Pada pembaca final SHA-256
`d9b64140f9340c75bc34c12bc02ee843d87de3566e331c50c2374075718aa2c6`, keenam
temuan pra-perbaikan benar-benar terselesaikan dan pemeriksaan penuh tidak
menemukan cacat baru. Putusan akhir ialah **PASS**, dengan
`P1=0`, `P2=0`, dan `P3=0`.
