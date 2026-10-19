"""Isi proposal. SATU-SATUNYA sumber teks untuk DOCX dan PDF.

Jenis blok:
  ("h1", teks)                      judul bagian bernomor
  ("h2", teks)                      subbagian
  ("p", teks)                       paragraf rata kanan-kiri, indentasi baris pertama
  ("p0", teks)                      paragraf tanpa indentasi
  ("list", [teks, ...], "1"|"-")    daftar bernomor atau berbutir
  ("fig", kunci, file, keterangan, lebar_cm)
  ("table", kunci, keterangan, header, baris, lebar_kolom_cm)
  ("pagebreak",)

Format inline: **tebal**, *miring*. Jangan menyarangkan *miring* di dalam **tebal** (tanda bintang
akan tercetak). Rujukan silang: {fig:kunci} dan {tab:kunci} diganti nomor gambar/tabel saat build.
Gambar dan tabel di BODY bernomor (1, 2, ...), sedangkan di LAMPIRAN berhuruf (A, B, ...).
Jangan memakai em dash; checks.py menolaknya.

Kaidah penulisan (EYD V dan KBBI):
- Huruf miring: istilah asing atau Arab yang belum diserap (talaqqi, jahr, sprint, use case),
  judul kitab dan buku, serta lambang statistik (p, r). Kata serapan KBBI (tajwid, tartil, mushaf,
  harakat, hijaiah, sanad, syarah, dasbor, progres) tidak dimiringkan.
- Singkatan ditulis lengkap pada pemakaian pertama: MTQMN, Kemenag, BTQ, TPQ, AI, SUS, TAM/SAM/SOM,
  ZISWAF, CSR, LPMQ, LAZ, UKM.
- Bilangan yang dapat ditulis dengan satu atau dua kata ditulis dengan huruf, kecuali dalam
  perincian, tabel, persentase, nilai uang, dan satuan waktu.
- "swt." dan "saw." ditulis huruf kecil dengan titik.

BODY (bagian 1-10) + Daftar Pustaka harus muat dalam 10 halaman bernomor.
Materi pendukung yang tidak muat diletakkan di LAMPIRAN, setelah Daftar Pustaka.
"""

COVER = {
    "event": "PROPOSAL\nMUSABAQAH DESAIN APLIKASI KOMPUTER AL-QUR'AN (DAQ)",
    "title": "MAKHRAJ",
    "subtitle": "Aplikasi Tahsin Berbasis Visualisasi Makhraj dan Rujukan Guru Bersanad\nbagi Pemula Pembaca Al-Qur'an",
    "authors_label": "Disusun oleh:",
    "authors": ["Faiz Iqbal I'tishom (164231059)", "M. Zahran Rahmandhina (164241070)"],
    "participant": "",
    "footer": "MUSABAQAH TILAWATIL QUR'AN MAHASISWA\nUNIVERSITAS AIRLANGGA\nSURABAYA\n2026",
}

