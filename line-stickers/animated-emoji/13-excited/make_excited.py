"""Excited emoji: two jumps from the Kling clip (frames 16-56, which end where they start). 20 frames are
picked evenly by amount of motion, and each shows for as long as the video takes to reach
the next one, so fast moves stay smooth. The floor shadow and specks are removed."""
import sys, os
from PIL import Image
SRC, OUT = sys.argv[1], sys.argv[2]            # folder of green-removed video frames (NNN.png), output folder
W, LOOP_MS, END = 540, 1000, 56                 # working canvas (3x of 180), one loop = two jumps (1.7x speed), loop end
SEQ = [16, 19, 23, 25, 26, 28, 29, 32, 33, 35, 36, 39, 43, 45, 46, 47, 49, 51, 53, 54]
gaps = [(SEQ[k+1] if k+1 < len(SEQ) else END) - SEQ[k] for k in range(len(SEQ))]
durs = [round(g * LOOP_MS / sum(gaps)) for g in gaps]
durs[-1] += LOOP_MS - sum(durs)
src = {i: Image.open(f"{SRC}/{i:03d}.png") for i in SEQ}
bbs = [f.getbbox() for f in src.values()]
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
print('ms', durs)
save(f180, f"{OUT}/excited.png", durs, 4)                     # 1 s x 4 = 4 s
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-excited.png", durs, 0)
