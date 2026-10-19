# Naskah dan storyboard video karya Makhraj

Target durasi **8 menit 40 detik** (syarat DAQ: 7-10 menit). Isi wajib menurut Panduan MTQMN XVIII hlm. 30 butir g:
profil regu, deskripsi singkat aplikasi, bagaimana aplikasi dimanfaatkan, dan bagaimana aplikasi digunakan pengguna.

## Aturan rekaman (Panduan hlm. 17, 30-31)

- **Jangan** ada nama, logo, jas almamater, atau bendera perguruan tinggi di video, termasuk di latar, slide, dan
  teks layar. Sebut nama anggota saja, tanpa nama kampus.
- Kirim lewat tautan Google Drive dengan akses terbuka.
- Narasi dan wajah di video direkam oleh tim sendiri. Rekaman layar di folder `rekaman/` adalah tangkapan aplikasi
  asli yang sedang dipakai, bukan animasi buatan.
- Klip Syaikh Aiman di dalam aplikasi adalah video YouTube milik kanal lain. Tampilkan sebentar saja (maksimal
  beberapa detik, tanpa suara penuh) atau minta izin kanal dulu sebelum suaranya ikut terekam di video karya.
- Keputusan tentang klausul surat orisinalitas tetap di tangan tim.

## Ringkasan bagian

| No | Waktu | Bagian | Isi wajib |
|---|---|---|---|
| 1 | 0:00-0:25 | Pembuka | |
| 2 | 0:25-1:15 | Profil regu | profil regu |
| 3 | 1:15-2:35 | Masalah dan gagasan | deskripsi singkat |
| 4 | 2:35-3:40 | Siapa memakai dan untuk apa | bagaimana dimanfaatkan |
| 5 | 3:40-7:20 | Demo aplikasi | bagaimana digunakan |
| 6 | 7:20-8:10 | Proses, validasi, dan rencana | bagaimana dimanfaatkan (keberlanjutan) |
| 7 | 8:10-8:40 | Penutup | |

## Storyboard

Kolom "Rekaman" merujuk berkas di `rekaman/` (dibuat dengan `rekam_layar.py`) atau rekaman yang harus diambil tim.

### 1. Pembuka (0:00-0:25)

| Visual | Narasi |
|---|---|
| Layar hitam, lalu ikon Makhraj (huruf ب putih di kotak teal). Teks: "Makhraj". | "Bismillahirrahmanirrahim. Assalamu'alaikum warahmatullahi wabarakatuh." |
| Teks layar: "Aplikasi tahsin berbasis visualisasi makhraj dan rujukan guru bersanad". | "Kami memperkenalkan Makhraj, aplikasi untuk belajar huruf hijaiah dari tempat keluarnya." |

Rekaman: ikon dari `paper/script/figures/cover_icon.png`.

### 2. Profil regu (0:25-1:15)

| Visual | Narasi |
|---|---|
| Kedua anggota di depan kamera, latar polos, tanpa atribut kampus. | "Kami regu yang terdiri dari dua orang. Saya Faiz Iqbal I'tishom, mengerjakan rancangan materi dan pengembangan aplikasi." |
| Anggota kedua. | "Saya M. Zahran Rahmandhina, mengerjakan desain antarmuka, pengujian, dan analisis pasar." |
| Keduanya. | "Kami berdua juga masih belajar memperbaiki bacaan. Dari situ kami tahu rasanya ingin belajar, tetapi canggung atau tidak sempat datang ke majelis." |

Catatan: sesuaikan pembagian peran dengan yang sebenarnya.

### 3. Masalah dan gagasan (1:15-2:35)

| Visual | Narasi |
|---|---|
| Grafik literasi (`paper/script/figures/fig01_literasi.png`). | "Survei Kemenag dan LK3P UI tahun 2023 terhadap lebih dari sepuluh ribu responden menunjukkan 61,51 persen mengenal huruf dan harakat, tetapi hanya 44,57 persen yang mampu membaca lancar sesuai tajwid." |
| Teks layar: "22,2% tidak punya majelis BTQ di sekitar rumah". | "Lebih dari seperlima responden bahkan tidak punya majelis baca tulis Al-Qur'an di sekitar tempat tinggalnya." |
| Tabel pembanding (Tabel 3 proposal) atau dua kotak: "apakah salah" dan "mengapa salah". | "Aplikasi yang ada sudah bisa memberi tahu apakah bacaan salah. Pemula juga perlu tahu mengapa salah: dari titik mana huruf seharusnya keluar dan bagaimana membetulkannya." |
| `rekaman/01_beranda_peta.webm` (cuplikan penampang). | "Makhraj menjawabnya dengan penampang mulut dan tenggorokan yang menyorot titik makhraj, contoh pelafalan dari Asy-Syaikh Aiman Rusydi Suwaid, dan latihan yang meniru talaqqi." |

### 4. Siapa memakai dan untuk apa (2:35-3:40)

| Visual | Narasi |
|---|---|
| Gambar alur lima langkah (`fig02_alur_belajar.png`). | "Alurnya mengikuti talaqqi: lihat, dengar, tiru, bandingkan, dan terapkan." |
| Teks layar tiga segmen. | "Pengguna utamanya pemula segala usia: mahasiswa dan pekerja muda, orang tua yang mendampingi anak, serta mualaf dan lansia." |
| Teks layar: "TPQ, majelis taklim, tutorial BTQ kampus". | "Bagi pengajar dan lembaga, Makhraj menghemat waktu menjelaskan makhraj, sehingga pertemuan tatap muka bisa dipakai untuk mengoreksi." |
| Peta jalan (`fig04_roadmap.png`). | "Inti pembelajaran tetap gratis. Pada tahap berikutnya, pengguna dapat menyetor bacaan kepada pengajar mitra, dan lembaga dapat memakai dasbor kelas." |

