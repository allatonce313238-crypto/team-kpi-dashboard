import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
def strip(path):
    a=np.asarray(Image.open(path).convert('RGBA')).astype(np.float32)
    rgb=a[...,:3]; al=a[...,3]
    mn=rgb.min(2); mx=rgb.max(2)
    whitish=(mn>150)&((mx-mn)<70)
    trans=al<128
    region=trans|whitish
    lab,_=ndi.label(region,structure=np.ones((3,3)))
    seeds=np.unique(lab[trans]); seeds=seeds[seeds>0]
    rem=np.isin(lab,seeds)&~trans          # whitish pixels connected to transparency
    newal=al.copy(); newal[rem]=0; newal[trans&whitish]=0
    # soften the grey anti-alias pixels between removed white and the black line
    edge=ndi.binary_dilation(rem|trans,iterations=1)&~(rem|trans)
    L=rgb.mean(2)
    soft=np.clip((235-L)/(235-60),0,1)
    newal[edge]=np.minimum(newal[edge],255*soft[edge])
    newal[newal<20]=0
    out=np.dstack([rgb,newal]).round().astype(np.uint8)
    return Image.fromarray(out,'RGBA'), int(rem.sum())
if __name__=='__main__':
    im,n=strip(sys.argv[1]); im.save(sys.argv[2]); print(sys.argv[1].split('/')[-1],'removed px',n)
