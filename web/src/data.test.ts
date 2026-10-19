import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'
import { anggotaArea, contohKata, harakatHuruf, hurufById, kataMemuat, kodeHuruf, kuisMirip, materi, sifatHuruf, tesMakhraj, titikById, type Quran } from './data/materi'
import { hariBeruntun, hariIni, hariPekanIni, skorSus, useApp } from './store'

const q: Quran = JSON.parse(readFileSync(new URL('../public/data/quran.json', import.meta.url), 'utf8'))
const ids = (xs: { id: string }[]) => xs.map((x) => x.id)

describe('materi', () => {
  it('29 huruf, 17 titik, 5 area; semua rujukan valid', () => {
    expect(materi.huruf).toHaveLength(29)
    expect(materi.titik).toHaveLength(17)
    expect(materi.area).toHaveLength(5)
    for (const h of materi.huruf) {
      expect(titikById(h.titik), h.id).toBeTruthy()
      if (h.titikMad) expect(titikById(h.titikMad)).toBeTruthy()
    }
    for (const m of materi.mirip) expect(hurufById(m.a) && hurufById(m.b)).toBeTruthy()
  })

  it('Al-Lisan memuat 18 huruf, Al-Halq 6, Al-Jauf 3 (sesuai kitab)', () => {
    expect(anggotaArea('lisan')).toHaveLength(18)
    expect(anggotaArea('halq')).toHaveLength(6)
    expect(ids(anggotaArea('jauf')).sort()).toEqual(['alif', 'wau', 'ya'])
  })

  it('sifat dihitung dari kelompok matan', () => {
    const s = (id: string) => ids(sifatHuruf(hurufById(id)!))
    expect(s('ba')).toEqual(['jahr', 'syiddah', 'istifal', 'infitah', 'idzlaq', 'qalqalah'])
    expect(s('shad')).toEqual(['hams', 'rakhawah', 'istila', 'ithbaq', 'ishmat', 'safir'])
    expect(s('ra')).toEqual(['jahr', 'tawassuth', 'istifal', 'infitah', 'idzlaq', 'inhiraf', 'takrir'])
    expect(s('dhad')).toContain('istithalah')
    // setiap huruf punya tepat 5 sifat berlawanan
    for (const h of materi.huruf) expect(sifatHuruf(h).filter((x) => x.lawan || ['syiddah', 'tawassuth', 'rakhawah'].includes(x.id)).length).toBe(5)
  })

  it('harakat sukun memakai hamzah di depan', () => {
    expect(harakatHuruf(hurufById('ba')!).map((h) => h.teks)).toEqual(['بَ', 'بِ', 'بُ', 'أَبْ'])
  })
})

describe('sorot huruf di mushaf', () => {
  it('harakat diabaikan; alif wasla dan hamzah di atas alif ikut terhitung', () => {
    expect(kataMemuat('ٱلْحَمْدُ', kodeHuruf('ح'))).toBe(true)
    expect(kataMemuat('ٱلْحَمْدُ', kodeHuruf('ه'))).toBe(false)
    expect(kataMemuat('ٱلْحَمْدُ', kodeHuruf('ا'))).toBe(true)
    expect(kataMemuat('أَعُوذُ', kodeHuruf('ء'))).toBe(true)
  })
  it('Al-Fatihah: 4 kata memuat ب (seperti layar MVP)', () => {
    const kode = kodeHuruf('ب')
    const n = q.suras[0].ayahs.flatMap((a) => a.split(' ')).filter((k) => kataMemuat(k, kode)).length
    expect(n).toBe(4)
  })
  it('contoh kata diambil apa adanya dari teks', () => {
    const c = contohKata(q, hurufById('qaf')!, 3)
    expect(c.length).toBe(3)
    for (const x of c) expect(q.suras[x.surah - 1].ayahs[x.ayat - 1].split(' ')).toContain(x.kata)
  })
})

describe('soal', () => {
  it('tes A dan B: 20 soal, jawaban ada di opsi, huruf tidak tumpang tindih, deterministik', () => {
    const a = tesMakhraj('A'), b = tesMakhraj('B')
    expect(a).toHaveLength(20)
    expect(b).toHaveLength(20)
    for (const s of [...a, ...b]) expect(s.opsi.map((o) => o.id)).toContain(s.jawab)
    expect(tesMakhraj('A')).toEqual(a)
    const hurufSoal = (xs: typeof a) => xs.slice(0, 14).map((s) => s.id.split('-').pop())
    expect(hurufSoal(a).filter((x) => hurufSoal(b).includes(x))).toEqual([])
    // wau/ya punya dua area: tidak boleh jadi soal area (jawabannya ambigu)
    expect([...a, ...b].filter((s) => /area-(wau|ya)$/.test(s.id))).toEqual([])
  })
  it('kuis mirip punya soal untuk keenam pasangan', () => {
    for (const m of materi.mirip) expect(kuisMirip(m, q).length).toBeGreaterThanOrEqual(2)
  })
})

describe('progres dan SUS', () => {
  it('skor SUS: semua netral = 50, terbaik = 100', () => {
    expect(skorSus(Array(10).fill(3))).toBe(50)
    expect(skorSus([5, 1, 5, 1, 5, 1, 5, 1, 5, 1])).toBe(100)
  })
  it('hari beruntun dan hari per pekan', () => {
    const now = new Date(2026, 9, 19)
    const d = (k: number) => hariIni(new Date(2026, 9, 19 - k))
    expect(hariBeruntun([d(0), d(1), d(2), d(4)], now)).toBe(3)
    expect(hariBeruntun([d(1), d(2)], now)).toBe(2)
    expect(hariPekanIni([d(0), d(3), d(6), d(7)], now)).toBe(3)
  })
})

describe('hari aktif', () => {
  it('hanya kegiatan bermakna yang menambah hari aktif; buka tetap tercatat di log', () => {
    useApp.getState().reset()
    useApp.getState().catat('buka')
    expect(useApp.getState().hariAktif).toEqual([])
    expect(useApp.getState().events.map((e) => e.jenis)).toEqual(['buka'])
    useApp.getState().catat('langkah', 'ba')
    useApp.getState().catat('rekam', 'ba')
    expect(useApp.getState().hariAktif).toEqual([hariIni()])
  })
})
