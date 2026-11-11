import json,sys
sys.path.insert(0,".")
from helpers import *
from helpers import _shift,_words
w=json.load(open("../pores_words.json"))
GOLD={7,12,13,19,20,23,24,27,28,35,39,42,49,51,57,70,75}
def W(i,txt=None,g=None): return {"w":txt or w[i][2],"t":w[i][0],"e":w[i][1],"g":(i in GOLD) if g is None else g}
def rows(bl): return [[dict(W(i),r=ri) for ri,(a,b) in enumerate(bl) for i in range(a,b)]]
chunks=[]
for bl in [[(0,3),(3,5)],[(5,7),(7,9)],[(9,11),(11,14)],[(14,16)],[(16,19),(19,21)],
           [(29,31),(31,33)],[(33,36)],
           [(54,56),(56,58)],
           [(69,72),(72,74)],[(74,76)]]: chunks+=rows(bl)
cnt={"type":"counter","start":w[21][0]-0.15,"end":w[28][0]+1.0,"items":[
  {"num":"١","t":w[21][0],"words":[W(21),W(22)]},{"num":"١","t":w[23][0],"words":[W(23),W(24)]},
  {"num":"٢","t":w[25][0],"words":[W(25),W(26)]},{"num":"٢","t":w[27][0],"words":[W(27),W(28)]}]}
items=[(38,40),(40,43),(43,45),(45,47),(47,49),(49,52),(52,54)]
num={"type":"num","start":w[36][0]-0.15,"end":w[53][0]+1.0,"num":"١","ringT":w[36][0],"title":[W(36),W(37)],
     "items":[{"t":w[a][0],"words":[W(i) for i in range(a,b)]} for a,b in items]}
for k in range(1,len(num["items"])):
    pl=max(o["t"] for o in num["items"][k-1]["words"]); t0=max(num["items"][k]["t"],pl+0.8)
    num["items"][k]["t"]=round(t0,3); _shift(num["items"][k]["words"],t0)
num["end"]=round(max(o["t"] for o in _words(num["items"]))+1.0,3)
devices=[cnt,num]
devices_wait(chunks,devices,None); apply_holds(devices,None,None,None)
if num["start"]<13.06: num["start"]=13.06; _shift(_words(num["items"])+num["title"],13.18)
num["end"]=round(max(o["t"] for o in _words(num["items"]))+1.0,3)
INS=json.load(open("ins_stack.json"))
insert={"start":INS["open"]-0.05,"end":INS["end"],"hide":INS["open"],"drop_to":27.0}
N={"appear":0.0,"stretch":0.30,"split":0.68,"dr":1.02,"marwa":1.48,"magdy":1.86,"title":2.48,"exit":5.55}
cuts=[0,6.08,7.6,11.92,14.22,17.28,20.16,23.72,25.4,27.1,32.16]; lap=[1000,1000,1180,1000,1000,1150,1000,1160,1000,1020]
END={"start":31.10,"close":31.90,"dur":32.16}
data={"chunks":chunks,"devices":devices,"cuts":cuts[1:-1],"lap":lap,"N":N,"END":END,"trans":[],"insert":insert}
json.dump(data,open("data.json","w"),ensure_ascii=False)
PK=json.load(open("/home/user/claude/sfx_library/saber_v2/peaks.json"))
def sfx(f,t,seg=None): return f"{f}@{t:.2f}@{PK[f] if not seg else seg[2]}"+(f"@{seg[0]}@{seg[1]}" if seg else "")
it=INS["items"]
fx=[sfx("soft reveal/1.MP3",N["split"]),sfx("pop/2.MP3",N["magdy"]),
 sfx("Hint , notification/simble notification.MP3",w[17][0]),
 sfx("pop/1.mp4",cnt["items"][0]["words"][0]["t"]),sfx("Hint , notification/solid.MP3",cnt["items"][2]["words"][0]["t"]),
 sfx("Hint , notification/info.MP3",w[35][0]),
 sfx("paper.MP3",num["start"]+0.12),sfx("pop/3.MP3",num["items"][1]["words"][2]["t"]),sfx("pop/4.MP3",num["items"][5]["t"]),
 sfx("whoosh/big.MP3",INS["open"]+0.05),sfx("mouse click 1.MP3",it[0]["t"]+0.12),sfx("photo insert.MP3",it[1]["t"]),
 sfx("keaboard.MP3",it[2]["t"],(0.0,0.75,0.05)),sfx("Hint , notification/1.mp4",it[3]["t"]),sfx("correct answer.MP3",it[4]["t"]),sfx("whoosh/light .MP3",INS["close"]+0.03),
 sfx("اصوات تنفع لبداية او نهاية الفيديو/whoosh with impact.MP3",END["close"])]
open("sfx.txt","w").write("\n".join(fx)+"\n")
print("devices",[(d["type"],d["start"],d["end"]) for d in devices]); print("\n".join(fx))
