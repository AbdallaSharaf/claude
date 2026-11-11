import numpy as np,subprocess,json,sys
n=sys.argv[1]
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f"{n}.mp4","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
hop=160; e=np.sqrt((a[:len(a)//hop*hop].reshape(-1,hop)**2).mean(1)); db=20*np.log10(e+1e-9)
thr=np.percentile(db,30)+12; sp=db>thr
# pauses >= 0.12 s
P=[]; i=0
while i<len(sp):
    if not sp[i]:
        j=i
        while j<len(sp) and not sp[j]: j+=1
        if (j-i)>=12: P.append((round(i*0.01,2),round(j*0.01,2)))
        i=j
    else: i+=1
w=json.load(open(f"{n}_words.json"))
# snap: a word that starts inside a pause starts when the voice comes back
for x in w:
    for a0,b0 in P:
        if a0-0.02<=x[0]<b0 and b0-x[0]<0.7: x[0]=b0
json.dump(w,open(f"{n}_words_snap.json","w"),ensure_ascii=False)
json.dump(P,open(f"{n}_pauses.json","w"))
# word followed by a pause
out=[]
for k,x in enumerate(w):
    nxt=w[k+1][0] if k+1<len(w) else 99
    gap=max([b0-a0 for a0,b0 in P if a0>=x[0] and b0<=nxt+0.05]+[0])
    out.append(f"{k}:{x[2]}" + (f" ‖{gap:.2f}" if gap>=0.12 else ""))
print(" ".join(out))
