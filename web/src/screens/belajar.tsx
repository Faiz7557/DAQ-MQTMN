import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router'
import {
  anggotaArea, anggotaTitik, areaById, areaOf, contohKata, harakatHuruf, hurufById, kuisMirip, loadQuran, materi,
  sifatHuruf, titikById, urutan, type Contoh, type Huruf, type Quran, type Soal,
} from '../data/materi'
import { hariPekanIni, useApp } from '../store'
import {
  Arab, BadgeValidasi, Catatan, Cincin, Halaman, Ikon, Kartu, KlipGuru, Logo, Penampang, Pil, Segmen, Subjudul, Tebal, Tombol,
  UbinHuruf, VideoKosong, toast, type KlipRef, type Sorot,
} from '../components'
import { Latihan } from './latihan'

export function useQuran() {
  const [q, setQ] = useState<Quran | null>(null)
  useEffect(() => { loadQuran().then(setQ).catch(() => toast('Teks Al-Qur\'an gagal dimuat.')) }, [])
  return q
}

const sorotTitik = (h: Huruf): Sorot => {
  const p = titikById(h.titik).posisi
  return [p[0], p[1], p[2], p[2]]
}

/** Klip yang dipakai: sumber pilihan pengguna, lalu sumber lain bila kosong. */
export function klipHuruf(h: Huruf, sumber: 'andalasy' | 'resmi') {
  const urut = sumber === 'resmi' ? [['resmi', h.videoAlt], ['andalasy', h.video]] : [['andalasy', h.video], ['resmi', h.videoAlt]]
  const [sid, id] = urut.find(([, v]) => v) ?? []
  if (!id) return null
  const src = materi.sumberVideo.find((s) => s.id === sid)!
  return { id, kanal: src.kanal, guru: src.guru }
}

const pasanganDari = (h: Huruf) => materi.mirip
  .map((m, i) => ({ m, i }))
  .filter(({ m }) => m.a === h.id || m.b === h.id)

const namaPendek = (h: Huruf) => h.nama.split(' (')[0]

/** Isian teal bergradasi; warnanya tetap di mode terang dan gelap. */
const PANEL_TEAL = 'relative overflow-hidden bg-gradient-to-br from-[#147a73] via-[#0f5e5e] to-[#0a4343] text-white'

