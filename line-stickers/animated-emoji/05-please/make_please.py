"""Please emoji: head sway (tilt right -> centre -> tilt right) from the Kling clip, skipping the slow blink.
Eyes enlarged in code (~65%, Puss-in-Boots style) with a smooth magnifier around each eye.
The wing tip touches the video's right edge when he tilts, so it is faded out instead of cut straight."""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
SRC, OUT = sys.argv[1], sys.argv[2]            # folder of green-removed video frames (NNN.png), output folder
W, LOOP_MS, N = 540, 1000, 20                   # working canvas (3x of 180), one loop, frames
A, B = 44, 67                                   # 67 matches 44, so the sway loops seamlessly
SEQ = [round(A + (B - A) * k / N) for k in range(N)]
durs = [LOOP_MS // N] * N
K, RF, EYE_R = 0.40, 2.2, 49                    # magnifier strength (centre x1/(1-K)), reach, eye radius px
FADE = 14                                       # px faded at the video's right edge

def find_eyes(a):
    r, g, b, al = [a[..., k].astype(int) for k in range(4)]
    m = ndi.binary_opening((b > r + 50) & (b > g + 20) & (al > 200), iterations=2)
    dark = (r + g + b < 150) & (al > 200)       # pupil
    lab, n = ndi.label(m)
    eyes = []
    for k, sl in enumerate(ndi.find_objects(lab), 1):
        y0, x0 = sl[0].start, sl[1].start
        h, w = sl[0].stop - y0, sl[1].stop - x0
        if 380 < y0 < 600 and 200 < x0 < 720 and 80 < w < 150 and 30 < h < 110:
            reg = ndi.binary_fill_holes(ndi.binary_closing((lab[sl] == k) | dark[sl], iterations=6))
            ys, xs = np.nonzero(reg)
            eyes.append((x0 + xs.mean(), y0 + ys.mean()))
    assert len(eyes) == 2, eyes
    return sorted(eyes)

def bulge(a, eyes):
    H, Wd = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:Wd].astype(np.float32)
    sx, sy = xx.copy(), yy.copy()
    R = EYE_R * RF
    for cx, cy in eyes:
        dx, dy = xx - cx, yy - cy
        d = np.sqrt(dx*dx + dy*dy) / R
        f = np.where(d < 1, 1 - K * (1 - d*d)**2, 1)
        sx = np.where(d < 1, cx + dx * f, sx); sy = np.where(d < 1, cy + dy * f, sy)
    out = np.stack([ndi.map_coordinates(a[..., c].astype(np.float32), [sy, sx], order=1) for c in range(4)], -1)
    return out

raw = {i: np.asarray(Image.open(f"{SRC}/{i:03d}.png")) for i in range(A - 1, B + 2)}
pos = {i: np.array(find_eyes(raw[i])) for i in raw}
src = {}
for i in set(SEQ):
    eyes = (pos[i - 1] + pos[i] + pos[i + 1]) / 3    # smoothed so the eyes don't jitter
    a = bulge(raw[i], eyes)
    ramp = np.clip((a.shape[1] - 1 - np.arange(a.shape[1])) / FADE, 0, 1)
    a[..., 3] *= ramp[None, :]
    src[i] = Image.fromarray(np.clip(a, 0, 255).round().astype(np.uint8), 'RGBA')

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
print('frames', SEQ)
save(f180, f"{OUT}/please.png", durs, 4)                      # 1 s x 4 = 4 s
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-please.png", durs, 0)
