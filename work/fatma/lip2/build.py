import json,sys
sys.path.insert(0,".")
from helpers import *
PRE=3/25
w=json.load(open("../lip_words.json")); w[0][0]=0.44; w[10][2]="للشفايف؟"
GOLD=set()
def H(text,t,g=()):
    """a headline in clean wording: every word comes in together when she starts saying it"""
    return [{"w":x,"t":t,"e":t,"g":(k in g)} for k,x in enumerate(text.split(" "))]
def block(*rows):
    out=[]
    for ri,(text,t,g) in enumerate(rows):
        for o in H(text,t,g): o["r"]=ri; out.append(o)
    return out
T=lambda i:w[i][0]
chunks=[block(("Lip\u00a0Filler",T(5),(0,)),("مش مجرد تكبير شفايف",T(7),(2,))),
        block(("الأهم من نوع الفيلر",T(59),(3,))),
        block(("اختيار الدكتور المناسب",T(65),(1,2))),
        block(("نوع المادة والتكنيك",T(71),()),("المناسب لكل حالة",T(71),()))]
def card(title,rows,start,end,top=1000):
    L=[H(title,title_t,(0,1,2)) for title_t in [start+PRE]]
    for text,t in rows: L.append(H(text,t))
    return {"type":"list","start":round(start,3),"end":round(end,3),"top":top,"num":"","lines":L}
c2=card("تحسين الشكل",[("حالات الشفة الأرنبية",T(41)),("علاج الندبات",T(45))],T(38)-PRE,T(48)-PRE-0.04)
c3=card("مع تقدم العمر",[("تعويض حجم الشفايف",T(53)),("فرد الخطوط الرفيعة",T(56))],T(48)-PRE,T(59)-PRE-0.04)
o=lambda txt,t:{"w":txt,"t":t}
O=6.30; C=11.40
INS={"open":O,"close":C,"end":round(C+0.32,2),"ck":0.2,"cy1":0.18,"fa":0.2,"fb":0.3,"cy":900,"sc":0.66,"dx":50,"dy":310,"y0":round(900+(1090-1210)/0.66),"y1":round(900+(1090-1210)/0.66),
 "items":[{"icon":"check","lines":[[o("Lip Asymmetry",T(19))]],"r":40},
          {"icon":"check","dark":True,"lines":[[o("Gummy Smile",T(25))]],"r":75},
          {"icon":"mag","search":True,"lines":[[o("تراجع",T(27)),o("الشفة",T(28))]],"key":"⌘K","r":40},
          {"icon":"dot","lines":[[o("العلوية",T(29)),o("أو",T(29)),o("السفلية",T(29))]],"key":"↵","r":40}]}
json.dump(INS,open("ins.json","w"),ensure_ascii=False)
open("ins_page.html","w").write(open("../ins_items.html").read().replace("DATA",json.dumps(INS,ensure_ascii=False)))
devices=[c2,c3]
insert={"start":O-0.05,"end":INS["end"],"hide":O,"drop_to":20.0}
N={"appear":5.05,"stretch":5.30,"split":5.55,"dr":5.75,"marwa":6.00,"magdy":6.25,"title":6.55,"exit":8.40}
cuts=[0,4.08,6.24,8.24,11.04,16.32,20.44,23.56,27.52]; lap=[1270,1050,1270,1050,1270,1050,1270,1050]
END={"start":26.75,"close":27.45,"dur":27.52}
data={"chunks":chunks,"devices":devices,"cuts":cuts[1:-1],"lap":lap,"N":N,"END":END,"trans":[],"insert":insert,"minHold":0.0,"nameY":175}
json.dump(data,open("data.json","w"),ensure_ascii=False)
PK=json.load(open("/home/user/claude/sfx_library/saber_v2/peaks.json"))
def sfx(f,t,seg=None): return f"{f}@{t:.2f}@{PK[f] if not seg else seg[2]}"+(f"@{seg[0]}@{seg[1]}" if seg else "")
fx=[sfx("whoosh/light .MP3",0.90),sfx("معلومة مهمة في اول اخر الفيديو مش هوك.MP3",T(7)),sfx("pop/2.MP3",N["magdy"]),
 sfx("whoosh/big.MP3",O+0.05),sfx("mouse click 1.MP3",T(19)+0.12),sfx("camera shuter.MP3",T(25)),sfx("keaboard.MP3",T(27),(0.0,0.7,0.05)),
 sfx("Hint , notification/1.mp4",T(29)),sfx("whoosh/fast paper.MP3",C+0.03),
 sfx("paper.MP3",T(38)),sfx("pop/1.mp4",T(41)),sfx("pop/3.MP3",T(45)),
 sfx("whoosh/hard paper turn.MP3",T(48)),sfx("pop/4.MP3",T(53)),
 sfx("correct answer.MP3",T(65)),
 sfx("اصوات تنفع لبداية او نهاية الفيديو/whoosh with impact.MP3",END["close"])]
open("sfx.txt","w").write("\n".join(fx)+"\n")
print("devices",[(d["start"],d["end"]) for d in devices],"insert",O,C,INS["end"])
