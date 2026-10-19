"""Semua gambar proposal, digambar dengan matplotlib supaya bisa diedit ulang.

Satu fungsi per gambar. Hasil PNG masuk ke script/figures/.
save() memeriksa tumpang-tindih antarteks; build gagal kalau ada label yang bertumpuk.
"""
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"
SCREENS = HERE / "screens" / "png"
FONTS = HERE.parents[1] / "app" / "assets" / "fonts"

# Font gambar = font aplikasi (Plus Jakarta Sans), supaya diagram senada dengan screenshot MVP.
for f in FONTS.glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))
SANS = "Plus Jakarta Sans"
ARAB = "Noto Naskh Arabic"

# Palet mengikuti purwarupa aplikasi.
TEAL = "#0F5E5E"      # warna merek: judul, aksen diagram
TEAL_M = "#9CC7C1"
TEAL_L = "#E3F1EE"
GOLD = "#B5760E"      # Tahap 2-3, arus uang
GOLD_D = "#7A520C"    # teks di atas latar emas muda
GOLD_L = "#F7EBD3"
INK = "#1C2333"       # teks utama
GREY = "#5A6070"      # teks sekunder
MUTED = "#8A93A3"
LINE = "#C9CED6"      # garis tepi kotak
HAIR = "#E4E7EB"      # garis bantu grafik
CREAM = "#FBF8F2"
# Seri grafik data (lolos validate_palette.js: chroma, CVD, kontras).
S_TEAL = "#008C7E"
S_GOLD = "#B5760E"

plt.rcParams.update(
    {
        "font.family": SANS,
        "font.size": 8,
        "axes.edgecolor": LINE,
        "axes.labelcolor": GREY,
        "xtick.color": GREY,
        "ytick.color": INK,
        "axes.linewidth": 0.6,
        "savefig.dpi": 300,
    }
)

CM = 1 / 2.54


class OverlapError(Exception):
    pass


def _check_overlap(fig, name):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    boxes = []
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text().strip():
            continue
        if getattr(t, "_allow_overlap", False):
            continue
        bb = t.get_window_extent(renderer).expanded(0.98, 0.95)
        boxes.append((t.get_text().replace("\n", " ")[:40], bb))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if boxes[i][1].overlaps(boxes[j][1]):
                raise OverlapError(f"{name}: teks '{boxes[i][0]}' menumpuk dengan '{boxes[j][0]}'")


def save(fig, name, check=True):
    OUT.mkdir(exist_ok=True)
    if check:
        _check_overlap(fig, name)
    path = OUT / f"{name}.png"
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03, facecolor="white")
    plt.close(fig)
    return path


def blank(w_cm, h_cm, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w_cm * CM, h_cm * CM), constrained_layout=False)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc="white", ec=INK, lw=1.0, ls="-", r=0.12, z=1):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
            fc=fc, ec=ec, lw=lw, ls=ls, zorder=z,
        )
    )


def arrow(ax, p1, p2, color=INK, ls="-", lw=1.0, style="-|>", ms=9, z=2, shrink=0):
    ax.add_patch(
        FancyArrowPatch(
            p1, p2, arrowstyle=style, mutation_scale=ms, color=color,
            lw=lw, ls=ls, zorder=z, shrinkA=shrink, shrinkB=shrink,
        )
    )


# ---------------------------------------------------------------- Gambar 1
def fig_literasi():
    """Tangga kemampuan baca Al-Qur'an, survei Kemenag & LK3P UI 2023."""
    labels = [
        "Mengenal huruf dan harakat",
        "Merangkai huruf menjadi kata",
        "Membaca ayat dengan lancar",
        "Membaca lancar sesuai tajwid",
    ]
    vals = [61.51, 59.92, 48.96, 44.57]
    # Digambar pada ukuran cetak (11,5 cm) supaya huruf tidak menyusut.
    fig, ax = plt.subplots(figsize=(11.5 * CM, 4.9 * CM))
    y = list(range(len(vals)))[::-1]
    # Penekanan: jenjang awal dan jenjang tajwid; dua jenjang tengah diredam.
    colors = [TEAL_M, "#D5E6E2", "#D5E6E2", TEAL]
    ax.barh(y, vals, color=colors, height=0.5, zorder=2)
    for yi, v in zip(y, vals):
        lab = f"{v:.2f}%".replace(".", ",")
        if yi == 0:  # nilai jenjang tajwid di dalam batang, karena ujungnya ditempati celah
            ax.text(v - 1.5, yi, lab, ha="right", va="center", fontsize=7.5, color="white", weight="semibold", zorder=3)
        else:
            ax.text(v + 1.5, yi, lab, va="center", fontsize=7.5, color=INK, weight="semibold")
    # Celah: bagian yang sudah mengenal huruf tetapi belum sesuai tajwid.
    ax.add_patch(Rectangle((44.57, -0.25), 61.51 - 44.57, 0.5, fc=GOLD_L, ec=GOLD, lw=0.8, ls=(0, (2, 1.5)), zorder=1))
    ax.text(63.5, -0.02, "celah 16,94 poin:\nkenal huruf, belum tajwid",
            va="center", fontsize=7.2, color=GOLD_D, linespacing=1.15)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.5)
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 20))
    ax.set_xticklabels([f"{v}%" for v in range(0, 101, 20)], fontsize=7)
    ax.set_xlabel("Persentase responden (n = 10.347)", fontsize=7.5)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", color=HAIR, lw=0.6, zorder=0)
    ax.set_ylim(-0.55, 3.45)
    fig.tight_layout()
    return save(fig, "fig01_literasi")


# ---------------------------------------------------------------- Gambar 2
def _badge(ax, x, y, n, fc=TEAL, r=0.27):
    ax.add_patch(Circle((x, y), r, fc=fc, ec="none", zorder=3))
    ax.text(x, y - 0.01, str(n), ha="center", va="center", fontsize=8, weight="bold", color="white", zorder=4)


def fig_alur_belajar():
    """Lima langkah talaqqi digital."""
    fig, ax = blank(15.5, 4.4, (0, 15.5), (0.05, 4.25))
    steps = [
        ("Lihat", "Peta makhraj dan\nanimasi 3 langkah"),
        ("Dengar", "Klip pelafalan\nSyaikh Aiman Suwaid"),
        ("Tiru", "Rekam suara dengan\nmode cermin kamera"),
        ("Bandingkan", "Putar bergantian,\nisi daftar periksa"),
        ("Terapkan", "Temukan huruf itu\ndi ayat (sorot huruf)"),
    ]
    w, h, gap, x0, y0 = 2.66, 1.9, 0.4, 0.1, 2.15
    for i, (t, d) in enumerate(steps):
        x = x0 + i * (w + gap)
        rbox(ax, x, y0, w, h, fc=TEAL_L if i in (0, 4) else "white", ec=TEAL if i in (0, 4) else LINE, lw=0.9, r=0.18)
        _badge(ax, x + 0.42, y0 + h - 0.42, i + 1)
        ax.text(x + 0.82, y0 + h - 0.43, t, ha="left", va="center", fontsize=8.6, weight="bold", color=TEAL)
        ax.text(x + w / 2, y0 + 0.62, d, ha="center", va="center", fontsize=6.9, color=INK, linespacing=1.2)
        if i < 4:
            arrow(ax, (x + w + 0.05, y0 + h / 2), (x + w + gap - 0.05, y0 + h / 2), color=TEAL, lw=1.1, ms=8)
    xa = x0 + w / 2
    xe = x0 + 4 * (w + gap) + w / 2
    ax.plot([xe, xe], [y0, 1.2], color=MUTED, lw=0.9)
    ax.plot([xe, xa], [1.2, 1.2], color=MUTED, lw=0.9)
    arrow(ax, (xa, 1.2), (xa, y0 - 0.02), color=MUTED, lw=0.9, ms=8)
    ax.text(5.0, 0.98, "ulangi untuk huruf berikutnya", ha="center", va="center", fontsize=6.8, color=GREY)
    x4 = x0 + 3 * (w + gap) + w / 2
    arrow(ax, (x4, y0), (x4, 0.58), color=GOLD, ls=(0, (3, 2)), lw=1.0, ms=8)
    rbox(ax, x4 - 1.75, 0.1, 3.5, 0.48, fc=GOLD_L, ec=GOLD, lw=0.8, r=0.12)
    ax.text(x4, 0.34, "Setor ke pengajar (Tahap 2)", ha="center", va="center", fontsize=6.8, color=GOLD_D, weight="semibold")
    return save(fig, "fig02_alur_belajar")


