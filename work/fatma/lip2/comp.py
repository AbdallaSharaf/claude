import numpy as np,subprocess,math,sys,os
from PIL import Image,ImageFilter,ImageEnhance
src,out=sys.argv[1],sys.argv[2]; N=688; fps=25; W,H=1080,1920; O,C=6.10,10.62
def spr(t,Ts):
    if t<=0: return 0
    z=0.82;w=4/(z*Ts);wd=w*math.sqrt(1-z*z); return 1-math.exp(-z*w*t)*(math.cos(wd*t)+(z*w/wd)*math.sin(wd*t))
def spx(t,Ts):
    if t<=0: return 0
    w=5.8/Ts; return 1-(1+w*t)*math.exp(-w*t)
dec=subprocess.Popen(["ffmpeg","-v","error","-i",src,"-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(fps),"-i","-","-c:v","libx264","-crf","16","-preset","medium","-pix_fmt","yuv420p",out],stdin=subprocess.PIPE)
last=None
for i in range(N):
    b=dec.stdout.read(W*H*3)
    if len(b)==W*H*3:
        fr=np.frombuffer(b,np.uint8).reshape(H,W,3)
        if last is None or fr[::40,::40].mean()>20: last=fr
    t=i/fps; z=1.0+0.035*(0.5-0.5*math.cos(2*math.pi*t/9.0)); im=Image.fromarray(last)
    if z>1.0005: im=im.transform((W,H),Image.AFFINE,(1/z,0,(W-W/z)/2,0,1/z,(H-H/z)*0.4),resample=Image.BICUBIC)
    v=max(0.0,min(1.0,spr(t-O,.35)*(1-spx(t-C,.42))))
    if v>0.01: im=ImageEnhance.Color(im.filter(ImageFilter.GaussianBlur(14*v))).enhance(1+0.12*v)
    im=im.convert("RGBA")
    if v>0.01: im.alpha_composite(Image.new("RGBA",im.size,(58,18,25,int(46*v))))
    for d in ("fr","fi"):
        f=f"{d}/f{i:04d}.png"
        if os.path.exists(f): im.alpha_composite(Image.open(f).convert("RGBA"))
    enc.stdin.write(im.convert("RGB").tobytes())
enc.stdin.close(); enc.wait()