BODY = [
    # ------------------------------------------------------------------ 1
    ("h1", "1. Judul Aplikasi"),
    ("p0", "**Makhraj: Aplikasi Tahsin Berbasis Visualisasi Makhraj dan Rujukan Guru Bersanad bagi Pemula Pembaca Al-Qur'an**"),
    ("p",
     "Makhraj adalah aplikasi Android dan web untuk siapa saja yang baru mulai belajar membaca Al-Qur'an, "
     "dari anak bersama pendampingnya hingga orang dewasa dan lansia. Nama aplikasi diambil dari istilah "
     "tajwid *makhraj*, yaitu tempat keluarnya huruf. Setiap huruf hijaiah dipelajari dari tempat "
     "keluarnya: pengguna melihat penampang mulut dan tenggorokan yang menyorot titik makhraj, mendengar "
     "contoh pelafalan dari Asy-Syaikh Aiman Rusydi Suwaid, merekam dan membandingkan bacaannya sendiri, "
     "lalu menemukan huruf yang sama di dalam mushaf. Dengan cara ini, setiap kesalahan bacaan dapat "
     "ditelusuri sampai ke bagian mulut tempat kesalahan itu terjadi."),

    # ------------------------------------------------------------------ 2
    ("h1", "2. Latar Belakang"),
    ("p",
     "Allah swt. memerintahkan agar Al-Qur'an dibaca dengan tartil (QS. Al-Muzzammil [73]: 4). Rasulullah saw. "
     "menyebut orang terbaik sebagai orang yang belajar Al-Qur'an dan mengajarkannya (HR. Al-Bukhari no. 5027) "
     "dan menjanjikan dua pahala bagi orang yang membacanya dengan terbata-bata karena merasa berat "
     "(HR. Al-Bukhari no. 4937; Muslim no. 798). Pemula yang terbata-bata pun berpahala; yang mereka perlukan "
     "adalah tempat belajar yang mudah dijangkau. Tema Musabaqah Tilawatil "
     "Qur'an Mahasiswa Nasional (MTQMN), yaitu penguatan karakter Qurani mahasiswa yang berdampak (Direktorat "
     "Pembelajaran dan Kemahasiswaan, 2025), juga bertumpu pada kemampuan paling dasar itu: membaca Al-Qur'an "
     "dengan benar."),
    ("p",
     "Kemampuan itu belum merata. Survei Potensi Literasi Al-Qur'an oleh Kementerian Agama (Kemenag) dan LK3P "
     "Universitas Indonesia terhadap 10.347 responden di 34 provinsi (NU Online, 2023) menunjukkan angka "
     "yang turun pada setiap jenjang kemampuan (Gambar {fig:literasi}). Sebanyak 61,51% responden mengenal huruf "
     "dan harakat, tetapi yang mampu membaca dengan lancar sesuai tajwid hanya 44,57%, dan 38,49% responden belum "
     "memiliki literasi baca Al-Qur'an (Asrori, 2023). Selisih hampir 17 poin itu menunjukkan banyaknya orang yang "
     "sudah mengenal huruf, tetapi bacaannya belum sesuai tajwid."),
    ("fig", "literasi", "fig01_literasi.png",
     "Kemampuan baca Al-Qur'an masyarakat Indonesia (diolah dari Asrori, 2023)", 11.0),
    ("p",
     "Akses belajar juga terbatas. Survei yang sama mencatat 22,2% responden tidak memiliki majelis "
     "baca tulis Al-Qur'an (BTQ) di sekitar tempat tinggalnya dan 59,36% tidak pernah mengikuti majelis "
     "tersebut (Asrori, 2023). Orang dewasa menghadapi hambatan tambahan, seperti rasa canggung belajar "
     "bersama anak-anak di taman pendidikan Al-Qur'an (TPQ), jadwal kerja atau kuliah yang padat, dan jarak "
     "ke guru. Lingkungan kampus pun mengalami hal serupa: dosen agama di Universitas Lambung Mangkurat "
     "menemukan lebih dari 60% mahasiswa baru belum bisa mengaji pada 2021 (Suryo, 2024)."),
    ("p",
     "Di sisi lain, 80,66% penduduk Indonesia telah terhubung ke internet (Bisnis.com, 2025), dan aplikasi "
     "belajar mengaji sudah memiliki pengguna. Aplikasi ngaji.ai menilai bacaan dengan teknologi pengenalan "
     "suara dan telah diunduh ratusan ribu kali sejak Maret 2024 (Infobank, 2025), sedangkan Tarteel mendeteksi "
     "kata yang terlewat atau keliru saat pengguna menghafal (Tarteel, t.t.). Kedua aplikasi tersebut unggul "
     "dalam memberi tahu *apakah* bacaan salah. Pemula juga perlu tahu *mengapa* bacaannya salah: dari titik "
     "mana huruf seharusnya keluar dan bagaimana membetulkannya. Ilmu tajwid menjelaskannya melalui makhraj "
     "dan sifat huruf, tetapi penjelasan itu umumnya hanya tersedia di kitab atau di majelis tatap muka. "
     "Tabel {tab:celah} merangkum tiga celah yang menjadi pijakan Makhraj."),
    ("table", "celah", "Tiga celah yang dijawab Makhraj",
     ["Celah", "Kondisi saat ini", "Yang ditawarkan Makhraj"],
     [
         ["Kebutuhan pemula",
          "Belajar bergantung pada guru dan majelis; 22,2% responden tidak memiliki majelis BTQ; orang dewasa sering canggung",
          "Belajar mandiri kapan saja dengan urutan yang meniru *talaqqi*, lalu bertahap terhubung ke pengajar"],
         ["Kompetitor",
          "Aplikasi yang ada menilai benar atau salah; letak makhraj tidak menjadi inti materi",
          "Penampang mulut dan tenggorokan interaktif untuk setiap huruf, lengkap dengan sifat dan kesalahan umum"],
         ["Rujukan keilmuan",
          "Contoh suara sering tidak menyebut identitas guru ataupun sanadnya",
          "Contoh dari Asy-Syaikh Aiman Rusydi Suwaid, ulama *qiraat* penyusun kitab *At-Tajwid al-Mushawwar*"],
     ],
     [3.0, 6.1, 6.4]),
    ("p",
     "Studi awal Katz dan Mehta (2015) pada lima peserta menemukan bahwa umpan balik visual gerak lidah "
     "membantu peserta mengucapkan bunyi baru dengan lebih akurat, sedangkan prinsip multimedia Mayer (2009) menyatakan bahwa "
     "orang belajar lebih baik dari kata dan gambar daripada dari kata saja. Tradisi tajwid pun memakai gambar: "
     "Syaikh Aiman menyusun *At-Tajwid al-Mushawwar*, kitab tajwid bergambar (Suwaid, 2014), dan syarah "
     "*Al-Muqaddimah al-Jazariyyah* menyertakan penampang mulut untuk menunjukkan letak makhraj (Salim, 2007). "
     "Makhraj memakai bentuk yang lebih sederhana dan murah daripada alat pelacak lidah, yaitu penampang yang "
     "menyorot titik makhraj ditambah cermin kamera untuk gerak bibir, lalu menambahkan latihan harian. Efek "
     "bentuk sederhana ini diuji pada evaluasi MVP (Subbab 5.4)."),

    # ------------------------------------------------------------------ 3
    ("h1", "3. Tujuan dan Manfaat"),
    ("p0", "Tujuan pengembangan Makhraj adalah sebagai berikut."),
    ("list", [
        "Membangun produk layak minimum atau *minimum viable product* (MVP) untuk Android dan web dari satu basis "
        "kode yang mengajarkan 29 huruf hijaiah (28 huruf dan hamzah) melalui 5 area dan 17 titik makhraj.",
        "Menyediakan alur latihan mandiri lihat, dengar, tiru, bandingkan, dan terapkan dengan contoh pelafalan "
        "dari guru bersanad.",
        "Menghubungkan setiap pelajaran huruf dengan mushaf melalui fitur sorot huruf sehingga materi langsung "
        "dipraktikkan pada ayat.",
        "Mengukur dampak MVP melalui uji kegunaan dan uji pemahaman makhraj sebelum dan sesudah pemakaian.",
    ], "1"),
    ("p0", "Manfaat yang diharapkan adalah sebagai berikut."),
    ("list", [
        "**Bagi pemula segala usia:** belajar dari dasar tanpa rasa canggung dan memahami alasan sebuah huruf "
        "dibaca dengan cara tertentu.",
        "**Bagi pengajar dan lembaga** (TPQ, majelis taklim, dan tutorial baca Al-Qur'an di kampus): media bantu "
        "yang menghemat waktu menjelaskan makhraj sehingga pertemuan tatap muka dapat difokuskan pada koreksi.",
        "**Bagi mahasiswa:** sarana memperbaiki bacaan sendiri sekaligus wadah menjadi relawan pengajar ketika "
        "fitur setor bacaan dibuka pada Tahap 2.",
        "**Bagi pengembangan ilmu:** pada Tahap 3, rekaman yang sudah dikoreksi pengajar dan disetujui pemiliknya "
        "dapat menjadi korpus riset pengenalan bacaan Al-Qur'an oleh penutur Indonesia.",
    ], "-"),
    ("p",
     "Makhraj menjawab tema MTQMN, yaitu penguatan karakter Qurani mahasiswa yang berdampak menuju Indonesia "
     "Emas, melalui tiga peran mahasiswa: yang membangun aplikasinya, yang memakainya untuk memperbaiki bacaan, "
     "dan yang kelak menjadi pengajar. Karakter itu dilatih lewat desainnya: istiqamah melalui latihan harian "
     "yang kecil, adab kepada guru melalui rujukan bersanad tanpa papan peringkat, dan kepedulian melalui bacaan "
     "yang sudah diperbaiki untuk membantu orang lain. Generasi yang membaca Al-Qur'an dengan benar dan mau "
     "mengajarkannya adalah bagian dari bekal Indonesia Emas 2045."),

    # ------------------------------------------------------------------ 4
    ("h1", "4. Batasan"),
    ("list", [
        "Sasaran utama adalah pemula yang belum bisa atau belum lancar membaca Al-Qur'an. Pengguna anak "
        "memakai aplikasi bersama orang tua atau pengajar.",
        "Teks Al-Qur'an memakai rasm Utsmani riwayat Hafsh dari 'Ashim, bersumber dari Tanzil. Tashih ke Lajnah "
        "Pentashihan Mushaf Al-Qur'an (LPMQ) diajukan sebelum rilis publik.",
        "Materi MVP mencakup makhraj dan sifat 29 huruf, harakat dasar, serta enam pasangan huruf yang sering "
        "tertukar (ح-ه, ث-س, ذ-ز, ص-س, ق-ك, ع-ء). Hukum tajwid lanjutan dibahas pada tahap berikutnya.",
        "MVP belum menilai bacaan secara otomatis. Pengguna menilai bacaannya sendiri dengan bantuan pembanding "
        "suara, cermin kamera, dan daftar periksa. Koreksi oleh pengajar (Tahap 2) dan penilaian berbasis "
        "kecerdasan buatan atau *artificial intelligence* (AI) (Tahap 3) dirancang bertahap (Lampiran 9).",
        "Contoh pelafalan diambil dari daftar putar latihan makhraj Syaikh Aiman di kanal Al-Andalasy "
        "(Al-Andalasy, t.t.); klip ض dan ط diambil dari kanal resmi Dr. Ayman Swaid (Suwaid, t.t.), sehingga "
        "28 dari 29 huruf memiliki klip dan hanya ا yang belum. "
        "Klip diputar melalui pemutar resmi YouTube tanpa diunduh atau disimpan, sesuai dengan kebijakan "
        "pengembang YouTube (Google, t.t.). Izin pemakaian diajukan kepada pengelola kanal sebelum rilis publik.",
        "Makhraj tidak menggantikan guru. Aplikasi ini menyiapkan pemula sebelum dan di antara pertemuan "
        "*talaqqi* dengan guru.",
    ], "1"),

    # ------------------------------------------------------------------ 5
    ("h1", "5. Metode"),
    ("h2", "5.1 Metode Pembelajaran: *Talaqqi* Digital"),
    ("p",
     "Al-Qur'an diajarkan secara *talaqqi* dan *musyafahah*: murid melihat gerak mulut guru, mendengar, "
     "menirukan, lalu dikoreksi. Makhraj menerjemahkan urutan tersebut ke dalam lima langkah, yaitu lihat, "
     "dengar, tiru, bandingkan, dan terapkan (Gambar {fig:alur}). Pengguna melihat letak makhraj, mendengar klip "
     "Syaikh Aiman, merekam bacaannya dengan bantuan cermin kamera, membandingkannya dengan contoh guru, lalu "
     "mencari huruf itu di dalam ayat. Langkah keempat kelak bercabang ke pengajar ketika fitur setor bacaan dibuka."),
    ("fig", "alur", "fig02_alur_belajar.png", "Alur belajar *talaqqi* digital pada Makhraj", 13.4),
    ("h2", "5.2 Metode Pengembangan Perangkat Lunak"),
    ("p",
     "Pengembangan menggabungkan *design thinking* (Brown, 2008) untuk memahami masalah pengguna dan Scrum "
     "(Schwaber & Sutherland, 2020) untuk membangun MVP secara bertahap. Tahap empati dan definisi bertumpu "
     "pada kajian data literasi di atas; wawancara dengan pemula dan pengajar dilakukan bersamaan dengan uji "
     "pengguna (Subbab 5.4). Tahap ideasi dan purwarupa menghasilkan desain enam layar yang kini berjalan "
     "sebagai MVP (Bagian 9). MVP dikembangkan dalam empat *sprint* dua mingguan: (1) data mushaf dan materi "
     "huruf, (2) peta makhraj dan pelajaran lima langkah, (3) rekam, cermin, dan bandingkan, serta (4) huruf mirip, "
     "progres, dan perangkat uji coba. Purwarupa pertama dibuat dengan Flutter, lalu dipindah ke React agar web "
     "dan APK memakai satu hasil *build* (Lampiran 6)."),
    ("h2", "5.3 Penyusunan dan Validasi Materi"),
    ("p",
     "Materi makhraj dan sifat huruf disusun dari matan *Al-Muqaddimah al-Jazariyyah* karya Ibnu al-Jazari "
     "beserta syarahnya, *Fath Rabb al-Bariyyah* (Salim, 2007), dan kitab *At-Tajwid al-Mushawwar* "
     "(Suwaid, 2014). Validasi berjalan dua lapis. Lapis pertama adalah pencocokan data materi aplikasi dengan "
     "bab \"Makharij al-Huruf\" dan \"Shifat al-Huruf\" dalam *Fath Rabb al-Bariyyah*. Dari 14 butir yang "
     "diperiksa, 10 butir sesuai dan 4 butir perlu disesuaikan, misalnya letak *khaisyum* yang semula ditulis \"pangkal "
     "hidung\", padahal kitab menyebut rongga hidung bagian dalam (Lampiran 1). Lapis kedua adalah tinjauan "
     "pengajar tahsin bersanad; selama tinjauan ini belum selesai, setiap pelajaran di aplikasi memuat label "
     "\"belum divalidasi pengajar\"."),
    ("h2", "5.4 Rencana Evaluasi"),
    ("p",
     "Sebelum uji lapangan, lima sampai delapan calon pengguna mencoba MVP sambil menyuarakan pikirannya "
     "(*think-aloud*) agar masalah kegunaan diperbaiki lebih dulu. Uji lapangan memakai desain praeksperimen satu "
     "kelompok dengan tes awal dan tes akhir (*one-group pretest-posttest design*; Creswell & Creswell, 2018). Dua "
     "puluh pemula berusia minimal 18 tahun, yaitu mahasiswa dan masyarakat umum, dipilih secara purposif dan memakai "
     "MVP selama dua pekan setelah memberikan persetujuan. Tes pemahaman memakai dua bentuk paralel (A dan B) yang "
     "diperiksa pengajar tahsin, sedangkan rekaman bacaan dinilai dua pengajar secara terpisah tanpa mengetahui "
     "urutan rekaman, dengan kesepakatan antarpenilai diukur memakai koefisien kappa (Cohen, 1960). Karena tanpa "
     "kelompok kontrol, hasilnya diperlakukan sebagai bukti awal. Kegunaan diukur dengan *System Usability Scale* "
     "(SUS; Brooke, 1996) versi Indonesia; indikator lainnya disajikan pada Tabel {tab:evaluasi} dan rancangan "
     "lengkapnya pada Lampiran 8."),
    ("table", "evaluasi", "Rencana evaluasi MVP",
     ["Aspek", "Instrumen", "Target"],
     [
         ["Kegunaan", "SUS, 10 butir", "Rata-rata minimal 68 (Sauro & Lewis, 2016)"],
         ["Pemahaman makhraj", "Tes 20 soal bentuk A/B, awal dan akhir", "Naik bermakna (Wilcoxon, *p* < 0,05; efek *r*)"],
         ["Kualitas bacaan", "10 kata, rubrik, dua penilai", "Kesalahan menurun; kappa minimal 0,60"],
         ["Keterlibatan", "Catatan pemakaian", "Minimal 50% peserta aktif 4 hari per pekan"],
     ],
     [3.3, 4.6, 7.6]),

    # ------------------------------------------------------------------ 6
    ("h1", "6. Market Analisis"),
    ("h2", "6.1 Segmen dan Ukuran Pasar"),
    ("p",
     "Penduduk Indonesia yang beragama Islam berjumlah 245,97 juta jiwa (Databoks, 2024). Dengan proporsi "
     "survei literasi, sekitar 136,3 juta orang belum membaca dengan lancar sesuai tajwid. Angka ini menjadi "
     "pasar total atau *total addressable market* (TAM), yang mencakup orang yang belum bisa membaca sama sekali "
     "dan orang yang sudah mengenal huruf tetapi bacaannya belum sesuai tajwid. Sekitar 110 juta di antaranya "
     "sudah terhubung ke internet sehingga dapat dijangkau aplikasi (*serviceable available market*, SAM). "
     "Target tiga tahun pertama ditetapkan 100 ribu pengguna aktif bulanan (*serviceable obtainable market*, SOM), "
     "atau kurang dari 0,1% SAM. Angka ini merupakan estimasi kasar yang masih mencakup anak usia dini sehingga berfungsi sebagai "
     "batas atas (Lampiran 2). Segmen yang dibidik meliputi mahasiswa dan pekerja muda, orang tua yang "
     "mendampingi anak, mualaf dan lansia, serta lembaga seperti TPQ dan tutorial baca Al-Qur'an di kampus."),
    ("h2", "6.2 Analisis Kompetitor"),
    ("p",
     "Tabel {tab:kompetitor} membandingkan Makhraj dengan tiga aplikasi yang paling dekat berdasarkan informasi "
     "publik per Oktober 2026; keterangan \"tidak\" berarti fitur tersebut tidak ditemukan dalam informasi publik. "
     "Posisi Makhraj terhadap ngaji.ai (Gambar {fig:pasar}, Lampiran 2) dapat diringkas sebagai berikut: ngaji.ai "
     "memberi tahu pengguna bahwa bacaannya salah, sedangkan Makhraj menunjukkan letak kesalahannya dan cara "
     "membetulkannya dengan contoh dari guru bersanad. Pembeda Makhraj ada pada perpaduan fitur dalam satu alur "
     "belajar, bukan pada satu fitur tunggal. Analisis SWOT dan mitigasinya disajikan pada Tabel {tab:swot} (Lampiran 2)."),
    ("table", "kompetitor", "Perbandingan fitur Makhraj dengan aplikasi sejenis",
     ["Fitur", "ngaji.ai", "Tarteel", "Qur'an Kemenag", "Makhraj"],
     [
         ["Mushaf lengkap", "Ada", "Ada", "Ada", "Ada"],
         ["Materi bertahap untuk pemula", "Ada", "Tidak", "Tidak", "Ada"],
         ["Visualisasi letak makhraj", "Tidak", "Tidak", "Tidak", "Ada"],
         ["Contoh pelafalan per huruf dari guru bersanad yang disebut namanya", "Tidak", "Tidak", "Tidak", "Ada"],
         ["Penilaian bacaan otomatis", "Ada", "Ada (per kata)", "Tidak", "Tahap 3"],
         ["Koreksi oleh pengajar manusia", "Tidak", "Tidak", "Tidak", "Tahap 2"],
         ["Sorot huruf yang baru dipelajari di mushaf", "Tidak", "Tidak", "Tidak", "Ada"],
     ],
     [6.3, 2.2, 2.4, 2.4, 2.2]),
    ("h2", "6.3 Model Bisnis dan Keberlanjutan"),
    ("p",
     "Inti pembelajaran, yaitu 29 pelajaran huruf, peta makhraj, rekam dan bandingkan, serta mushaf, tetap "
     "gratis karena merupakan bagian dari dakwah. Pendapatan berasal dari dua sumber: paket Setor ke Pengajar "
     "seharga Rp20.000 per lima setoran dengan bagi hasil 70% untuk pengajar tahsin dan lisensi dasbor lembaga "
     "Rp300.000 per kelas per tahun untuk TPQ, sekolah, dan tutorial kampus. Dana zakat, infak, sedekah, dan wakaf "
     "(ZISWAF) serta program tanggung jawab sosial perusahaan atau *corporate social responsibility* (CSR) "
     "membiayai setoran pengguna kurang mampu. Dengan asumsi 1% pengguna membeli empat paket per tahun, biaya tahun pertama "
     "sebesar Rp4,6 juta ditutup dengan dana tim atau hibah kemahasiswaan, tahun kedua mencapai impas, dan "
     "kas kumulatif menjadi positif pada tahun ketiga (Gambar {fig:roadmap}). Agar tidak bergantung pada tim, "
     "pemeliharaan dirancang beralih bertahap ke UKM kerohanian kampus, dan honor Rp2.800 per setoran menjadi "
     "tambahan bagi pengajar relawan, bukan nafkah utama. Pemetaan lengkapnya disajikan pada Lampiran 3."),
    ("fig", "roadmap", "fig04_roadmap.png", "Peta jalan dan ringkasan model bisnis Makhraj per tahap", 14.4),

    # ------------------------------------------------------------------ 7
    ("h1", "7. Desain"),
    ("h2", "7.1 *Use Case Diagram*"),
    ("p",
     "Sistem memiliki tiga aktor (Gambar {fig:usecase}). Pengguna dapat menjelajah peta makhraj, mempelajari "
     "huruf beserta klip guru, merekam dan membandingkan bacaan, berlatih huruf "
     "mirip, membaca mushaf dengan sorot huruf, melihat progres, dan mengikuti uji coba. Admin mengelola materi dan klip, sedangkan "
     "pengajar memvalidasi materi dan, pada Tahap 2, memberi koreksi atas rekaman yang disetor pengguna. "
     "*Use case* Tahap 2 ditandai dengan garis putus-putus."),
    ("fig", "usecase", "fig05_usecase.png", "Diagram *use case* Makhraj", 12.0),
    ("h2", "7.2 *Class Diagram*"),
    ("p",
     "Struktur kelas mengikuti susunan ilmu makhraj (Gambar {fig:class}). Kelas *AreaMakhraj* memuat beberapa "
     "*TitikMakhraj*, setiap titik menjadi tempat keluar satu atau lebih *Huruf*, dan setiap huruf memiliki "
     "banyak *Sifat* serta satu *Pelajaran* yang memuat potongan *KlipVideo*. Kelas *Pengguna* menyimpan "
     "*Progres* dan *Rekaman*, sedangkan *Setoran* dan *Koreksi* disiapkan untuk Tahap 2."),
    ("fig", "class", "fig06_class.png", "Diagram kelas Makhraj", 12.2),
    ("h2", "7.3 *Entity Relationship Diagram*"),
    ("p",
     "Gambar {fig:erd} menunjukkan model data konseptual dengan notasi *crow's foot*. Relasi banyak-ke-banyak "
     "antara huruf dan sifat dipecah melalui tabel *huruf_sifat*, sedangkan pasangan huruf mirip merujuk dua "
     "kali ke tabel huruf. Pada Tahap 2, setiap entitas dipetakan menjadi koleksi Cloud Firestore."),
    ("fig", "erd", "fig07_erd.png", "*Entity relationship diagram* (ERD) Makhraj", 10.0),

    # ------------------------------------------------------------------ 8
    ("h1", "8. Implementasi Teknologi"),
    ("p",
     "MVP Makhraj dibangun dengan React 19, TypeScript, dan Vite (Gambar {fig:arsitektur}). Satu hasil *build* "
     "dipasang sebagai web dan *progressive web app* (PWA) yang materi, peta makhraj, dan mushafnya tetap jalan "
     "tanpa internet (klip guru memerlukan koneksi), lalu dibungkus Capacitor menjadi aplikasi Android. Data pengguna tinggal di perangkat: progres di localStorage dan rekaman "
     "suara di IndexedDB. Firebase dipakai untuk *hosting* web; autentikasi dan sinkronisasi progres menyusul pada "
     "Tahap 2. Teks rasm Utsmani riwayat Hafsh dari Tanzil (CC BY 3.0) ditampilkan apa adanya beserta atribusinya "
     "(Tanzil Project, t.t.). Terjemahan Kemenag yang dipakai adalah edisi lama dari Tanzil yang hanya boleh "
     "dipakai secara nonkomersial, sehingga hanya tampil pada fitur inti yang gratis; izin LPMQ diajukan sebelum "
     "layanan berbayar Tahap 2 dibuka. "
     "Rincian fitur ada pada Tabel {tab:fitur} (Lampiran 4), sedangkan teknologi dan lisensi pada Lampiran 6 dan 7."),
    ("fig", "arsitektur", "fig08_arsitektur.png", "Arsitektur sistem Makhraj", 10.4),

    # ------------------------------------------------------------------ 9
    ("h1", "9. Tampilan Purwarupa"),
    ("p",
     "Gambar {fig:screens_a} menampilkan MVP React yang sudah berjalan: beranda dengan 29 ubin huruf (a), peta "
     "makhraj berisi 5 area dan 17 titik (b), dan pelajaran huruf ب (c). Setiap huruf dipelajari dalam lima "
     "langkah (lihat, dengar, tiru, bandingkan, terapkan), dan sifatnya dihitung otomatis dari matan "
     "*Al-Jazariyyah*. Antarmuka memenuhi kontras WCAG 2.2 AA dan memakai tombol minimal 48 px serta ukuran teks "
     "yang dapat diperbesar (Lampiran 11). Pelajaran rinci baru tersedia untuk ب, ح, dan ه. Menu Saya memuat perangkat uji coba: persetujuan peserta, tes A/B 20 soal, angket SUS, "
     "dan ekspor hasil. Layar lainnya disajikan pada Gambar {fig:screens_b} (Lampiran 5)."),
    ("fig", "screens_a", "fig09_screens_a.png", "Tampilan MVP Makhraj: beranda, peta makhraj, dan pelajaran huruf", 10.7),

    # ------------------------------------------------------------------ 10
    ("h1", "10. Dokumentasi"),
    ("p",
     "Tautan karya dan dokumentasi proses disajikan pada Tabel {tab:dokumentasi} dan dapat diakses tanpa kata sandi."),
    ("table", "dokumentasi", "Dokumentasi dan tautan karya",
     ["Butir", "Keterangan atau tautan"],
     [
         ["Video karya (7 hingga 10 menit)", "[tautan Google Drive]"],
         ["Aplikasi web dan APK Android", "[tautan Firebase Hosting]; [tautan Google Drive]"],
         ["Kode sumber dan purwarupa desain", "[tautan GitHub]; [tautan purwarupa]"],
         ["Foto perumusan masalah, konsultasi, dan uji coba", "[tautan folder foto]"],
     ],
     [7.0, 8.5]),
]

