# Proposal DAQ: Makhraj

Proposal Musabaqah Desain Aplikasi Komputer Al-Qur'an (DAQ) untuk aplikasi **Makhraj**, aplikasi tahsin berbasis visualisasi makhraj dan rujukan guru bersanad. Hasil akhirnya ada di `output/` (DOCX dan PDF). Semuanya digenerate dari kode di `script/`.

## Aturan utama

1. **Jangan mengedit file di `output/` secara manual.** Semua perubahan dilakukan di `script/`, lalu jalankan build.
2. Teks hanya ada di `script/content.py`. DOCX dan PDF dibangun dari sumber yang sama, jadi isinya selalu identik.
3. Setiap build harus diakhiri dengan pengecekan halaman (lihat checklist). Batas panduan adalah **8-10 halaman**. Bagian 1-10 **dan** Daftar Pustaka dijaga muat dalam 10 halaman bernomor; materi pendukung masuk `LAMPIRAN` (pola contoh *Executive Summary IFEST Teen Tensors*).

## Cara regenerate

```bash
cd paper/script
pip install -r requirements.txt
python build.py                 # semuanya: layar purwarupa, gambar, cek, DOCX, PDF, pratinjau
python build.py --skip-figures  # lebih cepat kalau hanya mengubah teks
python build.py --no-pdf        # hanya DOCX
python _sheet.py                # gabungkan pratinjau halaman jadi _preview/sheet.png
```

- PDF dikonversi dari DOCX memakai **Microsoft Word** (pywin32), jadi tata letak PDF sama dengan tampilan DOCX di Word. Kalau Word tidak ada, LibreOffice bisa dipakai: `soffice --headless --convert-to pdf output/Proposal_DAQ_Makhraj.docx`. Karena metrik font berbeda, halaman bisa bergeser, jadi cek ulang batas halamannya.
- Build mencetak akhir bagian 1-10, akhir Daftar Pustaka, dan rentang halaman lampiran. Kalau salah satu `LEBIH`, pangkas teks, perkecil gambar, atau pindahkan materi ke `LAMPIRAN`.
- Build juga mencetak `PERINGATAN` selama placeholder `[tautan ...]` masih ada.
- Layar purwarupa dirender dengan Edge/Chrome headless dan butuh internet untuk memuat Google Fonts. Layar hanya dirender ulang kalau sumbernya berubah.

## Peta file

| File | Isi |
|---|---|
| `script/content.py` | `COVER` (sampul), `BODY` (bagian 1-10), dan `LAMPIRAN` (Lampiran 1-5, setelah Daftar Pustaka). Rujukan silang ditulis `{fig:kunci}` / `{tab:kunci}`; di BODY dinomori 1, 2, ..., di LAMPIRAN berhuruf A, B, .... |
| `script/references.py` | `REFERENCES`: Daftar Pustaka APA 7 (dikutip di bagian 1-10 atau lampiran). `REFERENCES_LAMPIRAN`: sumber yang hanya dikutip di lampiran, dicetak sebagai "Rujukan Lampiran" di akhir lampiran supaya Daftar Pustaka tetap dalam 10 halaman. `checks.py` menolak kutipan di badan yang hanya ada di `REFERENCES_LAMPIRAN`. |
| `script/figures.py` | Semua gambar, satu fungsi per gambar. Badan: `fig_literasi` (G1), `fig_alur_belajar` (G2), `fig_roadmap` (G3, peta jalan + ringkasan model bisnis per tahap), `fig_usecase`, `fig_class`, `fig_erd`, `fig_arsitektur`, `fig_screens`. Lampiran: `fig_pasar` (A, hitungan TAM/SAM/SOM di `market_numbers`), `fig_bmc` (Business Model Canvas), `fig_ekosistem` (aliran nilai dan dana), `fig_keuangan` (proyeksi + skenario; angka di `FIN_*`, `SCENARIOS`), `fig_gantt` (rencana 36 bulan; `GANTT`, `MILESTONES`). |
| `script/screens/src/*.dc.html` | Sumber 6 layar purwarupa (salinan dari kanvas desain). `support.js` adalah runtime kecil untuk merendernya; `render_screens.py` mengubahnya menjadi PNG di `screens/png/`. |
| `script/checks.py` | Menolak em dash, gambar yang hilang, rujukan silang yang salah, gambar atau tabel yang tidak dirujuk, dan sitasi tanpa pustaka. |
| `script/build.py` | Format dokumen (margin, font, keterangan gambar dan tabel, nomor halaman) dan konversi ke PDF. |
| `script/_preview/` | PNG tiap halaman PDF untuk render check (bukan hasil akhir). |

