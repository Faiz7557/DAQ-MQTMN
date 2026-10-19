import { useCallback, useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router'
import { harakatHuruf, hurufById, sifatHuruf, titikById, type Huruf } from '../data/materi'
import { rekaman, useApp, type Rekaman } from '../store'
import { Arab, Catatan, Halaman, Ikon, Kartu, KlipGuru, Subjudul, Tombol, VideoKosong, toast, type KlipRef } from '../components'
import { klipHuruf } from './belajar'

const MAKS_DETIK = 8

/** Format yang didukung perangkat: WebM/Opus (Chrome, Android, Safari 18.4+), lalu MP4/AAC (iOS lama). */
function pilihMime() {
  if (typeof MediaRecorder === 'undefined') return null
  return ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4'].find((m) => MediaRecorder.isTypeSupported(m)) ?? ''
}

/** Puncak amplitudo untuk gelombang; juga mengukur durasi (WebM dari Chrome tidak membawa durasi). */
async function analisis(blob: Blob, n = 64): Promise<{ puncak: number[]; durasi: number }> {
  try {
    const ctx = new AudioContext()
    const buf = await ctx.decodeAudioData(await blob.arrayBuffer())
    ctx.close()
    const data = buf.getChannelData(0)
    const step = Math.max(1, Math.floor(data.length / n))
    const puncak = Array.from({ length: n }, (_, i) => {
      let m = 0
      for (let j = i * step; j < Math.min(data.length, (i + 1) * step); j++) m = Math.max(m, Math.abs(data[j]))
      return m
    })
    const max = Math.max(...puncak, 0.01)
    return { puncak: puncak.map((p) => p / max), durasi: buf.duration }
  } catch {
    return { puncak: [], durasi: 0 }
  }
}

function Gelombang({ puncak, warna = 'var(--color-tint)' }: { puncak: number[]; warna?: string }) {
  if (!puncak.length) return <div className="h-12 rounded-xl bg-sand" />
  return (
    <svg viewBox={`0 0 ${puncak.length * 4} 48`} className="h-12 w-full" preserveAspectRatio="none" aria-hidden>
      {puncak.map((p, i) => {
        const h = Math.max(2, p * 44)
        return <rect key={i} x={i * 4 + 0.5} y={24 - h / 2} width={3} height={h} rx={1.5} fill={warna} />
      })}
    </svg>
  )
}

// ---------- Cermin kamera depan (hanya pratinjau, tidak direkam/diunggah) ----------
function Cermin() {
  const [nyala, setNyala] = useState(false)
  const [galat, setGalat] = useState<string | null>(null)
  const video = useRef<HTMLVideoElement>(null)
  useEffect(() => {
    if (!nyala) return
    let stream: MediaStream | null = null
    navigator.mediaDevices
      .getUserMedia({ video: { facingMode: 'user', width: { ideal: 480 }, height: { ideal: 360 }, frameRate: { ideal: 15 } }, audio: false })
      .then((s) => { stream = s; if (video.current) video.current.srcObject = s })
      .catch(() => { setGalat('Kamera tidak dapat dibuka. Izinkan akses kamera di pengaturan peramban, atau berlatih dengan cermin biasa.'); setNyala(false) })
    return () => stream?.getTracks().forEach((t) => t.stop())
  }, [nyala])
  return (
    <div>
      {nyala ? (
        <div className="relative overflow-hidden rounded-2xl bg-black">
          <video ref={video} autoPlay playsInline muted className="aspect-[4/3] w-full -scale-x-100 object-cover" aria-label="Cermin kamera depan" />
          <span className="absolute top-2 left-2 rounded-full bg-black/55 px-2.5 py-1 text-xs text-white">Cermin · tidak direkam</span>
        </div>
      ) : (
        <button onClick={() => { setGalat(null); setNyala(true) }} className="flex min-h-24 w-full flex-col items-center justify-center gap-1 rounded-2xl border border-dashed border-border bg-sand text-sm font-semibold text-grey hover:border-tint hover:text-ink">
          <Ikon n="camera" className="size-6" /> Nyalakan cermin kamera untuk melihat gerak bibir
        </button>
      )}
      {nyala && <Tombol varian="teks" onClick={() => setNyala(false)} className="mt-1">Matikan cermin</Tombol>}
      {galat && <p className="mt-2 text-sm text-danger" role="alert">{galat}</p>}
    </div>
  )
}

// ---------- Perekam ----------
function Perekam({ h, onBaru }: { h: Huruf; onBaru: () => void }) {
  const [status, setStatus] = useState<'siap' | 'rekam' | 'olah'>('siap')
  const [detik, setDetik] = useState(0)
  const [level, setLevel] = useState(0)
  const [galat, setGalat] = useState<string | null>(null)
  const rec = useRef<MediaRecorder | null>(null)
  const { catat } = useApp()
  const mime = pilihMime()

  const mulai = async () => {
    setGalat(null)
    if (!window.isSecureContext) return setGalat('Perekaman butuh koneksi aman (HTTPS atau localhost).')
    if (mime === null) return setGalat('Peramban ini belum mendukung perekaman suara. Coba Chrome terbaru.')
    let stream: MediaStream
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true } })
    } catch {
      return setGalat('Mikrofon tidak diizinkan. Buka pengaturan situs/aplikasi, izinkan mikrofon, lalu coba lagi.')
    }
    const ctx = new AudioContext()
    const an = ctx.createAnalyser()
    an.fftSize = 512
    ctx.createMediaStreamSource(stream).connect(an)
    const buf = new Uint8Array(an.fftSize)
    let raf = 0
    const ukur = () => {
      an.getByteTimeDomainData(buf)
      let m = 0
      for (const v of buf) m = Math.max(m, Math.abs(v - 128))
      setLevel(m / 128)
      raf = requestAnimationFrame(ukur)
    }
    ukur()

    const chunks: Blob[] = []
    const r = new MediaRecorder(stream, mime ? { mimeType: mime, audioBitsPerSecond: 64000 } : undefined)
    rec.current = r
    const t0 = Date.now()
    const tik = window.setInterval(() => {
      const s = (Date.now() - t0) / 1000
      setDetik(s)
      if (s >= MAKS_DETIK) r.state === 'recording' && r.stop()
    }, 100)
    r.ondataavailable = (e) => e.data.size && chunks.push(e.data)
    r.onstop = async () => {
      clearInterval(tik)
      cancelAnimationFrame(raf)
      ctx.close()
      stream.getTracks().forEach((t) => t.stop())
      setStatus('olah')
      const blob = new Blob(chunks, { type: r.mimeType || mime || 'audio/webm' })
      const { durasi } = await analisis(blob, 8)
      await rekaman.simpan({ id: crypto.randomUUID(), huruf: h.id, blob, mime: blob.type, t: new Date().toISOString(), durasi: durasi || (Date.now() - t0) / 1000 })
      catat('rekam', h.id, `${durasi.toFixed(1)}s`)
      setStatus('siap')
      setLevel(0)
      onBaru()
    }
    r.start()
    setStatus('rekam')
  }

  useEffect(() => () => { if (rec.current?.state === 'recording') rec.current.stop() }, [])

  return (
    <div className="text-center">
      <button onClick={status === 'rekam' ? () => rec.current?.stop() : mulai} disabled={status === 'olah'}
        aria-label={status === 'rekam' ? 'Berhenti merekam' : 'Mulai merekam'}
        className={`relative mx-auto grid size-24 place-items-center rounded-full text-white sm:size-28 ${status === 'rekam' ? 'bg-danger' : 'bg-teal shadow-teal hover:brightness-110'}`}>
        {status === 'rekam' && <span className="absolute inset-0 rounded-full border-4 border-danger/40" style={{ transform: `scale(${1 + level * 0.5})` }} />}
        <Ikon n={status === 'rekam' ? 'stop' : 'mic'} className="size-10" />
      </button>
      <p className="mt-3 font-semibold" aria-live="polite">
        {status === 'rekam' ? `Merekam… ${detik.toFixed(1)} / ${MAKS_DETIK} detik` : status === 'olah' ? 'Menyimpan…' : 'Ketuk untuk merekam'}
      </p>
      {galat && <p className="mt-2 text-sm text-danger" role="alert">{galat}</p>}
      <p className="mt-1 text-xs text-grey">Rekaman hanya disimpan di perangkat ini.</p>
    </div>
  )
}

