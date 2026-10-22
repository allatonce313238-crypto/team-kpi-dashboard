"""Proud: stands tall and confident, mouth closed, slow breathing.
Kling opened his mouth in frames ~12-54, so only closed-mouth frames 1-10 are used (ping-pong),
plus a gentle breathing stretch in code: up to 2% taller, anchored at the feet. 2 s loop x 2."""
import sys, os, math
from PIL import Image
SRC, OUT = sys.argv[1], sys.argv[2]
W, LOOP_MS, N, BREATH = 540, 2000, 20, 0.02
SEQ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
durs = [LOOP_MS // N] * N
src = {i: Image.open(f"{SRC}/{i:03d}.png") for i in set(SEQ)}
bbs = [src[i].getbbox() for i in src]
box = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
s = (W - 12) / ((box[3] - box[1]) * (1 + BREATH))          # leave room for the tallest breath
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)
out = []
for k, i in enumerate(SEQ):
    b = 1 + BREATH * (1 - math.cos(2 * math.pi * k / N)) / 2  # in at the middle, out at the ends
    h = round(ch * b)
    m = src[i].crop(box).convert('RGBa').resize((cw, h), Image.LANCZOS).convert('RGBA')
    c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    c.alpha_composite(m, ((W - cw) // 2, W - 6 - h))        # feet stay on the same line
    out.append(c)

def save(frs, path, durs, loop):
    sz = frs[0].width
    tall = Image.new('RGBA', (sz, sz*len(frs))); [tall.paste(f, (0, sz*i)) for i, f in enumerate(frs)]
    P = tall.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    q = [P.crop((0, sz*i, sz, sz*i+sz)) for i in range(len(frs))]
    for x in q: x.info = dict(P.info)
    q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=loop, disposal=0, blend=0, optimize=True)
    print(os.path.basename(path), len(frs), 'frames', sum(durs), 'ms x', loop, os.path.getsize(path)//1024, 'KB')

os.makedirs(f"{OUT}/frames", exist_ok=True)
for f in os.listdir(f"{OUT}/frames"): os.remove(f"{OUT}/frames/{f}")
f180 = [o.convert('RGBa').resize((180, 180), Image.LANCZOS).convert('RGBA') for o in out]
for i, f in enumerate(f180): f.save(f"{OUT}/frames/{i+1:02d}.png")
save(f180, f"{OUT}/proud.png", durs, 2)
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out], f"{OUT}/preview-proud.png", durs, 0)