# ---------------------------------------------------------------- Gambar A (lampiran)
MUSLIM = 245_973_915  # Dukcapil, semester I 2024
P_BELUM_TAJWID = 1 - 0.4457
P_INTERNET = 0.8066


def market_numbers():
    tam = MUSLIM * P_BELUM_TAJWID
    sam = MUSLIM * P_BELUM_TAJWID * P_INTERNET
    som = 100_000
    return tam, sam, som


def fig_pasar():
    """(a) TAM-SAM-SOM, (b) peta posisi kompetitor."""
    tam, sam, som = market_numbers()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(15.5 * CM, 6.6 * CM), gridspec_kw={"width_ratios": [1.05, 1]})
    a1.set_xlim(0, 12)
    a1.set_ylim(-0.9, 7.4)
    a1.set_aspect("equal")
    a1.axis("off")
    cx = 3.6
    rings = [(3.5, TEAL_L), (2.45, TEAL_M), (0.95, TEAL)]
    for r, fc in rings:
        a1.add_patch(Circle((cx, r), r, fc=fc, ec="white", lw=1.5))
    fmt = lambda v: f"{v / 1e6:.1f} juta".replace(".", ",")
    rows = [
        ("TAM", fmt(tam), "Muslim belum lancar\nsesuai tajwid"),
        ("SAM", fmt(sam), "TAM yang terhubung\ninternet (80,66%)"),
        ("SOM", "100 ribu", "pengguna aktif bulanan\npada tahun ketiga"),
    ]
    for (k, v, d), (r, _) in zip(rows, rings):
        top = 2 * r - 0.25
        a1.plot([cx, 7.3], [top, top], color=MUTED, lw=0.6)
        a1.add_patch(Circle((cx, top), 0.1, fc=INK, ec="white", lw=0.8, zorder=3))
        a1.text(7.45, top + 0.1, f"{k}  {v}", ha="left", va="bottom", fontsize=8, weight="bold", color=INK)
        a1.text(7.45, top - 0.1, d, ha="left", va="top", fontsize=6.4, color=GREY, linespacing=1.15)
    a1.text(6.0, -0.8, "(a) Ukuran pasar (estimasi batas atas)", ha="center", fontsize=7.5, color=INK)
    # (b)
    a2.set_xlim(0, 10)
    a2.set_ylim(0, 10)
    a2.set_xticks([])
    a2.set_yticks([])
    for s in a2.spines.values():
        s.set_color(LINE)
    a2.axhline(5, color=HAIR, lw=0.8)
    a2.axvline(5, color=HAIR, lw=0.8)
    a2.set_xlabel("Kedalaman penjelasan makhraj", fontsize=7.2)
    a2.set_ylabel("Umpan balik otomatis", fontsize=7.2)
    a2.text(0.3, 9.7, "menilai bacaan,\nsedikit penjelasan", ha="left", va="top", fontsize=6, color=MUTED, linespacing=1.1)
    a2.text(9.7, 0.3, "menjelaskan,\nbelum menilai", ha="right", va="bottom", fontsize=6, color=MUTED, linespacing=1.1)
    pts = [
        ("Qur'an Kemenag", 1.5, 2.2, MUTED, "left"),
        ("Tarteel", 1.7, 7.4, MUTED, "left"),
        ("ngaji.ai", 3.4, 6.3, MUTED, "left"),
        ("Makhraj Tahap 1", 8.2, 3.2, TEAL, "right"),
        ("Makhraj Tahap 3", 8.4, 8.1, GOLD, "right"),
    ]
    arrow(a2, (8.25, 3.65), (8.38, 7.6), color=GOLD, ls=(0, (3, 2)), lw=1.0, ms=8)
    for name, x, y, c, ha in pts:
        a2.scatter([x], [y], s=55, color=c, edgecolors="white", linewidths=1.2, zorder=3)
        dx = 0.45 if ha == "left" else -0.45
        a2.text(x + dx, y, name, ha=ha, va="center", fontsize=6.9, color=INK,
                weight="bold" if "Makhraj" in name else "normal")
    a2.set_title("(b) Peta posisi (analisis penulis)", fontsize=7.5, y=-0.2, color=INK)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.14, wspace=0.08)
    return save(fig, "fig03_pasar")


# ---------------------------------------------------------------- Gambar 3 (halaman utama)
STAGES = [
    ("Tahap 1", "MVP dan validasi", "Tahun 1", TEAL, TEAL_L),
    ("Tahap 2", "Setor ke pengajar", "Tahun 2", "#2E7F79", "#EAF3F1"),
    ("Tahap 3", "Penilaian AI", "Tahun 3", GOLD, GOLD_L),
]
ROWS = [
    ("Produk", [
        "29 pelajaran huruf, peta\nmakhraj, rekam, mushaf",
        "setor rekaman ke pengajar,\ndasbor kelas lembaga",
        "skor makhraj per huruf\nberbasis AI, tajwid lanjutan"]),
    ("Pendapatan", [
        "belum ada; dana tim atau\nhibah Rp4,6 juta",
        "paket setoran Rp20.000\n(70% pengajar), lisensi kelas",
        "setoran dan lisensi;\nZISWAF untuk subsidi"]),
    ("Indikator", [
        "SUS minimal 68;\n29 huruf ditinjau guru",
        "300 penyetor aktif;\n10 kelas lembaga",
        "40 kelas lembaga;\nkas kumulatif positif"]),
]
MAU = ["5.000", "30.000", "100.000"]
NET = ["-4,6", "+0,2", "+6,4"]


