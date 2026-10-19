import { useEffect, useImperativeHandle, useRef, useState, useSyncExternalStore, type ReactNode, type Ref } from 'react'
import { flushSync } from 'react-dom'
import { Link, NavLink, useNavigate } from 'react-router'
import { materi, pecahTebal } from './data/materi'
import { useApp } from './store'

// ---------- Ikon (inline, tanpa pustaka) ----------
const P: Record<string, string> = {
  back: 'M15 18l-6-6 6-6',
  next: 'M9 18l6-6-6-6',
  home: 'M3 11l9-8 9 8v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z',
  map: 'M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12zM12 11a2 2 0 1 0 0-4 2 2 0 0 0 0 4z',
  book: 'M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM4 21V5M8 7h7',
  user: 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0',
  mic: 'M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3zM5 11a7 7 0 0 0 14 0M12 18v3',
  stop: 'M7 7h10v10H7z',
  play: 'M8 5v14l11-7z',
  check: 'M5 12l5 5 9-10',
  trash: 'M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3',
  camera: 'M3 8a2 2 0 0 1 2-2h2l2-2h6l2 2h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM12 17a4 4 0 1 0 0-8 4 4 0 0 0 0 8z',
  pair: 'M8 7h11M16 4l3 3-3 3M16 17H5M8 14l-3 3 3 3',
  info: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 16v-5M12 8h.01',
  external: 'M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5',
  list: 'M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01',
  search: 'M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM20 20l-4-4',
  download: 'M12 4v11M7 10l5 5 5-5M5 20h14',
  sun: 'M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4',
  moon: 'M20.5 14.5A8.5 8.5 0 1 1 9.5 3.5a7 7 0 0 0 11 11z',
  auto: 'M12 21a9 9 0 1 1 0-18 9 9 0 0 1 0 18zM12 3v18M12 8h4M12 12h5M12 16h4',
}
export function Ikon({ n, className = 'size-5' }: { n: keyof typeof P | string; className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d={P[n]} />
    </svg>
  )
}

// ---------- Tema terang/gelap ----------
export type Tema = 'terang' | 'gelap'
const mqGelap = () => matchMedia('(prefers-color-scheme: dark)')
export const temaSistem = (): Tema => (mqGelap().matches ? 'gelap' : 'terang')

/** Tema yang berlaku sekarang: pilihan pengguna, atau ikut sistem bila "Otomatis". */
export function useTemaAktif(): Tema {
  const pilih = useApp((s) => s.pengaturan.tema ?? 'sistem')
  const sistemGelap = useSyncExternalStore(
    (cb) => { const m = mqGelap(); m.addEventListener('change', cb); return () => m.removeEventListener('change', cb) },
    () => mqGelap().matches,
  )
  return pilih === 'sistem' ? (sistemGelap ? 'gelap' : 'terang') : pilih
}

/** Pasang tema di <html>. Dengan `asal`, tema baru melebar sebagai lingkaran dari titik ketukan;
    tanpa itu (atau saat gerak dikurangi) memakai silang-pudar. `ubah` dijalankan di dalam transisi
    supaya ikon tombol ikut berganti pada cuplikan baru, bukan sebelum cuplikan lama diambil. */
export function terapkanTema(t: Tema, asal?: { x: number; y: number }, ubah?: () => void) {
  const html = document.documentElement
  const ganti = () => {
    html.dataset.theme = t
    document.querySelector('meta[name=theme-color]')?.setAttribute('content', t === 'gelap' ? '#0B1214' : '#FAF7F1')
    if (ubah) flushSync(ubah)
  }
  if (html.dataset.theme === t || !document.startViewTransition) return ganti()
  const lingkar = !!asal && !matchMedia('(prefers-reduced-motion: reduce)').matches
  if (lingkar) html.classList.add('vt-lingkar')
  const vt = document.startViewTransition(ganti)
  if (lingkar && asal) {
    const r = Math.hypot(Math.max(asal.x, innerWidth - asal.x), Math.max(asal.y, innerHeight - asal.y))
    vt.ready.then(() => html.animate(
      { clipPath: [`circle(0px at ${asal.x}px ${asal.y}px)`, `circle(${r}px at ${asal.x}px ${asal.y}px)`] },
      { duration: 650, easing: 'cubic-bezier(0.2, 0.8, 0.2, 1)', pseudoElement: '::view-transition-new(root)' },
    )).catch(() => {})
  }
  vt.finished.finally(() => html.classList.remove('vt-lingkar'))
}

