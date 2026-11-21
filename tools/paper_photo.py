"""Halftone (Bayer-dithered, 2 inks) newspaper photo: Manhattan skyline with a rift in the sky.
Writes paper_photo.png 160x64 (shown at 3x in the newspaper)."""
import random,sys,math
from PIL import Image
OUT=sys.argv[1] if len(sys.argv)>1 else 'paper_photo.png'
W,H=160,64;INK=(29,27,23,255);PAPER=(233,227,211,255)
B=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
tone=[[0.0]*W for _ in range(H)]            # 0 = paper, 1 = full ink
for y in range(H):
  for x in range(W): tone[y][x]=.2+.3*(y/H)  # sky: darker towards the horizon
# the rift: jagged bright crack with a soft halo
r=random.Random(3);cx=W*.62;pts=[]
x_=cx
for y in range(1,40):                       # zigzag crack, sampled per row
  x_+=r.choice([-3,-2,2,3]) if y%2==0 else 0;pts.append((x_,y))
for y in range(H):
  for x in range(W):
    d=min(abs(x-px_)+abs(y-py_)*2 for px_,py_ in pts)
    if d<1: tone[y][x]=0
    elif d<5: tone[y][x]=max(0,tone[y][x]-(1-d/5)*.3)
# skyline
r=random.Random(11);top=[H]*W;shade=[.8]*W;x=0
while x<W:
  w=r.randint(5,12);h=r.randint(10,26);s=r.choice([.9,1.0,1.0])
  for i in range(w):
    if x+i<W: top[x+i]=H-h;shade[x+i]=s if i<w-3 else .72
  x+=w
def tower(cx,w,h,sp):
  for i in range(-w//2,w-w//2): top[cx+i]=min(top[cx+i],H-h);shade[cx+i]=.72 if i<w//3 else 1.0
  for k in range(sp): top[cx]=min(top[cx],H-h-k)
tower(48,12,40,0);tower(48,8,46,0);tower(48,4,50,8)      # Empire State
tower(112,10,36,0);tower(112,6,41,0);tower(112,2,44,7)   # Chrysler
tower(80,9,30,0);tower(20,8,28,0);tower(140,9,32,0)
for x in range(W):
  for y in range(top[x],H): tone[y][x]=shade[x]
for x in range(W):                                        # windows (paper-white dots)
  for y in range(top[x]+3,H-2,3):
    if x%3==1 and r.random()<.35: tone[y][x]=.05
im=Image.new('RGBA',(W,H));px=im.load()
for y in range(H):
  for x in range(W): px[x,y]=INK if tone[y][x]*16>B[y%4][x%4]+.5 else PAPER
for x in range(W): px[x,0]=INK;px[x,H-1]=INK
for y in range(H): px[0,y]=INK;px[W-1,y]=INK
im.save(OUT);im.resize((W*4,H*4),Image.NEAREST).save(OUT.replace('.png','_big.png'));print('ok')