def fig_roadmap():
    """Peta jalan tiga tahap sekaligus ringkasan model bisnis per tahap."""
    fig, ax = blank(15.5, 7.3, (0, 15.5), (0, 7.3))
    lx, cw, gap = 2.05, 4.3, 0.17
    xs = [lx + i * (cw + gap) for i in range(3)]
    top = 7.2
    for (tag, name, yr, fc, bg), x in zip(STAGES, xs):
        rbox(ax, x, 0.55, cw, top - 0.55, fc=bg, ec="none", r=0.18, z=0)
        rbox(ax, x, top - 0.85, cw, 0.85, fc=fc, ec="none", r=0.18, z=1)
        ax.add_patch(Rectangle((x, top - 0.85), cw, 0.3, fc=fc, ec="none", zorder=1))
        ax.text(x + 0.22, top - 0.25, f"{tag.upper()}  ·  {yr.upper()}", ha="left", va="center", fontsize=6, color="white", zorder=2)
        ax.text(x + 0.22, top - 0.6, name, ha="left", va="center", fontsize=8.6, weight="bold", color="white", zorder=2)
    ytop = top - 1.0
    ax.text(0.05, ytop - 0.55, "Pengguna aktif\nbulanan (target)", ha="left", va="center", fontsize=6.8, color=GREY, linespacing=1.1)
    for x, m in zip(xs, MAU):
        ax.text(x + 0.22, ytop - 0.55, m, ha="left", va="center", fontsize=13, weight="bold", color=INK)
    y = ytop - 1.15
    rh = 1.05
    for label, cells in ROWS:
        for x in xs:
            ax.plot([x + 0.22, x + cw - 0.22], [y, y], color="white", lw=1.4, zorder=1)
        ax.plot([0.05, lx - 0.15], [y, y], color=HAIR, lw=0.7)
        ax.text(0.05, y - rh / 2, label, ha="left", va="center", fontsize=7, weight="semibold", color=GREY)
        for x, c in zip(xs, cells):
            ax.text(x + 0.22, y - rh / 2, c, ha="left", va="center", fontsize=6.8, color=INK, linespacing=1.2)
        y -= rh
    for x in xs:
        ax.plot([x + 0.22, x + cw - 0.22], [y, y], color="white", lw=1.4, zorder=1)
    ax.plot([0.05, lx - 0.15], [y, y], color=HAIR, lw=0.7)
    ax.text(0.05, y - 0.4, "Selisih kas\n(juta rupiah)", ha="left", va="center", fontsize=6.8, color=GREY, linespacing=1.1)
    for x, n in zip(xs, NET):
        neg = n.startswith("-")
        ax.text(x + 0.22, y - 0.4, n, ha="left", va="center", fontsize=10, weight="bold", color="#9A3B2E" if neg else S_TEAL)
    ax.text(lx + (3 * cw + 2 * gap) / 2, 0.22, "Inti pembelajaran tetap gratis di semua tahap",
            ha="center", va="center", fontsize=7, color=TEAL, weight="semibold")
    return save(fig, "fig04_roadmap")


# ---------------------------------------------------------------- Gambar 5
def _actor(ax, x, y, label, sub=None, color=INK):
    ax.add_patch(Ellipse((x, y + 0.95), 0.36, 0.36, fc="white", ec=color, lw=1.1))
    ax.plot([x, x], [y + 0.77, y + 0.25], color=color, lw=1.1)
    ax.plot([x - 0.3, x + 0.3], [y + 0.6, y + 0.6], color=color, lw=1.1)
    ax.plot([x, x - 0.25], [y + 0.25, y - 0.15], color=color, lw=1.1)
    ax.plot([x, x + 0.25], [y + 0.25, y - 0.15], color=color, lw=1.1)
    ax.text(x, y - 0.45, label, ha="center", va="center", fontsize=8, weight="bold", color=color)
    if sub:
        ax.text(x, y - 0.82, sub, ha="center", va="center", fontsize=7, color=GREY)


def fig_usecase():
    fig, ax = blank(15.5, 8.5, (0, 16), (1.0, 9.7))
    rbox(ax, 2.5, 1.15, 11.0, 8.3, fc=CREAM, ec=INK, lw=1, r=0.2, z=0)
    ax.text(8.0, 9.12, "Sistem Makhraj", ha="center", fontsize=9, weight="bold")
    W, H = 3.85, 0.78
    c1, c2 = 4.75, 10.9
    rows = [8.15, 7.1, 6.05, 5.0, 3.95, 2.9, 1.85, 0.85]

    def uc(x, y, text, t2=False):
        ax.add_patch(Ellipse((x, y), W, H, fc=GOLD_L if t2 else "white",
                             ec=GOLD if t2 else TEAL, lw=1.1, ls=(0, (3, 2)) if t2 else "-", zorder=2))
        ax.text(x, y, text, ha="center", va="center", fontsize=6.9, zorder=3, linespacing=1.05)
        return (x, y)

    left = [
        uc(c1, rows[0], "Mengikuti uji coba\n(tes A/B dan SUS)"),
        uc(c1, rows[1], "Menjelajah peta makhraj"),
        uc(c1, rows[2], "Mempelajari huruf"),
        uc(c1, rows[3], "Merekam dan\nmembandingkan bacaan"),
        uc(c1, rows[4], "Berlatih huruf mirip"),
        uc(c1, rows[5], "Membaca mushaf\ndengan sorot huruf"),
        uc(c1, rows[6], "Melihat progres belajar"),
    ]
    klip = uc(c2 - 2.35, rows[2], "Memutar klip guru")
    setor = uc(c2 - 2.35, rows[3] - 1.05, "Menyetor rekaman\n(Tahap 2)", t2=True)
    koreksi = uc(c2, rows[5] - 0.3, "Memberi koreksi\n(Tahap 2)", t2=True)
    kelola = uc(c2, rows[0], "Mengelola materi\nhuruf dan klip")
    validasi = uc(c2, rows[1] - 0.05, "Memvalidasi materi")

    _actor(ax, 1.15, 4.4, "Pengguna", "(pemula)")
    _actor(ax, 14.9, 6.95, "Admin", "(kurator konten)")
    _actor(ax, 14.9, 2.6, "Pengajar", "tahsin")
    for (x, y) in left:
        ax.plot([1.45, x - W / 2], [5.15, y], color=INK, lw=0.7, zorder=1)
    for p in (kelola,):
        ax.plot([14.6, p[0] + W / 2], [7.6, p[1]], color=INK, lw=0.7, zorder=1)
    for p in (validasi, koreksi):
        ax.plot([14.6, p[0] + W / 2], [3.25, p[1]], color=INK, lw=0.7, zorder=1)
    # include / extend
    arrow(ax, (c1 + W / 2, rows[2]), (klip[0] - W / 2, klip[1]), color=GREY, ls=(0, (3, 2)), lw=0.9, style="->")
    t = ax.text((c1 + W / 2 + klip[0] - W / 2) / 2, rows[2] + 0.42, "«include»", ha="center", fontsize=6.8, color=GREY)
    arrow(ax, (setor[0] - W / 2 + 0.25, setor[1] + 0.2), (c1 + W / 2 - 0.1, rows[3] - 0.15), color=GREY, ls=(0, (3, 2)), lw=0.9, style="->")
    ax.text(setor[0] - 1.55, setor[1] + 0.62, "«extend»", ha="center", fontsize=6.8, color=GREY)
    arrow(ax, (setor[0] + W / 2, setor[1]), (koreksi[0] - W / 2 + 0.2, koreksi[1] + 0.15), color=GOLD, ls=(0, (3, 2)), lw=0.9, style="->")
    return save(fig, "fig05_usecase")


# ---------------------------------------------------------------- Gambar 6 & 7
def _class_box(ax, x, top, w, name, attrs, methods=None, t2=False, fs=6.6, lh=0.33):
    ec = GOLD if t2 else TEAL
    ls = (0, (3, 2)) if t2 else "-"
    head_h = 0.48
    a_h = lh * len(attrs) + 0.14
    m_h = (lh * len(methods) + 0.14) if methods is not None else 0
    h = head_h + a_h + m_h
    y = top - h
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=1, ls=ls, zorder=2))
    ax.add_patch(Rectangle((x, top - head_h), w, head_h, fc=GOLD_L if t2 else TEAL_L, ec=ec, lw=1, ls=ls, zorder=2))
    ax.text(x + w / 2, top - head_h / 2, name, ha="center", va="center", fontsize=fs + 0.6, weight="bold", zorder=3)
    for i, a in enumerate(attrs):
        ax.text(x + 0.1, top - head_h - 0.07 - lh * (i + 0.5), a, ha="left", va="center", fontsize=fs, zorder=3)
    if methods is not None:
        ym = top - head_h - a_h
        ax.plot([x, x + w], [ym, ym], color=ec, lw=0.8, ls=ls, zorder=3)
        for i, m in enumerate(methods):
            ax.text(x + 0.1, ym - 0.07 - lh * (i + 0.5), m, ha="left", va="center", fontsize=fs, zorder=3)
    return dict(x=x, y=y, w=w, h=h, top=top, cx=x + w / 2, cy=y + h / 2, right=x + w, bottom=y)


