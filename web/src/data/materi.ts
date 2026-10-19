import raw from './materi.json'

// ---------- Tipe materi ----------
export type Area = { id: string; nama: string; arab: string; arti: string; elips: number[]; deskripsi: string }
export type Titik = { id: string; no: number; area: string; nama: string; posisi: number[]; deskripsi: string }
export type Langkah = { label: string; judul: string; isi: string; r: number; panah: string }
export type Pelajaran = { makhraj: string; langkah?: Langkah[]; kesalahanUmum?: string; cek?: string[] }
export type Huruf = {
  id: string
  huruf: string
  nama: string
  latin: string
  titik: string
  titikMad?: string
  video: string | null
  videoAlt: string | null
  catatan?: string
  pelajaran?: Pelajaran
  kesalahan?: { teks: string; sumber: string }
}
export type Mirip = { a: string; b: string; judul: string; ringkas: string }

export const materi = raw as unknown as {
  tervalidasi: boolean
  sumberVideo: { id: string; kanal: string; guru: string; judul: string; playlist: string }[]
  area: Area[]
  titik: Titik[]
  huruf: Huruf[]
  mirip: Mirip[]
}

const byId = <T extends { id: string }>(xs: T[]) => new Map(xs.map((x) => [x.id, x]))
const hurufMap = byId(materi.huruf)
const titikMap = byId(materi.titik)
const areaMap = byId(materi.area)

export const hurufById = (id: string) => hurufMap.get(id)
export const titikById = (id: string) => titikMap.get(id)!
export const areaById = (id: string) => areaMap.get(id)!
export const areaOf = (h: Huruf) => areaById(titikById(h.titik).area)
export const urutan = (h: Huruf) => materi.huruf.indexOf(h) + 1

/** Huruf yang keluar dari suatu area (wau dan ya juga masuk Al-Jauf sebagai huruf mad). */
export function anggotaArea(areaId: string): Huruf[] {
  return materi.huruf.filter(
    (h) => titikById(h.titik).area === areaId || (h.titikMad && titikById(h.titikMad).area === areaId),
  )
}
export const anggotaTitik = (titikId: string) => materi.huruf.filter((h) => h.titik === titikId)

// ---------- Sifat huruf ----------
// Dihitung dari kelompok huruf pada matan Al-Jazariyyah, sehingga konsisten untuk ke-29 huruf.
export type Sifat = { id: string; nama: string; arti: string; lawan?: string; tonjol?: boolean; leksikal?: boolean }

export const SIFAT: Record<string, Sifat> = {
  hams: { id: 'hams', nama: 'Hams', arti: 'napas mengalir', lawan: 'jahr' },
  jahr: { id: 'jahr', nama: 'Jahr', arti: 'napas tertahan', lawan: 'hams' },
  syiddah: { id: 'syiddah', nama: 'Syiddah', arti: 'suara tertahan' },
  tawassuth: { id: 'tawassuth', nama: 'Tawassuth', arti: 'suara antara tertahan dan mengalir' },
  rakhawah: { id: 'rakhawah', nama: 'Rakhawah', arti: 'suara mengalir' },
  istila: { id: 'istila', nama: "Isti'la", arti: 'pangkal lidah terangkat, huruf tebal', lawan: 'istifal', tonjol: true },
  istifal: { id: 'istifal', nama: 'Istifal', arti: 'pangkal lidah turun, huruf tipis', lawan: 'istila' },
  ithbaq: { id: 'ithbaq', nama: 'Ithbaq', arti: 'lidah menutup ke langit-langit', lawan: 'infitah', tonjol: true },
  infitah: { id: 'infitah', nama: 'Infitah', arti: 'lidah tidak menempel ke langit-langit', lawan: 'ithbaq' },
  idzlaq: { id: 'idzlaq', nama: 'Idzlaq', arti: 'ringan diucapkan', lawan: 'ishmat', leksikal: true },
  ishmat: { id: 'ishmat', nama: 'Ishmat', arti: 'berat diucapkan', lawan: 'idzlaq', leksikal: true },
  safir: { id: 'safir', nama: 'Shafir', arti: 'berdesis seperti siulan', tonjol: true },
  qalqalah: { id: 'qalqalah', nama: 'Qalqalah', arti: 'memantul saat sukun', tonjol: true },
  lin: { id: 'lin', nama: 'Lin', arti: 'lunak, saat sukun didahului fathah', tonjol: true },
  inhiraf: { id: 'inhiraf', nama: 'Inhiraf', arti: 'makhrajnya condong', tonjol: true },
  takrir: { id: 'takrir', nama: 'Takrir', arti: 'cenderung bergetar; dijaga agar tidak berulang', tonjol: true },
  tafasysyi: { id: 'tafasysyi', nama: 'Tafasysyi', arti: 'angin menyebar di dalam mulut', tonjol: true },
  istithalah: { id: 'istithalah', nama: 'Istithalah', arti: 'bunyi memanjang di tepi lidah', tonjol: true },
  ghunnah: { id: 'ghunnah', nama: 'Ghunnah', arti: 'dengung dari rongga hidung', tonjol: true },
}

