import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router'
import { materi, tesMakhraj } from '../data/materi'
import { eksporStudi, hariBeruntun, hariPekanIni, rekaman, skorSus, useApp } from '../store'
import { Catatan, Halaman, Ikon, Kartu, Logo, Saklar, Segmen, Subjudul, Tombol, temaSistem, terapkanTema, toast } from '../components'

// ================= Profil =================
export function Saya() {
  const s = useApp()
  const [jmlRekaman, setJml] = useState(0)
  const nav = useNavigate()
  useEffect(() => { rekaman.semua().then((r) => setJml(r.length)).catch(() => {}) }, [])
  const hapusSemua = async () => {
    if (!confirm('Hapus semua progres, hasil tes, dan rekaman di perangkat ini? Tindakan ini tidak dapat dibatalkan.')) return
    await rekaman.hapusSemua().catch(() => {})
    s.reset()
    setJml(0)
    toast('Semua data di perangkat ini sudah dihapus.')
  }
  return (
    <Halaman judul="Saya" sub="Progres & pengaturan" kembali={false} lebar="lebar">
      <div className="mb-5 grid grid-cols-3 gap-3 sm:gap-4">
        {[
          [`${s.dikuasai.length}/${materi.huruf.length}`, 'huruf dikuasai'],
          [String(s.pengaturan.tampilkanHari ? hariBeruntun(s.hariAktif) : s.hariAktif.length), s.pengaturan.tampilkanHari ? 'hari beruntun' : 'hari belajar'],
          [String(jmlRekaman), 'rekaman'],
        ].map(([v, l]) => (
          <Kartu key={l} className="!p-4 text-center sm:!p-5 sm:text-left">
            <p className="text-2xl font-extrabold tracking-tight sm:text-3xl">{v}</p>
            <p className="mt-0.5 text-xs text-grey sm:text-sm">{l}</p>
          </Kartu>
        ))}
      </div>

      <div className="grid gap-4 xl:grid-cols-2 xl:items-start xl:gap-6">
        <div className="space-y-4">
          <Kartu>
            <Subjudul>Pengaturan</Subjudul>
            <p className="mb-2 text-[0.95rem] font-semibold">Tampilan</p>
            <Segmen label="Tampilan" nilai={s.pengaturan.tema ?? 'sistem'}
              onUbah={(v) => terapkanTema(v === 'sistem' ? temaSistem() : v, undefined, () => s.atur({ tema: v }))}
              pilihan={([['sistem', 'auto', 'Otomatis'], ['terang', 'sun', 'Terang'], ['gelap', 'moon', 'Gelap']] as const)
                .map(([v, i, l]) => ({ v, l: <span className="inline-flex items-center gap-1.5"><Ikon n={i} className="size-4" />{l}</span> }))} />
            <p className="mt-2 text-xs text-grey">Otomatis mengikuti pengaturan terang/gelap perangkat.</p>
            <div className="my-4 border-t border-line" />
            <p className="mb-2 text-[0.95rem] font-semibold">Ukuran teks</p>
            <Segmen label="Ukuran teks" nilai={s.pengaturan.skalaTeks} onUbah={(v) => s.atur({ skalaTeks: v })}
              pilihan={[{ v: 0.9, l: 'Kecil' }, { v: 1, l: 'Normal' }, { v: 1.15, l: 'Besar' }, { v: 1.3, l: 'Terbesar' }]} />
            <div className="my-4 border-t border-line" />
            <Saklar cek={s.pengaturan.tampilkanHari} onUbah={(v) => s.atur({ tampilkanHari: v })}
              judul="Tampilkan hitungan hari belajar" ket="Matikan jika hitungan membuat Anda belajar demi angka." />
            <div className="my-4 border-t border-line" />
            <p className="mb-2 text-[0.95rem] font-semibold">Sumber klip guru</p>
            <Segmen label="Sumber klip guru" nilai={s.pengaturan.sumberVideo} onUbah={(v) => s.atur({ sumberVideo: v })}
              pilihan={[{ v: 'andalasy', l: 'Al-Andalasy' }, { v: 'resmi', l: 'Kanal resmi' }]} />
            <p className="mt-2 text-xs text-grey">{s.pengaturan.sumberVideo === 'andalasy' ? 'Sesi panjang dari kanal Al-Andalasy.' : 'Klip pendek dari kanal resmi Dr. Ayman Swaid.'}</p>
          </Kartu>

          <Link to="/saya/studi" className="tekan group flex items-center gap-4 rounded-[1.5rem] border border-line bg-surface p-5 shadow-kartu hover:border-tint">
            <span className="grid size-12 shrink-0 place-items-center rounded-2xl bg-teal-light text-teal-dark"><Ikon n="list" /></span>
            <span className="min-w-0 flex-1"><span className="block font-bold">Uji coba aplikasi</span><span className="block text-sm text-grey">Tes pemahaman, kuesioner SUS, ekspor data</span></span>
            <Ikon n="next" className="size-5 text-grey transition-transform group-hover:translate-x-0.5" />
          </Link>
        </div>

        <div className="space-y-4">
          <Kartu>
            <Subjudul>Peta jalan</Subjudul>
            <ol className="relative space-y-4 text-sm leading-relaxed before:absolute before:top-2 before:bottom-2 before:left-[0.6875rem] before:w-px before:bg-border">
              {([
                ['Tahap 1 (versi ini)', '29 huruf, peta makhraj, rekam dan bandingkan, huruf mirip, mushaf dengan sorot huruf.', true],
                ['Tahap 2', 'Akun dan sinkronisasi, setor bacaan ke pengajar, koreksi per huruf, dasbor kelas.', false],
                ['Tahap 3', 'Penilaian makhraj berbantuan AI dari rekaman yang sudah dikoreksi pengajar; nilai yang tidak meyakinkan tetap diteruskan ke pengajar.', false],
              ] as const).map(([j, t, aktif]) => (
                <li key={j} className="relative flex gap-3">
                  <span className={`relative mt-0.5 grid size-6 shrink-0 place-items-center rounded-full ring-4 ring-surface ${aktif ? 'bg-teal text-white' : 'bg-sand text-grey'}`}>
                    {aktif ? <Ikon n="check" className="size-3.5" /> : <span className="size-1.5 rounded-full bg-current" />}
                  </span>
                  <span className={aktif ? '' : 'text-grey'}><strong className="block text-ink">{j}</strong>{t}</span>
                </li>
              ))}
            </ol>
          </Kartu>

          <Kartu>
            <Subjudul>Sumber dan atribusi</Subjudul>
            <ul className="divide-y divide-line text-sm leading-relaxed text-grey">
              <li className="pb-2.5"><strong className="text-ink">Materi makhraj dan sifat:</strong> Al-Muqaddimah al-Jazariyyah dan Fath Rabb al-Bariyyah. Semua materi belum divalidasi pengajar bersanad.</li>
              <li className="py-2.5"><strong className="text-ink">Klip guru:</strong> Asy-Syaikh Aiman Rusydi Suwaid, kanal YouTube Al-Andalasy dan kanal resmi Dr. Ayman Swaid, diputar lewat pemutar resmi YouTube tanpa diunduh.</li>
              <li className="py-2.5"><strong className="text-ink">Teks Al-Qur'an:</strong> Tanzil Project, Uthmani 1.1, CC BY 3.0 (tanpa perubahan).</li>
              <li className="py-2.5"><strong className="text-ink">Terjemahan:</strong> Kementerian Agama RI melalui Tanzil, nonkomersial.</li>
              <li className="pt-2.5"><strong className="text-ink">Font:</strong> Scheherazade New dan Plus Jakarta Sans (SIL Open Font License).</li>
            </ul>
          </Kartu>
        </div>
      </div>

      <div className="mx-auto mt-8 max-w-md">
        <Tombol varian="bahaya" ikon="trash" className="w-full" onClick={hapusSemua}>Hapus semua data di perangkat ini</Tombol>
        <button onClick={() => { s.atur({ onboarding: false }); nav('/') }} className="mt-2 min-h-11 w-full rounded-xl text-sm font-semibold text-tint hover:bg-teal-light">Lihat pengenalan aplikasi lagi</button>
        <p className="mt-4 text-center text-xs text-grey">Makhraj versi 0.2.0 (purwarupa React)</p>
      </div>
    </Halaman>
  )
}