def _mult(ax, x, y, text, ha="center"):
    t = ax.text(x, y, text, ha=ha, va="center", fontsize=6.4, color=INK, zorder=4)
    return t


def fig_class():
    fig, ax = blank(15.5, 11.2, (0, 16), (0, 11.6))
    W = 3.45
    xs = [0.15, 4.2, 8.25, 12.3]
    tops = [11.45, 7.45, 3.55]
    b = {}
    b["area"] = _class_box(ax, xs[0], tops[0], W, "AreaMakhraj", ["- id: String", "- nama: String", "- letak: String"], ["+ daftarTitik()"])
    b["titik"] = _class_box(ax, xs[1], tops[0], W, "TitikMakhraj", ["- id: String", "- nama: String", "- koordinatSorot: Path"], ["+ sorot()"])
    b["huruf"] = _class_box(ax, xs[2], tops[0], W, "Huruf", ["- id: String", "- karakter: String", "- nama: String", "- urutan: int"], ["+ daftarSifat()", "+ contohKata()"])
    b["sifat"] = _class_box(ax, xs[3], tops[0], W, "Sifat", ["- id: String", "- nama: String", "- arti: String"], [])
    b["user"] = _class_box(ax, xs[0], tops[1], W, "Pengguna", ["- id: String", "- nama: String", "- email: String", "- peran: Peran"], ["+ masuk()", "+ lihatProgres()"])
    b["prog"] = _class_box(ax, xs[1], tops[1], W, "Progres", ["- status: Status", "- skorCekMandiri: int", "- diperbarui: DateTime"], ["+ perbarui()"])
    b["pel"] = _class_box(ax, xs[2], tops[1], W, "Pelajaran", ["- id: String", "- langkahAnimasi: List", "- kesalahanUmum: String"], ["+ mulai()"])
    b["mirip"] = _class_box(ax, xs[3], tops[1], W, "PasanganMirip", ["- id: String", "- contohKata: List"], ["+ mulaiKuis()"])
    b["rek"] = _class_box(ax, xs[0], tops[2], W, "Rekaman", ["- id: String", "- berkas: Blob", "- durasi: int", "- tanggal: DateTime"], ["+ rekam()", "+ putar()"])
    b["setor"] = _class_box(ax, xs[1], tops[2], W, "Setoran", ["- id: String", "- status: Status", "- tanggal: DateTime"], ["+ kirim()"], t2=True)
    b["kor"] = _class_box(ax, xs[2], tops[2], W, "Koreksi", ["- id: String", "- catatan: String", "- nilai: int"], ["+ beriCatatan()"], t2=True)
    b["klip"] = _class_box(ax, xs[3], tops[2], W, "KlipVideo", ["- youtubeId: String", "- detikMulai: int", "- detikSelesai: int", "- harakat: String"], ["+ putar()"])

    def hline(p, q, m1, m2, y=None):
        yy = y if y is not None else min(p["top"], q["top"]) - 0.75
        ax.plot([p["right"], q["x"]], [yy, yy], color=INK, lw=0.8, zorder=1)
        _mult(ax, p["right"] + 0.06, yy + 0.2, m1, ha="left")
        _mult(ax, q["x"] - 0.06, yy - 0.2, m2, ha="right")

    def vline(p, q, m1, m2, x):
        ax.plot([x, x], [p["bottom"], q["top"]], color=INK, lw=0.8, zorder=1)
        _mult(ax, x + 0.1, p["bottom"] - 0.2, m1, ha="left")
        _mult(ax, x + 0.1, q["top"] + 0.2, m2, ha="left")

    hline(b["area"], b["titik"], "1", "1..*")
    hline(b["titik"], b["huruf"], "1", "1..*")
    hline(b["huruf"], b["sifat"], "*", "*")
    hline(b["user"], b["prog"], "1", "0..*")
    hline(b["rek"], b["setor"], "1", "0..1")
    hline(b["setor"], b["kor"], "1", "0..1")
    vline(b["huruf"], b["pel"], "1", "1", b["huruf"]["cx"])
    vline(b["user"], b["rek"], "1", "0..*", b["user"]["cx"])
    # diagonal
    def dline(p1, p2, m1, m2, o1, o2):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=INK, lw=0.8, zorder=1)
        _mult(ax, p1[0] + o1[0], p1[1] + o1[1], m1)
        _mult(ax, p2[0] + o2[0], p2[1] + o2[1], m2)

    dline((b["prog"]["right"] - 0.3, b["prog"]["top"]), (b["huruf"]["x"] + 0.5, b["huruf"]["bottom"]), "*", "1", (-0.25, 0.22), (-0.3, -0.2))
    dline((b["huruf"]["right"] - 0.4, b["huruf"]["bottom"]), (b["mirip"]["x"] + 0.6, b["mirip"]["top"]), "2", "*", (0.25, -0.2), (-0.3, 0.2))
    dline((b["pel"]["right"] - 0.4, b["pel"]["bottom"]), (b["klip"]["x"] + 0.6, b["klip"]["top"]), "1", "1..*", (0.25, -0.2), (-0.35, 0.2))
    return save(fig, "fig06_class")


def _crow(ax, x, y, direction, many):
    """Ujung relasi crow's foot. direction: arah garis menuju entitas ('left','right','up','down')."""
    d = 0.22
    if direction in ("left", "right"):
        s = 1 if direction == "right" else -1  # kaki di luar entitas, menyebar di sisi entitas
        bx = x + s * d
        if many:
            for dy in (-0.16, 0, 0.16):
                ax.plot([bx, x], [y, y + dy], color=INK, lw=0.8, zorder=3)
        ax.plot([bx + s * 0.06] * 2, [y - 0.14, y + 0.14], color=INK, lw=0.8, zorder=3)
    else:
        s = -1 if direction == "down" else 1
        by = y + s * d
        if many:
            for dx in (-0.16, 0, 0.16):
                ax.plot([x, x + dx], [by, y], color=INK, lw=0.8, zorder=3)
        ax.plot([x - 0.14, x + 0.14], [by + s * 0.06] * 2, color=INK, lw=0.8, zorder=3)


