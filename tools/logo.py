import math,random
from PIL import Image
W,H=88,40;CX,CY=W/2-.5,H/2-.5
px=[[None]*W for _ in range(H)]
def put(x,y,c):
  if 0<=x<W and 0<=y<H: px[y][x]=c
# ---- lemniscate ring ----
A,SY=41.5,1.12;pts=[]
for i in range(4000):
  t=i/4000*2*math.pi;d=1+math.sin(t)**2
  pts.append((CX+A*math.cos(t)/d,CY+SY*A*math.sin(t)*math.cos(t)/d))
CY_L={'hi':'#bff3f8','mid':'#5fd4e0','lo':'#2f8a96','edge':'#1d5a62'}
CY_R={'hi':'#d6c2fa','mid':'#b48ef0','lo':'#6e4fa8','edge':'#43306a'}
ring={}
for y in range(H):
  for x in range(W):
    d=min((x-a)**2+(y-b)**2 for a,b in pts[::3])**.5
    if d<=3.2: ring[(x,y)]=d
# ---- earths ----
random.seed(4)
def noise_field(seed,n=7):
  r=random.Random(seed);return [(r.uniform(-1,1),r.uniform(-1,1),r.uniform(.16,.34)) for _ in range(n)]
LAND={'L':noise_field(11,6),'R':noise_field(29,7)}
R=11.6;EL=(CX-12.2,CY);ER=(CX+12.2,CY)
OCEAN=['#173a6e','#235aa0','#3a82cc','#7cc0f0'];GRN=['#24502c','#3f8a3e','#77b85a','#b6dc8a'];CLOUD='#eef6f8'
def earth_px(x,y,c,key):
  dx,dy=(x-c[0])/R,(y-c[1])/R;rr=dx*dx+dy*dy
  if rr>1: return None
  dz=math.sqrt(1-rr)
  # light from the impact flash in the centre + a bit from above
  lx=1 if c[0]<CX else -1;L=(lx*.75,-.45,.5);n=math.sqrt(sum(v*v for v in L))
  b=max(0,(dx*L[0]+dy*L[1]+dz*L[2])/n)
  u=dx/(1+dz*.6);v=dy/(1+dz*.6)  # fake sphere mapping
  land=sum(math.exp(-((u-a)**2+(v-bb)**2)/(s*s)) for a,bb,s in LAND[key])
  cl=math.sin(u*9+key.__hash__()%5)*math.sin(v*14)>.93
  lvl=0 if b<.18 else 1 if b<.45 else 2 if b<.8 else 3
  if rr>.86: lvl=max(0,lvl-1)
  if cl and lvl>=1: return CLOUD if lvl>=2 else '#a8c4d0'
  return (GRN if land>.8 else OCEAN)[lvl]
for y in range(H):
  for x in range(W):
    for c,k in ((EL,'L'),(ER,'R')):
      e=earth_px(x,y,c,k)
      if e: put(x,y,e)
for y in range(H):
  for x in range(W):
    for c in (EL,ER):
      d=math.hypot(x-c[0],y-c[1])
      if R-.2<=d<R+.9 and px[y][x] is None: put(x,y,'#0c1830')
# ---- ring on top (outer arcs), but earths cover the inner arcs near the centre ----
def ring_col(x,y,d):
  pal=CY_L if x<CX else CY_R
  top=y<CY-2 or (y<CY+2 and abs(x-CX)<6)
  if d>2.4: return pal['edge']
  if y<CY-5: return pal['hi']
  if y>CY+5: return pal['lo']
  return pal['mid']
for (x,y),d in ring.items():
  inside_earth=any(((x-c[0])**2+(y-c[1])**2)<(R-.2)**2 for c in (EL,ER))
  if inside_earth: continue
  put(x,y,ring_col(x,y,d))
# ---- impact: flash, cracks, debris ----
FL=['#fff6d8','#ffd27a','#e0a43a','#c84a3a']
for y in range(H):
  for x in range(W):
    d=math.hypot((x-CX)*1.0,(y-CY)*1.25)
    if d<1.2: put(x,y,FL[0])
    elif d<2.3: put(x,y,FL[1])
    elif d<3.3 and px[y][x] in (None,)+tuple(OCEAN+GRN+[CLOUD,'#a8c4d0']): put(x,y,FL[2])
# glowing cracks running into both earths
for sgn in (-1,1):
  for path in ([(1,0),(1,-1),(1,0),(1,1),(1,0)],[(1,1),(1,1),(1,0)],[(1,-1),(1,-1),(1,0),(1,-1)]):
    x,y=int(CX+.5+sgn*4),int(CY+.5)
    for i,(ax,ay) in enumerate(path):
      x+=sgn*ax;y+=ay
      if px[y][x] in OCEAN+GRN+[CLOUD,'#a8c4d0']: put(x,y,FL[1] if i<2 else FL[2])
# debris shooting up and down out of the collision
for x,y,c in [(43,10,FL[1]),(44,7,FL[2]),(42,5,'#8a7a60'),(45,4,FL[1]),(41,2,FL[2]),(46,1,'#8a7a60'),
              (44,29,FL[1]),(43,32,FL[2]),(45,34,'#8a7a60'),(42,35,FL[1]),(46,37,FL[2]),(40,38,'#8a7a60'),
              (38,8,FL[2]),(50,9,FL[2]),(37,31,FL[2]),(51,30,FL[2])]:
  if px[y][x] is None: put(x,y,c)
# ---- outputs ----
def svg(vb):
  out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="352" height="{352*int(vb.split()[3])//88}" shape-rendering="crispEdges">']
  for y in range(H):
    x=0
    while x<W:
      c=px[y][x]
      if c is None: x+=1;continue
      x2=x
      while x2+1<W and px[y][x2+1]==c: x2+=1
      out.append(f'<rect x="{x}" y="{y}" width="{x2-x+1}" height="1" fill="{c}"/>');x=x2+1
  return ''.join(out)+'</svg>'
open('logo-mark.svg','w').write(svg('0 0 88 40'))
open('favicon.svg','w').write(svg('0 -24 88 88').replace('height="352"','height="352"'))
im=Image.new('RGBA',(W,H),(20,22,26,255))
for y in range(H):
  for x in range(W):
    if px[y][x]: im.putpixel((x,y),tuple(int(px[y][x][i:i+2],16) for i in (1,3,5))+(255,))
im.resize((W*8,H*8),Image.NEAREST).save('preview.png');im.resize((W//2,H//2),Image.BOX).resize((W*2,H*2),Image.NEAREST).save('preview_small.png')
print('ok')
