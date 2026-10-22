import os, bisect
from PIL import Image, ImageDraw, ImageFont
names=['Hello','Good morning','Good night','On my way!','Working','Coffee break','Eating','Thinking',
'OK','No','Thank you','Sorry','Please','Good job','Roger','Stop!',
'Love','Blow kiss','Shy','LOL','Excited','Happy dance','Congrats','Proud','Sly smirk',
'Surprised','Confused','Sad','Crying','Tired','Scared','Disgusted','Angry',
'Fighting!','Block!','Hug','Mangkorn pile',"I'll carry it",'Training!','Magic lesson']
src='line-emoji-upload'; COLS,CW,CH,PAD=8,210,232,20; ROWS=5
W,H=COLS*CW+2*PAD, ROWS*CH+2*PAD
BG=(253,248,238,255); font=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf',17)
emo=[]
for i in range(40):
    im=Image.open(f'{src}/{i+1:03d}.png'); fr=[]; d=[]
    for k in range(im.n_frames): im.seek(k); fr.append(im.convert('RGBA')); d.append(im.info['duration'])
    cum=[]; s=0
    for x in d: s+=x; cum.append(s)
    emo.append((fr,cum))
base=Image.new('RGBA',(W,H),BG); dr=ImageDraw.Draw(base)
for i,n in enumerate(names):
    x=PAD+(i%COLS)*CW; y=PAD+(i//COLS)*CH
    t=f'{i+1:03d} {n}'; tw=dr.textlength(t,font=font); dr.text((x+(CW-tw)/2,y+190),t,fill=(70,60,50),font=font)
TICK=50; out=[]
for t in range(0,4000,TICK):
    f=base.copy()
    for i,(fr,cum) in enumerate(emo):
        k=min(bisect.bisect_right(cum,t%cum[-1]),len(fr)-1)
        f.alpha_composite(fr[k],(PAD+(i%COLS)*CW+(CW-180)//2, PAD+(i//COLS)*CH+5))
    out.append(f.convert('RGB'))
o='animated-emoji/all-40-animated'
out[0].save(o+'.webp',save_all=True,append_images=out[1:],duration=TICK,loop=0,quality=88,method=4)
out[0].save(o+'.gif',save_all=True,append_images=out[1:],duration=TICK,loop=0)
os.makedirs('/tmp/claude-0/-home-user-team-kpi-dashboard/a9a03ffe-ca8c-52f7-a0da-75638deed7be/scratchpad/ov',exist_ok=True)
for j,f in enumerate(out): f.save(f'/tmp/claude-0/-home-user-team-kpi-dashboard/a9a03ffe-ca8c-52f7-a0da-75638deed7be/scratchpad/ov/{j:03d}.png')
out[30].save('/tmp/claude-0/-home-user-team-kpi-dashboard/a9a03ffe-ca8c-52f7-a0da-75638deed7be/scratchpad/ov-still.png')
print(W,H,len(out))