// ---------- Daftar rekaman + pembanding ----------
function useRekaman(id: string) {
  const [list, setList] = useState<(Rekaman & { puncak: number[] })[]>([])
  const muat = useCallback(async () => {
    const xs = (await rekaman.milik(id).catch(() => [])).sort((a, b) => b.t.localeCompare(a.t))
    setList(await Promise.all(xs.map(async (r) => ({ ...r, puncak: (await analisis(r.blob)).puncak }))))
  }, [id])
  useEffect(() => { muat() }, [muat])
  return { list, muat }
}

function Putar({ r }: { r: Rekaman & { puncak: number[] } }) {
  const [main, setMain] = useState(false)
  const audio = useRef<HTMLAudioElement | null>(null)
  useEffect(() => () => { audio.current?.pause(); if (audio.current) URL.revokeObjectURL(audio.current.src) }, [])
  const toggle = () => {
    if (main) { audio.current?.pause(); return }
    if (!audio.current) {
      audio.current = new Audio(URL.createObjectURL(r.blob))
      audio.current.onended = audio.current.onpause = () => setMain(false)
    }
    audio.current.currentTime = 0
    audio.current.play().then(() => setMain(true)).catch(() => toast('Rekaman tidak dapat diputar di perangkat ini.'))
  }
  return (
    <button onClick={toggle} aria-label={main ? 'Hentikan rekaman' : 'Putar rekaman saya'}
      className={`grid size-12 shrink-0 place-items-center rounded-full ${main ? 'bg-gold-mid text-on-gold' : 'bg-teal text-white shadow-teal'}`}>
      <Ikon n={main ? 'stop' : 'play'} />
    </button>
  )
}

