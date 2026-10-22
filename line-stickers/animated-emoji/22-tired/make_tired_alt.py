"""Tired alternates: Kling barely moved him, so the motion is added in code as a squash anchored at the floor.
  A "breathe": slow even breathing, 3% flatter and 2% wider and back.
  B "sigh":    a short inhale (4% taller), then a long heavy sigh that deflates him 7% flatter and 3% wider.
usage: make_tired_alt.py SRC OUT A|B"""
import sys, os, math
from PIL import Image
SRC, OUT, MODE = sys.argv[1], sys.argv[2], sys.argv[3]
W, N, LOOP_MS = 540, 20, 2000
src = [Image.open(f"{SRC}/{round(1 + 72 * k / N):03d}.png") for k in range(N)]
bbs = [s.getbbox() for s in src]
box = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
s = (W - 40) / max(box[2] - box[0], box[3] - box[1])
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)

def shape(t):                                   # t in [0, 1) -> (width scale, height scale)
    if MODE == 'A':
        p = (1 - math.cos(2 * math.pi * t)) / 2
        return 1 + 0.02 * p, 1 - 0.03 * p
    if t < 0.2:                                  # quick inhale
        p = math.sin(math.pi / 2 * t / 0.2)
        return 1 - 0.01 * p, 1 + 0.04 * p
    p = (t - 0.2) / 0.8                          # long heavy sigh, then settle back to rest
    d = math.sin(math.pi * p) ** 0.6
    return 1 + 0.03 * d - 0.01 * (1 - p) * (p < 0.15), 1 + 0.04 * max(0, 1 - p / 0.15) - 0.07 * d

out = []
for k, im in enumerate(src):
    sx, sy = shape(k / N)
    w, h = round(cw * sx), round(ch * sy)
    m = im.crop(box).convert('RGBa').resize((w, h), Image.LANCZOS).convert('RGBA')
    c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    c.alpha_composite(m, ((W - w) // 2, (W + ch) // 2 - h))   # bottom stays on the same line
    out.append(c)

def save(frs, path, durs, loop):
    sz = frs[0].width
    tall = Image.new('RGBA', (sz, sz*len(frs))); [tall.paste(f, (0, sz*i)) for i, f in enumerate(frs)]
    P = tall.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    q = [P.crop((0, sz*i, sz, sz*i+sz)) for i in range(len(frs))]
    for x in q: x.info = dict(P.info)
    q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=loop, disposal=0, blend=0, optimize=True)
    print(os.path.basename(path), len(frs), 'frames', sum(durs), 'ms x', loop, os.path.getsize(path)//1024, 'KB')

f180 = [o.convert('RGBa').resize((180, 180), Image.LANCZOS).convert('RGBA') for o in out]
save(f180, f"{OUT}/tired-alt-{MODE}.png", [LOOP_MS // N] * N, 2)