// ================= Pengenalan (pertama kali dibuka) =================
const HURUF_HIAS = ['ب', 'ح', 'ع', 'ق', 'ض', 'ص', 'ط', 'ظ', 'ه']

export function Pengenalan() {
  const { atur } = useApp()
  return (
    <main className="grid min-h-dvh lg:grid-cols-[1fr_1.05fr]">
      <section className="relative flex min-h-[38dvh] items-center justify-center overflow-hidden rounded-b-[2.5rem] bg-gradient-to-br from-[#147a73] via-[#0f5e5e] to-[#0a4343] px-6 pt-[env(safe-area-inset-top)] lg:sticky lg:top-0 lg:h-dvh lg:rounded-none">
        <span className="pola-khatam absolute inset-0 opacity-90" />
        <div aria-hidden className="absolute inset-0 grid grid-cols-3 place-items-center gap-6 p-10 opacity-[0.12] lg:p-20">
          {HURUF_HIAS.map((h) => <span key={h} lang="ar" className="arab text-6xl text-white lg:text-8xl">{h}</span>)}
        </div>
        <div className="animate-muncul relative flex flex-col items-center text-center text-white">
          <Logo className="size-24 rounded-[1.75rem] text-6xl shadow-angkat ring-1 ring-white/30 lg:size-32 lg:text-7xl" />
          <p className="mt-4 text-2xl font-extrabold tracking-tight lg:text-3xl">Makhraj</p>
          <p className="text-sm text-white/75">Huruf dari tempat keluarnya</p>
        </div>
      </section>

      <section className="mx-auto flex w-full max-w-xl flex-col justify-center px-6 py-10 pb-[max(2.5rem,env(safe-area-inset-bottom))] lg:px-12">
        <div className="animate-masuk">
          <p className="label-kecil mb-2">Selamat datang</p>
          <h1 className="judul-besar mb-4 text-[2.25rem] sm:text-5xl">Belajar huruf dari tempat keluarnya</h1>
          <p className="mb-8 text-lg leading-relaxed text-grey">Lihat letak makhraj di penampang mulut, dengarkan guru bersanad, rekam bacaan Anda, lalu temukan hurufnya di dalam ayat.</p>
          <ul className="mb-8 grid gap-3 sm:grid-cols-2">
            {[
              ['map', 'Lihat', 'Penampang mulut dan tenggorokan menyorot titik makhraj.'],
              ['play', 'Dengar', 'Contoh dari Asy-Syaikh Aiman Rusydi Suwaid.'],
              ['mic', 'Tiru dan bandingkan', 'Rekam sendiri, putar bergantian, cek dengan daftar.'],
              ['book', 'Terapkan', 'Sorot huruf yang dipelajari di mushaf.'],
            ].map(([i, j, t]) => (
              <li key={j} className="flex gap-3 rounded-2xl border border-line bg-surface p-3.5 shadow-kartu">
                <span className="grid size-10 shrink-0 place-items-center rounded-xl bg-teal-light text-teal-dark"><Ikon n={i} /></span>
                <span className="text-sm leading-snug"><strong className="block text-[0.95rem]">{j}</strong><span className="text-grey">{t}</span></span>
              </li>
            ))}
          </ul>
          <Catatan nada="teal">Makhraj tidak menggantikan guru. Aplikasi ini menyiapkan Anda sebelum dan di antara pertemuan talaqqi.</Catatan>
          <Tombol className="mt-6 w-full text-base" onClick={() => atur({ onboarding: true })}>Mulai belajar <Ikon n="next" /></Tombol>
        </div>
      </section>
    </main>
  )
}

