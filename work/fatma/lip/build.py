import json,sys
sys.path.insert(0,".")
from helpers import *
from helpers import _shift,_words
w=json.load(open("../lip_words.json"))
w[10][2]="للشفايف؟"
GOLD={6,9,16,19,25,27,39,43,46,55,58,66,67,76}
def W(i,txt=None,g=None): return {"w":txt or w[i][2],"t":w[i][0],"e":w[i][1],"g":(i in GOLD) if g is None else g}
def rows(bl): return [[dict(W(i),r=ri) for ri,(a,b) in enumerate(bl) for i in range(a,b)]]
chunks=[]
for bl in [[(0,2)],[(2,4),(4,7)],[(7,10),(10,11)],[(11,14)],
           [(32,35),(35,37)],
           [(47,50),(50,52)],
           [(59,61),(61,64)],[(64,66),(66,68)],[(68,71),(71,73)],[(73,75),(75,77)]]: chunks+=rows(bl)
devices=[
 {"type":"cmp","start":w[37][0]-0.15,"end":w[46][1]+1.0,"sections":[{"head":[W(37),W(38),W(39)],"traits":[]},{"head":[W(40),W(41),W(42),W(43)],"traits":[[W(44),W(45),W(46)]]}]},
 {"type":"pair","start":w[52][0]-0.15,"end":w[58][0]+1.0,"items":[{"num":"١","t":w[52][0],"words":[W(52),W(53),W(54),W(55)]},{"num":"٢","t":w[56][0],"words":[W(56),W(57),W(58)]}]}]
N={"appear":0.0,"stretch":0.30,"split":0.98,"dr":1.22,"marwa":1.74,"magdy":2.22,"title":2.80,"exit":5.15}
OPEN=5.70
insert={"start":OPEN-0.05,"end":12.6}
ins={"open":OPEN,"close":11.9,"cards":[
 {"x":160,"y":300,"w":760,"h":170,"t":w[14][0],"titles":[{"text":"في حالات كتيرة جدًا","y":40,"t":w[14][0],"wt":[w[i][0] for i in (14,15,16,17)],"size":56}]},
 {"x":160,"y":530,"w":760,"h":250,"t":w[19][0],"num":"١","titles":[{"text":"Lip Asymmetry","y":50,"t":w[19][0],"wt":[w[19][0]],"g":True,"size":56}],
   "subs":[{"text":"أو عدم تماثل الشفايف","y":150,"t":w[20][0],"wt":[w[i][0] for i in (20,21,22,23)]}]},
 {"x":160,"y":840,"w":760,"h":170,"t":w[24][0],"num":"٢","titles":[{"text":"أو Gummy Smile","y":45,"t":w[24][0],"wt":[w[24][0],w[25][0]],"size":56}]},
 {"x":160,"y":1070,"w":760,"h":250,"t":w[26][0],"num":"٣","titles":[{"text":"أو تراجع الشفة","y":50,"t":w[26][0],"wt":[w[i][0] for i in (26,27,28)],"g":True,"size":56}],
   "subs":[{"text":"العلوية أو السفلية","y":150,"t":w[29][0],"wt":[w[i][0] for i in (29,30,31)]}]}],
 "cam":[[0,540,880,1.0],[OPEN,540,420,1.25],[w[19][0]-0.3,540,660,1.22],[w[24][0]-0.3,540,900,1.22],[w[26][0]-0.3,540,1170,1.22],[11.4,540,810,0.92]],
 "ball":[[OPEN-0.05,None],[w[17][0],{"wd":[0,"t",0,3]}],[w[19][0],{"wd":[1,"t",0,0]}],[w[23][0],{"wd":[1,"s",0,3]}],[w[25][0],{"wd":[2,"t",0,1]}],[w[28][0],{"wd":[3,"t",0,2]}],[w[31][0],{"wd":[3,"s",0,2]}],[11.6,{"w":{"x":540,"y":810}}],[12.6,None]]}
devices_wait(chunks,devices,None); apply_holds(devices,None,insert,ins); insert_timing(ins,insert,chunks)
d0=devices[0]; st=round(insert["end"]+0.84,3)
if d0["start"]<st: d0["start"]=st; _shift(_words(d0),st+0.12); d0["end"]=round(max(o["t"] for o in _words(d0["sections"]))+1.0,3)
sec=d0["sections"]; t2=max(o["t"] for o in _words(sec[0]))+0.8
if sec[1]["head"][0]["t"]<t2: _shift(_words(sec[1]),t2)
d0["end"]=round(max(o["t"] for o in _words(d0["sections"]))+1.0,3)
cuts=[0,4.08,6.24,8.24,11.04,16.32,20.44,23.56,27.48]; lap=[1270,1050,1270,1050,1270,1050,1270,1050]
def lap_at(t): return lap[max(i for i,c in enumerate(cuts[:-1]) if c<=t)]
ins["ball"][0][1]={"s":{"x":540,"y":lap_at(ins["open"])+70}}; ins["ball"][-1][1]={"s":{"x":540,"y":lap_at(ins["close"])+70}}
END={"start":26.72,"close":27.40,"dur":27.52}
insert["hide"]=5.80; insert["drop_to"]=10.9
data={"chunks":chunks,"devices":devices,"cuts":cuts[1:-1],"lap":lap,"N":N,"END":END,"trans":[],"insert":insert}
json.dump(data,open("data.json","w"),ensure_ascii=False); json.dump(ins,open("ins.json","w"),ensure_ascii=False)
PK=json.load(open("/home/user/claude/sfx_library/saber_v2/peaks.json"))
def sfx(f,t): return f"{f}@{t:.2f}@{PK[f]}"
d0,d1=devices
fx=[sfx("soft reveal/1.MP3",N["split"]),sfx("pop/2.MP3",N["magdy"]),
 sfx("معلومة مهمة في اول اخر الفيديو مش هوك.MP3",w[7][0]),
 sfx("whoosh/big.MP3",ins["open"]+0.05),sfx("pop/1.mp4",max(w[19][0],ins["open"]+0.5)),sfx("Hint , notification/solid.MP3",w[25][0]),sfx("pop/3.MP3",w[26][0]),sfx("whoosh/light .MP3",ins["close"]+0.03),
 sfx("paper.MP3",d0["sections"][0]["head"][0]["t"]),sfx("pop/4.MP3",d0["sections"][1]["traits"][0][0]["t"]),
 sfx("Hint , notification/info.MP3",d1["items"][0]["words"][0]["t"]),sfx("Hint , notification/1.mp4",d1["items"][1]["words"][0]["t"]),
 sfx("correct answer.MP3",w[66][0]),
 sfx("اصوات تنفع لبداية او نهاية الفيديو/whoosh with impact.MP3",END["close"])]
open("sfx.txt","w").write("\n".join(fx)+"\n")
print("insert",insert,"open/close",ins["open"],ins["close"]); print("devices",[(d["type"],d["start"],d["end"]) for d in devices])