// ================= Beranda =================
export function Beranda() {
  const { dikuasai, hariAktif, pengaturan } = useApp()
  const nav = useNavigate()
  const berikut = materi.huruf.find((h) => !dikuasai.includes(h.id)) ?? materi.huruf[0]
  const total = materi.huruf.length
  const persen = Math.round((dikuasai.length / total) * 100)
  const hari = hariPekanIni(hariAktif)
  return (
    <Halaman kembali={false} lebar="lebar" sub="Assalamu'alaikum" judul="Belajar dari tempat keluarnya huruf"
      kanan={<Logo className="size-12 rounded-2xl text-3xl lg:hidden" />}>

      <div className="mb-4 grid gap-4 xl:grid-cols-[1.45fr_1fr]">
        <section className={`${PANEL_TEAL} rounded-[1.75rem] p-6 shadow-teal sm:p-8`}>
          <span className="pola-khatam absolute inset-0 [mask-image:radial-gradient(circle_at_85%_20%,black,transparent_70%)]" />
          <span lang="ar" aria-hidden className="arab pointer-events-none absolute -bottom-16 -left-4 text-[14rem] leading-none text-white/[0.07] select-none sm:text-[17rem]">{berikut.huruf}</span>
          <div className="relative">
            <p className="text-sm font-semibold text-white/75">Pelajaran berikutnya · {urutan(berikut)} dari {total}</p>
            <div className="mt-4 flex items-center gap-4 sm:gap-5">
              <span lang="ar" className="arab grid size-20 shrink-0 place-items-center rounded-3xl bg-white/15 text-5xl ring-1 ring-white/25 backdrop-blur sm:size-24 sm:text-6xl">{berikut.huruf}</span>
              <div className="min-w-0">
                <p className="text-2xl font-extrabold tracking-tight sm:text-3xl">Huruf {berikut.nama}</p>
                <p className="mt-0.5 text-sm text-white/80">{[...new Set([areaOf(berikut).nama, titikById(berikut.titik).nama])].join(' · ')}</p>
              </div>
            </div>
            <button onClick={() => nav(`/huruf/${berikut.id}`)}
              className="mt-6 inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-2xl bg-white px-6 font-bold text-[#0f5e5e] shadow-angkat hover:bg-[#eef7f5] sm:w-auto">
              Mulai pelajaran <Ikon n="next" className="size-5" />
            </button>
          </div>
        </section>

        <div className="grid grid-cols-2 gap-4 xl:grid-cols-1">
          <Kartu className="flex flex-col justify-between gap-3 !p-4 sm:!p-5 xl:flex-row xl:items-center xl:justify-start xl:gap-5">
            <Cincin nilai={dikuasai.length / total} ukuran={60} tebal={6}><span className="text-xs font-bold">{persen}%</span></Cincin>
            <div>
              <p className="text-[1.75rem] leading-none font-extrabold tracking-tight">{dikuasai.length}<span className="text-base font-semibold text-grey">/{total}</span></p>
              <p className="mt-1 text-sm text-grey">huruf dikuasai</p>
            </div>
          </Kartu>
          {pengaturan.tampilkanHari ? (
            <Kartu className="flex flex-col justify-between gap-3 !p-4 sm:!p-5">
              <div>
                <p className="text-[1.75rem] leading-none font-extrabold tracking-tight">{hari}<span className="text-base font-semibold text-grey">/7</span></p>
                <p className="mt-1 text-sm text-grey">hari belajar pekan ini</p>
              </div>
              <div className="flex gap-1" aria-hidden>
                {Array.from({ length: 7 }, (_, k) => <span key={k} className={`h-1.5 flex-1 rounded-full ${k < hari ? 'bg-tint' : 'bg-sand'}`} />)}
              </div>
              <p className="text-xs text-grey">Sedikit tapi rutin lebih baik.</p>
            </Kartu>
          ) : (
            <Link to="/mirip" className="tekan flex flex-col justify-between rounded-[1.5rem] border border-line bg-surface p-4 shadow-kartu hover:border-tint sm:p-5">
              <span className="grid size-10 place-items-center rounded-xl bg-teal-light text-teal-dark"><Ikon n="pair" /></span>
              <span><span className="block text-sm text-grey">Latihan</span><span className="block font-bold">Huruf mirip</span></span>
            </Link>
          )}
        </div>
      </div>

      <div className="mb-10 grid grid-cols-2 gap-3 xl:grid-cols-4">
        {[
          { to: '/peta', ikon: 'map', j: 'Peta makhraj', s: '5 area · 17 titik' },
          { to: '/mirip', ikon: 'pair', j: 'Huruf mirip', s: '6 pasangan' },
          { to: '/mushaf', ikon: 'book', j: 'Mushaf', s: 'Sorot huruf di ayat' },
          { to: '/saya/studi', ikon: 'list', j: 'Uji coba', s: 'Tes & kuesioner' },
        ].map((m) => (
          <Link key={m.to} to={m.to} className="tekan group flex min-h-20 items-center gap-3 rounded-[1.25rem] border border-line bg-surface p-3.5 shadow-kartu hover:border-tint sm:p-4">
            <span className="grid size-11 shrink-0 place-items-center rounded-2xl bg-teal-light text-teal-dark"><Ikon n={m.ikon} /></span>
            <span className="min-w-0 flex-1"><span className="block text-[0.95rem] leading-tight font-bold">{m.j}</span><span className="mt-0.5 block text-xs text-grey">{m.s}</span></span>
            <Ikon n="next" className="hidden size-4 text-grey transition-transform group-hover:translate-x-0.5 sm:block" />
          </Link>
        ))}
      </div>

      <Subjudul kanan={<span className="text-sm font-semibold text-grey">{dikuasai.length} dikuasai</span>}>Semua huruf</Subjudul>
      <div dir="rtl" className="grid grid-cols-5 gap-2.5 sm:grid-cols-7 sm:gap-3 md:grid-cols-8 xl:grid-cols-10">
        {materi.huruf.map((h) => (
          <UbinHuruf key={h.id} huruf={h.huruf} aktif={dikuasai.includes(h.id)} label={`Huruf ${h.nama}`} onClick={() => nav(`/huruf/${h.id}`)} />
        ))}
      </div>
      <p className="mx-auto mt-10 max-w-md text-center text-xs leading-relaxed text-grey">
        Makhraj menyiapkan Anda sebelum dan di antara pertemuan dengan guru. Aplikasi ini tidak menggantikan talaqqi.
      </p>
    </Halaman>
  )
}

