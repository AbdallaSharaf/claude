import json,sys; sys.path.insert(0,"..")
from kb import *
w=json.load(open("../pores_words.json")); w[0][0]=0.53; T=lambda i:w[i][0]
chunks=[KB(("كلنا عندنا مسام",[T(0),T(1),T(2)]),("حاجة طبيعية جدًا",[T(6),T(7),T(8)])),
        KB(("فتحات الغدد الدهنية",[T(11),T(12),T(13)])),
        KB(("إيه الحل؟",[T(34),T(35)])),
        KB(("نتيجة أفضل",[T(56),T(57)])),
        KB(("ندمج بين الروتين",[T(70),T(71),T(72)]),("والجلسة المناسبة",[T(73),T(74)]),("لبشرتك",[T(75)]))]
c1=card("إمتى بتزيد وسع أكتر؟",[("الإفرازات الدهنية",T(23)),("عامل وراثي",T(27)),("البشرة الدهنية",T(31))],T(17)-PRE,T(34)-PRE-0.04)
c2=card("نظبط الروتين",[("غسول Salicylic Acid",T(40)),("مرطب مناسب",T(43)),("Niacinamide أو Retinol",T(49)),("حسب الحالة",T(52))],T(38)-PRE,T(56)-PRE-0.04,top=930)
O=22.70; C=26.95; K0=24.38; KC=[round(K0+x,3) for x in KEY[:6]]
INS=ins(O,C,[{"icon":"drop","lines":[[o("Skin Boosters",T(62))]],"r":40},
             {"icon":"syringe","dark":True,"lines":[[o("Mesobotox",T(63))]],"r":75},
             {"icon":"laser","lines":[[o("Fractional",T(64)),o("Laser",T(64))]],"r":40,"type":[KC[:4],KC[4:]]},
             {"icon":"pen","lines":[[o("Dermapen",T(65))]],"r":40},
             {"icon":"needles","lines":[[o("Microneedling RF",T(66))]],"r":40}],round(900+(1040-310-900)/0.66))
insert={"start":O-0.05,"end":INS["end"],"hide":O,"drop_to":27.0}
TITLE={"text":"المسام","t":T(0),"block":0,"svg":'<svg width="60" height="60" viewBox="0 0 52 52" fill="none" stroke="#FAF2EC" stroke-width="2.8" stroke-linecap="round"><circle cx="26" cy="26" r="17"/><circle cx="19" cy="21" r="2.2"/><circle cx="31" cy="20" r="2.6"/><circle cx="24" cy="31" r="2.8"/><circle cx="34" cy="31" r="2"/></svg>'}
N={"appear":6.18,"stretch":6.40,"split":6.65,"dr":6.85,"marwa":7.10,"magdy":7.35,"title":7.60,"exit":9.80}
cuts=[0,6.08,7.6,11.92,14.22,17.28,20.16,23.72,25.4,27.1,32.16]; lap=[1000,1000,1180,1000,1000,1150,1000,1160,1000,1020]
END={"start":31.25,"close":31.95,"dur":32.16}
data={"title":TITLE,"chunks":chunks,"devices":[c1,c2],"cuts":cuts[1:-1],"lap":lap,"N":N,"END":END,"trans":[],"insert":insert,"minHold":0.0,"nameY":175}
fx=[sfx("soft reveal/1.MP3",0.90),sfx("معلومة مهمة في اول اخر الفيديو مش هوك.MP3",T(7)),sfx("whoosh/fast paper.MP3",6.04),sfx("pop/2.MP3",N["magdy"]),
 sfx("Hint , notification/simble notification.MP3",T(17)),sfx("pop/1.mp4",T(23)),sfx("Hint , notification/solid.MP3",T(27)),
 sfx("Hint , notification/info.MP3",T(35)),sfx("paper.MP3",T(38)),sfx("pop/3.MP3",T(40)),sfx("pop/4.MP3",T(49)),
 sfx("whoosh/big.MP3",O+0.05),sfx("mouse click 1.MP3",T(62)+0.12),sfx("photo insert.MP3",T(63)),sfx("keaboard.MP3",K0,(0.6,1.55,0.045)),
 sfx("Hint , notification/1.mp4",T(65)),sfx("correct answer.MP3",T(66)),sfx("whoosh/light .MP3",C+0.03),
 sfx("اصوات تنفع لبداية او نهاية الفيديو/whoosh with impact.MP3",END["close"])]
import os; os.chdir(".."); write("pores",data,INS,fx); print("ok pores")
