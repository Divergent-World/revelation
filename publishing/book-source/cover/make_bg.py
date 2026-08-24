from PIL import Image, ImageDraw, ImageChops
import os, sys, json
Image.MAX_IMAGE_PIXELS=None
PAGES = int(sys.argv[1]) if len(sys.argv)>1 else 164
DPI=300; PT=DPI/72.0
TRIM_W, TRIM_H = 900.0, 765.0
WRAP = 35.748
SPINE = round(PAGES*0.006763*72, 3)
CW_PT = TRIM_W*2 + SPINE + WRAP*2
CH_PT = TRIM_H + WRAP*2
W,H = round(CW_PT*PT), round(CH_PT*PT)
NIGHT=(14,10,8)
front_x0 = round((WRAP+TRIM_W+SPINE)*PT); front_w = W-front_x0
src=Image.open("T3-T07.png").convert("RGB")
s=max(front_w/src.width, H/src.height)
im=src.resize((round(src.width*s),round(src.height*s)),Image.LANCZOS)
ox=round((im.width-front_w)*0.80); oy=round((im.height-H)*0.24)
im=im.crop((ox,oy,ox+front_w,oy+H))
def rh(fn):
    m=Image.new("L",(front_w,H)); d=ImageDraw.Draw(m)
    for x in range(front_w): d.line([(x,0),(x,H)],fill=int(255*fn(x/front_w)))
    return m
def rv(fn):
    m=Image.new("L",(front_w,H)); d=ImageDraw.Draw(m)
    for y in range(H): d.line([(0,y),(front_w,y)],fill=int(255*fn(y/H)))
    return m
gut=rh(lambda t: 0.16+0.52*min(1.0,(t/0.40)**0.85))
def vb(t):
    v=1.0
    if 0.24<t<0.52: v*=1.0-0.34*(1-abs(t-0.38)/0.14)**1.2
    if t>0.72:      v*=1.0-0.62*((t-0.72)/0.28)**1.4
    return max(0.05,v)
band=rv(vb)
vig=Image.new("L",(front_w,H),255); d3=ImageDraw.Draw(vig)
R=round(170*PT)
for i in range(R): d3.rectangle([i,i,front_w-1-i,H-1-i],outline=int(255-110*(1-i/R)**2))
mask=ImageChops.multiply(ImageChops.multiply(gut,band),vig)
im=Image.composite(im,Image.new("RGB",(front_w,H),NIGHT),mask)
canvas=Image.new("RGB",(W,H),NIGHT); canvas.paste(im,(front_x0,0))
canvas.save("cover_bg.jpg","JPEG",quality=94,optimize=True,dpi=(DPI,DPI))
json.dump([W,H], open("../indesign/coverbg_dims.json","w"))
print("pages=%d spine=%.3fin cover=%.3f x %.3f in  bg=%dx%d px (%.1f MB)"
      % (PAGES, SPINE/72, CW_PT/72, CH_PT/72, W, H, os.path.getsize("cover_bg.jpg")/1e6))
open("dims.txt","w").write("%.4f %.4f %.4f" % (CW_PT, CH_PT, SPINE))
