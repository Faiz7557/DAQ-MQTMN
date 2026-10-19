"""Render 6 layar mockup (.dc.html) menjadi PNG lewat browser headless.

Hasil: screens/png/<Nama>.png (skala 2x). Dipanggil oleh build.py hanya kalau
PNG belum ada atau sumbernya lebih baru, karena butuh koneksi internet untuk font.
Ganti PNG di screens/png/ dengan screenshot MVP asli kalau aplikasinya sudah jadi.
"""
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
PNG = HERE / "png"

# Tinggi tiap artboard, sesuai kanvas mockup.
SCREENS = {
    "Main": 844,
    "Peta": 980,
    "Pelajaran": 1320,
    "Latihan": 1000,
    "Mirip": 1000,
    "Mushaf": 844,
}

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def find_browser():
    for b in BROWSERS:
        if Path(b).exists():
            return b
    raise SystemExit("Browser headless (Edge/Chrome) tidak ditemukan.")


def needs_render():
    for name in SCREENS:
        png = PNG / f"{name}.png"
        src = SRC / f"{name}.dc.html"
        if not png.exists() or png.stat().st_mtime < src.stat().st_mtime:
            return True
    return False


def render(force=False):
    if not force and not needs_render():
        return
    PNG.mkdir(exist_ok=True)
    shutil.copy(HERE / "support.js", SRC / "support.js")
    browser = find_browser()
    for name, height in SCREENS.items():
        out = PNG / f"{name}.png"
        url = (SRC / f"{name}.dc.html").as_uri()
        subprocess.run(
            [
                browser,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--allow-file-access-from-files",
                "--force-device-scale-factor=2",
                f"--window-size=390,{height}",
                "--virtual-time-budget=10000",
                f"--screenshot={out}",
                url,
            ],
            check=True,
            capture_output=True,
            timeout=120,
        )
        print(f"  layar {name} -> {out.name}")


if __name__ == "__main__":
    render(force=True)
