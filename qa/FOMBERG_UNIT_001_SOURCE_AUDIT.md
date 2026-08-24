# Audit sumber Fomberg Unit 001 — §§1.1–1.2 / D60-R08

## Status dan ruang lingkup

Status audit: **`ADMISSIBLE_AFTER_REPAIR`**. Audit ini hanya membekukan dan
mencacah sumber; belum ada terjemahan, perubahan pembaca, perubahan backend,
atau perbaikan yang diterapkan. Semua butir di bagian *Temuan sumber dan
perbaikan yang diusulkan* membedakan teks sumber yang benar-benar ada dari
tindakan editorial yang baru diusulkan.

- `course_route_unit_id`: **`D60-R08`**.
- Unit komponen: **Fomberg Unit 001**, §§1.1–1.2, dari pengantar kompleks
  Delta sampai definisi siklus homolog.
- Rentang fisik sumber: `algebraic_topology.tex` baris **31–614**, inklusif.
- Baris 31 ialah `\section{Homology}`; baris 32 membuka §1.1
  `Delta-complexes`; baris 346 membuka §1.2 `Simplicial homology`.
- Baris 613 menutup catatan terakhir, baris 614 kosong, dan baris 615 membuka
  §1.3 `Singular homology`. Dengan demikian baris 615 tidak termasuk unit ini.
- Pada PDF baseline beku, isi unit mulai pada halaman fisik 3 dan berakhir di
  halaman fisik 8; §1.3 juga mulai pada halaman 8. Batas unit adalah batas
  sumber di dalam halaman, bukan batas potong halaman PDF.

## Otoritas byte

- Repositori resmi: `https://git.sr.ht/~yp/math-notes`.
- Commit: `563194fae879178b9a6871b249513bfc27968975`.
- Tree: `fb678966d1533d529bdd72f49d8496a3bdc14a9b`.
- Berkas: `authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/tree/algebraic_topology.tex`.
- Berkas lengkap: **223.886 byte**, **6.069 baris LF**, SHA-256
  `d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483`.
- Rentang 31–614: **584 baris**, **21.875 byte** dengan LF penutup baris 614
  dipertahankan, SHA-256
  `68cb0dea7aa24a42e979877a95acf61b8152c87ed86d88ad7deac7cb5cea2fe3`.
- Offset byte rentang dalam berkas lengkap: mulai **671**, berakhir **22.545**
  (inklusif). Berkas memakai LF murni; tidak ada CRLF.
- Manifest/build gate induk yang sudah lulus tetap
  `qa/FOMBERG_AUTHORITY_BUILD_GATE_QA.json`; hash rentang unit di atas dihitung
  ulang langsung dari berkas otoritas, bukan disalin dari manifest itu.

## Hak, atribusi, dan aset

- `LICENSE` pada tree beku ialah **CC BY-SA 4.0**, 20.140 byte, SHA-256
  `0b7fc2608b6d990314e908569407a6058b4a29175167c6d91ca0070c946661be`.
- `header.tex:62–69, 434–436` menyebut **Yeheli Fomberg** sebagai pencatat
  catatan dan `algebraic_topology.tex:5–6` menyebut materi berdasarkan kuliah
  **Nir Lazarovich**.
- `header.tex:100–108` memuat pemberitahuan bahwa catatan tidak didukung oleh
  para pengajar dan bahwa revisi/kesalahan menjadi tanggung jawab pencatat.
  Atribusi, pemberitahuan perubahan, ShareAlike, dan non-endorsement itu wajib
  dipertahankan pada turunan.
- Dalam baris 31–614 tidak ada `input`, `include`, `includegraphics`, gambar
  eksternal, atau sitasi. Keempat belas diagram adalah TeX/TikZ inline di
  dalam komponen berlisensi yang sama. Dependensi `header.tex` berada dalam
  tree resmi yang sama; overlay build CC0 bukan bagian dari prosa yang akan
  diterjemahkan.

## Sensus sintaks aktif

Komentar LaTeX dikeluarkan dari sensus objek aktif, tetapi tetap tercakup dalam
hash byte. Ada 513 baris aktif tak-kosong dan 32 baris yang seluruhnya komentar.

