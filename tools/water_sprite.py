"""Seamless animated water texture for the sea around Manhattan.
Writes sprites/water.png: 8 frames of 192x96 side by side (1536x96).
Mostly transparent: it is laid over the weather-dependent water gradient in frame().
Each wave is a short crest on the isometric diagonal (2 px right, 1 px up) with a dark trough
below it; crests rise, drift a little and fade, each with its own phase."""
import math,random,sys
from PIL import Image
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
TW,TH,NF=192,96,8
LO,MID,HI,GLINT=(38,66,90),(56,92,120),(96,138,166),(160,200,222);TROUGH=(6,14,22)
rnd=random.Random(1929)
waves=[]
for cy in range(0,TH,16):
  for cx in range(0,TW,32):
    waves.append(dict(x=cx+rnd.randrange(0,26),y=cy+rnd.randrange(0,12),L=rnd.choice([2,2,3,3,4]),ph=rnd.random(),big=rnd.random()<.2))
sheet=Image.new('RGBA',(TW*NF,TH),(0,0,0,0))
for f in range(NF):
  fr=Image.new('RGBA',(TW,TH),(0,0,0,0));px=fr.load()
  def put(x,y,c,a):
    x%=TW;y%=TH
    if px[x,y][3]<a: px[x,y]=c+(a,)
  for w in waves:
    t=(f/NF+w['ph'])%1;life=math.sin(t*math.pi)
    if life<.6: continue   # each crest is only visible for part of its cycle
    sx=w['x']+int(t*4)*2;sy=w['y']-int(t*4)     # drift along the diagonal
    col=HI if life>.8 else MID if life>.45 else LO;a=int(110+140*life)
    for i in range(w['L']):
      x=sx+i*2;y=sy-i
      put(x,y,col,a);put(x+1,y,col,a)
      put(x,y+1,TROUGH,int(90*life));put(x+1,y+1,TROUGH,int(90*life))
    if w['big'] and life>.85: put(sx+w['L'],sy-w['L']//2,GLINT,240)
  sheet.paste(fr,(f*TW,0))
sheet.save(f'{OUT}/water.png');print('ok')