// ================= Uji coba: persetujuan, tes, SUS, ekspor =================
const bentukUntuk = (kode: string | undefined, fase: 'sebelum' | 'sesudah'): 'A' | 'B' => {
  // Urutan bentuk ditukar antarpeserta: nomor ganjil A lalu B, nomor genap B lalu A.
  const genap = Number((kode ?? '').replace(/\D/g, '') || 1) % 2 === 0
  return (fase === 'sebelum') !== genap ? 'A' : 'B'
}

const KOTAK_CEK = 'mt-0.5 size-5 shrink-0 accent-teal'

export function Studi() {
  const s = useApp()
  const studi = s.pengaturan.studi
  const [kode, setKode] = useState('')
  const [dewasa, setDewasa] = useState(false)
  const [setuju, setSetuju] = useState(false)
  const sebelum = s.tes.find((t) => t.fase === 'sebelum'), sesudah = s.tes.find((t) => t.fase === 'sesudah')
  const unduh = () => {
    const url = URL.createObjectURL(new Blob([eksporStudi()], { type: 'application/json' }))
    const a = Object.assign(document.createElement('a'), { href: url, download: `makhraj-studi-${studi?.kode ?? 'tanpa-kode'}.json` })
    a.click()
    URL.revokeObjectURL(url)
  }
  return (
    <Halaman judul="Uji coba aplikasi">
      {!studi ? (
        <Kartu>
          <Subjudul>Lembar persetujuan</Subjudul>
          <div className="space-y-3 text-sm leading-relaxed text-grey">
            <p>Uji coba ini menilai kegunaan aplikasi dan pemahaman makhraj selama dua pekan. Yang dikumpulkan: jawaban tes, kuesioner SUS, huruf yang ditandai dikuasai, dan catatan pemakaian (waktu membuka pelajaran, merekam, membaca surah).</p>
            <p><strong className="text-ink">Rekaman suara tidak ikut diekspor</strong> dan tetap di perangkat Anda. Data dikirim hanya jika Anda sendiri mengunduh berkas ekspor dan menyerahkannya kepada peneliti.</p>
            <p>Anda boleh berhenti kapan saja dan menghapus semua data dari halaman Saya. Data dipakai hanya untuk evaluasi aplikasi ini, sesuai UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi.</p>
          </div>
          <label className="mt-5 block text-sm font-semibold">Kode peserta dari peneliti
            <input value={kode} onChange={(e) => setKode(e.target.value.toUpperCase().slice(0, 8))} placeholder="mis. P07"
              className="mt-1.5 min-h-12 w-full rounded-2xl border border-line bg-cream px-4 font-normal outline-none placeholder:text-grey focus:border-tint" />
          </label>
          <div className="mt-4 space-y-1 rounded-2xl bg-sand p-2">
            <label className="flex min-h-11 cursor-pointer items-start gap-3 rounded-xl p-2 text-sm hover:bg-surface"><input type="checkbox" className={KOTAK_CEK} checked={dewasa} onChange={(e) => setDewasa(e.target.checked)} />Saya berusia 18 tahun atau lebih.</label>
            <label className="flex min-h-11 cursor-pointer items-start gap-3 rounded-xl p-2 text-sm hover:bg-surface"><input type="checkbox" className={KOTAK_CEK} checked={setuju} onChange={(e) => setSetuju(e.target.checked)} />Saya sudah membaca penjelasan di atas dan bersedia ikut.</label>
          </div>
          <Tombol className="mt-5 w-full" disabled={!kode || !dewasa || !setuju}
            onClick={() => { s.atur({ studi: { kode, dewasa, setuju: new Date().toISOString() } }); s.catat('setuju_studi') }}>Ikut uji coba</Tombol>
          <p className="mt-3 text-center text-xs text-grey">Peserta di bawah 18 tahun memerlukan persetujuan orang tua di luar aplikasi.</p>
        </Kartu>
      ) : (
        <div className="space-y-3">
          <Catatan nada="teal">Peserta <strong>{studi.kode}</strong> · hari belajar 7 hari terakhir: <strong>{hariPekanIni(s.hariAktif)}</strong>/7 (target minimal 4).</Catatan>
          {[
            { to: '/tes/sebelum', j: 'Tes sebelum belajar', d: sebelum ? `Selesai · skor ${sebelum.skor}/${sebelum.total}` : '20 soal · sekitar 10 menit', ok: !!sebelum },
            { to: '/', j: 'Belajar dua pekan', d: `${s.dikuasai.length}/29 huruf dikuasai`, ok: false },
            { to: '/tes/sesudah', j: 'Tes sesudah belajar', d: sesudah ? `Selesai · skor ${sesudah.skor}/${sesudah.total}` : 'Kerjakan setelah dua pekan', ok: !!sesudah },
            { to: '/sus', j: 'Kuesioner kegunaan (SUS)', d: s.sus.length ? `Selesai · skor ${s.sus.at(-1)!.skor}` : '10 pernyataan', ok: s.sus.length > 0 },
          ].map((x, k) => (
            <Link key={x.to + x.j} to={x.to} className="tekan group flex items-center gap-4 rounded-[1.5rem] border border-line bg-surface p-4 shadow-kartu hover:border-tint">
              <span className={`grid size-11 shrink-0 place-items-center rounded-full text-sm font-bold ${x.ok ? 'bg-teal text-white' : 'bg-sand text-ink'}`}>{x.ok ? <Ikon n="check" /> : k + 1}</span>
              <span className="min-w-0 flex-1"><span className="block font-bold">{x.j}</span><span className="block text-sm text-grey">{x.d}</span></span>
              <Ikon n="next" className="size-5 text-grey transition-transform group-hover:translate-x-0.5" />
            </Link>
          ))}
          <Tombol varian="garis" ikon="download" className="mt-2 w-full" onClick={unduh}>Unduh data uji coba (JSON)</Tombol>
          <button className="min-h-11 w-full rounded-xl text-sm text-grey hover:bg-sand" onClick={() => { if (confirm('Keluar dari uji coba? Hasil tes tetap tersimpan sampai Anda menghapus data.')) s.atur({ studi: null }) }}>Keluar dari uji coba</button>
        </div>
      )}
    </Halaman>
  )
}

