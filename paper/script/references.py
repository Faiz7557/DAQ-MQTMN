"""Daftar pustaka, gaya APA 7 berbahasa Indonesia, urut abjad. Format inline sama dengan content.py.

Setiap entri di sini dirujuk di content.py. Kalau menambah rujukan di teks,
tambahkan entrinya di sini juga; checks.py mencocokkan nama penulis dan tahun.
Hadis dirujuk di dalam teks saja (nomor hadis), mengikuti kebiasaan penulisan di Indonesia.
Rentang halaman memakai tanda pisah pendek (en dash), bukan tanda hubung.
"""

REFERENCES = [
    ("Al-Andalasy", "t.t.",
     "Al-Andalasy. (t.t.). *Tahsin Camp: Latihan makhorijul huruf bersama Dr. Aiman Rusydi* [Daftar putar video]. "
     "YouTube. Diakses 19 Oktober 2026, dari https://www.youtube.com/playlist?list=PLAlKX7OdTPPbUICvGO1w_xFGorWbtBWLu"),
    ("Asrori", "2023",
     "Asrori, A. M. (2023, 13 Oktober). Indeks literasi Al-Qur'an kategori tinggi, Kemenag berkomitmen perkuat "
     "pembelajaran Qur'an. *NU Online*. https://nu.or.id/nasional/indeks-literasi-al-qur-an-kategori-tinggi-"
     "kemenag-berkomitmen-perkuat-pembelajaran-qur-an-eoKUd"),
    ("Bisnis.com", "2025",
     "Bisnis.com. (2025, 6 Agustus). Data APJII: Pengguna internet di Indonesia tembus 229,43 juta orang pada "
     "2025. https://teknologi.bisnis.com/read/20250806/101/1899997/data-apjii-pengguna-internet-di-indonesia-"
     "tembus-22943-juta-orang-pada-2025"),
    ("Brooke", "1996",
     "Brooke, J. (1996). SUS: A \"quick and dirty\" usability scale. Dalam P. W. Jordan, B. Thomas, B. A. "
     "Weerdmeester, & I. L. McClelland (Ed.), *Usability evaluation in industry* (hlm. 189–194). Taylor & Francis."),
    ("Brown", "2008",
     "Brown, T. (2008). Design thinking. *Harvard Business Review, 86*(6), 84–92."),
    ("Cohen", "1960",
     "Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological "
     "Measurement, 20*(1), 37–46. https://doi.org/10.1177/001316446002000104"),
    ("Creswell", "2018",
     "Creswell, J. W., & Creswell, J. D. (2018). *Research design: Qualitative, quantitative, and mixed methods "
     "approaches* (Edisi ke-5). SAGE Publications."),
    ("Databoks", "2024",
     "Databoks. (2024, 8 Agustus). Mayoritas penduduk Indonesia beragama Islam pada semester I 2024. *Katadata*. "
     "https://databoks.katadata.co.id/datapublish/2024/08/08/mayoritas-penduduk-indonesia-beragama-islam-pada-"
     "semester-i-2024"),
    ("Direktorat Pembelajaran dan Kemahasiswaan", "2025",
     "Direktorat Pembelajaran dan Kemahasiswaan. (2025). *Panduan Musabaqah Tilawatil Qur'an Mahasiswa Nasional "
     "ke-XVIII tahun 2025*. Direktorat Jenderal Pendidikan Tinggi, Kementerian Pendidikan Tinggi, Sains, dan "
     "Teknologi Republik Indonesia."),
    ("Google", "t.t.",
     "Google. (t.t.). *YouTube API Services: Developer policies*. Diakses 18 Oktober 2026, dari "
     "https://developers.google.com/youtube/terms/developer-policies"),
    ("Infobank", "2025",
     "Infobank. (2025, 26 Februari). Ngaji.ai hadirkan fitur baru bantu khatam Al-Qur'an selama Ramadan. "
     "*Infobanknews*. https://infobanknews.com/ngaji-ai-hadirkan-fitur-baru-bantu-khatam-al-quran-selama-ramadan"),
    ("Katz", "2015",
     "Katz, W. F., & Mehta, S. (2015). Visual feedback of tongue movement for novel speech sound learning. "
     "*Frontiers in Human Neuroscience, 9*, 612. https://doi.org/10.3389/fnhum.2015.00612"),
    ("Mayer", "2009",
     "Mayer, R. E. (2009). *Multimedia learning* (Edisi ke-2). Cambridge University Press."),
    ("NU Online", "2023",
     "NU Online. (2023, 12 Oktober). Gandeng LK3P UI, Kemenag rilis hasil survei indeks literasi Al-Qur'an. "
     "https://nu.or.id/nasional/gandeng-lk3p-ui-kemenag-rilis-hasil-survei-indeks-literasi-al-qur-an-hpt3q"),
    ("Salim", "2007",
     "Salim, S. M. (2007). *Fath Rabb al-Bariyyah: Syarh al-Muqaddimah al-Jazariyyah fi 'ilm at-tajwid* "
     "(Edisi ke-4). Dar al-Ghautsani li ad-Dirasat al-Qur'aniyyah."),
    ("Sauro", "2016",
     "Sauro, J., & Lewis, J. R. (2016). *Quantifying the user experience: Practical statistics for user "
     "research* (Edisi ke-2). Morgan Kaufmann."),
    ("Schwaber", "2020",
     "Schwaber, K., & Sutherland, J. (2020). *The Scrum guide*. https://scrumguides.org/scrum-guide.html"),
    ("Suryo", "2024",
     "Suryo, A. (2024, 6 Februari). Ngaji.ai, belajar mengaji kini bisa pakai AI. *detikInet*. "
     "https://inet.detik.com/mobile-apps/d-7179292/ngaji-ai-belajar-mengaji-kini-bisa-pakai-ai"),
    ("Suwaid", "t.t.",
     "Suwaid, A. R. (t.t.). *Silsilat al-huruf al-'Arabiyyah* [Daftar putar video]. YouTube. "
     "https://www.youtube.com/playlist?list=PLJi21Zen45zT3XYozZ4BMaFxzuFb4xGcz"),
    ("Suwaid", "2014",
     "Suwaid, A. R. (2014). *At-Tajwid al-mushawwar* (Jilid 1–2). Dar al-Ghautsani li ad-Dirasat al-Qur'aniyyah."),
    ("Tanzil Project", "t.t.",
     "Tanzil Project. (t.t.). *Quran text license*. Diakses 18 Oktober 2026, dari "
     "https://tanzil.net/docs/text_license"),
    ("Tarteel", "t.t.",
     "Tarteel. (t.t.). *Introducing mistake detection*. Diakses 18 Oktober 2026, dari "
     "https://tarteel.ai/blog/introducing-mistake-detection/"),
]