// ================= Pelajaran huruf: lihat, dengar, tiru, bandingkan, terapkan =================
const LANGKAH = ['Lihat', 'Dengar', 'Tiru', 'Bandingkan', 'Terapkan'] as const

export function Pelajaran() {
  const { id = 'ba', langkah } = useParams()
  const h = hurufById(id)
  const nav = useNavigate()
  const { catat } = useApp()
  const step = Math.max(0, Math.min(4, Number(langkah ?? 0)))
  useEffect(() => { if (h) catat('langkah', h.id, LANGKAH[step]) }, [h, step, catat])
  if (!h) return <Halaman judul="Huruf tidak ditemukan"><Tombol onClick={() => nav('/')}>Ke beranda</Tombol></Halaman>

  const ke = (i: number) => nav(`/huruf/${h.id}/${i}`, { replace: true })
  const i = urutan(h)
  const sebelum = materi.huruf[i - 2], sesudah = materi.huruf[i]

  return (
    <Halaman judul={`Pelajaran ${i} dari ${materi.huruf.length}`} lebar="lebar">
      <div className="mb-5 flex items-center gap-4 sm:gap-6">
        <span lang="ar" className={`${PANEL_TEAL} arab grid size-20 shrink-0 place-items-center rounded-[1.6rem] text-[3.25rem] shadow-teal sm:size-28 sm:text-7xl`}>
          <span className="pola-khatam absolute inset-0 opacity-70" />
          <span className="relative">{h.huruf}</span>
        </span>
        <div className="min-w-0">
          <p className="label-kecil">{areaOf(h).nama}</p>
          <h2 className="judul-besar mt-1 text-[1.75rem] sm:text-4xl">Huruf {h.nama}</h2>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            <span className="text-sm text-grey">{areaOf(h).arti}</span>
            <BadgeValidasi ok={materi.tervalidasi} />
          </div>
        </div>
      </div>

      <nav aria-label="Langkah belajar" className="sticky top-[calc(env(safe-area-inset-top)+3.5rem)] z-10 mb-5">
        <ol className="grid grid-cols-5 gap-1 rounded-2xl border border-line bg-sand/95 p-1 shadow-kartu backdrop-blur">
          {LANGKAH.map((l, k) => (
            <li key={l}>
              <button onClick={() => ke(k)} aria-current={k === step ? 'step' : undefined}
                className={`flex min-h-12 w-full flex-col items-center justify-center gap-0.5 rounded-xl text-[0.66rem] font-semibold tracking-[-0.01em] min-[400px]:text-[0.72rem] sm:flex-row sm:gap-1.5 sm:text-sm ${k === step ? 'bg-surface text-ink shadow-kartu' : k < step ? 'text-tint' : 'text-grey hover:text-ink'}`}>
                {k < step
                  ? <Ikon n="check" className="size-3.5 sm:size-4" />
                  : <span className={`grid size-4 place-items-center rounded-full text-[0.6rem] sm:size-5 sm:text-[0.7rem] ${k === step ? 'bg-teal text-white' : 'bg-border/70'}`}>{k + 1}</span>}
                <span className="max-w-full truncate">{l}</span>
              </button>
            </li>
          ))}
        </ol>
      </nav>

      <div key={step} className="animate-masuk">
        {step === 0 && <LangkahLihat h={h} />}
        {step === 1 && <LangkahDengar h={h} />}
        {step === 2 && <Latihan h={h} mode="tiru" />}
        {step === 3 && <Latihan h={h} mode="bandingkan" />}
        {step === 4 && <LangkahTerapkan h={h} />}
      </div>

      <div className="kaca-latar sticky bottom-0 z-10 -mx-4 mt-8 -mb-12 px-4 pt-3 pb-[max(1rem,env(safe-area-inset-bottom))] sm:-mx-6 sm:px-6 lg:-mx-10 lg:px-10">
        <div className="ml-auto flex max-w-xl gap-3">
          {step > 0 ? <Tombol varian="garis" ikon="back" onClick={() => ke(step - 1)} className="flex-1">{LANGKAH[step - 1]}</Tombol>
            : sebelum && <Tombol varian="garis" ikon="back" onClick={() => nav(`/huruf/${sebelum.id}`, { replace: true })} className="flex-1">{namaPendek(sebelum)}</Tombol>}
          {step < 4 ? <Tombol onClick={() => ke(step + 1)} className="flex-[1.4]">Lanjut: {LANGKAH[step + 1]}</Tombol>
            : sesudah && <Tombol onClick={() => nav(`/huruf/${sesudah.id}`, { replace: true })} className="flex-[1.4]">Berikutnya: {namaPendek(sesudah)}</Tombol>}
        </div>
      </div>
    </Halaman>
  )
}