export function Tes() {
  const { fase = 'sebelum' } = useParams() as { fase: 'sebelum' | 'sesudah' }
  const s = useApp()
  const nav = useNavigate()
  const bentuk = bentukUntuk(s.pengaturan.studi?.kode, fase)
  const [soal] = useState(() => tesMakhraj(bentuk))
  const [i, setI] = useState(0)
  const [jawab, setJawab] = useState<Record<string, string>>({})
  const [hasil, setHasil] = useState<number | null>(null)
  const x = soal[i]
  const kirim = () => {
    const skor = soal.filter((q) => jawab[q.id] === q.jawab).length
    s.simpanTes({ bentuk, fase, skor, total: soal.length, jawaban: jawab, t: new Date().toISOString() })
    s.catat('tes', undefined, `${fase}:${bentuk}:${skor}`)
    setHasil(skor)
  }
  if (hasil !== null) return (
    <Halaman judul="Tes selesai">
      <Kartu className="py-10 text-center">
        <p className="label-kecil">Skor Anda</p>
        <p className="my-3 text-6xl font-extrabold tracking-tight">{hasil}<span className="text-2xl font-semibold text-grey">/{soal.length}</span></p>
        <p className="mx-auto max-w-sm text-sm text-grey">Kunci jawaban tidak ditampilkan agar tes sesudah belajar tetap adil.</p>
      </Kartu>
      <Tombol className="mt-4 w-full" onClick={() => nav('/saya/studi', { replace: true })}>Kembali ke uji coba</Tombol>
    </Halaman>
  )
  return (
    <Halaman judul={`Tes ${fase} belajar · bentuk ${bentuk}`}>
      <div className="mb-2 flex items-center justify-between text-sm font-semibold text-grey">
        <span>Soal {i + 1} dari {soal.length}</span><span>{Object.keys(jawab).length} terjawab</span>
      </div>
      <div className="mb-5 h-2 overflow-hidden rounded-full bg-sand" role="progressbar" aria-valuenow={i + 1} aria-valuemin={1} aria-valuemax={soal.length} aria-label="Kemajuan tes">
        <div className="h-full rounded-full bg-tint transition-all duration-500" style={{ width: `${((i + 1) / soal.length) * 100}%` }} />
      </div>
      <Kartu key={i} className="animate-muncul">
        <p className="mb-4 text-lg font-semibold leading-snug sm:text-xl">{x.tanya}</p>
        {x.arab && <p className="mb-4 rounded-2xl bg-sand py-2 text-center"><span lang="ar" dir="rtl" className="arab text-6xl">{x.arab}</span></p>}
        <div className={`grid gap-2 ${x.opsi[0].arab ? 'grid-cols-2' : 'grid-cols-1'}`}>
          {x.opsi.map((o) => (
            <button key={o.id} onClick={() => setJawab({ ...jawab, [x.id]: o.id })} aria-pressed={jawab[x.id] === o.id}
              className={`min-h-14 rounded-2xl border-2 px-4 text-left font-semibold ${o.arab ? 'arab text-center text-3xl' : ''} ${jawab[x.id] === o.id ? 'border-teal bg-teal-light text-teal-dark' : 'border-line bg-surface hover:border-tint'}`}>
              {o.label}
            </button>
          ))}
        </div>
      </Kartu>
      <div className="mt-4 flex gap-3">
        <Tombol varian="garis" disabled={i === 0} onClick={() => setI(i - 1)} className="flex-1">Sebelumnya</Tombol>
        {i < soal.length - 1
          ? <Tombol disabled={!jawab[x.id]} onClick={() => setI(i + 1)} className="flex-1">Berikutnya</Tombol>
          : <Tombol disabled={Object.keys(jawab).length < soal.length} onClick={kirim} className="flex-1">Selesai</Tombol>}
      </div>
    </Halaman>
  )
}