| Jenis | Jumlah |
|---|---:|
| Bagian / subbagian aktif | 1 / 2 |
| Definisi | 14 |
| Catatan (*remark*) | 14 |
| Contoh | 10 |
| Lema / korolari / bukti | 1 / 1 / 1 |
| Teorema / proposisi | 0 / 0 |
| Latihan atau pertanyaan formal | 0 |
| Daftar `enumerate` / butir | 2 / 5 |
| Blok matematika display | 24 |
| Diagram `tikzpicture` / inline `tikz` / `tikzcd` | 6 / 6 / 2 |
| Label / rujukan silang | 5 / 8 |
| Sitasi / berkas eksternal | 0 / 0 |

Komentar 507–515 memuat calon contoh RP2 yang belum jadi; komentar 586–608
memuat penanda “examples?” dan calon contoh torus yang belum jadi. Keduanya
bukan materi pembaca aktif dan tidak boleh dihitung sebagai contoh atau
latihan sumber.

## Inventaris objek semantik lengkap

### Definisi (14)

1. 52–56: vektor bebas afin.
2. 58–61: simpleks-$n$.
3. 70–76: simpleks-$n$ standar.
4. 85–93: pemetaan barisentris.
5. 95–102: muka simpleks.
6. 109–116: batas dan interior simpleks.
7. 118–134: struktur kompleks-Delta dengan tiga aksioma.
8. 286–295: kompleks simpleksial dengan dua syarat tambahan.
9. 347–360: grup rantai simpleksial melalui empat deskripsi ekuivalen.
10. 379–386: pemetaan batas.
11. 550–553: siklus.
12. 555–558: batas sebagai citra pemetaan batas.
13. 566–570: homologi.
14. 578–584: siklus homolog dan kelas homologi.

### Catatan (14)

- 48–50: interpretasi elemen `pi_n`;
- 77–83: parametrikasi semua simpleks oleh simpleks standar;
- 103–107: dimensi dan urutan muka;
- 136–144: rumus restriksi muka dalam aksioma kompleks-Delta;
- 146–151: notasi `Delta_n` bagi himpunan simpleks berdimensi $n$;
- 172–181: struktur diskret patologis pada lingkaran;
- 263–278: urutan/orientasi muka pada contoh RP2;
- 280–284: ruang ditentukan oleh data kompleks-Delta;
- 336–338: hubungan dengan graf sederhana;
- 340–344: struktur kompleks-Delta diskret pada sembarang himpunan;
- 362–364: elemen grup rantai disebut rantai-$n$;
- 388–390: pemetaan batas merupakan homomorfisma;
- 497–505: tanda orientasi pada batas muka torus;
- 610–613: hubungan homologi derajat satu dengan abelianisasi grup
  fundamental.

### Contoh (10)

- 63–68: simpleks dimensi 0–3;
- 153–170: kompleks-Delta lingkaran;
- 183–214: triangulasi torus;
- 216–261: kompleks-Delta RP2 dan model hasil baginya;
- 297–309: segitiga sebagai kompleks simpleksial;
- 311–334: dua kompleks-Delta yang bukan kompleks simpleksial;
- 366–377: grup rantai pada lingkaran;
- 392–430: batas sisi dan segitiga berorientasi;
- 432–448: pemetaan batas lingkaran bernilai nol;
- 450–496: kompleks rantai dan batas pada torus.

### Hasil dan bukti

- Lema 517–520 (`lem:partial-partial-zero`):
  `partial_(n-1) compose partial_n = 0`.
- Bukti 521–548: bukti sumber ada, tetapi formula indeksnya tidak sah; lihat
  `FOM-U001-PR-001` di bawah.
- Korolari 560–564: inklusi batas ke siklus, tetapi indeks sumber salah; lihat
  `FOM-U001-SRC-010`.
- Tidak ada latihan, petunjuk, jawaban, atau solusi sumber. Lapisan penguasaan
  D60-R08 karena itu harus ditulis tersendiri kelak dan tetap dilabeli sebagai
  materi asli, bukan diperlakukan sebagai terjemahan Fomberg.

## Inventaris matematika display lengkap (24)

