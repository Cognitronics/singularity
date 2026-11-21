"""Install Higgsfield images into V2: crop to the opaque bbox, scale to WIDTH px, save as play2/sprites/<name>.png
and register the sprite in the V2_ART set of play2/index.html (so it skips the night filter).
usage: python3 install_v2.py <src_dir> <width> name1 name2 ...   (name like bld/harlem; source file <src_dir>/<basename>.png)"""
import sys,os,re
from PIL import Image
src,W,names=sys.argv[1],int(sys.argv[2]),sys.argv[3:]
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site','play2')
for n in names:
  im=Image.open(os.path.join(src,os.path.basename(n)+'.png')).convert('RGBA')
  a=im.split()[3].point(lambda v:255 if v>20 else 0);im=im.crop(a.getbbox())
  im=im.resize((W,round(im.height*W/im.width)),Image.LANCZOS)
  out=os.path.join(ROOT,'sprites',n+'.png');im.save(out,optimize=True);print(n,im.size)
p=os.path.join(ROOT,'index.html');s=open(p).read()
m=re.search(r"const V2_ART=new Set\(\[(.*?)\]\);",s);have=set(re.findall(r"'([^']+)'",m.group(1)))
allv=sorted(have|set(names));s=s[:m.start()]+"const V2_ART=new Set(["+",".join("'%s'"%x for x in allv)+"]);"+s[m.end():]
open(p,'w').write(s);print('V2_ART:',len(allv))
