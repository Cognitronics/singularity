"""Three instability backgrounds from one PixelLab Brooklyn Bridge image (art/inst_ok.png):
inst_ok = untouched, inst_warn = far (right) end ghosted as if vibrating,
inst_crit = whole bridge smeared with ghost copies and a violet aura."""
import sys
from PIL import Image,ImageChops,ImageFilter
src,out=sys.argv[1],sys.argv[2]
base=Image.open(src).convert('RGB');W,H=base.size
base.save(f'{out}/inst_ok.png')
def ghost(img,shifts,mask):
  acc=img.copy()
  for (dx,dy),a in shifts:
    sh=ImageChops.offset(img,dx,dy);acc=Image.blend(acc,sh,a)
  return Image.composite(acc,img,mask)
# warn: ghosting ramps in from 35% of the width to full at the right edge
m=Image.new('L',(W,H))
for x in range(W): 
  v=max(0,min(255,int((x/W-.35)/.45*255)))
  for y in range(H): m.putpixel((x,y),v)
warn=ghost(base,[((2,0),.35),((-3,0),.3),((5,1),.2)],m)
warn.save(f'{out}/inst_warn.png')
# crit: everything smeared, then a violet glow around the bright parts
full=Image.new('L',(W,H),255)
crit=ghost(base,[((3,0),.4),((-4,0),.35),((7,1),.3),((-8,-1),.25),((0,2),.2)],full)
crit=crit.filter(ImageFilter.BoxBlur(1))
bright=crit.convert('L').point(lambda v:255 if v>85 else 0).filter(ImageFilter.GaussianBlur(5))
violet=Image.new('RGB',(W,H),(180,142,240))
crit=Image.composite(ImageChops.screen(crit,violet),crit,bright.point(lambda v:min(255,int(v*1.1))))
crit=Image.blend(crit,Image.new('RGB',(W,H),(96,44,160)),.34)
crit.save(f'{out}/inst_crit.png');print('ok')
