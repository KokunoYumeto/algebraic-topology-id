# Tinjauan independen Unit 29

## Putusan

**PASS — P1: 0, P2: 0, P3: 0.** Unit 29 menutup seluruh rentang sumber
`Notes.tex:6053–6270`, mempertahankan semua objek matematis dan urutan
semantiknya, serta berakhir pada kursor tepat `Notes.tex:6271`, tempat penanda
Kuliah 30 muncul di tengah kalimat. Delapan temuan selama tinjauan telah
diselesaikan sebelum pengakuan unit; tidak ada temuan terbuka.

## Identitas yang ditinjau

- Otoritas: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`.
- Commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Tree: `aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5`.
- Berkas otoritas: 331.447 byte, 6.368 baris, SHA-256
  `cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7`.
- Rentang aktif: 218 baris LF, 11.447 byte, SHA-256
  `33c6b7bfe3216d271c6b1f9d0cb952e6ef02a5e27a57f686936e764bfc4a9233`.
- Audit sumber final: `qa/UNIT_029_SOURCE_AUDIT.md`, 5.738 byte, 101 baris,
  SHA-256
  `6b3e96ca5a7d24a4f8182c46f02e99194c9538ca534b4b550ea23b666ad89afb`.
- Pembaca final: `source/id-ID/units/unit-029-lecture-029.md`, 27.687 byte,
  805 baris, SHA-256
  `cfb8fa5c49593a187bed5df1d4173cc952100b18e5faa009cb8d57036c5726c4`.

## Penutupan sumber dan arah pembanding

Sensus literal diverifikasi langsung pada rentang beku: satu penanda kuliah,
dua definisi, satu lema, satu fakta, dua teorema, satu korolari, tiga contoh,
dua catatan, dua lingkungan bukti, empat catatan pinggir, empat diagram
Xy-pic, satu gambar TikZ, satu label, dan satu rujukan silang. Tidak ada
latihan/pertanyaan formal, gambar eksternal, perintah sitasi, `input`, atau
`include`.

Semua pemetaan pembanding telah diperiksa satu per satu. Inklusi simpleks
istimewa menghasilkan restriksi
`C^*_{sing}(|X|;R)→C^*_Delta(X;R)`, bukan arah sebaliknya. Arah ini konsisten
pada persegi kealamian, peta barisan eksak pendek, lima suku barisan eksak
panjang, fakta relatif, Teorema 29.1, Korolari 29.1, dan ketiga pemeriksaan
penguasaan yang memakainya. Identitas
`rho_X |f|^* = f^* rho_Y` mengikuti
`|f| chi_x = chi_{f(x)}` dan mempertahankan kontravariansi kedua baris.

Pada fakta relatif, hasil bagi kerangka memberi baji sfera dan kohomologi
derajat `n` berupa hasil kali salinan `R`. Peta faktor sekarang ditulis tepat
sebagai tarik-balik peta hasil bagi pasangan
`q_x:(Delta^n,partial Delta^n)→(S^n,*)`, yaitu
`q_x^*:H-tilde^n(S^n;R)→H^n(Delta^n,partial Delta^n;R)`. Penggunaan kohomologi
tereduksi membuat pernyataan tetap benar pada `n=0`.

## Bukti perbandingan hingga dan tak hingga

Bukti berdimensi hingga memuat kasus dasar dimensi nol, hipotesis induksi pada
kerangka, kedua isomorfisma relatif, kedua isomorfisma kerangka, dan penerapan
Lema Lima pada lima suku berurutan. Diagram lima suku sumber direflow sebagai
dua baris eksak yang dapat dibaca pada layar sempit, dengan kelima peta
vertikal dijelaskan menurut posisinya; tidak ada suku yang hilang.

Untuk himpunan-Delta berdimensi tak hingga, pembaca tidak menyimpulkan hasil
hanya dari setiap simpleks singular secara individual. Ia memakai filtrasi
kerangka CW: penambahan sel berdimensi sekurang-kurangnya `k+2` tidak mengubah
`H^k`, sistem invers `H^k` stabil setelah kerangka `k+1`, dan sistem
`H^{k-1}` juga stabil. Karena itu suku turunan-limit
`lim^1 H^{k-1}` dalam barisan eksak Milnor lenyap, lalu teorema berdimensi
hingga berlaku pada `(k+1)`-kerangka. Ini menutup peralihan ke seluruh
realisasi tanpa mengandaikan satu subkompleks hingga yang seragam bagi semua
simpleks singular.

## Kompleks CW, pasangan, dan aksioma

Keempat diagram Xy-pic sumber mempunyai representasi semantik: persegi
kealamian, peta barisan eksak pendek, lima suku barisan eksak panjang, dan
persegi pushout CW. Gambar TikZ sumber direflow sebagai daftar batas sfera,
peta pelekatan, cakram pengisi, dan ruang hasil. Dua catatan pinggir definisi
CW juga tertutup: identifikasi simpleks dengan cakram/batas sfera dan gabungan
sebagai kolimit topologis filtrasi dijelaskan eksplisit.

Indeks pelekatan dimulai pada `n=0` dan memakai `J_{n+1}` untuk sel
berdimensi `n+1`, sehingga sel-1 tidak hilang. Contoh pasangan
`(D^n,S^{n-1})` membedakan batas `S^0` pada `n=1` dari struktur sfera untuk
`n≥2`. Klaim manifold dibatasi dengan benar: manifold mulus kompak mempunyai
struktur CW hingga, sedangkan manifold topologis kompak dinyatakan mempunyai
tipe homotopi CW hingga tanpa klaim triangulabilitas universal.

Objek dan morfisma `CW^(2)` bertipe benar. Morfisma `hCW^(2)` adalah kelas
homotopi pemetaan pasangan, bukan hanya pemetaan yang merupakan ekuivalensi
homotopi. Teorema Eilenberg–Steenrod menulis satu fungtor dari kategori
berlawanan dan menjelaskan kontravariansi hanya sekali. Eksisi komplemen
diterapkan hanya jika kedua objek merupakan pasangan CW; bentuk eksisi kuat
melalui `q:(X,A)→(X/A,*)` tetap sepenuhnya di dalam domain. Aditivitas,
barisan eksak natural, eksisi, dimensi, serta normalisasi koefisien semuanya
dipertahankan.

## Temuan yang diselesaikan

1. `UNIT029-MATH-P2-001` — Faktor sfera pada penjelasan fakta relatif masih
   memakai `H^n(S^n;R)`, yang bukan faktor yang benar pada dimensi nol.
   **Diselesaikan:** faktor diganti dengan kohomologi tereduksi dan peta
   dinyatakan sebagai tarik-balik peta hasil bagi pasangan.
2. `UNIT029-MATH-P2-002` — Stabilisasi hanya disebut pada derajat `k`, padahal
   penghilangan suku turunan-limit juga memerlukan stabilisasi derajat
   `k-1`. **Diselesaikan:** kedua sistem invers dan barisan eksak Milnor kini
   dinyatakan eksplisit.
3. `UNIT029-TYPE-P2-003` — Formulasi eksisi mengizinkan “penggantian model”
   tanpa menetapkan objek dan morfismanya. **Diselesaikan:** eksisi komplemen
   dibatasi pada pasangan CW dan bentuk hasil bagi kuat ditulis sebagai peta
   pasangan CW yang bertipe lengkap.
4. `UNIT029-REFLOW-P3-001` — Diagram barisan eksak panjang awalnya hanya
   menampilkan tiga dari lima suku sumber. **Diselesaikan:** kedua baris lima
   suku kini direflow utuh, dan audit mencatat keempat diagram serta gambar
   TikZ secara terpisah.
5. `UNIT029-CW-P3-002` — Dua catatan pinggir CW belum terlihat eksplisit dan
   contoh `(D^n,S^{n-1})` tidak membedakan kasus `S^0`.
   **Diselesaikan:** identifikasi cakram, kolimit filtrasi, dan struktur batas
   untuk `n=1` serta `n≥2` sekarang lengkap.
6. `UNIT029-LANG-P3-003` — Pembaca memakai varian `funktor`, `funktorial`,
   `naturalitas`, dan `bujur sangkar`, bukan pilihan utama glosarium.
   **Diselesaikan:** seluruh unit memakai `fungtor`, `fungtorial`, `kealamian`,
   dan `persegi`; ejaan `aditivitas` juga dinormalkan.
7. `UNIT029-TERM-P3-004` — Audit sumber yang telah diperbaiki masih memakai
   `bola` untuk objek $S^n$ dan `perpanjangan` untuk *extension*.
   **Diselesaikan:** kontrol kini memakai **sfera** dan **perluasan**, sesuai
   istilah terterima; pembaca matematis dan batas sumber tidak berubah.
8. `UNIT029-QA-P3-005` — Sensus awal menghitung 48 ID karena pola audit
   melewatkan ID akar kuliah `o012-rbt-l29`. **Diselesaikan:** sensus final
   menghitung 49 ID unik dan sembilan judul teridentifikasi; render Pandoc
   mempertahankan seluruh 49 ID tanpa duplikasi. Pembaca tidak berubah.

## Bahasa, struktur, penguasaan, dan provenance

Istilah `himpunan-Delta`, `korantai simpleksial`, `kohomologi tereduksi`,
`kerangka`, `peta pelekatan`, `pasangan CW`, `kelas homotopi`, `fungtor`,
`kealamian`, `sfera`, `perluasan`, dan `Lema Lima` sesuai glosarium yang sudah diakui. Tidak ada
prosa Inggris pembaca yang tersisa selain judul karya, nama diri, dan fragmen
literal sumber yang diperlukan untuk provenance.

Pembaca memiliki 49 ID stabil, semuanya unik; 40 objek berpagar seimbang
(1 boundary, 1 corollary, 2 definition, 3 example, 6 exercise, 1 fact,
1 figure, 6 hint, 1 lemma, 4 proof, 6 solution, 6 source-audit, 2 theorem).
Keenam latihan asli edisi masing-masing mempunyai tepat satu petunjuk dan satu
solusi lengkap. Atribusi Roberts, commit/rentang, hak CC BY 4.0,
non-endorsement, kredit kontributor manusia, dan provenance model exact
`OpenAI Codex gpt-5.6-sol, Ultra` semuanya hadir; tidak ada penanda privat.

Render sementara Pandoc 3.9.0.2 ke HTML5 MathML selesai dengan exit 0 dan
`--fail-if-warnings`: 129.591 byte, 258 simpul MathML, seluruh 49 ID muncul
tepat dalam keluaran, dan tidak ada ID hilang. Berkas render sementara telah
dihapus setelah pemeriksaan.

## Batas

Unit ini berakhir pada `Notes.tex:6270`. Baris sumber berikutnya adalah 6271,
yang memuat `\lecturenum{30}` dan memulai Kuliah 30.
