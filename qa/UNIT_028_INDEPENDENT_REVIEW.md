# Tinjauan independen Unit 28

## Putusan

**PASS — P1: 0, P2: 0, P3: 0.** Unit 28 menutup seluruh rentang sumber
`Notes.tex:5924–6052`, mempertahankan urutan semantik dan semua rumus, serta
berakhir pada kursor tepat `Notes.tex:6053` (`\lecturenum{29}`). Enam temuan
selama tinjauan telah diselesaikan sebelum pengakuan unit; tidak ada temuan
terbuka.

## Identitas yang ditinjau

- Otoritas: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`.
- Commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Tree: `aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5`.
- Berkas otoritas: 331.447 byte, 6.368 baris, SHA-256
  `cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7`.
- Rentang aktif: 129 baris LF, 8.257 byte, SHA-256
  `f3e4a526fa2e504a449a606150c399520c255a98a91d60c934737f87497b4b51`.
- Audit sumber final: `qa/UNIT_028_SOURCE_AUDIT.md`, 5.660 byte, 96 baris,
  SHA-256
  `2b181bcd12c95210395b3aec8b866b69093d6636b89773d08d93cec41870fa4a`.
- Pembaca final: `source/id-ID/units/unit-028-lecture-028.md`, 26.072 byte,
  814 baris, SHA-256
  `b69036f5a0a8151942288f04197a9dc69c81d2902fe8a15a0e73601978fefe67`.

## Penutupan sumber dan matematika

Sensus literal diverifikasi langsung pada rentang beku: satu penanda kuliah,
satu definisi, tiga proposisi, dua teorema, satu korolari, satu contoh baru dan
satu penutup contoh yang dimulai pada Unit 27, satu catatan, tiga lingkungan
bukti, lima catatan pinggir, satu label, lima rujukan silang, dan sepuluh
lingkungan pajangan. Tidak ada latihan/pertanyaan formal, diagram, gambar,
`input`, `include`, atau perintah `\cite`; dua rujukan bibliografis tekstual
ke Proposition 2.22 dan Proposition A.4 dalam buku Hatcher dipertahankan dalam
catatan edisi.

Pemetaan rumus dan objek diperiksa satu per satu. Pembaca memuat kedua langkah
reduksi Mayer–Vietoris dan rumus lengkap kohomologi sfera; pilihan koefisien
taknol pada setiap penggunaan kohomologi sebagai pendeteksi; argumen invariansi
dimensi; teorema eksisi beserta arah `j^*`; teorema
hasil bagi, korolari barisan eksak, dan bukti mandirinya; empat identifikasi
hasil bagi kerangka; definisi baji; suku relatif kerangka; rumus hasil kali
kohomologi baji; contoh baji sfera; serta rumus evaluasi dan pemeriksaan
diferensial bagi peta pembanding korantai.

- Inklusi eksisi
  `(X\setminus Z,A\setminus Z)\hookrightarrow(X,A)` benar-benar menghasilkan
  `H^k(X,A;R)→H^k(X\setminus Z,A\setminus Z;R)`.
- Peta hasil bagi `q:(X,A)→(X/A,*)` benar-benar menghasilkan
  `q^*:H^k(X/A,*;R)→H^k(X,A;R)`; panah sebaliknya disebut hanya sebagai
  invers isomorfisma.
- Bukti hasil bagi menutup semua prasyarat: `A` tertutup, `U` terbuka,
  kontraktilitas `U/A`, dua penerapan eksisi, homeomorfisma pasangan
  komplemen, dan barisan eksak tereduksi.
- Proposisi baji tak berhingga kini mensyaratkan `J` takkosong serta setiap
  titik dasar tertutup dan merupakan retrak deformasi suatu lingkungan
  terbuka. Dengan `Y=⊔X_α` dan `A=⊔{x_α}`, Teorema 28.2 sah diterapkan pada
  `Y/A=∨X_α`; kompleks rantai relatif terurai sebagai jumlah langsung dan
  kompleks korantai sebagai hasil kali.
- Inklusi simpleks istimewa
  `X_n→Top(Δ^n,|X|)` diprakomposisikan, sehingga arah kanoniknya adalah
  `C^*_{sing}(|X|;R)→C^*_Δ(X;R)`. Identitas
  `ρ_{n+1}δ_sing=δ_Δρ_n` telah diperiksa indeks dan tandanya.

## Temuan yang diselesaikan

1. `UNIT028-MATH-P2-001` — Pernyataan baji hanya menyebut retrak deformasi
   lingkungan, tanpa ketertutupan titik dasar atau `J` takkosong. Ini belum
   memenuhi seluruh hipotesis Teorema 28.2 yang dipakai oleh pembuktian.
   **Diselesaikan:** pernyataan, bukti, contoh, dan audit kini memuat hipotesis
   tepat dan menunjukkan penerapan teorema pada pasangan gabungan saling lepas.
2. `UNIT028-AUDIT-P3-001` — Pembaca sudah membetulkan catatan sumber
   `X\setminus\varnothing:=X\sqcup\{*\}` menjadi
   `X/\varnothing=X_+`, tetapi audit belum mencatat koreksi semantik ini.
   **Diselesaikan:** koreksi kini tercatat pada audit sumber dan blok audit
   pembaca.
3. `UNIT028-PROV-P3-002` — Audit lama menyatakan tidak ada sitasi tanpa
   membedakan ketiadaan perintah `\cite` dari dua rujukan tekstual Hatcher;
   rujukan A.4 juga belum tampak dalam pembaca. **Diselesaikan:** sensus kini
   menyatakan perbedaannya secara tepat dan pembaca mempertahankan rujukan A.4.
4. `UNIT028-MATH-P3-003` — Klaim bahwa kohomologi membedakan sfera berlainan
   dimensi mendahului pilihan eksplisit `R≠0`; dengan gelanggang nol, argumen
   pendeteksian itu tidak bekerja. **Diselesaikan:** pembaca kini membedakan
   validitas rumus untuk semua `R` dari penggunaan pendeteksian yang selalu
   memilih `R≠0`, dan audit merekam cakupan koreksi tersebut.
5. `UNIT028-TERM-P3-004` — Draf Unit 28 memakai `bola` untuk objek $S^n$,
   padahal konvensi lapangan yang sudah diterima pada Unit 27 ialah
   `sfera` untuk *sphere* dan `bola` hanya untuk *ball*. **Diselesaikan:** semua
   prosa Unit 28 yang merujuk $S^n$ kini memakai `sfera`; tidak ada makna
   bola/cakram sejati yang diubah.
6. `UNIT028-TERM-P3-005` — Satu kalimat masih memakai varian yang dikenali
   tetapi tidak diutamakan, `funktor`. **Diselesaikan:** bentuk itu dinormalkan
   menjadi **fungtor**, sesuai entri terterima `O012-TERM-0004`; matematika,
   ID, dan batas sumber tidak berubah.

## Bahasa, struktur, penguasaan, dan provenance

Istilah `kohomologi tereduksi`, `eksisi`, `ruang hasil bagi`, `baji`, `sfera`, `fungtor`,
`korantai`, `kobatas`, `simpleksial`, dan `retrak deformasi` dipakai secara
alami dan konsisten. Konvensi `sfera`=$S^n$ dibedakan dari `bola` untuk
*ball*. *Join* sumber yang salah tidak dipertahankan. Tidak ada
prosa Inggris pembaca yang tersisa selain judul karya/nama perintah sumber dan
rujukan bibliografis yang memang harus presisi.

Pembaca memiliki 47 ID stabil, semuanya unik; 39 objek berpagar seimbang
(3 aside, 1 boundary, 1 corollary, 1 definition, 1 example, 6 exercise,
6 hint, 4 proof, 3 proposition, 6 solution, 5 source-audit, 2 theorem).
Keenam latihan asli edisi masing-masing mempunyai tepat satu petunjuk dan satu
solusi lengkap. Atribusi Roberts, commit/rentang/hak CC BY 4.0,
non-endorsement, kredit kontributor manusia, dan provenance model exact
`OpenAI Codex gpt-5.6-sol, Ultra` semuanya ada; tidak ada penanda privat.

Render sementara Pandoc 3.9.0.2 ke HTML5 MathML selesai dengan exit 0 dan
`--fail-if-warnings`: 122.657 byte, 261 simpul MathML, seluruh 47 ID muncul
tepat dalam keluaran, dan tidak ada ID hilang. Berkas render sementara telah
dihapus setelah pemeriksaan.

## Batas

Unit ini berakhir pada `Notes.tex:6052`. Baris sumber berikutnya adalah 6053,
awal Kuliah 29. Unit 29 wajib memakai arah pembanding
`C^*_{sing}(|X|;R)→C^*_Δ(X;R)` yang sudah diperbaiki di sini.
