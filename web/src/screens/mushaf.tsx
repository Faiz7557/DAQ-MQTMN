import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams, useSearchParams } from 'react-router'
import { hurufById, kataMemuat, kodeHuruf, loadTerjemah, materi } from '../data/materi'
import { useApp } from '../store'
import { Arab, BintangNomor, Halaman, Ikon, Kartu, Saklar } from '../components'
import { useQuran } from './belajar'

const angkaArab = (n: number) => String(n).replace(/\d/g, (d) => '٠١٢٣٤٥٦٧٨٩'[Number(d)])

export function DaftarSurah() {
  const q = useQuran()
  const [cari, setCari] = useState('')
  const { terakhirSurah } = useApp()
  const nav = useNavigate()
  const daftar = useMemo(() => {
    if (!q) return []
    const k = cari.trim().toLowerCase().replace(/[^a-z0-9]/g, '')
    return q.suras.filter((s) => !k || String(s.n) === k || s.tname.toLowerCase().replace(/[^a-z0-9]/g, '').includes(k) || s.name.includes(cari.trim()))
  }, [q, cari])
  const terakhir = q?.suras[terakhirSurah - 1]
  return (
    <Halaman judul="Mushaf" sub="114 surah · Rasm Utsmani" kembali={false} lebar="lebar">
      <div className="mb-6 grid gap-4 md:grid-cols-[1.2fr_1fr] md:items-stretch">
        {terakhir ? (
          <button onClick={() => nav(`/mushaf/${terakhirSurah}`)}
            className="relative flex items-center gap-4 overflow-hidden rounded-[1.5rem] bg-gradient-to-br from-[#147a73] via-[#0f5e5e] to-[#0a4343] p-5 text-left text-white shadow-teal">
            <span className="pola-khatam absolute inset-0 [mask-image:linear-gradient(to_left,black,transparent)]" />
            <span className="relative grid size-12 shrink-0 place-items-center rounded-2xl bg-white/15 ring-1 ring-white/25"><Ikon n="book" className="size-6" /></span>
            <span className="relative min-w-0 flex-1"><span className="block text-sm text-white/75">Lanjutkan membaca</span><span className="block truncate text-lg font-bold">{terakhir.n}. {terakhir.tname}</span></span>
            <Arab className="relative text-3xl">{terakhir.name}</Arab>
          </button>
        ) : <div className="h-[5.5rem] animate-pulse rounded-[1.5rem] bg-sand" />}
        <label className="relative flex items-center">
          <span className="sr-only">Cari surah</span>
          <Ikon n="search" className="pointer-events-none absolute left-4 size-5 text-grey" />
          <input type="search" value={cari} onChange={(e) => setCari(e.target.value)} placeholder="Cari nama atau nomor surah"
            className="h-full min-h-12 w-full rounded-2xl border border-line bg-surface pr-4 pl-12 shadow-kartu outline-none placeholder:text-grey focus:border-tint" />
        </label>
      </div>
      {!q ? (
        <div className="grid gap-2.5 md:grid-cols-2 xl:grid-cols-3">{Array.from({ length: 9 }, (_, k) => <div key={k} className="h-[4.25rem] animate-pulse rounded-2xl bg-sand" />)}</div>
      ) : (
        <ul className="grid gap-2.5 md:grid-cols-2 xl:grid-cols-3">
          {daftar.map((s) => (
            <li key={s.n}>
              <Link to={`/mushaf/${s.n}`} className="tekan flex min-h-[4.25rem] items-center gap-3 rounded-2xl border border-line bg-surface px-3 py-2 shadow-kartu hover:border-tint">
                <BintangNomor n={s.n} aktif={s.n === terakhirSurah} />
                <span className="min-w-0 flex-1"><span className="block truncate font-semibold">{s.tname}</span><span className="block text-xs text-grey">{s.ayahs.length} ayat · {s.type === 'Meccan' ? 'Makkiyah' : 'Madaniyah'}</span></span>
                <Arab className="text-2xl text-tint">{s.name}</Arab>
              </Link>
            </li>
          ))}
          {daftar.length === 0 && <li className="col-span-full rounded-2xl border border-dashed border-border p-6 text-center text-grey">Surah tidak ditemukan.</li>}
        </ul>
      )}
      <Atribusi />
    </Halaman>
  )
}