## Keputusan yang sudah diambil

- **Lomba:** MTQMN, cabang DAQ. Sistematika mengikuti panduan MTQMN XVIII 2025, hlm. 31: 1) Judul Aplikasi, 2) Latar Belakang, 3) Tujuan dan Manfaat, 4) Batasan, 5) Metode, 6) Market Analisis, 7) Desain (Use Case, Class Diagram, ERD), 8) Implementasi Teknologi, 9) Tampilan Purwarupa, 10) Dokumentasi.
- **Format:** A4, Times New Roman 12, spasi 1,15, margin 2,5 cm di semua sisi. Isi tabel memakai 10 pt dan keterangan gambar/tabel 12 pt (dinaikkan dari 11 pt pada 19 Okt 2026); panduan hanya menyebut "Times New Roman 12". Menaikkan `TABLE_PT` ke 12 tidak muat dalam 10 halaman.
- **Halaman (19 Okt 2026, purwarupa React):** sampul tidak bernomor. Bagian 1-10 berakhir di halaman 9 dan Daftar Pustaka di halaman 10 (sisa kurang dari 1 baris). Baevski, Osterwalder, dan UU PDP hanya dikutip di lampiran sehingga dipindah ke Rujukan Lampiran. Lampiran (hlm. 11-26) dibuka dengan catatan bahwa lampiran berada di luar batas 8-10 halaman: (1) pencocokan materi dengan *Fath Rabb al-Bariyyah* + pola kesalahan penutur Indonesia, (2) TAM/SAM/SOM + SWOT, (3) model bisnis, keuangan, skenario, pemasaran, Gantt, (4) implementasi dan status fitur, (5) screenshot lanjutan, (6) keputusan teknologi (Flutter ke React), (7) sumber konten, lisensi, kebijakan YouTube, (8) rancangan uji coba dan instrumen, (9) kajian kesiapan AI penilai, (10) pelindungan data dan backend Tahap 2, (11) aksesibilitas, (12) risiko dan status pekerjaan, lalu Rujukan Lampiran. Tambahan teks di bagian 5 menggeser Tabel 3 dan gambar desain: setiap tambah teks di badan, cek lagi celah kosong di hlm. 5-7.
- **Sampul:** nama + NIM anggota dan "UNIVERSITAS AIRLANGGA, SURABAYA" mengikuti suntingan manual tim. Catatan risiko: Panduan (hlm. 17, butir 9) melarang nama/atribut perguruan tinggi pada video, foto, dan virtual meeting; untuk proposal tidak disebut eksplisit. Hapus dari `COVER` kalau ingin aman.
- **Bahasa:** Indonesia, formal akademik, tanpa em dash, sudah diaudit dengan skill `ai-paraphrase` (tingkat Sedang).
- **Sitasi:** APA 7, nama-tahun. Hadis dirujuk di teks dengan nomor hadis, tanpa entri pustaka.
- **Produk:** pemula segala usia; React 19 + Vite + Capacitor (web/PWA + Android, kode di `../web/`); progres di localStorage, rekaman di IndexedDB; Firebase Hosting, Auth/Firestore pada Tahap 2; klip guru lewat YouTube IFrame resmi (tanpa unduh), ض/ط dari kanal resmi Dr. Ayman Swaid; teks rasm Utsmani riwayat Hafsh dari Tanzil (CC BY 3.0, tidak boleh diubah; bukan Mushaf Standar Indonesia); terjemahan Kemenag edisi lama via Tanzil, nonkomersial (izin LPMQ sebelum premium). Jangan menulis "edisi 2019". Tahap 1 MVP, Tahap 2 setor ke pengajar, Tahap 3 penilaian AI.
- **Gaya gambar:** font Plus Jakarta Sans (font aplikasi, dari `../app/assets/fonts`) dan palet merek teal-emas. Seri grafik data memakai `S_TEAL #008C7E` dan `S_GOLD #B5760E`, lolos validator palet (chroma, CVD, kontras). Gambar badan yang dicetak jauh lebih kecil dari 15,5 cm sebaiknya digambar pada ukuran cetaknya (contoh `fig_literasi`, 11,5 cm) supaya huruf tidak menyusut di bawah ~6 pt. `python _stitch.py out.png fig01_literasi ...` menggabungkan PNG untuk diperiksa.
- **Angka keuangan** di `figures.py` (`FIN_*`, `SCENARIOS`, `MAU`, `NET`) harus sama dengan Tabel C dan D di `content.py`; ubah keduanya bersamaan.
- **Rujukan gaya penulisan:** pola dari contoh paper juara di `../contoh paper/` (corong latar belakang berbasis data, tiga celah, tabel pembanding, modul input-proses-keluaran, peta jalan).

