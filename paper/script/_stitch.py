"""Gabungkan beberapa PNG gambar menjadi satu pratinjau: python _stitch.py out.png fig1 fig2 ..."""
import sys
from PIL import Image

out, names = sys.argv[1], sys.argv[2:]
ims = [Image.open(f"figures/{n}.png").convert("RGB") for n in names]
W = 1600
ims = [im.resize((W, int(im.height * W / im.width))) for im in ims]
c = Image.new("RGB", (W, sum(i.height + 24 for i in ims)), "#888")
y = 0
for i in ims:
    c.paste(i, (0, y))
    y += i.height + 24
c.save(f"_preview/{out}")