# Sumber yang hanya dikutip di LAMPIRAN. Dicetak sebagai "Rujukan Lampiran" di akhir lampiran,
# sehingga tidak menambah panjang Daftar Pustaka dalam batas 10 halaman.
REFERENCES_LAMPIRAN = [
    ("Baevski", "2020",
     "Baevski, A., Zhou, H., Mohamed, A., & Auli, M. (2020). wav2vec 2.0: A framework for self-supervised "
     "learning of speech representations. *Advances in Neural Information Processing Systems, 33*, 12449–12460."),
    ("Osterwalder", "2010",
     "Osterwalder, A., & Pigneur, Y. (2010). *Business model generation: A handbook for visionaries, game "
     "changers, and challengers*. John Wiley & Sons."),
    ("Undang-Undang", "2022",
     "Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi. (2022). "
     "Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196."),
    ("Abdelfattah", "2025",
     "Abdelfattah, A., Khalil, M. I., & Abbas, H. (2025). *Automatic pronunciation error detection and correction "
     "of the Holy Quran's learners using deep learning* (arXiv:2509.00094). arXiv. https://arxiv.org/abs/2509.00094"),
    ("El Kheir", "2025a",
     "El Kheir, Y., Ibrahim, O., Meghanani, A., Almarwani, N., Toyin, H. O., Alharbi, S., Alfadly, M., Alkanhal, L., "
     "Selim, I., Elbatal, S., Mdhaffar, S., Hain, T., Hifny, Y., Shahin, M., & Ali, A. (2025a). *Towards a unified "
     "benchmark for Arabic pronunciation assessment: Quranic recitation as case study* (arXiv:2506.07722). arXiv. "
     "https://arxiv.org/abs/2506.07722"),
    ("El Kheir", "2025b",
     "El Kheir, Y., Meghanani, A., Toyin, H. O., Almarwani, N., Ibrahim, O., Elshahawy, Y. A., Shahin, M., & Ali, A. "
     "(2025b). Iqra'Eval: A shared task on Qur'anic pronunciation assessment. Dalam *Proceedings of the Third Arabic "
     "Natural Language Processing Conference: Shared Tasks* (hlm. 443–452). Association for Computational "
     "Linguistics. https://aclanthology.org/2025.arabicnlp-sharedtasks.61/"),
    ("El Kheir", "2026",
     "El Kheir, Y., Meghanani, A., Shahin, M., Ibrahim, O., Chowdhury, S. A., AlMarwani, N., Elshahawy, Y., & Ali, A. "
     "(2026). *IQRA 2026: Interspeech challenge on automatic pronunciation assessment for Modern Standard Arabic "
     "(MSA)* (arXiv:2603.29087). arXiv. https://arxiv.org/abs/2603.29087"),
    ("Firebase", "t.t.-a",
     "Firebase. (t.t.-a). *Default bucket and billing requirements for Cloud Storage for Firebase after September "
     "2024*. Diakses 19 Oktober 2026, dari https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024"),
    ("Firebase", "t.t.-b",
     "Firebase. (t.t.-b). *Firebase pricing*. Diakses 19 Oktober 2026, dari https://firebase.google.com/pricing"),
    ("Ionic", "t.t.",
     "Ionic. (t.t.). *Updating from Capacitor 7 to Capacitor 8*. Capacitor Documentation. Diakses 19 Oktober 2026, "
     "dari https://capacitorjs.com/docs/updating/8-0"),
    ("Mediana", "2026",
     "Mediana, C. (2026, 29 Agustus). Beredar peraturan pelaksana UU Perlindungan Data Pribadi. *Kompas.id*. "
     "https://www.kompas.id/artikel/peraturan-pelaksana-uu-pdp-akhirnya-terbit-lembaga-pengawas-masih-dinanti"),
    ("Salameh", "2024",
     "Salameh, R., Al Mdfaa, M., Askarbekuly, N., & Mazzara, M. (2024). *Quranic audio dataset: Crowdsourced and "
     "labeled recitation from non-Arabic speakers* (arXiv:2405.02675). arXiv. https://arxiv.org/abs/2405.02675"),
    ("Sharfina", "2016",
     "Sharfina, Z., & Santoso, H. B. (2016). An Indonesian adaptation of the System Usability Scale (SUS). Dalam "
     "*2016 International Conference on Advanced Computer Science and Information Systems (ICACSIS)* (hlm. 145–148). "
     "IEEE. https://doi.org/10.1109/ICACSIS.2016.7872776"),
    ("Suryana", "2026",
     "Suryana, A. R., Marlina, L., & Musthafa, I. (2026). Analisis komparatif kesalahan fonologis pengucapan huruf "
     "Arab dalam pembacaan Al-Qur'an pada penutur dewasa bahasa Sunda dan bahasa Jawa di Kabupaten Brebes. "
     "*Jurnal Pendidikan Bahasa, 16*(3). https://doi.org/10.37630/jpb.v16i3.4684"),
    ("Trofimovich", "2016",
     "Trofimovich, P., Isaacs, T., Kennedy, S., Saito, K., & Crowther, D. (2016). Flawed self-assessment: "
     "Investigating self- and other-perception of second language speech. *Bilingualism: Language and Cognition, "
     "19*(1), 122–140."),
    ("Uchihara", "2024",
     "Uchihara, T., Karas, M., & Thomson, R. I. (2024). Does perceptual high variability phonetic training improve "
     "L2 speech production? A meta-analysis of perception-production connection. *Applied Psycholinguistics, "
     "45*(4), 591–623. https://doi.org/10.1017/S0142716424000195"),
    ("Uchihara", "2025",
     "Uchihara, T., Karas, M., & Thomson, R. I. (2025). High variability phonetic training (HVPT): A meta-analysis "
     "of L2 perceptual training studies. *Studies in Second Language Acquisition*. "
     "https://doi.org/10.1017/S0272263125100879"),
    ("W3C", "2023",
     "World Wide Web Consortium [W3C]. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. "
     "https://www.w3.org/TR/WCAG22/"),
    ("Wright", "2011",
     "Wright, R., & McCloy, D. (2011). *Neutral sagittal section* [Gambar SVG, CC0 1.0]. Wikimedia Commons. "
     "https://commons.wikimedia.org/wiki/File:Neutral_Sagittal_Section.svg"),
]
