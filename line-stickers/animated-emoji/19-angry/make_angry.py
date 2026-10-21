"""Angry emoji: the stomp and the rage part of the Kling clip, played forward and back
at an even speed, plus pixel-art steam puffs."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
SRC, OUT = sys.argv[1], sys.argv[2]            # folder of green-removed video frames (NNN.png), output folder
W, LOOP_MS = 540, 1000                          # working canvas (3x of 180), one loop
INK, STEAM = (42, 26, 58, 255), (250, 246, 240, 255)
# video frames 8..29 (foot up -> stomp -> shouting), dense around the stomp, then back again
FWD = [8, 9, 10, 11, 12, 14, 17, 20, 23, 26, 29]
SEQ = FWD + FWD[-2:0:-1]                        # 20 frames, ping-pong
SEQ = SEQ[4:] + SEQ[:4]                         # start on the stomp landing (the still LINE shows)
# show each frame for as long as the video takes to reach the next one, so the speed is even
gaps = [abs(SEQ[(k+1) % len(SEQ)] - SEQ[k]) for k in range(len(SEQ))]
durs = [round(g * LOOP_MS / sum(gaps)) for g in gaps]
durs[-1] += LOOP_MS - sum(durs)
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
        steam(g, hx+dx, hy+dy, (t / 500 + phase) % 1)            # by time: 2 puffs per loop each
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
save(f180, f"{OUT}/angry.png", durs, 4)
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-angry.png", durs, 0)
