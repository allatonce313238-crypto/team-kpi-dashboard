import numpy as np, cv2, math, sys
from PIL import Image, ImageDraw
S=sys.argv[1]
base=Image.open(f"{S}/base.png").convert('RGBA'); N=base.width
poly=[(8,176),(13,159),(30,147),(55,140),(80,139),(97,146),(100,170),(101,203),(110,212),(111,240),(122,258),(128,288),(110,298),(88,296),(74,280),(54,262),(42,250),(36,228),(16,204)]
m=Image.new('L',base.size,0); ImageDraw.Draw(m).polygon(poly,fill=255)
mask=np.asarray(m)>0
B=np.asarray(base).astype(np.uint8)
arm=B.copy(); arm[~mask]=0
# body: remove arm, inpaint the hole (colour and alpha) from surrounding pixels
hole=mask.astype(np.uint8)*255
pm=B.copy()
rgb=cv2.inpaint(pm[...,:3],hole,5,cv2.INPAINT_TELEA)
al=cv2.inpaint(pm[...,3],hole,5,cv2.INPAINT_TELEA)
from scipy import ndimage as ndi
near=ndi.binary_dilation((pm[...,3]>128)&~mask,iterations=6)
yy=np.arange(N)[:,None]*np.ones((1,N)); xx_=np.arange(N)[None,:]*np.ones((N,1))
al=np.where(mask,np.where(((al>128)&near)|((yy>268)&(xx_>60)),255,0),pm[...,3]).astype(np.uint8)   # behind the lower sleeve is body/cape
lab,n=ndi.label(al>0); sz=ndi.sum(al>0,lab,range(1,n+1))
al[np.isin(lab,1+np.flatnonzero(sz<200))]=0       # drop stray specks
rgb=rgb.astype(np.int16); g=rgb[...,1]; mx=np.maximum(rgb[...,0],rgb[...,2])
rgb[...,1]=np.where(g>mx+30,mx,g)                   # no green specks
body=np.dstack([rgb.astype(np.uint8),al])
Image.fromarray(body,'RGBA').save(f"{S}/max/body.png"); Image.fromarray(arm,'RGBA').save(f"{S}/max/arm.png")
PIV=(115,292)
def frame(t,amp=14,bob=2):
    k=(1-math.cos(2*math.pi*t))/2              # eased 0 -> 1 -> 0
    ang=-amp*k                                  # paw swings toward the face and back
    by=-bob*k                                   # tiny lift with the swing
    armI=Image.fromarray(arm,'RGBA').rotate(ang,resample=Image.BICUBIC,center=PIV)
    c=Image.new('RGBA',(N,N),(0,0,0,0))
    c.alpha_composite(Image.fromarray(body,'RGBA'),(0,round(by)))
    c.alpha_composite(armI,(0,round(by)))
    return c,ang
