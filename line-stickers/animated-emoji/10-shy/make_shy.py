"""Shy >///< emoji: Kling wiggle loop, no overlay."""
import sys, os
from PIL import Image
CUT, OUT = sys.argv[1], sys.argv[2]            # folder of 16 green-removed frames, output folder
N, W = 16, 540                                  # frames, working canvas (3x of 180)
frames = [Image.open(f"{CUT}/{k:02d}.png") for k in range(N)]
box = (20, 149, 940, 902)                       # union bbox; the bottom edge is the flat cut
s = (W - 12) / (box[2] - box[0])               # fill the width
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)
cx, cy = (W-cw)//2, W-6-ch                      # centered, flat cut on the bottom edge

out = []
for f in frames:
    c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
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
save(f180, f"{OUT}/shy.png", [62, 63]*8, 4)                  # one wiggle per second, 4 loops = 4 s
save([o.convert('RGBa').resize((360, 360), Image.LANCZOS).convert('RGBA') for o in out],
     f"{OUT}/preview-shy.png", [62, 63]*8, 0)
