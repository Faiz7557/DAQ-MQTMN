# Makhraj (purwarupa React)

Aplikasi tahsin yang mengajarkan 29 huruf hijaiyah dari tempat keluarnya (makhraj). Satu basis kode React untuk **web/PWA** dan **Android** (Capacitor). Pengganti MVP Flutter di `../app/`. Rancangan dan dasar risetnya: `C:\Uner\Lomba\MTQMN\Penyisihan\reports\Rancangan prototype Makhraj React.md`.

## Menjalankan

```bash
npm install
npm run dev          # http://localhost:5173 (mikrofon/kamera butuh localhost atau HTTPS)
npm test             # tes Vitest: materi, sifat, sorot huruf, soal, SUS, hari belajar
npm run build        # dist/ siap di-hosting statis (Firebase Hosting, Cloudflare Pages, dll.)
npm run preview      # http://localhost:8078
npm run e2e          # Playwright + axe-core di Edge: audit WCAG 2.2 A/AA 12 layar, alur rekam, cermin kamera
npm run cap:sync     # build lalu salin ke android/
```

APK: buka `android/` di Android Studio (butuh Android SDK, JDK 21), lalu Build > Build APK. Android SDK belum terpasang di laptop ini, jadi APK belum pernah dibuat.

Tanpa Android SDK: jadikan folder `web/` root repo GitHub, lalu push. Workflow `.github/workflows/apk.yml` menjalankan tes, build, `cap sync`, dan `gradlew assembleDebug`; APK debug muncul di tab Actions > Artifacts. Push tag `v*` (mis. `git tag v0.2.0 && git push --tags`) untuk melampirkan APK ke GitHub Releases sebagai tautan unduh tanpa login (isi Tabel 4 proposal). Workflow ini belum pernah dijalankan.

## Fitur Tahap 1 (sudah jalan)

| Rute | Isi |
|---|---|
| Pengenalan | Muncul sekali saat pertama dibuka |
| `/` Beranda | Pelajaran berikutnya, huruf dikuasai x/29, hari belajar pekan ini (bisa disembunyikan), 29 ubin huruf |
| `/huruf/:id/:langkah` | Pelajaran 5 langkah: **Lihat** (penampang + titik + sifat + kesalahan umum), **Dengar** (klip guru YouTube + tombol harakat), **Tiru** (cermin kamera + rekam), **Bandingkan** (putar bergantian, gelombang, daftar cek, tandai dikuasai), **Terapkan** (contoh kata dari mushaf) |
| `/peta` | Penampang interaktif: 5 area, 17 titik, huruf per titik |
| `/mirip`, `/mirip/:i` | 6 pasangan: dua penampang, tabel perbandingan sifat, kuis otomatis |
| `/mushaf`, `/mushaf/:n?huruf=` | 114 surah Tanzil, cari surah, sorot kata yang memuat huruf (harakat diabaikan), terjemahan |
| `/saya` | Statistik, ukuran teks, sumber video, atribusi, hapus semua data |
| `/saya/studi`, `/tes/:fase`, `/sus` | Uji coba 20 peserta: persetujuan (18+), tes 20 soal bentuk A/B bergantian, SUS 10 butir, ekspor JSON |

Data pengguna disimpan di perangkat: progres di `localStorage` (`makhraj-v1`), rekaman di IndexedDB (`makhraj/rekaman`). Tidak ada yang diunggah.

## Peta kode

| Path | Isi |
|---|---|
| `src/data/materi.json` | **Konten**: 5 area, 17 titik (dengan deskripsi dari Fath Rabb), 29 huruf (titik, video, pelajaran), 6 pasangan mirip. Bisa diedit tanpa menyentuh kode |
| `src/data/materi.ts` | Tipe, sifat dihitung dari kelompok huruf matan Al-Jazariyyah, harakat, pencocokan huruf di mushaf, generator kuis dan tes |
| `src/store.ts` | Progres, log pemakaian, hasil tes/SUS, rekaman IndexedDB, ekspor studi |
| `src/components.tsx` | Komponen UI, penampang kepala (SVG), klip YouTube (IFrame API resmi) |
| `src/screens/` | `belajar` (beranda, pelajaran, peta, mirip), `latihan` (rekam/bandingkan), `mushaf`, `saya` (profil, studi, tes, SUS) |
| `public/data/` | Teks Tanzil + terjemahan + lisensi (disalin dari `../app/assets/quran`) |
| `android/` | Proyek Capacitor; izin `RECORD_AUDIO` dan `CAMERA` sudah ada di manifest |

## Yang masih harus dikerjakan tim

1. **Validasi guru.** Semua materi `"tervalidasi": false`; badge "Belum divalidasi pengajar" tampil di setiap pelajaran.
2. **Detik klip harakat.** Tombol harakat memutar video dari awal; isi `mulai`/`selesai` per harakat agar dipotong dengan `loadVideoById({startSeconds, endSeconds})`.
3. **Pelajaran rinci 26 huruf** (langkah animasi, kesalahan umum, daftar cek khusus). Saat ini hanya ب ح ه yang rinci; huruf lain memakai deskripsi titik dan sifat yang dihitung otomatis.
4. **Klip alif** belum ada di kedua kanal. ض dan ط memakai kanal resmi Dr. Ayman Swaid.
5. **Izin**: kanal Al-Andalasy dan kanal resmi (video), LPMQ (terjemahan; Tanzil hanya nonkomersial).
6. **Penampang kepala** masih ilustrasi sederhana; gambar ulang di atas basis CC0 (Wright & McCloy, Wikimedia Commons) dan minta guru memeriksa letak titik.
7. **SUS**: ganti terjemahan kerja dengan versi tervalidasi (Sharfina & Santoso, 2016) sebelum studi resmi.
8. **Uji di perangkat Android nyata**: YouTube di WebView bisa gagal (Error 153); tautan "Buka di YouTube" disediakan sebagai cadangan.
9. **Tahap 2**: Firebase (Auth anonim + Firestore asia-southeast2), setor ke pengajar (butuh paket Blaze untuk Storage).

## Sumber dan lisensi

- Teks Al-Qur'an: Tanzil Project, Uthmani 1.1, CC BY 3.0, ditampilkan tanpa perubahan.
- Terjemahan: Kementerian Agama RI melalui Tanzil, nonkomersial.
- Video: Asy-Syaikh Aiman Rusydi Suwaid (kanal Al-Andalasy dan kanal resmi), pemutar resmi YouTube, tidak diunduh.
- Font: Scheherazade New dan Plus Jakarta Sans (SIL OFL) lewat Fontsource.
