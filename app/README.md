# Makhraj (MVP)

Aplikasi tahsin untuk pemula yang mengajarkan huruf hijaiyah dari tempat keluarnya (makhraj). Satu basis kode Flutter untuk **web** dan **Android**. Proposal lombanya ada di `../paper/`.

## Fitur Tahap 1 (MVP)

| Layar | Rute | Isi |
|---|---|---|
| Beranda | `/` | Pelajaran berikutnya, huruf dikuasai x/29, hari beruntun, menu |
| Peta makhraj | `/peta` | Penampang kepala interaktif, 5 area (ketuk area atau chip), daftar huruf per area |
| Pelajaran huruf | `/huruf/:id` | Sorotan titik makhraj, animasi 3 langkah (ب), video Syaikh Aiman Suwaid, tombol harakat, letak makhraj, sifat, kesalahan umum |
| Rekam & bandingkan | `/latihan/:id` | Cermin kamera depan, klip guru, rekam suara lokal + gelombang, daftar cek mandiri, tandai dikuasai |
| Huruf mirip | `/mirip`, `/mirip/:i` | 6 pasangan; ح-ه lengkap dengan perbandingan titik dan kuis |
| Mushaf | `/mushaf`, `/mushaf/:n?huruf=ba` | 114 surah (teks Tanzil), cari surah, sorot kata yang memuat huruf yang dipelajari, terjemahan Kemenag |
| Profil | `/profil` | Statistik, sumber & atribusi, atur ulang progres |

Belum termasuk (sesuai proposal): setor ke pengajar (Tahap 2), penilaian AI (Tahap 3), dan login/sinkronisasi Firebase. Progres saat ini disimpan di perangkat (`shared_preferences`).

## Menjalankan

Toolchain dipasang di `D:\dev` dan tidak mengubah pengaturan sistem. Muat dulu di setiap terminal baru:

```powershell
. .\tool\env.ps1      # PowerShell
```
```bash
source tool/env.sh    # Git Bash
```

```bash
flutter pub get
flutter run -d chrome                       # web (mode debug)
flutter test                                # 9 tes data + alur
flutter build web --release --no-web-resources-cdn
flutter build apk --debug                   # butuh Android SDK, lihat di bawah
```

Mode demo untuk video dan screenshot (web): `http://localhost:8077/?demo=1#/` mengisi 3 huruf dikuasai dan 5 hari beruntun. `&frame=390x844` merender dalam bingkai ponsel berukuran tetap, dipakai `tool/capture.py`.

## Peta kode

| Path | Isi |
|---|---|
| `assets/data/materi.json` | **Semua materi tajwid**: 5 area, 29 huruf (area, ID video, titik), pelajaran ب/ح/ه, 6 pasangan mirip + kuis. Bisa diedit tanpa menyentuh kode. |
| `assets/quran/` | Hasil `tool/build_quran.py` dari teks Tanzil (jangan diedit manual) |
| `lib/data/` | Model materi, pemuat Al-Qur'an + pencocokan huruf, progres |
| `lib/widgets/head_diagram.dart` | Penampang kepala (path SVG dari desain) + sorotan beranimasi |
| `lib/widgets/common.dart` | Header, ubin huruf, `KlipGuru` (thumbnail, lalu YouTube IFrame resmi), navigasi bawah |
| `lib/screens/` | Satu file per layar |
| `tool/` | `env.ps1`/`env.sh`, `build_quran.py`, `capture.py` (screenshot proposal) |

## Yang perlu dilengkapi tim

1. **Validasi materi.** Semua pelajaran bertanda `"tervalidasi": false` dan aplikasi menampilkan badge "Belum divalidasi pengajar". Setelah ditinjau guru tahsin, ubah menjadi `true`.
2. **Detik klip harakat.** `"mulai": null` di `materi.json` membuat tombol harakat memutar video dari awal. Catat detiknya dari video (misalnya `"mulai": 12.5`).
3. **Pelajaran 26 huruf lainnya** (titik rinci, sifat, kesalahan umum), dan materi untuk 5 pasangan mirip lainnya.
4. **Video untuk ا, ض, ط.** Huruf-huruf ini tidak ada di playlist Al-Andalasy.
5. **Izin**: kanal Al-Andalasy (video) dan LPMQ Kemenag (terjemahan) sebelum ada fitur berbayar.
6. **Firebase** (Auth + Firestore + Hosting): jalankan `flutterfire configure` dengan proyek milik tim, lalu sambungkan `Progress` ke Firestore.
7. **Gambar penampang kepala** masih ilustrasi sederhana dari desain; sebaiknya diganti gambar anatomi yang dicek guru.

## Sumber dan lisensi konten

- Teks Al-Qur'an: Tanzil Project, Uthmani 1.1, CC BY 3.0 (ditampilkan tanpa perubahan; lisensi lengkap di `assets/quran/TANZIL_LICENSE.txt`).
- Terjemahan: Kementerian Agama RI melalui Tanzil, untuk penggunaan nonkomersial.
- Video: Asy-Syaikh Aiman Rusydi Suwaid, kanal YouTube Al-Andalasy, diputar lewat pemutar resmi YouTube (tidak diunduh).
- Font: Noto Naskh Arabic dan Plus Jakarta Sans (SIL Open Font License).
