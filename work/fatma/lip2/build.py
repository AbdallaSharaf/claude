import json,sys
sys.path.insert(0,".")
from helpers import *
PRE=3/25
w=json.load(open("../lip_words.json")); w[0][0]=0.44; w[10][2]="للشفايف؟"
GOLD={6,9,16,38,39,43,46,53,55,58,66,67,76}
def W(i,g=None): return {"w":w[i][2],"t":w[i][0],"e":w[i][1],"g":(i in GOLD) if g is None else g}
def rows(bl): return [[dict(W(i),r=ri) for ri,R in enumerate(bl) for i in R]]
chunks=[]
for bl in [[[0,1]],[[5,6],[7,8,9,10]],[[15,16]],[[61,62,63]],[[66,67]],[[70,71,72],[73,74,75,76]]]: chunks+=rows(bl)
def lst(title,rws,num,start,end,top=900):
    L=[[W(i) for i in title]]
    for R in rws:
        hdr=R[0]=="h"; idx=R[1:] if hdr else R; row=[W(i) for i in idx]
        if hdr: row[0]["hdr"]=1
        L.append(row)
    return {"type":"list","start":round(start,3),"end":round(end,3),"top":top,"num":num,"lines":L}
o=lambda i:{"w":w[i][2],"t":w[i][0]}
O=6.36; C=11.60
INS={"open":O,"close":C,"end":round(C+0.32,2),"ck":0.2,"cy1":0.18,"fa":0.2,"fb":0.3,"cy":900,"sc":0.66,"dx":50,"dy":310,"y0":round(900+(1090-1210)/0.66),"y1":round(900+(1090-1210)/0.66),
 "items":[{"icon":"check","lines":[[o(19)],[o(20),o(21),o(22),o(23)]],"r":40},
          {"icon":"check","dark":True,"lines":[[o(24),o(25)]],"r":75},
          {"icon":"mag","search":True,"lines":[[o(26),o(27),o(28)]],"key":"⌘K","r":40},
          {"icon":"dot","lines":[[o(29),o(30),o(31)]],"key":"↵","r":40}]}
json.dump(INS,open("ins.json","w"),ensure_ascii=False)
open("ins_page.html","w").write(open("../ins_items.html").read().replace("DATA",json.dumps(INS,ensure_ascii=False)))
card=lst([38,39],[[42,43],[45,46],["h",47,48,49],[53,54,55],[56,57,58]],"",w[38][0]-PRE,w[61][0]-PRE-0.04)
devices=[card]
insert={"start":O-0.05,"end":INS["end"],"hide":O,"drop_to":12.5}
N={"appear":5.05,"stretch":5.30,"split":5.55,"dr":5.75,"marwa":6.00,"magdy":6.25,"title":6.55,"exit":8.40}
cuts=[0,4.08,6.24,8.24,11.04,16.32,20.44,23.56,27.52]; lap=[1270,1050,1270,1050,1270,1050,1270,1050]
END={"start":26.75,"close":27.45,"dur":27.52}
data={"chunks":chunks,"devices":devices,"cuts":cuts[1:-1],"lap":lap,"N":N,"END":END,"trans":[],"insert":insert,"minHold":0.0,"nameY":175}
json.dump(data,open("data.json","w"),ensure_ascii=False)
PK=json.load(open("/home/user/claude/sfx_library/saber_v2/peaks.json"))
def sfx(f,t,seg=None): return f"{f}@{t:.2f}@{PK[f] if not seg else seg[2]}"+(f"@{seg[0]}@{seg[1]}" if seg else "")
fx=[sfx("whoosh/light .MP3",0.90),sfx("معلومة مهمة في اول اخر الفيديو مش هوك.MP3",w[7][0]),sfx("pop/2.MP3",N["magdy"]),
 sfx("whoosh/big.MP3",O+0.05),sfx("mouse click 1.MP3",w[19][0]+0.12),sfx("camera shuter.MP3",w[24][0]),sfx("keaboard.MP3",w[26][0],(0.0,0.7,0.05)),
 sfx("Hint , notification/1.mp4",w[29][0]),sfx("whoosh/fast paper.MP3",C+0.03),
 sfx("paper.MP3",w[38][0]),sfx("pop/1.mp4",w[41][0]),sfx("pop/3.MP3",w[45][0]),
 sfx("whoosh/hard paper turn.MP3",w[47][0]),sfx("pop/4.MP3",w[53][0]),
 sfx("correct answer.MP3",w[66][0]),
 sfx("اصوات تنفع لبداية او نهاية الفيديو/whoosh with impact.MP3",END["close"])]
open("sfx.txt","w").write("\n".join(fx)+"\n")
print("devices",[(d["start"],d["end"]) for d in devices],"insert",O,C,INS["end"])