function LangkahLihat({ h }: { h: Huruf }) {
  const p = h.pelajaran
  const [k, setK] = useState(0)
  const langkah = p?.langkah?.[k]
  const base = sorotTitik(h)
  const t = titikById(h.titik)
  const sesama = anggotaTitik(h.titik).filter((x) => x.id !== h.id)
  const sifat = sifatHuruf(h)
  const pasangan = pasanganDari(h)
  return (
    <div className="grid gap-4 xl:grid-cols-[1.1fr_1fr] xl:items-start xl:gap-6">
      <Kartu className="!p-4 sm:!p-5 xl:sticky xl:top-[calc(env(safe-area-inset-top)+8.5rem)]">
        <Subjudul>Visualisasi makhraj</Subjudul>
        <Penampang sorot={langkah ? [base[0], base[1], langkah.r, langkah.r] : base} panah={langkah?.panah}
          label={`Penampang samping mulut, menyorot makhraj huruf ${h.nama}: ${t.nama}`} />
        {p?.langkah && (
          <>
            <div className="mt-3">
              <Segmen label="Tahap gerakan" nilai={k} onUbah={setK} pilihan={p.langkah.map((l, i) => ({ v: i, l: l.label }))} />
            </div>
            <div key={k} className="animate-muncul mt-3 rounded-2xl bg-teal-light px-4 py-3">
              <p className="font-bold text-teal-dark">{langkah!.judul}</p>
              <p className="text-sm leading-relaxed text-teal-dark">{langkah!.isi}</p>
            </div>
          </>
        )}
        <p className="mt-3 text-center text-xs text-grey">Ilustrasi penampang samping; letak titik perlu dicocokkan dengan guru.</p>
      </Kartu>

      <div className="space-y-4">
        <Kartu>
          <Subjudul>Letak makhraj</Subjudul>
          <p className="mb-2 inline-flex items-center gap-2 rounded-full bg-teal-light px-3 py-1 text-xs font-bold text-teal-dark">Titik {t.no} dari 17 · {t.nama}</p>
          <p className="text-[1.0625rem] leading-relaxed">{p ? <Tebal s={p.makhraj} /> : t.deskripsi}</p>
          {h.titikMad && <p className="mt-3 text-sm leading-relaxed text-grey">Ketika menjadi huruf mad (mati dan didahului harakat yang sesuai), {h.nama.toLowerCase()} keluar dari Al-Jauf.</p>}
          {h.catatan && <p className="mt-3 text-sm leading-relaxed text-grey">{h.catatan}</p>}
          {sesama.length > 0 && (
            <div className="mt-4">
              <p className="label-kecil mb-2">Satu titik dengan</p>
              <div className="flex flex-wrap gap-2">
                {sesama.map((x) => (
                  <Link key={x.id} to={`/huruf/${x.id}`} className="tekan inline-flex min-h-11 items-center gap-1.5 rounded-xl bg-sand px-3 text-sm font-semibold hover:bg-teal-light">
                    <Arab className="text-xl leading-none">{x.huruf}</Arab> {namaPendek(x)}
                  </Link>
                ))}
              </div>
            </div>
          )}
          {(p?.kesalahanUmum || h.kesalahan) && (
            <div className="mt-4"><Catatan><strong>Kesalahan umum: </strong>{p?.kesalahanUmum ?? h.kesalahan!.teks}</Catatan></div>
          )}
          {pasangan.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {pasangan.map(({ m, i }) => {
                const lain = hurufById(m.a === h.id ? m.b : m.a)!
                return <Link key={i} to={`/mirip/${i}`} className="tekan inline-flex min-h-11 items-center gap-2 rounded-full border border-line bg-surface px-4 text-sm font-semibold hover:border-tint">
                  <Ikon n="pair" className="size-4 text-tint" /> Sering tertukar dengan <Arab className="text-lg leading-none">{lain.huruf}</Arab>
                </Link>
              })}
            </div>
          )}
        </Kartu>

        <Kartu>
          <Subjudul>Sifat huruf</Subjudul>
          <ul className="flex flex-wrap gap-2">
            {sifat.map((s) => (
              <li key={s.id} className={`rounded-xl px-3 py-1.5 text-sm ${s.tonjol ? 'bg-gold-light text-gold-ink' : 'bg-sand text-ink'}`}>
                <strong>{s.nama}</strong> · {s.arti}
              </li>
            ))}
          </ul>
          <p className="mt-3 text-xs leading-relaxed text-grey">Disusun dari pembagian sifat pada Al-Muqaddimah al-Jazariyyah. Idzlaq dan Ishmat adalah sifat leksikal yang tidak memengaruhi pelafalan.</p>
        </Kartu>
      </div>
    </div>
  )
}

