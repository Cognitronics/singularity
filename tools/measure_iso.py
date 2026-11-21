"""Measure how straight the isometric angle of building images is.
Prints per image: base slope left/right and Lshare (share of base width left of the front corner; 0.50 = perfect)."""
import sys
from PIL import Image
import numpy as np
for f in sys.argv[1:]:
  a=np.array(Image.open(f).convert('RGBA'))[:,:,3]>40;H,W=a.shape
  ys,xs=np.nonzero(a);by=ys.max();bx=xs[ys==by].mean()
  low=ys>ys.min()+(by-ys.min())*0.55;lx=xs[low].min();ly=ys[low][xs[low]==lx].mean();rx=xs[low].max();ry=ys[low][xs[low]==rx].mean()
  ls=(bx-lx)/(rx-lx);ok='OK' if abs(ls-.5)<=.06 else 'SCHIEF'
  print("%-24s slopeL %.2f slopeR %.2f Lshare %.2f %s"%(f.split('/')[-1],(by-ly)/max(1,bx-lx),(by-ry)/max(1,rx-bx),ls,ok))