LAMPIRAN = [
    ("p0", "Lampiran ini berisi materi pendukung dan berada di luar batas 8-10 halaman isi proposal (Bagian 1-10 dan Daftar Pustaka)."),
    # ------------------------------------------------------------------ L1
    ("h2", "Lampiran 1. Hasil Pencocokan Materi dengan *Fath Rabb al-Bariyyah*"),
    ("p",
     "Data materi aplikasi dicocokkan dengan bab \"Makharij al-Huruf\" dan \"Shifat al-Huruf\" dalam *Fath Rabb "
     "al-Bariyyah* (Salim, 2007), syarah *Al-Muqaddimah al-Jazariyyah*. Tabel {tab:validasi} memuat seluruh butir "
     "yang diperiksa. Butir yang perlu disesuaikan masih berupa usulan dan baru diterapkan setelah disetujui "
     "pengajar tahsin bersanad. Beberapa rincian tidak dibahas dalam kitab ini, yaitu \"bagian bibir yang basah\" "
     "pada ب, perbandingan ب dengan bunyi /p/, perumpamaan bunyi ح dan ه, serta bentuk ilustrasi penampang. "
     "Rincian tersebut diperiksa dalam *At-Tajwid al-Mushawwar* dan dikonfirmasi kepada pengajar, sedangkan "
     "ilustrasi dibandingkan dengan gambar makhraj di dalam kitab."),
    ("table", "validasi", "Pencocokan materi aplikasi dengan *Fath Rabb al-Bariyyah*",
     ["Butir materi aplikasi", "Keterangan kitab", "Hasil"],
     [
         ["17 titik makhraj dalam 5 area (*jauf*, *halq*, *lisan*, *syafatain*, *khaisyum*)",
          "Pendapat yang dipilih: 17 makhraj khusus dalam 5 makhraj umum", "Sesuai"],
         ["*Al-jauf*: rongga mulut dan tenggorokan, tempat huruf mad (alif, wau, ya)",
          "Ruang kosong di dalam mulut dan tenggorokan; tempat alif, wau, dan ya mad", "Sesuai"],
         ["*Al-halq*: pangkal (ء ه), tengah (ع ح), ujung (غ خ)",
          "*Aqsha*, *wasath*, dan *adna al-halq* dengan pembagian yang sama", "Sesuai"],
         ["*Al-lisan*: 18 huruf", "Sepuluh makhraj di lidah dengan total 18 huruf", "Sesuai"],
         ["*Asy-syafatain*: ب dan م dengan merapatkan bibir; ف dari bibir bawah dan gigi atas",
          "Dua bibir bertemu rapat; ف dari bagian dalam bibir bawah dengan ujung gigi seri atas", "Sesuai"],
         ["*Al-khaisyum*: tempat dengung (*ghunnah*) pada ن dan م", "*Ghunnah* keluar dari *khaisyum*", "Sesuai"],
         ["Enam sifat ب: *jahr*, *syiddah*, *istifal*, *infitah*, *idzlaq*, *qalqalah*",
          "ب tidak termasuk huruf *hams*, *isti'la*, dan *ithbaq*; termasuk huruf *syiddah*, *idzlaq*, dan *qalqalah*",
          "Sesuai"],
         ["Arti *jahr* \"napas tertahan\" dan *syiddah* \"suara tertahan\" pada ب",
          "*Jahr*: tertahannya napas; *syiddah*: tertahannya suara", "Sesuai"],
         ["*Qalqalah* ب hanya saat bersukun (latihan أَبْ)", "Syarat *qalqalah*: hurufnya bersukun", "Sesuai"],
         ["ح dari tengah tenggorokan, ه dari pangkal tenggorokan (kuis huruf mirip)",
          "Pembagian yang sama", "Sesuai"],
         ["*Khaisyum* ditulis \"pangkal hidung\"",
          "Rongga hidung bagian dalam yang tersambung ke mulut", "Perlu disesuaikan"],
         ["و ditulis \"dengan memonyongkan bibir\"",
          "Dua bibir membulat dan terbuka, tidak dirapatkan", "Perlu disesuaikan"],
         ["*Istifal* diartikan \"tipis\"",
          "Pangkal lidah turun dari langit-langit; tipis adalah akibatnya", "Perlu disesuaikan"],
         ["*Idzlaq* diartikan \"ringan diucapkan\"",
          "Definisi sesuai, tetapi *idzlaq* tidak memengaruhi cara pelafalan",
          "Perlu disesuaikan: tidak dijadikan bahan latihan"],
     ],
     [6.0, 6.8, 2.7]),

    ("p",
     "Pemilihan enam pasangan huruf mirip juga diperiksa terhadap pola kesalahan penutur Indonesia. Suryana dkk. "
     "(2026) menemukan bahwa penutur dewasa berbahasa Jawa cenderung mengganti ق dengan ك, sedangkan penutur "
     "berbahasa Sunda cenderung melemahkan ع. Temuan ini sejalan dengan pasangan ق-ك dan ع-ء di aplikasi. Pemetaan "
     "kesalahan yang lebih rinci, misalnya ف menjadi /p/, belum dimasukkan ke materi karena sumbernya baru terbaca "
     "dari abstrak."),

    # ------------------------------------------------------------------ L2
    ("h2", "Lampiran 2. Rincian Analisis Pasar dan SWOT"),
    ("p",
     "Ukuran pasar dihitung dari jumlah penduduk Muslim (Databoks, 2024), proporsi survei literasi (Asrori, "
     "2023), dan penetrasi internet (Bisnis.com, 2025). TAM = 245,97 juta × (100% − 44,57%) = 136,3 juta orang "
     "yang belum lancar membaca sesuai tajwid. SAM = TAM × 80,66% = 110,0 juta orang yang dapat dijangkau "
     "aplikasi. SOM = 100 ribu pengguna aktif bulanan pada tahun ketiga. Proporsi survei diterapkan pada seluruh "
     "penduduk Muslim, termasuk anak usia dini, sehingga TAM dan SAM merupakan batas atas. Gambar {fig:pasar} "
     "menggambarkan ukuran pasar dan posisi Makhraj di antara aplikasi sejenis."),
    ("fig", "pasar", "fig03_pasar.png", "Ukuran pasar dan posisi Makhraj terhadap aplikasi sejenis", 14.0),
    ("table", "swot", "Analisis SWOT Makhraj beserta mitigasinya",
     ["Kekuatan (*strengths*)", "Kelemahan (*weaknesses*)"],
     [
         ["Perpaduan penampang makhraj, contoh guru yang disebut namanya, latihan rekam, dan sorot huruf di mushaf "
          "dalam satu alur; rujukan guru bersanad yang jelas; materi "
          "dicocokkan dengan kitab syarah; inti gratis",
          "Belum ada penilaian otomatis pada MVP; contoh suara bergantung pada video pihak lain dan belum "
          "tersedia untuk ا; pelajaran rinci baru tiga huruf"],
         ["**Peluang** (*opportunities*)", "**Ancaman** (*threats*)"],
         ["Penetrasi internet 80,66%; program literasi Al-Qur'an pemerintah; kebutuhan tutorial baca Al-Qur'an "
          "di kampus; pengajar tahsin yang mencari penghasilan daring",
          "Pesaing dapat menambah materi makhraj; izin konten ditolak; retensi pengguna aplikasi edukasi rendah"],
         ["**Mitigasi kelemahan**", "**Mitigasi ancaman**"],
         ["Koreksi pengajar dibuka pada Tahap 2 sebelum penilaian AI; klip yang kosong diisi rekaman pengajar "
          "mitra bersanad; pelajaran 26 huruf disusun pada *sprint* kedua",
          "Keunggulan dijaga melalui validasi materi dan jaringan pengajar; jika izin kanal ditolak, seluruh klip "
          "diganti rekaman pengajar mitra; retensi dijaga dengan target harian kecil dan hari beruntun"],
     ],
     [7.75, 7.75]),

    # ------------------------------------------------------------------ L3
    ("h2", "Lampiran 3. Pemetaan Model Bisnis dan Rencana Implementasi"),
    ("p",
     "Lampiran ini memetakan cara Makhraj menciptakan, menyalurkan, dan menjaga nilainya. Seluruh angka keuangan "
     "merupakan asumsi perencanaan dalam juta rupiah dan akan diperbarui setelah uji pengguna."),
    ("p0",
     "**a. Kanvas model bisnis.** Gambar {fig:bmc} memetakan model bisnis Makhraj dengan kerangka *Business Model "
     "Canvas* (Osterwalder & Pigneur, 2010) dan dibaca mengikuti nomor blok, dari segmen pengguna sampai struktur "
     "biaya. Proposisi nilai di tengah menjadi pembeda utama: Makhraj tidak berhenti pada penilaian benar atau "
     "salah, tetapi menunjukkan letak kesalahan dan cara membetulkannya."),
    ("fig", "bmc", "fig11_bmc.png", "Kanvas model bisnis Makhraj", 15.5),
    ("p0",
     "**b. Aliran nilai dan dana.** Gambar {fig:ekosistem} menunjukkan pertukaran antarpihak. Pengguna hanya membayar "
     "koreksi oleh manusia, sedangkan materi tetap gratis. Bagi hasil 70% menjadi insentif bagi pengajar untuk "
     "bergabung, lembaga membayar dasbor kelas, dan mitra ZISWAF menerima laporan dampak atas subsidi yang diberikan."),
    ("fig", "ekosistem", "fig12_ekosistem.png", "Aliran nilai dan aliran dana dalam ekosistem Makhraj", 14.0),
    ("p0",
     "**c. Proyeksi keuangan.** Tabel {tab:biaya} dan Gambar {fig:keuangan}a merinci skenario dasar. Biaya "
     "pengembangan oleh tim tidak dihitung karena dikerjakan mahasiswa secara sukarela, dan dana ZISWAF tidak dicatat "
     "sebagai pendapatan karena seluruhnya disalurkan untuk subsidi setoran. Biaya Firebase memakai perkiraan riset "
     "tim (sekitar US$85 per bulan pada 100 ribu pengguna aktif, kurs Rp16.000) dan belum memasukkan biaya autentikasi "
     "di atas 50 ribu pengguna, yang dikendalikan dengan menghapus akun anonim yang tidak aktif."),
    ("table", "biaya", "Proyeksi biaya dan pendapatan Makhraj (juta rupiah)",
     ["Komponen", "Tahun 1", "Tahun 2", "Tahun 3"],
     [
         ["Target pengguna aktif bulanan", "5.000", "30.000", "100.000"],
         ["**Biaya**", "", "", ""],
         ["Akun pengembang Google Play (sekali bayar, US$25)", "0,4", "-", "-"],
         ["Domain dan layanan Firebase (paket gratis pada Tahun 1, lalu sekitar US$25 dan US$85 per bulan)", "0,2", "5,0", "16,6"],
         ["Honor tinjauan materi oleh pengajar tahsin bersanad", "3,0", "2,0", "2,0"],
         ["Sewa GPU untuk melatih model penilai makhraj (Tahap 3)", "-", "-", "5,0"],
         ["Promosi dan kerja sama kampus", "1,0", "3,0", "6,0"],
         ["**Total biaya**", "**4,6**", "**10,0**", "**29,6**"],
         ["**Pendapatan**", "", "", ""],
         ["Setor ke Pengajar: 1% pengguna × 4 paket × Rp20.000, porsi operasional 30%", "-", "7,2", "24,0"],
         ["Lisensi lembaga Rp0,3 juta per kelas (10 kelas, lalu 40 kelas)", "-", "3,0", "12,0"],
         ["**Total pendapatan**", "-", "**10,2**", "**36,0**"],
         ["**Selisih tahunan**", "**−4,6**", "**+0,2**", "**+6,4**"],
         ["Bagian pengajar mitra dari Setor ke Pengajar (70%)", "-", "16,8", "56,0"],
     ],
     [9.1, 2.1, 2.1, 2.2]),
    ("fig", "keuangan", "fig13_keuangan.png", "Proyeksi keuangan dan sensitivitas skenario Makhraj", 15.5),
    ("p0",
     "**d. Uji skenario.** Tabel {tab:skenario} dan Gambar {fig:keuangan}b menguji tiga kombinasi jumlah pengguna, "
     "konversi, dan jumlah kelas. Biaya Firebase naik sebanding dengan jumlah pengguna. Pada skenario pesimis, defisit "
     "Rp9,4 juta ditutup dengan menunda sewa GPU, memangkas biaya promosi, dan memindahkan *hosting* web ke layanan "
     "statis gratis. Dengan 100 ribu pengguna dan 40 kelas, titik impas tahunan tercapai pada konversi 0,73%."),
    ("table", "skenario", "Uji skenario pada Tahun 3 (juta rupiah)",
     ["Skenario", "Pengguna aktif", "Konversi setoran", "Kelas lembaga", "Pendapatan", "Biaya", "Selisih"],
     [
         ["Pesimis", "50.000", "0,5%", "20", "12,0", "21,4", "−9,4"],
         ["**Dasar**", "**100.000**", "**1%**", "**40**", "**36,0**", "**29,6**", "**+6,4**"],
         ["Optimis", "150.000", "2%", "80", "96,0", "37,7", "+58,3"],
     ],
     [2.2, 2.4, 2.4, 2.2, 2.2, 1.8, 2.3]),
    ("p0",
     "**e. Strategi pemasaran.** Setiap segmen dijangkau melalui kanal yang sudah dipercaya segmen itu, dengan "
     "penawaran dan target awal pada Tabel {tab:gtm}. Singkatan UKM berarti unit kegiatan mahasiswa, sedangkan "
     "LAZ berarti lembaga amil zakat."),
    ("table", "gtm", "Strategi pemasaran per segmen pengguna",
     ["Segmen", "Kanal utama", "Penawaran", "Target awal"],
     [
         ["Mahasiswa dan pekerja muda", "Tutorial BTQ kampus, UKM kerohanian, dan media sosial",
          "Belajar privat tanpa canggung; peluang menjadi relawan pengajar", "2.000 pengguna dari 5 kampus (Tahun 1)"],
         ["Orang tua dan anak", "TPQ, majelis taklim, dan grup orang tua",
          "Belajar bersama anak dengan inti gratis", "1.500 keluarga (Tahun 1)"],
         ["Mualaf dan lansia", "Pusat pembinaan mualaf, majelis taklim, dan LAZ",
          "Pendampingan dan setoran bersubsidi ZISWAF", "300 penerima subsidi (Tahun 2)"],
         ["Lembaga", "Kemitraan langsung, dimulai dari kampus tim",
          "Dasbor kelas Rp300.000 per kelas per tahun", "10 kelas (Tahun 2) dan 40 kelas (Tahun 3)"],
     ],
     [3.1, 4.4, 4.6, 3.4]),
    ("p0",
     "**f. Rencana implementasi.** Gambar {fig:gantt} menjabarkan peta jalan pada Gambar {fig:roadmap} menjadi lima "
     "jalur kerja selama 36 bulan dengan empat tonggak: rilis publik (bulan ke-6), pembukaan layanan setoran "
     "(bulan ke-13), uji beta penilaian AI (bulan ke-30), dan kas kumulatif positif (bulan ke-36)."),
    ("fig", "gantt", "fig14_gantt.png", "Rencana implementasi Makhraj selama 36 bulan", 15.5),

    # ------------------------------------------------------------------ L4
    ("h2", "Lampiran 4. Implementasi dan Status Fitur MVP"),
    ("p",
     "Tabel {tab:fitur} merinci masukan, proses, dan keluaran setiap fitur utama beserta statusnya pada MVP. "
     "Kode MVP juga dilengkapi dua belas tes unit untuk materi, sifat, sorot huruf, soal, SUS, dan hari belajar, "
     "serta empat belas tes ujung ke ujung di peramban untuk aksesibilitas, alur rekam, dan cermin kamera."),
    ("table", "fitur", "Implementasi dan status fitur utama MVP",
     ["Fitur", "Masukan", "Proses", "Keluaran", "Status MVP"],
     [
         ["Peta makhraj", "Ketukan pada area atau titik", "Penampang kepala SVG; 5 area dan 17 titik dipetakan ke huruf",
          "Titik tersorot dan daftar huruf", "Berjalan, 17 titik dan 29 huruf"],
         ["Pelajaran huruf", "Huruf yang dipilih",
          "Lima langkah: lihat, dengar, tiru, bandingkan, terapkan; sifat dihitung otomatis dari matan",
          "Pemahaman letak dan sifat huruf",
          "Rinci untuk ب, ح, ه; klip untuk 28 huruf; klip ض dan ط dari kanal resmi Dr. Ayman Swaid"],
         ["Rekam dan bandingkan", "Suara dan kamera depan",
          "Rekaman di IndexedDB diputar bergantian dengan klip guru; gelombang suara; kamera seperti cermin",
          "Rekaman dan daftar periksa mandiri", "Berjalan"],
         ["Huruf mirip", "Pasangan huruf", "Dua penampang berdampingan; tabel perbandingan sifat; kuis otomatis",
          "Skor kuis", "Berjalan, 6 pasangan"],
         ["Sorot huruf", "Huruf yang dipelajari", "Harakat diabaikan saat pencarian; kata yang memuat huruf ditandai",
          "Ayat dengan kata tersorot", "Berjalan, 114 surah"],
         ["Progres", "Hasil latihan", "Disimpan di localStorage; sinkronisasi Firestore pada Tahap 2",
          "Huruf dikuasai dan hari belajar", "Berjalan (lokal)"],
         ["Uji coba", "Persetujuan dan jawaban peserta",
          "Tes 20 soal bentuk A/B bergantian, SUS 10 butir, catatan pemakaian", "Berkas JSON untuk analisis",
          "Berjalan"],
     ],
     [2.5, 2.4, 4.6, 3.1, 2.9]),
    ("p",
     "Rekaman baru diunggah ketika pengguna menyetor bacaan pada Tahap 2, dengan persetujuan sesuai dengan "
     "Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi. Pada Tahap 3, model wav2vec 2.0 "
     "(Baevski dkk., 2020) dilatih ulang dengan rekaman terkoreksi untuk menilai makhraj per huruf; nilai yang "
     "meragukan diteruskan kepada pengajar."),

    # ------------------------------------------------------------------ L5
    ("h2", "Lampiran 5. Tampilan Purwarupa Lanjutan"),
    ("p",
     "Gambar {fig:screens_b} melanjutkan Gambar {fig:screens_a}. Layar rekam dan bandingkan (d) memberi bacaan "
     "latihan per harakat, misalnya أَبْ untuk melatih pantulan *qalqalah*, lalu menyediakan cermin kamera, tombol "
     "rekam, dan klip contoh dari Syaikh Aiman; rekaman pengguna diputar bergantian dengan contoh guru dan "
     "ditampilkan bentuk gelombangnya. Layar huruf mirip (e) menampilkan penampang ح dan ه berdampingan beserta "
     "tabel perbandingan sifatnya, lalu kuis yang dibuat otomatis. Layar mushaf (f) menyorot empat kata berhuruf ب pada Surah "
     "Al-Fatihah dan mencantumkan atribusi teks Tanzil serta terjemahan Kemenag via Tanzil di bagian bawah."),
    ("fig", "screens_b", "fig10_screens_b.png", "Tampilan MVP Makhraj: rekam, huruf mirip, dan mushaf", 13.0),

    # ------------------------------------------------------------------ L6
    ("h2", "Lampiran 6. Keputusan Teknologi Purwarupa"),
    ("p",
     "MVP pertama Makhraj ditulis dengan Flutter. Setelah fitur inti berjalan, tim memindahkannya ke React dengan "
     "tiga pertimbangan. Pertama, Capacitor membungkus folder hasil *build* yang sama dengan versi web menjadi APK "
     "Android, sehingga yang diuji juri di peramban dan di ponsel adalah kode yang sama. Kedua, perekaman suara "
     "(MediaRecorder), kamera depan (getUserMedia), dan mode luring (*service worker*) sudah tersedia sebagai API "
     "bawaan peramban, sehingga tidak perlu plugin tambahan. Ketiga, teks Arab dan penampang kepala dirender sebagai "
     "DOM dan SVG biasa, sehingga bisa diberi label aksesibilitas dan diperiksa langsung di peramban. Tabel "
     "{tab:stack} merangkum pilihan per lapisan. Capacitor 8 mensyaratkan Node.js 22, minSdk 24, dan targetSdk 36 "
     "(Ionic, t.t.)."),
    ("table", "stack", "Pilihan teknologi purwarupa React dan alasannya",
     ["Lapisan", "Pilihan", "Alasan", "Alternatif yang tidak dipakai"],
     [
         ["Tampilan dan *build*", "React 19, TypeScript, Vite 8", "Aplikasi satu halaman tanpa server; hasil *build* statis",
          "Next.js: fitur *server rendering* tidak terpakai"],
         ["Android", "Capacitor 8", "Satu folder *build* untuk web dan APK; izin mikrofon dan kamera diteruskan dari WebView",
          "TWA: bergantung pada Chrome dan koneksi; React Native: tampilan harus ditulis ulang"],
         ["Navigasi", "React Router (mode *hash*)", "Berjalan sama di *hosting* statis dan WebView tanpa pengaturan server", "-"],
         ["Penyimpanan", "Zustand + localStorage; IndexedDB",
          "Progres kecil berupa teks; rekaman berupa *blob* yang terlalu besar untuk localStorage",
          "Basis data daring pada Tahap 1"],
         ["Gaya dan huruf", "Tailwind CSS 4; Scheherazade New dan Plus Jakarta Sans",
          "Fon berlisensi SIL OFL boleh dibundel; tanda khusus rasm Utsmani tampil benar",
          "Fon KFGQPC: lisensinya melarang reproduksi tanpa izin"],
         ["Luring", "vite-plugin-pwa", "Aplikasi, fon, materi, dan teks Al-Qur'an tersimpan untuk dipakai tanpa internet", "-"],
         ["Rekam dan cermin", "MediaRecorder dan getUserMedia", "API bawaan; format rekaman dipilih sesuai dukungan perangkat",
          "Plugin perekam native"],
         ["Pengujian", "Vitest (12 tes); Playwright + axe-core (14 tes)", "Menguji logika materi dan soal, aksesibilitas 12 layar, alur rekam, dan cermin kamera", "-"],
     ],
     [2.4, 3.6, 5.3, 4.2]),

    # ------------------------------------------------------------------ L7
    ("h2", "Lampiran 7. Sumber Konten, Lisensi, dan Kebijakan Pemutar Video"),
    ("p",
     "Setiap fitur Makhraj bergantung pada data dengan syarat pakai yang berbeda, sehingga sumber data dikunci "
     "sebelum fitur dibangun (Tabel {tab:lisensi}). Teks Al-Qur'an dari Tanzil berlisensi CC BY 3.0 dan tidak boleh "
     "diubah (Tanzil Project, t.t.). Karena itu, fitur sorot huruf tidak menyentuh teks yang ditampilkan: aplikasi "
     "hanya membandingkan huruf dasar pada salinan setiap kata, sehingga harakat dan tanda waqaf otomatis diabaikan. "
     "Teks yang dipakai adalah rasm Utsmani riwayat Hafsh dari Tanzil, bukan Mushaf Standar Indonesia, karena teks "
     "digital Mushaf Standar Indonesia belum tersedia secara terbuka. Terjemahan Kemenag yang disebarkan Tanzil "
     "adalah edisi lama dan hanya boleh dipakai untuk keperluan nonkomersial."),
    ("table", "lisensi", "Sumber konten, syarat pemakaian, dan status pada MVP",
     ["Data", "Sumber", "Syarat utama", "Status MVP"],
     [
         ["Teks ayat", "Tanzil Uthmani 1.1", "CC BY 3.0; tanpa perubahan; atribusi dan tautan", "Dipakai, 114 surah"],
         ["Pencocokan huruf", "Salinan kata dari teks Tanzil", "Teks yang tampil tidak diubah", "Dipakai"],
         ["Terjemahan", "Terjemahan Kemenag edisi lama via Tanzil", "Nonkomersial; izin LPMQ sebelum layanan berbayar",
          "Dipakai dengan label edisi"],
         ["Fon ayat", "Scheherazade New (SIL OFL)", "Bebas dibundel", "Dipakai"],
         ["Klip guru", "Kanal Al-Andalasy dan kanal resmi Dr. Ayman Swaid",
          "Pemutar resmi YouTube; tanpa unduh dan tanpa *cache*", "28 dari 29 huruf; alif belum ada"],
         ["Makhraj dan sifat", "*Fath Rabb al-Bariyyah* dan *At-Tajwid al-Mushawwar*", "Divalidasi pengajar bersanad",
          "3 pelajaran rinci; belum divalidasi"],
         ["Penampang kepala", "Gambar sendiri; basis CC0 (Wright & McCloy, 2011) untuk versi berikutnya",
          "Diperiksa pengajar", "Ilustrasi sederhana"],
     ],
     [2.5, 4.3, 4.6, 4.1]),
    ("p",
     "Klip guru diambil dari dua kanal (Tabel {tab:klip}). Kebijakan pengembang YouTube melarang pengunduhan, "
     "penyimpanan untuk pemutaran luring, pemisahan audio dari video, dan penutupan pemutar (Google, t.t.). "
     "Akibatnya, perbandingan suara dilakukan bergantian: klip guru diputar di pemutar YouTube, lalu rekaman pengguna "
     "diputar terpisah. Risiko teknis terbesar adalah galat pemutaran YouTube di WebView Android. Aplikasi sudah "
     "menyediakan tautan \"Buka di YouTube\" sebagai cadangan, dan uji di perangkat nyata dijadwalkan sebelum uji "
     "lapangan. Untuk jangka panjang, tim akan merekam contoh pendek per huruf dan harakat dari pengajar validator "
     "dengan izin tertulis, sehingga contoh itu dapat diputar luring dan dipakai pada Tahap 3."),
    ("table", "klip", "Pembagian peran klip guru",
     ["Peran klip", "Sumber", "Huruf yang hanya ada di sumber ini", "Catatan"],
     [
         ["Dengar: klip pendek 1 sampai 4 menit", "Kanal resmi Dr. Ayman Swaid", "ض, ط",
          "Diunggah pemilik kanal sendiri"],
         ["Dengar dan tiru per harakat", "Kanal Al-Andalasy (Tahsin Camp)", "ص, ق, غ, ء",
          "Konteks Indonesia; beberapa huruf digabung dalam satu video"],
         ["Alif", "Belum ada klip khusus", "-", "Ditampilkan sebagai huruf mad dari *al-jauf* tanpa video"],
     ],
     [3.8, 3.7, 3.6, 4.4]),

    # ------------------------------------------------------------------ L8
    ("h2", "Lampiran 8. Rancangan Uji Coba dan Instrumen"),
    ("p",
     "Uji coba mengukur perubahan pemahaman dan bacaan peserta, selain kegunaan aplikasi (Tabel {tab:uji}). Semua "
     "instrumen yang diisi peserta sudah tersedia di menu Saya pada aplikasi. Peserta memasukkan kode dari peneliti, "
     "menyatakan berusia minimal 18 tahun, dan menyetujui lembar penjelasan. Data tersimpan di perangkat dan baru "
     "sampai ke peneliti ketika peserta sendiri mengunduh berkas ekspor JSON dan menyerahkannya. Rekaman suara tidak "
     "ikut diekspor."),
    ("table", "uji", "Tahapan uji coba, instrumen, dan analisis",
     ["Tahap", "Peserta", "Instrumen", "Analisis"],
     [
         ["Uji kegunaan formatif", "5 sampai 8 orang campuran: mahasiswa, orang tua, lansia",
          "8 tugas *think-aloud*, termasuk menolak izin kamera; *Single Ease Question*",
          "Tingkat penyelesaian tugas dan tingkat keparahan masalah; perbaikan dicatat per versi"],
         ["Tes pemahaman", "20 pemula, minimal 18 tahun",
          "20 soal: 7 area, 7 titik, 6 sifat; bentuk A dan B dengan urutan ditukar antarpeserta",
          "Uji Wilcoxon bertanda, median dan rentang antarkuartil, ukuran efek *r*"],
         ["Kualitas bacaan", "Peserta yang sama",
          "10 kata direkam pada hari ke-0 dan ke-14; rubrik 0 sampai 2 per huruf sasaran",
          "Dinilai dua pengajar tanpa mengetahui urutan rekaman; kappa Cohen"],
         ["Kegunaan", "Peserta yang sama", "SUS 10 butir versi Indonesia (Sharfina & Santoso, 2016)",
          "Rata-rata dan interval kepercayaan 95% dibandingkan dengan ambang 68"],
         ["Keterlibatan", "Peserta yang sama", "Log pemakaian dari berkas ekspor",
          "Persentase peserta yang aktif minimal 4 hari per pekan"],
     ],
     [2.6, 3.3, 5.0, 4.6]),
    ("p",
     "Soal tes dibangkitkan dari data materi dengan bilangan acak berbenih tetap, sehingga setiap peserta menerima "
     "soal yang sama untuk bentuk yang sama. Peserta bernomor ganjil mengerjakan bentuk A sebelum belajar dan bentuk "
     "B sesudahnya, sedangkan peserta bernomor genap sebaliknya. Aplikasi menghitung hari aktif sebagai hari dengan minimal "
     "satu kegiatan bermakna, yaitu membuka langkah pelajaran, merekam, menjawab kuis, atau membaca surah; membuka "
     "aplikasi saja tetap tercatat di log, tetapi tidak dihitung sebagai hari aktif. Butir SUS "
     "di aplikasi masih berupa terjemahan kerja dan akan diganti dengan versi Indonesia yang sudah divalidasi sebelum "
     "studi resmi."),
    ("p",
     "Target rekaman ditetapkan sebagai \"jumlah kesalahan menurun\", bukan \"bacaan menjadi benar\". Meta-analisis "
     "pelatihan fonetik dengan variasi tinggi menemukan efek besar pada kemampuan membedakan bunyi (*g* = 0,92 untuk "
     "tes awal dan akhir; Uchihara dkk., 2025), tetapi perbaikan pengucapan jauh lebih kecil, yaitu 10,5% pada butir "
     "yang dilatih dan 4,5% pada butir yang tidak dilatih (Uchihara dkk., 2024). Penilaian diri pengucapan juga "
     "sering tidak akurat; penutur yang lemah cenderung menilai dirinya terlalu tinggi (Trofimovich dkk., 2016). "
     "Karena itu, daftar periksa di aplikasi memakai butir yang dapat diamati, label \"belum divalidasi pengajar\" "
     "tetap tampil, dan penilaian akhir diserahkan kepada pengajar. Hasil Katz dan Mehta (2015) juga hanya berasal "
     "dari lima peserta dengan umpan balik lidah secara langsung, sehingga dipakai sebagai alasan desain, bukan "
     "sebagai perkiraan besar efek."),

    # ------------------------------------------------------------------ L9
    ("h2", "Lampiran 9. Kajian Kesiapan Penilaian Bacaan Otomatis"),
    ("p",
     "MVP sengaja tidak menilai bacaan secara otomatis. Tabel {tab:ai} merangkum hasil penelitian terbaru tentang "
     "deteksi kesalahan pelafalan bacaan Al-Qur'an. Sistem terbaik pada Iqra'Eval 2025 hanya mencapai presisi 0,37, "
     "artinya hampir dua pertiga bacaan yang ditandai salah sebenarnya benar, dan 35% kesalahan nyata lolos "
     "(El Kheir dkk., 2025b). Angka ini diukur pada penutur asli bahasa Arab; belum ada angka untuk penutur Indonesia "
     "ataupun untuk pasangan huruf seperti ح-ه dan ق-ك. Memberi skor yang sering keliru kepada pemula akan merusak "
     "kepercayaan pada aplikasi yang bersandar pada rujukan guru."),
    ("table", "ai", "Hasil penelitian deteksi kesalahan pelafalan bacaan Al-Qur'an",
     ["Studi", "Data uji", "Hasil terbaik", "Catatan untuk Makhraj"],
     [
         ["QuranMB.v1 (El Kheir dkk., 2025a)", "98 ayat, 18 penutur asli yang sengaja membuat kesalahan tertentu",
          "F1 29,88%; presisi 18,70%", "Kesalahan buatan, bukan kesalahan pemula"],
         ["Iqra'Eval 2025 (El Kheir dkk., 2025b)", "Tolok ukur yang sama, 2025",
          "F1 0,4726; presisi 0,3713; penerimaan salah 0,3499", "Sebagian besar tanda kesalahan keliru"],
         ["IQRA 2026 (El Kheir dkk., 2026)", "QuranMB.v2, 1.643 ujaran beranotasi ahli", "F1 0,7201",
          "Membaik, tetapi belum diuji pada penutur Indonesia"],
         ["Abdelfattah dkk. (2025)", "848 jam audio bacaan", "PER 0,21%; F1 tajwid 75,8%",
          "Data latih dari qari, bukan pemula"],
         ["Salameh dkk. (2024)", "Sekitar 7.000 bacaan dari 1.287 peserta non-Arab", "Kesepakatan antaranotator 0,63",
          "Label per bacaan, bukan per huruf"],
     ],
     [3.5, 4.4, 3.6, 4.0]),
    ("p",
     "Kekurangan terbesar ada pada data: belum ada data publik berisi bacaan penutur Indonesia dengan label kesalahan "
     "makhraj dari pengajar. Tahap 2 Makhraj menghasilkan data semacam itu sebagai hasil sampingan koreksi. Rekaman "
     "baru dipakai untuk riset bila pemiliknya memberi persetujuan terpisah yang dapat ditarik kembali. Label "
     "mengikuti rubrik pengajar (tepat, bergeser ke huruf lain, atau kurang jelas), sebagian rekaman dinilai dua "
     "kali untuk menghitung kappa, dan metadata yang disimpan hanya kelompok usia, jenis kelamin, bahasa ibu, dan "
     "jenis perangkat. Model pada Tahap 3 dibangun dari data tersebut, dan setiap hasil yang meragukan tetap "
     "diteruskan kepada pengajar."),

    # ------------------------------------------------------------------ L10
    ("h2", "Lampiran 10. Pelindungan Data dan Rencana *Backend* Tahap 2"),
    ("p",
     "Pada MVP tidak ada data pengguna yang dikirim ke server. Tabel {tab:data} memetakan letak setiap jenis data "
     "sekarang dan pada Tahap 2. Firebase dipilih untuk Tahap 2 karena Firestore dapat ditempatkan di Jakarta "
     "(asia-southeast2) dan paket gratisnya mencakup 1 GiB data, 50 ribu baca dan 20 ribu tulis per hari, serta "
     "autentikasi hingga 50 ribu pengguna aktif bulanan (Firebase, t.t.-b). Kuota ini jauh di atas kebutuhan uji 20 "
     "peserta. Sejak 3 Februari 2026, proyek dengan paket gratis tidak lagi dapat membaca dan menulis Cloud Storage "
     "(Firebase, t.t.-a). Karena itu, unggah rekaman baru dibangun bersama layanan setoran berbayar, saat proyek "
     "pindah ke paket Blaze dengan peringatan anggaran."),
    ("table", "data", "Letak dan perlindungan data pengguna",
     ["Data", "MVP (Tahap 1)", "Tahap 2", "Perlindungan"],
     [
         ["Progres, pengaturan, log pemakaian", "localStorage perangkat", "Firestore Jakarta, per akun",
          "Pengguna hanya dapat membaca dan menulis datanya sendiri"],
         ["Rekaman suara", "IndexedDB perangkat", "Cloud Storage hanya saat disetor",
          "Persetujuan per setoran; batas ukuran; dihapus 90 hari setelah dikoreksi"],
         ["Hasil tes dan SUS", "Perangkat; ekspor JSON oleh peserta", "Firestore, koleksi studi",
          "Kode peserta, tanpa nama; peserta minimal 18 tahun"],
         ["Akun", "Tidak ada", "Login anonim, lalu Google atau tautan surel",
          "Tanpa nomor telepon; akun dapat dihapus"],
     ],
     [3.3, 3.6, 3.6, 5.0]),
    ("p",
     "Persetujuan disusun per tujuan: data progres untuk akun, ikut riset, unggah rekaman per setoran, dan analitik. "
     "Setiap persetujuan dapat ditarik dari menu Saya, dan pengguna dapat mengunduh atau menghapus seluruh datanya. "
     "Peraturan pelaksana Undang-Undang Nomor 27 Tahun 2022 dilaporkan ditetapkan sebagai PP Nomor 33 Tahun 2026 "
     "dengan masa transisi enam bulan, tetapi belum diundangkan secara resmi saat proposal ini ditulis (Mediana, "
     "2026). Tim akan mencocokkan kewajiban teknisnya, seperti tenggat penarikan persetujuan dan pemberitahuan "
     "insiden, dengan teks resmi sebelum Tahap 2 dibuka. Satu anggota tim ditunjuk sebagai kontak pelindungan data."),

    # ------------------------------------------------------------------ L11
    ("h2", "Lampiran 11. Aksesibilitas dan Adab Desain"),
    ("p",
     "Pengguna Makhraj mencakup lansia, sehingga aksesibilitas diperlakukan sebagai syarat. Acuannya adalah WCAG "
     "2.2, yang meminta kontras minimal 4,5:1 untuk teks dan 3:1 untuk penanda nonteks (W3C, 2023). Pada palet awal, "
     "teks berwarna emas di atas latar krem hanya mencapai kontras 2,65:1. Tabel {tab:aksesibilitas} merinci "
     "perbaikan yang sudah diterapkan di purwarupa React."),
    ("table", "aksesibilitas", "Penerapan aksesibilitas dan adab desain pada purwarupa",
     ["Aspek", "Penerapan", "Status"],
     [
         ["Kontras warna", "Emas hanya untuk hiasan; teks memakai emas gelap yang lolos AA", "Diterapkan"],
         ["Sorot kata di mushaf",
          "Latar emas muda dan garis bawah teal 3 px; fon dan ukuran tidak diubah agar sambungan huruf Arab tetap utuh",
          "Diterapkan"],
         ["Ukuran sentuh dan teks", "Tombol minimal 48 px; ukuran teks dapat diperbesar dari menu Saya", "Diterapkan"],
         ["Gerak", "Animasi dimatikan bila perangkat meminta gerak dikurangi", "Diterapkan"],
         ["Navigasi papan ketik", "Garis fokus yang jelas; tombol ikon memakai label", "Diterapkan"],
         ["Gamifikasi", "Tanpa papan peringkat, poin, dan iklan; hari belajar pekan ini dapat disembunyikan", "Diterapkan"],
         ["Kejujuran materi", "Label \"Belum divalidasi pengajar\" pada setiap pelajaran sampai ditinjau", "Diterapkan"],
         ["Audit otomatis", "axe-core (WCAG 2.2 A dan AA) pada 12 layar; satu temuan label tombol harakat sudah diperbaiki; tanpa pelanggaran serius",
          "Lolos"],
         ["Pembaca layar", "Uji dengan TalkBack di perangkat Android", "Rencana"],
     ],
     [3.2, 9.6, 2.7]),

    # ------------------------------------------------------------------ L12
    ("h2", "Lampiran 12. Risiko, Mitigasi, dan Status Pekerjaan"),
    ("p",
     "Sebagian besar risiko yang tersisa menyangkut konten dan izin. Tabel {tab:risiko} memuat risiko yang "
     "masih terbuka beserta batas waktunya, dan Tabel {tab:status} memisahkan pekerjaan Tahap 1 yang sudah selesai "
     "dari yang belum."),
    ("table", "risiko", "Risiko yang masih terbuka dan mitigasinya",
     ["Risiko", "Dampak", "Mitigasi", "Batas waktu"],
     [
         ["Materi belum divalidasi pengajar", "Klaim rujukan guru bersanad melemah",
          "Sesi validasi mingguan; minimal 10 huruf (enam pasangan mirip) divalidasi", "Sebelum uji lapangan"],
         ["Izin klip YouTube belum tertulis", "Fitur dengar bisa harus diganti",
          "Minta izin tertulis ke kedua kanal; siapkan rekaman pengajar mitra", "Sebelum fitur berbayar"],
         ["YouTube gagal di WebView Android", "Klip tidak terputar di APK",
          "Uji di dua ponsel; tautan \"Buka di YouTube\"", "Sebelum penjurian"],
         ["Terjemahan nonkomersial", "Tidak boleh dipakai di layanan berbayar",
          "Izin LPMQ atau terjemahan dibatasi pada fitur gratis", "Sebelum Tahap 2"],
         ["Teks bukan Mushaf Standar Indonesia", "Pertanyaan tentang tashih", "Konsultasi dan tashih ke LPMQ",
          "Sebelum rilis publik"],
         ["Uji terbatas dianggap publikasi karya", "Pelanggaran aturan lomba",
          "Konfirmasi ke panitia sebelum uji dua pekan", "Sebelum uji lapangan"],
         ["Nama \"Makhraj\" sudah dipakai pihak lain", "Sengketa merek", "Cek Play Store dan PDKI", "Sebelum rilis"],
     ],
     [3.6, 3.5, 5.6, 2.8]),
    ("table", "status", "Status pekerjaan Tahap 1",
     ["Pekerjaan", "Status"],
     [
         ["Web/PWA dan proyek Android Capacitor dari satu kode; 12 tes unit dan 14 tes peramban", "Selesai"],
         ["Materi 5 area, 17 titik, 29 huruf, 6 pasangan mirip; sifat dihitung otomatis", "Selesai"],
         ["Mushaf 114 surah dengan sorot huruf dan terjemahan berlabel", "Selesai"],
         ["Rekam, cermin kamera, gelombang suara, dan putar bergantian", "Selesai"],
         ["Persetujuan, tes A/B, SUS, dan ekspor JSON untuk uji coba", "Selesai"],
         ["APK Android dibangun dan diuji di perangkat nyata", "Belum (Android SDK belum terpasang)"],
         ["Detik mulai dan selesai klip per harakat", "Belum"],
         ["Pelajaran rinci untuk 26 huruf lainnya", "Belum"],
         ["Validasi materi dan ilustrasi oleh pengajar", "Belum"],
         ["Uji kegunaan formatif dan uji lapangan 20 peserta", "Belum"],
     ],
     [11.5, 4.0]),
]
