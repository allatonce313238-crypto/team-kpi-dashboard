"""Sly smirk emoji: chest-up, rubbing paws with a scheming grin, with a dark jittering "snicker" aura
(rings of short dash clusters) drawn in code behind him. Kling 3.0 with the same image as start and
end frame, so the clip loops by itself. 2 s loop x 2."""
import sys, os, math, random
from PIL import Image, ImageDraw
SRC, OUT = sys.argv[1], sys.argv[2]            # folder of green-removed video frames (NNN.png), output folder
W, LOOP_MS, N = 540, 2000, 20                   # working canvas (3x of 180), one loop, frames
A, B = 1, 73                                    # frame 73 matches frame 1
SEQ = [round(A + (B - A) * k / N) for k in range(N)]
durs = [LOOP_MS // N] * N
MAX_H = 440                                     # Max's height on the canvas, leaving room for the aura
CX, CY, RX, RY = 270, 290, 252, 250             # aura ellipse
DASH = (70, 50, 60, 235)

def aura(k, n=60, seed=7):
    rnd = random.Random(seed); jit = random.Random(seed * 1000 + k)
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.04, 0.04)
        r = rnd.uniform(0.84, 1.0)
        x = CX + RX * r * math.cos(a) + jit.uniform(-3, 3)
        y = CY + RY * r * math.sin(a) + jit.uniform(-3, 3)
        ln = rnd.uniform(12, 20)
        ux, uy = math.cos(a), math.sin(a)               # radial direction
        px, py = -uy, ux                                # tangent, spacing for parallel strokes
        for s in range(rnd.choice((2, 3))):
            ox, oy = px * (s - 1) * 7, py * (s - 1) * 7
            d.line([(x + ox - ux * ln / 2, y + oy - uy * ln / 2), (x + ox + ux * ln / 2, y + oy + uy * ln / 2)],
                   fill=DASH, width=4)
    return im

src = {i: Image.open(f"{SRC}/{i:03d}.png") for i in set(SEQ)}
bbs = [src[i].getbbox() for i in src]
box = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
s = MAX_H / (box[3] - box[1])
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)
px, py = (W - cw) // 2, W - ch                  # bottom-aligned: chest-up crop continues off the bottom edge

out = []
for k, i in enumerate(SEQ):
    c = aura(k)
    m = src[i].crop(box).convert('RGBa').resize((cw, ch), Image.LANCZOS).convert('RGBA')
    c.alpha_composite(m, (px, py)); out.append(c)

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
print('frames', SEQ)
save(f180, f"{OUT}/sly-smirk.png", durs, 2)                   # 2 s x 2 = 4 s
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-sly-smirk.png", durs, 0)