// Kelompok huruf (matan): فحثه شخص سكت, أجد قط بكت, لن عمر, خص ضغط قظ, ...
const KELOMPOK: Record<string, string> = {
  hams: 'فحثهشخصسكت',
  syiddah: 'ءجدقطبكت',
  tawassuth: 'لنعمر',
  istila: 'خصضغطقظ',
  ithbaq: 'صضطظ',
  idzlaq: 'فرمنلب',
  safir: 'صزس',
  qalqalah: 'قطبجد',
  lin: 'وي',
  inhiraf: 'لر',
  takrir: 'ر',
  tafasysyi: 'ش',
  istithalah: 'ض',
  ghunnah: 'نم',
}

export function sifatHuruf(h: Huruf): Sifat[] {
  const c = h.huruf
  const has = (k: string) => KELOMPOK[k].includes(c)
  const ids = [
    has('hams') ? 'hams' : 'jahr',
    has('syiddah') ? 'syiddah' : has('tawassuth') ? 'tawassuth' : 'rakhawah',
    has('istila') ? 'istila' : 'istifal',
    has('ithbaq') ? 'ithbaq' : 'infitah',
    has('idzlaq') ? 'idzlaq' : 'ishmat',
    ...['safir', 'qalqalah', 'lin', 'inhiraf', 'takrir', 'tafasysyi', 'istithalah', 'ghunnah'].filter(has),
  ]
  return ids.map((id) => SIFAT[id])
}

// ---------- Harakat untuk tombol dengar dan latihan ----------
export type Harakat = { teks: string; label: string }
const F = 'َ', K = 'ِ', D = 'ُ', S = 'ْ'

export function harakatHuruf(h: Huruf): Harakat[] {
  if (h.id === 'alif') return [
    { teks: 'بَا', label: 'baa (mad)' },
    { teks: 'تَا', label: 'taa (mad)' },
    { teks: 'قَالَ', label: 'qaala' },
  ]
  const c = h.id === 'hamzah' ? 'أ' : h.huruf
  const bawah = h.id === 'hamzah' ? 'إ' : c
  const l = h.latin.replace(/\s.*/, '')
  return [
    { teks: c + F, label: `${l}a fathah` },
    { teks: bawah + K, label: `${l}i kasrah` },
    { teks: c + D, label: `${l}u dammah` },
    { teks: 'أ' + F + h.huruf + S, label: `a${l} sukun` },
  ]
}

// ---------- Pencocokan huruf di mushaf ----------
// Bentuk tulisan yang dihitung sebagai huruf yang sama. Teks tampilan Tanzil tidak diubah;
// pencocokan hanya melihat huruf dasar, sehingga harakat dan tanda waqaf otomatis diabaikan.
const VARIAN: Record<string, string> = {
  'ا': 'اأإآٱٰ',
  'ء': 'ءأإؤئٕٔ',
  'ي': 'يى',
}
export const kodeHuruf = (huruf: string) => new Set(VARIAN[huruf] ?? huruf)
export const kataMemuat = (kata: string, kode: Set<string>) => [...kata].some((c) => kode.has(c))

// ---------- Teks Al-Qur'an (Tanzil Utsmani, CC BY 3.0, tidak diubah) ----------
export type Surah = { n: number; name: string; tname: string; ename: string; type: string; basmalah: boolean; ayahs: string[] }
export type Quran = { basmalah: string; suras: Surah[] }

let quranP: Promise<Quran> | null = null
let terjemahP: Promise<string[][]> | null = null
const dataUrl = (f: string) => new URL(`data/${f}`, document.baseURI).href
export const loadQuran = () => (quranP ??= fetch(dataUrl('quran.json')).then((r) => r.json()))
export const loadTerjemah = () => (terjemahP ??= fetch(dataUrl('id.json')).then((r) => r.json()))

export type Contoh = { kata: string; surah: number; ayat: number; tname: string }

/** Contoh kata dari mushaf (Al-Fatihah lalu Juz 'Amma) yang memuat huruf; diambil apa adanya dari teks. */
export function contohKata(q: Quran, h: Huruf, maks = 3, tanpa?: Huruf): Contoh[] {
  const kode = kodeHuruf(h.huruf)
  const hindari = tanpa ? kodeHuruf(tanpa.huruf) : null
  const out: Contoh[] = []
  const seen = new Set<string>()
  for (const s of [q.suras[0], ...q.suras.slice(77)]) {
    for (const [i, ayat] of s.ayahs.entries()) {
      for (const kata of ayat.split(' ')) {
        if (kata.length < 2 || seen.has(kata) || !kataMemuat(kata, kode)) continue
        if (hindari && kataMemuat(kata, hindari)) continue
        seen.add(kata)
        out.push({ kata, surah: s.n, ayat: i + 1, tname: s.tname })
        if (out.length >= maks) return out
      }
    }
  }
  return out
}

// ---------- Soal ----------
export type Soal = { id: string; tanya: string; arab?: string; opsi: { id: string; label: string; arab?: boolean }[]; jawab: string }