// Terjemahan kerja SUS. Ganti dengan versi tervalidasi (Sharfina & Santoso, 2016) sebelum studi resmi.
const SUS = [
  'Saya rasa saya akan sering menggunakan aplikasi ini.',
  'Saya merasa aplikasi ini rumit tanpa alasan yang jelas.',
  'Saya merasa aplikasi ini mudah digunakan.',
  'Saya merasa membutuhkan bantuan orang yang paham teknologi untuk dapat menggunakan aplikasi ini.',
  'Saya merasa fitur-fitur aplikasi ini terpadu dengan baik.',
  'Saya merasa banyak hal yang tidak konsisten dalam aplikasi ini.',
  'Saya membayangkan kebanyakan orang akan cepat belajar menggunakan aplikasi ini.',
  'Saya merasa aplikasi ini sangat merepotkan untuk digunakan.',
  'Saya merasa sangat percaya diri menggunakan aplikasi ini.',
  'Saya perlu mempelajari banyak hal sebelum dapat menggunakan aplikasi ini.',
]

export function Sus() {
  const s = useApp()
  const nav = useNavigate()
  const [j, setJ] = useState<number[]>(Array(10).fill(0))
  const lengkap = j.every((x) => x > 0)
  return (
    <Halaman judul="Kuesioner kegunaan (SUS)">
      <Catatan nada="teal">Pilih seberapa setuju Anda: <strong>1</strong> = sangat tidak setuju, <strong>5</strong> = sangat setuju.</Catatan>
      <ol className="mt-4 space-y-3">
        {SUS.map((t, i) => (
          <li key={i}>
            <Kartu className="!p-4 sm:!p-5">
              <fieldset>
                <legend className="mb-3 font-semibold leading-snug"><span className="text-grey">{i + 1}.</span> {t}</legend>
                <div className="grid grid-cols-5 gap-2">
                  {[1, 2, 3, 4, 5].map((v) => (
                    <label key={v} className={`flex min-h-12 cursor-pointer items-center justify-center rounded-xl border font-bold transition-colors has-[:focus-visible]:outline-3 has-[:focus-visible]:outline-tint ${j[i] === v ? 'border-teal bg-teal text-white' : 'border-line bg-cream hover:border-tint'}`}>
                      <input type="radio" name={`sus${i}`} className="sr-only" checked={j[i] === v} onChange={() => setJ(j.map((x, k) => (k === i ? v : x)))} />{v}
                    </label>
                  ))}
                </div>
                <div className="mt-1.5 flex justify-between text-[0.7rem] text-grey" aria-hidden><span>Sangat tidak setuju</span><span>Sangat setuju</span></div>
              </fieldset>
            </Kartu>
          </li>
        ))}
      </ol>
      <Tombol className="mt-5 w-full" disabled={!lengkap} onClick={() => {
        const skor = skorSus(j)
        s.simpanSus({ jawaban: j, skor, t: new Date().toISOString() })
        s.catat('sus', undefined, String(skor))
        toast(`Terima kasih. Skor SUS: ${skor}`)
        nav('/saya/studi', { replace: true })
      }}>Kirim jawaban {!lengkap && `(${j.filter((x) => x > 0).length}/10)`}</Tombol>
      <p className="mt-3 text-center text-xs text-grey">Data disimpan di perangkat ini.</p>
    </Halaman>
  )
}
