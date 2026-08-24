# Audit sumber Unit 28 — Kuliah 28 Roberts

## Otoritas dan batas

- Repositori resmi: `DavidMichaelRoberts/AlgebraicTopology2019`.
- Commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Tree: `aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5`.
- Berkas: `Notes.tex`.
- Rentang aktif: baris fisik **5924–6052**, inklusif. Baris 5924 memuat
  penanda `\lecturenum{28}` di tengah kalimat yang melanjutkan contoh pada
  Kuliah 27; baris 6053 memulai `\lecturenum{29}` dan tidak termasuk.
- Rentang aktif terdiri atas **129 baris**. Setelah baris digabung dengan LF dan
  satu terminator LF penutup dipertahankan, rentang berukuran **8.257 byte**
  UTF-8 dengan SHA-256
  `f3e4a526fa2e504a449a606150c399520c255a98a91d60c934737f87497b4b51`.
- Lisensi komponen sumber: CC BY 4.0.

## Sensus literal

Rentang memuat satu penanda kuliah, satu definisi, tiga proposisi, dua teorema,
satu korolari, satu contoh mandiri selain lanjutan contoh dari Unit 27, satu
catatan, tiga lingkungan bukti, lima catatan pinggir, satu label, dan lima
rujukan silang. Tidak ada latihan atau pertanyaan formal sumber, diagram
Xy-pic/TikZ, gambar eksternal, perintah `\cite`, `input`, ataupun `include`.
Ada dua rujukan bibliografis tekstual ke Proposition 2.22 dan Proposition A.4
dalam buku Hatcher; keduanya dicatat dalam edisi.

## Penutupan semantik dan koreksi yang diterapkan

1. **Lanjutan contoh tidak diputus.** Baris 5924–5937 menyelesaikan perhitungan
   kohomologi sfera yang dimulai pada Unit 27. Edisi menandainya sebagai lanjutan
   yang eksplisit, mempertahankan kedua kasus induksi dan penutup lingkungan
   contoh.
2. **Koefisien taknol pada argumen pendeteksian.** Klaim bahwa sfera berlainan
   dimensi tidak ekuivalen homotopi dan bukti di baris 5951–5959 sama-sama
   mendeteksi satu salinan `R`. Argumen itu tidak bekerja dengan gelanggang nol,
   karena semua grup kohomologi lalu nol. Edisi menyatakan pilihan gelanggang
   koefisien taknol (misalnya `Z`) setiap kali kohomologi dipakai sebagai
   pendeteksi, dan menangani dimensi nol secara terpisah.
3. **Eksisi tetap kontravarian.** Untuk inklusi pasangan
   `(X\setminus Z,A\setminus Z) -> (X,A)`, panah kohomologi sumber dari
   `H^k(X,A;R)` ke `H^k(X\setminus Z,A\setminus Z;R)` sudah benar dan
   dipertahankan.
4. **Arah peta hasil bagi diperbaiki.** Baris 5973–5979 mengatakan bahwa peta
   hasil bagi `q:(X,A)->(X/A,*)` *menginduksi* panah
   `H^k(X,A;R)->H^k(X/A,*;R)`. Kohomologi bersifat kontravarian, sehingga panah
   terinduksi yang benar adalah
   `q^*:H^k(X/A,*;R)->H^k(X,A;R)`. Edisi menyatakan panah yang benar dan hanya
   menulis arah sebaliknya sebagai invers dari isomorfisma itu.
5. **Bukti teorema hasil bagi ditutup.** Sumber hanya merujuk Proposition 2.22
   Hatcher. Edisi memberi argumen penuh: ganti `A` dengan lingkungan terbuka
   `U` yang diretrak-deformasikan ke `A`; pakai eksisi untuk menghapus `A` dan
   titik hasil baginya; identifikasi pasangan komplemen; lalu gunakan
   kontraktilitas `U/A` untuk memperoleh kohomologi tereduksi.
6. **Istilah `join` diperbaiki menjadi `wedge`.** Baris 6004 dan 6013
   menyebut hasil bagi bertitik yang dilambangkan `vee` sebagai *join*.
   Konstruksi itu adalah **baji** (*wedge sum*), bukan *join*. Koreksi yang sama
   sudah menjadi konvensi global edisi.
7. **Hipotesis baji tak berhingga ditambahkan.** Proposisi baris 6025–6031
   dinyatakan untuk keluarga ruang bertitik sembarang. Agar aksioma baji bagi
   kohomologi singular berlaku dalam bentuk yang dipakai, edisi mengambil
   himpunan indeks takkosong dan mensyaratkan setiap titik dasar tertutup serta
   merupakan retrak deformasi suatu lingkungan terbuka. Dengan demikian,
   gabungan saling lepas semua titik dasar merupakan subruang tertutup yang
   diretrak-deformasikan dari sebuah lingkungan, sehingga Teorema hasil bagi
   28.2 benar-benar dapat diterapkan. Hipotesis ini mencakup kompleks CW yang
   bertitik dasar pada sel-0 dan semua sfera pada aplikasi berikutnya.
8. **Koefisien yang hilang dipulihkan.** Ruas kiri proposisi baji kehilangan
   `R`; edisi menuliskan `\widetilde H^k(-;R)` pada kedua ruas.
9. **Arah peta pembanding korantai diperbaiki.** Inklusi himpunan simpleks
   istimewa `X_n -> Top(Delta^n,|X|)` menghasilkan peta *restriksi*
   `C^n_sing(|X|;R)->C^n_Delta(X;R)`, bukan inklusi dengan arah sebaliknya
   seperti baris 6045–6048. Edisi memberi rumus evaluasi dan memeriksa bahwa
   peta itu berkomutasi dengan diferensial. Unit 29 harus mempertahankan arah
   ini pada seluruh diagram pembanding.
10. **Notasi hasil bagi ruang kosong diperbaiki.** Catatan pinggir baris 5969
    menulis `X\setminus\emptyset := X\sqcup\pt`, padahal selisih dengan
    himpunan kosong adalah `X`. Konteks pasangan hasil bagi memerlukan
    `X/\emptyset=X_+:=X\sqcup\{*\}`, dan itulah notasi yang dipakai edisi.
11. Salah ketik lokal `satsifying`, `acually`, `pair of space`, dan
    `|\sk_{n-1}X)\bullet|` dinormalkan tanpa mengubah isi matematika.

## Lapisan penguasaan edisi

Karena rentang tidak mempunyai latihan sumber, edisi menambahkan enam
pemeriksaan penguasaan dengan petunjuk dan solusi lengkap: kohomologi sfera;
invariansi dimensi; arah eksisi; teorema hasil bagi; hasil bagi kerangka dan
kohomologi baji; serta arah dan sifat peta pembanding korantai. Semua materi
tambahan dilabeli sebagai materi asli edisi dan dirilis di bawah CC BY 4.0.

## Putusan audit

`ADMISSIBLE_AFTER_REPAIR`. Seluruh prosa dan objek matematika sumber pada
baris 5924–6052 dapat diterjemahkan secara kontigu. Koreksi di atas harus
terlihat pada catatan audit dalam pembaca, ledger merugikan, dan backend
semantik sebelum Unit 28 diakui sebagai selesai.
