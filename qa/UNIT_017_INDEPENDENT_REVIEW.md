# Tinjauan independen Unit 17

Tanggal tinjauan: 22 Agustus 2026  
Status: **LULUS; P1 = 0, P2 = 0, P3 = 0 yang masih terbuka**

## Identitas beku dan batas tinjauan

- Sumber: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`, baris 3384--3481 inklusif. Baris 3482, penanda Kuliah 18, tidak termasuk.
- Commit hulu: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- `Notes.tex`: 331.447 byte; 6.368 baris; SHA-256 `cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7`.
- Audit sumber pengendali: `qa/UNIT_017_SOURCE_AUDIT.md`; 12.303 byte; 237 baris; SHA-256 `31d984a617844f664bb7ddf35037d6b7f33041f08230c29cbcd301680e9566ce`.
- Batas ledger hidup yang dipakai: `O012-ADV-0227` dan `O012-TERM-0240`.
- Unit yang ditinjau: `source/id-ID/units/unit-017-lecture-017.md`.
- Unit final: **29.921 byte; 952 baris; SHA-256 `713e8b44b22620d9dd0531e19316932a1f18b1109fea80d7787cad218e4e45f9`**.

Tinjauan membandingkan seluruh 98 baris sumber dengan seluruh unit, klaim demi
klaim dan rumus demi rumus, lalu memeriksa dua belas kewajiban perbaikan pada
audit sumber. Tidak ada materi Kuliah 18 yang masuk dan tidak ada materi Kuliah
17 yang hilang.

## Penutupan sumber dan urutan semantik

Sensus sumber tertutup lengkap: dua lema, satu akibat, satu teorema, satu
definisi, satu contoh, satu proposisi, tiga bukti formal sumber, satu sketsa
kepenuhan yang semula belum lengkap, tiga tampilan matematika, satu `align*`
berisi dua operasi potongan, tiga catatan pinggir, serta judul bagian grup
homotopi lebih tinggi. Pertanyaan tentang bentuk `pi_n` dipertahankan sebagai
pertanyaan retoris, bukan diubah menjadi latihan sumber.

Lema keunikan, akibat kesetiaan, teorema klasifikasi, definisi `pi_n`, model
sfera/kubus/cakram, adjungsi loop, konstruksi grup, argumen Eckmann--Hilton,
contoh grup topologis, kedua konkatenasi loop ganda, dan proposisi komutativitas
semuanya hadir dalam urutan sumber. Tambahan bukti dan pemeriksaan penguasaan
ditandai sebagai materi edisi, bukan disamarkan sebagai teks Roberts.

## Ruang penutup: tipe, komponen, dan kepenuhan

Lema 17.1 memakai persamaan bertipe benar

\[
\pi\circ f=p=\pi\circ g,
\]

dan bukti mengevaluasi `g(gamma(0))`, bukan ekspresi sumber yang tidak
terdefinisi. Keunikan pengangkatan diterapkan tepat pada domain yang terhubung
lintasan.

Bukti kesetiaan memisahkan setiap komponen lintasan ruang total sumber. Ia
memakai hasil Unit 15 bahwa setiap komponen memetakan surjektif ke basis yang
terhubung lintasan, memilih satu titik komponen di atas `x_0`, lalu menerapkan
lema keunikan pada pembatasan kedua peta. Basis yang tidak terhubung ditangani
komponen demi komponen. Notasi pembatasan serat selalu memakai `x_0` dan semua
peta mempunyai domain serta kodomain yang benar.

Bukti kepenuhan sekarang lengkap. Dari transformasi natural
`eta: rho_1 => rho_2`, unit mendefinisikan `F(z)=eta_x(z)` pada serat di atas
`x`; ini langsung memberi `pi_2 F=pi_1`. Untuk kontinuitas, unit memilih satu
lingkungan terbuka terhubung lintasan yang diliputi merata oleh kedua penutup,
menandai lembar dengan serat `A_i`, dan memakai naturalitas transpor untuk
mendapat rumus lokal

\[
\tau_2F\tau_1^{-1}(u,a)=(u,\eta_x(a)).
\]

Rumus itu identitas pada faktor terbuka dan fungsi tetap pada koordinat diskret,
sehingga kontinu. Lingkungan tersebut menutupi basis; jadi `F` kontinu global,
terletak di atas `X`, dan menginduksi tepat `eta`. Keunikan dan kesimpulan penuh,
setia, serta surjektif secara esensial semuanya dinyatakan tanpa lompatan.

## Konvensi aksi

Monodromi langsung tetap aksi kanan:

\[
(z\cdot g)\cdot h=z\cdot(gh),
\qquad
\varphi(z\cdot g)=\varphi(z)\cdot g.
\]

Komponen titik basis dari transformasi natural ditulis sebagai morfisme
`Set_G` kanan. Unit secara eksplisit membedakannya dari (1) notasi kiri yang
diperoleh dengan invers dan (2) aksi kiri serat demi serat Unit 16 yang memakai
prefiks untuk membentuk `H\backslash\widetilde X`. Tidak ada koset atau aksi
kiri baru dalam pembuktian kepenuhan dan tidak ditemukan pembalikan urutan
konkatenasi.

## Rentang `n`, model relatif, dan struktur grup

Definisi membedakan semua rentang yang diperlukan:

- untuk `n >= 0`, `pi_n(X,x)=[(S^n,1),(X,x)]_*` adalah himpunan bertitik;
- untuk `n >= 1`, model `I^n/partial I^n` dan `D^n/partial D^n`, adjungsi loop,
  dan struktur grup berlaku;
- untuk `n = 0`, unit menjelaskan bahwa `I^0` dan `D^0` hanya satu titik dengan
  batas kosong, sehingga hasil baginya bukan `S^0`;
- untuk `n >= 2`, argumen dua koordinat membuktikan komutativitas.

Notasi berbasis `pi_0(X,x)` berfungsi sebagai himpunan komponen lintasan bertitik;
ia tidak dipakai untuk mengklaim struktur grup. Semua tiga syarat homotopi relatif
dituliskan. Proses currying `f(u,t) -> (u -> (t -> f(u,t)))` bertipe benar dan
memberi `pi_n(X,x) ~= pi_{n-1}(Omega_x X,c_x)` tepat untuk `n >= 1`.

Operasi grup pada kelas kubus menggunakan konkatenasi kronologis koordinat
terakhir. Kedua cabang bertemu pada nilai `x`, operasi turun ke homotopi relatif,
kelas konstan menjadi unit, pembalikan koordinat memberi invers, dan
reparametrisasi memberi asosiativitas pada kelas. Postkomposisi mempertahankan
operasi, sehingga funktor ke `Grp` hanya diklaim untuk `n >= 1`.

## Eckmann--Hilton dan loop teriterasi

Lema 17.2 memperbaiki kesimpulan sumber secara tepat. Dua operasi berunit dengan
hukum pertukaran dibuktikan mempunyai unit yang sama, berimpit, asosiatif, dan
komutatif; kesimpulan tanpa hipotesis tambahan adalah **monoid komutatif**.
Kontracontoh `Z_{>=0}` dengan penjumlahan memenuhi semua hipotesis tetapi tidak
mempunyai invers aditif bagi unsur positif. Grup abelian baru disimpulkan bila
invers sudah tersedia secara terpisah.

Contoh grup topologis menerapkan lema pada kelas loop, bukan pada loop mentah.
Perkalian titik demi titik dan konkatenasi memenuhi identitas pertukaran secara
potongan; kelas loop konstan adalah unit bersama dan invers berasal dari
pembalikan loop dalam struktur konkatenasi. Pernyataan berlaku untuk semua grup
topologis, tidak hanya grup Lie.

Pada loop ganda, kedua operasi ditulis benar:

\[
(f_1\#_2f_2)(s,t)=
\begin{cases}
f_1(s,2t),&t\leq\tfrac12,\\
f_2(s,2t-1),&t\geq\tfrac12.
\end{cases}
\]

Cabang kedua memakai `f_2`, bukan pengulangan `f_1` pada sumber. Kedua jahitan,
syarat batas, dan kontinuitas melalui lema penempelan diperiksa. Inventaris empat
kuadran menghasilkan identitas pertukaran mentah yang benar. Unit kemudian
menegaskan bahwa unit dan asosiativitas konkatenasi mentah hanya berlaku hingga
homotopi, sehingga Eckmann--Hilton diterapkan sesudah kedua operasi turun ke
kelas. Identifikasi

\[
\pi_n(X,x)\cong\pi_{n-2}(\Omega_x^2X,c_{c_x})
\]

dipakai untuk setiap `n >= 2`; operasi koordinat kedua adalah hukum grup yang
sudah dibangun, dan pembalikan koordinat menyediakan invers. Deduksi bahwa
`pi_n` abelian lengkap dan tidak meminta invers dari lema Eckmann--Hilton.

## Enam pemeriksaan penguasaan

Enam pemeriksaan mempunyai enam solusi lengkap dan cocok satu-ke-satu:

1. keunikan pengangkatan dan kesetiaan komponen demi komponen;
2. konstruksi peta penuh, kontinuitas lokal, dan ekuivariansi kanan;
3. korespondensi sfera/kubus/cakram, seluruh syarat relatif, dan pengecualian
   `n = 0`;
4. teorema Eckmann--Hilton yang benar serta kontracontoh tanpa invers;
5. jahitan, batas, empat kuadran, dan alasan bekerja pada kelas homotopi;
6. komutativitas `pi_1` grup topologis dan `pi_n` untuk `n >= 2`, dengan asal
   invers dinyatakan pada kedua penerapan.

Semua enam soal ditandai `data-origin="edition-original"`. Tidak ada solusi yang
memakai materi Kuliah 18 atau hasil yang belum dibuktikan.

## Aksesibilitas, bahasa, terminologi, dan asal-usul

Ketiga catatan pinggir masuk ke urutan bacaan: dua invarian komponen dimensi
rendah, definisi `Y/A`, dan perluasan dari grup Lie ke grup topologis. Tampilan
operasi grup yang panjang direflow menjadi `aligned`; kedua operasi loop ganda
diberi uraian jahitan dan daftar linear empat kuadran. Tidak ada gambar, SVG,
warna, atau posisi dua dimensi yang dibutuhkan untuk memahami matematika.

Bahasa Indonesia alami dan konsisten. Pencarian terbatas tidak menemukan
kebocoran prosa Inggris; bentuk sumber yang salah hanya disebut singkat ketika
menjelaskan koreksi. Atribusi Roberts, CC BY 4.0, perubahan edisi, asal materi
penguasaan, dan non-endorsement dinyatakan eksplisit. Tidak ada aset eksternal
atau materi pihak ketiga yang diimpor.

Ledger terminologi hidup berakhir tepat pada `O012-TERM-0240`. Sebelas istilah
provisional audit Unit 17 tidak mempunyai padanan yang sudah terdaftar, sedangkan
istilah yang telah ada—antara lain aksi kanan, konkatenasi, ruang loop, funktor
penuh/setia, transformasi natural, dan surjektif secara esensial—dipakai
konsisten. Penomoran istilah dan adverse Unit 17 memang belum dialokasikan pada
batas tinjauan ini; tidak ditemukan benturan atau perbaikan tambahan di luar dua
belas baris provisional audit.

## Validasi mekanis

- 34 pengenal stabil didefinisikan dan semuanya unik; Pandoc memancarkan tepat
  34 ID tersebut tanpa duplikasi.
- 18 fenced-div pembuka dan 18 penutup; seimbang.
- 62 pasangan delimiter matematika tampil `$$`; seimbang.
- 6 pemeriksaan penguasaan, 6 solusi, dan 6 tag asal edisi; lengkap satu-ke-satu.
- HTML semantik memuat 384 elemen MathML, tanpa SVG atau gambar.
- Pandoc 3.9.0.2, Markdown ke native dengan `--fail-if-warnings`: exit 0.
- Pandoc 3.9.0.2, HTML5 mandiri dengan MathML, `--section-divs`, dan
  `--fail-if-warnings`: exit 0.
- Pencarian terbatas menemukan nol `xymatrix`, `marginnote`, atau `lecturenum`
  yang tersisa, nol cabang lama `f_1(s,2t-1)`, dan nol sebutan nama payung
  proyek.

## Disposisi akhir

Tidak ditemukan cacat matematis, logis, struktural, bahasa, aksesibilitas,
provenans, atau build yang masih terbuka. **P1 = 0, P2 = 0, P3 = 0.** Unit 17
layak dibekukan pada identitas berkas di atas.
