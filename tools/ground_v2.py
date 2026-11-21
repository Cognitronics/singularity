"""V2 street ground: same geometry as ground_sprite.py (wide streets SW/BK), but surfaces are Higgsfield
textures projected isometrically (texture axes = map grid axes). Rendered at SCALE x (default 2).
usage: python3 ground_v2.py <texdir> <outdir> [scale]"""
import sys,math
import numpy as np
from PIL import Image
TEX,OUT=sys.argv[1],sys.argv[2];S=int(sys.argv[3]) if len(sys.argv)>3 else 2
SW,BK=.19,.27;TW,TH=19,9.5
ISLE=[[3,5],[2,6],[1,7],[1,8],[0,8],[0,9],[0,10],[0,10],[0,9],[0,9],[0,9],[0,9],[0,9],[1,8],[1,8],[1,8],[1,8],[1,8],[1,8],[1,8],[1,8],[1,8],[1,7],[2,7],[2,6],[3,6]]
def district(x,y):
  if y<0 or y>25: return None
  a,b=ISLE[y]
  if x<a or x>b: return None
  if y<=3: return 'fidi'
  if y<=7: return 'village' if x<5 else 'les'
  if y<=12: return 'hells' if x<3 else 'times' if x<=5 else 'midtown'
  if y<=19: return 'park'
  return 'harlem'
OXI,OYI=-4,-252;W,H=692*S,352*S
v,u=np.mgrid[0:H,0:W].astype(np.float32)
X=(u+.5)/S+OXI;Y=(v+.5)/S+OYI;s=X/TW;d=Y/TH;gx=(s+d)/2;gy=(s-d)/2
tx=np.floor(gx).astype(int);ty=np.floor(gy).astype(int);fx=gx-tx;fy=gy-ty
# tile tables (x -2..12, y -2..27)
X0,Y0=-2,-2;TWN,THN=15,30
code=np.zeros((THN,TWN),np.int8);cut=np.zeros((THN,TWN,4),bool)
for yy in range(THN):
  for xx in range(TWN):
    dd=district(xx+X0,yy+Y0)
    if dd is None: continue
    code[yy,xx]=2 if dd=='park' else (3 if dd=='times' else 1)
    for k,(cx_,cy_) in enumerate(((0,0),(1,0),(0,1),(1,1))):
      nx=xx+X0+(1 if cx_ else -1);ny=yy+Y0+(1 if cy_ else -1)
      cut[yy,xx,k]=district(nx,yy+Y0) is None and district(xx+X0,ny) is None
ix=np.clip(tx-X0,0,TWN-1);iy=np.clip(ty-Y0,0,THN-1);inside=(tx>=X0)&(tx<X0+TWN)&(ty>=Y0)&(ty<Y0+THN)
C=np.where(inside,code[iy,ix],0)
RC=.38;cutmask=np.zeros_like(C,bool)
for k,(cx_,cy_) in enumerate(((0,0),(1,0),(0,1),(1,1))):
  ox=RC if cx_==0 else 1-RC;oy=RC if cy_==0 else 1-RC
  near=(np.abs(fx-cx_)<RC)&(np.abs(fy-cy_)<RC)
  cutmask|=inside&cut[iy,ix,k]&near&(np.hypot(fx-ox,fy-oy)>RC)
street_land=(C==1)|(C==3)
land=street_land&~cutmask
battery=(C==0)&(gy>=-.75)&(gy<.05)&(np.hypot((gx-4.5)/1.6,(gy-.05)/.8)<1)
PIERS=[(-0.9,0,y+0.38,y+0.6) for y in range(4,13)]+[(6.9,7.6,1.38,1.58),(7.9,8.6,2.38,2.58),(8.9,9.5,3.4,3.6)]
pier=np.zeros_like(battery)
for a,b,c,e in PIERS: pier|=(C==0)&(gx>=a)&(gx<=b)&(gy>=c)&(gy<=e)
def tex(name,K,dark=1.0):
  t=np.asarray(Image.open(f'{TEX}/{name}.png').convert('RGB').resize((512,512),Image.LANCZOS)).astype(np.float32)
  tu=((gx*K)%512).astype(int);tv=((gy*K)%512).astype(int);return t[tv,tu]*dark
e=np.minimum(np.minimum(fx,1-fx),np.minimum(fy,1-fy))
img=np.zeros((H,W,4),np.float32)
asph=tex('tex_asphalt',190,.95);side=tex('tex_sidewalk',260,.85);cob=tex('tex_cobble',300,.75);grass=tex('tex_grass',160,1.0)
blk=land&(e>=BK);sw=land&(e>=SW)&(e<BK);st=land&(e<SW)
img[blk,:3]=cob[blk];img[sw,:3]=side[sw];img[st,:3]=asph[st]
curb=sw&(e<SW+.018);img[curb,:3]*=.45
# markings: yellow centre dashes between two street tiles, crosswalk stripes
fxw=np.stack([fx,1-fx,fy,1-fy]);dist=fxw.min(0);idx=fxw.argmin(0)
along=np.where(idx<2,fy,fx)
nbx=tx+np.array([-1,1,0,0])[idx];nby=ty+np.array([0,0,-1,1])[idx]
ncode=np.where((nbx>=X0)&(nbx<X0+TWN)&(nby>=Y0)&(nby<Y0+THN),code[np.clip(nby-Y0,0,THN-1),np.clip(nbx-X0,0,TWN-1)],0)
dash=st&(dist<.022)&((ncode==1)|(ncode==3))&((np.floor(along*10)%3)==1)
img[dash,:3]=img[dash,:3]*.35+np.array([216,192,96])*.65*.8
cw=st&(((along>=SW)&(along<=BK-.01))|((along>=1-BK+.01)&(along<=1-SW)))&(dist<SW-.01)&((np.floor(dist*40)%2)==0)
img[cw,:3]=img[cw,:3]*.45+np.array([200,196,184])*.55*.75
img[land,3]=255
# Battery Park: grass texture + curved path
img[battery,:3]=grass[battery];pth=battery&(np.abs(np.hypot((gx-4.5)/1.1,(gy+.1)/.5)-1)<.06);img[pth,:3]=side[pth]*.9;img[battery,3]=255
# piers: dark wet planks
pl=pier;img[pl,:3]=np.where(((np.floor(gx*14)%2)==0)[pl][:,None],np.array([82,66,50]),np.array([62,50,40]));img[pl,3]=255
Image.fromarray(img.clip(0,255).astype(np.uint8)).save(f'{OUT}/ground.png',optimize=True)
m=np.zeros((H,W,4),np.uint8);m[...,:3]=255;m[...,3]=np.where(sw,255,0);Image.fromarray(m).save(f'{OUT}/ground_side.png',optimize=True)
print('ok',W,H)
