"""lower only the effects where voice+effects would clip; her samples are never changed"""
import numpy as np,subprocess,sys
src,mixf=sys.argv[1],sys.argv[2]
m=np.fromfile(mixf,np.float32).reshape(-1,2)
v=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",src,"-ac","2","-ar","48000","-f","f32le","-"],capture_output=True).stdout,np.float32).reshape(-1,2)
v=np.concatenate([v,np.zeros((max(0,len(m)-len(v)),2),np.float32)])[:len(m)]
s=m-v; lim=0.98
need=np.ones(len(m),np.float32)
a=np.abs(s).max(1)+1e-9; room=np.clip(lim-np.abs(v).max(1),0,None)
g=np.minimum(1.0,room/a); g[np.abs(s).max(1)<1e-6]=1.0
# smooth: gain can only drop, released over 30 ms
w=1440; gs=np.minimum.accumulate(g[::-1])[::-1] if False else g
k=np.ones(w)/w; gs=np.minimum(g,np.convolve(np.minimum(g,1),k,mode="same"))
for _ in range(2): gs=np.minimum(gs,np.convolve(gs,k,mode="same"))
out=v+s*gs[:,None]
print("before",round(float(np.abs(m).max()),3),"after",round(float(np.abs(out).max()),3),"voice",round(float(np.abs(v).max()),3))
out.astype(np.float32).tofile(mixf)