function LangkahDengar({ h }: { h: Huruf }) {
  const { pengaturan, catat } = useApp()
  const klip = klipHuruf(h, pengaturan.sumberVideo)
  const ref = useRef<KlipRef>(null)
  const dengar = (label: string) => {
    ref.current?.putar(null)
    catat('dengar_harakat', h.id, label)
    toast('Penanda detik untuk harakat ini belum dicatat, jadi video diputar dari awal.')
  }
  return (
    <Kartu className="!p-4 sm:!p-6">
      <div className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <div>
          <Subjudul>Dengarkan dari guru</Subjudul>
          {klip ? <KlipGuru ref={ref} videoId={klip.id} judul={`Pelafalan huruf ${h.nama}`} /> : <VideoKosong huruf={h.huruf} />}
          {klip && <p className="text-sm text-grey">{klip.guru} · {klip.kanal}</p>}
        </div>
        <div>
          <p className="mb-3 font-bold tracking-tight">Dengar per harakat</p>
          <div dir="rtl" className="grid grid-cols-4 gap-2 xl:grid-cols-2">
            {harakatHuruf(h).map((x) => (
              // Nama aksesibel diambil dari isi tombol (WCAG 2.5.3): huruf berharakat + label Latin.
              <button key={x.teks} disabled={!klip} onClick={() => dengar(x.label)}
                className="arab flex min-h-16 flex-col items-center justify-center rounded-2xl border border-line bg-cream text-3xl hover:border-tint disabled:opacity-40 xl:min-h-24 xl:text-4xl">
                <span lang="ar" className="leading-tight">{x.teks}</span>
                <span dir="ltr" className="sr-only font-sans text-xs text-grey xl:not-sr-only xl:block">{x.label}</span>
              </button>
            ))}
          </div>
          <p className="mt-4 text-xs leading-relaxed text-grey">Video diputar lewat pemutar resmi YouTube dan tidak diunduh. Perhatikan gerak mulut guru, lalu lanjut ke langkah Tiru.</p>
        </div>
      </div>
    </Kartu>
  )
}

function LangkahTerapkan({ h }: { h: Huruf }) {
  const q = useQuran()
  const contoh: Contoh[] = useMemo(() => (q ? contohKata(q, h, 6) : []), [q, h])
  const { dikuasai, tandai } = useApp()
  const sudah = dikuasai.includes(h.id)
  return (
    <div className="grid gap-4 xl:grid-cols-[1.5fr_1fr] xl:items-start xl:gap-6">
      <Kartu>
        <Subjudul>Temukan di dalam ayat</Subjudul>
        <p className="mb-4 text-sm text-grey">Kata dari Al-Fatihah dan Juz 'Amma yang memuat huruf <Arab className="text-lg text-ink">{h.huruf}</Arab>. Baca pelan dan perhatikan makhrajnya.</p>
        {!q ? <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3">{Array.from({ length: 6 }, (_, k) => <div key={k} className="h-24 animate-pulse rounded-2xl bg-sand" />)}</div> : (
          <ul className="grid grid-cols-2 gap-2.5 sm:grid-cols-3">
            {contoh.map((c) => (
              <li key={c.kata + c.surah}>
                <Link to={`/mushaf/${c.surah}?huruf=${h.id}#a${c.ayat}`} className="tekan block rounded-2xl border border-line bg-cream p-3 text-center hover:border-tint">
                  <Arab className="text-3xl">{c.kata}</Arab>
                  <span className="block text-xs text-grey">QS {c.tname}: {c.ayat}</span>
                </Link>
              </li>
            ))}
          </ul>
        )}
        <Link to={`/mushaf/1?huruf=${h.id}`} className="mt-4 inline-flex min-h-11 items-center gap-1.5 font-semibold text-tint hover:underline">
          <Ikon n="book" className="size-4" /> Sorot huruf {h.huruf} di Al-Fatihah
        </Link>
      </Kartu>
      <div className="space-y-4">
        <Tombol varian={sudah ? 'garis' : 'utama'} ikon="check" onClick={() => tandai(h.id, !sudah)} className="w-full">
          {sudah ? 'Sudah dikuasai · ketuk untuk membatalkan' : 'Tandai sudah dikuasai'}
        </Tombol>
        <Catatan nada="teal">Tandai dikuasai jika Anda sudah bisa menunjukkan letak makhrajnya dan bacaan Anda mirip contoh guru. Bila ragu, minta guru mendengarkan.</Catatan>
      </div>
    </div>
  )
}

