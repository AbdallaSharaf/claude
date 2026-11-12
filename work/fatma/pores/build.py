import json,sys
sys.path.insert(0,".")
from helpers import *
from helpers import _shift,_words
w=json.load(open("../pores_words.json")); w[0][0]=0.53
GOLD={7,12,13,19,20,23,24,27,28,35,39,42,49,51,57,70,75}
def W(i,txt=None,g=None): return {"w":txt or w[i][2],"t":w[i][0],"e":w[i][1],"g":(i in GOLD) if g is None else g}
def rows(bl): return [[dict(W(i),r=ri) for ri,R in enumerate(bl) for i in R]]
chunks=[]
for bl in [[[0,1,2]],[[6,7,8]],[[11,12,13]],[[17,18],[19,20]],[[31,32]],[[35]],[[56,57]],[[70,71,72],[73,74,75]]]: chunks+=rows(bl)
cnt={"type":"counter","start":round(w[23][0]-PRE,3),"end":round(w[31][0]-PRE-0.04,3),"items":[
  {"num":"١","t":w[23][0],"words":[W(23),W(24)]},{"num":"٢","t":w[27][0],"words":[W(27),W(28)]}]}
lst={"type":"list","start":round(w[38][0]-PRE,3),"end":round(w[56][0]-PRE-0.04,3),"top":1000,"num":"١",
     "lines":[[W(38),W(39)],[W(40),W(42)],[W(43),W(44)],[W(49),W(50),W(51)],[W(52),W(53)]]}
devices=[cnt,lst]
INS=json.load(open("ins_stack.json"))
insert={"start":INS["open"]-0.05,"end":INS["end"],"hide":INS["open"],"drop_to":27.0}
N={"appear":6.18,"stretch":6.40,"split":6.65,"dr":6.85,"marwa":7.10,"magdy":7.35,"title":7.60,"exit":9.80}
cuts=[0,6.08,7.6,11.92,14.22,17.28,20.16,23.72,25.4,27.1,32.16]; lap=[1000,1000,1180,1000,1000,1150,1000,1160,1000,1020]
END={"start":31.25,"close":31.95,"dur":32.16}
MINHOLD=0.35
data={"chunks":chunks,"devices":devices,"cuts":cuts[1:-1],"lap":lap,"N":N,"END":END,"trans":[],"insert":insert,"minHold":0.0,"nameY":175}
json.dump(data,open("data.json","w"),ensure_ascii=False)
PK=json.load(open("/home/user/claude/sfx_library/saber_v2/peaks.json"))
def sfx(f,t,seg=None): return f"{f}@{t:.2f}@{PK[f] if not seg else seg[2]}"+(f"@{seg[0]}@{seg[1]}" if seg else "")
it=INS["items"]
fx=[sfx("soft reveal/1.MP3",0.90),sfx("معلومة مهمة في اول اخر الفيديو مش هوك.MP3",w[7][0]),sfx("whoosh/fast paper.MP3",6.04),sfx("pop/2.MP3",N["magdy"]),
 sfx("Hint , notification/simble notification.MP3",w[17][0]),
 sfx("pop/1.mp4",cnt["items"][0]["words"][0]["t"]),sfx("Hint , notification/solid.MP3",cnt["items"][1]["words"][0]["t"]),
 sfx("Hint , notification/info.MP3",w[35][0]),
 sfx("paper.MP3",w[38][0]),sfx("pop/3.MP3",w[40][0]),sfx("pop/4.MP3",w[49][0]),
 sfx("whoosh/big.MP3",INS["open"]+0.05),sfx("mouse click 1.MP3",it[0]["t"]+0.12),sfx("photo insert.MP3",it[1]["t"]),
 sfx("keaboard.MP3",it[2]["t"],(0.0,0.75,0.05)),sfx("Hint , notification/1.mp4",it[3]["t"]),sfx("correct answer.MP3",it[4]["t"]),sfx("whoosh/light .MP3",INS["close"]+0.03),
 sfx("اصوات تنفع لبداية او نهاية الفيديو/whoosh with impact.MP3",END["close"])]
open("sfx.txt","w").write("\n".join(fx)+"\n")
print("devices",[(d["type"],d["start"],d["end"]) for d in devices]); print("\n".join(fx))
