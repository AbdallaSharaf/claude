import json,sys
sys.path.insert(0,".")
from helpers import *
from helpers import _shift,_words
PRE=3/25
w=json.load(open("../collagen_words.json")); w[0][0]=0.66
GOLD={9,10,11,15,25,27,33,47,49,58,63,71,77,81,89,93,95}
def W(i,g=None): return {"w":w[i][2],"t":w[i][0],"e":w[i][1],"g":(i in GOLD) if g is None else g}
def rows(bl): return [[dict(W(i),r=ri) for ri,(a,b) in enumerate(bl) for i in range(a,b)]]
chunks=[]
for bl in [[(0,2),(2,5)],[(5,8),(8,12)],[(12,15),(15,17)],[(83,85),(85,89)],[(89,92),(92,97)]]: chunks+=rows(bl)
def lst(title,rws,num,end_word):
    return {"type":"list","start":round(w[title[0]][0]-PRE,3),"end":round(w[end_word][0]-PRE-0.04,3),"top":1000,"num":num,
            "lines":[[W(i) for i in range(*title)]]+[[W(i) for i in range(a,b)] for a,b in rws]}
face=lst((17,24),[(24,26),(26,30),(30,36),(36,39)],"١",39)
neck=lst((39,46),[(46,48),(48,51)],"٢",51)
hands=lst((74,75),[(75,79),(79,83)],"٤",83)
hands["start"]=round(w[74][0]-PRE,3)
neck["end"]=16.95
# belly insert (UI stack)
o=lambda i:{"w":w[i][2],"t":w[i][0]}
O=16.98; C=24.25
INS={"open":O,"close":C,"end":round(C+0.55,2),"cy":900,"sc":0.66,"dx":50,"dy":310,"y0":round(900+(1040-310-900)/0.66),"y1":round(900+(1040-310-900)/0.66),
 "items":[{"icon":"num","num":"٣","lines":[[o(51),o(52)]],"r":40},
          {"icon":"check","dark":True,"lines":[[o(53),o(54),o(55)]],"r":75},
          {"icon":"mag","search":True,"lines":[[o(i) for i in range(56,61)]],"key":"⌘K","r":40},
          {"icon":"dot","lines":[[o(i) for i in range(61,65)]],"key":"↵","r":40},
          {"icon":"info","lines":[[o(i) for i in range(65,69)],[o(i) for i in range(69,72)]],"r":40}]}
json.dump(INS,open("ins.json","w"),ensure_ascii=False)
open("ins_page.html","w").write(open("../ins_items.html").read().replace("DATA",json.dumps(INS,ensure_ascii=False)))
devices=[face,neck,hands]
insert={"start":O-0.05,"end":INS["end"],"hide":O,"drop_to":24.5}
N={"appear":5.35,"stretch":5.60,"split":5.85,"dr":6.05,"marwa":6.30,"magdy":6.55,"title":6.85,"exit":9.60}
cuts=[0,5.14,6.68,10.72,13.38,17.16,21.88,24.42,27.36,28.72,35.44]; lap=[1000,1000,1180,1000,1000,1170,1060,1000,1170,1060]
END={"start":33.70,"close":34.50,"dur":35.44}
data={"chunks":chunks,"devices":devices,"cuts":cuts[1:-1],"lap":lap,"N":N,"END":END,"trans":[],"insert":insert,"minHold":0.0,"nameY":175}
json.dump(data,open("data.json","w"),ensure_ascii=False)
PK=json.load(open("/home/user/claude/sfx_library/saber_v2/peaks.json"))
def sfx(f,t,seg=None): return f"{f}@{t:.2f}@{PK[f] if not seg else seg[2]}"+(f"@{seg[0]}@{seg[1]}" if seg else "")
fx=[sfx("photo insert.MP3",0.90),sfx("Hint , notification/info.MP3",w[9][0]),sfx("whoosh/light .MP3",5.0),sfx("pop/2.MP3",N["magdy"]),
 sfx("paper.MP3",w[17][0]),sfx("pop/1.mp4",w[24][0]),sfx("pop/3.MP3",w[27][0]),sfx("pop/4.MP3",w[33][0]),
 sfx("whoosh/hard paper turn.MP3",w[39][0]),sfx("Hint , notification/1.mp4",w[46][0]),
 sfx("whoosh/big.MP3",O+0.05),sfx("mouse click 1.MP3",w[51][0]+0.12),sfx("camera shuter.MP3",w[53][0]),sfx("keaboard.MP3",w[56][0],(0.0,1.4,0.05)),
 sfx("Hint , notification/simble notification.MP3",w[61][0]),sfx("معلومة مهمة في اول اخر الفيديو مش هوك.MP3",w[65][0]),sfx("whoosh/fast paper.MP3",C+0.03),
 sfx("soft reveal/1.MP3",w[74][0]),sfx("Hint , notification/solid.MP3",w[89][0]),
 sfx("اصوات تنفع لبداية او نهاية الفيديو/whoosh with impact.MP3",END["close"])]
open("sfx.txt","w").write("\n".join(fx)+"\n")
print("devices",[(d["type"],d["num"],d["start"],d["end"]) for d in devices],"insert",O,C)