### 5. Demo aplikasi (3:40-7:20)

Rekam dari ponsel sungguhan bila APK sudah ada; kalau belum, pakai rekaman layar web di `rekaman/`.

| Waktu | Visual | Narasi | Rekaman |
|---|---|---|---|
| 3:40 | Beranda. | "Di beranda, pengguna melihat pelajaran berikutnya, jumlah huruf yang dikuasai, dan hari belajar pekan ini. Hitungan hari ini bisa disembunyikan; Makhraj tidak memakai papan peringkat." | `01_beranda_peta.webm` |
| 4:05 | Peta makhraj: ketuk area dan titik. | "Peta makhraj menunjukkan lima area dan tujuh belas titik tempat keluarnya huruf. Ketuk sebuah titik untuk melihat huruf yang keluar dari sana." | `01_beranda_peta.webm` |
| 4:35 | Pelajaran ح langkah Lihat. | "Kita ambil huruf ha. Langkah pertama, lihat: titiknya di tengah tenggorokan. Sifat huruf ditampilkan beserta kesalahan yang sering terjadi." | `02_pelajaran_ha.webm` |
| 5:05 | Langkah Dengar (klip tampil sebentar). | "Langkah kedua, dengar: contoh pelafalan dari Syaikh Aiman, yang bisa diputar per harakat." | `02_pelajaran_ha.webm` |
| 5:25 | Langkah Tiru: cermin dan rekam. Rekam dari ponsel tim. | "Langkah ketiga, tiru: pengguna menyalakan cermin kamera untuk melihat gerak mulutnya, lalu merekam bacaannya. Rekaman hanya tersimpan di perangkat." | rekam tim |
| 5:55 | Langkah Bandingkan. | "Langkah keempat, bandingkan: rekaman diputar bergantian dengan contoh guru, lalu pengguna mengisi daftar cek." | `02_pelajaran_ha.webm` + rekam tim |
| 6:15 | Langkah Terapkan. | "Langkah kelima, terapkan: huruf itu dicari di dalam ayat." | `02_pelajaran_ha.webm` |
| 6:30 | Huruf mirip ح-ه dan kuis. | "Fitur huruf mirip menaruh dua penampang berdampingan. Pengguna melihat bedanya, lalu menjawab kuis." | `03_huruf_mirip.webm` |
| 6:55 | Mushaf dengan sorot huruf. | "Di mushaf, kata yang memuat huruf yang dipelajari disorot tanpa mengubah teks Al-Qur'an. Teks berasal dari Tanzil, dan terjemahannya diberi label sumber." | `04_mushaf.webm` |
| 7:10 | Menu Saya: uji coba. | "Untuk uji coba, aplikasi sudah menyediakan lembar persetujuan, tes sebelum dan sesudah, kuesioner kegunaan, dan ekspor data." | `05_uji_coba.webm` |

### 6. Proses, validasi, dan rencana (7:20-8:10)

| Visual | Narasi |
|---|---|
| Lampiran 1 proposal (tabel pencocokan) atau kitab *Fath Rabb al-Bariyyah*. | "Materi kami cocokkan dengan Fath Rabb al-Bariyyah, syarah Al-Muqaddimah al-Jazariyyah. Selama belum ditinjau pengajar bersanad, setiap pelajaran memberi label 'belum divalidasi pengajar'." |
| Foto atau rekaman konsultasi dengan pengajar (bila sudah ada). | "[Isi setelah konsultasi: siapa pengajarnya dan apa hasilnya.]" |
| Teks layar rencana uji. | "Kami merencanakan uji dua pekan dengan dua puluh pemula dewasa: tes pemahaman sebelum dan sesudah, kuesioner kegunaan, dan rekaman yang dinilai dua pengajar." |
| Peta jalan. | "Tahap berikutnya adalah setoran bacaan kepada pengajar, lalu penilaian otomatis yang dibangun dari rekaman yang sudah dikoreksi pengajar." |

### 7. Penutup (8:10-8:40)

| Visual | Narasi |
|---|---|
| Kedua anggota. | "Rasulullah saw. bersabda bahwa orang yang membaca Al-Qur'an dengan terbata-bata karena berat mendapat dua pahala. Semoga Makhraj membantu lebih banyak orang memulai langkah itu." |
| Ikon dan teks "Makhraj". | "Wassalamu'alaikum warahmatullahi wabarakatuh." |

## Daftar periksa sebelum unggah

- [ ] Durasi 7-10 menit.
- [ ] Empat isi wajib ada: profil regu, deskripsi, pemanfaatan, cara pakai.
- [ ] Tidak ada nama atau atribut perguruan tinggi di gambar, suara, dan teks layar.
- [ ] Klip YouTube Syaikh Aiman hanya tampil singkat, atau izin kanal sudah ada.
- [ ] Angka di narasi sama dengan proposal (61,51%; 44,57%; 22,2%; 5 area; 17 titik; 29 huruf).
- [ ] Tautan Google Drive dibuka untuk umum dan dicoba dari akun lain.
