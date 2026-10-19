# Validasi `app/assets/data/materi.json` terhadap *Fath Rabb al-Bariyyah*

Rujukan: Salim, S. M. (2007). *Fath Rabb al-Bariyyah: Syarh al-Muqaddimah al-Jazariyyah fi 'ilm at-tajwid* (Edisi ke-4).
Nomor halaman di bawah adalah **halaman PDF** (file `فتح رب البرية شرح المقدمة الجزرية.pdf`), bukan folio cetak.

Cakupan: bab Makharij al-Huruf (PDF 31-41) dan bab Shifat al-Huruf (PDF 43-54).
Pemeriksaan ini tidak menggantikan tinjauan pengajar bersanad; kolom `tervalidasi` tetap `false`.

## Sesuai kitab

| Bagian materi.json | Kitab | Halaman PDF |
|---|---|---|
| 17 titik makhraj dalam 5 area (jauf, halq, lisan, syafatain, khaisyum) | Pendapat yang dipilih: 17 makhraj, 5 makhraj umum | 31-32 |
| `jauf`: rongga mulut dan tenggorokan, tempat huruf mad; anggota alif, wau, ya | "الفراغ الذي بداخل الفم والحلق"; alif, wau dan ya madiyyah | 33 |
| `halq`: pangkal (ء ه), tengah (ع ح), ujung (غ خ) | Aqsha, wasath, adna al-halq dengan pembagian yang sama | 33-34 |
| `lisan`: 18 huruf | Makhraj 5-14 (10 titik) di lidah, total 18 huruf | 34-39 |
| `syafatain`: ب م dengan bibir rapat, ف dari bibir bawah dan gigi atas | "الشفتان معاً بانطباق"; ف dari "بطن الشفة السفلى مع أطراف الثنايا العليا" | 39 |
| `khaisyum`: tempat ghunnah pada ن dan م | Ghunnah keluar dari khaisyum pada nun dan mim | 40 |
| `ba` 6 sifat: jahr, syiddah, istifal, infitah, idzlaq, qalqalah | Ba di luar huruf hams; termasuk أجد قط بكت, فر من لب, قطب جد; di luar huruf isti'la dan ithbaq | 44-54 |
| `ba` arti Jahr "napas tertahan", Syiddah "suara tertahan" | Jahr: "انحباس النفس"; Syiddah: "انحباس الصوت" | 45 |
| `ba` qalqalah hanya saat sukun (langkah 3, kesalahan umum, latihan أَبْ) | "ويشترط لقلقلة هذه الحروف أن تكون ساكنة" | 54 |
| `haa` wasthul halq, `ha` aqshal halq, kuis mirip ح/ه | Sama | 33 |

## Perlu disesuaikan

Usulan 1-3 sudah diterapkan ke `materi.json` (19 Oktober 2026); usulan 4 memang tanpa perubahan. Semua tetap menunggu tinjauan guru (`tervalidasi: false`).

1. **`area.khaisyum.deskripsi`**: "Pangkal hidung" → kitab: "خرق الأنف المنجذب إلى داخل الفم", yaitu rongga hidung bagian dalam yang tersambung ke mulut (PDF 40). Usul: "Rongga hidung bagian dalam. Tempat keluarnya dengung (ghunnah) pada ن dan م."
2. **`area.syafatain.deskripsi`**: "و dengan memonyongkan" → kitab: wau keluar dari dua bibir "بانفتاح" dan keterangan gambar "باستدارة الشفتين مع ارتفاع أقصى اللسان" (PDF 39). Usul: "و dengan membulatkan bibir tanpa merapatkannya."
3. **`ba.sifat` Istifal "tipis"**: "tipis" adalah akibat (tarqiq), sedangkan definisinya "انحطاط مؤخرة اللسان عن الحنك الأعلى" (PDF 51). Usul: "pangkal lidah turun, huruf tipis".
4. **`ba.sifat` Idzlaq "ringan diucapkan"**: sesuai definisi "سرعة النطق" (PDF 52). Namun syarih mencatat bahwa idzlaq dan ishmat adalah sifat leksikal yang tidak memengaruhi pelafalan (PDF 53). Usul: biarkan, tetapi jangan dijadikan bahan latihan pelafalan.

## Tidak disebut di kitab ini (cek ke *At-Tajwid al-Mushawwar* atau guru)

- `ba.pelajaran.makhraj` dan langkah 1: "pada bagian yang basah" (kitab hanya menyebut "بانطباق").
- `ba` langkah 2: "Berbeda dengan bunyi p".
- `haa.pelajaran.makhraj`: "seperti berbisik dalam dan sedikit tertekan"; `ha`: "seperti napas yang ringan dan lepas". Keduanya tidak bertentangan dengan sifat hams (PDF 45), tetapi juga tidak tertulis di kitab.
- Koordinat `elips` dan `titik` (ilustrasi app) tidak bisa divalidasi dari teks. Bandingkan secara visual dengan gambar kitab (Gambar 1-12, PDF 33-40).
