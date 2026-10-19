"""Pemeriksaan otomatis sebelum build. Gagal = build berhenti."""
import re
from pathlib import Path

from content import BODY, COVER, LAMPIRAN
from references import REFERENCES, REFERENCES_LAMPIRAN

HERE = Path(__file__).resolve().parent
EM_DASH = "—"


def _texts():
    out = []
    for v in COVER.values():
        out.extend(v if isinstance(v, list) else [v])
    for b in BODY + LAMPIRAN:
        kind = b[0]
        if kind in ("h1", "h2", "p", "p0"):
            out.append(b[1])
        elif kind == "list":
            out.extend(b[1])
        elif kind == "fig":
            out.append(b[3])
        elif kind == "table":
            out.append(b[2])
            out.extend(b[3])
            for row in b[4]:
                out.extend(row)
    out.extend(r[2] for r in REFERENCES + REFERENCES_LAMPIRAN)
    return out


CITE = r"\(([A-Z][\w.\- ]+?)(?: dkk\.| & [\w]+| dan [\w]+)?, (\d{4}|t\.t\.)\)"


def _cites(text, refs):
    """Kutipan (Nama, tahun) di text yang tidak punya entri di refs."""
    return [(n, y) for n, y in re.findall(CITE, text)
            if not any((n.startswith(a) or a.startswith(n)) and y == yr.split("-")[0] for a, yr, _ in refs)]


def run():
    errors = []
    texts = _texts()
    for t in texts:
        if EM_DASH in t:
            errors.append(f"em dash ditemukan: ...{t[max(0, t.index(EM_DASH) - 30):t.index(EM_DASH) + 10]}...")

    figs = {b[1]: b[2] for b in BODY + LAMPIRAN if b[0] == "fig"}
    tabs = {b[1] for b in BODY + LAMPIRAN if b[0] == "table"}
    for key, fname in figs.items():
        if not (HERE / "figures" / fname).exists():
            errors.append(f"gambar hilang: figures/{fname}")
    body_text = " ".join(texts[: len(texts) - len(REFERENCES) - len(REFERENCES_LAMPIRAN)])
    for kind, key in re.findall(r"\{(fig|tab):([a-z_]+)\}", body_text):
        if (kind == "fig" and key not in figs) or (kind == "tab" and key not in tabs):
            errors.append(f"rujukan silang tidak dikenal: {{{kind}:{key}}}")
    for key in figs:
        if "{fig:" + key + "}" not in body_text:
            errors.append(f"Gambar '{key}' tidak dirujuk di teks")
    for key in tabs:
        if "{tab:" + key + "}" not in body_text:
            errors.append(f"Tabel '{key}' tidak dirujuk di teks")

    # Setiap pustaka harus dikutip, dan setiap kutipan (Nama, tahun) harus punya entri.
    # Badan hanya boleh mengutip Daftar Pustaka; lampiran boleh juga mengutip Rujukan Lampiran.
    def blok_teks(blocks):
        out = []
        for b in blocks:
            if b[0] in ("h1", "h2", "p", "p0"):
                out.append(b[1])
            elif b[0] == "list":
                out.extend(b[1])
            elif b[0] == "fig":
                out.append(b[3])
            elif b[0] == "table":
                out.append(b[2])
                out.extend(b[3])
                out.extend(c for row in b[4] for c in row)
        return " ".join(out)

    badan, lampiran = blok_teks(BODY), blok_teks(LAMPIRAN)
    for author, year, _ in REFERENCES:
        if author not in body_text or year not in body_text:
            errors.append(f"pustaka tidak dikutip di teks: {author} ({year})")
    for author, year, _ in REFERENCES_LAMPIRAN:
        if author not in lampiran or year not in lampiran:
            errors.append(f"rujukan lampiran tidak dikutip di lampiran: {author} ({year})")
    for n, y in _cites(badan, REFERENCES):
        errors.append(f"kutipan di badan tanpa entri Daftar Pustaka: ({n}, {y})")
    for n, y in _cites(lampiran, REFERENCES + REFERENCES_LAMPIRAN):
        errors.append(f"kutipan di lampiran tanpa entri: ({n}, {y})")

    # Miring di dalam tebal tidak didukung add_rich: tanda bintangnya akan tercetak.
    for t in texts:
        for tok in re.findall(r"\*\*.+?\*\*", t):  # sama dengan TOKEN di build.add_rich
            if "*" in tok[2:-2]:
                errors.append(f"miring bersarang di dalam tebal: {tok[:50]}")

    # Placeholder tidak menggagalkan build, tetapi harus diisi sebelum dikirim.
    holes = sorted(set(re.findall(r"\[(?:tautan|Nama|Nomor)[^\]]*\]", body_text)))
    if holes:
        print(f"  PERINGATAN: {len(holes)} placeholder belum diisi: {', '.join(holes)}")

    if errors:
        raise SystemExit("checks.py gagal:\n  - " + "\n  - ".join(errors))
    print("  checks: lolos")


if __name__ == "__main__":
    run()