export function BacaSurah() {
  const { n = '1' } = useParams()
  const [sp, setSp] = useSearchParams()
  const q = useQuran()
  const [terjemah, setTerjemah] = useState<string[][] | null>(null)
  const [tampilTerjemah, setTampilTerjemah] = useState(true)
  const { bacaSurah, catat, dikuasai } = useApp()
  const nomor = Math.min(114, Math.max(1, Number(n) || 1))
  const hurufId = sp.get('huruf')
  const h = hurufId ? hurufById(hurufId) : undefined
  const kode = useMemo(() => (h ? kodeHuruf(h.huruf) : null), [h])

  useEffect(() => { bacaSurah(nomor); catat('baca_surah', h?.id, String(nomor)) }, [nomor]) // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { if (tampilTerjemah && !terjemah) loadTerjemah().then(setTerjemah) }, [tampilTerjemah, terjemah])
  useEffect(() => {
    if (!q || !location.hash) return
    document.getElementById(location.hash.slice(1))?.scrollIntoView({ block: 'center' })
  }, [q])

  if (!q) return (
    <Halaman judul="Mushaf" lebar="baca">
      <div className="space-y-3">{Array.from({ length: 4 }, (_, k) => <div key={k} className="h-28 animate-pulse rounded-[1.5rem] bg-sand" />)}</div>
    </Halaman>
  )
  const s = q.suras[nomor - 1]
  const jumlah = kode ? s.ayahs.reduce((a, ay) => a + ay.split(' ').filter((k) => kataMemuat(k, kode)).length, 0) : 0
  // Daftar sorot: huruf yang sudah dipelajari lebih dulu, lalu sisanya.
  const pilihan = [...materi.huruf].sort((a, b) => Number(dikuasai.includes(b.id)) - Number(dikuasai.includes(a.id)))

  return (
    <Halaman judul={`${s.n}. ${s.tname}`} lebar="baca">
      <header className="mb-5 text-center">
        <div className="relative mx-auto grid max-w-md place-items-center overflow-hidden rounded-[1.75rem] bg-gradient-to-br from-[#147a73] via-[#0f5e5e] to-[#0a4343] px-6 py-7 text-white shadow-teal">
          <span className="pola-khatam absolute inset-0 opacity-80" />
          <Arab className="relative text-5xl leading-snug">{s.name}</Arab>
          <p className="relative mt-1 text-lg font-bold">{s.tname}</p>
          <p className="relative text-sm text-white/75">{s.ayahs.length} ayat · {s.type === 'Meccan' ? 'Makkiyah' : 'Madaniyah'}</p>
        </div>
      </header>

      <Kartu className="mb-5 !p-4">
        <p className="label-kecil mb-2.5">Sorot kata yang memuat huruf</p>
        <div dir="rtl" className="tanpa-scrollbar -mx-4 flex gap-2 overflow-x-auto px-4 pb-1">
          <button dir="ltr" onClick={() => setSp({})} className={`min-h-11 shrink-0 rounded-xl px-3 text-sm font-semibold ${!h ? 'bg-teal text-white' : 'bg-sand text-ink hover:bg-teal-light'}`}>Tanpa sorot</button>
          {pilihan.map((x) => (
            <button key={x.id} onClick={() => setSp({ huruf: x.id }, { replace: true })} aria-label={`Sorot huruf ${x.nama}`} aria-pressed={x.id === h?.id}
              className={`arab grid size-11 shrink-0 place-items-center rounded-xl border text-2xl ${x.id === h?.id ? 'border-teal bg-teal text-white' : dikuasai.includes(x.id) ? 'border-transparent bg-teal-light text-teal-dark' : 'border-line bg-surface hover:border-tint'}`}>
              <span lang="ar">{x.huruf}</span>
            </button>
          ))}
        </div>
        {h && <p className="mt-3 text-sm text-teal-dark" aria-live="polite"><strong>{jumlah} kata</strong> memuat huruf <Arab className="text-lg">{h.huruf}</Arab> ({h.nama}) di surah ini. Harakat diabaikan saat mencari.</p>}
        <div className="mt-3 flex flex-wrap items-center justify-between gap-x-4 gap-y-2 border-t border-line pt-3">
          <div className="min-w-48 flex-1"><Saklar cek={tampilTerjemah} onUbah={setTampilTerjemah} judul="Terjemahan" /></div>
          {h && <Link to={`/huruf/${h.id}`} className="tekan inline-flex min-h-11 items-center gap-1 rounded-full bg-teal-light px-4 text-sm font-semibold text-teal-dark">Pelajaran {h.nama.split(' (')[0]} <Ikon n="next" className="size-4" /></Link>}
        </div>
      </Kartu>

      {s.basmalah && <p className="mb-5 text-center"><Arab className="text-3xl sm:text-4xl">{q.basmalah}</Arab></p>}
      <ol className="divide-y divide-line overflow-hidden rounded-[1.5rem] border border-line bg-surface shadow-kartu">
        {s.ayahs.map((ayat, i) => (
          <li key={i} id={`a${i + 1}`} className="scroll-mt-24 px-4 py-5 target:bg-gold-light/50 sm:px-6">
            <p lang="ar" dir="rtl" className="arab text-[1.85rem] leading-[2.4] sm:text-[2.15rem]">
              {ayat.split(' ').map((kata, j) => (
                <span key={j}>
                  <span className={kode && kataMemuat(kata, kode) ? 'sorot' : undefined}>{kata}</span>{' '}
                </span>
              ))}
              <span className="text-tint" aria-label={`ayat ${i + 1}`}>﴿{angkaArab(i + 1)}﴾</span>
            </p>
            {tampilTerjemah && terjemah && <p className="mt-2 text-[0.95rem] leading-relaxed text-grey"><span className="mr-1 inline-grid min-w-6 place-items-center rounded-md bg-sand px-1 text-xs font-bold text-ink">{i + 1}</span>{terjemah[nomor - 1][i]}</p>}
          </li>
        ))}
      </ol>
      <div className="mt-6 grid grid-cols-2 gap-3">
        {nomor > 1 ? <Link to={`/mushaf/${nomor - 1}${h ? `?huruf=${h.id}` : ''}`} className="tekan flex min-h-14 items-center gap-2 rounded-2xl bg-teal-light px-4 font-semibold text-teal-dark"><Ikon n="back" /><span className="min-w-0 truncate">{q.suras[nomor - 2].tname}</span></Link> : <span />}
        {nomor < 114 && <Link to={`/mushaf/${nomor + 1}${h ? `?huruf=${h.id}` : ''}`} className="tekan flex min-h-14 items-center justify-end gap-2 rounded-2xl bg-teal px-4 font-semibold text-white shadow-teal"><span className="min-w-0 truncate">{q.suras[nomor].tname}</span><Ikon n="next" /></Link>}
      </div>
      <Atribusi />
    </Halaman>
  )
}

const Atribusi = () => (
  <p className="mx-auto mt-8 max-w-2xl text-center text-xs leading-relaxed text-grey">
    Teks Al-Qur'an: Tanzil Project, Uthmani 1.1 (CC BY 3.0), ditampilkan tanpa perubahan ·{' '}
    <a className="underline" href="https://tanzil.net" target="_blank" rel="noreferrer">tanzil.net</a>. Terjemahan: Kementerian Agama RI melalui Tanzil (penggunaan nonkomersial).
  </p>
)