| Baris | Isi/fungsi |
|---|---|
| 35–37 | skema ruang topologis ke data aljabar |
| 40–42 | `X mapsto pi_0(X)` |
| 44–47 | `(X,x_0) mapsto pi_1(X,x_0)` |
| 73–75 | definisi simpleks standar |
| 80–82 | parametrikasi barisentris |
| 90–92 | rumus pemetaan barisentris |
| 97–100 | identitas muka dengan satu verteks dihapus |
| 139–142 | komposisi pemetaan karakteristik dengan muka |
| 164–167 | pemetaan verteks dan sisi untuk lingkaran |
| 219–254 | dua model diagramatik RP2 dalam satu display |
| 314–328 | dua noncontoh kompleks simpleksial |
| 352–359 | empat deskripsi grup rantai bebas |
| 382–384 | formula batas berselang-seling |
| 394–415 | diagram sisi dan simpleks-2 berorientasi |
| 417–419 | batas sisi |
| 421–426 | batas simpleks-2; sisi kiri sumber salah tulis |
| 444–446 | perhitungan batas rantai lingkaran |
| 479–484 | kompleks rantai torus |
| 486–490 | nilai `partial_1` pada tiga sisi torus |
| 492–495 | nilai `partial_2` pada dua muka torus |
| 526–528 | formula batas dalam bukti lema |
| 531–540 | ekspansi batas-ganda sumber |
| 542–547 | klaim pembatalan pasangan sumber |
| 571–577 | diagram grup rantai tanpa konteks |

Rumus inline tetap berada dalam objek induknya dan tercakup byte demi byte oleh
hash rentang. “24” di atas berarti blok display aktif, bukan jumlah seluruh
fragmen matematika inline atau node berlabel di dalam TikZ.

## Inventaris diagram lengkap (14)

- `tikzpicture`: 157–161 (lingkaran), 186–209 (torus), 300–307
  (segitiga), 369–373 (lingkaran/rantai), 435–439 (lingkaran/batas), dan
  453–476 (torus/batas).
- Inline `tikz`: 220–243 dan 244–253 (dua model RP2), 315–319 dan
  320–327 (dua noncontoh), serta 395–400 dan 401–414 (sisi dan simpleks-2).
- `tikzcd`: 479–484 (kompleks rantai torus) dan 571–577 (diagram rantai
  tak berkonteks).

Tidak ada raster, SVG, PDF gambar, atau URL aset. Saat reflow, orientasi panah,
label verteks/sisi/muka, pola dua simpleks, dan korespondensi dengan formula
batas adalah data matematika dan tidak boleh diganti oleh kotak dekoratif.

## Label dan rujukan silang lengkap

| Label | Baris definisi | Rujukan aktif |
|---|---:|---|
| `def:sigma-complex` | 119 | 137, 176, 269 |
| `exmp:delta-complex-rp2` | 217 | 265 |
| `rem:order` | 264 | 502 |
| `def:simplicial-complex` | 287 | 330, 332 |
| `lem:partial-partial-zero` | 518 | 561 |

Kelima label teresolusi di dalam unit; tidak ada rujukan keluar, label
persamaan, `cite`, atau bibliografi pada rentang ini. Label sumber harus tetap
punya alias stabil meskipun ID semantik edisi nanti lebih deskriptif.

## Temuan sumber dan perbaikan yang diusulkan

Kolom kedua selalu menyatakan **fakta sumber**. Kolom ketiga hanya menyatakan
**perbaikan yang diusulkan**; belum ada satu pun yang diterapkan oleh audit ini.

