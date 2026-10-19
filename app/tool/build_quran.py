"""Ubah teks Tanzil menjadi aset JSON yang ringkas untuk aplikasi.

Masukan (folder ini):  quran-uthmani.txt, id.indonesian.txt, quran-data.xml
Keluaran (assets/quran/): quran.json, id.json, TANZIL_LICENSE.txt

Teks Al-Qur'an TIDAK diubah (syarat lisensi Tanzil). Satu-satunya perlakuan:
basmalah yang Tanzil sisipkan di awal ayat 1 setiap surah (kecuali Al-Fatihah dan
At-Taubah) dipisahkan ke tanda `basmalah: true`, lalu aplikasi menampilkannya
sebagai baris sendiri, persis seperti di mushaf cetak.

Jalankan:  python tool/build_quran.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets" / "quran"


def read_tanzil(path):
    header, rows = [], {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        if line.startswith("#"):
            header.append(line)
            continue
        s, a, text = line.split("|", 2)
        rows.setdefault(int(s), []).append(text)
    return header, rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    header, quran = read_tanzil(HERE / "quran-uthmani.txt")
    t_header, trans = read_tanzil(HERE / "id.indonesian.txt")
    meta = {}
    xml = (HERE / "quran-data.xml").read_text(encoding="utf-8")
    for m in re.finditer(r'<sura index="(\d+)" ayas="(\d+)"[^>]*name="([^"]+)" tname="([^"]+)" ename="([^"]+)" type="(\w+)"', xml):
        meta[int(m.group(1))] = dict(name=m.group(3), tname=m.group(4), ename=m.group(5), type=m.group(6))

    basmalah = quran[1][0]
    prefix = basmalah + " "
    suras = []
    for n in range(1, 115):
        ayahs = list(quran[n])
        has_b = False
        if n not in (1, 9) and ayahs[0].startswith(prefix):
            ayahs[0] = ayahs[0][len(prefix):]
            has_b = True
        suras.append({"n": n, **meta[n], "basmalah": has_b, "ayahs": ayahs})
        assert len(trans[n]) == len(ayahs), n
    (OUT / "quran.json").write_text(json.dumps({"basmalah": basmalah, "suras": suras}, ensure_ascii=False), encoding="utf-8")
    (OUT / "id.json").write_text(json.dumps([trans[n] for n in range(1, 115)], ensure_ascii=False), encoding="utf-8")
    (OUT / "TANZIL_LICENSE.txt").write_text(
        "TEKS AL-QUR'AN\n" + "\n".join(header) + "\n\nTERJEMAHAN INDONESIA (Kementerian Agama RI, via Tanzil)\n"
        + "\n".join(t_header) + "\n", encoding="utf-8")
    stripped = sum(1 for s in suras if s["basmalah"])
    print(f"114 surah, {sum(len(s['ayahs']) for s in suras)} ayat, basmalah dipisah di {stripped} surah")


if __name__ == "__main__":
    main()
