"""Manhattan street ground sprite (all land tiles except Central Park).
Same geometry as the procedural ground in index.html: asphalt across the whole tile,
sidewalk ring between .13 and .22, block (under the building) from .22 to .78.
Writes sprites/ground.png (colours already night-graded, the game draws it ungraded)
and sprites/ground_side.png (white sidewalk mask, tinted cyan at runtime by Control)."""
import math,random,sys
from PIL import Image
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
SW=float(sys.argv[2]) if len(sys.argv)>2 else .13   # asphalt half-width per tile edge (V1 .13)
BK=float(sys.argv[3]) if len(sys.argv)>3 else .22   # block starts here (V1 .22)
FOAM_ON=(sys.argv[4]!='nofoam') if len(sys.argv)>4 else True
TW,TH=19,9.5
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
RC=.38  # coast corner rounding radius (tile units)
def coast_cut(tx,ty,fx,fy):
  """True if this point of a land tile is cut away by a rounded coastal corner."""
  for cx,cy in ((0,0),(1,0),(0,1),(1,1)):
    nx=tx+(1 if cx else -1);ny=ty+(1 if cy else -1)
    if district(nx,ty) is None and district(tx,ny) is None:
      if abs(fx-cx)<RC and abs(fy-cy)<RC:
        ox=RC if cx==0 else 1-RC;oy=RC if cy==0 else 1-RC
        if math.hypot(fx-ox,fy-oy)>RC: return True
  return False
def battery(gx,gy): return -0.75<=gy<0.05 and math.hypot((gx-4.5)/1.6,(gy-0.05)/0.8)<1
PIERS=[(-0.9,0,y+0.38,y+0.6) for y in range(4,13)]+[(6.9,7.6,1.38,1.58),(7.9,8.6,2.38,2.58),(8.9,9.5,3.4,3.6)]  # South Street Seaport piers on the East River
def pier(gx,gy): return any(a<=gx<=b and c<=gy<=d for a,b,c,d in PIERS)
def land_pt(gx,gy):
  tx,ty=math.floor(gx),math.floor(gy);dd=district(tx,ty)
  if dd is not None: return not coast_cut(tx,ty,gx-tx,gy-ty)
  return battery(gx,gy) or pier(gx,gy)
def night(c):
  r,g,b=c;l=.3*r+.59*g+.11*b;r=r*.45+l*.55;g=g*.45+l*.55;b=b*.45+l*.55+6
  return tuple(max(0,min(255,round(v*.57))) for v in (r,g,b))
