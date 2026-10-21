"""Thank you emoji: one bow from the Kling clip (upright -> bow -> upright), feet planted,
starting on the bow so LINE's still image shows it. No overlays."""
import sys, os
from PIL import Image
SRC, OUT = sys.argv[1], sys.argv[2]            # folder of green-removed video frames (NNN.png), output folder
W, LOOP_MS, N = 540, 2000, 20                   # working canvas (3x of 180), one loop, frames
A, B = 27, 71                                   # upright -> bow -> upright
SEQ = [round(A + (B - A) * k / N) for k in range(N)]
start = SEQ.index(min(SEQ, key=lambda f: abs(f - 50)))   # deepest bow
SEQ = SEQ[start:] + SEQ[:start]
durs = [LOOP_MS // N] * N
src = {i: Image.open(f"{SRC}/{i:03d}.png") for i in set(SEQ)}
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

f180 = [o.convert('RGBa').resize((180, 180), Image.LANCZOS).convert('RGBA') for o in out]
for i, f in enumerate(f180): f.save(f"{OUT}/frames/{i+1:02d}.png")
print('frames', SEQ)
save(f180, f"{OUT}/thank-you.png", durs, 2)                  # 2 s x 2 = 4 s
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-thank-you.png", durs, 0)
