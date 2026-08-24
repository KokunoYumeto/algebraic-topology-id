# Audit sumber Unit 29 — Kuliah 29 Roberts

## Otoritas dan batas

- Repositori resmi: `DavidMichaelRoberts/AlgebraicTopology2019`.
- Commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Tree: `aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5`.
- Berkas: `Notes.tex`.
- Rentang aktif: baris fisik **6053–6270**, inklusif. Baris 6053 adalah
  `\lecturenum{29}`; baris 6271 memuat `\lecturenum{30}` di tengah kalimat dan
  tidak termasuk.
- Rentang aktif terdiri atas **218 baris**. Setelah digabung dengan LF dan satu
  terminator LF penutup dipertahankan, rentang berukuran **11.447 byte** UTF-8
  dengan SHA-256
  `33c6b7bfe3216d271c6b1f9d0cb952e6ef02a5e27a57f686936e764bfc4a9233`.
- Lisensi komponen sumber: CC BY 4.0.

## Sensus literal

Rentang memuat satu penanda kuliah, dua definisi, satu lema, satu fakta, dua
teorema, satu korolari, tiga contoh, dua catatan, dua lingkungan bukti, empat
catatan pinggir, empat diagram Xy-pic, satu gambar TikZ, satu label, dan satu
rujukan silang. Tidak ada latihan atau pertanyaan formal sumber, gambar
eksternal, sitasi, `input`, ataupun `include`.

## Penutupan semantik dan koreksi wajib

1. **Seluruh peta pembanding dibalik ke arah kanonik.** Unit 28 membuktikan
   bahwa inklusi simpleks istimewa
   `X_n -> Top(Delta^n,|X|)` menghasilkan restriksi
   `rho:C_sing^*(|X|;R)->C_Delta^*(X;R)`. Diagram pada baris 6054–6077,
   fakta baris 6079–6090, teorema dan korolari baris 6093–6122 semuanya memakai
   arah sebaliknya. Edisi harus menggambar baris singular di atas dan baris
   simpleksial di bawah (atau membalik panah vertikal), lalu menyatakan
   isomorfisma yang diinduksi `H_sing^k(|X|;R)->H_Delta^k(X;R)`. Invers boleh
   ditulis, tetapi tidak boleh disebut peta yang diinduksi inklusi simpleks.
2. **Fakta relatif dinormalkan.** Pada derajat `k=n`, faktor sfera harus ditulis
   `\widetilde H^n(S^n;R)` dan peta faktor berjalan dari kohomologi tereduksi
   sfera hasil bagi menuju kohomologi pasangan simpleks. Semua koefisien `R`
   dipertahankan.
3. **Induksi Lema Lima ditutup.** Bukti satu kalimat pada baris 6097–6100 harus
   menyatakan kasus dasar, hipotesis induksi pada kerangka, dua isomorfisma
   relatif, diagram barisan eksak panjang dengan arah benar, dan penerapan Lema
   Lima pada lima suku berurutan.
4. **Kasus tak berdimensi hingga dijelaskan jujur.** Sumber menunjuk pada
   kolimit terfilter tanpa memberikan argumen. Edisi boleh mempertahankan
   batas pedagogis itu, tetapi harus menyatakan mekanisme yang benar: derajat
   `k` stabil setelah kerangka `k+1`; sistem invers pada derajat `k-1` juga
   stabil, sehingga suku `lim^1 H^{k-1}` dalam barisan eksak Milnor lenyap.
   Klaim bahwa
   setiap simpleks singular mempunyai citra dalam suatu subkompleks hingga
   harus dibedakan dari klaim adanya satu kerangka hingga yang bekerja seragam
   bagi semua simpleks.
5. **Notasi korolari diperbaiki.** `H^k(X_bullet)` yang kehilangan `R`, salah
   ketik `stil`, dan tanda titik ganda dinormalkan.
6. **Indeks pelekatan sel dimulai pada nol.** Definisi sumber meminta langkah
   pelekatan hanya untuk `n>=1`, sehingga tidak pernah menambahkan sel-1 dari
   `X_0`. Syarat yang benar adalah `n>=0`: sel `(n+1)` dilekatkan melalui
   `S^n -> X_n`.
7. **Seluruh diagram direflow secara semantik.** Empat diagram Xy-pic sumber
   dipertahankan sebagai persegi kealamian, peta barisan eksak pendek, lima
   suku barisan eksak panjang, dan persegi pushout CW. Gambar TikZ yang
   memperlihatkan beberapa cakram dengan batas dipetakan ke lokus pada `X_n`
   disajikan sebagai daftar objek, peta pelekatan, pushout, dan hasil
   `X_{n+1}`. Makna semuanya tetap tersedia pada HTML responsif dan teknologi
   bantu.
8. **Contoh manifold dibatasi pada klaim yang aman.** Edisi menyatakan bahwa
   manifold mulus kompak mempunyai struktur CW hingga dan manifold topologis
   kompak mempunyai tipe homotopi CW hingga. Klaim homeomorfisma literal pada
   kategori topologis memerlukan hipotesis dimensi/kategori tambahan dan tidak
   disamakan dengan triangulabilitas umum.
9. **Kategori homotopi dibahasakan tanpa ambiguitas.** Morfisma
   `hCW^(2)` adalah **kelas homotopi pemetaan pasangan**, bukan “kelas
   ekuivalensi homotopi” yang dapat keliru dibaca sebagai hanya pemetaan yang
   merupakan ekuivalensi homotopi.
10. **Aksioma eksisi harus bertipe benar.** Teorema sumber mendefinisikan
    `h^k` hanya pada pasangan CW, tetapi kemudian mengevaluasi
    `(X\setminus Z,A\setminus Z)`, yang tidak otomatis pasangan CW. Edisi
    menyatakan eksisi komplemen hanya ketika kedua objek benar-benar pasangan
    CW dan memberi formulasi eksisi kuat melalui peta hasil bagi pasangan CW.
    Ini menghilangkan penerapan fungtor pada objek di luar domainnya.
11. **Aksioma dan normalisasi tetap lengkap.** Aditivitas menghasilkan hasil
    kali pada kohomologi, barisan eksak panjang bersifat natural, eksisi
    berjalan kontravarian, dan dimensi memberi `h^0(*)=R` serta nol pada
    derajat lain. Homotopi sudah diinkorporasikan dengan bekerja pada kategori
    homotopi.

## Lapisan penguasaan edisi

Karena tidak ada latihan sumber, pembaca menambahkan enam pemeriksaan
penguasaan dengan petunjuk dan solusi lengkap: kealamian peta pembanding;
induksi kerangka dan Lema Lima; perluasan ke himpunan-Delta tak berdimensi
hingga; konstruksi CW dan indeks sel; pasangan CW serta hasil bagi; dan
rekonstruksi aksioma Eilenberg–Steenrod. Semua tambahan dilabeli sebagai
materi asli edisi di bawah CC BY 4.0.

## Putusan audit

`ADMISSIBLE_AFTER_REPAIR`. Rentang dapat diterjemahkan secara kontigu setelah
seluruh arah pembanding dan kesalahan tipe di atas diperbaiki secara seragam.
Unit 29 tidak boleh mengembalikan arah peta yang telah dibetulkan pada Unit 28.
