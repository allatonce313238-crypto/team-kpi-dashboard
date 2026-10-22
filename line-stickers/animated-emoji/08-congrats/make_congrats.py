"""Congrats emoji: curled up hugging his chest (held still), then BURSTS open cheering with confetti.
Kling 3.0 start/end frames. The curl (1-33) has jittery feet and the burst (35-36) is a blurry smear,
so the curl is one held frame and the burst cuts straight to the open pose, which is then held still
(no arm waving). 2 s loop x 2.
Crop is set around Max (largest blob) so the confetti runs off the edges instead of shrinking him."""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
SRC, OUT = sys.argv[1], sys.argv[2]            # folder of green-removed video frames (NNN.png), output folder
W, LOOP_MS = 540, 2000                          # working canvas (3x of 180), one loop
CURL, HOLD, BACK = 19, 41, 34                   # still curl, held open pose (sharp, arms up), curl-back frame
SEQ = [CURL, 37, 38, 39, HOLD, BACK]
durs = [560, 60, 60, 60, 1080, 180]
durs[0] += LOOP_MS - sum(durs)
PAD = 8

src = {i: Image.open(f"{SRC}/{i:03d}.png") for i in set(SEQ)}

def max_box(im):
    a = ndi.binary_opening(np.asarray(im)[..., 3] > 0, iterations=8)   # cut confetti touching him
    lab, n = ndi.label(a)
    k = np.argmax(ndi.sum(a, lab, range(1, n + 1))) + 1
    ys, xs = np.nonzero(lab == k)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1

bbs = [max_box(src[i]) for i in src]
x0, y0 = min(b[0] for b in bbs) - PAD, min(b[1] for b in bbs) - PAD
x1, y1 = max(b[2] for b in bbs) + PAD, max(b[3] for b in bbs) + PAD
side = max(x1 - x0, y1 - y0)
cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
box = (cx - side // 2, cy - side // 2, cx - side // 2 + side, cy - side // 2 + side)

out = []
for i in SEQ:
    m = src[i].crop(box).convert('RGBa').resize((W, W), Image.LANCZOS).convert('RGBA')
    out.append(m)

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
print('box', box, 'frames', SEQ, durs)
save(f180, f"{OUT}/congrats.png", durs, 2)                    # 2 s x 2 = 4 s
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-congrats.png", durs, 0)
