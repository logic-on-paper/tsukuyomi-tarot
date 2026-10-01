"""外側 12% 以内にある明るい縁（クリーム色の台紙）を検出して切り落とし、7:12 の 700x1200 JPG に揃える。"""
import pathlib, sys
from PIL import Image
import numpy as np
D = pathlib.Path(r"D:\PWA\tsukuyomi-tarot\cards")
ids = [int(a) for a in sys.argv[1:]] or range(22)
for i in ids:
    p = D / f"{i:02d}.png"
    im = Image.open(p).convert("RGB")
    a = np.asarray(im.convert("L")).astype(float)
    h, w = a.shape
    thr = 150
    def last_light(seq):
        n = -1
        for k, row in enumerate(seq):
            if row.mean() > thr: n = k
        return n + 1
    top = last_light(a[:int(h*0.12)]); bot = last_light(a[::-1][:int(h*0.12)])
    left = last_light(a.T[:int(w*0.12)]); right = last_light(a.T[::-1][:int(w*0.12)])
    pad = 10
    im = im.crop((left+pad, top+pad, w-right-pad, h-bot-pad))
    cw, ch = im.size
    if cw/ch > 7/12:
        nw = int(ch*7/12); im = im.crop(((cw-nw)//2, 0, (cw-nw)//2+nw, ch))
    else:
        nh = int(cw*12/7); im = im.crop((0, (ch-nh)//2, cw, (ch-nh)//2+nh))
    im = im.resize((700, 1200), Image.LANCZOS)
    im.save(D / f"{i:02d}.jpg", quality=88, optimize=True)
    print(f"{i:02d} trim t{top} b{bot} l{left} r{right}")
