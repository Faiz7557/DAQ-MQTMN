import { create } from 'zustand'
import { persist } from 'zustand/middleware'

// Semua data pengguna disimpan di perangkat (MVP tanpa akun). Sinkron Firestore menyusul (Tahap 2).
export const hariIni = (d = new Date()) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`

export type Event = { t: string; jenis: string; huruf?: string; detail?: string }
export type HasilTes = { bentuk: 'A' | 'B'; fase: 'sebelum' | 'sesudah'; skor: number; total: number; jawaban: Record<string, string>; t: string }
export type HasilSus = { jawaban: number[]; skor: number; t: string }

type State = {
  dikuasai: string[]
  hariAktif: string[]
  terakhirSurah: number
  cek: Record<string, number[]>
  events: Event[]
  tes: HasilTes[]
  sus: HasilSus[]
  pengaturan: {
    onboarding: boolean
    tampilkanHari: boolean
    skalaTeks: number
    sumberVideo: 'andalasy' | 'resmi'
    /** Simpanan lama tidak punya kolom ini; anggap 'sistem'. */
    tema?: 'sistem' | 'terang' | 'gelap'
    studi: null | { kode: string; setuju: string; dewasa: boolean }
  }
  catat: (jenis: string, huruf?: string, detail?: string) => void
  tandai: (id: string, v: boolean) => void
  setCek: (id: string, idx: number[]) => void
  bacaSurah: (n: number) => void
  simpanTes: (h: HasilTes) => void
  simpanSus: (h: HasilSus) => void
  atur: (p: Partial<State['pengaturan']>) => void
  reset: () => void
}

const awal = {
  dikuasai: [] as string[],
  hariAktif: [] as string[],
  terakhirSurah: 1,
  cek: {} as Record<string, number[]>,
  events: [] as Event[],
  tes: [] as HasilTes[],
  sus: [] as HasilSus[],
  pengaturan: { onboarding: false, tampilkanHari: true, skalaTeks: 1, sumberVideo: 'andalasy' as const, studi: null },
}

// Hari aktif = hari dengan minimal satu kegiatan bermakna (Lampiran 8 proposal); 'buka' saja tidak dihitung.
const BERMAKNA = new Set(['langkah', 'rekam', 'kuis_mirip', 'tes', 'baca_surah'])

export const useApp = create<State>()(
  persist(
    (set) => ({
      ...awal,
      catat: (jenis, huruf, detail) =>
        set((s) => {
          const today = hariIni()
          // ponytail: log dibatasi 2000 kejadian terakhir; cukup untuk studi 2 pekan, pindah ke Firestore jika lebih.
          const events = [...s.events, { t: new Date().toISOString(), jenis, huruf, detail }].slice(-2000)
          const hariAktif = !BERMAKNA.has(jenis) || s.hariAktif.includes(today) ? s.hariAktif : [...s.hariAktif, today].slice(-400)
          return { events, hariAktif }
        }),
      tandai: (id, v) => {
        set((s) => ({ dikuasai: v ? [...new Set([...s.dikuasai, id])] : s.dikuasai.filter((x) => x !== id) }))
        useApp.getState().catat(v ? 'dikuasai' : 'batal_dikuasai', id)
      },
      setCek: (id, idx) => set((s) => ({ cek: { ...s.cek, [id]: idx } })),
      bacaSurah: (n) => set({ terakhirSurah: n }),
      simpanTes: (h) => set((s) => ({ tes: [...s.tes, h] })),
      simpanSus: (h) => set((s) => ({ sus: [...s.sus, h] })),
      atur: (p) => set((s) => ({ pengaturan: { ...s.pengaturan, ...p } })),
      reset: () => set({ ...awal, pengaturan: { ...awal.pengaturan, onboarding: true } }),
    }),
    { name: 'makhraj-v1' },
  ),
)

/** Hari beruntun sampai hari ini (atau kemarin, agar tidak langsung putus di pagi hari). */
export function hariBeruntun(hari: string[], now = new Date()): number {
  const set = new Set(hari)
  const d = new Date(now)
  if (!set.has(hariIni(d))) d.setDate(d.getDate() - 1)
  let n = 0
  while (set.has(hariIni(d))) {
    n++
    d.setDate(d.getDate() - 1)
  }
  return n
}

/** Jumlah hari belajar dalam 7 hari terakhir: indikator studi "aktif 4 hari per pekan". */
export function hariPekanIni(hari: string[], now = new Date()): number {
  const set = new Set(hari)
  let n = 0
  for (let i = 0; i < 7; i++) {
    const d = new Date(now)
    d.setDate(d.getDate() - i)
    if (set.has(hariIni(d))) n++
  }
  return n
}

/** Skor SUS (Brooke, 1996): butir ganjil (x-1), butir genap (5-x), jumlah dikali 2,5. */
export const skorSus = (j: number[]) => j.reduce((a, x, i) => a + (i % 2 === 0 ? x - 1 : 5 - x), 0) * 2.5

// ---------- Rekaman suara di IndexedDB (tidak pernah diunggah pada MVP) ----------
export type Rekaman = { id: string; huruf: string; blob: Blob; mime: string; t: string; durasi: number }

function db(): Promise<IDBDatabase> {
  return new Promise((ok, gagal) => {
    const r = indexedDB.open('makhraj', 1)
    r.onupgradeneeded = () => r.result.createObjectStore('rekaman', { keyPath: 'id' }).createIndex('huruf', 'huruf')
    r.onsuccess = () => ok(r.result)
    r.onerror = () => gagal(r.error)
  })
}
async function tx<T>(mode: IDBTransactionMode, fn: (s: IDBObjectStore) => IDBRequest<T>): Promise<T> {
  const d = await db()
  return new Promise((ok, gagal) => {
    const req = fn(d.transaction('rekaman', mode).objectStore('rekaman'))
    req.onsuccess = () => ok(req.result)
    req.onerror = () => gagal(req.error)
  })
}
export const rekaman = {
  simpan: (r: Rekaman) => tx('readwrite', (s) => s.put(r)),
  milik: (huruf: string) => tx<Rekaman[]>('readonly', (s) => s.index('huruf').getAll(huruf)),
  semua: () => tx<Rekaman[]>('readonly', (s) => s.getAll()),
  hapus: (id: string) => tx('readwrite', (s) => s.delete(id)),
  hapusSemua: () => tx('readwrite', (s) => s.clear()),
}

/** Ekspor data studi tanpa rekaman, untuk diserahkan peserta kepada peneliti. */
export function eksporStudi(): string {
  const s = useApp.getState()
  return JSON.stringify(
    {
      aplikasi: 'makhraj-web',
      versi: '0.2.0',
      diekspor: new Date().toISOString(),
      peserta: s.pengaturan.studi?.kode ?? null,
      persetujuan: s.pengaturan.studi?.setuju ?? null,
      dikuasai: s.dikuasai,
      hariAktif: s.hariAktif,
      tes: s.tes,
      sus: s.sus,
      events: s.events,
    },
    null,
    2,
  )
}