// ================= Peta makhraj =================
export function Peta() {
  const [area, setArea] = useState('syafatain')
  const [titik, setTitik] = useState<string | null>(null)
  const { dikuasai } = useApp()
  const nav = useNavigate()
  const a = areaById(area)
  const titikArea = materi.titik.filter((t) => t.area === area)
  const anggota = titik ? anggotaTitik(titik) : anggotaArea(area)

  const tap = (x: number, y: number) => {
    let best: string | null = null, luas = Infinity
    for (const ar of materi.area) {
      const [cx, cy, rx, ry] = ar.elips
      const dx = (x - cx) / (rx + 6), dy = (y - cy) / (ry + 6)
      if (dx * dx + dy * dy <= 1 && rx * ry < luas) { best = ar.id; luas = rx * ry }
    }
    if (best) { setArea(best); setTitik(null) }
  }
  const tTerpilih = titik ? titikById(titik) : null
  const sorot: Sorot = tTerpilih ? [tTerpilih.posisi[0], tTerpilih.posisi[1], tTerpilih.posisi[2], tTerpilih.posisi[2]] : (a.elips as Sorot)

  return (
    <Halaman judul="Peta makhraj" sub="5 area · 17 titik" kembali={false} lebar="lebar">
      <div className="grid gap-5 xl:grid-cols-[1.15fr_1fr] xl:items-start xl:gap-6">
        <Kartu className="!p-3 sm:!p-4 xl:sticky xl:top-8">
          <Penampang sorot={sorot} onTap={tap}
            titik={titikArea.map((t) => ({ x: t.posisi[0], y: t.posisi[1], aktif: t.id === titik, label: `Titik ${t.no}: ${t.nama}`, onClick: () => setTitik(t.id === titik ? null : t.id) }))}
            label={`Penampang samping kepala, menyorot ${a.nama} (${a.arti})`} />
          <p className="mt-3 text-center text-xs text-grey">Ketuk area untuk melihat hurufnya; ketuk titik kecil untuk melihat satu makhraj.</p>
        </Kartu>

        <div className="min-w-0">
          <div className="tanpa-scrollbar -mx-4 mb-4 flex gap-2 overflow-x-auto px-4 pb-1 sm:mx-0 sm:flex-wrap sm:px-0">
            {materi.area.map((x) => <span key={x.id} className="shrink-0"><Pil aktif={x.id === area} onClick={() => { setArea(x.id); setTitik(null) }}>{x.nama}</Pil></span>)}
          </div>
          <Kartu>
            <div key={area + titik} className="animate-muncul">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <h2 className="text-xl font-extrabold tracking-tight">{a.nama}</h2>
                  <p className="text-sm text-grey">{a.arti}</p>
                </div>
                <Arab className="text-3xl leading-tight text-tint">{a.arab}</Arab>
              </div>
              <p className="mt-3 leading-relaxed">{tTerpilih ? <><strong>Titik {tTerpilih.no}, {tTerpilih.nama}:</strong> {tTerpilih.deskripsi}</> : a.deskripsi}</p>
            </div>
            {titikArea.length > 1 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {titikArea.map((t) => (
                  <button key={t.id} onClick={() => setTitik(t.id === titik ? null : t.id)} aria-pressed={t.id === titik}
                    className={`min-h-10 rounded-xl px-3 text-xs font-semibold ${t.id === titik ? 'bg-teal text-white' : 'bg-sand text-ink hover:bg-teal-light'}`}>
                    {t.no}. {t.nama}
                  </button>
                ))}
              </div>
            )}
            <p className="label-kecil mt-6 mb-3">
              {anggota.length ? `${anggota.length} huruf · ketuk untuk belajar` : 'Ghunnah dibahas pada materi tajwid lanjutan.'}
            </p>
            <div dir="rtl" className="grid grid-cols-5 gap-2.5 sm:grid-cols-6">
              {anggota.map((h) => <UbinHuruf key={h.id} huruf={h.huruf} aktif={dikuasai.includes(h.id)} label={`Belajar huruf ${h.nama}`} onClick={() => nav(`/huruf/${h.id}`)} />)}
            </div>
          </Kartu>
        </div>
      </div>
    </Halaman>
  )
}

