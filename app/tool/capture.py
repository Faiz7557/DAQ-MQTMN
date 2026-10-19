"""Tangkap layar aplikasi web untuk proposal (780 x 1688 px = 390 x 844 @2x).

Prasyarat: `flutter build web --release --no-web-resources-cdn`, lalu server statis
melayani app/build/web di http://localhost:8077 (lihat .claude/launch.json).

Pakai:  python tool/capture.py [--out ../paper/script/screens/png] [nama ...]
Hasil memakai mode demo (?demo=1): 3 huruf dikuasai, 5 hari beruntun.
"""
import argparse
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
BASE = "http://localhost:8077/?demo=1&frame=390x844#"
SCREENS = {
    "Main": "/",
    "Peta": "/peta",
    "Pelajaran": "/huruf/ba",
    "Latihan": "/latihan/ba",
    "Mirip": "/mirip/0",
    "Mushaf": "/mushaf/1?huruf=ba",
}
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE.parent.parent / "paper" / "script" / "screens" / "png"))
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    browser = next(b for b in BROWSERS if Path(b).exists())
    for name, route in SCREENS.items():
        if a.names and name not in a.names:
            continue
        target = out / f"{name}.png"
        subprocess.run(
            [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
             "--force-device-scale-factor=2", "--window-size=800,900", "--virtual-time-budget=20000",
             f"--user-data-dir={HERE / '.capture-profile'}", f"--screenshot={target}", BASE + route],
            check=True, capture_output=True, timeout=180,
        )
        Image.open(target).crop((0, 0, 780, 1688)).save(target)
        print(f"{name}: {target}")


if __name__ == "__main__":
    main()
