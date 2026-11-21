"""Sketch of the Brooklyn Bridge in the game's exact isometric geometry (2x logical scale).
Bridge runs along gx from 10 (Manhattan) to 14 (Brooklyn) at gy=3.5, towers at gx 11 and 13.
Canvas 192x160 = logical 96x80 with origin at logical (OX+246, OY+26).
The sketch is the init image for a PixelLab pass; the result is drawn 1:1 at half size."""
import math,sys
from PIL import Image,ImageDraw
OUT=sys.argv[1] if len(sys.argv)>1 else 'bridge_sketch.png'
S=2;W,H=192,160
def c(gx,gy,z): return (((gx+gy)*19-246)*S,((gx-gy)*9.5-z-26)*S)
im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
STONE_T,STONE_L,STONE_D,ARCH=(206,194,168),(176,162,136),(132,120,100),(36,32,28)
DECK_T,DECK_S,CABLE,LAMP=(98,92,84),(58,54,50),(222,214,196),(255,214,122)
Y0,Y1=3.36,3.64;DZ=9
def poly(pts,f): d.polygon([tuple(map(round,p)) for p in pts],fill=f)
def ln(a,b,f,w=1): d.line([tuple(map(round,a)),tuple(map(round,b))],fill=f,width=w)
def deck(x0,x1):
  poly([c(x0,Y0,DZ),c(x1,Y0,DZ),c(x1,Y1,DZ),c(x0,Y1,DZ)],DECK_T)
  poly([c(x0,Y0,DZ),c(x1,Y0,DZ),c(x1,Y0,DZ-2.5),c(x0,Y0,DZ-2.5)],DECK_S)
  for k in range(0,17):                       # truss pattern on the deck side
    x=x0+(x1-x0)*k/16;ln(c(x,Y0,DZ),c(x,Y0,DZ-2.5),(40,36,34))
  for k in range(1,8):                        # lamps along the walkway
    x=x0+(x1-x0)*k/8;p=c(x,3.5,DZ+.6);d.point((round(p[0]),round(p[1])),fill=LAMP)
def cable_z(gx):
  if gx<=11: return DZ+1+(gx-10)*(30-DZ-1)    # land span: straight up to the tower top
  if gx>=13: return 30-(gx-13)*(30-DZ-1)
  t=(gx-11)/2;return 30-16*(1-(2*t-1)**2)     # main span sag
def cables(gy,front):
  pts=[c(10+i*.02,gy,cable_z(10+i*.02)) for i in range(201)]
  d.line([tuple(map(round,p)) for p in pts],fill=CABLE,width=1)
  for k in range(1,40):                       # vertical suspenders
    gx=10+k*.1
    if abs(gx-11)<.12 or abs(gx-13)<.12: continue
    ln(c(gx,gy,cable_z(gx)),c(gx,gy,DZ),(170,164,150) if front else (120,116,108))
  for t in (11,13):                           # diagonal stays fanning from the tower tops
    for k in (-.9,-.6,-.3,.3,.6,.9):
      ln(c(t,gy,29),c(t+k,gy,DZ),(150,144,132) if front else (110,106,98))
def tower(x):
  x0,x1=x-.11,x+.11;z1=31
  poly([c(x1,Y0,0),c(x1,Y1,0),c(x1,Y1,z1),c(x1,Y0,z1)],STONE_L)      # face toward Brooklyn (visible)
  poly([c(x0,Y0,0),c(x1,Y0,0),c(x1,Y0,z1),c(x0,Y0,z1)],STONE_D)      # south face
  poly([c(x0,Y0,z1),c(x1,Y0,z1),c(x1,Y1,z1),c(x0,Y1,z1)],STONE_T)    # top
  for gy0,gy1 in ((Y0+.03,3.47),(3.53,Y1-.03)):                       # two gothic arches
    zb,zt=DZ-1,23
    pts=[c(x1,gy0,zb),c(x1,gy1,zb),c(x1,gy1,zt-3),c(x1,(gy0+gy1)/2,zt),c(x1,gy0,zt-3)]
    poly(pts,ARCH)
  ln(c(x1,Y0,z1-2),c(x1,Y1,z1-2),STONE_T)                             # cornice
  ln(c(x0,Y0,z1-2),c(x1,Y0,z1-2),STONE_L)
cables(Y1-.02,False)                 # far cable behind
deck(10,11.0);deck(11.0,13.0);deck(13.0,14)
tower(11);tower(13)
cables(Y0+.02,True)                  # near cable in front
im.save(OUT);im.resize((W*4,H*4),Image.NEAREST).save(OUT.replace('.png','_big.png'));print('ok')
