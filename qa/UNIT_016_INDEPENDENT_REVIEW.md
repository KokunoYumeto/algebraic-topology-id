# Tinjauan independen Unit 16

Tanggal tinjauan: 22 Agustus 2026  
Status: **LULUS; P1 = 0, P2 = 0, P3 = 0 yang masih terbuka**

## Identitas beku dan ruang lingkup

- Sumber: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`, baris 3287--3383 inklusif. Baris 3384, penanda Kuliah 17, tidak termasuk.
- Commit hulu: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- `Notes.tex`: 331.447 byte; 6.368 baris; SHA-256 `cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7`.
- Audit sumber pengendali: `qa/UNIT_016_SOURCE_AUDIT.md`; 5.898 byte; 108 baris; SHA-256 `52476eb5e239fa4d752b8a9f533c8bc00b442fe27e5b5fe48925dc9b6eb3a288`.
- Unit yang ditinjau: `source/id-ID/units/unit-016-lecture-016.md`.
- Unit final: **33.863 byte; 984 baris; SHA-256 `6a89d6e02de654c98294a5f6f092bb76bd63f6d537e358a49bcdac25adb8da55`**.

Tinjauan ini membandingkan seluruh unit, klaim demi klaim dan rumus demi rumus,
dengan tepat 97 baris sumber tersebut serta setiap kewajiban pada audit sumber.
Tidak ada materi Kuliah 17 yang masuk dan tidak ada bagian Kuliah 16 yang hilang.

## Penutupan sumber

Sensus sumber tertutup lengkap: penanda Kuliah 16; satu definisi aksi serat demi
serat; satu proposisi hasil bagi ruang penutup beserta bukti; satu lema
ekuivariansi yang pada sumber hanya diberi kata `Exercise`; inventaris dua
masalah; konstruksi ruang kelas lintasan; proposisi penutup universal beserta
bukti; dan proposisi surjektivitas esensial. Kedua segitiga Xy-pic, empat catatan
pinggir, trivialiasi lokal, tindakan grup, serta tampilan funktor terakhir
semuanya mempunyai pengganti semantik dalam urutan bacaan.

Urutan matematis sumber dipertahankan. Perubahan urutan lokal hanya terjadi bila
diperlukan untuk mengganti argumen topologis sumber yang tidak sah dengan bukti
basis penutup: identifikasi serat sebagai hom-set grupoid dinyatakan lebih dahulu,
diskretnya serat kemudian dibuktikan dari lembar lokal. Catatan sumber yang
menunda pembuktian ke Hatcher tetap dicatat, tetapi penjelasan edisi berdiri
sendiri dan tidak mengandalkan hasil yang ditunda itu.

## Topologi basis penutup

Konstruksi menggunakan himpunan kelas homotopi lintasan dengan titik ujung tetap
dan secara eksplisit **mendefinisikan** topologinya dengan basis

\[
U_{[\gamma]}=\{[\gamma\#\eta]:\eta\text{ lintasan di }U,
\ \eta(0)=\gamma(1)\}.
\]

Lingkungan `U` disyaratkan terbuka, terhubung lintasan, dan mempunyai citra
fundamental trivial di `X`. Unit membuktikan kedua aksioma basis, bijektivitas dan
keterbukaan setiap pembatasan `p|_{U_a}`, kontinuitas `p`, partisi
`p^{-1}(U)` menjadi lembar, serta trivialiasi bertipe lengkap. Tidak ada pemilih
lintasan yang diasumsikan berubah kontinu. Peta dari ruang lintasan ditampilkan
hanya pada tingkat himpunan dan unit secara eksplisit tidak mengklaim bahwa
topologi basis sama dengan topologi hasil bagi kompak-terbuka.

Metode ini memenuhi tepat kewajiban basis penutup bergaya Hatcher pada audit
sumber, tetapi seluruh pemaparan pembuktiannya berupa prosa Indonesia mandiri.
Tidak ada kalimat Inggris, gambar, atau ekspresi prosa Hatcher yang disalin; pranala
ke sumber resmi berfungsi sebagai atribusi atas rujukan yang disebut Roberts.

## Handedness, koset, dan dua aksi

Semua rumus konsisten dengan konkatenasi kronologis:

- monodromi langsung adalah aksi kanan
  `[gamma] . [eta] = [gamma # eta]`;
- tindakan penutup universal adalah aksi kiri serat demi serat
  `h . [gamma] = [omega # gamma]`, untuk `h=[omega]`;
- kedua tindakan berbeda dan dibuktikan komutatif;
- hasil bagi oleh aksi kiri `H` ditulis `H\backslash\widetilde X`, dengan serat
  bertitik `H\backslash G`, yaitu ruang koset kanan;
- tindakan turun adalah `(Hg) . k = H(gk)`;
- peta hasil bagi pada serat dibuktikan ekuivarian terhadap transpor kanan.

Tidak ditemukan peralihan tersembunyi ke aksi kiri monodromi atau ke `G/H`.
Tanda `G/H` hanya muncul dalam penjelasan eksplisit tentang bentuk sumber yang
dikoreksi. Aksi prefiks kiri tidak dipakai sebagai penstabil aksi sufiks kanan.

## Verifikasi seluruh perbaikan dan bukti

Proposisi hasil bagi memperlakukan grup sebagai diskret, memperhalus ke
lingkungan terhubung lintasan yang diliputi merata, membuktikan bahwa setiap
elemen grup mempermutasikan lembar utuh, membuktikan keterbukaan peta hasil bagi,
dan memperoleh model lokal `U\times(K\backslash F)`. Jadi identifikasi pembatasan/hasil bagi
tidak lagi diserahkan kepada tugas eksternal.

Lema ekuivariansi membuktikan latihan sumber langsung dari keunikan pengangkatan.
Proposisi penutup universal membuktikan, dalam urutan lengkap, aksioma basis,
lembar lokal, keterhubungan lintasan, kontinuitas dan kebebasan aksi kiri,
komutasi dengan monodromi kanan, serta keterhubungan sederhana. Bukti terakhir
mengonstruksi pengangkatan `t -> [alpha_t]`, menunjukkan citra `p_*` trivial
melalui kriteria pengangkatan tertutup, lalu memakai injektivitas `p_*`; ia tidak
mengulang kekeliruan sumber yang menyamakan tindakan kiri dan penstabil kanan.

Untuk subgrup `H`, unit membuktikan

\[
(p_H)_*\pi_1(H\backslash\widetilde X,H[c_{x_0}])=H
\leq\pi_1(X,x_0),
\]

sementara `pi_1(\widetilde X,[c_{x_0}])=1`. Dengan demikian, persamaan salah
`pi_1(X^(1),*)=H` tidak diwariskan.

Surjektivitas esensial juga tidak dibiarkan sebagai frasa “bekerja mundur”. Unit
menguraikan suatu himpunan-`G` kanan menjadi orbit, memilih penstabil `H_i`,
membangun koproduk `H_i\backslash\widetilde X`, dan membuktikan pemetaan
`H_i g -> s_i . g` terdefinisi baik, bijektif, dan ekuivarian kanan. Rumus
perluasan melalui transpor lintasan bertipe benar; pemeriksaan perubahan pilihan
lintasan dan naturalitasnya memakai urutan komposisi kronologis yang tepat.
Konstruksi kemudian diulangi secara independen pada setiap komponen lintasan
terbuka. Catatan batas hasil menyatakan dengan benar bahwa kepenuhan, kesetiaan,
dan ekuivalensi kategori belum dibuktikan pada Unit 16.

## Pendamping penguasaan

Enam pemeriksaan penguasaan mempunyai enam solusi lengkap dan cocok satu-ke-satu:

1. hasil bagi lokal suatu ruang penutup;
2. komutasi aksi kiri hasil bagi dan monodromi kanan;
3. aksioma basis, partisi lembar, dan homeomorfisme lokal tanpa pemilih lintasan;
4. rumus pengangkatan serta keterhubungan lintasan dan sederhana;
5. realisasi subgrup dan citra `p_H*`;
6. realisasi orbit demi orbit dan komponen demi komponen.

Semua enam soal ditandai `data-origin="edition-original"`. Solusinya tidak memakai
klasifikasi transformasi dek, kepenuhan, atau kesetiaan dari kuliah kemudian.
Perhitungan koset pada Solusi 16.6 benar untuk aksi kanan: kesamaan nilai memberi
`g'g^{-1} in H_i`, sehingga `H_i g'=H_i g`.

## Aksesibilitas, bahasa, dan asal-usul

Kedua Xy-pic direflow menjadi Diagram 16.1--16.2 dengan inventaris linear semua
objek, panah, dan persamaan komutativitas. Tidak ada SVG, bitmap, warna, atau
penempatan dua dimensi yang diperlukan untuk memahami relasi. Keempat catatan
pinggir masuk ke prosa utama: segitiga hasil bagi, singkatan lintasan konstan,
catatan Hatcher/bukti tertunda, dan lintasan `s -> (t -> gamma(st))`.

Bahasa Indonesia dibaca alami dan konsisten dengan terminologi unit-unit
sebelumnya. Pencarian terbatas tidak menemukan kebocoran prosa Inggris; kata
`Exercise`, `equvariant`, dan `path lifing` hanya muncul sebagai kutipan singkat
atas bentuk sumber yang sedang ditutup atau dikoreksi. Tidak ada sebutan nama
payung proyek.
Atribusi Roberts, CC BY 4.0, perubahan edisi, asal materi penguasaan, dan
non-endorsement dinyatakan eksplisit. Tidak ada materi pihak ketiga yang tidak
diatribusikan atau aset eksternal yang diimpor.

## Validasi mekanis

- 33 pengenal stabil didefinisikan dan semuanya unik; Pandoc memancarkan tepat
  33 ID tersebut tanpa duplikasi.
- 20 fenced-div pembuka dan 20 penutup; seimbang.
- 63 pasangan delimiter matematika tampil `$$`; seimbang.
- 6 pemeriksaan penguasaan, 6 solusi, dan 6 tag asal edisi; lengkap satu-ke-satu.
- HTML semantik memuat 507 elemen MathML, tanpa SVG atau gambar.
- Pandoc 3.9.0.2, Markdown ke native dengan `--fail-if-warnings`: exit 0.
- Pandoc 3.9.0.2, HTML5 mandiri dengan MathML, `--section-divs`, dan
  `--fail-if-warnings`: exit 0.
- Pencarian terbatas menemukan nol `xymatrix`, `marginnote`, atau `lecturenum`
  yang tersisa.

## Disposisi akhir

Tidak ditemukan cacat matematis, logis, struktural, bahasa, aksesibilitas,
provenans, atau build yang masih terbuka. **P1 = 0, P2 = 0, P3 = 0.** Unit 16
layak dibekukan pada identitas berkas di atas.