function daftarCek(h: Huruf): string[] {
  if (h.pelajaran?.cek) return h.pelajaran.cek
  const t = titikById(h.titik)
  return [
    `Bunyi keluar dari ${t.nama.toLowerCase()}: ${t.deskripsi.charAt(0).toLowerCase()}${t.deskripsi.slice(1)}`,
    ...sifatHuruf(h).filter((s) => s.tonjol).map((s) => `${s.nama}: ${s.arti}`),
    'Bacaan saya terdengar mirip contoh guru',
  ]
}

export function Latihan({ h, mode }: { h: Huruf; mode: 'tiru' | 'bandingkan' }) {
  const { list, muat } = useRekaman(h.id)
  const { cek, setCek, pengaturan, dikuasai, tandai, catat } = useApp()
  const klip = klipHuruf(h, pengaturan.sumberVideo)
  const klipRef = useRef<KlipRef>(null)
  const items = daftarCek(h)
  const tercentang = cek[h.id] ?? []
  const sudah = dikuasai.includes(h.id)
  const latihan = harakatHuruf(h)

  if (mode === 'tiru') return (
    <div className="grid gap-4 xl:grid-cols-2 xl:items-start xl:gap-6">
      <div className="space-y-4">
        <Kartu>
          <Subjudul>Tirukan bacaan ini</Subjudul>
          <div dir="rtl" className="mb-3 grid grid-cols-4 gap-2">
            {latihan.map((x) => <span key={x.teks} className="grid min-h-20 place-items-center rounded-2xl bg-sand"><Arab className="text-5xl leading-tight">{x.teks}</Arab></span>)}
          </div>
          <p className="text-center text-sm text-grey">{latihan.map((x) => x.label).join(' · ')}</p>
        </Kartu>
        <Kartu className="py-8"><Perekam h={h} onBaru={muat} /></Kartu>
        {list.length > 0 && <p className="text-center text-sm text-grey">{list.length} rekaman tersimpan. Lanjut ke langkah Bandingkan.</p>}
      </div>
      <Kartu className="!p-4 sm:!p-5"><Subjudul>Cermin</Subjudul><Cermin /></Kartu>
    </div>
  )

  return (
    <div className="grid gap-4 xl:grid-cols-2 xl:items-start xl:gap-6">
      <div className="space-y-4">
      <Kartu className="!p-4 sm:!p-5">
        <Subjudul>Contoh guru</Subjudul>
        {klip ? <KlipGuru ref={klipRef} videoId={klip.id} judul={`Pelafalan huruf ${h.nama}`} /> : <VideoKosong huruf={h.huruf} />}
      </Kartu>
      <Kartu>
        <Subjudul>Rekaman saya</Subjudul>
        {list.length === 0 ? (
          <p className="text-sm text-grey">Belum ada rekaman. Kembali ke langkah Tiru untuk merekam.</p>
        ) : (
          <ul className="space-y-3">
            {list.slice(0, 5).map((r, i) => (
              <li key={r.id} className="flex items-center gap-3">
                <Putar r={r} />
                <div className="min-w-0 flex-1">
                  <Gelombang puncak={r.puncak} warna={i === 0 ? 'var(--color-tint)' : 'var(--color-border)'} />
                  <p className="text-xs text-grey">{new Date(r.t).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })} · {r.durasi.toFixed(1)} detik</p>
                </div>
                <button onClick={async () => { await rekaman.hapus(r.id); muat() }} aria-label="Hapus rekaman" className="grid size-11 place-items-center rounded-full text-grey hover:bg-danger-light hover:text-danger"><Ikon n="trash" /></button>
              </li>
            ))}
          </ul>
        )}
        <p className="mt-3 text-xs leading-relaxed text-grey">Putar contoh guru, lalu rekaman Anda, bergantian. Gelombang hanya menunjukkan keras-pelan suara; ia bukan penilaian benar-salah.</p>
      </Kartu>
      </div>
      <div className="space-y-4">
      <Kartu>
        <Subjudul>Daftar cek mandiri</Subjudul>
        <ul className="space-y-2">
          {items.map((it, i) => {
            const on = tercentang.includes(i)
            return (
              <li key={i}>
                <label className={`flex min-h-12 cursor-pointer items-start gap-3 rounded-2xl border p-3 ${on ? 'border-teal bg-teal-light' : 'border-line bg-surface hover:border-tint'}`}>
                  <input type="checkbox" checked={on} className="mt-0.5 size-5 accent-teal"
                    onChange={() => { setCek(h.id, on ? tercentang.filter((x) => x !== i) : [...tercentang, i]); catat('cek', h.id, String(i)) }} />
                  <span className="text-sm leading-relaxed">{it}</span>
                </label>
              </li>
            )
          })}
        </ul>
        <Tombol varian={sudah ? 'garis' : 'utama'} ikon="check" className="mt-4 w-full" onClick={() => tandai(h.id, !sudah)}>
          {sudah ? 'Sudah dikuasai · ketuk untuk membatalkan' : 'Tandai sudah dikuasai'}
        </Tombol>
        {tercentang.length < items.length && !sudah && <p className="mt-2 text-center text-xs text-grey">Saran: centang semua butir dulu sebelum menandai dikuasai.</p>}
      </Kartu>
      <Catatan nada="teal">Masih ragu? Bawa rekaman ini ke guru Anda. Fitur setor bacaan ke pengajar dirancang untuk Tahap 2.</Catatan>
      </div>
    </div>
  )
}

/** Rute /latihan/:id: tiru dan bandingkan dalam satu layar. */
export function LayarLatihan() {
  const { id = 'ba' } = useParams()
  const h = hurufById(id)
  if (!h) return <Halaman judul="Tidak ditemukan">Huruf tidak ada.</Halaman>
  return (
    <Halaman judul={`Latihan huruf ${h.nama}`} lebar="lebar">
      <Latihan h={h} mode="tiru" />
      <div className="h-6" />
      <Latihan h={h} mode="bandingkan" />
    </Halaman>
  )
}