function acak(seed: number) {
  // mulberry32: soal tetap sama untuk seed yang sama (tes sebelum/sesudah harus identik antarpeserta)
  return () => {
    seed |= 0
    seed = (seed + 0x6d2b79f5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}
function kocok<T>(xs: T[], r: () => number): T[] {
  const a = [...xs]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(r() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

const opsiHuruf = (hs: Huruf[]) => hs.map((h) => ({ id: h.id, label: h.huruf, arab: true }))

/** Kuis pasangan huruf mirip: dari perbedaan titik makhraj dan sifat. */
export function kuisMirip(m: Mirip, q?: Quran): Soal[] {
  const a = hurufById(m.a)!, b = hurufById(m.b)!
  const pair = opsiHuruf([a, b])
  const soal: Soal[] = []
  if (a.titik !== b.titik) {
    for (const h of [a, b]) {
      const t = titikById(h.titik)
      soal.push({ id: `titik-${h.id}`, tanya: `Huruf mana yang keluar dari ${t.nama}: ${t.deskripsi.toLowerCase()}`, opsi: pair, jawab: h.id })
    }
  }
  const sa = sifatHuruf(a).filter((s) => !s.leksikal), sb = sifatHuruf(b).filter((s) => !s.leksikal)
  for (const [h, mine, other] of [[a, sa, sb], [b, sb, sa]] as const) {
    const beda = mine.find((s) => !other.some((o) => o.id === s.id))
    if (beda) soal.push({ id: `sifat-${h.id}`, tanya: `Huruf mana yang bersifat ${beda.nama} (${beda.arti})?`, opsi: pair, jawab: h.id })
  }
  if (q) {
    for (const [h, lain] of [[a, b], [b, a]] as const) {
      const c = contohKata(q, h, 1, lain)[0]
      if (c) soal.push({ id: `kata-${h.id}`, tanya: `Kata ini (QS ${c.tname}: ${c.ayat}) memakai huruf yang mana?`, arab: c.kata, opsi: pair, jawab: h.id })
    }
  }
  return soal
}

/**
 * Tes pemahaman makhraj 20 soal, dua bentuk paralel (A dan B) dengan huruf yang berbeda,
 * untuk desain sebelum-sesudah dengan urutan bentuk yang ditukar antarpeserta.
 */
export function tesMakhraj(bentuk: 'A' | 'B'): Soal[] {
  const r = acak(bentuk === 'A' ? 20261 : 20262)
  const semua = kocok(materi.huruf.filter((h) => h.id !== 'alif'), acak(7))
  const milik = semua.filter((_, i) => (i % 2 === 0) === (bentuk === 'A'))
  const soal: Soal[] = []

  // Wau dan ya punya dua area (huruf mad di Al-Jauf), jadi tidak dipakai untuk soal area.
  const untukArea = milik.filter((h) => !h.titikMad).slice(0, 7)
  const untukTitik = milik.filter((h) => !untukArea.includes(h)).slice(0, 7)

  // 7 soal area
  for (const h of untukArea) {
    soal.push({
      id: `${bentuk}-area-${h.id}`,
      tanya: 'Dari area makhraj mana huruf ini keluar?',
      arab: h.huruf,
      opsi: kocok(materi.area.filter((a) => a.id !== 'khaisyum'), r).map((a) => ({ id: a.id, label: `${a.nama} (${a.arti.toLowerCase()})` })),
      jawab: areaOf(h).id,
    })
  }
  // 7 soal titik: pilih huruf dari deskripsi titik
  for (const h of untukTitik) {
    const t = titikById(h.titik)
    const pengecoh = kocok(materi.huruf.filter((x) => x.titik !== h.titik && x.id !== 'alif'), r).slice(0, 3)
    soal.push({
      id: `${bentuk}-titik-${h.id}`,
      tanya: `Huruf mana yang keluar dari: ${t.deskripsi.toLowerCase()}`,
      opsi: kocok(opsiHuruf([h, ...pengecoh]), r),
      jawab: h.id,
    })
  }
  // 6 soal sifat: huruf mana yang punya sifat tertentu
  const sifatUji = bentuk === 'A' ? ['qalqalah', 'istila', 'hams', 'safir', 'ithbaq', 'ghunnah'] : ['qalqalah', 'istila', 'hams', 'safir', 'ithbaq', 'inhiraf']
  for (const sid of sifatUji) {
    const s = SIFAT[sid]
    const punya = materi.huruf.filter((h) => sifatHuruf(h).some((x) => x.id === sid))
    const tidak = materi.huruf.filter((h) => h.id !== 'alif' && !punya.includes(h))
    const benar = kocok(punya, r)[0]
    soal.push({
      id: `${bentuk}-sifat-${sid}`,
      tanya: `Huruf mana yang bersifat ${s.nama} (${s.arti})?`,
      opsi: kocok(opsiHuruf([benar, ...kocok(tidak, r).slice(0, 3)]), r),
      jawab: benar.id,
    })
  }
  return soal
}

// ---------- Teks **tebal** sederhana ----------
export const pecahTebal = (s: string) => s.split('**').map((t, i) => ({ t, tebal: i % 2 === 1 }))
