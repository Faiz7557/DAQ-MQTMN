"""Rekam layar purwarupa React sebagai B-roll video karya (lihat naskah-video.md).

Prasyarat: `npm run build && npm run preview` di ../web (http://127.0.0.1:8078), lalu
    pip install playwright   (Edge sudah terpasang; tidak perlu `playwright install`)
    python rekam_layar.py          (semua adegan; `python rekam_layar.py 04` hanya adegan 04)
Hasil: rekaman/01_beranda_peta.webm ... 05_uji_coba.webm, 780x1688 (tampilan ponsel 390x844 diperbesar 2x).
Mikrofon dan kamera memakai perangkat palsu Chromium (nada uji dan pola gambar), jadi adegan
cermin kamera sebaiknya direkam ulang dari ponsel tim.
"""
import json
import re
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8078/#"
OUT = Path(__file__).resolve().parent / "rekaman"
# Playwright merekam pada ukuran viewport (tanpa device scale), jadi tampilan 390 px CSS diperbesar dengan
# CSS zoom 2 di viewport 780x1688. Efek samping: grid ubin beranda memakai 6 kolom (breakpoint sm).
VIEW = {"width": 780, "height": 1688}
hari = [(date.today() - timedelta(days=i)).isoformat() for i in (6, 4, 3, 1, 0)]
STATE = {
    "state": {
        "dikuasai": ["ba", "ha", "mim"], "hariAktif": hari, "terakhirSurah": 1, "cek": {}, "events": [],
        "tes": [], "sus": [],
        "pengaturan": {"onboarding": True, "tampilkanHari": True, "skalaTeks": 1, "sumberVideo": "andalasy", "studi": None},
    },
    "version": 0,
}


def coba(aksi):
    """Satu langkah demo; kalau elemen tidak ada, rekaman tetap lanjut."""
    try:
        aksi()
    except Exception as e:  # noqa: BLE001 - B-roll, bukan tes
        print("   lewati:", str(e).splitlines()[0][:90])


def gulir(page, dy, kali=1, jeda=900):
    for _ in range(kali):
        page.mouse.wheel(0, dy * 2)
        page.wait_for_timeout(jeda)


def tombol(page, pola):
    return page.get_by_role("button", name=re.compile(pola, re.I)).first


def adegan_beranda_peta(page):
    page.goto(BASE + "/")
    page.wait_for_timeout(3000)
    gulir(page, 350, 3)
    gulir(page, -1200)
    page.wait_for_timeout(800)
    coba(lambda: page.get_by_role("link", name=re.compile("^Peta", re.I)).first.click(timeout=3000))
    page.wait_for_timeout(2500)
    for area in ("Al-Halq", "Al-Lisan", "Asy-Syafatain", "Al-Halq"):
        coba(lambda a=area: tombol(page, a).click(timeout=3000))
        page.wait_for_timeout(1600)
    coba(lambda: tombol(page, "wasath").click(timeout=3000))
    page.wait_for_timeout(2000)
    gulir(page, 400, 2)


def adegan_pelajaran(page):
    page.goto(BASE + "/huruf/haa")
    page.wait_for_timeout(3000)
    gulir(page, 350, 3)
    gulir(page, -1200)
    coba(lambda: tombol(page, "Lanjut: Dengar").click(timeout=3000))
    page.wait_for_timeout(5000)  # pemutar YouTube dimuat
    coba(lambda: page.locator('[aria-label*=", dengar "]').first.click(timeout=3000))
    page.wait_for_timeout(4000)
    coba(lambda: tombol(page, "Lanjut: Tiru").click(timeout=3000))
    page.wait_for_timeout(2500)
    coba(lambda: tombol(page, "rekam").click(timeout=3000))
    page.wait_for_timeout(3000)
    coba(lambda: tombol(page, "berhenti").click(timeout=3000))
    page.wait_for_timeout(1500)
    gulir(page, 400, 2)
    coba(lambda: tombol(page, "Lanjut: Bandingkan").click(timeout=3000))
    page.wait_for_timeout(2500)
    gulir(page, 350, 2)
    for k in range(3):
        coba(lambda k=k: page.get_by_role("checkbox").nth(k).click(timeout=2000))
        page.wait_for_timeout(600)
    gulir(page, 400, 2)
    coba(lambda: tombol(page, "Lanjut: Terapkan").click(timeout=3000))
    page.wait_for_timeout(3000)
    gulir(page, 350, 3)


