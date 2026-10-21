"""Shy >///< emoji: Kling wiggle loop + pixel-art >///< speech bubble."""
import sys, os
from PIL import Image, ImageDraw
CUT, OUT = sys.argv[1], sys.argv[2]            # folder of 16 green-removed frames, output folder
N, W = 16, 540                                  # frames, working canvas (3x of 180)
INK, WHITE, PINK = (42, 26, 58, 255), (255, 255, 255, 255), (232, 69, 122, 255)
frames = [Image.open(f"{CUT}/{k:02d}.png") for k in range(N)]
box = (20, 149, 940, 902)                       # union bbox; the bottom edge is the flat cut
s = 0.53
cw, ch = round((box[2]-box[0])*s), round((box[3]-box[1])*s)
cx, cy = (W-cw)//2, W-6-ch                      # centered, flat cut on the bottom edge

GLYPH = {'>': ["100", "010", "001", "010", "100"],
         '<': ["001", "010", "100", "010", "001"],
         '/': ["001", "001", "010", "100", "100"]}

def bubble(k):
    """Speech bubble on the 180px grid, scaled up 3x so it stays crisp."""
    lo = Image.new('RGBA', (W//3, W//3), (0, 0, 0, 0)); g = ImageDraw.Draw(lo)
    dy = -1 if (k // 4) % 2 else 0              # tiny bob
    x0, y0, x1, y1 = 104, 3+dy, 177, 33+dy
    g.polygon([(112, y1-2), (124, y1-2), (102, y1+12)], fill=INK)                  # tail
    g.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=INK)
    g.rounded_rectangle([x0+2, y0+2, x1-2, y1-2], radius=8, fill=WHITE)
    g.polygon([(114, y1-3), (121, y1-3), (106, y1+7)], fill=WHITE)
    px = 3                                       # glyph pixel size
    tx, ty = x0 + (x1-x0 - (5*3*px + 4*3))//2, y0 + (y1-y0 - 5*px)//2 + 1
    for ch_ in ">///<":
        for r, row in enumerate(GLYPH[ch_]):
            for c, bit in enumerate(row):
                if bit == '1': g.rectangle([tx+c*px, ty+r*px, tx+c*px+px-1, ty+r*px+px-1], fill=PINK)
        tx += 3*px + 3
    return lo.resize((W, W), Image.NEAREST)

out = []
for k, f in enumerate(frames):
    c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    m = f.crop(box).convert('RGBa').resize((cw, ch), Image.LANCZOS).convert('RGBA')
    c.alpha_composite(m, (cx, cy)); c.alpha_composite(bubble(k)); out.append(c)

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