// ================= Huruf mirip =================
export function MiripDaftar() {
  const nav = useNavigate()
  return (
    <Halaman lebar="baca">
      <h2 className="judul-besar mb-2 text-3xl sm:text-4xl">Huruf mirip</h2>
      <p className="mb-6 max-w-xl leading-relaxed text-grey">Pasangan huruf yang sering tertukar oleh pemula. Bandingkan letak dan sifatnya, lalu uji diri dengan kuis.</p>
      <ul className="grid gap-3 md:grid-cols-2">
        {materi.mirip.map((m, i) => {
          const a = hurufById(m.a)!, b = hurufById(m.b)!
          return (
            <li key={i}>
              <button onClick={() => nav(`/mirip/${i}`)} className="group flex w-full items-center gap-4 rounded-[1.5rem] border border-line bg-surface p-4 text-left shadow-kartu hover:border-tint">
                <span className="flex shrink-0" dir="rtl">
                  <span className="arab z-10 grid size-14 place-items-center rounded-2xl bg-teal text-3xl text-white ring-4 ring-surface" lang="ar">{a.huruf}</span>
                  <span className="arab -mr-3 grid size-14 place-items-center rounded-2xl bg-gold-light text-3xl text-gold-ink ring-4 ring-surface" lang="ar">{b.huruf}</span>
                </span>
                <span className="min-w-0 flex-1"><span className="block font-bold">{namaPendek(a)} dan {namaPendek(b)}</span><span className="mt-0.5 block text-sm leading-snug text-grey">{m.judul}</span></span>
                <Ikon n="next" className="size-5 shrink-0 text-grey transition-transform group-hover:translate-x-0.5" />
              </button>
            </li>
          )
        })}
      </ul>
    </Halaman>
  )
}

