"""Gabungkan pratinjau halaman PDF menjadi satu lembar kontak (untuk render check)."""
from pathlib import Path
from PIL import Image

pages = sorted(Path("_preview").glob("page*.png"))
ims = [Image.open(p) for p in pages]
w, h = ims[0].size
cols = 5
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w + (cols + 1) * 8, rows * h + (rows + 1) * 8), (120, 120, 120))
for i, im in enumerate(ims):
    r, c = divmod(i, cols)
    sheet.paste(im, (8 + c * (w + 8), 8 + r * (h + 8)))
sheet.save("_preview/sheet.png")