hx=lambda h:tuple(int(h[i:i+2],16) for i in (1,3,5))
ASPH=[night(hx(c)) for c in ('#55555a','#5a5a5e','#606064')]
TRACK=night(hx('#4c4c50'));SIDE=[night(hx(c)) for c in ('#c4beb2','#d0cabe','#aea89c')]
GRASS=[night(hx(c)) for c in ('#4f7a3e','#5a8a46')];PATHC=night(hx('#b8ae96'));TREEC=night(hx('#2e5a2c'));PIERW=night(hx('#8a7258'));PIERD=night(hx('#6a5644'))
CURB=night(hx('#3e3c3a'));BLOCK=night(hx('#4a4844'));CROSS=night(hx('#e8e2d4'));MAN=night(hx('#3a3a3e'))
DASH=hx('#d8c060');NEON=[hx('#f06a6a'),hx('#5fd4e0'),hx('#d070e0'),hx('#ffd27a')]
# image covers gx 0..10, gy 0..26: X=(gx+gy)*19 in [0,684], Y=(gx-gy)*9.5 in [-247,95]
OXI,OYI=-4,-252;W,H=692,352
img=Image.new('RGBA',(W,H),(0,0,0,0));side=Image.new('L',(W,H),0);px=img.load();sp=side.load()
rnd=random.Random(1920)
def land(x,y): return district(x,y) is not None
for v in range(H):
  for u in range(W):
    X=u+OXI+.5;Y=v+OYI+.5;s=X/TW;d=Y/TH;gx=(s+d)/2;gy=(s-d)/2
    tx,ty=math.floor(gx),math.floor(gy);dd=district(tx,ty)
    if dd is None:
      if battery(gx,gy):
        c=GRASS[1] if rnd.random()<.8 else GRASS[0]
        if abs(math.hypot((gx-4.5)/1.1,(gy+.1)/.5)-1)<.07: c=PATHC
        if rnd.random()<.06: c=TREEC
        px[u,v]=c+(255,)
      elif pier(gx,gy):
        e=min(abs(gx-a) for a,b,c2,d2 in PIERS for a in (a,b)) if False else 0
        px[u,v]=(PIERW if (int(gx*14)%2) else PIERD)+(255,)
      continue
    if dd=='park': continue
    fx,fy=gx-tx,gy-ty
    if coast_cut(tx,ty,fx,fy): continue
    e=min(fx,1-fx,fy,1-fy)
    if e>=BK: px[u,v]=BLOCK+(255,);continue
    if e>=SW:
      c=SIDE[0] if rnd.random()<.85 else SIDE[1] if rnd.random()<.5 else SIDE[2]
      # paving seams
      if abs((fx*12)%1-.5)<.06 and (fy<BK or fy>1-BK) or abs((fy*12)%1-.5)<.06 and (fx<BK or fx>1-BK): c=SIDE[2]
      if e<SW+.015: c=CURB
      px[u,v]=c+(255,);sp[u,v]=255;continue
    # street: asphalt with noise, tyre tracks, centre dashes, crosswalks, manholes
    c=ASPH[1] if rnd.random()<.8 else rnd.choice((ASPH[0],ASPH[2]))
    # which edge are we on?
    near=[(fx,'w'),(1-fx,'e'),(fy,'n'),(1-fy,'s')];near.sort();dist,side_=near[0]
    along=fy if side_ in 'we' else fx
    if SW*.38<dist<SW*.54 and .25<along<.75: c=TRACK
    # yellow centre dash on the tile border (only between two land tiles, not next to the park)
    nb={'w':(tx-1,ty),'e':(tx+1,ty),'n':(tx,ty-1),'s':(tx,ty+1)}[side_]
    nd=district(*nb)
    if dist<.025 and nd and nd!='park' and int(along*10)%3==1: c=DASH
    # crosswalk stripes where the street meets an intersection
    if (along<SW or along>1-SW) and dist<SW:
      pass
    elif SW<=along<=BK-.01 or 1-BK+.01<=along<=1-SW:
      if dist<SW-.01 and int(dist*40)%2==0: c=CROSS
    if rnd.random()<.0015: c=MAN
    if dd=='times' and rnd.random()<.04: c=tuple(int(a*.55+b*.45) for a,b in zip(c,rnd.choice(NEON)))   # neon reflections
    px[u,v]=c+(255,)
# surf: dotted light foam in the water right along Manhattan's shore (Central Park included)
FOAM=[(150,178,196),(110,140,162),(80,108,130)]
def landpx(u,v):
  X=u+OXI+.5;Y=v+OYI+.5;s_=X/TW;d_=Y/TH;gx=(s_+d_)/2;gy=(s_-d_)/2
  return land_pt(gx,gy)
LAND=[[landpx(u,v) for u in range(W)] for v in range(H)]
for v in range(H):
  for u in range(W):
    if LAND[v][u]: continue
    dmin=9
    for dy in range(-3,4):
      for dx in range(-5,6):
        uu,vv=u+dx,v+dy
        if 0<=uu<W and 0<=vv<H and LAND[vv][uu]: dmin=min(dmin,max(abs(dx)/2,abs(dy)))
    if not FOAM_ON: continue
    if dmin<=1.5 and (u*7+v*13)%5<3: px[u,v]=FOAM[0]+(200,)
    elif dmin<=2.5 and (u*5+v*11)%7<2: px[u,v]=FOAM[1]+(150,)
    elif dmin<=3 and (u*3+v*17)%11==0: px[u,v]=FOAM[2]+(120,)
img.save(f'{OUT}/ground.png')
sm=Image.new('RGBA',(W,H),(255,255,255,0));sm.putalpha(side);sm.save(f'{OUT}/ground_side.png')
print('ok',W,H)