export function MiripDetail() {
  const { i = '0' } = useParams()
  const m = materi.mirip[Number(i)]
  const q = useQuran()
  const { catat } = useApp()
  const soal = useMemo(() => (m ? kuisMirip(m, q ?? undefined) : []), [m, q])
  if (!m) return <Halaman judul="Tidak ditemukan">Pasangan tidak ada.</Halaman>
  const a = hurufById(m.a)!, b = hurufById(m.b)!
  const sa = sifatHuruf(a), sb = sifatHuruf(b)
  const semuaSifat = [...new Map([...sa, ...sb].map((s) => [s.id, s])).values()]
  return (
    <Halaman judul={m.judul} lebar="baca">
      <p className="mb-5 text-[1.0625rem] leading-relaxed">{m.ringkas}</p>
      <div className="mb-4 grid grid-cols-2 gap-3 sm:gap-4">
        {[a, b].map((h, k) => (
          <Kartu key={h.id} className="!p-3 sm:!p-4">
            <div className="mb-2 flex items-center justify-between gap-2">
              <span lang="ar" className={`arab grid size-12 place-items-center rounded-2xl text-3xl sm:size-14 sm:text-4xl ${k === 0 ? 'bg-teal text-white' : 'bg-gold-light text-gold-ink'}`}>{h.huruf}</span>
              <span className="min-w-0 truncate text-right text-sm font-bold">{namaPendek(h)}</span>
            </div>
            <Penampang sorot={sorotTitik(h)} zoom label={`Makhraj ${h.nama}: ${titikById(h.titik).nama}`} />
            <p className="mt-3 text-xs leading-snug text-grey sm:text-sm"><strong className="text-ink">{titikById(h.titik).nama}.</strong> {titikById(h.titik).deskripsi}</p>
            <Link to={`/huruf/${h.id}`} className="mt-1 inline-flex min-h-11 items-center gap-1 text-sm font-semibold text-tint hover:underline">Pelajari {namaPendek(h)} <Ikon n="next" className="size-4" /></Link>
          </Kartu>
        ))}
      </div>
      <Kartu className="mb-4">
        <Subjudul>Perbandingan sifat</Subjudul>
        <div className="-mx-2 overflow-x-auto">
          <table className="w-full text-sm">
            <thead><tr className="text-left text-grey"><th className="px-2 py-1 font-semibold">Sifat</th><th className="w-14 text-center"><Arab className="text-2xl text-ink">{a.huruf}</Arab></th><th className="w-14 text-center"><Arab className="text-2xl text-ink">{b.huruf}</Arab></th></tr></thead>
            <tbody>
              {semuaSifat.map((s) => {
                const ya = sa.some((x) => x.id === s.id), yb = sb.some((x) => x.id === s.id)
                return (
                  <tr key={s.id} className={`border-t border-line ${ya !== yb ? 'bg-gold-light font-semibold text-gold-ink' : ''}`}>
                    <td className="px-2 py-2.5">{s.nama} <span className="font-normal opacity-75">· {s.arti}</span></td>
                    <td className="text-center">{ya ? <Ikon n="check" className="mx-auto size-4" /> : <span className="opacity-40">–</span>}<span className="sr-only">{ya ? 'ya' : 'tidak'}</span></td>
                    <td className="text-center">{yb ? <Ikon n="check" className="mx-auto size-4" /> : <span className="opacity-40">–</span>}<span className="sr-only">{yb ? 'ya' : 'tidak'}</span></td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-xs text-grey">Baris berwarna adalah pembeda kedua huruf.</p>
      </Kartu>
      <Kuis soal={soal} onSelesai={(skor) => catat('kuis_mirip', `${a.id}-${b.id}`, `${skor}/${soal.length}`)} />
    </Halaman>
  )
}

export function Kuis({ soal, onSelesai }: { soal: Soal[]; onSelesai?: (skor: number) => void }) {
  const [jawab, setJawab] = useState<Record<string, string>>({})
  const selesai = soal.length > 0 && Object.keys(jawab).length === soal.length
  const skor = soal.filter((s) => jawab[s.id] === s.jawab).length
  useEffect(() => { if (selesai) onSelesai?.(skor) }, [selesai]) // eslint-disable-line react-hooks/exhaustive-deps
  if (!soal.length) return null
  return (
    <Kartu>
      <Subjudul kanan={<span className="text-sm font-semibold text-grey">{Object.keys(jawab).length}/{soal.length}</span>}>Kuis pemahaman</Subjudul>
      <ol className="space-y-6">
        {soal.map((s, n) => {
          const dipilih = jawab[s.id]
          return (
            <li key={s.id}>
              <p className="mb-2.5 font-semibold leading-snug"><span className="text-grey">{n + 1}.</span> {s.tanya}</p>
              {s.arab && <p className="mb-2 text-center"><Arab className="text-5xl">{s.arab}</Arab></p>}
              <div className="grid grid-cols-2 gap-2">
                {s.opsi.map((o) => {
                  const benar = o.id === s.jawab
                  const gaya = !dipilih ? 'border-line bg-surface hover:border-tint'
                    : benar ? 'border-teal bg-teal-light text-teal-dark' : o.id === dipilih ? 'border-danger bg-danger-light text-danger' : 'border-line bg-surface opacity-50'
                  return (
                    <button key={o.id} disabled={!!dipilih} onClick={() => setJawab({ ...jawab, [s.id]: o.id })}
                      className={`relative min-h-14 rounded-2xl border-2 px-3 font-semibold ${gaya} ${o.arab ? 'arab text-3xl' : 'text-sm'}`}>
                      {o.label}{dipilih && benar && <span className="sr-only"> (jawaban benar)</span>}
                      {dipilih && benar && <Ikon n="check" className="absolute top-2 right-2 size-4" />}
                    </button>
                  )
                })}
              </div>
            </li>
          )
        })}
      </ol>
      {selesai && <div className="animate-muncul mt-6"><Catatan nada="teal"><strong>Skor {skor} dari {soal.length}.</strong> {skor === soal.length ? 'Masya Allah, semua benar.' : 'Ulangi bagian yang keliru lewat pelajaran hurufnya.'}</Catatan></div>}
    </Kartu>
  )
}
