import numpy as np,subprocess,math,os
from PIL import Image,ImageFilter
O,C=23.0,27.62; a,b=550,725; W,H=1080,1920
def spr(t,Ts):
    if t<=0: return 0
    z=0.82;w=4/(z*Ts);wd=w*math.sqrt(1-z*z); return 1-math.exp(-z*w*t)*(math.cos(wd*t)+(z*w/wd)*math.sin(wd*t))
def spx(t,Ts):
    if t<=0: return 0
    w=5.8/Ts; return 1-(1+w*t)*math.exp(-w*t)
dec=subprocess.Popen(["ffmpeg","-v","error","-ss",str(a/25),"-i","../pores.mp4","-frames:v",str(b-a),"-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","25","-i","-","-ss",str(a/25),"-t",str((b-a)/25),"-i","../pores.mp4","-map","0:v","-map","1:a","-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-shortest","/home/user/claude/output/fatma/pores_insert_preview.mp4"],stdin=subprocess.PIPE)
for i in range(a,b):
    fr=np.frombuffer(dec.stdout.read(W*H*3),np.uint8).reshape(H,W,3); t=i/25
    im=Image.fromarray(fr); v=max(0,min(1,spr(t-O,.35)*(1-spx(t-C,.42))))
    if v>0.01: im=im.filter(ImageFilter.GaussianBlur(14*v))
    im=im.convert("RGBA"); f=f"fi/f{i:04d}.png"
    if os.path.exists(f): im.alpha_composite(Image.open(f).convert("RGBA"))
    enc.stdin.write(im.convert("RGB").tobytes())
enc.stdin.close(); enc.wait()