def fig_erd():
    fig, ax = blank(15.5, 10.6, (0, 16.5), (0, 11.3))
    W = 2.75
    xs = [0.1, 3.45, 6.8, 10.15, 13.5]
    tops = [11.15, 7.05, 3.2]
    pk, fk = "PK ", "FK "
    e = {}
    e["area"] = _class_box(ax, xs[0], tops[0], W, "area_makhraj", [pk + "id", "nama", "letak"], None)
    e["titik"] = _class_box(ax, xs[1], tops[0], W, "titik_makhraj", [pk + "id", fk + "area_id", "nama", "koordinat_sorot"], None)
    e["huruf"] = _class_box(ax, xs[2], tops[0], W, "huruf", [pk + "id", fk + "titik_id", "karakter", "nama", "urutan"], None)
    e["hs"] = _class_box(ax, xs[3], tops[0], W, "huruf_sifat", [pk + fk + "huruf_id", pk + fk + "sifat_id"], None)
    e["sifat"] = _class_box(ax, xs[4], tops[0], W, "sifat", [pk + "id", "nama", "arti"], None)
    e["user"] = _class_box(ax, xs[0], tops[1], W, "pengguna", [pk + "id", "nama", "email", "peran"], None)
    e["prog"] = _class_box(ax, xs[1], tops[1], W, "progres", [pk + "id", fk + "pengguna_id", fk + "huruf_id", "status", "skor_cek_mandiri"], None)
    e["pel"] = _class_box(ax, xs[2], tops[1], W, "pelajaran", [pk + "id", fk + "huruf_id", "langkah_animasi", "kesalahan_umum"], None)
    e["klip"] = _class_box(ax, xs[3], tops[1], W, "klip_video", [pk + "id", fk + "pelajaran_id", "youtube_id", "detik_mulai", "detik_selesai"], None)
    e["mirip"] = _class_box(ax, xs[4], tops[1], W, "pasangan_mirip", [pk + "id", fk + "huruf_a_id", fk + "huruf_b_id", "contoh_kata"], None)
    e["rek"] = _class_box(ax, xs[0], tops[2], W, "rekaman", [pk + "id", fk + "pengguna_id", fk + "huruf_id", "berkas_lokal", "tanggal"], None)
    e["setor"] = _class_box(ax, xs[1], tops[2], W, "setoran", [pk + "id", fk + "rekaman_id", fk + "pengajar_id", "status"], None, t2=True)
    e["kor"] = _class_box(ax, xs[2], tops[2], W, "koreksi", [pk + "id", fk + "setoran_id", "catatan", "nilai"], None, t2=True)

    def h(p, q, many_p, many_q, y):
        ax.plot([p["right"], q["x"]], [y, y], color=INK, lw=0.8, zorder=1)
        _crow(ax, p["right"], y, "right", many_p)
        _crow(ax, q["x"], y, "left", many_q)

    def v(p, q, many_p, many_q, x):
        ax.plot([x, x], [p["bottom"], q["top"]], color=INK, lw=0.8, zorder=1)
        _crow(ax, x, p["bottom"], "down", many_p)
        _crow(ax, x, q["top"], "up", many_q)

    y0 = tops[0] - 0.85
    h(e["area"], e["titik"], False, True, y0)
    h(e["titik"], e["huruf"], False, True, y0)
    h(e["huruf"], e["hs"], False, True, y0)
    h(e["hs"], e["sifat"], True, False, y0)
    y1 = tops[1] - 0.85
    h(e["user"], e["prog"], False, True, y1)
    h(e["pel"], e["klip"], False, True, y1)
    y2 = tops[2] - 0.85
    h(e["rek"], e["setor"], False, False, y2)
    h(e["setor"], e["kor"], False, False, y2)
    v(e["huruf"], e["pel"], False, False, e["huruf"]["cx"])
    v(e["user"], e["rek"], False, True, e["user"]["cx"])
    # progres -> huruf dan pasangan_mirip -> huruf dengan garis siku
    mid = (e["huruf"]["bottom"] + tops[1]) / 2 + 0.1
    xa = e["huruf"]["x"] + 0.45
    xp = e["prog"]["cx"] + 0.6
    ax.plot([xp, xp, xa, xa], [tops[1], mid, mid, e["huruf"]["bottom"]], color=INK, lw=0.8, zorder=1)
    _crow(ax, xp, tops[1], "up", True)
    _crow(ax, xa, e["huruf"]["bottom"], "down", False)
    xb = e["huruf"]["right"] - 0.45
    xm = e["mirip"]["cx"]
    mid2 = mid - 0.25
    ax.plot([xm, xm, xb, xb], [tops[1], mid2, mid2, e["huruf"]["bottom"]], color=INK, lw=0.8, zorder=1)
    _crow(ax, xm, tops[1], "up", True)
    _crow(ax, xb, e["huruf"]["bottom"], "down", False)
    # legenda
    lx, ly = 10.1, 1.9
    ax.text(lx, ly + 0.55, "Notasi crow's foot:", fontsize=7, weight="bold")
    ax.plot([lx, lx + 1.0], [ly, ly], color=INK, lw=0.8)
    _crow(ax, lx + 1.0, ly, "left", False)
    ax.text(lx + 1.25, ly, "satu", fontsize=7, va="center")
    ax.plot([lx + 2.6, lx + 3.6], [ly, ly], color=INK, lw=0.8)
    _crow(ax, lx + 3.6, ly, "left", True)
    ax.text(lx + 3.85, ly, "banyak", fontsize=7, va="center")
    ax.add_patch(Rectangle((lx, ly - 1.0), 0.5, 0.35, fc=GOLD_L, ec=GOLD, ls=(0, (3, 2)), lw=1))
    ax.text(lx + 0.7, ly - 0.83, "entitas Tahap 2", fontsize=7, va="center")
    return save(fig, "fig07_erd")