def adegan_mirip(page):
    page.goto(BASE + "/mirip/0")
    page.wait_for_timeout(3000)
    gulir(page, 350, 4)
    # Jawab tiga soal kuis pertama dengan opsi pertama yang masih bisa dipilih.
    for _ in range(3):
        coba(lambda: page.locator("button.min-h-14:not([disabled])").first.click(timeout=2000))
        page.wait_for_timeout(1500)
        gulir(page, 250)


def adegan_mushaf(page):
    page.goto(BASE + "/mushaf/1")
    page.wait_for_timeout(3000)
    coba(lambda: page.locator('button[aria-label^="Sorot huruf"]', has_text="ح").first.click(timeout=3000))
    page.wait_for_timeout(2000)
    coba(lambda: tombol(page, "Terjemahan").click(timeout=3000))
    page.wait_for_timeout(1800)
    gulir(page, 350, 3)
    coba(lambda: tombol(page, "Terjemahan").click(timeout=3000))
    page.wait_for_timeout(1500)


def adegan_uji_coba(page):
    page.goto(BASE + "/saya/studi")
    page.wait_for_timeout(2500)
    gulir(page, 300)
    coba(lambda: page.get_by_role("textbox").first.fill("P07", timeout=3000))
    page.wait_for_timeout(800)
    for k in range(2):
        coba(lambda k=k: page.get_by_role("checkbox").nth(k).check(timeout=2000))
        page.wait_for_timeout(700)
    coba(lambda: tombol(page, "Ikut uji coba").click(timeout=3000))
    page.wait_for_timeout(2500)
    coba(lambda: page.get_by_role("link", name=re.compile("Tes sebelum", re.I)).click(timeout=3000))
    page.wait_for_timeout(2500)
    for _ in range(3):
        coba(lambda: page.locator("main button:not([disabled])").nth(1).click(timeout=2000))
        page.wait_for_timeout(1200)
        coba(lambda: tombol(page, "Berikutnya").click(timeout=2000))
        page.wait_for_timeout(1200)


ADEGAN = [("01_beranda_peta", adegan_beranda_peta), ("02_pelajaran_ha", adegan_pelajaran),
          ("03_huruf_mirip", adegan_mirip), ("04_mushaf", adegan_mushaf), ("05_uji_coba", adegan_uji_coba)]


def main():
    OUT.mkdir(exist_ok=True)
    tmp = OUT / "_tmp"
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", args=["--use-fake-ui-for-media-stream", "--use-fake-device-for-media-stream"])
        for nama, adegan in ADEGAN:
            if sys.argv[1:] and not any(nama.startswith(a) for a in sys.argv[1:]):  # mis. python rekam_layar.py 04
                continue
            ctx = b.new_context(viewport=VIEW, service_workers="block", permissions=["microphone", "camera"],
                                record_video_dir=str(tmp), record_video_size=VIEW)
            ctx.add_init_script("document.addEventListener('DOMContentLoaded', () => { document.documentElement.style.zoom = '2' })")
            # Isi state demo sekali per konteks; navigasi berikutnya memakai progres yang sedang berjalan.
            ctx.add_init_script(f"if (!sessionStorage.getItem('seed')) {{ localStorage.setItem('makhraj-v1', "
                                f"{json.dumps(json.dumps(STATE))}); sessionStorage.setItem('seed', '1') }}")
            page = ctx.new_page()
            print(nama)
            adegan(page)
            page.wait_for_timeout(1200)
            video = page.video
            ctx.close()
            shutil.move(video.path(), OUT / f"{nama}.webm")
        b.close()
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