| ID | Fakta sumber | Perbaikan yang diusulkan |
|---|---|---|
| `FOM-U001-SRC-001` | 48–50 menyebut elemen `pi_n` sebagai pemetaan dari sfera. | Untuk $n\geq1$, nyatakan elemen sebagai kelas homotopi berbasis dari pemetaan berbasis $(S^n,s_0)\to(X,x_0)$; jangan hilangkan titik dasar atau relasi homotopi. |
| `FOM-U001-SRC-002` | 52–60 mendefinisikan bebas afin di $R^n$, lalu simpleks-$n$ di $R^m$. | Gunakan $v_0,\ldots,v_n\in R^m$ dengan $n\leq m$ secara konsisten. |
| `FOM-U001-SRC-003` | 74 menulis `[e_0,...,e_N]`; `N` tidak didefinisikan. | Ganti menjadi `[e_0,...,e_n]` dan normalkan satu simbol `Delta^n`. |
| `FOM-U001-SRC-004` | 87 memakai `mapsto` sebagai panah tipe pada `b: Delta^n mapsto [...]`. | Gunakan `to`; pertahankan `mapsto` hanya untuk aturan nilai elemen. |
| `FOM-U001-SRC-005` | 95–101 menyebut muka `[v_1,...,v_n]`, menghapus indeks $1\leq i\leq n$, tetapi kemudian menyebut hasil sebagai muka simpleks-$n$. | Mulai dari `[v_0,...,v_n]` dan izinkan $0\leq i\leq n$; hasilnya simpleks-$(n-1)$. |
| `FOM-U001-SRC-006` | 172–180 memakai kardinal tak ditentukan `aleph` dan akhirnya menyebut struktur diskret sebagai “Delta-simplex”, bukan struktur kompleks-Delta. | Tulis “satu simpleks-0 untuk setiap titik” dan “struktur kompleks-Delta pada topologi diskret”. |
| `FOM-U001-SRC-007` | Judul contoh 183 mengatakan `T^1`, sedangkan 184 mendefinisikan $S^1\times S^1$. | Gunakan $T^2$ secara konsisten. |
| `FOM-U001-SRC-008` | 218 menulis hasil bagi `D^2/forall x in S^1 : x sim -x`, yang bukan notasi relasi hasil bagi yang terbentuk baik. | Tulis $D^2/(x\sim -x\text{ untuk setiap }x\in S^1)$. |
| `FOM-U001-SRC-009` | 347–360 mendefinisikan $C_n^Delta$ hanya untuk $n\geq1$, tetapi 375 dan sesudahnya memakai $C_0$; indeks pada tanda jumlah langsung juga implisit. | Definisikan $C_n^Delta$ untuk $n\geq0$, tulis indeks basis/jumlah langsung eksplisit, dan nyatakan $partial_0=0$. |
| `FOM-U001-SRC-010` | 422 menulis `sigma(sigma)` untuk batas simpleks; 443–447 mengganti `partial_1` dengan `sigma_1` dan menulis `a in Z` tanpa makro himpunan bilangan bulat. | Gunakan `partial(sigma)`/`partial_2(sigma)`, `partial_1(ae)=a partial_1(e)`, dan `a in mathbb Z`. |
| `FOM-U001-SRC-011` | 497–504 mengatakan restriksi pemetaan karakteristik $V$ ke muka “sama dengan $-g$”. Negatif bukan pemetaan topologis; ia adalah koefisien rantai berorientasi. | Nyatakan restriksi sebagai $g$ yang orientasi terinduksinya berlawanan, sehingga kontribusinya pada rantai batas ialah $-g$. |
| `FOM-U001-PR-001` | Bukti 521–548 mengambil `sigma in C_(n+1)` tetapi menerapkan `partial_n` dan memetakan simpleks dengan verteks $v_0,...,v_n$; 536–546 menghapus `v_j` dua kali, kehilangan jumlah luar, dan tidak memberi pasangan indeks yang sah. Bukti yang tercetak tidak membuktikan lema. | Ganti dengan bukti lengkap untuk `sigma in C_n`: kelompokkan dua cara menghapus setiap pasangan $i<j$; koefisiennya $(-1)^{i+j-1}+(-1)^{i+j}=0$. Tandai sebagai perbaikan bukti asli edisi, bukan terjemahan literal. |
| `FOM-U001-SRC-012` | 555–568 mendefinisikan $B_n=im partial_n$, lalu menyatakan $B_{n+1}\subseteq Z_n$ dan $H_n=Z_n/B_{n+1}$; 582 justru memakai konvensi standar $B_n$. | Tetapkan $B_n=im partial_{n+1}$, kemudian $B_n\subseteq Z_n$ dan $H_n=Z_n/B_n$ di seluruh unit. |
| `FOM-U001-SRC-013` | Diagram 571–577 (`0, Z, Z^3, Z^3, 0`) tidak menyebut ruang, basis, atau matriks, dan tidak tersambung oleh prosa. | Jangan menebak contoh yang dimaksud. Pertahankan sebagai skema sumber yang ditandai tak berkonteks atau beri konteks editorial yang dapat dibuktikan dari data unit; rekam keputusan itu sebagai koreksi. |
| `FOM-U001-SRC-014` | 610–612 menyatakan $H^1(X)$ adalah abelianisasi $pi_1(X)$ tanpa hipotesis keterhubungan atau titik dasar. | Untuk kompleks-Delta terhubung-lintasan dan $x_0\in X$, tulis $H_1^Delta(X;Z)\cong pi_1(X,x_0)_ab$; bedakan ini dari $H^1$. Beri bukti/rujukan internal ketika jembatan singular tersedia. |
| `FOM-U001-SRC-015` | 497–500 menyebut suatu muka sebagai citra simpleks-2, sehingga pemetaan karakteristik $V$ bertipe dua dimensi tercampur dengan pembatasan-pembatasan mukanya yang berdomain simpleks-1. | Nyatakan bahwa $V$ mempunyai domain $[v_0,v_1,v_2]$ dan bahwa muka-mukanya ialah pembatasan $V$ pada $[v_0,v_1]$, $[v_1,v_2]$, dan $[v_0,v_2]$; kemudian pisahkan lagi tanda rantai dari pemetaan muka. |
| `FOM-U001-COPY-001` | Salah tulis/prosa rusak muncul pada 43 (`it`/`say`), 52 (`Affinitely`), 67 (`tetraeder`), 154 (kata kerja hilang), 263 (`Orienatation`), 271 (`sigma complex`), 273 (`are order`), 282 (frasa terpotong), 337 (`graphes`), 427 (`have do`), dan 583 (`somtimes`). | Normalisasi ejaan dan tata bahasa dalam bahasa Indonesia tanpa mengubah objek matematikanya; simpan locator ini dalam ledger koreksi. |

