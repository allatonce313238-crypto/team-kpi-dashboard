"""Sorry emoji: starts on the deep bow, rises to a guilty look, bows again. 2 s loop x 2.
The wing tip touches the video's right edge during the bow, so it is faded out instead of cut straight."""
import sys, os
import numpy as np
from PIL import Image
SRC, OUT = sys.argv[1], sys.argv[2]            # folder of green-removed video frames (NNN.png), output folder
W, LOOP_MS = 540, 2000                          # working canvas (3x of 180), one loop
HOLD_BOW, HOLD_UP, STEP = 40, 16, 60            # held frames, ms per motion frame
SEQ = ([HOLD_BOW] + [53, 55, 57, 59, 61, 63, 65]   # rise out of the deep bow
       + [5, 7, 9, 11, 13] + [HOLD_UP]             # up to the guilty look (65 -> 5 is the closest match)
       + [21, 23, 25, 27, 29, 31])                 # bow down again
durs = [STEP] * len(SEQ)
durs[SEQ.index(HOLD_UP)] = 260
durs[0] += LOOP_MS - sum(durs)                  # long hold on the bow
FADE = 14                                       # px faded at the video's right edge

def load(i):
    im = Image.open(f"{SRC}/{i:03d}.png")
    a = np.asarray(im).astype(np.float32).copy()
    w = a.shape[1]
    ramp = np.clip((w - 1 - np.arange(w)) / FADE, 0, 1)
    a[..., 3] *= ramp[None, :]
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

os.makedirs(f"{OUT}/frames", exist_ok=True)
f180 = [o.convert('RGBa').resize((180, 180), Image.LANCZOS).convert('RGBA') for o in out]
for i, f in enumerate(f180): f.save(f"{OUT}/frames/{i+1:02d}.png")
print('frames', SEQ, durs)
save(f180, f"{OUT}/sorry.png", durs, 2)                       # 2 s x 2 = 4 s
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-sorry.png", durs, 0)
