"""LOL emoji: lying on his back, rolling side to side laughing, legs kicking. Kling 3.0 (start = end frame).
Two rocks from the clip (20 -> 40, frame 40 matches 20), 1 s loop x 4. The tail touches the video's
left edge in a few frames, so it is faded out instead of cut straight. No overlays."""
import sys, os
import numpy as np
from PIL import Image
SRC, OUT = sys.argv[1], sys.argv[2]            # folder of green-removed video frames (NNN.png), output folder
W, LOOP_MS, N = 540, 1000, 20                   # working canvas (3x of 180), one loop, frames
A, B = 20, 40                                   # two rocks; 40 matches 20
FADE = 14                                       # px faded at the video's left edge
SEQ = [round(A + (B - A) * k / N) for k in range(N)]
durs = [LOOP_MS // N] * N
def load(i):
    a = np.asarray(Image.open(f"{SRC}/{i:03d}.png")).astype(np.float32).copy()
    a[..., 3] *= np.clip(np.arange(a.shape[1]) / FADE, 0, 1)[None, :]
    return Image.fromarray(a.round().astype(np.uint8), 'RGBA')

src = {i: load(i) for i in set(SEQ)}
bbs = [src[i].getbbox() for i in src]
box = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
s = (W - 12) / max(box[2] - box[0], box[3] - box[1])
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)
cx, cy = (W-cw)//2, (W-ch)//2

out = []
for i in SEQ:
    c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    m = src[i].crop(box).convert('RGBa').resize((cw, ch), Image.LANCZOS).convert('RGBA')
    c.alpha_composite(m, (cx, cy)); out.append(c)

def save(frs, path, durs, loop):
    sz = frs[0].width
    tall = Image.new('RGBA', (sz, sz*len(frs))); [tall.paste(f, (0, sz*i)) for i, f in enumerate(frs)]
    P = tall.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    q = [P.crop((0, sz*i, sz, sz*i+sz)) for i in range(len(frs))]
    for x in q: x.info = dict(P.info)
    q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=loop, disposal=0, blend=0, optimize=True)
    print(os.path.basename(path), len(frs), 'frames', sum(durs), 'ms x', loop, os.path.getsize(path)//1024, 'KB')

f180 = [o.convert('RGBa').resize((180, 180), Image.LANCZOS).convert('RGBA') for o in out]
os.makedirs(f"{OUT}/frames", exist_ok=True)
for i, f in enumerate(f180): f.save(f"{OUT}/frames/{i+1:02d}.png")
print('frames', SEQ)
save(f180, f"{OUT}/lol.png", durs, 4)                  # 1 s x 4 = 4 s
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-lol.png", durs, 0)
