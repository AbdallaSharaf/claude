import json,sys; sys.path.insert(0,"..")
from kb import *
w=json.load(open("../collagen_words.json")); w[0][0]=0.66; T=lambda i:w[i][0]
chunks=[KB(("أنا متأكدة",[T(0),T(1)]),("كل يوم بتسمعي",[T(3),T(4),T(5)])),
        KB(("محفزات الكولاجين",[T(9),T(10)])),
        KB(("إمتى نستخدمها؟",[T(15),T(16)])),
        KB(("أنسب محفز",[T(93),T(94)]),("كولاجين لحالتك",[T(95),T(96)]))]
c1=card("لو وشك بدأ يظهر فيه",[("خطوط ابتسامة",T(24)),("ترهل في الجلد",T(27)),("ندبات حب شباب",T(33))],T(19)-PRE,T(41)-PRE-0.04,top=920)
O=17.22; C=24.95; K0=18.34; KC=[round(K0+x,3) for x in KEY]
c2=card("لو بدأ يظهر في رقبتك",[("خطوط عرضية",T(46)),("ترهل بسيط",T(49))],T(41)-PRE,O-0.06)
c3=card("الإيدين",[("تحسين جودة الجلد",T(76)),("حجم وامتلاء طبيعي",T(80))],T(74)-PRE,T(89)-PRE-0.04)
INS=ins(O,C,[{"icon":"belly","lines":[[o("البطن",17.30)]],"r":40},
             {"icon":"scale","dark":True,"lines":[[o("ترهل",T(55)),o("بعد",T(56)),o("فقدان",T(57)),o("الوزن",T(58))]],"r":75,"type":[KC[0:2],KC[2:4],KC[4:6],KC[6:8]]},
             {"icon":"stroller","lines":[[o("بعد",T(62)),o("الولادات",T(63)),o("المتكررة",T(64))]],"r":40},
             {"icon":"infoc","lines":[[o("بشرط",T(65)),o("ما تكونش",T(68))],[o("محتاجة",T(69)),o("تدخل",T(70)),o("جراحي",T(71))]],"r":40}],round(900+(1040-310-900)/0.66))
INS["items"][1]["lines"][0][0]["t"]=K0+0.12
insert={"start":O-0.05,"end":INS["end"],"hide":O,"drop_to":24.9}
TITLE=[{"text":"Collagen Biostimulators","t":T(11),"block":1,"below":1,"fit":1,"svg":'<svg width="60" height="60" viewBox="0 0 52 52" fill="none" stroke="#FAF2EC" stroke-width="2.8" stroke-linecap="round"><path d="M9 19 C17 11 25 27 33 19 S41 17 44 15"/><path d="M9 33 C17 25 25 41 33 33 S41 31 44 29"/><path d="M16 15 V37 M26 19 V39 M36 15 V35" stroke-dasharray="2 4.5"/></svg>'},
       {"text":"اسألينا","t":T(89),"block":3,"svg":'<svg width="56" height="56" viewBox="0 0 52 52" fill="none" stroke="#FAF2EC" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M44 9 L8 24 L22 29 L27 43 Z"/><path d="M22 29 L44 9"/></svg>'}]
N={"appear":5.35,"stretch":5.60,"split":5.85,"dr":6.05,"marwa":6.30,"magdy":6.55,"title":6.85,"exit":9.60}
cuts=[0,5.14,6.68,10.72,13.38,17.16,21.88,24.42,27.36,28.72,35.44]; lap=[1000,1000,1180,1000,1000,1170,1060,1000,1170,1060]
END={"start":33.70,"close":34.50,"dur":35.44}
data={"title":TITLE,"chunks":chunks,"devices":[c1,c2,c3],"cuts":cuts[1:-1],"lap":lap,"N":N,"END":END,"trans":[],"insert":insert,"minHold":0.0,"nameY":175}
fx=[sfx("photo insert.MP3",0.90),sfx("Hint , notification/info.MP3",T(11)),sfx("whoosh/light .MP3",5.0),sfx("pop/2.MP3",N["magdy"]),
 sfx("paper.MP3",T(19)),sfx("pop/1.mp4",T(24)),sfx("pop/3.MP3",T(27)),sfx("pop/4.MP3",T(33)),
 sfx("whoosh/hard paper turn.MP3",T(45)),sfx("Hint , notification/1.mp4",T(46)),
 sfx("whoosh/big.MP3",O+0.05),sfx("mouse click 1.MP3",17.42),sfx("keaboard.MP3",K0,(0.6,2.1,0.045)),
 sfx("camera shuter.MP3",T(62)),sfx("معلومة مهمة في اول اخر الفيديو مش هوك.MP3",T(65)),sfx("whoosh/fast paper.MP3",C+0.03),
 sfx("soft reveal/1.MP3",T(74)),sfx("Hint , notification/solid.MP3",T(89)),
 sfx("اصوات تنفع لبداية او نهاية الفيديو/whoosh with impact.MP3",END["close"])]
import os; os.chdir(".."); write("collagen",data,INS,fx); print("ok collagen")
