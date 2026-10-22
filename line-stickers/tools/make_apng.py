"""Build a LINE animated emoji (180x180 APNG) from green-removed Kling frames.

usage: make_apng.py SRC OUT NAME --seq 1,5,9 --durs 100,100,100 --loops 2
SRC holds NNN.png frames; OUT gets NAME.png, preview-NAME.png and frames/.
--durs may be a single value for every frame."""
import argparse, os
from PIL import Image

W = 540                                         # working canvas (3x of 180)

def save(frs, path, durs, loop):
    sz = frs[0].width
    tall = Image.new('RGBA', (sz, sz*len(frs))); [tall.paste(f, (0, sz*i)) for i, f in enumerate(frs)]
    P = tall.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    q = [P.crop((0, sz*i, sz, sz*i+sz)) for i in range(len(frs))]
    for x in q: x.info = dict(P.info)
    q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=loop, disposal=0, blend=0, optimize=True)
    print(os.path.basename(path), len(frs), 'frames', sum(durs), 'ms x', loop, os.path.getsize(path)//1024, 'KB')

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out'); ap.add_argument('name')
ap.add_argument('--seq', required=True); ap.add_argument('--durs', required=True)
ap.add_argument('--loops', type=int, required=True)
a = ap.parse_args()
seq = [int(x) for x in a.seq.split(',')]
durs = [int(x) for x in a.durs.split(',')]
if len(durs) == 1: durs *= len(seq)
assert len(durs) == len(seq) and 5 <= len(seq) <= 20

src = {i: Image.open(f"{a.src}/{i:03d}.png") for i in set(seq)}
bbs = [src[i].getbbox() for i in src]
box = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
s = (W - 12) / max(box[2] - box[0], box[3] - box[1])
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)
cx, cy = (W-cw)//2, (W-ch)//2
out = []
for i in seq:
    c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    c.alpha_composite(src[i].crop(box).convert('RGBa').resize((cw, ch), Image.LANCZOS).convert('RGBA'), (cx, cy))
    out.append(c)
os.makedirs(f"{a.out}/frames", exist_ok=True)
for f in os.listdir(f"{a.out}/frames"): os.remove(f"{a.out}/frames/{f}")
f180 = [o.convert('RGBa').resize((180, 180), Image.LANCZOS).convert('RGBA') for o in out]
for i, f in enumerate(f180): f.save(f"{a.out}/frames/{i+1:02d}.png")
save(f180, f"{a.out}/{a.name}.png", durs, a.loops)
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{a.out}/preview-{a.name}.png", durs, 0)