# ---------------------------------------------------------------- Gambar 8
def fig_arsitektur():
    fig, ax = blank(15.5, 7.4, (0, 16), (0, 7.6))
    # perangkat
    rbox(ax, 0.1, 0.2, 6.6, 7.2, fc=CREAM, ec=TEAL, lw=1.1, r=0.2)
    ax.text(3.4, 7.0, "Aplikasi React: web/PWA dan Android", ha="center", fontsize=8.5, weight="bold", color=TEAL)
    ax.text(3.4, 2.05, "satu build Vite; APK Android lewat Capacitor", ha="center", va="center", fontsize=6.8, color=GREY)
    mods = ["Mushaf + sorot huruf", "Peta makhraj (5 area, 17 titik)", "Pelajaran 5 langkah per huruf",
            "Rekam, cermin kamera, bandingkan", "Huruf mirip dan kuis", "Uji coba: tes A/B, SUS, ekspor"]
    for i, m in enumerate(mods):
        rbox(ax, 0.45, 6.05 - i * 0.68, 5.9, 0.52, fc="white", ec=LINE, lw=0.8, r=0.1)
        ax.text(3.4, 6.31 - i * 0.68, m, ha="center", va="center", fontsize=7.6)
    rbox(ax, 0.45, 0.45, 5.9, 1.05, fc=TEAL_L, ec=TEAL, lw=0.8, r=0.1)
    ax.text(3.4, 1.18, "Penyimpanan lokal", ha="center", va="center", fontsize=7.8, weight="bold")
    ax.text(3.4, 0.76, "progres: localStorage; rekaman: IndexedDB", ha="center", va="center", fontsize=7.2)
    # firebase
    rbox(ax, 8.0, 3.7, 3.7, 3.7, fc="white", ec=INK, lw=1, r=0.2)
    ax.text(9.85, 7.0, "Firebase", ha="center", fontsize=8.5, weight="bold")
    for i, s in enumerate(["Hosting (web/PWA)", "Auth (Tahap 2)", "Firestore (Tahap 2)", "Storage (Tahap 2)"]):
        t2 = "Tahap 2" in s
        rbox(ax, 8.25, 6.05 - i * 0.68, 3.2, 0.52, fc=GOLD_L if t2 else TEAL_L, ec=GOLD if t2 else TEAL,
             lw=0.8, ls=(0, (3, 2)) if t2 else "-", r=0.1)
        ax.text(9.85, 6.31 - i * 0.68, s, ha="center", va="center", fontsize=7.6)
    # eksternal
    rbox(ax, 12.6, 3.7, 3.3, 3.7, fc="white", ec=INK, lw=1, r=0.2)
    ax.text(14.25, 7.0, "Sumber eksternal", ha="center", fontsize=8.5, weight="bold")
    ext = [("YouTube IFrame", "kanal Syaikh Aiman"), ("Teks Tanzil", "CC BY 3.0"), ("Terjemahan Kemenag", "Tanzil, nonkomersial")]
    for i, (a, s) in enumerate(ext):
        yb = 5.95 - i * 0.78
        rbox(ax, 12.85, yb, 2.8, 0.62, fc="white", ec=LINE, lw=0.8, r=0.1)
        ax.text(14.25, yb + 0.42, a, ha="center", va="center", fontsize=7.0, weight="bold")
        ax.text(14.25, yb + 0.17, s, ha="center", va="center", fontsize=6.6, color=GREY)
    # AI tahap 3
    rbox(ax, 8.0, 0.3, 7.9, 2.2, fc=GOLD_L, ec=GOLD, lw=1, ls=(0, (3, 2)), r=0.2)
    ax.text(11.95, 2.1, "Layanan penilaian AI (Tahap 3)", ha="center", fontsize=8.2, weight="bold", color="#7A520C")
    ax.text(11.95, 1.25, "model pengenal ucapan (wav2vec 2.0) dilatih ulang\npada rekaman yang sudah dikoreksi pengajar;\nskor rendah atau ragu diteruskan ke pengajar",
            ha="center", va="center", fontsize=7.2, color=INK, linespacing=1.15)
    # panah
    arrow(ax, (6.75, 5.6), (7.95, 5.6), style="<|-|>", color=GOLD, ls=(0, (3, 2)), lw=1.0)
    ax.text(7.35, 5.85, "sinkron", ha="center", fontsize=6.6, color=GREY)
    ax.plot([14.25, 14.25, 6.8], [3.65, 3.25, 3.25], color=TEAL, lw=1.1)
    arrow(ax, (7.2, 3.25), (6.75, 3.25), color=TEAL, lw=1.1)
    ax.text(10.5, 2.92, "klip diputar lewat pemutar resmi (tanpa unduh)", ha="center", fontsize=6.6, color=GREY)
    arrow(ax, (6.75, 1.4), (7.95, 1.4), style="<|-|>", color=GOLD, ls=(0, (3, 2)), lw=1.0)
    return save(fig, "fig08_arsitektur")


# ---------------------------------------------------------------- Lampiran 3: model bisnis
def _bullets(items, width):
    lines = []
    for it in items:
        w = textwrap.wrap(it, width)
        lines.append("• " + w[0])
        lines.extend("   " + x for x in w[1:])
    return "\n".join(lines)


BMC = {
    "kp": ("Mitra Utama", [
        "Pengajar tahsin bersanad: validasi materi dan koreksi",
        "TPQ, majelis taklim, tutorial BTQ kampus",
        "Lembaga zakat, wakaf, dan program CSR",
        "Sumber konten: kanal Al-Andalasy, Tanzil, LPMQ"]),
    "ka": ("Aktivitas Utama", [
        "Menyusun dan memvalidasi materi makhraj",
        "Mengembangkan aplikasi per sprint",
        "Merekrut dan melatih pengajar mitra"]),
    "kr": ("Sumber Daya Utama", [
        "Materi 29 huruf yang tervalidasi",
        "Klip guru bersanad",
        "Kode React dan Capacitor",
        "Jaringan pengajar; korpus rekaman"]),
    "vp": ("Proposisi Nilai", [
        "Menunjukkan letak kesalahan dan cara membetulkannya, bukan hanya benar atau salah",
        "Talaqqi digital lima langkah",
        "Contoh dari guru bersanad yang disebut namanya",
        "Inti gratis; belajar privat tanpa rasa canggung"]),
    "cr": ("Relasi Pengguna", [
        "Belajar mandiri dengan target harian kecil",
        "Koreksi personal dari pengajar (Tahap 2)",
        "Komunitas relawan mahasiswa"]),
    "ch": ("Saluran", [
        "Google Play dan web",
        "Kampus: tutorial BTQ, UKM kerohanian",
        "TPQ dan majelis taklim",
        "Konten makhraj pendek di media sosial"]),
    "cs": ("Segmen Pengguna", [
        "Mahasiswa dan pekerja muda",
        "Orang tua yang mendampingi anak",
        "Mualaf dan lansia",
        "Lembaga: TPQ, sekolah, kampus"]),
    "cost": ("Struktur Biaya", [
        "Firebase dan domain: Rp0,2 juta (Tahun 1) hingga Rp16,6 juta (Tahun 3)",
        "Honor tinjauan materi oleh pengajar: Rp2-3 juta per tahun",
        "Promosi dan kemitraan: Rp1-6 juta per tahun; sewa GPU Tahap 3: Rp5 juta",
        "Pengembangan dikerjakan tim tanpa gaji"]),
    "rev": ("Sumber Pendapatan", [
        "Paket Setor ke Pengajar Rp20.000 per lima setoran: 70% untuk pengajar, 30% untuk operasional",
        "Lisensi dasbor lembaga Rp300.000 per kelas per tahun",
        "Dana ZISWAF dan CSR membiayai setoran pengguna kurang mampu"]),
}


def _bmc_block(ax, x, y, w, h, key, n, fc="white", ec=LINE, hc=TEAL, width=23):
    title, items = BMC[key]
    rbox(ax, x, y, w, h, fc=fc, ec=ec, lw=0.8, r=0.12)
    _badge(ax, x + 0.3, y + h - 0.3, n, fc=hc, r=0.18)
    ax.text(x + 0.56, y + h - 0.31, title, ha="left", va="center", fontsize=6.8, weight="bold", color=hc)
    ax.text(x + 0.14, y + h - 0.6, _bullets(items, width), ha="left", va="top", fontsize=6.1, color=INK, linespacing=1.25)


def fig_bmc():
    """Business Model Canvas Makhraj."""
    fig, ax = blank(15.5, 7.6, (0, 15.5), (0, 7.6))
    g = 0.08
    cw = (15.5 - 4 * g) / 5
    xs = [i * (cw + g) for i in range(5)]
    y0, y1 = 2.25, 7.55
    mid = (y0 + y1) / 2
    _bmc_block(ax, xs[0], y0, cw, y1 - y0, "kp", 8)
    _bmc_block(ax, xs[1], mid + g / 2, cw, y1 - mid - g / 2, "ka", 7)
    _bmc_block(ax, xs[1], y0, cw, mid - y0 - g / 2, "kr", 6)
    _bmc_block(ax, xs[2], y0, cw, y1 - y0, "vp", 2, fc=TEAL_L, ec=TEAL)
    _bmc_block(ax, xs[3], mid + g / 2, cw, y1 - mid - g / 2, "cr", 4)
    _bmc_block(ax, xs[3], y0, cw, mid - y0 - g / 2, "ch", 3)
    _bmc_block(ax, xs[4], y0, cw, y1 - y0, "cs", 1)
    half = (15.5 - g) / 2
    _bmc_block(ax, 0, 0.05, half, y0 - 0.05 - g, "cost", 9, fc="#F3F4F6", width=64)
    _bmc_block(ax, half + g, 0.05, half, y0 - 0.05 - g, "rev", 5, fc=GOLD_L, ec=GOLD, hc=GOLD_D, width=64)
    return save(fig, "fig11_bmc")