/** Tombol cepat terang <-> gelap; ikon matahari/bulan berputar saat berganti. */
export function TombolTema({ className = '' }: { className?: string }) {
  const aktif = useTemaAktif()
  const atur = useApp((s) => s.atur)
  const gelap = aktif === 'gelap'
  return (
    <button aria-label={gelap ? 'Ganti ke mode terang' : 'Ganti ke mode gelap'} title={gelap ? 'Mode terang' : 'Mode gelap'}
      onClick={(e) => {
        const b = e.currentTarget.getBoundingClientRect()
        const baru: Tema = gelap ? 'terang' : 'gelap'
        terapkanTema(baru, { x: b.left + b.width / 2, y: b.top + b.height / 2 }, () => atur({ tema: baru }))
      }}
      className={`relative grid size-11 shrink-0 place-items-center overflow-hidden rounded-full border border-line bg-surface text-ink shadow-kartu hover:border-tint ${className}`}>
      <span className={`absolute transition-all duration-500 ease-[var(--ease-pegas)] ${gelap ? 'scale-50 -rotate-90 opacity-0' : 'scale-100 rotate-0 opacity-100'}`}><Ikon n="moon" /></span>
      <span className={`absolute text-gold-mid transition-all duration-500 ease-[var(--ease-pegas)] ${gelap ? 'scale-100 rotate-0 opacity-100' : 'scale-50 rotate-90 opacity-0'}`}><Ikon n="sun" /></span>
    </button>
  )
}

// ---------- Tata letak ----------
const LEBAR = {
  sempit: 'max-w-2xl',
  baca: 'max-w-3xl',
  lebar: 'max-w-6xl',
}

/** Halaman dengan judul besar (tab utama) atau bilah judul ringkas yang melekat (subhalaman). */
export function Halaman({ children, judul, kembali = true, kanan, sub, lebar = 'sempit' }: {
  children: ReactNode; judul?: string; kembali?: boolean; kanan?: ReactNode; sub?: ReactNode; lebar?: keyof typeof LEBAR
}) {
  const nav = useNavigate()
  return (
    <main className={`mx-auto w-full ${LEBAR[lebar]} px-4 pb-12 sm:px-6 lg:px-10`}>
      {kembali ? (
        <header className="kaca-latar sticky top-0 z-20 -mx-4 mb-4 px-2 pt-[env(safe-area-inset-top)] sm:-mx-6 sm:px-4 lg:-mx-10 lg:px-8">
          <div className="flex min-h-14 items-center gap-1">
            <button onClick={() => (history.length > 1 ? nav(-1) : nav('/'))} aria-label="Kembali"
              className="flex min-h-11 min-w-11 items-center gap-0.5 rounded-full pr-3 pl-1.5 font-semibold text-tint hover:bg-teal-light">
              <Ikon n="back" className="size-6" /><span className="hidden text-[0.95rem] sm:inline">Kembali</span>
            </button>
            {judul ? <h1 className="min-w-0 flex-1 truncate text-[1.0625rem] font-bold tracking-tight">{judul}</h1> : <span className="flex-1" />}
            {kanan}
          </div>
        </header>
      ) : (
        (judul || kanan) && (
          <header className="mb-6 flex items-start justify-between gap-4 pt-[max(1.75rem,calc(env(safe-area-inset-top)+1rem))] lg:pt-12">
            <div className="min-w-0">
              {sub && <p className="label-kecil mb-1.5">{sub}</p>}
              {judul && <h1 className="judul-besar text-[1.875rem] sm:text-[2.5rem] lg:text-5xl">{judul}</h1>}
            </div>
            <div className="flex shrink-0 items-center gap-2">
              <TombolTema className="lg:hidden" />
              {kanan}
            </div>
          </header>
        )
      )}
      <div className="animate-masuk">{children}</div>
    </main>
  )
}

export const Kartu = ({ children, className = '' }: { children: ReactNode; className?: string }) => (
  <section className={`rounded-[1.5rem] border border-line bg-surface p-5 shadow-kartu sm:p-6 ${className}`}>{children}</section>
)
export const Subjudul = ({ children, kanan }: { children: ReactNode; kanan?: ReactNode }) => (
  <div className="mb-3 flex items-center justify-between gap-3">
    <h2 className="text-[1.0625rem] font-bold tracking-tight">{children}</h2>
    {kanan}
  </div>
)

