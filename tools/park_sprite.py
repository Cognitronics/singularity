import math,random
from PIL import Image,ImageDraw
W,H=288,144
# park grid: gx 1..9, gy 13..20 ; canvas coords: u=(gx+gy)*19-265, v=(gx-gy)*9.5+181
def to_uv(gx,gy): return ((gx+gy)*19-265,(gx-gy)*9.5+181)
def to_g(u,v): s=(u+265)/19;d=(v-181)/9.5;return ((s+d)/2,(s-d)/2)
corners=[to_uv(1,13),to_uv(9,13),to_uv(9,20),to_uv(1,20)]
def inside(gx,gy): return 1<=gx<=9 and 13<=gy<=20
rnd=random.Random(5)
GR=[(74,118,58),(88,136,66),(104,152,76)];MEAD=(126,170,88);PATH=(196,182,140);WALL=(120,112,100)
WAT=[(40,86,140),(58,112,170),(120,170,210)];TREE=[(34,70,40),(50,100,52),(78,132,64),(120,168,84)]
im=Image.new('RGB',(W,H),(20,24,30));px=im.load()
def water(gx,gy):
  # Reservoir (north, gy 17.3-19.3) and The Lake (south-west)
  r1=((gx-5.0)/2.1)**2+((gy-18.4)/1.0)**2
  r2=((gx-3.0)/1.1)**2+((gy-14.6)/.55)**2+.25*math.sin(gx*5)
  return r1<1 or r2<1, r1, r2
def meadow(gx,gy): return ((gx-6.4)/1.4)**2+((gy-14.4)/.9)**2<1 or ((gx-6.8)/1.0)**2+((gy-16.3)/.6)**2<1
def path(gx,gy):
  e=min(gx-1,9-gx,gy-13,20-gy)
  if .12<e<.24: return True                          # perimeter path inside the wall
  if abs(gx-5.0-0.35*math.sin(gy*1.3))<.07 and gy<17.1: return True   # the Mall / east drive
  if abs(gy-16.8-0.25*math.sin(gx*1.7))<.06: return True           # transverse road
  if abs(gx-2.2-0.3*math.sin(gy*2.1))<.06 and 15.2<gy<17: return True
  return False
for v in range(H):
  for u in range(W):
    gx,gy=to_g(u+.5,v+.5)
    if not inside(gx,gy): continue
    e=min(gx-1,9-gx,gy-13,20-gy)
    if e<.1: px[u,v]=WALL;continue
    w,r1,r2=water(gx,gy)
    if w:
      rr=min(r1,r2);px[u,v]=WAT[2] if (rnd.random()<.035 and rr<.75) else WAT[1] if rr<.75 else WAT[0];continue
    if path(gx,gy): px[u,v]=PATH;continue
    if meadow(gx,gy): px[u,v]=MEAD;continue
    px[u,v]=GR[(int(gx*7)+int(gy*5)+rnd.randint(0,2))%3 if rnd.random()<.25 else 1]
# trees: round canopies with shadow, avoid water/meadow/paths
d=ImageDraw.Draw(im)
trees=[]
for i in range(900):
  gx=rnd.uniform(1.25,8.75);gy=rnd.uniform(13.25,19.75)
  w,_,_=water(gx,gy)
  if w or meadow(gx,gy) or path(gx,gy): continue
  dens=.55+.45*math.sin(gx*1.9)*math.cos(gy*1.3)
  if gy>15.2 and gy<16.6 and 2.5<gx<5: dens+=.4   # the Ramble: dense woods
  if rnd.random()>dens: continue
  trees.append((gx,gy))
trees.sort(key=lambda t:-(t[0]-t[1]))  # back to front
trees=trees[::-1]
trees.sort(key=lambda t:(t[0]-t[1]))
for gx,gy in trees:
  u,v=to_uv(gx,gy);r=rnd.choice([2,2,3,3,4])
  d.ellipse([u-r+1,v-r//2+1,u+r+2,v+r//2+2],fill=(40,60,34))
  d.ellipse([u-r,v-r*1.6,u+r,v+r*.4-1],fill=TREE[0]);d.ellipse([u-r+.5,v-r*1.6,u+r-1,v],fill=TREE[1])
  d.ellipse([u-r+1,v-r*1.5,u+r-2,v-r*.6],fill=TREE[2]);d.point((u-1,v-r*1.2),fill=TREE[3])
im.save('base.png');im.resize((W*3,H*3),Image.NEAREST).save('base_big.png')
mask=Image.new('L',(W,H),0);ImageDraw.Draw(mask).polygon(corners,fill=255);mask.save('mask.png')
print(corners)
