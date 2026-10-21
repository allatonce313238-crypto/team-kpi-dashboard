"""Angry emoji built around the stomp: the foot lifts and holds, slams down fast, the
landing holds with a dust burst, then a short shouting part. Plus pixel-art steam."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
SRC, OUT = sys.argv[1], sys.argv[2]            # folder of green-removed video frames (NNN.png), output folder
W, LOOP_MS = 540, 2000                          # working canvas (3x of 180), one loop
INK, STEAM = (42, 26, 58, 255), (250, 246, 240, 255)
# (video frame, ms). Video frames 8..26: foot up (8) -> landing (12) -> shouting (14..26).
SHOT = ([(12, 90)] * 3                                       # landing, held for 3 frames while the dust bursts
        + [(f, 95) for f in (14, 17, 20, 23, 26, 23, 20, 17, 14)]   # shouting and punching
        + [(f, 75) for f in (11, 10, 9)]                     # foot lifts (wind-up)
        + [(8, 300)]                                         # foot held high
        + [(f, 30) for f in (9, 10, 11)])                    # slam down
SEQ = [f for f, _ in SHOT]
durs = [d for _, d in SHOT]
slow = [k for k, d in enumerate(durs) if d > 30]             # stretch everything but the slam to fit the loop
extra = LOOP_MS - sum(durs)
for k in slow: durs[k] += extra * durs[k] // sum(durs[j] for j in slow)
durs[0] += LOOP_MS - sum(durs)
FOOT = (55, 166)                                # landing foot on the 180 grid (from frame 12)
box = (0, 30, 960, 946)                         # union bbox of the frames used
s = 0.5
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)
cx, cy = (W-cw)//2, W-6-ch                      # room above the head for the steam

def head(f):
    """Centre of the silver helmet plate, in 180px grid coordinates."""
    a = np.asarray(f).astype(int); al = a[..., 3]
    mx, mn = a[..., :3].max(2), a[..., :3].min(2)
    plate = (al > 200) & (mn > 130) & (mx < 235) & (mx - mn < 22)
    plate[450:] = False; plate[:, :200] = False; plate[:, 800:] = False
    ys, xs = np.nonzero(plate)
    return (cx + (xs.mean()-box[0])*s) / 3, (cy + (ys.mean()-box[1])*s) / 3

def steam(g, x, y, p):
    """A puff that rises and grows over its life p in [0, 1), drawn with an ink outline."""
    r = round(3 + 4*p)
    y -= round(10*p)
    for rad, fill in ((r+1, INK), (r, STEAM)):
        for ox, oy, k in ((0, 0, 0), (-r, 2, 1), (r, 2, 1)):
            rr = rad - k
            g.ellipse([x+ox-rr, y+oy-rr, x+ox+rr, y+oy+rr], fill=fill)

def dust(g, p):
    """Dust clouds bursting left and right of the landing foot over its life p in [0, 1)."""
    fx, fy = FOOT
    r = round(5 + 4*p); spread = round(10 + 16*p)
    for side in (-1, 1):
        x = fx + side*spread
        for rad, fill in ((r+1, INK), (r, STEAM)):
            for ox, oy, k in ((0, 0, 0), (side*r, 1, 1)):
                rr = rad - k
                g.ellipse([x+ox-rr, fy+oy-rr, x+ox+rr, fy+oy+rr], fill=fill)
    if p < 0.35:                                # impact ticks right after landing
        for dx, dy in ((-14, -12), (0, -18), (14, -12)):
            x0, y0 = fx + dx, fy + dy
            g.line([x0, y0, x0 + dx//3, y0 + dy//3], fill=INK, width=3)
            g.line([x0, y0, x0 + dx//3, y0 + dy//3], fill=STEAM, width=1)

src = {i: Image.open(f"{SRC}/{i:03d}.png") for i in set(SEQ)}
heads = {i: head(f) for i, f in src.items()}
out, t = [], 0
for k, i in enumerate(SEQ):
    c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    m = src[i].crop(box).convert('RGBa').resize((cw, ch), Image.LANCZOS).convert('RGBA')
    c.alpha_composite(m, (cx, cy))
    hx, hy = map(round, heads[i])
    lo = Image.new('RGBA', (W//3, W//3), (0, 0, 0, 0)); g = ImageDraw.Draw(lo)
    for phase, dx, dy in ((0.0, -30, -10), (0.5, -12, -18)):  # two puffs, half a cycle apart
        steam(g, hx+dx, hy+dy, (t / 500 + phase) % 1)            # by time: 4 puffs per loop each
    if t < 420: dust(g, t / 420)                                  # the burst lasts 0.42 s after landing
    c.alpha_composite(lo.resize((W, W), Image.NEAREST)); out.append(c)
    t += durs[k]

def save(frs, path, durs, loop):
    sz = frs[0].width
    tall = Image.new('RGBA', (sz, sz*len(frs))); [tall.paste(f, (0, sz*i)) for i, f in enumerate(frs)]
    P = tall.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    q = [P.crop((0, sz*i, sz, sz*i+sz)) for i in range(len(frs))]
    for x in q: x.info = dict(P.info)
    q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=loop, disposal=0, blend=0, optimize=True)
    print(os.path.basename(path), len(frs), 'frames', sum(durs), 'ms x', loop, os.path.getsize(path)//1024, 'KB')

f180 = [o.convert('RGBa').resize((180, 180), Image.LANCZOS).convert('RGBA') for o in out]
for i, f in enumerate(f180): f.save(f"{OUT}/frames/{i+1:02d}.png")
print('frames', SEQ); print('ms', durs)
save(f180, f"{OUT}/angry.png", durs, 2)       # 2 s x 2 = 4 s
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-angry.png", durs, 0)