def _node(ax, x, y, w, h, title, sub, fc="white", ec=LINE, tc=INK):
    rbox(ax, x - w / 2, y - h / 2, w, h, fc=fc, ec=ec, lw=0.9, r=0.18, z=2)
    ax.text(x, y + 0.17, title, ha="center", va="center", fontsize=7.8, weight="bold", color=tc, zorder=3)
    ax.text(x, y - 0.22, sub, ha="center", va="center", fontsize=6.2, color=tc if fc == TEAL else GREY, zorder=3)


def fig_ekosistem():
    """Aliran nilai (layanan) dan aliran dana antarpihak."""
    fig, ax = blank(15.5, 8.4, (0, 15.5), (0, 8.4))
    cx, cy = 7.75, 4.25
    _node(ax, cx, cy, 3.0, 1.5, "Makhraj", "platform belajar\ndan koreksi", fc=TEAL, ec=TEAL, tc="white")
    nodes = {
        "L": (1.65, cy, "Pengguna pemula", "segala usia"),
        "R": (13.85, cy, "Pengajar mitra", "tahsin bersanad"),
        "T": (cx, 7.55, "Lembaga", "TPQ, sekolah, kampus"),
        "B": (cx, 0.95, "Mitra ZISWAF dan CSR", "LAZ, wakaf, perusahaan"),
    }
    for x, y, t, s in nodes.values():
        _node(ax, x, y, 3.2, 1.2, t, s)
    kw = dict(lw=1.1, ms=8, z=1)
    # kiri: pengguna
    arrow(ax, (3.3, cy + 0.32), (6.2, cy + 0.32), color=GOLD, **kw)
    ax.text(4.75, cy + 0.5, "Rp20.000 per\npaket setoran", ha="center", va="bottom", fontsize=6.2, color=GOLD_D)
    arrow(ax, (6.2, cy - 0.32), (3.3, cy - 0.32), color=TEAL, **kw)
    ax.text(4.75, cy - 0.5, "materi gratis\ndan koreksi", ha="center", va="top", fontsize=6.2, color=TEAL)
    # kanan: pengajar
    arrow(ax, (9.3, cy + 0.32), (12.2, cy + 0.32), color=GOLD, **kw)
    ax.text(10.75, cy + 0.5, "70% hasil\nsetoran", ha="center", va="bottom", fontsize=6.2, color=GOLD_D)
    arrow(ax, (12.2, cy - 0.32), (9.3, cy - 0.32), color=TEAL, **kw)
    ax.text(10.75, cy - 0.5, "koreksi dan\nvalidasi materi", ha="center", va="top", fontsize=6.2, color=TEAL)
    # atas: lembaga
    arrow(ax, (cx - 0.7, 6.9), (cx - 0.7, 5.05), color=GOLD, **kw)
    ax.text(cx - 0.9, 5.98, "lisensi Rp300.000\nper kelas per tahun", ha="right", va="center", fontsize=6.2, color=GOLD_D, linespacing=1.15)
    arrow(ax, (cx + 0.7, 5.05), (cx + 0.7, 6.9), color=TEAL, **kw)
    ax.text(cx + 0.9, 5.98, "dasbor kelas dan\nlaporan kemajuan", ha="left", va="center", fontsize=6.2, color=TEAL, linespacing=1.15)
    # bawah: ZISWAF
    arrow(ax, (cx - 0.7, 1.6), (cx - 0.7, 3.45), color=GOLD, **kw)
    ax.text(cx - 0.9, 2.52, "dana subsidi setoran\npengguna kurang mampu", ha="right", va="center", fontsize=6.2, color=GOLD_D, linespacing=1.15)
    arrow(ax, (cx + 0.7, 3.45), (cx + 0.7, 1.6), color=TEAL, **kw)
    ax.text(cx + 0.9, 2.52, "laporan dampak:\npenerima dan huruf dikuasai", ha="left", va="center", fontsize=6.2, color=TEAL, linespacing=1.15)
    # legenda
    for i, (c, t) in enumerate([(TEAL, "layanan atau nilai"), (GOLD, "aliran dana")]):
        yy = 7.85 - i * 0.4
        ax.plot([0.15, 0.85], [yy, yy], color=c, lw=1.6)
        ax.text(1.0, yy, t, ha="left", va="center", fontsize=6.4, color=INK)
    return save(fig, "fig12_ekosistem")


FIN_YEARS = ["Tahun 1", "Tahun 2", "Tahun 3"]
FIN_COST = [4.6, 10.0, 29.6]
FIN_REV = [0.0, 10.2, 36.0]
SCENARIOS = [("Pesimis", -9.4), ("Dasar", 6.4), ("Optimis", 58.3)]


def _num(v, sign=False):
    s = f"{v:+.1f}" if sign else f"{v:.1f}"
    return s.replace(".", ",")


