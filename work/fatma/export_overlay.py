"""transparent overlay (captions + cards + insert + name + ending + Saber Group credit) as ProRes 4444 with alpha,
and an effects-only WAV the same length as the video. usage: export_overlay.py <dir> <src.mp4> <N> <name>"""
import sys,os,subprocess,runpy,numpy as np
from PIL import Image
d,src,N,name=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]; PM="--premult" in sys.argv
OUT="/home/user/claude/output/fatma/overlay"; W,H,fps=1080,1920,25
sys.argv=["sg_intro.py","x.mp4","y.mp4","--fps","25","--fonts","/home/user/claude/.claude/skills/montage/fonts"]
sg=runpy.run_path("/home/user/claude/.claude/skills/marwa-brown-close/scripts/sg_intro.py",run_name="sg")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgba","-s",f"{W}x{H}","-r",str(fps),"-i","-",
    "-c:v","prores_ks","-profile:v","4444","-pix_fmt","yuva444p10le","-vendor","apl0",f"{OUT}/{name}_overlay"+("_capcut" if PM else "")+".mov"],stdin=subprocess.PIPE)
for i in range(N):
    im=Image.new("RGBA",(W,H),(0,0,0,0))
    for sub in ("fr","fi"):
        f=f"{d}/{sub}/f{i:04d}.png"
        if os.path.exists(f): im.alpha_composite(Image.open(f).convert("RGBA"))
    t=i/fps
    if t<sg["OUT_T"]: sg["draw"](im,t)
    if PM:   # CapCut reads alpha as premultiplied: colour = colour x alpha
        a=np.asarray(im,np.float32); a[...,:3]*=a[...,3:4]/255.0; enc.stdin.write(np.round(a).astype(np.uint8).tobytes())
    else: enc.stdin.write(im.tobytes())
enc.stdin.close(); enc.wait()
if PM: sys.exit()
# effects only = final mix minus her voice (same samples, same length as the video)
m=np.fromfile(f"{d}/mix.f32",np.float32).reshape(-1,2)
v=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",src,"-ac","2","-ar","48000","-f","f32le","-"],capture_output=True).stdout,np.float32).reshape(-1,2)
v=np.concatenate([v,np.zeros((max(0,len(m)-len(v)),2),np.float32)])[:len(m)]
fx=(m-v); n=int(round(N/fps*48000)); fx=np.concatenate([fx,np.zeros((max(0,n-len(fx)),2),np.float32)])[:n]
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar","48000","-ac","2","-i","-","-c:a","pcm_s24le",f"{OUT}/{name}_sfx.wav"],input=fx.astype(np.float32).tobytes(),check=True)
print(name,"peak fx",round(float(np.abs(fx).max()),3))
