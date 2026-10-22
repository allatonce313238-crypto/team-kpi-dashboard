import sys, os, numpy as np
from PIL import Image
from scipy import ndimage as ndi

def cut(path):
    rgb = np.asarray(Image.open(path).convert('RGB')).astype(np.float32)
    r,g,b = rgb[...,0], rgb[...,1], rgb[...,2]
    spill = g - np.maximum(r,b)
    green = (spill > 60) & (g > 120)
    lab, n = ndi.label(green, structure=np.ones((3,3)))
    H,W = green.shape
    border = set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]]))) - {0}
    white = (rgb.min(axis=2) > 200)
    bg = np.zeros_like(green)
    objs = ndi.find_objects(lab)
    for i,sl in enumerate(objs, 1):
        if sl is None: continue
        if i in border:
            bg |= lab == i; continue
        y0,y1 = max(sl[0].start-3,0), min(sl[0].stop+3,H)
        x0,x1 = max(sl[1].start-3,0), min(sl[1].stop+3,W)
        m = lab[y0:y1,x0:x1] == i
        ring = ndi.binary_dilation(m, iterations=3) & ~ndi.binary_dilation(m, iterations=1)
        ring &= ~green[y0:y1,x0:x1]
        if ring.sum() and white[y0:y1,x0:x1][ring].mean() > 0.5:
            bg[y0:y1,x0:x1] |= m
    K = np.median(rgb[bg], axis=0)
    spillK = K[1] - max(K[0],K[2])
    alpha = np.ones((H,W), np.float32)
    alpha[bg] = 0
    edge = ndi.binary_dilation(bg, iterations=2) & ~bg
    a = np.clip(1 - spill/spillK, 0, 1)
    alpha[edge] = np.minimum(alpha[edge], a[edge])
    out = rgb.copy()
    ae = np.maximum(alpha, 1e-3)[...,None]
    unmixed = np.clip((rgb - (1-ae)*K)/ae, 0, 255)
    out[edge] = unmixed[edge]
    # despill any remaining green tint on edge pixels
    out[...,1][edge] = np.minimum(out[...,1][edge], np.maximum(out[...,0],out[...,2])[edge] + 10)
    alpha[alpha < 0.08] = 0
    rgba = np.dstack([out, alpha*255]).round().astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA'), int(bg.sum()), n

def fit(im, maxw, maxh, margin):
    im = im.crop(im.getbbox())
    s = min((maxw-2*margin)/im.width, (maxh-2*margin)/im.height)
    w,h = max(1,round(im.width*s)), max(1,round(im.height*s))
    im = im.convert('RGBa').resize((w,h), Image.LANCZOS).convert('RGBA')
    return im

def canvas(im, W, H):
    c = Image.new('RGBA', (W,H), (0,0,0,0))
    c.paste(im, ((W-im.width)//2, (H-im.height)//2))
    return c

def main():
  src, outdir = sys.argv[1], sys.argv[2]
  files = sys.argv[3:]
  os.makedirs(outdir, exist_ok=True)
  for idx,f in enumerate(files,1):
      full, nbg, n = cut(f)
      full.save(os.path.join(outdir, 'full_%02d.png'%idx))
      st = fit(full, 370, 320, 10)
      W = st.width + 20 + (st.width % 2); H = st.height + 20 + (st.height % 2)
      W, H = min(W,370), min(H,320)
      canvas(st, W, H).save(os.path.join(outdir, '%02d.png'%idx), optimize=True)
      if idx == int(src):
          canvas(fit(full,240,240,6),240,240).save(os.path.join(outdir,'main.png'), optimize=True)
          canvas(fit(full,96,74,2),96,74).save(os.path.join(outdir,'tab.png'), optimize=True)
      print(idx, os.path.basename(f), (W,H), 'components', n)

if __name__=='__main__':
    main()