def fig_keuangan():
    """(a) biaya, pendapatan, dan kas kumulatif; (b) selisih Tahun 3 per skenario."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(15.5 * CM, 6.4 * CM), gridspec_kw={"width_ratios": [1.6, 1]})
    x = np.arange(3)
    bw = 0.3
    a1.bar(x - bw / 2 - 0.02, FIN_COST, bw, color=S_GOLD, label="Biaya", zorder=2)
    a1.bar(x + bw / 2 + 0.02, FIN_REV, bw, color=S_TEAL, label="Pendapatan", zorder=2)
    for xi, c, r in zip(x, FIN_COST, FIN_REV):
        a1.text(xi - bw / 2 - 0.02, c + 0.8, _num(c), ha="center", va="bottom", fontsize=6.4, color=INK)
        a1.text(xi + bw / 2 + 0.02, r + 0.8, _num(r) if r else "0", ha="center", va="bottom", fontsize=6.4, color=INK)
    cum = np.cumsum(np.array(FIN_REV) - np.array(FIN_COST))
    a1.plot(x, cum, color=INK, lw=1.4, zorder=3, label="Kas kumulatif")
    a1.scatter(x, cum, s=28, color=INK, edgecolors="white", linewidths=1.2, zorder=4)
    for xi, v in zip(x, cum):
        a1.text(xi, v - 3.6, _num(v, True), ha="center", va="center", fontsize=6.4, color=INK, weight="bold", zorder=5,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    a1.axhline(0, color=GREY, lw=0.7, zorder=1)
    a1.set_xticks(x)
    a1.set_xticklabels(FIN_YEARS, fontsize=7)
    a1.set_xlabel(" ", fontsize=6.4)
    a1.set_ylim(-9, 42)
    a1.set_ylabel("juta rupiah", fontsize=6.8)
    a1.tick_params(labelsize=6.6, length=0)
    a1.grid(axis="y", color=HAIR, lw=0.6, zorder=0)
    a1.spines[["top", "right", "left"]].set_visible(False)
    a1.legend(loc="upper left", fontsize=6.4, frameon=False, ncol=3, handlelength=1.4, columnspacing=1.0)
    a1.set_title("(a) Proyeksi skenario dasar", fontsize=7.4, y=-0.36, color=INK)
    # (b)
    names = [s for s, _ in SCENARIOS]
    vals = [v for _, v in SCENARIOS]
    yb = np.arange(3)[::-1]
    a2.barh(yb, vals, 0.42, color=[MUTED, S_TEAL, MUTED], zorder=2)
    for yi, v in zip(yb, vals):
        a2.text(max(v, 0) + 2, yi, _num(v, True), ha="left", va="center", fontsize=6.6, color=INK, weight="bold")
    a2.axvline(0, color=GREY, lw=0.7)
    a2.set_yticks(yb)
    a2.set_yticklabels(names, fontsize=7)
    a2.set_xlim(-22, 95)
    a2.tick_params(labelsize=6.6, length=0)
    a2.grid(axis="x", color=HAIR, lw=0.6, zorder=0)
    a2.spines[["top", "right", "left"]].set_visible(False)
    a2.set_xlabel("selisih Tahun 3 (juta rupiah)", fontsize=6.4)
    a2.set_title("(b) Sensitivitas skenario", fontsize=7.4, y=-0.36, color=INK)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.95, bottom=0.27, wspace=0.32)
    return save(fig, "fig13_keuangan")


GANTT = [
    ("Produk", [
        ("MVP 29 huruf, rilis Play dan web", 1, 6),
        ("Setor ke pengajar, dasbor lembaga", 9, 14),
        ("Korpus rekaman dan model penilai AI", 16, 33)]),
    ("Konten", [
        ("Tinjauan materi oleh guru bersanad", 1, 9),
        ("Rekaman guru mitra untuk huruf tanpa klip", 4, 10),
        ("Materi tajwid lanjutan", 20, 30)]),
    ("Kemitraan", [
        ("Rekrut dan latih pengajar mitra", 7, 14),
        ("Pilot kelas TPQ dan tutorial kampus", 10, 20),
        ("Kemitraan LAZ, wakaf, dan CSR", 13, 27)]),
    ("Legal dan data", [
        ("Izin kanal video, LPMQ, dan tashih teks", 1, 6),
        ("Kebijakan privasi dan persetujuan rekaman", 9, 12)]),
    ("Evaluasi", [
        ("Uji kegunaan 5-8 orang (think-aloud)", 3, 3),
        ("Uji 20 pemula (SUS, tes awal-akhir)", 4, 6),
        ("Evaluasi dampak skala lebih besar", 22, 26)]),
]
MILESTONES = [(6, "Rilis publik"), (13, "Setoran dibuka"), (30, "AI beta"), (36, "Kas positif")]


def fig_gantt():
    """Rencana implementasi 36 bulan."""
    fig, ax = plt.subplots(figsize=(15.5 * CM, 9.6 * CM))
    for i, (bg, lab) in enumerate([(TEAL_L, "Tahap 1"), ("#EEF5F3", "Tahap 2"), (GOLD_L, "Tahap 3")]):
        ax.axvspan(i * 12, (i + 1) * 12, color=bg, zorder=0, lw=0)
        ax.text(i * 12 + 6, -1.55, f"{lab}  ·  Tahun {i + 1}", ha="center", va="center", fontsize=7, weight="bold",
                color=GOLD_D if i == 2 else TEAL)
    y = 0
    ticks, labels = [], []
    for group, rows in GANTT:
        ax.text(-0.4, y, group.upper(), ha="right", va="center", fontsize=6.2, weight="bold", color=GREY)
        y += 1
        for name, s, e in rows:
            ax.barh(y, e - s + 1, left=s - 1, height=0.5, color=TEAL if group == "Produk" else "#2E7F79", zorder=2)
            ticks.append(y)
            labels.append(name)
            y += 1
    y_end = y - 0.4
    for m, t in MILESTONES:
        ax.plot([m, m], [-0.3, y_end], color=GOLD, lw=0.7, ls=(0, (2, 2)), zorder=1)
        ax.scatter([m], [-0.55], marker="D", s=26, color=GOLD, edgecolors="white", linewidths=1, zorder=4, clip_on=False)
        ax.text(m - 0.35, -0.55, t, ha="right", va="center", fontsize=6, color=GOLD_D)
    ax.set_yticks(ticks)
    ax.set_yticklabels(labels, fontsize=6.4)
    ax.set_ylim(y - 0.4, -2.1)
    ax.set_xlim(0, 36)
    ax.set_xticks(range(0, 37, 3))
    ax.set_xticklabels([str(v) for v in range(0, 37, 3)], fontsize=6.4)
    ax.set_xlabel("bulan ke-", fontsize=6.8)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.subplots_adjust(left=0.33, right=0.99, top=0.99, bottom=0.09)
    return save(fig, "fig14_gantt")


# ---------------------------------------------------------------- Gambar 9 & 10
def _trim(img, bg=(251, 248, 242), tol=6):
    """Potong ruang kosong bawah yang sewarna latar."""
    px = img.convert("RGB").load()
    w, h = img.size
    y = h - 1
    while y > 0:
        row_bg = all(abs(px[x, y][k] - bg[k]) <= tol for x in range(0, w, 8) for k in range(3))
        if not row_bg:
            break
        y -= 1
    return img.crop((0, 0, w, min(h, y + 40)))


def _screens(names, labels, outname, H=1688):
    # H = tinggi layar yang ditampilkan (1688 = 844 px CSS x 2); lebih kecil = bagian bawah dipotong.
    fig, axes = plt.subplots(1, 3, figsize=(15.5 * CM, 11.3 * CM * H / 1688))
    for ax, n, lab in zip(axes, names, labels):
        img = Image.open(SCREENS / f"{n}.png").convert("RGB")
        img = _trim(img)
        if img.size[1] > H:
            img = img.crop((0, 0, img.size[0], H))
        canvas = Image.new("RGB", (img.size[0], H), CREAM)
        canvas.paste(img, (0, 0))
        im = ax.imshow(canvas)
        clip = FancyBboxPatch((0, 0), canvas.size[0], H, boxstyle="round,pad=0,rounding_size=60",
                              transform=ax.transData, fc="none")
        im.set_clip_path(clip)
        ax.add_patch(FancyBboxPatch((0, 0), canvas.size[0], H, boxstyle="round,pad=0,rounding_size=60",
                                    fc="none", ec=INK, lw=1.4))
        ax.set_xlim(-10, canvas.size[0] + 10)
        ax.set_ylim(H + 10, -10)
        ax.axis("off")
        ax.set_title(lab, y=-0.075, fontsize=9)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.06, wspace=0.08)
    return save(fig, outname, check=False)


def fig_screens():
    a = _screens(["Main", "Peta", "Pelajaran"], ["(a) Beranda", "(b) Peta makhraj", "(c) Pelajaran huruf"], "fig09_screens_a", H=1420)
    b = _screens(["Latihan", "Mirip", "Mushaf"], ["(d) Rekam dan bandingkan", "(e) Huruf mirip", "(f) Mushaf dan sorot huruf"], "fig10_screens_b")
    return a, b


def fig_cover_icon():
    """Ikon aplikasi untuk sampul: huruf ba di kotak hijau toska."""
    fig, ax = blank(4.2, 4.2, (0, 10), (0, 10))
    rbox(ax, 0.3, 0.3, 9.4, 9.4, fc=TEAL, ec=TEAL, r=2.2)
    ax.text(5, 5.0, "ب", ha="center", va="center", fontsize=70, color="white", family=ARAB)
    return save(fig, "cover_icon", check=False)


ALL = [fig_cover_icon, fig_literasi, fig_alur_belajar, fig_pasar, fig_roadmap, fig_usecase, fig_class, fig_erd, fig_arsitektur,
       fig_bmc, fig_ekosistem, fig_keuangan, fig_gantt, fig_screens]


def build_all():
    for f in ALL:
        f()
        print(f"  gambar {f.__name__} selesai")


if __name__ == "__main__":
    build_all()
