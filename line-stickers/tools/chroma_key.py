"""Remove the green screen from Kling frames.

usage: python3 -I chroma_key.py RAW_DIR KEY_DIR [MIN_SPECK_PX=150]
Use MIN 40 when the clip has small hearts, sparkles or sweat drops."""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cut_stickers import cut
from PIL import Image
from scipy import ndimage as ndi
src, dst = sys.argv[1], sys.argv[2]
MIN = int(sys.argv[3]) if len(sys.argv) > 3 else 150
for f in sorted(os.listdir(src)):
    im, _, _ = cut(os.path.join(src, f))
    a = np.asarray(im).astype(np.float32).copy()
    r, g, b, al = a[...,0], a[...,1], a[...,2], a[...,3]
    al[(g - np.maximum(r, b) > 35) & (g > 110)] = 0
    lab, n = ndi.label(al > 0)
    if n:
        sizes = ndi.sum(np.ones_like(al), lab, range(1, n+1))
        for i, s in enumerate(sizes, 1):
            if s < MIN: al[lab == i] = 0
    a[...,1] = np.minimum(g, np.maximum(r, b) + 10)
    Image.fromarray(a.round().astype(np.uint8), 'RGBA').save(os.path.join(dst, f))
