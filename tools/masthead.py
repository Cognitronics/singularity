"""Pixel-art masthead for the in-game newspaper "The Manhattan Ether".
160x52 image (shown at 3x): double rules, tiny THE, title in a hand-made bold serif pixel font,
an ink skyline (Liberty, Empire State, Chrysler) with a cyan/violet ether glow behind it."""
import random,sys
from PIL import Image
OUT=sys.argv[1] if len(sys.argv)>1 else 'masthead.png'
W,H=160,52;INK=(29,27,23,255);CY=(47,138,150,255);VI=(110,79,168,255);WIN=(233,227,211,255)
im=Image.new('RGBA',(W,H),(0,0,0,0));px=im.load()
def put(x,y,c):
  if 0<=x<W and 0<=y<H: px[x,y]=c
G={
'M':["##.....##",".##...##.",".###.###.",".#######.",".##.#.##.",".##...##.",".##...##.",".##...##.",".##...##.",".##...##.","###...###"],
'A':["...##...","..####..","..####..",".##..##.",".##..##.",".##..##.",".######.",".######.",".##..##.",".##..##.","###..###"],
'N':["##....###",".##....#.",".###...#.",".####..#.",".##.##.#.",".##..###.",".##...##.",".##....#.",".##....#.",".##....#.","###...###"],
'H':["###..###",".##..##.",".##..##.",".##..##.",".######.",".######.",".##..##.",".##..##.",".##..##.",".##..##.","###..###"],
'T':["########","########","#..##..#","...##...","...##...","...##...","...##...","...##...","...##...","..####..","..####.."],
'E':["#######.",".##...#.",".##.....",".##..#..",".#####..",".#####..",".##..#..",".##.....",".##...#.",".##...#.","#######."],
'R':["######..",".##..##.",".##..##.",".##..##.",".#####..",".####...",".##.##..",".##..##.",".##..##.",".##..##.","###..###"]}
TINY={'T':["###",".#.",".#.",".#.",".#."],'H':["#.#","#.#","###","#.#","#.#"],'E':["###","#..","##.","#..","###"]}
def text(s,font,y,gap,space):
  w=sum((len(font[ch][0])+gap) if ch!=' ' else space for ch in s)-gap;x=(W-w)//2
  for ch in s:
    if ch==' ': x+=space;continue
    for j,row in enumerate(font[ch]):
      for i,v in enumerate(row):
        if v=='#': put(x+i,y+j,INK)
    x+=len(font[ch][0])+gap
for x in range(W): put(x,0,INK);put(x,2,INK);put(x,H-3,INK);put(x,H-1,INK)
text('THE',TINY,4,1,3);text('MANHATTAN ETHER',G,10,1,6)
# ether glow behind the skyline: dithered cyan core, violet fringe
for y in range(23,49):
  for x in range(W):
    d=((x-W/2)/58)**2+((y-48)/24)**2      # half-ellipse of ether light rising behind the skyline
    if d<.35 and (x+y)%2==0: put(x,y,CY)
    elif d<.6 and (x*3+y)%4==0: put(x,y,CY)
    elif d<.95 and (x+2*y)%5==0: put(x,y,VI)
# skyline silhouette
r=random.Random(7);top=[49]*W;x=0
while x<W:
  w=r.randint(3,7);h=r.randint(3,9)
  for i in range(w): top[min(W-1,x+i)]=49-h
  x+=w+r.choice([0,0,1])
def tower(cx,w,h,spire):
  for i in range(-w//2,w-w//2): top[cx+i]=min(top[cx+i],49-h)
  for k in range(spire): put(cx,49-h-1-k,INK)
tower(62,7,15,0);tower(62,5,19,0);tower(62,3,22,5)          # Empire State: stepped + mast
tower(98,6,14,0);tower(98,4,17,0);tower(98,2,19,5)          # Chrysler: crown + needle
tower(40,5,12,0);tower(122,5,13,2);tower(80,6,10,0);tower(140,4,11,0)
for x in range(W):
  for y in range(top[x],50): put(x,y,INK)
for x in range(W):                         # lit windows
  for y in range(top[x]+2,48,2):
    if x%2==0 and r.random()<.18: put(x,y,WIN)
# Liberty on the left: pedestal + figure + torch
for y in range(41,50):
  for i in range(7,14): put(i,y,INK)
for y in range(32,41): put(10,y,INK);put(11,y,INK)
put(9,34,INK);put(12,29,INK);put(12,30,INK);put(12,31,INK);put(12,28,CY);put(11,27,CY);put(10,31,INK);put(11,31,INK);put(10,30,INK)
im.save(OUT);im.resize((W*4,H*4),Image.NEAREST).save(OUT.replace('.png','_big.png'));print('ok')
