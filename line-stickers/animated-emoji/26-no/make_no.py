"""No: Kling opened his mouth while shaking his head (frames ~7-55), which looked wrong, so only the closed-mouth
frames are used (58-73, ping-pong) and the gentle "no" sway is added in code: the whole figure tilts left and right
(+-4 degrees) around his feet, twice per loop. 2 s x 2."""
import sys, os, math
from PIL import Image
SRC, OUT = sys.argv[1], sys.argv[2]
W, N, LOOP_MS, TILT = 540, 20, 2000, 4.0
base = [58, 60, 62, 64, 66, 68, 70, 72, 73, 72, 70, 68, 66, 64, 62, 60, 58, 59, 61, 63]
src = {i: Image.open(f"{SRC}/{i:03d}.png") for i in set(base)}
bbs = [src[i].getbbox() for i in src]
box = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
s = (W - 70) / max(box[2] - box[0], box[3] - box[1])          # margin so the tilted sign stays inside
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)
out = []
for k, i in enumerate(base):
    m = src[i].crop(box).convert('RGBa').resize((cw, ch), Image.LANCZOS)
    c = Image.new('RGBa', (W, W)); c.paste(m, ((W - cw) // 2, W - 20 - ch))
    a = TILT * math.sin(4 * math.pi * k / N)                    # two side-to-side shakes per loop
    c = c.rotate(a, resample=Image.BICUBIC, center=(W // 2, W - 20))
    out.append(c.convert('RGBA'))

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
save(f180, f"{OUT}/no.png", [LOOP_MS // N] * N, 2)
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out], f"{OUT}/preview-no.png", [LOOP_MS // N] * N, 0)