Temuan yang paling berisiko ialah `FOM-U001-PR-001`,
`FOM-U001-SRC-012`, `FOM-U001-SRC-014`, dan `FOM-U001-SRC-015`: keempatnya
mengubah kebenaran atau tipe objek matematika, bukan sekadar gaya. Korolari 560–564 mempunyai
justifikasi langsung setelah indeks diperbaiki; tidak ada “bukti hilang” lain
yang bernama theorem/proposition dalam rentang ini. Klaim abelianisasi memang
menjanjikan penjelasan “later”, tetapi sumber beku hanya mengulang klaim itu
kemudian; unit ini tidak menyediakan buktinya.

## Risiko terminologi id-ID

Audit ini tidak mengubah glosarium. Kandidat berikut harus diselaraskan dengan
backend Roberts yang sudah hidup sebelum terjemahan:

- `simplex` -> **simpleks**, `simplicial` -> **simpleksial**, dan `standard
  n-simplex` -> **simpleks-$n$ standar** sudah konsisten dengan terminologi
  lane.
- `edge` sudah dibekukan sebagai **sisi**. Karena itu `face` sebaiknya
  **muka**, bukan “sisi”, agar sisi berdimensi satu tidak bertabrakan dengan
  muka kodimensi satu.
- `chain` -> **rantai**, `chain complex` -> **kompleks rantai**; jangan pakai
  *korantai*, yang sudah dikhususkan untuk `cochain`.
- `boundary` -> **batas** selaras dengan `coboundary` -> **kobatas**; konteks
  harus membedakan subruang topologis `partial Delta^n`, pemetaan batas, dan
  subgrup batas.
- `barycentric` -> **barisentris** mengikuti terminologi lane; `affinely
  independent` memerlukan bentuk konsisten **bebas afin**.
- `cycle`, `homologous`, dan `homology class` sebaiknya masing-masing
  **siklus**, **homolog**, dan **kelas homologi**. Jangan menerjemahkan
  `image` sebagai “bayangan”: lane memakai **citra**; `kernel` tetap
  **kernel**.
- `orientation` harus **orientasi**, bukan sekadar “arah”, karena tandanya
  merupakan koefisien rantai. `vertex` perlu dibekukan sebagai **verteks** dan
  tidak dicampur dengan “titik sudut” di dalam satu unit.
- `Delta-complex` dan `Delta-set` adalah objek berbeda. Gunakan
  **kompleks-Delta** di unit ini dan pertahankan **himpunan-Delta** untuk objek
  semisimpleksial Roberts.

## Putusan dan kursor

Rentang 31–614 merupakan unit kontigu yang sah secara hak dan tertutup secara
struktur, tetapi **tidak boleh diterjemahkan secara literal tanpa dossier
perbaikan di atas**. Kursor sumber sesudah unit ialah baris **615**, tepat pada
`\subsection{Singular homology}`. Langkah produksi berikutnya dapat menerjemahkan
Fomberg Unit 001/D60-R08 setelah setiap temuan berisiko tinggi diberi status
perbaikan eksplisit, seluruh 14 diagram direflow tanpa kehilangan orientasi,
dan enam masalah penguasaan dengan petunjuk serta solusi lengkap dibuat sebagai
lapisan asli yang terpisah.
