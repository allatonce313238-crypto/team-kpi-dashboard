"""On my way! emoji: Kling run cycle + pixel-art speed lines and dust puffs."""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw
CUT, OUT = sys.argv[1], sys.argv[2]            # folder of 16 green-removed frames, output folder
N, W = 16, 540                                  # frames, working canvas (3x of 180)
INK, LINE, DUST = (42, 26, 58, 255), (255, 255, 255, 255), (244, 234, 216, 255)
frames = [Image.open(f"{CUT}/{k:02d}.png") for k in range(N)]
box = (20, 74, 912, 960)                        # union bbox of the run frames (Kling 3.0 redo, video frames 7-31)
s = 449 / max(box[2] - box[0], box[3] - box[1])
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)
cx, cy = W-8-cw, W-14-ch                        # right-aligned, room on the left for effects

def pix(draw_fn):
    """Draw on a 180px canvas and scale up 3x, so effects use the emoji's real pixel grid."""
    lo = Image.new('RGBA', (W//3, W//3), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(lo))
    return lo.resize((W, W), Image.NEAREST)

def speed_lines(k):
    def d(g):
        for y, ln, ph in ((26, 30, 0), (40, 22, 5), (54, 34, 2), (68, 18, 6), (122, 20, 3), (138, 28, 7)):
            t = ((k + ph) % 8) / 8                      # one sweep per run cycle
            x = round(58 - t * 70)                      # slides left, off the edge
            if t > 0.85: continue                       # short gap before it restarts
            g.rectangle([x-1, y-1, x+ln, y+2], fill=INK); g.rectangle([x, y, x+ln-1, y+1], fill=LINE)
    return pix(d)

def dust(k):
    def d(g):
        for start, fx in ((0, 70), (4, 58)):            # two foot contacts per run cycle
            age = (k - start) % 8
            if age > 5: continue
            r = 3 + age                                  # grows
            x = fx - age * 3                             # drifts back
            y = 168 - age // 2
            for ox, oy, rr in ((0, 0, r), (-r, 1, r-1), (r-1, 2, r-2)):
                if rr < 1: continue
                g.ellipse([x+ox-rr-1, y+oy-rr-1, x+ox+rr+1, y+oy+rr+1], fill=INK)
            for ox, oy, rr in ((0, 0, r), (-r, 1, r-1), (r-1, 2, r-2)):
                if rr < 1: continue
                g.ellipse([x+ox-rr, y+oy-rr, x+ox+rr, y+oy+rr], fill=DUST)
    return pix(d)

out = []
for k, f in enumerate(frames):
    c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    c.alpha_composite(speed_lines(k)); c.alpha_composite(dust(k))     # effects behind Max
    m = f.crop(box).convert('RGBa').resize((cw, ch), Image.LANCZOS).convert('RGBA')
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
for i, f in enumerate(f180): f.save(f"{OUT}/frames/{i+1:02d}.png")
save(f180, f"{OUT}/on-my-way.png", [62, 63]*8, 4)          # 2 run cycles per second, 4 loops = 4 s
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-on-my-way.png", [62, 63]*8, 0)
