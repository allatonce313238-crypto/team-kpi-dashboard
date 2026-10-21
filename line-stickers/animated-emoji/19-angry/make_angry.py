"""Angry emoji: Kling rage clip played forward and back, plus pixel-art steam,
a pulsing anger mark and a small tremble."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
CUT, OUT = sys.argv[1], sys.argv[2]            # folder of 18 green-removed frames (ping-pong order), output folder
N, W = 18, 540                                  # frames, working canvas (3x of 180)
INK, RED, STEAM = (42, 26, 58, 255), (240, 36, 56, 255), (250, 246, 240, 255)
frames = [Image.open(f"{CUT}/{k:02d}.png") for k in range(N)]
box = (0, 80, 960, 948)                         # union bbox of the clip
s = 0.52
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)
cx, cy = (W-cw)//2, W-6-ch                      # room above the head for the effects

def head(f):
    """Centre of the silver helmet plate, in 180px grid coordinates."""
    a = np.asarray(f).astype(int); r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    mx, mn = a[..., :3].max(2), a[..., :3].min(2)
    plate = (al > 200) & (mn > 130) & (mx < 235) & (mx - mn < 22)
    plate[450:] = False; plate[:, :200] = False; plate[:, 800:] = False
    ys, xs = np.nonzero(plate)
    return (cx + (xs.mean()-box[0])*s) / 3, (cy + (ys.mean()-box[1])*s) / 3

VEIN = [".##...##.",
        "#..#.#..#",
        "#.......#",
        ".#.....#.",
        ".........",
        ".#.....#.",
        "#.......#",
        "#..#.#..#",
        ".##...##."]

def anger_mark(g, x, y, big):
    """Pulsing 'anger vein' symbol; the big phase pushes each corner 1px outward."""
    for pass_, col in ((1, INK), (0, RED)):
        for r, row in enumerate(VEIN):
            for c, ch_ in enumerate(row):
                if ch_ != '#': continue
                ox = (1 if c > 4 else -1) if big else 0
                oy = (1 if r > 4 else -1) if big else 0
                px, py = x + (c-4)*3 + ox, y + (r-4)*3 + oy
                g.rectangle([px-pass_, py-pass_, px+2+pass_, py+2+pass_], fill=col)

def steam(g, x, y, age):
    """A puff that rises and grows, drawn with an ink outline."""
    r = 3 + age
    y -= age * 2
    for rad, fill in ((r+1, INK), (r, STEAM)):
        for ox, oy, k in ((0, 0, 0), (-r, 2, 1), (r, 2, 1)):
            rr = rad - k
            g.ellipse([x+ox-rr, y+oy-rr, x+ox+rr, y+oy+rr], fill=fill)

out = []
for k, f in enumerate(frames):
    j = 3 if k % 2 else 0                       # 1px tremble on the 180 grid
    c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    m = f.crop(box).convert('RGBa').resize((cw, ch), Image.LANCZOS).convert('RGBA')
    c.alpha_composite(m, (cx + j, cy))
    hx, hy = head(f); hx = round(hx + j/3); hy = round(hy)
    lo = Image.new('RGBA', (W//3, W//3), (0, 0, 0, 0)); g = ImageDraw.Draw(lo)
    for start, dx, dy in ((0, -30, -10), (3, -12, -18)):     # two puffs, 3 frames apart
        age = (k - start) % 6
        if age < 5: steam(g, hx+dx, hy+dy, age)
    anger_mark(g, hx+28, hy-12, big=(k // 3) % 2 == 0)
    c.alpha_composite(lo.resize((W, W), Image.NEAREST)); out.append(c)

def save(frs, path, durs, loop):
    sz = frs[0].width
    tall = Image.new('RGBA', (sz, sz*len(frs))); [tall.paste(f, (0, sz*i)) for i, f in enumerate(frs)]
    P = tall.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    q = [P.crop((0, sz*i, sz, sz*i+sz)) for i in range(len(frs))]
    for x in q: x.info = dict(P.info)
    q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=loop, disposal=0, blend=0, optimize=True)
    print(os.path.basename(path), len(frs), 'frames', sum(durs), 'ms x', loop, os.path.getsize(path)//1024, 'KB')

durs = [56]*10 + [55]*8                         # about 2x the clip's speed, 1 s per loop
f180 = [o.convert('RGBa').resize((180, 180), Image.LANCZOS).convert('RGBA') for o in out]
for i, f in enumerate(f180): f.save(f"{OUT}/frames/{i+1:02d}.png")
save(f180, f"{OUT}/angry.png", durs, 4)
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-angry.png", durs, 0)