## Catatan teknis

- **Teks Arab di tengah kalimat Indonesia.** `add_rich` menaruh setiap rangkaian huruf Arab di *run* tersendiri bertanda `w:rtl`. Word mengabaikan tanda LRM, dan LRE/LRI tercetak sebagai kotak; hanya cara ini yang menjaga urutan "(ح-ه, ث-س, ...)" (sudah diuji).
- **Tabel** tanpa warna latar. Kolom angka/status pada tabel di `CENTER_TABLES` (`build.py`) rata tengah; sel rata tengah secara vertikal.
- **Kaidah penulisan** (EYD V, KBBI, APA 7) dirangkum di docstring `content.py`. `checks.py` juga menolak huruf miring yang bersarang di dalam huruf tebal, karena tanda bintangnya akan tercetak.
- **Gambar mendorong halaman.** Gambar yang tidak muat akan pindah ke halaman berikutnya dan meninggalkan ruang kosong. Lebar gambar sudah disetel supaya Daftar Pustaka selesai di halaman 10 (ERD 10 cm, arsitektur 10,4 cm, screenshot 9 cm). Paragraf rekaman/wav2vec (Tahap 2-3) dipindah ke Lampiran 4 demi batas halaman. Kalau teks bagian 7-9 ditambah, cek lagi apakah Gambar 7 atau 8 terdorong; ini titik yang paling rawan bergeser.
- **Lebar kolom tabel** diisi ke `tblGrid` (`t.columns[i].width`), karena tabel ber-layout tetap di Word mengabaikan lebar sel.
- **Kalimat pengantar daftar** yang berakhir titik dua otomatis diberi *keep with next* supaya tidak yatim di bawah halaman.
- **Heredoc dan escape.** Saat menambal file Python lewat shell, `\n` dan `\u....` di dalam string bisa berubah menjadi karakter asli. Lebih aman mengedit langsung di editor.
- **Diagram ERD** memakai notasi crow's foot buatan sendiri (`_crow`). Jarak antarkotak minimal 0,6 unit supaya ujung relasi tidak bertabrakan.
- **Overlap check.** `figures.save()` gagal kalau ada teks yang bertumpuk. Untuk gambar screenshot, pengecekan ini dimatikan (`check=False`).
- **Gambar 9-10 adalah screenshot purwarupa React** dari `../web` (390 x 844 @2x, state demo: 3 huruf dikuasai, 5 hari belajar). Untuk memperbaruinya: `npm run build && npm run preview` di `../web`, buka tiap rute (`/`, `/peta`, `/huruf/ba`, `/latihan/ba`, `/mirip/0`, `/mushaf/1?huruf=ba`) dengan viewport 390 x 844 dan skala 2, lalu simpan PNG 780 x 1688 px ke `script/screens/png/` (`Main`, `Peta`, `Pelajaran`, `Latihan`, `Mirip`, `Mushaf`). `../app/tool/capture.py` hanya untuk MVP Flutter lama. Hapus `figures/fig09*.png` dan `fig10*.png`, lalu `python build.py`. Mockup lama tetap ada di `script/screens/src/` sebagai arsip desain; `render_screens` tidak menimpa PNG yang lebih baru dari sumbernya.
- **PDF dibuat di instans Word terpisah** (`DispatchEx`), sehingga Word yang sedang kamu pakai tidak ikut tertutup. Kalau `Proposal_DAQ_Makhraj.docx` sedang terbuka, build menyimpan hasilnya sebagai `...-terbaru.docx/pdf`.

## Yang masih harus diisi atau diverifikasi tim