export const Tebal = ({ s }: { s: string }) => (
  <>{pecahTebal(s).map((p, i) => (p.tebal ? <strong key={i}>{p.t}</strong> : <span key={i}>{p.t}</span>))}</>
)

export const Catatan = ({ children, nada = 'emas' }: { children: ReactNode; nada?: 'emas' | 'teal' }) => (
  <div className={`flex gap-3 rounded-2xl px-4 py-3.5 text-sm leading-relaxed ${nada === 'emas' ? 'bg-gold-light text-gold-ink' : 'bg-teal-light text-teal-dark'}`}>
    <Ikon n="info" className="mt-0.5 size-4 shrink-0 opacity-80" />
    <div className="min-w-0">{children}</div>
  </div>
)

export const BadgeValidasi = ({ ok }: { ok: boolean }) => (
  <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold ${ok ? 'bg-teal-light text-teal-dark' : 'bg-gold-light text-gold-ink'}`}>
    <Ikon n={ok ? 'check' : 'info'} className="size-3.5" />
    {ok ? 'Divalidasi pengajar' : 'Belum divalidasi pengajar'}
  </span>
)

export function Tombol({ children, onClick, ikon, varian = 'utama', disabled, className = '', type = 'button' }: {
  children: ReactNode; onClick?: () => void; ikon?: string; varian?: 'utama' | 'garis' | 'teks' | 'bahaya'; disabled?: boolean; className?: string; type?: 'button' | 'submit'
}) {
  const gaya = {
    utama: 'bg-teal text-white shadow-teal hover:brightness-110',
    garis: 'bg-teal-light text-teal-dark hover:brightness-[.97]',
    teks: 'text-tint hover:bg-teal-light',
    bahaya: 'bg-danger-light text-danger hover:brightness-[.97]',
  }[varian]
  return (
    <button type={type} onClick={onClick} disabled={disabled}
      className={`inline-flex min-h-12 items-center justify-center gap-2 rounded-2xl px-5 text-[0.95rem] font-semibold disabled:cursor-not-allowed disabled:opacity-40 disabled:shadow-none ${gaya} ${className}`}>
      {ikon && <Ikon n={ikon} />}
      {children}
    </button>
  )
}

export function UbinHuruf({ huruf, aktif, onClick, label }: { huruf: string; aktif?: boolean; onClick?: () => void; label: string }) {
  return (
    <button onClick={onClick} aria-label={label} title={label}
      className={`arab relative grid aspect-square w-full place-items-center rounded-[1.1rem] border text-[2rem] sm:text-[2.25rem] ${aktif ? 'border-teal bg-teal text-white shadow-teal' : 'border-line bg-surface text-ink shadow-kartu hover:-translate-y-0.5 hover:border-tint'}`}>
      <span lang="ar" className="leading-none">{huruf}</span>
      {aktif && <span className="absolute -top-1.5 -right-1.5 grid size-5 place-items-center rounded-full bg-gold-mid text-on-gold ring-2 ring-cream"><Ikon n="check" className="size-3" /></span>}
    </button>
  )
}

export function Pil({ children, aktif, onClick }: { children: ReactNode; aktif?: boolean; onClick?: () => void }) {
  return (
    <button onClick={onClick} aria-pressed={aktif}
      className={`min-h-11 rounded-full border px-4 text-sm font-semibold ${aktif ? 'border-teal bg-teal text-white' : 'border-line bg-surface text-ink hover:border-tint'}`}>
      {children}
    </button>
  )
}

/** Kontrol segmen ala iOS: satu pilihan dari beberapa. */
export function Segmen<T extends string | number>({ pilihan, nilai, onUbah, label }: {
  pilihan: { v: T; l: ReactNode }[]; nilai: T; onUbah: (v: T) => void; label: string
}) {
  return (
    <div role="radiogroup" aria-label={label} className="flex gap-1 rounded-2xl bg-sand p-1">
      {pilihan.map((p) => (
        <button key={String(p.v)} role="radio" aria-checked={p.v === nilai} onClick={() => onUbah(p.v)}
          className={`min-h-10 flex-1 rounded-xl px-1.5 py-1 text-[0.8125rem] leading-tight font-semibold sm:text-sm ${p.v === nilai ? 'bg-surface text-ink shadow-kartu' : 'text-grey hover:text-ink'}`}>
          {p.l}
        </button>
      ))}
    </div>
  )
}

/** Sakelar: checkbox asli (semantik terjaga) dengan tampilan iOS. */
export function Saklar({ cek, onUbah, judul, ket }: { cek: boolean; onUbah: (v: boolean) => void; judul: string; ket?: string }) {
  return (
    <label className="flex min-h-12 cursor-pointer items-center justify-between gap-4">
      <span className="min-w-0"><span className="block text-[0.95rem] font-semibold">{judul}</span>{ket && <span className="mt-0.5 block text-xs leading-relaxed text-grey">{ket}</span>}</span>
      <input type="checkbox" role="switch" className="peer sr-only" checked={cek} onChange={(e) => onUbah(e.target.checked)} />
      <span aria-hidden className="relative h-[31px] w-[51px] shrink-0 rounded-full bg-border transition-colors peer-checked:bg-teal peer-focus-visible:outline-3 peer-focus-visible:outline-offset-2 peer-focus-visible:outline-tint after:absolute after:top-[2px] after:left-[2px] after:size-[27px] after:rounded-full after:bg-white after:shadow-md after:transition-transform after:duration-200 peer-checked:after:translate-x-5" />
    </label>
  )
}

/** Cincin kemajuan (0-1). */
export function Cincin({ nilai, ukuran = 64, tebal = 7, children }: { nilai: number; ukuran?: number; tebal?: number; children?: ReactNode }) {
  const r = (ukuran - tebal) / 2, k = 2 * Math.PI * r
  return (
    <span className="relative inline-grid shrink-0 place-items-center" style={{ width: ukuran, height: ukuran }}>
      <svg viewBox={`0 0 ${ukuran} ${ukuran}`} className="absolute inset-0 -rotate-90" aria-hidden>
        <circle cx={ukuran / 2} cy={ukuran / 2} r={r} fill="none" stroke="var(--color-sand)" strokeWidth={tebal} />
        <circle cx={ukuran / 2} cy={ukuran / 2} r={r} fill="none" stroke="var(--color-tint)" strokeWidth={tebal} strokeLinecap="round"
          strokeDasharray={k} strokeDashoffset={k * (1 - Math.min(1, Math.max(0, nilai)))} style={{ transition: 'stroke-dashoffset 600ms var(--ease-pegas)' }} />
      </svg>
      <span className="relative">{children}</span>
    </span>
  )
}

/** Lencana nomor berbentuk bintang delapan (khatam), motif mushaf. */
export function BintangNomor({ n, aktif }: { n: number | string; aktif?: boolean }) {
  return (
    <span className="relative grid size-11 shrink-0 place-items-center">
      <svg viewBox="0 0 44 44" className="absolute inset-0" aria-hidden>
        <g fill={aktif ? 'var(--color-teal)' : 'var(--color-sand)'} stroke={aktif ? 'var(--color-teal)' : 'var(--color-border)'} strokeWidth="1">
          <rect x="9" y="9" width="26" height="26" rx="3" />
          <rect x="9" y="9" width="26" height="26" rx="3" transform="rotate(45 22 22)" />
        </g>
      </svg>
      <span className={`relative text-[0.8rem] font-bold tabular-nums ${aktif ? 'text-white' : 'text-ink'}`}>{n}</span>
    </span>
  )
}

/** Logo: ubin teal dengan mim dan titik emas, sama dengan ikon aplikasi. */
export const Logo = ({ className = 'size-11 text-3xl rounded-[0.9rem]' }: { className?: string }) => (
  <span lang="ar" aria-hidden className={`arab relative grid shrink-0 place-items-center overflow-hidden bg-teal leading-none text-white ${className}`}>
    <span className="pola-khatam absolute inset-0 opacity-60" />
    <span className="absolute top-[16%] right-[18%] size-[18%] rounded-full bg-gold-mid" />
    <span className="relative -mt-[8%]">م</span>
  </span>
)

const MENU = [
  { to: '/', n: 'home', l: 'Belajar' },
  { to: '/peta', n: 'map', l: 'Peta' },
  { to: '/mushaf', n: 'book', l: 'Mushaf' },
  { to: '/saya', n: 'user', l: 'Saya' },
]

/** Bilah tab melayang di ponsel/tablet; bilah sisi permanen di layar lebar (pola tab bar -> sidebar). */
export function Navigasi({ tampilBawah }: { tampilBawah: boolean }) {
  const { dikuasai } = useApp()
  const total = materi.huruf.length
  return (
    <>
      <aside className="kaca-latar fixed inset-y-0 left-0 z-30 hidden w-72 flex-col border-r border-line px-4 py-7 lg:flex" aria-label="Navigasi utama">
        <div className="mb-8 flex items-center gap-2 px-2">
          <Link to="/" className="flex min-w-0 flex-1 items-center gap-3">
            <Logo />
            <span className="min-w-0"><span className="block text-lg font-extrabold tracking-tight">Makhraj</span><span className="block truncate text-xs text-grey">Huruf dari tempat keluarnya</span></span>
          </Link>
          <TombolTema />
        </div>
        <ul className="space-y-1">
          {[...MENU, { to: '/mirip', n: 'pair', l: 'Huruf mirip' }, { to: '/saya/studi', n: 'list', l: 'Uji coba' }].map((i, k) => (
            <li key={i.to}>
              {k === 4 && <p className="label-kecil mt-6 mb-2 px-3">Latihan</p>}
              <NavLink to={i.to} end={i.to === '/' || i.to === '/saya'}
                className={({ isActive }) => `flex min-h-11 items-center gap-3 rounded-xl px-3 text-[0.95rem] font-semibold ${isActive ? 'bg-teal-light text-teal-dark' : 'text-ink/80 hover:bg-sand'}`}>
                <Ikon n={i.n} className="size-5 opacity-90" />{i.l}
              </NavLink>
            </li>
          ))}
        </ul>
        <div className="mt-auto rounded-2xl border border-line bg-surface p-4 shadow-kartu">
          <div className="flex items-center gap-3">
            <Cincin nilai={dikuasai.length / total} ukuran={44} tebal={5}><span className="text-[0.7rem] font-bold">{Math.round((dikuasai.length / total) * 100)}%</span></Cincin>
            <p className="text-sm leading-snug"><strong>{dikuasai.length} dari {total}</strong><span className="block text-xs text-grey">huruf dikuasai</span></p>
          </div>
          <p className="mt-3 text-xs leading-relaxed text-grey">Pendamping talaqqi, bukan pengganti guru.</p>
        </div>
      </aside>

      {tampilBawah && (
        <nav className="pointer-events-none fixed inset-x-0 bottom-0 z-30 px-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] lg:hidden" aria-label="Navigasi utama">
          <ul className="kaca pointer-events-auto mx-auto flex max-w-md rounded-[1.75rem] border border-line/80 p-1.5 shadow-angkat">
            {MENU.map((i) => (
              <li key={i.to} className="flex-1">
                <NavLink to={i.to} end={i.to === '/'}
                  className={({ isActive }) => `tekan flex min-h-14 flex-col items-center justify-center gap-0.5 rounded-[1.35rem] text-[0.7rem] font-semibold ${isActive ? 'bg-teal-light text-teal-dark' : 'text-grey hover:text-ink'}`}>
                  <Ikon n={i.n} className="size-[1.4rem]" />
                  {i.l}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </>
  )
}

// ---------- Toast ----------
export const toast = (pesan: string) => window.dispatchEvent(new CustomEvent('toast', { detail: pesan }))
export function Toaster() {
  const [msg, setMsg] = useState<string | null>(null)
  useEffect(() => {
    let t: number
    const on = (e: Event) => {
      setMsg((e as CustomEvent<string>).detail)
      clearTimeout(t)
      t = window.setTimeout(() => setMsg(null), 3500)
    }
    window.addEventListener('toast', on)
    return () => window.removeEventListener('toast', on)
  }, [])
  return (
    <div role="status" aria-live="polite" className="pointer-events-none fixed inset-x-0 bottom-[calc(6.5rem+env(safe-area-inset-bottom))] z-40 flex justify-center px-5 lg:bottom-8 lg:pl-72">
      {msg && <p key={msg} className="animate-muncul max-w-md rounded-2xl bg-ink px-4 py-3 text-sm font-medium text-cream shadow-angkat">{msg}</p>}
    </div>
  )
}

// ---------- Penampang kepala ----------
// Koordinat 300x240, sama dengan purwarupa desain. Ilustrasi sederhana: perlu dicek guru tahsin
// dan digambar ulang di atas basis CC0 (Wright & McCloy, Wikimedia Commons).
const OUTLINE = 'M262 14 C190 8 128 30 112 70 C106 86 100 98 80 116 L94 124 C92 130 86 136 82 140 C86 144 90 146 90 147 C88 149 84 151 82 155 C88 160 92 166 94 172 C96 182 104 190 130 194 C150 197 160 202 165 212 L170 236 L292 236 L292 14 Z'
const GARIS = [
  'M100 114 C140 100 190 98 222 110',
  'M104 124 C150 116 190 118 222 124',
  'M92 136 C130 126 185 124 214 134 C222 140 224 150 220 160',
  'M222 124 C232 160 232 200 226 236',
  'M204 196 C202 212 200 225 198 236',
]
const LIDAH = 'M92 150 C112 138 165 132 196 144 C210 152 212 172 204 196 L182 196 C160 180 120 168 92 156 Z'

export type Sorot = [number, number, number, number]

export function Penampang({ sorot, panah, onTap, label, titik, zoom }: {
  sorot?: Sorot | null; panah?: string; onTap?: (x: number, y: number) => void; label: string
  titik?: { x: number; y: number; aktif?: boolean; label: string; onClick?: () => void }[]; zoom?: boolean
}) {
  const vb = zoom ? [60, 90, 180, 144] : [0, 0, 300, 240]
  const ref = useRef<SVGSVGElement>(null)
  const klik = (e: React.MouseEvent<SVGSVGElement>) => {
    if (!onTap || !ref.current) return
    const p = ref.current.createSVGPoint()
    p.x = e.clientX
    p.y = e.clientY
    const m = ref.current.getScreenCTM()
    if (!m) return
    const q = p.matrixTransform(m.inverse())
    onTap(q.x, q.y)
  }
  return (
    <svg ref={ref} viewBox={vb.join(' ')} role="img" aria-label={label} onClick={klik}
      className={`block w-full rounded-2xl bg-sand ${onTap ? 'cursor-pointer' : ''}`}>
      <path d={OUTLINE} fill="var(--color-surface)" stroke="var(--color-ink)" strokeWidth={2} strokeLinejoin="round" />
      {GARIS.map((d) => <path key={d} d={d} fill="none" stroke="var(--color-grey)" strokeOpacity={0.55} strokeWidth={2} strokeLinecap="round" />)}
      <path d={LIDAH} fill="var(--color-lidah)" stroke="var(--color-lidah-garis)" strokeWidth={1.5} />
      {sorot && (
        <g style={{ transform: `translate(${sorot[0]}px, ${sorot[1]}px) scale(${sorot[2]}, ${sorot[3]})`, transition: 'transform 420ms var(--ease-pegas)' }}>
          <circle r={1} fill="rgba(226,169,59,.42)" stroke="var(--color-sorot-garis)" strokeWidth={2.5} vectorEffect="non-scaling-stroke" />
        </g>
      )}
      {panah && <path d={panah} fill="none" stroke="var(--color-tint)" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round" />}
      {titik?.map((t) => (
        <g key={t.label} onClick={(e) => { e.stopPropagation(); t.onClick?.() }} className={t.onClick ? 'cursor-pointer' : ''}>
          <title>{t.label}</title>
          {/* Area ketuk tak terlihat agar titik kecil mudah disentuh jari. */}
          {t.onClick && <circle cx={t.x} cy={t.y} r={9} fill="transparent" />}
          <circle cx={t.x} cy={t.y} r={t.aktif ? 4.8 : 3.4} fill={t.aktif ? 'var(--color-tint)' : 'var(--color-surface)'} stroke="var(--color-tint)" strokeWidth={1.6} />
        </g>
      ))}
    </svg>
  )
}

// ---------- Klip guru: thumbnail dulu, YouTube IFrame resmi setelah diketuk ----------
// Kebijakan YouTube API: video tidak diunduh/di-cache, audio tidak dipisah, pemutar tidak ditutupi,
// ukuran minimal 200x200 px. Potongan memakai loadVideoById({startSeconds, endSeconds}).
declare global {
  interface Window { YT?: any; onYouTubeIframeAPIReady?: () => void }
}
let ytApi: Promise<any> | null = null
const muatYT = () =>
  (ytApi ??= new Promise((ok) => {
    if (window.YT?.Player) return ok(window.YT)
    window.onYouTubeIframeAPIReady = () => ok(window.YT)
    const s = document.createElement('script')
    s.src = 'https://www.youtube.com/iframe_api'
    document.head.appendChild(s)
  }))

export type KlipRef = { putar: (mulai?: number | null, selesai?: number | null) => void }

export function KlipGuru({ videoId, judul, ref }: { videoId: string; judul: string; ref?: Ref<KlipRef> }) {
  const [aktif, setAktif] = useState(false)
  const host = useRef<HTMLDivElement>(null)
  const player = useRef<any>(null)
  const antre = useRef<{ mulai?: number | null; selesai?: number | null } | null>(null)

  const muat = (mulai?: number | null, selesai?: number | null) => {
    const opsi = { videoId, startSeconds: mulai ?? 0, ...(selesai ? { endSeconds: selesai } : {}) }
    player.current.loadVideoById(opsi)
  }
  useImperativeHandle(ref, () => ({
    putar: (mulai, selesai) => {
      if (player.current?.loadVideoById) return muat(mulai, selesai)
      antre.current = { mulai, selesai }
      setAktif(true)
    },
  }))

  useEffect(() => {
    if (!aktif || !host.current) return
    let batal = false
    // YT.Player mengganti elemen target dengan iframe; target dibuat manual agar DOM milik React tidak disentuh.
    const target = document.createElement('div')
    target.className = 'absolute inset-0 size-full'
    host.current.appendChild(target)
    muatYT().then((YT) => {
      if (batal) return
      player.current = new YT.Player(target, {
        host: 'https://www.youtube-nocookie.com',
        videoId,
        playerVars: { rel: 0, playsinline: 1, modestbranding: 1, start: antre.current?.mulai ?? 0 },
        events: {
          onReady: (e: any) => {
            const q = antre.current
            antre.current = null
            if (q?.selesai) muat(q.mulai, q.selesai)
            else e.target.playVideo()
          },
          onError: () => toast('Video tidak dapat diputar di sini. Gunakan tautan "Buka di YouTube".'),
        },
      })
    })
    const el = host.current
    return () => {
      batal = true
      player.current?.destroy?.()
      player.current = null
      el.replaceChildren()
    }
  }, [aktif, videoId])

  useEffect(() => setAktif(false), [videoId])

  return (
    <div>
      <div className="relative aspect-video min-h-[200px] w-full overflow-hidden rounded-2xl bg-black">
        {aktif ? (
          <div ref={host} className="absolute inset-0 size-full" />
        ) : (
          <button onClick={() => setAktif(true)} className="group absolute inset-0 size-full" aria-label={`Putar video: ${judul}`}>
            <img src={`https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`} alt="" loading="lazy" className="size-full object-cover opacity-80 transition-transform duration-500 group-hover:scale-[1.03]" />
            <span className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
            <span className="absolute inset-0 grid place-items-center">
              <span className="grid size-16 place-items-center rounded-full bg-white/90 text-[#0f5e5e] shadow-angkat backdrop-blur transition-transform group-hover:scale-105"><Ikon n="play" className="ml-0.5 size-7" /></span>
            </span>
          </button>
        )}
      </div>
      <a href={`https://www.youtube.com/watch?v=${videoId}`} target="_blank" rel="noreferrer"
        className="mt-2 inline-flex min-h-11 items-center gap-1.5 text-sm font-semibold text-tint hover:underline">
        <Ikon n="external" className="size-4" /> Buka di YouTube
      </a>
    </div>
  )
}

export function VideoKosong({ huruf }: { huruf: string }) {
  return (
    <div className="grid aspect-video place-items-center rounded-2xl border border-dashed border-border bg-sand p-6 text-center text-sm leading-relaxed text-grey">
      <p>Klip guru untuk huruf <Arab className="text-xl text-ink">{huruf}</Arab> belum tersedia dari kanal rujukan. Pelajari letaknya dari penampang dan tanyakan contoh pelafalannya kepada guru.</p>
    </div>
  )
}

export const Arab = ({ children, className = '' }: { children: ReactNode; className?: string }) => (
  <span lang="ar" dir="rtl" className={`arab ${className}`}>{children}</span>
)