1. Semua tautan di Tabel 4 (Dokumentasi) (video, aplikasi web, APK, GitHub, purwarupa, folder foto).
2. Gambar 8 dan Gambar B sudah memakai screenshot MVP; perbarui kalau tampilan aplikasi berubah.
3. Hasil uji coba nyata. Bagian 5.4 masih berupa **rencana** evaluasi. Kalau uji dengan 20 pengguna sudah dilakukan, tambahkan hasilnya karena ini memperkuat aspek Proses.
4. Pengajar tahsin bersanad yang akan memvalidasi materi (5.3), dan wawancara pemula/pengajar (5.2). Keduanya masih ditulis sebagai rencana.
5. Izin kanal Al-Andalasy (daftar putar "Tahsin Camp") dan kanal resmi Dr. Ayman Swaid (ض, ط); hanya ا yang belum punya klip dan izin LPMQ untuk terjemah Kemenag. Proposal menyatakan izin kanal diajukan sebelum rilis publik.
6. Tabel 3 (pembanding): fitur pesaing dicek dari informasi publik. Sebaiknya coba langsung ngaji.ai, Tarteel, dan Qur'an Kemenag sebelum dikirim.
7. Materi makhraj sudah dicocokkan dengan *Fath Rabb al-Bariyyah* (`../validasi-materi-fath-rabb.md`, Lampiran 1); 4 usulan perbaikan `materi.json` menunggu persetujuan guru.
8. Proyeksi biaya-pendapatan (Lampiran 3, Tabel C) adalah asumsi tim: harga paket Rp20.000, bagi hasil 70/30, konversi 1%, lisensi Rp300.000/kelas. Sesuaikan kalau tim punya angka lain.
9. Surat pernyataan orisinalitas memuat klausul "tidak dibuat dengan bantuan kecerdasan buatan dalam bentuk apa pun". Putuskan bersama apakah bisa ditandatangani dengan jujur.
10. Butir SUS di aplikasi masih terjemahan kerja; ganti dengan versi Sharfina & Santoso (2016) sebelum studi resmi (Lampiran 8).
11. PP 33/2026 (peraturan pelaksana UU PDP) baru dikutip dari pemberitaan Kompas; cocokkan pasal dengan teks resmi JDIH (Lampiran 10).
12. Biaya Firebase di Tabel C/D dan `FIN_*` sudah direvisi (19 Okt 2026) memakai perkiraan riset React: sekitar US$25 per bulan pada 30 ribu MAU dan US$85 per bulan pada 100 ribu MAU, kurs Rp16.000, tanpa biaya Auth di atas 50 ribu MAU (perkiraan riset ≈US$275 per bulan, belum terverifikasi). Akibatnya selisih Tahun 2 menjadi +0,2, Tahun 3 +6,4, titik impas 0,73%, dan skenario pesimis −9,4. Verifikasi tarif asia-southeast2 di Google Cloud Pricing Calculator.
13. Bagian 6.3 sekarang menyatakan pemeliharaan "dirancang beralih bertahap ke UKM kerohanian kampus". Pastikan rencana ini disetujui atau setidaknya dibicarakan dengan UKM sebelum presentasi, dan bila bisa minta surat minat (dilampirkan, bukan di Bagian 1-10).
14. Paragraf tema (akhir Bagian 3) mengutip tema MTQMN XVIII 2025. Kalau panduan MTQMN 2026 terbit dengan tema baru, ganti kalimat pertamanya dan rujukan Direktorat Pembelajaran dan Kemahasiswaan.
15. Simulasi penilaian juri dan daftar pekerjaan yang hanya bisa diselesaikan tim (APK, uji *think-aloud*, nama pengajar validator, izin kanal, pelajaran rinci 12 huruf pasangan mirip, uji langsung aplikasi pesaing) ada di `../../../reports/Review juri proposal Makhraj.md`.

## Checklist sebelum selesai

- [ ] `python build.py` lolos tanpa error (checks lolos, tidak ada overlap teks di gambar)
- [ ] Status batas halaman `AMAN`
- [ ] Buka `_preview/sheet.png`: tidak ada gambar terpotong, keterangan tidak terpisah dari gambarnya, tidak ada judul bagian yatim di bawah halaman
- [ ] Buka DOCX di Word: jumlah halaman sama dengan PDF
- [ ] Tidak ada em dash (dicek otomatis)
- [ ] Placeholder `[...]` sudah diisi sebelum dikirim

## Sumber data utama

Survei literasi Al-Qur'an Kemenag dan LK3P UI 2023 (NU Online, 2023; Asrori, 2023), penduduk Muslim semester I 2024 (Databoks, 2024), penetrasi internet APJII 2025 (Bisnis.com, 2025), ngaji.ai (Suryo, 2024; Infobank, 2025), Tarteel, kebijakan YouTube API, dan lisensi Tanzil. Daftar lengkap ada di `script/references.py`.
